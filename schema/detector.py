"""
Schema detector.

This module automatically detects the logical schema
of a dataset based on column names.

The detector relies on the alias registry and produces
a DatasetSchema consumed by downstream components.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from typing import Final

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd

# ==================================================
# Local Imports
# ==================================================

from app.logging import LoggerFactory

from .aliases import ALIASES
from .models import (
    ColumnSchema,
    ColumnType,
    DatasetSchema,
)

# ==================================================
# Logger
# ==================================================

logger = LoggerFactory.get_logger(__name__)

# ==================================================
# Type Mapping
# ==================================================

COLUMN_TYPE_MAP: Final[dict[str, ColumnType]] = {

    "id": ColumnType.ID,

    "name": ColumnType.NAME,

    "first_name": ColumnType.FIRST_NAME,

    "last_name": ColumnType.LAST_NAME,

    "email": ColumnType.EMAIL,

    "phone": ColumnType.PHONE,

    "website": ColumnType.WEBSITE,

    "address": ColumnType.ADDRESS,

    "city": ColumnType.CITY,

    "state": ColumnType.STATE,

    "country": ColumnType.COUNTRY,

    "zip_code": ColumnType.ZIP_CODE,

    "date": ColumnType.DATE,

}

# ==================================================
# Schema Detector
# ==================================================


class SchemaDetector:
    """
    Detect the logical schema of a dataset.
    """

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def detect(
        self,
        dataframe: pd.DataFrame,
    ) -> DatasetSchema:
        """
        Detect the schema.

        Parameters
        ----------
        dataframe
            Input dataframe.

        Returns
        -------
        DatasetSchema
        """

        schema = DatasetSchema()

        for column in dataframe.columns:

            schema.add(

                self._detect_column(
                    dataframe,
                    column,
                )

            )

        logger.info(

            "Detected %d columns.",

            len(schema),

        )

        return schema

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _detect_column(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> ColumnSchema:
        """
        Detect a single column.
        """

        normalized = (

            str(column)

            .strip()

            .lower()

        )

        column_type = self._match_alias(
            normalized
        )

        series = dataframe[column]

        return ColumnSchema(

            name=column,

            column_type=column_type,

            pandas_dtype=str(
                series.dtype
            ),

            nullable=series.isna().any(),

            unique=series.is_unique,

            inferred=False,

            confidence=1.0,

        )

    # --------------------------------------------------

    def _match_alias(
        self,
        column_name: str,
    ) -> ColumnType:
        """
        Match a column name against
        the alias registry.
        """

        for logical_name, aliases in ALIASES.items():

            if column_name in aliases:

                return COLUMN_TYPE_MAP[
                    logical_name
                ]

        return ColumnType.UNKNOWN