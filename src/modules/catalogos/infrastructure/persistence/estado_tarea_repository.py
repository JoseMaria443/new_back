"""
Adaptador de persistencia para el repositorio de Estados de Tarea.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional

from sqlalchemy import Table, Column, String, insert, select, update, delete
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.engine import Engine

from ...domain.entities import EstadoTarea
from ...domain.ports import EstadoTareaRepository
from shared.infrastructure.database.connection import DatabaseConnection


class EstadoTareaRepositoryAdapter(EstadoTareaRepository):
    """
    Implementación concreta del repositorio de Estados de Tarea.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, engine: Optional[Engine] = None):
        self._engine = engine or DatabaseConnection.get_engine()
    
    @property
    def table(self) -> Table:
        """Define la tabla ESTADO_TAREA según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "ESTADO_TAREA" in metadata.tables:
            return metadata.tables["ESTADO_TAREA"]
        return Table(
            "ESTADO_TAREA",
            metadata,
            Column("idEstadoTarea", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(50), unique=True, nullable=False),
        )
    
    def add(self, estado: EstadoTarea) -> EstadoTarea:
        """Agrega un estado de tarea y retorna la entidad persistida."""
        with self._engine.connect() as conn:
            stmt = insert(self.table).values(
                idEstadoTarea=estado.id,
                nombre=estado.nombre
            ).returning(
                self.table.c.idEstadoTarea,
                self.table.c.nombre
            )
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return EstadoTarea(
                id=row.idEstadoTarea,
                nombre=row.nombre
            )
    
    def get_by_id(self, id: UUID) -> Optional[EstadoTarea]:
        """Obtiene un estado de tarea por su ID."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idEstadoTarea,
                self.table.c.nombre
            ).where(self.table.c.idEstadoTarea == id)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return EstadoTarea(
                id=row.idEstadoTarea,
                nombre=row.nombre
            )
    
    def get_by_nombre(self, nombre: str) -> Optional[EstadoTarea]:
        """Obtiene un estado de tarea por su nombre."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idEstadoTarea,
                self.table.c.nombre
            ).where(self.table.c.nombre == nombre)
            
            result = conn.execute(stmt)
            row = result.fetchone()
            
            if row is None:
                return None
            
            return EstadoTarea(
                id=row.idEstadoTarea,
                nombre=row.nombre
            )
    
    def get_all(self) -> List[EstadoTarea]:
        """Obtiene todos los estados de tarea."""
        with self._engine.connect() as conn:
            stmt = select(
                self.table.c.idEstadoTarea,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            rows = result.fetchall()
            
            return [
                EstadoTarea(id=row.idEstadoTarea, nombre=row.nombre)
                for row in rows
            ]
    
    def update(self, estado: EstadoTarea) -> EstadoTarea:
        """Actualiza un estado de tarea existente."""
        with self._engine.connect() as conn:
            stmt = update(self.table).where(
                self.table.c.idEstadoTarea == estado.id
            ).values(
                nombre=estado.nombre
            ).returning(
                self.table.c.idEstadoTarea,
                self.table.c.nombre
            )
            
            result = conn.execute(stmt)
            row = result.fetchone()
            conn.commit()
            
            return EstadoTarea(
                id=row.idEstadoTarea,
                nombre=row.nombre
            )