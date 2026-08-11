"""
Pipeline orchestration engine.

This module defines the main Pipeline class responsible
for orchestrating pipeline stages.

The pipeline itself contains no business logic.
Instead, it executes a sequence of PipelineStage
objects using a shared PipelineContext.

Responsibilities
----------------
- Stage execution
- Error handling
- Run lifecycle
- Logging
- Result collection
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from typing import Iterable

# ==================================================
# Local Imports
# ==================================================

from app.logging import LoggerFactory
from core.context import PipelineContext
from core.result import StageResult
from core.stage import PipelineStage
from app.exceptions import StageExecutionError

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# Pipeline
# ==================================================


class Pipeline:
    """
    Main pipeline orchestrator.

    The pipeline executes stages sequentially using
    a shared PipelineContext.
    """

    def __init__(
        self,
        stages: Iterable[PipelineStage],
    ) -> None:

        self._stages = list(stages)

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def run(
        self,
        context: PipelineContext,
    ) -> list[StageResult]:
        """
        Execute all pipeline stages.

        Parameters
        ----------
        context
            Shared execution context.

        Returns
        -------
        list[StageResult]
            Results from every executed stage.
        """

        logger.info(
            "Pipeline started."
        )

        context.run.start()

        results: list[StageResult] = []

        try:

            for stage in self._stages:

                logger.info(
                    "Executing stage: %s",
                    stage.name,
                )

                result = stage.execute(
                    context
                )

                results.append(
                    result
                )

                context.run.stages_completed += 1

                if result.failed:

                    raise StageExecutionError(
                        f"{stage.name} failed."
                    )

            context.run.finish()

            logger.info(
                "Pipeline completed successfully."
            )

            return results

        except Exception:

            context.run.fail()

            logger.exception(
                "Pipeline execution failed."
            )

            raise

    # --------------------------------------------------

    @property
    def stages(
        self,
    ) -> tuple[PipelineStage, ...]:
        """
        Return registered stages.
        """

        return tuple(
            self._stages
        )

    # --------------------------------------------------

    def add_stage(
        self,
        stage: PipelineStage,
    ) -> None:
        """
        Append a stage to the pipeline.
        """

        self._stages.append(
            stage
        )

    # --------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove all stages.
        """

        self._stages.clear()

    # --------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Return the number of registered stages.
        """

        return len(
            self._stages
        )

    # --------------------------------------------------

    def __iter__(
        self,
    ):
        """
        Iterate over registered stages.
        """

        return iter(
            self._stages
        )