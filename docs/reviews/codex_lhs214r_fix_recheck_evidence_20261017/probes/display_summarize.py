"""Summarize independent rerun contracts without calling production helpers."""
import json
from pathlib import Path

review = Path(__file__).resolve().parents[1]
s = json.loads((review/'evidence/display_source.json').read_text(encoding='utf-8'))
b = json.loads((review/'evidence/display_base.json').read_text(encoding='utf-8'))
fresh = json.loads((review/'evidence/display_fresh_source.json').read_text(encoding='utf-8'))
fb = json.loads((review/'evidence/display_fresh_base.json').read_text(encoding='utf-8'))

def ionrow(label):
    return (label.startswith('σ_ionic ') or label.startswith('Ionic conductivity') or
            label.startswith('R_brug ') or label.startswith('Contact-free / Full') or
            label.startswith('σ_brug / σ_ionic') or label.startswith('Plastic amplification'))

# Paper labels are read from the output, not guessed from implementation.
labels = [r[0] for r in s['cases']['normal_csv']['rendered_rows']]
print(json.dumps({'labels':labels},ensure_ascii=False))
mask_labels = [labels[i] for i in (0,1,2,5,6)]
assert all(any(word in label for word in ('σ_ionic', 'σ_full', 'σ_Bruggeman')) for label in mask_labels)
problems=[]
checked=0
for name,c in s['cases'].items():
    if name.startswith(('normal_', 'producer_ml_el_')): ok=(True,True)
    elif name.startswith(('physics_', 'producer_ml_physics_')): ok=(True,False)
    elif name.startswith('hertz_'): ok=(False,True)
    else: ok=(False,False)
    if name.startswith('producer_'):
        bed = name.removeprefix('producer_').rsplit('_',1)[0]
        mx = s['producer_runs'][bed]['metrics']
    else:
        mx = {'sigma_full_mScm':.6, 'sigma_full_mScm_physics':.9}
    for r in c['rendered_rows']:
        if len(r)<4 or r[0] not in mask_labels: continue
        checked+=1
        ratio=r[0].startswith('Plastic amplification')
        for idx,accepted in ((1,ok[0]),(2,ok[1])):
            if not (all(ok) if ratio else accepted) and not str(r[idx]).startswith('—'):
                problems.append([name,r[0],idx,r[idx]])
            if r[0]==labels[0] and accepted:
                value = mx['sigma_full_mScm' + ('_physics' if idx==2 else '')]
                if str(r[idx]) != str(round(value,4)): problems.append([name,r[0],idx,'not current',r[idx],value])
        if not all(ok) and str(r[3])!='—': problems.append([name,r[0],'delta',r[3]])

delta=[]
unchanged=[]
for name,c in s['cases'].items():
    (unchanged if c['rendered_rows']==b['cases'][name]['rendered_rows'] else delta).append(name)
def select_rows(case):
    return [r for r in case['rendered_rows'] if r and (r[0] in mask_labels or 'state' in r[0] or 'handover status' in r[0])]
selected={name:select_rows(s['cases'][name]) for name in ('producer_ml_physics_split','producer_ml_hertz_csv','producer_ml_el_fourcol','producer_nonthrough_csv')}
known=fresh['known']
k1=known['K1_grade_impact']
summary=dict(cases=len(s['cases']), errors=s['errors'], rendered_changed=len(delta), unchanged=unchanged,
    assertion_row_count=checked, mask_delta_problems=problems, selected=selected,
    producer_csv_preserved={k:v['preexisting_csv_preserved'] for k,v in s['producer_runs'].items()},
    fresh_cases=len(fresh['cases']), fresh_errors={n:v['error'] for n,v in fresh['cases'].items() if 'error' in v},
    fresh_failed_checks=[c for c in fresh['checks'] if not c['passed']],
    fresh_old_and_new_same_derived_rows={n:all(fresh['cases'][n]['rendered'].get(labels[i])==fb['cases'][n]['rendered'].get(labels[i]) for i in (1,5,6)) for n in fresh['cases'] if n.startswith('missing_both')},
    K1_grade_axes=[{k:a[k] for k in ('label','value','score','grade')} for a in k1['axes']],
    K2_stop_rejected=known['K2_stop_verdict'].get('value',[None])[0] is False,
    K2_exception_reason='⑦ τ 인계 도우미 실패 (OverflowError' in str(known['K2_stop_verdict']),
    K3_metadata=known['K3_ion_columns']['value']['ion_sigma0_mScm'],
    K3_status={m:known['K3_ion_columns']['value']['ion_net_status_'+m] for m in ('hertz','physics')},
    K3_sigma0_problem=known['K3_sigma0_problem'], K4=known['K4_stage_e_missing_keys'])
(review/'evidence/display_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ('selected','fresh_failed_checks')},ensure_ascii=False))
