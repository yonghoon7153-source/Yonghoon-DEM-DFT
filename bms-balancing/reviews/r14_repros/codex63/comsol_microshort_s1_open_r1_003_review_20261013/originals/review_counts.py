"""Reviewer-only reconciliation of stored JSON results, no candidate execution."""
from pathlib import Path
from collections import Counter
import json,hashlib
ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence'
def read(n): return json.loads((E/n).read_text(encoding='utf-8-sig'))
def digest(n): return hashlib.sha256((E/n).read_bytes()).hexdigest()
plan=read('EFFECTIVE_VALIDATION_PLAN.json')
combined=read('CASE_RESULT_MAP.json')
python=read('PYTHON_CASE_RESULTS.json')
java_lines=[json.loads(line) for line in (E/'Java_helper.stdout.txt').read_text(encoding='utf-8-sig').splitlines() if line.strip()]
java=[r for r in java_lines if 'id' in r]
java_footer=[r for r in java_lines if 'id' not in r]
assert len(java_footer)==1
assert len(plan['cases'])==len(combined['cases'])==len(python)==93
pi={r['id']:r for r in plan['cases']}; ci={r['id']:r for r in combined['cases']}; py={r['id']:r for r in python}; ja={r['id']:r for r in java}
assert len(pi)==len(ci)==len(py)==93 and len(ja)==6
assert pi.keys()==ci.keys()==py.keys()
assert {r['id'] for r in plan['cases'] if r['engine']=='Java_helper'}==ja.keys()
for key,p in pi.items():
    c=ci[key]
    assert c['engine']==p['engine'] and c['group']==p['group'],key
    assert c['expected']==p['expected_assertion'],key
    assert c['target']==p['target_function'],key
    assert c['required_reach']==p['required_reach'] and c['forbidden_reach']==p['forbidden_reach'],key
    assert c['planned_counts']==p['call_counts'],key
    source=py[key] if p['engine']=='Python' else ja[key]
    assert c['actual']==source and c['status']==source['status']=='PASS',key
    if p['engine']=='Java_helper': assert py[key]['status']=='NOT_RUN',key
for stage in ['Python','Java_compile','Java_helper']:
    rec=read(stage+'.RETURN.json')
    assert rec['child_rc']==0 and rec['timeout']==False
    for io in ['stdout','stderr']:
        name=stage+'.'+io+'.txt'
        assert digest(name)==rec[io]['sha256'] and (E/name).stat().st_size==rec[io]['bytes']
refs=read('REFERENCE_INDEX.json')
for r in refs:
    assert digest(r['entry'])==r['sha256'] and (E/r['entry']).stat().st_size==r['bytes']
result={'kind':'REVIEWER_CASE_AND_RETURN_RECONCILIATION','plan_sha256':digest('EFFECTIVE_VALIDATION_PLAN.json'),
 'map_sha256':digest('CASE_RESULT_MAP.json'),'group_counts':dict(Counter(r['group'] for r in plan['cases'])),
 'expected_engine_counts':dict(Counter(r['engine'] for r in plan['cases'])),
 'python_stage_status_counts':dict(Counter(r['status'] for r in python)),
 'java_status_counts':dict(Counter(r['status'] for r in java)),
 'combined_status_counts':dict(Counter(r['status'] for r in combined['cases'])),
 'ids_exact_set':True,'expected_reach_counts_equal_to_plan':True,
 'combined_actuals_equal_original_engine_results':True,'three_return_stream_hashes_equal':True,
 'reference_copies_hashes_matched':len(refs),
 'scope':'Data comparisons only; does not execute cases or prove installed COMSOL/API/OS behavior.'}
(ROOT/'notes').mkdir(exist_ok=True)
with (ROOT/'notes/CASE_RECONCILIATION.json').open('x',encoding='utf-8') as f: json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))
