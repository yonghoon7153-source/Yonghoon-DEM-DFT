"""Run the real verifier CLI against reviewer copies; no production modifications."""
from pathlib import Path
import sys,json,subprocess,os,shutil
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/reread_extra';D.mkdir(exist_ok=True)
rel='docs/data/lhs_network194_11fcf91e8';hd=S/rel/'handover_v12_20261006'
base=D/'reference';base.mkdir(exist_ok=True)
for relfile in [rel+'/manifest.json',rel+'/merged/lhs/metrics_flat.csv',rel+'/merged/lhs/status.json',rel+'/merged/lhsx/metrics_flat.csv',rel+'/merged/lhsx/status.json','docs/data/lhs_handover_20261001.csv','docs/data/lhsx_handover_20261001.csv','docs/data/lhs_perc_audit_20261001/lhs_20261001_d1ec42fba/perc_audit.tsv','docs/data/lhs_perc_audit_20261001/lhsx_20261001_d1ec42fba/perc_audit.tsv']:
 q=base/relfile;q.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(S/relfile,q)
v=D/'reread_v12.py';shutil.copyfile(hd/'reread_v12.py',v)
mp=base/rel/'manifest.json';orig=json.loads(mp.read_text());out=[]
for label in ('baseline','queue_empty','plan_absent','queue_duplicate'):
 m=json.loads(json.dumps(orig))
 if label=='queue_empty':m['plan']['queue']=[]
 if label=='plan_absent':m.pop('plan',None)
 if label=='queue_duplicate':m['plan']['queue'].append(copy:=dict(m['plan']['queue'][0]))
 mp.write_text(json.dumps(m),encoding='utf8');o=D/(label+'.json')
 env=dict(os.environ,REPO=str(base),PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
 p=subprocess.run([sys.executable,str(v),'--handover-dir',str(hd),'--seal-audit',str(hd/'seal_audit.tsv'),'--out',str(o)],env=env,capture_output=True,text=True,encoding='utf8')
 j=json.loads(o.read_text());out.append(dict(label=label,rc=p.returncode,verdict=j['verdict'],c8=j['C8_seal_audit'],fails=j['fails']))
 (D/(label+'.log')).write_text(p.stdout+p.stderr,encoding='utf8');print(label,p.returncode,j['verdict'],j['C8_seal_audit']['queue_n'],flush=True)
mp.write_text(json.dumps(orig),encoding='utf8')
(R/'evidence/reread_extra.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf8')
