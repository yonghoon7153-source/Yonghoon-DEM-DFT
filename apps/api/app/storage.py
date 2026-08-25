"""Where bytes live.

Original ``.wrd`` files are kept verbatim and never modified; parsed columns
are cached next to them as compressed ``.npz`` (ADR 0003).  Both are content-
addressed by the upload's SHA-256, so re-uploading the same file is a no-op
rather than a duplicate.
"""

from __future__ import annotations

import contextlib
import json
import os
import tempfile
import zipfile
from pathlib import Path

import numpy as np

from wrdkit import WrdFile, read_wrd

from .settings import settings


class StorageError(RuntimeError):
    """A stored file is not what the database says it is."""


def upload_path(sha256: str) -> Path:
    return settings.uploads_dir / f"{sha256}.wrd"


def spectrum_upload_path(sha256: str, suffix: str) -> Path:
    """Where an impedance original lives.

    The extension is kept because it is not decoration: ``.mpr`` and ``.mpt``
    are read by different code, and a stored file that has lost the difference
    cannot be re-parsed without guessing.  Anything unexpected becomes
    ``.bin`` rather than being trusted into a path.
    """
    clean = suffix.lower().lstrip(".")
    if clean not in ("mpr", "mpt", "mps"):
        clean = "bin"
    return settings.uploads_dir / f"{sha256}.{clean}"


def spectrum_dir(spectrum_id: int) -> Path:
    return settings.spectra_dir / str(spectrum_id)


def spectrum_points_path(spectrum_id: int) -> Path:
    return spectrum_dir(spectrum_id) / "points.npz"


def cache_spectrum(spectrum_id: int, spectrum) -> Path:
    """Persist the parsed points so a plot need not re-read the original."""
    directory = spectrum_dir(spectrum_id)
    directory.mkdir(parents=True, exist_ok=True)
    target = spectrum_points_path(spectrum_id)
    payload = {"frequency_hz": spectrum.frequency_hz,
               "z_re": spectrum.z_re, "z_im": spectrum.z_im}
    payload.update({f"col::{name}": values
                    for name, values in spectrum.columns.items()})
    _write_atomically(target, lambda handle: np.savez_compressed(handle, **payload))
    return target


def load_spectrum(spectrum_id: int):
    """The cached points, or ``None`` when the cache is gone or unreadable."""
    from wrdkit.eis import Spectrum

    path = spectrum_points_path(spectrum_id)
    if not path.exists():
        return None
    try:
        with np.load(path, allow_pickle=False) as archive:
            frequency = archive["frequency_hz"]
            z_re = archive["z_re"]
            z_im = archive["z_im"]
            columns = {name[5:]: archive[name] for name in archive.files
                       if name.startswith("col::")}
    except (OSError, ValueError, KeyError):
        return None
    return Spectrum(frequency_hz=frequency, z_re=z_re, z_im=z_im,
                    columns=columns)


def load_gitt(sha256: str) -> WrdFile | None:
    """A GITT record, re-read from its immutable original.

    No parse cache, unlike cycling.  The cycling cache exists because a profile
    request needs a few columns out of a 20 MB file and there are dozens of
    such requests per screen; a GITT screen asks twice, for the whole record,
    and a second copy of the same numbers is a second thing to keep in step
    with the original.  If this turns out slow on a real file, the cache goes
    in then -- with a reason.
    """
    try:
        return reparse(sha256)
    except (FileNotFoundError, StorageError):
        return None


def drop_spectrum_cache(spectrum_id: int) -> None:
    """Remove a spectrum's parsed points.  The original upload stays (§0.2)."""
    directory = spectrum_dir(spectrum_id)
    if not directory.exists():
        return
    for child in directory.iterdir():
        child.unlink(missing_ok=True)
    directory.rmdir()


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
    # A unique temporary name, not a fixed one.  Two requests can miss the
    # cache for the same run at the same moment (a profile and an export, say);
    # with a shared ``.name.tmp`` they write into one file, and whichever
    # renames second publishes a blend of both -- or fails outright, because
    # the first one's ``unlink`` already took the path out from under it.
    handle_fd, temporary_name = tempfile.mkstemp(
        dir=str(target.parent), prefix=f".{target.name}.", suffix=".tmp")
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle_fd, "wb") as handle:
            write(handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)


def store_bytes(content: bytes, target: Path) -> Path:
    """Write *content* to *target* unless the same length is already there.

    The caller names the file after its own content hash, so a size mismatch
    can only be a partial write from an earlier attempt.
    """
    settings.ensure_dirs()
    if not target.exists() or target.stat().st_size != len(content):
        _write_atomically(target, lambda handle: handle.write(content))
    return target


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
        # Open the file here rather than handing ``np.load`` a path.  When the
        # archive is truncated, ``np.load`` raises while constructing -- so the
        # ``with`` it would have managed never runs, and the descriptor it
        # opened stays alive.  On Windows an open descriptor blocks unlink, so
        # the recovery below fails with PermissionError and the run 500s for
        # good.  Owning the handle means it closes on the way out either way.
        with open(target, "rb") as handle, \
                np.load(handle, allow_pickle=False) as archive:
            columns = {name: archive[name] for name in archive.files}
    except (zipfile.BadZipFile, OSError, ValueError, KeyError, EOFError):
        drop_run_cache(run_id)
        return None

    meta = cached_meta(run_id)
    if meta is None:
        # ``drop_run_cache`` removes meta.json first precisely so a cache it
        # could not finish deleting is not trusted afterwards.  An archive that
        # cannot say which file it came from is not evidence of anything.
        drop_run_cache(run_id)
        return None
    if not _columns_match_meta(columns, meta):
        # Same file, wrong contents: an interrupted publish, or a cache written
        # by an older parser that named or sized its columns differently.  The
        # sha check above cannot see this, and slicing a CycleRecord range into
        # arrays of the wrong length shows a different part of the run without
        # saying so.
        drop_run_cache(run_id)
        return None
    return columns


def _columns_match_meta(columns: dict[str, np.ndarray], meta: dict) -> bool:
    """Does the archive hold what ``meta.json`` says it holds?"""
    expected_names = meta.get("columns")
    if expected_names is not None and set(expected_names) != set(columns):
        return False
    expected_rows = meta.get("row_count")
    if expected_rows is None:
        return True
    return all(len(array) == expected_rows for array in columns.values())


def drop_run_cache(run_id: int) -> None:
    """Throw the cache away.  Never raise -- the caller can always re-parse.

    Deleting can genuinely fail: on Windows another handle on the archive
    blocks unlink, and a read-only mount refuses outright.  Raising here would
    turn a recoverable cache miss into a 500 on every profile and export of
    that run, which is strictly worse than leaving a stale directory behind.
    So the failure is swallowed, and ``meta.json`` is removed first: without
    it :func:`load_columns` cannot confirm the archive's identity, so the
    leftover is never trusted even if its bytes survive.
    """
    directory = run_dir(run_id)
    if not directory.exists():
        return
    with contextlib.suppress(OSError):
        (directory / "meta.json").unlink(missing_ok=True)
    for child in sorted(directory.iterdir()):
        with contextlib.suppress(OSError):
            child.unlink()
    with contextlib.suppress(OSError):
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
