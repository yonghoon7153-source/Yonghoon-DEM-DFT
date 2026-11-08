"""Tiny independent fixture/branch checks, not a research or full-gate run.

The four mutation checks call production functions on minimal memory records.
read_attempt alone is replaced by an explicit synthetic attempt identity. Paths
are nonexistent and early return happens before disk provenance checking.
"""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import sys

OUT = Path(__file__).resolve().parent
REPO = Path(os.environ.get('RINT_REVIEW_REPO', str(OUT.parent / 'package/repo'))).resolve()
sys.path.insert(0, str(REPO / 'scripts'))
import rint_r_chain as RR

source_path = REPO / 'scripts/rint_r_chain.py'
test_path = REPO / 'scripts/test_rint_r_chain.py'
source = source_path.read_text(encoding='utf-8')
tests = test_path.read_text(encoding='utf-8')
before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [source_path, test_path, REPO / 'docs/reviews/findings.json']}
results = {}

def record(name, actual, expected):
    results[name] = {'actual': actual, 'expected': expected, 'pass': actual == expected}

ct_node = next(n for n in ast.parse(tests).body if isinstance(n, ast.FunctionDef) and n.name == 'ct06_pub')
fixture_ns = {'hashlib': hashlib, 'SBE_KIT': 'kit_SBE_vgcf100'}
exec(compile(ast.Module(body=[ct_node], type_ignores=[]), str(test_path), 'exec'), fixture_ns)
fixture = fixture_ns['ct06_pub']

for kit in ['kit_SBE_vgcf100', 'kit_DBE_vgcf100']:
    rec = {'kit': kit, 'arms': 1, 'arm_list': None}
    pub = fixture(kit=kit)
    record(kit + '_success', RR.arms_read_kind([pub], rec)[0], 'verified')
    record(kit + '_failure_ids', RR.arms_read_kind([{k: pub[k] for k in RR.ARM_FILE_ID_KEYS}], rec)[0], 'file_ids')
    record(kit + '_prefix_value', RR.arm_file_prefix(kit), 'p2_' + kit[len('kit_'):] + '_')
    record(kit + '_public_keys', sorted(pub), sorted(RR.ARM_PUBLIC))
    for key, val in [('protocol_id', 'p3ca-test'), ('sid_fp', 'f' * 16)]:
        record(kit + '_old_' + key, RR.arms_read_kind([dict(pub, **{key: val})], rec)[0], 'bad')

fn_nodes = {n.name: n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef)}
def compile_fn(name, old=None, new=None, ro=1):
    fn_source = ast.get_source_segment(source, fn_nodes[name])
    if old is not None:
        assert fn_source.count(old) == 1
        fn_source = fn_source.replace(old, new)
    ns = dict(RR.__dict__)
    ns['read_attempt'] = lambda _folder: {'n': 3 if ro == 2 else 2, 'resume_of': ro}
    exec(compile(fn_source, str(source_path) + ':synthetic', 'exec'), ns)
    return ns[name]

def outcome(call):
    try:
        result = call()
        return 'None' if result is None else ('reason' if isinstance(result, str) and result else repr(result))
    except Exception as exc:
        return type(exc).__name__

def summ(frm=1, copied=None, compared=None):
    copies = [] if copied is None else [{'name': 'C', 'copied_from': copied}]
    return {'resume': {'from': frm, 'copied': [] if copied is None else ['C'], 'rerun': 'R', 'compared': [] if compared is None else compared, 'determinism': None}, 'runs': copies + [{'name': 'R'}]}

cases = [
    ('M14', 'resume_rerun_problem', "type(r['copied_from']) is int and r['copied_from'] == frm", "r['copied_from'] == frm", summ(copied=True), 1, 'None'),
    ('M18', 'resume_rerun_problem', 'if cmp_ != [] or det is not None:', 'if det is not None:', summ(compared=[{'file': 'x', 'same': True}]), 1, 'None'),
    ('M54', 'resume_rerun_problem', 'lo = ro if ro is not None else 1', 'lo = 1', summ(), 2, 'None'),
    ('M47', 'resume_mismatch_problem', "if not (type(x) is dict and x.get('same') is True)]", "if not (x.get('same') is True)]", summ(compared=[5]), 1, 'AttributeError'),
]
for name, fn, old, new, s, ro, mutant_want in cases:
    def run(f):
        if fn == 'resume_mismatch_problem':
            return f(copy.deepcopy(s), 'TIME_LIMIT', 'NEXT')
        return f(copy.deepcopy(s), OUT / 'nonexistent_synthetic' / ('attempt_3' if ro == 2 else 'attempt_2'), 'TIME_LIMIT', 'R')
    record(name + '_current_rejects', outcome(lambda: run(compile_fn(fn, ro=ro))), 'reason')
    record(name + '_mutation_changes_result', outcome(lambda: run(compile_fn(fn, old, new, ro=ro))), mutant_want)

for name, s, ro in [('copy_int', summ(copied=1), 1), ('precompare_empty', summ(), 1), ('from_equals_resumeof', summ(frm=2), 2)]:
    record('positive_' + name, outcome(lambda: compile_fn('resume_rerun_problem', ro=ro)(s, OUT / 'nonexistent_synthetic' / ('attempt_3' if ro == 2 else 'attempt_2'), 'TIME_LIMIT', 'R')), 'None')

after = {p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in before}
record('source_and_ledger_unchanged', before == after, True)
report = {'environment': sys.version, 'scope': __doc__, 'count': len(results), 'passed': sum(x['pass'] for x in results.values()), 'checks': results, 'sha256': before}
(OUT / 'tiny_checks.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'count': report['count'], 'passed': report['passed'], 'failed': [k for k, v in results.items() if not v['pass']]}, ensure_ascii=False))
sys.exit(0 if report['count'] == report['passed'] else 1)
