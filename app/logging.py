"""
Centralized logging utilities.

This module provides a single logging interface for the
Data Quality Platform.

All application components should obtain loggers from
this module instead of creating their own logging
configuration.

Features
--------
- Console logging
- File logging
- Configurable log level
- Consistent formatting
- Thread-safe
- Airflow compatible
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ==================================================
# Local Imports
# ==================================================

from .settings import settings

# ==================================================
# Constants
# ==================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==================================================
# Logging Factory
# ==================================================


class LoggerFactory:
    """
    Creates and manages application loggers.

    Loggers are created only once and reused
    throughout the application.
    """

    _configured: bool = False

    @classmethod
    def configure(cls) -> None:
        """
        Configure the root logger.
        """

        if cls._configured:
            return

        settings.log_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        formatter = logging.Formatter(
            fmt=LOG_FORMAT,
            datefmt=DATE_FORMAT,
        )

        # ------------------------------------------
        # Console Handler
        # ------------------------------------------

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(
            formatter
        )

        # ------------------------------------------
        # File Handler
        # ------------------------------------------

        file_handler = RotatingFileHandler(
            filename=settings.log_directory / "platform.log",
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(
            formatter
        )

        # ------------------------------------------
        # Root Logger
        # ------------------------------------------

        root_logger = logging.getLogger()

        root_logger.setLevel(
            settings.log_level.upper()
        )

        root_logger.addHandler(
            console_handler
        )

        root_logger.addHandler(
            file_handler
        )

        cls._configured = True

    # --------------------------------------------------

    @classmethod
    def get_logger(
        cls,
        name: str,
    ) -> logging.Logger:
        """
        Return a configured logger.

        Parameters
        ----------
        name
            Logger name.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """

        cls.configure()

        return logging.getLogger(
            name
        )


# ==================================================
# Default Logger
# ==================================================

logger = LoggerFactory.get_logger(
    "data_quality"
)