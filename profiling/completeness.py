"""
Completeness Analyzer.

Computes completeness metrics for datasets
and individual columns.
"""

from __future__ import annotations

import pandas as pd


class CompletenessAnalyzer:
    """
    Analyze dataset completeness.
    """

    def dataset_score(
        self,
        dataframe: pd.DataFrame,
    ) -> float:

        if dataframe.empty:
            return 0.0

        total = dataframe.shape[0] * dataframe.shape[1]

        missing = dataframe.isna().sum().sum()

        return round(
            (1 - missing / total) * 100,
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

            missing = dataframe[column].isna().sum()

            scores[column] = round(
                (1 - missing / rows) * 100,
                2,
            )

        return scores