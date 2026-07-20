"""
Router de API para el recurso MedioRecepcion.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos import MedioRecepcionCreateRequest, MedioRecepcionResponse, ArchivarRequest
from ....application.use_cases import MedioRecepcionUseCases
from ....infrastructure.persistence import MedioRecepcionRepositoryAdapter

router = APIRouter(prefix="/medios-recepcion", tags=["medios-recepcion"])


def get_medio_recepcion_use_cases() -> MedioRecepcionUseCases:
    """Factory dependency para obtener casos de uso de MedioRecepcion."""
    repository = MedioRecepcionRepositoryAdapter()
    return MedioRecepcionUseCases(repository)


@router.post("/", response_model=MedioRecepcionResponse, status_code=status.HTTP_201_CREATED)
async def create_medio_recepcion(
    request: MedioRecepcionCreateRequest,
    use_cases: MedioRecepcionUseCases = Depends(get_medio_recepcion_use_cases)
) -> MedioRecepcionResponse:
    """Crea un nuevo medio de recepción."""
    try:
        return use_cases.create(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[MedioRecepcionResponse])
async def list_medios_recepcion_activos(
    use_cases: MedioRecepcionUseCases = Depends(get_medio_recepcion_use_cases)
) -> List[MedioRecepcionResponse]:
    """Lista solo los medios de recepción activos (no archivados). Para dropdowns/checkboxes."""
    return use_cases.get_activos()


@router.get("/todos", response_model=List[MedioRecepcionResponse])
async def list_medios_recepcion_todos(
    use_cases: MedioRecepcionUseCases = Depends(get_medio_recepcion_use_cases)
) -> List[MedioRecepcionResponse]:
    """Lista TODOS los medios de recepción (activos y archivados). Solo para vista de Configuración."""
    return use_cases.get_all()


@router.get("/{medio_id}", response_model=MedioRecepcionResponse)
async def get_medio_recepcion(
    medio_id: UUID,
    use_cases: MedioRecepcionUseCases = Depends(get_medio_recepcion_use_cases)
) -> MedioRecepcionResponse:
    """Obtiene un medio de recepción por ID."""
    medio = use_cases.get_by_id(medio_id)
    if medio is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    return medio


@router.patch("/{medio_id}/archivar", response_model=MedioRecepcionResponse)
async def archivar_medio_recepcion(
    medio_id: UUID,
    request: ArchivarRequest,
    use_cases: MedioRecepcionUseCases = Depends(get_medio_recepcion_use_cases)
) -> MedioRecepcionResponse:
    """Archiva (True) o desarchiva (False) un medio de recepción."""
    updated = use_cases.set_archivado(medio_id, request.archivado)
    if updated is None:
        raise HTTPException(status_code=404, detail="Medio de recepción no encontrado")
    return updated