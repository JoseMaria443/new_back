"""
Adaptadores de persistencia del módulo de catálogos.
"""
from .area_repository import AreaRepositoryAdapter
from .cargo_repository import CargoRepositoryAdapter
from .tipo_comunicado_repository import TipoComunicadoRepositoryAdapter
from .medio_recepcion_repository import MedioRecepcionRepositoryAdapter
from .rol_destinatario_repository import RolDestinatarioRepositoryAdapter
from .rol_responsable_repository import RolResponsableRepositoryAdapter
from .estado_tarea_repository import EstadoTareaRepositoryAdapter

__all__ = [
    "AreaRepositoryAdapter",
    "CargoRepositoryAdapter",
    "TipoComunicadoRepositoryAdapter",
    "MedioRecepcionRepositoryAdapter",
    "RolDestinatarioRepositoryAdapter",
    "RolResponsableRepositoryAdapter",
    "EstadoTareaRepositoryAdapter",
]