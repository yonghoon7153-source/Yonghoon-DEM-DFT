"""Recipient evidence-link inspection only; no received module is imported."""
import collections, hashlib, json, re
from decimal import Decimal as D
from pathlib import Path

ROOT=Path(__file__).resolve().parent
R=ROOT/'received'
S=ROOT/'supplement'
checks=[]
def load(p): return json.loads(p.read_bytes())
def check(label, ok):
    checks.append({'check':label,'pass':bool(ok)})
    if not ok: raise ValueError(label)
def norm(p):return str(p).replace('\\','/').casefold()
def identity(p):
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    return {'bytes':p.stat().st_size,'sha256':h}
def matches(p, ref):return identity(p)=={k:ref[k] for k in ['bytes','sha256']}
mapping=load(R/'delivery/SOURCE_PATH_MAP.json')
reverse={norm(v):R/k for k,v in mapping.items()}
check('source map one-to-one',len(reverse)==len(mapping))
def refcheck(ref):
    p=reverse.get(norm(ref['path']))
    return p is not None and matches(p,ref)
C=load(R/'candidate/CONTRACT.json')
M=load(R/'candidate/CODE_MANIFEST.json')
mh=identity(R/'candidate/CODE_MANIFEST.json')['sha256']
check('accepted candidate manifest identity',mh=='6b9ae2a75a2035d0cc80359f5d83cc3ca5dc5aa744b68255d219ce8a55feb603')
check('candidate five source hashes match manifest',len(M['files'])==5 and all(matches(R/'candidate'/x['file'],x) for x in M['files']))
prior=ROOT.parent/'normal30_validation_review_20260930/received'
prior_matches=[]
for x in M['files']:
    ps=[p for p in prior.rglob(Path(x['file']).name) if p.is_file() and matches(p,x)]
    prior_matches.append({'file':x['file'],'previous_identical_copies':len(ps)})
check('all five sources byte-identical to previous independently reviewed validation package',all(x['previous_identical_copies']>0 for x in prior_matches))
check('staged compile Java identical to candidate', (R/'run/Normal30Candidate.java').read_bytes()==(R/'candidate/src/Normal30Candidate.java').read_bytes())
check('class file identity matches compile artifact seal',matches(R/'run/Normal30Candidate.class',load(R/'run/CLASS_IDENTITY.json')))
check('all 16 external source dependencies and 6 baseline CSVs bound to actual included files',len(C['external_source_pins'])==16 and len(C['baseline_files'])==6 and all(refcheck(x) for x in C['external_source_pins']+list(C['baseline_files'].values())))
A=load(R/'authorization/normal30_001.json'); release=load(R/'authorization/VALIDATION_RELEASE.json'); user=load(R/'authorization/USER_DECISION.json')
check('inactive original contract preserved; separate manifest-bound one-shot approval',M['approved'] is False and M['usable'] is False and C['approved'] is False and C['usable'] is False and A['approved'] is True and A['native30_one_shot'] is True and all(x['run_id']==C['run_id'] and x['code_manifest_sha256']==mh for x in [A,release,user]))
check('approval binds exact commands/budgets/user record/release',A['commands']==C['commands'] and A['budgets_seconds']==C['budgets_seconds'] and matches(R/'authorization/USER_DECISION.json',A['user_decision']) and matches(R/'authorization/VALIDATION_RELEASE.json',A['validation_release']))
check('approval no retry/no policy relaxation and explicitly accepts policy/startup limits',A['allow_policy_changes'] is False and A['automatic_retry'] is False and A['additional_shell_or_import_fallback'] is False and A['effective_policy_unverified_accepted'] is True and A['startup_autoload_unverified_accepted'] is True)
# Validation evidence is historical, not re-executed. Find matching prior recipient bytes by hash.
prior_by_name=collections.defaultdict(list)
for p in prior.parent.rglob('*'):
    if p.is_file():prior_by_name[p.name].append(p)
