"""Package reviewer artifacts and verify preserved inputs; no subject execution."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import stat
import subprocess
import zipfile

O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g80_20260928')
SEND = Path('C:/Users/Administrator/Downloads/GATE81_SEND.md')
BASE = '9a26dd5f31ca6fae45d5a55f5c59e33408371984'

def identity(b):
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def write_json(p, v):
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

b = SEND.read_bytes()
send_identity = identity(b)
assert send_identity['sha256'] == '64847ca0d7d8cdda80e0016b5b1ac7f3754552ebb64754f1996ee691dbfb001e'
assert b'88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e' in b
(O / 'reference/GATE81_SEND.received.md').write_bytes(b)
write_json(O / 'SEND_SUPPLEMENT_AUDIT.json', {
    'file': str(SEND), **send_identity,
    'same_request_head_code_digest_and_scope': True,
    'sender_final_report': {'docs_lint': '358 passed; rc0', 'pytest': '1960 passed; 1 xfailed; rc0', 'smoke': 'rc0'},
    'source': 'User supplied send note; raw test logs not independently obtained',
    'initial_docs_lint_failures': 4, 'initial_docs_lint_causes_unresolved': 3,
    'recipient_test_execution': 0,
    'decision_unchanged': True,
})
before = json.loads((O / 'SOURCE_BEFORE.json').read_text(encoding='utf-8'))
for p, want in before.items():
    q = Path(p) if Path(p).is_absolute() else W / p
    assert identity(q.read_bytes()) == want, p
assert SEND.read_bytes() == b
assert subprocess.check_output(['git', '-C', str(W), 'rev-parse', 'HEAD']).decode().strip() == BASE
assert not subprocess.check_output(['git', '-C', str(W), 'status', '--porcelain=v1', '-uall']).strip()
write_json(O / 'FINAL_PRESERVATION.json', {
    'base_snapshot_unchanged': len(before), 'supplement_unchanged': 1,
    'total_selected_files': len(before) + 1, 'local_HEAD': BASE, 'local_tree_clean': True,
    'scope': 'Selected local inputs since audit/addendum snapshots; not remote all-state evidence',
})
exclude = {'MANIFEST.json', 'DELIVERY_RECEIPT.json'}
files = {p.relative_to(O).as_posix(): p.read_bytes() for p in sorted(O.rglob('*')) if p.is_file() and p.name not in exclude and p.suffix != '.zip'}
assert 'REVIEW_KO.md' in files and 'reference/GATE81_SEND.received.md' in files
assert len(files) == len({n.casefold() for n in files})
manifest = {'scope': 'Gate81 read-only design/scope review; includes later send-note review; not implementation or execution authorization', 'files': {n: identity(b) for n, b in files.items()}}
mb = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
(O / 'MANIFEST.json').write_bytes(mb)
zp = O / 'GATE81_REVIEW_20260928.zip'
with zipfile.ZipFile(zp, 'x', zipfile.ZIP_DEFLATED) as z:
    for n, b in files.items():
        z.writestr(n, b)
    z.writestr('MANIFEST.json', mb)
with zipfile.ZipFile(zp) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(files) | {'MANIFEST.json'}
    assert len(z.namelist()) == len({n.casefold() for n in z.namelist()})
    assert z.read('MANIFEST.json') == mb
    for n, expected in manifest['files'].items():
        pp = PurePosixPath(n)
        assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in n and ':' not in n
        assert not stat.S_ISLNK(z.getinfo(n).external_attr >> 16)
        assert identity(z.read(n)) == expected
r = {
    'scope': 'Reviewer-generated package; subsequent recipient remains null', 'recipient': None,
    'zip': zp.name, **identity(zp.read_bytes()),
    'manifest_sha256': identity(mb)['sha256'], 'payload_count': len(files),
    'exact_set_size_SHA_CRC_path_case_link_verified': True,
    'selected_input_files_unchanged': len(before) + 1,
    'decision': 'Conditional design suitability with G81-N1/N2/N3; one limited implementation round recommended only after separate user approval',
    'implementation_approved': False, 'execution_GO': False, 'subject_execution': 0,
}
write_json(O / 'DELIVERY_RECEIPT.json', r)
print(json.dumps(r, ensure_ascii=False))
