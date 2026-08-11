"""
Pipeline Runner.

Executes the complete data quality pipeline while preserving
the original source dataframe and producing the canonical
Flag Preview output.
"""

from __future__ import annotations

from extract.factory import ReaderFactory
from profiling.profiler import DatasetProfiler
from validation.validator import Validator

from flag_preview.builder import FlagPreviewBuilder
from validation.flag_mapper import ValidationFlagMapper

from cleaning.engine import CleaningEngine

from reporting.report_generator import ReportGenerator
from reporting.cleaning_report import CleaningReport

from audit.audit_exporter import AuditExporter

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

            print(
                f"Missing Values : "
                f"{metrics.missing_values}"
            )

            print(
                f"Duplicate Rows : "
                f"{metrics.duplicate_rows}"
            )

            print(
                f"Completeness   : "
                f"{metrics.completeness:.2%}"
            )

        # --------------------------------------------------
        # Validation
        # --------------------------------------------------

        validation_result = None
        flag_preview = None

        if self.config.enable_validation:

            print("\nValidation...")

            validator = Validator()

            validation_result = validator.validate(
                dataframe
            )

            print(validation_result)

            # --------------------------------------------------
            # Flag Preview
            # --------------------------------------------------
            #
            # Validation NEVER modifies the source dataframe.
            # PipelineResult.rule_results contains the canonical
            # RuleResult objects produced by the validator.
            #

            print("\nBuilding Flag Preview...")

            flag_mapper = ValidationFlagMapper()

            flags = flag_mapper.build_flags(
                dataframe,
                validation_result.rule_results,
            )

            flag_preview = FlagPreviewBuilder().build(
                dataframe,
                flags,
            )

            print(
                f"Flag Preview Rows    : "
                f"{len(flag_preview):,}"
            )

            print(
                f"Flag Preview Columns : "
                f"{len(flag_preview.columns)}"
            )

        # --------------------------------------------------
        # Cleaning
        # --------------------------------------------------

        cleaning_results = None
        audit_records = []

        if self.config.enable_cleaning:

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

            print(
                f"Audit Records : "
                f"{len(audit_records)}"
            )

        else:

            cleaned_dataframe = dataframe.copy(
                deep=True
            )

        # --------------------------------------------------
        # Output Directory
        # --------------------------------------------------

        self.config.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # --------------------------------------------------
        # Save Flag Preview
        # --------------------------------------------------

        if flag_preview is not None:

            flag_preview.to_csv(
                self.config.output_directory
                / "flag_preview.csv",
                index=False,
            )

            print(
                "Flag Preview saved to: "
                f"{self.config.output_directory / 'flag_preview.csv'}"
            )

        # --------------------------------------------------
        # Save Cleaned Data
        # --------------------------------------------------

        if (
            self.config.enable_cleaning
            and self.config.save_cleaned_data
        ):

            cleaned_dataframe.to_csv(
                self.config.output_directory
                / "cleaned_data.csv",
                index=False,
            )

        # --------------------------------------------------
        # Reports
        # --------------------------------------------------

        print("\nGenerating reports...")

        if (
            validation_result is not None
            and self.config.save_validation_report
        ):

            generator = ReportGenerator(
                self.config.output_directory
            )

            generator.generate(
                validation_result
            )

        if (
            cleaning_results is not None
            and self.config.save_cleaning_report
        ):

            CleaningReport().generate(
                cleaning_results,
                self.config.output_directory
                / "cleaning_report.txt",
            )

        if audit_records:

            AuditExporter().export_csv(
                audit_records,
                self.config.output_directory
                / "audit_log.csv",
            )

        print(
            f"Reports saved to: "
            f"{self.config.output_directory.resolve()}"
        )

        print(
            "\nPipeline completed successfully."
        )