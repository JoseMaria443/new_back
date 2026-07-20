"""
Casos de uso para el recurso RolDestinatario.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.entities import RolDestinatario
from ...domain.ports import RolDestinatarioRepository
from ..dtos import RolDestinatarioCreateRequest, RolDestinatarioResponse


class RolDestinatarioUseCases:
    """Casos de uso de negocio para la gestión de Roles de Destinatario."""

    def __init__(self, repository: RolDestinatarioRepository):
        self.repository = repository

    def create(self, request: RolDestinatarioCreateRequest) -> RolDestinatarioResponse:
        """Crea un nuevo rol de destinatario."""
        rol = RolDestinatario(descripcion_rol=request.descripcion_rol)
        saved = self.repository.add(rol)
        return RolDestinatarioResponse.model_validate(saved)

    def get_by_id(self, rol_id: UUID) -> Optional[RolDestinatarioResponse]:
        """Obtiene un rol de destinatario por su ID."""
        rol = self.repository.get_by_id(rol_id)
        if not rol:
            return None
        return RolDestinatarioResponse.model_validate(rol)

    def get_all(self) -> List[RolDestinatarioResponse]:
        """Obtiene todos los roles de destinatario."""
        roles = self.repository.get_all()
        return [RolDestinatarioResponse.model_validate(r) for r in roles]

    def get_activos(self) -> List[RolDestinatarioResponse]:
        """Obtiene solo los roles de destinatario activos."""
        roles = self.repository.get_activos()
        return [RolDestinatarioResponse.model_validate(r) for r in roles]

    def set_archivado(self, rol_id: UUID, archivado: bool) -> Optional[RolDestinatarioResponse]:
        """Archiva o desarchiva un rol de destinatario."""
        rol = self.repository.get_by_id(rol_id)
        if not rol:
            return None
        updated = self.repository.set_archivado(rol_id, archivado)
        return RolDestinatarioResponse.model_validate(updated)
