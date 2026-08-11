"""
Duplicate Validation Rule.

Detect duplicate rows inside a dataset.
"""

from __future__ import annotations

import pandas as pd

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity


class DuplicateValidationRule(BaseRule):
    """
    Detect duplicate records.
    """

    def __init__(self) -> None:

        super().__init__(
            RuleMetadata(
                name="duplicate_validation",
                version="2.0.0",
                category=RuleCategory.VALIDATION,
                severity=RuleSeverity.WARNING,
                description="Detect duplicate rows.",
            )
        )

    # --------------------------------------------------

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        dataframe = context.dataframe

        if dataframe is None:

            return result

        duplicates = dataframe.duplicated(
            keep=False
        )

        if not duplicates.any():

            return result

        for index in dataframe[duplicates].index:

            result.add_failure(

                row=int(index),

                column="*",

                value=None,

                message="Duplicate record detected.",

            )

        return result