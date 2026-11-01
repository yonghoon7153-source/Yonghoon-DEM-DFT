from pathlib import Path
import sys, json, csv, math, hashlib, shutil, tempfile, copy
import numpy as np

BASE=Path(__file__).resolve().parents[1]
SRC=BASE/'source/repo/docs/50kg/report_y4/draft2'
OUT=BASE/'figures_review'
sys.path.insert(0,str(SRC))
import run_draft2_metrics as R
def read(p):
    with open(p,encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
recs={b:json.loads((SRC/f'data/{b}/metrics_{b}.json').read_text(encoding='utf8')) for b in ['D1','D2','D3']}
checks=[]
def check(name,a,b,tol=6e-9):
    if isinstance(a,(int,float)) and isinstance(b,(int,float)):
        ok=math.isclose(a,b,rel_tol=tol,abs_tol=tol)
    else:ok=a==b
    checks.append(dict(name=name,ok=ok,actual=a,expected=b))
def number(v):return float(v) if v not in ('',None) else None
meta=json.loads((SRC/'figs/figs_meta.json').read_text(encoding='utf8'))
for b,h in meta['metrics_sha256'].items():check('metrics sha '+b,hashlib.sha256((SRC/f'data/{b}/metrics_{b}.json').read_bytes()).hexdigest(),h)
for stem,m in meta['figures'].items():
    for f,h in m['files'].items():check('figure sha '+f,hashlib.sha256((SRC/'figs'/f).read_bytes()).hexdigest(),h)
    check('figure rows '+stem,len(read(SRC/'figs'/f'{stem}.csv')),m['csv_rows'])
for row in read(SRC/'metrics_all.csv'):
    b=row['bed']
    if b not in recs:continue
    rec=recs[b]
    for k,v in row.items():
        if k in rec['metrics']:check('metrics_all '+b+' '+k,number(v),rec['metrics'][k])
    check('metrics_all '+b+' step',int(row['end_step']),rec['frame']['end_step'])
    check('metrics_all '+b+' archive',row['tgz_sha256'],rec['provenance']['end_set']['tgz_sha256'])

for r in read(SRC/'figs/p1_bed_strip.csv'):
    b=r['bed']
    if b not in recs:continue
    rec=recs[b];sec=read(SRC/f'data/{b}/section_{b}.csv')
    for field,expected in [('end_step',rec['frame']['end_step']),('plate_z_um',rec['metrics']['plate_z_um']),('n_am_end',rec['inventory']['n_am']),('n_se_end',rec['inventory']['n_se']),('section_y_um',rec['section']['y0_um']),('n_am_in_section',len({x['particle_id'] for x in sec if x['phase']=='AM'})),('n_se_in_section',len({x['particle_id'] for x in sec if x['phase']=='SE'}))]:check('p1 '+b+' '+field,float(r[field]),expected)

p2=read(SRC/'figs/p2_compaction.csv');relaxfig=read(SRC/'figs/p2_relaxation.csv')
for b,rec in recs.items():
    curve=read(SRC/f'data/{b}/curve_{b}.csv');orig=[r for r in curve if r['branch']=='loading' and float(r['plate_pressure_MPa'])>1.0];drawn=[r for r in p2 if r['bed']==b and r['panel']=='a_loading']
    check('p2 loading rows '+b,len(drawn),len(orig))
    for i,(a,z) in enumerate(zip(drawn,orig)):
        for k in ['plate_pressure_MPa','eps_sphere_pct']:check('p2 '+b+' '+str(i)+' '+k,float(a[k]),float(z[k]))
    end=next(r for r in p2 if r['bed']==b and r['panel']=='b_end')
    for k in ['eps_sphere_pct','eps_union_exact_pct']:check('p2 end '+b+' '+k,float(end[k]),rec['metrics'][k])
    check('p2 end '+b+' pressure',float(end['plate_pressure_MPa']),rec['metrics']['p_end_MPa'])
    ro=[r for r in curve if r['branch']=='fixed_height_relaxation'];rd=[r for r in relaxfig if r['bed']==b and r['point']=='relaxation']
    check('p2 relax rows '+b,len(rd),len(ro))
    for i,(a,z) in enumerate(zip(rd,ro)):
        check('relax '+b+' '+str(i)+' pressure',float(a['plate_pressure_MPa']),float(z['plate_pressure_MPa']))
        check('relax '+b+' '+str(i)+' step',float(a['steps_after_stop_k']),(int(z['step'])-rec['compaction']['stop_step'])/1000)
    t0=next(r for r in relaxfig if r['bed']==b and r['point']=='t0minus_last_compression_output')
    check('relax '+b+' t0',float(t0['plate_pressure_MPa']),rec['metrics']['p_t0minus_MPa'])
maps={
'p3_contacts':{'a_am_se_cn':('am_se_cn_mean',None),'b_se_se_cn':('se_se_cn_mean',None),'c_am_coverage':('coverage_hertz_pct','coverage_physics_union_pct')},
'p4_tortuosity':{'a_geometric':('tau_geo_all',None),'b_transport':('tau2_ion_hertz','tau2_ion_physics')},
'p4_f_connect':{'a_f_ion':('f_ion_hertz','f_ion_physics'),'b_se_connected_am':('se_connected_am_pct',None)}}
for stem,mp in maps.items():
    for r in read(SRC/f'figs/{stem}.csv'):
        if r['bed'] not in recs:continue
        if r['panel'] not in mp:
            checks.append(dict(name='unmapped '+stem+' '+r['panel'],ok=False));continue
        k,ph=mp[r['panel']];m=recs[r['bed']]['metrics']
        check(stem+' '+r['bed']+' '+k,number(r['value']),m[k])
        if ph:check(stem+' '+r['bed']+' '+ph,number(r['physics']),m[ph])
for stem,keycol in [('p7_summary_heat','metric'),('p7_lit_direction','quantity')]:
    for r in read(SRC/f'figs/{stem}.csv'):
        if r['bed'] not in recs:continue
        k=r[keycol];check(stem+' '+r['bed']+' '+k,number(r['value']),recs[r['bed']]['metrics'][k])
        if 'ratio_to_D3' in r:check(stem+' ratio '+r['bed']+' '+k,number(r['ratio_to_D3']),recs[r['bed']]['metrics'][k]/recs['D3']['metrics'][k])
for r in read(SRC/'figs/p3_per_am.csv'):
    if r['bed'] not in recs:continue
    p=read(SRC/f"data/{r['bed']}/per_am_{r['bed']}.csv")
    k='area_am_se_um2' if r['panel'].startswith('a_') else ('coverage_physics_union_pct' if 'Physics' in r['quantity'] else 'coverage_hertz_pct')
    xs=np.array([float(v[k]) for v in p if v[k]!=''])
    for col,q in [('p5',5),('p25',25),('median',50),('p75',75),('p95',95)]:check('box '+r['bed']+' '+k+' '+col,float(r[col]),float(np.percentile(xs,q)))
    check('box '+r['bed']+' '+k+' mean',float(r['mean']),float(np.mean(xs)))
    check('box '+r['bed']+' '+k+' n',int(r['n']),len(xs))
for r in read(SRC/'figs/p3_overlap_threshold.csv'):
    if r['bed'] not in recs:continue
    k='am_frac_overlap_'+('card_' if r['panel']=='(b)' else '')+'gt_'+str(int(float(r['threshold_pct'])))+'_pct'
    check('overlap '+r['bed']+' '+k,float(r['am_frac_pct']),recs[r['bed']]['metrics'][k])
for stem,mp in [('p6_z_structure',{'a_local_porosity_union':('por_union_pct',None,None),'b_se_connected_am':('am_connected_pct',None,None)}),('p6_z_stress',{'a_lw_am':('lw_am_median_MPa','lw_am_q25_MPa','lw_am_q75_MPa'),'b_lw_se':('lw_se_median_MPa','lw_se_q25_MPa','lw_se_q75_MPa')})]:
    srcrows={b:read(SRC/f'data/{b}/zprof_{b}.csv') for b in recs}
    for r in read(SRC/f'figs/{stem}.csv'):
        orig=min(srcrows[r['bed']],key=lambda z:abs(float(z['z_mid_um'])-float(r['z_mid_um'])))
        for field in ['z_lo_um','z_hi_um','z_mid_um']:check(stem+' '+r['bed']+' '+field,float(r[field]),float(orig[field]))
        for field,k in zip(['value','band_lo','band_hi'],mp[r['panel']]):
            if k:check(stem+' '+r['bed']+' '+k,float(r[field]),float(orig[k]))
for r in read(SRC/'figs/diag_relax_drop_vs_N.csv'):
    if r['bed'] not in recs:continue
    m=recs[r['bed']]['metrics'];n=int(r['n_particles'])
    check('diag '+r['bed']+' dp',float(r['dp_MPa']),m['p_t0minus_MPa']-m['p_end_MPa'])
    check('diag '+r['bed']+' drag',float(r['dp_est_MPa']),n*0.001)
    check('diag '+r['bed']+' ratio',float(r['dp_over_est']),(m['p_t0minus_MPa']-m['p_end_MPa'])/(n*0.001))

transport={}
for b,rec in recs.items():
    m=rec['metrics'];row=rec['tau_flux_row'];L=m['plate_z_um'];Lm=m['thickness_mass_conserving_um'];phi=m['phi_se_mass_conserving']
    transport[b]=dict(L_gap=L,L_mc=Lm,L_gap_over_L_mc=L/Lm,phi_mc=phi,phi_sphere=phi*Lm/L,phi_am_mc=m['phi_am_mass_conserving'],one_minus_phi_sum=1-phi-m['phi_am_mass_conserving'],eps_union=m['eps_union_exact_pct']/100)
    for mode in ['hertz','physics']:
        f=m['f_ion_'+mode];gap=row['f_ion_'+mode+'_gap'];tau=m['tau2_ion_'+mode]
        transport[b][mode]=dict(f=f,f_gap=gap,tau=tau,calc_f=gap*L/Lm,calc_tau_mc=phi/f,calc_tau_sphere=phi*Lm/L/gap)
        check('transport '+b+' '+mode+' f_mc',f,gap*L/Lm)
        check('transport '+b+' '+mode+' tau',tau,phi*Lm/L/gap)
transport['D1_D3_ratios']={mode:dict(f_mc=recs['D1']['metrics']['f_ion_'+mode]/recs['D3']['metrics']['f_ion_'+mode],f_gap=recs['D1']['tau_flux_row']['f_ion_'+mode+'_gap']/recs['D3']['tau_flux_row']['f_ion_'+mode+'_gap']) for mode in ['hertz','physics']}

# Synthetic consumer probes: no solver, no source write. Every variant retains correct schema and bed.
probes=[]
variants={
'same_step_false':lambda r:r['frame']['same_step_set'].update(contact=r['frame']['end_step']-1,ok=False),
'network_not_computed':lambda r:r['metrics'].update(ion_net_status_hertz='NOT_COMPUTED'),
'wrong_case':lambda r:r.update(case='kg50_d3_b50_s1',d50_se_um=3.0),
'failed_aggregate_check':lambda r:r['aggregate_checks'].update(synthetic_check=False),
'metric_only_changed':lambda r:r['metrics'].update(f_ion_hertz=0.123),
}
tempfile.tempdir=str(OUT)
# ZIP omits two dependencies; parent fetched the same pinned commit into remote/.
# Resolve only absent paths there; never edit the source snapshot.
orig_rp=R.src.rp
R.src.rp=lambda rel:orig_rp(rel) if orig_rp(rel).is_file() else BASE/'remote'/rel
with tempfile.TemporaryDirectory(prefix='consumer_') as t:
    scratch=Path(t);(scratch/'D1').mkdir();R.DATA=scratch;R.HERE=scratch
    for label,fn in variants.items():
        obj=copy.deepcopy(recs['D1']);fn(obj);(scratch/'D1/metrics_D1.json').write_text(json.dumps(obj),encoding='utf8')
        try:
            loaded=R.load_beds();rows=R.merge();d1=next(r for r in rows if r['bed']=='D1')
            probes.append(dict(variant=label,accepted=True,status=d1['status'],f=d1['f_ion_hertz'],declared_case=loaded['D1']['case'],merged_case=d1['case']))
        except Exception as e:probes.append(dict(variant=label,accepted=False,error=repr(e)))
out=dict(check_count=len(checks),failed=[c for c in checks if not c['ok']],checks=checks,transport=transport,consumer_probes=probes)
(OUT/'figure_numeric_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:out[k] for k in ['check_count','failed','transport','consumer_probes']},ensure_ascii=False,indent=2))
