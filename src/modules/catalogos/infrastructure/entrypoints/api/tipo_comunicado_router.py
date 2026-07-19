"""
Router de API para el recurso TipoComunicado.
"""
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ....domain.entities import TipoComunicado
from ....domain.ports import TipoComunicadoRepository
from ....infrastructure.persistence import TipoComunicadoRepositoryAdapter

router = APIRouter(prefix="/tipos-comunicado", tags=["tipos-comunicado"])


def get_tipo_comunicado_repository() -> TipoComunicadoRepository:
    return TipoComunicadoRepositoryAdapter()


@router.post("/", response_model=dict)
async def create_tipo_comunicado(
    nombre: str,
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> dict:
    try:
        tipo = TipoComunicado(nombre=nombre)
        saved = repository.add(tipo)
        return {"id": str(saved.id), "nombre": saved.nombre, "archivado": saved.archivado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/activos", response_model=List[dict])
async def list_tipos_comunicado_activos(
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> List[dict]:
    """Lista solo los tipos de comunicado activos (no archivados). Para dropdowns/checkboxes."""
    tipos = repository.get_activos()
    return [{"id": str(t.id), "nombre": t.nombre, "archivado": t.archivado} for t in tipos]


@router.get("/todos", response_model=List[dict])
async def list_tipos_comunicado_todos(
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> List[dict]:
    """Lista TODOS los tipos de comunicado (activos y archivados). Solo para vista de Configuración."""
    tipos = repository.get_all()
    return [{"id": str(t.id), "nombre": t.nombre, "archivado": t.archivado} for t in tipos]


@router.get("/{tipo_id}", response_model=dict)
async def get_tipo_comunicado(
    tipo_id: UUID,
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> dict:
    tipo = repository.get_by_id(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    return {"id": str(tipo.id), "nombre": tipo.nombre, "archivado": tipo.archivado}


@router.patch("/{tipo_id}/archivar", response_model=dict)
async def archivar_tipo_comunicado(
    tipo_id: UUID,
    archivado: bool,
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> dict:
    """Archiva (True) o desarchiva (False) un tipo de comunicado."""
    tipo = repository.get_by_id(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    
    updated = repository.set_archivado(tipo_id, archivado)
    return {"id": str(updated.id), "nombre": updated.nombre, "archivado": updated.archivado}