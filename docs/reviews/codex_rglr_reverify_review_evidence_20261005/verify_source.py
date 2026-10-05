"""Portable, read-only verification of the pinned review copy (not a production seal)."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent
m=json.loads((R/'source_manifest.json').read_text(encoding='utf8'));bad=[]
for item in m['files']:
 p=R/'source'/item['path']
 if not p.is_file():bad.append(dict(path=item['path'],error='missing'));continue
 b=p.read_bytes();sha=hashlib.sha256(b).hexdigest()
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 if sha!=item['sha256'] or blob!=item['expected']:bad.append(dict(path=item['path'],error='hash mismatch'))
print(json.dumps(dict(commit=m['commit'],files=len(m['files']),verified=len(m['files'])-len(bad),bad=bad),indent=2))
raise SystemExit(bool(bad))
