"""
Adaptador de persistencia para el repositorio de Cargos.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import Cargo
from ...domain.ports import CargoRepository
from shared.infrastructure.database.connection import DatabaseConnection


class CargoRepositoryAdapter(CargoRepository):
    """
    Implementación concreta del repositorio de Cargos.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla CARGO según el esquema SQL."""
        return Table(
            "CARGO",
            self._engine.metadata,
            Column("idCargo", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(100), unique=True, nullable=False),
        )
    
    def add(self, cargo: Cargo) -> Cargo:
        """Agrega un cargo y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idCargo=cargo.id,
                nombre=cargo.nombre
            ).returning(
                self.table.c.idCargo,
                self.table.c.nombre
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return Cargo(
                id=row.idCargo,
                nombre=row.nombre
            )
    
    def get_by_id(self, id: UUID) -> Optional[Cargo]:
        """Obtiene un cargo por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idCargo,
                self.table.c.nombre
            ).where(self.table.c.idCargo == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return Cargo(
                id=row.idCargo,
                nombre=row.nombre
            )
    
    def get_by_nombre(self, nombre: str) -> Optional[Cargo]:
        """Obtiene un cargo por su nombre."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idCargo,
                self.table.c.nombre
            ).where(self.table.c.nombre == nombre)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return Cargo(
                id=row.idCargo,
                nombre=row.nombre
            )
    
    def get_all(self) -> List[Cargo]:
        """Obtiene todos los cargos."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idCargo,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                Cargo(id=row.idCargo, nombre=row.nombre)
                for row in rows
            ]
    
    def update(self, cargo: Cargo) -> Cargo:
        """Actualiza un cargo existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idCargo == cargo.id
            ).values(
                nombre=cargo.nombre
            ).returning(
                self.table.c.idCargo,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return Cargo(
                id=row.idCargo,
                nombre=row.nombre
            )
    
    def delete(self, id: UUID) -> None:
        """Elimina un cargo por su ID."""
        with self._engine.connect() as conn:
            stmt = delete(self.table).where(self.table.c.idCargo == id)
            conn.execute(stmt)
            conn.commit()