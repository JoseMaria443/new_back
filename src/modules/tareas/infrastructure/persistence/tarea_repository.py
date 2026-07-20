"""
Adaptador de persistencia para el repositorio de Tareas.
Usa SQLAlchemy Core, respetando el esquema existente.
"""
from uuid import UUID
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from sqlalchemy import Table, Column, String, DateTime, Text, insert, select, update
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Session

from ...domain.entities import Tarea
from ...domain.ports import TareaRepository
from shared.infrastructure.database.connection import DatabaseConnection


class TareaRepositoryAdapter(TareaRepository):
    """
    Implementación concreta del repositorio de Tareas.
    """

    def __init__(self, session: Optional[Session] = None):
        self._session = session

    @contextmanager
    def _get_session(self):
        """
        Provee una sesión: reutiliza la inyectada (self._session) si existe,
        o abre y cierra una nueva con manejo ACID (commit/rollback) si no.
        """
        if self._session is not None:
            yield self._session
        else:
            with DatabaseConnection.get_session() as session:
                yield session

    @property
    def table(self) -> Table:
        """Define la tabla TAREA según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "TAREA" in metadata.tables:
            return metadata.tables["TAREA"]
        return Table(
            "TAREA",
            metadata,
            Column("idTarea", PG_UUID(as_uuid=True), primary_key=True),
            Column("idComunicado", PG_UUID(as_uuid=True), nullable=False),
            Column("idEstadoTarea", PG_UUID(as_uuid=True), nullable=False),
            Column("resumenActividad", Text, nullable=False),
            Column("descripcion", Text, nullable=False),
            Column("fechaEntrega", DateTime(timezone=True), nullable=False),
            Column("fechaRegistro", DateTime(timezone=True)),
        )

    @property
    def responsable_table(self) -> Table:
        """Define la tabla TAREA_RESPONSABLE según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "TAREA_RESPONSABLE" in metadata.tables:
            return metadata.tables["TAREA_RESPONSABLE"]
        return Table(
            "TAREA_RESPONSABLE",
            metadata,
            Column("idTarea", PG_UUID(as_uuid=True), primary_key=True),
            Column("idResponsable", PG_UUID(as_uuid=True), primary_key=True),
            Column("idRolResponsable", PG_UUID(as_uuid=True), nullable=False),
            Column("fechaRegistro", DateTime(timezone=True)),
        )

    def _row_to_tarea(self, row) -> Tarea:
        return Tarea(
            id=row.idTarea,
            idComunicado=row.idComunicado,
            idEstadoTarea=row.idEstadoTarea,
            resumenActividad=row.resumenActividad,
            descripcion=row.descripcion,
            fechaEntrega=row.fechaEntrega,
            fechaRegistro=row.fechaRegistro,
        )

    def add_with_responsables(
        self, tarea: Tarea, responsables: List[Dict[str, Any]]
    ) -> Tarea:
        """
        Inserta la tarea y sus responsables en una sola transacción ACID
        (commit único al final, rollback si cualquier paso falla).
        fechaRegistro NO se envía: la asigna la base de datos.
        """
        with self._get_session() as session:
            try:
                stmt = insert(self.table).values(
                    idTarea=tarea.id,
                    idComunicado=tarea.idComunicado,
                    idEstadoTarea=tarea.idEstadoTarea,
                    resumenActividad=tarea.resumenActividad,
                    descripcion=tarea.descripcion,
                    fechaEntrega=tarea.fechaEntrega,
                ).returning(
                    self.table.c.idTarea,
                    self.table.c.idComunicado,
                    self.table.c.idEstadoTarea,
                    self.table.c.resumenActividad,
                    self.table.c.descripcion,
                    self.table.c.fechaEntrega,
                    self.table.c.fechaRegistro,
                )
                result = session.execute(stmt)
                row = result.fetchone()

                for resp in responsables:
                    session.execute(
                        insert(self.responsable_table).values(
                            idTarea=row.idTarea,
                            idResponsable=resp["idResponsable"],
                            idRolResponsable=resp["idRolResponsable"],
                        )
                    )

                if self._session is not None:
                    session.commit()

                return self._row_to_tarea(row)
            except Exception:
                session.rollback()
                raise

    def get_by_id(self, id: UUID) -> Optional[Tarea]:
        with self._get_session() as session:
            stmt = select(self.table).where(self.table.c.idTarea == id)
            row = session.execute(stmt).fetchone()
            if row is None:
                return None
            return self._row_to_tarea(row)

    def get_all(self) -> List[Tarea]:
        with self._get_session() as session:
            stmt = select(self.table)
            rows = session.execute(stmt).fetchall()
            return [self._row_to_tarea(row) for row in rows]

    def get_responsables(self, id_tarea: UUID) -> List[Dict[str, Any]]:
        with self._get_session() as session:
            stmt = select(self.responsable_table).where(
                self.responsable_table.c.idTarea == id_tarea
            )
            rows = session.execute(stmt).fetchall()
            return [
                {
                    "idResponsable": row.idResponsable,
                    "idRolResponsable": row.idRolResponsable,
                }
                for row in rows
            ]

    def is_responsable(self, id_tarea: UUID, id_empleado: UUID) -> bool:
        with self._get_session() as session:
            stmt = select(self.responsable_table).where(
                self.responsable_table.c.idTarea == id_tarea,
                self.responsable_table.c.idResponsable == id_empleado,
            )
            row = session.execute(stmt).fetchone()
            return row is not None

    def update_estado(self, id_tarea: UUID, id_estado_tarea: UUID) -> Tarea:
        with self._get_session() as session:
            stmt = update(self.table).where(
                self.table.c.idTarea == id_tarea
            ).values(
                idEstadoTarea=id_estado_tarea
            ).returning(
                self.table.c.idTarea,
                self.table.c.idComunicado,
                self.table.c.idEstadoTarea,
                self.table.c.resumenActividad,
                self.table.c.descripcion,
                self.table.c.fechaEntrega,
                self.table.c.fechaRegistro,
            )
            result = session.execute(stmt)
            row = result.fetchone()
            return self._row_to_tarea(row)