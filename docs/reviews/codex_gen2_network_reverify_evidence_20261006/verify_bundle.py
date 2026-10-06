"""Verify preserved artifacts and pinned Git blobs; does not contact GitHub or write files."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parent
rows=json.loads((R/'bundle_manifest.json').read_text(encoding='utf8'));bad=[]
for e in rows:
 p=R/e['path']
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=e['sha256']:bad.append(e['path'])
src=json.loads((R/'source_manifest.json').read_text(encoding='utf8'))
for e in src:
 p=R/'source'/e['path'];b=p.read_bytes()
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=e['sha']:bad.append('gitblob:'+e['path'])
print(json.dumps(dict(files=len(rows),pinned_blobs=len(src),failures=bad),ensure_ascii=False))
raise SystemExit(1 if bad else 0)
