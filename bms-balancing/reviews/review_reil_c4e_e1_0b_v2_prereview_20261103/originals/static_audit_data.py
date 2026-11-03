"""Reviewer-owned data audit: hash, copy verified unchanged bytes, parse AST only.

No received Python is imported, compiled, executed, or tested. No Git fixture,
launcher, step runner, subprocess from received code, ruff, or probe is run.
"""
import ast
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / 'reil_c4e_e1_0b_prereview_20261030'
DOCREL = Path('bms-balancing/docs')
NEW = ROOT / 'source' / DOCREL
OLD = PRIOR / 'source' / DOCREL
BASIS = ROOT / 'basis' / 'unchanged_at_pin'
BASE = '90a842a9df9eb676c20ce1b9d4babf0cf0c5d637'
HEAD = '421d746e3676f7444fbf18355aecbf8d2da8bcf3'
issues = []


def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def ident(p):
    raw = p.read_bytes()
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def tree(p):
    return ast.parse(p.read_text(encoding='utf-8'), filename=p.name)


def check(value, label):
    if not value:
        issues.append(label)
    return bool(value)


def literal(t, name):
    return ast.literal_eval(next(n.value for n in t.body if isinstance(n, ast.Assign)
                                and any(isinstance(x, ast.Name) and x.id == name for x in n.targets)))


def nodekey(n, i):
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign):
        return 'assign:' + ','.join(ast.unparse(t) for t in n.targets)
    if isinstance(n, (ast.Import, ast.ImportFrom)):
        return 'import:' + ast.dump(n, include_attributes=False)
    if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
        return 'docstring'
    if isinstance(n, ast.If):
        return 'if:' + ast.unparse(n.test)
    return type(n).__name__ + ':' + str(i)


def nodes(t):
    out, occurrences = {}, {}
    for i, n in enumerate(t.body):
        key = nodekey(n, i)
        occurrences[key] = occurrences.get(key, 0) + 1
        if occurrences[key] > 1:
            key += ' #' + str(occurrences[key])
        out[key] = ast.dump(n, include_attributes=False)
    return out


def diff(a, b):
    aa, bb = nodes(tree(a)), nodes(tree(b))
    same = sorted(k for k in aa.keys() & bb.keys() if aa[k] == bb[k])
    return {'same_including_main_if': len(same),
            'same_excluding_if': sum(not k.startswith('if:') for k in same),
            'changed': sorted(k for k in aa.keys() & bb.keys() if aa[k] != bb[k]),
            'added': sorted(bb.keys() - aa.keys()), 'removed': sorted(aa.keys() - bb.keys())}


prior_before = {p.relative_to(PRIOR).as_posix(): ident(p) for p in PRIOR.rglob('*') if p.is_file()}
compare = load(ROOT / 'COMPARE_FROM_PRIOR.json')
assert compare['base'] == BASE and compare['head'] == HEAD
assert compare['status'] == 'ahead' and compare['behind_by'] == 0 and compare['ahead_by'] == 4
assert compare['too_large'] in (None, False) and len(compare['files']) == 56
changed = {x['filename'] for x in compare['files']} | {x['previous_filename'] for x in compare['files'] if x.get('previous_filename')}
assert len({x['filename'] for x in compare['files']}) == 56
copied = []


def unchanged_copy(rel, src):
    rel = Path(rel).as_posix()
    assert rel not in changed, ('Cannot inherit a changed file', rel)
    dest = BASIS / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        assert dest.read_bytes() == src.read_bytes(), ('Existing basis differs', rel)
    else:
        shutil.copyfile(src, dest)
    copied.append({'repository_path': rel, 'source': src.relative_to(PRIOR).as_posix(),
                   'captured': dest.relative_to(ROOT).as_posix(), **ident(dest),
                   'unchanged_by_complete_compare': True})
    return dest


source_identities = []
for row in load(ROOT / 'SOURCE_IDENTITIES.json'):
    p = ROOT / 'source' / row['path']
    raw = p.read_bytes()
    blob_sha = hashlib.sha1(b'blob ' + str(len(raw)).encode('ascii') + b'\0' + raw).hexdigest()
    match = check(ident(p) == {k: row[k] for k in ('bytes', 'sha256')} and blob_sha == row['blob_sha'],
                  'Captured source identity mismatch: ' + row['path'])
    source_identities.append({'path': row['path'], **ident(p), 'blob_sha': blob_sha, 'match': match})

