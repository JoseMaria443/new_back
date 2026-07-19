"""
Adaptador de persistencia para el repositorio de Roles de Destinatario.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import RolDestinatario
from ...domain.ports import RolDestinatarioRepository
from shared.infrastructure.database.connection import DatabaseConnection


class RolDestinatarioRepositoryAdapter(RolDestinatarioRepository):
    """
    Implementación concreta del repositorio de Roles de Destinatario.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla ROL_DESTINATARIO según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "ROL_DESTINATARIO" in metadata.tables:
            return metadata.tables["ROL_DESTINATARIO"]
        return Table(
            "ROL_DESTINATARIO",
            metadata,
            Column("idRolDestinatario", PG_UUID(as_uuid=True), primary_key=True),
            Column("descripcionRol", String(100), unique=True, nullable=False),
        )
    
    def add(self, rol: RolDestinatario) -> RolDestinatario:
        """Agrega un rol de destinatario y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idRolDestinatario=rol.id,
                descripcionRol=rol.descripcionRol
            ).returning(
                self.table.c.idRolDestinatario,
                self.table.c.descripcionRol
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return RolDestinatario(
                id=row.idRolDestinatario,
                descripcionRol=row.descripcionRol
            )
    
    def get_by_id(self, id: UUID) -> Optional[RolDestinatario]:
        """Obtiene un rol de destinatario por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idRolDestinatario,
                self.table.c.descripcionRol
            ).where(self.table.c.idRolDestinatario == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return RolDestinatario(
                id=row.idRolDestinatario,
                descripcionRol=row.descripcionRol
            )
    
    def get_by_descripcion(self, descripcion: str) -> Optional[RolDestinatario]:
        """Obtiene un rol de destinatario por su descripción."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idRolDestinatario,
                self.table.c.descripcionRol
            ).where(self.table.c.descripcionRol == descripcion)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return RolDestinatario(
                id=row.idRolDestinatario,
                descripcionRol=row.descripcionRol
            )
    
    def get_all(self) -> List[RolDestinatario]:
        """Obtiene todos los roles de destinatario."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idRolDestinatario,
                self.table.c.descripcionRol
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                RolDestinatario(id=row.idRolDestinatario, descripcionRol=row.descripcionRol)
                for row in rows
            ]
    
    def update(self, rol: RolDestinatario) -> RolDestinatario:
        """Actualiza un rol de destinatario existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idRolDestinatario == rol.id
            ).values(
                descripcionRol=rol.descripcionRol
            ).returning(
                self.table.c.idRolDestinatario,
                self.table.c.descripcionRol
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return RolDestinatario(
                id=row.idRolDestinatario,
                descripcionRol=row.descripcionRol
            )
    
    def delete(self, id: UUID) -> None:
        """Elimina un rol de destinatario por su ID."""
        with self._engine.connect() as conn:
            stmt = delete(self.table).where(self.table.c.idRolDestinatario == id)
            conn.execute(stmt)
            conn.commit()