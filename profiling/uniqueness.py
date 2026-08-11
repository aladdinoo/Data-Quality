"""
Uniqueness Analyzer.

Measures uniqueness of dataset values.
"""

from __future__ import annotations

import pandas as pd


class UniquenessAnalyzer:
    """
    Analyze uniqueness metrics.
    """

    def dataset_score(
        self,
        dataframe: pd.DataFrame,
    ) -> float:

        if dataframe.empty:
            return 0.0

        duplicate_rows = dataframe.duplicated().sum()

        unique_rows = len(dataframe) - duplicate_rows

        return round(
            unique_rows / len(dataframe) * 100,
            2,
        )

    def column_scores(
        self,
        dataframe: pd.DataFrame,
    ) -> dict[str, float]:

        scores: dict[str, float] = {}

        rows = len(dataframe)

        if rows == 0:
            return scores

        for column in dataframe.columns:

            unique = dataframe[column].nunique(
                dropna=True
            )

            scores[column] = round(
                unique / rows * 100,
                2,
            )

        return scores