unchanged_drafts = [
    'REIL_C4E1_LAUNCHER_DRAFT_v6_20261030.py.txt',
    'REIL_C4E1_RUNNER_CONTROLS_DRAFT_v4_20261030.py.txt',
    'REIL_C4E1_0B_END_WRITER_DRAFT_20261030.py.txt',
]
draft_paths = {name: unchanged_copy(DOCREL / name, OLD / name) for name in unchanged_drafts}
controls_name = 'REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v7_20261030.py.txt'
runner_name = 'REIL_C4E1_STEP_RUNNER_DRAFT_v7_20261030.py.txt'
draft_paths.update({controls_name: NEW / controls_name, runner_name: NEW / runner_name})
drafts = [{'file': name, **ident(path), 'AST_parse_ok': isinstance(tree(path), ast.Module)} for name, path in draft_paths.items()]
runner = tree(NEW / runner_name)
fixed, red, green = [literal(runner, k) for k in ('_FIXED', 'RED_LAUNCH', 'IMPL')]
launchpath = literal(runner, 'LAUNCH')
check(len(fixed) == 13, '_FIXED count must be 13')
overrides = {'bms-balancing/tests/test_reil_c4e1_launch.py': NEW / controls_name,
             'bms-balancing/tests/test_reil_c4e1_runner.py': draft_paths[unchanged_drafts[1]]}
seals = []
for rel, expected in {launchpath: red, **fixed}.items():
    p = overrides.get(rel)
    if p is None:
        p = unchanged_copy(rel, PRIOR / 'basis' / 'unchanged_at_pin' / rel)
    actual = ident(p)
    seals.append({'path': rel, 'phase': 'RED' if rel == launchpath else 'both', 'expected': expected,
                  'actual': actual, 'match': check(actual == expected, 'Seal mismatch: ' + rel),
                  'source': p.relative_to(ROOT).as_posix()})
impl = draft_paths[unchanged_drafts[0]]
seals.append({'path': launchpath, 'phase': 'GREEN', 'expected': green, 'actual': ident(impl),
              'match': check(ident(impl) == green, 'GREEN seal mismatch'), 'source': impl.relative_to(ROOT).as_posix()})
check(len(seals) == 15, 'Expected 15 unique phase-aware seal rows')

controls_diff = diff(OLD / controls_name.replace('_v7_', '_v6_'), NEW / controls_name)
runner_diff = diff(OLD / runner_name.replace('_v7_', '_v6_'), NEW / runner_name)
controls_ast = tree(NEW / controls_name)
functions = {n.name: n for n in controls_ast.body if isinstance(n, ast.FunctionDef)}
testnames = {int(re.match(r'test_l(\d+)_', n).group(1)): n for n in functions if re.match(r'test_l\d+_', n)}
allowed_controls = sorted(['docstring'] + [testnames[i] for i in (23, 29, 30)])
check(controls_diff == {'same_including_main_if': 74, 'same_excluding_if': 74,
                       'changed': allowed_controls, 'added': ['_normal_fetch_meta'], 'removed': []},
      'Controls AST diff differs from allowed scope / 74 unchanged nodes')
check(runner_diff == {'same_including_main_if': 59, 'same_excluding_if': 58,
                     'changed': ['assign:_FIXED', 'docstring'], 'added': [], 'removed': []},
      'Runner AST diff differs from allowed scope / 59 unchanged nodes')
old_fixed = literal(tree(OLD / runner_name.replace('_v7_', '_v6_')), '_FIXED')
fixed_changes = [k for k in set(fixed) | set(old_fixed) if fixed.get(k) != old_fixed.get(k)]
check(fixed_changes == ['bms-balancing/tests/test_reil_c4e1_launch.py'], 'Runner changed more than launcher controls seal')

old_runner_controls = unchanged_copy('bms-balancing/tests/test_reil_c4e1_runner.py',
                                     PRIOR / 'basis' / 'unchanged_at_pin/bms-balancing/tests/test_reil_c4e1_runner.py')
runner_controls_diff = diff(old_runner_controls, draft_paths[unchanged_drafts[1]])
check(runner_controls_diff['same_including_main_if'] == 46 and len(runner_controls_diff['changed']) == 6,
      'Runner controls corrected unchanged count is not 46 / changed count not 6')
count_paths = [NEW / controls_name, draft_paths[unchanged_drafts[1]],
               BASIS / 'bms-balancing/tests/test_reil_c4e.py', BASIS / 'bms-balancing/tests/test_reil_c4e_fix.py']
