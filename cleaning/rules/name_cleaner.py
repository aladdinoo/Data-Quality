"""
Name Cleaning Rule.
"""

from __future__ import annotations

import re

import pandas as pd

from cleaning.result import CleaningResult
from .base import CleaningRule


class NameCleaner(CleaningRule):

    name = "name_cleaner"
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

        if "name" not in dataframe.columns:
            return result

        for index, value in dataframe["name"].items():

            result.rows_processed += 1

            if pd.isna(value):
                continue

            original = str(value)

            cleaned = re.sub(
                r"\s+",
                " ",
                original.strip(),
            )

            cleaned = cleaned.title()

            if cleaned != original:

                dataframe.at[index, "name"] = cleaned

                result.rows_modified += 1

                result.modifications.append(
                    {
                        "row": index,
                        "column": "name",
                        "old": original,
                        "new": cleaned,
                    }
                )

        return result