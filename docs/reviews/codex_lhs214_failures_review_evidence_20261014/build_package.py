"""Verify pinned review inputs, re-run offline probes, and package review evidence."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import zipfile

R = Path(__file__).resolve().parent
PIN = '1087a9b2f4a93aa6a3b0debc698a14fffa13488d'
INPUT_SHA = '250e7a9ddf180192f724c827431b9ef3f56e3bdc485d709c0f3a7c1234d7f4b4'
manifest = json.loads((R / 'source_manifest.json').read_text(encoding='utf-8'))
assert manifest['pin'] == PIN
bad = []
for item in manifest['files']:
    b = (R / 'source' / item['path']).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    if hashlib.sha256(b).hexdigest() != item['sha256'] or blob != item['sha']:
        bad.append(item['path'])
assert not bad, bad
assert len(manifest['files']) == 974
input_archive = R / 'submitted/lhs214_run_evidence_1014_1520.tgz'
assert hashlib.sha256(input_archive.read_bytes()).hexdigest() == INPUT_SHA

env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
           OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
           TEMP=str(R / 'tmp'), TMP=str(R / 'tmp'))
results = []
for name in ['evidence_audit', 'solver_probe', 'consumer_contracts']:
    cmd = [sys.executable, '-X', 'utf8', '-B', str(R / 'probes' / (name + '.py'))]
    p = subprocess.run(cmd, cwd=R, env=env, capture_output=True, text=True,
                       encoding='utf-8', timeout=120)
    log = R / 'evidence' / (name + '_rerun.log')
    log.write_text(p.stdout + '\nSTDERR:\n' + p.stderr, encoding='utf-8')
    results.append({'probe': name, 'rc': p.returncode,
                    'log': log.relative_to(R).as_posix()})
    assert p.returncode == 0, results[-1]

verification = {'pin': PIN, 'source_files_git_blob_and_sha256_verified': len(manifest['files']),
                'source_unchanged': True, 'input_tgz_sha256': INPUT_SHA,
                'offline_probe_reruns': results, 'production_run': False,
                'target_source_modified': False}
(R / 'evidence/final_verification.json').write_text(
    json.dumps(verification, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

files = sorted(p for p in R.rglob('*') if p.is_file()
               and 'tmp' not in p.relative_to(R).parts
               and '__pycache__' not in p.relative_to(R).parts
               and p.name != 'package_manifest.json')
entries = [{'path': p.relative_to(R).as_posix(), 'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
pm = R / 'package_manifest.json'
pm.write_text(json.dumps({'pin': PIN, 'scope': 'review evidence, not a production approval',
                          'files': entries}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
output = R.parent / 'codex_lhs214_failures_review_1087a9b2f_20261014.zip'
with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in files + [pm]:
        z.write(p, R.name + '/' + p.relative_to(R).as_posix())
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(set(z.namelist()))
    for item in entries:
        b = z.read(R.name + '/' + item['path'])
        assert hashlib.sha256(b).hexdigest() == item['sha256']
receipt = {'zip': output.name, 'bytes': output.stat().st_size,
           'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
           'entries': len(files) + 1, 'crc': 'PASS', 'entry_hashes': 'PASS',
           'review_pin': PIN}
output.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt, indent=2))
