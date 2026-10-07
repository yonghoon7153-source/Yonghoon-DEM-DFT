"""Read-only audit/release gates on reviewer synthetic records; no workers launched."""
from pathlib import Path
import sys,json,copy,shutil,subprocess,os
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/new_gates';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import run_network_194_parallel as rn,lhs_release_build as lb
base=R/'evidence/seal_paths/baseline'
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False),encoding='utf8')
aud=[]
for label in ['none','empty_file','unsealed_log','unsealed_log_lost','only_nonrepo_line']:
 d=D/label;shutil.copytree(base,d,dirs_exist_ok=True)
 m=json.loads((d/'manifest.json').read_text());m['observe_imports']=True;save(d/'manifest.json',m)
 logs=d/rn.IMPORT_OBS_DIR/'log';logs.mkdir(parents=True,exist_ok=True)
 if label!='none':(logs/'1000.txt').write_text('' if label=='empty_file' else str(S/'scripts/network_conductivity.py')+'\n',encoding='utf8')
 if label=='unsealed_log':(logs/'1001.txt').write_text(str(S/'scripts/coating_presets.py')+'\n',encoding='utf8')
 if label=='only_nonrepo_line':(logs/'1000.txt').write_text('not-a-valid-module-path\n',encoding='utf8')
 p=subprocess.run([sys.executable,str(S/'scripts/run_network_194_parallel.py'),'audit','--root',str(d),'--json',str(d/'audit.json')],capture_output=True,text=True,encoding='utf8')
 (d/'audit.log').write_text(p.stdout+p.stderr,encoding='utf8');j=json.loads((d/'audit.json').read_text())
 row=dict(label=label,rc=p.returncode,observed=j.get('import_observation'),problems=j.get('import_observation_problems'),verdicts=j.get('verdicts'));aud.append(row);print('IMPORT',json.dumps(row,ensure_ascii=False))
gate=[]
ok=dict(schema='g2_network_reread/v2',expected_generation='g2',n_fail=0,expected_set='production194',expected_n=194,read_n=194,set_equal=True)
for label in ['good','absent','invalid_json','null','empty_object','n_fail_null','failed','failed_audit','refused_audit']:
 d=D/('release_'+label);d.mkdir(exist_ok=True)
 if label!='absent':
  rr=copy.deepcopy(ok)
  if label=='empty_object':rr={}
  if label=='null':rr=None
  if label=='n_fail_null':rr['n_fail']=None
  if label=='failed':rr['n_fail']=1
  save(d/'reread.json',rr)
  if label=='invalid_json':(d/'reread.json').write_text('{',encoding='utf8')
 audit=dict(refused=True,eligibility=dict(kind='invalid',problems=['review fixture'])) if label=='refused_audit' else dict(verdicts=dict(UNSEALED=1),generation_problems=['wrong generation']) if label=='failed_audit' else dict(verdicts=dict(SEALED=194))
 save(d/'seal_audit.json',audit)
 try:r,w=lb.v13_batch_gate_check(str(d));row=dict(label=label,accepted=True,warnings=w,records=r)
 except Exception as e:row=dict(label=label,accepted=False,error=str(e))
 gate.append(row);print('RELEASE',label,row['accepted'])
out=dict(audit=aud,release_gate=gate,qualification='Synthetic completed one-case audit records; no production 194. Release gate is real called function, not a full release build.')
save(R/'evidence/new_gates.json',out)
