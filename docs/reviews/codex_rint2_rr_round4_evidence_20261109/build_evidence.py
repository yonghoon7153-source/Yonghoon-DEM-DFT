"""Package read-only review evidence; excludes scratch Git/work directories."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent/"codex_rint2_rr_round4_1f9f3607eb2f_independent_20261109.zip"
full={"input","package","reference_round3"}
flat={"arm_contract","docs_tests","resume_attack"}
sub={"arm_contract":{"original_replay","closure_replay"},
     "resume_attack":{"frozen_cases"},"docs_tests":{"m56_synthetic"}}
files=[]
for p in ROOT.rglob("*"):
    if not p.is_file():continue
    rel=p.relative_to(ROOT)
    if any(x in (".git","__pycache__") for x in rel.parts):continue
    if len(rel.parts)==1:
        if p.name in ("SHA256SUMS","delivery.json"):continue
        if p.suffix in (".md",".py",".json"):files.append(p)
    elif rel.parts[0] in full:files.append(p)
    elif rel.parts[0] in flat:
        if len(rel.parts)==2 or rel.parts[1] in sub.get(rel.parts[0],set()):
            files.append(p)
files=sorted(files,key=lambda p:p.relative_to(ROOT).as_posix())
sha=lambda b:hashlib.sha256(b).hexdigest()
manifest="".join(sha(p.read_bytes())+"  "+p.relative_to(ROOT).as_posix()+"\n" for p in files)
(ROOT/"SHA256SUMS").write_text(manifest,encoding="utf-8",newline="\n")
with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files+[ROOT/"SHA256SUMS"]:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for line in z.read("SHA256SUMS").decode().splitlines():
        h,n=line.split("  ",1)
        assert sha(z.read(n))==h,n
    assert not any("/.git/" in n or "/scratch_" in n for n in names)
result={"file":str(OUT),"bytes":OUT.stat().st_size,"sha256":sha(OUT.read_bytes()),
        "files":len(files)+1,"manifest_entries":len(files),"crc":"PASS","all_manifest_hashes":"PASS"}
(ROOT/"delivery.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
OUT.with_suffix(".sha256").write_text(result["sha256"]+"  "+OUT.name+"\n",encoding="utf-8")
print(json.dumps(result))