validation_refs=[]
for ref in release['validation_evidence']:
    p=reverse.get(norm(ref['path']))
    name=Path(ref['path'].replace('\\','/')).name
    downloaded=Path('C:/Users/Administrator/Downloads')/name
    found=bool(p and matches(p,ref)) or any(matches(q,ref) for q in prior_by_name[name]) or (downloaded.is_file() and matches(downloaded,ref))
    validation_refs.append({'file':Path(ref['path'].replace('\\','/')).name,'bytes':ref['bytes'],'sha256':ref['sha256'],'matched_prior_or_current_copy':found})
check('17 references present; seven core validation results match received prior copies',len(validation_refs)==17 and all(x['matched_prior_or_current_copy'] for x in validation_refs[:7]))
state=load(R/'run/NATIVE_STATE.json'); start=load(R/'run/START.json')
check('native state has one compile/one batch, no error and same initial time/run/manifest',state['native_attempts']=={'compile':1,'batch':1} and state['errors']==[] and state['start']==start['start'] and state['code_manifest_sha256']==mh and state['run_id']==C['run_id'])
events_summary={}; ret={}
for phase in ['compile','batch']:
    reservation=load(R/f'run/{phase}_RESERVATION.json'); ret[phase]=load(R/f'run/{phase}_RETURN.json')
    check(f'{phase} reserved argv/cwd exact contract',reservation['argv']==C['commands'][phase] and norm(reservation['cwd'])==norm(C['run_root']))
    paths=sorted((R/'run').glob(phase+'_event_*.json'))
    check(f'{phase} continuous event file numbering', [p.name for p in paths]==[f'{phase}_event_{i:06d}.json' for i in range(1,len(paths)+1)])
    es=[load(p) for p in paths]; kinds=[e['event'] for e in es]
    check(f'{phase} root->assignment->resume once, diagnostic last, no termination event',kinds[:3]==['root','assignment','resume'] and all(kinds.count(k)==1 for k in ['root','assignment','resume','diagnostic']) and kinds[-1]=='diagnostic' and set(kinds)<=set(['root','assignment','resume','poll','diagnostic']))
    root=es[0]['root_pid']; creation=es[0]['root_creation_filetime']
    check(f'{phase} suspended creation and assignment before resume same root lifetime',es[0]['suspended'] is True and all(e['root_pid']==root and e['root_creation_filetime']==creation for e in es[:3]) and es[1]['assigned_before_resume'] is True and es[2]['assigned_before_resume'] is True)
    final=es[-1]['terminal_observation']
    check(f'{phase} terminal event / return / native state identical',final==ret[phase]==state[phase])
    check(f'{phase} exit0 and owned process cleanup',final['rc']==0 and final['timeout'] is False and final['cleanup']=='PASS' and all(final[k] is True for k in ['started','resumed','ownership_verified','root_exit_observed','exit_query_succeeded','handles_closed']) and all(final[k]==[] for k in ['remaining_owned','unattributed_comsol','cleanup_errors','recording_errors']) and final['original_error'] is None and final['termination_request'] is None and es[-2]['job_members']==[])
    events_summary[phase]={'events':len(es),'counts':dict(collections.Counter(kinds)),'elapsed_seconds':final['elapsed_seconds'],'cleanup_seconds':final['cleanup_elapsed_seconds']}
