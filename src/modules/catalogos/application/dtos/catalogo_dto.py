"""
DTOs (Schemas de Pydantic) para el módulo de Catálogos.
Manejan la validación de entrada (RequestDTO) y formateo de salida (ResponseDTO).
"""
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


# --- Schemas para Archivar ---
class ArchivarRequest(BaseModel):
    """Payload para archivar (soft delete) o desarchivar un recurso de catálogo."""
    archivado: bool


# --- Area ---
class AreaCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del área no puede estar vacío ni contener solo espacios")
        return v.strip()


class AreaResponse(BaseModel):
    id: UUID
    nombre: str
    archivado: bool

    class Config:
        from_attributes = True


# --- Cargo ---
class CargoCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del cargo no puede estar vacío ni contener solo espacios")
        return v.strip()


class CargoResponse(BaseModel):
    id: UUID
    nombre: str
    archivado: bool

    class Config:
        from_attributes = True


# --- TipoComunicado ---
class TipoComunicadoCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del tipo de comunicado no puede estar vacío ni contener solo espacios")
        return v.strip()


class TipoComunicadoResponse(BaseModel):
    id: UUID
    nombre: str
    archivado: bool

    class Config:
        from_attributes = True


# --- MedioRecepcion ---
class MedioRecepcionCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del medio de recepción no puede estar vacío ni contener solo espacios")
        return v.strip()


class MedioRecepcionResponse(BaseModel):
    id: UUID
    nombre: str
    archivado: bool

    class Config:
        from_attributes = True


# --- RolDestinatario ---
class RolDestinatarioCreateRequest(BaseModel):
    descripcion_rol: str = Field(..., min_length=1, max_length=100)

    @field_validator("descripcion_rol")
    @classmethod
    def validate_descripcion(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La descripción del rol no puede estar vacía ni contener solo espacios")
        return v.strip()


class RolDestinatarioResponse(BaseModel):
    id: UUID
    descripcion_rol: str
    archivado: bool

    class Config:
        from_attributes = True


# --- RolResponsable ---
class RolResponsableCreateRequest(BaseModel):
    descripcion_rol: str = Field(..., min_length=1, max_length=100)

    @field_validator("descripcion_rol")
    @classmethod
    def validate_descripcion(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La descripción del rol no puede estar vacía ni contener solo espacios")
        return v.strip()


class RolResponsableResponse(BaseModel):
    id: UUID
    descripcion_rol: str
    archivado: bool

    class Config:
        from_attributes = True


# --- EstadoTarea ---
class EstadoTareaCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre del estado no puede estar vacío ni contener solo espacios")
        return v.strip()


class EstadoTareaResponse(BaseModel):
    id: UUID
    nombre: str

    class Config:
        from_attributes = True
