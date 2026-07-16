"""
Router de API para el recurso EstadoTarea.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ...domain.entities import EstadoTarea
from ...domain.ports import EstadoTareaRepository
from ...infrastructure.persistence import EstadoTareaRepositoryAdapter

router = APIRouter(prefix="/estados-tarea", tags=["estados-tarea"])


def get_estado_tarea_repository() -> EstadoTareaRepository:
    return EstadoTareaRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_estado_tarea(
    nombre: str,
    repository: EstadoTareaRepository = Depends(get_estado_tarea_repository)
) -> dict:
    try:
        estado = EstadoTarea(nombre=nombre)
        saved = repository.add(estado)
        return {"id": str(saved.id), "nombre": saved.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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


@router.put("/{estado_id}", response_model=dict)
async def update_estado_tarea(
    estado_id: UUID,
    nombre: str,
    repository: EstadoTareaRepository = Depends(get_estado_tarea_repository)
) -> dict:
    estado = repository.get_by_id(estado_id)
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado de tarea no encontrado")
    
    try:
        estado.nombre = nombre
        updated = repository.update(estado)
        return {"id": str(updated.id), "nombre": updated.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{estado_id}", status_code=204)
async def delete_estado_tarea(
    estado_id: UUID,
    repository: EstadoTareaRepository = Depends(get_estado_tarea_repository)
) -> None:
    estado = repository.get_by_id(estado_id)
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado de tarea no encontrado")
    repository.delete(estado_id)