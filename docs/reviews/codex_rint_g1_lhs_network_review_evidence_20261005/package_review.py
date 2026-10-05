"""Package owned review artifacts; no production mutation or campaign execution."""
import hashlib,json,re,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
R=Path(__file__).resolve().parent
NAME="codex_rint_g1_lhs_network_review_20261005.zip"
report=R/"codex_review_rint_g1_lhs_network_20261005.md"
body=report.read_text(encoding="utf-8")
manifest=json.loads((R/"source_manifest.json").read_text(encoding="utf-8"))
assert len(manifest["files"])==223 and all(x["verified"] for x in manifest["files"])
for file,line in re.findall(r"30c8205c5efb3873ae6fa856881fa184bd041d4d/([^)#]+)#L(\d+)",body):
    src=R/"source"/file
    assert src.is_file(),file
    assert 1<=int(line)<=len(src.read_text(encoding="utf-8").splitlines()),(file,line)
for q in range(1,12):
    assert re.search(r"^### Q"+str(q)+r"\.",body,re.M),q
for i in range(1,11):
    assert f"### RGL-{i:02d} " in body,i
assert "{{src:" not in body
exclude_names={NAME,"package_manifest.json","package_receipt.json",NAME+".sha256"}
files=[]
for p in sorted(R.rglob("*")):
    if not p.is_file() or p.name in exclude_names: continue
    rel=p.relative_to(R)
    if any(x in {"__pycache__","mplcache",".git"} for x in rel.parts): continue
    if p.suffix in {".pyc",".pyo"}: continue
    files.append(p)
rows=[{"path":p.relative_to(R).as_posix(),"bytes":p.stat().st_size,
       "sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
pm={"schema":"review_package_manifest/v1","commit":manifest["commit"],
    "created_utc":datetime.now(timezone.utc).isoformat(),
    "note":"Self excluded; ZIP receipt and SHA sidecar are outside ZIP.","files":rows}
(R/"package_manifest.json").write_text(json.dumps(pm,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
with zipfile.ZipFile(R/NAME,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:
        z.write(p,p.relative_to(R).as_posix())
    z.write(R/"package_manifest.json","package_manifest.json")
with zipfile.ZipFile(R/NAME) as z:
    assert z.testzip() is None
    assert len(set(z.namelist()))==len(z.namelist())
    for name in z.namelist():
        p=PurePosixPath(name)
        assert not p.is_absolute() and ".." not in p.parts and ":" not in name and "\\" not in name,name
    got=json.loads(z.read("package_manifest.json"))
    for row in got["files"]:
        data=z.read(row["path"])
        assert len(data)==row["bytes"]
        assert hashlib.sha256(data).hexdigest()==row["sha256"],row["path"]
    entries=len(z.namelist())
b=(R/NAME).read_bytes()
receipt={"schema":"review_package_receipt/v1","zip":NAME,"bytes":len(b),
    "sha256":hashlib.sha256(b).hexdigest(),"entries":entries,
    "manifest_files_verified":len(rows),"crc":"PASS","entry_path_hazards":[],
    "source_git_blobs_verified":223,"commit":manifest["commit"],
    "report_sha256":hashlib.sha256(report.read_bytes()).hexdigest(),
    "report_source_links_checked":len(re.findall(r"#L\d+",body)),
    "production_modified":False,"large_campaign_executed":False}
(R/"package_receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
(R/(NAME+".sha256")).write_text(receipt["sha256"]+"  "+NAME+"\n",encoding="utf-8")
print(json.dumps(receipt,ensure_ascii=False,indent=2))

