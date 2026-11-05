"""Small real producer/contract review of RR1-01 and the declared Q3 limit.
Resident fixture builders supply geometry; mutation and rational solve are independent.
No registered campaign, production kit, or source mutation.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[k]='1'
import sys, json, copy
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent.parent/'received'/'repo'; OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
import test_carbon_junction as T, step3_sigma as S, carbon_junction as C
import ca_ext_svcf as V, run_contract as RC, rint_r_chain as RR
T.S3=S; T.CJ=C
polys=[[(1.5,1.5,.5),(1.5,1.5,4.9)],[(2.5,.5,4.5),(2.5,2.5,4.5)],
       [(.5,1.5,9.5),(.5,1.5,5.5),(2.9,1.5,5.5)],[(5.5,1.5,.5),(5.5,1.5,9.5)]]
sdcp=[(1.95,1.5,5.05)]; shape=(7,3,10)
captured=[]; original=C.CjuncAssembler._assemble
def capture(self,*a,**kw):
    result,stats=original(self,*a,**kw)
    if 'L' in result:
        captured.append({'L':result['L'].toarray().tolist(),'b':result['b'].tolist(),'Ab':result['Ab'].tolist(),
                         'gb':result['gb'].tolist(),'At':result['At'].tolist(),'gt':result['gt'].tolist(),
                         'graph_fp':stats.get('graph_fp'),'counterfactual':kw.get('counterfactual',False)})
    return result,stats
C.CjuncAssembler._assemble=capture
try: run=T._qd3_run(polys,sdcp,shape,sdcp_mod={'c':1.})
finally: C.CjuncAssembler._assemble=original
reg,plan,result,raw=run
honest=V.sv_cf_record(raw)
origsolve=S._solve_cg
def no_solve(*a,**kw): raise AssertionError('graph-only attempted a solve')
S._solve_cg=no_solve
try: graphs=T._qg_graphs(polys,sdcp,shape,sdcp_mod={'c':1.})
finally: S._solve_cg=origsolve
def exact_current(a):
    n=len(a['b']); mat=[[F(x) for x in row]+[F(b)] for row,b in zip(a['L'],a['b'])]
    for j in range(n):
        p=next(i for i in range(j,n) if mat[i][j]); mat[j],mat[p]=mat[p],mat[j]
        for i in range(j+1,n):
            if not mat[i][j]: continue
            m=mat[i][j]/mat[j][j]
            for k in range(j,n+1):mat[i][k]-=m*mat[j][k]
    x=[F(0)]*n
    for j in reversed(range(n)):x[j]=(mat[j][n]-sum(mat[j][k]*x[k] for k in range(j+1,n)))/mat[j][j]
    return sum(F(g)*(1-x[i]) for i,g in zip(a['Ab'],a['gb']))
currents=[exact_current(a) for a in captured]
assert len(currents)==2
ratio=currents[0]/currents[1]
assert F(honest['ratio_cert_interval'][0])<=ratio<=F(honest['ratio_cert_interval'][1])
swapped=copy.deepcopy(honest)
swapped['conv_cert']=copy.deepcopy(honest['conv_cert_full'])
swapped['G_cut_code']=honest['G_full_code']; swapped['sv_counterfactual_ratio']=1.
swapped['sv_counterfactual_ratio_hi']=1.
swapped['ratio_cert_interval']=[V._enc(x) for x in V.cert_interval(swapped)]
assert all(honest[k]==swapped[k] for k in honest if k.startswith('n_'))
forged=copy.deepcopy(swapped); forged['conv_cert'][V.GRAPH_KEY]=graphs['lower']
def inspect(name,rec,source):
    man=T._qg_manifest(reg,plan,result,rec)
    contract=RC.ca_ext_record_ok(man,graphs=source)
    gs=RR.sv_graph_state(rec,{},0,'fixture.json',str(OUT),graph_src=(lambda ctx:source) if source is not None else None,plan={})
    flags=RR.sv_assess({('1','P0','R_j0'):{'sv_cf':V.chain_view(rec),'sv_graph':gs}},1.01,'R_j0',require_graph=True)[0]
    OUT.joinpath(name+'_manifest.json').write_text(json.dumps(man,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
    return {'contract':contract,'graph_state':gs,'flags':flags,'interval':rec['ratio_cert_interval']}
cases={'honest':inspect('honest',honest,graphs),'original_swap':inspect('swap',swapped,graphs),
       'no_source':inspect('no_source',honest,None),'declared_Q3_forgery':inspect('forged',forged,graphs)}
assert cases['honest']['contract']==(True,None) and cases['honest']['flags']==['SV_DEPENDENT']
assert cases['original_swap']['contract'][0] is False and cases['original_swap']['graph_state']['state']=='mismatch'
assert cases['no_source']['flags']==['SV_UNCHECKED']
assert cases['declared_Q3_forgery']['contract']==(True,None) and cases['declared_Q3_forgery']['flags']==[]
extra={}
for name,args in [('QDX',(T.QDX_POLYS,T.QDX_SDCP,T.QDX_N)),('QD4',(T.QD4_POLYS,T.QD4_SDCP,T.QD4_N))]:
    rr=T._qd3_run(*args); rg,pp,rs,rw=rr; rec=V.sv_cf_record(rw)
    gg=T._qg_graphs(*args); man=T._qg_manifest(rg,pp,rs,rec)
    assert RC.ca_ext_record_ok(man,graphs=gg)==(True,None)
    bad={}
    for key in ('n_reach_pairs_cut','n_reach_pairs_cut_vs_lower','n_edges_cut','n_plate_couplings_cut'):
        for value in (None,True,-1,1.,'1',2**63,float('nan')):
            mm=copy.deepcopy(man); mm['ca_ext']['cjunc']['evidence']['solve']['sv_counterfactual']['upper'][key]=value
            ans=RC.ca_ext_record_ok(mm,graphs=gg); bad[f'{key}={value!r}']=ans
            assert ans[0] is False,(name,key,value)
    mm=copy.deepcopy(man); ev=mm['ca_ext']['cjunc']['evidence']; rr2=ev['solve']['sv_counterfactual']
    ev['census']['n_unsplit_bridging_components']=0; rr2['n_unsplit_bridging_components']=0; rr2['upper']=None
    for key in ('status','sv_counterfactual_ratio','ratio_limit'):rr2[key+'_hi']=rr2[key]
    rr2['ratio_cert_interval']=[V._enc(x) for x in V.cert_interval(rr2)]
    internal=RC.ca_ext_record_ok(mm); external=RC.ca_ext_record_ok(mm,graphs=gg)
    sealed={k:regv for k,regv in rg['census'].items() if k in V.CENSUS_KEYS}
    census_problem=RR.sv_census_problem(rr2,ev['census'],sealed)
    assert internal==(True,None) and external[0] is False and census_problem
    extra[name]={'bad_count_mutations_rejected':len(bad),'census_edited_internal':internal,'census_edited_graph_source':external,
                 'census_edited_S0':census_problem}
out={'scope':'Real producer/contract and graph-state/decision functions; not full ledger read_run or production shell execution.',
     'exact_ratio':float(ratio),'exact_ratio_fraction':str(ratio),'graphs':graphs,'counts':{k:honest[k] for k in honest if k.startswith('n_')},
     'cases':cases,'adjacent_mutations':extra,'Q3_classification':'Declared coordinated certificate-fingerprint forgery limitation, not a new residual finding.'}
OUT.joinpath('actual_binding_results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False,allow_nan=False),encoding='utf-8')
OUT.joinpath('actual_assemblies.json').write_text(json.dumps(captured,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps(out,indent=2,ensure_ascii=False))
