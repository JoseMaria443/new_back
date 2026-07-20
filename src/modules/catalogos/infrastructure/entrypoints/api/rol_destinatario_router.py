"""
Router de API para el recurso RolDestinatario.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos import RolDestinatarioCreateRequest, RolDestinatarioResponse, ArchivarRequest
from ....application.use_cases import RolDestinatarioUseCases
from ....infrastructure.persistence import RolDestinatarioRepositoryAdapter

router = APIRouter(prefix="/roles-destinatario", tags=["roles-destinatario"])


def get_rol_destinatario_use_cases() -> RolDestinatarioUseCases:
    """Factory dependency para obtener casos de uso de RolDestinatario."""
    repository = RolDestinatarioRepositoryAdapter()
    return RolDestinatarioUseCases(repository)


@router.post("/", response_model=RolDestinatarioResponse, status_code=status.HTTP_201_CREATED)
async def create_rol_destinatario(
    request: RolDestinatarioCreateRequest,
    use_cases: RolDestinatarioUseCases = Depends(get_rol_destinatario_use_cases)
) -> RolDestinatarioResponse:
    """Crea un nuevo rol de destinatario."""
    try:
        return use_cases.create(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[RolDestinatarioResponse])
async def list_roles_destinatario_activos(
    use_cases: RolDestinatarioUseCases = Depends(get_rol_destinatario_use_cases)
) -> List[RolDestinatarioResponse]:
    """Lista solo los roles de destinatario activos (no archivados). Para dropdowns/checkboxes."""
    return use_cases.get_activos()


@router.get("/todos", response_model=List[RolDestinatarioResponse])
async def list_roles_destinatario_todos(
    use_cases: RolDestinatarioUseCases = Depends(get_rol_destinatario_use_cases)
) -> List[RolDestinatarioResponse]:
    """Lista TODOS los roles de destinatario (activos y archivados). Solo para vista de Configuración."""
    return use_cases.get_all()


@router.get("/{rol_id}", response_model=RolDestinatarioResponse)
async def get_rol_destinatario(
    rol_id: UUID,
    use_cases: RolDestinatarioUseCases = Depends(get_rol_destinatario_use_cases)
) -> RolDestinatarioResponse:
    """Obtiene un rol de destinatario por ID."""
    rol = use_cases.get_by_id(rol_id)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    return rol


@router.patch("/{rol_id}/archivar", response_model=RolDestinatarioResponse)
async def archivar_rol_destinatario(
    rol_id: UUID,
    request: ArchivarRequest,
    use_cases: RolDestinatarioUseCases = Depends(get_rol_destinatario_use_cases)
) -> RolDestinatarioResponse:
    """Archiva (True) o desarchiva (False) un rol de destinatario."""
    updated = use_cases.set_archivado(rol_id, request.archivado)
    if updated is None:
        raise HTTPException(status_code=404, detail="Rol de destinatario no encontrado")
    return updated