"""
Rule severity.

This module defines the severity levels assigned to
validation and cleaning rules.

Severity is used for reporting, monitoring,
quality scoring, and alert generation.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from enum import IntEnum


# ==================================================
# Rule Severity
# ==================================================

class RuleSeverity(IntEnum):
    """
    Rule severity levels.

    Higher values indicate more severe issues.
    """

    # --------------------------------------------------
    # Informational
    # --------------------------------------------------

    INFO = 10

    # --------------------------------------------------
    # Minor issue
    # --------------------------------------------------

    WARNING = 20

    # --------------------------------------------------
    # Data quality problem
    # --------------------------------------------------

    ERROR = 30

    # --------------------------------------------------
    # Pipeline cannot continue
    # --------------------------------------------------

    CRITICAL = 40

    # --------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------

    @property
    def label(
        self,
    ) -> str:
        """
        Human-readable severity.
        """

        return self.name.title()

    @property
    def is_blocking(
        self,
    ) -> bool:
        """
        Whether execution should stop.
        """

        return self >= RuleSeverity.CRITICAL

    @property
    def affects_quality_score(
        self,
    ) -> bool:
        """
        Whether this severity contributes
        to quality scoring.
        """

        return self >= RuleSeverity.WARNING

    @property
    def weight(
        self,
    ) -> int:
        """
        Numeric weight used by quality
        scoring algorithms.
        """

        weights = {

            RuleSeverity.INFO: 0,

            RuleSeverity.WARNING: 1,

            RuleSeverity.ERROR: 5,

            RuleSeverity.CRITICAL: 10,

        }

        return weights[self]