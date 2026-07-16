"""
Entidades y excepciones del dominio compartido.
"""
from .base_entity import BaseEntity
from .exceptions import (
    DomainError,
    EntityNotFoundError,
    BusinessRuleViolationError,
    ValidationError,
    FileStorageError,
    FileParseError,
)

__all__ = [
    "BaseEntity",
    "DomainError",
    "EntityNotFoundError",
    "BusinessRuleViolationError",
    "ValidationError",
    "FileStorageError",
    "FileParseError",
]