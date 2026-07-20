"""
Helper para resolver un ESTADO_TAREA por nombre de forma robusta
(sin distinguir mayúsculas/espacios), ya que ESTADO_TAREA es de solo
lectura por API y sus registros se siembran manualmente en la base de
datos (Sección III: sin endpoint de escritura para este catálogo).
"""
from typing import Any

from shared.domain.exceptions import BusinessRuleViolationError


def _normalize(nombre: str) -> str:
    return nombre.strip().upper().replace(" ", "_")


def find_estado_by_nombre(estado_tarea_repository: Any, nombre_buscado: str):
    """
    Busca un EstadoTarea comparando nombres normalizados (mayúsculas,
    sin espacios extra, espacios internos tratados como '_').
    Lanza BusinessRuleViolationError si no se encuentra: significa que
    el catálogo ESTADO_TAREA no tiene sembrado el estado esperado.
    """
    objetivo = _normalize(nombre_buscado)
    for estado in estado_tarea_repository.get_all():
        if _normalize(estado.nombre) == objetivo:
            return estado
    raise BusinessRuleViolationError(
        f"El catálogo ESTADO_TAREA no tiene sembrado el estado '{nombre_buscado}'. "
        f"Debe insertarse manualmente en la base de datos (sin endpoint de escritura)."
    )