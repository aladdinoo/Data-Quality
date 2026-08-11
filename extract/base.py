"""
Abstract data reader.

This module defines the abstract interface implemented
by every data reader.

Supported readers include:

- CSV
- Excel
- Parquet
- S3
- ClickHouse
- Database readers

Every reader returns a pandas DataFrame.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from abc import ABC, abstractmethod
from pathlib import Path

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd


# ==================================================
# Base Reader
# ==================================================

class DataReader(ABC):
    """
    Abstract base class for all data readers.

    Every concrete reader must implement the
    read() method.
    """

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    @abstractmethod
    def read(
        self,
        source: str | Path,
    ) -> pd.DataFrame:
        """
        Read a dataset.

        Parameters
        ----------
        source
            File path, URL, or other supported source.

        Returns
        -------
        pandas.DataFrame
            Loaded dataset.
        """

        raise NotImplementedError

    # --------------------------------------------------

    @abstractmethod
    def supports(
        self,
        source: str | Path,
    ) -> bool:
        """
        Determine whether this reader supports
        the given source.

        Parameters
        ----------
        source
            Input source.

        Returns
        -------
        bool
            True if supported.
        """

        raise NotImplementedError

    # --------------------------------------------------

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Reader name.

        Returns
        -------
        str
            Human-readable reader name.
        """

        raise NotImplementedError