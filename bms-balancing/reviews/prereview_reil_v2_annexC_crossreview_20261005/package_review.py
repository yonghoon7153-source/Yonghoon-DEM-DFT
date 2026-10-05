"""Package only this review and the received document bundle; no PDF/data payload."""
import ast
import hashlib
import json
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parent
archive = R.parent / "REIL_V2_ANNEX_C_CROSSREVIEW_20261005.zip"
if archive.exists():
    raise FileExistsError(archive)
names = [
    "README_KO.md", "REIL_V2_ANNEX_C_CROSSREVIEW_20261005.md", "REPLY_KO.md", "DECISION.json",
    "independent_document_checks.py", "package_review.py",
    "evidence/intake.json", "evidence/remote_identity.json", "evidence/independent_checks.json",
    "input_bundle/README_KO.md", "input_bundle/REVIEW_KO.md", "input_bundle/CLAUDE_REPLY_KO.md",
    "input_bundle/DECISION.json", "input_bundle/RECEIVED_SNAPSHOT.json", "input_bundle/REVIEW_CHECKS.json",
    "input_bundle/reviewer_document_checks.py", "input_bundle/PACKAGE_MANIFEST.json",
]

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def readj(name):
    return json.loads((R/name).read_text(encoding="utf8"))

evidence = readj("evidence/independent_checks.json")
decision = readj("DECISION.json")
assert evidence["all_pass"] and evidence["check_count"] == 63
assert not decision["execution_authorized"] and not decision["new_P1_found_in_scope"]
assert all(x["correction_status"].startswith("NOT_VERIFIED") for x in decision["findings"])
assert all(x["passed"] for x in evidence["checks"])
assert len(names) == len(set(names))
for name in names:
    b = (R/name).read_bytes()
    if name.endswith(".json"):
        json.loads(b)
    if name in ("independent_document_checks.py", "package_review.py"):
        ast.parse(b.decode("utf8"))
    if name.endswith(".md"):
        assert b.count(b"```") % 2 == 0, name
intake = readj("evidence/intake.json")
source_zip = Path(intake["input_zip"]["path"])
assert sha(source_zip.read_bytes()) == intake["input_zip"]["sha256"]
with zipfile.ZipFile(source_zip) as z:
    for name in z.namelist():
        assert (R/"input_bundle"/name).read_bytes() == z.read(name)

manifest = dict(schema="review_delivery_manifest/v1", scope="Review artifacts and original review documents only",
                excludes=["PDF", "PDF extracted text", "PNG renders", "workbooks", "research source", "notebooks"],
                payload=[dict(path=n, bytes=(R/n).stat().st_size, sha256=sha((R/n).read_bytes())) for n in names])
(R/"PACKAGE_MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED) as z:
    for name in names+["PACKAGE_MANIFEST.json"]:
        z.write(R/name, name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and len(z.namelist()) == len(set(z.namelist())) == 18
    assert set(z.namelist()) == set(names)|{"PACKAGE_MANIFEST.json"}
    for row in manifest["payload"]:
        b=z.read(row["path"])
        assert len(b)==row["bytes"] and sha(b)==row["sha256"]
receipt = dict(zip=str(archive), bytes=archive.stat().st_size, sha256=sha(archive.read_bytes()),
               entries=18, payload_checks=True, original_bundle_unchanged=True,
               execution_authorized=False)
(R/"evidence/delivery_receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
print(json.dumps(receipt, ensure_ascii=False))
