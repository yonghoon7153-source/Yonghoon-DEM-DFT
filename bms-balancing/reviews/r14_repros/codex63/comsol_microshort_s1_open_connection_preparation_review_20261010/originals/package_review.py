"""Package this review only; never run submitted code."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile
ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_REVIEW_20261010.zip'
assert not ARCHIVE.exists()
manifest_path=ROOT/'REVIEW_MANIFEST.json'
receipt_path=ROOT/'REVIEW_DELIVERY_RECEIPT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
src=Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_20261009.zip')
assert sha(src.read_bytes())=='32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c'
rows=[]
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p not in (ARCHIVE,manifest_path,receipt_path):
        b=p.read_bytes();rows.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)})
assert len(rows)==len({r['path'].casefold() for r in rows})
manifest={'schema':'REVIEW_PACKAGE_V1','self_excluded':True,'payload_count':len(rows),'files':rows}
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with zipfile.ZipFile(ARCHIVE,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for r in rows:z.write(ROOT/r['path'],r['path'])
    z.write(manifest_path,manifest_path.name)
with zipfile.ZipFile(ARCHIVE) as z:
    assert set(z.namelist())=={r['path'] for r in rows}|{manifest_path.name}
    for r in rows:
        b=z.read(r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
    assert z.read(manifest_path.name)==manifest_path.read_bytes()
assert sha(src.read_bytes())=='32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c'
r={'status':'REVIEW_PACKAGE_VERIFIED','recipient':None,'archive':{'path':str(ARCHIVE),'bytes':ARCHIVE.stat().st_size,'sha256':sha(ARCHIVE.read_bytes())},'payload_count':len(rows),'manifest_sha256':sha(manifest_path.read_bytes()),'input_archive_unchanged':True,'received_code_executions':0,'COMSOL_JVM_tests':0,'native_ready':False,'decision':'REVISIONS_REQUIRED_BEFORE_LIMITED_VALIDATION'}
receipt_path.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(r,ensure_ascii=False,indent=2))
