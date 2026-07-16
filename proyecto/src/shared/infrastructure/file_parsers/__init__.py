"""
Parsers de archivos: PDF, imágenes y fábrica.
"""
from .pdf_parser import PDFParserPort, PDFParserAdapter
from .image_parser import ImageParserPort, ImageParserAdapter
from .parser_factory import ParserFactory

__all__ = [
    "PDFParserPort",
    "PDFParserAdapter",
    "ImageParserPort",
    "ImageParserAdapter",
    "ParserFactory",
]