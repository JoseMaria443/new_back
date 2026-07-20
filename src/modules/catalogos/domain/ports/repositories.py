"""
Interfaces de repositorios para el módulo de catálogos.
Definen los contratos que deben implementar los adaptadores de persistencia.
"""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional

from ..entities import (
    Area,
    Cargo,
    TipoComunicado,
    MedioRecepcion,
    RolDestinatario,
    RolResponsable,
    EstadoTarea,
)


class AreaRepository(ABC):
    """
    Puerto para el repositorio de Áreas.
    """
    
    @abstractmethod
    def add(self, area: Area) -> Area:
        """Agrega un área."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Area]:
        """Obtiene un área por ID."""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Area]:
        """Obtiene un área por nombre."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Area]:
        """Obtiene todas las áreas."""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[Area]:
        """Obtiene solo los registros con archivado == False."""
        pass
    
    @abstractmethod
    def set_archivado(self, id: UUID, archivado: bool) -> Area:
        """Archiva o desarchiva un registro (único método para ocultar/mostrar)."""
        pass


class CargoRepository(ABC):
    """
    Puerto para el repositorio de Cargos.
    """
    
    @abstractmethod
    def add(self, cargo: Cargo) -> Cargo:
        """Agrega un cargo."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Cargo]:
        """Obtiene un cargo por ID."""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[Cargo]:
        """Obtiene un cargo por nombre."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Cargo]:
        """Obtiene todos los cargos."""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[Cargo]:
        """Obtiene solo los registros con archivado == False."""
        pass
    
    @abstractmethod
    def set_archivado(self, id: UUID, archivado: bool) -> Cargo:
        """Archiva o desarchiva un registro (único método para ocultar/mostrar)."""
        pass


class TipoComunicadoRepository(ABC):
    """
    Puerto para el repositorio de Tipos de Comunicado.
    """
    
    @abstractmethod
    def add(self, tipo: TipoComunicado) -> TipoComunicado:
        """Agrega un tipo de comunicado."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[TipoComunicado]:
        """Obtiene un tipo de comunicado por ID."""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[TipoComunicado]:
        """Obtiene un tipo de comunicado por nombre."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[TipoComunicado]:
        """Obtiene todos los tipos de comunicado."""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[TipoComunicado]:
        """Obtiene solo los registros con archivado == False."""
        pass
    
    @abstractmethod
    def set_archivado(self, id: UUID, archivado: bool) -> TipoComunicado:
        """Archiva o desarchiva un registro (único método para ocultar/mostrar)."""
        pass


class MedioRecepcionRepository(ABC):
    """
    Puerto para el repositorio de Medios de Recepción.
    """
    
    @abstractmethod
    def add(self, medio: MedioRecepcion) -> MedioRecepcion:
        """Agrega un medio de recepción."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[MedioRecepcion]:
        """Obtiene un medio de recepción por ID."""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[MedioRecepcion]:
        """Obtiene un medio de recepción por nombre."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[MedioRecepcion]:
        """Obtiene todos los medios de recepción."""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[MedioRecepcion]:
        """Obtiene solo los registros con archivado == False."""
        pass
    
    @abstractmethod
    def set_archivado(self, id: UUID, archivado: bool) -> MedioRecepcion:
        """Archiva o desarchiva un registro (único método para ocultar/mostrar)."""
        pass


class RolDestinatarioRepository(ABC):
    """
    Puerto para el repositorio de Roles de Destinatario.
    """
    
    @abstractmethod
    def add(self, rol: RolDestinatario) -> RolDestinatario:
        """Agrega un rol de destinatario."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[RolDestinatario]:
        """Obtiene un rol de destinatario por ID."""
        pass
    
    @abstractmethod
    def get_by_descripcion(self, descripcion: str) -> Optional[RolDestinatario]:
        """Obtiene un rol de destinatario por descripción."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[RolDestinatario]:
        """Obtiene todos los roles de destinatario."""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[RolDestinatario]:
        """Obtiene solo los registros con archivado == False."""
        pass
    
    @abstractmethod
    def set_archivado(self, id: UUID, archivado: bool) -> RolDestinatario:
        """Archiva o desarchiva un registro (único método para ocultar/mostrar)."""
        pass


class RolResponsableRepository(ABC):
    """
    Puerto para el repositorio de Roles de Responsable.
    """
    
    @abstractmethod
    def add(self, rol: RolResponsable) -> RolResponsable:
        """Agrega un rol de responsable."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[RolResponsable]:
        """Obtiene un rol de responsable por ID."""
        pass
    
    @abstractmethod
    def get_by_descripcion(self, descripcion: str) -> Optional[RolResponsable]:
        """Obtiene un rol de responsable por descripción."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[RolResponsable]:
        """Obtiene todos los roles de responsable."""
        pass
    
    @abstractmethod
    def get_activos(self) -> List[RolResponsable]:
        """Obtiene solo los registros con archivado == False."""
        pass
    
    @abstractmethod
    def set_archivado(self, id: UUID, archivado: bool) -> RolResponsable:
        """Archiva o desarchiva un registro (único método para ocultar/mostrar)."""
        pass


class EstadoTareaRepository(ABC):
    """
    Puerto para el repositorio de Estados de Tarea.
    """
    
    @abstractmethod
    def add(self, estado: EstadoTarea) -> EstadoTarea:
        """Agrega un estado de tarea."""
        pass
    
    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[EstadoTarea]:
        """Obtiene un estado de tarea por ID."""
        pass
    
    @abstractmethod
    def get_by_nombre(self, nombre: str) -> Optional[EstadoTarea]:
        """Obtiene un estado de tarea por nombre."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[EstadoTarea]:
        """Obtiene todos los estados de tarea."""
        pass
    
    @abstractmethod
    def update(self, estado: EstadoTarea) -> EstadoTarea:
        """Actualiza un estado de tarea."""
        pass