"""
Cleaning Report.
"""

from __future__ import annotations

from pathlib import Path

from cleaning.result import CleaningResult


class CleaningReport:

    def generate(

        self,
        results: list[CleaningResult],
        output_file: Path,

    ) -> None:

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as report:

            report.write(
                "Data Cleaning Report\n"
            )

            report.write(
                "=" * 60 + "\n\n"
            )

            total_processed = 0
            total_modified = 0
            total_flagged = 0

            for result in results:

                total_processed += result.rows_processed
                total_modified += result.rows_modified
                total_flagged += result.rows_flagged

            report.write(
                f"Rows Processed : {total_processed}\n"
            )

            report.write(
                f"Rows Modified  : {total_modified}\n"
            )

            report.write(
                f"Rows Flagged   : {total_flagged}\n\n"
            )

            report.write(
                "Cleaner\tModified\tFlagged\n"
            )

            for result in results:

                report.write(

                    f"{result.cleaner}\t"

                    f"{result.rows_modified}\t"

                    f"{result.rows_flagged}\n"

                )