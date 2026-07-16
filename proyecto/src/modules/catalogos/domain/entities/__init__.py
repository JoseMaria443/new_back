"""
Entidades del módulo de catálogos.
"""
from .area import Area
from .cargo import Cargo
from .tipo_comunicado import TipoComunicado
from .medio_recepcion import MedioRecepcion
from .rol_destinatario import RolDestinatario
from .rol_responsable import RolResponsable
from .estado_tarea import EstadoTarea

__all__ = [
    "Area",
    "Cargo",
    "TipoComunicado",
    "MedioRecepcion",
    "RolDestinatario",
    "RolResponsable",
    "EstadoTarea",
]