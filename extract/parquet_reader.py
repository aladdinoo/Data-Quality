"""
Parquet data reader.

This module provides a concrete implementation of the
DataReader interface for reading Apache Parquet files.
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
# Constants
# ==================================================

SUPPORTED_EXTENSIONS = {
    ".parquet",
    ".pq",
}

# ==================================================
# Parquet Reader
# ==================================================


class ParquetReader(DataReader):
    """
    Reader for Apache Parquet datasets.
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

        return "Parquet Reader"

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def supports(
        self,
        source: str | Path,
    ) -> bool:
        """
        Determine whether this reader supports
        the given source.
        """

        return (
            Path(source)
            .suffix
            .lower()
            in SUPPORTED_EXTENSIONS
        )

    # --------------------------------------------------

    def read(
        self,
        source: str | Path,
        **kwargs: Any,
    ) -> pd.DataFrame:
        """
        Read a Parquet dataset.

        Parameters
        ----------
        source
            Path to the Parquet file.

        kwargs
            Additional pandas.read_parquet arguments.

        Returns
        -------
        pandas.DataFrame
            Loaded dataset.
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
            "Reading Parquet file: %s",
            path,
        )

        dataframe = pd.read_parquet(
            path,
            **kwargs,
        )

        logger.info(
            "Loaded %d rows and %d columns.",
            len(dataframe),
            len(dataframe.columns),
        )

        return dataframe