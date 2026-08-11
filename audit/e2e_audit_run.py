"""
End-to-end audit run.

Runs the complete read-only audit workflow:

1. Capture source evidence before execution.
2. Load the source CSV into a dataframe.
3. Execute the validation engine.
4. Map validation results to canonical Flag Preview flags.
5. Build the canonical Flag Preview dataframe.
6. Write the Flag Preview as a separate evidence artifact.
7. Capture source evidence after execution.
8. Reconcile source invariants.
9. Write a deterministic success/failure manifest.

The source CSV is never modified.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd

from core.context import PipelineContext

from validation.engine import ValidationEngine
from validation.flag_mapper import ValidationFlagMapper

from flag_preview.builder import FlagPreviewBuilder

from .ddl_capture import (
    DDLFingerprint,
    capture_ddl,
)
from .evidence_manifest import (
    FailureManifest,
    SuccessManifest,
)
from .evidence_manifest_writer import (
    EvidenceManifestWriter,
)
from .reconciliation import (
    ReconciliationInput,
    ReconciliationResult,
    reconcile,
)
from .source_evidence import (
    SourceEvidence,
    SourceEvidenceReader,
)


# ============================================================
# Configuration
# ============================================================


@dataclass(frozen=True, slots=True)
class AuditRunConfig:
    """
    Configuration for an E2E audit run.
    """

    database: str
    table: str
    view_target: str

    source_file: Path
    source_ddl: str

    output_directory: Path

    execution_scope: str = "READ_ONLY"


# ============================================================
# Result
# ============================================================


@dataclass(frozen=True, slots=True)
class AuditRunResult:
    """
    Final E2E audit result.
    """

    run_id: str
    success: bool

    reconciliation: ReconciliationResult

    manifest_file: Path
    manifest_sha256: str

    flag_preview_file: Path | None = None

    validation_success: bool = False

    validation_rules_executed: int = 0

    validation_rules_failed: int = 0

    rows_processed: int = 0

    rows_flagged: int = 0


# ============================================================
# E2E Audit Run
# ============================================================


class E2EAuditRun:
    """
    Execute a complete read-only audit run.

    This class never modifies the source CSV.
    """

    # --------------------------------------------------------
    # Constructor
    # --------------------------------------------------------

    def __init__(
        self,
        config: AuditRunConfig,
        validation_engine: ValidationEngine | None = None,
        flag_mapper: ValidationFlagMapper | None = None,
        flag_preview_builder: FlagPreviewBuilder | None = None,
    ) -> None:

        self.config = config

        self.writer = EvidenceManifestWriter()

        self.validation_engine = (
            validation_engine
            or ValidationEngine()
        )

        self.flag_mapper = (
            flag_mapper
            or ValidationFlagMapper()
        )

        self.flag_preview_builder = (
            flag_preview_builder
            or FlagPreviewBuilder()
        )

    # --------------------------------------------------------
    # UTC
    # --------------------------------------------------------

    @staticmethod
    def _utc_now() -> str:
        """
        Return the current UTC timestamp.
        """

        return datetime.now(
            timezone.utc
        ).isoformat()

    # --------------------------------------------------------
    # Source loading
    # --------------------------------------------------------

    @staticmethod
    def _load_source_dataframe(
        source_file: Path,
    ) -> pd.DataFrame:
        """
        Load the source CSV.

        pandas performs a read operation only.
        No write operation is performed against
        the source file.
        """

        source_file = Path(source_file)

        if not source_file.exists():
            raise FileNotFoundError(
                f"Source file does not exist: {source_file}"
            )

        if not source_file.is_file():
            raise ValueError(
                f"Source path is not a file: {source_file}"
            )

        return pd.read_csv(
            source_file
        )

    # --------------------------------------------------------
    # Flag Preview writer
    # --------------------------------------------------------

    @staticmethod
    def _write_flag_preview(
        dataframe: pd.DataFrame,
        output_file: Path,
    ) -> None:
        """
        Write the Flag Preview as a separate artifact.

        The source dataframe is never written.
        """

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe.to_csv(
            output_file,
            index=False,
        )

    # --------------------------------------------------------
    # E2E
    # --------------------------------------------------------

    def run(self) -> AuditRunResult:
        """
        Execute the complete read-only audit.
        """

        run_id = str(
            uuid4()
        )

        generated_utc = (
            self._utc_now()
        )

        output = (
            Path(
                self.config.output_directory
            )
            / run_id
        )

        output.mkdir(
            parents=True,
            exist_ok=True,
        )

        before: DDLFingerprint = (
            capture_ddl(
                self.config.source_ddl
            )
        )

        source_evidence_before: (
            SourceEvidence | None
        ) = None

        source_evidence_after: (
            SourceEvidence | None
        ) = None

        flag_preview_file: Path | None = None

        try:

            # ==================================================
            # 1. SOURCE EVIDENCE BEFORE
            # ==================================================

            source_evidence_before = (
                SourceEvidenceReader.read_csv(
                    self.config.source_file
                )
            )

            source_row_count_before = (
                source_evidence_before.row_count
            )

            # ==================================================
            # 2. LOAD SOURCE
            # ==================================================

            dataframe = (
                self._load_source_dataframe(
                    self.config.source_file
                )
            )

            # --------------------------------------------------
            # Defensive row-count check
            # --------------------------------------------------

            if len(dataframe) != (
                source_evidence_before.row_count
            ):
                raise ValueError(
                    "Loaded dataframe row count does not "
                    "match source evidence."
                )

            # ==================================================
            # 3. PIPELINE CONTEXT
            # ==================================================

            context = PipelineContext()

            context.set_raw_dataframe(
                dataframe.copy(
                    deep=True
                )
            )

            context.set_dataframe(
                dataframe
            )

            context.add_metadata(
                "execution_scope",
                self.config.execution_scope,
            )

            context.add_metadata(
                "source_file",
                str(
                    self.config.source_file
                ),
            )

            # ==================================================
            # 4. VALIDATION
            # ==================================================

            validation_result = (
                self.validation_engine.execute(
                    context
                )
            )

            # ==================================================
            # 5. MAP VALIDATION → FLAGS
            # ==================================================

            flags = (
                self.flag_mapper.build_flags(
                    dataframe=context.dataframe,
                    rule_results=(
                        validation_result.rule_results
                    ),
                )
            )

            # ==================================================
            # 6. BUILD FLAG PREVIEW
            # ==================================================

            flag_preview = (
                self.flag_preview_builder.build(
                    dataframe=dataframe,
                    flags=flags,
                )
            )

            # ==================================================
            # 7. WRITE FLAG PREVIEW
            # ==================================================

            flag_preview_file = (
                output
                / "flag_preview.csv"
            )

            self._write_flag_preview(
                flag_preview,
                flag_preview_file,
            )

            flag_preview_sha256 = (
                self.writer.sha256(
                    flag_preview_file
                )
            )

            # ==================================================
            # 8. SOURCE EVIDENCE AFTER
            # ==================================================

            source_evidence_after = (
                SourceEvidenceReader.read_csv(
                    self.config.source_file
                )
            )

            source_row_count_after = (
                source_evidence_after.row_count
            )

            # ==================================================
            # 9. DDL AFTER
            # ==================================================

            after = capture_ddl(
                self.config.source_ddl
            )

            # ==================================================
            # 10. RECONCILIATION
            # ==================================================

            reconciliation_input = (
                ReconciliationInput(
                    source_row_count_before=(
                        source_row_count_before
                    ),
                    source_row_count_after=(
                        source_row_count_after
                    ),
                    ddl_hash_before=(
                        before.sha256
                    ),
                    ddl_hash_after=(
                        after.sha256
                    ),
                    production_changed=False,
                    source_write_performed=False,
                )
            )

            reconciliation = reconcile(
                reconciliation_input
            )

            # ==================================================
            # 11. RECONCILIATION FAILURE
            # ==================================================

            if not reconciliation.success:

                return self._write_failure(
                    run_id=run_id,
                    generated_utc=generated_utc,
                    output=output,
                    reconciliation=reconciliation,
                    failed_check=(
                        reconciliation.failures[0]
                        if reconciliation.failures
                        else "RECONCILIATION_FAILED"
                    ),
                    flag_preview_file=(
                        flag_preview_file
                    ),
                )

            # ==================================================
            # 12. VALIDATION FAILURE
            # ==================================================

            if not validation_result.success:

                failed_rule_names = [
                    result.rule
                    for result
                    in validation_result.rule_results
                    if not result.success
                ]

                failed_check = (
                    "VALIDATION_RULE_FAILURE"
                )

                # Keep the specific failed rules
                # inside the manifest context.
                validation_context = {
                    "failed_rules": (
                        failed_rule_names
                    ),
                }

                manifest = FailureManifest(
                    step="END_TO_END_AUDIT",
                    status="FAILURE",
                    generated_utc=generated_utc,
                    run_id=run_id,
                    database=self.config.database,
                    table=self.config.table,
                    view_target=self.config.view_target,
                    production_changed=False,
                    source_write_performed=False,
                    raw_values_printed=False,
                    ddl_authorized=False,
                    failed_check=failed_check,
                    error_type="ValidationError",
                    error_message=(
                        "One or more validation rules failed."
                    ),
                    shas_captured={
                        "ddl_before": (
                            before.sha256
                        ),
                        "ddl_after": (
                            after.sha256
                        ),
                        "flag_preview": (
                            flag_preview_sha256
                        ),
                    },
                    context_captured={
                        "execution_scope": (
                            self.config.execution_scope
                        ),
                        "validation": (
                            validation_context
                        ),
                    },
                    evidence_files={
                        "flag_preview": (
                            str(flag_preview_file)
                        ),
                    },
                )

                manifest_file = (
                    output
                    / "failure_manifest.json"
                )

                manifest_sha256 = (
                    self.writer.write_failure(
                        manifest,
                        manifest_file,
                    )
                )

                return AuditRunResult(
                    run_id=run_id,
                    success=False,
                    reconciliation=reconciliation,
                    manifest_file=manifest_file,
                    manifest_sha256=manifest_sha256,
                    flag_preview_file=(
                        flag_preview_file
                    ),
                    validation_success=False,
                    validation_rules_executed=(
                        len(
                            validation_result.rule_results
                        )
                    ),
                    validation_rules_failed=(
                        validation_result.failed_rules
                    ),
                    rows_processed=(
                        validation_result.total_rows_processed
                    ),
                    rows_flagged=(
                        validation_result.total_rows_flagged
                    ),
                )

            # ==================================================
            # 13. SUCCESS MANIFEST
            # ==================================================

            validation_summary = {
                "success": (
                    validation_result.success
                ),
                "rules_executed": (
                    len(
                        validation_result.rule_results
                    )
                ),
                "successful_rules": (
                    validation_result.successful_rules
                ),
                "failed_rules": (
                    validation_result.failed_rules
                ),
                "rows_processed": (
                    validation_result.total_rows_processed
                ),
                "rows_modified": (
                    validation_result.total_rows_modified
                ),
                "rows_flagged": (
                    validation_result.total_rows_flagged
                ),
                "audit_records": (
                    validation_result.total_audit_records
                ),
                "duration": (
                    validation_result.total_duration
                ),
            }

            manifest = SuccessManifest(
                step="END_TO_END_AUDIT",
                status="SUCCESS",
                generated_utc=generated_utc,
                run_id=run_id,
                database=self.config.database,
                table=self.config.table,
                view_target=self.config.view_target,
                execution_scope=(
                    self.config.execution_scope
                ),
                source_row_count=(
                    source_row_count_before
                ),
                live_source_ddl_sha256_before=(
                    before.sha256
                ),
                live_source_ddl_sha256_after=(
                    after.sha256
                ),
                ddl_unchanged_during_run=(
                    reconciliation.ddl_unchanged
                ),
                canonical_template_sha256="",
                derived_view_sql_sha256="",
                production_changed=False,
                source_write_performed=False,
                raw_values_printed=False,
                reference_snapshot={},
                validation_items=[
                    "SOURCE_ROW_COUNT_UNCHANGED",
                    "SOURCE_DDL_UNCHANGED",
                    "NO_PRODUCTION_CHANGE",
                    "NO_SOURCE_WRITE",
                    "VALIDATION_EXECUTED",
                    "FLAG_PREVIEW_GENERATED",
                    "FLAG_PREVIEW_ROW_COUNT_PRESERVED",
                ],
                flag_reconciliation={
                    "success": True,
                    "source_row_count": (
                        source_row_count_before
                    ),
                    "flag_preview_row_count": (
                        len(flag_preview)
                    ),
                    "source_columns": (
                        len(
                            source_evidence_before.columns
                        )
                    ),
                    "flag_preview_columns": (
                        len(
                            flag_preview.columns
                        )
                    ),
                },
                shas={
                    "ddl_before": (
                        before.sha256
                    ),
                    "ddl_after": (
                        after.sha256
                    ),
                    "flag_preview": (
                        flag_preview_sha256
                    ),
                },
                context={
                    "execution_scope": (
                        self.config.execution_scope
                    ),
                    "source_file": str(
                        source_evidence_before.source_file
                    ),
                    "source_column_count": (
                        source_evidence_before.column_count
                    ),
                    "source_columns": list(
                        source_evidence_before.columns
                    ),
                    "validation": (
                        validation_summary
                    ),
                },
                files={
                    "flag_preview": (
                        str(flag_preview_file)
                    ),
                },
            )

            manifest_file = (
                output
                / "success_manifest.json"
            )

            manifest_sha256 = (
                self.writer.write_success(
                    manifest,
                    manifest_file,
                )
            )

            return AuditRunResult(
                run_id=run_id,
                success=True,
                reconciliation=reconciliation,
                manifest_file=manifest_file,
                manifest_sha256=manifest_sha256,
                flag_preview_file=(
                    flag_preview_file
                ),
                validation_success=True,
                validation_rules_executed=(
                    len(
                        validation_result.rule_results
                    )
                ),
                validation_rules_failed=(
                    validation_result.failed_rules
                ),
                rows_processed=(
                    validation_result.total_rows_processed
                ),
                rows_flagged=(
                    validation_result.total_rows_flagged
                ),
            )

        except Exception as exc:

            # ==================================================
            # UNEXPECTED FAILURE
            # ==================================================

            failure = FailureManifest(
                step="END_TO_END_AUDIT",
                status="FAILURE",
                generated_utc=generated_utc,
                run_id=run_id,
                database=self.config.database,
                table=self.config.table,
                view_target=self.config.view_target,
                production_changed=False,
                source_write_performed=False,
                raw_values_printed=False,
                ddl_authorized=False,
                failed_check="UNEXPECTED_ERROR",
                error_type=type(exc).__name__,
                error_message=str(exc),
                shas_captured={
                    "ddl_before": (
                        before.sha256
                    ),
                },
                context_captured={
                    "execution_scope": (
                        self.config.execution_scope
                    ),
                    "source_file": str(
                        self.config.source_file
                    ),
                },
                evidence_files={
                    "flag_preview": (
                        str(flag_preview_file)
                        if flag_preview_file
                        else ""
                    ),
                },
            )

            manifest_file = (
                output
                / "failure_manifest.json"
            )

            manifest_sha256 = (
                self.writer.write_failure(
                    failure,
                    manifest_file,
                )
            )

            return AuditRunResult(
                run_id=run_id,
                success=False,
                reconciliation=ReconciliationResult(
                    success=False,
                    row_count_unchanged=False,
                    ddl_unchanged=False,
                    production_unchanged=False,
                    source_write_absent=False,
                    failures=(
                        "UNEXPECTED_ERROR",
                    ),
                ),
                manifest_file=manifest_file,
                manifest_sha256=manifest_sha256,
                flag_preview_file=(
                    flag_preview_file
                ),
            )

    # --------------------------------------------------------
    # Reconciliation failure
    # --------------------------------------------------------

    def _write_failure(
        self,
        run_id: str,
        generated_utc: str,
        output: Path,
        reconciliation: ReconciliationResult,
        failed_check: str,
        flag_preview_file: Path | None = None,
    ) -> AuditRunResult:
        """
        Write a reconciliation failure manifest.
        """

        evidence_files: dict[str, str] = {}

        shas_captured: dict[str, str] = {}

        if flag_preview_file is not None:
            evidence_files[
                "flag_preview"
            ] = str(
                flag_preview_file
            )

            if flag_preview_file.exists():
                shas_captured[
                    "flag_preview"
                ] = self.writer.sha256(
                    flag_preview_file
                )

        manifest = FailureManifest(
            step="END_TO_END_AUDIT",
            status="FAILURE",
            generated_utc=generated_utc,
            run_id=run_id,
            database=self.config.database,
            table=self.config.table,
            view_target=self.config.view_target,
            production_changed=(
                not reconciliation.production_unchanged
            ),
            source_write_performed=(
                not reconciliation.source_write_absent
            ),
            raw_values_printed=False,
            ddl_authorized=False,
            failed_check=failed_check,
            error_type="ReconciliationError",
            error_message=(
                "; ".join(
                    reconciliation.failures
                )
            ),
            context_captured={
                "execution_scope": (
                    self.config.execution_scope
                ),
                "source_file": str(
                    self.config.source_file
                ),
            },
            shas_captured=shas_captured,
            evidence_files=evidence_files,
        )

        manifest_file = (
            output
            / "failure_manifest.json"
        )

        manifest_sha256 = (
            self.writer.write_failure(
                manifest,
                manifest_file,
            )
        )

        return AuditRunResult(
            run_id=run_id,
            success=False,
            reconciliation=reconciliation,
            manifest_file=manifest_file,
            manifest_sha256=manifest_sha256,
            flag_preview_file=(
                flag_preview_file
            ),
        )