"""
Pipeline Runner.

Entry point for executing
the Data Quality Platform.
"""

from .config import RunnerConfig
from .pipeline_runner import PipelineRunner

__all__ = [
    "RunnerConfig",
    "PipelineRunner",
]