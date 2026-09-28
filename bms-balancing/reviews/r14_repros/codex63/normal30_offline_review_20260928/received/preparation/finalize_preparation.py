"""Static seal/package only. Never import or execute candidate files."""
from pathlib import Path
import ast, csv, difflib, hashlib, json, re, stat, time, zipfile
from datetime import datetime, timezone
from decimal import Decimal as D
R=Path(__file__).resolve().parents[1];O=R.parent/'guard1198_limited_validation_R1_20260928'
def read(p):return json.loads(Path(p).read_text('utf-8-sig'))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def ref(p):
    p=Path(p)
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    return dict(path=p.as_posix(),bytes=p.stat().st_size,sha256=h)
def write(name,obj):
    (R/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False)+'\n','utf-8')
def text(p):return Path(p).read_text('utf-8-sig')
def func(s):
    lines=s.splitlines(True)
    return {v.name:''.join(lines[v.lineno-1:v.end_lineno]) for v in ast.parse(s).body if isinstance(v,ast.FunctionDef)}

m=read(R/'CODE_MANIFEST.json');oldhash=ref(R/'CODE_MANIFEST.json')['sha256']
write('preparation/INITIAL_CODE_MANIFEST.json',m)
write('preparation/INITIAL_STATIC_SOURCE_CHECKS.json',read(R/'STATIC_SOURCE_CHECKS.json'))
for r in m['files']:
    got=ref(R/r['file']);r.update(bytes=got['bytes'],sha256=got['sha256'])
write('CODE_MANIFEST.json',m);mh=ref(R/'CODE_MANIFEST.json')['sha256']
cm=read(R/'COMMAND_MAP.json');cm=json.loads(json.dumps(cm).replace(oldhash,mh));write('COMMAND_MAP.json',cm)
for p in R.glob('*.md'):
    s=text(p)
    if '__MANIFEST_SHA__' in s:p.write_text(s.replace('__MANIFEST_SHA__',mh),'utf-8')
c=read(R/'CONTRACT.json');oldc=read(O/'CONTRACT.json')

groups=[]
def group(id,engine,functions,cases):
    groups.append(dict(id=id,engine=engine,actual_sources=functions,cases=[dict(id=id+'-'+str(i+1).zfill(2),setup=a,expected=b) for i,(a,b) in enumerate(cases)]))
CP='src/diagnostic_consumer.py:';EP='src/candidate_entry.py:';PS='PARENT_COMMAND.ps1:'
group('PY01','isolated Python',[CP+'analyze',EP+'analyze'],[
 ('Complete normal30 fixture, exact437 requested times plus legal internal steps, baseline187 prefix, all required tables/axes/state','NORMAL_30S_DIAGNOSTIC_COMPLETE; entry rc0; overall/normal INCOMPLETE'),
 ('Electrolyte protection at <30, valid pair/native reason/full evidence','PROTECTED_STOP_30S_INCOMPLETE; entry rc1; never normal complete'),
 ('OCP or surface protection observed then terminal numeric range violation','termination preserved; numeric error; INCOMPLETE/rc1')])
group('PY02','isolated Python',[CP+'guard_evidence',CP+'native_stop'],[
 ('threshold1198 left in candidate data','NORMAL_THRESHOLD or THRESHOLD'),
 ('All guards0 but final29.9','DID_NOT_REACH_30'),
 ('Stored time >30','GUARD_TIME_RANGE'),
 ('Guard at30 exactly with matching stop','Protected classification, never normal'),
 ('Initial guard or earlier guard followed by more integration','INITIAL_GUARD/GUARD_BEFORE_FINAL')])
group('PY03','isolated Python',[CP+'native_stop',EP+'process_ok'],[
 ('Wrong stop reason or native stop on normal result','NATIVE_STOP_REASON/NATIVE_STOP_COUNT'),
 ('fatal in raw log despite native rc0','NATIVE_FATAL or NATIVE_FATAL_RC0'),
 ('Extra out step after stop/end or missing sequential step','INTEGRATION_AFTER_TERMINATION/NATIVE_STORED_STEP_COUNT'),
 ('Producer failure/absent completion/output failure','PRODUCER_OUTPUT_FAILURE')])
group('PY04','isolated Python',[CP+'coverage',CP+'numeric'],[
 ('Missing one old0–5 requested time','STRICT_REQUEST_TIME_MISSING'),
 ('Missing one required >5 requested time','STRICT_REQUEST_TIME_MISSING'),
 ('Empty or t0-only common times','Strict missing or EMPTY_OR_ZERO_ONLY_COMMON; no zero-delta PASS'),
 ('Stop time exists in baseline but is beyond pre-stop comparison prefix','Full intersection includes stop; common comparison excludes it')])
