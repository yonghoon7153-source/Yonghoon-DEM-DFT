"""Read-only source identity and source diffs; owned review outputs only."""
import hashlib,json,difflib,platform,sys
from pathlib import Path
R=Path(__file__).resolve().parent; OLD=R.parent/"rint_g1_lhs_network_review_20261005"; S=R/"source"
base_manifest=R/'inputs/base_source_manifest.json'
old=json.loads((base_manifest if base_manifest.is_file() else OLD/"source_manifest.json").read_text(encoding="utf8"))
compare=json.loads((R/"compare_metadata.json").read_text(encoding="utf8"))
assert compare["status"]=="ahead" and len(compare["files"])<300
expect={x["path"]:x["git_blob_expected"] for x in old["files"]}
changes={x["filename"]:x for x in compare["files"]}
for x in compare["files"]:
    if x["status"]=="removed":expect.pop(x["filename"],None)
    else: expect[x["filename"]]=x["sha"]
fetched=set()
for ledger in ('acquisition.json','fixture_acquisition.json'):
    for x in json.loads((R/ledger).read_text(encoding="utf8"))["files"]:
        expect[x["path"]]=x["sha"];fetched.add(x['path'])
rows=[]
for p in sorted(S.rglob("*")):
    if not p.is_file():continue
    path=p.relative_to(S).as_posix();b=p.read_bytes()
    actual=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    # Mechanical transport cleanup only if removing one added LF exactly recovers the pinned Git blob.
    if actual!=expect.get(path) and '--normalize-transport' in sys.argv and b.endswith(b'\n'):
        clean=b[:-1]
        recovered=hashlib.sha1(b'blob '+str(len(clean)).encode()+b'\0'+clean).hexdigest()
        if recovered==expect.get(path):
            p.write_bytes(clean); b=clean; actual=recovered
    rows.append(dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),
        git_blob=actual,expected=expect.get(path),verified=actual==expect.get(path),
        origin="fetched_at_pin" if path in fetched else "unchanged_in_complete_compare"))
bad=[x for x in rows if not x["verified"]]
(R/"source_manifest.json").write_text(json.dumps(dict(commit=compare["head"],base=compare["base"],files=rows,
    identity_method="Old verified blob + complete 138-file ancestor comparison; changed/new fetched at new pin.",
    platform=platform.platform()),ensure_ascii=False,indent=2),encoding="utf8")
D=R/"diffs";D.mkdir(exist_ok=True)
for path in changes:
    a,b=OLD/"source"/path,S/path
    if not a.is_file() or not b.is_file():continue
    if path.startswith(("scripts/","webapp/")):
        t="".join(difflib.unified_diff(a.read_text(encoding="utf8").splitlines(True),b.read_text(encoding="utf8").splitlines(True),
            fromfile="old/"+path,tofile="new/"+path))
        (D/(path.replace("/","__")+".diff")).write_text(t,encoding="utf8")
print(json.dumps(dict(files=len(rows),verified=len(rows)-len(bad),bad=bad),ensure_ascii=False))
raise SystemExit(bool(bad))
