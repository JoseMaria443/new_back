"""
Casos de uso para el recurso RolResponsable.
"""
from uuid import UUID
from typing import List, Optional

from ...domain.entities import RolResponsable
from ...domain.ports import RolResponsableRepository
from ..dtos import RolResponsableCreateRequest, RolResponsableResponse


class RolResponsableUseCases:
    """Casos de uso de negocio para la gestión de Roles de Responsable."""

    def __init__(self, repository: RolResponsableRepository):
        self.repository = repository

    def create(self, request: RolResponsableCreateRequest) -> RolResponsableResponse:
        """Crea un nuevo rol de responsable."""
        rol = RolResponsable(descripcion_rol=request.descripcion_rol)
        saved = self.repository.add(rol)
        return RolResponsableResponse.model_validate(saved)

    def get_by_id(self, rol_id: UUID) -> Optional[RolResponsableResponse]:
        """Obtiene un rol de responsable por su ID."""
        rol = self.repository.get_by_id(rol_id)
        if not rol:
            return None
        return RolResponsableResponse.model_validate(rol)

    def get_all(self) -> List[RolResponsableResponse]:
        """Obtiene todos los roles de responsable."""
        roles = self.repository.get_all()
        return [RolResponsableResponse.model_validate(r) for r in roles]

    def get_activos(self) -> List[RolResponsableResponse]:
        """Obtiene solo los roles de responsable activos."""
        roles = self.repository.get_activos()
        return [RolResponsableResponse.model_validate(r) for r in roles]

    def set_archivado(self, rol_id: UUID, archivado: bool) -> Optional[RolResponsableResponse]:
        """Archiva o desarchiva un rol de responsable."""
        rol = self.repository.get_by_id(rol_id)
        if not rol:
            return None
        updated = self.repository.set_archivado(rol_id, archivado)
        return RolResponsableResponse.model_validate(updated)
