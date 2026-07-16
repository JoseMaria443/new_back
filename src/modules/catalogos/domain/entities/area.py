"""
Entidad Area.
Representa un área de la universidad.
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class Area(BaseEntity):
    """
    Entidad que representa un área de la universidad.
    Mapeo 1:1 con la tabla AREA del esquema SQL.
    """
    # idArea -> id (heredado de BaseEntity)
    nombre: str  # VARCHAR(150) UNIQUE NOT NULL
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del área no puede estar vacío")
        
        if len(self.nombre) > 150:
            raise ValueError("El nombre del área no puede exceder 150 caracteres")