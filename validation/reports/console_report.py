"""
Console validation report.
"""

from __future__ import annotations

from .report import ValidationReport


class ConsoleReport:
    """
    Pretty console renderer.
    """

    def render(
        self,
        report: ValidationReport,
    ) -> str:

        summary = report.summary

        lines: list[str] = []

        lines.append("=" * 60)
        lines.append("VALIDATION REPORT")
        lines.append("=" * 60)

        if report.dataset_name:
            lines.append(
                f"Dataset         : {report.dataset_name}"
            )

        lines.append(
            f"Generated       : {report.created_at}"
        )

        lines.append("")

        lines.append(
            f"Rules Executed  : {summary.total_rules}"
        )

        lines.append(
            f"Rules Passed    : {summary.successful_rules}"
        )

        lines.append(
            f"Rules Failed    : {summary.failed_rules}"
        )

        lines.append("")

        lines.append(
            f"Rows Processed  : {summary.rows_processed}"
        )

        lines.append(
            f"Rows Modified   : {summary.rows_modified}"
        )

        lines.append(
            f"Rows Flagged    : {summary.rows_flagged}"
        )

        lines.append("")

        lines.append(
            f"Errors          : {summary.total_errors}"
        )

        lines.append(
            f"Warnings        : {summary.total_warnings}"
        )

        lines.append(
            f"Quality Score   : {summary.quality_score:.2f}%"
        )

        lines.append(
            f"Duration        : {summary.total_duration:.3f}s"
        )

        lines.append("")
        lines.append("-" * 60)

        for result in report.pipeline_result.rule_results:

            status = (
                "PASS"
                if result.success
                else "FAIL"
            )

            lines.append(
                f"{status:<5} {result.rule}"
            )

            if result.errors:

                lines.append(
                    f"   Errors   : {result.errors}"
                )

            if result.warnings:

                lines.append(
                    f"   Warnings : {result.warnings}"
                )

            if result.rows_flagged:

                lines.append(
                    f"   Flagged  : {result.rows_flagged}"
                )

        lines.append("=" * 60)

        return "\n".join(lines)