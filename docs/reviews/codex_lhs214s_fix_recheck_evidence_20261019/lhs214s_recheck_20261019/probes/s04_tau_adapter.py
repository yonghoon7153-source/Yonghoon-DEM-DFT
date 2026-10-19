"""Preserve tau-label assertions; supply Git-show bytes from verified snapshot.

Only the four H2 TSV Git content reads are intercepted. Each returned byte string
must match the submitted pinned tree Git blob and its source manifest SHA256.
No Git program is executed and no production function or expectation is changed.
"""
import hashlib
import json
from pathlib import Path
import runpy
import subprocess

REVIEW = Path(__file__).resolve().parents[1]
ROOT = REVIEW / 'source'
manifest = json.loads((REVIEW / 'source_manifest.json').read_text(encoding='utf-8'))
assert manifest['pin'] == '685c2bbdbbfee82898a9ec062bb9c2bc94612fc8'
files = {r['path']: r for r in manifest['files']}
original = subprocess.run
reads = []

def source_bytes(command, *args, **kwargs):
    if isinstance(command, list) and command and command[0] == 'git':
        assert len(command) == 5 and command[1] == '-C' and Path(command[2]).resolve() == ROOT.resolve()
        assert command[3] == 'show' and command[4].startswith('HEAD:')
        rel = command[4][5:].replace('\\', '/')
        assert rel.startswith(('docs/data/lhs_release_20261001/', 'docs/data/lhs_release_20261001_v11/')) and rel.endswith('_columns.tsv')
        data = (ROOT / rel).read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        sha = hashlib.sha256(data).hexdigest()
        assert blob == files[rel]['git_blob'] and sha == files[rel]['sha256']
        reads.append(dict(path=rel, git_blob=blob, sha256=sha))
        return subprocess.CompletedProcess(command, 0, stdout=data, stderr=b'')
    return original(command, *args, **kwargs)

subprocess.run = source_bytes
try:
    runpy.run_path(str(ROOT / 'webapp/test_tau_labels.py'), run_name='__main__')
finally:
    (REVIEW / 'evidence/s04_tau_adapter_reads.json').write_text(json.dumps(reads, indent=2), encoding='utf-8')
