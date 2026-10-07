"""Synthetic launch records only; actual audit/reread CLI, no worker launch or simulation."""
from pathlib import Path
import sys,os,json,shutil,subprocess,copy,io,contextlib,ast
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/seal_paths';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
import run_network_194_parallel as rn,lhs_webapp_batch as LWB
import test_gen2_publication_handover as PH
PIN='0801d4ceb540f5a5813761b20a5e0f304ed80a03';CASE='lhs00_000'
base=R/'evidence/branch_policy/baseline'
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x),encoding='utf8')
hashes=rn.code_hashes();fp=rn.code_fp(hashes)
dep=rn.code_dependency_closure(S)
unsealed=[]
for rel in dep['files']:
 tree=ast.parse((S/rel).read_text(encoding='utf8'))
 for n in ast.walk(tree):
  names=[a.name for a in n.names] if isinstance(n,ast.Import) else [n.module] if isinstance(n,ast.ImportFrom) and n.level==0 and n.module else []
  for name in names:
   for folder in ['scripts','webapp']:
    p=f'{folder}/{name.split(".")[0]}.py'
    if (S/p).exists() and p not in rn.CODE_FILES:unsealed.append(dict(importer=rel,line=n.lineno,module=p))

def fixture(label):
 root=D/label;har=root/'harvest';har.mkdir(parents=True,exist_ok=True)
 h=har/(CASE+'.json');write(h,{'raw':{k:{'sha256':'1'*64} for k in ['atom','contact','mesh','deck']}})
 cohort=root/'cohort.tsv';cohort.write_text('case\n'+CASE+'\n',encoding='utf8')
 cd=root/'cases'/CASE;dst=cd/'work/results'/CASE;shutil.copytree(base,dst,dirs_exist_ok=True)
 fm=json.loads((dst/'full_metrics.json').read_text());rid=fm['network_run_id'];wr=dict(git_sha=PIN,dirty=False)
 rec=dict(case=CASE,status='done',stop_after='network',failed_stages=[],network_run_id=rid)
 st=dict(schema=LWB.SCHEMA,stop_after='network',harvest_dir=str(har),cohort=str(cohort),runs=[wr],cases={CASE:rec})
 flat={CASE:dict({k:v for k,v in fm.items() if not isinstance(v,(dict,list))},case=CASE)}
 LWB.write_outputs(cd/'out',st,flat);LWB.write_outputs(root/'merged/lhs',st,flat)
 shutil.copytree(dst,root/'merged/lhs/results'/CASE,dirs_exist_ok=True)
 seal=dict(schema=rn.ATTEMPT_SEAL_SCHEMA,launch_fp=fp,fp_start=fp,fp_end=fp,record_written=True,record_sha=rn._rec_sha(rec),worker_run=wr,git_sha_start=PIN,git_sha_end=PIN,dirty_start=False,dirty_end=False)
 write(cd/'worker.json',dict(attempts=[dict(attempt=1,run=1,seal=seal)]))
 plan=dict(cohorts=[dict(name='lhs',harvest_dir=str(har),cohort=str(cohort))],queue=[dict(case=CASE,cohort='lhs')])
 man=dict(schema=rn.SCHEMA,repo_root=str(S),python=sys.executable,git=dict(sha=PIN,dirty=False),code_hashes=hashes,expected_network_generation='g2',generation_probe=dict(generation='g2',g2_name='g2',problems=[]),dependency_closure=dep,seal=dict(schema=rn.LAUNCH_SEAL_SCHEMA,code_fp=fp,files=len(hashes),expected_network_generation='g2'),plan=plan,input_digest=rn.plan_input_digest(plan))
 man.update(launch_format=rn.LAUNCH_FORMAT,code_dependency_closure=dep['files'],handover_code_hashes={x:rn.sha256_file(S/x) for x in rn.HANDOVER_FILES},observe_imports=False)
 man['seal']['launch_format']=rn.LAUNCH_FORMAT
 return root,man,h

out=[]
for label in ['baseline','raw_sha_changed','raw_sha_changed_digest_deleted','raw_sha_changed_digest_null','legacy_record_declared_g2','legacy_record_both_declarations_deleted']:
 root,man,h=fixture(label)
 if label.startswith('raw_sha_changed'):
  j=json.loads(h.read_text());j['raw']['atom']['sha256']='0'*64;write(h,j)
 if label.endswith('digest_deleted'):man.pop('input_digest')
 if label.endswith('digest_null'):man['input_digest']=None
 if label.startswith('legacy_record'):
  p=root/'cases'/CASE/'work/results'/CASE/'network_conductivity_dual.json';du=json.loads(p.read_text());PH.strip_g2(du);write(p,du)
 if label.endswith('both_declarations_deleted'):
  man.pop(rn.GEN_KEY);man['seal'].pop(rn.GEN_KEY)
 write(root/'manifest.json',man)
 p=subprocess.run([sys.executable,str(S/'scripts/run_network_194_parallel.py'),'audit','--root',str(root),'--json',str(root/'audit.json')],capture_output=True,text=True,encoding='utf8')
 (root/'cli.log').write_text(p.stdout+p.stderr,encoding='utf8')
 j=json.loads((root/'audit.json').read_text())
 x=dict(label=label,rc=p.returncode,audit=j)
 if label.endswith('both_declarations_deleted'):x['retry_generation_gate']=rn.generation_gate(man,S)
 out.append(x);print(label,p.returncode,j.get('generation_problems'),j.get('input_problems'),flush=True)

rr=[]
for label in ['baseline','plan_absent','cohorts_empty_queue_present','cohorts_absent_queue_present']:
 root,man,h=fixture('reread_'+label)
 if label=='plan_absent':man.pop('plan')
 if label=='cohorts_empty_queue_present':man['plan']['cohorts']=[]
 if label=='cohorts_absent_queue_present':man['plan'].pop('cohorts')
 write(root/'manifest.json',man)
 p=subprocess.run([sys.executable,str(S/'scripts/g2_network_reread.py'),'--launcher-root',str(root),'--expect-case','lhs:'+CASE,'--json',str(root/'reread.json')],capture_output=True,text=True,encoding='utf8')
 (root/'cli.log').write_text(p.stdout+p.stderr,encoding='utf8')
 x=dict(label=label,rc=p.returncode,result=json.loads((root/'reread.json').read_text()))
 rr.append(x);print('reread',label,p.returncode,len(x['result']['cases']),x['result']['n_fail'],flush=True)
(R/'evidence/seal_paths.json').write_text(json.dumps(dict(code_fp=fp,code_files=len(hashes),dependency_closure=dep,function_imports_not_sealed=unsealed,audit=out,reread=rr),indent=2,ensure_ascii=False),encoding='utf8')
