"""
Routers de API del módulo de catálogos.
"""
from .area_router import router as area_router
from .cargo_router import router as cargo_router
from .tipo_comunicado_router import router as tipo_comunicado_router
from .medio_recepcion_router import router as medio_recepcion_router
from .rol_destinatario_router import router as rol_destinatario_router
from .rol_responsable_router import router as rol_responsable_router
from .estado_tarea_router import router as estado_tarea_router

__all__ = [
    "area_router",
    "cargo_router",
    "tipo_comunicado_router",
    "medio_recepcion_router",
    "rol_destinatario_router",
    "rol_responsable_router",
    "estado_tarea_router",
]