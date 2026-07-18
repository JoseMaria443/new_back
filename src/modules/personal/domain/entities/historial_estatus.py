"""
Entidad HistorialEstatus.
Representa un registro de cambio de estatus de un empleado.
"""
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import Optional
from enum import Enum

from shared.domain.base_entity import BaseEntity


class AccionHistorial(str, Enum):
    """Tipos de acciones de historial."""
    DESACTIVACION = "DESACTIVACION"
    REACTIVACION = "REACTIVACION"


@dataclass
class HistorialEstatus(BaseEntity):
    """
    Entidad que representa un registro de historial de estatus.
    Mapeo 1:1 con la tabla HISTORIAL_ESTATUS del esquema SQL.
    """
    # idHistorial -> id (heredado de BaseEntity)
    idEmpleadoAfectado: UUID  # UUID NOT NULL, FK a EMPLEADO
    idEmpleadoModifica: UUID  # UUID NOT NULL, FK a EMPLEADO
    accion: AccionHistorial  # VARCHAR(50) CHECK (accion IN ('DESACTIVACION', 'REACTIVACION'))
    fechaRegistro: Optional[datetime] = field(default=None)  # TIMESTAMP WITH TIME ZONE
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.idEmpleadoAfectado:
            raise ValueError("El idEmpleadoAfectado es requerido")
        
        if not self.idEmpleadoModifica:
            raise ValueError("El idEmpleadoModifica es requerido")
        
        if not self.accion:
            raise ValueError("La acción es requerida")