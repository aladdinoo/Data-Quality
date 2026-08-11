"""
Tests for the canonical Flag Preview contract.

Batch 1 tests:
- 33 source passthrough columns
- 8 canonical flags
- 41 total columns
- source values remain unchanged
- flags are UInt8
- flags contain only 0/1
- missing source columns are rejected
"""

from __future__ import annotations

import pandas as pd
import pytest

from flag_preview.builder import FlagPreviewBuilder
from flag_preview.flags import QUALITY_FLAGS
from flag_preview.schema import (
    FLAG_PREVIEW_COLUMNS,
    SOURCE_COLUMNS,
)


def make_source_dataframe() -> pd.DataFrame:
    """
    Create a minimal synthetic source dataframe
    containing all 33 canonical source columns.
    """

    data = {}

    for column in SOURCE_COLUMNS:
        data[column] = [
            f"{column}_row_1",
            f"{column}_row_2",
            f"{column}_row_3",
        ]

    return pd.DataFrame(data)


def test_flag_preview_has_41_columns() -> None:
    """
    The preview must contain exactly 33 source columns + 8 flags.
    """

    source = make_source_dataframe()

    preview = FlagPreviewBuilder().build(source)

    assert len(SOURCE_COLUMNS) == 33
    assert len(QUALITY_FLAGS) == 8
    assert len(preview.columns) == 41


def test_flag_preview_column_order() -> None:
    """
    Columns must exactly match the canonical contract.
    """

    source = make_source_dataframe()

    preview = FlagPreviewBuilder().build(source)

    assert tuple(preview.columns) == FLAG_PREVIEW_COLUMNS


def test_source_values_are_unchanged() -> None:
    """
    The builder must never modify source values.
    """

    source = make_source_dataframe()

    original = source.copy(deep=True)

    preview = FlagPreviewBuilder().build(source)

    pd.testing.assert_frame_equal(
        source,
        original,
    )

    for column in SOURCE_COLUMNS:
        pd.testing.assert_series_equal(
            preview[column],
            original[column],
            check_names=True,
        )


def test_source_dataframe_is_not_modified() -> None:
    """
    Building the preview must not mutate the original dataframe.
    """

    source = make_source_dataframe()

    original_columns = list(source.columns)
    original_values = source.copy(deep=True)

    FlagPreviewBuilder().build(source)

    assert list(source.columns) == original_columns

    pd.testing.assert_frame_equal(
        source,
        original_values,
    )


def test_all_flags_are_present() -> None:
    """
    All eight canonical flags must exist.
    """

    source = make_source_dataframe()

    preview = FlagPreviewBuilder().build(source)

    for flag in QUALITY_FLAGS:
        assert flag in preview.columns


def test_flags_are_uint8() -> None:
    """
    Every quality flag must be non-nullable UInt8.
    """

    source = make_source_dataframe()

    preview = FlagPreviewBuilder().build(source)

    for flag in QUALITY_FLAGS:
        assert str(preview[flag].dtype) == "UInt8"


def test_default_flags_are_zero() -> None:
    """
    Flags without calculated values are initialized to zero.
    """

    source = make_source_dataframe()

    preview = FlagPreviewBuilder().build(source)

    for flag in QUALITY_FLAGS:
        assert preview[flag].tolist() == [0, 0, 0]


def test_flags_accept_only_zero_or_one() -> None:
    """
    Supplied flags must remain within the canonical domain {0, 1}.
    """

    source = make_source_dataframe()

    flags = {
        QUALITY_FLAGS[0]: pd.Series([0, 1, 0]),
        QUALITY_FLAGS[1]: pd.Series([1, 0, 1]),
    }

    preview = FlagPreviewBuilder().build(
        source,
        flags=flags,
    )

    for flag in QUALITY_FLAGS:
        values = set(preview[flag].tolist())

        assert values.issubset({0, 1})


def test_supplied_flags_are_preserved() -> None:
    """
    Explicitly supplied flag values must appear in the preview.
    """

    source = make_source_dataframe()

    flags = {
        QUALITY_FLAGS[0]: pd.Series([1, 0, 1]),
        QUALITY_FLAGS[3]: pd.Series([0, 1, 1]),
    }

    preview = FlagPreviewBuilder().build(
        source,
        flags=flags,
    )

    assert preview[QUALITY_FLAGS[0]].tolist() == [1, 0, 1]

    assert preview[QUALITY_FLAGS[3]].tolist() == [0, 1, 1]


def test_missing_source_column_is_rejected() -> None:
    """
    The builder must reject a dataframe that does not contain
    all 33 canonical source columns.
    """

    source = make_source_dataframe()

    source = source.drop(
        columns=[SOURCE_COLUMNS[0]]
    )

    with pytest.raises(ValueError):
        FlagPreviewBuilder().build(source)


def test_flag_length_mismatch_is_rejected() -> None:
    """
    A flag with a different number of rows must be rejected.
    """

    source = make_source_dataframe()

    flags = {
        QUALITY_FLAGS[0]: pd.Series([1, 0]),
    }

    with pytest.raises(ValueError):
        FlagPreviewBuilder().build(
            source,
            flags=flags,
        )


def test_preview_has_same_row_count_as_source() -> None:
    """
    The preview must never add or remove source rows.
    """

    source = make_source_dataframe()

    preview = FlagPreviewBuilder().build(source)

    assert len(preview) == len(source)


def test_original_index_is_preserved() -> None:
    """
    The source dataframe index must remain unchanged.
    """

    source = make_source_dataframe()

    source.index = [10, 20, 30]

    preview = FlagPreviewBuilder().build(source)

    assert preview.index.tolist() == [10, 20, 30]