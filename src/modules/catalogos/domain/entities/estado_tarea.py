"""
Entidad EstadoTarea.
Representa el estado de una tarea (asignada, cancelada, retrasada, etc.).
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class EstadoTarea(BaseEntity):
    """
    Entidad que representa un estado de tarea.
    Mapeo 1:1 con la tabla ESTADO_TAREA del esquema SQL.
    """
    # idEstadoTarea -> id (heredado de BaseEntity)
    nombre: str  # VARCHAR(50) UNIQUE NOT NULL
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del estado no puede estar vacío")
        
        if len(self.nombre) > 50:
            raise ValueError("El nombre del estado no puede exceder 50 caracteres")