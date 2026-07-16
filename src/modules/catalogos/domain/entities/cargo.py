"""
Entidad Cargo.
Representa un cargo funcional en la universidad.
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class Cargo(BaseEntity):
    """
    Entidad que representa un cargo funcional.
    Mapeo 1:1 con la tabla CARGO del esquema SQL.
    """
    # idCargo -> id (heredado de BaseEntity)
    nombre: str  # VARCHAR(100) UNIQUE NOT NULL
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del cargo no puede estar vacío")
        
        if len(self.nombre) > 100:
            raise ValueError("El nombre del cargo no puede exceder 100 caracteres")