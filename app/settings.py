"""
Application configuration.

This module centralizes all platform configuration.

The Settings dataclass provides immutable configuration
used throughout the Data Quality Platform.

No component should hard-code file paths, retry counts,
batch sizes, or environment-specific values.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass
from pathlib import Path

# ==================================================
# Settings
# ==================================================


@dataclass(slots=True, frozen=True)
class Settings:
    """
    Global platform configuration.
    """

    # --------------------------------------------------
    # Environment
    # --------------------------------------------------

    environment: str = "development"

    debug: bool = True

    # --------------------------------------------------
    # Storage
    # --------------------------------------------------

    data_directory: Path = Path("data")

    raw_directory: Path = Path("data/raw")

    curated_directory: Path = Path("data/curated")

    audit_directory: Path = Path("data/audit")

    evidence_directory: Path = Path("data/evidence")

    reports_directory: Path = Path("data/reports")

    rules_directory: Path = Path("rules")

    # --------------------------------------------------
    # Processing
    # --------------------------------------------------

    batch_size: int = 100_000

    chunk_size: int = 50_000

    max_retries: int = 3

    worker_count: int = 4

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    validation_threshold: float = 0.95

    quality_score_threshold: float = 90.0

    enable_human_review: bool = True

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    log_level: str = "INFO"

    log_directory: Path = Path("logs")

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata_database: str = "metadata.db"

    # --------------------------------------------------
    # ClickHouse
    # --------------------------------------------------

    clickhouse_host: str = "localhost"

    clickhouse_port: int = 9000

    clickhouse_database: str = "data_quality"

    clickhouse_username: str = "default"

    clickhouse_password: str = ""

    # --------------------------------------------------
    # PostgreSQL
    # --------------------------------------------------

    postgres_host: str = "localhost"

    postgres_port: int = 5432

    postgres_database: str = "metadata"

    postgres_username: str = "postgres"

    postgres_password: str = ""

    # --------------------------------------------------
    # Airflow
    # --------------------------------------------------

    airflow_dag_directory: Path = Path("airflow/dags")

    airflow_enabled: bool = False

    # --------------------------------------------------
    # Streamlit
    # --------------------------------------------------

    streamlit_port: int = 8501

    streamlit_host: str = "localhost"

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def create_directories(self) -> None:
        """
        Create all required application directories.

        Existing directories are ignored.
        """

        directories = (

            self.data_directory,

            self.raw_directory,

            self.curated_directory,

            self.audit_directory,

            self.evidence_directory,

            self.reports_directory,

            self.rules_directory,

            self.log_directory,

        )

        for directory in directories:

            directory.mkdir(

                parents=True,

                exist_ok=True,

            )


# ==================================================
# Default Settings
# ==================================================

settings = Settings()