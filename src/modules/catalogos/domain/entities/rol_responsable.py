"""
Entidad RolResponsable.
Representa el rol de un responsable en una tarea.
"""
from dataclasses import dataclass
from uuid import UUID

from shared.domain.base_entity import BaseEntity


@dataclass
class RolResponsable(BaseEntity):
    """
    Entidad que representa un rol de responsable.
    Mapeo 1:1 con la tabla ROL_RESPONSABLE del esquema SQL.
    """
    # idRolResponsable -> id (heredado de BaseEntity)
    descripcionRol: str  # VARCHAR(100) UNIQUE NOT NULL
    archivado: bool = False
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.descripcionRol or not self.descripcionRol.strip():
            raise ValueError("La descripción del rol no puede estar vacía")
        
        if len(self.descripcionRol) > 100:
            raise ValueError("La descripción del rol no puede exceder 100 caracteres")