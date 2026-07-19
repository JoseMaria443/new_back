"""
Gestión de conexión a base de datos usando SQLAlchemy Core.
No se usa ORM, solo el motor de conexión y SQL crudo.
Provee sesiones para transacciones ACID.
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator

from config.settings import settings


class DatabaseConnection:
    """
    Adaptador de conexión a base de datos.
    Usa SQLAlchemy Core sin ORM.
    Provee sesiones para transacciones ACID.
    """
    
    _engine: Engine = None
    _session_factory = None
    _metadata: MetaData = None
    
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
    def get_session_factory(cls):
        """Obtiene o crea el factory de sesiones."""
        if cls._session_factory is None:
            cls._session_factory = sessionmaker(
                bind=cls.get_engine(),
                class_=Session,
                expire_on_commit=False
            )
        return cls._session_factory
    
    @classmethod
    def get_metadata(cls) -> MetaData:
        """
        Obtiene el objeto MetaData compartido para definir tablas con
        SQLAlchemy Core. Un Engine no tiene atributo `.metadata`; el
        MetaData se crea y comparte aparte, una sola vez por proceso.
        """
        if cls._metadata is None:
            cls._metadata = MetaData()
        return cls._metadata
    
    @classmethod
    @contextmanager
    def get_session(cls) -> Generator[Session, None, None]:
        """
        Context manager para obtener una sesión con transacciones ACID.
        Uso: with DatabaseConnection.get_session() as session:
        """
        session_factory = cls.get_session_factory()
        session = session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
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
            cls._session_factory = None