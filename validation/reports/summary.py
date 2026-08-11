"""
Validation summary.

Aggregates execution statistics from all validation rules.
"""

from __future__ import annotations

from dataclasses import dataclass

from rules.executor import PipelineResult


@dataclass(slots=True)
class ValidationSummary:
    """
    High-level validation statistics.
    """

    total_rules: int = 0

    successful_rules: int = 0

    failed_rules: int = 0

    rows_processed: int = 0

    rows_modified: int = 0

    rows_flagged: int = 0

    total_errors: int = 0

    total_warnings: int = 0

    total_duration: float = 0.0

    quality_score: float = 100.0

    @classmethod
    def from_pipeline_result(
        cls,
        result: PipelineResult,
    ) -> "ValidationSummary":
        """
        Build summary from PipelineResult.
        """

        errors = sum(
            rule.errors
            for rule in result.rule_results
        )

        warnings = sum(
            rule.warnings
            for rule in result.rule_results
        )

        score = max(
            0.0,
            100.0 - float(errors + warnings),
        )

        return cls(
            total_rules=len(result.rule_results),
            successful_rules=result.successful_rules,
            failed_rules=result.failed_rules,
            rows_processed=result.total_rows_processed,
            rows_modified=result.total_rows_modified,
            rows_flagged=result.total_rows_flagged,
            total_errors=errors,
            total_warnings=warnings,
            total_duration=result.total_duration,
            quality_score=score,
        )