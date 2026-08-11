"""
Rule registry.

This module manages the collection of all registered
data quality rules.

The registry is responsible for:

- Registering rules
- Enabling/disabling rules
- Looking up rules
- Returning execution order
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from collections.abc import Iterator

# ==================================================
# Local Imports
# ==================================================

from .base import BaseRule


# ==================================================
# Rule Registry
# ==================================================


class RuleRegistry:
    """
    Registry of all available rules.
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(self) -> None:

        self._rules: list[BaseRule] = []

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def register(
        self,
        rule: BaseRule,
    ) -> None:
        """
        Register a new rule.

        Parameters
        ----------
        rule
            Rule instance.
        """

        self._rules.append(rule)

    # --------------------------------------------------

    def unregister(
        self,
        name: str,
    ) -> None:
        """
        Remove a rule by name.
        """

        self._rules = [

            rule

            for rule in self._rules

            if rule.name != name

        ]

    # --------------------------------------------------

    def clear(
        self,
    ) -> None:
        """
        Remove all registered rules.
        """

        self._rules.clear()

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> BaseRule | None:
        """
        Retrieve a rule by name.
        """

        for rule in self._rules:

            if rule.name == name:

                return rule

        return None

    # --------------------------------------------------

    def enabled_rules(
        self,
    ) -> list[BaseRule]:
        """
        Return all enabled rules ordered
        by category execution priority.
        """

        enabled = [

            rule

            for rule in self._rules

            if rule.metadata.enabled

        ]

        enabled.sort(

            key=lambda rule: (

                rule.metadata.category.execution_order,

                rule.name,

            )

        )

        return enabled

    # --------------------------------------------------

    def by_category(
        self,
        category: str,
    ) -> list[BaseRule]:
        """
        Return rules belonging to
        one category.
        """

        return [

            rule

            for rule in self._rules

            if rule.metadata.category.value == category

        ]

    # --------------------------------------------------
    # Magic Methods
    # --------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self._rules
        )

    def __iter__(
        self,
    ) -> Iterator[BaseRule]:

        return iter(
            self.enabled_rules()
        )

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return any(

            rule.name == name

            for rule in self._rules

        )