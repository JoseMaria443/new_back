"""
Repositorio base abstracto.
Define la interfaz común para todos los repositorios.
"""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Interfaz base para repositorios.
    Cada repositorio concreto implementa estas operaciones.
    """
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Agrega una entidad y retorna la entidad persistida."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        """Obtiene una entidad por su ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Obtiene todas las entidades."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Actualiza una entidad existente."""
        pass
    
    @abstractmethod
    def delete(self, id: UUID) -> None:
        """Elimina una entidad por su ID."""
        pass