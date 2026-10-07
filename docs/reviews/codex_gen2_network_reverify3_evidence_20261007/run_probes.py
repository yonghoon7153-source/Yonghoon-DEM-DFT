from pathlib import Path
import os,sys,subprocess,json,time
R=Path(__file__).resolve().parent;S=R/'source'
(R/'tmp').mkdir(exist_ok=True);(R/'evidence').mkdir(exist_ok=True)
sys.stdout.reconfigure(encoding='utf8')
env=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
env['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(R/'deps'),str(S/'scripts'),str(S/'webapp')])
env.update(TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
out=[]
for n in sys.argv[1:] or ['acceptance','branch_policy','dependency_gap','input_digest']:
 t=time.monotonic();p=subprocess.run([sys.executable,'-B',str(R/'probes'/f'{n}.py')],cwd=R,env=env,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=300)
 (R/'evidence'/f'{n}.log').write_text(p.stdout+p.stderr,encoding='utf8');r=dict(probe=n,rc=p.returncode,seconds=time.monotonic()-t,tail=(p.stdout+p.stderr).splitlines()[-8:]);out.append(r);print(json.dumps(r,ensure_ascii=False),flush=True)
(R/'evidence'/('runs_'+('_'.join(sys.argv[1:]) or 'original')+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
sys.exit(any(r['rc']!=0 for r in out))
