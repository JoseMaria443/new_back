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
        return {"id": str(saved.id), "nombre": saved.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[dict])
async def list_tipos_comunicado(
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> List[dict]:
    tipos = repository.get_all()
    return [{"id": str(t.id), "nombre": t.nombre} for t in tipos]


@router.get("/{tipo_id}", response_model=dict)
async def get_tipo_comunicado(
    tipo_id: UUID,
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> dict:
    tipo = repository.get_by_id(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    return {"id": str(tipo.id), "nombre": tipo.nombre}


@router.put("/{tipo_id}", response_model=dict)
async def update_tipo_comunicado(
    tipo_id: UUID,
    nombre: str,
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> dict:
    tipo = repository.get_by_id(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    
    try:
        tipo.nombre = nombre
        updated = repository.update(tipo)
        return {"id": str(updated.id), "nombre": updated.nombre}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{tipo_id}", status_code=204)
async def delete_tipo_comunicado(
    tipo_id: UUID,
    repository: TipoComunicadoRepository = Depends(get_tipo_comunicado_repository)
) -> None:
    tipo = repository.get_by_id(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail="Tipo de comunicado no encontrado")
    repository.delete(tipo_id)