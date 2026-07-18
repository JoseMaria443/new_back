"""
Excepciones del módulo de seguridad.
"""
from shared.domain.exceptions import DomainError


class AuthenticationError(DomainError):
    """Error de autenticación (credenciales inválidas)."""
    pass


class AuthorizationError(DomainError):
    """Error de autorización (no tiene permisos para la operación)."""
    pass


class TokenExpiredError(DomainError):
    """Error cuando el token JWT ha expirado."""
    pass