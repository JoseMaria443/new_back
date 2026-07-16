"""
Gestión de conexión a base de datos usando SQLAlchemy Core.
No se usa ORM, solo el motor de conexión y SQL crudo.
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from contextlib import contextmanager
from typing import Generator

from config.settings import settings


class DatabaseConnection:
    """
    Adaptador de conexión a base de datos.
    Usa SQLAlchemy Core sin ORM.
    """
    
    _engine: Engine = None
    
    @classmethod
    def get_engine(cls) -> Engine:
        """Obtiene o crea el motor de base de datos."""
        if cls._engine is None:
            cls._engine = create_engine(
                settings.DATABASE_URL,
                echo=settings.DATABASE_ECHO,
                pool_pre_ping=True,
                pool_recycle=3600
            )
        return cls._engine
    
    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator:
        """
        Context manager para obtener una conexión.
        Uso: with DatabaseConnection.get_connection() as conn:
        """
        engine = cls.get_engine()
        with engine.connect() as connection:
            yield connection
    
    @classmethod
    def close(cls) -> None:
        """Cierra el motor de base de datos."""
        if cls._engine:
            cls._engine.dispose()
            cls._engine = None