"""
Router de API para el recurso RolDestinatario.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ...domain.entities import RolDestinatario
from ...domain.ports import RolDestinatarioRepository
from ...infrastructure.persistence import RolDestinatarioRepositoryAdapter

router = APIRouter(prefix="/roles-destinatario", tags=["roles-destinatario"])


def get_rol_destinatario_repository() -> RolDestinatarioRepository:
    return RolDestinatarioRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_rol_destinatario(
    descripcionRol: str,
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> dict:
    try:
        rol = RolDestinatario(descripcionRol=descripcionRol)
        saved = repository.add(rol)
        return {"id": str(saved.id), "descripcionRol": saved.descripcionRol}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_roles_destinatario(
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> List[dict]:
    roles = repository.get_all()
    return [{"id": str(r.id), "descripcionRol": r.descripcionRol} for r in roles]


@router.get("/{rol_id}", response_model=dict)
async def get_rol_destinatario(
    rol_id: UUID,
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> dict:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    return {"id": str(rol.id), "descripcionRol": rol.descripcionRol}


@router.put("/{rol_id}", response_model=dict)
async def update_rol_destinatario(
    rol_id: UUID,
    descripcionRol: str,
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> dict:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    
    try:
        rol.descripcionRol = descripcionRol
        updated = repository.update(rol)
        return {"id": str(updated.id), "descripcionRol": updated.descripcionRol}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{rol_id}", status_code=204)
async def delete_rol_destinatario(
    rol_id: UUID,
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> None:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    repository.delete(rol_id)