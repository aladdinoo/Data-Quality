"""
Audit Logger.
"""

from __future__ import annotations

from pathlib import Path
import csv

from .audit_record import AuditRecord


class AuditLogger:
    """
    Collect and persist audit records.
    """

    def __init__(self) -> None:

        self.records: list[AuditRecord] = []

    def add(
        self,
        record: AuditRecord,
    ) -> None:

        self.records.append(record)

    def extend(
        self,
        records: list[AuditRecord],
    ) -> None:

        self.records.extend(records)

    def clear(self) -> None:

        self.records.clear()

    @property
    def total_records(self) -> int:

        return len(self.records)

    def save_csv(
        self,
        output_file: Path,
    ) -> None:

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_file.open(
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
                    "review_required",
                    "user",
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
                        record.review_required,
                        record.user,
                    ]
                )