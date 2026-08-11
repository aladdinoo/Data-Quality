"""
Profiling Metrics.

Defines the metrics collected during dataset profiling.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ProfilingMetrics:
    """
    Dataset quality metrics.
    """

    row_count: int = 0

    column_count: int = 0

    missing_values: int = 0

    duplicate_rows: int = 0

    unique_values: int = 0

    completeness: float = 0.0

    uniqueness: float = 0.0

    memory_usage: int = 0

    def as_dict(self) -> dict[str, object]:
        """
        Convert metrics to dictionary.
        """

        return {
            "row_count": self.row_count,
            "column_count": self.column_count,
            "missing_values": self.missing_values,
            "duplicate_rows": self.duplicate_rows,
            "unique_values": self.unique_values,
            "completeness": self.completeness,
            "uniqueness": self.uniqueness,
            "memory_usage": self.memory_usage,
        }