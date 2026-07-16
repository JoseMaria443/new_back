"""
Excepciones del dominio.
Definen errores de negocio y violaciones de invariantes.
"""
from typing import Optional


class DomainError(Exception):
    """Error base del dominio."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainError):
    """Error cuando una entidad no se encuentra en el repositorio."""
    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(f"{entity_type} con ID {entity_id} no encontrado")


class BusinessRuleViolationError(DomainError):
    """Error cuando se viola una regla de negocio."""
    pass


class ValidationError(DomainError):
    """Error de validación de datos."""
    pass


class FileStorageError(DomainError):
    """Error al guardar o recuperar archivos."""
    pass


class FileParseError(DomainError):
    """Error al parsear un archivo adjunto."""
    pass