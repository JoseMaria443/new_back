"""
Use case para crear tareas (Sección V SGC2I).
"""
from uuid import UUID
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from ...domain.entities import Tarea
from ...domain.ports import TareaRepository
from ..estado_lookup import find_estado_by_nombre
from shared.domain.exceptions import BusinessRuleViolationError


def _as_aware_utc(value: datetime) -> datetime:
    """
    Normaliza a datetime timezone-aware (UTC). Algunos motores (ej. SQLite,
    usado en pruebas) no preservan el timezone al leer de vuelta un valor
    guardado; en Postgres real esto no ocurre, pero se normaliza aquí para
    que la comparación de fechas sea segura sin importar el motor.
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


class CreateTareaUseCase:
    """
    Caso de uso para registrar una nueva tarea derivada de un comunicado.

    Valida: idComunicado existente, fechaEntrega >= fechaRecepcion del
    comunicado padre, cada idRolResponsable existente en el catálogo.
    Fuerza el estado inicial a ASIGNADA, ignorando cualquier estado que
    mande el cliente (no se acepta idEstadoTarea en el payload).
    """

    def __init__(
        self,
        repository: TareaRepository,
        comunicado_repository: Any,
        estado_tarea_repository: Any,
        rol_responsable_repository: Optional[Any] = None,
    ):
        self._repository = repository
        self._comunicado_repository = comunicado_repository
        self._estado_tarea_repository = estado_tarea_repository
        self._rol_responsable_repository = rol_responsable_repository

    def execute(
        self,
        idComunicado: UUID,
        resumenActividad: str,
        descripcion: str,
        fechaEntrega: datetime,
        responsables: List[Dict[str, Any]],
    ) -> Tarea:
        # idComunicado debe existir
        comunicado = self._comunicado_repository.get_by_id(idComunicado)
        if comunicado is None:
            raise BusinessRuleViolationError(
                f"El comunicado {idComunicado} no existe"
            )

        # fechaEntrega debe ser mayor o igual a fechaRecepcion del comunicado padre
        if _as_aware_utc(fechaEntrega) < _as_aware_utc(comunicado.fechaRecepcion):
            raise BusinessRuleViolationError(
                "fechaEntrega no puede ser anterior a la fechaRecepcion del comunicado padre"
            )

        # Cada idRolResponsable debe existir en el catálogo
        if self._rol_responsable_repository is not None:
            for resp in responsables:
                rol_id = resp["idRolResponsable"]
                if self._rol_responsable_repository.get_by_id(rol_id) is None:
                    raise BusinessRuleViolationError(
                        f"El rol de responsable {rol_id} no existe"
                    )

        # Estado inicial forzado a ASIGNADA (se ignora cualquier estado del cliente)
        estado_asignada = find_estado_by_nombre(self._estado_tarea_repository, "ASIGNADA")

        tarea = Tarea(
            idComunicado=idComunicado,
            idEstadoTarea=estado_asignada.id,
            resumenActividad=resumenActividad,
            descripcion=descripcion,
            fechaEntrega=fechaEntrega,
        )

        return self._repository.add_with_responsables(tarea, responsables)