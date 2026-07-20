"""
Router de API para el recurso Tarea.
"""
from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ....domain.entities import Tarea
from ....domain.ports import TareaRepository
from ....infrastructure.persistence import TareaRepositoryAdapter
from ....application.use_cases import CreateTareaUseCase, TransicionEstadoTareaUseCase

from modules.comunicados.domain.ports import ComunicadoRepository
from modules.comunicados.infrastructure.persistence import ComunicadoRepositoryAdapter
from modules.catalogos.domain.ports import EstadoTareaRepository, RolResponsableRepository
from modules.catalogos.infrastructure.persistence import (
    EstadoTareaRepositoryAdapter,
    RolResponsableRepositoryAdapter,
)

from shared.infrastructure.security.security import get_current_active_user, require_roles
from shared.domain.exceptions import BusinessRuleViolationError

router = APIRouter(prefix="/tareas", tags=["tareas"])


def get_tarea_repository() -> TareaRepository:
    return TareaRepositoryAdapter()


def get_comunicado_repository() -> ComunicadoRepository:
    return ComunicadoRepositoryAdapter()


def get_estado_tarea_repository() -> EstadoTareaRepository:
    return EstadoTareaRepositoryAdapter()


def get_rol_responsable_repository() -> RolResponsableRepository:
    return RolResponsableRepositoryAdapter()


class ResponsableIn(BaseModel):
    idResponsable: UUID
    idRolResponsable: UUID


class CreateTareaRequest(BaseModel):
    idComunicado: UUID
    resumenActividad: str
    descripcion: str
    fechaEntrega: datetime
    responsables: List[ResponsableIn]
    # idEstadoTarea NUNCA se acepta del payload: se fuerza a ASIGNADA.


class TareaResponse(BaseModel):
    id: str
    idComunicado: str
    resumenActividad: str
    descripcion: str
    fechaEntrega: datetime
    fechaRegistro: Optional[datetime]
    idEstadoTarea: str
    estado: str  # nombre del estado, incluyendo VENCIDA calculada


def _compute_estado_nombre(estado_real_nombre: str, fecha_entrega: datetime) -> str:
    """
    VENCIDA es una transición calculada (no persistida): si la tarea sigue
    en ASIGNADA o EN_PROCESO y ya pasó su fechaEntrega, se muestra como
    VENCIDA en la respuesta, sin alterar el valor guardado en BD.
    """
    normalizado = estado_real_nombre.strip().upper().replace(" ", "_")
    if normalizado in ("ASIGNADA", "EN_PROCESO"):
        ahora = datetime.now(timezone.utc)
        entrega = fecha_entrega
        if entrega.tzinfo is None:
            entrega = entrega.replace(tzinfo=timezone.utc)
        if entrega < ahora:
            return "VENCIDA"
    return estado_real_nombre


def _to_response(tarea: Tarea, estado_tarea_repository: Any) -> TareaResponse:
    estado = estado_tarea_repository.get_by_id(tarea.idEstadoTarea)
    estado_nombre = estado.nombre if estado is not None else "DESCONOCIDO"
    return TareaResponse(
        id=str(tarea.id),
        idComunicado=str(tarea.idComunicado),
        resumenActividad=tarea.resumenActividad,
        descripcion=tarea.descripcion,
        fechaEntrega=tarea.fechaEntrega,
        fechaRegistro=tarea.fechaRegistro,
        idEstadoTarea=str(tarea.idEstadoTarea),
        estado=_compute_estado_nombre(estado_nombre, tarea.fechaEntrega),
    )


@router.post("/", response_model=TareaResponse, status_code=201)
async def create_tarea(
    request: CreateTareaRequest,
    current_user: dict = Depends(get_current_active_user),
    repository: TareaRepository = Depends(get_tarea_repository),
    comunicado_repository: ComunicadoRepository = Depends(get_comunicado_repository),
    estado_tarea_repository: EstadoTareaRepository = Depends(get_estado_tarea_repository),
    rol_responsable_repository: RolResponsableRepository = Depends(get_rol_responsable_repository),
) -> TareaResponse:
    """
    Crea una nueva tarea derivada de un comunicado.
    Estado inicial forzado a ASIGNADA. Requiere JWT válido (cualquier
    empleado autenticado).
    """
    use_case = CreateTareaUseCase(
        repository, comunicado_repository, estado_tarea_repository, rol_responsable_repository
    )
    try:
        tarea = use_case.execute(
            idComunicado=request.idComunicado,
            resumenActividad=request.resumenActividad,
            descripcion=request.descripcion,
            fechaEntrega=request.fechaEntrega,
            responsables=[r.model_dump() for r in request.responsables],
        )
        return _to_response(tarea, estado_tarea_repository)
    except BusinessRuleViolationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=List[TareaResponse])
