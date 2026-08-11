"""
CSV data reader.

This module provides a concrete implementation of the
DataReader interface for reading CSV files.
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

from app.exceptions import (
    DatasetNotFoundError,
    UnsupportedFileTypeError,
)

from app.logging import LoggerFactory

from .base import DataReader

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# CSV Reader
# ==================================================


class CSVReader(DataReader):
    """
    Reader for CSV datasets.
    """

    # --------------------------------------------------
    # Properties
    # --------------------------------------------------

    @property
    def name(
        self,
    ) -> str:
        """
        Reader name.
        """

        return "CSV Reader"

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def supports(
        self,
        source: str | Path,
    ) -> bool:
        """
        Whether this reader supports the source.
        """

        return (
            Path(source)
            .suffix
            .lower()
            == ".csv"
        )

    # --------------------------------------------------

    def read(
        self,
        source: str | Path,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Read a CSV file.

        Parameters
        ----------
        source
            CSV file path.

        kwargs
            Additional pandas.read_csv arguments.

        Returns
        -------
        pandas.DataFrame
        """

        path = Path(source)

        if not path.exists():

            raise DatasetNotFoundError(
                f"Dataset not found: {path}"
            )

        if not self.supports(path):

            raise UnsupportedFileTypeError(
                f"{path.suffix} is not supported."
            )

        logger.info(
            "Reading CSV file: %s",
            path,
        )

        dataframe = pd.read_csv(
            path,
            **kwargs,
        )

        logger.info(
            "Loaded %d rows and %d columns.",
            len(dataframe),
            len(dataframe.columns),
        )

        return dataframe