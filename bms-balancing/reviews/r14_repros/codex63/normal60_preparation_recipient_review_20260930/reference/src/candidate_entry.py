"""Inactive, untested connection candidate. Separate validation release AND
manifest-bound user approval are required before any OS/console/native action.
Existing C2 source loading, input body and private Job transport are reused.
No new monitor, process-name termination, policy relaxation or retry.
"""
from pathlib import Path
import argparse, hashlib, json, os, sys, time, types, shutil, re
ROOT=Path(__file__).resolve().parent.parent
ENTRY_START=time.monotonic()
def need(x,why):
    if not x:raise RuntimeError(why)
def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'DUPLICATE_JSON');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
def read(p):return strict(Path(p).read_bytes())
def digest(raw):return hashlib.sha256(raw).hexdigest()
def ref(p):
    p=Path(p)
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    return {'path':p.resolve().as_posix(),'bytes':p.stat().st_size,'sha256':h}
def check(r):need(ref(r['path'])==r,'FILE_IDENTITY');return Path(r['path']).read_bytes()
def save(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,sort_keys=True,allow_nan=False)+'\n').encode()
    with Path(p).open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    need(Path(p).read_bytes()==raw,'RECORD_READBACK')
def source_module(name,path,expected):
    need(name not in sys.modules,'PRELOADED_SOURCE')
    raw=check(expected);need(Path(path).resolve()==Path(expected['path']).resolve(),'MODULE_PATH')
    m=types.ModuleType(name);m.__file__=str(Path(path).resolve());m.__cached__=None
    # Executes the retained verified source buffer; no pyc/PathFinder lookup.
    exec(compile(raw,m.__file__,'exec',dont_inherit=True),m.__dict__)
    return m
def seal(expected):
    raw=(ROOT/'CODE_MANIFEST.json').read_bytes();need(digest(raw)==expected,'MANIFEST_SHA');m=strict(raw)
    need(m.get('approved') is False and m.get('usable') is False,'CANDIDATE_FLAGS')
    for r in m['files']:
        p=ROOT/r['file'];need(p.resolve().is_relative_to(ROOT),'MANIFEST_PATH')
        need(p.stat().st_size==r['bytes'] and digest(p.read_bytes())==r['sha256'],'CODE_BYTES')
    c=read(ROOT/'CONTRACT.json');need(c['approved'] is False and c['usable'] is False,'CONTRACT_FLAGS')
    for r in c['external_source_pins']:check(r)
    return c,m
def permission(c,expected,path):
    need(Path(path).resolve().as_posix()==c['approval_path'],'APPROVAL_PATH')
    a=read(path);release=read(c['release_path'])
    for r in (a,release):need(r.get('code_manifest_sha256')==expected and r.get('run_id')==c['run_id'],'AUTHORIZATION_IDENTITY')
    need(a.get('approved') is True and a.get('native60_one_shot') is True,'SEPARATE_NATIVE_APPROVAL')
    need(a.get('allow_policy_changes') is False and a.get('effective_policy_unverified_accepted') is True,'POLICY_SCOPE')
    need(a.get('commands')==c['commands'] and a.get('budgets_seconds')==c['budgets_seconds'],'APPROVAL_COMMAND_BUDGET')
    need(release.get('changed_branch_validation')=='PASS' and release.get('native_permission_route_reviewed') is True,'VALIDATION_OR_ROUTE_PENDING')
    need(release.get('manifest_bytes_unchanged_since_validation') is True,'VALIDATION_SEAL')
    for r in release['validation_evidence']:check(r)
    need(len(release['validation_evidence'])>0,'VALIDATION_EVIDENCE_EMPTY')
    need(ref(c['release_path'])==a['validation_release'],'RELEASE_APPROVAL_BINDING')
    check(a['user_decision']);need(Path(a['user_decision']['path']).resolve().is_relative_to(Path(c['approval_path']).parent),'DECISION_PATH')
    return a
def policy_values(raw):
    d={}
    for line in raw.decode('utf-8-sig').splitlines():
        if line.startswith('security.'):
            k,v=line.split('=',1);need(k not in d,'POLICY_DUPLICATE');d[k]=v
    need(d and d.get('security.external.enable')=='on','ENFORCE_REQUIRED');return d
def process_ok(r,logs):
    need(r.get('started') is True and type(r.get('rc')) is int and r['rc']==0,'PROCESS_RC')
    need(r.get('timeout') is False and r.get('cleanup')=='PASS' and r.get('ownership_verified') is True,'PROCESS_CLEANUP')
    need(r.get('root_exit_observed') is True and r.get('exit_query_succeeded') is True and r.get('handles_closed') is True,'PROCESS_TERMINAL')
    need(r.get('remaining_owned')==[] and r.get('unattributed_comsol')==[],'PROCESS_MEMBERS')
    need(not r.get('original_error') and r.get('cleanup_errors')==[] and r.get('recording_errors')==[] and not r.get('termination_request'),'PROCESS_ERRORS')
    need(not re.search(r'/\*{3,}\s*Error\s*\*{3,}/|Error running java class\.|Security preference .*does not allow',logs,re.I),'NATIVE_FATAL_RC0')
