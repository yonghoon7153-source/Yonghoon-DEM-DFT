"""Reviewer-owned deterministic package checks; received code is data only."""
import binascii
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
ROOT = Path(__file__).resolve().parents[1]
ZIPNAME = "REIL_C4E_E1_V4_ULTRA_REVIEW_20261021.zip"
def ident(p):
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def save(name, obj):
    with (ROOT / name).open("x", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
before = json.loads((ROOT / "SELECTED_REVIEW_INPUTS_BEFORE.json").read_text(encoding="utf-8"))
rows = []
for r in before["files"]:
    now = ident(Path(r["path"]))
    match = now == {"bytes": r["bytes"], "sha256": r["sha256"]}
    rows.append({"path": r["path"], **now, "matches_before": match})
if not all(r["matches_before"] for r in rows):
    raise RuntimeError("Selected input identity changed")
save("SELECTED_REVIEW_INPUTS_AFTER.json", {"utc": datetime.now(timezone.utc).isoformat(), "count": len(rows),
    "all_match": True, "scope": "Local uploads and pinned capture copies only; after review prose, before ZIP", "files": rows})
excluded = {ZIPNAME, "PACKAGE_MANIFEST.json", "DELIVERY_RECEIPT.json", "PACKAGE_TOOL_RETURN.json", "FINAL_CHECK.json"}
payload = sorted(p for p in ROOT.rglob("*") if p.is_file() and p.name not in excluded)
manifest = {"kind": "REVIEW_PACKAGE_MANIFEST", "files": [{"path": p.relative_to(ROOT).as_posix(), **ident(p)} for p in payload]}
save("PACKAGE_MANIFEST.json", manifest)
archive = ROOT / ZIPNAME
with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in payload + [ROOT / "PACKAGE_MANIFEST.json"]:
        z.write(p, p.relative_to(ROOT).as_posix())
expected = {r["path"]: r for r in manifest["files"]}
expected["PACKAGE_MANIFEST.json"] = ident(ROOT / "PACKAGE_MANIFEST.json")
with zipfile.ZipFile(archive) as z:
    infos = z.infolist()
    names = [i.filename for i in infos]
    assert set(names) == set(expected) and len(names) == len(expected)
    assert len({n.casefold() for n in names}) == len(names)
    for i in infos:
        q = PurePosixPath(i.filename)
        assert not q.is_absolute() and ".." not in q.parts and "\\" not in i.filename and ":" not in i.filename
        assert not stat.S_ISLNK(i.external_attr >> 16)
        b = z.read(i)
        assert len(b) == expected[i.filename]["bytes"]
        assert hashlib.sha256(b).hexdigest() == expected[i.filename]["sha256"]
        assert binascii.crc32(b) & 0xffffffff == i.CRC
for r in rows:
    assert ident(Path(r["path"])) == {"bytes": r["bytes"], "sha256": r["sha256"]}
receipt = {"kind": "REVIEW_DELIVERY_RECEIPT", "utc": datetime.now(timezone.utc).isoformat(), "recipient": None,
           "archive": {"path": str(archive), **ident(archive)}, "manifest": ident(ROOT / "PACKAGE_MANIFEST.json"),
           "payload_count": len(payload), "entries": len(expected),
           "verification": "Exact set, sizes, decompressed SHA256, recomputed CRC32, case uniqueness, safe paths and no symlink metadata matched",
           "selected_inputs": len(rows), "selected_input_recheck_after_package": True,
           "decision": "CHANGES_REQUIRED_NO_EXECUTION", "current_P2": 1, "separate_P3": 1,
           "target_imports": 0, "target_tests": 0, "received_code_execution": 0, "remote_writes": 0,
           "budget_seconds": None, "whole_review_elapsed_claim": None,
           "boundary": "After ZIP readback and selected input recheck; before receipt write and tool return"}
save("DELIVERY_RECEIPT.json", receipt)
print(json.dumps({"kind": "STATIC_REVIEW_PACKAGE_RETURN", "archive": receipt["archive"], "payload_count": len(payload),
                  "entries": len(expected), "receipt": ident(ROOT / "DELIVERY_RECEIPT.json"), "selected_inputs_unchanged": len(rows),
                  "target_tests": 0, "decision": receipt["decision"], "boundary": "After receipt write/readback; before tool return"}, ensure_ascii=False))
