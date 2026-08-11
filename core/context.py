"""
Pipeline execution context.

This module defines the shared execution context used
throughout the Data Quality Platform.

The PipelineContext carries all runtime objects required
during pipeline execution, allowing stages to communicate
without tight coupling.

Each pipeline stage receives exactly one object:

    PipelineContext

instead of a long list of parameters.

This greatly improves maintainability, extensibility,
and testability.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field
from typing import Any

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd

# ==================================================
# Local Imports
# ==================================================

from app.settings import Settings, settings
from audit.audit_logger import AuditLogger
from core.run import PipelineRun

# ==================================================
# Pipeline Context
# ==================================================


@dataclass(slots=True)
class PipelineContext:
    """
    Shared execution context.

    Every pipeline stage receives and updates
    this object.
    """

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    run: PipelineRun = field(
        default_factory=PipelineRun
    )

    settings: Settings = field(
        default_factory=lambda: settings
    )

    # --------------------------------------------------
    # Data
    # --------------------------------------------------

    raw_dataframe: pd.DataFrame | None = None

    dataframe: pd.DataFrame | None = None

    schema: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Audit
    # --------------------------------------------------

    audit: AuditLogger = field(
        default_factory=AuditLogger
    )

    # --------------------------------------------------
    # Rules
    # --------------------------------------------------

    active_rules: list[str] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Evidence
    # --------------------------------------------------

    evidence: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    metrics: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @property
    def rows(self) -> int:
        """
        Return the current number of rows.
        """

        if self.dataframe is None:
            return 0

        return len(self.dataframe)

    @property
    def columns(self) -> int:
        """
        Return the current number of columns.
        """

        if self.dataframe is None:
            return 0

        return len(self.dataframe.columns)

    @property
    def has_data(self) -> bool:
        """
        Whether a dataframe exists.
        """

        return self.dataframe is not None

    @property
    def has_schema(self) -> bool:
        """
        Whether schema detection has completed.
        """

        return bool(self.schema)

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def set_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Replace the current dataframe.
        """

        self.dataframe = dataframe

    # --------------------------------------------------

    def set_raw_dataframe(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Store the immutable raw dataframe.
        """

        self.raw_dataframe = dataframe

    # --------------------------------------------------

    def add_metric(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a pipeline metric.
        """

        self.metrics[key] = value

    # --------------------------------------------------

    def add_evidence(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store evidence generated during execution.
        """

        self.evidence[key] = value

    # --------------------------------------------------

    def add_metadata(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store execution metadata.
        """

        self.metadata[key] = value

    # --------------------------------------------------

    def register_rule(
        self,
        rule_name: str,
    ) -> None:
        """
        Register an executed rule.
        """

        if rule_name not in self.active_rules:

            self.active_rules.append(
                rule_name
            )