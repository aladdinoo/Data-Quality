"""
Audit Logger.
"""

from __future__ import annotations

from pathlib import Path
import csv

from .models import AuditRecord


class AuditLogger:
    """
    Store audit records.
    """

    def __init__(
        self,
        output_file: Path,
    ) -> None:

        self.output_file = output_file

        self.records: list[AuditRecord] = []

    def add(
        self,
        record: AuditRecord,
    ) -> None:

        self.records.append(record)

    def save(self) -> None:

        self.output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self.output_file.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    "timestamp",
                    "rule",
                    "row",
                    "column",
                    "old_value",
                    "new_value",
                    "action",
                    "automatic",
                    "review_required",
                ]
            )

            for record in self.records:

                writer.writerow(
                    [
                        record.timestamp.isoformat(),
                        record.rule,
                        record.row,
                        record.column,
                        record.old_value,
                        record.new_value,
                        record.action,
                        record.automatic,
                        record.review_required,
                    ]
                )