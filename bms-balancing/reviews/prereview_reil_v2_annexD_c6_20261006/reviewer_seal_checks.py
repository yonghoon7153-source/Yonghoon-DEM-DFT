"""Reviewer-owned byte/document checks only. Never imports supplied code or NumPy.

Inputs are the two saved document snapshots and Git tree metadata. Sobol files
are synthetic C6 artifacts, not REIL observations. No arrays are regenerated.
"""
import ast
import base64
import difflib
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
snap = json.loads((ROOT / 'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
tree = json.loads((ROOT / 'TREE_SELECTION.json').read_text(encoding='utf-8'))
prior = json.loads((ROOT / 'PRIOR_BASIS.json').read_text(encoding='utf-8'))
index = {x['path']: x for x in tree['entries']}
checks = []
def check(name, ok, detail=None):
    checks.append({'id': name, 'pass': bool(ok), 'detail': detail})
def sha(b):
    return hashlib.sha256(b).hexdigest()
def raw(rec):
    return base64.b64decode(rec['content']) if rec['encoding'] == 'base64' else rec['content'].encode('utf-8')

files = {p: raw(r) for p, r in snap['files'].items()}
check('tree_not_truncated', tree['truncated'] is False)
for p, b in files.items():
    r = snap['files'][p]
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    check('git_blob:' + p, blob == r['sha'] == index[p]['sha'])
    check('git_size:' + p, len(b) == index[p]['size'], len(b))

prefix = 'bms-balancing/reil_c6_20261005/'
manifest = json.loads(files[prefix + 'MANIFEST.json'])
check('manifest_sha256', sha(files[prefix + 'MANIFEST.json']) == 'e4adba0fed22e51de37d98067a623e2e3e9575cc9e1ea039a3a88363e2378e9f')
check('manifest_payload_count', len(manifest) == 10, len(manifest))
actual = {p.removeprefix(prefix) for p in index if p.startswith(prefix)}
check('directory_exact_set', actual == set(manifest) | {'MANIFEST.json', 'README.md'}, sorted(actual))
check('C6_RUN_log_absent_in_fixed_tree', 'C6_RUN.log' not in actual)
for name, expected in manifest.items():
    check('manifest_member:' + name, sha(files[prefix + name]) == expected)

sobol = json.loads(files[prefix + 'SOBOL_PHASE_A.json'])
for name, record in sobol['arrays'].items():
    b = files[prefix + 'sobol_' + name + '.npy']
    check('npy_magic:' + name, b[:8] == b'\x93NUMPY\x01\x00')
    n = int.from_bytes(b[8:10], 'little')
    header = ast.literal_eval(b[10:10+n].decode('ascii').strip())
    payload = b[10+n:]
    check('npy_header:' + name, header == {'descr': '<f8', 'fortran_order': False, 'shape': (64, 4)}, header)
    check('npy_payload_length:' + name, len(payload) == 64 * 4 * 8, len(payload))
    check('npy_sha:' + name, sha(b) == record['npy_sha256'])
    check('npy_raw_sha:' + name, sha(payload) == record['raw_float64_le_sha256'])

base = 'bms-balancing/docs/REIL_EXTERNAL_VALIDATION_PROTOCOL_v2'
for suffix in ['', '_ANNEX_A', '_ANNEX_B', '_ANNEX_C']:
    p = base + suffix + '.md'
    check('prior_document_unchanged:' + suffix, prior['files'][p]['sha'] == index[p]['sha'])
p = 'wiki/raw/papers/li2026_half-cell-fitting-multiobjective-benchmark.md'
check('raw_digest_unchanged', prior['files'][p]['sha'] == index[p]['sha'])
core = 'bms-balancing/docs/REIL_C1_CORE_SPEC_20261005.md'
old = prior['files'][core]['content'].splitlines()
new = snap['files'][core]['content'].splitlines()
diff = list(difflib.unified_diff(old, new, fromfile='prior C1-core', tofile='current C1-core', lineterm=''))
opts = json.loads(files[prefix + 'COBYQA_OPTIONS.json'])
check('cobyqa_expected_eight_option_names', set(opts['options']) == {'disp','maxfev','maxiter','f_target','feasibility_tol','initial_tr_radius','final_tr_radius','scale'})
check('sobol_rng_keyword', sobol['seed_keyword'] == 'rng' and 'rng=<seed>' in sobol['call'])
result = {'scope': 'Reviewer byte/hash/header checks, not submitted C6 test reruns or independent environment measurements.', 'fixed_commit': snap['fixed_commit'], 'passed': sum(c['pass'] for c in checks), 'failed': sum(not c['pass'] for c in checks), 'checks': checks, 'core_diff': diff, 'limitations': ['C6_RUN.log absent from fixed tree.', 'Supplied code, REIL observations and notebooks were not opened.', 'No environment rebuilt; no source tests, optimizer or Sobol generator executed.']}
print(json.dumps(result, ensure_ascii=False, indent=2))
