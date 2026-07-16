"""
Punto de entrada principal de la aplicación.
Configura y ejecuta el servidor FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings

# Crear la aplicación FastAPI
app = FastAPI(
    title="API de Comunicados Institucionales",
    description="Sistema de gestión de comunicados, tareas y evidencias universitarias",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers del módulo de catálogos
from modules.catalogos.infrastructure.entrypoints.api import (
    area_router,
    cargo_router,
    tipo_comunicado_router,
    medio_recepcion_router,
    rol_destinatario_router,
    rol_responsable_router,
    estado_tarea_router,
)

# Registrar routers
app.include_router(area_router)
app.include_router(cargo_router)
app.include_router(tipo_comunicado_router)
app.include_router(medio_recepcion_router)
app.include_router(rol_destinatario_router)
app.include_router(rol_responsable_router)
app.include_router(estado_tarea_router)


@app.get("/")
async def root():
    """Endpoint raíz de la API."""
    return {
        "message": "API de Comunicados Institucionales",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )