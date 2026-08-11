"""
Data extractor.

This module provides the high-level interface used by the
pipeline to load datasets.

The extractor delegates the reading operation to the
appropriate DataReader selected by the ReaderFactory.

Clients should interact only with this class rather than
individual readers.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from pathlib import Path
from typing import Any

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd

# ==================================================
# Local Imports
# ==================================================

from app.logging import LoggerFactory

from .factory import ReaderFactory

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# Data Extractor
# ==================================================


class DataExtractor:
    """
    High-level dataset extractor.

    This class delegates file loading to the
    appropriate reader implementation.
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(
        self,
        factory: ReaderFactory | None = None,
    ) -> None:
        """
        Initialize the extractor.

        Parameters
        ----------
        factory
            Optional reader factory.
        """

        self._factory = (
            factory
            if factory is not None
            else ReaderFactory()
        )

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def read(
        self,
        source: str | Path,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Load a dataset.

        Parameters
        ----------
        source
            Dataset location.

        kwargs
            Reader-specific keyword arguments.

        Returns
        -------
        pandas.DataFrame
            Loaded dataset.
        """

        reader = self._factory.get_reader(
            source
        )

        logger.info(
            "Selected reader: %s",
            reader.name,
        )

        dataframe = reader.read(
            source,
            **kwargs,
        )

        logger.info(
            "Dataset loaded successfully."
        )

        return dataframe

    # --------------------------------------------------

    @property
    def factory(
        self,
    ) -> ReaderFactory:
        """
        Return the underlying reader factory.
        """

        return self._factory