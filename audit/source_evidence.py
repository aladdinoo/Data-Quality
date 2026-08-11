"""
Source evidence helpers.

Provides read-only evidence capture for local CSV source files.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True, slots=True)
class SourceEvidence:
    """
    Immutable evidence captured from a source file.
    """

    source_file: Path
    row_count: int
    column_count: int
    columns: tuple[str, ...]


class SourceEvidenceReader:
    """
    Read source data without modifying the source file.
    """

    @staticmethod
    def read_csv(
        source_file: Path,
    ) -> SourceEvidence:
        """
        Read a CSV file in read-only mode and capture
        deterministic structural evidence.
        """

        source_file = Path(source_file)

        if not source_file.exists():
            raise FileNotFoundError(
                f"Source file does not exist: {source_file}"
            )

        if not source_file.is_file():
            raise ValueError(
                f"Source path is not a file: {source_file}"
            )

        dataframe = pd.read_csv(source_file)

        return SourceEvidence(
            source_file=source_file,
            row_count=len(dataframe),
            column_count=len(dataframe.columns),
            columns=tuple(
                str(column)
                for column in dataframe.columns
            ),
        )