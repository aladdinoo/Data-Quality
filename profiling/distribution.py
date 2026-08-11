"""
Distribution Analyzer.

Computes value distributions
for dataset columns.
"""

from __future__ import annotations

import pandas as pd


class DistributionAnalyzer:
    """
    Analyze column distributions.
    """

    def categorical_distribution(
        self,
        dataframe: pd.DataFrame,
        column: str,
        top: int = 20,
    ) -> dict:

        if column not in dataframe.columns:
            return {}

        return (
            dataframe[column]
            .value_counts(dropna=False)
            .head(top)
            .to_dict()
        )

    def numeric_summary(
        self,
        dataframe: pd.DataFrame,
        column: str,
    ) -> dict:

        if column not in dataframe.columns:
            return {}

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            return {}

        summary = dataframe[column].describe()

        return {
            "count": float(summary["count"]),
            "mean": float(summary["mean"]),
            "std": float(summary["std"]),
            "min": float(summary["min"]),
            "25%": float(summary["25%"]),
            "50%": float(summary["50%"]),
            "75%": float(summary["75%"]),
            "max": float(summary["max"]),
        }