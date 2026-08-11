"""
Rule categories.

This module defines the supported categories for
data quality rules.

Categories are used to organize rules, control
execution order, reporting, and orchestration.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from enum import StrEnum


# ==================================================
# Rule Category
# ==================================================

class RuleCategory(StrEnum):
    """
    Supported rule categories.
    """

    # --------------------------------------------------
    # Data Validation
    # --------------------------------------------------

    VALIDATION = "validation"

    # --------------------------------------------------
    # Data Cleaning
    # --------------------------------------------------

    CLEANING = "cleaning"

    # --------------------------------------------------
    # Standardization
    # --------------------------------------------------

    NORMALIZATION = "normalization"

    # --------------------------------------------------
    # Duplicate Detection
    # --------------------------------------------------

    DUPLICATE_DETECTION = "duplicate_detection"

    # --------------------------------------------------
    # Schema Validation
    # --------------------------------------------------

    SCHEMA = "schema"

    # --------------------------------------------------
    # Data Profiling
    # --------------------------------------------------

    PROFILING = "profiling"

    # --------------------------------------------------
    # Business Rules
    # --------------------------------------------------

    BUSINESS = "business"

    # --------------------------------------------------
    # Data Enrichment
    # --------------------------------------------------

    ENRICHMENT = "enrichment"

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    @property
    def label(
        self,
    ) -> str:
        """
        Human-readable category name.
        """

        return self.value.replace(
            "_",
            " ",
        ).title()

    @property
    def execution_order(
        self,
    ) -> int:
        """
        Default execution priority.

        Lower values execute first.
        """

        priorities = {

            RuleCategory.SCHEMA: 10,

            RuleCategory.PROFILING: 20,

            RuleCategory.VALIDATION: 30,

            RuleCategory.NORMALIZATION: 40,

            RuleCategory.CLEANING: 50,

            RuleCategory.DUPLICATE_DETECTION: 60,

            RuleCategory.BUSINESS: 70,

            RuleCategory.ENRICHMENT: 80,

        }

        return priorities[self]