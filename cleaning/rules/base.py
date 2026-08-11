"""
Base Cleaning Rule.

The base rule defines the execution interface.
Business decisions should be supplied by the rule policy/contract,
not hardcoded into the CleaningEngine.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from cleaning.result import CleaningResult


class CleaningRule(ABC):
    """
    Base class for all cleaning rules.
    """

    name = "base_cleaner"
    version = "1.0.0"
    priority = 100

    # Default metadata only.
    # Final action policy will be handled separately.
    auto_apply = False
    review_required = True

    @abstractmethod
    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> CleaningResult:
        """
        Execute the rule.

        The rule returns a CleaningResult containing:
        - modifications
        - flags
        - errors
        - execution metrics
        """

    def can_auto_apply(self) -> bool:
        """
        Return whether this rule is currently allowed
        to apply an automatic modification.
        """
        return bool(self.auto_apply)

    def requires_review(self) -> bool:
        """
        Return whether the rule requires review.
        """
        return bool(self.review_required)

    def metadata(self) -> dict:
        """
        Return stable metadata describing the rule.
        """
        return {
            "name": self.name,
            "version": self.version,
            "priority": self.priority,
            "auto_apply": self.can_auto_apply(),
            "review_required": self.requires_review(),
        }