"""
Configuración de la aplicación.
Carga variables de entorno y define configuraciones por defecto.
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación cargada desde variables de entorno.
    """
    
    # Base de datos
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/comunicados_db"
    DATABASE_ECHO: bool = False
    
    # Almacenamiento de archivos
    FILE_STORAGE_PATH: str = "storage"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # Seguridad
    SECRET_KEY: str = "change-this-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()