"""
Rule execution result.

This module defines the result returned after executing
a data quality rule.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RuleResult:
    """
    Result produced by a rule execution.
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    rule: str = ""
    version: str = ""

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    success: bool = True
    message: str = ""
    duration: float = 0.0

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    rows_processed: int = 0
    rows_modified: int = 0
    rows_flagged: int = 0

    errors: int = 0
    warnings: int = 0

    # --------------------------------------------------
    # Quality
    # --------------------------------------------------

    quality_score: float | None = None

    # --------------------------------------------------
    # Audit
    # --------------------------------------------------

    audit_records: int = 0

    review_required: bool = False

    # --------------------------------------------------
    # Extra
    # --------------------------------------------------

    metrics: dict[str, float] = field(default_factory=dict)

    details: dict[str, object] = field(default_factory=dict)

    failures: list[dict] = field(default_factory=list)

    # ==================================================
    # Helpers
    # ==================================================

    def add_failure(
        self,
        *,
        row: int,
        column: str,
        value: object,
        message: str,
    ) -> None:
        """
        Register a validation failure.
        """

        self.failures.append(
            {
                "row": row,
                "column": column,
                "value": value,
                "message": message,
            }
        )

        self.rows_flagged += 1
        self.errors += 1
        self.success = False

    # --------------------------------------------------

    def add_warning(
        self,
        *,
        row: int,
        column: str,
        value: object,
        message: str,
    ) -> None:
        """
        Register a warning.
        """

        self.failures.append(
            {
                "row": row,
                "column": column,
                "value": value,
                "message": message,
                "level": "warning",
            }
        )

        self.rows_flagged += 1
        self.warnings += 1

    # --------------------------------------------------

    def add_metric(
        self,
        key: str,
        value: float,
    ) -> None:

        self.metrics[key] = value

    # --------------------------------------------------

    @property
    def has_changes(self) -> bool:
        return self.rows_modified > 0

    @property
    def has_flags(self) -> bool:
        return self.rows_flagged > 0

    @property
    def has_errors(self) -> bool:
        return self.errors > 0

    @property
    def has_warnings(self) -> bool:
        return self.warnings > 0

    # --------------------------------------------------

    def merge(
        self,
        other: "RuleResult",
    ) -> None:

        self.rows_processed += other.rows_processed
        self.rows_modified += other.rows_modified
        self.rows_flagged += other.rows_flagged

        self.errors += other.errors
        self.warnings += other.warnings

        self.audit_records += other.audit_records
        self.duration += other.duration

        self.success = self.success and other.success

        self.review_required = (
            self.review_required
            or other.review_required
        )

        self.metrics.update(other.metrics)
        self.details.update(other.details)
        self.failures.extend(other.failures)