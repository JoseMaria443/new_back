"""
Entidad TipoComunicado.
Representa un tipo de comunicado (Oficio, Circular, Informativo, etc.).
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class TipoComunicado(BaseEntity):
    """
    Entidad que representa un tipo de comunicado.
    Mapeo 1:1 con la tabla TIPO_COMUNICADO del esquema SQL.
    """
    # idTipoComunicado -> id (heredado de BaseEntity)
    nombre: str  # VARCHAR(100) UNIQUE NOT NULL
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del tipo de comunicado no puede estar vacío")
        
        if len(self.nombre) > 100:
            raise ValueError("El nombre del tipo de comunicado no puede exceder 100 caracteres")