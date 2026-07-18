"""
Router de API para el recurso Área.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import Area
from ....domain.ports import AreaRepository
from ....infrastructure.persistence import AreaRepositoryAdapter

router = APIRouter(prefix="/areas", tags=["areas"])


def get_area_repository() -> AreaRepository:
    """Factory para obtener el repositorio de áreas."""
    return AreaRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_area(
    nombre: str,
    repository: AreaRepository = Depends(get_area_repository)
) -> dict:
    """Crea un nuevo área."""
    try:
        area = Area(nombre=nombre)
        saved = repository.add(area)
        return {"id": str(saved.id), "nombre": saved.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_areas(
    repository: AreaRepository = Depends(get_area_repository)
) -> List[dict]:
    """Lista todas las áreas."""
    areas = repository.get_all()
    return [{"id": str(a.id), "nombre": a.nombre} for a in areas]


@router.get("/{area_id}", response_model=dict)
async def get_area(
    area_id: UUID,
    repository: AreaRepository = Depends(get_area_repository)
) -> dict:
    """Obtiene un área por ID."""
    area = repository.get_by_id(area_id)
    if area is None:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return {"id": str(area.id), "nombre": area.nombre}


@router.put("/{area_id}", response_model=dict)
async def update_area(
    area_id: UUID,
    nombre: str,
    repository: AreaRepository = Depends(get_area_repository)
) -> dict:
    """Actualiza un área existente."""
    area = repository.get_by_id(area_id)
    if area is None:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    
    try:
        area.nombre = nombre
        updated = repository.update(area)
        return {"id": str(updated.id), "nombre": updated.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{area_id}", status_code=204)
async def delete_area(
    area_id: UUID,
    repository: AreaRepository = Depends(get_area_repository)
) -> None:
    """Elimina un área."""
    area = repository.get_by_id(area_id)
    if area is None:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    repository.delete(area_id)