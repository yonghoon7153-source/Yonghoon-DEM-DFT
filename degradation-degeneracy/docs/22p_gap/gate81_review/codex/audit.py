"""Reviewer-owned data/static inspection; never imports or executes subject code."""
from pathlib import Path
import ast
import hashlib
import json
import subprocess

O = Path(__file__).resolve().parent
W = Path('C:/Users/Administrator/Documents/Codex/g80_20260928')
D = W / 'degradation-degeneracy'
U = Path('C:/Users/Administrator/Downloads/GATE81_REQUEST.md')
BASE = '9a26dd5f31ca6fae45d5a55f5c59e33408371984'
HEAD = '88ac144a8bb9a0e805b06e8240d1d64a4ca6a16e'
CODE = '6ffa98d4df542aa42abde2f94685beffec33312c'

def git(*a):
    return subprocess.check_output(['git', '-C', str(W), *a])

def identity(b):
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def save(n, data):
    p = O / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def copy_bytes(n, b):
    p = O / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)

def in_scope(p):
    prefix = 'degradation-degeneracy/'
    if not p.startswith(prefix):
        return False
    r = p[len(prefix):]
    return r.startswith(('src/', 'tools/', 'configs/', 'scripts/')) or r == 'run.sh' or ('/' not in r and r.startswith('requirements') and r.endswith('.txt'))

assert git('rev-parse', 'HEAD').decode().strip() == BASE
assert not git('status', '--porcelain=v1', '-uall').strip()
remote = json.loads((O / 'evidence/REMOTE_COMPARE.json').read_text(encoding='utf-8'))
assert remote['base'] == BASE and remote['head'] == HEAD
assert remote['status'] == 'ahead' and remote['behind_by'] == 0
assert remote['merge_base_commit']['sha'] == BASE
assert not remote.get('too_large')
assert not any(in_scope(f['filename']) for f in remote['files'])
scope = sorted(p for p in git('ls-files', '-z').decode().split('\0') if in_scope(p))
assert len(scope) == 58
refs = [
    'src/fitting.py', 'src/io.py', 'src/grid.py', 'tools/design_wire.py',
    'tools/design_golden.yaml', 'tools/gen_design_golden.py', 'tools/preserve.py',
    'docs/22p_gap/STAGE3_CONTRACT.md', 'docs/22p_gap/GATE78_REQUEST.md',
    'docs/22p_gap/GATE79_REQUEST.md', 'docs/22p_gap/GATE80_REQUEST.md',
    'docs/22p_gap/CLAIM_STATUS.yaml', 'docs/22p_gap/row_projection.py',
    'tests/test_design_wire.py', 'tests/test_gate79_stage3_logging.py',
]
selected = sorted(set(scope) | {'degradation-degeneracy/' + p for p in refs})
before = {p: identity((W / p).read_bytes()) for p in selected}
before[str(U)] = identity(U.read_bytes())
save('SOURCE_BEFORE.json', before)
dig = hashlib.sha256()
for p in scope:
    b = (W / p).read_bytes()
    assert b == git('show', BASE + ':' + p), p
    dig.update(p.removeprefix('degradation-degeneracy/').encode())
    dig.update(b)
assert dig.hexdigest()[:16] == 'eda3feb8f4536511'
assert not git('diff', '--no-ext-diff', CODE, BASE, '--', *scope)

rf = json.loads((O / 'evidence/REMOTE_REQUEST_RESPONSE.json').read_text(encoding='utf-8'))
rb = rf['content'].encode('utf-8')
blob = hashlib.sha1(b'blob ' + str(len(rb)).encode() + b'\0' + rb).hexdigest()
assert blob == rf['sha'], 'Connector content does not reproduce Git blob'
ub = U.read_bytes()
normalized_equal = ub.decode('utf-8-sig').replace('\r\n', '\n').rstrip('\n') == rb.decode('utf-8').replace('\r\n', '\n').rstrip('\n')
assert normalized_equal
copy_bytes('reference/GATE81_REQUEST.received.md', ub)
copy_bytes('reference/GATE81_REQUEST.repository.md', rb)
for p in refs:
    assert not any(f['filename'] == 'degradation-degeneracy/' + p for f in remote['files'])
    copy_bytes('reference/' + p, (D / p).read_bytes())
