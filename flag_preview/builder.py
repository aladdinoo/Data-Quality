"""
Flag Preview builder.

Builds the canonical Flag Preview output without modifying
source values.
"""

from __future__ import annotations

import pandas as pd

from .flags import QUALITY_FLAGS
from .schema import (
    FLAG_PREVIEW_COLUMNS,
    SOURCE_COLUMNS,
    validate_schema_columns,
)


class FlagPreviewBuilder:
    """
    Build the canonical Flag Preview dataframe.

    Contract:
    - Source columns pass through unchanged.
    - Eight UInt8 quality flags are added.
    - No source value is modified.
    - No source row is deleted.
    """

    def build(
        self,
        dataframe: pd.DataFrame,
        flags: dict[str, pd.Series] | None = None,
    ) -> pd.DataFrame:
        """
        Build a Flag Preview dataframe.

        Parameters
        ----------
        dataframe:
            Original source dataframe.

        flags:
            Optional mapping of canonical flag names to pandas Series.

        Returns
        -------
        pd.DataFrame
            41-column Flag Preview.
        """

        if dataframe is None:
            raise ValueError("Source dataframe cannot be None.")

        missing_columns = [
            column
            for column in SOURCE_COLUMNS
            if column not in dataframe.columns
        ]

        if missing_columns:
            raise ValueError(
                "Source dataframe is missing required columns: "
                + ", ".join(missing_columns)
            )

        # Copy only the source columns.
        # The original dataframe is never modified.
        preview = dataframe.loc[:, SOURCE_COLUMNS].copy()

        flags = flags or {}

        for flag_name in QUALITY_FLAGS:

            if flag_name in flags:

                series = flags[flag_name]

                if len(series) != len(preview):
                    raise ValueError(
                        f"Flag '{flag_name}' length does not match "
                        "the source dataframe."
                    )

                preview[flag_name] = (
                    series
                    .fillna(0)
                    .astype("UInt8")
                )

            else:
                # Until the corresponding canonical rule is implemented,
                # the flag is initialized to zero.
                preview[flag_name] = pd.Series(
                    0,
                    index=preview.index,
                    dtype="UInt8",
                )

        # Final contract check.
        validate_schema_columns(
            tuple(preview.columns)
        )

        return preview