compile_start=load(R/'run/compile_RESERVATION.json')['start']; batch_start=load(R/'run/batch_RESERVATION.json')['start']
check('compile completed before batch reservation',compile_start+ret['compile']['elapsed_seconds'] <= batch_start)
check('compile+batch within 3600s and cleanup within120s',sum(x['elapsed_seconds'] for x in ret.values()) <= C['budgets_seconds']['compile_batch'] and sum(x['cleanup_elapsed_seconds'] for x in ret.values())<=C['budgets_seconds']['process_cleanup_total'])
gate=load(R/'run/GATE.json')
check('two fresh challenges before compile, same run, non-elevated console records',gate['status']=='INPUT_GATE_OK' and len(gate['answers'])==2 and all(x['challenge']==x['response'] and 0<=x['end']-x['start']<=60 and state['start']<=x['start']<=x['end']<compile_start for x in gate['answers']) and gate['identity']['elevated'] is False and gate['console']['stdin_isatty'] is True)
policy=load(R/'run/POLICY_BEFORE.json')
check('policy before matches approved hash, enforce on and limited, all16 security values',policy['default']==A['default_prefs_identity'] and policy['changes_authorized'] is False and len(policy['security'])==16 and policy['security']['security.external.enable']=='on' and policy['security']['security.external.filepermission']=='limited')
check('source-bound native state records baseline/source and default/private-policy preservation',all(state[x]=='PASS' for x in ['preservation','policy_preservation','process_cleanup']) and state['effective_policy']=='UNVERIFIED')
diag=load(R/'run/DIAGNOSTIC_RESULT.json'); num=load(ROOT/'NUMERIC_AUDIT.json')
check('analysis reports limited normal completion, retains overall/normal gate and policy limit',diag['errors']==[] and diag['limited_result']=='NORMAL_30S_DIAGNOSTIC_COMPLETE' and diag['overall']==diag['normal_gate']=='INCOMPLETE' and diag['effective_policy']=='UNVERIFIED' and diag['native_approved_by_this_result'] is False)
for a,b in [('maximum_voltage_delta_V','max_voltage_difference_V'),('maximum_surface_delta','max_surface_difference'),('maximum_Li_relative_drift','maximum_relative_Li_drift'),('maximum_voltage_identity_V','max_voltage_identity_residual_V')]:
    check('reported arithmetic matches recipient: '+a,D(diag['numeric'][a])==D(num[b]))
check('all 35 analysis table seals match actual CSVs',len(diag['tables_manifest'])==35 and all(matches(R/'run/tables'/k,v) for k,v in diag['tables_manifest'].items()))
ps=load(R/'parent/PARENT_START.json'); nr=load(R/'parent/NATIVE_PARENT_RETURN.json'); ar=load(R/'parent/ANALYSIS_PARENT_RETURN.json'); decision=load(R/'parent/PARENT_LOCAL_DECISION.json'); boundary=load(R/'parent/FINAL_BOUNDARY.json'); postrec=load(R/'delivery/POST_WRITE_USER_RETURN.json'); post=postrec['value'] if 'value' in postrec else postrec.get('postwrite')
check('parent start binds exact authorization/release and manifest',matches(R/'authorization/normal30_001.json',ps['approval']) and matches(R/'authorization/VALIDATION_RELEASE.json',ps['release']) and ps['manifest_sha256']==mh)
for name,record in [('native',nr),('analysis',ar)]:
    check(name+' parent returned real child rc0, no invocation error',record['native_rc']==0 and record['returned'] is True and record['invocation_succeeded'] is True and record['new_error'] is False and record['exception'] is None and record['top_error'] is None)
check('parent ordering and analysis900 budget',nr['end_seconds']<=ar['start_seconds']<=ar['end_seconds']<=boundary['elapsed_seconds'] and ar['elapsed_seconds']<=C['budgets_seconds']['analysis'])
check('parent local decision binds actual child returns',decision['native_return']==nr and decision['analysis_return']==ar and decision['auto_retry'] is False)
check('final pre-write boundary hashes transcript/local decision',matches(R/'parent/PARENT_TRANSCRIPT.txt',boundary['transcript']) and matches(R/'parent/PARENT_LOCAL_DECISION.json',boundary['local_decision']) and boundary['errors']==[] and boundary['body_completed_without_error'] is True)
check('post-write exact boundary bytes + monotonic order +5100/300 budget + no fake outer rc',matches(R/'parent/FINAL_BOUNDARY.json',post['boundary']) and post['pre_write_seconds']==boundary['elapsed_seconds'] and post['snapshot_seconds']>=boundary['elapsed_seconds'] and post['delivery_elapsed_seconds']>=boundary['delivery_elapsed_seconds'] and post['snapshot_seconds']<=C['budgets_seconds']['overall'] and post['delivery_elapsed_seconds']<=C['budgets_seconds']['delivery'] and post['record_errors']==[] and post['within_limits'] is True and post['raw_host_rc'] is None)
raw=(R/'user_console/PASTED_TERMINAL.txt').read_text(encoding='utf-8-sig')
parsed=[]
for s in raw.splitlines():
    if s.startswith('{'):
        try:parsed.append(json.loads(s))
        except ValueError:pass
