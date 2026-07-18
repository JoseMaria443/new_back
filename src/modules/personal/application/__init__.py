"""
Use cases del módulo de personal.
"""
from .login_empleado import LoginEmpleadoUseCase
from .create_empleado import CreateEmpleadoUseCase
from .update_empleado_estatus import UpdateEmpleadoEstatusUseCase

__all__ = [
    "LoginEmpleadoUseCase",
    "CreateEmpleadoUseCase",
    "UpdateEmpleadoEstatusUseCase",
]