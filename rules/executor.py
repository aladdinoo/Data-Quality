"""
Rule executor.

This module executes registered data quality rules
in a deterministic order.

The executor is responsible for:

- Executing enabled rules
- Collecting execution results
- Handling failures
- Producing an aggregate execution result
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field

# ==================================================
# Local Imports
# ==================================================

from app.logging import LoggerFactory

from core.context import PipelineContext

from .registry import RuleRegistry
from .result import RuleResult

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)


# ==================================================
# Pipeline Result
# ==================================================

@dataclass(slots=True)
class PipelineResult:
    """
    Aggregate result of all executed rules.
    """

    rule_results: list[RuleResult] = field(
        default_factory=list
    )

    total_duration: float = 0.0

    successful_rules: int = 0

    failed_rules: int = 0

    total_rows_processed: int = 0

    total_rows_modified: int = 0

    total_rows_flagged: int = 0

    total_audit_records: int = 0

    # --------------------------------------------------

    @property
    def success(
        self,
    ) -> bool:

        return self.failed_rules == 0


# ==================================================
# Rule Executor
# ==================================================

class RuleExecutor:
    """
    Executes all registered rules.
    """

    # --------------------------------------------------

    def __init__(
        self,
        registry: RuleRegistry,
    ) -> None:

        self._registry = registry

    # --------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineResult:
        """
        Execute every enabled rule.
        """

        pipeline_result = PipelineResult()

        logger.info(
            "Starting rule execution."
        )

        for rule in self._registry:

            try:

                result = rule.execute(
                    context
                )

                pipeline_result.rule_results.append(
                    result
                )

                pipeline_result.total_duration += (
                    result.duration
                )

                pipeline_result.total_rows_processed += (
                    result.rows_processed
                )

                pipeline_result.total_rows_modified += (
                    result.rows_modified
                )

                pipeline_result.total_rows_flagged += (
                    result.rows_flagged
                )

                pipeline_result.total_audit_records += (
                    result.audit_records
                )

                if result.success:

                    pipeline_result.successful_rules += 1

                else:

                    pipeline_result.failed_rules += 1

            except Exception as exc:

                logger.exception(

                    "Rule '%s' failed.",

                    rule.name,

                )

                pipeline_result.failed_rules += 1

                pipeline_result.rule_results.append(

                    RuleResult(

                        rule=rule.name,

                        version=rule.version,

                        success=False,

                        message=str(exc),

                    )

                )

        logger.info(

            "Finished executing %d rules.",

            len(
                pipeline_result.rule_results
            ),

        )

        return pipeline_result