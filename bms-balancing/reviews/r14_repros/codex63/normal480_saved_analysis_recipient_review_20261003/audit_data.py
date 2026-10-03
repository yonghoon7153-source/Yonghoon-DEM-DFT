"""Reviewer-owned read-only audit; never imports supplied scripts."""
from pathlib import Path
from decimal import Decimal as D, getcontext
import csv, json, hashlib
getcontext().prec=50
ROOT=Path(__file__).resolve().parent
R=ROOT/'received'
PRIOR=ROOT.parent/'normal480_native_review_20261001'
N=PRIOR/'received'
T=N/'run/tables'
checks=[]
def check(n,v):
    checks.append({'check':n,'pass':bool(v)})
    assert v,n
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        rd=csv.DictReader(f)
        assert rd.fieldnames and len(rd.fieldnames)==len(set(rd.fieldnames))
        for r in rd:
            assert None not in r and None not in r.values()
            yield r
def decrows(p):
    for row in read(p):
        r={k:D(v) for k,v in row.items()}
        assert all(v.is_finite() for v in r.values())
        yield r
def timed(p):
    rr=list(decrows(p)); ts=[r['time_s'] for r in rr]
    assert ts==sorted(set(ts))
    return {r['time_s']:r for r in rr}
def equal(a,b): return abs(a-b)<=D('1e-40')
binding=json.loads((R/'INPUT_BINDING.json').read_bytes())
native=Path('C:/Users/Administrator/Downloads/COMSOL63_NORMAL480_NATIVE_RESULT_20261001.zip')
check('Native ZIP independently matches analysis input binding',native.stat().st_size==binding['native_zip']['bytes'] and sha(native)==binding['native_zip']['sha256'])
for e in binding['used_payload_entries']:
    p=N/e['file']
    check('Used raw/source size and SHA '+e['file'],p.stat().st_size==e['bytes'] and sha(p)==e['sha256'])
small=['preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv','electrolyte_guard.csv','preflight_MinLine_ce.csv','preflight_MaxLine_ce.csv']
gl,bn,bp,gd,mn,mx=[timed(T/f) for f in small]
data=timed(R/'TIME_SERIES.csv');ts=list(data)
check('All 5740 times identical, ordered unique, 0 to 480',len(ts)==5740 and ts[0]==0 and ts[-1]==480 and all(list(a)==ts for a in [gl,bn,bp,gd,mn,mx]))
li_keys=['Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2']
li0=sum(gl[D(0)][k] for k in li_keys)
terms={'Eeq':'Eeq_V','etaMid':'etamid_V','phiL':'phil_V'}
expected={}
field_count=0
for t in ts:
    r={**gl[t],**gd[t]}
    r['voltage_V']=bp[t]['phis_V']-bn[t]['phis_V']
    v0=bp[D(0)]['phis_V']-bn[D(0)]['phis_V']
    r['voltage_change_from0_mV']=(r['voltage_V']-v0)*1000
    for term,k in terms.items():
        for e,src,sgn in [('N',bn,-1),('P',bp,1)]:
            r[f'{term}_{e}_V']=src[t][k]
            r[f'{term}_{e}_contribution_from0_mV']=sgn*(src[t][k]-src[D(0)][k])*1000
        r[f'{term}_PminusN_V']=bp[t][k]-bn[t][k]
        r[f'{term}_net_change_from0_mV']=((bp[t][k]-bn[t][k])-(bp[D(0)][k]-bn[D(0)][k]))*1000
    r['voltage_identity_residual_V']=r['voltage_V']-sum(r[f'{k}_PminusN_V'] for k in terms)
    r['change_identity_residual_V']=(r['voltage_change_from0_mV']-sum(r[f'{k}_net_change_from0_mV'] for k in terms))/1000
    r['ce_max_all_MaxLine_mol_m3']=mx[t]['ce_mol_m3'];r['ce_min_all_MinLine_mol_m3']=mn[t]['ce_mol_m3']
    r['ce_global_spread_mol_m3']=mx[t]['ce_mol_m3']-gd[t]['ce_min_all_mol_m3']
    r['Li_total_mol_m2']=sum(gl[t][k] for k in li_keys)
    r['Li_relative_change']=(r['Li_total_mol_m2']-li0)/li0
    for k in li_keys: r[k.replace('_mol_m2','_change_mol_m2')]=gl[t][k]-gl[D(0)][k]
    r['reaction_sum_A_m2']=gl[t]['reaction_N_A_m2']+gl[t]['reaction_P_A_m2']
    r.update(N_OCP_lower_margin=gl[t]['xsurf_N_min'],N_OCP_upper_margin=D('.98')-gl[t]['xsurf_N_max'],P_OCP_lower_margin=gl[t]['xsurf_P_min']-D('.2228930343076256'),P_OCP_upper_margin=D('.983245033354389')-gl[t]['xsurf_P_max'])
    assert set(r)==set(data[t]),(t,set(r)^set(data[t]))
    for k,v in r.items():
        assert equal(v,data[t][k]),(t,k,v,data[t][k])
        field_count+=1
    assert all(r[k]==0 for k in ['ocp_guard','surface_guard','electrolyte_guard','threshold_mol_m3'])
    assert all(src[t]['Eeq_V']==src[t]['direct_Eeq_surface_V'] for src in [bn,bp])
    expected[t]=r
