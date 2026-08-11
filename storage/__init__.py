"""
Storage Layer.

Provides a unified interface for reading and writing
datasets from different storage backends.

Supported backends:

- Local File System
- Amazon S3
- ClickHouse
- PostgreSQL
"""

from .base import StorageBackend
from .factory import StorageFactory
from .local import LocalStorage

__all__ = [
    "StorageBackend",
    "StorageFactory",
    "LocalStorage",
]