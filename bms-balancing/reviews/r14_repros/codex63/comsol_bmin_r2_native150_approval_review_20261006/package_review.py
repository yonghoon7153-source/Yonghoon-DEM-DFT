"""Package only reviewer artifacts. No received modules are imported."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parent
archive = root.parent / 'BMIN_R2_NATIVE150_APPROVAL_REVIEW_20261006.zip'
if archive.exists():
    raise SystemExit('Existing reviewer ZIP; no overwrite')
sha = lambda b: hashlib.sha256(b).hexdigest()
names = [
    'REVIEW_KO.md', 'CLAUDE_REPLY_KO.md', 'DECISION.json', 'RECEIVED_SNAPSHOT.json',
    'PRIOR_VALIDATION_DECISION.json', 'STATIC_CHECKS.json', 'STATIC_CHECKS_FINAL.json',
    'REVIEWER_CHECK_HISTORY.json', 'reviewer_static_checks.py', 'package_review.py'
]
items = []
for name in names:
    raw = (root / name).read_bytes()
    if name.endswith('.json'):
        json.loads(raw)
    items.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
manifest = {'scope': 'Reviewer static evidence; not native execution authorization',
            'created_at': datetime.now(timezone.utc).isoformat(), 'files': items}
manifest_raw = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
(root / 'PACKAGE_MANIFEST.json').write_bytes(manifest_raw)
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as z:
    for name in names:
        z.write(root / name, name)
    z.writestr('PACKAGE_MANIFEST.json', manifest_raw)
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist()) == len(set(z.namelist())) == len(names) + 1
    assert set(z.namelist()) == set(names) | {'PACKAGE_MANIFEST.json'}
    assert z.testzip() is None
    assert z.read('PACKAGE_MANIFEST.json') == manifest_raw
    for row in items:
        raw = z.read(row['path'])
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
initial = json.loads((root / 'STATIC_CHECKS_FINAL.json').read_text(encoding='utf-8'))
local = Path(initial['identities']['local_attachment']['path'])
assert sha(local.read_bytes()) == initial['identities']['local_attachment']['sha256']
raw = archive.read_bytes()
receipt = {'status': 'REVIEW_PACKAGE_VERIFIED', 'recipient': None,
           'archive': {'path': str(archive), 'bytes': len(raw), 'sha256': sha(raw)},
           'payload_count': len(names), 'manifest_sha256': sha(manifest_raw),
           'checks': ['exact_set', 'no_duplicate', 'CRC', 'member_size_sha256', 'manifest_bytes', 'local_attachment_unchanged'],
           'stage1_preflight_approved': False, 'native150_approved': False,
           'received_code_executed': False, 'execution_machine_observed': False}
(root / 'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False))
