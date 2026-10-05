"""Review-only small regressions in the pinned snapshot; never launches a campaign."""
import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
R=Path(__file__).resolve().parent;W=R.parent;S=R/'source';E=R/'evidence'
JOBS={
 'tau':['scripts/test_tau_flux.py'], 'pipeline':['webapp/test_pipeline_provenance.py'],
 'tau_status':['webapp/test_tau_handover_status.py'], 'chain':['webapp/test_network_handover_chain.py'],
 'network':['scripts/network_conductivity.py','--selftest'],
 'boundary':['scripts/test_network_boundary_rule.py'], 'lw':['scripts/test_love_weber_stress.py'],
 'lw_labels':['webapp/test_stress_lw_labels.py'], 'lhs':['scripts/lhs_design_dataset.py','--selftest'],
 'stress_audit':['scripts/lhs_stress_constriction_audit.py','--selftest'],
 'group':['webapp/test_closed_param_groupview.py'], 'grade':['webapp/test_tau_grade_unify.py'],
 'receipts':['scripts/test_rint_receipts.py'], 'launcher':['scripts/run_network_194_parallel.py','--selftest'],
 'smoke':['scripts/wsl_network_smoke.py','--selftest']}
def env():
 e=dict(os.environ,PYTHONUTF8='1',PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1',MPLCONFIGDIR=str(E/'mplcache'))
 e['PYTHONPATH']=os.pathsep.join([str(W/'lhs_coverage_review_20260930/deps'),str(W/'audit_review_evidence_20260909/pydeps'),str(S/'scripts'),str(S/'webapp')])
 return e
def run(item):
 name,args=item;t=time.monotonic()
 try:
  p=subprocess.run([sys.executable,*args],cwd=S,env=env(),text=True,encoding='utf8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  rc,out=p.returncode,p.stdout
 except subprocess.TimeoutExpired as exc:rc,out=124,str(exc.stdout)
 (E/(name+'.log')).write_text(out,encoding='utf8')
 row=dict(name=name,args=args,rc=rc,seconds=round(time.monotonic()-t,3),tail=out.splitlines()[-8:])
 print(json.dumps(row,ensure_ascii=False),flush=True);return row
if __name__=='__main__':
 names=sys.argv[1:] or list(JOBS)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,[(n,JOBS[n]) for n in names]))
 (E/('tests_'+('_'.join(names))+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
 raise SystemExit(any(r['rc'] for r in rows))
