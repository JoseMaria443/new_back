"""
Adaptador de persistencia para el repositorio de Empleados.
Usa SQLAlchemy Core con SQL crudo.
"""
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from sqlalchemy import Table, Column, String, Boolean, insert, select, update
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Session

from ...domain.entities import Empleado, HistorialEstatus, AccionHistorial
from ...domain.ports import EmpleadoRepository, HistorialEstatusRepository
from shared.infrastructure.database.connection import DatabaseConnection


class EmpleadoRepositoryAdapter(EmpleadoRepository):
    """
    Implementación concreta del repositorio de Empleados.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, session: Optional[Session] = None):
        self._session = session
    
    @property
    def table(self) -> Table:
        """Define la tabla EMPLEADO según el esquema SQL."""
        return Table(
            "EMPLEADO",
            DatabaseConnection.get_engine().metadata,
            Column("idEmpleado", PG_UUID(as_uuid=True), primary_key=True),
            Column("nombre", String(100), nullable=False),
            Column("email", String(150), unique=True, nullable=False),
            Column("idArea", PG_UUID(as_uuid=True), nullable=False),
            Column("activo", Boolean, default=True),
            Column("fechaRegistro", String),  # Se maneja como TIMESTAMP
            Column("password_hash", String(255)),  # No está en el SQL original
        )
    
    def add(self, empleado: Empleado) -> Empleado:
        """Agrega un empleado y retorna la entidad persistida."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = insert(self.table).values(
            idEmpleado=empleado.id,
            nombre=empleado.nombre,
            email=empleado.email,
            idArea=empleado.idArea,
            activo=empleado.activo,
            password_hash=empleado.password_hash
        ).returning(
            self.table.c.idEmpleado,
            self.table.c.nombre,
            self.table.c.email,
            self.table.c.idArea,
            self.table.c.activo,
            self.table.c.fechaRegistro,
        )
        
        result = session.execute(stmt)
        row = result.fetchone()
        
        return Empleado(
            id=row.idEmpleado,
            nombre=row.nombre,
            email=row.email,
            idArea=row.idArea,
            activo=row.activo,
            fechaRegistro=row.fechaRegistro,
            password_hash=empleado.password_hash,
        )
    
    def get_by_id(self, id: UUID) -> Optional[Empleado]:
        """Obtiene un empleado por su ID."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = select(
            self.table.c.idEmpleado,
            self.table.c.nombre,
            self.table.c.email,
            self.table.c.idArea,
            self.table.c.activo,
            self.table.c.fechaRegistro,
        ).where(self.table.c.idEmpleado == id)
        
        result = session.execute(stmt)
        row = result.fetchone()
        
        if row is None:
            return None
        
        return Empleado(
            id=row.idEmpleado,
            nombre=row.nombre,
            email=row.email,
            idArea=row.idArea,
            activo=row.activo,
            fechaRegistro=row.fechaRegistro,
            password_hash=None,  # No se expone el hash
        )
    
    def get_by_email(self, email: str) -> Optional[Empleado]:
        """Obtiene un empleado por su email."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = select(
            self.table.c.idEmpleado,
            self.table.c.nombre,
            self.table.c.email,
            self.table.c.idArea,
            self.table.c.activo,
            self.table.c.fechaRegistro,
            self.table.c.password_hash,
        ).where(self.table.c.email == email)
        
        result = session.execute(stmt)
        row = result.fetchone()
        
        if row is None:
            return None
        
        return Empleado(
            id=row.idEmpleado,
            nombre=row.nombre,
            email=row.email,
            idArea=row.idArea,
            activo=row.activo,
            fechaRegistro=row.fechaRegistro,
            password_hash=row.password_hash,
        )
    
    def get_all(self) -> List[Empleado]:
        """Obtiene todos los empleados."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = select(
            self.table.c.idEmpleado,
            self.table.c.nombre,
            self.table.c.email,
            self.table.c.idArea,
            self.table.c.activo,
            self.table.c.fechaRegistro,
        )
        
        result = session.execute(stmt)
        rows = result.fetchall()
        
        return [
            Empleado(
                id=row.idEmpleado,
                nombre=row.nombre,
                email=row.email,
                idArea=row.idArea,
                activo=row.activo,
                fechaRegistro=row.fechaRegistro,
                password_hash=None,
            )
            for row in rows
        ]
    
    def update(self, empleado: Empleado) -> Empleado:
        """Actualiza un empleado existente."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = update(self.table).where(
            self.table.c.idEmpleado == empleado.id
        ).values(
            nombre=empleado.nombre,
            email=empleado.email,
            idArea=empleado.idArea,
            activo=empleado.activo,
        ).returning(
            self.table.c.idEmpleado,
            self.table.c.nombre,
            self.table.c.email,
            self.table.c.idArea,
            self.table.c.activo,
            self.table.c.fechaRegistro,
        )
        
        result = session.execute(stmt)
        row = result.fetchone()
        
        return Empleado(
            id=row.idEmpleado,
            nombre=row.nombre,
            email=row.email,
            idArea=row.idArea,
            activo=row.activo,
            fechaRegistro=row.fechaRegistro,
            password_hash=empleado.password_hash,
        )
    
    def update_estatus(
        self, 
        id: UUID, 
        activo: bool, 
        idEmpleadoModifica: UUID
    ) -> Empleado:
        """
        Actualiza el estatus de un empleado y crea registro en HISTORIAL_ESTATUS.
        Usa transacción ACID.
        """
        with DatabaseConnection.get_session() as session:
            # Actualizar el estatus del empleado
            stmt = update(self.table).where(
                self.table.c.idEmpleado == id
            ).values(
                activo=activo
            ).returning(
                self.table.c.idEmpleado,
                self.table.c.nombre,
                self.table.c.email,
                self.table.c.idArea,
                self.table.c.activo,
                self.table.c.fechaRegistro,
            )
            
            result = session.execute(stmt)
            row = result.fetchone()
            
            # Crear registro en HISTORIAL_ESTATUS
            historial_repo = HistorialEstatusRepositoryAdapter(session)
            accion = AccionHistorial.DESACTIVACION if not activo else AccionHistorial.REACTIVACION
            
            historial = HistorialEstatus(
                idEmpleadoAfectado=id,
                idEmpleadoModifica=idEmpleadoModifica,
                accion=accion,
            )
            historial_repo.add(historial)
            
            return Empleado(
                id=row.idEmpleado,
                nombre=row.nombre,
                email=row.email,
                idArea=row.idArea,
                activo=row.activo,
                fechaRegistro=row.fechaRegistro,
                password_hash=None,
            )
    
    def get_cargos(self, idEmpleado: UUID) -> List[UUID]:
        """
        Obtiene los IDs de cargos asignados a un empleado.
        """
        session = self._session or next(DatabaseConnection.get_session())
        
        empleado_cargo_table = Table(
            "EMPLEADO_CARGO",
            DatabaseConnection.get_engine().metadata,
            Column("idEmpleado", PG_UUID(as_uuid=True), primary_key=True),
            Column("idCargo", PG_UUID(as_uuid=True), primary_key=True),
        )
        
        stmt = select(empleado_cargo_table.c.idCargo).where(
            empleado_cargo_table.c.idEmpleado == idEmpleado
        )
        
        result = session.execute(stmt)
        rows = result.fetchall()
        
        return [row.idCargo for row in rows]