group('PY05','isolated Python',[CP+'runtime_evidence',CP+'binding_evidence'],[
 ('Readback threshold1198 or wrong storage/selection binding','GUARD_BINDING_VALUE/COUPLING_BINDING'),
 ('tlist unchanged5 or altered cap/rtol','RUNTIME_TLIST/RUNTIME_SETTING'),
 ('Duplicate runtime key or absent table','RUNTIME_SETTINGS_SCHEMA or preserved file error')])
group('PY06','isolated Python',[CP+'numeric',CP+'profile',CP+'units_evidence'],[
 ('NaN/Infinity in new late interval','NONFINITE'),
 ('Wrong unit/domain/coordinate or241 count','UNIT_STAGE/PROFILE_COORD_DOMAIN/PROFILE_COUNT'),
 ('Initial Li components changed but total preserved','INITIAL_LI_COMPONENT'),
 ('Voltage/surface comparison or Li drift/identity exceeds retained limits','SAMPLE_TOLERANCE/LI_DRIFT/VOLTAGE_IDENTITY')])
group('PY07','isolated Python',[CP+'late_summary',CP+'numeric'],[
 ('Normal30 complete late interval endpoints/extrema','OBSERVED; count/range correct; no baseline-equivalence claim'),
 ('Protective stop before5','NOT_REACHED; no fabricated late interval')])
group('PY08','isolated Python',[CP+'analyze',EP+'analyze',EP+'incomplete_result'],[
 ('Early binding/guard/CSV extraction failure routed through real entry','Original reason; schema present; rc1; no KeyError'),
 ('Analysis output save fails after a primary numeric error','Primary plus recording error preserved; rc1'),
 ('Native state error/cleanup/policy/preservation INCOMPLETE','No normal or acceptable protected result'),
 ('Analysis900 or overall5100 overrun','FINAL_BUDGET; rc1')])
group('PY09','isolated Python',[EP+'permission',EP+'execute',EP+'seal'],[
 ('1198 auth or wrong manifest/run/approval path/commands','Reject before adapter/native call'),
 ('Wrong cwd/source/Python options or existingrun','Reject before gate/Job; native count0'),
 ('Future release lacks exact validation evidence/prefs identity','Reject; no real authorization created')])
group('J01','inert Java helper stub',['src/Normal30Candidate.java:checkShape'],[
 ('Extracted actual helper accepts complete0..30 valid matrix','PASS'),
 ('Legal >5 but <=30 stored times','PASS'),
 ('Time >30','TIME_ORDER')])
group('J02','inert Java helper stub',['src/Normal30Candidate.java:checkShape'],[
 ('Duplicate/decreasing time or missing t0','Reject correct shape/time reason'),
 ('Nonfinite row or unequal width','Reject nonfinite/shape reason')])
group('J03','static binding inside Java validation preparation',['src/Normal30Candidate.java:threshold/tlist/log literals'],[
 ('Extracted helper bytes and candidate SHA mismatch','Stop before compile'),
 ('187 original tokens /250 new tokens /readback0 /runAll1 assertions','Static binding only, not model execution')])
group('PS01','Windows PowerShell5.1',[PS+'GDecision'],[
 ('Actual Python fixture normal result + typed native0/analysis0','AWAITING_30S_LIMITED_EXTERNAL_ACCEPTANCE'),
 ('Actual Python fixture protected result + native0/analysis1/invocation false','PROTECTED_STOP_30S_INCOMPLETE'),
 ('rc1 with normal label or rc0 with protected label','INCOMPLETE')])
group('PS02','Windows PowerShell5.1',[PS+'GDecision'],[
 ('Summary only /missing each result axis /empty required structure','INCOMPLETE for each sealed subfixture'),
 ('Wrong run/hash or missing table manifest/runtime evidence','INCOMPLETE'),
 ('Wrong terminal30/pair/native reason or missing requested coverage','INCOMPLETE')])
group('PS03','Windows PowerShell5.1',[PS+'GDecision'],[
 ('Nonfinite metric /limit exceeded /missing Li component or late summary','INCOMPLETE'),
 ('Return rc null/stale7/exception/new_error or not returned','INCOMPLETE; no real child process required'),
 ('Analysis >900 or overall >5100','INCOMPLETE')])
