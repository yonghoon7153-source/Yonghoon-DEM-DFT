"""Package reviewer-authored findings and selected inert evidence; no tests run."""
from pathlib import Path
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parent
payload = {}
def add(name, p):
    payload[name] = p.read_bytes()
def digest(b):
    return hashlib.sha256(b).hexdigest()

for name in ('REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_V3_ACCEPTANCE_KO.md',
             'DECISION.json','ARCHIVE_AUDIT.json','EVIDENCE_AUDIT.json',
             'audit_package.py','audit_records.py','package_review.py'):
    add(name, R / name)
assert json.loads(payload['EVIDENCE_AUDIT.json'])['status'] == 'PASS'
assert json.loads(payload['DECISION.json'])['native60_approved'] is False
for name in ('FINAL_STATUS.json','CASE_RECONCILIATION.json','HARNESS_CACHE_BINDING.json',
             'PRE_TEST_SEAL.json','PRESERVATION_AFTER.json','EXTRACTED_SOURCES.json',
             'LONG_HORIZON_REVIEW_ACK.json','NEXT_NATIVE60_INACTIVE.json',
             'candidate/CODE_MANIFEST.json','previous_failed_attempt/FIRST_FAILURE.json'):
    add('evidence/' + name, R / 'received' / name)
for name in ('DELIVERY_RECEIPT.json','PACKAGING_TOOL_RETURN.json','DELIVERY_CLOSEOUT.json'):
    add('evidence/supplement/' + name, R / 'supplement' / name)
v3 = Path('C:/Users/Administrator/Desktop/CLAUDE_REPLY_NORMAL30_LONG_HORIZON_KO_v3.md')
add('source/CLAUDE_REPLY_NORMAL30_LONG_HORIZON_KO_v3.md', v3)
assert digest(payload['source/CLAUDE_REPLY_NORMAL30_LONG_HORIZON_KO_v3.md']) == json.loads(payload['EVIDENCE_AUDIT.json'])['inputs'][str(v3)]['sha256']
rows = [{'file': n, 'bytes': len(b), 'sha256': digest(b)} for n, b in sorted(payload.items())]
mb = json.dumps({'scope': 'Recipient review, not execution approval', 'payloads': rows}, ensure_ascii=False, indent=2).encode()
target = R / 'NORMAL60_VALIDATION_AND_CLAUDE_V3_RECIPIENT_REVIEW_20260930.zip'
with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as z:
    for name, b in sorted(payload.items()):
        z.writestr(name, b)
    z.writestr('MANIFEST.json', mb)
with zipfile.ZipFile(target) as z:
    assert len(z.namelist()) == len(set(z.namelist())) == len(payload) + 1
    assert set(z.namelist()) == set(payload) | {'MANIFEST.json'}
    assert z.testzip() is None
    assert z.read('MANIFEST.json') == mb
    for row in rows:
        raw = z.read(row['file'])
        assert len(raw) == row['bytes'] and digest(raw) == row['sha256']
b = target.read_bytes()
receipt = {'scope': 'Generated recipient review package; no COMSOL or received tests run',
           'path': str(target), 'bytes': len(b), 'sha256': digest(b),
           'payload_count': len(payload), 'manifest_sha256': digest(mb),
           'exact_set_size_sha_crc_verified': True,
           'native60_approved': False, 'recipient': None}
(R / 'REVIEW_PACKAGE_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False))
