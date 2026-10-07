"""Reviewer-owned data-only packaging; never import or execute received sources."""
from pathlib import Path
import hashlib
import json
import time
import zipfile

ROOT = Path(__file__).resolve().parent
INPUT = Path("C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_OFFLINE_PREPARATION_20261007.zip")
OUTPUT = ROOT / "COMSOL_MICROSHORT_S1O_PREPARATION_REVIEW_20261007.zip"
MANIFEST = ROOT / "REVIEW_PACKAGE_MANIFEST.json"
CLOSEOUT = ROOT / "REVIEW_CLOSEOUT.json"
RECEIPT = ROOT / "REVIEW_DELIVERY_RECEIPT.json"
START = time.monotonic()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def create_json(path, obj):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

for target in (OUTPUT, MANIFEST, CLOSEOUT, RECEIPT):
    if target.exists():
        raise RuntimeError("Existing output; do not overwrite: " + str(target))
original = INPUT.read_bytes()
assert len(original) == 761798
assert digest(original) == "0cae7accaf26397d883e0d8b732357fc2dc640553c603825a6a155bf8d4aaf53"
with zipfile.ZipFile(INPUT) as archive:
    names = archive.namelist()
    actual_names = {p.relative_to(ROOT / "received").as_posix()
                    for p in (ROOT / "received").rglob("*") if p.is_file()}
    assert actual_names == set(names)
    for name in names:
        assert (ROOT / "received" / name).read_bytes() == archive.read(name), name
    assert archive.testzip() is None

create_json(CLOSEOUT, {
    "kind": "REVIEWER_DATA_ONLY_CLOSEOUT",
    "original_zip_bytes": len(original),
    "original_zip_sha256": digest(original),
    "received_files_unchanged_against_zip": len(names),
    "scope": "Local review input ZIP and extracted evidence, not execution-machine original files or policies",
    "received_programs_or_tests_executed": 0,
    "COMSOL": 0, "JVM": 0,
    "source_edits": 0,
    "outbound_sends": 0,
    "native_approval_created": False,
    "reported_external_receipt_and_return_are_user_message_data": True,
})
paths = sorted(p for p in ROOT.rglob("*")
               if p.is_file() and p not in (OUTPUT, MANIFEST, RECEIPT))
assert not any(p.is_symlink() for p in paths)
payload = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in paths}
assert len(payload) == len({n.casefold() for n in payload})
manifest = {
    "kind": "S1O_RECIPIENT_REVIEW_PACKAGE_MANIFEST",
    "input_archive_sha256": digest(original),
    "files": [{"path": name, "bytes": len(data), "sha256": digest(data)}
              for name, data in payload.items()],
    "manifest_self_hash_excluded": True,
    "included_received_sources_are_evidence_not_execution_instructions": True,
}
create_json(MANIFEST, manifest)
manifest_bytes = MANIFEST.read_bytes()
with zipfile.ZipFile(OUTPUT, "x", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
    for name, data in payload.items():
        archive.writestr(name, data)
    archive.writestr(MANIFEST.name, manifest_bytes)
with zipfile.ZipFile(OUTPUT) as archive:
    assert set(archive.namelist()) == set(payload) | {MANIFEST.name}
    assert len(archive.namelist()) == len(payload) + 1
    for name, data in payload.items():
        assert archive.read(name) == data, name
    assert archive.read(MANIFEST.name) == manifest_bytes
    assert archive.testzip() is None
output_bytes = OUTPUT.read_bytes()
assert INPUT.read_bytes() == original
receipt = {
    "kind": "RECIPIENT_REVIEW_DELIVERY_RECEIPT",
    "recipient": None,
    "status": "PARTIAL_OFFLINE_PREPARATION_ACCEPTED_SOURCE_CORRECTIONS_REQUIRED",
    "zip": {"path": str(OUTPUT), "bytes": len(output_bytes), "sha256": digest(output_bytes)},
    "payload_count": len(payload),
    "manifest_sha256": digest(manifest_bytes),
    "readback_exact_set_bytes_sha_crc": True,
    "original_input_zip_unchanged": True,
    "received_files_unchanged": len(names),
    "packaging_only_snapshot_seconds_before_receipt_write": time.monotonic() - START,
    "scope": "Reviewer packaging only; not original preparation time or native runtime; before receipt write and tool return",
    "received_code_and_tests_executed": 0,
    "native_approved": False,
}
create_json(RECEIPT, receipt)
assert json.loads(RECEIPT.read_text(encoding="utf-8")) == receipt
print(json.dumps(receipt, ensure_ascii=False))
