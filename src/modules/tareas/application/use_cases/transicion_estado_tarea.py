"""
Use case genérico para transiciones de estado de una tarea
(REVISADA, RECHAZADA, CANCELADA, EN_PROCESO).
"""
from uuid import UUID
from typing import Any

from ...domain.entities import Tarea
from ...domain.ports import TareaRepository
from ..estado_lookup import find_estado_by_nombre
from shared.domain.exceptions import BusinessRuleViolationError


class TransicionEstadoTareaUseCase:
    """
    Caso de uso genérico para mover una tarea a un nuevo estado por nombre.
    La validación de permisos (ej. "solo Director") se hace en el router,
    no aquí.
    """

    def __init__(self, repository: TareaRepository, estado_tarea_repository: Any):
        self._repository = repository
        self._estado_tarea_repository = estado_tarea_repository

    def execute(self, id_tarea: UUID, nombre_estado_destino: str) -> Tarea:
        tarea = self._repository.get_by_id(id_tarea)
        if tarea is None:
            raise BusinessRuleViolationError(f"La tarea {id_tarea} no existe")

        estado_destino = find_estado_by_nombre(
            self._estado_tarea_repository, nombre_estado_destino
        )

        return self._repository.update_estado(id_tarea, estado_destino.id)