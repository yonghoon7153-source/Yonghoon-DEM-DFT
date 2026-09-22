"""Review-owned runner. Never edits the target; saves raw process outputs."""
import datetime,json,os,pathlib,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent
WORK=HERE.parents[1]
ROOT=WORK/'work/gate66-head/degradation-degeneracy'
PY=WORK/'work/gate65-venv/Scripts/python.exe'
commands={
 'identity':[str(PY),'-c','from src.io import source_digest; import sys; print(sys.version); print(source_digest())'],
 'targeted':[str(PY),'-m','pytest','tests/test_gate65_defensive.py','tests/test_gate64_defensive.py','--noconftest','-q','-p','no:cacheprovider','-k','not kernel_lock_probe_control_actually','--basetemp='+str(HERE/'pytest-target'),'--junitxml='+str(HERE/'targeted.xml')],
 'preimages':[str(PY),'docs/22p_gap/mutation_replay.py','--check-preimages'],
 'collection':[str(PY),'-m','pytest','tests/test_gate65_defensive.py','--collect-only','-q','-p','no:cacheprovider'],
 'replay':[str(PY),'docs/22p_gap/mutation_replay.py','-k','g65','--keep-sandbox'],
 'old_real_entry':[str(PY),str(WORK/'outputs/gate65_review_20260922/repro_real_entry.py'),'--repo',str(ROOT),'--out',str(HERE/'old-real-entry')],
 'premise_env_disabled':[str(PY),'-m','pytest','tests/test_gate65_defensive.py','--noconftest','-q','-p','no:cacheprovider','-k','the_interpreter_fixture_measures_its_own_premise','--basetemp='+str(HERE/'pytest-premise-disabled'),'--junitxml='+str(HERE/'premise-env-disabled.xml')],
}
name=sys.argv[1];cmd=commands[name]
env=dict(os.environ);env['PYTHONIOENCODING']='utf-8';env['PYTHONUTF8']='1';env['PYTHONDONTWRITEBYTECODE']='1'
if name=='premise_env_disabled':env['PYTHONNOUSERSITE']='1'
t=time.monotonic()
try:
 p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,timeout=900)
 out,err,rc=p.stdout,p.stderr,p.returncode
except subprocess.TimeoutExpired as e:
 out,err,rc=e.stdout or b'',e.stderr or b'',None
(HERE/(name+'.stdout.bin')).write_bytes(out);(HERE/(name+'.stderr.bin')).write_bytes(err)
rec=dict(command=cmd,cwd=str(ROOT),rc=rc,seconds=time.monotonic()-t,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),env_overrides={k:env.get(k) for k in ('PYTHONIOENCODING','PYTHONUTF8','PYTHONDONTWRITEBYTECODE','PYTHONNOUSERSITE')})
(HERE/(name+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(rec));print(out.decode('utf-8','replace')[-10000:]);print(err.decode('utf-8','replace')[-5000:])
sys.exit(rc if rc is not None else 124)
