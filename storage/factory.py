"""
Storage Factory.
"""

from __future__ import annotations

from .clickhouse import ClickHouseStorage
from .local import LocalStorage
from .postgres import PostgresStorage
from .s3 import S3Storage


class StorageFactory:
    """
    Create storage backend instances.
    """

    @staticmethod
    def create(
        backend: str,
    ):

        backend = backend.lower()

        if backend == "local":
            return LocalStorage()

        if backend == "s3":
            return S3Storage()

        if backend == "clickhouse":
            return ClickHouseStorage()

        if backend == "postgres":
            return PostgresStorage()

        raise ValueError(
            f"Unsupported storage backend: {backend}"
        )