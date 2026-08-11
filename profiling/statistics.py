"""
Dataset statistics.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DatasetStatistics:
    """
    Column-level statistics.
    """

    numeric_columns: list[str] = field(
        default_factory=list
    )

    categorical_columns: list[str] = field(
        default_factory=list
    )

    datetime_columns: list[str] = field(
        default_factory=list
    )

    object_columns: list[str] = field(
        default_factory=list
    )

    boolean_columns: list[str] = field(
        default_factory=list
    )

    def as_dict(self) -> dict[str, object]:

        return {

            "numeric_columns": self.numeric_columns,

            "categorical_columns": self.categorical_columns,

            "datetime_columns": self.datetime_columns,

            "object_columns": self.object_columns,

            "boolean_columns": self.boolean_columns,

        }