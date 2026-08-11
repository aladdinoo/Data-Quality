"""
Report Generator.

Generate HTML and JSON reports for the Data Quality Platform.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any


class ReportGenerator:
    """
    Generate validation reports.
    """

    def __init__(self, output_directory: Path) -> None:
        self.output_directory = output_directory
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def generate(self, pipeline_result: Any) -> None:
        """
        Generate all reports.
        """

        self._write_json(pipeline_result)
        self._write_html(pipeline_result)

    def _write_json(self, pipeline_result: Any) -> None:
        """
        Save JSON report.
        """

        output = self.output_directory / "validation_report.json"

        report = {
            "successful_rules": pipeline_result.successful_rules,
            "failed_rules": pipeline_result.failed_rules,
            "rows_flagged": pipeline_result.total_rows_flagged,
            "duration": pipeline_result.total_duration,
            "rules": [],
        }

        for rule in pipeline_result.rule_results:

            report["rules"].append(
                {
                    "rule": rule.rule,
                    "success": rule.success,
                    "errors": rule.errors,
                    "warnings": rule.warnings,
                    "rows_flagged": rule.rows_flagged,
                    "review_required": rule.review_required,
                    "failures": rule.failures,
                }
            )

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def _write_html(self, pipeline_result: Any) -> None:
        """
        Save HTML report.
        """

        output = self.output_directory / "validation_report.html"

        rows = []

        for rule in pipeline_result.rule_results:

            color = "#28a745" if rule.success else "#dc3545"

            rows.append(
                f"""
                <tr>
                    <td>{rule.rule}</td>
                    <td style="color:{color};font-weight:bold;">
                        {"PASS" if rule.success else "FAIL"}
                    </td>
                    <td>{rule.errors}</td>
                    <td>{rule.warnings}</td>
                    <td>{rule.rows_flagged}</td>
                </tr>
                """
            )

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Validation Report</title>

<style>

body{{
font-family:Arial;
margin:40px;
background:#f8f9fa;
}}

table{{
width:100%;
border-collapse:collapse;
}}

th,td{{
border:1px solid #ccc;
padding:10px;
text-align:left;
}}

th{{
background:#343a40;
color:white;
}}

h1{{
color:#333;
}}

.summary{{
margin-bottom:30px;
}}

</style>

</head>

<body>

<h1>Data Quality Validation Report</h1>

<div class="summary">

<p><strong>Successful Rules:</strong> {pipeline_result.successful_rules}</p>

<p><strong>Failed Rules:</strong> {pipeline_result.failed_rules}</p>

<p><strong>Rows Flagged:</strong> {pipeline_result.total_rows_flagged}</p>

<p><strong>Total Duration:</strong> {pipeline_result.total_duration:.3f} sec</p>

</div>

<table>

<tr>

<th>Rule</th>

<th>Status</th>

<th>Errors</th>

<th>Warnings</th>

<th>Rows Flagged</th>

</tr>

{''.join(rows)}

</table>

</body>

</html>
"""

        output.write_text(
            html,
            encoding="utf-8",
        )