check('Every time-series field traced or recalculated from raw inputs',True)
keytimes=list(map(D,['0','5','30','60','120','240','360','480']))
key=timed(R/'KEY_TIMES.csv')
check('KEY_TIMES exactly 8 original stored rows',list(key)==keytimes and all(key[t]==data[t] for t in keytimes))
intervals=list(decrows(R/'INTERVAL_VOLTAGE.csv'))
check('Seven declared intervals including overlapping total/recent windows',[(r['start_s'],r['end_s']) for r in intervals]==[(D(a),D(b)) for a,b in [(0,5),(5,30),(30,120),(120,240),(240,480),(0,480),(360,480)]])
for r in intervals:
    a,b=r['start_s'],r['end_s']; dur=b-a
    q={'start_s':a,'end_s':b,'duration_s':dur,'voltage_change_mV':(expected[b]['voltage_V']-expected[a]['voltage_V'])*1000}
    for k in terms:q[k+'_change_mV']=(expected[b][k+'_PminusN_V']-expected[a][k+'_PminusN_V'])*1000
    q['residual_V']=(q['voltage_change_mV']-sum(q[k+'_change_mV'] for k in terms))/1000
    q['voltage_secant_mV_per_s']=q['voltage_change_mV']/dur
    assert all(equal(v,r[k]) for k,v in q.items())
check('Interval signed contribution, residual and secant arithmetic',True)
ec=list(read(R/'ELECTRODE_CONTRIBUTIONS.csv'))
assert len(ec)==42
seen=set()
for r in ec:
    a,b=D(r['start_s']),D(r['end_s']); term,e=r['term'],r['electrode'];src=bn if e=='N' else bp;sign=-1 if e=='N' else 1;k=terms[term]
    token=(a,b,term,e);assert token not in seen;seen.add(token)
    q={'boundary_id':1 if e=='N' else 4,'start_V':src[a][k],'end_V':src[b][k],'temporal_change_mV':(src[b][k]-src[a][k])*1000,'voltage_sign':sign,'signed_contribution_mV':sign*(src[b][k]-src[a][k])*1000}
    assert all(equal(D(r[k]),D(v)) for k,v in q.items())
check('42 electrode contributions use P positive N negative',True)
rates=list(read(R/'SECANT_RATES.csv'))
assert len(rates)==7*16
for r in rates:
    a,b=D(r['start_s']),D(r['end_s']);k=r['metric'];aa,bb=expected[a][k],expected[b][k]
    assert all(equal(D(r[k]),v) for k,v in {'start_value':aa,'end_value':bb,'change':bb-aa,'secant_change_per_s':(bb-aa)/(b-a)}.items())
