"""
Pipeline run metadata.

This module defines the PipelineRun object used to
track a single execution of the Data Quality Platform.

Each execution receives a unique identifier and stores
timing, versions, execution status, and metadata.

The PipelineRun object is later consumed by:

- Audit
- Lineage
- Monitoring
- Reporting
- Airflow
- Streamlit
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter
from uuid import uuid4

# ==================================================
# Local Imports
# ==================================================

from app.constants import (
    APPLICATION_VERSION,
    PipelineStatus,
)

# ==================================================
# Pipeline Run
# ==================================================


@dataclass(slots=True)
class PipelineRun:
    """
    Represents a single pipeline execution.
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    run_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    pipeline_version: str = APPLICATION_VERSION

    rule_version: str = "1.0.0"

    dataset_version: str = "1.0.0"

    environment: str = "development"

    # --------------------------------------------------
    # Timing
    # --------------------------------------------------

    started_at: datetime = field(
        default_factory=datetime.utcnow
    )

    finished_at: datetime | None = None

    duration_seconds: float = 0.0

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    status: PipelineStatus = PipelineStatus.PENDING

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    rows_processed: int = 0

    rows_failed: int = 0

    rows_cleaned: int = 0

    rules_executed: int = 0

    stages_completed: int = 0

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Internal Timer
    # --------------------------------------------------

    _started_timer: float = field(
        init=False,
        repr=False,
    )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def __post_init__(
        self,
    ) -> None:
        """
        Initialize the internal timer.
        """

        self._started_timer = perf_counter()

    # --------------------------------------------------

    def start(
        self,
    ) -> None:
        """
        Mark the pipeline as running.
        """

        self.status = PipelineStatus.RUNNING

    # --------------------------------------------------

    def finish(
        self,
    ) -> None:
        """
        Mark the pipeline as successful.
        """

        self.finished_at = datetime.utcnow()

        self.duration_seconds = (
            perf_counter()
            - self._started_timer
        )

        self.status = PipelineStatus.SUCCESS

    # --------------------------------------------------

    def fail(
        self,
    ) -> None:
        """
        Mark the pipeline as failed.
        """

        self.finished_at = datetime.utcnow()

        self.duration_seconds = (
            perf_counter()
            - self._started_timer
        )

        self.status = PipelineStatus.FAILED

    # --------------------------------------------------

    def cancel(
        self,
    ) -> None:
        """
        Mark the pipeline as cancelled.
        """

        self.finished_at = datetime.utcnow()

        self.duration_seconds = (
            perf_counter()
            - self._started_timer
        )

        self.status = PipelineStatus.CANCELLED

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    @property
    def successful(
        self,
    ) -> bool:
        """
        Whether execution completed successfully.
        """

        return (
            self.status
            is PipelineStatus.SUCCESS
        )

    @property
    def failed(
        self,
    ) -> bool:
        """
        Whether execution failed.
        """

        return (
            self.status
            is PipelineStatus.FAILED
        )

    # --------------------------------------------------

    def summary(
        self,
    ) -> dict[str, object]:
        """
        Return a serializable execution summary.
        """

        return {

            "run_id": self.run_id,

            "status": self.status.value,

            "started_at": self.started_at,

            "finished_at": self.finished_at,

            "duration_seconds": round(
                self.duration_seconds,
                3,
            ),

            "pipeline_version":
                self.pipeline_version,

            "rule_version":
                self.rule_version,

            "dataset_version":
                self.dataset_version,

            "rows_processed":
                self.rows_processed,

            "rows_cleaned":
                self.rows_cleaned,

            "rows_failed":
                self.rows_failed,

            "rules_executed":
                self.rules_executed,

            "stages_completed":
                self.stages_completed,

        }