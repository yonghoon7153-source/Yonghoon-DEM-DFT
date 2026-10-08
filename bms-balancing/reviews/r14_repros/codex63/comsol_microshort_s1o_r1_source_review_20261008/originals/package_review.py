"""Reviewer-owned data-only packaging. Does not import received modules."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import zipfile

ROOT = Path(__file__).resolve().parent
DOWNLOADS = Path('C:/Users/Administrator/Downloads')
INPUTS = [
    ('main', DOWNLOADS / 'COMSOL_MICROSHORT_S1O_R1_OFFLINE_CORRECTIONS_20261008 (1).zip',
     '0a18cb64f8bcbcd4725b45088ee310f85e9292a1ffdced2332b5102f5fd6f9dc'),
    ('supplement', DOWNLOADS / 'COMSOL_MICROSHORT_S1O_R1_DELIVERY_SUPPLEMENT_20261008 (1).zip',
     '4cfd310ae5c019cce63a2ce012debfa9307f44ac739c1253cc07a5cf0c8d73b2'),
]
OUT = ROOT / 'COMSOL_MICROSHORT_S1O_R1_SOURCE_REVIEW_20261008.zip'
MANIFEST = ROOT / 'REVIEW_MANIFEST.json'
RECEIPT = ROOT / 'REVIEW_DELIVERY_RECEIPT.json'
for target in (OUT, MANIFEST, RECEIPT):
    if target.exists():
        raise SystemExit('STOP_EXISTING_OUTPUT: ' + str(target))

def digest(data):
    return sha256(data).hexdigest()

originals = []
for label, path, expected in INPUTS:
    data = path.read_bytes()
    if digest(data) != expected:
        raise SystemExit('INPUT_IDENTITY_CHANGED: ' + str(path))
    originals.append({'file': path.name, 'bytes': len(data), 'sha256': expected})
    with zipfile.ZipFile(path) as source_zip:
        names = [i.filename for i in source_zip.infolist() if not i.is_dir()]
        received = ROOT / 'received' / label
        actual = sorted(p.relative_to(received).as_posix() for p in received.rglob('*') if p.is_file())
        if sorted(names) != actual:
            raise SystemExit('RECEIVED_SET_CHANGED: ' + label)
        for name in names:
            if source_zip.read(name) != (received / name).read_bytes():
                raise SystemExit('RECEIVED_BYTES_CHANGED: ' + label + '/' + name)

decision = json.loads((ROOT / 'DECISION.json').read_text(encoding='utf-8'))
assert decision['validation_approved'] is False
assert decision['native_approved'] is False
assert decision['received_code_executed'] == 0
assert len(decision['findings']) == 3

files = {}
for name in ('README_KO.md', 'REVIEW_KO.md', 'CLAUDE_REPLY_KO.md',
             'VALIDATION_APPROVAL_DRAFT_KO.md', 'DECISION.json', 'INPUT_CHECK.json',
             'STATIC_DATA_AUDIT.json', 'inspect_inputs.py', 'static_data_audit.py',
             'package_review.py'):
    files[name] = (ROOT / name).read_bytes()
for directory in ('notes', 'received'):
    for path in (ROOT / directory).rglob('*'):
        if path.is_file():
            files[path.relative_to(ROOT).as_posix()] = path.read_bytes()
request_path = DOWNLOADS / 'COMSOL_MICROSHORT_S1O_R1_REVIEW_SEND_20261008.md'
files['received/REVIEW_SEND_KO.md'] = request_path.read_bytes()
if len({name.casefold() for name in files}) != len(files):
    raise SystemExit('DUPLICATE_ARCHIVE_NAME')

manifest = {
    'kind': 'INDEPENDENT_STATIC_REVIEW_PACKAGE_MANIFEST',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'self_excluded': True,
    'payload_count': len(files),
    'source_archives': originals,
    'review_request': {'bytes': len(files['received/REVIEW_SEND_KO.md']),
                       'sha256': digest(files['received/REVIEW_SEND_KO.md'])},
    'files': [{'path': name, 'bytes': len(data), 'sha256': digest(data)}
              for name, data in sorted(files.items())],
}
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
with MANIFEST.open('xb') as stream:
    stream.write(manifest_bytes)
with zipfile.ZipFile(OUT, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for name, data in sorted(files.items()):
        archive.writestr(name, data)
    archive.writestr(MANIFEST.name, manifest_bytes)
with zipfile.ZipFile(OUT) as archive:
    expected_names = set(files) | {MANIFEST.name}
    if set(archive.namelist()) != expected_names or len(archive.namelist()) != len(expected_names):
        raise SystemExit('OUTPUT_SET_MISMATCH')
    for name, data in files.items():
        if archive.read(name) != data:
            raise SystemExit('OUTPUT_BYTE_MISMATCH: ' + name)
    if archive.read(MANIFEST.name) != manifest_bytes:
        raise SystemExit('OUTPUT_MANIFEST_MISMATCH')
    if archive.testzip() is not None:
        raise SystemExit('OUTPUT_CRC_FAILURE')
for _, path, expected in INPUTS:
    if digest(path.read_bytes()) != expected:
        raise SystemExit('INPUT_CHANGED_AFTER_PACKAGING')
archive_bytes = OUT.read_bytes()
receipt = {
    'kind': 'REVIEW_PACKAGE_DELIVERY_RECEIPT',
    'recipient': None,
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'package': {'file': OUT.name, 'bytes': len(archive_bytes), 'sha256': digest(archive_bytes)},
    'payload_count': len(files), 'entries': len(files) + 1,
    'manifest_sha256': digest(manifest_bytes),
    'output_set_bytes_sha_crc_verified': True,
    'received_members_unchanged': True,
    'input_archives_unchanged': True,
    'source_corrections': 'STATIC_ACCEPTED_WITHIN_REVIEWED_SCOPE',
    'validation_plan': 'P2_CORRECTIONS_REQUIRED_BEFORE_TEST',
    'original_delivery_closeout': 'MISSING_FINAL_SUPPLEMENT_SIDECARS',
    'received_code_executed': 0, 'COMSOL_calls': 0,
    'validation_approved': False, 'native_approved': False,
    'scope': 'Reviewer package checks, not original execution-host or original timing observation. Receipt outside sealed review ZIP.'
}
with RECEIPT.open('x', encoding='utf-8', newline='\n') as stream:
    json.dump(receipt, stream, ensure_ascii=False, indent=2)
    stream.write('\n')
assert json.loads(RECEIPT.read_text(encoding='utf-8')) == receipt
print(json.dumps(receipt, ensure_ascii=False))
