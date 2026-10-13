"""Reviewer-owned metadata/archive utility. Never imports reviewed sources."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ATTACHMENT = Path('C:/Users/Administrator/Downloads/REIL_C4_PREREVIEW_SEND_TO_CODEX_v2_20261013.md')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()

def put(name, obj):
    target = ROOT / name
    if target.exists():
        raise RuntimeError('Refusing existing generated file: ' + name)
    target.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

index = json.loads((ROOT / 'SOURCE_INDEX.json').read_text(encoding='utf-8'))
sources = []
canonical = {}
for entry in index['sources']:
    p = ROOT / 'sources' / entry['path']
    data = p.read_bytes()
    candidates = [('EXACT', data)]
    if data.endswith(b'\n'):
        candidates.append(('ONE_CAPTURE_TRAILING_LF_IGNORED', data[:-1]))
    matches = [(kind, value) for kind, value in candidates if blob(value) == entry['git_blob_sha1']]
    if not matches:
        raise RuntimeError('Source capture not bound to remote Git blob: ' + entry['path'])
    kind, bound = matches[0]
    canonical[entry['path']] = bound
    sources.append({**entry, 'capture_bytes': len(data), 'capture_sha256': sha(data),
                    'remote_bytes': len(bound), 'remote_sha256': sha(bound), 'binding': kind})

attached = ATTACHMENT.read_bytes()
remote_send = canonical['bms-balancing/docs/REIL_C4_PREREVIEW_SEND_TO_CODEX_v2_20261013.md']
attach_record = {'path': str(ATTACHMENT), 'bytes': len(attached), 'sha256': sha(attached),
                 'equals_remote_bytes': attached == remote_send,
                 'equals_text_after_lineending_and_trailing_newline_normalization':
                 attached.replace(b'\r\n', b'\n').rstrip(b'\n') == remote_send.replace(b'\r\n', b'\n').rstrip(b'\n')}
if not attach_record['equals_text_after_lineending_and_trailing_newline_normalization']:
    raise RuntimeError('Attachment and reviewed request differ beyond final newline/line endings')

put('SOURCE_MANIFEST.json', {'repository': index['repository'], 'frozen_ref': index['frozen_ref'],
    'scope': 'Remote source text captures and local attachment; not execution-machine observation.',
    'attachment': attach_record, 'sources': sources,
    'capture_note': 'One extra final LF in some reviewer display captures is explicitly distinguished from remote bytes. No source was executed.',
    'c5_cost_evidence_metadata': 'C5_COST_AUDIT.json source_files and final_record contain additional evidence bindings.'})

payload_names = ['REVIEW_KO.md', 'REQUEST_CORRECTIONS_KO.md', 'ENV_APPROVAL_DRAFT_KO.md',
    'CLAUDE_REPLY_KO.md', 'DECISION.json', 'C5_COST_AUDIT.json', 'SOURCE_INDEX.json',
    'SOURCE_MANIFEST.json', 'package_review.py']
payload = {n: (ROOT / n).read_bytes() for n in payload_names}
manifest = {'kind': 'REVIEW_PACKAGE_MANIFEST', 'frozen_ref': index['frozen_ref'],
    'scope': 'Review documents, cost-only derived audit, provenance and reviewer packaging utility. No raw fit results, notebooks, xlsx or pickle.',
    'files': [{'path': n, 'bytes': len(b), 'sha256': sha(b)} for n, b in sorted(payload.items())]}
put('PACKAGE_MANIFEST.json', manifest)
payload['PACKAGE_MANIFEST.json'] = (ROOT / 'PACKAGE_MANIFEST.json').read_bytes()
zpath = ROOT / 'REIL_C4_PREREVIEW_REPLY_20261013.zip'
with zipfile.ZipFile(zpath, 'x', zipfile.ZIP_DEFLATED) as z:
    for n, b in payload.items():
        z.writestr(n, b)
with zipfile.ZipFile(zpath) as z:
    if set(z.namelist()) != set(payload) or len(z.namelist()) != len(payload):
        raise RuntimeError('Archive set/duplicate mismatch')
    if z.testzip() is not None:
        raise RuntimeError('Archive CRC mismatch')
    for n, b in payload.items():
        if z.read(n) != b:
            raise RuntimeError('Archive bytes mismatch: ' + n)
zbytes = zpath.read_bytes()
receipt = {'kind': 'REVIEW_DELIVERY_RECEIPT', 'recipient': None,
    'archive': {'path': str(zpath), 'bytes': len(zbytes), 'sha256': sha(zbytes)},
    'entries': len(payload), 'manifest_payload_count': len(payload_names),
    'verification': 'exact set, no duplicate names, CRC and byte-for-byte reread match',
    'scope': 'Reviewer-created response package, not a native execution receipt or user approval',
    'executed_reviewed_code': False, 'tests_or_fitting_or_installation': False}
put('DELIVERY_RECEIPT.json', receipt)
print(json.dumps({'receipt': receipt, 'source_bindings': len(sources), 'attachment': attach_record}, ensure_ascii=False))
