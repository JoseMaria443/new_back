"""
Use case para crear empleados.
Solo roles "Administrador"/"Director" pueden usarlo (validado en el router
vía la dependencia require_roles, no aquí).
"""
from uuid import UUID
from typing import List, Optional, Any

from ...domain.entities import Empleado
from ...domain.ports import EmpleadoRepository
from shared.infrastructure.security.security import get_password_hash
from shared.domain.exceptions import BusinessRuleViolationError


class CreateEmpleadoUseCase:
    """
    Caso de uso para crear un nuevo empleado.
    Valida: email único, idArea existente y no archivada, cargos existentes y no archivados;
    y asigna los cargos en la misma transacción del alta del empleado.
    """
    
    def __init__(
        self,
        repository: EmpleadoRepository,
        area_repository: Optional[Any] = None,
        cargo_repository: Optional[Any] = None,
    ):
        self._repository = repository
        self._area_repository = area_repository
        self._cargo_repository = cargo_repository
    
    def execute(
        self,
        nombre: str,
        email: str,
        password: str,
        idArea: UUID,
        cargos: List[UUID],
    ) -> Empleado:
        """
        Crea un nuevo empleado con sus cargos asignados.
        """
        if self._repository.get_by_email(email) is not None:
            raise BusinessRuleViolationError(
                f"Ya existe un empleado registrado con el email {email}"
            )
        
        # Validar que el área exista y no esté archivada
        if self._area_repository is not None:
            area = self._area_repository.get_by_id(idArea)
            if area is None:
                raise BusinessRuleViolationError(
                    f"El área {idArea} no existe en el catálogo"
                )
            if getattr(area, "archivado", False):
                raise BusinessRuleViolationError(
                    f"El área '{area.nombre}' está archivada y no puede ser asignada a un empleado"
                )
        
        # Validar que los cargos existan y no estén archivados
        if self._cargo_repository is not None:
            for cargo_id in cargos:
                cargo = self._cargo_repository.get_by_id(cargo_id)
                if cargo is None:
                    raise BusinessRuleViolationError(
                        f"El cargo {cargo_id} no existe en el catálogo"
                    )
                if getattr(cargo, "archivado", False):
                    raise BusinessRuleViolationError(
                        f"El cargo '{cargo.nombre}' está archivado y no puede ser asignado a un empleado"
                    )
        
        password_hash = get_password_hash(password)
        
        empleado = Empleado(
            nombre=nombre,
            email=email,
            idArea=idArea,
            password_hash=password_hash,
        )
        
        saved = self._repository.add_with_cargos(empleado, cargos)
        
        return saved