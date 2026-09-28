"""One inert suite. Source/engine/case seal must exist before invocation."""
from pathlib import Path
import sys,os,json,time,hashlib,types,csv,io,base64,copy,ast,contextlib
from decimal import Decimal as D
R=Path(__file__).resolve().parent.parent; S=R.parent/'guard1198_limited_validation_R1_20260928'
def reject_native(event,args):
    if event in ('subprocess.Popen','os.system','os.startfile','ctypes.dlopen') or event.startswith('winreg.'):
        raise RuntimeError('INERT_NATIVE_BOUNDARY:'+event)
sys.addaudithook(reject_native)
queue=[];ms=types.ModuleType('msvcrt');ms.kbhit=lambda:bool(queue);ms.getwch=lambda:queue.pop(0);sys.modules['msvcrt']=ms
wj=types.ModuleType('winjob');sys.modules['winjob']=wj
def load(name,p):
    m=types.ModuleType(name);m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def ident(p):
    raw=Path(p).read_bytes();return {'path':Path(p).resolve().as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def put(p,obj):p.write_text(json.dumps(obj),'utf-8')
seal=json.loads((R/'PRE_TEST_SEAL.json').read_text());
for p in seal['files']:
    assert ident(p['path'])==p,'SEAL_CHANGED'
C=load('consumer',S/'src/trigger_consumer.py');E=load('entry',S/'src/candidate_entry.py')
original_source_module=E.source_module
cfg=json.loads((S/'CONTRACT.json').read_text());MH=hashlib.sha256((S/'CODE_MANIFEST.json').read_bytes()).hexdigest()
F=R/'fixtures';assert not F.exists();F.mkdir()
results=[];observations=[];begin=time.monotonic();counter=0
def expect(fn,reason):
    try:fn()
    except Exception as e:
        assert reason in str(e),(reason,type(e).__name__,str(e));observations.append({'type':type(e).__name__,'reason':str(e),'expected_reason':reason});return
    raise AssertionError('EXPECTED_REJECTION:'+reason)
def csvbytes(headers,rows):
    out=io.StringIO(newline='');w=csv.writer(out,lineterminator='\n');w.writerow(headers);w.writerows(rows);return out.getvalue().encode()
def fixture():
    global counter
    counter+=1;p=F/('f%03d'%counter);p.mkdir();c=copy.deepcopy(cfg);c['run_root']=p.as_posix();c['requested_times_s']=['0','0.0001','0.0002'];ts=['0','0.0001','0.0002'];tables={}
    tables['guard_binding.csv']=csvbytes(C.HEADERS['guard_binding.csv'],[[c['guard_expression'],'stepbefore_stepafter','on','true','1198.0']])
    tables['electrolyte_guard.csv']=csvbytes(C.HEADERS['electrolyte_guard.csv'],[[t,v,v,v+1,v+2,1198,int(v<=1198),0,0] for t,v in zip(ts,[1200,1199,1197])])
    tables['preflight_global.csv']=csvbytes(C.HEADERS['preflight_global.csv'],[[t,1,1,1,.5,.5,.5,.5,.5,.5,0,0,0,0] for t in ts])
    for n,v in [('preflight_boundary1.csv',0),('preflight_boundary4.csv',2)]:tables[n]=csvbytes(C.HEADERS[n],[[t,v,0,v,0,0,.5,.5,1,1,2,v,0] for t in ts])
    for electrode,domain in [('N',1),('P',3)]:
        n='axes_profile_'+electrode+'.csv';tables[n]=csvbytes(C.HEADERS[n],[[t,x,.5,.5,0,0,0,domain] for t in ts for x in c['coordinates'][electrode]])
    units={'eguard':['s']+['mol/m^3']*5+['1']*3,'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],'point4':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],'MinLinece':['s','mol/m^3'],'MaxLinece':['s','mol/m^3'],'profiletimes':['s'],'profileN':['s','m','1','1','V','V','V','1'],'profileP':['s','m','1','1','V','V','V','1']}
    for tag,u in units.items():
        for phase in (['inferred','configured','evaluated'] if tag=='eguard' else ['configured','evaluated']):
            v=u.copy()
            if phase!='configured':
                for i in ([6,7,8] if tag=='eguard' else [10] if tag=='nglobal' else [7] if tag in ('profileN','profileP') else []):v[i]=''
            txt='['+', '.join(v)+']';tables['units_'+tag+'_'+phase+'.csv']=csvbytes(['tag','phase','expected','actual'],[[tag,phase,txt,txt]])
    base=p/'baseline';base.mkdir();c['baseline_files']={}
    for n in ['electrolyte_guard.csv','preflight_global.csv','preflight_boundary1.csv','preflight_boundary4.csv','axes_profile_N.csv','axes_profile_P.csv']:
        (base/n).write_bytes(tables[n]);c['baseline_files'][n]=ident(base/n)
    state={'run_id':c['run_id'],'code_manifest_sha256':MH,'start':time.monotonic(),'status':'NATIVE_RETURN_READY','errors':[],'preservation':'PASS','process_cleanup':'PASS','policy_preservation':'PASS'}
    batch='<---- Time-Dependent Solver 1\n'+''.join(str(i)+' '+t+' 0.0001 out x\n' for i,t in enumerate(ts))+'Information: Stop condition fulfilled at t = 0.0002 ('+c['stop_description']+').\n----- Time-Dependent Solver 1 ----->\n'
    prefix='\n'.join('ELECTROLYTE_COUPLING='+tag+'|dimension=1|entities='+sel+'|points=lagrange|lagrange=5' for tag,sel in [('minguardall','[1, 2, 3]'),('minguard1','[1]'),('minguard2','[2]'),('minguard3','[3]')])+'\nGUARD1198_PRODUCER_COMPLETE\n'
    return p,c,state,batch,prefix,tables
def run_analysis(f,mutate=None,expected=None,record_failure=False):
    p,c,state,batch,prefix,tables=f
    if mutate:batch,prefix=mutate(tables,batch,prefix)
    put(p/'NATIVE_STATE.json',state);(p/'batch.log').write_text(batch,'utf-8');(p/'batch_console.log').write_text(prefix+''.join('AUDIT_TABLE_BASE64='+n+'|'+base64.b64encode(raw).decode()+'\n' for n,raw in tables.items()),'utf-8')
    old=E.save
    if record_failure:E.save=lambda *a:(_ for _ in ()).throw(OSError('RECORD_FAILURE'))
    out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out):rc=E.analyze(c,MH)
    finally:E.save=old
    result=json.loads(out.getvalue().splitlines()[-1])['analysis_result']
    assert all(k in result for k in E.incomplete_result()),'SCHEMA'
    observations.append({'path':'candidate_entry.analyze -> trigger_consumer.analyze/extract_tables','return_code':rc,'limited_result':result['limited_result'],'errors':result['errors']})
    if expected:
        assert rc==1 and result['limited_result']=='INCOMPLETE' and expected in json.dumps(result['errors']) and 'KeyError' not in json.dumps(result['errors']),result
    else:assert rc==0 and result['limited_result']=='TRIGGER_AND_SAMPLED_DATA_ACCEPTABLE',result
    return result
def case(group,name,fn):
    assert time.monotonic()-begin<90,'SUITE_BUDGET'
    before=len(observations)
    try:fn();results.append({'group':group,'case':name,'status':'PASS','observed':observations[before:]})
    except BaseException as e:results.append({'group':group,'case':name,'status':'FAIL','type':type(e).__name__,'error':str(e),'observed':observations[before:]});raise
def failtable(name,change):
    def f(t,b,p):t[name]=change(t[name]);return b,p
    return f
def guards():
    p,c,s,b,prefix,t=fixture();dest=p/'direct';dest.mkdir()
    for n,raw in t.items():(dest/n).write_bytes(raw)
    return c,C.timed(dest/'electrolyte_guard.csv'),dest
def authorize(c,p):
    aroot=p/'fixture_auth';aroot.mkdir();decision=aroot/'decision.txt';decision.write_text('INERT FIXTURE ONLY')
    proof=aroot/'proof.txt';proof.write_text('INERT TEST PROOF')
    c['approval_path']=(aroot/'approval.json').as_posix();c['release_path']=(aroot/'release.json').as_posix()
    release={'code_manifest_sha256':MH,'run_id':c['run_id'],'changed_branch_validation':'PASS','native_permission_route_reviewed':True,'manifest_bytes_unchanged_since_validation':True,'validation_evidence':[ident(proof)]};put(Path(c['release_path']),release)
    a={'code_manifest_sha256':MH,'run_id':c['run_id'],'approved':True,'native1198_one_shot':True,'allow_policy_changes':False,'effective_policy_unverified_accepted':True,'commands':c['commands'],'budgets_seconds':c['budgets_seconds'],'validation_release':ident(Path(c['release_path'])),'user_decision':ident(decision)};put(Path(c['approval_path']),a);return a,release
def good_process():return dict(started=True,rc=0,timeout=False,cleanup='PASS',ownership_verified=True,root_exit_observed=True,exit_query_succeeded=True,handles_closed=True,remaining_owned=[],unattributed_comsol=[],original_error=None,cleanup_errors=[],recording_errors=[],termination_request=None,cleanup_elapsed_seconds=0.,elapsed_seconds=.01)
def inert_execute(mode):
    p,c,s,b,prefix,t=fixture();c['run_root']=(p/'run').as_posix();c['cwd']=p.as_posix();prefs=p/'fixture.prefs';prefs.write_text('security.external.enable=on\nsecurity.test=fixture\n');c['policy']['default_prefs_path']=prefs.as_posix()
    a,_=authorize(c,p);a['default_prefs_identity']=ident(prefs);put(Path(c['approval_path']),a)
    legacy=json.loads(Path(c['legacy_contract']['path']).read_bytes());gate=load('legacy_gate',Path(c['legacy_gate']['path']))
    launcher_source=Path(legacy['base_root'])/'launcher.py';tree=ast.parse(launcher_source.read_text('utf-8-sig'));node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='timed_attest');body=ast.get_source_segment(launcher_source.read_text('utf-8-sig'),node)
    namespace={'os':types.SimpleNamespace(name='nt'),'sys':types.SimpleNamespace(stdin=types.SimpleNamespace(isatty=lambda:True)),'time':time};exec(compile(body,'sealed:launcher.timed_attest','exec'),namespace)
    class Adapter:
        def environment(self):return dict(executable=legacy['python']['path'],python_sha256=legacy['python']['sha256'],cwd=legacy['base_root'],startup_options_ok=True,os_name='nt')
        def identity(self):return dict(user='fixture\\bml',sid='S-1-fixture',elevated=False)
        def console(self):return dict(stdin_isatty=True,crt_input_mode_ok=True,std_input_mode_ok=True)
        def pending_input(self):return False
        def nonce(self):
            prefix='C2_INPUT_' if not getattr(self,'second',False) else 'C2_RETURN_';self.second=True;queue.extend(prefix+'12345678\r');return '12345678'
    class App:
        launcher=types.SimpleNamespace(timed_attest=namespace['timed_attest'])
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def recheck(self):E.seal(MH)
    gate.NativeAdapter=Adapter;gate.VerifiedApplications=lambda c:App()
    E.source_module=lambda name,path,pin:gate if name=='_guard1198_existing_c2' else original_source_module(name,path,pin)
    calls=[]
    class Transport:
        def resources(self,root):return {'free_disk_bytes':20*2**30,'available_ram_bytes':1}
        def census(self):return []
        def run(self,argv,cwd,log,*rest):
            phase='compile' if not calls else 'batch';calls.append(phase);run=Path(cwd);Path(log).write_text('fixture','utf-8');res=good_process()
            observations.append({'path':'inert_transport_arguments','phase':phase,'argv':argv,'expected_argv':c['commands'][phase],'cwd':cwd,'expected_cwd':str(Path(c['run_root']))})
            assert argv==c['commands'][phase] and cwd==str(Path(c['run_root'])),'EXACT_ARGV_CWD'
            if phase=='compile':(run/'Guard1198Candidate.class').write_bytes(b'\xca\xfe\xba\xbeFIXTURE')
            else:(run/c['expected_mph_name']).write_bytes(b'INERT_NOT_MPH');(run/'batch.log').write_text('fixture')
            if mode=='compile_fail' and phase=='compile':res['rc']=7
            if mode=='cleanup_fail':res['cleanup']='INCOMPLETE';res['cleanup_errors']=['FIXTURE_CLEANUP']
            if mode=='policy_changed':(run/'prefs/comsol.prefs').write_text('security.external.enable=off')
            if mode=='stale_class':(run/'EXTRA.class').write_bytes(b'\xca\xfe\xba\xbeFIXTURE')
            if mode=='staged_changed':(run/'Guard1198Candidate.java').write_text('FIXTURE_CHANGED')
            if mode=='output_missing' and phase=='batch':(run/c['expected_mph_name']).unlink()
            return res
    wj.WindowsJobTransport=Transport;cwd=Path.cwd();os.chdir(p);E.ENTRY_START=time.monotonic()
    try:
        with contextlib.redirect_stdout(io.StringIO()):rc=E.execute(c,a,MH)
    finally:os.chdir(cwd);E.source_module=original_source_module
    state=json.loads((Path(c['run_root'])/'NATIVE_STATE.json').read_text());gate_record=json.loads((Path(c['run_root'])/'GATE.json').read_text());assert len(gate_record['answers'])==2
    if mode=='normal':assert rc==0 and calls==['compile','batch'],state
    else:assert rc==1 and state['errors'] and calls==(['compile','batch'] if mode=='output_missing' else ['compile']),state
    if mode=='cleanup_fail':assert len(state['errors'])>=2,state
    observations.append({'path':'candidate_entry.execute -> original input_gate/timed_attest -> inert transport','mode':mode,'rc':rc,'argv_calls':calls,'gate_answers':len(gate_record['answers']),'errors':state['errors']})
