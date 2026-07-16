"""
Puertos (interfaces) del módulo de catálogos.
"""
from .repositories import (
    AreaRepository,
    CargoRepository,
    TipoComunicadoRepository,
    MedioRecepcionRepository,
    RolDestinatarioRepository,
    RolResponsableRepository,
    EstadoTareaRepository,
)

__all__ = [
    "AreaRepository",
    "CargoRepository",
    "TipoComunicadoRepository",
    "MedioRecepcionRepository",
    "RolDestinatarioRepository",
    "RolResponsableRepository",
    "EstadoTareaRepository",
]