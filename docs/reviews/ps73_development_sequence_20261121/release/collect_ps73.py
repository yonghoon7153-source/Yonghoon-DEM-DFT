"""Read an author-private status snapshot and terminal reports, without scheduling jobs."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import sys
import zipfile

ARMS = ("UB", "UT", "UC", "UVa", "UVb", "UTc")
JOB_FILES = ("intent.json", "reply.json", "node_started.json", "node_finished.json",
             "accounting.json", "receipt.json", "sbatch.stdout", "sbatch.stderr")


def safe_file(base, path):
    try:
        p = path.relative_to(base)
        parent = base
        if base.is_symlink():
            return False
        for part in p.parts:
            parent = parent / part
            if parent.is_symlink():
                return False
        return path.is_file()
    except ValueError:
        return False


def collect(ops, original, stream):
    state = ops / "state"
    bed = original / "ps_7_3_r45"
    if not state.is_dir() or state.is_symlink() or bed.is_symlink():
        raise ValueError("state or bed is absent or linked")
    files = {}
    result = {"purpose": "AUTHOR_PRIVATE_DEVELOPMENT_RETURN", "submitted_by_collection": False,
              "captured_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "terminal_reports": [], "pending_or_unavailable": []}
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        def add(name, data):
            z.writestr(name, data)
            files[name] = hashlib.sha256(data).hexdigest()

        def add_file(name, path, root):
            if not safe_file(root, path):
                return False
            h = hashlib.sha256()
            before = path.stat()
            with path.open("rb") as src, z.open(name, "w", force_zip64=True) as dst:
                for chunk in iter(lambda: src.read(1024*1024), b""):
                    h.update(chunk)
                    dst.write(chunk)
            after = path.stat()
            if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                    after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
                raise ValueError("file changed during collection: " + name)
            files[name] = h.hexdigest()
            return True

        for p in sorted(state.glob("*.json")):
            add_file("state/" + p.name, p, state)
        for arm in ARMS:
            job = state / "jobs" / arm
            for key in JOB_FILES:
                add_file("state/jobs/" + arm + "/" + key, job / key, state)
            if not any(safe_file(state, job / key) for key in ("receipt.json", "accounting.json")):
                result["pending_or_unavailable"].append(arm)
                continue
            name = arm + ".report.tgz"
            if add_file("reports/" + name, bed / name, original):
                result["terminal_reports"].append(arm)
            else:
                result["pending_or_unavailable"].append(arm)
        # The derived selection file can change between arms. Capture it only at an
        # explicit terminal review when the controller has stopped dispatching.
        final = state / "sequence_result.json"
        if safe_file(state, final):
            add_file("reports/selection.json", bed / "selection.json", original)
        add("collection.json", (json.dumps(result, indent=2) + "\n").encode())
        z.writestr("SHA256SUMS", "".join(h + "  " + k + "\n" for k,h in sorted(files.items())).encode())


if __name__ == "__main__":
    try:
        ops = Path.home() / "ps73_dev_ops_20261121"
        original = Path.home() / "ps45_a5_rj_9fd6aa9d3bee_1120_once"
        collect(ops, original, sys.stdout.buffer)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print("COLLECTION_INCOMPLETE:", error, file=sys.stderr)
        sys.exit(2)
