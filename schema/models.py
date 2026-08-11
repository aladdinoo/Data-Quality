"""
Schema models.

This module defines the schema objects used throughout
the Data Quality Platform.

A detected dataset schema consists of:

DatasetSchema
    ├── ColumnSchema
    ├── ColumnSchema
    ├── ColumnSchema
    └── ...

Every component of the platform relies on these models
instead of working directly with pandas columns.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field
from enum import Enum

# ==================================================
# Column Type
# ==================================================


class ColumnType(str, Enum):
    """
    Supported logical column types.
    """

    UNKNOWN = "unknown"

    ID = "id"

    NAME = "name"

    FIRST_NAME = "first_name"

    LAST_NAME = "last_name"

    FULL_NAME = "full_name"

    EMAIL = "email"

    PHONE = "phone"

    WEBSITE = "website"

    ADDRESS = "address"

    CITY = "city"

    STATE = "state"

    COUNTRY = "country"

    ZIP_CODE = "zip_code"

    DATE = "date"

    DATETIME = "datetime"

    LATITUDE = "latitude"

    LONGITUDE = "longitude"

    COMPANY = "company"

    BOOLEAN = "boolean"

    INTEGER = "integer"

    FLOAT = "float"

    TEXT = "text"


# ==================================================
# Column Schema
# ==================================================


@dataclass(slots=True)
class ColumnSchema:
    """
    Logical description of a dataset column.
    """

    name: str

    column_type: ColumnType

    pandas_dtype: str

    nullable: bool = True

    unique: bool = False

    inferred: bool = False

    confidence: float = 1.0


# ==================================================
# Dataset Schema
# ==================================================


@dataclass(slots=True)
class DatasetSchema:
    """
    Logical dataset schema.
    """

    columns: list[ColumnSchema] = field(
        default_factory=list
    )

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def add(
        self,
        column: ColumnSchema,
    ) -> None:
        """
        Add a detected column.
        """

        self.columns.append(column)

    # --------------------------------------------------

    def find(
        self,
        column_type: ColumnType,
    ) -> ColumnSchema | None:
        """
        Find the first column of a given type.
        """

        for column in self.columns:

            if column.column_type == column_type:

                return column

        return None

    # --------------------------------------------------

    def find_all(
        self,
        column_type: ColumnType,
    ) -> list[ColumnSchema]:
        """
        Return all matching columns.
        """

        return [

            column

            for column in self.columns

            if column.column_type == column_type

        ]

    # --------------------------------------------------

    @property
    def emails(
        self,
    ) -> list[ColumnSchema]:

        return self.find_all(
            ColumnType.EMAIL
        )

    @property
    def phones(
        self,
    ) -> list[ColumnSchema]:

        return self.find_all(
            ColumnType.PHONE
        )

    @property
    def dates(
        self,
    ) -> list[ColumnSchema]:

        return self.find_all(
            ColumnType.DATE
        )

    @property
    def websites(
        self,
    ) -> list[ColumnSchema]:

        return self.find_all(
            ColumnType.WEBSITE
        )

    # --------------------------------------------------

    def __len__(
        self,
    ) -> int:

        return len(
            self.columns
        )

    def __iter__(
        self,
    ):

        return iter(
            self.columns
        )