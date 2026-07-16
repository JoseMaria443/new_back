"""
Adaptador de persistencia para el repositorio de Roles de Responsable.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import RolResponsable
from ...domain.ports import RolResponsableRepository
from shared.infrastructure.database.connection import DatabaseConnection


class RolResponsableRepositoryAdapter(RolResponsableRepository):
    """
    Implementación concreta del repositorio de Roles de Responsable.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla ROL_RESPONSABLE según el esquema SQL."""
        return Table(
            "ROL_RESPONSABLE",
            self._engine.metadata,
            Column("idRolResponsable", PG_UUID(as_uuid=True), primary_key=True),
            Column("descripcionRol", String(100), unique=True, nullable=False),
        )
    
    def add(self, rol: RolResponsable) -> RolResponsable:
        """Agrega un rol de responsable y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idRolResponsable=rol.id,
                descripcionRol=rol.descripcionRol
            ).returning(
                self.table.c.idRolResponsable,
                self.table.c.descripcionRol
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return RolResponsable(
                id=row.idRolResponsable,
                descripcionRol=row.descripcionRol
            )
    
    def get_by_id(self, id: UUID) -> Optional[RolResponsable]:
        """Obtiene un rol de responsable por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idRolResponsable,
                self.table.c.descripcionRol
            ).where(self.table.c.idRolResponsable == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return RolResponsable(
                id=row.idRolResponsable,
                descripcionRol=row.descripcionRol
            )
    
    def get_by_descripcion(self, descripcion: str) -> Optional[RolResponsable]:
        """Obtiene un rol de responsable por su descripción."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idRolResponsable,
                self.table.c.descripcionRol
            ).where(self.table.c.descripcionRol == descripcion)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return RolResponsable(
                id=row.idRolResponsable,
                descripcionRol=row.descripcionRol
            )
    
    def get_all(self) -> List[RolResponsable]:
        """Obtiene todos los roles de responsable."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idRolResponsable,
                self.table.c.descripcionRol
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                RolResponsable(id=row.idRolResponsable, descripcionRol=row.descripcionRol)
                for row in rows
            ]
    
    def update(self, rol: RolResponsable) -> RolResponsable:
        """Actualiza un rol de responsable existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idRolResponsable == rol.id
            ).values(
                descripcionRol=rol.descripcionRol
            ).returning(
                self.table.c.idRolResponsable,
                self.table.c.descripcionRol
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return RolResponsable(
                id=row.idRolResponsable,
                descripcionRol=row.descripcionRol
            )
    
    def delete(self, id: UUID) -> None:
        """Elimina un rol de responsable por su ID."""
        with self._engine.connect() as conn:
            stmt = delete(self.table).where(self.table.c.idRolResponsable == id)
            conn.execute(stmt)
            conn.commit()