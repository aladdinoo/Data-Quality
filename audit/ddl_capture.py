"""
DDL capture utilities.

Provides deterministic SHA-256 hashing and comparison
for source DDL before and after an audit run.

This module supports both the current DDLCapture API
and the legacy DDLFingerprint API used by the E2E audit
runner.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


# ============================================================
# Normalization
# ============================================================


def normalize_ddl(ddl: str) -> str:
    """
    Normalize DDL deterministically before hashing.

    Whitespace differences do not change the fingerprint.
    """

    if ddl is None:
        raise ValueError("DDL cannot be None.")

    return " ".join(str(ddl).split())


# ============================================================
# Hashing
# ============================================================


def hash_ddl(ddl: str) -> str:
    """
    Return the SHA-256 fingerprint of normalized DDL.
    """

    normalized = normalize_ddl(ddl)

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


# ============================================================
# Current API
# ============================================================


class DDLCapture:
    """
    Stateless DDL hashing utility.
    """

    @staticmethod
    def _normalize(ddl: str) -> str:
        """
        Normalize DDL deterministically.
        """

        return normalize_ddl(ddl)

    @staticmethod
    def sha256(ddl: str) -> str:
        """
        Return SHA-256 fingerprint of normalized DDL.
        """

        return hash_ddl(ddl)

    @staticmethod
    def unchanged(
        before: str,
        after: str,
    ) -> bool:
        """
        Return True when both DDL definitions are equivalent.
        """

        return (
            DDLCapture.sha256(before)
            == DDLCapture.sha256(after)
        )


# ============================================================
# Legacy API
# ============================================================


@dataclass(frozen=True, slots=True)
class DDLFingerprint:
    """
    Immutable fingerprint of a DDL definition.

    Kept for compatibility with the E2E audit runner.
    """

    sha256: str


def capture_ddl(ddl: str) -> DDLFingerprint:
    """
    Capture a deterministic fingerprint for a DDL definition.
    """

    return DDLFingerprint(
        sha256=hash_ddl(ddl)
    )


def ddl_unchanged(
    before: str,
    after: str,
) -> bool:
    """
    Return True when two DDL definitions are equivalent.
    """

    return (
        hash_ddl(before)
        == hash_ddl(after)
    )


# ============================================================
# Explicit exports
# ============================================================


__all__ = [
    "DDLCapture",
    "DDLFingerprint",
    "capture_ddl",
    "ddl_unchanged",
    "hash_ddl",
    "normalize_ddl",
]