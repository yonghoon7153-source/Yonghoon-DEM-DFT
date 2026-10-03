"""Package review artifacts, verifying pinned source blobs; no production writes."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parent
dest = root.parent / 'codex_rint_stage1_review_20261003.zip'
if dest.exists():
    raise SystemExit(f'Refusing to replace existing bundle: {dest}')
source_manifest=json.loads((root/'source_manifest.json').read_text(encoding='utf-8'))
for entry in source_manifest['files']:
    data=(root/'source'/entry['path']).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert blob==entry['git_blob_sha1'], entry['path']
files=sorted(p for p in root.rglob('*') if p.is_file()
             and '__pycache__' not in p.parts and p.suffix!='.pyc'
             and p.name!='SHA256SUMS.json')
hashes={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
mf=root/'SHA256SUMS.json'
mf.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files+[mf]:
        z.write(p,root.name+'/'+p.relative_to(root).as_posix())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for path,digest in hashes.items():
        assert hashlib.sha256(z.read(root.name+'/'+path)).hexdigest()==digest,path
print(json.dumps(dict(zip=str(dest),bytes=dest.stat().st_size,files=len(files)+1,
                     sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                     source_blobs_verified=len(source_manifest['files'])),indent=2))
