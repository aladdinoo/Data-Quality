"""
CSV validation report.
"""

from __future__ import annotations

import csv
from pathlib import Path

from .report import ValidationReport


class CsvReport:
    """
    Export rule results to CSV.
    """

    def write(
        self,
        report: ValidationReport,
        output_file: str | Path,
    ) -> Path:

        output_file = Path(output_file)

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
                "rule",
                "version",
                "success",
                "errors",
                "warnings",
                "rows_processed",
                "rows_modified",
                "rows_flagged",
                "duration_seconds",
                "message",
            ])

            for result in report.pipeline_result.rule_results:

                writer.writerow([
                    result.rule,
                    result.version,
                    result.success,
                    result.errors,
                    result.warnings,
                    result.rows_processed,
                    result.rows_modified,
                    result.rows_flagged,
                    round(result.duration, 6),
                    result.message,
                ])

        return output_file