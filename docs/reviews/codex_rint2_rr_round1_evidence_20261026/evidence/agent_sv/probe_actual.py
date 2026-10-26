"""Read-only SV review: actual producer fixtures, contract and decision probes.
Synthetic transport manifest only; all solve/certificate/edge/census values are actual producer output.
"""
import os
for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'): os.environ[k]='1'
from pathlib import Path
import sys, json, math, copy, hashlib
ROOT=Path(__file__).resolve().parents[2]
W=ROOT.parent
sys.path[:0]=[str(ROOT/'repo/scripts'),str(W/'lhs_coverage_review_20260930/deps'),str(W/'gen2_network_reverify3_20261007/deps')]
import numpy as np, scipy
import test_carbon_junction as T, step3_sigma as S, carbon_junction as C
import ca_ext_svcf as V, ca_ext_cjunc as CW, run_contract as RC, rint_r_chain as RR
T.S3=S; T.CJ=C
OUT=ROOT/'evidence/agent_sv'

def manifest(reg,pl,r,rec=None):
    a=pl['record']; sd=pl.get('sdcp_mod')
    prot=CW.cjunc_protocol_record(R_j_ohm=a['R_j_ohm'],len_law=a['len_law'],unreg_law=a['unreg_law'],s_min_um=a['s_min_um'],tol_ff_um=a['thresholds']['tol_ff_um'],ptfe_jlaw=a['ptfe_jlaw'],ptfe_stamp=a['ptfe_stamp'])
    sdp=None if sd is None else CW.sdcp_mod_protocol_record(c=sd['c'],tol_sj_um=a['thresholds']['tol_sj_um'])
    prep={'protocol':prot,'sdcp_protocol':sdp,'counts':a['counts'],'census':reg['census'],'fp':{'sid':reg['fp']['sid'],'registry':reg['fp']['registry'],'plan_rows':pl['fp_rows']},'plan':pl}
    rc={name:CW.solve_receipt(r if name=='electronic_main' else None,prep,name=name,disabled_why=None if name=='electronic_main' else 'review fixture disabled') for name in CW.SOLVES}
    blk=CW.payload_blocks(prep,rc,r)
    V.attach_evidence(blk['cjunc']['evidence'],{'threshold':None})
    if rec is not None: blk['cjunc']['evidence']['solve']['sv_counterfactual']=copy.deepcopy(rec)
    return {'fibre_stamp':'segment','ptfe_stamp':'off','component_plan':{'electronic':True,'ionic':False,'thermal':False,'pore':False,'collector':False},'field_requested':False,'periodic_xy':False,'interface_model':None,'sdcp_bridge_um':0.0,'sigma_vgcf_S_cm':100.0,'ca_ext_requested':sorted(blk),'ca_ext':{'schema':RC.CA_EXT_SCHEMA,**blk}}

def evidence(reg,pl,r,cf): return T._qd3_ev(reg,pl,r,cf)
def record(e): return e['solve']['sv_counterfactual']
def flags(e,t): return RR.sv_assess({('1','P0','R_j0'):{'sv_cf':V.chain_view(record(e))}},t,'R_j0')[0]
def assess(run,t):
    reg,pl,r,cf=run; ev=evidence(*run); m=manifest(reg,pl,r)
    return ev, {'problem':V.sv_cf_problem(ev,True),'run_contract':RC.ca_ext_record_ok(m),'flags':flags(ev,t),'interval':record(ev)['ratio_cert_interval'],'nominal':cf['sv_counterfactual_ratio'],'counts':{k:cf.get(k) for k in ('n_sv_faces_cut','n_reach_pairs_cut','n_unsplit_bridging_components')},'topo_main':[cf['conv_cert_full'].get(k) for k in V.CERT_TOPO_KEYS],'topo_cut':[cf['conv_cert'].get(k) for k in V.CERT_TOPO_KEYS]}

