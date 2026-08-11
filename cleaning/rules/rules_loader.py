"""
Cleaning Rules Loader.
"""

from __future__ import annotations

from cleaning.rules import (

    EmailCleaner,
    NameCleaner,
    PhoneCleaner,
    WebsiteCleaner,

)


class CleaningRulesLoader:
    """
    Load all cleaning rules.
    """

    def load(self):

        return [

            EmailCleaner(),
            NameCleaner(),
            PhoneCleaner(),
            WebsiteCleaner(),

        ]