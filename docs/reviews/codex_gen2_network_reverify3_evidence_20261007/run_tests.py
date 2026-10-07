from pathlib import Path
import os,sys,subprocess,json,time,concurrent.futures
sys.stdout.reconfigure(encoding='utf8')
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence'
(R/'tmp').mkdir(exist_ok=True);E.mkdir(exist_ok=True)
jobs=[['webapp/test_gen2_publication_handover.py'],['scripts/test_gen2_role_contract.py'],['scripts/g2_network_reread.py','--selftest'],['scripts/test_lhs_release_v13.py'],['scripts/seal_s3_prerun.py','--selftest'],['scripts/run_s3_psi.py','--selftest'],['webapp/test_pipeline_provenance.py'],['webapp/test_network_handover_chain.py'],['scripts/lhs_design_dataset.py','--selftest'],['scripts/test_network_solve_certificate.py'],['scripts/test_tau_flux.py'],['webapp/test_tau_handover_status.py'],['scripts/test_reread_v12.py'],['webapp/test_gen2_stamp_record.py'],['webapp/test_psi_generation_stamp.py'],['scripts/test_network_generation2.py'],['scripts/test_network_boundary_rule.py'],['webapp/test_tau_grade_unify.py'],['webapp/test_tau_labels.py']]
if len(sys.argv)>1: jobs=[j for j in jobs if Path(j[0]).stem in sys.argv[1:]]
def run(args):
 env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
 env['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(R/'deps'),str(S/'scripts'),str(S/'webapp')])
 env.update(TMP=str(R/'tmp'),TEMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
 t=time.monotonic()
 try:
  x=subprocess.run([sys.executable,'-B',*args],cwd=S,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=240)
  rc=x.returncode;log=x.stdout+x.stderr
 except subprocess.TimeoutExpired as ex:rc=124;log='timeout: '+str(ex)
 (E/(Path(args[0]).stem+'.log')).write_text(log,encoding='utf8')
 row=dict(args=args,rc=rc,seconds=time.monotonic()-t,tail=log.splitlines()[-7:]);print(json.dumps(row,ensure_ascii=False),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,jobs))
(E/('tests_rerun.json' if len(sys.argv)>1 else 'tests.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
sys.exit(any(r['rc']!=0 for r in rows))