counts = [{'file': p.relative_to(ROOT).as_posix(), 'test_functions': sum(isinstance(n, ast.FunctionDef) and n.name.startswith('test_') for n in tree(p).body)} for p in count_paths]
check([x['test_functions'] for x in counts] == [33, 11, 21, 6], 'Test function count mismatch')

request = (NEW / 'REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md').read_text(encoding='utf-8')
prior_request = (OLD / 'REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md').read_text(encoding='utf-8')
def red_table(s):
    return {int(m.group(1)): {'nodeid': m.group(2), 'exception': m.group(3), 'message': m.group(4), 'line': int(m.group(5))}
            for m in re.finditer(r'^\| (\d+) \| `(test_l[^`]+)` \| (AssertionError|AttributeError) \| (.*?) \| (\d+) \|$', s, re.M)}
redrows, oldred = red_table(request), red_table(prior_request)
check(len(redrows) == 9, 'RED table must contain nine rows')
red_locations = []
for i, row in redrows.items():
    n = functions[row['nodeid']]
    hits = [x for x in ast.walk(n) if isinstance(x, (ast.Assert, ast.Assign)) and x.lineno == row['line']]
    expected_type = ast.Assert if row['exception'] == 'AssertionError' else ast.Assign
    match = len(hits) == 1 and isinstance(hits[0], expected_type)
    oldn = next(x for x in tree(OLD / controls_name.replace('_v7_', '_v6_')).body if isinstance(x, ast.FunctionDef) and x.name == row['nodeid'])
    oldhits = [x for x in ast.walk(oldn) if isinstance(x, (ast.Assert, ast.Assign)) and x.lineno == oldred[i]['line']]
    unchanged_statement = match and len(oldhits) == 1 and ast.dump(hits[0], include_attributes=False) == ast.dump(oldhits[0], include_attributes=False)
    check(match and unchanged_statement, 'Predicted RED line / statement mismatch: ' + row['nodeid'])
    check({k: v for k, v in row.items() if k != 'line'} == {k: v for k, v in oldred[i].items() if k != 'line'},
          'RED nodeid / exception / message changed: ' + row['nodeid'])
    red_locations.append({**row, 'AST_node': type(hits[0]).__name__ if hits else None,
                          'source': ast.unparse(hits[0]) if hits else None, 'same_statement_as_v6': unchanged_statement})
check([x['line'] for x in red_locations] == [460,707,749,897,946,988,999,1030,1065], 'Unexpected RED predicted line list')

v5 = tree(BASIS / launchpath)
def bindings(t):
    out = {'__file__', '__name__', '__doc__', '__package__', '__loader__', '__spec__', '__builtins__', '__cached__'}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            out.add(n.name)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            out.update(x.asname or x.name.split('.')[0] for x in n.names)
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            for x in ast.walk(n):
                if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Store):
                    out.add(x.id)
    return out
v5bindings = bindings(v5)
v6bindings = bindings(tree(impl))
allattrs = [{'attribute': n.attr, 'line': n.lineno} for n in ast.walk(controls_ast)
            if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'L']
missing = [x for x in allattrs if x['attribute'] not in v5bindings]
guard_attrs = []
for testid in (23,29,30):
    name = testnames[testid]
    cutoff = next(x['line'] for x in red_locations if x['nodeid'] == name)
    prefix = [n for n in ast.walk(functions[name]) if getattr(n, 'lineno', cutoff) < cutoff]
    expanded = list(prefix)
    pending = {n.func.id for n in prefix if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in functions}
    helpers = set()
    while pending:
        key = pending.pop()
        if key in helpers:
            continue
        helpers.add(key)
        ns = list(ast.walk(functions[key]))
        expanded.extend(ns)
        pending.update(n.func.id for n in ns if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in functions and n.func.id not in helpers)
    attrs = sorted({n.attr for n in expanded if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'L'})
    absent = sorted(set(attrs) - v5bindings)
    check(not absent, 'Missing v5 L attribute before expected RED in ' + name)
    guard_attrs.append({'test': name, 'expected_failure_line': cutoff, 'direct_and_helper_L_attributes': attrs,
                        'transitive_local_helpers': sorted(helpers), 'missing_from_v5': absent})
check(not (set(x['attribute'] for x in allattrs) - v6bindings), 'Controls L attribute missing from v6')

