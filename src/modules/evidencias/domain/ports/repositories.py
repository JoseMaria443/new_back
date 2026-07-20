"""
Interfaz de repositorio para el módulo de evidencias.
"""
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional

from ..entities import Evidencia


class EvidenciaRepository(ABC):
    """
    Puerto para el repositorio de Evidencias.
    """

    @abstractmethod
    def add_with_tarea(self, evidencia: Evidencia, id_tarea: UUID) -> Evidencia:
        """
        Inserta la evidencia en ARCHIVO_EVIDENCIA y su vinculación en TAREA_EVIDENCIA
        en una sola transacción ACID.
        """
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[Evidencia]:
        """Obtiene una evidencia por su ID."""
        pass

    @abstractmethod
    def get_by_doi(self, doi: str) -> Optional[Evidencia]:
        """Obtiene una evidencia por su doi (único)."""
        pass

    @abstractmethod
    def get_all(self) -> List[Evidencia]:
        """Obtiene todas las evidencias."""
        pass

    @abstractmethod
    def get_by_tarea(self, id_tarea: UUID) -> List[Evidencia]:
        """Obtiene todas las evidencias vinculadas a una tarea."""
        pass
