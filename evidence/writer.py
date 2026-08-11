"""
Evidence manifest writer.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .manifest import (
    FailureManifest,
    SuccessManifest,
)


class EvidenceWriter:
    """
    Write validation manifests and calculate
    their SHA-256 from the actual file bytes.
    """

    def __init__(
        self,
        directory: str | Path,
    ) -> None:

        self.directory = Path(directory)

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    @staticmethod
    def _sha256_file(
        path: Path,
    ) -> str:

        digest = hashlib.sha256()

        with path.open("rb") as file:

            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _write_json(
        path: Path,
        payload: dict[str, Any],
    ) -> str:

        data = json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        ).encode("utf-8")

        path.write_bytes(data)

        return hashlib.sha256(data).hexdigest()

    def write_success(
        self,
        manifest: SuccessManifest,
    ) -> dict[str, Any]:

        if manifest.status != "SUCCESS":
            raise ValueError(
                "Success manifest status must be SUCCESS."
            )

        path = (
            self.directory
            / f"success_manifest_{manifest.run_id}.json"
        )

        payload = asdict(manifest)

        manifest_sha256 = self._write_json(
            path,
            payload,
        )

        result = dict(payload)

        # IMPORTANT:
        # This value is returned to the caller,
        # but is NOT written inside the JSON file.
        result["success_manifest_sha256"] = (
            manifest_sha256
        )

        result["manifest_path"] = str(path)

        return result

    def write_failure(
        self,
        manifest: FailureManifest,
    ) -> dict[str, Any]:

        if manifest.status != "FAILURE":
            raise ValueError(
                "Failure manifest status must be FAILURE."
            )

        path = (
            self.directory
            / f"failure_manifest_{manifest.run_id}.json"
        )

        payload = asdict(manifest)

        manifest_sha256 = self._write_json(
            path,
            payload,
        )

        result = dict(payload)

        result["failure_manifest_sha256"] = (
            manifest_sha256
        )

        result["manifest_path"] = str(path)

        return result