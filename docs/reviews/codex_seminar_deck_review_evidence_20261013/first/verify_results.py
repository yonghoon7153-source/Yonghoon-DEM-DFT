"""Independent read-only arithmetic on saved sources. No solver/campaign run."""
from pathlib import Path
import csv, json, math, statistics
R=Path(__file__).resolve().parent
S=R/'sources/code'
pa=S/'docs/data/phase_a_rep100_20260930/pa100'
arms=[json.loads(f.read_text()) for f in pa.glob('*/arms/arm_*.json')]
pri={(x['vgcf_wt'],x['vox'],x['origin']):x for x in arms if x['role']=='primary'}
qc=[x for x in arms if x['role']=='qc_replay']
comp=[]
for v in [.15,.2,.25]:
    for o in range(8):
        for w in [1,2,3]:
            d=math.log(pri[w+1,v,o]['sigma_e']/pri[w,v,o]['sigma_e'])
            comp.append((d,v,o,w,w+1))
replay=[abs(math.log(x['sigma_e']/pri[x['vgcf_wt'],x['vox'],x['origin']]['sigma_e'])) for x in qc]
print('PHASE_A',json.dumps({'primary':len(pri),'qc':len(qc),'comparisons':len(comp),'violate_0p04pct':sum(d<=math.log1p(.0004) for d,*_ in comp),'min_increment_pct':math.expm1(min(comp)[0])*100,'worst_key':min(comp)[1:],'max_replay_pct':math.expm1(max(replay))*100,'all_cg0':all(x['cg_info']==0 and not x['unconverged'] for x in arms),'code_sha':sorted({x['code_sha'] for x in arms})}))
planes=json.loads((S/'docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json').read_text())['cases']
for name,c in planes.items():
    cuts=c['cuts']; den=sum(x['load_mpa'] for x in cuts)
    shares={g:sum(x['load_mpa']*x['share_group_pct'][g] for x in cuts)/den for g in ['AM–AM','AM–SE','SE–SE']}
    print('PLANE',name,json.dumps({'n':len(cuts),'share':shares,'pressure_mean':den/len(cuts)}))
# Coarse CL-24 ladder: solve the three-point power-law fit, strictly diagnostic.
h=[.4,.3,.25]; y=[1.4215,1.1621,1.0849]
q=(y[0]-y[1])/(y[1]-y[2]); lo,hi=.0001,20
for _ in range(100):
    p=(lo+hi)/2; ratio=(h[0]**p-h[1]**p)/(h[1]**p-h[2]**p)
    if ratio<q:lo=p
    else:hi=p
p=(lo+hi)/2; C=(y[0]-y[1])/(h[0]**p-h[1]**p); const=y[0]-C*h[0]**p
print('CL24_DIAGNOSTIC_FIT',json.dumps({'p':p,'increment_ratio':q,'max_residual':max(abs(a-(const+C*b**p)) for a,b in zip(y,h)),'continuum_value_intentionally_not_reported':True}))
cohorts=[]
for name in ['lhs','lhsx']:
    with (S/f'docs/data/lhs_release_20261006_v12/{name}_release_20261006_v12.csv').open() as f: rows=list(csv.DictReader(f))
    cohorts.append(rows)
    tau=[float(x['tortuosity_SE_wall']) for x in rows if x['tortuosity_SE_wall']]
    print('LHS',name,json.dumps({'n':len(rows),'percolating':sum(float(x['percolation_pct'])>0 for x in rows),'geom_tau_n':len(tau),'tau_min':min(tau),'tau_max':max(tau),'physical_HOLD':sum(x['physical_target_status']=='HOLD' for x in rows),'loading_values':sorted({x.get('loading_mAh_cm2','absent') for x in rows}),'e_se_values':sorted({x.get('e_se_gpa','absent') for x in rows}),'pressure_values':sorted({x.get('pressure_MPa','absent') for x in rows})}))
# Recompute between-cohort fraction of porosity variance from CSV values.
ys=[[float(x['porosity_union_exact_pct']) for x in rows] for rows in cohorts]
all_y=sum(ys,[]); mu=statistics.mean(all_y)
between=sum(len(y)*(statistics.mean(y)-mu)**2 for y in ys)
total=sum((x-mu)**2 for x in all_y)
print('LHS_BETWEEN_COHORT_VARIANCE',between/total)
print('DCP_RATIOS',54/4.47,70.6/12.4)
