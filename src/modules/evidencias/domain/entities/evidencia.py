"""
Entidad Evidencia / ArchivoEvidencia.
Representa un archivo comprobatorio registrado como prueba de trabajo.
Mapeo 1:1 con la tabla ARCHIVO_EVIDENCIA del esquema SQL.
"""
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime
from typing import Optional

from shared.domain.base_entity import BaseEntity


@dataclass
class Evidencia(BaseEntity):
    # idArchivoEvidencia -> id (heredado de BaseEntity)
    doi: str  # VARCHAR(100) UNIQUE NOT NULL
    descripcion: str  # TEXT NOT NULL
    urlArchivo: str  # VARCHAR(500) NOT NULL
    nombreOriginal: str  # VARCHAR(255) NOT NULL
    idElaborador: UUID  # FK EMPLEADO
    fechaRegistro: Optional[datetime] = field(default=None)

    def __post_init__(self) -> None:
        """Validaciones de invariantes."""
        if not self.doi or not self.doi.strip():
            raise ValueError("El doi de la evidencia no puede estar vacío")
        if len(self.doi) > 100:
            raise ValueError("El doi no puede exceder 100 caracteres")

        if not self.descripcion or not self.descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")

        if not self.urlArchivo or not self.urlArchivo.strip():
            raise ValueError("La urlArchivo no puede estar vacía")
        if len(self.urlArchivo) > 500:
            raise ValueError("La urlArchivo no puede exceder 500 caracteres")

        if not self.nombreOriginal or not self.nombreOriginal.strip():
            raise ValueError("El nombreOriginal no puede estar vacío")
        if len(self.nombreOriginal) > 255:
            raise ValueError("El nombreOriginal no puede exceder 255 caracteres")
