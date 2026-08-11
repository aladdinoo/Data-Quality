"""
Canonical flag names for the Flag Preview contract.
"""

from __future__ import annotations

FIRST_NAME_CLEANING_CANDIDATE = "first_name_cleaning_candidate"
LAST_NAME_CLEANING_CANDIDATE = "last_name_cleaning_candidate"
NAME_CLEANING_CANDIDATE = "name_cleaning_candidate"

EMAIL_BLANK = "email_blank"
EMAIL_SYNTAX_FAILURE = "email_syntax_failure"
PROPOSED_EMAIL_EXPORT_ELIGIBLE = "proposed_email_export_eligible"

ZIP_STATE_ASSESSABLE = "zip_state_assessable"
GEOGRAPHY_MISMATCH_CANDIDATE = "geography_mismatch_candidate"


QUALITY_FLAGS = (
    FIRST_NAME_CLEANING_CANDIDATE,
    LAST_NAME_CLEANING_CANDIDATE,
    NAME_CLEANING_CANDIDATE,
    EMAIL_BLANK,
    EMAIL_SYNTAX_FAILURE,
    PROPOSED_EMAIL_EXPORT_ELIGIBLE,
    ZIP_STATE_ASSESSABLE,
    GEOGRAPHY_MISMATCH_CANDIDATE,
)