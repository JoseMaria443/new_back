"""
Use case para el login de empleados.
Autentica con email/password y genera JWT.
"""
from uuid import UUID
from typing import Dict, Any, Optional

from ...domain.entities import Empleado
from ...domain.ports import EmpleadoRepository
from shared.infrastructure.security.security import (
    verify_password,
    create_access_token,
)
from shared.infrastructure.security.exceptions import AuthenticationError


class LoginEmpleadoUseCase:
    """
    Caso de uso para autenticar un empleado.
    Retorna un token JWT con idEmpleado, email y roles/cargos.
    """
    
    def __init__(self, repository: EmpleadoRepository, cargo_repository: Optional[Any] = None):
        self._repository = repository
        self._cargo_repository = cargo_repository
    
    def execute(self, email: str, password: str) -> Dict[str, Any]:
        """
        Ejecuta el login del empleado.
        Retorna el token JWT y datos del usuario.
        """
        # Buscar empleado por email
        empleado = self._repository.get_by_email(email)
        
        if empleado is None:
            raise AuthenticationError("Credenciales inválidas")
        
        # Verificar contraseña
        if not verify_password(password, empleado.password_hash):
            raise AuthenticationError("Credenciales inválidas")
        
        # Obtener cargos del empleado
        cargos = self._repository.get_cargos(empleado.id)
        
        # Obtener nombres de cargos
        cargos_nombres = []
        if self._cargo_repository is not None:
            for cargo_id in cargos:
                cargo = self._cargo_repository.get_by_id(cargo_id)
                if cargo is not None:
                    cargos_nombres.append(cargo.nombre)
        
        # Crear token JWT
        token_data = {
            "idEmpleado": str(empleado.id),
            "email": empleado.email,
            "nombre": empleado.nombre,
            "activo": empleado.activo,
            "cargos": [str(c) for c in cargos],
            "cargos_nombres": cargos_nombres,
        }
        
        print(f"DEBUG LOGIN PAYLOAD: {token_data}")
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "empleado": {
                "id": str(empleado.id),
                "nombre": empleado.nombre,
                "email": empleado.email,
                "activo": empleado.activo,
            }
        }