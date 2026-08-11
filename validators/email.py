"""
Email validation utilities.
"""

from __future__ import annotations

import re


class EmailValidator:
    """
    Validate email syntax.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def is_valid(
        self,
        value: str,
    ) -> bool:
        """
        Return True if the email is valid.
        """

        return bool(
            self.EMAIL_PATTERN.fullmatch(
                value.strip()
            )
        )