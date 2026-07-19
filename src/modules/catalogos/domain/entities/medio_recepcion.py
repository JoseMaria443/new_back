"""
Entidad MedioRecepcion.
Representa un medio de recepción de comunicados.
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class MedioRecepcion(BaseEntity):
    """
    Entidad que representa un medio de recepción.
    Mapeo 1:1 con la tabla MEDIO_RECEPCION del esquema SQL.
    """
    # idMedioRecepcion -> id (heredado de BaseEntity)
    nombre: str  # VARCHAR(100) UNIQUE NOT NULL
    archivado: bool = False
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del medio de recepción no puede estar vacío")
        
        if len(self.nombre) > 100:
            raise ValueError("El nombre del medio de recepción no puede exceder 100 caracteres")