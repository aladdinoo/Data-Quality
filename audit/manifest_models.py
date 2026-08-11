"""
Evidence manifest models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SuccessManifest:
    step: str
    status: str
    generated_utc: str
    run_id: str
    database: str
    table: str
    view_target: str

    execution_scope: str
    source_row_count: int

    live_source_ddl_sha256_before: str
    live_source_ddl_sha256_after: str
    ddl_unchanged_during_run: bool

    canonical_template_sha256: str
    derived_view_sql_sha256: str

    name_action_status: str = (
        "PENDING_BUSINESS_DECISION"
    )

    production_changed: bool = False
    source_write_performed: bool = False
    raw_values_printed: bool = False

    reference_snapshot: dict[str, Any] = field(
        default_factory=dict
    )

    validation_items: list[str] = field(
        default_factory=list
    )

    flag_reconciliation: dict[str, Any] = field(
        default_factory=dict
    )

    shas: dict[str, str] = field(
        default_factory=dict
    )

    context: dict[str, Any] = field(
        default_factory=dict
    )

    files: dict[str, str] = field(
        default_factory=dict
    )


@dataclass(slots=True)
class FailureManifest:
    step: str
    status: str
    generated_utc: str
    run_id: str
    database: str
    table: str
    view_target: str

    production_changed: bool = False
    source_write_performed: bool = False
    raw_values_printed: bool = False

    ddl_authorized: bool = False
    failed_check: str = ""
    error_type: str = ""
    error_message: str = ""

    shas_captured: dict[str, str] = field(
        default_factory=dict
    )

    context_captured: dict[str, Any] = field(
        default_factory=dict
    )

    evidence_files: dict[str, str] = field(
        default_factory=dict
    )