group('PS04','Windows PowerShell5.1',[PS+'outer catch/finally exact source extent'],[
 ('Inject body failure after local decision','Final limited INCOMPLETE; original error preserved'),
 ('Final record IO failure /transcript failure','FINAL_RECORD_ERROR; no accepted boundary'),
 ('Final snapshot/delivery budget exceeded','within_limits false; final limited INCOMPLETE')])
group('PS05','Windows PowerShell5.1',[PS+'outer finally exact source extent',PS+'BSave'],[
 ('Valid completion with inert transcript/reference adapters','Boundary says SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT; raw_host_rc null'),
 ('Missing captured final return/prompt evidence at external acceptance step','External acceptance incomplete; never synthesize OSrc0')])
plan={'status':'PROPOSED_NOT_EXECUTED','manifest_sha256':mh,'logical_groups':len(groups),'listed_case_specs':sum(len(g['cases']) for g in groups),'assertion_count':None,
      'case_count_note':'Listed cases may contain enumerated mutation subfixtures; expand and seal exact engine fixtures before first test. No claim that listed cases are passed assertions.',
      'sessions':{'Python':{'max':1,'seconds':120},'Java_compile':{'max':1,'seconds':90},'Java_stub_JVM':{'max':1,'seconds':60},'Windows_PowerShell_5_1':{'max':1,'seconds':90}},
      'budget_seconds':{'harness_and_seal':600,'Python':120,'Java_compile':90,'Java_stub_JVM':60,'PS51':90,'preserve_package':300,'incomplete_closeout':120,'overall':1380},
      'before_import':'Block COMSOL, native transport, console/token and Job entry points with inert adapters before target load. Execute actual final consumer/entry/PS branch, no substitute classifier.',
      'Java_scope':'Only exact checkShape helper and minimal inert dependencies; no whole model class or COMSOL jars/model load. Compiler/JDK identities from prior accepted stub record, read then seal.',
      'PowerShell_scope':'Extract exact GDecision and required finalization extent into fixture scope. Stub console/transcript/OS-facing adapters. No native children, input, Job or policy calls. BInvoke unchanged tests reused.',
      'first_failure':'Preserve raw first failure and stop all later sessions. No fixes/retries/engine fallback after testing begins.',
      'groups':groups}
write('LIMITED_VALIDATION_PLAN.json',plan)
field={'document_kind':'FIELD_SPECIFICATION_NOT_AUTHORIZATION','approved':False,'usable':False,'run_id':c['run_id'],'code_manifest_sha256':mh,
       'future_approval_path':c['approval_path'],'future_release_path':c['release_path'],
       'activation_requires':['separate accepted changed-branch validation bound to unchanged manifest','actual user native30 decision','current approved default prefs identity','current permission/path review using accepted route; no policy change'],
       'required_future_fields':{'approved':'boolean true only after actual user authorization','native30_one_shot':'boolean true only for separately approved one native30 attempt','allow_policy_changes':False,'effective_policy_unverified_accepted':'explicit user decision','commands':c['commands'],'budgets_seconds':c['budgets_seconds'],'user_decision':'exact existing original statement record path/bytes/SHA, not created now','validation_release':'path/bytes/SHA of separate accepted release, not created now','default_prefs_identity':'path/bytes/SHA of exact current user-approved file; not guessed'},
       'future_release_required':{'changed_branch_validation':'PASS only from actual accepted test results','native_permission_route_reviewed':'explicit assessment, not native-success guarantee','manifest_bytes_unchanged_since_validation':True,'validation_evidence':'nonempty pinned source/engine/result records'}}
write('NATIVE_APPROVAL_FIELD_SPEC.json',field)

diff=[]
for a,b in [('src/Guard1198Candidate.java','src/Normal30Candidate.java'),('src/trigger_consumer.py','src/diagnostic_consumer.py'),('src/candidate_entry.py','src/candidate_entry.py'),('PARENT_COMMAND.ps1','PARENT_COMMAND.ps1'),('CONTRACT.json','CONTRACT.json')]:
    diff.extend(difflib.unified_diff(text(O/a).splitlines(True),text(R/b).splitlines(True),fromfile='accepted1198/'+a,tofile='candidate30/'+b))
(R/'SOURCE_DIFF.patch').write_text(''.join(diff),'utf-8')

# Independent final static audit; no production import/function calls.
checks=[]
def ok(name,condition):
    if not condition:raise AssertionError(name)
    checks.append(name)
