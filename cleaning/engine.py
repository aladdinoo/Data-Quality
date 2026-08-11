"""
Cleaning Engine.

Execution layer responsible for running registered cleaning rules,
collecting results, and writing audit records.

The engine does not define business rules.
"""

from __future__ import annotations

import pandas as pd

from audit.audit_logger import AuditLogger
from cleaning.result import CleaningResult
from cleaning.rules.rules_loader import CleaningRulesLoader


class CleaningEngine:
    """
    Execute all registered cleaning rules.
    """

    def __init__(self) -> None:
        self.audit = AuditLogger()
        self.cleaners = CleaningRulesLoader().load()

    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> tuple[
        pd.DataFrame,
        list[CleaningResult],
        list,
    ]:

        cleaned = dataframe.copy()

        results: list[CleaningResult] = []

        for cleaner in self.cleaners:

            try:
                result = cleaner.clean(cleaned)

            except Exception as exc:

                result = CleaningResult(
                    cleaner=cleaner.name,
                    success=False,
                    message=str(exc),
                    errors=[
                        {
                            "rule": cleaner.name,
                            "error": str(exc),
                        }
                    ],
                )

            results.append(result)

            if not result.success:
                continue

            for modification in result.modifications:

                if (
                    "old" not in modification
                    or "new" not in modification
                ):
                    continue

                self.audit.log(
                    rule=cleaner.name,
                    row=modification["row"],
                    column=modification["column"],
                    old_value=modification["old"],
                    new_value=modification["new"],
                    automatic=cleaner.can_auto_apply(),
                    action="UPDATE",
                )

        return (
            cleaned,
            results,
            self.audit.records,
        )