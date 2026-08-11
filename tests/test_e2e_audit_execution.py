import pandas as pd
from pathlib import Path

from audit.e2e_audit_run import (
    AuditRunConfig,
    E2EAuditRun,
)


SOURCE_FILE = (
    Path(__file__).resolve().parents[1]
    / "sample_data"
    / "customers.csv"
)


def test_e2e_audit_run_real_source(tmp_path):
    config = AuditRunConfig(
        database="local_csv",
        table="customers",
        view_target="customers_flag_preview",
        source_file=SOURCE_FILE,
        source_ddl=(
            "CREATE TABLE customers "
            "(id INT, name TEXT, email TEXT, "
            "phone TEXT, website TEXT, zip TEXT, date TEXT)"
        ),
        output_directory=tmp_path,
        execution_scope="READ_ONLY",
    )

    result = E2EAuditRun(config).run()

    # ---------------------------------------------------------
    # E2E run must succeed
    # ---------------------------------------------------------

    assert result.success is True

    # ---------------------------------------------------------
    # Source reconciliation
    # ---------------------------------------------------------

    assert result.reconciliation.success is True

    assert result.reconciliation.failures == ()

    assert (
        result.reconciliation.row_count_unchanged
        is True
    )

    assert (
        result.reconciliation.ddl_unchanged
        is True
    )

    assert (
        result.reconciliation.production_unchanged
        is True
    )

    assert (
        result.reconciliation.source_write_absent
        is True
    )

    # ---------------------------------------------------------
    # Success manifest
    # ---------------------------------------------------------

    assert result.manifest_file.exists()

    assert (
        result.manifest_file.name
        == "success_manifest.json"
    )

    assert result.manifest_sha256

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    assert result.validation_success is True

    assert (
        result.validation_rules_executed
        == 10
    )

    assert (
        result.validation_rules_failed
        == 0
    )

    # ---------------------------------------------------------
    # Flag Preview
    # ---------------------------------------------------------

    assert result.flag_preview_file is not None

    assert result.flag_preview_file.exists()

    preview = pd.read_csv(
        result.flag_preview_file
    )

    # The source contains exactly 10,000 rows.
    # rows_processed must NOT be used here because
    # it represents the aggregate processing count
    # across validation rules.
    assert len(preview) == 10_000