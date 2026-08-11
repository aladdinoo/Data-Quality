"""
Name validation utilities.
"""

from __future__ import annotations

import re


class NameValidator:
    """
    Validate person or company names.
    """

    INVALID_VALUES = {

        "",

        "null",

        "none",

        "unknown",

        "n/a",

        "na",

        "-",

    }

    NAME_PATTERN = re.compile(

        r"^[A-Za-zÀ-ÿ\u0600-\u06FF\s'.-]{2,100}$"

    )

    def is_valid(
        self,
        value: str,
    ) -> bool:
        """
        Return True if the name is valid.
        """

        text = value.strip()

        if not text:

            return False

        if text.lower() in self.INVALID_VALUES:

            return False

        return bool(

            self.NAME_PATTERN.fullmatch(
                text
            )

        )