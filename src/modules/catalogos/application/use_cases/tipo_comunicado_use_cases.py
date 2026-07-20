"""
Casos de uso para el recurso TipoComunicado.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.entities import TipoComunicado
from ...domain.ports import TipoComunicadoRepository
from ..dtos import TipoComunicadoCreateRequest, TipoComunicadoResponse


class TipoComunicadoUseCases:
    """Casos de uso de negocio para la gestión de Tipos de Comunicado."""

    def __init__(self, repository: TipoComunicadoRepository):
        self.repository = repository

    def create(self, request: TipoComunicadoCreateRequest) -> TipoComunicadoResponse:
        """Crea un nuevo tipo de comunicado."""
        tipo = TipoComunicado(nombre=request.nombre)
        saved = self.repository.add(tipo)
        return TipoComunicadoResponse.model_validate(saved)

    def get_by_id(self, tipo_id: UUID) -> Optional[TipoComunicadoResponse]:
        """Obtiene un tipo de comunicado por su ID."""
        tipo = self.repository.get_by_id(tipo_id)
        if not tipo:
            return None
        return TipoComunicadoResponse.model_validate(tipo)

    def get_all(self) -> List[TipoComunicadoResponse]:
        """Obtiene todos los tipos de comunicado."""
        tipos = self.repository.get_all()
        return [TipoComunicadoResponse.model_validate(t) for t in tipos]

    def get_activos(self) -> List[TipoComunicadoResponse]:
        """Obtiene solo los tipos de comunicado activos."""
        tipos = self.repository.get_activos()
        return [TipoComunicadoResponse.model_validate(t) for t in tipos]

    def set_archivado(self, tipo_id: UUID, archivado: bool) -> Optional[TipoComunicadoResponse]:
        """Archiva o desarchiva un tipo de comunicado."""
        tipo = self.repository.get_by_id(tipo_id)
        if not tipo:
            return None
        updated = self.repository.set_archivado(tipo_id, archivado)
        return TipoComunicadoResponse.model_validate(updated)
