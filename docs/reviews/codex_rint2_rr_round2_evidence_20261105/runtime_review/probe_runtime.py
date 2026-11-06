"""Independent synthetic review, Windows/Python 3.12. No real R inputs or solver.
Linux identity/containment checks use explicit /proc fixtures or mocks.
Git mutations are confined to this evidence directory's scratch repositories.
The ledger_lock replacement is deliberately single-threaded and DOES NOT test flock.
"""
import contextlib, copy, hashlib, inspect, io, json, os, platform, subprocess, sys, types, time
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / 'received' / 'repo'
sys.path.insert(0, str(REPO / 'scripts'))
import rint_r_chain as r
import rint_first_result as fr

SCRATCH = HERE / ('scratch_' + str(time.time_ns()))
SCRATCH.mkdir(exist_ok=True)
# Windows ownership mismatch workaround on actual Git invocations only. No global config.
# Production ledger strips GIT_* environment; preserve its actual command except for this flag.
original_run = subprocess.run
def safe_git_run(argv,*a,**k):
    if isinstance(argv,list) and argv[:2]==['git','-C'] and Path(argv[2]).resolve().is_relative_to(SCRATCH.resolve()):
        argv=argv[:3]+['-c','safe.directory='+str(Path(argv[2]).resolve()).replace('\\','/')]+argv[3:]
    return original_run(argv,*a,**k)
subprocess.run=safe_git_run
ROWS=[]
def ck(name, got, expected):
    ROWS.append({'name':name,'pass':got==expected,'got':got,'expected':expected})
    if got != expected: print('FAIL',name,repr(got),'!=',repr(expected))
