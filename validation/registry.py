"""
Validation registry.

Thin wrapper around the shared RuleRegistry.
"""

from __future__ import annotations

from rules.base import BaseRule
from rules.registry import RuleRegistry


class ValidationRegistry:
    """
    Validation registry.

    Delegates storage to RuleRegistry.
    """

    def __init__(
        self,
    ) -> None:

        self._registry = RuleRegistry()

    # --------------------------------------------------

    @property
    def registry(
        self,
    ) -> RuleRegistry:

        return self._registry

    # --------------------------------------------------

    def register(
        self,
        rule: BaseRule,
    ) -> None:

        self._registry.register(
            rule
        )

    # --------------------------------------------------

    def clear(
        self,
    ) -> None:

        self._registry.clear()

    # --------------------------------------------------

    def __iter__(
        self,
    ):

        return iter(
            self._registry
        )

    # --------------------------------------------------

    def __len__(
        self,
    ):

        return len(
            self._registry
        )