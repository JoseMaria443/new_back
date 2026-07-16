"""
Router de API para el recurso RolResponsable.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ...domain.entities import RolResponsable
from ...domain.ports import RolResponsableRepository
from ...infrastructure.persistence import RolResponsableRepositoryAdapter

router = APIRouter(prefix="/roles-responsable", tags=["roles-responsable"])


def get_rol_responsable_repository() -> RolResponsableRepository:
    return RolResponsableRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_rol_responsable(
    descripcionRol: str,
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> dict:
    try:
        rol = RolResponsable(descripcionRol=descripcionRol)
        saved = repository.add(rol)
        return {"id": str(saved.id), "descripcionRol": saved.descripcionRol}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_roles_responsable(
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> List[dict]:
    roles = repository.get_all()
    return [{"id": str(r.id), "descripcionRol": r.descripcionRol} for r in roles]


@router.get("/{rol_id}", response_model=dict)
async def get_rol_responsable(
    rol_id: UUID,
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> dict:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    return {"id": str(rol.id), "descripcionRol": rol.descripcionRol}


@router.put("/{rol_id}", response_model=dict)
async def update_rol_responsable(
    rol_id: UUID,
    descripcionRol: str,
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> dict:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    
    try:
        rol.descripcionRol = descripcionRol
        updated = repository.update(rol)
        return {"id": str(updated.id), "descripcionRol": updated.descripcionRol}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{rol_id}", status_code=204)
async def delete_rol_responsable(
    rol_id: UUID,
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> None:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    repository.delete(rol_id)