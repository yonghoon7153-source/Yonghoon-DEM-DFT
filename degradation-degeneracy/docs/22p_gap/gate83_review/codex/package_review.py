"""Package reviewer evidence only; never imports or executes received code."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
ZIP_NAME = 'GATE83_REVIEW_20260930.zip'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def write_new(name, value):
    with (ROOT / name).open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


audit = read('STATIC_AUDIT.json')
assert audit['status'] == 'PASS'
assert len(audit['checks']) == 218 and all(c['pass'] for c in audit['checks'])
identity = read('IDENTITY_AUDIT.json')
assert identity['source_digest'] == '7187bd31740514d4'
assert len(identity['scope']) == 58
for record in identity['scope']:
    content = (ROOT / 'reference' / record['path']).read_bytes()
    assert len(content) == record['bytes']
    assert sha(content) == record['sha256']
decision = read('DECISION.json')
assert decision['decision'] == 'ROUND1_CLOSURE_ACCEPTED'
assert decision['execution_go'] is False and decision['round2_authorized'] is False
assert read('RECEIPT_AUDIT.json')['status'] == 'PASS'

prior = ROOT.parent / 'gate82_review_20260930' / 'GATE82_REVIEW_20260930.zip'
prior_bytes = prior.read_bytes()
assert len(prior_bytes) == 1036284
assert sha(prior_bytes) == '6445eb4afec4d87d8c00f163f1e69162b531d550fc5f28e140c7e29e8edf0e08'
write_new('PRIOR_PACKAGE_IDENTIFICATION.json', {
    'scope': 'Current read-only comparison against prior known package identity; not a whole-workspace preservation assertion',
    'file': prior.name, 'bytes': len(prior_bytes), 'sha256': sha(prior_bytes),
    'matches_prior_identity': True, 'prior_package_modified': False,
})

excluded = {ZIP_NAME, 'PACKAGE_MANIFEST.json', 'DELIVERY_RECEIPT.json'}
payload = []
seen = set()
for path in sorted(ROOT.rglob('*')):
    assert not path.is_symlink(), str(path)
    if not path.is_file():
        continue
    name = path.relative_to(ROOT).as_posix()
    if name in excluded:
        continue
    assert '__pycache__' not in path.parts and path.suffix != '.pyc'
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and ':' not in name
    assert name.casefold() not in seen
    seen.add(name.casefold())
    data = path.read_bytes()
    payload.append({'path': name, 'bytes': len(data), 'sha256': sha(data)})
write_new('PACKAGE_MANIFEST.json', {
    'scope': 'Reviewer reports, inert source copies, API response serializations and data-only audit evidence; not an execution authorization',
    'payload_count': len(payload), 'files': payload,
})
manifest_data = (ROOT / 'PACKAGE_MANIFEST.json').read_bytes()
with ZipFile(ROOT / ZIP_NAME, 'x', compression=ZIP_DEFLATED, compresslevel=9) as z:
    for item in payload:
        z.write(ROOT / item['path'], item['path'])
    z.write(ROOT / 'PACKAGE_MANIFEST.json', 'PACKAGE_MANIFEST.json')
with ZipFile(ROOT / ZIP_NAME, 'r') as z:
    names = z.namelist()
    assert len(names) == len(set(names)) == len(payload) + 1
    assert set(names) == {x['path'] for x in payload} | {'PACKAGE_MANIFEST.json'}
    assert z.testzip() is None
    assert z.read('PACKAGE_MANIFEST.json') == manifest_data
    for item in payload:
        content = z.read(item['path'])
        assert len(content) == item['bytes'] and sha(content) == item['sha256']
package = (ROOT / ZIP_NAME).read_bytes()
receipt = {
    'created_at_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'REVIEW_PACKAGE_VERIFIED', 'recipient': None,
    'package': {'file': ZIP_NAME, 'bytes': len(package), 'sha256': sha(package)},
    'payload_count': len(payload), 'total_zip_entries': len(payload) + 1,
    'manifest_sha256': sha(manifest_data),
    'verification': ['exact_set', 'unique_casefold_names', 'safe_relative_paths', 'no_source_symlinks', 'payload_size_sha256', 'CRC'],
    'static_data_checks': len(audit['checks']),
    'source_digest': identity['source_digest'], 'decision': decision['decision'],
    'supplied_code_executed': False, 'repository_test_runs': 0,
    'execution_go': False, 'round2_authorized': False,
    'receipt_scope': 'Reviewer package generation and readback; no sender computation rerun. Receipt is outside ZIP to avoid self-reference.',
}
write_new('DELIVERY_RECEIPT.json', receipt)
assert read('DELIVERY_RECEIPT.json') == receipt
print(json.dumps(receipt, ensure_ascii=False))
