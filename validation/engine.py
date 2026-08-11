"""
Validation engine.

Coordinates validation rule execution.
"""

from __future__ import annotations

from app.logging import LoggerFactory

from core.context import PipelineContext

from rules.executor import (
    PipelineResult,
    RuleExecutor,
)

from rules.loader import RuleLoader
from rules.registry import RuleRegistry

from .policies import ValidationPolicy

logger = LoggerFactory.get_logger(__name__)


class ValidationEngine:
    """
    Executes validation rules.
    """

    def __init__(
        self,
        registry: RuleRegistry | None = None,
        executor: RuleExecutor | None = None,
        policy: ValidationPolicy | None = None,
    ) -> None:

        if registry is None:

            registry = RuleLoader().load()

        if executor is None:

            executor = RuleExecutor(
                registry
            )

        if policy is None:

            policy = ValidationPolicy()

        self._registry = registry
        self._executor = executor
        self._policy = policy

    @property
    def registry(self) -> RuleRegistry:

        return self._registry

    def execute(
        self,
        context: PipelineContext,
    ) -> PipelineResult:

        logger.info(
            "Validation started."
        )

        self._policy.before_validation(
            context
        )

        result = self._executor.execute(
            context
        )

        self._policy.after_validation(
            context,
            result,
        )

        logger.info(
            "Validation finished."
        )

        return result