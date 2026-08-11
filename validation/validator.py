"""
Validation facade.
"""

from __future__ import annotations

import pandas as pd

from app.logging import LoggerFactory

from core.context import PipelineContext

from rules.executor import PipelineResult

from .engine import ValidationEngine

logger = LoggerFactory.get_logger(__name__)


class DataValidator:
    """
    High-level validation API.
    """

    def __init__(
        self,
        engine: ValidationEngine | None = None,
    ) -> None:

        self._engine = engine or ValidationEngine()

    @property
    def engine(
        self,
    ) -> ValidationEngine:

        return self._engine

    def validate(
        self,
        dataframe: pd.DataFrame,
        context: PipelineContext | None = None,
    ) -> PipelineResult:

        if context is None:

            context = PipelineContext()

        context.set_dataframe(
            dataframe
        )

        logger.info(
            "Running validation."
        )

        return self._engine.execute(
            context
        )

    def __call__(
        self,
        dataframe: pd.DataFrame,
        context: PipelineContext | None = None,
    ) -> PipelineResult:

        return self.validate(
            dataframe,
            context,
        )


Validator = DataValidator