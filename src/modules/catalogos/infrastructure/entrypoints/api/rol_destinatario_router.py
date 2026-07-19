"""
Router de API para el recurso RolDestinatario.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import RolDestinatario
from ....domain.ports import RolDestinatarioRepository
from ....infrastructure.persistence import RolDestinatarioRepositoryAdapter

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
        return {"id": str(saved.id), "descripcionRol": saved.descripcionRol, "archivado": saved.archivado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[dict])
async def list_roles_destinatario_activos(
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> List[dict]:
    """Lista solo los roles de destinatario activos (no archivados). Para dropdowns/checkboxes."""
    roles = repository.get_activos()
    return [{"id": str(r.id), "descripcionRol": r.descripcionRol, "archivado": r.archivado} for r in roles]


@router.get("/todos", response_model=List[dict])
async def list_roles_destinatario_todos(
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> List[dict]:
    """Lista TODOS los roles de destinatario (activos y archivados). Solo para vista de Configuración."""
    roles = repository.get_all()
    return [{"id": str(r.id), "descripcionRol": r.descripcionRol, "archivado": r.archivado} for r in roles]


@router.get("/{rol_id}", response_model=dict)
async def get_rol_destinatario(
    rol_id: UUID,
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> dict:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    return {"id": str(rol.id), "descripcionRol": rol.descripcionRol, "archivado": rol.archivado}


@router.patch("/{rol_id}/archivar", response_model=dict)
async def archivar_rol_destinatario(
    rol_id: UUID,
    archivado: bool,
    repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository)
) -> dict:
    """Archiva (True) o desarchiva (False) un rol de destinatario."""
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    
    updated = repository.set_archivado(rol_id, archivado)
    return {"id": str(updated.id), "descripcionRol": updated.descripcionRol, "archivado": updated.archivado}