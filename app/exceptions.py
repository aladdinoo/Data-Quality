"""
Application-specific exceptions.

This module defines the exception hierarchy used by the
Data Quality Platform.

All custom exceptions inherit from DataQualityError,
allowing the pipeline to catch platform-specific failures
without masking unexpected system exceptions.
"""

from __future__ import annotations

# ==================================================
# Base Exception
# ==================================================


class DataQualityError(Exception):
    """
    Base exception for the Data Quality Platform.

    All platform exceptions should inherit from this class.
    """

    pass


# ==================================================
# Configuration
# ==================================================


class ConfigurationError(DataQualityError):
    """
    Raised when application configuration is invalid.
    """

    pass


# ==================================================
# Pipeline
# ==================================================


class PipelineError(DataQualityError):
    """
    Raised when a pipeline execution fails.
    """

    pass


class StageExecutionError(PipelineError):
    """
    Raised when a pipeline stage fails.
    """

    pass


# ==================================================
# Data
# ==================================================


class DatasetError(DataQualityError):
    """
    Base exception for dataset-related failures.
    """

    pass


class DatasetNotFoundError(DatasetError):
    """
    Raised when a dataset cannot be located.
    """

    pass


class UnsupportedFileTypeError(DatasetError):
    """
    Raised when attempting to read an unsupported file.
    """

    pass


class DatasetVersionError(DatasetError):
    """
    Raised when dataset version information is invalid.
    """

    pass


# ==================================================
# Schema
# ==================================================


class SchemaError(DataQualityError):
    """
    Raised when schema detection fails.
    """

    pass


class SchemaMismatchError(SchemaError):
    """
    Raised when the detected schema differs from the
    expected schema.
    """

    pass


class SchemaDriftError(SchemaError):
    """
    Raised when schema evolution is detected.
    """

    pass


# ==================================================
# Validation
# ==================================================


class ValidationError(DataQualityError):
    """
    Raised when validation fails.
    """

    pass


class ValidationRuleError(ValidationError):
    """
    Raised when a validation rule cannot be executed.
    """

    pass


class InvariantViolationError(ValidationError):
    """
    Raised when an invariant is violated.
    """

    pass


# ==================================================
# Cleaning
# ==================================================


class CleaningError(DataQualityError):
    """
    Raised when data cleaning fails.
    """

    pass


class NormalizationError(CleaningError):
    """
    Raised when normalization cannot be completed.
    """

    pass


class DuplicateDetectionError(CleaningError):
    """
    Raised when duplicate detection fails.
    """

    pass


# ==================================================
# Rules
# ==================================================


class RuleError(DataQualityError):
    """
    Raised for rule-related failures.
    """

    pass


class RuleNotFoundError(RuleError):
    """
    Raised when a requested rule cannot be found.
    """

    pass


class RuleVersionError(RuleError):
    """
    Raised when a rule version is invalid.
    """

    pass


class RuleConfigurationError(RuleError):
    """
    Raised when a rule configuration is invalid.
    """

    pass


# ==================================================
# Audit
# ==================================================


class AuditError(DataQualityError):
    """
    Raised for audit logging failures.
    """

    pass


class EvidenceError(DataQualityError):
    """
    Raised when evidence generation fails.
    """

    pass


class LineageError(DataQualityError):
    """
    Raised when lineage recording fails.
    """

    pass


# ==================================================
# Storage
# ==================================================


class StorageError(DataQualityError):
    """
    Raised when storage operations fail.
    """

    pass


class RawStorageError(StorageError):
    """
    Raised for raw storage failures.
    """

    pass


class CuratedStorageError(StorageError):
    """
    Raised for curated storage failures.
    """

    pass


class MetadataError(StorageError):
    """
    Raised when metadata operations fail.
    """

    pass


# ==================================================
# Security
# ==================================================


class PermissionDeniedError(DataQualityError):
    """
    Raised when access is denied.
    """

    pass


class PIIAccessError(PermissionDeniedError):
    """
    Raised when unauthorized access to PII is attempted.
    """

    pass


# ==================================================
# Monitoring
# ==================================================


class MonitoringError(DataQualityError):
    """
    Raised when monitoring or metrics collection fails.
    """

    pass