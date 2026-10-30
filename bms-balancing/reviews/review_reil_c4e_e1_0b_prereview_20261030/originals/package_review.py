"""Reviewer-authored data packaging only. Never imports any reviewed target."""
import hashlib, json, stat, zipfile, zlib
from pathlib import Path, PurePosixPath
ROOT = Path(__file__).resolve().parent
ARCHIVE = "REIL_C4E_E1_0B_PREREVIEW_20261030.zip"
def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
def save(name, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with (ROOT/name).open("xb") as f:
        f.write(data)
    assert (ROOT/name).read_bytes() == data
    return identity(data)
audit = json.loads((ROOT/"STATIC_AUDIT.json").read_text(encoding="utf-8"))
sources = json.loads((ROOT/"SOURCE_IDENTITIES.json").read_text(encoding="utf-8"))
pairs = []
for row in sources:
    pairs.append((ROOT/"source"/row["path"], row, "pinned_Git_blob_capture"))
for row in audit["attachments"]:
    pairs.append((Path(row["path"]), row, "user_supplied_local_attachment"))
for row in audit["local_current_counterparts"]:
    pairs.append((ROOT/row["captured"], row, "unchanged_at_pin_captured_basis"))
observed = []
for path, expected, scope in pairs:
    ident = identity(path.read_bytes())
    assert ident == {k:expected[k] for k in ("bytes","sha256")}, str(path)
    observed.append({"path":str(path), **ident, "scope":scope, "matches_recorded":True})
save("SELECTED_INPUTS_POST_REVIEW.json", {"kind":"LOCAL_REVIEW_INPUT_IDENTITY_READBACK", "count":len(observed), "all_match":True, "files":observed, "scope":"Only named local attachments/captured bytes; no remote working-tree remeasurement"})
excluded = {ARCHIVE, "PACKAGE_MANIFEST.json", "DELIVERY_RECEIPT.json", "PACKAGE_TOOL_RETURN.json"}
payloads = {}
for path in sorted(ROOT.rglob("*")):
    if path.is_file() and path.name not in excluded:
        assert not path.is_symlink(), str(path)
        name = path.relative_to(ROOT).as_posix()
        p = PurePosixPath(name)
        assert not p.is_absolute() and ".." not in p.parts and ":" not in name and "\\" not in name
        payloads[name] = path.read_bytes()
assert len({n.casefold() for n in payloads}) == len(payloads)
rows = [{"path":n, **identity(b), "crc32":f"{zlib.crc32(b)&0xffffffff:08x}"} for n,b in payloads.items()]
manifest_id = save("PACKAGE_MANIFEST.json", {"kind":"REVIEW_PACKAGE_MANIFEST", "payload_count":len(rows), "files":rows, "target_execution":0, "decision":"E1_0B_PREREVIEW_CHANGES_REQUIRED_BEFORE_APPROVAL"})
archive_entries = {**payloads, "PACKAGE_MANIFEST.json":(ROOT/"PACKAGE_MANIFEST.json").read_bytes()}
with zipfile.ZipFile(ROOT/ARCHIVE, "x", compression=zipfile.ZIP_DEFLATED) as z:
    for name, data in archive_entries.items():
        z.writestr(name,data)
with zipfile.ZipFile(ROOT/ARCHIVE) as z:
    assert set(z.namelist()) == set(archive_entries)
    assert len(z.namelist()) == len(archive_entries)
    assert len({n.casefold() for n in z.namelist()}) == len(z.namelist())
    for info in z.infolist():
        assert not stat.S_ISLNK(info.external_attr >> 16)
        expected = archive_entries[info.filename]
        actual = z.read(info.filename)
        assert actual == expected and info.file_size == len(expected)
        assert info.CRC == zlib.crc32(actual)&0xffffffff
for path, expected, scope in pairs:
    assert identity(path.read_bytes()) == {k:expected[k] for k in ("bytes","sha256")}
archive_id = identity((ROOT/ARCHIVE).read_bytes())
receipt = {"kind":"E1_0B_PREREVIEW_DELIVERY_RECEIPT", "recipient":None, "archive":{"name":ARCHIVE,**archive_id}, "manifest":{"name":"PACKAGE_MANIFEST.json",**manifest_id}, "payload_count":len(rows), "entries":len(archive_entries), "verification":"Exact set, safe unique paths, sizes, decompressed bytes/SHA256 and independently computed CRC32 match", "selected_local_inputs_rechecked":len(pairs), "all_selected_match":True, "pinned_commit":"90a842a9df9eb676c20ce1b9d4babf0cf0c5d637", "decision":"E1_0B_PREREVIEW_CHANGES_REQUIRED_BEFORE_APPROVAL", "required_findings":1, "functional_tests":0, "received_program_execution":0, "execution_approved":False, "whole_work_elapsed_claim":None, "boundary":"After archive verification and selected local input rehash; before receipt write and tool return"}
receipt_id = save("DELIVERY_RECEIPT.json", receipt)
print(json.dumps({"kind":"E1_0B_REVIEW_PACKAGE_RETURN", "archive":{"name":ARCHIVE,**archive_id}, "manifest":manifest_id, "receipt":receipt_id, "payloads":len(rows), "entries":len(archive_entries), "selected_local_inputs_matched":len(pairs), "decision":receipt["decision"], "functional_tests":0, "received_program_execution":0, "boundary":"After receipt write/readback; before tool return and subsequent transcription"},ensure_ascii=False))
