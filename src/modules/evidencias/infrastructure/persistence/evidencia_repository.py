"""
Adaptador de persistencia para el repositorio de Evidencias.
Usa SQLAlchemy Core con SQL crudo, respetando el esquema existente.
"""
from uuid import UUID
from typing import List, Optional
from contextlib import contextmanager

from sqlalchemy import Table, Column, String, Text, DateTime, insert, select
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Session

from ...domain.entities import Evidencia
from ...domain.ports import EvidenciaRepository
from shared.infrastructure.database.connection import DatabaseConnection


class EvidenciaRepositoryAdapter(EvidenciaRepository):
    """
    Implementación concreta del repositorio de Evidencias.
    """

    def __init__(self, session: Optional[Session] = None):
        self._session = session

    @contextmanager
    def _get_session(self):
        if self._session is not None:
            yield self._session
        else:
            with DatabaseConnection.get_session() as session:
                yield session

    @property
    def table(self) -> Table:
        """Define la tabla ARCHIVO_EVIDENCIA según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "ARCHIVO_EVIDENCIA" in metadata.tables:
            return metadata.tables["ARCHIVO_EVIDENCIA"]
        return Table(
            "ARCHIVO_EVIDENCIA",
            metadata,
            Column("idArchivoEvidencia", PG_UUID(as_uuid=True), primary_key=True),
            Column("doi", String(100), unique=True, nullable=False),
            Column("descripcion", Text, nullable=False),
            Column("urlArchivo", String(500), nullable=False),
            Column("nombreOriginal", String(255), nullable=False),
            Column("idElaborador", PG_UUID(as_uuid=True), nullable=False),
            Column("fechaRegistro", DateTime(timezone=True)),
        )

    @property
    def tarea_evidencia_table(self) -> Table:
        """Define la tabla puente TAREA_EVIDENCIA según el esquema SQL."""
        metadata = DatabaseConnection.get_metadata()
        if "TAREA_EVIDENCIA" in metadata.tables:
            return metadata.tables["TAREA_EVIDENCIA"]
        return Table(
            "TAREA_EVIDENCIA",
            metadata,
            Column("idTarea", PG_UUID(as_uuid=True), primary_key=True),
            Column("idArchivoEvidencia", PG_UUID(as_uuid=True), primary_key=True),
        )

    def _row_to_evidencia(self, row) -> Evidencia:
        return Evidencia(
            id=row.idArchivoEvidencia,
            doi=row.doi,
            descripcion=row.descripcion,
            urlArchivo=row.urlArchivo,
            nombreOriginal=row.nombreOriginal,
            idElaborador=row.idElaborador,
            fechaRegistro=row.fechaRegistro,
        )

    def add_with_tarea(self, evidencia: Evidencia, id_tarea: UUID) -> Evidencia:
        """
        Inserta la evidencia en ARCHIVO_EVIDENCIA y la relación en TAREA_EVIDENCIA
        en una sola transacción ACID.
        """
        with self._get_session() as session:
            try:
                stmt = insert(self.table).values(
                    idArchivoEvidencia=evidencia.id,
                    doi=evidencia.doi,
                    descripcion=evidencia.descripcion,
                    urlArchivo=evidencia.urlArchivo,
                    nombreOriginal=evidencia.nombreOriginal,
                    idElaborador=evidencia.idElaborador,
                ).returning(
                    self.table.c.idArchivoEvidencia,
                    self.table.c.doi,
                    self.table.c.descripcion,
                    self.table.c.urlArchivo,
                    self.table.c.nombreOriginal,
                    self.table.c.idElaborador,
                    self.table.c.fechaRegistro,
                )
                result = session.execute(stmt)
                row = result.fetchone()

                # Insertar en la tabla puente TAREA_EVIDENCIA
                session.execute(
                    insert(self.tarea_evidencia_table).values(
                        idTarea=id_tarea,
                        idArchivoEvidencia=row.idArchivoEvidencia,
                    )
                )

                if self._session is not None:
                    session.commit()

                return self._row_to_evidencia(row)
            except Exception:
                session.rollback()
                raise

    def get_by_id(self, id: UUID) -> Optional[Evidencia]:
        with self._get_session() as session:
            stmt = select(self.table).where(self.table.c.idArchivoEvidencia == id)
            row = session.execute(stmt).fetchone()
            if row is None:
                return None
            return self._row_to_evidencia(row)

    def get_by_doi(self, doi: str) -> Optional[Evidencia]:
        with self._get_session() as session:
            stmt = select(self.table).where(self.table.c.doi == doi)
            row = session.execute(stmt).fetchone()
            if row is None:
                return None
            return self._row_to_evidencia(row)

    def get_all(self) -> List[Evidencia]:
        with self._get_session() as session:
            stmt = select(self.table)
            rows = session.execute(stmt).fetchall()
            return [self._row_to_evidencia(row) for row in rows]

    def get_by_tarea(self, id_tarea: UUID) -> List[Evidencia]:
        with self._get_session() as session:
            stmt = (
                select(self.table)
                .select_from(
                    self.table.join(
                        self.tarea_evidencia_table,
                        self.table.c.idArchivoEvidencia == self.tarea_evidencia_table.c.idArchivoEvidencia,
                    )
                )
                .where(self.tarea_evidencia_table.c.idTarea == id_tarea)
            )
            rows = session.execute(stmt).fetchall()
            return [self._row_to_evidencia(row) for row in rows]
