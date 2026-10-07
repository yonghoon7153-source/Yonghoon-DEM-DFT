"""Independent actual CLI + publisher probes. Fault injection is not a physical bed result."""
from pathlib import Path
import sys,os,json,copy,contextlib,io,inspect,shutil
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/branch_policy';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import app,pipeline_service as ps,tau_flux as tf,test_pipeline_provenance as TP
import test_gen2_publication_handover as PH,lhs_design_dataset as LDD,lhs_webapp_batch as LWB
import scipy.sparse.linalg as spl

def mutate(d,label):
 for name,key in PH.NET_FILES:
  p=Path(d)/name;o=json.loads(p.read_text(encoding='utf8'));r=o.get('hertzian') if key is None else o if key=='hertzian' else None
  if r:
   if label=='cf_sigma0_x2':
    c=r['solve_certificate_bulk_net'];c['sigma_bulk_S_cm']*=2
    q=c['I_bottom']/c['delta_V']*c['g_to_q']
    r['sigma_bulk_net_mScm']=round(1000*q*c['sigma_bulk_S_cm'],6)
   if label=='full_cert_sigma0_x2':r['solve_certificate_full']['sigma_bulk_S_cm']*=2
   if label=='diagnostic_fields_absent':
    for k in ['sigma_bulk_net','sigma_bulk_net_mScm','sigma_bulk_net_status','sigma_bulk_net_reason','solve_certificate_bulk_net']:r.pop(k,None)
  p.write_text(json.dumps(o),encoding='utf8')

def in_h0_cf():
 f=sys._getframe(1);mode=None
 while f:
  if f.f_code.co_name=='solve_network':mode=f.f_locals.get('mode')
  if f.f_code.co_name=='run_decomposition':
   return mode=='bulk_only' and f.f_locals.get('_mode')=='ionic' and f.f_locals.get('contact_mode')=='hertzian' and f.f_locals.get('hertz_constriction')=='maxwell'
  f=f.f_back
 return False

out=[]
for label in ['baseline','cf_sigma0_x2','full_cert_sigma0_x2','diagnostic_fields_absent','honest_cf_exception','honest_cf_cert_failure']:
 d=D/label;d.mkdir(exist_ok=True);a,c=TP._write_bed(str(d),'through');(d/'full_metrics.json').write_text(json.dumps(TP._bed_ledger('through')),encoding='utf8')
 runner=TP._CLIRunner(mutate=(lambda p,l=label:mutate(p,l)) if label in ['cf_sigma0_x2','full_cert_sigma0_x2','diagnostic_fields_absent'] else None)
 raw={n:getattr(spl,n) for n in ('spsolve','cg','gmres')};hits=[]
 def wrapper(n):
  def call(A,b,*args,**kw):
   if label.startswith('honest_cf') and in_h0_cf():
    hits.append(n)
    if label=='honest_cf_exception':raise RuntimeError('REVIEW_INJECTED_CF_ONLY_SOLVER_EXCEPTION')
    import numpy as np
    return np.zeros_like(b) if n=='spsolve' else (np.zeros_like(b),0)
   return raw[n](A,b,*args,**kw)
  return call
 log=io.StringIO()
 with contextlib.redirect_stdout(log),patch.multiple(spl,**{n:wrapper(n) for n in raw}):
  stages,rid=app._network_and_stage_e(str(d),str(S/'scripts'),a,c,'1:SE',1,[],runner=runner,stop_before_stage_e=True)
 status,failed=ps.summarize(stages);row=tf.case_row(str(d));du=json.loads((d/'network_conductivity_dual.json').read_text()) if (d/'network_conductivity_dual.json').exists() else runner.produced.get('network_conductivity_dual.json',{})
 rh=du.get('hertzian',{});item=dict(label=label,status=status,fault_calls=hits,full_q=rh.get('sigma_full'),cf_q=rh.get('sigma_bulk_net'),cf_dim=rh.get('sigma_bulk_net_mScm'),sigma0=rh.get('sigma_grain_S_cm'),cf_status=rh.get('sigma_bulk_net_status'),cf_reason=rh.get('sigma_bulk_net_reason'),cf_cert=rh.get('solve_certificate_bulk_net'),contract=tf.network_generation_contract(du),stop=ps.network_stop_verdict(str(d),rid),tau=row.get('tau2_ion_hertz'),why=PH._why(stages))
 br=D/('handover_'+label);res=br/'results';res.mkdir(parents=True,exist_ok=True);cd=res/'lhs00_000';shutil.copytree(d,cd,dirs_exist_ok=True)
 fm=json.loads((cd/'full_metrics.json').read_text());st=dict(schema=LWB.SCHEMA,stop_after='network',harvest_dir='',cohort='',runs=[],cases={'lhs00_000':dict(case='lhs00_000',stop_after='network',status=status,failed_stages=[],network_run_id=rid)})
 LWB.write_outputs(br/'batch',st,{'lhs00_000':dict({k:v for k,v in fm.items() if not isinstance(v,(dict,list))},case='lhs00_000')})
 try:
  h=LDD.load_tau_results(res,LDD.load_webapp(br/'batch'),expected_generation='g2');item['handover']=True
 except Exception as ex:item['handover']=False;item['handover_error']=str(ex)
 import g2_network_reread as rr
 if status=='done':
  re=rr.reread_case(d,'g2',ps,tf);item['reread_bad']=[x for x in re['checks'] if not x['ok']]
 (d/'review_run.log').write_text(log.getvalue(),encoding='utf8');out.append(item)
 print(label,status,'q=',item['full_q'],'cf=',item['cf_dim'],'handover=',item['handover'],'fault_calls=',hits,'reread_bad=',item.get('reread_bad'),flush=True)
(R/'evidence/branch_policy.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
