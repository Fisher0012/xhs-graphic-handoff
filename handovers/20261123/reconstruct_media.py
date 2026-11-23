#!/usr/bin/env python3
"""Restore media larger than 50 MiB from lossless raw shards, then run sha256sum -c.

Run from any working directory:

    python3 handovers/20261123/reconstruct_media.py

The frozen snapshot under 完整交接/ is not rewritten except for the seven
original paths named in storage/SHARD_MANIFEST.json. Existing files that
already match size and SHA256 are left in place. A different file at the
same path is left untouched and the script exits with an error.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SNAPSHOT = ROOT / "完整交接"
MANIFEST_PATH = ROOT / "storage" / "SHARD_MANIFEST.json"
READ = 8 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(READ), b""):
            digest.update(block)
    return digest.hexdigest()


def require_inside(base: Path, path: Path) -> Path:
    resolved = path.resolve()
    resolved.relative_to(base.resolve())
    return resolved


def restore(manifest: dict) -> None:
    snapshot = require_inside(ROOT, SNAPSHOT)
    for record in manifest["files"]:
        relative = Path(record["relative_path"])
        if relative.is_absolute() or ".." in relative.parts:
            raise SystemExit(f"unsafe relative path: {record['relative_path']}")
        destination = require_inside(snapshot, snapshot / relative)
        expected_size = int(record["size"])
        expected_sha = record["sha256"]
        if destination.exists():
            if destination.stat().st_size == expected_size and sha256_file(destination) == expected_sha:
                print(f"ALREADY_OK {record['relative_path']}")
                continue
            raise SystemExit(
                f"refusing to overwrite different file: {record['relative_path']}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        partial = destination.with_name(destination.name + ".partial")
        output_hash = hashlib.sha256()
        written = 0
        try:
            with partial.open("wb") as output:
                for piece in record["pieces"]:
                    piece_path = require_inside(ROOT, ROOT / piece["path"])
                    piece_hash = hashlib.sha256()
                    piece_size = 0
                    with piece_path.open("rb") as source:
                        for block in iter(lambda: source.read(READ), b""):
                            piece_hash.update(block)
                            output_hash.update(block)
                            output.write(block)
                            piece_size += len(block)
                    if piece_size != int(piece["size"]) or piece_hash.hexdigest() != piece["sha256"]:
                        raise SystemExit(f"piece mismatch: {piece['path']}")
                    written += piece_size
            if written != expected_size or output_hash.hexdigest() != expected_sha:
                raise SystemExit(f"restored file mismatch: {record['relative_path']}")
            partial.replace(destination)
        except Exception:
            if partial.exists():
                partial.unlink()
            raise
        print(f"RESTORED_OK {record['relative_path']} {written} {expected_sha}")


def verify_snapshot() -> None:
    checksums = SNAPSHOT / "SHA256SUMS"
    if not checksums.is_file():
        raise SystemExit(f"missing {checksums}")
    result = subprocess.run(
        ["sha256sum", "-c", "SHA256SUMS"],
        cwd=SNAPSHOT,
        text=True,
        capture_output=True,
    )
    sys.stdout.write(result.stdout)
    sys.stderr.write(result.stderr)
    ok = result.stdout.count(": OK\n")
    failed = result.stdout.count(": FAILED\n")
    print(f"SHA256SUM_RESULT ok={ok} failed={failed} exit={result.returncode}")
    if result.returncode != 0 or failed:
        raise SystemExit(result.returncode or 1)


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    restore(manifest)
    verify_snapshot()


if __name__ == "__main__":
    main()
