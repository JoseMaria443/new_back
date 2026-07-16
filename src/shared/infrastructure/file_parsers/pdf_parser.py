"""
Parser para archivos PDF.
Extrae texto y metadatos de documentos PDF.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any


class PDFParserPort(ABC):
    """
    Puerto (interfaz) para el parser de PDF.
    """
    
    @abstractmethod
    def extract_text(self, file_content: bytes) -> str:
        """
        Extrae el texto de un archivo PDF.
        """
        pass
    
    @abstractmethod
    def extract_metadata(self, file_content: bytes) -> Dict[str, Any]:
        """
        Extrae los metadatos de un archivo PDF.
        """
        pass


class PDFParserAdapter(PDFParserPort):
    """
    Adaptador para parsear archivos PDF usando pypdf.
    """
    
    def __init__(self):
        try:
            from pypdf import PdfReader
            self.PdfReader = PdfReader
        except ImportError:
            raise ImportError("pypdf no está instalado. Ejecuta: pip install pypdf")
    
    def extract_text(self, file_content: bytes) -> str:
        """Extrae el texto de un archivo PDF."""
        import io
        
        text_parts: List[str] = []
        reader = self.PdfReader(io.BytesIO(file_content))
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        return "\n".join(text_parts)
    
    def extract_metadata(self, file_content: bytes) -> Dict[str, Any]:
        """Extrae los metadatos de un archivo PDF."""
        import io
        
        reader = self.PdfReader(io.BytesIO(file_content))
        metadata = reader.metadata
        
        return {
            "title": metadata.title if metadata else None,
            "author": metadata.author if metadata else None,
            "subject": metadata.subject if metadata else None,
            "creator": metadata.creator if metadata else None,
            "producer": metadata.producer if metadata else None,
            "creation_date": str(metadata.creation_date) if metadata and metadata.creation_date else None,
            "modification_date": str(metadata.modification_date) if metadata and metadata.modification_date else None,
        }