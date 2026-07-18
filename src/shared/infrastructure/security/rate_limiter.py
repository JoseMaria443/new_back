"""
Rate limiting para proteger endpoints sensibles.
Usa slowapi para limitar peticiones por IP.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


# Limiter global configurado para usar IP del cliente
limiter = Limiter(key_func=get_remote_address)


async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    """
    Manejador de excepción para rate limiting.
    Retorna una respuesta 429 Too Many Requests.
    """
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Demasiadas peticiones. Por favor, espere antes de intentar nuevamente."
        }
    )


# Decorador para aplicar rate limiting
rate_limiter = limiter