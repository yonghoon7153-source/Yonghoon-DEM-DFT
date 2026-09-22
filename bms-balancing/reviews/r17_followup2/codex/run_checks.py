"""Diagnostic runner. Target source is unmodified; logs go beside this script."""
import datetime, json, os, pathlib, subprocess, sys, time, uuid
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'work/r17-followup2-a4c311ef/bms-balancing'
name, *args = sys.argv[1:]
if args[:2] == ['-m', 'pytest']:
    base = HERE/('pytest-'+name+'-'+uuid.uuid4().hex[:8])
    if base.exists() or not base.resolve().is_relative_to(HERE):
        raise RuntimeError('Unsafe pytest scratch path')
    args.append('--basetemp='+str(base))
env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
start = time.monotonic()
with (HERE/(name+'.log')).open('w',encoding='utf-8') as log:
    p = subprocess.run([sys.executable,*args],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
record = dict(command=[sys.executable,*args],cwd=str(ROOT),rc=p.returncode,
              seconds=time.monotonic()-start,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version)
(HERE/(name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
print((HERE/(name+'.log')).read_text(encoding='utf-8')[-14000:])
sys.exit(p.returncode)
