"""Independent no-fetch recheck. Only local file transport; no simulator."""
from pathlib import Path
import argparse,subprocess,os,sys,json,hashlib,shutil,importlib.util
from unittest import mock
R=Path(__file__).resolve().parent;(R/'tmp').mkdir(exist_ok=True);P=argparse.ArgumentParser();P.add_argument('--out',type=Path,required=True);A=P.parse_args();O=A.out.resolve();O.mkdir(parents=True,exist_ok=False)
PIN='4c29705fa1c4ba94737a858b206fa4f4c5bb2bde';S=R/'snapshot';script=S/'scripts/test_dem_gen2_t12_consumer_contract.py';D=Path('docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024');manifest=json.loads((S/D/'source-manifest.json').read_text(encoding='utf8'));previous=json.loads((S/D/'fixture-results.json').read_text(encoding='utf8'));empty=O/'empty-remote.git'
subprocess.run(['git','init','--bare','--quiet',str(empty)],check=True)
objects=json.loads((R/'evidence/object_database.json').read_text())['objects'];out=[]
def hash_files(repo):
 return {str(x.relative_to(repo)):hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(repo.rglob('*')) if x.is_file()}
def run(label,missing=None,target=script,guarded=True):
 case=O/label;case.mkdir();repo=case/'repo';shutil.copytree(R/'object_repo',repo)
 e={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};e.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0=repo.as_posix(),GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
 for k,v in [('core.repositoryformatversion','1'),('extensions.partialclone','origin'),('remote.origin.url',str(empty)),('remote.origin.promisor','true'),('remote.origin.partialclonefilter','blob:none')]:subprocess.run(['git','-C',str(repo),'config',k,v],env=e,check=True)
 if missing:
  z=(repo/'.git/objects'/missing[:2]/missing[2:]).resolve();assert z.is_relative_to((repo/'.git/objects').resolve());z.unlink()
 before=hash_files(repo);trace=case/'trace.jsonl';e.update(GIT_NO_LAZY_FETCH='0',GIT_TRACE2_EVENT=trace.as_posix(),GIT_TRACE2_ENV_VARS='GIT_NO_LAZY_FETCH');cmd=[sys.executable,'-I','-X','utf8','-B',str(target),'--repo',str(repo)];q=subprocess.run(cmd,capture_output=True,env=e,timeout=45);(case/'stdout.json').write_bytes(q.stdout);(case/'stderr.txt').write_bytes(q.stderr);events=[json.loads(l) for l in trace.read_text(encoding='utf8').splitlines()];fetch=[v for v in events if v.get('event')=='child_start' and 'fetch' in v.get('argv',[])];reads=[v['argv'] for v in events if v.get('event')=='start' and 'show' in v.get('argv',[])];envv=[v for v in events if v.get('event')=='def_param' and v.get('param')=='GIT_NO_LAZY_FETCH'];row={'case':label,'missing':missing,'returncode':q.returncode,'fetch_count':len(fetch),'show_count':len(reads),'shows':reads,'env_trace':envv,'whole_repo_files_unchanged':before==hash_files(repo),'caller_no_lazy_fetch':'0','stdout_sha256':hashlib.sha256(q.stdout).hexdigest(),'trace_sha256':hashlib.sha256(trace.read_bytes()).hexdigest()}
 if guarded:
  row['pass']=not fetch and row['whole_repo_files_unchanged'] and bool(reads) and all('--no-lazy-fetch' in v for v in reads) and bool(envv) and all(v['value']=='1' for v in envv)
  if missing:row['pass'] &= q.returncode==2
  else:
   j=json.loads(q.stdout);row['exact52']=j['cases']==previous['cases'];row['source_hashes_match']=j['source_sha256']==manifest['files_sha256']==previous['source_sha256'];row['status']=j['status'];row['physical_ready']=j['physical_ready'];row['physical_T12']=j['physical_T12'];row['pass'] &= q.returncode==0 and row['exact52'] and row['source_hashes_match'] and j['passed']==j['case_count']==52 and j['physical_ready'] is False and j['physical_T12']=='NOT_RUN' and len(reads)==6
 else:row['pass']=q.returncode==2 and len(fetch)>0
 out.append(row);print(label,q.returncode,len(fetch),row['pass'],flush=True)
run('complete')
for i,obj in enumerate(objects):run('missing_'+str(i)+'_'+obj['type'],obj['sha'])
# Independent mutation: both protections removed, with original fixtures unchanged.
mut=O/'unprotected_source'
for name in ['scripts/test_dem_gen2_t12_consumer_contract.py',str(D/'source-manifest.json'),str(D/'p1-consumer-contract.json')]:
 dest=mut/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(S/name,dest)
m=mut/'scripts/test_dem_gen2_t12_consumer_contract.py';t=m.read_text(encoding='utf8');assert t.count('"git", "--no-lazy-fetch", "-C"')==1;assert t.count('dict(os.environ, GIT_NO_LAZY_FETCH="1")')==1;t=t.replace('"git", "--no-lazy-fetch", "-C"','"git", "-C"').replace('dict(os.environ, GIT_NO_LAZY_FETCH="1")','dict(os.environ)');m.write_text(t,encoding='utf8');blob=next(x for x in objects if x['sha']=='55e8793ad35f72723de7195101be1834996b16a2')['sha'];run('guards_removed_control',blob,m,False)
# Unsupported capability is an explicitly mocked subprocess result, not an old-Git claim.
spec=importlib.util.spec_from_file_location('target',script);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);dest=O/'unsupported';dest.mkdir()
with mock.patch.dict(os.environ,{'GIT_NO_LAZY_FETCH':'0'}),mock.patch.object(module.subprocess,'run',return_value=subprocess.CompletedProcess(['git'],129,stdout=b'',stderr=b'unknown option: --no-lazy-fetch')) as call:
 try:module.snapshot(R/'object_repo',manifest,dest);refused=False
 except ValueError as error:refused=True;message=str(error)
 compat={'type':'mock, no real old Git used','refused':refused,'child_calls':call.call_count,'explicit_flag':'--no-lazy-fetch' in call.call_args.args[0],'forced_environment':call.call_args.kwargs['env']['GIT_NO_LAZY_FETCH'],'output_files':len(list(dest.iterdir())),'message':message};compat['pass']=refused and call.call_count==1 and compat['explicit_flag'] and compat['forced_environment']=='1' and compat['output_files']==0
report={'pin':'96f15ed17e03181b6096fb65f71ec7f577f17523','consumer':PIN,'git':subprocess.check_output(['git','--version']).decode().strip(),'python':sys.version.split()[0],'platform':sys.platform,'runner_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'cases':out,'compatibility_mock':compat,'pass':all(x['pass'] for x in out) and compat['pass'],'physical_runs':0};(O/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');assert report['pass'];print('PASS',len(out),'actual conditions + compatibility mock')
