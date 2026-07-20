"""
Casos de uso para el recurso Área.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.entities import Area
from ...domain.ports import AreaRepository
from ..dtos import AreaCreateRequest, AreaResponse


class AreaUseCases:
    """Casos de uso de negocio para la gestión de Áreas."""

    def __init__(self, repository: AreaRepository):
        self.repository = repository

    def create(self, request: AreaCreateRequest) -> AreaResponse:
        """Crea una nueva área."""
        area = Area(nombre=request.nombre)
        saved = self.repository.add(area)
        return AreaResponse.model_validate(saved)

    def get_by_id(self, area_id: UUID) -> Optional[AreaResponse]:
        """Obtiene un área por su ID."""
        area = self.repository.get_by_id(area_id)
        if not area:
            return None
        return AreaResponse.model_validate(area)

    def get_all(self) -> List[AreaResponse]:
        """Obtiene todas las áreas."""
        areas = self.repository.get_all()
        return [AreaResponse.model_validate(a) for a in areas]

    def get_activos(self) -> List[AreaResponse]:
        """Obtiene solo las áreas activas."""
        areas = self.repository.get_activos()
        return [AreaResponse.model_validate(a) for a in areas]

    def set_archivado(self, area_id: UUID, archivado: bool) -> Optional[AreaResponse]:
        """Archiva o desarchiva un área."""
        area = self.repository.get_by_id(area_id)
        if not area:
            return None
        updated = self.repository.set_archivado(area_id, archivado)
        return AreaResponse.model_validate(updated)
