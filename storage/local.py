"""
Local Storage Backend.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .base import StorageBackend


class LocalStorage(StorageBackend):
    """
    Local filesystem storage.
    """

    def read(
        self,
        source: str,
    ) -> pd.DataFrame:

        path = Path(source)

        suffix = path.suffix.lower()

        if suffix == ".csv":
            return pd.read_csv(path)

        if suffix in (".parquet", ".pq"):
            return pd.read_parquet(path)

        if suffix in (".xlsx", ".xls"):
            return pd.read_excel(path)

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    def write(
        self,
        dataframe: pd.DataFrame,
        destination: str,
    ) -> None:

        path = Path(destination)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        suffix = path.suffix.lower()

        if suffix == ".csv":
            dataframe.to_csv(
                path,
                index=False,
            )
            return

        if suffix in (".parquet", ".pq"):
            dataframe.to_parquet(
                path,
                index=False,
            )
            return

        if suffix in (".xlsx", ".xls"):
            dataframe.to_excel(
                path,
                index=False,
            )
            return

        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    def exists(
        self,
        path: str,
    ) -> bool:

        return Path(path).exists()