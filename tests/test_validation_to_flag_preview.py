import pandas as pd

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


def make_source_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            column: [f"{column}_1", f"{column}_2"]
            for column in SOURCE_COLUMNS
        }
    )


def test_validation_results_become_flag_preview_flags():
    dataframe = make_source_dataframe()

    dataframe.loc[0, "email_address"] = "good@example.com"
    dataframe.loc[1, "email_address"] = "bad"

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

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    assert len(preview) == len(dataframe)

    assert preview.loc[0, "email_syntax_failure"] == 0
    assert preview.loc[1, "email_syntax_failure"] == 1

    assert preview.loc[0, "email_blank"] == 0
    assert preview.loc[1, "email_blank"] == 0

    assert preview.loc[
        0,
        "proposed_email_export_eligible",
    ] == 1

    assert preview.loc[
        1,
        "proposed_email_export_eligible",
    ] == 0


def test_blank_email_is_not_export_eligible():
    dataframe = make_source_dataframe()

    dataframe.loc[0, "email_address"] = ""
    dataframe.loc[1, "email_address"] = "   "

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    assert preview["email_blank"].tolist() == [1, 1]

    assert (
        preview["proposed_email_export_eligible"].tolist()
        == [0, 0]
    )


def test_validation_flag_does_not_modify_source():
    dataframe = make_source_dataframe()
    original = dataframe.copy(deep=True)

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


def test_flag_preview_has_canonical_41_columns():
    dataframe = make_source_dataframe()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    expected_columns = (
        SOURCE_COLUMNS
        + EXPECTED_FLAG_COLUMNS
    )

    assert len(preview.columns) == 41

    assert preview.columns.tolist() == expected_columns


def test_flag_columns_are_uint8():
    dataframe = make_source_dataframe()

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    for column in EXPECTED_FLAG_COLUMNS:
        assert str(preview[column].dtype) == "UInt8"


def test_unrelated_flags_remain_zero():
    dataframe = make_source_dataframe()

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

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    preview = FlagPreviewBuilder().build(
        dataframe,
        flags,
    )

    assert preview["email_syntax_failure"].tolist() == [0, 1]

    assert preview["email_blank"].tolist() == [0, 0]

    assert (
        preview["proposed_email_export_eligible"].tolist()
        == [1, 0]
    )

    assert (
        preview["first_name_cleaning_candidate"].tolist()
        == [0, 0]
    )

    assert (
        preview["last_name_cleaning_candidate"].tolist()
        == [0, 0]
    )

    assert (
        preview["name_cleaning_candidate"].tolist()
        == [0, 0]
    )

    assert (
        preview["zip_state_assessable"].tolist()
        == [0, 0]
    )

    assert (
        preview["geography_mismatch_candidate"].tolist()
        == [0, 0]
    )