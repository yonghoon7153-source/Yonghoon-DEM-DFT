"""Authoring/static-data tool. Does not import/execute candidate code or start engines."""
from pathlib import Path
import ast, csv, difflib, hashlib, json, re, time
from decimal import Decimal as D
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT.parent/'guard1198_limited_validation_R1_20260928'
def sha(b):return hashlib.sha256(b).hexdigest()
def ref(p):
    p=Path(p)
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    return {'path':p.as_posix(),'bytes':p.stat().st_size,'sha256':h}
def put(name,data):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    raw=data if isinstance(data,bytes) else data.encode('utf-8')
    with p.open('xb') as f:f.write(raw)
def dump(name,data):put(name,json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
def text(p):return Path(p).read_text('utf-8-sig')
def replace(s,a,b,n=None):
    count=s.count(a)
    assert count and (n is None or count==n),(a,count,n)
    return s.replace(a,b)
def blocks(s):
    # Parse only; never compile, import, eval or execute target methods.
    tree=ast.parse(s)
    lines=s.splitlines(keepends=True)
    return {x.name:''.join(lines[x.lineno-1:x.end_lineno]) for x in tree.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
assert sha((OLD/'CODE_MANIFEST.json').read_bytes())=='0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45'
manifest=json.loads(text(OLD/'CODE_MANIFEST.json'))
for r in manifest['files']:
    p=OLD/r['file'];assert p.stat().st_size==r['bytes'] and ref(p)['sha256']==r['sha256'],r
c=json.loads(text(OLD/'CONTRACT.json'));original_contract=json.loads(text(OLD/'CONTRACT.json'))
preserve=[OLD/r['file'] for r in manifest['files']]+[OLD/'CODE_MANIFEST.json',OLD/'COMMAND_MAP.json']
preserve += [Path(r['path']) for r in c['baseline_files'].values()]
preserve += [OLD/'future_run_001'/n for n in ('NATIVE_STATE.json','TRIGGER_RESULT.json','compile_RETURN.json','batch_RETURN.json','OUTPUT_MPH_IDENTITY.json')]
preserve += [OLD/'future_parent_001'/n for n in ('NATIVE_PARENT_RETURN.json','ANALYSIS_PARENT_RETURN.json','FINAL_BOUNDARY.json')]
preserve += [Path(r['path']) for r in c['external_source_pins']]
preserve += [Path('C:/Users/BML/.codex/attachments/8b4e0bac-508b-4964-8512-07a527685efa/붙여넣은 텍스트.txt')]
preserve=list(dict.fromkeys(preserve));before=[ref(p) for p in preserve]
dump('PRESERVATION_BEFORE.json',before)
for r in manifest['files']:put('basis/'+r['file'],(OLD/r['file']).read_bytes())
put('basis/CODE_MANIFEST.json',(OLD/'CODE_MANIFEST.json').read_bytes())
put('basis/RECEIVED_REVIEW.txt',preserve[-1].read_bytes())
for n in ('NATIVE_STATE.json','compile_RETURN.json','batch_RETURN.json','OUTPUT_MPH_IDENTITY.json'):
    put('basis/native_'+n,(OLD/'future_run_001'/n).read_bytes())
put('basis/prior_FINAL_BOUNDARY.json',(OLD/'future_parent_001/FINAL_BOUNDARY.json').read_bytes())

oldreq=c['requested_times_s'];assert len(oldreq)==187 and D(oldreq[-1])==5
newreq=oldreq+[format(D(i)/10,'f') for i in range(51,301)]
assert len(newreq)==437 and len(set(map(D,newreq)))==437
java_old=(OLD/'src/Guard1198Candidate.java').read_bytes();java=java_old
replacements=[
 ('Guard1198Candidate','Normal30Candidate','identity'),
 ('5-second transient','30-second transient','time label'),
 ('values[0][i]>5||','values[0][i]>30||','output time bound'),
 ('evaluate("ce_stop_threshold")!=1198.0','evaluate("ce_stop_threshold")!=0.0','normal threshold readback'),
 ('PREFLIGHT_SOLVE_BEGIN=0..5 seconds','PREFLIGHT_SOLVE_BEGIN=0..30 seconds','time label'),
 ('fresh common dense time grid, 5 seconds only','fresh common dense time grid, 30 seconds only','time label'),
 ('"1198[mol/m^3]"','"0[mol/m^3]"','test threshold to existing normal'),
 ('set("tlist","'+' '.join(oldreq)+'")','set("tlist","'+' '.join(newreq)+'")','requested time extension'),
 ('GUARD1198_PRODUCER_COMPLETE','NORMAL30_PRODUCER_COMPLETE','producer identity')]
java_changes=[]
for a,b,why in replacements:
    aa,bb=a.encode(),b.encode();count=java.count(aa);assert count,(a,count)
    java_changes.append({'before':a,'after':b,'occurrences':count,'category':why});java=java.replace(aa,bb)
reverse=java
for a,b,why in reversed(replacements):reverse=reverse.replace(b.encode(),a.encode())
assert reverse==java_old,'JAVA_REVERSE_BYTES'
put('src/Normal30Candidate.java',java)
dump('JAVA_ALLOWED_REPLACEMENTS.json',java_changes)
assert java.count(b'.runAll()')==1 and b'getPreference(' not in java and b'loadCopy(' not in java

def reroot(x):
    if isinstance(x,str):return x.replace(OLD.as_posix(),ROOT.as_posix()).replace('Guard1198Candidate','Normal30Candidate').replace('guard1198_candidate_001','normal30_candidate_001').replace('guard1198_001.json','normal30_001.json')
    if isinstance(x,list):return [reroot(v) for v in x]
    if isinstance(x,dict):return {k:reroot(v) for k,v in x.items()}
    return x
c=reroot(c);c['threshold_mol_m3']='0';c['maximum_physical_s']='30'
c['requested_times_s']=newreq;c['baseline_requested_times_s']=oldreq
c['candidate_java']=ref(ROOT/'src/Normal30Candidate.java')
c['guard_stop_descriptions']={'electrolyte_guard':'Electrolyte minimum <= threshold','ocp_guard':'OCP surface outside table','surface_guard':'Invalid surface concentration'}
c['budgets_seconds']={'preflight_and_input':180,'compile_batch':3600,'process_cleanup_total':120,'analysis':900,'delivery':300,'overall':5100}
c['resource_proposal']['disk_start_gib']=20
c['resource_proposal']['memory_note']='Observe start RAM; no new RAM floor or working-set monitor. Previous 8 GiB start threshold is not reintroduced.'
c['policy']['native_permission_status']='1198 predecessor completed under unchanged policy; new execution rechecks approved prefs identity. No blanket effective-policy claim or fallback.'
c['future_native_blockers']=['new changed branches not validated','new source/class compatibility not tested','current-policy identity must match future user approval','separate manifest-bound validation release and native30 user approval absent']
c['parent_completion_boundary']={'accepted_proposal':'SCRIPT_FINAL_RECORD_AND_USER_OBSERVED_PROMPT_RETURN','outer_powershell_exit_code':None,'reason':'-NoExit keeps process alive; do not invent raw host rc. Child native and analyzer rc are captured separately.'}
with (OLD/'future_run_001/tables/axes_runtime_settings.csv').open(encoding='utf-8-sig',newline='') as f:settings={r['key']:r['actual_value'] for r in csv.DictReader(f)}
keys=['geometry_length_unit','geometry_dimension','rtol','initialstepbdf','initialstepbdfactive','maxstepconstraintbdf','maxstepexpressionbdf','maxstepbdf','tstepsbdf','tout','consistent','atolglobalmethod','atolglobalvaluemethod','atolglobalfactor','atolglobal','eventtol','profile_time_interpolation','profile_spatial_evaluation']
c['runtime_settings_required']={k:settings[k] for k in keys}
dump('CONTRACT.json',c)

consumer_old=text(OLD/'src/trigger_consumer.py');consumer=consumer_old
newblocks=blocks(text(ROOT/'preparation/consumer_changes.txt'));oldblocks=blocks(consumer)
for name,body in newblocks.items():
    if name in oldblocks:consumer=replace(consumer,oldblocks[name],body,1)
    else:consumer+='\n'+body+'\n'
consumer=replace(consumer,'UNEXECUTED candidate: early-stop consumer.','UNEXECUTED candidate: normal30/protected-stop consumer.',1)
consumer=replace(consumer,"'threshold_SI':'1198.0'","'threshold_SI':'0.0'",1)
initial="""    components={}
    for key in ('Li_N_mol_m2','Li_P_mol_m2','Li_electrolyte_mol_m2'):
        current=glob[D(0)][key];reference=base[names[0]][D(0)][key]
        need(current>0 and reference>0,'INITIAL_LI_COMPONENT_POSITIVE')
        delta=abs((current-reference)/reference)
        need(delta<=number(c['limits']['relative_Li']),'INITIAL_LI_COMPONENT')
        components[key]={'status':'PASS','current':str(current),'baseline':str(reference),'relative_delta':str(delta)}
"""
consumer=replace(consumer,'    li=voltage=deltaV=dx=D(0)\n',initial+'    li=voltage=deltaV=dx=D(0)\n',1)
consumer=replace(consumer,"'status':'PASS','coverage':info,","'status':'PASS','coverage':info,'initial_Li_components':components,'late_interval':late_summary(glob,n,p,g),",1)
consumer=replace(consumer,"'stop_times_not_interpolated':[str(t) for t in times[-2:] if t not in common]","'terminal_times_excluded_from_comparison':[str(t) for t in times[-2:] if t not in common]",1)
put('src/diagnostic_consumer.py',consumer)

entry_old=text(OLD/'src/candidate_entry.py');entry=entry_old
for a,b in [('Guard1198Candidate','Normal30Candidate'),('native1198_one_shot','native30_one_shot'),('trigger_consumer.py','diagnostic_consumer.py'),('_guard1198_consumer','_normal30_consumer'),('_guard1198_existing_c2','_normal30_existing_c2'),('TRIGGER_RESULT.json','DIAGNOSTIC_RESULT.json'),('TRIGGER_AND_SAMPLED_DATA_ACCEPTABLE','NORMAL_30S_DIAGNOSTIC_COMPLETE')]:entry=replace(entry,a,b)
entry=replace(entry,blocks(entry)['incomplete_result'],newblocks['incomplete_result'],1)
for a,b in [('ENTRY_START+180',"ENTRY_START+c['budgets_seconds']['preflight_and_input']"),('>=10*2**30',">=c['resource_proposal']['disk_start_gib']*2**30"),('ENTRY_START<=180',"ENTRY_START<=c['budgets_seconds']['preflight_and_input']"),('1800-native_spent',"c['budgets_seconds']['compile_batch']-native_spent"),('cleanup_total<=120 and native_spent<=1800',"cleanup_total<=c['budgets_seconds']['process_cleanup_total'] and native_spent<=c['budgets_seconds']['compile_batch']"),("state['start']+3000","state['start']+c['budgets_seconds']['overall']"),("result['analysis_elapsed_seconds']>600","result['analysis_elapsed_seconds']>c['budgets_seconds']['analysis']")]:entry=replace(entry,a,b)
put('src/candidate_entry.py',entry)

parent_old=text(OLD/'PARENT_COMMAND.ps1');parent=parent_old
start=parent.index('function GDecision(');end=parent.index('\ntry {',start)
parent=parent[:start]+text(ROOT/'preparation/decision.ps1.txt').rstrip()+parent[end:]
for a,b in [(OLD.as_posix(),ROOT.as_posix()),('native1198_one_shot','native30_one_shot'),('TRIGGER_RESULT.json','DIAGNOSTIC_RESULT.json'),('3000','5100')]:parent=replace(parent,a,b)
parent=replace(parent,'$bDeliveryStart=$null',"$bDeliveryStart=$null\n$limited='INCOMPLETE'",1)
parent=replace(parent,"raw_host_rc='not_known_before_return'","raw_host_rc=$null;host_boundary='SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT';script_body_returned=$true;limited=$limited;local_decision=$(if (Test-Path -LiteralPath (Join-Path $bEvidence 'PARENT_LOCAL_DECISION.json')) { BRef (Join-Path $bEvidence 'PARENT_LOCAL_DECISION.json') } else { $null })",1)
parent=replace(parent,"kind='USER_PARENT_FINAL_RETURN';boundary=","kind='USER_PARENT_FINAL_RETURN';limited=$limited;record_errors=$bErrors;within_limits=$within;host_boundary='SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT';raw_host_rc=$null;boundary=",1)
put('PARENT_COMMAND.ps1',parent)

files=['src/Normal30Candidate.java','src/diagnostic_consumer.py','src/candidate_entry.py','PARENT_COMMAND.ps1','CONTRACT.json']
m={'schema':1,'run_id':c['run_id'],'approved':False,'usable':False,'status':'OFFLINE_CANDIDATE_NOT_VALIDATED','previous_manifest_sha256':sha((OLD/'CODE_MANIFEST.json').read_bytes()),'files':[dict(file=n,bytes=(ROOT/n).stat().st_size,sha256=ref(ROOT/n)['sha256']) for n in files]}
dump('CODE_MANIFEST.json',m);mh=ref(ROOT/'CODE_MANIFEST.json')['sha256']
cm=reroot(json.loads(text(OLD/'COMMAND_MAP.json')))
cm=json.loads(json.dumps(cm).replace('0c14c4f886d53398fc4869db117577066b821837cd3593a6727e2ac4d0a63c45',mh))
cm['parent']['completion_boundary']=c['parent_completion_boundary'];cm['gate']='Existing fresh same-process C2 input; no check-only re-diagnosis; no current execution.'
cm['not_created_paths'] += [(ROOT/'future_authorizations/USER_DECISION.json').as_posix()]
dump('COMMAND_MAP.json',cm)
for p in cm['not_created_paths']:assert not Path(p).exists(),p
assert c['cwd']==original_contract['cwd']
assert c['external_source_pins']==original_contract['external_source_pins']
assert c['baseline_files']==original_contract['baseline_files']
assert c['limits']==original_contract['limits'] and c['coordinates']==original_contract['coordinates']
diff=[]
for oldname,newname in [('src/Guard1198Candidate.java','src/Normal30Candidate.java'),('src/trigger_consumer.py','src/diagnostic_consumer.py'),('src/candidate_entry.py','src/candidate_entry.py'),('PARENT_COMMAND.ps1','PARENT_COMMAND.ps1'),('CONTRACT.json','CONTRACT.json')]:
    diff.extend(difflib.unified_diff(text(OLD/oldname).splitlines(True),text(ROOT/newname).splitlines(True),fromfile='accepted1198/'+oldname,tofile='candidate30/'+newname))
put('SOURCE_DIFF.patch',''.join(diff))
parse_info=[]
for n in ('src/candidate_entry.py','src/diagnostic_consumer.py'):
    t=ast.parse(text(ROOT/n));parse_info.append({'file':n,'python_syntax':'PARSED_ONLY','functions':[v.name for v in t.body if isinstance(v,ast.FunctionDef)]})
unchanged_consumer=sorted(k for k,v in blocks(consumer_old).items() if blocks(consumer).get(k)==v)
unchanged_entry=sorted(k for k,v in blocks(entry_old).items() if blocks(entry).get(k)==v)
dump('STATIC_SOURCE_CHECKS.json',{'status':'STATIC_CHECKS_ONLY_NOT_FUNCTIONAL_PASS','manifest_sha256':mh,'java_inverse_replacement_exact_bytes':reverse==java_old,'java_original_sha256':sha(java_old),'java_candidate_sha256':sha(java),'java_runAll_lexical_count':java.count(b'.runAll()'),'old_requested_count':len(oldreq),'new_requested_count':len(newreq),'unchanged_requested_prefix':newreq[:187]==oldreq,'Python':parse_info,'unchanged_consumer_functions':unchanged_consumer,'unchanged_entry_functions':unchanged_entry,'native_compile':0,'jvm':0,'candidate_import_or_execution':0,'console_or_job_tests':0,'baseline_pins_unchanged':True,'external_source_pins_unchanged':True,'coordinates_and_limits_unchanged':True,'not_created_paths':cm['not_created_paths'],'PowerShell':'Text reviewed only; no engine/parser invocation','Java':'Text/inverse-byte comparison only; not compiled'})
after=[ref(p) for p in preserve];assert after==before
dump('PRESERVATION_AFTER_BUILD.json',after)
dump('BUILD_COMPLETED.json',{'utc':datetime.now(timezone.utc).isoformat(),'monotonic_s':time.monotonic(),'manifest_sha256':mh,'source_file_count':len(files),'input_selected_count':len(before),'result':'STATIC_CANDIDATE_WRITTEN_NOT_VALIDATED'})
print(json.dumps({'manifest_sha256':mh,'java_sha256':sha(java),'requested_times':len(newreq),'preserved_selected':len(before),'candidate_execution':0}))
