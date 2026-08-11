import json

from audit.evidence_manifest import (
    EvidenceManifestWriter,
)
from audit.manifest_models import (
    SuccessManifest,
    FailureManifest,
)


def test_success_manifest_is_written(tmp_path):

    manifest = SuccessManifest(
        step="test",
        status="SUCCESS",
        generated_utc="2026-08-10T10:00:00+00:00",
        run_id="run-001",
        database="test_db",
        table="consumer",
        view_target="consumer_clean",
        execution_scope="sandbox",
        source_row_count=10,
        live_source_ddl_sha256_before="abc",
        live_source_ddl_sha256_after="abc",
        ddl_unchanged_during_run=True,
        canonical_template_sha256="template",
        derived_view_sql_sha256="view",
    )

    output = tmp_path / "success_manifest.json"

    digest = EvidenceManifestWriter().write_success(
        manifest,
        output,
    )

    assert output.exists()
    assert len(digest) == 64


def test_failure_manifest_is_written(tmp_path):

    manifest = FailureManifest(
        step="test",
        status="FAILURE",
        generated_utc="2026-08-10T10:00:00+00:00",
        run_id="run-001",
        database="test_db",
        table="consumer",
        view_target="consumer_clean",
        failed_check="ddl_unchanged",
        error_type="RuntimeError",
        error_message="DDL changed",
    )

    output = tmp_path / "failure_manifest.json"

    digest = EvidenceManifestWriter().write_failure(
        manifest,
        output,
    )

    assert output.exists()
    assert len(digest) == 64


def test_manifest_hash_is_not_inside_json(tmp_path):

    manifest = SuccessManifest(
        step="test",
        status="SUCCESS",
        generated_utc="2026-08-10T10:00:00+00:00",
        run_id="run-001",
        database="test_db",
        table="consumer",
        view_target="consumer_clean",
        execution_scope="sandbox",
        source_row_count=10,
        live_source_ddl_sha256_before="abc",
        live_source_ddl_sha256_after="abc",
        ddl_unchanged_during_run=True,
        canonical_template_sha256="template",
        derived_view_sql_sha256="view",
    )

    output = tmp_path / "manifest.json"

    EvidenceManifestWriter().write_success(
        manifest,
        output,
    )

    payload = json.loads(
        output.read_text(
            encoding="utf-8"
        )
    )

    assert "manifest_sha256" not in payload