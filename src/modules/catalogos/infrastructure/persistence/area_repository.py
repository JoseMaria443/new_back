"""
Adaptador de persistencia para el repositorio de Áreas.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import Area
from ...domain.ports import AreaRepository
from shared.infrastructure.database.connection import DatabaseConnection


class AreaRepositoryAdapter(AreaRepository):
    """
    Implementación concreta del repositorio de Áreas.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla AREA según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "AREA" in metadata.tables:
            return metadata.tables["AREA"]
        return Table(
            "AREA",
            metadata,
            Column("idArea", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(150), unique=True, nullable=False),
        )
    
    def add(self, area: Area) -> Area:
        """Agrega un área y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idArea=area.id,
                nombre=area.nombre
            ).returning(
                self.table.c.idArea,
                self.table.c.nombre
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return Area(
                id=row.idArea,
                nombre=row.nombre
            )
    
    def get_by_id(self, id: UUID) -> Optional[Area]:
        """Obtiene un área por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idArea,
                self.table.c.nombre
            ).where(self.table.c.idArea == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return Area(
                id=row.idArea,
                nombre=row.nombre
            )
    
    def get_by_nombre(self, nombre: str) -> Optional[Area]:
        """Obtiene un área por su nombre."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idArea,
                self.table.c.nombre
            ).where(self.table.c.nombre == nombre)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return Area(
                id=row.idArea,
                nombre=row.nombre
            )
    
    def get_all(self) -> List[Area]:
        """Obtiene todas las áreas."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idArea,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                Area(id=row.idArea, nombre=row.nombre)
                for row in rows
            ]
    
    def update(self, area: Area) -> Area:
        """Actualiza un área existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idArea == area.id
            ).values(
                nombre=area.nombre
            ).returning(
                self.table.c.idArea,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return Area(
                id=row.idArea,
                nombre=row.nombre
            )
    
    def delete(self, id: UUID) -> None:
        """Elimina un área por su ID."""
        with self._engine.connect() as conn:
            stmt = delete(self.table).where(self.table.c.idArea == id)
            conn.execute(stmt)
            conn.commit()