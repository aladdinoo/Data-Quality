"""
Validation policies.

Lifecycle hooks executed before and after validation.
"""

from __future__ import annotations

from app.logging import LoggerFactory

from core.context import PipelineContext

from rules.executor import PipelineResult

logger = LoggerFactory.get_logger(__name__)


class ValidationPolicy:
    """
    Validation lifecycle policy.
    """

    def before_validation(
        self,
        context: PipelineContext,
    ) -> None:

        logger.info(
            "Validation started."
        )

        context.add_metadata(

            "validation_started",

            True,

        )

    # --------------------------------------------------

    def after_validation(
        self,
        context: PipelineContext,
        result: PipelineResult,
    ) -> None:

        context.add_metadata(

            "validation_finished",

            True,

        )

        context.add_metric(

            "validation_success",

            result.success,

        )

        logger.info(
            "Validation finished."
        )