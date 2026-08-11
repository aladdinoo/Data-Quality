"""
Cleaning Result.

Represents the result of executing one cleaning rule.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CleaningResult:
    """
    Result produced by a single cleaning rule.
    """

    cleaner: str
    success: bool

    rows_processed: int = 0
    rows_modified: int = 0
    rows_flagged: int = 0

    duration: float = 0.0

    message: str = ""

    modifications: list[dict[str, Any]] = field(
        default_factory=list
    )

    flags: list[dict[str, Any]] = field(
        default_factory=list
    )

    errors: list[dict[str, Any]] = field(
        default_factory=list
    )