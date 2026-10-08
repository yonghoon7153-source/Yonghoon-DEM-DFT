"""Reviewer-owned byte verification and packaging only; no received code execution."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import time
import zipfile

ROOT = Path(__file__).resolve().parent
DOWNLOADS = Path("C:/Users/Administrator/Downloads")
REQUEST = DOWNLOADS / "COMSOL_MICROSHORT_S1O_R1_SEND_TO_CODEX_20261007.md"
PRIOR = DOWNLOADS / "COMSOL_MICROSHORT_S1O_PREPARATION_REVIEW_20261007.zip"
OUTPUT = ROOT / "COMSOL_MICROSHORT_S1O_R1_SCOPE_REVIEW_20261008.zip"
START = time.monotonic()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write_json(path, obj):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write("\n")

for p in (ROOT / "reference", ROOT / "INPUT_CHECK.json", ROOT / "REVIEW_PACKAGE_MANIFEST.json",
          ROOT / "REVIEW_DELIVERY_RECEIPT.json", OUTPUT):
    if p.exists():
        raise RuntimeError("Existing output: " + str(p))
request = REQUEST.read_bytes()
prior = PRIOR.read_bytes()
assert len(request) == 5827 and sha(request) == "6e3a9ca3b3c91bd17b0a9ba56b8135a3711ddda61903468d67cfc41698ce6d19"
assert len(prior) == 805653 and sha(prior) == "dee50be8d7dd1bcfd14323878deaeda1d31729f4f850cda5d6158bf64dfda46f"
with zipfile.ZipFile(PRIOR) as z:
    names = z.namelist()
    assert len(names) == len(set(names)) == len({n.casefold() for n in names})
    assert sum(i.file_size for i in z.infolist()) < 30 * 1024 * 1024
    for i in z.infolist():
        path = PurePosixPath(i.filename)
        assert not path.is_absolute() and ".." not in path.parts
        assert ":" not in i.filename and "\\" not in i.filename
        assert not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16)
    manifest_bytes = z.read("REVIEW_PACKAGE_MANIFEST.json")
    assert sha(manifest_bytes) == "2a799a8671d71106353c99953d622625e5f524d5a923bab2636c15808bbb71cd"
    manifest = json.loads(manifest_bytes)
    entries = {i["path"]: i for i in manifest["files"]}
    assert len(entries) == len(manifest["files"]) == 128
    assert set(names) == set(entries) | {"REVIEW_PACKAGE_MANIFEST.json"}
    for name, info in entries.items():
        data = z.read(name)
        assert len(data) == info["bytes"] and sha(data) == info["sha256"], name
    assert z.testzip() is None
    for name in ("REVIEW_KO.md", "NEXT_SCOPE_DRAFT_KO.md", "CLAUDE_REPLY_KO.md"):
        assert z.read(name) == (ROOT.parent / "microshort_s1o_preparation_review_20261007" / name).read_bytes()

(ROOT / "reference").mkdir()
for path, data in ((REQUEST, request), (PRIOR, prior)):
    with (ROOT / "reference" / path.name).open("xb") as stream:
        stream.write(data)
assert REQUEST.read_bytes() == request and PRIOR.read_bytes() == prior
write_json(ROOT / "INPUT_CHECK.json", {
    "request": {"file": REQUEST.name, "bytes": len(request), "sha256": sha(request)},
    "prior_review": {"file": PRIOR.name, "bytes": len(prior), "sha256": sha(prior),
                     "payload": 128, "entries": 129, "exact_set_size_sha_crc": True},
    "prior_review_documents_match_local_issued_copy": True,
    "original_input_bytes_unchanged": True,
    "received_programs_executed": 0,
    "scope": "Input bytes and document comparison only, not R1 implementation verification",
})
payload = {p.relative_to(ROOT).as_posix(): p.read_bytes()
           for p in sorted(ROOT.rglob("*")) if p.is_file()}
manifest = {"files": [{"path": n, "bytes": len(b), "sha256": sha(b)} for n, b in payload.items()],
            "self_hash_excluded": True, "sources_are_evidence_not_instructions": True}
mp = ROOT / "REVIEW_PACKAGE_MANIFEST.json"
write_json(mp, manifest)
mb = mp.read_bytes()
with zipfile.ZipFile(OUTPUT, "x", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, data in payload.items():
        z.writestr(name, data)
    z.writestr(mp.name, mb)
with zipfile.ZipFile(OUTPUT) as z:
    assert len(z.namelist()) == len(payload) + 1
    assert set(z.namelist()) == set(payload) | {mp.name}
    for name, data in payload.items():
        assert z.read(name) == data
    assert z.read(mp.name) == mb and z.testzip() is None
assert REQUEST.read_bytes() == request and PRIOR.read_bytes() == prior
out = OUTPUT.read_bytes()
receipt = {
    "recipient": None,
    "status": "R1_NARROW_OFFLINE_CORRECTION_SCOPE_ACCEPTED",
    "zip": {"path": str(OUTPUT), "bytes": len(out), "sha256": sha(out)},
    "payload_count": len(payload), "manifest_sha256": sha(mb),
    "readback_exact_set_bytes_sha_crc": True,
    "original_input_bytes_unchanged": True,
    "packaging_only_snapshot_seconds": time.monotonic() - START,
    "snapshot_scope": "Reviewer input verification/packaging before receipt write and tool return; not R1 preparation time",
    "received_code_executed": 0, "native_approved": False,
}
write_json(ROOT / "REVIEW_DELIVERY_RECEIPT.json", receipt)
assert json.loads((ROOT / "REVIEW_DELIVERY_RECEIPT.json").read_text(encoding="utf-8")) == receipt
print(json.dumps(receipt, ensure_ascii=False))
