"""
Ciclo de vida del comunicado (Regla IV: idEstadoComunicado).

Implementado como Enum en código, NO como columna en la base de datos:
el SQL original no tiene tabla ni columna para esto, y la propia
especificación SGC2I permite resolverlo "como su enumerador en código".
Valor actual: siempre PENDIENTE al crear un comunicado. Pendiente de
enriquecer con transiciones reales cuando se implemente la Sección V
(Tareas), que sí define un ciclo de vida completo y ligado a TAREA.
"""
from enum import Enum


class EstadoComunicado(str, Enum):
    PENDIENTE = "PENDIENTE"
    EN_PROCESO = "EN_PROCESO"
    ATENDIDO = "ATENDIDO"