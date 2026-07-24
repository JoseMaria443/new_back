"""
Router de API para el recurso Empleado.
Endpoints: /api/empleado (login, create) y /api/empleado/{id}/estatus
"""
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr

from ....domain.entities import Empleado
from ....domain.ports import EmpleadoRepository
from ....infrastructure.persistence import EmpleadoRepositoryAdapter
from ....application.use_cases import (
    LoginEmpleadoUseCase,
    CreateEmpleadoUseCase,
    UpdateEmpleadoEstatusUseCase,
)
from modules.catalogos.domain.ports import AreaRepository, CargoRepository
from modules.catalogos.infrastructure.persistence import (
    AreaRepositoryAdapter,
    CargoRepositoryAdapter,
)
from shared.infrastructure.security.security import (
    get_current_user,
    get_current_active_user,
    require_roles,
)
from shared.infrastructure.security.rate_limiter import rate_limiter
from shared.domain.exceptions import BusinessRuleViolationError


router = APIRouter(prefix="/api/empleado", tags=["empleados"])


# DTOs
class LoginRequest(BaseModel):
    """Request para login de empleado."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Response del login."""
    access_token: str
    token_type: str
    empleado: dict


class CreateEmpleadoRequest(BaseModel):
    """Request para crear empleado."""
    nombre: str
    email: EmailStr
    password: Optional[str] = None
    idArea: UUID
    cargos: List[UUID] = []
    acceso_sistema: bool = True


class EmpleadoResponse(BaseModel):
    """Response con datos de empleado."""
    id: str
    nombre: str
    email: str
    idArea: str
    activo: bool


def get_empleado_repository() -> EmpleadoRepository:
    """Factory para obtener el repositorio de empleados."""
    return EmpleadoRepositoryAdapter()


def get_area_repository() -> AreaRepository:
    """Factory para obtener el repositorio de áreas (catálogos)."""
    return AreaRepositoryAdapter()


def get_cargo_repository() -> CargoRepository:
    """Factory para obtener el repositorio de cargos (catálogos)."""
    return CargoRepositoryAdapter()


