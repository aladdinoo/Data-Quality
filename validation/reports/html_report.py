"""
HTML validation report.
"""

from __future__ import annotations

from pathlib import Path

from .report import ValidationReport


class HtmlReport:
    """
    Export validation report as HTML.
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

        summary = report.summary

        rows = []

        for result in report.pipeline_result.rule_results:

            color = (
                "#d4edda"
                if result.success
                else "#f8d7da"
            )

            rows.append(
                f"""
<tr style="background:{color}">
<td>{result.rule}</td>
<td>{result.version}</td>
<td>{result.success}</td>
<td>{result.errors}</td>
<td>{result.warnings}</td>
<td>{result.rows_flagged}</td>
<td>{result.duration:.4f}</td>
</tr>
"""
            )

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Validation Report</title>

<style>

body {{
    font-family: Arial;
    margin:40px;
}}

table {{
    border-collapse:collapse;
    width:100%;
}}

th,td {{
    border:1px solid #cccccc;
    padding:8px;
    text-align:left;
}}

th {{
    background:#2d6cdf;
    color:white;
}}

</style>

</head>

<body>

<h1>Validation Report</h1>

<h2>Summary</h2>

<ul>

<li>Total Rules : {summary.total_rules}</li>

<li>Passed : {summary.successful_rules}</li>

<li>Failed : {summary.failed_rules}</li>

<li>Errors : {summary.total_errors}</li>

<li>Warnings : {summary.total_warnings}</li>

<li>Rows Flagged : {summary.rows_flagged}</li>

<li>Quality Score : {summary.quality_score:.2f}%</li>

<li>Duration : {summary.total_duration:.4f} sec</li>

</ul>

<h2>Rule Results</h2>

<table>

<tr>

<th>Rule</th>

<th>Version</th>

<th>Success</th>

<th>Errors</th>

<th>Warnings</th>

<th>Flagged</th>

<th>Duration</th>

</tr>

{''.join(rows)}

</table>

</body>
</html>
"""

        output_file.write_text(
            html,
            encoding="utf-8",
        )

        return output_file