"""Create a new reviewer reply archive from static documents only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,zipfile,stat
ROOT=Path(__file__).resolve().parent
ZIP=ROOT.parent/"COMSOL_MICROSHORT_S1O_V2_REVIEW_20261007.zip"
MANIFEST=ROOT/"PACKAGE_MANIFEST.json"
RECEIPT=ROOT/"REVIEW_DELIVERY_RECEIPT.json"
AFTER=ROOT/"SELECTED_INPUTS_AFTER.json"
def sha(data): return hashlib.sha256(data).hexdigest()
def encode(value): return (json.dumps(value,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
def save(path,data):
    with path.open("xb") as stream: stream.write(data)
for path in (ZIP,MANIFEST,RECEIPT,AFTER):
    if path.exists(): raise RuntimeError("Existing output "+str(path))
items=json.loads((ROOT/"INPUT_IDENTITIES.json").read_text(encoding="utf-8"))
raw=[]
for item in items:
    data=Path(item["path"]).read_bytes()
    if len(data)!=item["bytes"] or sha(data)!=item["sha256"]: raise RuntimeError("Input changed")
    raw.append(data)
save(AFTER,encode({"scope":"Five named local inputs only, not machine-wide preservation","unchanged":True,"files":items}))
payload={}
for path in sorted(ROOT.rglob("*")):
    if path.is_symlink(): raise RuntimeError("Symlink refused")
    if not path.is_file(): continue
    name=path.relative_to(ROOT).as_posix()
    if name in ("PACKAGE_MANIFEST.json","REVIEW_DELIVERY_RECEIPT.json"): continue
    if path.suffix==".pyc" or "__pycache__" in path.parts: raise RuntimeError("Bytecode refused")
    data=path.read_bytes()
    if path.suffix==".json": json.loads(data)
    payload[name]=data
for name,data in zip([
    "reference/ATTACHED_V2_REQUEST.md",
    "basis/V1_REQUEST.md",
    "basis/PRIOR_ADDENDUM_KO.md",
    "basis/PRIOR_REVIEW_KO.md",
    "basis/PRIOR_DECISION.json",
],raw):
    if name in payload: raise RuntimeError("Member collision")
    payload[name]=data
if len(set(n.casefold() for n in payload))!=len(payload): raise RuntimeError("Case collision")
for name in payload:
    if name.startswith("/") or "\\" in name or ":" in name or ".." in name.split("/"): raise RuntimeError("Unsafe member")
manifest=encode({"kind":"NEW_DOCUMENT_REVIEW_MANIFEST","payload_count":len(payload),
    "files":[{"path":n,"bytes":len(d),"sha256":sha(d)} for n,d in sorted(payload.items())],
    "self_hash_excluded":True})
save(MANIFEST,manifest)
with zipfile.ZipFile(ZIP,"x",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for name,data in sorted(payload.items()): archive.writestr(name,data)
    archive.writestr("PACKAGE_MANIFEST.json",manifest)
expected=dict(payload)
expected["PACKAGE_MANIFEST.json"]=manifest
with zipfile.ZipFile(ZIP) as archive:
    names=archive.namelist()
    if len(names)!=len(set(names)) or set(names)!=set(expected): raise RuntimeError("Member set mismatch")
    if archive.testzip() is not None: raise RuntimeError("CRC failed")
    for info in archive.infolist():
        if stat.S_ISLNK(info.external_attr>>16): raise RuntimeError("Archive link")
        if archive.read(info)!=expected[info.filename]: raise RuntimeError("Byte readback mismatch")
for item,data in zip(items,raw):
    if Path(item["path"]).read_bytes()!=data: raise RuntimeError("Input changed after packaging")
archive_bytes=ZIP.read_bytes()
receipt={
    "kind":"NEW_REVIEW_PACKAGE_RECEIPT","created_utc":datetime.now(timezone.utc).isoformat(),
    "status":"REVIEW_PACKAGE_READBACK_VERIFIED","recipient":None,
    "archive":{"file":ZIP.name,"bytes":len(archive_bytes),"sha256":sha(archive_bytes)},
    "manifest":{"bytes":len(manifest),"sha256":sha(manifest)},"payload_count":len(payload),
    "checks":["exact_set","safe_path_case_collision_link","decompressed_member_bytes_and_sha256","manifest_bytes","CRC"],
    "selected_inputs_unchanged":len(items),
    "scope":"S1-O v2 document review only; no functional or native execution acceptance",
    "new_native_approval":False
}
save(RECEIPT,encode(receipt))
print(json.dumps(receipt,ensure_ascii=False))

