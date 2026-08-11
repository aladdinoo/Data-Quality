"""
Evidence manifest writer.

Success and failure manifests intentionally use
different schemas.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from audit.manifest_models import (
    SuccessManifest,
    FailureManifest,
)


class EvidenceManifestWriter:
    """Write deterministic success/failure evidence manifests."""

    def write_success(
        self,
        manifest: SuccessManifest,
        output_file: Path,
    ) -> str:
        return self._write(
            manifest,
            output_file,
            expected_status="SUCCESS",
        )

    def write_failure(
        self,
        manifest: FailureManifest,
        output_file: Path,
    ) -> str:
        return self._write(
            manifest,
            output_file,
            expected_status="FAILURE",
        )

    def _write(
        self,
        manifest: Any,
        output_file: Path,
        expected_status: str,
    ) -> str:
        if manifest.status != expected_status:
            raise ValueError(
                f"Expected status {expected_status!r}, "
                f"got {manifest.status!r}."
            )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        payload = asdict(manifest)

        # Manifest hash must never be embedded inside itself.
        payload.pop("manifest_sha256", None)

        content = json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )

        output_file.write_text(
            content + "\n",
            encoding="utf-8",
        )

        return self.sha256(output_file)

    @staticmethod
    def sha256(
        file_path: Path,
    ) -> str:
        digest = hashlib.sha256()

        with file_path.open("rb") as file:
            for chunk in iter(
                lambda: file.read(1024 * 1024),
                b"",
            ):
                digest.update(chunk)

        return digest.hexdigest()