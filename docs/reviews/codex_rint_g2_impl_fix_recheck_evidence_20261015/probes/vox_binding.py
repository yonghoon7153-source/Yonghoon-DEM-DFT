"""RIMP-05: real solver calls, exact spacing binding, independent positive controls."""
from pathlib import Path
import sys, json, copy, contextlib, io, importlib.util, hashlib
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'source/scripts'),str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps')]
import numpy as np
from scipy.sparse.linalg import spsolve
import step3_sigma as S

def plan_for(c,r,sid,h):
    led=S.am_iface_ledger(c,r,np.array([2,2]),sid,sid,(0.,0.,0.),h,delta_bound_um=0.,bridge_um=1.2*h)
    return S.am_iface_plan(led,{'AM_S|AM_S':1e-3})

def main():
    h=.2;c=np.array([[1.,1.,1.],[1.,1.,2.98]]);r=np.ones(2)
    with contextlib.redirect_stdout(io.StringIO()):
        sid,_=S.rasterize(c,r,np.array([2,2]),None,None,(0,0,0),(2,2,4),h,bridge_um=1.2*h)
    p=plan_for(c,r,sid,h);p2=plan_for(2*c,2*r,sid,2*h)
    sig=S.electronic_sigma_table(.010,.005,100.,10.,250.)
    cases=[('matching',h,p),('mismatched',2*h,p),('rebuilt_scaled',2*h,p2),
           ('nextafter_spacing',float(np.nextafter(h,np.inf)),p),('same_float64',float('0.2'),p),
           ('nan_spacing',float('nan'),p),('inf_spacing',float('inf'),p),('zero_spacing',0.,p),('negative_spacing',-.2,p)]
    for name,changes in [('plan_vox_changed',{'vox':.4}),('plan_vox_missing',{'vox':'DELETE'}),
                         ('plan_ledger_vox_changed',{'ledger':.4}),('plan_ledger_vox_nan',{'ledger':float('nan')})]:
        q=copy.deepcopy(p)
        for key,value in changes.items():
            if key=='ledger':q['ledger']['vox']=value
            elif value=='DELETE':q.pop(key)
            else:q[key]=value
        cases.append((name,h,q))
    rows=[];orig=S._solve_cg
    try:
        for name,vox,plan in cases:
            calls=[]
            def solve(L,b):
                calls.append(len(b));return spsolve(L.tocsc(),b),0
            S._solve_cg=solve
            row={'case':name,'solver_vox':vox,'plan_vox':plan.get('vox')}
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    out=S.solve_sigma_z(sid,sig,vox,return_field=True,z_bot_um=0.,z_top_um=20*vox,iface=plan)
                ledger=out['iface']['iface_contact_ledger']
                G=sum(float(np.sum(1e-8*vox*vox/a['rface'][~a['cut']])) for a in out['_iface']['axes'])
                row.update(status='SOLVED',sigma=out['sigma_eff'],resid=out['resid'],
                    reported_A_um2=ledger['A_film_sum_um2'],reported_G_S=ledger['film_G_S_total'],actual_G_S=G)
            except Exception as e:row.update(status='REJECT',exception=type(e).__name__,message=str(e))
            row['cg_calls']=len(calls);rows.append(row)
        direct=[]
        for vox in (None,.2,.4):
            try:S.iface_require_quantitative(p,sid,sig,vox=vox);status='ACCEPT'
            except Exception as e:status=type(e).__name__+': '+str(e)
            direct.append({'vox':vox,'result':status})
    finally:S._solve_cg=orig
    out={'rows':rows,'direct_gate_calls':direct,
         'scaled_A_ratio':rows[2]['reported_A_um2']/rows[0]['reported_A_um2'],
         'scaled_G_ratio':rows[2]['actual_G_S']/rows[0]['actual_G_S']}
    (R/'evidence/vox_binding.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
