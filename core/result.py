"""
Pipeline stage execution result.

This module defines the immutable result object returned
by every pipeline stage.

Instead of returning only a DataFrame, each stage returns
a StageResult containing execution status, metrics,
warnings, errors, timing information, and the processed
data.

This standard interface simplifies orchestration,
monitoring, reporting, auditing, and testing.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd

# ==================================================
# Local Imports
# ==================================================

from app.constants import StageStatus

# ==================================================
# Stage Metrics
# ==================================================


@dataclass(slots=True)
class StageMetrics:
    """
    Execution statistics for a pipeline stage.
    """

    rows_before: int = 0

    rows_after: int = 0

    columns: int = 0

    changes: int = 0

    warnings: int = 0

    errors: int = 0


# ==================================================
# Stage Result
# ==================================================


@dataclass(slots=True)
class StageResult:
    """
    Standard result returned by every pipeline stage.

    Parameters
    ----------
    stage
        Stage name.

    status
        Execution status.

    dataframe
        Output dataframe.

    metrics
        Execution metrics.

    warnings
        Warning messages.

    errors
        Error messages.

    metadata
        Additional stage metadata.
    """

    stage: str

    status: StageStatus

    dataframe: pd.DataFrame

    metrics: StageMetrics = field(
        default_factory=StageMetrics
    )

    warnings: list[str] = field(
        default_factory=list
    )

    errors: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    duration: float = 0.0

    # --------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------

    @property
    def successful(self) -> bool:
        """
        Whether the stage completed successfully.
        """

        return self.status is StageStatus.SUCCESS

    @property
    def failed(self) -> bool:
        """
        Whether the stage failed.
        """

        return self.status is StageStatus.FAILED

    @property
    def has_warnings(self) -> bool:
        """
        Whether warnings were generated.
        """

        return bool(self.warnings)

    @property
    def has_errors(self) -> bool:
        """
        Whether errors were generated.
        """

        return bool(self.errors)

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:
        """
        Add a warning message.
        """

        self.warnings.append(message)

        self.metrics.warnings += 1

    # --------------------------------------------------

    def add_error(
        self,
        message: str,
    ) -> None:
        """
        Add an error message.
        """

        self.errors.append(message)

        self.metrics.errors += 1

    # --------------------------------------------------

    def update_duration(
        self,
        started_at: float,
    ) -> None:
        """
        Compute execution duration.

        Parameters
        ----------
        started_at
            Start time obtained using perf_counter().
        """

        self.duration = perf_counter() - started_at

    # --------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """
        Return a serializable execution summary.
        """

        return {

            "stage": self.stage,

            "status": self.status.value,

            "duration_seconds": round(
                self.duration,
                3,
            ),

            "rows_before": self.metrics.rows_before,

            "rows_after": self.metrics.rows_after,

            "columns": self.metrics.columns,

            "changes": self.metrics.changes,

            "warnings": self.metrics.warnings,

            "errors": self.metrics.errors,

        }