import pandas as pd

from rules.result import RuleResult
from validation.flag_mapper import ValidationFlagMapper


def test_validation_flags_are_uint8():
    dataframe = pd.DataFrame(
        {
            "email": [
                "good@example.com",
                "bad",
                "ok@example.com",
            ]
        }
    )

    result = RuleResult(
        rule="email_validation",
        version="2.0.0",
    )

    result.add_failure(
        row=1,
        column="email",
        value="bad",
        message="Invalid email address.",
    )

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    assert "email_syntax_failure" in flags

    # Canonical project contract:
    # quality flags use pandas nullable UInt8.
    assert str(
        flags["email_syntax_failure"].dtype
    ) == "UInt8"


def test_validation_flag_marks_failed_row():
    dataframe = pd.DataFrame(
        {
            "email": [
                "good@example.com",
                "bad",
                "ok@example.com",
            ]
        }
    )

    result = RuleResult(
        rule="email_validation",
        version="2.0.0",
    )

    result.add_failure(
        row=1,
        column="email",
        value="bad",
        message="Invalid email address.",
    )

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    assert (
        flags["email_syntax_failure"].tolist()
        == [0, 1, 0]
    )


def test_blank_email_is_flagged():
    dataframe = pd.DataFrame(
        {
            "email": [
                "good@example.com",
                "",
                None,
            ]
        }
    )

    flags = ValidationFlagMapper().build_flags(
        dataframe,
        [],
    )

    assert (
        flags["email_blank"].tolist()
        == [0, 1, 1]
    )


def test_source_dataframe_is_not_modified():
    dataframe = pd.DataFrame(
        {
            "email": [
                "GOOD@EXAMPLE.COM",
                "bad",
            ]
        }
    )

    original = dataframe.copy(deep=True)

    result = RuleResult(
        rule="email_validation",
        version="2.0.0",
    )

    result.add_failure(
        row=1,
        column="email",
        value="bad",
        message="Invalid email address.",
    )

    ValidationFlagMapper().build_flags(
        dataframe,
        [result],
    )

    pd.testing.assert_frame_equal(
        dataframe,
        original,
    )