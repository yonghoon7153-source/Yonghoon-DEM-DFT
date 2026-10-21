"""Bounded exploratory search for actual zero-start Jacobi-CG false acceptance."""
import sys, time, json
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'lhs_coverage_review_20260930'/'deps'))
sys.path.insert(0,'/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee/scripts')   # path constant only (10-21 re-run)
import numpy as np
from scipy.sparse import csr_matrix, diags
from scipy.sparse.linalg import cg
import step3_conv_cert as cert

rng=np.random.default_rng(611)
found=[]; best=None; start=time.monotonic(); count=0
for sample in range(200000):
    n=int(rng.integers(6,26)); k=10.**rng.uniform(-5,5,n+1)
    # Passive one-dimensional inhomogeneous resistor chain plus source-only stub.
    # Exact conductance is 1/sum(1/k), with no ill-conditioned reference solve.
    G=10.**rng.uniform(6,17)
    A=np.zeros((n+1,n+1)); b=np.zeros(n+1); b[0]=k[0]; b[-1]=G
    A[0,0]+=k[0]; A[n-1,n-1]+=k[-1]; A[-1,-1]=G
    for j in range(n-1):
        A[j,j]+=k[j+1]; A[j+1,j+1]+=k[j+1]
        A[j,j+1]-=k[j+1]; A[j+1,j]-=k[j+1]
    eps=float(k.min()*10.**rng.uniform(-3,2))
    A[-1,-1]+=eps; A[0,0]+=eps; A[-1,0]-=eps; A[0,-1]-=eps
    L=csr_matrix(A); M=diags(1/A.diagonal())
    x,info=cg(L,b,rtol=1e-12,atol=0,M=M,maxiter=300)
    Ib=k[0]*(1-x[0])+G*(1-x[-1]); It=k[-1]*x[n-1]
    keff=k.copy(); keff[0]+=G*eps/(G+eps)
    true=1/np.sum(1/keff); err=abs(Ib-true)/true
    bal=abs(Ib-It)/abs(Ib) if Ib else np.inf
    count+=1
    if info==0 and err>1e-4:
        row={'sample':sample,'n':n,'G':G,'eps':eps,'k':k.tolist(),'info':int(info),'err':float(err),'balance':float(bal),'Ib':float(Ib),'It':float(It),'true_G':float(true),'phi':x.tolist()}
        if best is None or bal<best['balance']: best=row
        if bal<=1e-4:
            res=lambda LL,bb,xx,rt:cg(LL,bb,x0=xx,rtol=rt,atol=0,M=M,maxiter=300)
            c=cert.certify(L,b,x,int(info),float(np.linalg.norm(L@x-b)/np.linalg.norm(b)),1e-12,
                           np.array([0,n]),np.array([k[0],G]),np.array([n-1]),np.array([k[-1]]),1.,res)
            row['certificate']=c
            ib2, it2=c['resolve_I_bot'],c['resolve_I_top']
            if c['ok'] and abs(ib2-it2)/abs(ib2)<=1e-4:
                if not found or row['err'] > found[0]['err']: found[:] = [row]
    if time.monotonic()-start>80: break
out={'n_tests':count,'seconds':time.monotonic()-start,'found':found,'best_balance_bad':best}
(ROOT/'geometry'/'search_cg_connected_results.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
