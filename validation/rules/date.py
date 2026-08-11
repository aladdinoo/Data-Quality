"""
Date Validation Rule.

Validate date columns.
"""

from __future__ import annotations

import pandas as pd

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity


class DateValidationRule(BaseRule):
    """
    Validate dates.
    """

    def __init__(self) -> None:

        super().__init__(
            RuleMetadata(
                name="date_validation",
                version="2.0.0",
                category=RuleCategory.VALIDATION,
                severity=RuleSeverity.ERROR,
                description="Validate date values.",
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

        candidate_columns = [

            column

            for column in dataframe.columns

            if any(

                keyword in column.lower()

                for keyword in (

                    "date",

                    "time",

                    "created",

                    "updated",

                    "birth",

                )

            )

        ]

        for column in candidate_columns:

            parsed = pd.to_datetime(

                dataframe[column],

                errors="coerce",

            )

            invalid = parsed.isna() & dataframe[column].notna()

            for index in dataframe[invalid].index:

                result.add_failure(

                    row=int(index),

                    column=column,

                    value=dataframe.at[index, column],

                    message="Invalid date.",

                )

        return result