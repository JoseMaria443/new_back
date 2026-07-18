"""
Adaptadores de persistencia del módulo de personal.
"""
from .empleado_repository import (
    EmpleadoRepositoryAdapter,
    HistorialEstatusRepositoryAdapter,
)

__all__ = [
    "EmpleadoRepositoryAdapter",
    "HistorialEstatusRepositoryAdapter",
]