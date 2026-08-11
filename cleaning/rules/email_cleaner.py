"""
Email Cleaning Rule.
"""

from __future__ import annotations

import re

import pandas as pd

from cleaning.result import CleaningResult

from .base import CleaningRule


EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


class EmailCleaner(CleaningRule):

    name = "email_cleaner"
    version = "1.0.0"

    auto_apply = True
    review_required = False

    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> CleaningResult:

        result = CleaningResult(
            cleaner=self.name,
            success=True,
        )

        if "email" not in dataframe.columns:
            return result

        for index, value in dataframe["email"].items():

            result.rows_processed += 1

            if pd.isna(value):
                continue

            original = str(value)

            cleaned = (
                original.strip()
                .lower()
                .replace(" ", "")
            )

            if cleaned != original:

                dataframe.at[index, "email"] = cleaned

                result.rows_modified += 1

                result.modifications.append(
                    {
                        "row": index,
                        "column": "email",
                        "old": original,
                        "new": cleaned,
                    }
                )

            if not EMAIL_PATTERN.fullmatch(cleaned):

                result.rows_flagged += 1

                result.modifications.append(
                    {
                        "row": index,
                        "column": "email",
                        "value": cleaned,
                        "reason": "Invalid email",
                    }
                )

        return result