"""Read-only recipient linkage checks; references are never executed."""
import collections, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent; R=ROOT/'received'; S=ROOT/'supplement'
checks=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def identity(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def check(name,ok):
    checks.append({'check':name,'pass':bool(ok)}); assert ok,name
def norm(s):return s.replace('\\','/').casefold()
archive=read(ROOT/'ARCHIVE_AUDIT.json'); members=archive[0]['members']
mapping=read(R/'delivery/SOURCE_PATH_MAP.json')
by_path={norm(v):R/k for k,v in mapping.items()}
missing=set(); bound=set()
def ref(obj,label):
    p=by_path.get(norm(obj['path']))
    if p is None:missing.add(obj['path']);return False
    check(label,identity(p)=={k:obj[k] for k in ['bytes','sha256']});bound.add(str(p.relative_to(R)));return True
c=read(R/'candidate/CONTRACT.json'); m=read(R/'candidate/CODE_MANIFEST.json')
h=sha(R/'candidate/CODE_MANIFEST.json')
check('previously accepted native60 manifest',h=='82e556243b29b10ae65b95dcdff7f854734b6f1cfffc1881327cab1939ebe5c8')
check('historical inactive source flags preserved',not c['approved'] and not c['usable'] and not m['approved'] and not m['usable'])
prior=ROOT.parent/'normal60_validation_review_20260930/received/candidate'
for e in m['files']:
    check('sealed candidate '+e['file'],identity(R/'candidate'/e['file'])=={k:e[k] for k in ['bytes','sha256']})
    check('same bytes as accepted validation '+e['file'],sha(prior/e['file'])==e['sha256'])
check('compiled input is sealed Java',sha(R/'run/Normal60Candidate.java')==c['candidate_java']['sha256'])
ref(read(R/'run/CLASS_IDENTITY.json'),'class bytes')
for e in c['external_source_pins']:ref(e,'dependency '+e['path'])
for name,e in c['baseline_files'].items():
    ref(e,'baseline '+name)
    old=ROOT.parent/'normal30_native_review_20260930/received'/('baseline' if name.startswith('B020_') else 'run/tables')/name.removeprefix('B020_')
    check('baseline directly matches prior received '+name,identity(old)=={k:e[k] for k in ['bytes','sha256']})
auth=read(R/'authorization/normal60_001.json'); user=read(R/'authorization/USER_DECISION.json'); release=read(R/'authorization/VALIDATION_RELEASE.json')
check('historical authorization exact scope',auth['approved'] and auth['native60_one_shot'] and not auth['automatic_retry'] and not auth['allow_policy_changes'] and auth['commands']==c['commands'] and auth['budgets_seconds']==c['budgets_seconds'] and auth['run_id']==c['run_id'] and auth['code_manifest_sha256']==h)
for k in ['user_decision','validation_release']:ref(auth[k],'approval '+k)
ref(user['request_document'],'user approval request binding')
check('release of accepted46 tests, no source flag rewrite',release['code_manifest_sha256']==h and release['functional_cases']==46 and release['logical_groups']==12 and release['source_flags_remain_false'])
start=read(R/'run/START.json'); state=read(R/'run/NATIVE_STATE.json'); gate=read(R/'run/GATE.json'); diagnostic=read(R/'run/DIAGNOSTIC_RESULT.json')
check('gate response match and limits',gate['status']=='INPUT_GATE_OK' and len(gate['answers'])==2 and all(x['challenge']==x['response'] and 0<=x['end']-x['start']<=60 for x in gate['answers']) and not gate['identity']['elevated'] and all(gate['console'][k] for k in ['stdin_isatty','stdout_isatty','stderr_isatty','std_input_mode_ok','crt_input_mode_ok']))
check('single compile/batch and no native error',state['native_attempts']=={'batch':1,'compile':1} and state['errors']==[] and state['status']=='NATIVE_RETURN_READY' and start['start']==state['start'])
events_summary={}; reservations={}
for phase in ['compile','batch']:
    res=read(R/f'run/{phase}_RESERVATION.json'); ret=read(R/f'run/{phase}_RETURN.json');reservations[phase]=res
    check(phase+' argv/cwd',res['argv']==c['commands'][phase] and norm(res['cwd'])==norm(c['run_root']))
    check(phase+' native return and state',ret==state[phase] and ret['rc']==0 and ret['started'] and ret['resumed'] and ret['root_exit_observed'] and ret['wait_result']==0 and ret['exit_query_succeeded'] and not ret['timeout'] and not ret['recording_errors'] and ret['original_error'] is None)
    check(phase+' owned cleanup',ret['cleanup']=='PASS' and ret['ownership_verified'] and ret['handles_closed'] and not ret['remaining_owned'] and not ret['unattributed_comsol'] and not ret['cleanup_errors'])
    files=sorted((R/'run').glob(phase+'_event_*.json'));ev=[read(p) for p in files];counts=collections.Counter(x['event'] for x in ev)
    check(phase+' contiguous events/order',all(p.name==f'{phase}_event_{i:06d}.json' for i,p in enumerate(files,1)) and [x['event'] for x in ev[:3]]==['root','assignment','resume'] and ev[-1]['event']=='diagnostic' and all(x['event']=='poll' for x in ev[3:-1]))
    check(phase+' ownership consistency',ev[0]['suspended'] and ev[1]['assigned_before_resume'] and ev[2]['assigned_before_resume'] and all(x['root_pid']==ret['root_pid'] and x['root_creation_filetime']==ret['root_creation_filetime'] for x in ev[:3]) and ev[-1]['terminal_observation']==ret and ev[-2]['job_members']==[])
    events_summary[phase]={'count':len(files),'event_counts':dict(counts)}
check('phase order',reservations['compile']['start']+state['compile']['elapsed_seconds']<=reservations['batch']['start'] and gate['answers'][-1]['end']<=reservations['compile']['start'])
check('compile/batch and cleanup budgets',sum(state[x]['elapsed_seconds'] for x in ['compile','batch'])<=3600 and sum(state[x]['cleanup_elapsed_seconds'] for x in ['compile','batch'])<=120 and reservations['compile']['start']-state['start']<=180)
check('native elapsed identity',abs(state['end']-state['start']-state['elapsed_seconds'])<1e-6)
policy=read(R/'run/POLICY_BEFORE.json'); prepolicy=read(R/'preexec/POLICY_OBSERVATION.json')
check('recorded policy identity/security consistent',policy['default']==auth['default_prefs_identity']==prepolicy['identity'] and policy['security']==prepolicy['security'] and len(policy['security'])==16 and policy['security']['security.external.filepermission']=='limited' and not policy['changes_authorized'])
check('limited diagnostic and original boundaries retained',diagnostic['limited_result']=='NORMAL_60S_DIAGNOSTIC_COMPLETE' and diagnostic['sampled_comparison']=='PASS' and diagnostic['overall']==diagnostic['normal_gate']=='INCOMPLETE' and diagnostic['effective_policy']=='UNVERIFIED' and not diagnostic['native_approved_by_this_result'] and diagnostic['errors']==[])
for axis in ['preservation','policy_preservation','process_cleanup']:check('recorded '+axis,state[axis]==diagnostic[axis]=='PASS')
for name,obj in diagnostic['tables_manifest'].items():ref(obj,'table '+name)
ps=read(R/'parent/PARENT_START.json'); final=read(R/'parent/FINAL_BOUNDARY.json'); decision=read(R/'parent/PARENT_LOCAL_DECISION.json'); post=read(S/'POST_WRITE_USER_RETURN.json')['value']
for field in ['approval','release']:ref(ps[field],'parent '+field)
for field in ['transcript','local_decision']:ref(final[field],'boundary '+field)
check('post-write binds exact final boundary',identity(R/'parent/FINAL_BOUNDARY.json')=={k:post['boundary'][k] for k in ['bytes','sha256']} and (R/'delivery/POST_WRITE_USER_RETURN.json').read_bytes()==(S/'POST_WRITE_USER_RETURN.json').read_bytes())
parent_returns={}
for phase,name in [('native','NATIVE_PARENT_RETURN.json'),('analysis','ANALYSIS_PARENT_RETURN.json')]:
    ret=read(R/'parent'/name);parent_returns[phase]=ret
    check(phase+' parent return',ret==decision[phase+'_return'] and ret['native_rc']==0 and ret['returned'] and ret['invocation_succeeded'] and not ret['new_error'] and ret['exception'] is None and ret['top_error'] is None and abs(ret['end_seconds']-ret['start_seconds']-ret['elapsed_seconds'])<1e-6)
    check(phase+' parent argv',ret['argv']==['-I','-S','-B','-X','utf8',c['root']+'/src/candidate_entry.py','execute' if phase=='native' else 'analyze','--approval',c['approval_path'],'--manifest-sha',h] if '/' in ret['argv'][4] and '\\' not in ret['argv'][4] else all(norm(a)==norm(b) for a,b in zip(ret['argv'],['-I','-S','-B','-X','utf8',c['root']+'/src/candidate_entry.py','execute' if phase=='native' else 'analyze','--approval',c['approval_path'],'--manifest-sha',h])) and len(ret['argv'])==11)
    check(phase+' parent cwd and executable',norm(ret['cwd'])==norm(c['cwd']) and norm(ret['executable'])==norm(c['python']['path']))
check('parent phases and final boundary ordered',parent_returns['native']['end_seconds']<=parent_returns['analysis']['start_seconds']<parent_returns['analysis']['end_seconds']<=final['elapsed_seconds']<=post['snapshot_seconds']<=5100)
check('final record post-write budgets and errors',post['within_limits'] and final['within_limits'] and post['delivery_elapsed_seconds']<=300 and parent_returns['analysis']['elapsed_seconds']<=900 and post['pre_write_seconds']==final['elapsed_seconds'] and final['body_completed_without_error'] and not post['record_errors'] and not final['errors'] and final['raw_host_rc'] is None and post['raw_host_rc'] is None)
before=read(R/'delivery/PRESERVATION_BEFORE.json'); after=read(S/'PRESERVATION_AFTER.json')
bb={norm(x['path']):x for x in before}; aa={norm(x['path']):x for x in after}
check('preservation snapshot names unique',len(bb)==len(before) and len(aa)==len(after))
check('all3827 before identities unchanged in after',all(k in aa and {f:v[f] for f in ['bytes','sha256']}=={f:aa[k][f] for f in ['bytes','sha256']} for k,v in bb.items()))
available_before=0;available_after=0
for label,coll in [('before',before),('after',after)]:
    for e in coll:
        matched=ref(e,'preserved '+label+' '+e['path'])
        if matched:
            if label=='before':available_before+=1
            else:available_after+=1
receipt=read(S/'DELIVERY_RECEIPT.json'); tool=read(S/'PACKAGING_TOOL_RETURN.json')['completion']; output=json.loads(tool['output'])
check('receipt and actual package raw identity',{k:receipt['zip'][k] for k in ['bytes','sha256']}=={k:archive[0][k] for k in ['bytes','sha256']} and receipt['payload_count']==3817 and receipt['recipient'] is None)
check('packaging return independent of native parent',tool['exit_code']==0 and output['status']=='PACKAGED_AND_VERIFIED' and output['zip']==receipt['zip'] and output['payloads']==3817 and not output['new_execution_authorized'])
check('supplement binds main zip',read(S/'MANIFEST.json')['main_zip']==receipt['zip'])
res=read(R/'run/RESOURCES.json');check('start disk>=20GiB; no invented RAM floor',res['free_disk_bytes']>=20*1024**3 and c['resource_proposal']['available_ram_floor_gib'] is None)
result={'status':'PASS','scope':'Independent byte/JSON/event consistency review, not remote OS observation','checks':checks,'check_count':len(checks),'events':events_summary,'preservation':{'before_count':len(before),'after_count':len(after),'before_identities_directly_present':available_before,'after_identities_directly_present':available_after,'missing_reference_paths':sorted(missing),'distinct_directly_bound_members':len(bound)},'budgets':{'compile':state['compile']['elapsed_seconds'],'batch':state['batch']['elapsed_seconds'],'compile_batch':sum(state[x]['elapsed_seconds'] for x in ['compile','batch']),'native_parent':parent_returns['native']['elapsed_seconds'],'analysis_parent':parent_returns['analysis']['elapsed_seconds'],'post_write_overall':post['snapshot_seconds'],'native_local_delivery':post['delivery_elapsed_seconds'],'separate_packaging_post_receipt_snapshot':output['post_receipt_snapshot_seconds']},'resource_observation':res,'limitations':['Authorization and final user-console return are supplied transcriptions, not direct recipient user/OS observations.','MPH, full prefs and executable bytes absent; sender hash observations only.','Owned cleanup evidence is historical, not a fresh remote process inventory.','NoExit script completion; outer PowerShell process rc intentionally null.','Supplement own packaging outer return absent; no infinite follow-up required.']}
(ROOT/'RECORDS_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['checks','preservation']},indent=2))
print('PRESERVATION',len(before),len(after),available_before,available_after,'absent refs',len(missing))
