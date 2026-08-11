"""
Rule contract.

This module defines the immutable contract describing
how a rule behaves inside the Data Quality Platform.

A rule contract specifies:

- Rule metadata
- Target columns
- Expected inputs
- Expected outputs
- Success criteria

The contract is versioned and serves as the source of
truth for execution, auditing, validation, and reporting.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field

# ==================================================
# Local Imports
# ==================================================

from schema.models import ColumnType

from .metadata import RuleMetadata


# ==================================================
# Rule Contract
# ==================================================

@dataclass(slots=True, frozen=True)
class RuleContract:
    """
    Immutable definition of a rule.

    The contract describes what a rule expects,
    what it produces, and how it should behave.
    """

    # --------------------------------------------------
    # Rule Information
    # --------------------------------------------------

    metadata: RuleMetadata

    # --------------------------------------------------
    # Target Columns
    # --------------------------------------------------

    supported_columns: tuple[
        ColumnType,
        ...
    ] = ()

    required_columns: tuple[
        ColumnType,
        ...
    ] = ()

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    enabled: bool = True

    deterministic: bool = True

    parallelizable: bool = False

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    modifies_data: bool = False

    creates_review_flags: bool = False

    produces_metrics: bool = True

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    success_threshold: float = 1.0

    # --------------------------------------------------
    # Documentation
    # --------------------------------------------------

    notes: str = ""

    tags: tuple[str, ...] = ()

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def __post_init__(
        self,
    ) -> None:

        if not (
            0.0
            <= self.success_threshold
            <= 1.0
        ):

            raise ValueError(
                "success_threshold must "
                "be between 0 and 1."
            )

    # --------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------

    @property
    def identifier(
        self,
    ) -> str:
        """
        Fully-qualified contract identifier.
        """

        return (
            self.metadata.identifier
        )

    @property
    def supports_multiple_columns(
        self,
    ) -> bool:
        """
        Whether the rule supports more
        than one logical column.
        """

        return (
            len(
                self.supported_columns
            ) > 1
        )

    @property
    def requires_input(
        self,
    ) -> bool:
        """
        Whether at least one logical
        column is required.
        """

        return bool(
            self.required_columns
        )