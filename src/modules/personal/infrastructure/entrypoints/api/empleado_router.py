"""
Router de API para el recurso Empleado.
Endpoints: /api/empleado (login, create) y /api/empleado/{id}/estatus
"""
from uuid import UUID
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from ....domain.entities import Empleado
from ....domain.ports import EmpleadoRepository
from ....infrastructure.persistence import EmpleadoRepositoryAdapter
from ....application.use_cases import (
    LoginEmpleadoUseCase,
    CreateEmpleadoUseCase,
    UpdateEmpleadoEstatusUseCase,
)
from shared.infrastructure.security.security import (
    get_current_user,
    get_current_active_user,
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
    password: str
    idArea: UUID
    cargos: List[UUID] = []


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


@router.post("/login", response_model=LoginResponse)
@rate_limiter.limit("5/minute")
async def login(
    request: LoginRequest,
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> LoginResponse:
    """
    Login de empleado.
    Limitado a 5 peticiones/minuto por IP.
    No requiere autenticación previa.
    """
    use_case = LoginEmpleadoUseCase(repository)
    
    try:
        result = use_case.execute(
            email=request.email,
            password=request.password,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/", response_model=EmpleadoResponse, status_code=201)
async def create_empleado(
    request: CreateEmpleadoRequest,
    current_user: dict = Depends(get_current_active_user),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> EmpleadoResponse:
    """
    Crea un nuevo empleado.
    Solo roles "Administrador"/"Director" pueden usarlo.
    Requiere JWT válido.
    """
    # TODO: Validar que el usuario tenga rol "Administrador" o "Director"
    # Esto se haría verificando los cargos/roles del current_user
    
    use_case = CreateEmpleadoUseCase(repository)
    
    try:
        empleado = use_case.execute(
            nombre=request.nombre,
            email=request.email,
            password=request.password,
            idArea=request.idArea,
            roles=[],
            cargos=request.cargos,
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
    current_user: dict = Depends(get_current_active_user),
    repository: EmpleadoRepository = Depends(get_empleado_repository),
) -> EmpleadoResponse:
    """
    Actualiza el estatus (activo) de un empleado.
    Solo roles "Director" pueden usarlo.
    Crea automáticamente un registro en HISTORIAL_ESTATUS.
    El idEmpleadoModifica viene del JWT, no del request.
    """
    # TODO: Validar que el usuario tenga rol "Director"
    
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