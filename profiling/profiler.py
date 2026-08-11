"""
Dataset Profiler.
"""

from __future__ import annotations

import pandas as pd

from .metrics import ProfilingMetrics
from .statistics import DatasetStatistics


class DatasetProfiler:
    """
    Profile datasets before validation
    and cleaning.
    """

    def profile(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[
        ProfilingMetrics,
        DatasetStatistics,
    ]:

        metrics = ProfilingMetrics()

        statistics = DatasetStatistics()

        metrics.row_count = len(dataframe)

        metrics.column_count = len(
            dataframe.columns
        )

        metrics.missing_values = int(
            dataframe.isna().sum().sum()
        )

        metrics.duplicate_rows = int(
            dataframe.duplicated().sum()
        )

        metrics.memory_usage = int(
            dataframe.memory_usage(
                deep=True
            ).sum()
        )

        if metrics.row_count:

            metrics.completeness = (
                1
                - metrics.missing_values
                / (
                    metrics.row_count
                    * metrics.column_count
                )
            )

        statistics.numeric_columns = list(

            dataframe.select_dtypes(
                include="number"
            ).columns

        )

        statistics.object_columns = list(

            dataframe.select_dtypes(
                include="object"
            ).columns

        )

        statistics.datetime_columns = list(

            dataframe.select_dtypes(
                include="datetime"
            ).columns

        )

        statistics.boolean_columns = list(

            dataframe.select_dtypes(
                include="bool"
            ).columns

        )

        return (
            metrics,
            statistics,
        )