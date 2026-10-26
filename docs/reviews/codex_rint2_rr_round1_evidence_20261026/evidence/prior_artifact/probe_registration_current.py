"""Independent registration audit, pinned code imported read-only.

Passive responses A+B/(R+C) are analytic parallel-plus-series resistor
networks. Synthetic fixtures below are decision-logic probes, not bed runs.
"""
from __future__ import annotations
import json
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(os.environ.get('RINT_REVIEW_SOURCE', str(ROOT / 'source'))).resolve()
sys.path.insert(0, str(SOURCE / 'scripts'))
import rint_r_chain as rr

def arm(s, err=0.0):
    return {'sigma': float(s), 'err_rel': float(err),
            'state': 'zero' if s == 0 else 'positive', 'n_sdcp_near': 0}

def origin_ids(arms):
    return range(arms) if isinstance(arms, int) else arms

def ladder(func, scale, err=0.0, cap=80):
    def fetch(role, key, arms):
        r = rr.rj_float(key)/scale
        return [arm(func(r, i)*1e-3, err) for i in origin_ids(arms)]
    obj = rr.Ladder(fetch, max_points=cap)
    obj.run()
    obj.origin()
    return obj

def predict(func, limits=(0.5,1.0,2.0)):
    keys = dict(zip(rr.RJ_ROLES, map(rr.rj_key, limits)))
    lads = {law: dict(keys, r0_sigma=1.63e-3) for law in rr.LAWS}
    def fetch(kit, role, law, c, key, arms, sv_cf=False):
        return [arm(1.63e-3 if kit == rr.SBE_KIT else
                    func(rr.rj_float(key), i, law, c)*1e-3)
                for i in origin_ids(arms)]
    obj = rr.Predict(fetch, lads, None)
    obj.run()
    return obj

def label(values):
    return rr.judge({k:v*1e3 for k,v in values.items()})

def rca01():
    scale=10**4.75
    f=lambda r,i: 1.597+0.0363/(r+0.1)
    exact=[(0.0363/(1.63*t-1.597)-0.1)*scale for t in (1.02,0.98)]
    out=[]
    for err in (0.0,1e-4):
        l=ladder(f,scale,err)
        ends=[rr.rj_float(l.st[k]) for k in ('R_j_lo','R_j_hi')]
        assert ends[0] <= exact[0] and ends[1] >= exact[1]
        vals={('0','P0','R_j_lo'): (3+1/(ends[0]/scale+.1))*1e-3,
              ('1','P0','R_j_hi'): (3+1/(ends[1]/scale+.1))*1e-3}
        j=label(vals)
        assert j['verdict']=='CONSISTENT_WEAK'
        out.append({'err':err,'end_R':ends,'true_R':exact,
                    'R_ratio':l.st['R_ratio'],'points':l.st['n_runs'],
                    'R0':l.st['R_j0'],'verdict':j['verdict'],'W':j['W']})
    return out

def endpoint_sweep():
    checked=stopped=0
    for a in (0.0,0.5,1.2,1.55,1.59):
        for c in (.001,.1,1.,10.):
            for scale in (1e2,1e5,1e8):
                b=(1.63-a)*(1+c)
                if a+b/c < 1.63*1.02:
                    continue
                lo=b/(1.63*1.02-a)-c
                hi=b/(1.63*.98-a)-c
                def f(r,i): return a+b/(r+c)
                try: l=ladder(f,scale,1e-4)
                except rr.Stop:
                    stopped+=1
                    continue
                gotlo=rr.rj_float(l.st['R_j_lo'])/scale
                gothi=rr.rj_float(l.st['R_j_hi'])/scale
                assert gotlo<=lo and gothi>=hi,(a,b,c,gotlo,gothi,lo,hi)
                checked+=1
    return {'checked_passive_responses':checked,'fail_closed':stopped}

def guard_padding():
    # A valid (conservative) certificate can force many extensions beyond
    # the true inverse. x100 bounds the next ladder step, not total padding.
    e=1e-4
    a=(1.63*.98)/(1+e)-1e-12
    c=.1
    b=(1.63-a)*(1+c)
    l=ladder(lambda r,i:a+b/(r+c),1e5,e)
    true_hi=(b/(1.63*.98-a)-c)*1e5
    got_hi=rr.rj_float(l.st['R_j_hi'])
    assert got_hi/true_hi>100
    return {'A':a,'B':b,'C':c,'err':e,'true_hi_R':true_hi,
            'reported_hi_R':got_hi,'padding_factor':got_hi/true_hi,
            'n_runs':l.st['n_runs'],'status':'CALIBRATED',
            'last_step_bound':'x100 holds per extension; no total bound'}

