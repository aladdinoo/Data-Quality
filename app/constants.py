"""
Global constants and enumerations used throughout the
Data Quality Platform.

This module centralizes all shared constants, enums,
and default values to eliminate magic strings and
provide consistent behavior across the platform.

Every component (Pipeline, Validation, Cleaning,
Audit, Reporting, Airflow, and Streamlit) should
import constants from this module.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from enum import Enum
from typing import Final

# ==================================================
# Application Information
# ==================================================

APPLICATION_NAME: Final[str] = "Data Quality Platform"

APPLICATION_VERSION: Final[str] = "1.0.0"

# ==================================================
# Pipeline Status
# ==================================================


class PipelineStatus(str, Enum):
    """
    Overall pipeline execution status.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"


# ==================================================
# Stage Status
# ==================================================


class StageStatus(str, Enum):
    """
    Individual pipeline stage status.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    SKIPPED = "SKIPPED"


# ==================================================
# Rule Severity
# ==================================================


class RuleSeverity(str, Enum):
    """
    Severity level assigned to a rule.
    """

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"


# ==================================================
# Rule Action
# ==================================================


class RuleAction(str, Enum):
    """
    Action taken when a rule matches.
    """

    CLEAN = "CLEAN"

    REVIEW = "REVIEW"

    REJECT = "REJECT"

    IGNORE = "IGNORE"


# ==================================================
# Validation Status
# ==================================================


class ValidationStatus(str, Enum):
    """
    Validation result.
    """

    PASSED = "PASSED"

    FAILED = "FAILED"

    WARNING = "WARNING"


# ==================================================
# Duplicate Detection
# ==================================================


class DuplicateType(str, Enum):
    """
    Supported duplicate detection modes.
    """

    EXACT = "EXACT"

    FUZZY = "FUZZY"


# ==================================================
# Dataset Status
# ==================================================


class DatasetStatus(str, Enum):
    """
    Dataset lifecycle status.
    """

    RAW = "RAW"

    PROFILED = "PROFILED"

    VALIDATED = "VALIDATED"

    CLEANED = "CLEANED"

    CURATED = "CURATED"


# ==================================================
# Storage Layer
# ==================================================


class StorageType(str, Enum):
    """
    Storage backend.
    """

    RAW = "RAW"

    CURATED = "CURATED"

    AUDIT = "AUDIT"

    EVIDENCE = "EVIDENCE"


# ==================================================
# Environment
# ==================================================


class Environment(str, Enum):
    """
    Deployment environment.
    """

    DEVELOPMENT = "development"

    TESTING = "testing"

    STAGING = "staging"

    PRODUCTION = "production"


# ==================================================
# Evidence
# ==================================================


class EvidenceType(str, Enum):
    """
    Validation evidence artifact.
    """

    REPORT = "REPORT"

    GOLDEN_TEST = "GOLDEN_TEST"

    PILOT = "PILOT"

    AUDIT = "AUDIT"


# ==================================================
# Audit
# ==================================================

AUDIT_TIMESTAMP_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

DEFAULT_ENCODING: Final[str] = "utf-8"

DEFAULT_DATE_FORMAT: Final[str] = "%Y-%m-%d"

# ==================================================
# Processing
# ==================================================

DEFAULT_BATCH_SIZE: Final[int] = 100_000

DEFAULT_CHUNK_SIZE: Final[int] = 50_000

DEFAULT_MAX_RETRIES: Final[int] = 3

# ==================================================
# File Extensions
# ==================================================

SUPPORTED_FILE_EXTENSIONS: Final[frozenset[str]] = frozenset(
    {
        ".csv",
        ".xlsx",
        ".xls",
        ".parquet",
    }
)

# ==================================================
# Quality Score
# ==================================================

QUALITY_SCORE_MIN: Final[int] = 0

QUALITY_SCORE_MAX: Final[int] = 100

# ==================================================
# Default Rule Version
# ==================================================

DEFAULT_RULE_VERSION: Final[str] = "1.0.0"

DEFAULT_PIPELINE_VERSION: Final[str] = "1.0.0"