import concurrent.futures, json, os, subprocess, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[1]
S = R / 'source'
jobs = {
 'tau_flux': ['scripts/test_tau_flux.py'],
 'tau_grade_unify': ['webapp/test_tau_grade_unify.py'],
 'tau_labels': ['webapp/test_tau_labels.py'],
 'tau_handover_status': ['webapp/test_tau_handover_status.py'],
 'grade_engine': ['scripts/grade_engine.py', '--selftest'],
 'pipeline_provenance': ['webapp/test_pipeline_provenance.py'],
 'lhs_webapp_batch': ['scripts/lhs_webapp_batch.py', '--selftest'],
}
def run(item):
 name, args = item
 env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
 env['PYTHONPATH'] = os.pathsep.join([str(S/'scripts'), str(S/'webapp'), env.get('PYTHONPATH','')])
 start=time.time()
 try:
  p=subprocess.run([sys.executable,*args],cwd=S,env=env,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=240)
  rc,out=p.returncode,p.stdout
 except subprocess.TimeoutExpired as e:
  rc,out=124,str(e.stdout)
 (Path(__file__).parent/(name+'.log')).write_text(out,encoding='utf-8')
 result={'name':name,'args':args,'rc':rc,'seconds':round(time.time()-start,3),'tail':out.splitlines()[-9:]}
 print(json.dumps(result,ensure_ascii=False),flush=True)
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(run,jobs.items()))
(Path(__file__).parent/'baselines.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf-8')
