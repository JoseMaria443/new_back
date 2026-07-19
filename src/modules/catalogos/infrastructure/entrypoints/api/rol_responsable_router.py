"""
Router de API para el recurso RolResponsable.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import RolResponsable
from ....domain.ports import RolResponsableRepository
from ....infrastructure.persistence import RolResponsableRepositoryAdapter

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
        return {"id": str(saved.id), "descripcionRol": saved.descripcionRol, "archivado": saved.archivado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[dict])
async def list_roles_responsable_activos(
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> List[dict]:
    """Lista solo los roles de responsable activos (no archivados). Para dropdowns/checkboxes."""
    roles = repository.get_activos()
    return [{"id": str(r.id), "descripcionRol": r.descripcionRol, "archivado": r.archivado} for r in roles]


@router.get("/todos", response_model=List[dict])
async def list_roles_responsable_todos(
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> List[dict]:
    """Lista TODOS los roles de responsable (activos y archivados). Solo para vista de Configuración."""
    roles = repository.get_all()
    return [{"id": str(r.id), "descripcionRol": r.descripcionRol, "archivado": r.archivado} for r in roles]


@router.get("/{rol_id}", response_model=dict)
async def get_rol_responsable(
    rol_id: UUID,
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> dict:
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    return {"id": str(rol.id), "descripcionRol": rol.descripcionRol, "archivado": rol.archivado}


@router.patch("/{rol_id}/archivar", response_model=dict)
async def archivar_rol_responsable(
    rol_id: UUID,
    archivado: bool,
    repository: RolResponsableRepository = Depends(get_rol_responsable_repository)
) -> dict:
    """Archiva (True) o desarchiva (False) un rol de responsable."""
    rol = repository.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    
    updated = repository.set_archivado(rol_id, archivado)
    return {"id": str(updated.id), "descripcionRol": updated.descripcionRol, "archivado": updated.archivado}