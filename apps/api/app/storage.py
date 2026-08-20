"""Where bytes live.

Original ``.wrd`` files are kept verbatim and never modified; parsed columns
are cached next to them as compressed ``.npz`` (ADR 0003).  Both are content-
addressed by the upload's SHA-256, so re-uploading the same file is a no-op
rather than a duplicate.
"""

from __future__ import annotations

import json
import os
import zipfile
from pathlib import Path

import numpy as np

from wrdkit import WrdFile, read_wrd

from .settings import settings


class StorageError(RuntimeError):
    """A stored file is not what the database says it is."""


def upload_path(sha256: str) -> Path:
    return settings.uploads_dir / f"{sha256}.wrd"


def run_dir(run_id: int) -> Path:
    return settings.runs_dir / str(run_id)


def columns_path(run_id: int) -> Path:
    return run_dir(run_id) / "columns.npz"


def _write_atomically(target: Path, write) -> None:
    """Fill a temporary file next to *target*, then rename it into place.

    A crash or a full disk part-way through a direct write leaves a truncated
    file behind, and a truncated ``.wrd`` is silent: the row scanner stops at
    the last complete record and returns fewer rows without an error.  Since
    the name is the content hash, that corruption would then be confirmed
    forever -- nothing ever writes those bytes again.  ``os.replace`` is
    atomic on the same filesystem, so a reader sees either the old file or the
    complete new one.
    """
    temporary = target.with_name(f".{target.name}.tmp")
    try:
        with open(temporary, "wb") as handle:
            write(handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def store_upload(content: bytes, sha256: str) -> Path:
    """Write the original file if it is not already there."""
    settings.ensure_dirs()
    target = upload_path(sha256)
    # The name is the content hash, so a size mismatch can only mean a partial
    # write from an earlier attempt: rewrite rather than trust it.
    if not target.exists() or target.stat().st_size != len(content):
        _write_atomically(target, lambda handle: handle.write(content))
    return target


def cache_columns(run_id: int, wrd: WrdFile) -> Path:
    """Persist the parsed columns so a profile request need not re-parse."""
    directory = run_dir(run_id)
    directory.mkdir(parents=True, exist_ok=True)
    target = columns_path(run_id)
    _write_atomically(target, lambda handle: np.savez_compressed(handle, **wrd.data))
    meta = json.dumps({
        "source_name": wrd.metadata.source_name,
        "sha256": wrd.metadata.sha256,
        "row_count": wrd.metadata.row_count,
        "columns": [c.name for c in wrd.metadata.columns],
    }, ensure_ascii=False, indent=1)
    _write_atomically(directory / "meta.json",
                      lambda handle: handle.write(meta.encode("utf-8")))
    return target


def cached_meta(run_id: int) -> dict | None:
    """What the cache says it holds, or ``None`` when it says nothing."""
    path = run_dir(run_id) / "meta.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (ValueError, OSError):
        return None


def load_columns(run_id: int, expect_sha256: str | None = None
                 ) -> dict[str, np.ndarray] | None:
    """Read the cached columns, or ``None`` when the cache cannot be trusted.

    The cache is expendable by design (ADR 0003), so anything doubtful is
    thrown away and rebuilt from the original instead of raised: a truncated
    ``.npz`` would otherwise 500 every profile and export of that run forever,
    because the fallback only ran when the file was *missing*.  A cache whose
    ``meta.json`` names a different file is discarded for the opposite reason
    -- SQLite reuses row ids, so a stale directory can sit under a new run's
    id and quietly serve another cell's columns.
    """
    target = columns_path(run_id)
    if not target.exists():
        return None
    if expect_sha256:
        meta = cached_meta(run_id)
        if meta and meta.get("sha256") and meta["sha256"] != expect_sha256:
            drop_run_cache(run_id)
            return None
    try:
        with np.load(target, allow_pickle=False) as archive:
            return {name: archive[name] for name in archive.files}
    except (zipfile.BadZipFile, OSError, ValueError, KeyError, EOFError):
        drop_run_cache(run_id)
        return None


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
    wrd = read_wrd(path)
    # A truncated .wrd parses without complaint -- it simply carries fewer
    # rows -- so re-hashing is the only way to tell a damaged original from a
    # short experiment.  Failing here is the point: the stored row slices
    # would otherwise index past the end and draw an empty or wrong profile.
    if wrd.metadata.sha256 != sha256:
        raise StorageError(
            f"stored original for {sha256[:12]} no longer hashes to its name "
            f"(got {wrd.metadata.sha256[:12]}); the file on disk is damaged")
    return wrd
