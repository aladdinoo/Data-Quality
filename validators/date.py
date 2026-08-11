"""
Date validation utilities.
"""

from __future__ import annotations

from datetime import datetime
from typing import Final


class DateValidator:
    """
    Validate date values.

    Multiple common date formats are supported.
    """

    SUPPORTED_FORMATS: Final[tuple[str, ...]] = (

        "%Y-%m-%d",

        "%d/%m/%Y",

        "%m/%d/%Y",

        "%Y/%m/%d",

        "%d-%m-%Y",

    )

    def is_valid(
        self,
        value: object,
    ) -> bool:
        """
        Return True if the value is a valid date.
        """

        if value is None:
            return False

        text = str(value).strip()

        if not text:
            return False

        for date_format in self.SUPPORTED_FORMATS:

            try:

                datetime.strptime(
                    text,
                    date_format,
                )

                return True

            except ValueError:

                continue

        return False