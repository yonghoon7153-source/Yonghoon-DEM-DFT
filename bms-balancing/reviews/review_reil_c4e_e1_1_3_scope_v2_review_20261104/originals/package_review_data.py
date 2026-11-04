"""Reviewer data-only package tool. Never import or execute received sources."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile, zlib
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT / "REIL_C4E_E1_1_3_SCOPE_V2_REVIEW_20261104.zip"
MANIFEST = ROOT / "PACKAGE_MANIFEST.json"
RECEIPT = ROOT / "DELIVERY_RECEIPT.json"

def digest(data):
    return hashlib.sha256(data).hexdigest()

def record(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": digest(data)}

def write_new(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(data)
    if path.read_bytes() != data:
        raise ValueError("JSON write/readback mismatch: " + str(path))
    return record(path)

identities = json.loads((ROOT / "SOURCE_IDENTITIES.json").read_text(encoding="utf-8-sig"))
original = identities["attachment"]
observed = record(Path(original["path"]))
assert (observed["bytes"], observed["sha256"]) == (original["bytes"], original["sha256"])
copies = []
for row in identities["reused_sources"]:
    item = record(ROOT / "source" / row["path"])
    assert (item["bytes"], item["sha256"]) == (row["bytes"], row["sha256"])
    copies.append({"relative_path": "source/" + row["path"], "bytes": item["bytes"], "sha256": item["sha256"], "matches_prior_identity": True})
assert (ROOT / "input" / Path(original["path"]).name).read_bytes() == Path(original["path"]).read_bytes()
assert (ROOT / "source" / "bms-balancing" / "docs" / Path(original["path"]).name).read_bytes() == Path(original["path"]).read_bytes()
write_new(ROOT / "SOURCE_PRESERVATION_CHECK.json", {
    "kind": "REVIEW_SOURCE_IDENTITY_RECHECK",
    "utc": datetime.now(timezone.utc).isoformat(),
    "original_attachment": observed,
    "original_attachment_matches_intake": True,
    "reviewed_source_copies": copies,
    "original_attachment_count": 1,
    "fixed_source_copy_count": len(copies),
    "scope": "One locally received original attachment plus four fixed local source copies. Not a remote original preservation audit.",
    "received_program_execution": 0
})
decision = json.loads((ROOT / "REVIEW_DECISION.json").read_text(encoding="utf-8"))
assert decision["closures"]["E113_N1"] == "CLOSED"
assert decision["p1_document_direction_acceptable"] and not decision["p2_immediate_probe_ready"]
assert not decision["probe_authorized"] and not decision["actual_execution_authorized"]
assert json.loads((ROOT / "HEAD_AT_CLOSE.json").read_text(encoding="utf-8"))["matches_reviewed_pin"]
excluded = {"PACKAGE_MANIFEST.json", ARCHIVE.name, "DELIVERY_RECEIPT.json", "PACKAGE_TOOL_RETURN.json"}
payload = {}
for path in sorted(ROOT.rglob("*")):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel in excluded:
        continue
    if path.is_symlink():
        raise ValueError("Symlink excluded: " + rel)
    p = PurePosixPath(rel)
    if p.is_absolute() or any(x in ("", ".", "..") for x in p.parts) or "\\" in rel or ":" in rel:
        raise ValueError("Unsafe path: " + rel)
    payload[rel] = path.read_bytes()
assert len({name.casefold() for name in payload}) == len(payload)
rows = [{"path": name, "bytes": len(data), "sha256": digest(data)} for name, data in payload.items()]
manifest_obj = {
    "kind": "REVIEW_PACKAGE_MANIFEST",
    "payload_count": len(rows),
    "manifest_self_excluded": True,
    "files": rows,
    "scope": "Static review evidence and reviewer data tools; included received Python source is not execution authorization."
}
write_new(MANIFEST, manifest_obj)
sealed = dict(payload)
sealed[MANIFEST.name] = MANIFEST.read_bytes()
with zipfile.ZipFile(ARCHIVE, mode="x", compression=zipfile.ZIP_DEFLATED) as archive:
    for name, data in sealed.items():
        archive.writestr(name, data)
with zipfile.ZipFile(ARCHIVE, mode="r") as archive:
    members = archive.infolist()
    assert len(members) == len(sealed)
    assert {m.filename for m in members} == set(sealed)
    assert len({m.filename.casefold() for m in members}) == len(members)
    for member in members:
        p = PurePosixPath(member.filename)
        assert not p.is_absolute() and all(x not in ("", ".", "..") for x in p.parts)
        assert not stat.S_ISLNK(member.external_attr >> 16)
        data = archive.read(member.filename)
        assert member.file_size == len(sealed[member.filename])
        assert digest(data) == digest(sealed[member.filename])
        assert (zlib.crc32(data) & 0xffffffff) == member.CRC
    assert archive.testzip() is None
assert record(Path(original["path"]))["sha256"] == original["sha256"]
receipt = {
    "kind": "REIL_SCOPE_V2_REVIEW_DELIVERY_RECEIPT",
    "recipient": None,
    "archive": record(ARCHIVE),
    "manifest": record(MANIFEST),
    "payload_count": len(payload),
    "entries": len(sealed),
    "verification": "Exact set, safe unique relative paths, decompressed size/SHA256, link metadata and independently recomputed CRC32 matched.",
    "original_attachment_preserved": True,
    "fixed_source_copies_matched": 4,
    "decision": decision["decision"],
    "E113_N1": "CLOSED",
    "p1_document_direction_acceptable": True,
    "p2_immediate_probe_ready": False,
    "user_choices_recorded": False,
    "probe_execution": 0,
    "received_program_execution": 0,
    "actual_E1_execution_authorized": False,
    "numeric_review_budget_seconds": None,
    "whole_work_elapsed_claim": None,
    "boundary": "After ZIP readback and original attachment rehash; before receipt write/readback and tool return."
}
receipt_id = write_new(RECEIPT, receipt)
print(json.dumps({
    "kind": "REIL_SCOPE_V2_REVIEW_PACKAGE_RETURN",
    "archive": record(ARCHIVE),
    "receipt": receipt_id,
    "payload_count": len(payload),
    "entries": len(sealed),
    "decision": decision["decision"],
    "E113_N1": "CLOSED",
    "p1_document_direction_acceptable": True,
    "p2_immediate_probe_ready": False,
    "received_program_execution": 0,
    "probe_execution": 0,
    "boundary": "After review ZIP and receipt write/readback; before this tool return and its later transcription."
}, ensure_ascii=False, indent=2))

