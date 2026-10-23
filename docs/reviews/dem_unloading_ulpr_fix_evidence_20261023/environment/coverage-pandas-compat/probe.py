import argparse, hashlib, importlib.util, json, pathlib, subprocess, sys, types
ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--out',required=True);ap.add_argument('--overlay');a=ap.parse_args()
if a.overlay: sys.path.insert(0,a.overlay)
r=pathlib.Path(a.repo);o=pathlib.Path(a.out);o.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(r/'scripts'))
import numpy as np,pandas as pd
import coverage_physics_vs_hertzian as current
src=r/'scripts/coverage_physics_vs_hertzian.py'
historical=subprocess.check_output(['git','show','e72067854:scripts/coverage_physics_vs_hertzian.py'],cwd=r)
old=types.ModuleType('coverage_old');old.__file__=str(src);exec(compile(historical,str(src),'exec'),old.__dict__)
result={'versions':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__},'pinned':current._PIN_LEGACY,'source':{},'runs':{}}
for name in ['scripts/coverage_physics_vs_hertzian.py','scripts/plastic_coverage.py','scripts/dem_analysis_core.py']:
 data=(r/name).read_bytes();head=subprocess.check_output(['git','show','HEAD:'+name],cwd=r)
 result['source'][name]={'worktree_sha256':hashlib.sha256(data).hexdigest(),'head_sha256':hashlib.sha256(head).hexdigest(),'same':data==head}
for label,mod in [('current',current),('pre_v2',old)]:
 cd,tm,sc=current._selftest_fixture(o/label)
 summ=mod.compute_case(cd.name,cd,tm,scale=sc,write_csv=True,update_metrics=True)
 (o/(label+'-summary.json')).write_text(json.dumps(summ,sort_keys=True,indent=2)+'\n')
 dg=current._legacy_digests(cd,summ)
 result['runs'][label]={'digests':dg,'mismatched':[k for k in current._PIN_LEGACY if current._PIN_LEGACY[k]!=dg[k]],'summary':summ}
result['current_equals_pre_v2']=result['runs']['current']['digests']==result['runs']['pre_v2']['digests']
(o/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
