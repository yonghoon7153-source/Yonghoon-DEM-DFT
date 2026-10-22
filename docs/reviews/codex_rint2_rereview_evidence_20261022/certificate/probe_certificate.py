"""Independent bounded Rint2 certificate re-review; no production file writes."""
import contextlib
import importlib.util
import io
import json
import math
import os
import sys
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[1]
NEW = HERE.parent
SOURCE = Path(os.environ.get('RINT_REVIEW_SOURCE', str(NEW / 'source'))).resolve()
sys.path[:0] = [str(SOURCE / 'scripts')]
import numpy as np
from scipy.sparse import csr_matrix
import step3_conv_cert as cc
import step3_sigma as s3
import run_contract as rc

s3.GPU_SOLVE = False
s3.AMG_SOLVE = False
s3.CG_MAXITER = 1000

def quiet(fn, *a, **kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **kw)

def matrix(n, edges, bot, top):
    a = np.zeros((n, n)); b = np.zeros(n)
    for u, v, g in edges:
        a[u,u] += g; a[v,v] += g; a[u,v] -= g; a[v,u] -= g
    for i, g in bot:
        a[i,i] += g; b[i] += g
    for i, g in top:
        a[i,i] += g
    return (csr_matrix(a), b, np.array([i for i,g in bot], dtype=np.int64),
            np.array([g for i,g in bot]), np.array([i for i,g in top], dtype=np.int64),
            np.array([g for i,g in top]))

def rational_solve(n, edges, bot, top):
    a = [[F(0) for _ in range(n+1)] for _ in range(n)]
    for u,v,g in edges:
        g=F(float(g)); a[u][u]+=g; a[v][v]+=g; a[u][v]-=g; a[v][u]-=g
    for i,g in bot:
        a[i][i]+=F(float(g)); a[i][-1]+=F(float(g))
    for i,g in top:
        a[i][i]+=F(float(g))
    for j in range(n):
        pivot=next(i for i in range(j,n) if a[i][j])
        a[j],a[pivot]=a[pivot],a[j]
        q=a[j][j]; a[j]=[v/q for v in a[j]]
        for i in range(n):
            if i!=j and a[i][j]:
                q=a[i][j]; a[i]=[v-q*w for v,w in zip(a[i],a[j])]
    p=[row[-1] for row in a]
    return p,sum((F(float(g))*(1-p[i]) for i,g in bot),F(0))

def exact_energy(p, edges, bot, top):
    p=[F(float(v)) for v in p]
    return (sum((F(float(g))*(p[u]-p[v])**2 for u,v,g in edges),F(0))
            +sum((F(float(g))*(1-p[i])**2 for i,g in bot),F(0))
            +sum((F(float(g))*p[i]**2 for i,g in top),F(0)))

def cert_for(sysd,p):
    L,b,Ab,gb,At,gt=sysd
    den=np.linalg.norm(b)
    res=float(np.linalg.norm(L@p-b)/den) if den else 0.
    return quiet(cc.certify,L,b,p,0,res,1e-12,Ab,gb,At,gt,1.,
                 lambda L,b,x,rt:quiet(s3._solve_cg,L,b,x0=x,rtol=rt))

def prior_cases():
    path=HERE/'baseline_convergence_probes.py'
    spec=importlib.util.spec_from_file_location('prior_convergence',path)
    prior=importlib.util.module_from_spec(spec); spec.loader.exec_module(prior)
    prior.cert=cc; prior.s3=s3
    results={}
    for nm,kwargs in [('main',{'small':True}),('connected',{'small':'connected'}),('iter23',{})]:
        r=quiet(prior.actual_production_cg,**kwargs)
        results[nm]=r
    results['warm_candidate']=quiet(prior.warm_candidate)
    results['zero']=quiet(prior.valid_zero)
    return results

