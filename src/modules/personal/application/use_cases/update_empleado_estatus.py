"""
Use case para actualizar el estatus de un empleado.
Solo roles "Director" pueden usarlo.
"""
from uuid import UUID

from ...domain.ports import EmpleadoRepository
from shared.domain.exceptions import BusinessRuleViolationError


class UpdateEmpleadoEstatusUseCase:
    """
    Caso de uso para actualizar el estatus (activo) de un empleado.
    Solo usuarios con rol "Director" pueden ejecutarlo.
    Crea automáticamente un registro en HISTORIAL_ESTATUS.
    """
    
    def __init__(self, repository: EmpleadoRepository):
        self._repository = repository
    
    def execute(
        self,
        id: UUID,
        activo: bool,
        idEmpleadoModifica: UUID,
    ) -> None:
        """
        Actualiza el estatus del empleado.
        El idEmpleadoModifica viene del JWT, no del request.
        """
        # Verificar que el empleado existe
        empleado = self._repository.get_by_id(id)
        if empleado is None:
            raise BusinessRuleViolationError(f"Empleado con ID {id} no encontrado")
        
        # Actualizar estatus (el repositorio crea el historial)
        self._repository.update_estatus(id, activo, idEmpleadoModifica)