for r in m['files']:
    got=ref(R/r['file']);ok('seal '+r['file'],got['bytes']==r['bytes'] and got['sha256']==r['sha256'])
java=(R/'src/Normal30Candidate.java').read_bytes();inverse=java
for p in reversed(read(R/'JAVA_ALLOWED_REPLACEMENTS.json')):inverse=inverse.replace(p['after'].encode(),p['before'].encode())
ok('whole Java inverse bytes',inverse==(O/'src/Guard1198Candidate.java').read_bytes())
ok('original requested prefix',c['requested_times_s'][:187]==oldc['requested_times_s'])
ok('exact extension',list(map(D,c['requested_times_s'][187:]))==[D(i)/10 for i in range(51,301)])
ok('Java tlist to contract',re.findall(r'set\("tlist","([^"]+)"\)',java.decode())==[' '.join(c['requested_times_s'])])
ok('threshold shape and readback',b'"0[mol/m^3]"' in java and b'evaluate("ce_stop_threshold")!=0.0' in java and b'values[0][i]>30||' in java)
ok('unchanged scientific/external inputs',all(c[k]==oldc[k] for k in ('coordinates','limits','baseline_files','external_source_pins','python','legacy_gate','legacy_contract','legacy_inner_manifest','native_executable_pins','cwd')))
for p in ('src/candidate_entry.py','src/diagnostic_consumer.py'):ast.parse(text(R/p));checks.append('Python AST syntax only '+p)
entry=text(R/'src/candidate_entry.py');consumer=text(R/'src/diagnostic_consumer.py');parent=text(R/'PARENT_COMMAND.ps1')
ok('no trigger success reused',all('TRIGGER_AND_SAMPLED_DATA_ACCEPTABLE' not in s and 'TEST_TRIGGER_DETECTED' not in s for s in (entry,consumer,parent)))
ok('new auth field',all('native30_one_shot' in s and 'native1198_one_shot' not in s for s in (entry,parent)))
ok('entry source and result connection',"src/diagnostic_consumer.py" in entry and "DIAGNOSTIC_RESULT.json" in entry and 'DIAGNOSTIC_RESULT.json' in parent)
ok('fixed parent budget','5100' in parent and '900' in parent and '3000' not in parent)
ok('normal and protected rc cases',"NORMAL_30S_DIAGNOSTIC_COMPLETE" in parent and 'PROTECTED_STOP_30S_INCOMPLETE' in parent and '$Analysis.native_rc -ne 1' in parent)
ok('no fake raw host rc',"raw_host_rc=$null" in parent and 'SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT' in parent)
ok('entry incomplete schema identical',func(entry)['incomplete_result']==func(consumer)['incomplete_result'])
for n in ('BSave','BInvoke'):
    def psbody(s,name):return s[s.index('function '+name+'('):s.index('\nfunction ',s.index('function '+name+'(')+1)]
    ok('unchanged PS '+n,psbody(parent,n)==psbody(text(O/'PARENT_COMMAND.ps1'),n))
ok('budget sum',sum(v for k,v in c['budgets_seconds'].items() if k!='overall')==5100)
ok('RAM floor absent',c['resource_proposal']['available_ram_floor_gib'] is None and not c['resource_proposal']['new_working_set_monitor_implemented'])
ok('source inactive',all(x['approved'] is False and x['usable'] is False for x in (c,m,field)))
for p in cm['not_created_paths']:ok('absent '+p,not Path(p).exists())
for key in ('execute','analyze'):
    argv=cm[key]['argv'];ok('mapped '+key,argv==['-I','-S','-B','-X','utf8',(R/'src/candidate_entry.py').as_posix(),key,'--approval',c['approval_path'],'--manifest-sha',mh])
for key in ('compile','batch'):ok('native map '+key,cm['native'][key]['argv']==c['commands'][key] and cm['native'][key]['cwd']==c['run_root'])
before=read(R/'PRESERVATION_BEFORE.json');after=[ref(x['path']) for x in before]
ok('selected original preservation',after==before);write('PRESERVATION_AFTER.json',after)
write('FINAL_STATIC_CHECKS.json',{'status':'STATIC_ONLY_NOT_FUNCTIONAL_PASS','manifest_sha256':mh,'checks':checks,'check_count':len(checks),'scope':'Own JSON/hash/text/AST data checks. No candidate execution, Java compile/JVM/COMSOL/PS candidate parser/native/console tests.',
 'proposed_validation_logical_groups':len(groups),'proposed_listed_case_specs':plan['listed_case_specs'],'elapsed_comment':'First draft seal is retained in preparation/INITIAL_*; final catch/budget classification correction was static-only before any functional tests.'})
