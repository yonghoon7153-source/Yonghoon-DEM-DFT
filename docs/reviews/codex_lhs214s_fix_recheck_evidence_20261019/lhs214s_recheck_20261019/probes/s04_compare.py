"""Compare full-page and loader evidence produced by S04 probes."""
import difflib
import hashlib
import json
from pathlib import Path
import re

REVIEW = Path(__file__).resolve().parents[1]
E = REVIEW / 'evidence'
def read(name):
    return json.loads((E / name).read_text(encoding='utf-8'))

def tt(page):
    result = {}
    for label in ('σ_brug/σ_grain (Bruggeman)', 'σ_brug / σ_ionic', 'σ_Bruggeman (mS/cm)'):
        match = re.search(r"  '" + re.escape(label) + r"': \{.*?\n  \}", page, re.S)
        result[label] = re.findall(r"'(?:\\.|[^'\\])*'", match.group(0)) if match else None
    return result

old = read('s04_matrix_baseline.json')['cases']
new = read('s04_matrix_source.json')['cases']
summary = {'matrix': {}}
matrix = summary['matrix']
matrix['cases'] = len(new)
matrix['old_500'] = [k for k in old if old[k].get('http') == 500]
matrix['new_non200'] = [k for k in new if new[k].get('http') != 200]
matrix['loader_differences'] = [k for k in new if old[k].get('loader') != new[k].get('loader')]
matrix['effective_metrics_differences'] = [k for k in new if old[k].get('effective_metrics') != new[k].get('effective_metrics')]
matrix['surviving_route_cases'] = sum(old[k].get('http') == 200 for k in new)
matrix['surviving_route_differences'] = [k for k in new if old[k].get('http') == 200 and old[k].get('route') != new[k].get('route')]
matrix['inputs_unchanged_both'] = all(r.get('input_unchanged') for r in list(old.values()) + list(new.values()))
matrix['tooltip_string_differences'] = []
for name in new:
    if old[name].get('http') != 200:
        continue
    before = tt((E / 's04_matrix_baseline_work' / (name + '.html')).read_text(encoding='utf-8'))
    after = tt((E / 's04_matrix_source_work' / (name + '.html')).read_text(encoding='utf-8'))
    if before != after:
        matrix['tooltip_string_differences'].append(dict(case=name, before=before, after=after))
o = read('s04_types_baseline.json')['cases']
n = read('s04_types_source.json')['cases']
types = summary['types'] = {}
types['cases'] = len(n)
types['fixed_http'] = [k for k in n if o[k]['http'] != 200 and n[k]['http'] == 200]
types['regressed_http'] = [k for k in n if o[k]['http'] == 200 and n[k]['http'] != 200]
types['remaining_non200'] = [k for k in n if n[k]['http'] != 200]
numeric = [k for k in n if k == 'normal' or k.endswith(('_zero', '_integer', '_finite'))]
types['finite_numeric_controls'] = len(numeric)
types['finite_numeric_tooltip_differences'] = [k for k in numeric if tt((E / 's04_types_baseline_work' / (k + '.html')).read_text(encoding='utf-8')) != tt((E / 's04_types_source_work' / (k + '.html')).read_text(encoding='utf-8'))]
types['percolation_null_statuses'] = [o['percolation_pct_null']['http'], n['percolation_pct_null']['http']]
types['tau_null_matches_old_missing_tooltips'] = n['tortuosity_recommended_null']['tooltips'] == n['tortuosity_recommended_missing']['tooltips']
types['inputs_unchanged_both'] = all(r['inputs_unchanged'] for r in list(o.values()) + list(n.values()))
summary['source_equality'] = {}
baseline = REVIEW.parent / 'lhs214rr_recheck_20261019/source'
for rel in ('webapp/app.py', 'scripts/analyze_contacts.py', 'webapp/test_tau_labels.py'):
    a, b = (baseline / rel).read_bytes(), (REVIEW / 'source' / rel).read_bytes()
    summary['source_equality'][rel] = dict(equal=a == b, baseline_sha256=hashlib.sha256(a).hexdigest(), source_sha256=hashlib.sha256(b).hexdigest())
for rel in ('webapp/templates/single.html', 'scripts/check_all.sh'):
    a, b = (baseline / rel).read_text(encoding='utf-8'), (REVIEW / 'source' / rel).read_text(encoding='utf-8')
    (E / ('s04_diff_' + Path(rel).name + '.diff')).write_text(''.join(difflib.unified_diff(a.splitlines(True), b.splitlines(True), fromfile='77d8fd445/' + rel, tofile='685c2bbdb/' + rel)), encoding='utf-8')
(E / 's04_comparison.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(dict(matrix_cases=matrix['cases'], old_500=len(matrix['old_500']), new_non200=matrix['new_non200'], loader_differences=matrix['loader_differences'], surviving_route_cases=matrix['surviving_route_cases'], surviving_route_differences=matrix['surviving_route_differences'], tooltip_differences=[r['case'] for r in matrix['tooltip_string_differences']], types=types), ensure_ascii=False))
