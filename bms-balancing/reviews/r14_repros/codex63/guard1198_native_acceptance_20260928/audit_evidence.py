"""Read-only evidence bindings. No supplied module imports or native calls."""
from pathlib import Path
import hashlib,json,zipfile,stat,collections
O=Path(__file__).resolve().parent;R=O/'received'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def pairs(items):
    d={}
    for k,v in items:
        assert k not in d,k
        d[k]=v
    return d
def decode(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def load(n):return decode((R/n).read_bytes())
def equal_ref(r,b):assert {k:r[k] for k in ('bytes','sha256')}==ident(b)
pool={};counts={};nested=[]
for p in R.rglob('*'):
    if p.is_file():pool.setdefault(ident(p.read_bytes())['sha256'],[]).append(p.relative_to(R).as_posix())
for p in (R/'prior').glob('*.zip'):
    with zipfile.ZipFile(p) as z:
        ns=z.namelist();assert len(ns)==len(set(x.casefold() for x in ns))
        for e in z.infolist():
            assert not e.filename.startswith(('/','\\')) and '..' not in Path(e.filename).parts and ':' not in e.filename and '\\' not in e.filename
            assert not stat.S_ISLNK(e.external_attr>>16)
        mraw=z.read('PACKAGE_MANIFEST.json');files=decode(mraw)['files']
        assert set(ns)=={f['file'] for f in files}|{'PACKAGE_MANIFEST.json'}
        for f in files:
            b=z.read(f['file']);equal_ref(f,b);pool.setdefault(ident(b)['sha256'],[]).append(p.name+'!'+f['file'])
        pool.setdefault(ident(mraw)['sha256'],[]).append(p.name+'!PACKAGE_MANIFEST.json')
        assert z.testzip() is None
        nested.append({'name':p.name,**ident(p.read_bytes()),'payload':len(files),'manifest':ident(mraw),'verified':True})
        if 'PREEXEC' in p.name:
            for n in ['NEXT_1198_APPROVAL_DRAFT_KO.md','ROUTE_ASSESSMENT_KO.md','POLICY_OBSERVATION.json','APPROVAL_FIELD_MAPPING_KO.md']:
                out=O/'reference'/n;out.parent.mkdir(exist_ok=True);out.write_bytes(z.read(n))

c=load('candidate/CONTRACT.json');mraw=(R/'candidate/CODE_MANIFEST.json').read_bytes();m=decode(mraw);msha=ident(mraw)['sha256']
assert m['approved'] is False and m['usable'] is False
for f in m['files']:equal_ref(f,(R/'candidate'/f['file']).read_bytes())
equal_ref(c['candidate_java'],(R/'run/Guard1198Candidate.java').read_bytes())
equal_ref(load('run/CLASS_IDENTITY.json'),(R/'run/Guard1198Candidate.class').read_bytes())
assert (R/'run/Guard1198Candidate.class').read_bytes()[:4]==b'\xca\xfe\xba\xbe'
source_map=load('SOURCE_MAP_AND_PRESERVATION_BEFORE.json');assert source_map==load('PRESERVATION_AFTER.json')
for f in source_map:equal_ref(f['source'],(R/f['archive_path']).read_bytes())
external=[]
for f in c['external_source_pins']:
    matches=pool.get(f['sha256'],[]);assert matches,f['path'];external.append({'path':f['path'],'sha256':f['sha256'],'copies':matches})
for name,f in c['baseline_files'].items():equal_ref(f,(R/'baseline'/name).read_bytes())
a=load('authorization/guard1198_001.json');release=load('authorization/VALIDATION_RELEASE.json')
for x in [a,release]:assert x['run_id']==c['run_id'] and x['code_manifest_sha256']==msha
assert a['approved'] is True and a['native1198_one_shot'] is True and a['allow_policy_changes'] is False
assert a['commands']==c['commands'] and a['budgets_seconds']==c['budgets_seconds']
equal_ref(a['validation_release'],(R/'authorization/VALIDATION_RELEASE.json').read_bytes())
equal_ref(a['user_decision'],(R/'authorization/USER_DECISION.txt').read_bytes())
assert release['changed_branch_validation']=='PASS' and release['native_permission_route_reviewed'] is True
release_matches=[]
for f in release['validation_evidence']:
    hits=pool.get(f['sha256'],[]);assert hits,f['path']
    release_matches.append({'path':f['path'],'sha256':f['sha256'],'copies':hits})
start=load('parent/PARENT_START.json');state=load('run/NATIVE_STATE.json');result=load('run/TRIGGER_RESULT.json');decision=load('parent/PARENT_LOCAL_DECISION.json');boundary=load('parent/FINAL_BOUNDARY.json')
for key,n in [('approval','authorization/guard1198_001.json'),('release','authorization/VALIDATION_RELEASE.json')]:equal_ref(start[key],(R/n).read_bytes())
assert start['manifest_sha256']==msha and start['cwd'].replace('\\','/')==c['cwd']
assert state['native_attempts']=={'batch':1,'compile':1} and state['errors']==[] and state['status']=='NATIVE_RETURN_READY'
assert state['code_manifest_sha256']==result['code_manifest_sha256']==msha
phase_results={}
for phase in ['compile','batch']:
    res=load(f'run/{phase}_RETURN.json');reserve=load(f'run/{phase}_RESERVATION.json')
    assert reserve['argv']==c['commands'][phase] and reserve['cwd']==c['run_root']
    assert res==state[phase]
    es=sorted((R/'run').glob(f'{phase}_event_*.json'))
    assert [int(p.stem.rsplit('_',1)[1]) for p in es]==list(range(1,len(es)+1))
    events=[decode(p.read_bytes()) for p in es];enames=[x['event'] for x in events]
    assert enames[:3]==['root','assignment','resume'] and enames.count('resume')==1
    for e in events[:3]:assert e['root_pid']==res['root_pid'] and e['root_creation_filetime']==res['root_creation_filetime']
    assert events[0]['suspended'] is True and events[1]['assigned_before_resume'] is True
    assert events[-1]['terminal_observation']==res and events[-2]['job_members']==[]
    assert res['rc']==0 and res['wait_result']==0 and res['root_exit_observed'] and res['exit_query_succeeded']
    assert res['cleanup']=='PASS' and res['remaining_owned']==res['unattributed_comsol']==res['cleanup_errors']==res['recording_errors']==[]
    assert res['handles_closed'] and res['closed_handles']==['thread','process','job'] and not res['timeout'] and res['termination_request'] is None
    phase_results[phase]={'events':len(es),'event_counts':dict(collections.Counter(enames)),'rc':res['rc'],'elapsed_seconds':res['elapsed_seconds'],'cleanup_seconds':res['cleanup_elapsed_seconds'],'empty_job_observed':True,'owned_pids_count':len(res['observed_owned_pids'])}
assert sum(x['elapsed_seconds']-x['cleanup_seconds'] for x in phase_results.values())<c['budgets_seconds']['compile_batch']
assert sum(x['cleanup_seconds'] for x in phase_results.values())<c['budgets_seconds']['process_cleanup_total']
for key,n in [('native_return','parent/NATIVE_PARENT_RETURN.json'),('analysis_return','parent/ANALYSIS_PARENT_RETURN.json')]:
    v=load(n);assert decision[key]==v and v['native_rc']==0 and v['returned'] and not v['new_error'] and v['exception'] is None
    action='execute' if key=='native_return' else 'analyze'
    expected_argv=['-I','-S','-B','-X','utf8',c['root']+'/src/candidate_entry.py',action,'--approval',c['approval_path'],'--manifest-sha',msha]
    actual_argv=v['argv'].copy();actual_argv[5]=actual_argv[5].replace('\\','/')
    assert actual_argv==expected_argv
    assert v['executable']==c['python']['path'] and v['cwd'].replace('\\','/')==c['cwd']
assert decision['limited']=='AWAITING_LIMITED_EXTERNAL_ACCEPTANCE' and decision['overall']=='INCOMPLETE' and decision['auto_retry'] is False
assert boundary['errors']==[] and boundary['within_limits'] is True
equal_ref(boundary['transcript'],(R/'parent/PARENT_TRANSCRIPT.txt').read_bytes())
policy=load('run/POLICY_BEFORE.json');assert policy['default']==a['default_prefs_identity'] and len(policy['security'])==16
assert policy['security']['security.external.enable']=='on' and policy['security']['security.external.filepermission']=='limited' and policy['changes_authorized'] is False
console=[]
for line in (R/'user/PASTED_CONSOLE.txt').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('{'):console.append(decode(line))
assert len(console)==3
equal_ref(console[0]['record'],(R/'run/NATIVE_STATE.json').read_bytes())
equal_ref(console[1]['result'],(R/'run/TRIGGER_RESULT.json').read_bytes());assert console[1]['analysis_result']==result
equal_ref(console[2]['boundary'],(R/'parent/FINAL_BOUNDARY.json').read_bytes())
assert console[2]['snapshot_seconds']>=boundary['elapsed_seconds'] and console[2]['snapshot_seconds']<3000
gate=load('run/GATE.json');assert gate['status']=='INPUT_GATE_OK'
mph=load('run/OUTPUT_MPH_IDENTITY.json');assert mph==load('EXCLUDED_FILES.json')['mph']['identity']
audit={'status':'PASS_WITH_DECLARED_OBSERVATION_LIMITS','nested_packages':nested,'source_map_entries_byte_matched':len(source_map),'source_map_before_after_equal':True,'candidate_manifest_sha256':msha,'candidate_manifest_files':len(m['files']),'external_source_pins':len(external),'release_references':release_matches,'parent_argv_path_comparison':'Only argv[5] Windows backslash/slash normalized; all options/other arguments exact. Native compile/batch argv and cwd exact. Not byte-identical parent command-map argv.','approval_scope':'Fresh t0 threshold1198 maximum5s one-shot, unchanged policy; receipt and decision byte binding verified, not independent authentication of human origin','phases':phase_results,'native_state_elapsed_seconds':state['elapsed_seconds'],'parent_native_seconds':decision['native_return']['elapsed_seconds'],'parent_analysis_seconds':decision['analysis_return']['elapsed_seconds'],'parent_final_boundary_seconds':boundary['elapsed_seconds'],'user_transcribed_post_boundary_seconds':console[2]['snapshot_seconds'],'outer_powershell_final_rc':'UNVERIFIED; never substitute child rc0','policy':'Saved pre-policy limited/enforce on; unchanged post-policy assertions in sealed code and state. Full prefs absent, no current remote re-observation. Internal effective policy UNVERIFIED.','output_mph_identity_reported_not_directly_rehashed':mph,'numeric_result_error_count':len(result['errors']),'source_policy_preservation':state['preservation'],'source_process_cleanup':state['process_cleanup'],'source_policy_status':state['policy_preservation'],'subject_programs_executed':0}
(O/'EVIDENCE_AUDIT.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in audit.items() if k!='release_references'},ensure_ascii=False))
