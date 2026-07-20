"""
Router de API para el recurso TipoComunicado.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ....application.dtos import TipoComunicadoCreateRequest, TipoComunicadoResponse, ArchivarRequest
from ....application.use_cases import TipoComunicadoUseCases
from ....infrastructure.persistence import TipoComunicadoRepositoryAdapter

router = APIRouter(prefix="/tipos-comunicado", tags=["tipos-comunicado"])


def get_tipo_comunicado_use_cases() -> TipoComunicadoUseCases:
    """Factory dependency para obtener casos de uso de TipoComunicado."""
    repository = TipoComunicadoRepositoryAdapter()
    return TipoComunicadoUseCases(repository)


@router.post("/", response_model=TipoComunicadoResponse, status_code=status.HTTP_201_CREATED)
async def create_tipo_comunicado(
    request: TipoComunicadoCreateRequest,
    use_cases: TipoComunicadoUseCases = Depends(get_tipo_comunicado_use_cases)
) -> TipoComunicadoResponse:
    """Crea un nuevo tipo de comunicado."""
    try:
        return use_cases.create(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[TipoComunicadoResponse])
async def list_tipos_comunicado_activos(
    use_cases: TipoComunicadoUseCases = Depends(get_tipo_comunicado_use_cases)
) -> List[TipoComunicadoResponse]:
    """Lista solo los tipos de comunicado activos (no archivados). Para dropdowns/checkboxes."""
    return use_cases.get_activos()


@router.get("/todos", response_model=List[TipoComunicadoResponse])
async def list_tipos_comunicado_todos(
    use_cases: TipoComunicadoUseCases = Depends(get_tipo_comunicado_use_cases)
) -> List[TipoComunicadoResponse]:
    """Lista TODOS los tipos de comunicado (activos y archivados). Solo para vista de Configuración."""
    return use_cases.get_all()


@router.get("/{tipo_id}", response_model=TipoComunicadoResponse)
async def get_tipo_comunicado(
    tipo_id: UUID,
    use_cases: TipoComunicadoUseCases = Depends(get_tipo_comunicado_use_cases)
) -> TipoComunicadoResponse:
    """Obtiene un tipo de comunicado por ID."""
    tipo = use_cases.get_by_id(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    return tipo


@router.patch("/{tipo_id}/archivar", response_model=TipoComunicadoResponse)
async def archivar_tipo_comunicado(
    tipo_id: UUID,
    request: ArchivarRequest,
    use_cases: TipoComunicadoUseCases = Depends(get_tipo_comunicado_use_cases)
) -> TipoComunicadoResponse:
    """Archiva (True) o desarchiva (False) un tipo de comunicado."""
    updated = use_cases.set_archivado(tipo_id, request.archivado)
    if updated is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    return updated