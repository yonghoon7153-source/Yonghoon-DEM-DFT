from pathlib import Path
import tempfile,shutil,hashlib,re,subprocess,sys,json
R=Path(__file__).resolve().parents[3];W=Path(sys.argv[1]).resolve();W.mkdir(parents=True,exist_ok=False);REL='docs/reviews/mixer_first8_launch_preparation_20261106';SOURCE=R/REL
specs=[
 ('environment','submit_one.py.txt','    env=scheduler_environment()','    env=dict(os.environ)','test_submission_environment_injection'),
 ('campaign_capacity','submit_one.py.txt',"require(reserved+live['running_first8']<policy['max_concurrency'],'campaign slots reserved')","require(True,'campaign slots reserved')",'test_shared_concurrency_one'),
 ('campaign_uncertain','submit_one.py.txt',"require(outcome.get('state')=='SUBMITTED' and outcome.get('approval_sha256')==item.get('approval_sha256')\n                    and outcome.get('case')==case and str(outcome.get('job_id','')).isdigit(),'campaign uncertainty HOLD')","require(True,'campaign uncertainty HOLD')",'test_uncertain_submission_holds_other_cases'),
 ('end_receipt_exclusive','job_start.py.txt',"os.open(str(root/'job_end.json'),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)","os.open(str(root/'job_end.json'),os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)",'test_late_end_receipt_is_not_overwritten')]
results=[]
for name,file,old,new,test in specs:
 with tempfile.TemporaryDirectory(prefix='mla-mutation-') as td:
  repo=Path(td);d=repo/REL;shutil.copytree(SOURCE,d)
  for a in json.loads((SOURCE/'source_seal.json').read_bytes())['files']:
   p=repo/a['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(R/a['path'],p)
  f=d/file;s=f.read_text();assert s.count(old)==1,(name,s.count(old));f.write_text(s.replace(old,new))
  # Keep identity plumbing valid, so the selected behavior guard is tested.
  f=d/'submit_one.py.txt';s=f.read_text();h=hashlib.sha256((d/'job_start.py.txt').read_bytes()).hexdigest()
  f.write_text(re.sub("REVIEWED_JOB_START_SHA256='[0-9a-f]{64}'","REVIEWED_JOB_START_SHA256='"+h+"'",s))
  argv=[sys.executable,'-I','-B',str(d/'test_mla_boundaries.py'),'MLATests.'+test]
  p=subprocess.run(argv,capture_output=True);raw=p.stdout+p.stderr;(W/('mutation_'+name+'.log')).write_bytes(raw)
  detected=p.returncode==1 and b'FAIL:' in raw and b'ERROR:' not in raw
  results.append({'mutation':name,'test':test,'rc':p.returncode,'detected_by_assertion_failure':detected,'log':'mutation_'+name+'.log','scope':'scratch copy only; all product subprocesses mocked'})
(W/'mutations.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results));assert all(x['detected_by_assertion_failure'] for x in results)
