"""
Amazon S3 Storage Backend.
"""

from __future__ import annotations

import pandas as pd
import boto3

from io import BytesIO

from .base import StorageBackend


class S3Storage(StorageBackend):
    """
    Amazon S3 storage backend.
    """

    def __init__(self) -> None:

        self.client = boto3.client("s3")

    def read(
        self,
        bucket: str,
        key: str,
    ) -> pd.DataFrame:

        response = self.client.get_object(
            Bucket=bucket,
            Key=key,
        )

        return pd.read_parquet(
            BytesIO(
                response["Body"].read()
            )
        )

    def write(
        self,
        dataframe: pd.DataFrame,
        bucket: str,
        key: str,
    ) -> None:

        buffer = BytesIO()

        dataframe.to_parquet(
            buffer,
            index=False,
        )

        buffer.seek(0)

        self.client.put_object(
            Bucket=bucket,
            Key=key,
            Body=buffer.getvalue(),
        )

    def exists(
        self,
        bucket: str,
        key: str,
    ) -> bool:

        try:

            self.client.head_object(
                Bucket=bucket,
                Key=key,
            )

            return True

        except Exception:

            return False