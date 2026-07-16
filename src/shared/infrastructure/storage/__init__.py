"""
Adaptadores de almacenamiento de archivos.
"""
from .file_storage_adapter import FileStoragePort, LocalFileStorageAdapter

__all__ = ["FileStoragePort", "LocalFileStorageAdapter"]