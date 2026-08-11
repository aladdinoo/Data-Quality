"""
Abstract pipeline stage.

This module defines the abstract base class implemented
by every pipeline stage.

Each stage receives a shared PipelineContext and returns
a StageResult.

Stages should contain business logic only.
They should never orchestrate other stages.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from abc import ABC, abstractmethod
from time import perf_counter

# ==================================================
# Local Imports
# ==================================================

from app.constants import StageStatus
from app.logging import LoggerFactory
from core.context import PipelineContext
from core.result import StageMetrics, StageResult

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# Pipeline Stage
# ==================================================


class PipelineStage(ABC):
    """
    Abstract base class for every pipeline stage.

    All stages must inherit from this class and implement
    the process() method.

    Execution flow:

        execute()
              │
              ▼
          process()
              │
              ▼
        StageResult
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(
        self,
        name: str,
    ) -> None:
        """
        Initialize the stage.

        Parameters
        ----------
        name
            Human-readable stage name.
        """

        self._name = name

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Return the stage name.
        """

        return self._name

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> StageResult:
        """
        Execute the stage.

        Parameters
        ----------
        context
            Shared pipeline execution context.

        Returns
        -------
        StageResult
            Stage execution result.
        """

        logger.info(
            "Starting stage: %s",
            self.name,
        )

        started = perf_counter()

        metrics = StageMetrics()

        if context.dataframe is not None:

            metrics.rows_before = len(
                context.dataframe
            )

            metrics.columns = len(
                context.dataframe.columns
            )

        try:

            self.process(
                context,
                metrics,
            )

            if context.dataframe is not None:

                metrics.rows_after = len(
                    context.dataframe
                )

            result = StageResult(

                stage=self.name,

                status=StageStatus.SUCCESS,

                dataframe=context.dataframe,

                metrics=metrics,

            )

        except Exception as exc:

            logger.exception(
                "Stage failed: %s",
                self.name,
            )

            result = StageResult(

                stage=self.name,

                status=StageStatus.FAILED,

                dataframe=context.dataframe,

                metrics=metrics,

            )

            result.add_error(
                str(exc)
            )

        result.update_duration(
            started
        )

        logger.info(
            "Finished stage: %s (%.3f sec)",
            self.name,
            result.duration,
        )

        return result

    # --------------------------------------------------
    # Abstract API
    # --------------------------------------------------

    @abstractmethod
    def process(
        self,
        context: PipelineContext,
        metrics: StageMetrics,
    ) -> None:
        """
        Execute the business logic.

        Parameters
        ----------
        context
            Shared execution context.

        metrics
            Stage metrics that may be updated
            during processing.
        """

        raise NotImplementedError