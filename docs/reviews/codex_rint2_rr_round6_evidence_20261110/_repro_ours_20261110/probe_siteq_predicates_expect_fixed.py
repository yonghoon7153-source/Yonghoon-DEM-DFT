"""Safe isolated predicate replay. Does NOT import or run siteq_probe main.

Only c02b/c26/is_netfs AST definitions are compiled. Their OS/subprocess/data
inputs are synthetic in-memory fakes; no child, host probe, /proc or write runs.
Usage: python -I -B probe_siteq_predicates.py <extracted repo root>
"""
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import posixpath
import sys
from types import SimpleNamespace

repo = Path(sys.argv[1])
source = repo / 'docs/reviews/rint2_siteq_prep_20261109/tools/siteq_probe.py'
raw = source.read_bytes()
tree = ast.parse(raw, filename=str(source))
names = {'c02b', 'c26', 'is_netfs'}
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
assert {n.name for n in nodes} == names
code = compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec')
unit = {'python_minor': '3.8', 'numpy': '1.24.4', 'scipy': '1.10.1'}
calls = []
response = SimpleNamespace(returncode=0, stdout=b'', stderr=b'')

def fake_run(*args, **kwargs):
    calls.append({'argv': args[0], 'timeout': kwargs.get('timeout')})
    return response

path_mock = SimpleNamespace(abspath=posixpath.abspath, expanduser=lambda s: '/synthetic/home')
ns = {
    'shutil': SimpleNamespace(which=lambda _: '/synthetic/python3'),
    'sys': SimpleNamespace(executable='/synthetic/python3'),
    'subprocess': SimpleNamespace(run=fake_run, DEVNULL=-3, PIPE=-1),
    'json': json,
    'RR': SimpleNamespace(env_record=lambda: {'unit': unit.copy()}),
    'os': SimpleNamespace(path=path_mock),
    'UNIT_SNIPPET': 'NOT EXECUTED: synthetic subprocess response',
    'A': SimpleNamespace(out='/synthetic/out', repo='/synthetic/repo', plan_dirs=''),
    'NETFS': ('nfs', 'lustre', 'fuse'),
}
exec(code, ns)
out = {'source_sha256': hashlib.sha256(raw).hexdigest(),
       'executed_ast_functions': {n.name: [n.lineno, n.end_lineno] for n in nodes},
       'actual_subprocess_calls': 0,
       'actual_host_or_proc_access': False,
       'c02b': [], 'c26': [], 'provided_records': {}}
for tag, rc, stdout in [
    ('matching_unit_rc0', 0, json.dumps(dict(unit, executable='/synthetic/python3')).encode()),
    ('matching_unit_rc1', 1, json.dumps(dict(unit, executable='/synthetic/python3')).encode()),
    ('mismatched_unit_rc0', 0, json.dumps(dict(unit, numpy='bad')).encode()),
    ('invalid_json_rc0', 0, b'invalid'),
]:
    response.returncode, response.stdout = rc, stdout
    status, detail, data = ns['c02b']()
    out['c02b'].append({'case': tag, 'supplied_child_rc': rc, 'status': status,
                       'child_rc_preserved': 'returncode' in data or 'rc' in data,
                       'detail': detail, 'data': data})
assert [r['status'] for r in out['c02b']] == ['PASS', 'FAIL', 'FAIL', 'FAIL']

def fake_mount(p):
    if p == '/synthetic/missing_plan':
        return {'path': p, 'exists': False, 'error': 'FileNotFoundError'}
    if p == '/synthetic/otherfs_plan':
        return {'path': p, 'exists': True, 'fstype': 'ext4', 'st_dev': '8:2', 'writable': True}
    return {'path': p, 'exists': True, 'fstype': 'ext4', 'st_dev': '8:1', 'writable': True}

ns['mount_of'] = fake_mount
for plan in ['', '/synthetic/missing_plan', '/synthetic/otherfs_plan']:
    ns['A'].plan_dirs = plan
    status, detail, data = ns['c26']()
    out['c26'].append({'plan_dirs': plan, 'status': status, 'detail': detail,
                       'summary_rc_if_this_was_the_only_record': 1 if status in ('FAIL', 'ERROR') else 0})
assert [r['status'] for r in out['c26']] == ['PASS', 'PASS', 'WARN']

for machine in ('kgy', 'gabia'):
    p = repo / 'docs/data/rint2_siteq_20261109' / machine / 'siteq_result.json'
    d = json.loads(p.read_bytes())
    checks = {x['id']: x for x in d['checks']}
    counts = dict(Counter(x['status'] for x in d['checks']))
    assert counts == d['counts'] and len(checks) == 33
    out['provided_records'][machine] = {
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'counts': counts,
        'n_unique_checks': len(checks), 'probe_sha256': d['probe_sha256'],
        'probe_sha256_matches_read_source': d['probe_sha256'] == out['source_sha256'],
        'pin': d['pin'], 'uid': d['uid'], 'euid': d['euid'], 'plan_dirs': d['plan_dirs'],
        'utc_start': d['utc_start'], 'utc_end': d['utc_end'], 'seconds': d['seconds'],
        'summary_rc_recomputed_from_statuses': 1 if any(c['status'] in ('FAIL', 'ERROR') for c in d['checks']) else 0,
        'C02_unit': checks['C02']['data']['unit'],
        'C02b': checks['C02b']['data'],
        'C04_key': checks['C04']['data']['code_key_sha256'],
        'C13b': checks['C13b'], 'C16_mode000': checks['C16']['data']['got']['mode000'],
        'C17': checks['C17']['data'], 'C18': checks['C18']['data'],
        'C26': checks['C26'],
    }
print(json.dumps(out, ensure_ascii=False, indent=2))
