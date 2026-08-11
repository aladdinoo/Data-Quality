"""
Data Quality Platform

Core application package.

This package contains shared application-level
configuration, constants, exceptions and logging.

Version: 1.0.0
"""

from .constants import *
from .exceptions import *
from .logging import *
from .settings import *

__version__ = "1.0.0"

__all__ = [
    "__version__",
]