import pandas as pd
import pytest

from flag_preview.builder import FlagPreviewBuilder
from validation.flag_mapper import ValidationFlagMapper
from rules.result import RuleResult


SOURCE_COLUMNS = [
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
]


EXPECTED_FLAG_COLUMNS = [
    "first_name_cleaning_candidate",
    "last_name_cleaning_candidate",
    "name_cleaning_candidate",
    "email_blank",
    "email_syntax_failure",
    "proposed_email_export_eligible",
    "zip_state_assessable",
    "geography_mismatch_candidate",
]


EXPECTED_COLUMNS = SOURCE_COLUMNS + EXPECTED_FLAG_COLUMNS


def make_source_dataframe() -> pd.DataFrame:
    """
    Build a minimal dataframe matching the canonical
    33-column Flag Preview source contract.
    """

    return pd.DataFrame(
        {
            column: [
                f"{column}_1",
                f"{column}_2",
            ]
            for column in SOURCE_COLUMNS
        }
    )


def make_email_validation_result() -> RuleResult:
    """
    Create one invalid-email validation result.
    """

    result = RuleResult(
        rule="email_validation",
        version="2.0.0",
    )

    result.add_failure(
        row=1,
        column="email_address",
        value="bad",
        message="Invalid email address.",
    )

    return result


