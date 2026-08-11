"""
ZIP / Postal Code validation utilities.
"""

from __future__ import annotations

import re


class ZipValidator:
    """
    Validate ZIP or Postal Codes.
    """

    ZIP_PATTERN = re.compile(

        r"^[A-Za-z0-9\- ]{3,12}$"

    )

    def is_valid(
        self,
        value: str,
    ) -> bool:
        """
        Return True if the ZIP code is valid.
        """

        value = value.strip()

        if not value:

            return False

        return bool(

            self.ZIP_PATTERN.fullmatch(
                value
            )

        )