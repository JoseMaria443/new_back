"""
Casos de uso para el recurso MedioRecepcion.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.entities import MedioRecepcion
from ...domain.ports import MedioRecepcionRepository
from ..dtos import MedioRecepcionCreateRequest, MedioRecepcionResponse


class MedioRecepcionUseCases:
    """Casos de uso de negocio para la gestión de Medios de Recepción."""

    def __init__(self, repository: MedioRecepcionRepository):
        self.repository = repository

    def create(self, request: MedioRecepcionCreateRequest) -> MedioRecepcionResponse:
        """Crea un nuevo medio de recepción."""
        medio = MedioRecepcion(nombre=request.nombre)
        saved = self.repository.add(medio)
        return MedioRecepcionResponse.model_validate(saved)

    def get_by_id(self, medio_id: UUID) -> Optional[MedioRecepcionResponse]:
        """Obtiene un medio de recepción por su ID."""
        medio = self.repository.get_by_id(medio_id)
        if not medio:
            return None
        return MedioRecepcionResponse.model_validate(medio)

    def get_all(self) -> List[MedioRecepcionResponse]:
        """Obtiene todos los medios de recepción."""
        medios = self.repository.get_all()
        return [MedioRecepcionResponse.model_validate(m) for m in medios]

    def get_activos(self) -> List[MedioRecepcionResponse]:
        """Obtiene solo los medios de recepción activos."""
        medios = self.repository.get_activos()
        return [MedioRecepcionResponse.model_validate(m) for m in medios]

    def set_archivado(self, medio_id: UUID, archivado: bool) -> Optional[MedioRecepcionResponse]:
        """Archiva o desarchiva un medio de recepción."""
        medio = self.repository.get_by_id(medio_id)
        if not medio:
            return None
        updated = self.repository.set_archivado(medio_id, archivado)
        return MedioRecepcionResponse.model_validate(updated)
