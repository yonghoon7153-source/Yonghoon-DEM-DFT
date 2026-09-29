"""Package only explicit review artifacts; verify CRC and every member SHA256."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent
FILES=[
    "README.md","SOURCES.md","review.md","review_status.json",
    "bundle_original.md","bundle_lf.md","request_extracted.md","prereg_v23_extracted.md",
    "submitted_v22_to_v23.diff","audit_round9.py","audit_results.json","package_evidence.py",
    "baseline/prereg_v22.md","baseline/prior_r8_verdict.md","baseline/prior_r8_audit_results.json",
]
def sha(data):
    return hashlib.sha256(data).hexdigest()
records={}
for name in FILES:
    data=(ROOT/name).read_bytes()
    records[name]={"bytes":len(data),"sha256":sha(data)}
manifest={"schema":"review_evidence_manifest/v1","review":"mixer LH round 9 document closure",
          "scope":"No simulations, production changes, scheduler access or run authorization.",
          "files":records,"note":"MANIFEST.json excludes itself."}
(ROOT/"MANIFEST.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
dest=ROOT.parent/"codex_mixer_highbo_round9_prereg_20260929.zip"
members=FILES+["MANIFEST.json"]
with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(ROOT/name,arcname=name)
with zipfile.ZipFile(dest) as archive:
    assert len(archive.namelist())==len(members)
    assert set(archive.namelist())==set(members)
    assert archive.testzip() is None
    for name,item in records.items():
        data=archive.read(name)
        assert sha(data)==item["sha256"] and len(data)==item["bytes"]
    assert archive.read("MANIFEST.json")==(ROOT/"MANIFEST.json").read_bytes()
print(json.dumps({"zip":str(dest),"bytes":dest.stat().st_size,
                  "sha256":sha(dest.read_bytes()),"entries":len(members),
                  "verification":"CRC + member set + all SHA256 PASS"},ensure_ascii=False,indent=2))

