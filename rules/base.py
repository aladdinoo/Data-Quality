"""
Base rule.

This module defines the abstract base class implemented
by every validation and cleaning rule.

Rules are designed to be:

- Independent
- Deterministic
- Testable
- Versionable

Each rule operates on a pandas DataFrame and returns a
RuleResult describing the execution outcome.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from abc import ABC, abstractmethod
from time import perf_counter

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd

# ==================================================
# Local Imports
# ==================================================

from app.logging import LoggerFactory

from core.context import PipelineContext

from .metadata import RuleMetadata
from .result import RuleResult

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# Base Rule
# ==================================================


class BaseRule(ABC):
    """
    Abstract base class for all rules.

    Every validation rule and cleaning rule
    must inherit from this class.
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(
        self,
        metadata: RuleMetadata,
    ) -> None:

        self._metadata = metadata

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def metadata(
        self,
    ) -> RuleMetadata:
        """
        Return rule metadata.
        """

        return self._metadata

    @property
    def name(
        self,
    ) -> str:
        """
        Rule name.
        """

        return self.metadata.name

    @property
    def version(
        self,
    ) -> str:
        """
        Rule version.
        """

        return self.metadata.version

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def execute(
        self,
        context: PipelineContext,
    ) -> RuleResult:
        """
        Execute the rule.

        Parameters
        ----------
        context
            Shared pipeline context.

        Returns
        -------
        RuleResult
        """

        logger.info(
            "Running rule: %s (%s)",
            self.name,
            self.version,
        )

        started = perf_counter()

        result = self.apply(
            context
        )

        result.rule = self.name

        result.version = self.version

        result.duration = (
            perf_counter()
            - started
        )

        logger.info(

            "Finished rule: %s (%.3f sec)",

            self.name,

            result.duration,

        )

        return result

    # --------------------------------------------------
    # Abstract API
    # --------------------------------------------------

    @abstractmethod
    def apply(
        self,
        context: PipelineContext,
    ) -> RuleResult:
        """
        Execute the business logic.

        Parameters
        ----------
        context
            Shared execution context.

        Returns
        -------
        RuleResult
        """

        raise NotImplementedError