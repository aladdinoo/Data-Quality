"""
End-to-end audit evidence coordinator.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from audit.ddl_capture import DDLCapture
from audit.evidence_manifest import EvidenceManifestWriter
from audit.manifest_models import (
    SuccessManifest,
    FailureManifest,
)
from audit.reconciliation import EvidenceReconciler


class AuditEvidenceRun:
    """Build and persist evidence for one pipeline run."""

    def __init__(
        self,
        output_directory: Path,
    ) -> None:
        self.output_directory = output_directory

        self.writer = EvidenceManifestWriter()
        self.reconciler = EvidenceReconciler()

        self.run_id = str(uuid4())

    @staticmethod
    def generated_utc() -> str:
        return datetime.now(
            timezone.utc
        ).isoformat()

    def write_success(
        self,
        *,
        database: str,
        table: str,
        view_target: str,
        execution_scope: str,
        source_row_count: int,
        evidence_row_count: int,
        ddl_before: str,
        ddl_after: str,
        canonical_template_sha256: str,
        derived_view_sql_sha256: str,
        files: dict[str, str],
    ) -> Path:

        reconciliation = (
            self.reconciler.reconcile(
                source_row_count=source_row_count,
                evidence_row_count=evidence_row_count,
                source_ddl_before=ddl_before,
                source_ddl_after=ddl_after,
                production_changed=False,
                source_write_performed=False,
            )
        )

        if not reconciliation.success:
            raise RuntimeError(
                "Evidence reconciliation failed: "
                + ", ".join(
                    reconciliation.failed_checks
                )
            )

        manifest = SuccessManifest(
            step="end_to_end_audit",
            status="SUCCESS",
            generated_utc=self.generated_utc(),
            run_id=self.run_id,
            database=database,
            table=table,
            view_target=view_target,
            execution_scope=execution_scope,
            source_row_count=source_row_count,
            live_source_ddl_sha256_before=(
                DDLCapture.sha256(ddl_before)
            ),
            live_source_ddl_sha256_after=(
                DDLCapture.sha256(ddl_after)
            ),
            ddl_unchanged_during_run=True,
            canonical_template_sha256=(
                canonical_template_sha256
            ),
            derived_view_sql_sha256=(
                derived_view_sql_sha256
            ),
            production_changed=False,
            source_write_performed=False,
            raw_values_printed=False,
            flag_reconciliation={
                "success": True,
                "checks": reconciliation.checks,
                "details": reconciliation.details,
            },
            files=files,
        )

        output_file = (
            self.output_directory
            / "success_manifest.json"
        )

        self.writer.write_success(
            manifest,
            output_file,
        )

        return output_file

    def write_failure(
        self,
        *,
        database: str,
        table: str,
        view_target: str,
        failed_check: str,
        error: Exception,
        production_changed: bool = False,
        source_write_performed: bool = False,
    ) -> Path:

        manifest = FailureManifest(
            step="end_to_end_audit",
            status="FAILURE",
            generated_utc=self.generated_utc(),
            run_id=self.run_id,
            database=database,
            table=table,
            view_target=view_target,
            production_changed=production_changed,
            source_write_performed=(
                source_write_performed
            ),
            raw_values_printed=False,
            failed_check=failed_check,
            error_type=type(error).__name__,
            error_message=str(error),
        )

        output_file = (
            self.output_directory
            / "failure_manifest.json"
        )

        self.writer.write_failure(
            manifest,
            output_file,
        )

        return output_file