check('112 secants use exact endpoint times, not sample counts',True)
profiles=list(read(R/'SELECTED_PROFILES.csv'))
assert len(profiles)==3856
selected={}
for r in profiles:
    key=(r['electrode'],D(r['time_s']),D(r['coordinate_m']))
    assert key not in selected
    selected[key]={k:D(v) for k,v in r.items() if k!='electrode'}
    assert all(v.is_finite() for v in selected[key].values())
profile_source_counts={};checked=0
for e in ['N','P']:
    count=0
    for raw in read(T/f'axes_profile_{e}.csv'):
        count+=1;t=D(raw['time_s'])
        if t not in keytimes:continue
        q={k:D(v) for k,v in raw.items()}
        q['coordinate_um']=q['coordinate_m']*1000000
        q['surface_minus_particle_average']=q['x_surface']-q['x_particle_average']
        assert q==selected[(e,t,q['coordinate_m'])]
        checked+=1
    profile_source_counts[e]=count
    for t in keytimes:
        sl=[v for (ee,tt,x),v in selected.items() if ee==e and tt==t]
        xx=[r['coordinate_m'] for r in sl]
        assert len(xx)==241 and xx==sorted(set(xx)) and all(r['domain_id']==(1 if e=='N' else 3) for r in sl)
        assert abs(xx[0]-D('0' if e=='N' else '.000077'))<D('1e-16')
        assert abs(xx[-1]-D('.000052' if e=='N' else '.000121'))<D('1e-16')
check('3856 selected profile rows and same-coordinate gaps equal native CSV',checked==3856 and all(n==5740*241 for n in profile_source_counts.values()))
for r in read(R/'LOCAL_SURFACE_AVERAGE_GAPS.csv'):
    vals=[v['surface_minus_particle_average'] for (e,t,x),v in selected.items() if e==r['electrode'] and t==D(r['time_s'])]
    assert min(vals)==D(r['surface_minus_particle_average_min']) and max(vals)==D(r['surface_minus_particle_average_max'])
check('Local gap extrema from paired coordinates',True)
summary=json.loads((R/'SUMMARY.json').read_bytes())
for label,t in [('initial',D(0)),('final',D(480)),('recent120_start',D(360))]:
    assert set(summary[label])==set(expected[t])
    assert all(equal(D(v),expected[t][k]) for k,v in summary[label].items())
for sk,col in [('maximum_level_identity_residual_V','voltage_identity_residual_V'),('maximum_change_identity_residual_V','change_identity_residual_V'),('maximum_Li_relative_change','Li_relative_change')]:
    assert equal(D(summary[sk]),max(abs(r[col]) for r in expected.values()))
check('Summary key rows and maximum diagnostics',True)
before=json.loads((R/'SOURCE_PRESERVATION_BEFORE.json').read_bytes());after=json.loads((R/'SOURCE_PRESERVATION_AFTER.json').read_bytes())
check('Submitted preservation before/after identical',before==after)
result={'status':'PASS','scope':'Independent Decimal50 recalculation and raw-file comparison; not supplied analyzer execution or simulation','checks':checks,'time_series_fields_compared':field_count,'profile_source_rows_scanned':profile_source_counts,'profile_rows_compared':checked,'source_preservation_reported_count':len(before),'intervals':intervals,'maximum_level_identity_residual_V':max(abs(r['voltage_identity_residual_V']) for r in expected.values()),'maximum_change_identity_residual_V':max(abs(r['change_identity_residual_V']) for r in expected.values()),'maximum_Li_relative_drift':max(abs(r['Li_relative_change']) for r in expected.values()),'final':expected[D(480)],'no_new_native_execution':True,'received_code_executions':0}
(ROOT/'NUMERIC_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps({k:result[k] for k in ['status','time_series_fields_compared','profile_rows_compared','source_preservation_reported_count','intervals','maximum_level_identity_residual_V','maximum_change_identity_residual_V','maximum_Li_relative_drift']},default=str))
