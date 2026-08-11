"""
Validation report writer.
"""

from __future__ import annotations

from pathlib import Path

from .csv_report import CsvReport
from .html_report import HtmlReport
from .json_report import JsonReport
from .report import ValidationReport
from .text_report import TextReport


class ReportWriter:
    """
    Writes validation reports
    in multiple formats.
    """

    def __init__(self) -> None:

        self._text = TextReport()

        self._json = JsonReport()

        self._csv = CsvReport()

        self._html = HtmlReport()

    def write_all(
        self,
        report: ValidationReport,
        output_dir: str | Path,
    ) -> None:

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._text.write(
            report,
            output_dir / "validation_report.txt",
        )

        self._json.write(
            report,
            output_dir / "validation_report.json",
        )

        self._csv.write(
            report,
            output_dir / "validation_report.csv",
        )

        self._html.write(
            report,
            output_dir / "validation_report.html",
        )