for p in ['REVIEW_KO.md', 'DECISION.json']:
    copy_bytes('prior_gate80/' + p, (O.parent / 'gate80_review_20260928' / p).read_bytes())

def functions(p):
    tree = ast.parse((D / p).read_bytes())
    return tree, {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

ft, ff = functions('src/fitting.py')
wt, wf = functions('tools/design_wire.py')
pt, pf = functions('tools/preserve.py')
it, inf = functions('src/io.py')
nt, nf = functions('tests/test_gate79_stage3_logging.py')
def snippet(p, fn):
    return ast.get_source_segment((D / p).read_text(encoding='utf-8'), fn)

assert 'rng.uniform(lb, ub)' in snippet('src/fitting.py', ff['fit'])
assert 'np.clip' in snippet('src/fitting.py', ff['fit'])
assert 'v6_prep_logging' in snippet('src/fitting.py', ff['normalize_restart_record'])
assert 'legacy_dict' in snippet('src/fitting.py', ff['normalize_restart_record'])
assert 'digest(self.envelope())' in snippet('tools/preserve.py', pf['planned_id'])
assert 'planned-leg/v3' in snippet('tools/preserve.py', pf['envelope'])
assert 'candidate/v2' in snippet('tools/design_wire.py', wf['candidate_id'])
assert 'sig_version' in snippet('src/io.py', inf['validate_provenance'])
assert not any('design_wire' in (D / 'src' / p.name).read_text(encoding='utf-8') for p in (D / 'src').glob('*.py'))

facts = {
    'request_received': identity(ub), 'request_repository': identity(rb),
    'repository_blob_sha': blob, 'received_raw_identical': ub == rb,
    'received_normalized_text_identical': normalized_equal,
    'local_verified_base': BASE, 'remote_request_head_observed': HEAD,
    'code_commit': CODE, 'remote_compare_ahead_by': remote['ahead_by'],
    'remote_compare_changed_files': len(remote['files']),
    'remote_RUN_SCOPE_changed_files': [],
    'local_RUN_SCOPE_files': len(scope), 'source_digest': dig.hexdigest()[:16],
    'method': 'Local cached fixed code bytes plus connector compare proving no intervening RUN_SCOPE changes; no checkout or execution at remote HEAD',
    'functions': {p: {k: {'line': f.lineno, 'end_line': f.end_lineno} for k, f in fs.items() if k in names} for p, fs, names in [
        ('src/fitting.py', ff, ['fit', '_fit_one', 'normalize_restart_record']),
        ('src/io.py', inf, ['_restart_ok', 'validate_provenance']),
        ('tools/design_wire.py', wf, ['candidate_id', 'bank_id', 'design_binding', 'canonical_design_spec']),
        ('tools/preserve.py', pf, ['envelope', 'planned_id', 'check_envelope', 'seal_payload', 'run_transaction', 'leg_run_spec', 'run_spec_digest']),
    ]},
    'historical_logging_test': [n for n in nf if 'g79_06' in n],
    'subject_modules_imported': 0, 'subject_functions_called': 0,
    'pytest_smoke_mutation': 0, 'COMSOL_JVM': 0, 'restore_rescore_receipt_regeneration': 0,
    'implementation_start': False, 'execution_GO': False,
}
save('STATIC_DATA_AUDIT.json', facts)
after = {p: identity((Path(p) if Path(p).is_absolute() else W / p).read_bytes()) for p in before}
assert after == before
assert not git('status', '--porcelain=v1', '-uall').strip()
save('SOURCE_AFTER_CHECK.json', {'selected_files': len(before), 'unchanged': True, 'local_HEAD': BASE, 'clean': True, 'scope': 'Since reviewer audit snapshot; not all PC/remote state'})
print(json.dumps({'status': 'STATIC_DATA_AUDIT_PASS', 'head': HEAD, 'source_digest': facts['source_digest'], 'scope_files': len(scope), 'selected_files': len(before), 'raw_request_identical': ub == rb, 'normalized_request_identical': normalized_equal, 'subject_execution': 0}))
