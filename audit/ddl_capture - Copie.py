"""
DDL capture utilities.

Captures a deterministic SHA-256 fingerprint of source DDL
before and after an audit run.

This module never modifies the source database.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DDLFingerprint:
    """Immutable DDL fingerprint."""

    ddl: str
    sha256: str


def normalize_ddl(ddl: str) -> str:
    """
    Normalize DDL before hashing.

    Only deterministic whitespace normalization is performed.
    """
    if ddl is None:
        raise ValueError("DDL cannot be None.")

    return " ".join(str(ddl).split())


def hash_ddl(ddl: str) -> str:
    """
    Return SHA-256 hash of normalized DDL.
    """
    normalized = normalize_ddl(ddl)

    return hashlib.sha256(
        normalized.encode("utf-8")
    ).hexdigest()


def capture_ddl(ddl: str) -> DDLFingerprint:
    """
    Capture DDL and its deterministic hash.
    """
    normalized = normalize_ddl(ddl)

    return DDLFingerprint(
        ddl=normalized,
        sha256=hash_ddl(normalized),
    )


def ddl_unchanged(
    before: DDLFingerprint,
    after: DDLFingerprint,
) -> bool:
    """
    Return True when source DDL did not change.
    """
    return before.sha256 == after.sha256