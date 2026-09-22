"""Review-only runner: writes logs outside the target; never edits production files."""
import argparse, datetime, json, os, pathlib, platform, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1] / 'work' / 'r17-head' / 'bms-balancing'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('args', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = [sys.executable, *a.args]
    env = dict(os.environ, PYTHONUTF8='1', PYTHONDONTWRITEBYTECODE='1')
    start = time.monotonic()
    with (HERE / (a.name + '.log')).open('w', encoding='utf-8') as log:
        p = subprocess.run(cmd, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    record = dict(command=cmd, cwd=str(ROOT), rc=p.returncode, seconds=time.monotonic()-start,
                  utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  python=sys.version, platform=platform.platform())
    (HERE/(a.name+'.json')).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False),flush=True)
    print((HERE/(a.name+'.log')).read_text(encoding='utf-8')[-6000:])
    return p.returncode

if __name__ == '__main__':
    sys.exit(main())
