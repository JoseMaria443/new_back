"""
Infraestructura del módulo de personal.
"""
from .persistence import (
    EmpleadoRepositoryAdapter,
    HistorialEstatusRepositoryAdapter,
)

__all__ = [
    "EmpleadoRepositoryAdapter",
    "HistorialEstatusRepositoryAdapter",
]