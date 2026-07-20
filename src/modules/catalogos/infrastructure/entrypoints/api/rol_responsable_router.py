"""
Router de API para el recurso RolResponsable.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos import RolResponsableCreateRequest, RolResponsableResponse, ArchivarRequest
from ....application.use_cases import RolResponsableUseCases
from ....infrastructure.persistence import RolResponsableRepositoryAdapter

router = APIRouter(prefix="/roles-responsable", tags=["roles-responsable"])


def get_rol_responsable_use_cases() -> RolResponsableUseCases:
    """Factory dependency para obtener casos de uso de RolResponsable."""
    repository = RolResponsableRepositoryAdapter()
    return RolResponsableUseCases(repository)


@router.post("/", response_model=RolResponsableResponse, status_code=status.HTTP_201_CREATED)
async def create_rol_responsable(
    request: RolResponsableCreateRequest,
    use_cases: RolResponsableUseCases = Depends(get_rol_responsable_use_cases)
) -> RolResponsableResponse:
    """Crea un nuevo rol de responsable."""
    try:
        return use_cases.create(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[RolResponsableResponse])
async def list_roles_responsable_activos(
    use_cases: RolResponsableUseCases = Depends(get_rol_responsable_use_cases)
) -> List[RolResponsableResponse]:
    """Lista solo los roles de responsable activos (no archivados). Para dropdowns/checkboxes."""
    return use_cases.get_activos()


@router.get("/todos", response_model=List[RolResponsableResponse])
async def list_roles_responsable_todos(
    use_cases: RolResponsableUseCases = Depends(get_rol_responsable_use_cases)
) -> List[RolResponsableResponse]:
    """Lista TODOS los roles de responsable (activos y archivados). Solo para vista de Configuración."""
    return use_cases.get_all()


@router.get("/{rol_id}", response_model=RolResponsableResponse)
async def get_rol_responsable(
    rol_id: UUID,
    use_cases: RolResponsableUseCases = Depends(get_rol_responsable_use_cases)
) -> RolResponsableResponse:
    """Obtiene un rol de responsable por ID."""
    rol = use_cases.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    return rol


@router.patch("/{rol_id}/archivar", response_model=RolResponsableResponse)
async def archivar_rol_responsable(
    rol_id: UUID,
    request: ArchivarRequest,
    use_cases: RolResponsableUseCases = Depends(get_rol_responsable_use_cases)
) -> RolResponsableResponse:
    """Archiva (True) o desarchiva (False) un rol de responsable."""
    updated = use_cases.set_archivado(rol_id, request.archivado)
    if updated is None:
        raise HTTPException(status_code=404, detail="Rol de responsable no encontrado")
    return updated