"""Package only reviewer-owned outputs; never executes received sources."""
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
target = root.parent / 'BMIN_R2_RETRY3_SUPPLEMENT_REVIEW_20261006.zip'
if target.exists():
    raise SystemExit('Output archive exists; refusing overwrite')
names = ['REVIEW_KO.md', 'CLAUDE_REPLY_KO.md', 'DECISION.json', 'RECEIVED_SNAPSHOT.json', 'REVIEW_CHECKS.json', 'reviewer_checks.py', 'package_review.py']
def sha(b):
    return hashlib.sha256(b).hexdigest()
files = []
for name in names:
    b = (root/name).read_bytes()
    files.append({'file':name, 'bytes':len(b), 'sha256':sha(b)})
manifest = {'scope':'Reviewer-created supplement review; original retry3 archive not duplicated', 'files':files}
(root/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as z:
    for name in names + ['PACKAGE_MANIFEST.json']:
        z.write(root/name, name)
with zipfile.ZipFile(target) as z:
    assert set(z.namelist()) == set(names + ['PACKAGE_MANIFEST.json'])
    assert len(z.namelist()) == len(set(z.namelist()))
    assert z.testzip() is None
    for pin in files:
        b = z.read(pin['file'])
        assert len(b) == pin['bytes'] and sha(b) == pin['sha256']
    assert z.read('PACKAGE_MANIFEST.json') == (root/'PACKAGE_MANIFEST.json').read_bytes()
result = {'status':'REVIEW_PACKAGE_VERIFIED', 'path':str(target), 'bytes':target.stat().st_size, 'sha256':sha(target.read_bytes()), 'payload_count':len(names), 'manifest_count':1, 'COMSOL_calls':0, 'native150_approved':False}
print(json.dumps(result, ensure_ascii=False, indent=2))
