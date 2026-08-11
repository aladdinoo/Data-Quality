from pathlib import Path
import json

from audit.e2e_audit_run import (
    AuditRunConfig,
    E2EAuditRun,
)


ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILE = (
    ROOT
    / "sample_data"
    / "customers.csv"
)

OUTPUT_DIRECTORY = (
    ROOT
    / "audit_output"
)


def test_e2e_audit_writes_real_artifact():
    config = AuditRunConfig(
        database="local_csv",
        table="customers",
        view_target="customers_flag_preview",
        source_file=SOURCE_FILE,
        source_ddl=(
            "CREATE TABLE customers "
            "(id INT, name TEXT, email TEXT, "
            "phone TEXT, website TEXT, "
            "zip TEXT, date TEXT)"
        ),
        output_directory=OUTPUT_DIRECTORY,
        execution_scope="READ_ONLY",
    )

    result = E2EAuditRun(config).run()

    assert result.success is True
    assert result.reconciliation.success is True

    assert result.manifest_file.exists()

    assert (
        result.manifest_file.name
        == "success_manifest.json"
    )

    assert result.manifest_sha256

    manifest = json.loads(
        result.manifest_file.read_text(
            encoding="utf-8"
        )
    )

    assert manifest["status"] == "SUCCESS"

    assert manifest["step"] == "END_TO_END_AUDIT"

    assert manifest["database"] == "local_csv"

    assert manifest["table"] == "customers"

    assert manifest["execution_scope"] == "READ_ONLY"

    assert manifest["source_row_count"] == 10000

    assert (
        manifest["live_source_ddl_sha256_before"]
        == manifest["live_source_ddl_sha256_after"]
    )

    assert (
        manifest["ddl_unchanged_during_run"]
        is True
    )

    assert (
        manifest["production_changed"]
        is False
    )

    assert (
        manifest["source_write_performed"]
        is False
    )

    assert (
        manifest["raw_values_printed"]
        is False
    )

    assert (
        "SOURCE_ROW_COUNT_UNCHANGED"
        in manifest["validation_items"]
    )

    assert (
        "SOURCE_DDL_UNCHANGED"
        in manifest["validation_items"]
    )

    assert (
        "NO_PRODUCTION_CHANGE"
        in manifest["validation_items"]
    )

    assert (
        "NO_SOURCE_WRITE"
        in manifest["validation_items"]
    )