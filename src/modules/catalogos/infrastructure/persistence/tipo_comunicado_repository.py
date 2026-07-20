"""
Adaptador de persistencia para el repositorio de Tipos de Comunicado.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, Boolean, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import TipoComunicado
from ...domain.ports import TipoComunicadoRepository
from shared.infrastructure.database.connection import DatabaseConnection


class TipoComunicadoRepositoryAdapter(TipoComunicadoRepository):
    """
    Implementación concreta del repositorio de Tipos de Comunicado.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla TIPO_COMUNICADO según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "TIPO_COMUNICADO" in metadata.tables:
            return metadata.tables["TIPO_COMUNICADO"]
        return Table(
            "TIPO_COMUNICADO",
            metadata,
            Column("idTipoComunicado", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(100), unique=True, nullable=False),
            Column("archivado", Boolean, nullable=False, server_default="false"),
        )
    
    def add(self, tipo: TipoComunicado) -> TipoComunicado:
        """Agrega un tipo de comunicado y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idTipoComunicado=tipo.id,
                nombre=tipo.nombre,
                archivado=tipo.archivado
            ).returning(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def get_by_id(self, id: UUID) -> Optional[TipoComunicado]:
        """Obtiene un tipo de comunicado por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            ).where(self.table.c.idTipoComunicado == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def get_by_nombre(self, nombre: str) -> Optional[TipoComunicado]:
        """Obtiene un tipo de comunicado por su nombre."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            ).where(self.table.c.nombre == nombre)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def get_all(self) -> List[TipoComunicado]:
        """Obtiene todos los tipos de comunicado."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                TipoComunicado(id=row.idTipoComunicado, nombre=row.nombre, archivado=row.archivado)
                for row in rows
            ]
    
    def get_activos(self) -> List[TipoComunicado]:
        """Obtiene solo los tipos de comunicado activos (archivado == False)."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            ).where(self.table.c.archivado == False)
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                TipoComunicado(id=row.idTipoComunicado, nombre=row.nombre, archivado=row.archivado)
                for row in rows
            ]
    
    def set_archivado(self, id: UUID, archivado: bool) -> TipoComunicado:
        """Archiva o desarchiva un tipo de comunicado."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idTipoComunicado == id
            ).values(
                archivado=archivado
            ).returning(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def update(self, tipo: TipoComunicado) -> TipoComunicado:
        """Actualiza un tipo de comunicado existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idTipoComunicado == tipo.id
            ).values(
                nombre=tipo.nombre
            ).returning(
                self.table.c.idTipoComunicado,
                self.table.c.nombre,
                self.table.c.archivado
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre,
                archivado=row.archivado
            )
    
    def delete(self, id: UUID) -> None:
        """Borrado lógico (soft delete) de un tipo de comunicado por su ID."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(self.table.c.idTipoComunicado == id).values(archivado=True)
            conn.execute(stmt)
            conn.commit()