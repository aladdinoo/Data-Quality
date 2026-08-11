"""
Phone validation utilities.
"""

from __future__ import annotations

import re


class PhoneValidator:
    """
    Validate international phone numbers.
    """

    PHONE_PATTERN = re.compile(
        r"^\+?[0-9\-\s()]{7,20}$"
    )

    def is_valid(
        self,
        value: str,
    ) -> bool:
        """
        Return True if the phone number is valid.
        """

        return bool(
            self.PHONE_PATTERN.fullmatch(
                value.strip()
            )
        )