def sbe_origin_union():
    def f(r,i): return 1.43+.202/(r+.01) if i==0 else 1.53+.101/(r+.01)
    l=ladder(f,1e5)
    true_sets=[]
    for a,b in ((1.43,.202),(1.53,.101)):
        true_sets.append([b/(1.63*t-a)-.01 for t in (1.02,.98)])
    outer=[rr.rj_float(l.st[k])/1e5 for k in ('R_j_lo','R_j_hi')]
    assert outer[0]<=min(s[0] for s in true_sets)
    assert outer[1]>=max(s[1] for s in true_sets)
    return {'origin_true_intervals':true_sets,'reported_outer':outer,
            'pushes':{k:v['origin_pushes'] for k,v in l.st['ends'].items()}}

def dbe_origin():
    base=lambda r:3.02+1/(r+.1)
    other=lambda r:1.02+3.2/(r+.1)
    oldcase=predict(lambda r,i,l,c:base(r) if i==0 else other(r))
    j=label(oldcase.values())
    assert j['verdict']=='CONSISTENT_WEAK'
    assert len(oldcase.adj)==12
    blind=predict(lambda r,i,l,c:base(r) if i<3 else other(r))
    blind_j=label(blind.values())
    full={k:(3*base(rrr)+5*other(rrr))/8*1e-3
          for law in rr.LAWS for c in rr.CS
          for role,rrr in zip(rr.RJ_ROLES,(.5,1.,2.))
          for k in [(c,law,role)]}
    full_j=label(full)
    assert blind_j['verdict']=='PASS_INFORMATIVE'
    assert full_j['verdict']=='CONSISTENT_WEAK'
    return {'prior_counterexample':{'label':j['verdict'],'W':j['W'],'adjusted':len(oldcase.adj)},
            'three_origin_blindspot':{'sampled_label':blind_j['verdict'],'sampled_W':blind_j['W'],
              'eight_mean_label':full_j['verdict'],'eight_mean_W':full_j['W'],
              'adjusted_count':len(blind.adj),'sampled_origins':[0,1,2],
              'hidden_origins':[3,4,5,6,7]}}

def logic():
    vals={}
    for i,(c,law) in enumerate((c,l) for l in rr.LAWS for c in rr.CS):
        for role,s in zip(rr.RJ_ROLES,(4.8,4.4+i*.05,4.3)):
            vals[(c,law,role)]=s*1e-3
    statuses={law:'CALIBRATED' for law in rr.LAWS}
    main={'statuses':statuses,'vals':vals,'flags':[]}
    pub,res=rr.assemble(main,{v:main for v in rr.VARIANTS},([],{}))
    assert pub['verdict']=='PASS_INFORMATIVE'
    assert all(v['flag'] is None for v in pub['variants'].values())
    gap={('0','P0','R_j_lo'):3.8,('1','P0','R_j_hi'):4.,
         ('0','P1','R_j_lo'):5.2,('1','P1','R_j_hi'):5.4}
    gap_j=rr.judge(gap)
    assert gap_j['verdict']=='GAP_ENVELOPE_ONLY'
    assert rr.blocking_of(['DIA_UNCHECKED','SV_UNCHECKED'])==['SV_UNCHECKED']
    zeros=[]
    for data in ((0.,0.),(0.,5.),(4.68,4.68)):
        d={('0','P0','R_j_lo'):data[0],('1','P0','R_j_hi'):data[1]}
        j=rr.judge(d)
        scaled=rr.judge({k:v*1e-3 for k,v in d.items()},x=4.68e-3,ref=1.8877e-3)
        assert j['verdict']==scaled['verdict'] and j['state']==scaled['state']
        zeros.append({'values':data,'label':j['verdict'],'state':j['state']})
    return {'noop':pub,'gap':gap_j,'zero_scale_invariance':zeros}

def dbe_nonmonotone():
    # This deliberately violates passive-network R monotonicity. All values
    # are finite, c0=c1, origins equal; existing checks never compare R.
    f=lambda r,i,l,c:4.2 if r==.5 else (4.7 if r==1 else 4.4)
    p=predict(f)
    j=label(p.values())
    assert all(c['ok'] for c in p.checks['same_p'])
    assert j['verdict']=='PASS_INFORMATIVE'
    return {'R':[.5,1.,2.],'sigma_mScm':[4.2,4.7,4.4],
            'same_p_all_pass':True,'verdict':j['verdict'],
            'scope':'missing invariant guard, not a production physical counterexample'}

