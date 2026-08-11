"""
PostgreSQL Storage Backend.
"""

from __future__ import annotations

import pandas as pd

from sqlalchemy import create_engine

from .base import StorageBackend


class PostgresStorage(StorageBackend):
    """
    PostgreSQL backend.
    """

    def __init__(
        self,
        connection_string: str,
    ):

        self.engine = create_engine(
            connection_string
        )

    def read(
        self,
        query: str,
    ) -> pd.DataFrame:

        return pd.read_sql(
            query,
            self.engine,
        )

    def write(
        self,
        dataframe: pd.DataFrame,
        table: str,
    ) -> None:

        dataframe.to_sql(

            table,

            self.engine,

            if_exists="append",

            index=False,

        )

    def exists(
        self,
        table: str,
    ) -> bool:

        query = f"""

        SELECT EXISTS (

            SELECT 1

            FROM information_schema.tables

            WHERE table_name='{table}'

        )

        """

        return bool(

            pd.read_sql(
                query,
                self.engine,
            ).iloc[0, 0]

        )