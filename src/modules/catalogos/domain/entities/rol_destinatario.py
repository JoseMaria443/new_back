"""
Entidad RolDestinatario.
Representa el rol de un destinatario en un comunicado.
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class RolDestinatario(BaseEntity):
    """
    Entidad que representa un rol de destinatario.
    Mapeo 1:1 con la tabla ROL_DESTINATARIO del esquema SQL.
    """
    # idRolDestinatario -> id (heredado de BaseEntity)
    descripcionRol: str  # VARCHAR(100) UNIQUE NOT NULL
    archivado: bool = False
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.descripcionRol or not self.descripcionRol.strip():
            raise ValueError("La descripción del rol no puede estar vacía")
        
        if len(self.descripcionRol) > 100:
            raise ValueError("La descripción del rol no puede exceder 100 caracteres")