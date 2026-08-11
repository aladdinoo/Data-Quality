"""
Cleaning Rules Package.
"""

from .base import CleaningRule

from .email_cleaner import EmailCleaner
from .name_cleaner import NameCleaner
from .phone_cleaner import PhoneCleaner
from .website_cleaner import WebsiteCleaner


__all__ = [

    "CleaningRule",

    "EmailCleaner",
    "NameCleaner",
    "PhoneCleaner",
    "WebsiteCleaner",

]