def build_preview() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Build a Flag Preview from source data and validation results.
    """

    dataframe = make_source_dataframe()

    dataframe.loc[0, "email_address"] = "good@example.com"
    dataframe.loc[1, "email_address"] = "bad"

    result = make_email_validation_result()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    return dataframe, preview


def test_validation_results_become_flag_preview_flags():
    """
    Validation results must be converted into the
    canonical Flag Preview flags.
    """

    dataframe, preview = build_preview()

    assert len(preview) == len(dataframe)

    assert preview.loc[
        0,
        "email_syntax_failure",
    ] == 0

    assert preview.loc[
        1,
        "email_syntax_failure",
    ] == 1

    assert preview.loc[
        0,
        "email_blank",
    ] == 0

    assert preview.loc[
        1,
        "email_blank",
    ] == 0

    assert preview.loc[
        0,
        "proposed_email_export_eligible",
    ] == 1

    assert preview.loc[
        1,
        "proposed_email_export_eligible",
    ] == 0


def test_validation_flag_does_not_modify_source():
    """
    Building flags and Flag Preview must never modify
    the original source dataframe.
    """

    dataframe = make_source_dataframe()

    dataframe.loc[
        0,
        "email_address",
    ] = "good@example.com"

    dataframe.loc[
        1,
        "email_address",
    ] = "bad"

    original = dataframe.copy(deep=True)

    result = make_email_validation_result()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )


def test_flag_preview_has_canonical_columns():
    """
    Flag Preview must contain exactly the canonical
    41 columns in the canonical order.
    """

    _, preview = build_preview()

    assert len(preview.columns) == 41

    assert preview.columns.tolist() == EXPECTED_COLUMNS


def test_flag_preview_has_33_source_columns():
    """
    The first 33 columns must be the original source
    columns in exactly the original order.
    """

    _, preview = build_preview()

    actual_source_columns = preview.columns[:33].tolist()

    assert actual_source_columns == SOURCE_COLUMNS


def test_flag_preview_has_8_quality_flags():
    """
    The last 8 columns must be the canonical quality flags.
    """

    _, preview = build_preview()

    actual_flag_columns = preview.columns[33:].tolist()

    assert actual_flag_columns == EXPECTED_FLAG_COLUMNS


def test_all_flags_are_uint8():
    """
    All eight quality flags must be non-nullable UInt8
    values in the domain {0, 1}.
    """

    _, preview = build_preview()

    for column in EXPECTED_FLAG_COLUMNS:

        assert str(preview[column].dtype) == "UInt8"

        values = set(
            preview[column]
            .dropna()
            .tolist()
        )

        assert values.issubset({0, 1})


def test_flags_are_non_nullable():
    """
    Quality flags must never contain null values.
    """

    _, preview = build_preview()

    for column in EXPECTED_FLAG_COLUMNS:
        assert preview[column].isna().sum() == 0


def test_unrelated_flags_remain_zero():
    """
    An email validation failure must not accidentally
    activate unrelated Flag Preview flags.
    """

    _, preview = build_preview()

    assert (
        preview["email_syntax_failure"].tolist()
        == [0, 1]
    )

    assert (
        preview["email_blank"].tolist()
        == [0, 0]
    )

    assert (
        preview["proposed_email_export_eligible"].tolist()
        == [1, 0]
    )

    assert (
        preview[
            "first_name_cleaning_candidate"
        ].tolist()
        == [0, 0]
    )

    assert (
        preview[
            "last_name_cleaning_candidate"
        ].tolist()
        == [0, 0]
    )

    assert (
        preview[
            "name_cleaning_candidate"
        ].tolist()
        == [0, 0]
    )

    assert (
        preview[
            "zip_state_assessable"
        ].tolist()
        == [0, 0]
    )

    assert (
        preview[
            "geography_mismatch_candidate"
        ].tolist()
        == [0, 0]
    )


def test_email_blank_is_detected():
    """
    Blank, None, NaN and whitespace-only emails
    must produce email_blank = 1.
    """

    dataframe = make_source_dataframe()

    dataframe.loc[0, "email_address"] = ""
    dataframe.loc[1, "email_address"] = "   "

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [],
    )

    assert (
        flags["email_blank"].tolist()
        == [1, 1]
    )


def test_blank_email_is_not_export_eligible():
    """
    Blank emails must not be proposed as export eligible.
    """

    dataframe = make_source_dataframe()

    dataframe.loc[0, "email_address"] = ""
    dataframe.loc[1, "email_address"] = "   "

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [],
    )

    assert (
        flags[
            "proposed_email_export_eligible"
        ].tolist()
        == [0, 0]
    )


def test_invalid_email_is_not_export_eligible():
    """
    A syntactically invalid email must not be proposed
    as export eligible.
    """

    dataframe = make_source_dataframe()

    dataframe.loc[
        0,
        "email_address",
    ] = "good@example.com"

    dataframe.loc[
        1,
        "email_address",
    ] = "bad"

    result = make_email_validation_result()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    assert (
        flags[
            "proposed_email_export_eligible"
        ].tolist()
        == [1, 0]
    )


def test_source_values_are_passed_through_unchanged():
    """
    Every source column and value must pass through
    Flag Preview unchanged.
    """

    dataframe = make_source_dataframe()

    dataframe.loc[
        0,
        "first_name",
    ] = "12345"

    dataframe.loc[
        0,
        "email_address",
    ] = "bad"

    original = dataframe[
        SOURCE_COLUMNS
    ].copy(deep=True)

    result = make_email_validation_result()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    pd.testing.assert_frame_equal(
        preview[SOURCE_COLUMNS],
        original,
    )


def test_source_row_count_is_preserved():
    """
    Flag Preview must contain exactly the same number
    of rows as the source dataframe.
    """

    dataframe = make_source_dataframe()

    result = make_email_validation_result()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    assert len(preview) == len(dataframe)


def test_no_rows_are_deleted():
    """
    Building Flag Preview must never delete source rows.
    """

    dataframe = make_source_dataframe()

    result = make_email_validation_result()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    assert preview.index.tolist() == dataframe.index.tolist()


def test_geography_mismatch_requires_assessable():
    """
    geography_mismatch_candidate is only meaningful when
    zip_state_assessable = 1.

    This test verifies the contract at the Flag Preview
    level: non-assessable rows remain non-mismatched.
    """

    dataframe = make_source_dataframe()

    flags = {
        "zip_state_assessable": pd.Series(
            [0, 1],
            index=dataframe.index,
            dtype="UInt8",
        ),
        "geography_mismatch_candidate": pd.Series(
            [0, 1],
            index=dataframe.index,
            dtype="UInt8",
        ),
    }

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    assert (
        preview[
            "zip_state_assessable"
        ].tolist()
        == [0, 1]
    )

    assert (
        preview[
            "geography_mismatch_candidate"
        ].tolist()
        == [0, 1]
    )


def test_missing_optional_flags_default_to_zero():
    """
    If a canonical flag is not supplied by the mapper,
    FlagPreviewBuilder must create it as UInt8 zero.
    """

    dataframe = make_source_dataframe()

    preview = FlagPreviewBuilder().build(
        dataframe,
        {},
    )

    for column in EXPECTED_FLAG_COLUMNS:

        assert (
            preview[column].tolist()
            == [0, 0]
        )

        assert (
            str(preview[column].dtype)
            == "UInt8"
        )


def test_none_source_dataframe_is_rejected():
    """
    Builder must reject None as source data.
    """

    with pytest.raises(ValueError):

        FlagPreviewBuilder().build(
            None,
            {},
        )


def test_missing_source_column_is_rejected():
    """
    Builder must reject source data that does not satisfy
    the canonical 33-column source contract.
    """

    dataframe = make_source_dataframe()

    dataframe = dataframe.drop(
        columns=["zip_norm"]
    )

    with pytest.raises(ValueError):

        FlagPreviewBuilder().build(
            dataframe,
            {},
        )