def execute(c,a,expected):
    run=Path(c['run_root']);need(not run.exists(),'EXISTING_RUN_NO_RETRY')
    need(Path.cwd().resolve().as_posix()==c['cwd'],'CWD')
    need(os.name=='nt' and sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode and sys.flags.utf8_mode,'START_OPTIONS')
    need(ref(sys.executable)==c['python'],'PYTHON_IDENTITY')
    c2=source_module('_normal60_existing_c2',c['legacy_gate']['path'],c['legacy_gate'])
    legacy=strict(check(c['legacy_contract']));adapter=c2.NativeAdapter()
    c2.environment(legacy,adapter)
    state={'run_id':c['run_id'],'code_manifest_sha256':expected,'start':ENTRY_START,'status':'INCOMPLETE','errors':[],'native_attempts':{},'preservation':'INCOMPLETE','process_cleanup':'INCOMPLETE','policy_preservation':'INCOMPLETE','actual_cores':'UNVERIFIED','effective_policy':'UNVERIFIED'}
    run.mkdir();save(run/'START.json',state)
    baseline_before=[]
    policy_before=None;default=Path(c['policy']['default_prefs_path']);cleanup_total=0.0
    try:
        baseline_before=[ref(r['path']) for r in c['baseline_files'].values()]
        for actual,r in zip(baseline_before,c['baseline_files'].values()):need(actual==r,'BASELINE_IDENTITY')
        with c2.VerifiedApplications(legacy) as app:
            gate=c2.input_gate(app,adapter,time.monotonic,ENTRY_START+c['budgets_seconds']['preflight_and_input']);save(run/'GATE.json',gate)
            app.recheck();seal(expected);permission(c,expected,c['approval_path'])
            import winjob
            transport=winjob.WindowsJobTransport();resources=transport.resources(str(run));save(run/'RESOURCES.json',resources)
            need(resources['free_disk_bytes']>=c['resource_proposal']['disk_start_gib']*2**30,'DISK_START')
            need(time.monotonic()-ENTRY_START<=c['budgets_seconds']['preflight_and_input'],'PREFLIGHT_BUDGET')
            need(not any(x.get('name','').lower() in ('comsolbatch.exe','comsolcompile.exe') for x in transport.census()),'OTHER_NATIVE_BATCH_PRESENT')
            policy_before=check(a['default_prefs_identity']);need(Path(a['default_prefs_identity']['path']).resolve()==default.resolve(),'PREFS_PATH')
            security=policy_values(policy_before)
            for d in ('prefs','config_compile','data_compile','config_batch','data_batch'):(run/d).mkdir()
            with (run/'prefs/comsol.prefs').open('xb') as f:f.write(policy_before)
            save(run/'POLICY_BEFORE.json',{'default':ref(default),'security':security,'changes_authorized':False})
            with (run/'Normal60Candidate.java').open('xb') as f:f.write(check(c['candidate_java']))
            native_spent=0.0
            for phase in ('compile','batch'):
                check(c['native_executable_pins'][phase])
                need((run/'Normal60Candidate.java').read_bytes()==check(c['candidate_java']),'STAGED_SOURCE_CHANGED')
                if phase=='batch':
                    classes=list(run.glob('*.class'));need(len(classes)==1 and classes[0].name=='Normal60Candidate.class','CLASS_SET')
                    need(classes[0].read_bytes()[:4]==b'\xca\xfe\xba\xbe','CLASS_MAGIC')
                    save(run/'CLASS_IDENTITY.json',ref(classes[0]))
                app.recheck();seal(expected);need(default.read_bytes()==policy_before,'DEFAULT_PREFS_CHANGED')
                need(policy_values((run/'prefs/comsol.prefs').read_bytes())==security,'PRIVATE_POLICY_CHANGED')
                need(phase not in state['native_attempts'],'ATTEMPT_DUPLICATE');state['native_attempts'][phase]=1
                save(run/(phase+'_RESERVATION.json'),{'argv':c['commands'][phase],'cwd':run.as_posix(),'start':time.monotonic()})
                counter=[0]
                def update(v):
                    counter[0]+=1;save(run/(phase+'_event_%06d.json'%counter[0]),v)
                result=transport.run(c['commands'][phase],str(run),str(run/(phase+'_console.log')),c['budgets_seconds']['compile_batch']-native_spent,60,update)
                state[phase]=result;save(run/(phase+'_RETURN.json'),result)
                cleanup_total+=result['cleanup_elapsed_seconds'];native_spent+=result['elapsed_seconds']-result['cleanup_elapsed_seconds']
                need(cleanup_total<=c['budgets_seconds']['process_cleanup_total'] and native_spent<=c['budgets_seconds']['compile_batch'],'NATIVE_PHASE_BUDGET')
                logs=(run/(phase+'_console.log')).read_text('utf-8-sig')
                if phase=='batch':logs+='\n'+(run/'batch.log').read_text('utf-8-sig')
                process_ok(result,logs)
            mph=list(run.glob('*.mph'))
            need(len(mph)==1 and mph[0].name==c['expected_mph_name'],'OUTPUT_MPH_SET')
            save(run/'OUTPUT_MPH_IDENTITY.json',ref(mph[0]))
            state['status']='NATIVE_RETURN_READY'
    except BaseException as e:state['errors'].append({'stage':'execution','type':type(e).__name__,'error':str(e)})
    finally:
        try:
            after=[ref(r['path']) for r in c['baseline_files'].values()];need(after==baseline_before,'BASELINE_CHANGED');seal(expected);state['preservation']='PASS'
        except BaseException as e:state['errors'].append({'stage':'preservation','error':str(e)})
        try:
            need(policy_before is not None and default.read_bytes()==policy_before,'DEFAULT_POLICY_UNCONFIRMED')
            need(policy_values((run/'prefs/comsol.prefs').read_bytes())==policy_values(policy_before),'PRIVATE_POLICY_CHANGED')
            state['policy_preservation']='PASS'
        except BaseException as e:state['errors'].append({'stage':'policy','error':str(e)})
        try:
            need(state['native_attempts'] and all(state.get(p,{}).get('cleanup')=='PASS' for p in state['native_attempts']),'CLEANUP_NOT_CONFIRMED')
            state['process_cleanup']='PASS'
        except BaseException as e:state['errors'].append({'stage':'cleanup','error':str(e)})
        if state['errors']:state['status']='INCOMPLETE'
        state['end']=time.monotonic();state['elapsed_seconds']=state['end']-ENTRY_START
        save(run/'NATIVE_STATE.json',state)
    print(json.dumps({'status':state['status'],'record':ref(run/'NATIVE_STATE.json'),'actual_host_rc':'MUST_BE_OBSERVED_BY_PARENT'},ensure_ascii=False))
    return 0 if state['status']=='NATIVE_RETURN_READY' else 1
