from pathlib import Path
import subprocess,json,os,sys
r=Path(__file__).resolve().parent;env=dict(os.environ,TEMP=str(r/'tmp'),TMP=str(r/'tmp'),TMPDIR=str(r/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0=(r/'object_repo').as_posix(),GIT_NO_LAZY_FETCH='1')
s=r/'snapshot/docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024/independent-ulpri';summary=[]
for name,file in [('loader','reproduce_loader_checks.py'),('mutants','reproduce_consumer_mutants.py')]:
 out=r/'evidence'/name;cmd=[sys.executable,'-I','-X','utf8','-B',str(r/'run_harness_utf8.py'),str(s/file),'--source',str(r/'snapshot'),'--repo',str(r/'object_repo'),'--output',str(out)]
 p=subprocess.run(cmd,env=env,capture_output=True,timeout=180);(r/f'evidence/{name}.log').write_bytes(p.stdout);(r/f'evidence/{name}.stderr').write_bytes(p.stderr);summary.append({'name':name,'rc':p.returncode,'command':cmd,'child_encoding_adaptation':True});print(name,p.returncode,flush=True)
 if out.joinpath('report.json').exists():
  j=json.loads(out.joinpath('report.json').read_text(encoding='utf8'));print(len(j),sum(x.get('pass',x.get('detected',False)) for x in j),flush=True)
(r/'evidence/supplied_harness_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf8')
