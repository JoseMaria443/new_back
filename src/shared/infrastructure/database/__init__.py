"""
Adaptadores de base de datos.
"""
from .connection import DatabaseConnection
from .base_repository import BaseRepository

__all__ = ["DatabaseConnection", "BaseRepository"]