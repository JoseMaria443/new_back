"""
Router de API para el recurso EstadoTarea.
Solo expone métodos de lectura por inmutabilidad del catálogo.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....application.dtos import EstadoTareaResponse
from ....application.use_cases import EstadoTareaUseCases
from ....infrastructure.persistence import EstadoTareaRepositoryAdapter

router = APIRouter(prefix="/estados-tarea", tags=["estados-tarea"])


def get_estado_tarea_use_cases() -> EstadoTareaUseCases:
    """Factory dependency para obtener casos de uso de EstadoTarea."""
    repository = EstadoTareaRepositoryAdapter()
    return EstadoTareaUseCases(repository)


@router.get("/", response_model=List[EstadoTareaResponse])
async def list_estados_tarea(
    use_cases: EstadoTareaUseCases = Depends(get_estado_tarea_use_cases)
) -> List[EstadoTareaResponse]:
    """Lista todos los estados de tarea."""
    return use_cases.get_all()


@router.get("/{estado_id}", response_model=EstadoTareaResponse)
async def get_estado_tarea(
    estado_id: UUID,
    use_cases: EstadoTareaUseCases = Depends(get_estado_tarea_use_cases)
) -> EstadoTareaResponse:
    """Obtiene un estado de tarea por ID."""
    estado = use_cases.get_by_id(estado_id)
    if estado is None:
        raise HTTPException(status_code=404, detail="Estado de tarea no encontrado")
    return estado