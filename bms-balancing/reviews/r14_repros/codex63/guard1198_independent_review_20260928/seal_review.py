"""Package reviewer documents and inert source snapshots, never execute subject code."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import zipfile
from datetime import datetime, timezone

root = Path(__file__).resolve().parent
source = Path('C:/Users/Administrator/Downloads/COMSOL63_GUARD1198_OFFLINE_PREPARATION_20260928.zip')
expected = 'e8f544c01e3e8e8ba4ab27f294f1b8bb9124707ee0cfc38e2023a42f731279ec'
def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2)+'\n').encode('utf-8')

source_bytes = source.read_bytes()
assert identity(source_bytes)['sha256'] == expected
payload = {}
names = ['README_KO.md', 'REVIEW_KO.md', 'REVIEWER_REPLY_KO.md',
         'NEXT_LIMITED_VALIDATION_DIRECTIVE_KO.md', 'DECISION.json',
         'PACKAGE_AUDIT.json', 'DATA_STATIC_AUDIT.json', 'FAILURE_SCHEMA_EVIDENCE.json',
         'PARENT_SCHEMA_CASES.json', 'trigger_consumer.py.numbered.txt',
         'candidate_entry.py.numbered.txt', 'PARENT_COMMAND.ps1.numbered.txt',
         'audit_package.py', 'static_data_audit.py', 'seal_review.py']
for name in names:
    data = (root/name).read_bytes()
    data.decode('utf-8')
    if name.endswith('.json'):
        json.loads(data)
    payload[name] = data
references = ['src/Guard1198Candidate.java', 'src/trigger_consumer.py',
              'src/candidate_entry.py', 'PARENT_COMMAND.ps1', 'CONTRACT.json',
              'CODE_MANIFEST.json', 'LIMITED_VALIDATION_PLAN.json',
              'TRANSFORM_RECORD.json']
with zipfile.ZipFile(source) as archive:
    entries = archive.infolist()
    assert len(entries) == len({entry.filename.casefold() for entry in entries})
    for entry in entries:
        p = PurePosixPath(entry.filename)
        assert not p.is_absolute() and '..' not in p.parts
        assert '\\' not in entry.filename and ':' not in entry.filename
        assert not stat.S_ISLNK(entry.external_attr >> 16)
    assert archive.testzip() is None
    manifest = json.loads(archive.read('PACKAGE_MANIFEST.json'))
    assert set(archive.namelist()) == {r['file'] for r in manifest['files']} | {'PACKAGE_MANIFEST.json'}
    assert len(manifest['files']) == 62
    for item in manifest['files']:
        data = archive.read(item['file'])
        assert identity(data) == {k:item[k] for k in ('bytes', 'sha256')}
        assert data == (root/'received'/item['file']).read_bytes()
    for name in references:
        payload['reference/'+name] = archive.read(name)

package_manifest = encoded({'scope':'Reviewer documents and selected inert evidence snapshots',
    'subject_zip_sha256':expected,
    'files':[{'file':name, **identity(data)} for name,data in sorted(payload.items())]})
package = root/'COMSOL63_GUARD1198_INDEPENDENT_REVIEW_20260928.zip'
with zipfile.ZipFile(package, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
    for name,data in sorted(payload.items()):
        archive.writestr(name,data)
    archive.writestr('REVIEW_PACKAGE_MANIFEST.json',package_manifest)
with zipfile.ZipFile(package) as archive:
    assert archive.testzip() is None
    assert set(archive.namelist()) == set(payload)|{'REVIEW_PACKAGE_MANIFEST.json'}
    assert len(archive.namelist()) == len({n.casefold() for n in archive.namelist()})
    for name,data in payload.items():
        assert archive.read(name) == data
    assert archive.read('REVIEW_PACKAGE_MANIFEST.json') == package_manifest
assert source.read_bytes() == source_bytes
receipt = {'created_utc':datetime.now(timezone.utc).isoformat(),
    'scope':'Reviewer package generation, not native validation or execution approval',
    'package':{'path':str(package), **identity(package.read_bytes())},
    'payload_count':len(payload), 'entries':len(payload)+1,
    'manifest':identity(package_manifest),
    'exact_set_size_sha_crc_case_path_checked':True,
    'source_zip_and_all_extracted_payload_unchanged':True,
    'subject_code_imports_or_execution':0,
    'native_1198_approved':False, 'run_30s_approved':False,
    'recipient':None}
with (root/'REVIEW_DELIVERY_RECEIPT.json').open('xb') as stream:
    stream.write(encoded(receipt))
assert json.loads((root/'REVIEW_DELIVERY_RECEIPT.json').read_bytes()) == receipt
print(json.dumps(receipt, ensure_ascii=False))
