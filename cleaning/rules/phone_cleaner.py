"""
Phone Cleaning Rule.
"""

from __future__ import annotations

import re

import pandas as pd

from cleaning.result import CleaningResult
from .base import CleaningRule


class PhoneCleaner(CleaningRule):

    name = "phone_cleaner"
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

        if "phone" not in dataframe.columns:
            return result

        for index, value in dataframe["phone"].items():

            result.rows_processed += 1

            if pd.isna(value):
                continue

            original = str(value)

            cleaned = re.sub(
                r"[^\d+]",
                "",
                original.strip(),
            )

            if cleaned != original:

                dataframe.at[index, "phone"] = cleaned

                result.rows_modified += 1

                result.modifications.append(
                    {
                        "row": index,
                        "column": "phone",
                        "old": original,
                        "new": cleaned,
                    }
                )

        return result