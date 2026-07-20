"""
Casos de uso para el recurso EstadoTarea.
Solo operaciones de lectura por inmutabilidad del catálogo.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.ports import EstadoTareaRepository
from ..dtos import EstadoTareaResponse


class EstadoTareaUseCases:
    """Casos de uso de lectura para EstadoTarea."""

    def __init__(self, repository: EstadoTareaRepository):
        self.repository = repository

    def get_by_id(self, estado_id: UUID) -> Optional[EstadoTareaResponse]:
        """Obtiene un estado de tarea por su ID."""
        estado = self.repository.get_by_id(estado_id)
        if not estado:
            return None
        return EstadoTareaResponse.model_validate(estado)

    def get_all(self) -> List[EstadoTareaResponse]:
        """Obtiene todos los estados de tarea."""
        estados = self.repository.get_all()
        return [EstadoTareaResponse.model_validate(e) for e in estados]
