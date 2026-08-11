"""
Validation report manager.
"""

from __future__ import annotations

from pathlib import Path

from rules.executor import PipelineResult

from .report import ValidationReport
from .report_writer import ReportWriter


class ReportManager:
    """
    Creates and writes validation reports.
    """

    def __init__(
        self,
        output_dir: str | Path = "reports",
    ) -> None:

        self.output_dir = Path(output_dir)

        self.writer = ReportWriter()

    def generate(
        self,
        pipeline_result: PipelineResult,
    ) -> ValidationReport:

        report = ValidationReport(
            pipeline_result
        )

        self.writer.write_all(
            report,
            self.output_dir,
        )

        return report