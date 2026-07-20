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
    Normaliza a datetime timezone-aware (UTC).
    """
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


class CreateTareaUseCase:
    """
    Caso de uso para registrar una nueva tarea derivada de un comunicado.

    Lógica de Negocio:
    1. Valida existencia de idComunicado.
    2. Valida fechaEntrega >= fechaRecepcion del comunicado padre.
    3. Consulta EstadoTareaRepository buscando el estado "asignada" para inyectar su idEstadoTarea.
    4. Inserta la tarea y sus responsables transaccionalmente.
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
        # 1. Validar que el comunicado existe
        comunicado = self._comunicado_repository.get_by_id(idComunicado)
        if comunicado is None:
            raise BusinessRuleViolationError(
                f"El comunicado {idComunicado} no existe"
            )

        # 2. Validar que fechaEntrega >= fechaRecepcion del comunicado padre
        if _as_aware_utc(fechaEntrega) < _as_aware_utc(comunicado.fechaRecepcion):
            raise BusinessRuleViolationError(
                "La fechaEntrega de la tarea no puede ser anterior a la fechaRecepcion del comunicado padre"
            )

        # 3. Validar roles de responsables si el repositorio está disponible
        if self._rol_responsable_repository is not None:
            for resp in responsables:
                rol_id = resp["idRolResponsable"]
                if self._rol_responsable_repository.get_by_id(rol_id) is None:
                    raise BusinessRuleViolationError(
                        f"El rol de responsable {rol_id} no existe"
                    )

        # 4. Obtener el UUID del estado "asignada" desde el catálogo de estados
        estado_asignada = self._estado_tarea_repository.get_by_nombre("asignada")
        if estado_asignada is None:
            # Reintento con fallback si la BD tiene variante de mayúsculas
            estado_asignada = find_estado_by_nombre(self._estado_tarea_repository, "ASIGNADA")

        # 5. Instanciar la entidad Tarea con idEstadoTarea asignado
        tarea = Tarea(
            idComunicado=idComunicado,
            idEstadoTarea=estado_asignada.id,
            resumenActividad=resumenActividad,
            descripcion=descripcion,
            fechaEntrega=fechaEntrega,
        )

        # 6. Insertar en TAREA y TAREA_RESPONSABLE transaccionalmente
        return self._repository.add_with_responsables(tarea, responsables)