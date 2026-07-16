"""
Adaptador de persistencia para el repositorio de Tipos de Comunicado.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, insert, select, update, delete
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
        return Table(
            "TIPO_COMUNICADO",
            self._engine.metadata,
            Column("idTipoComunicado", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(100), unique=True, nullable=False),
        )
    
    def add(self, tipo: TipoComunicado) -> TipoComunicado:
        """Agrega un tipo de comunicado y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idTipoComunicado=tipo.id,
                nombre=tipo.nombre
            ).returning(
                self.table.c.idTipoComunicado,
                self.table.c.nombre
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre
            )
    
    def get_by_id(self, id: UUID) -> Optional[TipoComunicado]:
        """Obtiene un tipo de comunicado por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre
            ).where(self.table.c.idTipoComunicado == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre
            )
    
    def get_by_nombre(self, nombre: str) -> Optional[TipoComunicado]:
        """Obtiene un tipo de comunicado por su nombre."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre
            ).where(self.table.c.nombre == nombre)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre
            )
    
    def get_all(self) -> List[TipoComunicado]:
        """Obtiene todos los tipos de comunicado."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idTipoComunicado,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                TipoComunicado(id=row.idTipoComunicado, nombre=row.nombre)
                for row in rows
            ]
    
    def update(self, tipo: TipoComunicado) -> TipoComunicado:
        """Actualiza un tipo de comunicado existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idTipoComunicado == tipo.id
            ).values(
                nombre=tipo.nombre
            ).returning(
                self.table.c.idTipoComunicado,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return TipoComunicado(
                id=row.idTipoComunicado,
                nombre=row.nombre
            )
    
    def delete(self, id: UUID) -> None:
        """Elimina un tipo de comunicado por su ID."""
        with self._engine.connect() as conn:
            stmt = delete(self.table).where(self.table.c.idTipoComunicado == id)
            conn.execute(stmt)
            conn.commit()