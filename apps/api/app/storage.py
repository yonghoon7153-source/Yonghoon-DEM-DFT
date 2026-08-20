"""Where bytes live.

Original ``.wrd`` files are kept verbatim and never modified; parsed columns
are cached next to them as compressed ``.npz`` (ADR 0003).  Both are content-
addressed by the upload's SHA-256, so re-uploading the same file is a no-op
rather than a duplicate.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from wrdkit import WrdFile, read_wrd

from .settings import settings


def upload_path(sha256: str) -> Path:
    return settings.uploads_dir / f"{sha256}.wrd"


def run_dir(run_id: int) -> Path:
    return settings.runs_dir / str(run_id)


def columns_path(run_id: int) -> Path:
    return run_dir(run_id) / "columns.npz"


def store_upload(content: bytes, sha256: str) -> Path:
    """Write the original file if it is not already there."""
    settings.ensure_dirs()
    target = upload_path(sha256)
    if not target.exists():
        target.write_bytes(content)
    return target


def cache_columns(run_id: int, wrd: WrdFile) -> Path:
    """Persist the parsed columns so a profile request need not re-parse."""
    directory = run_dir(run_id)
    directory.mkdir(parents=True, exist_ok=True)
    target = columns_path(run_id)
    np.savez_compressed(target, **wrd.data)
    (directory / "meta.json").write_text(json.dumps({
        "source_name": wrd.metadata.source_name,
        "sha256": wrd.metadata.sha256,
        "row_count": wrd.metadata.row_count,
        "columns": [c.name for c in wrd.metadata.columns],
    }, ensure_ascii=False, indent=1))
    return target


def load_columns(run_id: int) -> dict[str, np.ndarray] | None:
    """Read the cached columns, or ``None`` when the cache is missing."""
    target = columns_path(run_id)
    if not target.exists():
        return None
    with np.load(target, allow_pickle=False) as archive:
        return {name: archive[name] for name in archive.files}


def drop_run_cache(run_id: int) -> None:
    directory = run_dir(run_id)
    if not directory.exists():
        return
    for child in directory.iterdir():
        child.unlink()
    directory.rmdir()


def reparse(sha256: str) -> WrdFile:
    """Re-read an original upload from disk."""
    path = upload_path(sha256)
    if not path.exists():
        raise FileNotFoundError(f"original upload for {sha256[:12]} is missing")
    return read_wrd(path)
