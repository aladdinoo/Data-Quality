"""
Flag Preview output schema.

Contract:
33 source passthrough columns + 8 quality flags = 41 columns.
"""

from __future__ import annotations

from .flags import QUALITY_FLAGS


SOURCE_COLUMNS = (
    "id",
    "email_address",
    "first_name",
    "last_name",
    "address",
    "city",
    "county_name",
    "state",
    "zip",
    "website_source",
    "phone_number",
    "gender",
    "dob",
    "registration_date",
    "valid",
    "extra",
    "email_id",
    "ethnicity",
    "ownrent",
    "domain",
    "main_interest",
    "sub_interest",
    "latitude",
    "longitude",
    "uploaded",
    "country",
    "websource_id",
    "interest_ids",
    "DNC",
    "source",
    "first_name_norm",
    "last_name_norm",
    "zip_norm",
)


FLAG_COLUMNS = QUALITY_FLAGS


FLAG_PREVIEW_COLUMNS = SOURCE_COLUMNS + FLAG_COLUMNS


EXPECTED_SOURCE_COLUMN_COUNT = 33
EXPECTED_FLAG_COLUMN_COUNT = 8
EXPECTED_TOTAL_COLUMN_COUNT = 41


def validate_schema_columns(columns: list[str] | tuple[str, ...]) -> None:
    """
    Validate that the produced Flag Preview has the canonical 41-column shape.
    """

    actual = tuple(columns)

    if len(actual) != EXPECTED_TOTAL_COLUMN_COUNT:
        raise ValueError(
            "Flag Preview must contain exactly "
            f"{EXPECTED_TOTAL_COLUMN_COUNT} columns; "
            f"received {len(actual)}."
        )

    if actual != FLAG_PREVIEW_COLUMNS:
        raise ValueError(
            "Flag Preview columns do not match the canonical contract."
        )