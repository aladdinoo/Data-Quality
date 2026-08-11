"""
JSON validation report.
"""

from __future__ import annotations

import json

from .report import ValidationReport


class JsonReport:
    """
    Serialize ValidationReport to JSON.
    """

    def render(
        self,
        report: ValidationReport,
        *,
        indent: int = 4,
    ) -> str:

        summary = report.summary

        data = {

            "generated_at": report.created_at.isoformat(),

            "dataset": report.dataset_name,

            "rows": report.total_rows,

            "columns": report.total_columns,

            "summary": {

                "rules": summary.total_rules,

                "passed": summary.successful_rules,

                "failed": summary.failed_rules,

                "rows_processed": summary.rows_processed,

                "rows_modified": summary.rows_modified,

                "rows_flagged": summary.rows_flagged,

                "errors": summary.total_errors,

                "warnings": summary.total_warnings,

                "quality_score": summary.quality_score,

                "duration": summary.total_duration,

            },

            "rules": [],

        }

        for result in report.pipeline_result.rule_results:

            data["rules"].append({

                "rule": result.rule,

                "version": result.version,

                "success": result.success,

                "errors": result.errors,

                "warnings": result.warnings,

                "rows_processed": result.rows_processed,

                "rows_modified": result.rows_modified,

                "rows_flagged": result.rows_flagged,

                "duration": result.duration,

                "message": result.message,

                "failures": result.failures,

            })

        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=False,
        )