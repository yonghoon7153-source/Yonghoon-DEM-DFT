"""Capture actual assembled systems and solve them by exact rational elimination."""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[k]='1'
from pathlib import Path
import sys,json,hashlib,copy
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[2]; W=ROOT.parent
sys.path[:0]=[str(ROOT/'repo/scripts'),str(W/'lhs_coverage_review_20260930/deps'),str(W/'gen2_network_reverify3_20261007/deps')]
import test_carbon_junction as T,step3_sigma as S,carbon_junction as C
T.S3=S;T.CJ=C
captured=[]; orig=C.CjuncAssembler._assemble
def capture(self,*args,**kw):
    out,st=orig(self,*args,**kw)
    if 'L' in out:
        ledger=st['sys']
        captured.append({'counterfactual':kw.get('counterfactual',False),'L':out['L'].toarray().tolist(),'b':out['b'].tolist(),'Ab':out['Ab'].tolist(),'gb':out['gb'].tolist(),'At':out['At'].tolist(),'gt':out['gt'].tolist(),'u':ledger['u'].tolist(),'v':ledger['v'].tolist(),'g':ledger['G'].tolist()})
    return out,st
polys=copy.deepcopy(T.QD7_PAR_POLYS);polys[2]=[(0.5,1.5,9.5)]+polys[2]
C.CjuncAssembler._assemble=capture
try: run=T._qd3_run(polys,T.QD7_PAR_SDCP,T.QD7_PAR_N,sdcp_mod={'c':1.0})
finally:C.CjuncAssembler._assemble=orig

def exact_current(a):
    n=len(a['b']); mat=[[F(x) for x in row]+[F(b)] for row,b in zip(a['L'],a['b'])]
    for j in range(n):
        p=next(k for k in range(j,n) if mat[k][j])
        mat[j],mat[p]=mat[p],mat[j]
        for i in range(j+1,n):
            if not mat[i][j]:continue
            mul=mat[i][j]/mat[j][j]
            for k in range(j,n+1):mat[i][k]-=mul*mat[j][k]
    x=[F(0)]*n
    for j in range(n-1,-1,-1):x[j]=(mat[j][n]-sum(mat[j][k]*x[k] for k in range(j+1,n)))/mat[j][j]
    return sum(F(g)*(1-x[i]) for i,g in zip(a['Ab'],a['gb']))
rows=[];curr=[]
for a in captured:
    i=exact_current(a);curr.append(i)
    can={'edges':sorted((min(u,v),max(u,v),float(g).hex()) for u,v,g in zip(a['u'],a['v'],a['g'])),'bot':sorted(zip(a['Ab'],map(float.hex,a['gb']))),'top':sorted(zip(a['At'],map(float.hex,a['gt'])))}
    rows.append({'counterfactual':a['counterfactual'],'n_dof':len(a['b']),'n_raw_edges':len(a['g']),'n_unique_pairs':len(set((min(u,v),max(u,v)) for u,v in zip(a['u'],a['v']))),'weighted_graph_sha256':hashlib.sha256(json.dumps(can,sort_keys=True).encode()).hexdigest(),'exact_assembled_system_current':float(i),'exact_current_fraction':str(i),'bottom_couplings':len(a['Ab']),'top_couplings':len(a['At'])})
ratio=curr[0]/curr[1]
out={'assemblies':rows,'exact_assembled_system_ratio':float(ratio),'ratio_fraction':str(ratio),'interpretation':'Only 1 parallel positive-conductance edge is removed; topology counts agree but weighted circuit differs. Exact elimination uses binary64 entries as exact rationals, independent of production solver and certification.'}
for name,data in [('k0_assembled_systems.json',captured),('weighted_graph_results.json',out)]:
    (ROOT/'evidence/agent_sv'/name).write_text(json.dumps(data,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps(out,indent=2))
assert len(captured)==2 and rows[0]['n_unique_pairs']==rows[1]['n_unique_pairs'] and rows[0]['weighted_graph_sha256']!=rows[1]['weighted_graph_sha256'] and float(ratio)>1.01
