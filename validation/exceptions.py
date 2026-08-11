"""
Validation exceptions.
"""

from __future__ import annotations


class ValidationError(Exception):
    """
    Base validation exception.
    """


class ValidationConfigurationError(
    ValidationError,
):
    """
    Invalid validation configuration.
    """


class ValidationExecutionError(
    ValidationError,
):
    """
    Raised when validation execution fails.
    """


class RuleRegistrationError(
    ValidationError,
):
    """
    Raised when rule registration fails.
    """


class RuleNotFoundError(
    ValidationError,
):
    """
    Raised when a rule cannot be found.
    """