check('user pasted terminal contains exactly same post-write object',sum(x==post for x in parsed)==1)
check('last STOP is literal unconditional no-rerun notice and prompt follows',"STOP. No rerun, cleanup fallback, policy toggle or additional solve. Preserve this output." in raw and raw.rfind('PS ')>raw.rfind('STOP.') and not re.search(r'^STOP:|^FINAL_RECORD_ERROR:',raw,re.M))
before=load(R/'delivery/PRESERVATION_BEFORE.json'); after=load(S/'PRESERVATION_AFTER.json')
bm={norm(x['path']):x for x in before}; am={norm(x['path']):x for x in after}
check('packaging preservation all3188 before entries same in after3197',len(bm)==len(before)==3188 and len(am)==len(after)==3197 and all(k in am and all(v[z]==am[k][z] for z in ['bytes','sha256']) for k,v in bm.items()))
present=[(p,am[norm(source)]) for name,source in mapping.items() if (p:=R/name).is_file() and norm(source) in am]
check('all mapped included files match after observation identities',all(matches(p,ref) for p,ref in present))
missing_before=[v for k,v in bm.items() if k not in reverse]
receipt=load(S/'DELIVERY_RECEIPT.json'); pack=load(S/'PACKAGING_TOOL_RETURN.json'); archives=load(ROOT/'ARCHIVE_AUDIT.json')
stdout=json.loads(pack['completion']['output'])
check('packaging rc0 and stdout matches independently received main ZIP',pack['completion']['exit_code']==0 and stdout['status']=='PACKAGED_AND_READBACK_VERIFIED' and all(stdout['zip'][k]==archives[0][k] for k in ['bytes','sha256']) and stdout['payload_count']==archives[0]['payloads'])
check('generation receipt still recipient null',receipt['recipient'] is None)
summary={'scope':'Received byte identities / recorded execution observations; not current remote machine measurements.',
    'status':'PASS','checks':checks,'source_manifest_sha256':mh,'prior_candidate_reuse':prior_matches,
    'historical_validation_references':validation_refs,'event_summary':events_summary,
    'packaging_preservation_before':len(before),'packaging_preservation_after':len(after),
    'included_files_directly_matched_to_after_records':len(present),'before_entries_not_in_source_map':missing_before,
    'parent_postwrite_seconds':post['snapshot_seconds'],'parent_delivery_seconds':post['delivery_elapsed_seconds'],
    'native_compile_plus_batch_seconds':sum(x['elapsed_seconds'] for x in ret.values()),
    'packaging_elapsed_snapshot_seconds':stdout['elapsed_snapshot_seconds'],
    'packaging_rc_source':'Sender tool-return object subsequently serialized; not the native-run parent exit.',
    'policy_scope':'Source-bound checks and state PASS; no raw prefs in package, no independent remote after read.',
    'human_origin_scope':gate['human_origin'],'postwrite_source':postrec.get('source'),
    'original_overall':'INCOMPLETE','original_normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','new_execution_approved':False}
(ROOT/'RECORDS_AUDIT.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['checks','historical_validation_references','before_entries_not_in_source_map']},ensure_ascii=False,indent=2))
