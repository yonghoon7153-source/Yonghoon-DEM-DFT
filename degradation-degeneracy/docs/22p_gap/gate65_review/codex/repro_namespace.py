"""Use ASCII JSON transport to isolate loader semantics from Windows cp949 stdout."""
from pathlib import Path
import argparse, json, os, subprocess, sys
p=argparse.ArgumentParser()
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--out',type=Path,required=True)
a=p.parse_args()
a.repo=a.repo.resolve()
a.out=a.out.resolve()
a.out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(a.repo/'docs/22p_gap'))
import mutation_replay as mr
(a.out/'sitecustomize').mkdir()
env=mr.replay_env()
env.update(PYTHONPATH=str(a.out),PYTHONNOUSERSITE='1')
src=mr._ENV_PROBE_BODY+'\nimport json\nprint(json.dumps(_receipt_facts('+repr(mr._probe_names())+', [], '+repr(str(a.out))+'), ensure_ascii=True))\n'
r=subprocess.run([sys.executable,'-c',src],cwd=a.out,env=env,capture_output=True,text=True,timeout=120)
assert r.returncode==0,r.stderr
got=json.loads(r.stdout)
try:
    mr._assert_receipt_is_complete(got)
    outcome='ACCEPTED'
except Exception as e:
    outcome=f'{type(e).__name__}: {e}'
observation={'transport':'ASCII JSON; unchanged receipt body and completeness checker',
             'receipt':got,'completeness_result':outcome}
(a.out/'observation.json').write_text(json.dumps(observation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'startup_status':got['startup']['status'],'history':got['startup']['startup_history'],'completeness_result':outcome},ensure_ascii=False))
