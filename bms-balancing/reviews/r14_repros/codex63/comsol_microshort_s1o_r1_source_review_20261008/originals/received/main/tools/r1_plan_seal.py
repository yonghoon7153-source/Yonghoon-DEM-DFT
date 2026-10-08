"""New static plan/manifest inspector and writer, no candidate imports/calls."""
from pathlib import Path
from decimal import Decimal
import json,hashlib,collections,datetime
OUT=Path(__file__).resolve().parents[1];BASE=OUT.parent/'microshort_s1o_20261007_133011'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x): (OUT/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def identity(p):
    b=p.read_bytes();return {'path':p.relative_to(OUT).as_posix(),'bytes':len(b),'sha256':sha(b)}
oldpath=OUT/'VALIDATION_PLAN.json';dest=OUT/'reference/ORIGINAL_VALIDATION_PLAN.json'
assert oldpath.resolve().is_relative_to(OUT.resolve()) and dest.resolve().is_relative_to(OUT.resolve())
assert oldpath.exists() and not dest.exists()
assert oldpath.read_bytes()==(BASE/'VALIDATION_PLAN.json').read_bytes()
oldpath.rename(dest) # move only this new owned copy; original is untouched
p=read(OUT/'VALIDATION_PLAN_R1.json');old=read(dest);cases=p['cases']
checks=[]
def check(n,v):
    checks.append({'name':n,'pass':bool(v)})
    if not v: raise ValueError('PLAN_STATIC_FAILED:'+n)
check('130_unique_IDs_inputs',len(cases)==len({r['id'] for r in cases})==len({r['input_id'] for r in cases})==130 and sum(r['input_count'] for r in cases)==130)
check('8_groups',len({r['group'] for r in cases})==p['groups']==8)
counts=collections.Counter('Python' if r['engine']=='Python' else 'PowerShell5.1' for r in cases)
check('engine_counts',dict(counts)==p['counts']=={'Python':99,'PowerShell5.1':31})
oldids={r['id'] for r in old['cases']};mapping=p['old98_mapping']
check('all_old98_mapped',len(oldids)==len(mapping)==98 and {r['old_id'] for r in mapping}==oldids)
check('32_new_IDs',len({r['id'] for r in cases}-oldids)==32)
check('all_not_run',p['approved'] is False and p['native_ready'] is False and p['functional_validation']=='NOT_RUN' and all(r['execution_status']=='NOT_RUN' for r in cases))
check('budget1860_sum',sum(v for k,v in p['budgets_s'].items() if k!='overall')==p['budgets_s']['overall']==1860)
for row in p['source_bindings']:
    raw=(OUT/row['relative_path']).read_bytes()
    check('source_pin:'+row['relative_path'],len(raw)==row['bytes'] and sha(raw)==row['sha256'])
for row in p['extraction_spans']:
    lines=(OUT/row['source']).read_text(encoding='utf-8').splitlines()
    span='\n'.join(lines[row['start_line']-1:row['end_line']]).encode()
    check('span:'+row['source']+':'+row['name'],sha(span)==row['sha256'])
policy=read(OUT/'contracts/POLICY_VARIANTS.json')
vec=policy['request_vectors']['sparse_0_120']['tokens_s']
check('protective_prefix90_count249',len(vec)==255 and len([t for t in vec if Decimal(t)<=90])==249)
ids={r['id']:r for r in cases}
for n in ('CHARGE_R112','CHARGE_R113'):
    check('unchanged_deadband_fixture_label:'+n,ids[n]['pinned_scalar_fixture']['production_deadband_C_m2']=='0.0002')
check('real_Python_to_PS_routes',all(n in p['fixture_connections'][k] for k,n in [('normal','CHARGE01'),('protective','CHARGE_R109'),('protective','PARENT03')]))
save('PLAN_STATIC_AUDIT.json',{'status':'PASS_STATIC_ONLY','checks':checks,'count':len(checks),'cases':130,'inputs':130,'groups':8,'counts':dict(counts),'executed_cases':0,'static_only_N4_not_counted_as_functional':1})

oldm=read(BASE/'CODE_MANIFEST.json')
paths=[r['path'] for r in oldm['files'] if r['path']!='VALIDATION_PLAN.json']+['VALIDATION_PLAN_R1.json']
manifest={'schema':'S1O_CODE_MANIFEST_R1','approved':False,'usable':False,'native_ready':False,'r1_status':'OFFLINE_CORRECTED_STATIC_ONLY_FUNCTIONAL_VALIDATION_NOT_RUN','parent_manifest_sha256':sha((BASE/'CODE_MANIFEST.json').read_bytes()),'current_validation_plan':'VALIDATION_PLAN_R1.json','historical_validation_plan':'reference/ORIGINAL_VALIDATION_PLAN.json','self_excluded':True,'files':[identity(OUT/n) for n in paths]}
save('CODE_MANIFEST.json',manifest)
save('PREPARATION_TOOL_ENGINE_IDENTITIES.json',{'scope':'Read-only byte identities for tools used in this authorized static preparation; not native or functional compatibility evidence','tools':[{'path':str(q),'bytes':q.stat().st_size,'sha256':sha(q.read_bytes())} for q in [Path('C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'),Path('C:/Users/BML/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe')]],'candidate_executed':False,'COMSOL':0,'JVM':0})
print(json.dumps({'kind':'R1_PLAN_AND_CODE_SEAL','plan_checks':len(checks),'functional_cases':130,'executed_cases':0,'code_files':len(paths),'code_manifest_sha256':sha((OUT/'CODE_MANIFEST.json').read_bytes())}))
