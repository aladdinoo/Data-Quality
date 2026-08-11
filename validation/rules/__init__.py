"""
Built-in validation rules.

This package contains all built-in validation rules
shipped with the Data Quality Platform.
"""

from .email import EmailValidationRule
from .phone import PhoneValidationRule
from .website import WebsiteValidationRule
from .zip import ZipValidationRule
from .name import NameValidationRule
from .duplicate import DuplicateValidationRule
from .date import DateValidationRule
from .schema import SchemaValidationRule
from .invariant import InvariantValidationRule
from .pii import PIIValidationRule

__all__ = [
    "EmailValidationRule",
    "PhoneValidationRule",
    "WebsiteValidationRule",
    "ZipValidationRule",
    "NameValidationRule",
    "DuplicateValidationRule",
    "DateValidationRule",
    "SchemaValidationRule",
    "InvariantValidationRule",
    "PIIValidationRule",
]