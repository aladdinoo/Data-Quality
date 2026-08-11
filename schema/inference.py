"""
Schema inference.

This module infers the logical type of dataset columns
based on their values when the column name alone is
insufficient.

Inference is heuristic-based and returns a detected
ColumnType together with a confidence score.
"""

from __future__ import annotations

# ==================================================
# Standard Library
# ==================================================

import re
from collections import Counter

# ==================================================
# Third-Party Libraries
# ==================================================

import pandas as pd

# ==================================================
# Local Imports
# ==================================================

from .models import ColumnType

# ==================================================
# Regular Expressions
# ==================================================

EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)

PHONE_PATTERN = re.compile(
    r"^\+?[0-9()\-\s]{7,20}$"
)

WEBSITE_PATTERN = re.compile(
    r"^(https?://|www\.)",
    re.IGNORECASE,
)

DATE_PATTERN = re.compile(
    r"^\d{4}[-/]\d{2}[-/]\d{2}$"
)

# ==================================================
# Inference Engine
# ==================================================


class InferenceEngine:
    """
    Infer logical column types from sample values.
    """

    def infer(
        self,
        series: pd.Series,
        sample_size: int = 100,
    ) -> tuple[ColumnType, float]:
        """
        Infer the logical type of a column.

        Parameters
        ----------
        series
            Input pandas Series.

        sample_size
            Maximum number of non-null values
            inspected.

        Returns
        -------
        tuple[ColumnType, float]
            Detected type and confidence.
        """

        sample = (

            series

            .dropna()

            .astype(str)

            .head(sample_size)

        )

        if sample.empty:

            return (
                ColumnType.UNKNOWN,
                0.0,
            )

        counter: Counter[ColumnType] = Counter()

        for value in sample:

            value = value.strip()

            if EMAIL_PATTERN.match(value):

                counter[ColumnType.EMAIL] += 1

                continue

            if WEBSITE_PATTERN.match(value):

                counter[ColumnType.WEBSITE] += 1

                continue

            if PHONE_PATTERN.match(value):

                counter[ColumnType.PHONE] += 1

                continue

            if DATE_PATTERN.match(value):

                counter[ColumnType.DATE] += 1

        if not counter:

            return (
                ColumnType.UNKNOWN,
                0.0,
            )

        detected, matches = counter.most_common(1)[0]

        confidence = matches / len(sample)

        return (
            detected,
            confidence,
        )