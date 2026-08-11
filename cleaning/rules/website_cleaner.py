"""
Website Cleaning Rule.
"""

from __future__ import annotations

import re

import pandas as pd

from cleaning.result import CleaningResult
from .base import CleaningRule


DOMAIN_PATTERN = re.compile(
    r"^(https?://)?([A-Za-z0-9-]+\.)+[A-Za-z]{2,}(/.*)?$"
)


class WebsiteCleaner(CleaningRule):

    name = "website_cleaner"
    version = "2.0.0"

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

        if "website" not in dataframe.columns:
            return result

        for index, value in dataframe["website"].items():

            result.rows_processed += 1

            if pd.isna(value):
                continue

            original = str(value).strip()

            cleaned = original

            # --------------------------------------
            # Fix common protocol mistakes
            # --------------------------------------

            replacements = {

                "htp://": "http://",
                "htps://": "https://",
                "ttp://": "http://",
                "ttps://": "https://",

                "htp:/": "http://",
                "http:/": "http://",
                "https:/": "https://",
                "htps:/": "https://",

            }

            for wrong, correct in replacements.items():

                if cleaned.startswith(wrong):

                    cleaned = correct + cleaned[len(wrong):]

                    break

            # --------------------------------------
            # Add https if only domain exists
            # --------------------------------------

            if (
                not cleaned.startswith("http://")
                and not cleaned.startswith("https://")
            ):

                if re.fullmatch(
                    r"([A-Za-z0-9-]+\.)+[A-Za-z]{2,}",
                    cleaned,
                ):

                    cleaned = "https://" + cleaned

            # --------------------------------------
            # Validate final URL
            # --------------------------------------

            if DOMAIN_PATTERN.fullmatch(cleaned):

                if cleaned != original:

                    dataframe.at[index, "website"] = cleaned

                    result.rows_modified += 1

                    result.modifications.append(
                        {
                            "row": index,
                            "column": "website",
                            "old": original,
                            "new": cleaned,
                            "reason": "Normalized website",
                        }
                    )

            else:

                result.rows_flagged += 1

                result.modifications.append(
                    {
                        "row": index,
                        "column": "website",
                        "value": original,
                        "reason": "Invalid website - review required",
                    }
                )

        return result