"""Read-only target review; all new logs go to this review directory."""
import datetime, json, os, pathlib, subprocess, sys, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'work/r17-response-7c8f61f9/bms-balancing'
name, *args = sys.argv[1:]
env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
started = time.monotonic()
with (HERE / (name+'.log')).open('w', encoding='utf-8') as log:
    p = subprocess.run([sys.executable, *args], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = dict(command=[sys.executable,*args], cwd=str(ROOT), rc=p.returncode,
              seconds=time.monotonic()-started, utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
              python=sys.version)
(HERE/(name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,ensure_ascii=False))
print((HERE/(name+'.log')).read_text(encoding='utf-8')[-10000:])
sys.exit(p.returncode)
