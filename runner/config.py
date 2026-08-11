"""
Runner Configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RunnerConfig:
    """
    Pipeline execution configuration.
    """

    # --------------------------------------------------
    # Input / Output
    # --------------------------------------------------

    input_file: Path

    output_directory: Path

    # --------------------------------------------------
    # Pipeline Stages
    # --------------------------------------------------

    enable_profiling: bool = True

    enable_validation: bool = True

    enable_cleaning: bool = True

    # --------------------------------------------------
    # Reports
    # --------------------------------------------------

    save_profile_report: bool = True

    save_validation_report: bool = True

    save_cleaning_report: bool = True

    save_cleaned_data: bool = True

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    verbose: bool = True