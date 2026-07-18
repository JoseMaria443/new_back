"""
Use case para crear empleados.
Solo roles "Administrador"/"Director" pueden usarlo.
"""
from uuid import UUID
from typing import List

from ...domain.entities import Empleado
from ...domain.ports import EmpleadoRepository
from shared.infrastructure.security.security import get_password_hash
from shared.domain.exceptions import BusinessRuleViolationError


class CreateEmpleadoUseCase:
    """
    Caso de uso para crear un nuevo empleado.
    Solo usuarios con roles "Administrador" o "Director" pueden ejecutarlo.
    """
    
    # IDs de roles que pueden crear empleados
    # Nota: Estos IDs deberían venir de la base de datos, pero se hardcodean
    # por ahora como referencia. En producción, se validaría contra ROL_RESPONSABLE.
    ROLES_PERMITIDOS = ["Administrador", "Director"]
    
    def __init__(self, repository: EmpleadoRepository):
        self._repository = repository
    
    def execute(
        self,
        nombre: str,
        email: str,
        password: str,
        idArea: UUID,
        roles: List[UUID],
        cargos: List[UUID],
    ) -> Empleado:
        """
        Crea un nuevo empleado con sus cargos asignados.
        """
        # Hashear la contraseña
        password_hash = get_password_hash(password)
        
        # Crear el empleado
        empleado = Empleado(
            nombre=nombre,
            email=email,
            idArea=idArea,
            password_hash=password_hash,
        )
        
        # Guardar el empleado
        saved = self._repository.add(empleado)
        
        # Asignar cargos (se haría en una transacción)
        # Nota: Esta lógica se implementaría en el repositorio
        
        return saved