"""
Audit Report.
"""

from __future__ import annotations

from pathlib import Path

from .audit_logger import AuditLogger


class AuditReport:
    """
    Generate a human-readable audit report.
    """

    def generate(
        self,
        logger: AuditLogger,
        output_file: Path,
    ) -> None:

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        automatic = sum(
            not record.review_required
            for record in logger.records
        )

        review = sum(
            record.review_required
            for record in logger.records
        )

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write(
                "Audit Report\n"
            )

            file.write(
                "=" * 60 + "\n\n"
            )

            file.write(
                f"Total Audit Records : {logger.total_records}\n"
            )

            file.write(
                f"Automatic Changes   : {automatic}\n"
            )

            file.write(
                f"Review Required     : {review}\n\n"
            )

            file.write(
                "Rule\tRow\tColumn\tReview\n"
            )

            for record in logger.records:

                file.write(

                    f"{record.rule}\t"
                    f"{record.row}\t"
                    f"{record.column}\t"
                    f"{record.review_required}\n"

                )