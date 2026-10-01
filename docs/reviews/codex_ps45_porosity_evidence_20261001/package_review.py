"""Package this independent review and verify its preserved Git reference bytes."""
from pathlib import Path
import hashlib
import json
import zipfile

root = Path(__file__).resolve().parent
for ref in json.loads((root/'reference_manifest.json').read_text(encoding='utf-8')):
    data = (root/'reference'/ref['path']).read_bytes()
    sha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert sha == ref['blob_sha'], (ref['path'], sha, ref['blob_sha'])
result = json.loads((root/'evidence/audit_result.json').read_text(encoding='utf-8'))
assert result['checks_passed'] == result['checks_total'] == 94
report = (root/'codex_ps45_porosity_verdict_20261001.md').read_text(encoding='utf-8')
for n in range(1,8):
    assert 'Q'+str(n) in report
assert report.count('```') % 2 == 0
files = sorted(p for p in root.rglob('*') if p.is_file() and p.name != 'DELIVERY_MANIFEST.json' and '__pycache__' not in p.parts)
manifest = dict(scope='porosity interpretation review; no simulations, production changes, or raw geometry reharvest',
                files=[dict(path=p.relative_to(root).as_posix(), bytes=p.stat().st_size,
                            sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files])
mp = root/'DELIVERY_MANIFEST.json'
mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dest = root.parent/'codex_ps45_porosity_review_20261001.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files+[mp]:
        z.write(p, arcname=root.name+'/'+p.relative_to(root).as_posix())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
print(json.dumps(dict(zip=str(dest),bytes=dest.stat().st_size,
                      sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
                      reference_git_blobs_verified=8,files=len(files)+1),indent=2))
