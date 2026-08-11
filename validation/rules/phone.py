from __future__ import annotations

from core.context import PipelineContext

from rules.base import BaseRule
from rules.category import RuleCategory
from rules.metadata import RuleMetadata
from rules.result import RuleResult
from rules.severity import RuleSeverity

from validators.phone import PhoneValidator


class PhoneValidationRule(BaseRule):

    def __init__(self) -> None:

        super().__init__(
            RuleMetadata(
                name="phone_validation",
                version="2.0.0",
                category=RuleCategory.VALIDATION,
                severity=RuleSeverity.ERROR,
                description="Validate phone numbers.",
            )
        )

        self.validator = PhoneValidator()

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        df = context.dataframe

        if df is None or "phone" not in df.columns:
            return result

        for index, value in df["phone"].items():

            if value is None:
                continue

            if not self.validator.is_valid(str(value)):

                result.add_failure(
                    row=index,
                    column="phone",
                    value=value,
                    message="Invalid phone number.",
                )

        return result