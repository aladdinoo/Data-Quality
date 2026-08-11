"""
Audit Logger.
"""

from __future__ import annotations

from datetime import datetime

from .audit_record import AuditRecord


class AuditLogger:
    """
    Collect audit records.
    """

    def __init__(self) -> None:

        self.records: list[AuditRecord] = []

    def log(
        self,
        rule: str,
        row: int,
        column: str,
        old_value: str,
        new_value: str,
        automatic: bool = True,
        action: str = "UPDATE",
    ) -> None:

        self.records.append(

            AuditRecord(

                timestamp=datetime.utcnow(),

                rule=rule,

                action=action,

                row=row,

                column=column,

                old_value=str(old_value),

                new_value=str(new_value),

                automatic=automatic,

            )

        )

    def __len__(self) -> int:

        return len(self.records)