def incomplete_result(state=None):
    state=state or {}
    return {'limited_result':'INCOMPLETE','diagnostic':'INCOMPLETE','sampled_comparison':'INCOMPLETE',
            'preservation':state.get('preservation','INCOMPLETE'),'process_cleanup':state.get('process_cleanup','INCOMPLETE'),
            'policy_preservation':state.get('policy_preservation','INCOMPLETE'),'errors':[],
            'overall':'INCOMPLETE','normal_gate':'INCOMPLETE','effective_policy':'UNVERIFIED','native_approved_by_this_result':False}

def analyze(c,expected):
    run=Path(c['run_root']);state={};result=incomplete_result();began=time.monotonic()
    try:
        state=read(run/'NATIVE_STATE.json');result=incomplete_result(state)
        need(state['run_id']==c['run_id'] and state['code_manifest_sha256']==expected,'STATE_IDENTITY')
        need(state['start']<=time.monotonic()<=state['start']+c['budgets_seconds']['overall'],'OVERALL_BUDGET')
        path=ROOT/'src/diagnostic_consumer.py'
        manifest=read(ROOT/'CODE_MANIFEST.json');pin=next(r for r in manifest['files'] if r['file']=='src/diagnostic_consumer.py')
        consumer=source_module('_normal60_consumer',path,{'path':path.as_posix(),'bytes':pin['bytes'],'sha256':pin['sha256']})
        tables=consumer.extract_tables(run/'batch_console.log',run/'tables')
        result=consumer.analyze(c,run/'tables',(run/'batch.log').read_text('utf-8-sig'),(run/'batch_console.log').read_text('utf-8-sig'),state)
        result['tables_manifest']=tables
    except BaseException as e:
        result['limited_result']='INCOMPLETE'
        result['errors'].append({'axis':'analysis','type':type(e).__name__,'error':str(e)})
    result['run_id']=c['run_id'];result['code_manifest_sha256']=expected;result['analysis_elapsed_seconds']=time.monotonic()-began
    if result['analysis_elapsed_seconds']>c['budgets_seconds']['analysis'] or ('start' in state and time.monotonic()>state['start']+c['budgets_seconds']['overall']):
        result['limited_result']='INCOMPLETE';result['errors'].append({'error':'FINAL_BUDGET'})
    record=None
    try:
        save(run/'DIAGNOSTIC_RESULT.json',result);record=ref(run/'DIAGNOSTIC_RESULT.json')
    except BaseException as e:
        result['limited_result']='INCOMPLETE';result['errors'].append({'axis':'record','type':type(e).__name__,'error':str(e)})
    print(json.dumps({'result':record,'analysis_result':result,'limited_result':result['limited_result'],'overall':'INCOMPLETE'},ensure_ascii=False))
    return 0 if result['limited_result']=='NORMAL_60S_DIAGNOSTIC_COMPLETE' else 1
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=('execute','analyze'));p.add_argument('--approval',required=True);p.add_argument('--manifest-sha',required=True);a=p.parse_args()
    c,_=seal(a.manifest_sha);auth=permission(c,a.manifest_sha,a.approval)
    return execute(c,auth,a.manifest_sha) if a.action=='execute' else analyze(c,a.manifest_sha)
if __name__=='__main__':raise SystemExit(main())
