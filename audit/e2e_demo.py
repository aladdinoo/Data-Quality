"""
Local E2E audit demonstration.
"""

from pathlib import Path

from audit.e2e_audit_run import (
    AuditRunConfig,
    E2EAuditRun,
)


def main() -> None:

    config = AuditRunConfig(
        database="consumer_db",
        table="consumer_data",
        view_target="consumer_data_clean",
        source_ddl="""
        CREATE TABLE consumer_data (
            id INTEGER,
            email TEXT,
            zip TEXT,
            state TEXT
        )
        """,
        output_directory=Path(
            "artifacts/e2e"
        ),
    )

    result = E2EAuditRun(
        config
    ).run()

    print()
    print("=" * 60)
    print("E2E AUDIT RESULT")
    print("=" * 60)

    print(
        f"Run ID       : {result.run_id}"
    )

    print(
        f"Success      : {result.success}"
    )

    print(
        f"Manifest     : {result.manifest_file}"
    )

    print(
        f"Manifest SHA : {result.manifest_sha256}"
    )

    print(
        f"Reconciled   : "
        f"{result.reconciliation.success}"
    )


if __name__ == "__main__":
    main()