"""Reviewer-owned, data-only packaging and verification. Never imports submitted code."""
from pathlib import Path
import hashlib
import json
import zipfile
import datetime

root = Path(__file__).resolve().parent
zip_path = root.parent / "GATE94_LIMITED_REVIEW_20261007.zip"
receipt_path = root / "REVIEW_DELIVERY_RECEIPT.json"
manifest_path = root / "PACKAGE_MANIFEST.json"
if zip_path.exists() or receipt_path.exists() or manifest_path.exists():
    raise SystemExit("STOP: review package destination exists")

def h(data):
    return hashlib.sha256(data).hexdigest()

inputs = json.loads((root / "INPUT_IDENTITIES.json").read_text(encoding="utf-8"))
input_results = []
payload = {}
for spec in inputs:
    path = Path(spec["path"])
    data = path.read_bytes()
    assert len(data) == spec["bytes"] and h(data) == spec["sha256"], spec["path"]
    payload["originals/" + path.name] = data
    input_results.append({**spec, "final_matches_first_read": True})

for path in sorted(root.rglob("*")):
    if not path.is_file():
        continue
    if path.is_symlink():
        raise ValueError("Symlink in reviewer output")
    rel = path.relative_to(root).as_posix()
    if "__pycache__" in path.parts or path.suffix == ".pyc":
        raise ValueError("Unexpected compiled file")
    data = path.read_bytes()
    if path.suffix == ".json":
        json.loads(data.decode("utf-8"))
    assert rel not in payload
    payload[rel] = data

decision = json.loads(payload["DECISION.json"])
assert not decision["execution_go"] and not decision["bundle6_closed"]
assert all(x == 0 for x in decision["reviewer_execution"].values())
assert all(row["pass"] for row in json.loads(payload["LOG_README_HASH_VERIFICATION.json"]))
rep = json.loads(payload["REFERENCE_BYTE_VERIFICATION.json"])
assert rep["request_attachment_match"]
aborted = json.loads(payload["evidence/main/aborted/ORIGINAL_CONTENT.json"])
original = aborted["content"].encode("utf-8")
assert len(original) == 1555
assert hashlib.sha1(b"blob " + str(len(original)).encode() + b"\0" + original).hexdigest() == aborted["blob"]

manifest = {
    "scope": "New recipient static review, not original execution evidence",
    "self_excluded": True,
    "payload_count": len(payload),
    "files": [{"path": p, "bytes": len(b), "sha256": h(b)} for p, b in sorted(payload.items())],
}
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
manifest_path.write_bytes(manifest_bytes)
payload["PACKAGE_MANIFEST.json"] = manifest_bytes
assert len({name.casefold() for name in payload}) == len(payload)
with zipfile.ZipFile(zip_path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in sorted(payload.items()):
        archive.writestr(name, data)
with zipfile.ZipFile(zip_path) as archive:
    assert len(archive.namelist()) == len(set(archive.namelist())) == len(payload)
    assert set(archive.namelist()) == set(payload)
    assert archive.testzip() is None
    for name, data in payload.items():
        assert archive.read(name) == data
for spec in inputs:
    data = Path(spec["path"]).read_bytes()
    assert len(data) == spec["bytes"] and h(data) == spec["sha256"]
zip_data = zip_path.read_bytes()
receipt = {
    "created_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "kind": "RECIPIENT_STATIC_REVIEW_PACKAGE",
    "status": "REVIEW_PACKAGE_VERIFIED",
    "zip": {"path": str(zip_path), "bytes": len(zip_data), "sha256": h(zip_data)},
    "payload_count": manifest["payload_count"],
    "manifest_bytes": len(manifest_bytes),
    "manifest_sha256": h(manifest_bytes),
    "checks": ["exact_set", "member_bytes_sha256", "CRC", "casefold_unique", "JSON_parse", "input_preservation"],
    "input_preservation": input_results,
    "repository_code_execution": 0,
    "tests_or_replay": 0,
    "comsol": 0,
    "remote_writes": 0,
    "external_sending": False,
    "execution_go": False,
    "bundle6_closed": False,
}
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
assert json.loads(receipt_path.read_text(encoding="utf-8")) == receipt
print(json.dumps({"status": receipt["status"], "zip": receipt["zip"], "payload_count": receipt["payload_count"], "recipient_review_status": decision["status"]}, ensure_ascii=False))
