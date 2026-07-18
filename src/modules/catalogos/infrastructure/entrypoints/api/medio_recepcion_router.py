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
        return {"id": str(saved.id), "nombre": saved.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_medios_recepcion(
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> List[dict]:
    medios = repository.get_all()
    return [{"id": str(m.id), "nombre": m.nombre} for m in medios]


@router.get("/{medio_id}", response_model=dict)
async def get_medio_recepcion(
    medio_id: UUID,
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> dict:
    medio = repository.get_by_id(medio_id)
    if medio is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    return {"id": str(medio.id), "nombre": medio.nombre}


@router.put("/{medio_id}", response_model=dict)
async def update_medio_recepcion(
    medio_id: UUID,
    nombre: str,
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> dict:
    medio = repository.get_by_id(medio_id)
    if medio is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    
    try:
        medio.nombre = nombre
        updated = repository.update(medio)
        return {"id": str(updated.id), "nombre": updated.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{medio_id}", status_code=204)
async def delete_medio_recepcion(
    medio_id: UUID,
    repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository)
) -> None:
    medio = repository.get_by_id(medio_id)
    if medio is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    repository.delete(medio_id)