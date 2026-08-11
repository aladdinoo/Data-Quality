"""
Excel data reader.

This module provides a concrete implementation of the
DataReader interface for reading Microsoft Excel files.
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
# Supported Extensions
# ==================================================

SUPPORTED_EXTENSIONS = {
    ".xlsx",
    ".xls",
}

# ==================================================
# Excel Reader
# ==================================================


class ExcelReader(DataReader):
    """
    Reader for Microsoft Excel datasets.
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

        return "Excel Reader"

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
        Read an Excel file.

        Parameters
        ----------
        source
            Excel file path.

        kwargs
            Additional pandas.read_excel arguments.

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
            "Reading Excel file: %s",
            path,
        )

        dataframe = pd.read_excel(
            path,
            **kwargs,
        )

        logger.info(
            "Loaded %d rows and %d columns.",
            len(dataframe),
            len(dataframe.columns),
        )

        return dataframe