async def list_tareas(
    current_user: dict = Depends(get_current_active_user),
    repository: TareaRepository = Depends(get_tarea_repository),
    estado_tarea_repository: EstadoTareaRepository = Depends(get_estado_tarea_repository),
) -> List[TareaResponse]:
    """Lista todas las tareas."""
    tareas = repository.get_all()
    return [_to_response(t, estado_tarea_repository) for t in tareas]


@router.get("/{tarea_id}", response_model=TareaResponse)
async def get_tarea(
    tarea_id: UUID,
    current_user: dict = Depends(get_current_active_user),
    repository: TareaRepository = Depends(get_tarea_repository),
    estado_tarea_repository: EstadoTareaRepository = Depends(get_estado_tarea_repository),
) -> TareaResponse:
    """
    Obtiene una tarea por ID.
    Efecto automático: si quien consulta es responsable de la tarea y el
    estado real actual es ASIGNADA, se transiciona automáticamente a
    EN_PROCESO (PATCH automático al acceder, regla V.2).
    """
    tarea = repository.get_by_id(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    estado_actual = estado_tarea_repository.get_by_id(tarea.idEstadoTarea)
    es_responsable = repository.is_responsable(tarea_id, UUID(current_user["idEmpleado"]))

    if (
        es_responsable
        and estado_actual is not None
        and estado_actual.nombre.strip().upper().replace(" ", "_") == "ASIGNADA"
    ):
        use_case = TransicionEstadoTareaUseCase(repository, estado_tarea_repository)
        tarea = use_case.execute(tarea_id, "EN_PROCESO")

    return _to_response(tarea, estado_tarea_repository)


@router.get("/{tarea_id}/responsables", response_model=List[dict])
async def get_responsables(
    tarea_id: UUID,
    current_user: dict = Depends(get_current_active_user),
    repository: TareaRepository = Depends(get_tarea_repository),
) -> List[dict]:
    """Obtiene los responsables de una tarea."""
    tarea = repository.get_by_id(tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    responsables = repository.get_responsables(tarea_id)
    return [
        {"idResponsable": str(r["idResponsable"]), "idRolResponsable": str(r["idRolResponsable"])}
        for r in responsables
    ]


def _transicionar(
    tarea_id: UUID,
    nombre_estado_destino: str,
    repository: TareaRepository,
    estado_tarea_repository: EstadoTareaRepository,
) -> TareaResponse:
    use_case = TransicionEstadoTareaUseCase(repository, estado_tarea_repository)
    try:
        tarea = use_case.execute(tarea_id, nombre_estado_destino)
        return _to_response(tarea, estado_tarea_repository)
    except BusinessRuleViolationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{tarea_id}/revisar", response_model=TareaResponse)
async def revisar_tarea(
    tarea_id: UUID,
    current_user: dict = Depends(require_roles(["Director"])),
    repository: TareaRepository = Depends(get_tarea_repository),
    estado_tarea_repository: EstadoTareaRepository = Depends(get_estado_tarea_repository),
) -> TareaResponse:
    """Aprueba/cierra la tarea (REVISADA). Solo rol Director."""
    return _transicionar(tarea_id, "REVISADA", repository, estado_tarea_repository)


@router.patch("/{tarea_id}/rechazar", response_model=TareaResponse)
async def rechazar_tarea(
    tarea_id: UUID,
    current_user: dict = Depends(require_roles(["Director"])),
    repository: TareaRepository = Depends(get_tarea_repository),
    estado_tarea_repository: EstadoTareaRepository = Depends(get_estado_tarea_repository),
) -> TareaResponse:
    """Rechaza la tarea y la regresa a EN_PROCESO. Solo rol Director."""
    return _transicionar(tarea_id, "EN_PROCESO", repository, estado_tarea_repository)


@router.patch("/{tarea_id}/cancelar", response_model=TareaResponse)
async def cancelar_tarea(
    tarea_id: UUID,
    current_user: dict = Depends(require_roles(["Director"])),
    repository: TareaRepository = Depends(get_tarea_repository),
    estado_tarea_repository: EstadoTareaRepository = Depends(get_estado_tarea_repository),
) -> TareaResponse:
    """Cancela la tarea, sin solicitar evidencias. Solo rol Director."""
    return _transicionar(tarea_id, "CANCELADA", repository, estado_tarea_repository)