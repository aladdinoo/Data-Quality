"""
Rule Engine.

Core infrastructure for the Data Quality Platform.

This package contains:

- BaseRule
- RuleRegistry
- RuleExecutor
- RuleLoader
- RuleResult
- RuleMetadata
"""

from .base import BaseRule
from .executor import RuleExecutor, PipelineResult
from .loader import RuleLoader
from .metadata import RuleMetadata
from .registry import RuleRegistry
from .result import RuleResult

__all__ = [
    "BaseRule",
    "RuleRegistry",
    "RuleExecutor",
    "RuleLoader",
    "RuleMetadata",
    "RuleResult",
    "PipelineResult",
]