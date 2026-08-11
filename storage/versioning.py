"""
Dataset Versioning.

Tracks dataset versions written
by the platform.
"""

from __future__ import annotations

from dataclasses import dataclass

from datetime import datetime


@dataclass(slots=True)
class DatasetVersion:
    """
    Dataset version metadata.
    """

    dataset: str

    version: str

    created_at: datetime

    created_by: str

    checksum: str

    row_count: int

    schema_version: str

    def as_dict(self) -> dict:

        return {

            "dataset": self.dataset,

            "version": self.version,

            "created_at": self.created_at.isoformat(),

            "created_by": self.created_by,

            "checksum": self.checksum,

            "row_count": self.row_count,

            "schema_version": self.schema_version,

        }