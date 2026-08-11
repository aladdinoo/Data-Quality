"""
ClickHouse Storage Backend.
"""

from __future__ import annotations

import pandas as pd

from clickhouse_connect import get_client

from .base import StorageBackend


class ClickHouseStorage(StorageBackend):
    """
    ClickHouse backend.
    """

    def __init__(
        self,
        host="localhost",
        port=8123,
        username="default",
        password="",
        database="default",
    ):

        self.client = get_client(

            host=host,

            port=port,

            username=username,

            password=password,

            database=database,

        )

    def read(
        self,
        query: str,
    ) -> pd.DataFrame:

        return self.client.query_df(
            query
        )

    def write(
        self,
        dataframe: pd.DataFrame,
        table: str,
    ) -> None:

        self.client.insert_df(
            table,
            dataframe,
        )

    def exists(
        self,
        table: str,
    ) -> bool:

        result = self.client.query(

            f"EXISTS TABLE {table}"

        )

        return bool(
            result.first_row[0]
        )