attachments = []
for file, localname in [('REIL_C4E_E1_0B_PREREVIEW_SEND_v2_20261030.md', 'REIL_C4E_E1_0B_PREREVIEW_SEND_v2_20261030.md'),
                        ('REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md', 'REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030 (1).md')]:
    p = Path('C:/Users/Administrator/Downloads') / localname
    match = check(p.read_bytes() == (NEW / file).read_bytes(), 'Attachment bytes mismatch: ' + localname)
    attachments.append({'local_path': str(p), 'repository_path': (DOCREL / file).as_posix(), **ident(p), 'same_bytes_at_pinned_commit': match})
    target = ROOT / 'basis' / 'attachments' / localname
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        assert target.read_bytes() == p.read_bytes()
    else:
        shutil.copyfile(p, target)

draft_doc_rows = []
for name, path in draft_paths.items():
    row = next((line for line in request.splitlines() if line.startswith('| `' + name + '`')), '')
    actual = ident(path)
    match = actual['sha256'] in row and f"{actual['bytes']:,}" in row
    check(match, 'Request draft hash/bytes table mismatch: ' + name)
    draft_doc_rows.append({'name': name, 'matches_document': match})
sha_cmd = next(line for line in request.splitlines() if 'sha256sum <초안 다섯> <복사본 넷>' in line)
sha_desc = next(line for line in request.splitlines() if line.startswith('- **`00_start.txt`**'))
check('sha256 열' in sha_desc, 'Corrected 00_start description not ten')
check('실행기 대조 v3 → v4 **46**' in request, 'Corrected AST count not 46 in request')
old_status = (OLD / 'REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
new_status = (NEW / 'REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
check(new_status.startswith(old_status), 'Prior status bytes no longer exact prefix')
prior_after = {p.relative_to(PRIOR).as_posix(): ident(p) for p in PRIOR.rglob('*') if p.is_file()}
check(prior_before == prior_after, 'Prior review basis changed during audit')
result = {
    'kind': 'E1_0B_V2_REVIEWER_STATIC_DATA_AUDIT', 'pinned_commit': HEAD, 'prior_commit': BASE,
    'method': 'Reviewer-owned data/AST audit only; received code never imported or executed',
    'compare': {'file_count': len(compare['files']), 'status': compare['status'], 'ahead_by': compare['ahead_by'],
                'behind_by': compare['behind_by'], 'too_large': compare['too_large'], 'complete_file_list_under_300': True},
    'captured_source_identities': source_identities, 'attachments': attachments,
    'draft_AST_parse_count': len(drafts), 'drafts': drafts, 'unchanged_inherited_sources': copied,
    'unchanged_scope': 'Immutable Git comparison + prior captured byte identities; not remote working-tree observation',
    'fixed_seal_rows': seals, 'fixed_seal_match_count': sum(x['match'] for x in seals),
    'target_count_each_phase': len(fixed) + 1, 'distinct_phase_aware_seal_rows': len(seals),
    'top_level_AST_comparison': {'launcher_controls_v6_to_v7': controls_diff, 'step_runner_v6_to_v7': runner_diff,
                                 'runner_controls_v3_to_v4': runner_controls_diff},
    'runner_FIXED_changed_keys': fixed_changes, 'test_function_counts': counts,
    'planned_GREEN_total': sum(x['test_functions'] for x in counts), 'planned_RED': {'expected_failures': 9, 'expected_passes':24},
    'predicted_RED_locations': red_locations, 'v5_missing_L_attributes_all_occurrences': missing,
    'pre_expected_failure_L_attribute_checks': guard_attrs,
    'v6_missing_L_attributes': sorted(set(x['attribute'] for x in allattrs) - v6bindings),
    'document_draft_table': draft_doc_rows, 'numeric_corrections': {'start_sha_literal_count': 5 + 4 + 1,
    'start_sha_command': sha_cmd, 'start_sha_description': sha_desc, 'runner_controls_same_nodes': 46},
    'prior_status_prefix_preserved': new_status.startswith(old_status), 'prior_review_basis_preserved': prior_before == prior_after,
    'functional_tests': 0, 'received_code_execution': 0, 'target_imports': 0, 'ruff_runs':0, 'Git_fixture_or_probe':0,
    'mismatches': issues, 'result': 'STATIC_DATA_MATCH' if not issues else 'MISMATCHES_FOUND',
}
(ROOT / 'STATIC_AUDIT.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'result': result['result'], 'mismatches': issues, 'seals': result['fixed_seal_match_count'],
                  'GREEN_total': result['planned_GREEN_total'], 'AST_diff': result['top_level_AST_comparison'],
                  'pre_failure_L_missing': [x['missing_from_v5'] for x in guard_attrs],
                  'prior_review_basis_preserved': result['prior_review_basis_preserved']}, ensure_ascii=False))
