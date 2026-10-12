"""Package review artifacts only; no simulation, git, or network operations."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parent
archive = root.parent / "codex_dem_unloading_prereg_rereview_20261012.zip"
contents = root / "CONTENTS_SHA256.json"
files = sorted(p for p in root.rglob("*") if p.is_file() and p != contents)
assert all("__pycache__" not in p.parts for p in files)
manifest = [{"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size,
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
contents.write_text(json.dumps({"files": manifest}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert not archive.exists(), "Refusing to replace an existing delivery archive"
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
    for p in files + [contents]:
        z.write(p, arcname=p.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as z:
    names = z.namelist()
    assert len(names) == len(set(n.casefold() for n in names))
    assert all(not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts and ":" not in n for n in names)
    assert z.testzip() is None
    for item in manifest:
        data = z.read(item["path"])
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
receipt = {"zip": str(archive), "bytes": archive.stat().st_size,
           "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
           "entries": len(names), "verified_manifest_files": len(manifest),
           "zip_entry_hazards": [], "crc": "PASS", "manifest": "PASS"}
archive.with_suffix(".receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(receipt, ensure_ascii=False, indent=2))
