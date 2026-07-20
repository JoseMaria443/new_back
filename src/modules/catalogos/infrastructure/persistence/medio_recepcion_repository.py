"""
Adaptador de persistencia para el repositorio de Medios de Recepción.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, Boolean, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import MedioRecepcion
from ...domain.ports import MedioRecepcionRepository
from shared.infrastructure.database.connection import DatabaseConnection


class MedioRecepcionRepositoryAdapter(MedioRecepcionRepository):
    """
    Implementación concreta del repositorio de Medios de Recepción.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla MEDIO_RECEPCION según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "MEDIO_RECEPCION" in metadata.tables:
            return metadata.tables["MEDIO_RECEPCION"]
        return Table(
            "MEDIO_RECEPCION",
            metadata,
            Column("idMedioRecepcion", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(100), unique=True, nullable=False),
            Column("archivado", Boolean, nullable=False, server_default="false"),
        )
    
    def add(self, medio: MedioRecepcion) -> MedioRecepcion:
        """Agrega un medio de recepción y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idMedioRecepcion=medio.id,
                nombre=medio.nombre,
                archivado=medio.archivado
            ).returning(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return MedioRecepcion(
                id=row.idMedioRecepcion,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def get_by_id(self, id: UUID) -> Optional[MedioRecepcion]:
        """Obtiene un medio de recepción por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            ).where(self.table.c.idMedioRecepcion == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return MedioRecepcion(
                id=row.idMedioRecepcion,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def get_by_nombre(self, nombre: str) -> Optional[MedioRecepcion]:
        """Obtiene un medio de recepción por su nombre."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            ).where(self.table.c.nombre == nombre)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return MedioRecepcion(
                id=row.idMedioRecepcion,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def get_all(self) -> List[MedioRecepcion]:
        """Obtiene todos los medios de recepción."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                MedioRecepcion(id=row.idMedioRecepcion, nombre=row.nombre, archivado=row.archivado)
                for row in rows
            ]
    
    def get_activos(self) -> List[MedioRecepcion]:
        """Obtiene solo los medios de recepción activos (archivado == False)."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            ).where(self.table.c.archivado == False)
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                MedioRecepcion(id=row.idMedioRecepcion, nombre=row.nombre, archivado=row.archivado)
                for row in rows
            ]
    
    def set_archivado(self, id: UUID, archivado: bool) -> MedioRecepcion:
        """Archiva o desarchiva un medio de recepción."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idMedioRecepcion == id
            ).values(
                archivado=archivado
            ).returning(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return MedioRecepcion(
                id=row.idMedioRecepcion,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def update(self, medio: MedioRecepcion) -> MedioRecepcion:
        """Actualiza un medio de recepción existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idMedioRecepcion == medio.id
            ).values(
                nombre=medio.nombre
            ).returning(
                self.table.c.idMedioRecepcion,
                self.table.c.nombre,
                self.table.c.archivado
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return MedioRecepcion(
                id=row.idMedioRecepcion,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def delete(self, id: UUID) -> None:
        """Borrado lógico (soft delete) de un medio de recepción por su ID."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(self.table.c.idMedioRecepcion == id).values(archivado=True)
            conn.execute(stmt)
            conn.commit()