ss=read(R/'STATIC_SOURCE_CHECKS.json');ss['manifest_sha256']=mh;ss['final_parent_error_boundary_tightened']=True;write('STATIC_SOURCE_CHECKS.json',ss)
write('TOOL_NOTES.json',{'data_read_limitations':[{'event':'Read of runtime_settings.csv failed because actual table is axes_runtime_settings.csv','handling':'Read actual file name from producer source; no native or analysis re-run.'},{'event':'Broad AGENTS.md search encountered unrelated access-denied work cache directories','handling':'No permissions changed or access bypass. Target source and working paths remained accessible.'}],'functional_test_failure':None,'candidate_or_native_runs':0})
start=read(R/'START.json');now=datetime.now(timezone.utc)
elapsed=(now-datetime.fromisoformat(start['start_utc'].replace('Z','+00:00'))).total_seconds()
write('TIME_ACCOUNTING.json',{'start_record':'START.json','pre_package_utc':now.isoformat(),'elapsed_wall_seconds_from_new_start':elapsed,'clock_note':'UTC wall difference for preparation; not native physical time or a claim of per-phase monotonic accounting. START also retains original Stopwatch ticks.','budget':'Latest directive supplied no numerical preparation cap; future validation/native budgets are proposals only.','native_physical_seconds':0,'COMSOL_compile':0,'JVM':0,'candidate_execution':0})
write('DELIVERY_STATUS.json',{'status':'OFFLINE_PREPARATION_COMPLETE_VALIDATION_NOT_RUN','manifest_sha256':mh,'approved':False,'usable':False,'next':'Review changed candidate and approve only limited validation; native30 requires later separate approval.','preserved_selected_count':len(before),'candidate_functional_runs':0,'native_runs':0})

# Exact package set is established once, after all source and documentation files.
zname='COMSOL63_NORMAL30_OFFLINE_PREPARATION_20260928.zip'
excluded={zname,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json'}
paths=sorted(p for p in R.rglob('*') if p.is_file() and p.name not in excluded)
payload=[dict(file=p.relative_to(R).as_posix(),bytes=p.stat().st_size,sha256=ref(p)['sha256']) for p in paths]
write('PACKAGE_MANIFEST.json',{'schema':1,'approved':False,'usable':False,'code_manifest_sha256':mh,'files':payload})
paths.append(R/'PACKAGE_MANIFEST.json')
with zipfile.ZipFile(R/zname,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in paths:z.write(p,p.relative_to(R).as_posix())
with zipfile.ZipFile(R/zname) as z:
    names=z.namelist();assert z.testzip() is None
    assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
    assert set(names)=={p.relative_to(R).as_posix() for p in paths}
    for i in z.infolist():
        assert not i.filename.startswith(('/','\\')) and '..' not in Path(i.filename).parts and not stat.S_ISLNK(i.external_attr>>16)
    for p in payload:
        raw=z.read(p['file']);assert len(raw)==p['bytes'] and sha(raw)==p['sha256']
receipt={'source':'LOCAL_STATIC_AUTHORING_AND_PACKAGE_TOOL','created_utc':datetime.now(timezone.utc).isoformat(),'zip':ref(R/zname),'package_manifest':ref(R/'PACKAGE_MANIFEST.json'),'code_manifest':ref(R/'CODE_MANIFEST.json'),'payload_count':len(payload),'zip_entries':len(paths),'recipient':None,'checks':'exact set, sizes/SHA, CRC, duplicate/casefold/path/symlink checks passed','native_runs':0,'functional_validation_runs':0,'actual_tool_return':'Not known inside this script; if retained, recorded separately after return.','elapsed_wall_seconds_from_START':(datetime.now(timezone.utc)-datetime.fromisoformat(start['start_utc'].replace('Z','+00:00'))).total_seconds()}
write('DELIVERY_RECEIPT.json',receipt)
print(json.dumps({'status':'OFFLINE_CANDIDATE_SEALED_NOT_EXECUTED','manifest_sha256':mh,'zip':receipt['zip'],'payload_count':len(payload),'static_checks':len(checks),'proposed_groups':len(groups),'proposed_case_specs':plan['listed_case_specs'],'elapsed_preparation_wall_s':receipt['elapsed_wall_seconds_from_START']},ensure_ascii=False))
