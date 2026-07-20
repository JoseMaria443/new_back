"""
DTOs para la gestión de Evidencias (Fase 3 / Sección V SGC2I).
"""
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class EvidenciaCreateRequest(BaseModel):
    """
    Payload de entrada para registrar una Evidencia.
    NO incluye idElaborador (inyectado del JWT) ni fechaRegistro.
    """
    idTarea: UUID = Field(..., description="UUID de la tarea a la que pertenece la evidencia")
    doi: str = Field(..., max_length=100, description="DOI único de la evidencia")
    descripcion: str = Field(..., description="Descripción detallada de la evidencia")
    urlArchivo: str = Field(..., max_length=500, description="URL o ruta del archivo de evidencia")
    nombreOriginal: str = Field(..., max_length=255, description="Nombre original del archivo adjunto")

    @field_validator("doi", "descripcion", "urlArchivo", "nombreOriginal")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("El campo no puede estar vacío ni contener solo espacios")
        return value.strip()


class EvidenciaResponse(BaseModel):
    """DTO de respuesta para una Evidencia creada/consultada."""
    id: UUID
    doi: str
    descripcion: str
    urlArchivo: str
    nombreOriginal: str
    idElaborador: UUID
    fechaRegistro: Optional[datetime] = None
    idTarea: Optional[UUID] = None

    model_config = ConfigDict(from_attributes=True)