@router.post("/login", response_model=LoginResponse)
@rate_limiter.limit("5/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    repository: EmpleadoRepository = Depends(get_empleado_repository),
    cargo_repository: CargoRepository = Depends(get_cargo_repository),
) -> LoginResponse:
    """
    Login de empleado.
    Limitado a 5 peticiones/minuto por IP.
    No requiere autenticación previa.
    """
    use_case = LoginEmpleadoUseCase(repository, cargo_repository)
    
    try:
        result = use_case.execute(
            email=login_data.email,
            password=login_data.password,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.get("/", response_model=List[EmpleadoResponse])
async def list_empleados(
    activo: Optional[bool] = None,
    current_user: dict = Depends(get_current_active_user),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> List[EmpleadoResponse]:
    """
    Lista todos los empleados, permitiendo filtrar por estatus activo.
    """
    if activo is not None:
        empleados = repository.get_by_activo(activo)
    else:
        empleados = repository.get_all()
        
    return [
        EmpleadoResponse(
            id=str(emp.id),
            nombre=emp.nombre,
            email=emp.email,
            idArea=str(emp.idArea),
            activo=emp.activo,
        )
        for emp in empleados
    ]


@router.post("/", response_model=EmpleadoResponse, status_code=201)
async def create_empleado(
    request: CreateEmpleadoRequest,
    current_user: dict = Depends(require_roles(["Administrador", "Director"])),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
    area_repository: AreaRepository = Depends(get_area_repository),
    cargo_repository: CargoRepository = Depends(get_cargo_repository),
) -> EmpleadoResponse:
    """
    Crea un nuevo empleado.
    Solo roles "Administrador"/"Director" pueden usarlo.
    Requiere JWT válido.
    """
    use_case = CreateEmpleadoUseCase(repository, area_repository, cargo_repository)
    
    try:
        empleado = use_case.execute(
            nombre=request.nombre,
            email=request.email,
            password=request.password,
            idArea=request.idArea,
            cargos=request.cargos,
            acceso_sistema=request.acceso_sistema,
        )
        
        return EmpleadoResponse(
            id=str(empleado.id),
            nombre=empleado.nombre,
            email=empleado.email,
            idArea=str(empleado.idArea),
            activo=empleado.activo,
        )
    except BusinessRuleViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.patch("/{empleado_id}/estatus", response_model=EmpleadoResponse)
async def update_empleado_estatus(
    empleado_id: UUID,
    activo: bool,
    current_user: dict = Depends(require_roles(["Director"])),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> EmpleadoResponse:
    """
    Actualiza el estatus (activo) de un empleado.
    Solo roles "Director" pueden usarlo.
    Crea automáticamente un registro en HISTORIAL_ESTATUS.
    El idEmpleadoModifica viene del JWT, no del request.
    """
    use_case = UpdateEmpleadoEstatusUseCase(repository)
    
    try:
        use_case.execute(
            id=empleado_id,
            activo=activo,
            idEmpleadoModifica=UUID(current_user["idEmpleado"]),
        )
        
        # Obtener el empleado actualizado
        empleado = repository.get_by_id(empleado_id)
        
        return EmpleadoResponse(
            id=str(empleado.id),
            nombre=empleado.nombre,
            email=empleado.email,
            idArea=str(empleado.idArea),
            activo=empleado.activo,
        )
    except BusinessRuleViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


class ToggleStatusRequest(BaseModel):
    """Request para cambiar de estatus a un empleado."""
    id_administrador: Optional[UUID] = None


class HistorialEstatusResponse(BaseModel):
    """Response con datos de historial de estatus."""
    id: str
    idEmpleadoAfectado: str
    idEmpleadoModifica: str
    accion: str
    fechaRegistro: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EmpleadoDetalleResponse(BaseModel):
    """Response con detalle de empleado e historial de estatus."""
    id: str
    nombre: str
    email: str
    idArea: str
    activo: bool
    historial: List[HistorialEstatusResponse] = []


@router.patch("/{empleado_id}/toggle-status", response_model=EmpleadoResponse)
async def toggle_empleado_status(
    empleado_id: UUID,
    request_data: Optional[ToggleStatusRequest] = None,
    id_administrador: Optional[UUID] = None,
    current_user: dict = Depends(get_current_active_user),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> EmpleadoResponse:
    """
    Invierte el valor de activo del empleado y registra la acción en HISTORIAL_ESTATUS.
    """
    admin_id = None
    if request_data and request_data.id_administrador:
        admin_id = request_data.id_administrador
    elif id_administrador:
        admin_id = id_administrador
    else:
        admin_id = UUID(current_user["idEmpleado"])

    empleado = repository.get_by_id(empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    nuevo_activo = not empleado.activo

    try:
        repository.update_estatus(
            id=empleado_id,
            activo=nuevo_activo,
            idEmpleadoModifica=admin_id,
        )
        
        updated_emp = repository.get_by_id(empleado_id)
        return EmpleadoResponse(
            id=str(updated_emp.id),
            nombre=updated_emp.nombre,
            email=updated_emp.email,
            idArea=str(updated_emp.idArea),
            activo=updated_emp.activo,
        )
    except BusinessRuleViolationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/{empleado_id}", response_model=EmpleadoDetalleResponse)
async def get_empleado_detalle(
    empleado_id: UUID,
    current_user: dict = Depends(get_current_active_user),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> EmpleadoDetalleResponse:
    """
    Obtiene el detalle de un empleado con su historial de estatus ordenado desc.
    """
    empleado = repository.get_by_id(empleado_id)
    if empleado is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    from modules.personal.infrastructure.persistence import HistorialEstatusRepositoryAdapter
    historial_repo = HistorialEstatusRepositoryAdapter()
    historial_items = historial_repo.get_by_empleado(empleado_id)

    return EmpleadoDetalleResponse(
        id=str(empleado.id),
        nombre=empleado.nombre,
        email=empleado.email,
        idArea=str(empleado.idArea),
        activo=empleado.activo,
        historial=[
            HistorialEstatusResponse(
                id=str(item.id),
                idEmpleadoAfectado=str(item.idEmpleadoAfectado),
                idEmpleadoModifica=str(item.idEmpleadoModifica),
                accion=item.accion.value,
                fechaRegistro=str(item.fechaRegistro) if item.fechaRegistro is not None else None,
            )
            for item in historial_items
        ]
    )