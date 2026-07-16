"""
Parser para archivos de imagen.
Extrae metadatos y dimensiones de imágenes.
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class ImageParserPort(ABC):
    """
    Puerto (interfaz) para el parser de imágenes.
    """
    
    @abstractmethod
    def extract_metadata(self, file_content: bytes) -> Dict[str, Any]:
        """
        Extrae los metadatos de una imagen.
        """
        pass
    
    @abstractmethod
    def get_dimensions(self, file_content: bytes) -> Dict[str, int]:
        """
        Obtiene las dimensiones de la imagen.
        """
        pass


class ImageParserAdapter(ImageParserPort):
    """
    Adaptador para parsear imágenes usando Pillow.
    """
    
    def __init__(self):
        try:
            from PIL import Image
            self.Image = Image
        except ImportError:
            raise ImportError("Pillow no está instalado. Ejecuta: pip install Pillow")
    
    def extract_metadata(self, file_content: bytes) -> Dict[str, Any]:
        """Extrae los metadatos de una imagen."""
        import io
        
        image = self.Image.open(io.BytesIO(file_content))
        
        return {
            "format": image.format,
            "mode": image.mode,
            "width": image.width,
            "height": image.height,
        }
    
    def get_dimensions(self, file_content: bytes) -> Dict[str, int]:
        """Obtiene las dimensiones de la imagen."""
        import io
        
        image = self.Image.open(io.BytesIO(file_content))
        
        return {
            "width": image.width,
            "height": image.height,
        }