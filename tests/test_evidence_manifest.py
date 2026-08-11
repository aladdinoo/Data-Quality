from __future__ import annotations

import hashlib
import json

import pytest

from evidence.manifest import (
    FailureManifest,
    SuccessManifest,
)
from evidence.writer import EvidenceWriter


def build_success_manifest() -> SuccessManifest:
    return SuccessManifest(
        step="flag_preview",
        status="SUCCESS",
        generated_utc="2026-08-10T10:00:00Z",
        run_id="20260810T100000Z",
        database="sandbox",
        table="consumer",
        view_target="sandbox.flag_preview_20260810T100000Z",
        execution_scope="sandbox_only",
        source_row_count=100,
        live_source_ddl_sha256_before="abc123",
        live_source_ddl_sha256_after="abc123",
        ddl_unchanged_during_run=True,
        canonical_template_sha256="rule_hash",
        derived_view_sql_sha256="sql_hash",
        validation_items=[
            "source_ddl_unchanged",
            "flag_reconciliation",
        ],
        flag_reconciliation={
            "email_blank": {
                "stage2_expected": 10,
                "observed": 10,
            }
        },
        shas={
            "source_ddl": "abc123",
        },
        context={
            "pilot_bounds": "sandbox_only",
        },
        files={
            "flag_preview.sql": "sql_hash",
        },
    )


def build_failure_manifest() -> FailureManifest:
    return FailureManifest(
        step="flag_preview",
        status="FAILURE",
        generated_utc="2026-08-10T10:00:00Z",
        run_id="20260810T100001Z",
        database="sandbox",
        table="consumer",
        view_target="sandbox.flag_preview_20260810T100001Z",
        ddl_authorized=False,
        failed_check="flag_reconciliation",
        error_type="ValidationError",
        error_message="Observed count does not match baseline.",
        shas_captured={
            "source_ddl": "abc123",
        },
        context_captured={
            "pilot_bounds": "sandbox_only",
        },
        evidence_files={
            "partial_output.sql": "hash123",
        },
    )


def test_success_manifest_is_written(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    manifest_path = tmp_path / (
        "success_manifest_20260810T100000Z.json"
    )

    assert manifest_path.exists()
    assert result["status"] == "SUCCESS"


def test_success_manifest_has_required_identity(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    assert result["step"] == "flag_preview"
    assert result["run_id"] == "20260810T100000Z"
    assert result["database"] == "sandbox"
    assert result["table"] == "consumer"
    assert result["view_target"].endswith(
        "20260810T100000Z"
    )


def test_success_manifest_safety_invariants(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    assert result["production_changed"] is False
    assert result["source_write_performed"] is False
    assert result["raw_values_printed"] is False


def test_success_manifest_contains_success_fields(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    assert result["execution_scope"] == "sandbox_only"
    assert result["source_row_count"] == 100
    assert "reference_snapshot" in result
    assert "validation_items" in result
    assert "flag_reconciliation" in result
    assert "shas" in result
    assert "context" in result
    assert "files" in result


def test_success_manifest_hash_is_not_inside_json(
    tmp_path,
):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    manifest_path = tmp_path / (
        "success_manifest_20260810T100000Z.json"
    )

    payload = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    assert "success_manifest_sha256" not in payload
    assert "success_manifest_sha256" in result


def test_success_manifest_hash_matches_file_bytes(
    tmp_path,
):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    manifest_path = tmp_path / (
        "success_manifest_20260810T100000Z.json"
    )

    expected = hashlib.sha256(
        manifest_path.read_bytes()
    ).hexdigest()

    assert result["success_manifest_sha256"] == expected


def test_success_manifest_hash_is_deterministic(
    tmp_path,
):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_success(
        build_success_manifest()
    )

    manifest_path = tmp_path / (
        "success_manifest_20260810T100000Z.json"
    )

    first_hash = hashlib.sha256(
        manifest_path.read_bytes()
    ).hexdigest()

    second_hash = hashlib.sha256(
        manifest_path.read_bytes()
    ).hexdigest()

    assert first_hash == second_hash
    assert result["success_manifest_sha256"] == first_hash


def test_failure_manifest_is_written(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_failure(
        build_failure_manifest()
    )

    manifest_path = tmp_path / (
        "failure_manifest_20260810T100001Z.json"
    )

    assert manifest_path.exists()
    assert result["status"] == "FAILURE"


def test_failure_manifest_has_failure_fields(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_failure(
        build_failure_manifest()
    )

    assert result["failed_check"] == (
        "flag_reconciliation"
    )

    assert result["error_type"] == (
        "ValidationError"
    )

    assert "shas_captured" in result
    assert "context_captured" in result
    assert "evidence_files" in result


def test_failure_manifest_does_not_use_success_schema(
    tmp_path,
):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_failure(
        build_failure_manifest()
    )

    assert "execution_scope" not in result
    assert "source_row_count" not in result
    assert "reference_snapshot" not in result
    assert "validation_items" not in result
    assert "flag_reconciliation" not in result


def test_failure_manifest_safety_invariants(tmp_path):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_failure(
        build_failure_manifest()
    )

    assert result["production_changed"] is False
    assert result["source_write_performed"] is False
    assert result["raw_values_printed"] is False


def test_failure_manifest_hash_is_not_inside_json(
    tmp_path,
):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_failure(
        build_failure_manifest()
    )

    manifest_path = tmp_path / (
        "failure_manifest_20260810T100001Z.json"
    )

    payload = json.loads(
        manifest_path.read_text(
            encoding="utf-8"
        )
    )

    assert "failure_manifest_sha256" not in payload
    assert "failure_manifest_sha256" in result


def test_failure_manifest_hash_matches_file_bytes(
    tmp_path,
):
    writer = EvidenceWriter(tmp_path)

    result = writer.write_failure(
        build_failure_manifest()
    )

    manifest_path = tmp_path / (
        "failure_manifest_20260810T100001Z.json"
    )

    expected = hashlib.sha256(
        manifest_path.read_bytes()
    ).hexdigest()

    assert result["failure_manifest_sha256"] == expected


def test_success_rejects_wrong_status(tmp_path):
    writer = EvidenceWriter(tmp_path)

    manifest = build_success_manifest()
    manifest.status = "FAILURE"

    with pytest.raises(ValueError):
        writer.write_success(manifest)


def test_failure_rejects_wrong_status(tmp_path):
    writer = EvidenceWriter(tmp_path)

    manifest = build_failure_manifest()
    manifest.status = "SUCCESS"

    with pytest.raises(ValueError):
        writer.write_failure(manifest)