"""
DTOs para la gestión de Comunicados (Sección IV SGC2I).
"""
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class DestinatarioIn(BaseModel):
    """Esquema de entrada para un destinatario en el payload."""
    idDestinatario: UUID = Field(..., description="UUID del empleado o entidad destinataria")
    idRolDestinatario: UUID = Field(..., description="UUID del rol de destinatario")


class ComunicadoCreateRequest(BaseModel):
    """
    Payload de entrada para la creación de un Comunicado.
    NO incluye idEmpleadoRegistro (inyectado del JWT), ni fechaRegistro / estado (manejados por DB/sistema).
    """
    folioDoi: str = Field(..., max_length=100, description="Folio DOI único del comunicado")
    numComunicado: str = Field(..., max_length=50, description="Número interno de comunicado")
    tema: str = Field(..., max_length=200, description="Tema o asunto del comunicado")
    fechaEmision: datetime = Field(..., description="Fecha de emisión del comunicado")
    fechaRecepcion: datetime = Field(..., description="Fecha de recepción del comunicado")
    emisorNombre: str = Field(..., max_length=200, description="Nombre libre del emisor")
    idTipoComunicado: UUID = Field(..., description="UUID del tipo de comunicado")
    idMedioRecepcion: UUID = Field(..., description="UUID del medio de recepción")
    destinatarios: List[DestinatarioIn] = Field(
        ..., min_items=1, description="Lista de destinatarios asignados"
    )
    archivoUrl: Optional[str] = Field(None, max_length=500, description="URL opcional del documento adjunto")

    @field_validator("folioDoi", "numComunicado", "tema")
    @classmethod
    def not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("El campo no puede estar vacío ni contener solo espacios")
        return value.strip()


class DestinatarioResponse(BaseModel):
    """DTO de respuesta para un destinatario."""
    idDestinatario: UUID
    idRolDestinatario: UUID

    model_config = ConfigDict(from_attributes=True)


class ComunicadoResponse(BaseModel):
    """DTO de respuesta para un Comunicado creado/consultado."""
    id: UUID
    folioDoi: str
    numComunicado: str
    tema: str
    fechaEmision: datetime
    fechaRecepcion: datetime
    fechaRegistro: Optional[datetime] = None
    emisorNombre: str
    idTipoComunicado: UUID
    idMedioRecepcion: UUID
    idEmpleadoRegistro: UUID
    idEstadoComunicado: str
    areaEmisoraNombre: Optional[str] = None
    empleadoRegistroNombre: Optional[str] = None
    archivoUrl: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
