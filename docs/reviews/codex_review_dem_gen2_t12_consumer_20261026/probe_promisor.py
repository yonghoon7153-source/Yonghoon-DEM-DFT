from pathlib import Path
import subprocess,os,sys,json,shutil,argparse
R=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=R/'evidence/promisor_probe');a=p.parse_args();O=a.out.resolve();O.mkdir(parents=True,exist_ok=False);repo=O/'partial';shutil.copytree(R/'object_repo',repo);empty=O/'empty-remote.git';subprocess.run(['git','init','--bare','--quiet',str(empty)],check=True)
env=dict(os.environ,GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='safe.directory',GIT_CONFIG_VALUE_0=repo.as_posix(),GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'));env.pop('GIT_NO_LAZY_FETCH',None)
for key,value in [('core.repositoryformatversion','1'),('extensions.partialclone','origin'),('remote.origin.url',str(empty)),('remote.origin.promisor','true'),('remote.origin.partialclonefilter','blob:none')]:
 subprocess.run(['git','-C',str(repo),'config',key,value],env=env,check=True)
tree=json.loads((R/'evidence/consumer_tree3.json').read_text());sha=next(x['sha'] for x in tree['tree'] if x['path']=='ul_gates.py');p=(repo/'.git/objects'/sha[:2]/sha[2:]).resolve();assert p.is_relative_to((repo/'.git/objects').resolve());p.unlink()
rows=[]
for label,block in [('unprotected',False),('lazy_fetch_disabled',True)]:
 e=dict(env,GIT_TRACE2_EVENT=(O/f'{label}.trace.jsonl').as_posix());
 if block:e['GIT_NO_LAZY_FETCH']='1'
 cmd=[sys.executable,'-I','-X','utf8','-B',str(R/'snapshot/scripts/test_dem_gen2_t12_consumer_contract.py'),'--repo',str(repo)];q=subprocess.run(cmd,env=e,capture_output=True,timeout=60);(O/f'{label}.stdout').write_bytes(q.stdout);(O/f'{label}.stderr').write_bytes(q.stderr);trace=[json.loads(l) for l in (O/f'{label}.trace.jsonl').read_text(encoding='utf8').splitlines()];fetch=[v for v in trace if v.get('event')=='child_start' and 'fetch' in v.get('argv',[])];rows.append({'case':label,'rc':q.returncode,'fetch_processes':len(fetch),'fetch_events':fetch,'protocol_allowed':'file only; no external network','stderr':q.stderr.decode('utf8')});print(label,q.returncode,len(fetch))
assert rows[0]['rc']==rows[1]['rc']==2 and rows[0]['fetch_processes']>0 and rows[1]['fetch_processes']==0
(O/'result.json').write_text(json.dumps({'missing_blob':sha,'source_unchanged':True,'rows':rows},indent=2),encoding='utf8')
