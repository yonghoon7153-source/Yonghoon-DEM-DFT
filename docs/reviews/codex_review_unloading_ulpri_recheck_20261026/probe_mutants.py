"""Kill four concrete guard reversions with the independent matrix fixtures."""
from pathlib import Path
import sys,hashlib,json,shutil,subprocess,os
R=Path(__file__).resolve().parent;K=R/'snapshot/docs/data/ps45_unload_20261009';O=R/'evidence/mutants';O.mkdir(exist_ok=False)
text=(K/'ul_reader.py').read_text(encoding='utf8');matrix=json.loads((R/'evidence/matrix_v2/result.json').read_text(encoding='utf8'))
mods=[('raw_scan_removed','    if os.path.isfile(event_path):','    if False:','event_U+2028_prefix_single'),('auth_poison_removed','if pr or marker_pr else _resume_auth','if pr else _resume_auth','event_U+00A0_suffix_coexist'),('manifest_guard_removed',"if any(c in ln for c in '\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'):",'if False:','manifest_U+2028_hidden'),('nel_omitted',"'\\v\\f\\x1c\\x1d\\x1e\\u0085\\u2028\\u2029'","'\\v\\f\\x1c\\x1d\\x1e\\u2028\\u2029'",'manifest_U+0085_hidden')]
results=[]
code="import sys,json;sys.dont_write_bytecode=True;sys.path.insert(0,sys.argv[1]);import ul_reader as u;r=u.read_run(sys.argv[2]);print(json.dumps({k:r[k] for k in ['resume_auth','n_superseded_rows','problems']}))"
for i,(name,before,after,label) in enumerate(mods):
 root=O/f'm{i}';kit=root/'kit';shutil.copytree(K,kit,ignore=shutil.ignore_patterns('__pycache__','*.pyc'));assert text.count(before)==1
 (kit/'ul_reader.py').write_bytes(text.replace(before,after,1).encode('utf8'))
 rec=next(x for x in matrix['cases'] if x['label']==label);assert rec['pass'];fixture=R/'evidence/matrix_v2'/f'c{rec["case"]:03}';run=root/'case';shutil.copytree(fixture,run)
 arm=run/'ps_7_3_r45/UT';p=subprocess.run([sys.executable,'-I','-X','utf8','-B','-c',code,str(kit),str(arm)],capture_output=True,timeout=30);assert p.returncode==0,p.stderr
 observed=json.loads(p.stdout);cp=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(kit/'ul_reader.py'),'arm',str(run),'ps_7_3_r45','UT'],capture_output=True,timeout=30);(root/'cli.log').write_bytes(cp.stdout+cp.stderr);v=json.loads((arm/'arm_verdict.json').read_text(encoding='utf8'))
 hashes={str(p.relative_to(run)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [arm/f'ul_{s}.csv' for s in ('events','windows','steps')]+[arm/'run_manifest.txt',*sorted((arm/'restart').glob('state*.in'))]}
 refused=not observed['resume_auth'] and observed['n_superseded_rows']==0 and bool(observed['problems']) and v['primary_status']=='UNIDENTIFIED' and v['rho_pct'] is None and not v['rank_eligible']
 results.append(dict(mutation=name,fixture_label=label,reader_sha256=hashlib.sha256((kit/'ul_reader.py').read_bytes()).hexdigest(),read_run=observed,primary=v['primary_status'],rho=v['rho_pct'],rank=v['rank_eligible'],rc=cp.returncode,inputs_unchanged=hashes==rec['input_hashes'],detected=not refused and cp.returncode==0 and hashes==rec['input_hashes']))
print(json.dumps({'count':len(results),'detected':sum(x['detected'] for x in results)}));(O/'result.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
