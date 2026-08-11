"""
Name Validation Rule.

Validates person names.

The rule detects obviously invalid names without modifying
the original dataset.
"""

from __future__ import annotations

import re

import pandas as pd

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity


class NameValidationRule(BaseRule):
    """
    Validate names.
    """

    def __init__(self) -> None:

        metadata = RuleMetadata(
            name="name_validation",
            version="2.0.0",
            category=RuleCategory.VALIDATION,
            severity=RuleSeverity.WARNING,
            description="Validate person names.",
        )

        super().__init__(metadata)

        self._pattern = re.compile(
            r"^[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ ,.'-]{1,100}$"
        )

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        dataframe = context.dataframe

        if dataframe is None:
            return result

        candidate_columns = [
            c for c in dataframe.columns
            if "name" in c.lower()
        ]

        if not candidate_columns:
            return result

        for column in candidate_columns:

            for index, value in dataframe[column].items():

                if pd.isna(value):
                    continue

                value = str(value).strip()

                if value == "":
                    continue

                result.rows_processed += 1

                if not self._pattern.fullmatch(value):

                    result.rows_flagged += 1
                    result.warnings += 1
                    result.review_required = True

                    result.failures.append(
                        {
                            "row": int(index),
                            "column": column,
                            "value": value,
                            "message": "Invalid person name.",
                        }
                    )

        return result