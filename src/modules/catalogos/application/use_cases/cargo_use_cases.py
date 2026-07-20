"""
Casos de uso para el recurso Cargo.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.entities import Cargo
from ...domain.ports import CargoRepository
from ..dtos import CargoCreateRequest, CargoResponse


class CargoUseCases:
    """Casos de uso de negocio para la gestión de Cargos."""

    def __init__(self, repository: CargoRepository):
        self.repository = repository

    def create(self, request: CargoCreateRequest) -> CargoResponse:
        """Crea un nuevo cargo."""
        cargo = Cargo(nombre=request.nombre)
        saved = self.repository.add(cargo)
        return CargoResponse.model_validate(saved)

    def get_by_id(self, cargo_id: UUID) -> Optional[CargoResponse]:
        """Obtiene un cargo por su ID."""
        cargo = self.repository.get_by_id(cargo_id)
        if not cargo:
            return None
        return CargoResponse.model_validate(cargo)

    def get_all(self) -> List[CargoResponse]:
        """Obtiene todos los cargos."""
        cargos = self.repository.get_all()
        return [CargoResponse.model_validate(c) for c in cargos]

    def get_activos(self) -> List[CargoResponse]:
        """Obtiene solo los cargos activos."""
        cargos = self.repository.get_activos()
        return [CargoResponse.model_validate(c) for c in cargos]

    def set_archivado(self, cargo_id: UUID, archivado: bool) -> Optional[CargoResponse]:
        """Archiva o desarchiva un cargo."""
        cargo = self.repository.get_by_id(cargo_id)
        if not cargo:
            return None
        updated = self.repository.set_archivado(cargo_id, archivado)
        return CargoResponse.model_validate(updated)
