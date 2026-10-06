from pathlib import Path
import os,sys,subprocess,json,time,concurrent.futures
sys.stdout.reconfigure(encoding='utf8')
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence';E.mkdir(exist_ok=True)
jobs=['scripts/test_physics_area_g2.py','scripts/test_network_dirichlet.py','scripts/test_network_generation2.py','scripts/test_psi_default_switch.py','scripts/test_tau_flux.py','scripts/test_constriction_power_share.py','webapp/test_psi_generation_stamp.py']
def run(p):
 env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
 env['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(S/'scripts'),str(S/'webapp')])
 t=time.monotonic()
 try:
  r=subprocess.run([sys.executable,p],cwd=S,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=240);rc=r.returncode;log=r.stdout+r.stderr
 except subprocess.TimeoutExpired:rc=124;log='timeout'
 (E/(Path(p).stem+'.log')).write_text(log,encoding='utf8')
 item=dict(path=p,rc=rc,seconds=time.monotonic()-t,tail=log.splitlines()[-5:]);print(json.dumps(item,ensure_ascii=False),flush=True);return item
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: rows=list(pool.map(run,jobs))
(E/'tests.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
