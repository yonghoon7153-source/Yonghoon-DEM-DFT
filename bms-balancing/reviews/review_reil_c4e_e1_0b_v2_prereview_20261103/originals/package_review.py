"""Reviewer-owned byte/JSON/ZIP packaging. Does not import reviewed programs."""
import hashlib
import json
import stat
import zipfile
import zlib
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / "reil_c4e_e1_0b_prereview_20261030"
ARCHIVE = "REIL_C4E_E1_0B_V2_PREREVIEW_20261103.zip"
DECISION = "E1_0B_PREREVIEW_ACCEPTED_FOR_USER_APPROVAL_NOT_EXECUTION"

def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def save(name, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with (ROOT / name).open("xb") as f:
        f.write(data)
    assert (ROOT / name).read_bytes() == data
    return identity(data)

def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

audit = read_json(ROOT / "STATIC_AUDIT.json")
decision = read_json(ROOT / "REVIEW_DECISION.json")
assert audit["result"] == "STATIC_DATA_MATCH" and not audit["mismatches"]
assert decision["decision"] == DECISION and not decision["new_blocking_findings"]
assert read_json(ROOT / "BRANCH_AT_CLOSE.json")["match"] is True
assert not read_json(ROOT / "L29_L30_STATIC_REVIEW.json")["conclusion"]["blocking_findings"]

prior_manifest = read_json(PRIOR / "PACKAGE_MANIFEST.json")
prior_rows = {r["path"]: r for r in prior_manifest["files"]}
prior_names = ["REVIEW_DECISION.json", "REVIEW_KO.txt", "Q4_STATIC_REVIEW.json",
    "source/bms-balancing/docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v6_20261030.py.txt",
    "source/bms-balancing/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v6_20261030.py.txt",
    "source/bms-balancing/docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md"]
pairs = []
for name in prior_names:
    source = PRIOR / name
    data = source.read_bytes()
    ident = identity(data)
    expected = prior_rows[name]
    assert ident == {k: expected[k] for k in ("bytes", "sha256")}, name
    destination = ROOT / "basis/prior_review" / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("xb") as f:
        f.write(data)
    assert destination.read_bytes() == data
    pairs.append((source, ident, "prior_review_original_read_only"))
prior_zip = PRIOR / "REIL_C4E_E1_0B_PREREVIEW_20261030.zip"
prior_data = prior_zip.read_bytes()
prior_id = identity(prior_data)
assert prior_id == {"bytes":735110,"sha256":"08fdc4587f2f95b60aa5594d2557f2a7fd792744f70f40957e7af34823e48805"}
with (ROOT / "basis/prior_review" / prior_zip.name).open("xb") as f:
    f.write(prior_data)
pairs.append((prior_zip, prior_id, "prior_review_archive_read_only"))

for row in read_json(ROOT / "SOURCE_IDENTITIES.json"):
    pairs.append((ROOT / "source" / row["path"], row, "pinned_Git_blob_capture"))
for row in audit["attachments"]:
    pairs.append((Path(row["local_path"]), row, "user_supplied_local_attachment"))
for row in audit["unchanged_inherited_sources"]:
    pairs.append((ROOT / row["captured"], row, "compare_proven_unchanged_capture"))
assert len({str(p).casefold() for p, _, _ in pairs}) == len(pairs)
observed = []
for path, expected, scope in pairs:
    ident = identity(path.read_bytes())
    assert ident == {k:expected[k] for k in ("bytes", "sha256")}, str(path)
    observed.append({"path":str(path), **ident, "scope":scope, "matches_recorded":True})
save("SELECTED_INPUTS_POST_REVIEW.json", {"kind":"LOCAL_REVIEW_INPUT_IDENTITY_READBACK", "count":len(observed), "all_match":True, "files":observed, "scope":"Named local attachment/original/capture paths only. Captures and prior archive are not extra remote originals; no remote working-tree remeasurement."})

excluded = {ARCHIVE, "PACKAGE_MANIFEST.json", "DELIVERY_RECEIPT.json", "PACKAGE_TOOL_RETURN.json", "PACKAGE_READBACK.json"}
payloads = {}
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.name not in excluded:
        assert not path.is_symlink(), str(path)
        name = path.relative_to(ROOT).as_posix()
        parts = PurePosixPath(name)
        assert not parts.is_absolute() and ".." not in parts.parts and ":" not in name and "\\" not in name
        payloads[name] = path.read_bytes()
assert len({n.casefold() for n in payloads}) == len(payloads)
rows = [{"path":n, **identity(b), "crc32":f"{zlib.crc32(b)&0xffffffff:08x}"} for n,b in payloads.items()]
manifest_id = save("PACKAGE_MANIFEST.json", {"kind":"REVIEW_PACKAGE_MANIFEST", "payload_count":len(rows), "files":rows, "received_program_execution":0, "decision":DECISION})
entries = {**payloads, "PACKAGE_MANIFEST.json":(ROOT / "PACKAGE_MANIFEST.json").read_bytes()}
with zipfile.ZipFile(ROOT / ARCHIVE, "x", compression=zipfile.ZIP_DEFLATED) as archive:
    for name, data in entries.items():
        archive.writestr(name, data)
with zipfile.ZipFile(ROOT / ARCHIVE) as archive:
    assert len(archive.namelist()) == len(entries) and set(archive.namelist()) == set(entries)
    assert len({n.casefold() for n in archive.namelist()}) == len(entries)
    for info in archive.infolist():
        assert not stat.S_ISLNK(info.external_attr >> 16)
        actual = archive.read(info.filename)
        assert actual == entries[info.filename] and info.file_size == len(actual)
        assert info.CRC == zlib.crc32(actual) & 0xffffffff
for path, expected, scope in pairs:
    assert identity(path.read_bytes()) == {k:expected[k] for k in ("bytes", "sha256")}
archive_id = identity((ROOT / ARCHIVE).read_bytes())
receipt = {"kind":"E1_0B_V2_PREREVIEW_DELIVERY_RECEIPT", "recipient":None,
    "archive":{"name":ARCHIVE, **archive_id}, "manifest":{"name":"PACKAGE_MANIFEST.json", **manifest_id},
    "payload_count":len(rows), "entries":len(entries),
    "verification":"Exact set, safe unique paths, decompressed bytes/size/SHA256 and independently computed CRC32 matched",
    "selected_local_input_paths_rechecked":len(pairs), "all_selected_match":True,
    "selected_scope":"Local attachments, captured Git blobs, prior evidence; no remote original count or remote working-tree audit",
    "pinned_commit":decision["pinned_commit"], "decision":DECISION, "E1_0B_N1":"STATICALLY_CLOSED",
    "new_required_findings":0, "functional_tests":0, "received_program_execution":0,
    "execution_approved":False, "whole_work_elapsed_claim":None,
    "boundary":"After archive verification and selected input rehash; before receipt write/readback and tool return"}
receipt_id = save("DELIVERY_RECEIPT.json", receipt)
print(json.dumps({"kind":"E1_0B_V2_REVIEW_PACKAGE_RETURN", "archive":{"name":ARCHIVE, **archive_id},
    "manifest":manifest_id, "receipt":receipt_id, "payload_count":len(rows), "entries":len(entries),
    "selected_local_input_paths_matched":len(pairs), "decision":DECISION, "functional_tests":0,
    "received_program_execution":0, "execution_approved":False,
    "boundary":"After receipt write/readback; before tool return and its subsequent transcription"}, ensure_ascii=False))
