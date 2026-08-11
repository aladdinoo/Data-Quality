"""
Schema registry.

This module defines the registry of supported logical
column types.

Each schema definition contains:

- Column type
- Known aliases
- Regular expression (optional)
- Description

The registry acts as the single source of truth for
schema detection, inference, validation, and cleaning.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

from dataclasses import dataclass, field
import re
from typing import Pattern

# ==================================================
# Local Imports
# ==================================================

from .models import ColumnType

# ==================================================
# Schema Definition
# ==================================================


@dataclass(slots=True, frozen=True)
class SchemaDefinition:
    """
    Definition of a logical column type.
    """

    column_type: ColumnType

    aliases: frozenset[str]

    description: str

    pattern: Pattern[str] | None = None


# ==================================================
# Registry
# ==================================================


class SchemaRegistry:
    """
    Registry containing all supported logical
    column definitions.
    """

    def __init__(self) -> None:

        self._definitions: dict[
            ColumnType,
            SchemaDefinition,
        ] = {}

        self._register_defaults()

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        definition: SchemaDefinition,
    ) -> None:

        self._definitions[
            definition.column_type
        ] = definition

    # --------------------------------------------------

    def get(
        self,
        column_type: ColumnType,
    ) -> SchemaDefinition | None:

        return self._definitions.get(
            column_type
        )

    # --------------------------------------------------

    def find_by_alias(
        self,
        column_name: str,
    ) -> ColumnType:

        normalized = (
            column_name
            .strip()
            .lower()
        )

        for definition in self._definitions.values():

            if normalized in definition.aliases:

                return definition.column_type

        return ColumnType.UNKNOWN

    # --------------------------------------------------

    def definitions(
        self,
    ) -> tuple[SchemaDefinition, ...]:

        return tuple(
            self._definitions.values()
        )

    # --------------------------------------------------
    # Default Definitions
    # --------------------------------------------------

    def _register_defaults(
        self,
    ) -> None:

        self.register(

            SchemaDefinition(

                column_type=ColumnType.EMAIL,

                aliases=frozenset({

                    "email",
                    "email_address",
                    "primary_email",
                    "work_email",

                }),

                description="Email address",

                pattern=re.compile(

                    r"^[A-Za-z0-9._%+-]+@"

                ),

            )

        )

        self.register(

            SchemaDefinition(

                column_type=ColumnType.PHONE,

                aliases=frozenset({

                    "phone",
                    "telephone",
                    "mobile",
                    "cell",

                }),

                description="Phone number",

            )

        )

        self.register(

            SchemaDefinition(

                column_type=ColumnType.WEBSITE,

                aliases=frozenset({

                    "website",
                    "url",
                    "domain",

                }),

                description="Website URL",

            )

        )

        self.register(

            SchemaDefinition(

                column_type=ColumnType.DATE,

                aliases=frozenset({

                    "date",
                    "created_at",
                    "updated_at",
                    "dob",

                }),

                description="Date",

            )

        )