def sv_origin_scope():
    # Record actual Predict fetch requests. Trigger all four origin
    # expansions, while requesting SV at all three R values.
    limits=(.5,1.,2.)
    keys=dict(zip(rr.RJ_ROLES,map(rr.rj_key,limits)))
    lads={law:dict(keys,r0_sigma=1.63e-3) for law in rr.LAWS}
    calls=[]
    def fetch(kit,role,law,c,key,arms,sv_cf=False):
        calls.append({'role':role,'law':law,'c':c,'rj':key,
                      'arms':list(origin_ids(arms)),'sv_cf':bool(sv_cf)})
        r=rr.rj_float(key)
        return [arm(1.63e-3 if kit==rr.SBE_KIT else
                    (3.02+1/(r+.1) if i==0 else 1.02+3.2/(r+.1))*1e-3)
                for i in origin_ids(arms)]
    p=rr.Predict(fetch,lads,None,sv_scope='all3')
    p.run()
    grouped={role:[x for x in calls if x['role']==role]
             for role in ('corner','origin','origin8')}
    assert len(p.adj)==12
    assert len(grouped['corner'])==12
    assert all(x['sv_cf'] and x['arms']==[0] for x in grouped['corner'])
    assert len(grouped['origin'])==len(grouped['origin8'])==12
    assert not any(x['sv_cf'] for role in ('origin','origin8') for x in grouped[role])
    return {'requested_scope':'all3','adjusted_values':len(p.adj),
            'fetch_counts':{role:len(items) for role,items in grouped.items()},
            'sv_enabled_counts':{role:sum(x['sv_cf'] for x in items) for role,items in grouped.items()},
            'calls':calls,
            'scope':'all3 covers twelve arm-0 corners; it does not certify SV independence of adjusted eight-origin means'}

def budget():
    f_lo=((4191+4276+4326)/3)/((691+692+731)/3)
    f_hi=((5054+5051+5476)/3)/((691+692+731)/3)
    def hours(dbe):
        return [(38*(175+704*f)+dbe*(2578*(1-704/879)+2578*(704/879)*f))/3600 for f in (f_lo,f_hi)]
    return {'SBE_arms':38,'DBE_arms_old':40,'DBE_arms_if_4_upper_solves':44,
            'published_formula_hours':hours(40),'same_formula_with_upper_hours':hours(44),
            'qualification':'arm-equivalent estimate only; upper solve can disconnect early or have different iterations; measure separately'}

def plan_validation():
    # Invoke the production loader on temporary audit fixtures only.
    base={'schema':rr.PLAN_SCHEMA,'len_law':'distributed_v0',
          'unreg_law':'cut','s_min_um':.5,'tol_ff_um':.1,
          'step3_rtol':1e-12,'p2_extra':'--maxiter 1000',
          'max_ladder_points':24,'calib_rj_ratio_max':'none',
          'sv_cf_threshold':2.,'sv_cf_scope':'all3'}
    fixtures=Path(__file__).parent/'fixtures'
    fixtures.mkdir(exist_ok=True)
    cases={}
    for field in ('max_ladder_points','s_min_um','sv_cf_threshold','calib_rj_ratio_max'):
        data=dict(base,**{field:10**400})
        cases['overflow_'+field]=json.dumps(data)
    cases['duplicate_top']=json.dumps(base)[:-1]+',"sv_cf_threshold":100}'
    cases['nan']=json.dumps(dict(base,sv_cf_threshold=float('nan')))
    cases['inf']=json.dumps(dict(base,sv_cf_threshold=float('inf')))
    out={}
    for name,raw in cases.items():
        path=fixtures/(name+'.json')
        path.write_text(raw,encoding='utf-8')
        try: rr.load_plan(path)
        except rr.Stop as exc: out[name]=exc.code
        else: out[name]='ACCEPTED'
        assert out[name]=='PLAN_INVALID',out
    return out

def main():
    out={'pin':'0b3012460fb8e8b7d53484b0efe399e2dc506aec',
         'RCA01':rca01(),'passive_endpoint_sweep':endpoint_sweep(),
         'certificate_padding':guard_padding(),'PRE2_impl03':plan_validation(),
         'SBE_origin_union':sbe_origin_union(),'RCA02_and_origin_scope':dbe_origin(),
         'RCA08_09_10_13':logic(),'DBE_R_monotonicity':dbe_nonmonotone(),
         'SV_all3_origin_scope':sv_origin_scope(),
         'time_estimate':budget()}
    # Probe output only; source archive remains untouched.
    (Path(__file__).parent/'probe_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False))

if __name__=='__main__': main()
