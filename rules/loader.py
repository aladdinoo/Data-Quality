"""
Rule loader.

Builds and populates the RuleRegistry with all available
validation rules.

Rules that cannot be imported are skipped and logged,
allowing the application to continue running.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from importlib import import_module

# ==================================================
# Local Imports
# ==================================================

from app.logging import LoggerFactory

from .registry import RuleRegistry

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# Available Rules
# ==================================================

RULES = [
    ("validation.rules.email", "EmailValidationRule"),
    ("validation.rules.phone", "PhoneValidationRule"),
    ("validation.rules.website", "WebsiteValidationRule"),
    ("validation.rules.zip", "ZipValidationRule"),
    ("validation.rules.name", "NameValidationRule"),
    ("validation.rules.date", "DateValidationRule"),
    ("validation.rules.duplicate", "DuplicateValidationRule"),
    ("validation.rules.schema", "SchemaValidationRule"),
    ("validation.rules.invariant", "InvariantValidationRule"),
    ("validation.rules.pii", "PIIValidationRule"),
]


# ==================================================
# Rule Loader
# ==================================================

class RuleLoader:
    """
    Loads all validation rules into a RuleRegistry.
    """

    def __init__(self) -> None:

        self._registry = RuleRegistry()

    # --------------------------------------------------

    @property
    def registry(self) -> RuleRegistry:
        """
        Return the internal registry.
        """
        return self._registry

    # --------------------------------------------------

    def load(self) -> RuleRegistry:
        """
        Load all available rules.

        Returns
        -------
        RuleRegistry
            Populated registry.
        """

        logger.info("Loading validation rules...")

        self._registry.clear()

        loaded = 0

        for module_name, class_name in RULES:

            try:

                module = import_module(module_name)

                rule_class = getattr(module, class_name)

                self._registry.register(
                    rule_class()
                )

                loaded += 1

                logger.info(
                    "Loaded rule: %s",
                    class_name,
                )

            except Exception:

                logger.exception(
                    "Failed loading rule: %s",
                    class_name,
                )

        logger.info(
            "Successfully loaded %d rule(s).",
            loaded,
        )

        return self._registry

    # --------------------------------------------------

    def reload(self) -> RuleRegistry:
        """
        Reload every rule.
        """

        self._registry.clear()

        return self.load()