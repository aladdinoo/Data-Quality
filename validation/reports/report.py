"""
Validation report model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from rules.executor import PipelineResult

from .summary import ValidationSummary


@dataclass(slots=True)
class ValidationReport:
    """
    Represents a complete validation report.
    """

    summary: ValidationSummary

    pipeline_result: PipelineResult

    created_at: datetime = field(
        default_factory=datetime.utcnow,
    )

    dataset_name: str = ""

    total_rows: int = 0

    total_columns: int = 0

    metadata: dict[str, object] = field(
        default_factory=dict,
    )

    @classmethod
    def from_pipeline_result(
        cls,
        result: PipelineResult,
        *,
        dataset_name: str = "",
        total_rows: int = 0,
        total_columns: int = 0,
        metadata: dict[str, object] | None = None,
    ) -> "ValidationReport":
        """
        Create a report from a PipelineResult.
        """

        return cls(
            summary=ValidationSummary.from_pipeline_result(
                result
            ),
            pipeline_result=result,
            dataset_name=dataset_name,
            total_rows=total_rows,
            total_columns=total_columns,
            metadata=metadata or {},
        )