try:
    case('PY01','complete_actual_entry_consumer',lambda:put(R/'records/positive_result.json',run_analysis(fixture())))
    case('PY02','binding_schema_no_KeyError',lambda:run_analysis(fixture(),failtable('guard_binding.csv',lambda x:x.replace(b'stepbefore_stepafter',b'wrong')), 'GUARD_BINDING_VALUE'))
    case('PY02','guard_schema_no_KeyError',lambda:run_analysis(fixture(),failtable('electrolyte_guard.csv',lambda x:x.replace(b'1198,0,0,0',b'1198,0,1,0')), 'OTHER_GUARD_OR_BOOLEAN'))
    case('PY03','wrong_stop_reason',lambda:run_analysis(fixture(),lambda t,b,p:(b.replace(cfg['stop_description'],'WRONG'),p),'NATIVE_STOP_REASON'))
    case('PY03','native_fatal',lambda:run_analysis(fixture(),lambda t,b,p:(b+'\nError running java class.\n',p),'NATIVE_FATAL'))
    case('PY03','producer_completion_missing',lambda:run_analysis(fixture(),lambda t,b,p:(b,p.replace('GUARD1198_PRODUCER_COMPLETE','')),'PRODUCER_OUTPUT_FAILURE'))
    case('PY03','integration_after_stop',lambda:run_analysis(fixture(),lambda t,b,p:(b+'3 0.0003 0.0001 out x\n',p),'INTEGRATION_AFTER_STOP'))
    case('PY04','stored_count',lambda:run_analysis(fixture(),lambda t,b,p:(b.replace('1 0.0001 0.0001 out x\n',''),p),'NATIVE_STORED_STEP_COUNT'))
    case('PY04','stored_time_mismatch',lambda:run_analysis(fixture(),lambda t,b,p:(b.replace('1 0.0001 0.0001','1 0.0009 0.0001'),p),'NATIVE_STORED_TIME_BINDING'))
    case('PY05','missing_strict_prefix',lambda:expect(lambda:C.coverage({'requested_times_s':['0','.1','.2']},[D(0),D('.2')],[D(0),D('.1'),D('.2')],D('.2')),'STRICT_REQUEST_TIME_MISSING'))
    case('PY06','zero_only',lambda:expect(lambda:C.coverage({'requested_times_s':['0']},[D(0)],[D(0)],D(0)),'INSUFFICIENT_REQUEST_PREFIX'))
    case('PY06','empty_common',lambda:expect(lambda:C.coverage({'requested_times_s':[]},[],[],D(0)),'INSUFFICIENT_REQUEST_PREFIX'))
    case('PY07','nonfinite_csv',lambda:run_analysis(fixture(),failtable('electrolyte_guard.csv',lambda x:x.replace(b'1200',b'NaN')),'NONFINITE'))
    case('PY07','duplicate_time',lambda:run_analysis(fixture(),failtable('electrolyte_guard.csv',lambda x:x.replace(b'0.0001,',b'0,')),'DUPLICATE_OR_UNORDERED_TIME'))
    case('PY07','profile_domain',lambda:run_analysis(fixture(),failtable('axes_profile_N.csv',lambda x:x.replace(b',1\n',b',3\n')),'PROFILE_COORD_DOMAIN'))
    def tie():
        c,g,_=guards();g[D(0)]['ce_min_d2_mol_m3']=D(1200);g[D(0)]['ce_min_d3_mol_m3']=D('1200.0000000001');r=C.guard_evidence(c,g);assert r['ties'][0]['exact_minimum_domains']==[1,2] and r['ties'][0]['near_tie_domains']==[3]
    case('PY08','exact_near_ties',tie)
    case('PY08','wrong_unit',lambda:run_analysis(fixture(),failtable('units_profileN_evaluated.csv',lambda x:x.replace(b'V',b'A')),'UNIT_STAGE'))
    case('PY09','Li_drift',lambda:run_analysis(fixture(),failtable('preflight_global.csv',lambda x:x.replace(b'0.0002,1,1,1',b'0.0002,2,1,1')),'LI_DRIFT'))
    case('PY09','voltage_identity',lambda:run_analysis(fixture(),failtable('preflight_boundary4.csv',lambda x:x.replace(b'0.0002,2,0,2,',b'0.0002,3,0,2,')),'VOLTAGE_IDENTITY'))
    def auth():
        p,c,*_=fixture();a,rel=authorize(c,p);assert E.permission(c,MH,c['approval_path'])==a
        a['approved']=False;put(Path(c['approval_path']),a);expect(lambda:E.permission(c,MH,c['approval_path']),'SEPARATE_NATIVE_APPROVAL')
        a['approved']=True;put(Path(c['approval_path']),a);rel['validation_evidence']=[];put(Path(c['release_path']),rel);expect(lambda:E.permission(c,MH,c['approval_path']),'VALIDATION_EVIDENCE_EMPTY')
    case('PY10','fixture_authorization',auth)
    case('PY11','actual_entry_and_original_two_input_bodies',lambda:inert_execute('normal'))
    case('PY12','compile_failure_stops_batch',lambda:inert_execute('compile_fail'))
    case('PY12','stale_extra_class',lambda:inert_execute('stale_class'))
    case('PY12','batch_output_missing',lambda:inert_execute('output_missing'))
    case('PY13','cleanup_primary_secondary',lambda:inert_execute('cleanup_fail'))
    case('PY13','private_policy_changed',lambda:inert_execute('policy_changed'))
    case('PY13','staged_source_changed',lambda:inert_execute('staged_changed'))
    case('PY14','extraction_failure_schema',lambda:run_analysis(fixture(),lambda t,b,p:(t.clear() or b,p),'NO_TABLES'))
    case('PY14','record_error_preserves_trigger_error',lambda:run_analysis(fixture(),failtable('guard_binding.csv',lambda x:x.replace(b'stepbefore_stepafter',b'wrong')),'GUARD_BINDING_VALUE',True))
    def budget():
        f=fixture();f[2]['start']-=3001;run_analysis(f,expected='OVERALL_BUDGET')
    case('PY14','overall_budget',budget)
finally:
    put(R/'records/PYTHON_RESULT.json',{'results':results,'elapsed_seconds':time.monotonic()-begin,'groups_passed':sorted({x['group'] for x in results if x['status']=='PASS'}),'native_calls':0})
print(json.dumps({'status':'PASS','subcases':len(results),'groups':14,'seconds':time.monotonic()-begin}))
