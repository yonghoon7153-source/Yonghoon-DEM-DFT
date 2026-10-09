"""Author-owned static-only verifier: bytes/JSON/AST/diff, not function tests."""
from pathlib import Path
import ast,json,hashlib,difflib
ROOT=Path(__file__).resolve().parents[1]
def ident(p):
 b=p.read_bytes();return {'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
def ck(name,ok,detail=None):
 checks.append({'check':name,'matched':bool(ok),'detail':detail})
 if not ok:
  (ROOT/'STATIC_FIRST_ERROR.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
  raise SystemExit('STATIC_FIRST_ERROR:'+name)
mf=json.loads((ROOT/'CODE_MANIFEST.json').read_bytes())
ck('inactive_manifest_flags',all(mf[k] is False for k in ('approved','usable','native_ready')))
for e in mf['files']:
 got=ident(ROOT/e['path']);ck('new_sealed_file:'+e['path'],got['bytes']==e['bytes'] and got['sha256']==e['sha256'])
before=json.loads((ROOT/'evidence/SELECTED_SOURCES_BEFORE.json').read_bytes())
after=[]
for e in before:
 got=ident(Path(e['path']));after.append(got);ck('preservation:'+e['path'],got==e)
with (ROOT/'evidence/SELECTED_SOURCES_AFTER_STATIC.json').open('x',encoding='utf-8') as f:json.dump(after,f,indent=2)
source=ROOT.parents[1]/'outputs/microshort_s1o_r1_20261008'
old=(source/'candidate/variants/P0.java.inactive.txt').read_bytes()
new=(ROOT/'candidate/P0.connection.java.inactive.txt').read_bytes()
fragment=(ROOT/'candidate/InstalledReadback.fragment.java.inactive.txt').read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
ck('java_exact_reverse',new.replace(fragment+b'\r\n',b'',1)==old)
ck('java_insertion_single',new.count(fragment)==1)
ck('java_denial_retained',new.count(b'denyS0Execution();')==old.count(b'denyS0Execution();'))
ck('java_no_runAll_call_added',new.count(b'.runAll(')==old.count(b'.runAll(')==0)
expected=''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile=str(source/'candidate/variants/P0.java.inactive.txt'),tofile=str(ROOT/'candidate/P0.connection.java.inactive.txt')))
# Different platform separators in diff headers are inspected separately; body must match.
actual=(ROOT/'candidate/P0.connection.diff.txt').read_bytes().decode()
ck('java_diff_body',actual.splitlines()[2:]==expected.splitlines()[2:])
functions=[]
for name in ('raw_connection.py.inactive.txt','resource_connection.py.inactive.txt'):
 p=ROOT/'candidate'/name;b=p.read_bytes();text=b.decode('utf-8');tree=ast.parse(text,filename=str(p))
 ck('ast_parse:'+name,True,'No compile/eval/exec/import of candidate')
 forbidden={'ctypes','subprocess','os','socket','requests','importlib','win32api','psutil'}
 imported={n.names[0].name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import)}|{n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module}
 ck('no_native_io_import:'+name,not imported&forbidden,sorted(imported))
 bad=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('eval','exec','compile','open','__import__','input')]
 ck('no_io_dynamic_calls:'+name,not bad)
 for n in ast.walk(tree):
  if isinstance(n,(ast.FunctionDef,ast.ClassDef)):
   span='\n'.join(text.splitlines()[n.lineno-1:n.end_lineno]).encode()
   functions.append({'file':'candidate/'+name,'name':n.name,'start_line':n.lineno,'end_line':n.end_lineno,'span_rule':'UTF8 LF between lines, no final LF; separate full raw-file seal','span_sha256':hashlib.sha256(span).hexdigest()})
 diff=''.join(difflib.unified_diff([],text.splitlines(True),fromfile='/dev/null',tofile='candidate/'+name))
 ck('new_file_diff:'+name,(ROOT/'candidate'/(name+'.diff.txt')).read_text(encoding='utf-8')==diff)
plan=json.loads((ROOT/'LIMITED_VALIDATION_PLAN.json').read_bytes());cases=plan['cases']
ck('plan_case_ids_unique',len(cases)==len({c['id'] for c in cases})==50)
ck('plan_groups',len({c['group'] for c in cases})==plan['groups']==8)
ck('plan_engines',plan['counts']=={'Python':44,'Java_helper':6})
ck('plan_budget',sum(v for k,v in plan['budget_proposal_s'].items() if k!='total')==plan['budget_proposal_s']['total']==1350)
ck('plan_expected_reach',all(c['reached_function_required'] and c['expected_reason_or_result'] and not c['unexpected_exception_is_pass'] for c in cases))
ck('plan_positive_controls_exist',all(c['positive_control'] in {r['id'] for r in cases} for c in cases))
for e in plan['source_pins']:
 ck('validation_source_pin:'+e['path'],ident(Path(e['path']))==e)
for e in plan['engine_pins_current_file_reads_no_version_invocation'].values():
 ck('validation_engine_pin:'+e['path'],ident(Path(e['path']))==e)
ck('fixture_not_created',not Path(plan['fixture_proposed_only_not_created']).exists())
ck('no_runtime_authorization_dirs',not any(p.name in ('future_run_001','future_parent_001','future_authorizations') for p in ROOT.rglob('*')))
total=sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())
ck('folder_under_50MiB_prepackage',total<=52428800,{'bytes':total})
with (ROOT/'FUNCTION_SPANS.json').open('x',encoding='utf-8') as f:json.dump(functions,f,indent=2)
result={'status':'STATIC_CONSISTENCY_MATCHED_NOT_FUNCTIONAL_PASS','checks':checks,'check_count':len(checks),'candidate_function_calls':0,'candidate_imports':0,'tests':0,'COMSOL_JVM_compile':0,'native_ready':False}
with (ROOT/'STATIC_CHECKS.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps({'static_checks':len(checks),'all_matched':True,'functions_indexed':len(functions),'selected_sources_unchanged':len(after),'tests_run':0,'native_ready':False}))
