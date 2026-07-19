"""
Router de API para el recurso Comunicado.
"""
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ....domain.entities import Comunicado, EstadoComunicado
from ....domain.ports import ComunicadoRepository
from ....infrastructure.persistence import ComunicadoRepositoryAdapter
from ....application.use_cases import CreateComunicadoUseCase

from modules.personal.domain.ports import EmpleadoRepository
from modules.personal.infrastructure.persistence import EmpleadoRepositoryAdapter
from modules.catalogos.domain.ports import (
    TipoComunicadoRepository,
    MedioRecepcionRepository,
    RolDestinatarioRepository,
)
from modules.catalogos.infrastructure.persistence import (
    TipoComunicadoRepositoryAdapter,
    MedioRecepcionRepositoryAdapter,
    RolDestinatarioRepositoryAdapter,
)

from shared.infrastructure.security.security import get_current_active_user
from shared.domain.exceptions import BusinessRuleViolationError

router = APIRouter(prefix="/comunicados", tags=["comunicados"])


def get_comunicado_repository() -> ComunicadoRepository:
    """Factory para obtener el repositorio de comunicados."""
    return ComunicadoRepositoryAdapter()


def get_empleado_repository() -> EmpleadoRepository:
    """Factory para obtener el repositorio de empleados (validar idEmisor)."""
    return EmpleadoRepositoryAdapter()


def get_tipo_comunicado_repository() -> TipoComunicadoRepository:
    """Factory para obtener el repositorio de tipos de comunicado."""
    return TipoComunicadoRepositoryAdapter()


def get_medio_recepcion_repository() -> MedioRecepcionRepository:
    """Factory para obtener el repositorio de medios de recepción."""
    return MedioRecepcionRepositoryAdapter()


def get_rol_destinatario_repository() -> RolDestinatarioRepository:
    """Factory para obtener el repositorio de roles de destinatario."""
    return RolDestinatarioRepositoryAdapter()


class DestinatarioIn(BaseModel):
    idDestinatario: UUID
    idRolDestinatario: UUID


class CreateComunicadoRequest(BaseModel):
    folioDoi: str
    numComunicado: str
    tema: str
    fechaEmision: datetime
    fechaRecepcion: datetime
    idEmisor: UUID
    idTipoComunicado: UUID
    idMedioRecepcion: UUID
    destinatarios: List[DestinatarioIn]
    # idEmpleadoRegistro y fechaRegistro NUNCA se aceptan del payload:
    # se inyectan desde el JWT y desde la base de datos, respectivamente.


class ComunicadoResponse(BaseModel):
    id: str
    folioDoi: str
    numComunicado: str
    tema: str
    fechaEmision: datetime
    fechaRecepcion: datetime
    fechaRegistro: Optional[datetime]
    idEmisor: str
    idTipoComunicado: str
    idMedioRecepcion: str
    idEmpleadoRegistro: str
    idEstadoComunicado: str


def _to_response(comunicado: Comunicado) -> ComunicadoResponse:
    return ComunicadoResponse(
        id=str(comunicado.id),
        folioDoi=comunicado.folioDoi,
        numComunicado=comunicado.numComunicado,
        tema=comunicado.tema,
        fechaEmision=comunicado.fechaEmision,
        fechaRecepcion=comunicado.fechaRecepcion,
        fechaRegistro=comunicado.fechaRegistro,
        idEmisor=str(comunicado.idEmisor),
        idTipoComunicado=str(comunicado.idTipoComunicado),
        idMedioRecepcion=str(comunicado.idMedioRecepcion),
        idEmpleadoRegistro=str(comunicado.idEmpleadoRegistro),
        # Enum en código (no persistido): siempre PENDIENTE al crear.
        # Se enriquecerá con transiciones reales en la Sección V (Tareas).
        idEstadoComunicado=EstadoComunicado.PENDIENTE.value,
    )


@router.post("/", response_model=ComunicadoResponse, status_code=201)
async def create_comunicado(
    request: CreateComunicadoRequest,
    current_user: dict = Depends(get_current_active_user),
    repository: ComunicadoRepository = Depends(get_comunicado_repository),
    empleado_repository: EmpleadoRepository = Depends(get_empleado_repository),
    tipo_repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository),
    medio_repository: MedioRecepcionRepository = Depends(get_medio_recepcion_repository),
    rol_destinatario_repository: RolDestinatarioRepository = Depends(get_rol_destinatario_repository),
) -> ComunicadoResponse:
    """
    Crea un nuevo comunicado con sus destinatarios.
    idEmpleadoRegistro se toma del JWT (nunca del payload).
    fechaRegistro la asigna la base de datos (nunca el cliente).
    Requiere JWT válido (cualquier empleado autenticado).
    """
    idEmpleadoRegistro = UUID(current_user["idEmpleado"])

    use_case = CreateComunicadoUseCase(
        repository,
        empleado_repository,
        tipo_repository,
        medio_repository,
        rol_destinatario_repository,
    )

    try:
        comunicado = use_case.execute(
            folioDoi=request.folioDoi,
            numComunicado=request.numComunicado,
            tema=request.tema,
            fechaEmision=request.fechaEmision,
            fechaRecepcion=request.fechaRecepcion,
            idEmisor=request.idEmisor,
            idTipoComunicado=request.idTipoComunicado,
            idMedioRecepcion=request.idMedioRecepcion,
            idEmpleadoRegistro=idEmpleadoRegistro,
            destinatarios=[d.model_dump() for d in request.destinatarios],
        )
        return _to_response(comunicado)
    except BusinessRuleViolationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[ComunicadoResponse])
async def list_comunicados(
    current_user: dict = Depends(get_current_active_user),
    repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> List[ComunicadoResponse]:
    """Lista todos los comunicados."""
    comunicados = repository.get_all()
    return [_to_response(c) for c in comunicados]


@router.get("/{comunicado_id}", response_model=ComunicadoResponse)
async def get_comunicado(
    comunicado_id: UUID,
    current_user: dict = Depends(get_current_active_user),
    repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> ComunicadoResponse:
    """Obtiene un comunicado por ID."""
    comunicado = repository.get_by_id(comunicado_id)
    if comunicado is None:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")
    return _to_response(comunicado)


@router.get("/{comunicado_id}/destinatarios", response_model=List[dict])
async def get_destinatarios(
    comunicado_id: UUID,
    current_user: dict = Depends(get_current_active_user),
    repository: ComunicadoRepository = Depends(get_comunicado_repository),
) -> List[dict]:
    """Obtiene los destinatarios de un comunicado."""
    comunicado = repository.get_by_id(comunicado_id)
    if comunicado is None:
        raise HTTPException(status_code=404, detail="Comunicado no encontrado")
    destinatarios = repository.get_destinatarios(comunicado_id)
    return [
        {"idDestinatario": str(d["idDestinatario"]), "idRolDestinatario": str(d["idRolDestinatario"])}
        for d in destinatarios
    ]