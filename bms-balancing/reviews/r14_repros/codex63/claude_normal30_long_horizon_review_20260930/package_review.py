"""Package only this review, with exact payload hashes. No supplied code execution."""
import hashlib
import json
import stat
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
destination = root / "CLAUDE_NORMAL30_LONG_HORIZON_RECIPIENT_REVIEW_20260930.zip"
if destination.exists():
    raise FileExistsError(destination)
names = ["REVIEW_KO.md", "CLAUDE_REPLY_KO.md", "NEXT_CODEX_INSTRUCTION_KO.md", "DECISION.json",
         "CALCULATION_AUDIT.json", "SOURCE_IDENTITIES.json", "review_arithmetic.py",
         "REVIEW_EXECUTION_NOTE.md", "package_review.py"]
payload = {n: (root/n).read_bytes() for n in names}
original = Path("C:/Users/Administrator/Downloads/CLAUDE_REPLY_NORMAL30_LONG_HORIZON_KO_v2.md")
payload["received/"+original.name] = original.read_bytes()
sources = json.loads(payload["SOURCE_IDENTITIES.json"])
for info in sources["after"]:
    p = Path(info["path"])
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    assert p.stat().st_size == info["bytes"] and h.hexdigest() == info["sha256"], p
manifest = {n: {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()} for n,b in sorted(payload.items())}
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2)+"\n").encode("utf-8")
with zipfile.ZipFile(destination,"x",compression=zipfile.ZIP_DEFLATED) as z:
    for name,data in sorted(payload.items()):
        z.writestr(name,data)
    z.writestr("MANIFEST.json",manifest_bytes)
with zipfile.ZipFile(destination) as z:
    assert z.testzip() is None
    listed = z.namelist()
    assert len(listed)==len(set(listed))==len({x.casefold() for x in listed})
    assert set(listed)==set(payload)|{"MANIFEST.json"}
    for info in z.infolist():
        assert not info.filename.startswith(("/","\\")) and ".." not in info.filename.split("/")
        assert not stat.S_ISLNK(info.external_attr >> 16)
    assert z.read("MANIFEST.json")==manifest_bytes
    for name,item in manifest.items():
        raw=z.read(name)
        assert len(raw)==item["bytes"] and hashlib.sha256(raw).hexdigest()==item["sha256"]
receipt={"scope":"New recipient interpretation review package; no execution approval",
         "zip":destination.name,"bytes":destination.stat().st_size,
         "sha256":hashlib.sha256(destination.read_bytes()).hexdigest(),
         "payload_count":len(payload),"total_entries":len(payload)+1,
         "manifest_sha256":hashlib.sha256(manifest_bytes).hexdigest(),
         "exact_set_size_sha_crc_path_link_checks":"PASS",
         "selected_input_files_rechecked_unchanged":len(sources["after"]),
         "COMSOL_calls":0,"native60_approved":False,"long_run_approved":False,
         "recipient_verification_of_this_new_package":None}
(root/"REVIEW_PACKAGE_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps(receipt,ensure_ascii=False))
