"""
Entidades del módulo de personal.
"""
from .empleado import Empleado
from .historial_estatus import HistorialEstatus, AccionHistorial

__all__ = [
    "Empleado",
    "HistorialEstatus",
    "AccionHistorial",
]
