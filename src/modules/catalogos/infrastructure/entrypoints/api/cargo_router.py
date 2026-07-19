"""
Router de API para el recurso Cargo.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import Cargo
from ....domain.ports import CargoRepository
from ....infrastructure.persistence import CargoRepositoryAdapter

router = APIRouter(prefix="/cargos", tags=["cargos"])


def get_cargo_repository() -> CargoRepository:
    return CargoRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_cargo(
    nombre: str,
    repository: CargoRepository = Depends(get_cargo_repository)
) -> dict:
    try:
        cargo = Cargo(nombre=nombre)
        saved = repository.add(cargo)
        return {"id": str(saved.id), "nombre": saved.nombre, "archivado": saved.archivado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[dict])
async def list_cargos_activos(
    repository: CargoRepository = Depends(get_cargo_repository)
) -> List[dict]:
    """Lista solo los cargos activos (no archivados). Para dropdowns/checkboxes."""
    cargos = repository.get_activos()
    return [{"id": str(c.id), "nombre": c.nombre, "archivado": c.archivado} for c in cargos]


@router.get("/todos", response_model=List[dict])
async def list_cargos_todos(
    repository: CargoRepository = Depends(get_cargo_repository)
) -> List[dict]:
    """Lista TODOS los cargos (activos y archivados). Solo para vista de Configuración."""
    cargos = repository.get_all()
    return [{"id": str(c.id), "nombre": c.nombre, "archivado": c.archivado} for c in cargos]


@router.get("/{cargo_id}", response_model=dict)
async def get_cargo(
    cargo_id: UUID,
    repository: CargoRepository = Depends(get_cargo_repository)
) -> dict:
    cargo = repository.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return {"id": str(cargo.id), "nombre": cargo.nombre, "archivado": cargo.archivado}


@router.patch("/{cargo_id}/archivar", response_model=dict)
async def archivar_cargo(
    cargo_id: UUID,
    archivado: bool,
    repository: CargoRepository = Depends(get_cargo_repository)
) -> dict:
    """Archiva (True) o desarchiva (False) un cargo."""
    cargo = repository.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    
    updated = repository.set_archivado(cargo_id, archivado)
    return {"id": str(updated.id), "nombre": updated.nombre, "archivado": updated.archivado}