class HistorialEstatusRepositoryAdapter(HistorialEstatusRepository):
    """
    Implementación concreta del repositorio de Historial de Estatus.
    Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
    """
    
    def __init__(self, session: Optional[Session] = None):
        self._session = session
    
    @property
    def table(self) -> Table:
        """Define la tabla HISTORIAL_ESTATUS según el esquema SQL."""
        return Table(
            "HISTORIAL_ESTATUS",
            DatabaseConnection.get_engine().metadata,
            Column("idHistorial", PG_UUID(as_uuid=True), primary_key=True),
            Column("idEmpleadoAfectado", PG_UUID(as_uuid=True), nullable=False),
            Column("idEmpleadoModifica", PG_UUID(as_uuid=True), nullable=False),
            Column("accion", String(50), nullable=False),
            Column("fechaRegistro", String),
        )
    
    def add(self, historial: HistorialEstatus) -> HistorialEstatus:
        """Agrega un registro de historial y retorna la entidad persistida."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = insert(self.table).values(
            idHistorial=historial.id,
            idEmpleadoAfectado=historial.idEmpleadoAfectado,
            idEmpleadoModifica=historial.idEmpleadoModifica,
            accion=historial.accion.value,
        ).returning(
            self.table.c.idHistorial,
            self.table.c.idEmpleadoAfectado,
            self.table.c.idEmpleadoModifica,
            self.table.c.accion,
            self.table.c.fechaRegistro,
        )
        
        result = session.execute(stmt)
        row = result.fetchone()
        
        return HistorialEstatus(
            id=row.idHistorial,
            idEmpleadoAfectado=row.idEmpleadoAfectado,
            idEmpleadoModifica=row.idEmpleadoModifica,
            accion=AccionHistorial(row.accion),
            fechaRegistro=row.fechaRegistro,
        )
    
    def get_by_id(self, id: UUID) -> Optional[HistorialEstatus]:
        """Obtiene un registro de historial por su ID."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = select(
            self.table.c.idHistorial,
            self.table.c.idEmpleadoAfectado,
            self.table.c.idEmpleadoModifica,
            self.table.c.accion,
            self.table.c.fechaRegistro,
        ).where(self.table.c.idHistorial == id)
        
        result = session.execute(stmt)
        row = result.fetchone()
        
        if row is None:
            return None
        
        return HistorialEstatus(
            id=row.idHistorial,
            idEmpleadoAfectado=row.idEmpleadoAfectado,
            idEmpleadoModifica=row.idEmpleadoModifica,
            accion=AccionHistorial(row.accion),
            fechaRegistro=row.fechaRegistro,
        )
    
    def get_all(self) -> List[HistorialEstatus]:
        """Obtiene todos los registros de historial."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = select(
            self.table.c.idHistorial,
            self.table.c.idEmpleadoAfectado,
            self.table.c.idEmpleadoModifica,
            self.table.c.accion,
            self.table.c.fechaRegistro,
        )
        
        result = session.execute(stmt)
        rows = result.fetchall()
        
        return [
            HistorialEstatus(
                id=row.idHistorial,
                idEmpleadoAfectado=row.idEmpleadoAfectado,
                idEmpleadoModifica=row.idEmpleadoModifica,
                accion=AccionHistorial(row.accion),
                fechaRegistro=row.fechaRegistro,
            )
            for row in rows
        ]
    
    def get_by_empleado(self, idEmpleado: UUID) -> List[HistorialEstatus]:
        """Obtiene el historial de estatus de un empleado."""
        session = self._session or next(DatabaseConnection.get_session())
        
        stmt = select(
            self.table.c.idHistorial,
            self.table.c.idEmpleadoAfectado,
            self.table.c.idEmpleadoModifica,
            self.table.c.accion,
            self.table.c.fechaRegistro,
        ).where(self.table.c.idEmpleadoAfectado == idEmpleado)
        
        result = session.execute(stmt)
        rows = result.fetchall()
        
        return [
            HistorialEstatus(
                id=row.idHistorial,
                idEmpleadoAfectado=row.idEmpleadoAfectado,
                idEmpleadoModifica=row.idEmpleadoModifica,
                accion=AccionHistorial(row.accion),
                fechaRegistro=row.fechaRegistro,
            )
            for row in rows
        ]