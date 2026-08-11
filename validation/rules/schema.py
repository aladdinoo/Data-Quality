"""
Schema Validation Rule.

Validate dataset schema.
"""

from __future__ import annotations

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity


class SchemaValidationRule(BaseRule):

    def __init__(self) -> None:

        super().__init__(
            RuleMetadata(
                name="schema_validation",
                version="2.0.0",
                category=RuleCategory.VALIDATION,
                severity=RuleSeverity.CRITICAL,
                description="Validate dataset schema.",
            )
        )

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        dataframe = context.dataframe

        expected_schema = context.schema

        if dataframe is None:

            return result

        if not expected_schema:

            return result

        expected_columns = set(expected_schema.keys())

        actual_columns = set(dataframe.columns)

        missing = expected_columns - actual_columns

        extra = actual_columns - expected_columns

        for column in sorted(missing):

            result.add_failure(
                row=-1,
                column=column,
                value=None,
                message="Missing required column.",
            )

        for column in sorted(extra):

            result.add_failure(
                row=-1,
                column=column,
                value=None,
                message="Unexpected column.",
            )

        return result