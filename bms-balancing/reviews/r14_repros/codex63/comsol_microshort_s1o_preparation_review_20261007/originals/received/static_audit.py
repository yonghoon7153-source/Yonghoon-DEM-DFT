"""New data-only S1-O static verifier. AST parse does NOT execute candidate code."""
import pathlib,json,ast,hashlib,re,datetime
R=pathlib.Path(__file__).resolve().parent
def ident(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
checks=[]
def check(name,condition):
 checks.append(dict(name=name,passed=bool(condition)))
 if not condition:raise ValueError('STATIC_CHECK_FAILED:'+name)
index={}
for name in ['consumer.py.inactive.txt','control.py.inactive.txt']:
 p=R/'candidate'/name; tree=ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
 index[p.relative_to(R).as_posix()]={n.name:n.lineno for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.ClassDef))}
 check('AST_PARSE:'+name,True)
 check('NO_NATIVE_IMPORT:'+name,not any(isinstance(n,ast.Import) and any(x.name in ('subprocess','ctypes') for x in n.names) for n in ast.walk(tree)))
 check('INACTIVE_TERMINAL_GUARD:'+name,'__main__' in p.read_text(encoding='utf-8-sig'))
p=R/'candidate/Parent.ps1.inactive.txt';txt=p.read_text(encoding='utf-8-sig')
index[p.relative_to(R).as_posix()]={m.group(1):txt[:m.start()].count('\n')+1 for m in re.finditer(r'^function (\w+)',txt,re.M)}
check('POWERSHELL_HAS_NO_NATIVE_START','Start-Process ' not in txt and 'S1O_OFFLINE_ONLY_NO_EXECUTABLE_PARENT_ENTRYPOINT' in txt)
for p in sorted((R/'contracts').glob('*.json')):
 j=json.loads(p.read_bytes());check('JSON_PARSE:'+p.name,True)
check('BINDING_NATIVE_FALSE',json.loads((R/'contracts/EXECUTION_BINDING.json').read_bytes())['native_ready'] is False)
binding=json.loads((R/'contracts/EXECUTION_BINDING.json').read_bytes())
check('RESOURCE_CONTRACT_HASH_LINK',ident(R/'contracts/RESOURCE_CONTRACT.json')['sha256']==binding['unit']['resource_contract_sha256'])
policy=json.loads((R/'contracts/POLICY_VARIANTS.json').read_bytes())
from decimal import Decimal
for key,n in [('dense_0_120',1337),('sparse_0_120',255),('sparse_0_3600',401)]:
 v=policy['request_vectors'][key]['tokens_s']; nums=[Decimal(x) for x in v]
 check('REQUEST_VECTOR:'+key,len(v)==n and len(set(nums))==n and nums==sorted(nums) and nums[0]==0)
check('P_COMMON_SUBSET',set(policy['request_vectors']['sparse_0_120']['tokens_s'])<=set(policy['request_vectors']['dense_0_120']['tokens_s']))
variants=json.loads((R/'VARIANT_STATIC_RESULT.json').read_bytes())
base=(R/'reference/s0/candidate/MicroshortS1RestCandidate.java.inactive.txt').read_bytes()
for v in variants['variants']:
 p=R/v['path'];check('VARIANT_SHA:'+v['variant'],ident(p)['sha256']==v['sha256'])
 t=p.read_bytes().decode('utf-8')
 for patch in reversed(v['patches']):
  check('REVERSE_UNIQUE:'+v['variant']+':'+patch['after'][:35],t.count(patch['after'])==1)
  t=t.replace(patch['after'],patch['before'],1)
 check('FULL_JAVA_REVERSE:'+v['variant'],t.encode('utf-8')==base)
 check('JAVA_DENY_NO_RUNALL:'+v['variant'],'.runAll(' not in p.read_text(encoding='utf-8') and 'denyS0Execution();' in p.read_text(encoding='utf-8'))
plan=json.loads((R/'VALIDATION_PLAN.json').read_bytes())
check('VALIDATION_UNIQUE_IDS',len({x['id'] for x in plan['cases']})==plan['unique_cases']==len(plan['cases']))
for c in plan['cases']:
 check('PLANNED_ACTUAL_FUNCTION:'+c['id'],all(n in index[c['source']] for n in c['target_functions']))
for r in plan['source_bindings']:
 check('VALIDATION_CURRENT_SOURCE:'+pathlib.Path(r['path']).name,ident(pathlib.Path(r['path']))==r)
originals=json.loads((R/'SELECTED_ORIGINALS_BEFORE.json').read_bytes())
after=[ident(pathlib.Path(x['path'])) for x in originals['files']]
check('SAME_SELECTED_ORIGINAL_SET_AND_BYTES',after==originals['files'])
inputs=json.loads((R/'INPUTS_BEFORE.json').read_bytes())['inputs']
check('ATTACHMENTS_UNCHANGED',[ident(pathlib.Path(x['path'])) for x in inputs]==inputs)
if (R/'CODE_MANIFEST.json').exists():
 manifest=json.loads((R/'CODE_MANIFEST.json').read_bytes())
 check('CODE_MANIFEST_INACTIVE',manifest['native_ready'] is False and manifest['approved'] is False and manifest['usable'] is False)
 for f in manifest['files']:
  actual=ident(R/f['path'])
  check('FINAL_CODE_MANIFEST:'+f['path'],actual['bytes']==f['bytes'] and actual['sha256']==f['sha256'])
 check('CODE_MANIFEST_NO_SELF_HASH',not any(f['path']=='CODE_MANIFEST.json' for f in manifest['files']))
 check('DECISION_CODE_HASH',json.loads((R/'DECISION.json').read_bytes())['code_manifest_sha256']==ident(R/'CODE_MANIFEST.json')['sha256'])
(R/'SELECTED_ORIGINALS_AFTER.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),files=after,inputs=inputs,same_set=True,scope='selected originals only; no MPH/prefs remeasurement'),indent=2),encoding='utf-8')
(R/'SOURCE_INDEX.json').write_text(json.dumps(index,indent=2),encoding='utf-8')
(R/'STATIC_AUDIT.json').write_text(json.dumps(dict(kind='STATIC_TEXT_JSON_AST_HASH_NOT_FUNCTIONAL_TEST',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,all_static_checks_passed=all(x['passed'] for x in checks),candidate_import=0,synthetic_tests=0,COMSOL=0,JVM=0,compile=0),indent=2),encoding='utf-8')
print(json.dumps(dict(static_checks=len(checks),passed=True,candidate_execution=0,validation_cases_proposed=plan['unique_cases'])))