def independent_cases():
    rng=np.random.default_rng(20261022)
    out={'networks':180,'candidates':0,'intervals':0,'not_certifiable':0,'passes_d':0,
         'false_passes':[],'interval_misses':[],'upper_below_exact_energy':[], 'exceptions':[]}
    for case in range(180):
        n=int(rng.integers(2,8))
        # Dyadic random conductance creates broad, exactly representable contrasts.
        def g(): return float((int(rng.integers(1,17))/16.)*2.**int(rng.integers(-44,45)))
        edges=[(i,i+1,g()) for i in range(n-1)]
        for i in range(n):
            for j in range(i+2,n):
                if rng.random()<.35: edges.append((i,j,g()))
        bot=[(0,g())]; top=[(n-1,g())]
        if case%3==0: bot.append((int(rng.integers(n)),g()))
        if case%4==0: top.append((int(rng.integers(n)),g()))
        p,truth=rational_solve(n,edges,bot,top)
        sysd=matrix(n,edges,bot,top)
        pp=np.array([float(x) for x in p])
        candidates=[('exact_rounded',pp),('random',rng.uniform(-1.,2.,n)),
                    ('near',pp+float(2.**int(rng.integers(-52,-10)))*rng.choice([-1.,1.],n))]
        for label,candidate in candidates:
            out['candidates']+=1
            try:
                L,b,Ab,gb,At,gt=sysd
                cb=quiet(cc.target_bracket,L,b,candidate,Ab,gb,At,gt)
                gp=cc.plate_currents(candidate,Ab,gb,At,gt)[0]
                jd=cc.target_judge(cb['target_lo'],cb['target_hi'],gp)
            except Exception as ex:
                out['exceptions'].append([case,label,type(ex).__name__,str(ex)]);continue
            if cb['target_lo'] is None or cb['target_hi'] is None:
                out['not_certifiable']+=1;continue
            out['intervals']+=1
            lo,hi=F(cb['target_lo']),F(cb['target_hi'])
            if not lo<=truth<=hi:
                out['interval_misses'].append([case,label,float(lo),float(truth),float(hi)])
            if hi<exact_energy(candidate,edges,bot,top):
                out['upper_below_exact_energy'].append([case,label])
            if jd['pass_d']:
                out['passes_d']+=1
                if abs(F(gp)-truth)>F(1,10000)*F(gp):
                    out['false_passes'].append([case,label,gp,float(truth)])
    return out

def topology_and_scale():
    out={}
    for name,n,edges,bot,top,p in [
        ('zero',2,[],[(0,1.)],[(1,1.)],[1.,0.]),
        ('zero_bad_phi',2,[],[(0,1.)],[(1,1.)],[1.-1e-9,0.]),
        ('one_node_two_plates',1,[],[(0,3.)],[(0,7.)],[.3]),
        ('floating_component',4,[(0,1,1.),(2,3,100.)],[(0,1.)],[(1,1.)],[2/3,1/3,30.,-30.]),
    ]:
        out[name]=cert_for(matrix(n,edges,bot,top),np.array(p))
    out['short']=cc.early_record({'sigma_eff':0.,'reason':'cjunc_electrode_short','n_dof':4},
                                zero_graph='cjunc_assembled',fp_sid='a'*32,fp_sig='b'*32)
    for name,scale in [('tiny_normal',1e-290),('subnormal',1e-320),('large_finite',1e290)]:
        s=matrix(1,[],[(0,scale)],[(0,scale)])
        try: out[name]=quiet(cc.target_bracket,s[0],s[1],np.array([.5]),*s[2:])
        except Exception as ex: out[name]={'exception':type(ex).__name__,'message':str(ex)}
    # Each energy subtotal is finite, their sum is not. All L elements remain finite.
    s=matrix(5,[],[(i,8e307) for i in range(5)],[(i,8e307) for i in range(5)])
    try: out['finite_subtotals_overflow']=quiet(cc.target_bracket,s[0],s[1],np.full(5,.5),*s[2:])
    except Exception as ex: out['finite_subtotals_overflow']={'exception':type(ex).__name__,'message':str(ex)}
    return out

def consumer_checks():
    c=cert_for(matrix(1,[],[(0,1.)],[(0,1.)]),np.array([.5]))
    c.update(cc.bind_record(fp_sid='a'*32,fp_sig='b'*32,fp_cjunc_registry='c'*32,fp_cjunc_rows='d'*32))
    man={'ca_ext':{'cjunc':{'evidence':{'fp':{'sid':'a'*32,'registry':'c'*32,'plan_rows':'d'*32}}}}}
    out={}
    mutations={
        'valid':{},'old_version':{'version':'conv-cert-v1'},
        'wide_interval':{'target_lo':.4,'target_hi':.6},'reversed_interval':{'target_lo':.6,'target_hi':.4},
        'wrong_sid':{'fp_sid':'f'*32},'wrong_plan':{'fp_cjunc_rows':'f'*32},
        'short_status':{'status':'ELECTRODE_SHORT'},
        'contradictory_U':{'target_U':1e-10},'contradictory_W':{'target_W':1e50},
        'contradictory_top_current':{'I_top':0.},'contradictory_resolve_sigma':{'sigma_resolve':100.},
        'changed_sigma_fingerprint':{'fp_sig':'f'*32},
    }
    for k,m in mutations.items():
        probe=dict(c,**m)
        problem=rc.conv_cert_problem(probe,.5,man)
        out[k]={'accepted':problem is None,'problem':problem}
    return out

def main():
    out={'scope':'Small synthetic networks; not production/campaign data.',
         'python':sys.version,'numpy':np.__version__,'source':cc.__file__,
         'prior':prior_cases(),'independent':independent_cases(),
         'topology_scale':topology_and_scale(),'consumer':consumer_checks()}
    print(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=True))
    (HERE/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=True),encoding='utf-8')

if __name__=='__main__': main()
