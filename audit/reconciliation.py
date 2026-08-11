"""
Audit reconciliation.

Validates the invariants of a read-only audit run.

The module exposes two compatible APIs:

1. Functional API:
   - ReconciliationInput
   - ReconciliationResult
   - reconcile()
   - assert_reconciled()

2. Facade API:
   - EvidenceReconciler
   - EvidenceReconciler().reconcile(...)

Both APIs use the same reconciliation rules.
"""

from __future__ import annotations

from dataclasses import dataclass


# ============================================================
# Reconciliation Input
# ============================================================


@dataclass(frozen=True, slots=True)
class ReconciliationInput:
    """Inputs required for reconciliation."""

    source_row_count_before: int
    source_row_count_after: int

    ddl_hash_before: str
    ddl_hash_after: str

    production_changed: bool
    source_write_performed: bool


# ============================================================
# Reconciliation Result
# ============================================================


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    """Result of audit reconciliation."""

    success: bool

    row_count_unchanged: bool
    ddl_unchanged: bool
    production_unchanged: bool
    source_write_absent: bool

    failures: tuple[str, ...]

    # --------------------------------------------------------
    # Compatibility with EvidenceReconciler tests
    # --------------------------------------------------------

    @property
    def failed_checks(self) -> list[str]:
        """
        Return canonical check names expected by the
        EvidenceReconciler facade tests.
        """

        mapping = {
            "SOURCE_ROW_COUNT_CHANGED":
                "row_count_preserved",

            "SOURCE_DDL_CHANGED":
                "ddl_unchanged",

            "PRODUCTION_CHANGED":
                "production_unchanged",

            "SOURCE_WRITE_PERFORMED":
                "source_write_not_performed",
        }

        return [
            mapping.get(
                failure,
                failure,
            )
            for failure in self.failures
        ]


# ============================================================
# Reconciliation Error
# ============================================================


class ReconciliationError(RuntimeError):
    """Raised when reconciliation fails."""


# ============================================================
# Functional Reconciliation API
# ============================================================


def reconcile(
    data: ReconciliationInput,
) -> ReconciliationResult:
    """
    Reconcile source invariants.

    The audit succeeds only when:

    - row count is unchanged
    - DDL is unchanged
    - production was not changed
    - no source write occurred
    """

    failures: list[str] = []

    # --------------------------------------------------------
    # Row count
    # --------------------------------------------------------

    row_count_unchanged = (
        data.source_row_count_before
        == data.source_row_count_after
    )

    if not row_count_unchanged:
        failures.append(
            "SOURCE_ROW_COUNT_CHANGED"
        )

    # --------------------------------------------------------
    # DDL
    # --------------------------------------------------------

    ddl_unchanged = (
        data.ddl_hash_before
        == data.ddl_hash_after
    )

    if not ddl_unchanged:
        failures.append(
            "SOURCE_DDL_CHANGED"
        )

    # --------------------------------------------------------
    # Production state
    # --------------------------------------------------------

    production_unchanged = (
        not data.production_changed
    )

    if not production_unchanged:
        failures.append(
            "PRODUCTION_CHANGED"
        )

    # --------------------------------------------------------
    # Source writes
    # --------------------------------------------------------

    source_write_absent = (
        not data.source_write_performed
    )

    if not source_write_absent:
        failures.append(
            "SOURCE_WRITE_PERFORMED"
        )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return ReconciliationResult(
        success=not failures,
        row_count_unchanged=row_count_unchanged,
        ddl_unchanged=ddl_unchanged,
        production_unchanged=production_unchanged,
        source_write_absent=source_write_absent,
        failures=tuple(failures),
    )


# ============================================================
# Assertion API
# ============================================================


def assert_reconciled(
    data: ReconciliationInput,
) -> ReconciliationResult:
    """
    Reconcile and raise when any invariant fails.
    """

    result = reconcile(data)

    if not result.success:
        raise ReconciliationError(
            "Audit reconciliation failed: "
            + ", ".join(result.failures)
        )

    return result


# ============================================================
# Evidence Reconciler Facade
# ============================================================


class EvidenceReconciler:
    """
    High-level reconciliation facade.

    This API is intentionally compatible with the E2E audit
    tests and accepts source/evidence row counts directly.
    """

    def reconcile(
        self,
        source_row_count: int,
        evidence_row_count: int,
        source_ddl_before: str,
        source_ddl_after: str,
        production_changed: bool,
        source_write_performed: bool,
    ) -> ReconciliationResult:
        """
        Reconcile source evidence against audit evidence.
        """

        from audit.ddl_capture import DDLCapture

        result = reconcile(
            ReconciliationInput(
                source_row_count_before=source_row_count,
                source_row_count_after=evidence_row_count,
                ddl_hash_before=DDLCapture.sha256(
                    source_ddl_before
                ),
                ddl_hash_after=DDLCapture.sha256(
                    source_ddl_after
                ),
                production_changed=production_changed,
                source_write_performed=source_write_performed,
            )
        )

        return result