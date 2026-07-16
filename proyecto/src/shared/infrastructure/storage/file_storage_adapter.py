"""
Adaptador de almacenamiento de archivos.
Abstrae la operación de guardar/recuperar archivos.
"""
import os
from abc import ABC, abstractmethod
from typing import Optional, BinaryIO


class FileStoragePort(ABC):
    """
    Puerto (interfaz) para el servicio de almacenamiento de archivos.
    """
    
    @abstractmethod
    def save(self, file_content: bytes, filename: str, content_type: str) -> str:
        """
        Guarda un archivo y retorna la URL o ruta del archivo almacenado.
        """
        pass
    
    @abstractmethod
    def get(self, file_path: str) -> Optional[bytes]:
        """
        Recupera el contenido de un archivo por su ruta.
        """
        pass
    
    @abstractmethod
    def delete(self, file_path: str) -> None:
        """
        Elimina un archivo del almacenamiento.
        """
        pass


class LocalFileStorageAdapter(FileStoragePort):
    """
    Adaptador de almacenamiento local de archivos.
    Guarda los archivos en el sistema de archivos local.
    """
    
    def __init__(self, base_path: str = "storage"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def save(self, file_content: bytes, filename: str, content_type: str) -> str:
        """Guarda el archivo localmente y retorna la ruta relativa."""
        safe_filename = f"{os.path.basename(filename)}"
        file_path = os.path.join(self.base_path, safe_filename)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        return file_path
    
    def get(self, file_path: str) -> Optional[bytes]:
        """Recupera el contenido del archivo."""
        full_path = os.path.join(self.base_path, file_path) if not os.path.isabs(file_path) else file_path
        
        if not os.path.exists(full_path):
            return None
        
        with open(full_path, 'rb') as f:
            return f.read()
    
    def delete(self, file_path: str) -> None:
        """Elimina el archivo del sistema."""
        full_path = os.path.join(self.base_path, file_path) if not os.path.isabs(file_path) else file_path
        
        if os.path.exists(full_path):
            os.remove(full_path)