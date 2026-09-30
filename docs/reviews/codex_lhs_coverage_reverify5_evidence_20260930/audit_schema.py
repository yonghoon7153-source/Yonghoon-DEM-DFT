"""Independent production-output mutations; no server, database, or DEM runs."""
import os, sys, json, copy, contextlib, io, subprocess
from pathlib import Path
E = Path(__file__).resolve().parent
C = E.parent/'candidate'
W = E.parent.parent
sys.path[:0] = [str(C/'scripts'), str(C/'webapp'), str(W/'lhs_coverage_review_20260930/deps')]
os.environ.update(SUPABASE_URL='', SUPABASE_KEY='', PYTHONDONTWRITEBYTECODE='1')
import pandas as pd
import coverage_physics_vs_hertzian as cv
import app
import pipeline_service as ps
F = E/'schema_fixtures'
F.mkdir(exist_ok=True)
def save(x, p):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2), encoding='utf-8')
def produce(name, variant='base', empty_am=False):
    d, tm, scale = cv._selftest_fixture(F/name, variant=variant)
    if empty_am:
        pd.DataFrame([(1,3,.001,0,0,0),(2,3,.001,0,0,.003)], columns=['id','type','radius','x','y','z']).to_csv(d/'atoms.csv',index=False)
        pd.DataFrame([],columns=['id1','id2','delta','contact_area']).to_csv(d/'contacts.csv',index=False)
    with contextlib.redirect_stdout(io.StringIO()):
        cv.compute_case(name, d, tm, scale=scale)
    return d, json.loads((d/'full_metrics.json').read_text(encoding='utf-8'))
R = {'positive_controls':{}, 'old_mutations':{}, 'additional_mutations':{}}
controls = {}
for name in ['base','denom_zero','nan_radius','isolated_zero','nan_delta','scale1','no_ligg_col','se_only']:
    d, fm = produce(name, variant='base' if name=='se_only' else name, empty_am=name=='se_only')
    controls[name] = fm
    R['positive_controls'][name] = dict(accepted=app._coverage_v2_written(str(d)), status=fm['coverage_status_physics_v2'], diag=fm['am_denominator_physics_v2'])
healthy = controls['base']
def probe(name, x, group='additional_mutations', stage=False):
    d = F/'mutations'/name
    save(x, d/'full_metrics.json')
    try:
        rec = dict(accepted=app._coverage_v2_written(str(d)))
    except Exception as ex:
        rec = dict(raised=type(ex).__name__, message=str(ex))
    rec['v2_record'] = {k:v for k,v in x.items() if k.endswith('_physics_v2')}
    if stage:
        prev = ps._RUNNER
        def writer(cmd, **kw):
            save(x,d/'full_metrics.json')
            return subprocess.CompletedProcess(cmd,0,'synthetic record mutation; producer execution substituted','')
        ps._RUNNER = writer
        try:
            result = app._coverage_stage([sys.executable,'coverage_physics_vs_hertzian.py',name],str(d),'coverage')
            rec['stage'] = result
            rec['pipeline_status'], rec['failed_stages'] = ps.summarize([result])
        except Exception as ex:
            rec['stage_exception'] = dict(type=type(ex).__name__, message=str(ex))
        finally:
            ps._RUNNER = prev
    R[group][name] = rec
old = ['missing_n_am_and_coverage','negative_n_am_and_no_coverage','nan_n_am_and_no_coverage',
       'ok_but_invalid_denom_count','area_nan','area_string','area_negative','coverage_negative',
       'ok_but_contact_failures','blank_with_positive_values']
for name in old:
    x=copy.deepcopy(healthy)
    if name.endswith('no_coverage') or name=='missing_n_am_and_coverage':
        for k in list(x):
            if k.startswith('coverage_AM') and k.endswith('_physics_v2'): del x[k]
    if name=='missing_n_am_and_coverage': del x['am_denominator_physics_v2']['n_am']
    elif name=='negative_n_am_and_no_coverage': x['am_denominator_physics_v2']['n_am']=-1
    elif name=='nan_n_am_and_no_coverage': x['am_denominator_physics_v2']['n_am']=float('nan')
    elif name=='ok_but_invalid_denom_count': x['am_denominator_physics_v2']['n_free_surface_nonpositive']=1
    elif name=='area_nan': x['area_AM전체_SE_total_physics_v2']=float('nan')
    elif name=='area_string': x['area_AM전체_SE_total_physics_v2']='broken'
    elif name=='area_negative': x['area_AM전체_SE_total_physics_v2']=-1.0
    elif name=='coverage_negative': x['coverage_AM_mean_physics_v2']=-1.0
    elif name=='ok_but_contact_failures': x['n_contact_failures_physics_v2']=1
    elif name=='blank_with_positive_values': x['coverage_status_physics_v2']='blank: undefined denominator'
    probe(name,x,'old_mutations',stage=name in ['missing_n_am_and_coverage','area_nan'])

for name in ['missing_fractions','none_fractions','wrong_fractions','empty_count_dicts','unknown_binding_keys',
             'contradictory_count_totals','n_am_zero_positive_area','zero_contacts_positive_area',
             'blank_bad_film','blank_none_rule','blank_missing_film','huge_integer_area']:
    x=copy.deepcopy(controls['se_only'] if name=='n_am_zero_positive_area' else healthy)
    if name=='missing_fractions':
        del x['cap_conflict_frac_physics_v2']; del x['cap_conflict_frac_cap_branch_physics_v2']
    elif name=='none_fractions':
        x['cap_conflict_frac_physics_v2']=None; x['cap_conflict_frac_cap_branch_physics_v2']=None
    elif name=='wrong_fractions':
        x['cap_conflict_n_physics_v2']=0; x['cap_conflict_frac_physics_v2']=1.0
    elif name=='empty_count_dicts':
        for k in app.COVERAGE_V2_COUNT_DICT_KEYS: x[k]={}
    elif name=='unknown_binding_keys': x['A_binding_counts_total_physics_v2']={'not_a_branch':x['n_contacts_physics_v2']}
    elif name=='contradictory_count_totals': x['A_binding_counts_total_physics_v2']['elastic']=10**6
    elif name=='n_am_zero_positive_area': x['area_AM전체_SE_total_physics_v2']=123.0
    elif name=='zero_contacts_positive_area':
        x['n_contacts_physics_v2']=x['n_cap_branch_physics_v2']=x['cap_conflict_n_physics_v2']=0
    elif name.startswith('blank_'):
        x=copy.deepcopy(controls['scale1'])
        if name=='blank_bad_film': x['h_film_sim_physics_v2']='broken'
        elif name=='blank_none_rule': x['rule_physics_v2']=None
        elif name=='blank_missing_film': del x['h_film_sim_physics_v2']
    elif name=='huge_integer_area': x['area_AM전체_SE_total_physics_v2']=10**400
    probe(name,x,stage=name in ['n_am_zero_positive_area','none_fractions','empty_count_dicts','huge_integer_area'])
assert all(x['accepted'] for x in R['positive_controls'].values())
assert not any(x.get('accepted') for x in R['old_mutations'].values())
save(R,E/'schema_results.json')
print(json.dumps({g:{k:{kk:vv for kk,vv in v.items() if kk not in ['v2_record','stage']} for k,v in d.items()} for g,d in R.items()},ensure_ascii=False,indent=2))
