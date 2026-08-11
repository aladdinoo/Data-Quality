"""
Pipeline Runner.
"""

from __future__ import annotations

from extract.factory import ReaderFactory
from profiling.profiler import DatasetProfiler
from validation.validator import Validator

from cleaning.engine import CleaningEngine

from reporting.report_generator import ReportGenerator
from reporting.cleaning_report import CleaningReport

from .config import RunnerConfig


class PipelineRunner:
    """
    Execute the complete data quality pipeline.
    """

    def __init__(
        self,
        config: RunnerConfig,
    ) -> None:

        self.config = config
        self.reader_factory = ReaderFactory()

    def run(self) -> None:

        print("=" * 60)
        print("DATA QUALITY PLATFORM")
        print("=" * 60)

        # --------------------------------------------------
        # Load Dataset
        # --------------------------------------------------

        print("\nLoading dataset...")

        reader = self.reader_factory.get_reader(
            self.config.input_file
        )

        dataframe = reader.read(
            self.config.input_file
        )

        print(f"Rows    : {len(dataframe):,}")
        print(f"Columns : {len(dataframe.columns)}")

        # --------------------------------------------------
        # Profiling
        # --------------------------------------------------

        if self.config.enable_profiling:

            print("\nProfiling...")

            profiler = DatasetProfiler()

            metrics, statistics = profiler.profile(
                dataframe
            )

            print(f"Missing Values : {metrics.missing_values}")
            print(f"Duplicate Rows : {metrics.duplicate_rows}")
            print(f"Completeness   : {metrics.completeness:.2%}")

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        validation_report = None

        if self.config.enable_validation:

            print("\nValidation...")

            validator = Validator()

            validation_report = validator.validate(
                dataframe
            )

            print(validation_report)

        # --------------------------------------------------
        # Cleaning
        # --------------------------------------------------

        print("\nCleaning...")

        cleaning_engine = CleaningEngine()

        (
            cleaned_dataframe,
            cleaning_results,
            audit_records,
        ) = cleaning_engine.clean(
            dataframe
        )

        print("Cleaning completed.")

        print(f"Audit Records : {len(audit_records)}")

        # --------------------------------------------------
        # Save Outputs
        # --------------------------------------------------

        self.config.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        cleaned_dataframe.to_csv(
            self.config.output_directory / "cleaned_data.csv",
            index=False,
        )

        # --------------------------------------------------
        # Reports
        # --------------------------------------------------

        print("\nGenerating reports...")

        if validation_report is not None:

            generator = ReportGenerator(
                self.config.output_directory
            )

            generator.generate(
                validation_report
            )

        CleaningReport().generate(
            cleaning_results,
            self.config.output_directory / "cleaning_report.txt",
        )

        print(
            f"Reports saved to: "
            f"{self.config.output_directory.resolve()}"
        )

        print("\nPipeline completed successfully.")