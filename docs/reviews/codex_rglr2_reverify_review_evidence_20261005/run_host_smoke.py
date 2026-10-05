"""Review-only synthetic real pipeline; use host subprocess waiting, not Linux wait4."""
import os,sys,json,subprocess,time,shutil
from pathlib import Path
from run_tests import env
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence'
root=E/'host_smoke';root.mkdir(exist_ok=True)
rows=[]
for name,stop in [('synthetic_general',None),('synthetic_network','network')]:
 spec=dict(root=str(root/name),id=name,kind='synthetic',bed='se_am',type_map='1:SE,2:AM_P',scale=1,stop=stop)
 pth=root/(name+'.json');pth.write_text(json.dumps(spec),encoding='utf8')
 t=time.monotonic()
 p=subprocess.run([sys.executable,str(S/'scripts/wsl_network_smoke.py'),'--_child',str(pth)],cwd=root,env=env(),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf8',errors='replace',timeout=180)
 (root/(name+'.log')).write_text(p.stdout,encoding='utf8')
 rep=root/name/'cases'/name/'report.json'
 report=json.loads(rep.read_text(encoding='utf8')) if rep.is_file() else {}
 rows.append(dict(name=name,rc=p.returncode,seconds=time.monotonic()-t,report=report))
 print(json.dumps(dict(name=name,rc=p.returncode,status=report.get('status'),stage_e=report.get('stage_e_ran'),why=report.get('why')),ensure_ascii=False),flush=True)
(E/'host_smoke_summary.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
