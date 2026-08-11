"""
Validation result models.

This module provides validation-specific result objects.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field
from typing import Any

# ==================================================
# Validation Failure
# ==================================================


@dataclass(slots=True)
class ValidationFailure:
    """
    Represents a single validation failure.
    """

    row: int

    column: str

    value: Any

    message: str


# ==================================================
# Validation Result
# ==================================================


@dataclass(slots=True)
class ValidationResult:
    """
    Validation summary.
    """

    failures: list[ValidationFailure] = field(
        default_factory=list
    )

    warnings: list[str] = field(
        default_factory=list
    )

    checked_rows: int = 0

    checked_columns: int = 0

    duration: float = 0.0

    # --------------------------------------------------

    @property
    def success(self) -> bool:

        return len(self.failures) == 0

    # --------------------------------------------------

    def add_failure(
        self,
        *,
        row: int,
        column: str,
        value: Any,
        message: str,
    ) -> None:

        self.failures.append(

            ValidationFailure(

                row=row,

                column=column,

                value=value,

                message=message,

            )

        )

    # --------------------------------------------------

    def add_warning(
        self,
        message: str,
    ) -> None:

        self.warnings.append(message)