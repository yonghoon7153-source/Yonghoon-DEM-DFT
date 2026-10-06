from pathlib import Path
import os,sys,subprocess,json,time,concurrent.futures
sys.stdout.reconfigure(encoding='utf8')
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence'
jobs=[['scripts/test_gen2_role_contract.py'],['scripts/test_network_solve_certificate.py'],
 ['webapp/test_gen2_publication_handover.py'],['webapp/test_tau_handover_status.py'],
 ['scripts/lhs_release_build.py','--selftest'],['scripts/test_reread_v12.py'],
 ['scripts/test_physics_area_g2.py'],['scripts/test_network_dirichlet.py'],
 ['scripts/test_network_generation2.py'],['scripts/test_psi_default_switch.py'],
 ['scripts/test_tau_flux.py'],['scripts/test_constriction_power_share.py'],
 ['webapp/test_psi_generation_stamp.py'],['webapp/test_pipeline_provenance.py']]
def run(args):
 env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
 env['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(S/'scripts'),str(S/'webapp')])
 tmp=R/'tmp';tmp.mkdir(exist_ok=True)
 env.update(TMP=str(tmp),TEMP=str(tmp),TMPDIR=str(tmp))
 t=time.monotonic()
 try:
  x=subprocess.run([sys.executable,*args],cwd=S,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=300)
  rc=x.returncode;log=x.stdout+x.stderr
 except subprocess.TimeoutExpired as ex:rc=124;log='timeout: '+str(ex)
 (E/(Path(args[0]).stem+'.log')).write_text(log,encoding='utf8')
 row=dict(args=args,rc=rc,seconds=time.monotonic()-t,tail=log.splitlines()[-6:]);print(json.dumps(row,ensure_ascii=False),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,jobs))
(E/'tests.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
