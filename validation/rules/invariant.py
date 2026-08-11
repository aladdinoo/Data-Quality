"""
Invariant Validation Rule.

Validate business invariants.
"""

from __future__ import annotations

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity


class InvariantValidationRule(BaseRule):

    def __init__(self) -> None:

        super().__init__(
            RuleMetadata(
                name="invariant_validation",
                version="2.0.0",
                category=RuleCategory.VALIDATION,
                severity=RuleSeverity.ERROR,
                description="Validate business invariants.",
            )
        )

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        dataframe = context.dataframe

        if dataframe is None:

            return result

        if "age" in dataframe.columns:

            invalid = dataframe["age"] < 0

            for index in dataframe[invalid].index:

                result.add_failure(
                    row=int(index),
                    column="age",
                    value=dataframe.at[index, "age"],
                    message="Negative age.",
                )

        if {
            "start_date",
            "end_date",
        }.issubset(dataframe.columns):

            invalid = dataframe["start_date"] > dataframe["end_date"]

            for index in dataframe[invalid].index:

                result.add_failure(
                    row=int(index),
                    column="end_date",
                    value=dataframe.at[index, "end_date"],
                    message="End date before start date.",
                )

        return result