"""
Rule metadata.

This module defines immutable metadata describing a rule.

The metadata uniquely identifies a rule and provides the
information required for auditing, reporting, versioning,
and execution.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass

# ==================================================
# Local Imports
# ==================================================

from .category import RuleCategory
from .severity import RuleSeverity

# ==================================================
# Rule Metadata
# ==================================================


@dataclass(slots=True, frozen=True)
class RuleMetadata:
    """
    Immutable rule metadata.

    Every rule must have exactly one metadata object.
    """

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    name: str

    version: str

    description: str

    # --------------------------------------------------
    # Classification
    # --------------------------------------------------

    category: RuleCategory

    severity: RuleSeverity

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    enabled: bool = True

    auto_fix: bool = False

    review_required: bool = False

    deterministic: bool = True

    # --------------------------------------------------
    # Documentation
    # --------------------------------------------------

    owner: str = ""

    documentation: str = ""

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def __post_init__(
        self,
    ) -> None:
        """
        Validate metadata.
        """

        if not self.name.strip():

            raise ValueError(
                "Rule name cannot be empty."
            )

        if not self.version.strip():

            raise ValueError(
                "Rule version cannot be empty."
            )

        if self.auto_fix and self.review_required:

            raise ValueError(

                "A rule cannot be both "

                "auto-fix and review-only."

            )

    # --------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        """
        Fully-qualified rule identifier.
        """

        return f"{self.name}:{self.version}"

    @property
    def is_review_only(
        self,
    ) -> bool:
        """
        Whether the rule only creates review flags.
        """

        return self.review_required

    @property
    def can_auto_fix(
        self,
    ) -> bool:
        """
        Whether the rule is allowed to
        automatically modify data.
        """

        return self.auto_fix