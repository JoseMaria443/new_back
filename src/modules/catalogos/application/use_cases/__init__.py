"""
Casos de uso del módulo de catálogos.
"""
from .area_use_cases import AreaUseCases
from .cargo_use_cases import CargoUseCases
from .tipo_comunicado_use_cases import TipoComunicadoUseCases
from .medio_recepcion_use_cases import MedioRecepcionUseCases
from .rol_destinatario_use_cases import RolDestinatarioUseCases
from .rol_responsable_use_cases import RolResponsableUseCases
from .estado_tarea_use_cases import EstadoTareaUseCases

__all__ = [
    "AreaUseCases",
    "CargoUseCases",
    "TipoComunicadoUseCases",
    "MedioRecepcionUseCases",
    "RolDestinatarioUseCases",
    "RolResponsableUseCases",
    "EstadoTareaUseCases",
]