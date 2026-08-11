"""
Map validation results to the canonical Flag Preview contract.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


class ValidationFlagMapper:
    """
    Convert validation results and source-data conditions
    into the canonical Flag Preview flags.

    Contract:
    - Source dataframe is never modified.
    - Only the canonical 8 Flag Preview flags are produced.
    - Flags are UInt8 values in {0, 1}.
    """

    CANONICAL_FLAGS = (
        "first_name_cleaning_candidate",
        "last_name_cleaning_candidate",
        "name_cleaning_candidate",
        "email_blank",
        "email_syntax_failure",
        "proposed_email_export_eligible",
        "zip_state_assessable",
        "geography_mismatch_candidate",
    )

    def build_flags(
        self,
        dataframe: pd.DataFrame,
        rule_results: Iterable,
    ) -> dict[str, pd.Series]:
        """
        Build canonical Flag Preview flags.

        The source dataframe is never modified.
        """

        if dataframe is None:
            raise ValueError("dataframe cannot be None.")

        index = dataframe.index

        # ---------------------------------------------------------
        # Initialize exactly the 8 canonical flags
        # ---------------------------------------------------------

        flags: dict[str, pd.Series] = {
            flag_name: pd.Series(
                0,
                index=index,
                dtype="UInt8",
            )
            for flag_name in self.CANONICAL_FLAGS
        }

        # ---------------------------------------------------------
        # Email blank
        # ---------------------------------------------------------

        email_column = None

        if "email_address" in dataframe.columns:
            email_column = "email_address"

        elif "email" in dataframe.columns:
            # Backward compatibility with the test/sample dataset.
            email_column = "email"

        if email_column is not None:

            email = dataframe[email_column]

            flags["email_blank"] = (
                (
                    email.isna()
                    | email.astype("string").str.strip().eq("")
                )
                .astype("UInt8")
            )

        # ---------------------------------------------------------
        # Validation rule results
        # ---------------------------------------------------------

        for rule_result in rule_results:

            rule_name = getattr(
                rule_result,
                "rule",
                "",
            )

            failures = getattr(
                rule_result,
                "failures",
                [],
            )

            # =====================================================
            # NAME VALIDATION
            # =====================================================

            if rule_name == "name_validation":

                for failure in failures:

                    row = failure.get("row")
                    column = failure.get("column")

                    if row not in index:
                        continue

                    if column == "first_name":

                        flags[
                            "first_name_cleaning_candidate"
                        ].loc[row] = 1

                    elif column == "last_name":

                        flags[
                            "last_name_cleaning_candidate"
                        ].loc[row] = 1

            # =====================================================
            # EMAIL VALIDATION
            # =====================================================

            elif rule_name == "email_validation":

                for failure in failures:

                    row = failure.get("row")

                    if row in index:
                        flags[
                            "email_syntax_failure"
                        ].loc[row] = 1

            # =====================================================
            # ZIP / STATE ASSESSMENT
            # =====================================================
            #
            # IMPORTANT:
            #
            # We do NOT interpret a generic zip_validation failure
            # as geography_mismatch_candidate.
            #
            # Geography mismatch is meaningful only when the row
            # was actually assessable against ZIP/state reference
            # data.
            #
            # Therefore this mapper supports explicit metadata from
            # the validation result when available.
            # =====================================================

            elif rule_name in {
                "zip_state_validation",
                "geography_validation",
                "zip_validation",
            }:

                for failure in failures:

                    row = failure.get("row")

                    if row not in index:
                        continue

                    # If the rule explicitly says that this row was
                    # assessed, mark it as assessable.
                    assessable = failure.get(
                        "assessable",
                        failure.get(
                            "zip_state_assessable",
                            False,
                        ),
                    )

                    mismatch = failure.get(
                        "geography_mismatch",
                        failure.get(
                            "mismatch",
                            False,
                        ),
                    )

                    if assessable:
                        flags[
                            "zip_state_assessable"
                        ].loc[row] = 1

                    # A mismatch is only valid when assessable = 1.
                    if assessable and mismatch:
                        flags[
                            "geography_mismatch_candidate"
                        ].loc[row] = 1

        # ---------------------------------------------------------
        # Name union
        # ---------------------------------------------------------
        #
        # name_cleaning_candidate is the union of the two
        # finer-grained name candidates.
        # ---------------------------------------------------------

        flags["name_cleaning_candidate"] = (
            (
                (flags["first_name_cleaning_candidate"] == 1)
                | (flags["last_name_cleaning_candidate"] == 1)
            )
            .astype("UInt8")
        )

        # ---------------------------------------------------------
        # Email export eligibility
        # ---------------------------------------------------------
        #
        # Proposal only.
        #
        # Nothing is deleted, blanked, suppressed, or modified.
        #
        # Eligible iff:
        #   email_blank == 0
        #   email_syntax_failure == 0
        # ---------------------------------------------------------

        flags["proposed_email_export_eligible"] = (
            (
                (flags["email_blank"] == 0)
                & (flags["email_syntax_failure"] == 0)
            )
            .astype("UInt8")
        )

        # ---------------------------------------------------------
        # Final safety normalization
        # ---------------------------------------------------------

        for flag_name in self.CANONICAL_FLAGS:

            flags[flag_name] = (
                flags[flag_name]
                .fillna(0)
                .astype("UInt8")
            )

        return flags