"""Reviewer-owned file identity/document partition checks; not REIL/P0 tests.

No submitted module imports, dataset reads, notebook reads, fitting or network.
Creates review evidence and a ZIP from an explicit local file list only.
"""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[1]
SNAPSHOT = json.loads((ROOT / 'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
PRIOR = json.loads((ROOT.parent / 'reil_v2_annex_b_review_20261004' / 'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
checks = []


def check(name, passed, **evidence):
    checks.append({'name': name, 'pass': bool(passed), **evidence})
    if not passed:
        raise AssertionError(name)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


identities = []
for path, record in SNAPSHOT['files'].items():
    raw = record['content'].encode('utf-8')
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
    check('git_blob:' + path, blob == record['sha'], expected=record['sha'], actual=blob)
    identities.append({'path': path, 'bytes': len(raw), 'sha256': sha(raw), 'git_blob': blob})

for name in ['REIL_EXTERNAL_VALIDATION_PROTOCOL_v2.md', 'REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_A.md', 'REIL_EXTERNAL_VALIDATION_PROTOCOL_v2_ANNEX_B.md']:
    path = 'bms-balancing/docs/' + name
    check('prior_document_unchanged:' + name,
          SNAPSHOT['files'][path]['content'] == PRIOR['files'][path]['content'] and
          SNAPSHOT['files'][path]['sha'] == PRIOR['files'][path]['sha'])

pdf_dir = Path('C:/Users/Administrator/Desktop/읽어야되는 논문/가형 논문')
pdfs = [
    ('21. Benchmarking half-cell model fitting approaches for lithium-ion battery degradation diagnostics.pdf', 6696708, '8ccf029c45a3be1b60f8994e36a5dd3b204cf65288b700175d4ad275cb3343c1'),
    ('21. Sup) Benchmarking half-cell model fitting approaches for lithium-ion battery degradation diagnostics.pdf', 5511025, '5d25a800f7e2c32fd849eed972f0ba0a23b36d0999bcb065186e6aab156460c9'),
]
pdf_identities = []
for name, expected_size, expected_sha in pdfs:
    raw = (pdf_dir / name).read_bytes()
    actual = {'path': str(pdf_dir / name), 'bytes': len(raw), 'sha256': sha(raw)}
    check('pdf_identity_after_review:' + name, len(raw) == expected_size and sha(raw) == expected_sha, **actual)
    pdf_identities.append(actual)

core = SNAPSHOT['files']['bms-balancing/docs/REIL_C1_CORE_SPEC_20261005.md']['content']
sheet_rows = {}
for line in core.splitlines():
    if not line.startswith('|'):
        continue
    parts = [x.strip() for x in line.split('|')]
    if len(parts) > 3 and parts[1].isdigit() and parts[2].startswith('`'):
        sheet_rows[int(parts[1])] = parts[2].strip('`')
check('document_table_19_sheets', set(sheet_rows) == set(range(1, 20)))
analysis = set(range(1, 12))
references = {15, 16}
outside = set(sheet_rows) - analysis - references
check('document_partition_only_not_workbook_observation', outside == {12, 13, 14, 17, 18, 19},
      analysis_sheet_indices=sorted(analysis), reference_sheet_indices=sorted(references),
      outside_sheets=[{'sheet_index': i, 'name': sheet_rows[i]} for i in sorted(outside)])

result = {
    'status': 'REVIEW_DOCUMENT_IDENTITIES_VERIFIED',
    'scope': 'Metadata, Git blob, prior text equality, document table partition only; not empirical validation or REIL tests.',
    'fixed_commit': SNAPSHOT['fixed_commit'],
    'checks': checks,
    'check_count': len(checks),
    'all_pass': all(c['pass'] for c in checks),
    'source_documents': identities,
    'pdf_identities': pdf_identities,
    'visual_inspection_pages': {'main': [7, 9, 10, 11, 12, 22, 23], 'supplement': [2, 3]},
    'text_extraction': 'pypdf; pdftotext unavailable on PATH; no installation attempted',
    'data_opened': False,
    'provided_programs_executed': False,
    'P0_executed': False,
    'native_calls': 0,
}
(ROOT / 'REVIEW_CHECKS.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

payload = ['README_KO.md', 'REVIEW_KO.md', 'CLAUDE_REPLY_KO.md', 'DECISION.json', 'RECEIVED_SNAPSHOT.json', 'REVIEW_CHECKS.json', 'reviewer_document_checks.py']
manifest = {'scope': 'Review delivery; excludes manifest itself and all PDFs/renders/extracted paper text.', 'payload': []}
for name in payload:
    raw = (ROOT / name).read_bytes()
    manifest['payload'].append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
(ROOT / 'PACKAGE_MANIFEST.json').write_bytes(manifest_bytes)
archive = ROOT.parent / 'REIL_V2_ANNEX_C_REVIEW_20261005.zip'
if archive.exists():
    raise FileExistsError(archive)
with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED) as zf:
    for name in payload + ['PACKAGE_MANIFEST.json']:
        zf.write(ROOT / name, arcname=name)
with zipfile.ZipFile(archive) as zf:
    assert zf.testzip() is None
    assert len(zf.namelist()) == len(set(zf.namelist())) == len(payload) + 1
    assert set(zf.namelist()) == set(payload + ['PACKAGE_MANIFEST.json'])
    assert zf.read('PACKAGE_MANIFEST.json') == manifest_bytes
    for item in manifest['payload']:
        raw = zf.read(item['path'])
        assert len(raw) == item['bytes'] and sha(raw) == item['sha256']
archive_raw = archive.read_bytes()
print(json.dumps({'status': 'REVIEW_PACKAGE_VERIFIED', 'document_identity_checks': len(checks), 'all_pass': True,
                  'zip': str(archive), 'bytes': len(archive_raw), 'sha256': sha(archive_raw),
                  'payload_count': len(payload), 'manifest_sha256': sha(manifest_bytes),
                  'REIL_tests': 0, 'P0': 0, 'COMSOL': 0, 'execution_approved': False}, ensure_ascii=False))
