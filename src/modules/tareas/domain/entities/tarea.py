"""
Entidad Tarea.
Representa una tarea derivada de un comunicado.
Mapeo 1:1 con la tabla TAREA del esquema SQL.
"""
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import Optional

from shared.domain.base_entity import BaseEntity


@dataclass
class Tarea(BaseEntity):
    # idTarea -> id (heredado de BaseEntity)
    idComunicado: UUID  # FK COMUNICADO
    idEstadoTarea: UUID  # FK ESTADO_TAREA
    resumenActividad: str  # TEXT NOT NULL
    descripcion: str  # TEXT NOT NULL
    fechaEntrega: datetime  # TIMESTAMP WITH TIME ZONE NOT NULL
    fechaRegistro: Optional[datetime] = field(default=None)  # la asigna el servidor/DB

    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.resumenActividad or not self.resumenActividad.strip():
            raise ValueError("El resumenActividad no puede estar vacío")

        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")