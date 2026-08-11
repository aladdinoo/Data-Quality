from audit.reconciliation import EvidenceReconciler


def test_reconciliation_success():
    result = EvidenceReconciler().reconcile(
        source_row_count=100,
        evidence_row_count=100,
        source_ddl_before="CREATE TABLE x",
        source_ddl_after="CREATE TABLE x",
        production_changed=False,
        source_write_performed=False,
    )

    assert result.success is True
    assert result.failed_checks == []


def test_reconciliation_rejects_row_loss():
    result = EvidenceReconciler().reconcile(
        source_row_count=100,
        evidence_row_count=99,
        source_ddl_before="CREATE TABLE x",
        source_ddl_after="CREATE TABLE x",
        production_changed=False,
        source_write_performed=False,
    )

    assert result.success is False
    assert "row_count_preserved" in (
        result.failed_checks
    )


def test_reconciliation_rejects_ddl_change():
    result = EvidenceReconciler().reconcile(
        source_row_count=100,
        evidence_row_count=100,
        source_ddl_before="CREATE TABLE x",
        source_ddl_after="CREATE TABLE y",
        production_changed=False,
        source_write_performed=False,
    )

    assert result.success is False
    assert "ddl_unchanged" in (
        result.failed_checks
    )


def test_reconciliation_rejects_production_change():
    result = EvidenceReconciler().reconcile(
        source_row_count=100,
        evidence_row_count=100,
        source_ddl_before="CREATE TABLE x",
        source_ddl_after="CREATE TABLE x",
        production_changed=True,
        source_write_performed=False,
    )

    assert result.success is False
    assert "production_unchanged" in (
        result.failed_checks
    )


def test_reconciliation_rejects_source_write():
    result = EvidenceReconciler().reconcile(
        source_row_count=100,
        evidence_row_count=100,
        source_ddl_before="CREATE TABLE x",
        source_ddl_after="CREATE TABLE x",
        production_changed=False,
        source_write_performed=True,
    )

    assert result.success is False
    assert "source_write_not_performed" in (
        result.failed_checks
    )