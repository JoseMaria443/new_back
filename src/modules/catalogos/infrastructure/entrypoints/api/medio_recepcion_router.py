"""
Router de API para el recurso MedioRecepcion.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import MedioRecepcion
from ....domain.ports import MedioRecepcionRepository
from ....infrastructure.persistence import MedioRecepcionRepositoryAdapter

router = APIRouter(prefix="/medios-recepcion", tags=["medios-recepcion"])


def get_medio_recepcion_repository() -> MedioRecepcionRepository:
    return MedioRecepcionRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_medio_recepcion(
    nombre: str,
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> dict:
    try:
        medio = MedioRecepcion(nombre=nombre)
        saved = repository.add(medio)
        return {"id": str(saved.id), "nombre": saved.nombre, "archivado": saved.archivado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[dict])
async def list_medios_recepcion_activos(
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> List[dict]:
    """Lista solo los medios de recepción activos (no archivados). Para dropdowns/checkboxes."""
    medios = repository.get_activos()
    return [{"id": str(m.id), "nombre": m.nombre, "archivado": m.archivado} for m in medios]


@router.get("/todos", response_model=List[dict])
async def list_medios_recepcion_todos(
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> List[dict]:
    """Lista TODOS los medios de recepción (activos y archivados). Solo para vista de Configuración."""
    medios = repository.get_all()
    return [{"id": str(m.id), "nombre": m.nombre, "archivado": m.archivado} for m in medios]


@router.get("/{medio_id}", response_model=dict)
async def get_medio_recepcion(
    medio_id: UUID,
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> dict:
    medio = repository.get_by_id(medio_id)
    if medio is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    return {"id": str(medio.id), "nombre": medio.nombre, "archivado": medio.archivado}


@router.patch("/{medio_id}/archivar", response_model=dict)
async def archivar_medio_recepcion(
    medio_id: UUID,
    archivado: bool,
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> dict:
    """Archiva (True) o desarchiva (False) un medio de recepción."""
    medio = repository.get_by_id(medio_id)
    if medio is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    
    updated = repository.set_archivado(medio_id, archivado)
    return {"id": str(updated.id), "nombre": updated.nombre, "archivado": updated.archivado}