"""
PII Validation Rule.

Detects Personally Identifiable Information (PII)
inside known sensitive columns.

The rule only flags records for review and never
modifies the original dataset.
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


class PIIValidationRule(BaseRule):
    """
    Detect PII values.
    """

    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_REGEX = re.compile(
        r"^\+?[0-9\s().-]{7,20}$"
    )

    SSN_REGEX = re.compile(
        r"^\d{3}-\d{2}-\d{4}$"
    )

    def __init__(self) -> None:

        metadata = RuleMetadata(
            name="pii_validation",
            version="2.0.0",
            category=RuleCategory.VALIDATION,
            severity=RuleSeverity.WARNING,
            description="Detect Personally Identifiable Information.",
        )

        super().__init__(metadata)

    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:

        result = RuleResult()

        dataframe = context.dataframe

        if dataframe is None:
            return result

        for column in dataframe.columns:

            name = column.lower()

            if "email" in name:
                self._scan_email(
                    dataframe,
                    column,
                    result,
                )

            elif any(
                key in name
                for key in (
                    "phone",
                    "mobile",
                    "cell",
                    "telephone",
                )
            ):
                self._scan_phone(
                    dataframe,
                    column,
                    result,
                )

            elif any(
                key in name
                for key in (
                    "ssn",
                    "passport",
                    "national",
                    "identity",
                    "id_number",
                )
            ):
                self._scan_generic(
                    dataframe,
                    column,
                    result,
                )

        return result

    def _scan_email(
        self,
        dataframe: pd.DataFrame,
        column: str,
        result: RuleResult,
    ) -> None:

        for index, value in dataframe[column].items():

            if pd.isna(value):
                continue

            result.rows_processed += 1

            value = str(value).strip()

            if self.EMAIL_REGEX.fullmatch(value):

                result.rows_flagged += 1
                result.review_required = True

                result.failures.append(
                    {
                        "row": int(index),
                        "column": column,
                        "value": value,
                        "message": "PII Email detected.",
                    }
                )

    def _scan_phone(
        self,
        dataframe: pd.DataFrame,
        column: str,
        result: RuleResult,
    ) -> None:

        for index, value in dataframe[column].items():

            if pd.isna(value):
                continue

            result.rows_processed += 1

            value = str(value).strip()

            if self.PHONE_REGEX.fullmatch(value):

                digits = re.sub(r"\D", "", value)

                if len(digits) >= 7:

                    result.rows_flagged += 1
                    result.review_required = True

                    result.failures.append(
                        {
                            "row": int(index),
                            "column": column,
                            "value": value,
                            "message": "PII Phone detected.",
                        }
                    )

    def _scan_generic(
        self,
        dataframe: pd.DataFrame,
        column: str,
        result: RuleResult,
    ) -> None:

        for index, value in dataframe[column].items():

            if pd.isna(value):
                continue

            result.rows_processed += 1

            value = str(value).strip()

            if value:

                result.rows_flagged += 1
                result.review_required = True

                result.failures.append(
                    {
                        "row": int(index),
                        "column": column,
                        "value": value,
                        "message": "Sensitive identifier detected.",
                    }
                )