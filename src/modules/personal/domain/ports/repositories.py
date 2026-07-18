"""
Interfaces de repositorios para el módulo de personal.
Definen los contratos que deben implementar los adaptadores de persistencia.
"""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional

from ..domain.entities import Empleado, HistorialEstatus


class EmpleadoRepository(ABC):
    """
    Puerto para el repositorio de Empleados.
    """
    
    @abstractmethod
    def add(self, empleado: Empleado) -> Empleado:
        """Agrega un empleado."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Empleado]:
        """Obtiene un empleado por ID."""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Empleado]:
        """Obtiene un empleado por email."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Empleado]:
        """Obtiene todos los empleados."""
        pass
    
    @abstractmethod
    def update(self, empleado: Empleado) -> Empleado:
        """Actualiza un empleado existente."""
        pass
    
    @abstractmethod
    def update_estatus(self, id: UUID, activo: bool, idEmpleadoModifica: UUID) -> Empleado:
        """
        Actualiza el estatus de un empleado y crea registro en HISTORIAL_ESTATUS.
        """
        pass
    
    @abstractmethod
    def get_cargos(self, idEmpleado: UUID) -> List[UUID]:
        """
        Obtiene los IDs de cargos asignados a un empleado.
        """
        pass


class HistorialEstatusRepository(ABC):
    """
    Puerto para el repositorio de Historial de Estatus.
    """
    
    @abstractmethod
    def add(self, historial: HistorialEstatus) -> HistorialEstatus:
        """Agrega un registro de historial."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[HistorialEstatus]:
        """Obtiene un registro de historial por ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[HistorialEstatus]:
        """Obtiene todos los registros de historial."""
        pass
    
    @abstractmethod
    def get_by_empleado(self, idEmpleado: UUID) -> List[HistorialEstatus]:
        """Obtiene el historial de estatus de un empleado."""
        pass