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
        responsables: List[UUID],
        colaboradores: List[UUID] = None,
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

        # 3. Obtener/resolver el rol de responsable "Líder/Principal"
        rol_lider = None
        if self._rol_responsable_repository is not None:
            rol_lider = self._rol_responsable_repository.get_by_descripcion("Líder/Principal")
            if rol_lider is None:
                rol_lider = self._rol_responsable_repository.get_by_descripcion("Líder") or \
                            self._rol_responsable_repository.get_by_descripcion("Principal")
                if rol_lider is None:
                    from modules.catalogos.domain.entities import RolResponsable
                    rol_lider = self._rol_responsable_repository.add(RolResponsable(descripcion_rol="Líder/Principal"))

        # 4. Obtener/resolver el rol de responsable "Apoyo/Colaborador"
        rol_apoyo = None
        if self._rol_responsable_repository is not None:
            rol_apoyo = self._rol_responsable_repository.get_by_descripcion("Apoyo/Colaborador")
            if rol_apoyo is None:
                rol_apoyo = self._rol_responsable_repository.get_by_descripcion("Apoyo") or \
                            self._rol_responsable_repository.get_by_descripcion("Colaborador")
                if rol_apoyo is None:
                    from modules.catalogos.domain.entities import RolResponsable
                    rol_apoyo = self._rol_responsable_repository.add(RolResponsable(descripcion_rol="Apoyo/Colaborador"))

        rol_lider_id = rol_lider.id if rol_lider is not None else UUID("00000000-0000-0000-0000-000000000001")
        rol_apoyo_id = rol_apoyo.id if rol_apoyo is not None else UUID("00000000-0000-0000-0000-000000000002")

        # 5. Unificar responsables y colaboradores en una sola lista de diccionarios
        colaboradores_list = colaboradores or []
        responsables_dto = []

        for r_id in responsables:
            responsables_dto.append({
                "idResponsable": r_id,
                "idRolResponsable": rol_lider_id
            })

        for c_id in colaboradores_list:
            responsables_dto.append({
                "idResponsable": c_id,
                "idRolResponsable": rol_apoyo_id
            })

        # 6. Obtener el UUID del estado "asignada" desde el catálogo de estados
        estado_asignada = self._estado_tarea_repository.get_by_nombre("asignada")
        if estado_asignada is None:
            # Reintento con fallback si la BD tiene variante de mayúsculas
            estado_asignada = find_estado_by_nombre(self._estado_tarea_repository, "ASIGNADA")

        # 7. Instanciar la entidad Tarea con idEstadoTarea asignado
        tarea = Tarea(
            idComunicado=idComunicado,
            idEstadoTarea=estado_asignada.id,
            resumenActividad=resumenActividad,
            descripcion=descripcion,
            fechaEntrega=fechaEntrega,
        )

        # 8. Insertar en TAREA y TAREA_RESPONSABLE transaccionalmente
        return self._repository.add_with_responsables(tarea, responsables_dto)