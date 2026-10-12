"""Read-only R7 test-quality audit; execute exact AST fixture/mutation statements.

No source rewrites and no network/pipeline execution. Output is JSON on stdout.
"""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SOURCE = BASE / 'source' / 'scripts' / 'g2_network_reread.py'
EV = BASE / 'source' / 'docs' / 'reviews' / 'codex_gen2_network_reverify6_evidence_20261011' / 'evidence'
CID = 'case15_network'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


current = load_module('r7_current', SOURCE)
parent = load_module('r7_parent', BASE / 'parent' / 'scripts' / 'g2_network_reread.py')
tree = ast.parse(SOURCE.read_text(encoding='utf-8'))
selftest = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_selftest')
body = next(n for n in selftest.body if isinstance(n, ast.Try)).body
ns = {'json': json}


def execute_nodes(nodes):
    module = ast.Module(body=nodes, type_ignores=[])
    exec(compile(module, str(SOURCE), 'exec'), ns)


def named_assignment(node, name):
    return isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets)


fixture_start = next(i for i, n in enumerate(body) if named_assignment(n, 'solver'))
fixture_end = next(i for i, n in enumerate(body) if named_assignment(n, 'c15'))
execute_nodes(body[fixture_start:fixture_end + 1])
verdicts = current.case15_negctl_verdicts(ns['c15'], {'rc': 0}, CID)
ns['base'] = dict(
    reports={CID: ns['c15']},
    timings={CID: {'rc': 0}},
    checks=[dict(id=i, name=n, verdict=v, detail=d) for i, n, v, d in verdicts],
    rc=0,
)
execute_nodes([n for n in body if isinstance(n, ast.FunctionDef) and n.name in ('_mut', '_r')])
mutation_start = next(i for i, n in enumerate(body) if named_assignment(n, '_A15'))
mutation_end = next(i for i, n in enumerate(body) if named_assignment(n, 'V6s'))
execute_nodes(body[mutation_start:mutation_end + 1])


def adjudicate(mod, doc):
    report = doc['reports'][CID]
    timing = doc.get('timings', {}).get(CID)
    vv = mod.case15_negctl_verdicts(report, timing, CID)
    problems = mod.case15_negctl_s0b_problems(CID, report, doc['checks'], timing)
    return dict(
        passes=not problems,
        nonpass_ids=[i for i, _, v, _ in vv if v != 'PASS'],
        nonpass_details={i: d for i, _, v, d in vv if v != 'PASS'},
        exceptions=[i for i, _, _, d in vv if str(d).startswith('판정 예외 ')],
        problem_count=len(problems),
    )


cases = []
for group in ('V6', 'V6s'):
    for label, doc in ns[group].items():
        cases.append(dict(label=label, group=group, parent=adjudicate(parent, doc), current=adjudicate(current, doc)))

records = []
for label in ('positive', 'raw_sha_missing', 'raw_sha_mismatch', 'negative_area_positive', 'negative_area_missing', 'raw_sha_flag_false', 'actual_permission_error'):
    path = EV / f'r6_s0b_{label}.input.json'
    doc = json.loads(path.read_text(encoding='utf-8'))
    old = BASE / 'baseline_r6' if (BASE / 'baseline_r6').exists() else BASE.parent / 'gen2_network_reverify6_20261011'
    original = old / 'evidence' / path.name
    records.append(dict(label=label, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        original_exists=original.exists(), original_bytes_equal=(original.read_bytes() == path.read_bytes()) if original.exists() else None,
                        parent=adjudicate(parent, doc), current=adjudicate(current, doc)))

result = dict(
    source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    parent_sha256=hashlib.sha256((BASE / 'parent' / 'scripts' / 'g2_network_reread.py').read_bytes()).hexdigest(),
    synthetic_positive=dict(parent=adjudicate(parent, ns['base']), current=adjudicate(current, ns['base'])),
    counts={group: dict(total=sum(x['group'] == group for x in cases),
                        parent_accepted=sum(x['group'] == group and x['parent']['passes'] for x in cases),
                        current_accepted=sum(x['group'] == group and x['current']['passes'] for x in cases)) for group in ('V6', 'V6s')},
    cases=cases,
    imported_records=records,
)
print(json.dumps(result, ensure_ascii=False, indent=2))