def write(p, o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(r.canon_bytes(o))
def mkdir(n):
    p=SCRATCH/n; p.mkdir(parents=True,exist_ok=True); return p
HOST={'machine_id':'review-machine','boot_id':'review-boot','pidns':'pid:[review]'}
TOKEN='a'*32

# Resource classification across summary and orphan/recovery routes.
texts={
    'plain':('', 'runner_rc'), 'python':('Traceback\nKeyError: sigma','runner_rc'),
    'oom':('CUDARuntimeError: cudaErrorMemoryAllocation','resource'),
    'host':('MemoryError','resource'), 'disk':('No space left on device','resource'),
    'gpu':('CUDA_ERROR_OUT_OF_MEMORY','resource'), 'cupy_oom':('OutOfMemoryError','resource'),
    'illegal_oom':('CUDA_ERROR_ILLEGAL_ADDRESS MemoryError','runner_rc'),
    'illegal_runtime':('cudaErrorIllegalAddress','runner_rc'),
    'assert':('CUDARuntimeError: device-side assert triggered','runner_rc'),
    'launch':('CUDA_ERROR_LAUNCH_FAILED','runner_rc'),
    'driver':('CUDADriverError','runner_rc'),
    'blas':('CUBLAS_STATUS_EXECUTION_FAILED','runner_rc'),
    'solver':('CUSOLVER_STATUS_EXECUTION_FAILED','runner_rc'),
    'sparse':('CUSPARSE_STATUS_INSUFFICIENT_RESOURCES','runner_rc'),
    'fft':('CUFFT_EXEC_FAILED','runner_rc'),
    'bare_oom':('CUDA error: out of memory','runner_rc'),
}
def group(folder,end,log='',name='L01',token=TOKEN):
    lp=folder/r.GROUPS_DIR/(name+'.launch.json')
    write(lp,{'schema':r.GROUP_SCHEMA,'name':name,'token':token,'host':HOST,
              'chain_pid':424242,'chain_start':100,'pid':424243,'runner_start':101,'started_utc':'2026-01-01T00:00:00Z'})
    write(lp.with_name(name+'.end.json'),dict({'schema':r.GROUP_SCHEMA,'name':name,'token':token,'confirmed':True},**end))
    (folder/'logs').mkdir(exist_ok=True)
    (folder/'logs'/(name+'.log')).write_text(log,encoding='utf8')
    return lp

for label,(txt,want) in texts.items():
    ck('word_'+label,r.words_cause(txt,'runner_rc'),want)
    for code,rc in [('RUNNER_RC',1),('GROUP_UNCONFIRMED',1),('TIME_LIMIT',None),('RUNNER_RC',None)]:
        f=mkdir('cause_'+label+'_'+code+'_'+str(rc)); (f/'logs').mkdir(exist_ok=True)
        (f/'logs'/'L01.log').write_text(txt,encoding='utf8')
        s={'status':'STOPPED','stop':{'code':code,'run':'L01'},'runs':[{'name':'L01','rc':rc,'group_cause':'signal' if rc is None and code=='RUNNER_RC' else None}]}
        base='timeout' if code=='TIME_LIMIT' else 'signal' if rc is None else None
        expected = ('runner_rc' if want=='runner_rc' and label not in ('plain','python') else base) if base else want
        ck('summary_'+label+'_'+code+'_'+str(rc),r.stop_cause(s,f),expected)
    for by,cause,ce,base in [('chain',None,None,'runner_rc'),('chain','timeout',None,'timeout'),('recover','parent_dead',{'cause':None,'rc':1},'runner_rc'),('recover','parent_dead',{'cause':'exception','rc':-9},'chain_exception')]:
        f=mkdir('orphan_'+label+'_'+by+'_'+str(cause)+'_'+base)
        er={'by':by,'cause':cause,'rc':1}
        if ce: er['chain_end']=ce
        group(f,er,txt); write(f/'one.first_result.json',{})
        expected = 'chain_exception' if base=='chain_exception' else (want if base=='runner_rc' else ('runner_rc' if want=='runner_rc' and label not in ('plain','python') else base))
        ck('orphan_'+label+'_'+base,r.orphan_cause(f), (expected,True))
        ck('eligible_'+label+'_'+base,r.result_fields(f,None)['resume_ok'],expected in r.RESUME_CAUSES)

# Exact process identity and visible/unseen-host policy, not an OS kill test.
start={'host':HOST,'chain_pid':424242,'chain_start':100}
for name,ps,expected in [('alive',(b'S',100,1,2,3),True),('reused',(b'S',101,1,2,3),False),('dead',None,False),('zombie',(b'Z',100,1,2,3),False)]:
    with patch.object(r,'proc_stat',return_value=ps):
        ck('parent_'+name,r.chain_parent_alive(start),expected)
        ck('start_'+name,bool(r.start_chain_problem(start,HOST,{'why':'cannot override'})[0]),expected)
with patch.object(r,'proc_stat',side_effect=PermissionError('fixture')):
    ck('parent_unreadable',r.chain_parent_alive(start),None)
    ck('visible_unknown_no_override',bool(r.start_chain_problem(start,HOST,{'why':'cannot override'})[0]),True)
with patch.object(r,'proc_stat',return_value=(b'S',999,1,2,3)):
    ck('unknown_start_live',r.chain_parent_alive(dict(start,chain_start=None)),True)
for field in HOST:
    h=dict(HOST); h[field]='other'
    ck('host_changed_'+field,r.host_seen(h,HOST)[0],False)
    ck('unseen_requires_operator_'+field,bool(r.start_chain_problem(dict(start,host=h),HOST)[0]),True)
    ck('unseen_operator_'+field,r.start_chain_problem(dict(start,host=h),HOST,{'why':'fixture'})[1],True)
ck('legacy_requires_operator',bool(r.start_chain_problem({'host':HOST},HOST)[0]),True)
ck('legacy_operator',r.start_chain_problem({'host':HOST},HOST,{'why':'fixture'})[1],True)
ck('no_start_legacy',r.start_chain_problem(None,HOST),(None,False))

# Fake /proc on real files: unrelated vs child, unreadable environment, live task under Z leader.
def proc(root,pid,state='S',start=100,ppid=1,pgrp=10,sid=10,env=b'',task=None):
    p=root/str(pid)
    if task is not None: p=p/'task'/str(task)
    p.mkdir(parents=True,exist_ok=True)
    fl=[state,str(ppid),str(pgrp),str(sid)]+['0']*15+[str(start)]+['0']*10
    (p/'stat').write_bytes((str(pid)+' (fixture) '+' '.join(fl)).encode())
    (p/'status').write_text('Uid:\t1000\t1000\t1000\t1000\n')
    if env is not None: (p/'environ').write_bytes(env)
    return p
pd=mkdir('proc_fixture'); proc(pd,10,env=b'RINT_RUN_TOKEN='+TOKEN.encode()+b'\0'); proc(pd,20,env=b'',sid=20,pgrp=20)
proc(pd,30,state='Z',env=None,sid=10,pgrp=10)
proc(pd,30,state='S',env=b'RINT_RUN_TOKEN='+TOKEN.encode()+b'\0',task=31)
with patch.object(r,'PROC_DIR',str(pd)):
    ck('proc_live_z_thread',r.group_members(TOKEN,uid=1000,run={'pid':10,'start':100}),[10,30])
    # Simulated EACCES, because Windows ACL semantics are not Linux /proc permissions.
    original=Path.read_bytes
    def denied(p):
        if p==pd/'20'/'environ': raise PermissionError('fixture')
        return original(p)
    with patch.object(Path,'read_bytes',denied):
        ck('unrelated_eacces_ignored',r.group_members(TOKEN,uid=1000,run={'pid':10,'start':100}),[10,30])
        proc(pd,20,env=b'',sid=10,pgrp=10)
        ck('related_eacces_unconfirmed',r.group_members(TOKEN,uid=1000,run={'pid':10,'start':100}),None)
        ck('visible_members_preserved',r.GROUP_SCAN[TOKEN]['members'],[10,30])
with patch.object(r,'group_members',return_value=None),patch.object(r,'group_kill_pids') as kill:
    ck('unknown_never_confirmed',r.group_settle(TOKEN,limit=0)[0],False)

# Binding at all consumers. Corrupt only end token/name, preserve confirmed true.
bf=mkdir('binding'); lp=group(bf,{'by':'chain','cause':None,'rc':0}); (bf/'run').mkdir(exist_ok=True)
rr=object.__new__(r.ResumeRunner); rr.src=bf
ck('bound_honest',r.group_pair(lp)[2],True)
ck('bound_honest_source_done',rr._src_done('L01','run'),True)
orig_end=json.loads(lp.with_name('L01.end.json').read_text())
for key,value in [('token','b'*32),('name','OTHER')]:
    write(lp.with_name('L01.end.json'),dict(orig_end,**{key:value}))
    ck('mismatched_'+key,r.group_pair(lp)[2],False)
    ck('groups_reject_'+key,bool(r.attempt_groups_problem(bf)),True)
    ck('orphan_reject_'+key,r.orphan_cause(bf)[1],False)
    ck('source_reject_'+key,rr._src_done('L01','run'),False)
    with patch.object(r,'chain_parent_alive',return_value=False),patch.object(r,'group_settle',return_value=(True,[],0)):
        end,why=r.recover_group(lp,HOST)
        ck('recover_reject_'+key,end is None and bool(why),True)
write(lp.with_name('L01.end.json'),orig_end)
for rc in [False,0.0,'0']:
    write(lp.with_name('L01.end.json'),dict(orig_end,rc=rc)); ck('source_rc_type_'+repr(rc),rr._src_done('L01','run'),False)

# Independent canonical ledger fixture and per-entry ordering.
header={'kind':'header','schema':r.LEDGER_SCHEMA,'plan_sha256':'1'*64,'utc':'fixture'}
def entry(n,target='ladder:P0',resume=None):
    return {'kind':'entry','n':n,'target':target,'machine':'kgy','resume_of':resume,'plan_sha256':'1'*64,'code_key_sha256':'2'*64,'env':{},'bed':{},'utc':'fixture'}
def result(n,**kw):
    return dict({'kind':'result','n':n,'status':'interrupted','stop':None,'side':'post','cause':'resource','resume_ok':True,'folder':'attempt_'+str(n),'folder_sha256':'3'*64,'by':'recover','utc':'fixture'},**kw)
def raw(*xs): return ''.join(r.ledger_line(x) for x in xs).encode()
def parse_fail(blob):
    try:r.ledger_parse(blob);return False
    except r.Stop:return True
sf=mkdir('ledger_case')/'attempt_1'; sf.mkdir(exist_ok=True)
sr={'kind':'start','n':1,'base':str(sf.parent.resolve()),'folder':'attempt_1','host':HOST,'chain_pid':424242,'chain_start':100,'utc':'fixture'}
ck('ledger_valid_start',len(r.ledger_parse(raw(header,entry(1),sr))['starts']),1)
for label,seq in [('duplicate',[header,entry(1),sr,sr]),('after_result',[header,entry(1),result(1),sr]),('before_entry',[header,sr,entry(1)])]:
    ck('ledger_start_'+label,parse_fail(raw(*seq)),True)
st=r.ledger_parse(raw(header,entry(1),result(1),entry(2,resume=1),result(2,side='pre',resume_ok=False,cause='gate'),entry(3,resume=1),result(3,status='completed',cause=None,resume_ok=False)))
ck('adopt_skip_pre_resume',r.adoption(st,'ladder:P0')['chain'],[1,3])
st2=copy.deepcopy(st); st2['entries'][3]['resume_of']=None
ck('adopt_refuse_new_post',r.adoption(st2,'ladder:P0')['problems'][0][0],'ATTEMPT_AFTER_ADOPTED')

# AL07 honest exception and each evidence guard.
af=mkdir('al07')/'attempt_1';af.mkdir(exist_ok=True)
side=af.parent/'attempt_1.rejected.json'
reject={'schema':r.REJECTED_SCHEMA,'n':1,'code':'OUTDIR_NOT_EMPTY','cause':'fixture','ledger_commit':'4'*40,'utc':'fixture'}
write(side,reject)
ar=result(1,status='rejected',stop={'code':'OUTDIR_NOT_EMPTY'},side='pre',cause='presolve',resume_ok=False,folder=side.name,folder_sha256=r.folder_digest(side))
ck('al07_honest',r.al07_foreign_ok(1,af,ar),True)
for label,mod in [('digest',{'folder_sha256':'0'*64}),('folder',{'folder':'attempt_1'}),('status',{'status':'interrupted'}),('stop',{'stop':{'code':'OTHER'}})]:
    ck('al07_'+label,r.al07_foreign_ok(1,af,dict(ar,**mod)),False)
for label,rec in [('empty',{}),('wrong_n',dict(reject,n=2)),('wrong_schema',dict(reject,schema='x')),('wrong_code',dict(reject,code='x'))]:
    write(side,rec); ck('al07_'+label,r.al07_foreign_ok(1,af,dict(ar,folder_sha256=r.folder_digest(side))),False)
write(side,reject)
for trace in ['attempt.json','ladder_summary.json','groups/L01.end.json','x/p2_a.json.tmp','x/one.first_result.json']:
    p=af/trace; write(p,{})
    ck('al07_trace_'+trace,r.al07_foreign_ok(1,af,ar),False); p.unlink()
st3=r.ledger_parse(raw(header,entry(1),ar));ck('found_honest_foreign',r.found_attempts_problem(st3,{1:[af]}),None)
write(side,{})
ck('found_reject_fake_exception',bool(r.found_attempts_problem(st3,{1:[af]})),True)
write(af/'attempt.json',{'schema':r.ATTEMPT_SCHEMA,'n':1,'target':'ladder:P1','machine':'kgy','resume_of':None,'ledger_commit':'4'*40})
ck('found_changed_target',bool(r.found_attempts_problem(st3,{1:[af]})),True)

# Real local Git IO, sequential; locking is explicitly replaced, never claimed tested.
@contextlib.contextmanager
def unlocked(*a,**k): yield
def git(d,*args):
    p=subprocess.run(['git','-C',str(d),'-c','user.name=review-fixture','-c','user.email=review@localhost','-c','commit.gpgsign=false','-c','core.autocrlf=false',*args],capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace'))
    return p.stdout.decode().strip()
ld=mkdir('git_ledger');git(ld,'init','-q');(ld/r.LEDGER_FILE).write_bytes(raw(header,entry(1)));git(ld,'add',r.LEDGER_FILE);git(ld,'commit','-qm','fixture')
h0=git(ld,'rev-parse','HEAD')
write(sf/'attempt.json',{'schema':r.ATTEMPT_SCHEMA,'n':1,'target':'ladder:P0','machine':'kgy','resume_of':None,'ledger_commit':h0})
with patch.object(r,'ledger_lock',unlocked):
    r.ledger_append(ld,sr,'start',expect=raw(header,entry(1)))
    # Second entry at a distinct base must not create it or alter bytes.
    second=SCRATCH/'not_created'
    args=types.SimpleNamespace(ledger=str(ld),attempt=1,out=str(second),variant=None,law='P0')
    before=(ld/r.LEDGER_FILE).read_bytes()
    with contextlib.redirect_stdout(io.StringIO()): rc=r.attempt_open(args,'ladder')
    ck('second_out_rejected',rc,3);ck('second_out_not_created',second.exists(),False)
    ck('second_out_ledger_unchanged',(ld/r.LEDGER_FILE).read_bytes()==before,True)
    with patch.object(r,'host_ident',return_value=HOST),patch.object(r,'proc_stat',return_value=(b'S',100,1,2,3)),contextlib.redirect_stdout(io.StringIO()):
        ck('recover_live_before_runner',r.recover_ledger(sf,ld),(1,0))
        ck('recover_live_operator_blocked',r.recover_ledger(sf,ld,{'folder':sf.resolve(),'attempt':1,'why':'fixture'}),(1,0))
    ck('recover_live_no_result',r.ledger_parse((ld/r.LEDGER_FILE).read_bytes())['results'],{})
    with patch.object(r,'host_ident',return_value=HOST),patch.object(r,'proc_stat',return_value=None),contextlib.redirect_stdout(io.StringIO()):
        ck('recover_dead_no_runner',r.recover_ledger(sf,ld),(0,0))
    ck('recover_dead_pre',r.ledger_parse((ld/r.LEDGER_FILE).read_bytes())['results'][1]['side'],'pre')
    # Folded evidence edit must be caught even with an existing result.
    write(sf/'changed.json',{})
    with contextlib.redirect_stdout(io.StringIO()):ck('recover_digest_changed',r.recover_ledger(sf,ld),(1,0))
    (sf/'changed.json').unlink()
    # Inject a real git add failure; transaction rollback must restore committed bytes.
    before=(ld/r.LEDGER_FILE).read_bytes();orig=r.ledger_git
    def fail_add(repo,*a,**kw):
        if a and a[0]=='add': raise r.Stop('ATTEMPT_LEDGER_MISMATCH','fixture add failed')
        return orig(repo,*a,**kw)
    with patch.object(r,'ledger_git',fail_add):
        try:r.ledger_append(ld,entry(2),'injected failure')
        except r.Stop:pass
    ck('append_failure_rollback',(ld/r.LEDGER_FILE).read_bytes()==before,True)
    ck('append_failure_index_clean',git(ld,'status','--porcelain'), '')
ck('history_honest',r.ledger_history_problem(ld,git(ld,'rev-parse','HEAD')),None)
# An ours merge that hides an alternative ledger edit must be rejected.
tip=git(ld,'rev-parse','HEAD');git(ld,'checkout','-qb','side',h0)
(ld/r.LEDGER_FILE).write_bytes(raw(header,entry(1),result(1)))
git(ld,'add',r.LEDGER_FILE);git(ld,'commit','-qm','hidden result');git(ld,'checkout','-q','-B','main',tip)
git(ld,'merge','-s','ours','--no-ff','side','-m','fixture ours')
ck('history_ours_rejected',bool(r.ledger_history_problem(ld,git(ld,'rev-parse','HEAD'))),True)

# Original verdict commit must ignore later different-target folders, but reject same-target ones.
vd=mkdir('verdict_ledger');git(vd,'init','-q');(vd/r.LEDGER_FILE).write_bytes(raw(header))
git(vd,'add',r.LEDGER_FILE);git(vd,'commit','-qm','header')
vb=mkdir('verdict_attempts'); vf=[]
with patch.object(r,'ledger_lock',unlocked):
    for n,target in [(1,'ladder:P0'),(2,'ladder:P1'),(3,'ladder:P0')]:
        hc=r.ledger_append(vd,entry(n,target),'entry')
        fp=vb/('attempt_'+str(n));fp.mkdir()
        write(fp/'attempt.json',{'schema':r.ATTEMPT_SCHEMA,'n':n,'target':target,'machine':'kgy','resume_of':None,'ledger_commit':hc})
        sm={'status':'CALIBRATED','plan':{'content':{'exec_policy':{'max_attempts':5}}}}
        write(fp/'ladder_summary.json',sm);write(fp/'result.first_result.json',{})
        r.ledger_append(vd,r.attempt_result_line(n,fp,sm,'chain'),'result');vf.append(fp)
        if n==1: oldcommit=git(vd,'rev-parse','HEAD')
        if n==2:
            pub=r.ledger_verdict_check([vf[0]],vd,commit=oldcommit)
            ck('reverify_ignore_later_other_target',pub['targets']['ladder:P0']['effective'],1)
        if n==3:
            try:r.ledger_verdict_check([vf[0]],vd,commit=oldcommit);code=None
            except r.Stop as ex:code=ex.code
            ck('reverify_refuse_later_same_target',code,'ATTEMPT_LEDGER_MISMATCH')

# Documentary source availability/hashes, not re-execution of submitted PASS logs.
rawdir=REPO/'docs/reviews/rint2_rr_fix_evidence_20261023/report_c_raw'
hashrows=[ln.split(None,1) for ln in (rawdir/'SHA256SUMS').read_text().splitlines() if ln.strip()]
ck('report_c_source_manifest_count',len(hashrows),93)
ck('report_c_source_hashes',all((rawdir/name).is_file() and hashlib.sha256((rawdir/name).read_bytes()).hexdigest()==sha for sha,name in hashrows),True)

# Known open PC6-05: unreadable/missing summary-route log remains retry eligible.
nf=mkdir('known_missing_log');write(nf/'result.first_result.json',{})
ns={'status':'STOPPED','stop':{'code':'TIME_LIMIT','run':'L01'},'runs':[{'name':'L01','rc':None,'outdir':'run'}]}
ck('known_PC6_05_summary_missing_log_resume',r.result_fields(nf,ns)['resume_ok'],True)

# Adjacent malformed rc probe. Store observations separately; do not define expected PASS as closure.
residual=[]
mf=mkdir('malformed_rc');write(mf/'result.first_result.json',{})
for rc in [1,False,0.0,'0',None,0]:
    group(mf,{'by':'chain','cause':None,'rc':rc},'Traceback\nKeyError: sigma')
    residual.append({'rc':rc,'type':type(rc).__name__,'runner_rc_failed':r.runner_rc_failed(rc),'group_problem':r.attempt_groups_problem(mf),
                     'orphan':r.orphan_cause(mf),'fields':r.result_fields(mf,None)})
integration=[]
for rc,label in [(1,'int_failure'),(False,'boolean_false'),(0.0,'float_zero')]:
    rd=mkdir('rc_ledger_'+label);git(rd,'init','-q');(rd/r.LEDGER_FILE).write_bytes(raw(header,entry(1)))
    git(rd,'add',r.LEDGER_FILE);git(rd,'commit','-qm','entry')
    rp=mkdir('rc_attempts_'+label)/'attempt_1';rp.mkdir()
    write(rp/'attempt.json',{'schema':r.ATTEMPT_SCHEMA,'n':1,'target':'ladder:P0','machine':'kgy','resume_of':None,'ledger_commit':git(rd,'rev-parse','HEAD')})
    group(rp,{'by':'chain','cause':None,'rc':rc},'Traceback\nKeyError: sigma');write(rp/'result.first_result.json',{})
    rstart=dict(sr,base=str(rp.parent.resolve()))
    with patch.object(r,'ledger_lock',unlocked),patch.object(r,'host_ident',return_value=HOST),patch.object(r,'proc_stat',return_value=None),contextlib.redirect_stdout(io.StringIO()):
        r.ledger_append(rd,rstart,'start')
        recovery=r.recover_ledger(rp,rd)
    rs=r.ledger_parse((rd/r.LEDGER_FILE).read_bytes())
    nxt=entry(2,resume=1)
    eligibility=r.attempt_order_problem(rs,nxt,{'exec_policy':{'max_attempts':4}})
    integration.append({'label':label,'rc':rc,'recovery':recovery,'result':rs['results'][1],
                        'next_resume_problem':eligibility,'ledger':str(rd),'attempt':str(rp)})
(HERE/'residual_rc.json').write_text(json.dumps(residual,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
(HERE/'residual_rc_integration.json').write_text(json.dumps(integration,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
# Verify the one-line candidate fix in memory only; submitted source stays untouched.
original_orphan=r.orphan_cause
fixsource=inspect.getsource(r.orphan_cause).replace("if by == 'chain' and gc is None and rc == 0:","if by == 'chain' and gc is None and type(rc) is int and rc == 0:")
fixed=dict(r.__dict__);exec(compile(fixsource,'candidate-fix-in-memory','exec'),fixed)
fixrows=[]
with patch.object(r,'orphan_cause',fixed['orphan_cause']):
    for rc in [1,False,0.0,'0',None,0]:
        group(mf,{'by':'chain','cause':None,'rc':rc},'Traceback\nKeyError: sigma')
        fixrows.append({'rc':rc,'type':type(rc).__name__,'fields':r.result_fields(mf,None)})
(HERE/'candidate_fix_results.json').write_text(json.dumps(fixrows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

# First result marker before returned result is visible; harmless mock solver subprocess.
child=HERE/'marker_child.py'
child.write_text('''import sys,types\nfrom pathlib import Path\nsys.path.insert(0,sys.argv[1])\nimport rint_first_result as r\nm=types.SimpleNamespace(_solve_cg=lambda: 7, solve_sigma_z=lambda: {"sigma":7})\nr.install(sys.argv[2],m)\nm._solve_cg()\nPath(sys.argv[3]).write_text("returned")\n''',encoding='utf8')
mark=SCRATCH/'first.first_result.json'; returned=SCRATCH/'returned.txt'
cmd=[sys.executable,'-B',str(child),str(REPO/'scripts'),str(mark),str(returned)]
p=subprocess.run(cmd,capture_output=True); ck('marker_success_rc',p.returncode,0)
ck('marker_before_return',mark.exists() and returned.exists(),True)
returned.unlink(); p=subprocess.run(cmd,capture_output=True)
ck('marker_existing_aborts',p.returncode,5);ck('marker_failure_no_return',returned.exists(),False)

# Independent arithmetic of original 82 and all3 86..98 equivalent solves.
budget=json.loads((REPO/'docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json').read_text(encoding='utf8'))
f=704/879
for label,dbe in [('old_registration_82_R0_only_one_machine_h',[44,44]),('all3_one_machine_h',[48,60])]:
    independently=[round((38*879+d*2578)*(1-f+f*k)/3600,1) for d,k in zip(dbe,[6.05,7.37])]
    ck('budget_'+label,budget[label],independently)

out={'environment':{'platform':platform.platform(),'python':sys.version,'mode':'synthetic-only; Linux identity mocked; Git sequential lock shim; no production runs'},
     'source_sha256':{str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [REPO/'scripts/rint_r_chain.py',REPO/'scripts/rint_first_result.py']},
     'passed':sum(x['pass'] for x in ROWS),'total':len(ROWS),'checks':ROWS}
(HERE/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str)+'\n',encoding='utf8')
print(json.dumps({k:out[k] for k in ['environment','passed','total']},ensure_ascii=False))
sys.exit(0 if out['passed']==out['total'] else 1)
