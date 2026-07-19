"""
Router de API para el recurso EstadoTarea.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import EstadoTarea
from ....domain.ports import EstadoTareaRepository
from ....infrastructure.persistence import EstadoTareaRepositoryAdapter

router = APIRouter(prefix="/estados-tarea", tags=["estados-tarea"])


def get_estado_tarea_repository() -> EstadoTareaRepository:
    return EstadoTareaRepositoryAdapter()


@router.get("/", response_model=List[dict])
async def list_estados_tarea(
    repository: EstadoTareaRepository = Depends(get_estado_tarea_repository)
) -> List[dict]:
    estados = repository.get_all()
    return [{"id": str(e.id), "nombre": e.nombre} for e in estados]


@router.get("/{estado_id}", response_model=dict)
async def get_estado_tarea(
    estado_id: UUID,
    repository: EstadoTareaRepository = Depends(get_estado_tarea_repository)
) -> dict:
    estado = repository.get_by_id(estado_id)
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado de tarea no encontrado")
    return {"id": str(estado.id), "nombre": estado.nombre}