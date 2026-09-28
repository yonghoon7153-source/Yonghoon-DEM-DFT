"""Verify pinned source bytes against Git blob hashes, without invoking Git."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / "sources.json").read_text(encoding="utf-8"))
bad = []
for entry in manifest["files"]:
    p = root / entry["path"]
    data = p.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    ok = actual == entry["blob_sha"]
    print(("OK " if ok else "MISMATCH ") + entry["path"])
    if not ok:
        bad.append(entry["path"])
print(str(len(manifest["files"]) - len(bad)) + "/" + str(len(manifest["files"])) + " byte-exact source blobs")
raise SystemExit(bool(bad))

