"""Package only reviewer-authored documents and byte-verified static evidence.
No candidate code imports, tests, COMSOL, networking or source writes.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / "COMSOL_MICROSHORT_S1O_PREREVIEW_20261007.zip"
MANIFEST = ROOT / "PACKAGE_MANIFEST.json"
RECEIPT = ROOT / "REVIEW_DELIVERY_RECEIPT.json"
AFTER = ROOT / "SELECTED_INPUTS_AFTER.json"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def create_file(path, data):
    with path.open("xb") as stream:
        stream.write(data)

def input_snapshot(items):
    result = []
    for item in items:
        path = Path(item["path"])
        data = path.read_bytes()
        actual = {"path": str(path), "bytes": len(data), "sha256": sha(data)}
        if actual != item:
            raise RuntimeError("Selected input identity mismatch: " + str(path))
        result.append(actual)
    return result

for output in (ARCHIVE, MANIFEST, RECEIPT, AFTER):
    if output.exists():
        raise RuntimeError("Refusing existing output: " + str(output))

inputs = json.loads((ROOT / "INPUT_IDENTITIES.json").read_text(encoding="utf-8"))
before = input_snapshot(inputs)
create_file(AFTER, encoded({
    "scope": "Only the eight selected local inputs, not machine-wide preservation",
    "observed_utc": datetime.now(timezone.utc).isoformat(),
    "unchanged": True,
    "files": before,
}))

payload = {}
for path in sorted(ROOT.rglob("*")):
    if path.is_symlink():
        raise RuntimeError("Symlink in review folder: " + str(path))
    if not path.is_file():
        continue
    name = path.relative_to(ROOT).as_posix()
    if name in ("PACKAGE_MANIFEST.json", "REVIEW_DELIVERY_RECEIPT.json"):
        continue
    if "__pycache__" in path.parts or path.suffix == ".pyc":
        raise RuntimeError("Unexpected Python bytecode")
    data = path.read_bytes()
    if path.suffix == ".json":
        json.loads(data)
    payload[name] = data

s0marker = "microshort_s0_deep_20261007"
for item in inputs[1:]:
    path = Path(item["path"])
    position = path.parts.index(s0marker)
    relative = "/".join(path.parts[position + 1:])
    name = "s0_basis/" + relative
    if name in payload:
        raise RuntimeError("Duplicate member")
    payload[name] = path.read_bytes()

folded = [name.casefold() for name in payload]
if len(folded) != len(set(folded)):
    raise RuntimeError("Case collision")
for name in payload:
    if name.startswith("/") or "\\" in name or ":" in name or ".." in name.split("/"):
        raise RuntimeError("Unsafe archive path")

manifest = {
    "kind": "NEW_REVIEW_ARTIFACT_MANIFEST",
    "scope": "S1-O send-document prereview only; no implementation or native acceptance",
    "payload_count": len(payload),
    "files": [{"path": name, "bytes": len(data), "sha256": sha(data)}
              for name, data in sorted(payload.items())],
    "manifest_self_hash_excluded": True,
}
manifest_bytes = encoded(manifest)
create_file(MANIFEST, manifest_bytes)
with zipfile.ZipFile(ARCHIVE, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for name, data in sorted(payload.items()):
        archive.writestr(name, data)
    archive.writestr("PACKAGE_MANIFEST.json", manifest_bytes)

expected = dict(payload)
expected["PACKAGE_MANIFEST.json"] = manifest_bytes
with zipfile.ZipFile(ARCHIVE) as archive:
    names = archive.namelist()
    if len(names) != len(set(names)) or set(names) != set(expected):
        raise RuntimeError("Exact archive member set mismatch")
    if archive.testzip() is not None:
        raise RuntimeError("CRC failed")
    for entry in archive.infolist():
        if stat.S_ISLNK(entry.external_attr >> 16):
            raise RuntimeError("Archive symlink")
        actual = archive.read(entry)
        if actual != expected[entry.filename]:
            raise RuntimeError("Readback byte mismatch")
after = input_snapshot(inputs)
if after != before:
    raise RuntimeError("Selected input changed during packaging")
zip_bytes = ARCHIVE.read_bytes()
receipt = {
    "kind": "NEW_REVIEW_PACKAGE_RECEIPT",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "status": "REVIEW_PACKAGE_READBACK_VERIFIED",
    "scope": "Review document delivery only, not S1-O implementation or execution evidence",
    "recipient": None,
    "archive": {"path": str(ARCHIVE), "bytes": len(zip_bytes), "sha256": sha(zip_bytes)},
    "manifest": {"bytes": len(manifest_bytes), "sha256": sha(manifest_bytes)},
    "payload_count": len(payload),
    "selected_inputs_unchanged": len(after),
    "checks": ["exact_set", "case_collision", "safe_paths", "no_links",
               "member_size_sha256_and_full_bytes", "manifest_bytes", "CRC"],
    "new_native_authorization": False,
    "source_scope_note": "No remote machine, runtime, policy, or numeric result independently observed",
}
create_file(RECEIPT, encoded(receipt))
text = {key: receipt[key] for key in ("status", "archive", "payload_count", "selected_inputs_unchanged")}
print(json.dumps(text, ensure_ascii=False))

