from pathlib import Path
import os,json,hashlib,subprocess,shutil,zlib,importlib.util
from unittest import mock
import sys
U=Path(__file__).parent;A=U.parent/'author';out=U/'independent-offline';out.mkdir(exist_ok=False);freeze=json.loads((A/'SOURCE-FREEZE.json').read_text());source=out/'source';repo=Path('/workspace/Yonghoon-DEM-DFT');sha=lambda b:hashlib.sha256(b).hexdigest()
for x in freeze['code_files']:
 b=Path(x['source']).read_bytes();assert sha(b)==x['sha256']==sha((repo/x['main_path']).read_bytes());p=source/x['main_path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
E='docs/reviews/dem_gen2_t12_consumer_contract_evidence_20261024'
for n in ['source-manifest.json','p1-consumer-contract.json','fixture-results.json']:
 p=source/E/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/E/n).read_bytes())
runner=source/'scripts/test_dem_gen2_t12_consumer_contract.py';author=json.loads((A/'final/result.json').read_text());positive=json.loads((A/'final/complete-six-blobs/stdout.json').read_text());old=json.loads((source/E/'fixture-results.json').read_text());assert positive['cases']==old['cases'] and positive['source_sha256']==old['source_sha256'] and positive['passed']==52 and positive['fixture_script_sha256']==sha(runner.read_bytes())
pt=[json.loads(l) for l in (A/'final/complete-six-blobs/trace.jsonl').read_text().splitlines()];reads=[e for e in pt if e.get('event')=='start' and 'show' in e.get('argv',[])];assert len(reads)==6 and all('--no-lazy-fetch' in e['argv'] for e in reads);assert not [e for e in pt if e.get('event')=='child_start' and 'fetch' in e.get('argv',[])]
seed=A/'final/complete';assert not (seed/'.git/objects/info/alternates').exists()
for obj in author['objects']:
 p=seed/'.git/objects'/obj['oid'][:2]/obj['oid'][2:];raw=zlib.decompress(p.read_bytes());header,b=raw.split(b'\0',1);assert hashlib.sha1(raw).hexdigest()==obj['oid'] and sha(b)==obj['sha256']
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')};env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_ALLOW_PROTOCOL='file',GIT_TERMINAL_PROMPT='0',GIT_NO_LAZY_FETCH='0')
remote=out/'empty.git';subprocess.run(['git','-c','init.templateDir=','init','--bare','-q',str(remote)],env=env,check=True)
def treehash(path):return {str(p.relative_to(path)):sha(p.read_bytes()) for p in path.rglob('*') if p.is_file()}
rows=[]
def run(name,missing,script):
 d=out/name;d.mkdir();objrepo=d/'repo';shutil.copytree(seed,objrepo);subprocess.run(['git','-C',str(objrepo),'config','remote.origin.url',str(remote)],env=env,check=True)
 oid=next(x['oid'] for x in author['objects'] if x['revision']==missing);(objrepo/'.git/objects'/oid[:2]/oid[2:]).unlink();before=treehash(objrepo);trace=d/'trace.jsonl';e=dict(env,GIT_TRACE2_EVENT=str(trace));cmd=[sys.executable,'-I','-X','utf8','-B',str(script),'--repo',str(objrepo)];cp=subprocess.run(cmd,env=e,capture_output=True,timeout=60);(d/'stdout').write_bytes(cp.stdout);(d/'stderr').write_bytes(cp.stderr);events=[json.loads(l) for l in trace.read_text().splitlines()];fetch=[x for x in events if x.get('event')=='child_start' and 'fetch' in x.get('argv',[])];shows=[x for x in events if x.get('event')=='start' and 'show' in x.get('argv',[])];row={'case':name,'rc':cp.returncode,'fetch_processes':len(fetch),'git_show_count':len(shows),'all_show_guarded':all('--no-lazy-fetch'in x['argv'] for x in shows),'entire_object_repo_files_unchanged':before==treehash(objrepo),'trace_sha256':sha(trace.read_bytes()),'parent_guard':'0'};rows.append(row);assert cp.returncode==2 and before==treehash(objrepo)
 if name.startswith('guarded'):assert not fetch and shows and row['all_show_guarded']
 else:assert fetch and not row['all_show_guarded']
pin=author['consumer_pin'];run('guarded-missing-blob',pin+':docs/data/ps45_unload_20261009/ul_gates.py',runner);run('guarded-missing-commit',pin,runner)
mut=out/'mutant';shutil.copytree(source,mut);mr=mut/'scripts/test_dem_gen2_t12_consumer_contract.py';s=mr.read_text();assert s.count('"git", "--no-lazy-fetch", "-C"')==1;s=s.replace('"git", "--no-lazy-fetch", "-C"','"git", "-C"').replace('dict(os.environ, GIT_NO_LAZY_FETCH="1")','dict(os.environ)');mr.write_text(s);run('whole-guard-removed',pin+':docs/data/ps45_unload_20261009/ul_gates.py',mr)
sp=importlib.util.spec_from_file_location('reviewed',runner);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);dest=out/'unsupported';dest.mkdir();manifest=json.loads((source/E/'source-manifest.json').read_text())
with mock.patch.dict(os.environ,{'GIT_NO_LAZY_FETCH':'0'}),mock.patch.object(m.subprocess,'run',return_value=subprocess.CompletedProcess(['git'],129,b'',b'unknown option')) as child:
 try:m.snapshot(seed,manifest,dest)
 except ValueError as e:assert '--no-lazy-fetch support is required' in str(e)
 else:raise AssertionError('Unsupported option accepted')
 assert child.call_count==1 and child.call_args.kwargs['env']['GIT_NO_LAZY_FETCH']=='1' and child.call_args.args[0][1]=='--no-lazy-fetch' and not list(dest.iterdir())
report={'status':'PASS','runner_sha256':sha(runner.read_bytes()),'positive52_reused_author_raw_receipt_and_six_guarded_reads_verified':True,'positive52_not_rerun':True,'actual_git_cases':rows,'unsupported_option_mock':'PASS explicitly mocked; not real oldGit certification','environment':'All inherited GIT_* removed for disposable repos; protocol=file only; global/system config disabled; parent guard=0; seed11object IDs/content verified; no alternates','source_scope':'Only snapshot acquisition/env/error behavior changed; exact consumer pin/hash/cases unchanged','external_T12R01':'OPEN pending external recheck','physical_T12':'NOT_RUN'}
(out/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
