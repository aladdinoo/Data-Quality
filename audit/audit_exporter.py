"""
Audit Exporter.
"""

from __future__ import annotations

import csv
from pathlib import Path

from audit.audit_record import AuditRecord


class AuditExporter:
    """
    Export audit records.
    """

    def export_csv(
        self,
        records: list[AuditRecord],
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

            writer.writerow([
                "timestamp",
                "rule",
                "action",
                "row",
                "column",
                "old_value",
                "new_value",
                "automatic",
            ])

            for record in records:

                writer.writerow([
                    record.timestamp,
                    record.rule,
                    record.action,
                    record.row,
                    record.column,
                    record.old_value,
                    record.new_value,
                    record.automatic,
                ])