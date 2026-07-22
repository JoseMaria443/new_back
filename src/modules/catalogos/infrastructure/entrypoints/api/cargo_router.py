"""
Router de API para el recurso Cargo.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos import CargoCreateRequest, CargoResponse, ArchivarRequest
from ....application.use_cases import CargoUseCases
from ....infrastructure.persistence import CargoRepositoryAdapter

router = APIRouter(prefix="/cargos", tags=["cargos"])


def get_cargo_use_cases() -> CargoUseCases:
    """Factory dependency para obtener casos de uso de Cargo."""
    repository = CargoRepositoryAdapter()
    return CargoUseCases(repository)


@router.post("/", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
async def create_cargo(
    request: CargoCreateRequest,
    use_cases: CargoUseCases = Depends(get_cargo_use_cases)
) -> CargoResponse:
    """Crea un nuevo cargo."""
    try:
        return use_cases.create(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[CargoResponse])
async def list_cargos_activos(
    use_cases: CargoUseCases = Depends(get_cargo_use_cases)
) -> List[CargoResponse]:
    """Lista solo los cargos activos (no archivados). Para dropdowns/checkboxes."""
    return use_cases.get_activos()


@router.get("/todos", response_model=List[CargoResponse])
async def list_cargos_todos(
    use_cases: CargoUseCases = Depends(get_cargo_use_cases)
) -> List[CargoResponse]:
    """Lista TODOS los cargos (activos y archivados). Solo para vista de Configuración."""
    return use_cases.get_all()


@router.get("/{cargo_id}", response_model=CargoResponse)
async def get_cargo(
    cargo_id: UUID,
    use_cases: CargoUseCases = Depends(get_cargo_use_cases)
) -> CargoResponse:
    """Obtiene un cargo por ID."""
    cargo = use_cases.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    return cargo


@router.patch("/{cargo_id}/archivar", response_model=CargoResponse)
async def archivar_cargo(
    cargo_id: UUID,
    request: ArchivarRequest,
    use_cases: CargoUseCases = Depends(get_cargo_use_cases)
) -> CargoResponse:
    """Archiva (True) o desarchiva (False) un cargo."""
    cargo = use_cases.get_by_id(cargo_id)
    if cargo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cargo no encontrado")
    
    if request.archivado and cargo.nombre.strip().lower() in ["administrador", "director", "docente"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Los roles core del sistema no pueden ser archivados"
        )

    updated = use_cases.set_archivado(cargo_id, request.archivado)
    return updated