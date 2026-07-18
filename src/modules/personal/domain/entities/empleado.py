"""
Entidad Empleado.
Representa un trabajador de la universidad.
"""
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import Optional

from shared.domain.base_entity import BaseEntity


@dataclass
class Empleado(BaseEntity):
    """
    Entidad que representa un empleado.
    Mapeo 1:1 con la tabla EMPLEADO del esquema SQL.
    """
    # idEmpleado -> id (heredado de BaseEntity)
    nombre: str  # VARCHAR(100) NOT NULL
    email: str  # VARCHAR(150) UNIQUE NOT NULL
    idArea: UUID  # UUID NOT NULL, FK a AREA
    activo: bool = field(default=True)  # BOOLEAN DEFAULT TRUE
    fechaRegistro: Optional[datetime] = field(default=None)  # TIMESTAMP WITH TIME ZONE
    password_hash: Optional[str] = field(default=None)  # No viene del SQL, pero se requiere para auth
    
    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del empleado no puede estar vacío")
        
        if len(self.nombre) > 100:
            raise ValueError("El nombre del empleado no puede exceder 100 caracteres")
        
        if not self.email or not self.email.strip():
            raise ValueError("El email no puede estar vacío")
        
        if len(self.email) > 150:
            raise ValueError("El email no puede exceder 150 caracteres")
        
        if not self.password_hash:
            raise ValueError("El hash de contraseña es requerido")