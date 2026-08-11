from __future__ import annotations

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity

from validators.zip import ZipValidator


class ZipValidationRule(BaseRule):

    def __init__(self) -> None:

        super().__init__(
            RuleMetadata(
                name="zip_validation",
                version="2.0.0",
                category=RuleCategory.VALIDATION,
                severity=RuleSeverity.WARNING,
                description="Validate ZIP/Postal codes.",
            )
        )

        self.validator = ZipValidator()

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        df = context.dataframe

        if df is None or "zip" not in df.columns:
            return result

        for index, value in df["zip"].items():

            if value is None:
                continue

            if not self.validator.is_valid(str(value)):

                result.add_failure(
                    row=index,
                    column="zip",
                    value=value,
                    message="Invalid ZIP code.",
                )

        return result