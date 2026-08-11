"""
Data reader factory.

This module provides a factory responsible for selecting
the appropriate DataReader implementation for a given
data source.

The factory is easily extensible by registering additional
reader implementations.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from pathlib import Path

# ==================================================
# Local Imports
# ==================================================

from app.exceptions import UnsupportedFileTypeError

from .base import DataReader
from .csv_reader import CSVReader
from .excel_reader import ExcelReader
from .parquet_reader import ParquetReader

# ==================================================
# Reader Factory
# ==================================================


class ReaderFactory:
    """
    Factory responsible for selecting
    the correct data reader.
    """

    # --------------------------------------------------
    # Constructor
    # --------------------------------------------------

    def __init__(
        self,
    ) -> None:

        self._readers: list[DataReader] = [

            CSVReader(),

            ExcelReader(),

            ParquetReader(),

        ]

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def get_reader(
        self,
        source: str | Path,
    ) -> DataReader:
        """
        Return a reader capable of handling
        the given source.

        Parameters
        ----------
        source
            Dataset location.

        Returns
        -------
        DataReader
            Matching reader implementation.
        """

        for reader in self._readers:

            if reader.supports(source):

                return reader

        raise UnsupportedFileTypeError(
            f"No reader available for: {source}"
        )

    # --------------------------------------------------

    def register(
        self,
        reader: DataReader,
    ) -> None:
        """
        Register a new reader.

        Parameters
        ----------
        reader
            Reader implementation.
        """

        self._readers.append(
            reader
        )

    # --------------------------------------------------

    @property
    def readers(
        self,
    ) -> tuple[DataReader, ...]:
        """
        Return registered readers.
        """

        return tuple(
            self._readers
        )

    # --------------------------------------------------

    def __len__(
        self,
    ) -> int:
        """
        Return number of registered readers.
        """

        return len(
            self._readers
        )