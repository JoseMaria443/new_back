"""
Router de API para el recurso Área.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos import AreaCreateRequest, AreaResponse, ArchivarRequest
from ....application.use_cases import AreaUseCases
from ....infrastructure.persistence import AreaRepositoryAdapter

router = APIRouter(prefix="/areas", tags=["areas"])


def get_area_use_cases() -> AreaUseCases:
    """Factory dependency para obtener casos de uso de Área."""
    repository = AreaRepositoryAdapter()
    return AreaUseCases(repository)


@router.post("/", response_model=AreaResponse, status_code=status.HTTP_201_CREATED)
async def create_area(
    request: AreaCreateRequest,
    use_cases: AreaUseCases = Depends(get_area_use_cases)
) -> AreaResponse:
    """Crea una nueva área."""
    try:
        return use_cases.create(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[AreaResponse])
async def list_areas_activos(
    use_cases: AreaUseCases = Depends(get_area_use_cases)
) -> List[AreaResponse]:
    """Lista solo las áreas activas (no archivadas). Para dropdowns/checkboxes."""
    return use_cases.get_activos()


@router.get("/todos", response_model=List[AreaResponse])
async def list_areas_todos(
    use_cases: AreaUseCases = Depends(get_area_use_cases)
) -> List[AreaResponse]:
    """Lista TODAS las áreas (activas y archivadas). Solo para vista de Configuración."""
    return use_cases.get_all()


@router.get("/{area_id}", response_model=AreaResponse)
async def get_area(
    area_id: UUID,
    use_cases: AreaUseCases = Depends(get_area_use_cases)
) -> AreaResponse:
    """Obtiene un área por ID."""
    area = use_cases.get_by_id(area_id)
    if area is None:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return area


@router.patch("/{area_id}/archivar", response_model=AreaResponse)
async def archivar_area(
    area_id: UUID,
    request: ArchivarRequest,
    use_cases: AreaUseCases = Depends(get_area_use_cases)
) -> AreaResponse:
    """Archiva (True) o desarchiva (False) un área."""
    updated = use_cases.set_archivado(area_id, request.archivado)
    if updated is None:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return updated