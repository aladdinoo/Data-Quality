"""
Website validation utilities.
"""

from __future__ import annotations

from urllib.parse import urlparse


class WebsiteValidator:
    """
    Validate website URLs.
    """

    def is_valid(
        self,
        value: str,
    ) -> bool:
        """
        Return True if the URL is valid.
        """

        value = value.strip()

        if not value:
            return False

        parsed = urlparse(value)

        return bool(
            parsed.scheme
            and parsed.netloc
        )