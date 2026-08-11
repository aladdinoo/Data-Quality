"""
Data Profiling Framework.

This package provides dataset profiling capabilities.

The profiling layer computes descriptive statistics,
quality metrics, distributions, completeness, uniqueness,
and other characteristics before validation or cleaning.

Modules
-------
- DatasetProfiler
- ProfilingMetrics
- DatasetStatistics
"""

from .metrics import ProfilingMetrics
from .profiler import DatasetProfiler
from .statistics import DatasetStatistics

__all__ = [
    "DatasetProfiler",
    "ProfilingMetrics",
    "DatasetStatistics",
]