# Concrete materialization of disclosed k=0 limitation. Only change from PAR:
# extend the left (currently dangling) branch to the upper electrode.
polys=copy.deepcopy(T.QD7_PAR_POLYS)
polys[2]=[(0.5,1.5,9.5)]+polys[2]
run=T._qd3_run(polys,T.QD7_PAR_SDCP,T.QD7_PAR_N,sdcp_mod={'c':1.0})
ev,base=assess(run,1.01)
sw=T._qd5_swap(ev,'lower',V)
reg,pl,r,cf=run
ms=manifest(reg,pl,r,record(sw))
raw=manifest(reg,pl,r)
counts_unchanged={k:record(ev).get(k)==record(sw).get(k) for k in record(ev) if k.startswith('n_')}
full_binding_keys=('version','status','I_bot','target_lo','target_hi')+V.BIND_FIELDS+V.CERT_TOPO_KEYS
full_binding_equal=all(record(sw)['conv_cert_full'].get(k)==r['conv_cert'].get(k) for k in full_binding_keys)
case={'geometry':{'polys':polys,'sdcp':T.QD7_PAR_SDCP,'shape':T.QD7_PAR_N,'h_um':1.0,'rj_ohm':1000.0,'sdcp_mod':{'c':1.0}},'honest':base,'swapped':{'problem':V.sv_cf_problem(sw,True),'run_contract':RC.ca_ext_record_ok(ms),'flags_t1_01':flags(sw,1.01),'interval':record(sw)['ratio_cert_interval'],'all_cut_counts_unchanged':all(counts_unchanged.values()),'counts_unchanged':counts_unchanged,'read_run_full_cert_comparison_equal':full_binding_equal},'G_full':cf['G_full_code'],'G_cut':cf['G_cut_code'],'threshold_note':'1.01 is a legal illustrative threshold; no numeric production threshold is registered in this pin. t=2 honestly clears before and after.','t2_honest':flags(ev,2.0),'t2_swapped':flags(sw,2.0)}
for nm,data in [('k0_honest_manifest.json',raw),('k0_swapped_manifest.json',ms),('k0_actual_main_result.json',{'conv_cert':r['conv_cert'],'sigma_eff':r['sigma_eff']}),('k0_actual_evidence.json',ev)]:
    p=OUT/nm; p.write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False,default=lambda x:x.item() if isinstance(x,np.generic) else x.tolist()),encoding='utf-8')
case['artifact_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('k0_*.json')}
assert base['run_contract']==(True,None) and case['swapped']['run_contract']==(True,None)
assert base['flags']==['SV_DEPENDENT'] and case['swapped']['flags_t1_01']==[]
assert case['swapped']['all_cut_counts_unchanged'] and full_binding_equal

# Re-exercise original RCA2-01 counterexample using actual certificates.
from scipy.sparse.linalg import spsolve
calls=[0]
def perturbed(L,b,*a,**kw):
    calls[0]+=1; x=spsolve(L.tocsc(),b)
    return (x+1e-8 if calls[0]==1 else x),0
sr=T._qd3_svx(solver=perturbed)
tr=T._svx_ref(T.SVX_RJ)[0]/T._svx_ref(T.SVX_RJ,with_sv=False)[0]
th=(sr[3]['sv_counterfactual_ratio']+tr)/2
e,ans=assess(sr,th)
ans.update(threshold=th,hand_circuit_ratio=tr,solver_calls=calls[0])
assert ans['problem'] is None and ans['run_contract']==(True,None) and ans['nominal']<th<ans['interval'][0] and ans['flags']==['SV_DEPENDENT']

# Honest FLOAT and upper-FLOAT records must not be refused by topology relation.
honest={}
for name,args in [('FLOAT',(T.QD7_FL_POLYS,T.QD7_FL_SDCP,T.QD7_FL_N)),('UFLOAT',(T.QD7_UFL_POLYS,T.QD7_UFL_SDCP,T.QD7_UFL_N)),('PAR',(T.QD7_PAR_POLYS,T.QD7_PAR_SDCP,T.QD7_PAR_N))]:
    rr=T._qd3_run(*args,sdcp_mod={'c':1.0} if name=='PAR' else None)
    _,honest[name]=assess(rr,2.0)
    assert honest[name]['run_contract']==(True,None)

# Original RCA2-04 bad record classes using certified real SVX output.
rr=T._qd3_svx(); ee=evidence(*rr); mm=manifest(*rr[:3]); mutations={}
def mut(name,fn):
    a=copy.deepcopy(mm); fn(a['ca_ext']['cjunc']['evidence']); result=RC.ca_ext_record_ok(a)
    mutations[name]=result; assert result[0] is False
mut('missing_lower_certificate',lambda a:record(a).update(conv_cert=None))
mut('foreign_main_certificate',lambda a:record(a).update(conv_cert=copy.deepcopy(record(ev)['conv_cert'])))
mut('unregistered_bracket_rule',lambda a:record(a).update(bracket_rule='another_rule'))
mut('unsplit_count_10pow400',lambda a:record(a).update(n_unsplit_bridging_components=10**400))
mut('unregistered_kind',lambda a:record(a).update(kind='counterfactual_cut_sv_faces'))
mut('unregistered_cut_rule',lambda a:record(a).update(rule='another_rule'))
qr=T._qd3_run(T.QD4_POLYS,T.QD4_SDCP,T.QD4_N)
qm=manifest(*qr[:3]); qm['ca_ext']['cjunc']['evidence']['solve']['sv_counterfactual']['upper']['n_components_removed']=0
mutations['two_unsplit_zero_removed']=RC.ca_ext_record_ok(qm)
assert mutations['two_unsplit_zero_removed'][0] is False
out={'runtime':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__},'scope':'Actual producer and ca_ext_record_ok + sv_assess; full read_run not invoked in this probe. read_run full-certificate equality checked verbatim.','k0_disclosed_limitation_realized':case,'RCA2_01_original_counterexample':ans,'honest_FLOAT':honest,'RCA2_04_negative_cases':mutations}
(OUT/'probe_actual_results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False))

