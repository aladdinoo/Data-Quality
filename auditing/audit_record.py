"""
Audit Record.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class AuditRecord:
    """
    Represents one cleaning action.
    """

    rule: str

    row: int

    column: str

    old_value: str | None

    new_value: str | None

    timestamp: datetime

    review_required: bool = False

    user: str = "system"