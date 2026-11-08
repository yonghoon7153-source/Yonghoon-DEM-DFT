"""Offline verify saved read-only GitHub tree responses against actual package bytes.
This verifies binding to the fetched pin, not authenticity of arbitrary edited evidence.
"""
import json, hashlib
from pathlib import Path
root=Path(__file__).resolve().parent
data=json.loads((root/"remote_provenance.json").read_text(encoding="utf-8"))
pin=(root/"package/PIN.txt").read_text().splitlines()[0]
assert data["commit"]["sha"]==pin
trees=data["trees"]
assert not data["errors"] and not data["mismatch"]
errors=[]
count=0
for p in (root/"package/repo").rglob("*"):
    if not p.is_file(): continue
    rel=p.relative_to(root/"package/repo").as_posix()
    d,_,n=rel.rpartition("/")
    t=trees.get(d,{})
    entry=next((e for e in t.get("tree",[]) if e["path"]==n),None)
    raw=p.read_bytes()
    blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    if not entry or entry["type"]!="blob" or entry["sha"]!=blob: errors.append(rel)
    count+=1
for d,t in trees.items():
    if not d: continue
    parent,_,name=d.rpartition("/")
    pe=next(e for e in trees[parent]["tree"] if e["path"]==name)
    assert pe["sha"]==t["sha"],d
assert count==403 and not errors,(count,errors)
delta=json.loads((root/"dependency_delta.json").read_text())
old={e["path"]:e["sha"] for e in delta["old_scripts"]["tree"]}
changed=[]
same=[]
for p in (root/"package/repo/scripts").glob("*"):
    if not p.is_file():continue
    raw=p.read_bytes();h=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
    (same if old[p.name]==h else changed).append(p.name)
assert len(same)==26 and sorted(changed)==["rint_r_chain.py","test_rint_r_chain.py"]
print(json.dumps({"pin":pin,"repo_blobs":count,"mismatch":errors,"unchanged_dependencies":len(same),"changed":changed}))

