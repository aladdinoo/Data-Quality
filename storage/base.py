"""
Base Storage Backend.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class StorageBackend(ABC):
    """
    Base class for all storage backends.
    """

    @abstractmethod
    def read(
        self,
        source: str,
    ) -> pd.DataFrame:
        """
        Read a dataset.
        """

    @abstractmethod
    def write(
        self,
        dataframe: pd.DataFrame,
        destination: str,
    ) -> None:
        """
        Write a dataset.
        """

    @abstractmethod
    def exists(
        self,
        path: str,
    ) -> bool:
        """
        Check whether the object exists.
        """