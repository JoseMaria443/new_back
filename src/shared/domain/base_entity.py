"""
Entidad base para todos los objetos de dominio.
Proporciona una identidad única basada en UUID.
"""
from abc import ABC
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime
from typing import Any


@dataclass
class BaseEntity(ABC):
    """
    Clase base abstracta para todas las entidades del dominio.
    Proporciona un identificador único y funcionalidad básica de igualdad.
    """
    id: UUID = field(default_factory=uuid4, kw_only=True)
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)