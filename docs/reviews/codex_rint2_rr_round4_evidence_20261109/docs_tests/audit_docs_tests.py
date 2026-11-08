"""Independent read-only audit of supplied source, tests, and raw evidence.

Run with the review's Windows Python -I -X utf8 -B. No repository writes.
"""
from pathlib import Path
import ast
import collections
import difflib
import hashlib
import json
import os
import re
import sys

OUT = Path(__file__).resolve().parent
REVIEW = OUT.parent
CUR = Path(os.environ.get('RINT_REVIEW_REPO', str(REVIEW / 'package/repo'))).resolve()
OLD = Path(os.environ.get('RINT_REVIEW_OLD_REPO', str(REVIEW / 'reference_round3'))).resolve()
E = CUR / 'docs/reviews/rint2_rr2_fix_evidence_20261105'

def text(p):
    return p.read_text(encoding='utf-8')

def dump(name, val):
    (OUT / name).write_text(json.dumps(val, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def funcs(src):
    tree = ast.parse(src)
    return {n.name: ast.dump(n, include_attributes=False) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}

def literal_assign(path, name):
    tree = ast.parse(text(path))
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets):
            return ast.literal_eval(n.value)
    raise KeyError(name)

diffs = {}
for rel in ['scripts/test_rint_r_chain.py', 'scripts/rint_r_chain.py', 'docs/reviews/codex_rint2_rr_round3_request_20261108.md']:
    before, after = text(OLD / rel), text(CUR / rel)
    stem = Path(rel).stem
    (OUT / (stem + '.diff')).write_text(''.join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), fromfile='round3/' + rel, tofile='round4/' + rel)), encoding='utf-8')
    detail = {'old_sha256': hashlib.sha256((OLD / rel).read_bytes()).hexdigest(), 'new_sha256': hashlib.sha256((CUR / rel).read_bytes()).hexdigest()}
    if rel.endswith('.py'):
        bf, af = funcs(before), funcs(after)
        detail.update(added=sorted(af.keys() - bf.keys()), removed=sorted(bf.keys() - af.keys()), changed_existing=sorted(k for k in bf.keys() & af.keys() if bf[k] != af[k]))
    diffs[rel] = detail
dump('diff_inventory.json', diffs)

row_inventory = {}
for folder, filenames in {
    'rr3_fix': ['before_RR3_rows.json', 'after_RR3_rows.json', 'cross_oldtests_fixedchain_rows.json'],
    'pa13_fix': ['pa13_rows_before.json', 'pa13_rows_after.json'],
    'pa14_fix': ['pa14_rows_before.json', 'pa14_rows_after.json'],
}.items():
    for filename in filenames:
        data = json.loads(text(E / folder / 'logs' / filename))
        info = {}
        for key, value in data.items():
            if not isinstance(value, dict):
                info[key] = value
                continue
            detail = value.get('detail', value.get('why', value))
            info[key] = {'ok': value.get('pass', value.get('ok')), 'n': detail.get('n'), 'n_bad': detail.get('n_bad'), 'row_count': len(detail['rows']) if isinstance(detail.get('rows'), dict) else None, 'bad_keys': sorted(detail.get('bad', {}))}
        row_inventory[folder + '/' + filename] = info
dump('row_counts.json', row_inventory)

raw_logs = {}
for folder in ['rr3_fix', 'pa13_fix', 'pa14_fix', 'preattack13', 'preattack14']:
    base = E / folder
    for p in sorted(base.rglob('*')):
        if p.suffix not in ('.log', '.out') or p.name.startswith('probe'):
            continue
        src = text(p)
        lines = src.splitlines()
        summary = [s for s in lines if not re.match(r'^\s+(PASS|FAIL)\s+', s) and re.search(r'(test_rint_r_chain:|PASS.*FAIL|FAIL.*PASS|passed|11.+통과|잡힘|놓침|건너뜀|383670|300378)', s)]
        if not summary:
            continue
        # Counts are mechanically read from individual PASS/FAIL rows as well as summary.
        pass_ids = re.findall(r'^\s+PASS\s+(\S+)', src, re.M)
        fail_ids = re.findall(r'^\s+FAIL\s+(\S+)', src, re.M)
        raw_logs[str(p.relative_to(E))] = {'summaries': summary[-4:], 'pass_rows': len(pass_ids), 'fail_rows': len(fail_ids), 'fail_ids': fail_ids}
dump('raw_log_counts.json', raw_logs)

mutation = {}
for folder, filename in [('rr3_fix', 'mutation_rr3.json'), ('pa13_fix', 'mutation_results.json'), ('pa14_fix', 'mutation_results.json')]:
    data = json.loads(text(E / folder / 'logs' / filename))
    mutation[folder] = data
dump('mutation_raw_records.json', mutation)
mutation_counts = {}
for folder, data in mutation.items():
    if folder == 'rr3_fix':
        mutation_counts[folder] = {'mutants': len(data['mutants']), 'caught': sum(r['caught'] is True for r in data['mutants']), 'without_failed_new': [r['name'] for r in data['mutants'] if not r.get('failed_new')]}
    else:
        mutants = {k: v for k, v in data.items() if k != 'M00_identity'}
        mutation_counts[folder] = {'mutants': len(mutants), 'statuses': dict(collections.Counter(v[0] for v in mutants.values())), 'without_failed_checks': [k for k, v in mutants.items() if not v[2]], 'identity': data['M00_identity']}
dump('mutation_counts.json', mutation_counts)

oldmut = {r[0]: r[1:] for r in literal_assign(E / 'preattack14/probes/mutate.py', 'M')}
newmut = {r[0]: r[1:] for r in literal_assign(E / 'pa14_fix/tools/mutate_pa14.py', 'MUTS')}
survivor_names = ['M14_copiedfrom_type', 'M18_rr_det_only', 'M47_mm_elem_type', 'M54_lo_one']
oldres = json.loads(text(E / 'preattack14/out/mutation_PA13.json'))
oldres.update(json.loads(text(E / 'preattack14/out/mutation_PA13_extra.json')))
dump('preattack14_mutation_counts.json', {'total': len(oldres), 'killed': sum(v['killed'] is True for v in oldres.values()), 'survivors': {k: v for k, v in oldres.items() if not v['killed']}})
newres = json.loads(text(E / 'pa14_fix/logs/mutation_results.json'))
survivors = {k: {'same_mutation': oldmut[k] == newmut[k], 'before': oldres[k], 'after': newres[k]} for k in survivor_names}
dump('survivor_coverage.json', survivors)

req = text(CUR / 'docs/reviews/codex_rint2_rr_round3_request_20261108.md').splitlines()
rr302 = []
for i, ln in enumerate(req, 1):
    if re.search('교차 대조 없음|디스크 signal_after 받음|STOPS 소속 안 봄|PC12 고침으로', ln):
        rr302.append({'line': i, 'has_correction': '11-08 정정' in ln and 'RR3-02' in ln, 'text': ln})
dump('rr3_02_corrections.json', rr302)
print(json.dumps({'python': sys.version, 'diff_existing_test_changes': diffs['scripts/test_rint_r_chain.py']['changed_existing'], 'removed_test_functions': diffs['scripts/test_rint_r_chain.py']['removed'], 'rr3_02_lines': [[x['line'], x['has_correction']] for x in rr302], 'survivor_same_mutation': {k: v['same_mutation'] for k, v in survivors.items()}, 'raw_logs_examined': len(raw_logs)}, ensure_ascii=False, indent=2))
