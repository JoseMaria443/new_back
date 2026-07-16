"""
Fábrica de parsers de archivos.
Selecciona el parser adecuado según el tipo de contenido.
"""
from typing import Optional, Dict, Any

from .pdf_parser import PDFParserPort, PDFParserAdapter
from .image_parser import ImageParserPort, ImageParserAdapter
from ...domain.exceptions import FileParseError


class ParserFactory:
    """
    Fábrica que selecciona el parser apropiado según el tipo de archivo.
    """
    
    # Mapeo de tipos MIME a extensiones
    PDF_MIME_TYPES = ['application/pdf']
    IMAGE_MIME_TYPES = [
        'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 
        'image/tiff', 'image/webp', 'image/svg+xml'
    ]
    
    def __init__(self):
        self._pdf_parser: Optional[PDFParserPort] = None
        self._image_parser: Optional[ImageParserPort] = None
    
    def get_parser(self, content_type: str) -> Optional[object]:
        """
        Retorna el parser apropiado para el tipo de contenido.
        """
        if content_type in self.PDF_MIME_TYPES:
            if self._pdf_parser is None:
                self._pdf_parser = PDFParserAdapter()
            return self._pdf_parser
        
        if content_type in self.IMAGE_MIME_TYPES:
            if self._image_parser is None:
                self._image_parser = ImageParserAdapter()
            return self._image_parser
        
        return None
    
    def can_parse(self, content_type: str) -> bool:
        """
        Verifica si el tipo de contenido es soportado.
        """
        return content_type in self.PDF_MIME_TYPES or content_type in self.IMAGE_MIME_TYPES
    
    def extract_text(self, file_content: bytes, content_type: str) -> str:
        """
        Extrae texto del archivo según su tipo.
        """
        parser = self.get_parser(content_type)
        
        if parser is None:
            raise FileParseError(f"Tipo de archivo no soportado: {content_type}")
        
        if hasattr(parser, 'extract_text'):
            return parser.extract_text(file_content)
        
        return ""
    
    def extract_metadata(self, file_content: bytes, content_type: str) -> Dict[str, Any]:
        """
        Extrae metadatos del archivo según su tipo.
        """
        parser = self.get_parser(content_type)
        
        if parser is None:
            raise FileParseError(f"Tipo de archivo no soportado: {content_type}")
        
        if hasattr(parser, 'extract_metadata'):
            return parser.extract_metadata(file_content)
        
        return {}