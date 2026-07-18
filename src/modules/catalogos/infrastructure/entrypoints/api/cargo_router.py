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
        return {"id": str(saved.id), "nombre": saved.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_cargos(
    repository: CargoRepository = Depends(get_cargo_repository)
) -> List[dict]:
    cargos = repository.get_all()
    return [{"id": str(c.id), "nombre": c.nombre} for c in cargos]


@router.get("/{cargo_id}", response_model=dict)
async def get_cargo(
    cargo_id: UUID,
    repository: CargoRepository = Depends(get_cargo_repository)
) -> dict:
    cargo = repository.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return {"id": str(cargo.id), "nombre": cargo.nombre}


@router.put("/{cargo_id}", response_model=dict)
async def update_cargo(
    cargo_id: UUID,
    nombre: str,
    repository: CargoRepository = Depends(get_cargo_repository)
) -> dict:
    cargo = repository.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    
    try:
        cargo.nombre = nombre
        updated = repository.update(cargo)
        return {"id": str(updated.id), "nombre": updated.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{cargo_id}", status_code=204)
async def delete_cargo(
    cargo_id: UUID,
    repository: CargoRepository = Depends(get_cargo_repository)
) -> None:
    cargo = repository.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    repository.delete(cargo_id)