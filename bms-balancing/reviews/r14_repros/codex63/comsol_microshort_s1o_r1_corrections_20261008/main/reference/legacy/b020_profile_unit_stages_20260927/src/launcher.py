"""Dedicated one-shot B launcher. Default `plan` only prints fixed command arrays.
Real execution requires a separate approved B receipt bound to CODE_MANIFEST SHA.
No existing worker, COMSOL MCP, shell, or result-directory fallback is used.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, time, sys

from execution_records import EventStore, require_terminal_evidence, digest as record_digest
from class_artifacts import validate_tree
from status_reader import read_status
from evidence_metrics import utc
from policy_binding import save_snapshot, bound_batch, mode_contract

HERE=Path(__file__).resolve().parent
PHASES=('apply','compile','batch','restore')
def cleanup_evidence_ok(result):
    if not isinstance(result,dict):return False
    known_unstarted=result.get('started') is False and result.get('not_started_verified') is True
    return (result.get('cleanup')=='PASS' and (result.get('ownership_verified') is True or known_unstarted)
        and result.get('remaining_owned')==[] and result.get('unattributed_comsol')==[])
def phase_cleanup_issues(state):
    """A reservation without a terminal result is UNKNOWN, regardless of census/flags."""
    attempts=state.get('attempts')
    if not isinstance(attempts,dict) or set(attempts)!=set(PHASES):return ['Invalid phase reservation set']
    issues=[]
    for name in PHASES:
        count=attempts[name];result=state.get(name+'_process');root=state.get('phase_roots',{}).get(name,{})
        if type(count) is not int or count not in (0,1):issues.append(name+': invalid reservation');continue
        if count==0:
            if result is not None or root:issues.append(name+': evidence without reservation')
            continue
        if not isinstance(result,dict):issues.append(name+': missing terminal result');continue
        if not cleanup_evidence_ok(result) or result.get('cleanup_errors',[])!=[]:
            issues.append(name+': terminal cleanup incomplete');continue
        if result.get('started') is True:
            pid=result.get('root_pid');created=result.get('root_creation_filetime')
            if not (result.get('ownership_verified') is True and type(pid) is int and pid>0 and type(created) is int and created>0
                and root.get('assigned_before_resume') is True and root.get('root_pid')==pid and root.get('root_creation_filetime')==created
                and type(result.get('rc')) is int and result.get('wait_result')==0
                and result.get('root_exit_observed') is True and result.get('exit_query_succeeded') is True and result.get('handles_closed') is True):
                issues.append(name+': terminal root identity/exit unconfirmed')
        elif result.get('started') is False and result.get('not_started_verified') is True:
            if root or result.get('root_pid') is not None or result.get('observed_owned_pids',[])!=[] or result.get('ownership_verified') is not False:
                issues.append(name+': no-start evidence conflicts with process evidence')
        else:issues.append(name+': start status unconfirmed')
    return issues
def decoded_log(path):
    data=Path(path).read_bytes()
    for encoding in ('utf-8-sig','cp949'):
        try:return data.decode(encoding),encoding
        except UnicodeDecodeError:pass
    raise ValueError('Native log encoding unsupported; preserve raw')
def read(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    with Path(p).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,obj):
    p=Path(p);tmp=p.with_name(p.name+'.tmp')
    with tmp.open('w',encoding='utf-8') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,p)
def security(p):
    values={}
    for line in Path(p).read_text(encoding='utf-8-sig').splitlines():
        if line.startswith('security.'):
            k,v=line.split('=',1)
            if k in values:raise ValueError('Duplicate security key')
            values[k]=v
    if values.get('security.external.enable')!='on':raise ValueError('Enforce not on')
    if 'security.external.filepermission' not in values:raise ValueError('Missing file permission')
    return values
def policy_delta(before,after,restore=False):
    key='security.external.filepermission'
    if set(before)!=set(after):raise ValueError('Security key set changed')
    if any(before[k]!=after[k] for k in before if k!=key):raise ValueError('Other security value changed')
    if restore:
        if before!=after:raise ValueError('Policy restore mismatch')
    elif before[key]==after[key]:raise ValueError('No observed permission change')
def fixed_paths(c):
    root=Path(c['run_root']).resolve(); paths=[Path(v).resolve() for v in c['paths'].values()]
    if len(set(paths))!=len(paths):raise ValueError('Path collision')
    for p in paths:
        if p.parent!=root:raise ValueError('Runtime directories must be disjoint direct children')
    for i,p in enumerate(paths):
        if any(p in q.parents or q in p.parents for q in paths[i+1:]):raise ValueError('Nested protected paths')
    input_path=Path(c['input']['path']).resolve()
    if root==input_path or root in input_path.parents:raise ValueError('Input inside disposable runtime')
    return root
def identities(c):
    records=[c['input'],*c['baseline_files'],*c['protected_files']]
    result={}
    for r in records:
        p=Path(r['path']);actual={'bytes':p.stat().st_size,'sha256':sha(p)}
        if actual!={'bytes':r['bytes'],'sha256':r['sha256']}:raise ValueError('Protected identity mismatch: '+str(p))
        result[str(p)]=actual
    return result
def no_pending_jobs(c):
    jobdir=Path(c['existing_job_directory'])
    for p in jobdir.glob('*/status.json'):
        s=read(p)
        if s.get('state') not in ('completed','failed','timed_out','cancelled','canceled'):
            raise ValueError('Existing job active/unknown: '+str(p))
def classify_process(result,log=''):
    if result.get('timeout') is True:return 'TIMEOUT'
    if result.get('timeout') is not False:return 'PROCESS_RESULT_INVALID'
    if result.get('cleanup')!='PASS':return 'HELPER_OR_OWNERSHIP_INCOMPLETE'
    if type(result.get('rc')) is not int:return 'PROCESS_RESULT_INVALID'
    if result.get('rc')!=0:return 'PROCESS_FAILED'
    if result.get('original_error') not in (None,'') or result.get('cleanup_errors',[])!=[] or result.get('recording_errors',[])!=[]:return 'PROCESS_ERROR'
    if result.get('job_only_termination') is True or result.get('exception_owned_handle_termination') is True:return 'PROCESS_ERROR'
    fatal=re.search(r'/\*{3,}\s*Error\s*\*{3,}/|Error running java class\.|Security preference .*does not allow',log)
    if fatal:return 'NATIVE_FATAL_RC0'
    if re.search(r'Time-Dependent Solver|Time-stepping completed|Mesh Statistics|Computing initial',log,re.I):return 'UNEXPECTED_COMPUTATION'
    return 'PROCESS_OK'
def complete_axes(s):
    names=('numeric_recovery','sampled_comparison','preservation','process_cleanup','policy_restore')
    return all(s.get(k)=='PASS' for k in names)
def timed_attest(prompt,seconds):
    # No daemon input thread can remain and consume a later restore response.
    if os.name!='nt' or not sys.stdin.isatty():raise RuntimeError('Bounded local console observation required; no unattended fallback')
    import msvcrt
    print(prompt,end='',flush=True);deadline=time.monotonic()+max(0,seconds);chars=[]
    while time.monotonic()<deadline:
        if not msvcrt.kbhit():time.sleep(.1);continue
        ch=msvcrt.getwch()
        if ch=='\x03':raise KeyboardInterrupt()
        if ch in ('\r','\n'):print();return ''.join(chars)
        if ch=='\b':
            if chars:chars.pop();print('\b \b',end='',flush=True)
        elif ch.isprintable() and len(chars)<128:chars.append(ch);print(ch,end='',flush=True)
    raise TimeoutError('UI observation budget exceeded')
def verify_approval(approval,c):
    mode_contract(c)
    a=read(approval);manifest=HERE/'CODE_MANIFEST.json'
    if a.get('stored_policy_evidence_accepted') is not True or a.get('effective_policy_unverified_accepted') is not True:raise ValueError('Revised policy evidence scope must be explicitly accepted')
    if a.get('phase')!='B' or a.get('approved') is not True or a.get('code_manifest_sha256')!=sha(manifest):raise ValueError('Separate sealed B approval required')
    if a.get('run_id')!=c['run_id'] or a.get('budgets_seconds')!=c['budgets_seconds']:raise ValueError('Run/budget approval mismatch')
    for k in ('all_files_scope_accepted','two_preferences_UI_sessions','no_elevation','no_solve'):
        if a.get(k) is not True:raise ValueError('Missing explicit approval: '+k)
    if c.get('B_path_ready') is not True:raise ValueError('B path binding unresolved; separate Java-path approval required')
    for r in read(manifest)['files']:
        if sha(HERE/r['file'])!=r['sha256'] or (HERE/r['file']).stat().st_size!=r['bytes']:raise ValueError('Prepared code/dependency mismatch: '+r['file'])
    for k in ('formal_command_approval_required','child_sequence_scope_accepted','prior_pending_preserved','current_prefs_source_accepted','owned_job_termination_accepted'):
        if a.get(k) is not True:raise ValueError('Missing A3 approval: '+k)
    return a

class Runner:
    def __init__(self,c,transport,attest=None):
        self.c=c;self.t=transport;self.attest=attest;self.root=fixed_paths(c);self.state_path=self.root/'state.json'
        self.events=EventStore(self.root,c['run_id'])
        self.state={'schema':2,'recording_errors':[],'run_id':c['run_id'],'cleanup_pending':True,'policy_restore':'NOT_STARTED','process_cleanup':'NOT_STARTED',
            'preservation':'NOT_STARTED','numeric_recovery':'NOT_STARTED','sampled_comparison':'NOT_STARTED','errors':[],
            'attempts':{'apply':0,'compile':0,'batch':0,'restore':0},'original_workers':'failed','normal_gate':'INCOMPLETE'}
    def record_failure(self,where,e):
        issue={'where':where,'error':type(e).__name__+': '+str(e)}
        self.state.setdefault('recording_errors',[]).append(issue)
        self.state['cleanup_pending']=True
        self.state['overall']='INCOMPLETE'
        # Diagnostic only, one fixed path and no overwrite/fallback. Never authorizes another phase.
        try:
            with (self.root/'recording_failure.json').open('x',encoding='utf-8') as f:
                json.dump({'run_id':self.c['run_id'],'first_recording_error':issue,'diagnostic_only':True},f);f.flush();os.fsync(f.fileno())
        except BaseException as emergency_error:
            self.state.setdefault('emergency_errors',[]).append(str(emergency_error))
    def save(self,**kw):
        self.state.update(kw)
        if self.state.get('recording_errors'):self.state.update(cleanup_pending=True,overall='INCOMPLETE')
        try:write(self.state_path,self.state)
        except BaseException as e:self.record_failure('summary',e)
    def error(self,phase,e):
        self.state['errors'].append({'phase':phase,'error':str(e)});self.save()
    def record_process(self,name,value):
        kind=value.get('event')
        if kind in ('root','assignment','resume'):
            try:self.events.append(name,kind,{k:v for k,v in value.items() if k!='event'})
            except BaseException as e:
                self.record_failure('required_'+kind,e);raise
        if 'root_pid' in value:self.state.setdefault('phase_roots',{}).setdefault(name,{}).update(value)
        row={'phase':name,'monotonic':time.monotonic(),'observation':value}
        try:
            with (self.root/'evidence/process_journal.jsonl').open('a',encoding='utf-8') as f:
                f.write(json.dumps(row,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
        except BaseException as e:self.record_failure('poll_journal',e)
        self.save(process_observation=value)
    def observe(self,prompt,deadline):return self.attest(prompt) if self.attest is not None else timed_attest(prompt,deadline-time.monotonic())
    def require_phase_cleanup(self):
        issues=phase_cleanup_issues(self.state)
        if any(self.state['attempts'].values()):
            try:require_terminal_evidence(self.root,self.state)
            except Exception as e:issues.append(str(e))
        if self.events.failed:issues.append('Required event durability unresolved')
        if issues or self.state.get('ownership_unresolved'):
            self.save(process_cleanup='INCOMPLETE',cleanup_pending=True,ownership_unresolved=True,phase_cleanup_issues=issues)
            raise RuntimeError('Owned process cleanup unresolved; no new phase launch: '+'; '.join(issues))
    def final_process_check(self,label):
        # Persist pending before a fallible query, including interruption during that query.
        self.save(process_cleanup='INCOMPLETE',cleanup_pending=True,final_process_query={'status':'UNKNOWN','context':label})
        issues=phase_cleanup_issues(self.state)
        if issues:self.save(ownership_unresolved=True,phase_cleanup_issues=issues)
        try:
            census=self.t.census()
            if not isinstance(census,list):raise RuntimeError('Process census result unavailable')
        except Exception as e:
            self.error(label+'_process_query',e);return
        self.save(final_process_query={'status':'PASS' if not census else 'LIVE_OR_UNATTRIBUTED','context':label,'census':census},
            process_cleanup='PASS' if not census and not issues and not self.state.get('ownership_unresolved') else 'INCOMPLETE')
    def phase(self,name,seconds):
        phase_started=time.monotonic();phase_utc=utc()
        if self.state['attempts'][name]:raise RuntimeError('No retry: '+name)
        self.require_phase_cleanup()
        if name!='restore' and self.state.get('recording_errors'):raise RuntimeError('Recording failure blocks new compute phase')
        # Durable reservation before process creation: ambiguous starts consume the attempt.
        self.state['attempts'][name]=1
        try:self.events.append(name,'reservation',{'argv_sha256':record_digest(self.c['commands'][name]),'cwd':str(self.root/'compile' if name=='compile' else self.root),'source_sha256':self.c['source_sha256']})
        except BaseException as e:
            self.record_failure('required_reservation',e);self.save();raise
        self.save(phase=name,process_cleanup='INCOMPLETE',cleanup_pending=True,process_observation={})
        if self.state.get('recording_errors') and name!='restore':raise RuntimeError('Reservation summary failure; attempt consumed')
        cwd=self.root/'compile' if name=='compile' else self.root
        try:
            result=self.t.run(self.c['commands'][name],cwd,self.root/'logs'/f'{name}_console.log',seconds,
                self.c['budgets_seconds']['process_cleanup'],lambda v:self.record_process(name,v),visible=name in ('apply','restore'))
        except BaseException as e:
            self.save(process_cleanup='INCOMPLETE',ownership_unresolved=True)
            self.error(name+'_transport',e)
            raise
        result=dict(result)
        result['recording_errors']=list(result.get('recording_errors',[]))+list(self.state.get('recording_errors',[]))
        self.state[name+'_process']=result
        try:self.events.append(name,'terminal',result)
        except BaseException as e:
            self.record_failure('required_terminal',e);self.state['ownership_unresolved']=True;self.save();raise
        issues=phase_cleanup_issues(self.state)
        if issues:self.state['ownership_unresolved']=True
        self.save(phase_cleanup_issues=issues,process_cleanup='PASS' if not issues and not self.state.get('ownership_unresolved') else 'INCOMPLETE')
        if not cleanup_evidence_ok(result):result=dict(result,cleanup='INCOMPLETE')
        if name=='batch' and result.get('timeout'):self.save(java_after_U='INCOMPLETE_UNLESS_SEPARATELY_VALIDATED; forced termination does not run finally')
        sources=[self.root/'logs'/f'{name}_console.log']
        if name=='batch':sources.append(self.root/'logs'/'batch.log')
        observed={}
        for path in sources:
            if path.is_file():
                text,encoding=decoded_log(path)
                observed[path.name]={'sha256':sha(path),'bytes':path.stat().st_size,'classification':classify_process(result,text),'decoded_as':encoding}
        log='\n'.join(decoded_log(path)[0] for path in sources if path.is_file())
        outcome=classify_process(result,log)
        if outcome=='PROCESS_OK' and len(observed)!=len(sources):outcome='NATIVE_LOG_MISSING'
        self.save(**{name+'_outcome':outcome,name+'_log_diagnostics':observed})
        elapsed=time.monotonic()-phase_started
        self.state.setdefault('phase_metrics',{})[name]={'started_at':phase_utc,'completed_at':utc(),'elapsed_seconds':elapsed,'limit_seconds':seconds,'observed':True,'budget_compliant':elapsed<=seconds}
        self.save()
        if time.monotonic()-phase_started>seconds:raise RuntimeError('Phase budget exceeded after final record: '+name)
        recording_only_restore=(name=='restore' and outcome=='PROCESS_ERROR' and classify_process(dict(result,recording_errors=[]),log)=='PROCESS_OK' and len(observed)==len(sources))
        if outcome!='PROCESS_OK' and not recording_only_restore:raise RuntimeError(outcome)
        if name=='batch' and not (self.root/'logs'/'batch.log').is_file():raise RuntimeError('Native batch log missing')
        if name=='batch':
            cores=re.findall(r'with\s+(\d+)\s+cores in total',log)
            self.save(actual_core_log_values=cores)
            if not cores or set(cores)!={str(self.c['resource_start']['cores'])}:raise RuntimeError('Actual core log missing/differs; do not infer from argv')
    def restore(self):
        self.require_phase_cleanup()
        # A failed final query never authorizes a second UI restore.
        if self.state.get('policy_restore')=='PASS':return
        if not self.state.get('policy_may_have_changed'):
            if not any(self.state['attempts'].values()) and not self.t.census():self.save(process_cleanup='PASS')
            self.save(policy_restore='PASS');return
        if self.t.census():raise RuntimeError('Live/unattributed COMSOL process: manual ownership resolution required; no name kill')
        deadline=time.monotonic()+self.c['budgets_seconds']['restore']
        self.phase('restore',deadline-time.monotonic())
        if self.observe('Restore-only UI: returned File system access to its original label; no model opened. Type RESTORED: ',deadline)!='RESTORED':raise RuntimeError('Restore observation missing')
        current=security(self.root/'prefs/comsol.prefs');policy_delta(self.state['security_before'],current,restore=True)
        write(self.root/'evidence/policy_after.json',{'security':current,'sha256':sha(self.root/'prefs/comsol.prefs'),'model_loads_reported':0})
        self.save(policy_restore='PASS')
        if time.monotonic()>deadline:
            self.save(policy_restore='INCOMPLETE');raise RuntimeError('Restore budget exceeded after final evidence')
    def execute(self):
        if self.c.get('usable') is not True or self.c.get('B_path_ready') is not True:raise RuntimeError('Offline candidate not authorized for native execution')
        mode_contract(self.c)
        # Never reuse a directory, including a prior complete or partial run.
        if self.root.exists():raise RuntimeError('Existing run/pending: inspect; do not resubmit')
        identity=self.t.identity()
        if identity.get('elevated') is not False:raise RuntimeError('Elevation/identity unclear')
        if self.t.census():raise RuntimeError('Existing COMSOL work; do not interfere')
        no_pending_jobs(self.c)
        resource=self.t.resources(Path(self.c['source_java']).parent)
        if resource['available_ram_bytes']<self.c['resource_start']['available_ram_gib']*2**30 or resource['free_disk_bytes']<self.c['resource_start']['free_disk_gib']*2**30:raise RuntimeError('Resource start condition not met')
        identities(self.c)
        source=self.c['default_prefs_source']
        if security(Path(self.c['default_prefs']))!=source['security']:raise RuntimeError('Current prefs security differs from sealed A3 source')
        expected=source['identity'];default_path=Path(self.c['default_prefs'])
        if sha(default_path)!=expected['sha256'] or default_path.stat().st_size!=expected['bytes']:raise RuntimeError('Current prefs identity differs from sealed A3 source')
        self.root.mkdir(parents=True,exist_ok=False)
        for p in self.c['paths'].values():Path(p).mkdir(exist_ok=False)
        self.save(identity=identity,resource_start=resource)
        write(self.root/'evidence/prior_pending_reconciliation.json',{
            'old_state_preserved':self.c.get('prior_incomplete',{}),'current_no_comsol_census':True,
            'current_protected_identities_checked':True,'new_run_id':self.c['run_id'],
            'old_pending_cleared':False,'scope':'THIS approved B attempt only; old procedure remains INCOMPLETE'})
        write(self.root/'evidence/execution_context.json',{
            'planned_context':self.c.get('execution_context',{}),'actual_runner_identity':identity,
            'tool_allowance_verified_by_python':False,
            'note':'Tool approval is external to this script. Preserve platform event separately when available; this file is not a tool receipt.'})
        default=Path(self.c['default_prefs'])
        try:
            write(self.root/'evidence/protected_before.json',identities(self.c))
            before=security(default);self.save(security_before=before)
            # Explicit B-only local copy, never in A tests or public handoff.
            shutil.copyfile(default,self.root/'prefs/comsol.prefs')
            self.save(policy_may_have_changed=True,policy_restore='INCOMPLETE')
            apply_deadline=time.monotonic()+self.c['budgets_seconds']['apply']
            self.phase('apply',apply_deadline-time.monotonic())
            if self.observe('Apply UI: All files selected; Enforce retained; no model opened. Type ALL_FILES: ',apply_deadline)!='ALL_FILES':raise RuntimeError('Apply observation missing')
            after=security(self.root/'prefs/comsol.prefs');policy_delta(before,after)
            self.save(security_applied=after,effective_policy_readback='UNVERIFIED',configured_policy_binding='INCOMPLETE')
            save_snapshot(self.c,'after_apply')
            identities(self.c)
            write(self.root/'evidence/policy_applied.json',{'security':after,'sha256':sha(self.root/'prefs/comsol.prefs'),'model_loads_reported':0,'UI_label_reported':'All files'})
            (self.root/'permission_token.txt').write_text(after['security.external.filepermission']+'\n',encoding='utf-8')
            if sha(self.c['source_java'])!=self.c['source_sha256']:raise RuntimeError('Prepared source changed before staging')
            shutil.copyfile(self.c['source_java'],self.root/'compile/StoredSolutionRecoveryA.java')
            if sha(self.root/'compile/StoredSolutionRecoveryA.java')!=self.c['source_sha256']:raise RuntimeError('Staged source mismatch')
            deadline=time.monotonic()+self.c['budgets_seconds']['compile_batch']
            self.phase('compile',deadline-time.monotonic())
            compiled=self.root/'compile/StoredSolutionRecoveryA.class'
            if not compiled.is_file() or compiled.stat().st_size==0:raise RuntimeError('Class missing after compile')
            class_check=validate_tree(self.root/'compile',self.c['source_sha256'])
            write(self.root/'evidence/class_artifacts.json',class_check)
            classes=sorted((self.root/'compile').glob('*.class'))
            identities(self.c)
            if sha(self.root/'compile/StoredSolutionRecoveryA.java')!=self.c['source_sha256']:raise RuntimeError('Source changed during compilation')
            write(self.root/'batch_authorized.json',{'run_id':self.c['run_id'],'classes':{p.name:sha(p) for p in classes},'source_sha256':sha(self.c['source_java'])})
            bound_batch(self,deadline)
            self.save(numeric_recovery='PENDING_OFFLINE')
        except BaseException as e:self.error(self.state.get('phase','prepare'),e)
        finally:
            try:
                write(self.root/'evidence/protected_after.json',identities(self.c));self.save(preservation='PASS')
            except Exception as e:self.save(preservation='INCOMPLETE');self.error('external_preservation',e)
            try:self.restore()
            except Exception as e:self.save(policy_restore='INCOMPLETE');self.error('policy_restore',e)
            try:
                identities(self.c)
            except Exception as e:self.save(preservation='INCOMPLETE');self.error('post_restore_preservation',e)
            self.final_process_check('post_restore')
            self.save(cleanup_pending=not(self.state['process_cleanup']=='PASS' and self.state['policy_restore']=='PASS'),overall='INCOMPLETE')
        return self.state
    def cleanup_only(self):
        self.state=read_status(self.state_path)
        try:self.events.events=__import__('execution_records').load_events(self.root,self.c['run_id'])
        except Exception as e:self.events.failed=True;self.record_failure('reentry_events',e)
        if self.state.get('run_id')!=self.c['run_id']:raise RuntimeError('Pending identity mismatch')
        try:self.require_phase_cleanup()
        except RuntimeError as e:self.error('cleanup_only',e);return self.state
        if not self.state.get('cleanup_pending'):return self.state
        if self.t.identity().get('elevated') is not False:raise RuntimeError('Elevation unclear')
        try:self.restore()
        except Exception as e:self.error('cleanup_only',e)
        try:identities(self.c)
        except Exception as e:self.save(preservation='INCOMPLETE');self.error('cleanup_preservation',e)
        self.final_process_check('cleanup')
        self.save(cleanup_pending=not(self.state['process_cleanup']=='PASS' and self.state['policy_restore']=='PASS'))
        return self.state

def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['plan','pending','execute','cleanup'],nargs='?',default='plan');p.add_argument('--approval');args=p.parse_args()
    c=read(HERE/'contract.json');root=fixed_paths(c)
    if args.action=='plan':print(json.dumps(c['commands'],indent=2));return
    if args.action=='pending':print(json.dumps(read_status(root/'state.json') if (root/'state.json').exists() else {'pending':'UNKNOWN_DIRECTORY' if root.exists() else 'NO_RUN_DIRECTORY'},indent=2));return
    if not args.approval:raise SystemExit('B approval absent; no COMSOL action')
    verify_approval(args.approval,c)
    from winjob import WindowsJobTransport
    runner=Runner(c,WindowsJobTransport())
    result=runner.execute() if args.action=='execute' else runner.cleanup_only()
    print(json.dumps(result,indent=2))
    if result.get('errors') or result.get('cleanup_pending'):raise SystemExit(1)
if __name__=='__main__':main()
