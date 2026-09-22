"""Reviewer-owned command capture; no target edits or real science runs."""
import datetime, json, os, pathlib, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parents[1]
REPO = WORK / 'work/gate67-head'
ROOT = REPO / 'degradation-degeneracy'
PY = WORK / 'work/gate65-venv/Scripts/python.exe'
tests = ['tests/test_gate66_defensive.py', 'tests/test_gate65_defensive.py', 'tests/test_gate64_defensive.py']
commands = {
 'identity': [str(PY), '-c', 'from src.io import source_digest; import sys; print(sys.version); print(source_digest())'],
 'targeted': [str(PY), '-m', 'pytest', *tests, '--noconftest', '-q', '-p', 'no:cacheprovider', '-k', 'not kernel_lock_probe_control_actually', '--basetemp='+str(HERE/'pytest-target'), '--junitxml='+str(HERE/'targeted.xml')],
 'preimages': [str(PY), 'docs/22p_gap/mutation_replay.py', '--check-preimages'],
 'collection': [str(PY), '-m', 'pytest', 'tests/test_gate66_defensive.py', '--collect-only', '-q', '-p', 'no:cacheprovider'],
 'replay': [str(PY), 'docs/22p_gap/mutation_replay.py', '-k', 'g66', '--keep-sandbox'],
 'old_repro': [str(PY), str(WORK/'outputs/gate66_review_20260922/repro_startup.py'), '--repo', str(ROOT), '--out', str(HERE/'old-startup'), '--full-sandbox', '--case', 'plain', '--case', 'cwd_only_candidate', '--case', 'cwd_on_pythonpath', '--case', 'remove_loaded_path', '--case', 'reorder_loaded_path'],
 'disabled': [str(PY), '-m', 'pytest', 'tests/test_gate65_defensive.py', '--noconftest', '-q', '-p', 'no:cacheprovider', '-k', 'the_interpreter_fixture_measures_its_own_premise', '--basetemp='+str(HERE/'pytest-disabled'), '--junitxml='+str(HERE/'disabled.xml')],
}
name=sys.argv[1]; cmd=commands[name]
env=dict(os.environ)
env.update(PYTHONIOENCODING='utf-8', PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
if name=='disabled': env['PYTHONNOUSERSITE']='1'
t=time.monotonic()
try:
 p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,timeout=1200)
 out,err,rc=p.stdout,p.stderr,p.returncode
except subprocess.TimeoutExpired as e: out,err,rc=e.stdout or b'',e.stderr or b'',None
(HERE/(name+'.stdout.bin')).write_bytes(out); (HERE/(name+'.stderr.bin')).write_bytes(err)
rec=dict(command=cmd,cwd=str(ROOT),rc=rc,seconds=time.monotonic()-t,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),env_overrides={k:env.get(k) for k in ('PYTHONUTF8','PYTHONIOENCODING','PYTHONDONTWRITEBYTECODE','PYTHONNOUSERSITE')})
(HERE/(name+'.json')).write_text(json.dumps(rec,indent=2),encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8');print(json.dumps(rec));print(out.decode('utf-8','replace')[-7000:]);print(err.decode('utf-8','replace')[-5000:])
sys.exit(rc if rc is not None else 124)
