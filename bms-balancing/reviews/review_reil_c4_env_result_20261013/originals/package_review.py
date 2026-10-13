"""Reviewer-owned text/hash/archive utility; never executes supplied source."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parent
ATTACHMENT = Path('C:/Users/Administrator/Downloads/REIL_C4_ENV_RESULT_REVIEW_SEND_20261013.md')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def encoded(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + '\n').encode('utf-8')

def create(name, data):
    with (ROOT / name).open('xb') as stream:
        stream.write(data)

generated = ['SOURCE_MANIFEST.json', 'PACKAGE_MANIFEST.json', 'DELIVERY_RECEIPT.json',
             'REIL_C4_ENV_REVIEW_REPLY_20261013.zip']
for name in generated:
    if (ROOT / name).exists():
        raise RuntimeError('Refuse overwrite: ' + name)

index = json.loads((ROOT / 'SOURCE_INDEX.json').read_text(encoding='utf-8'))
decision = json.loads((ROOT / 'DECISION.json').read_text(encoding='utf-8'))
assert decision['review_ref'] == index['ref']
for key in ['manifest_sha256', 'lock_sha256', 'profile_sha256']:
    assert re.fullmatch('[0-9a-f]{64}', decision['accepted_seal'][key]), key
sources, canonical = [], {}
for entry in index['sources']:
    data = (ROOT / 'sources' / entry['path']).read_bytes()
    candidates = [('EXACT', data)]
    if data.endswith(b'\n'):
        candidates.append(('ONE_CAPTURE_TRAILING_LF_IGNORED', data[:-1]))
    matches = [(kind, value) for kind, value in candidates if blob(value) == entry['blob']]
    if len(matches) != 1:
        raise RuntimeError('Capture not bound to remote Git blob: ' + entry['path'])
    binding, bound = matches[0]
    canonical[entry['path']] = bound
    sources.append({**entry, 'capture_bytes': len(data), 'capture_sha256': sha(data),
                    'remote_bytes': len(bound), 'remote_sha256': sha(bound), 'binding': binding})

attached = ATTACHMENT.read_bytes()
remote = canonical['bms-balancing/docs/REIL_C4_ENV_RESULT_REVIEW_SEND_20261013.md']
attachment = {'path': str(ATTACHMENT), 'bytes': len(attached), 'sha256': sha(attached),
              'exact_remote_bytes': attached == remote,
              'text_equal_ignoring_line_endings_and_terminal_newlines':
              attached.replace(b'\r\n', b'\n').rstrip(b'\n') == remote.replace(b'\r\n', b'\n').rstrip(b'\n')}
assert attachment['text_equal_ignoring_line_endings_and_terminal_newlines']
source_manifest = {'kind': 'REVIEW_SOURCE_MANIFEST', 'ref': index['ref'],
                   'attachment': attachment, 'sources': sources,
                   'scope': 'Selected original text captures; additional read-only source identities are recorded in notes. No source was executed.',
                   'capture_note': 'Capture newline discrepancies, if any, are explicit; remote bytes bind to immutable Git blob.'}
create('SOURCE_MANIFEST.json', encoded(source_manifest))

names = ['REVIEW_KO.md', 'CLAUDE_REPLY_KO.md', 'DECISION.json', 'SOURCE_INDEX.json',
         'SOURCE_MANIFEST.json', 'package_review.py', 'notes/SEAL_AUDIT.json',
         'notes/COMPARATOR_RESTORE_AUDIT.json', 'notes/RUNNER_AUDIT.json',
         'notes/RUNNER_PROVENANCE_SUPPLEMENT.json']
payload = {name: (ROOT / name).read_bytes() for name in names}
for name, data in payload.items():
    if name.endswith('.json'):
        json.loads(data)
manifest = {'kind': 'REVIEW_PACKAGE_MANIFEST', 'ref': index['ref'],
            'scope': 'Review documents, derived read-only audit notes, source bindings and reviewer utility; source captures remain local/GitHub. No runtime or approval token.',
            'files': [{'path': name, 'bytes': len(data), 'sha256': sha(data)} for name, data in sorted(payload.items())]}
create('PACKAGE_MANIFEST.json', encoded(manifest))
payload['PACKAGE_MANIFEST.json'] = (ROOT / 'PACKAGE_MANIFEST.json').read_bytes()
archive = ROOT / generated[-1]
with zipfile.ZipFile(archive, 'x', zipfile.ZIP_DEFLATED) as z:
    for name, data in payload.items():
        z.writestr(name, data)
with zipfile.ZipFile(archive) as z:
    assert len(z.namelist()) == len(payload)
    assert set(z.namelist()) == set(payload)
    assert len({name.casefold() for name in z.namelist()}) == len(payload)
    assert z.testzip() is None
    for name, data in payload.items():
        assert z.read(name) == data, name
archive_data = archive.read_bytes()
receipt = {'kind': 'REVIEW_DELIVERY_RECEIPT', 'recipient': None,
           'archive': {'path': str(archive), 'bytes': len(archive_data), 'sha256': sha(archive_data)},
           'payload_count': len(names), 'entries': len(payload),
           'verification': 'Exact set, casefold uniqueness, CRC, byte-for-byte reread and SHA256',
           'scope': 'Reviewer-created review package, not user approval or native execution evidence',
           'supplied_code_executed': False, 'scientific_tests_or_installations': False}
create('DELIVERY_RECEIPT.json', encoded(receipt))
print(json.dumps({'receipt': receipt, 'source_bindings': len(sources), 'attachment': attachment}, ensure_ascii=False))
