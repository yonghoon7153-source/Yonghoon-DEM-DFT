"""Execute requested small regression tests against untouched pinned source."""
import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
R=Path(__file__).resolve().parent; W=R.parent;S=R/'source'; E=R/'evidence'
P=sys.executable
JOBS={
'chain':['webapp/test_network_handover_chain.py'],
'pipeline':['webapp/test_pipeline_provenance.py'],
'tau_flux':['scripts/test_tau_flux.py'],
'tau_status':['webapp/test_tau_handover_status.py'],
'network':['scripts/network_conductivity.py','--selftest'],
'receipts':['scripts/test_rint_receipts.py'],
'contract':['scripts/run_contract.py','--selftest'],
'spearman':['scripts/rint03_je_compare.py','--selftest'],
'lw':['scripts/test_love_weber_stress.py'],
'lhs':['scripts/lhs_design_dataset.py','--selftest'],
'boundary':['scripts/test_network_boundary_rule.py'],
'power':['scripts/test_constriction_power_share.py'],
'verdict':['scripts/sdcp_gain_verdict.py','--selftest'],
'step3':['scripts/step3_sigma.py','--selftest-rint'],
'lw_labels':['webapp/test_stress_lw_labels.py'],
'rint_labels':['webapp/test_rint_scope_labels.py'],
'group':['webapp/test_closed_param_groupview.py'],
'grade':['webapp/test_tau_grade_unify.py'],
}
def env():
 e=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',PYTHONIOENCODING='utf-8',
        MPLCONFIGDIR=str(E/'mplcache'))
 e['PYTHONPATH']=os.pathsep.join([str(W/'lhs_coverage_review_20260930/deps'),str(W/'audit_review_evidence_20260909/pydeps'),str(S/'scripts'),str(S/'webapp')])
 return e
def run(pair):
 name,args=pair;t=time.monotonic()
 try:
  p=subprocess.run([P,*args],cwd=S,env=env(),text=True,encoding='utf8',errors='replace',
    stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  rc,out=p.returncode,p.stdout
 except subprocess.TimeoutExpired as ex:rc,out=124,str(ex.stdout)
 (E/(name+'.log')).write_text(out,encoding='utf8')
 rec=dict(name=name,args=args,rc=rc,seconds=round(time.monotonic()-t,3),tail=out.splitlines()[-8:])
 print(json.dumps(rec,ensure_ascii=False),flush=True)
 return rec
if __name__=='__main__':
 wanted=sys.argv[1:]
 jobs={k:v for k,v in JOBS.items() if not wanted or k in wanted}
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(run,jobs.items()))
 (E/('baseline_'+('_'.join(wanted) if wanted else 'all')+'.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')

