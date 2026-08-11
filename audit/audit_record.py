"""
Audit Record.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class AuditRecord:
    """
    Single audit event.
    """

    timestamp: datetime

    rule: str

    action: str

    row: int

    column: str

    old_value: str

    new_value: str

    automatic: bool

    user: str = "system"