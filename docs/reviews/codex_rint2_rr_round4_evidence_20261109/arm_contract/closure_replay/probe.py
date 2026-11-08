"""Independent bounded PC12 probes: actual functions, Windows regular files only.

No LIGGGHTS, GPU, remote host, real process group, or research input is invoked.
Only run_in_group is mocked in the producer probe; read_run and record production
are actual pinned functions. O_NONBLOCK=0 is a disclosed Windows compatibility
adaptation restricted to regular temporary files, not a POSIX qualification.
"""
import copy
import hashlib
import itertools
import json
import os
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get('RINT_REVIEW_REPO', str(HERE.parent / 'package' / 'repo'))).resolve()
sys.path.insert(0, str(REPO / 'scripts'))
import rint_r_chain as R

if not hasattr(os, 'O_NONBLOCK'):
    os.O_NONBLOCK = 0

OUT = {'pin': '17d45fb9cdfc7033bdfd41509527cea23ba1654c',
       'source_sha256': hashlib.sha256((REPO/'scripts/rint_r_chain.py').read_bytes()).hexdigest(),
       'scope': 'Windows regular-file helpers and mocked process-group return; no POSIX/process/CLI qualification',
       'python': sys.version, 'tests': {}}

def record(n=1, al=None):
    return {'name':'L01_floor', 'outdir':'L01_floor'+R.run_outdir_suffix(n, al),
            'arms':n, 'arm_list':al, 'rc':None, 'group_cause':'timeout', 'arms_read':[]}

def summary(code, run, rr):
    return {'status':'STOPPED','stop':{'code':code,'run':run,'reason':None},'runs':rr}

# Independent canonical domain: 8 prefix-count requests, plus every nonprefix
# subset of [0..7]. The production helper is called, not copied.
canon = [record(n) for n in range(1,9)]
for n in range(1,9):
    for al in itertools.combinations(range(8), n):
        if list(al) != list(range(n)):
            canon.append(record(n,list(al)))
good = [R.request_fields_problem(r) for r in canon]
invalid = []
for n in [None,False,True,0,-1,9,1.0,'1',10**30]:
    invalid.append({'name':'L01_floor','arms':n,'arm_list':None})
for n, al in [(1,[]),(1,[0]),(1,[8]),(1,[-1]),(2,[1,1]),(2,[2,1]),(3,[1,2]),
              (1,[True]),(1,[1.0]),(1,['1']),(1,(1,)),(1,'1')]:
    invalid.append({'name':'L01_floor','arms':n,'arm_list':al})
bad = [R.request_fields_problem(r) for r in invalid]
OUT['tests']['request_domain'] = {'valid_total':len(good),'valid_rejected':sum(x is not None for x in good),
                                 'invalid_total':len(bad),'invalid_accepted':sum(x is None for x in bad)}
assert all(x is None for x in good) and all(x is not None for x in bad)

# Enumerate summary->disk rows independently from the consumer table constant.
rows=[]
allowed=[('exit_ok',0,None,[('GROUP_UNCONFIRMED',False)]),
         ('exit_fail',3,None,[('GROUP_UNCONFIRMED',False),('RUNNER_RC',True)]),
         ('killed:timeout',None,'timeout',[('GROUP_UNCONFIRMED',False),('TIME_LIMIT',True)]),
         ('killed:signal',None,'signal',[('GROUP_UNCONFIRMED',False),('RUNNER_RC',True)]),
         ('killed:signal_after',None,None,[('GROUP_UNCONFIRMED',False),('RUNNER_RC',True)])]
for shape,rrc,cause,codes in allowed:
    for code,confirmed in codes:
        vals=[rrc] if shape.startswith('exit_') else ([-9,0,7] if shape.endswith('signal_after') else [-9,0,7,None])
        for drc in vals:
            rr={'rc':rrc}
            side={'cause':cause,'rc':drc,'confirmed':confirmed}
            why=R.chain_side_problem(code,'L01_floor',rr,shape,side)
            rows.append({'kind':'honest','shape':shape,'code':code,'disk':side,'problem':why})
            assert why is None
            for key,value in [('confirmed',not confirmed),('confirmed',int(confirmed)),('cause','made_up'),('rc',False),('rc',1.0),('rc','0')]:
                changed=dict(side); changed[key]=value
                why=R.chain_side_problem(code,'L01_floor',rr,shape,changed)
                rows.append({'kind':'mutant','shape':shape,'code':code,'disk':changed,'problem':why})
                assert why is not None
OUT['tests']['chain_side_matrix']={'rows':len(rows),'honest':sum(x['kind']=='honest' for x in rows),
                                   'mutants':sum(x['kind']=='mutant' for x in rows),'all_expected':True}
(HERE/'chain_side_rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')

with tempfile.TemporaryDirectory(prefix='rr3_pc12_',dir=HERE) as td:
    folder=Path(td)/'attempt_1';folder.mkdir()
    outdir=folder/'L01_floor_arm1';outdir.mkdir()
    # Valid JSON filename/index but wrong kit prefix => actual read_run fails.
    (outdir/'p2_wrong_kit_a0.json').write_text('{}\n',encoding='utf-8')
    _,req,_=R.run_request('L',1,R.SBE_KIT,'floor','P0',None,0.0,1,False,None)
    runner=R.Runner('unused.sh',folder,folder,{},None,time.time()+60,{},parent_env={})
    orig_group=R.run_in_group
    token='a'*32
    def fake_group(argv,cwd,env,logf,left,gdir,name):
        gdir=Path(gdir);gdir.mkdir(parents=True,exist_ok=True)
        launch={'schema':R.GROUP_SCHEMA,'name':name,'token':token}
        end={'schema':R.GROUP_SCHEMA,'name':name,'token':token,'by':'chain','cause':None,'rc':0,'confirmed':True}
        (gdir/f'{name}.launch.json').write_text(json.dumps(launch),encoding='utf-8')
        (gdir/f'{name}.end.json').write_text(json.dumps(end),encoding='utf-8')
        logf.write('synthetic mock process-group return rc 0\n')
        return 0,None,end
    R.run_in_group=fake_group
    # _execute rejects preexisting nonempty folder before mocked launch, so have
    # the mock materialize it at the moment a runner would produce its output.
    payload=(outdir/'p2_wrong_kit_a0.json').read_bytes()
    (outdir/'p2_wrong_kit_a0.json').unlink();outdir.rmdir()
    def fake_group_with_payload(*a,**kw):
        outdir.mkdir();(outdir/'p2_wrong_kit_a0.json').write_bytes(payload)
        return fake_group(*a,**kw)
    R.run_in_group=fake_group_with_payload
    try:
        runner._execute('L01_floor',req,outdir,{})
        raise AssertionError('expected real read_run failure')
    except R.Stop as e:
        real_failure={'code':e.code,'cause':e.cause,'run':e.run}
    finally:
        R.run_in_group=orig_group
    assert real_failure['code']=='ARM_JSON_COUNT'
    original=summary(real_failure['code'],'L01_floor',copy.deepcopy(runner.records))
    changed=copy.deepcopy(original)
    changed['stop']['code']='TIME_LIMIT';changed['stop']['run']='L02_ceiling'
    before=R.result_fields(folder,original)
    after=R.result_fields(folder,changed)
    problem=R.stop_record_problem(changed,folder)
    # Actual result-line encoder -> strict ledger parser -> next-entry policy,
    # with explicitly synthetic header/entry/start metadata. No git mutation,
    # ledger append, locks, recover process discovery, or launch is exercised.
    ledger_rows=[]
    header={'kind':'header','schema':R.LEDGER_SCHEMA,'plan_sha256':'b'*64,'utc':'synthetic'}
    entry={'kind':'entry','n':1,'target':'ladder:P0','machine':'synthetic','resume_of':None,
           'plan_sha256':'b'*64,'code_key_sha256':'c'*64,'env':{},'bed':{},'utc':'synthetic'}
    start={'kind':'start','n':1,'base':str(Path(td).resolve()),'folder':'attempt_1',
           'host':{'machine_id':None,'boot_id':None,'pidns':None},'utc':'synthetic',
           'chain_pid':1,'chain_start':None}
    next_entry=dict(entry,n=2,resume_of=1)
    for label,summ in [('original',original),('edited',changed)]:
        (folder/'ladder_summary.json').write_bytes(R.canon_bytes(summ))
        result=R.attempt_result_line(1,folder,summ,'recover')
        raw=''.join(R.ledger_line(x) for x in [header,entry,start,result]).encode('utf-8')
        parsed=R.ledger_parse(raw)
        order=R.attempt_order_problem(parsed,next_entry,{'exec_policy':{'max_attempts':2}})
        recount=R.result_line_problem(1,folder,result)
        ledger_rows.append({'label':label,'result':result,'parsed_result_resume_ok':parsed['results'][1]['resume_ok'],
                            'attempt_order_problem':order,'result_line_problem':recount})
        (HERE/f'counterexample_{label}_ledger.jsonl').write_bytes(raw)
    assert ledger_rows[0]['attempt_order_problem'][0]=='RESUME_NOT_ALLOWED'
    assert ledger_rows[1]['attempt_order_problem'][0] == 'RESUME_NOT_ALLOWED'
    assert all(x['result_line_problem'] is None for x in ledger_rows)
    # The actual resumed copy should still fail its read_run, delimiting impact.
    resumed=Path(td)/'attempt_2';resumed.mkdir()
    rr=R.ResumeRunner('unused.sh',folder,resumed,{},None,time.time()+60,{},parent_env={},src=folder,src_n=1)
    src_done=rr._src_done('L01_floor',outdir.name)
    copy_failure=None
    try:
        rr._copy('L01_floor',req,resumed/outdir.name)
    except R.Stop as e:
        copy_failure={'code':e.code,'cause':e.cause}
    OUT['tests']['prior_read_failure_promoted']={
        'producer_mock':'run_in_group return and files only; real Runner._execute/read_run/arm_file_shas',
        'original_failure':real_failure,'producer_records':runner.records,
        'only_summary_edits':{'stop.code':'TIME_LIMIT','stop.run':'L02_ceiling'},
        'original_result':before,'edited_result':after,'stop_record_problem':problem,
        'ledger_policy':ledger_rows,
        'source_done':src_done,'actual_copy_read_result':copy_failure,
        'physical_run_count':0}
    assert before['resume_ok'] is False and after['resume_ok'] is False and 'file_ids' in problem
    assert src_done and copy_failure['code']=='ARM_JSON_COUNT'
    (HERE/'counterexample_original_summary.json').write_text(json.dumps(original,ensure_ascii=False,indent=2),encoding='utf-8')
    (HERE/'counterexample_edited_summary.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2),encoding='utf-8')

with tempfile.TemporaryDirectory(prefix='rr3_json_',dir=HERE) as td:
    p=Path(td)/'summary.json'
    cases=[('duplicate','{"status":"STOPPED","status":"CALIBRATED"}','unreadable'),
           ('nan','{"x":NaN}','unreadable'),('positive_inf','{"x":Infinity}','unreadable'),
           ('negative_inf','{"x":-Infinity}','unreadable'),('good','{"x":null}','ok'),
           ('declared_numeric_overflow','{"x":1e400}','ok')]
    rows=[]
    for label,raw,want in cases:
        p.write_text(raw,encoding='utf-8');v,h,s=R.read_summary_state(td,p.name)
        rows.append({'case':label,'state':s,'expectation':want});assert s==want
    OUT['tests']['strict_summary']=rows

att={'n':1,'ledger_commit':'a'*40}
base={'schema':R.REJECTED_SCHEMA,'n':1,'code':'MACHINE_NOT_ALLOWED','cause':'synthetic','utc':'synthetic','ledger_commit':'a'*40}
rej=[]
for code in ['XYZ','CALIBRATED','PREDICTED','STOPPED','MACHINE_NOT_ALLOWED','GENERATION','OUTDIR_NOT_EMPTY']:
    rec=dict(base,code=code);why=R.rejected_form_problem(rec,att)
    rej.append({'code':code,'problem':why});assert (why is None)==(code in R.STOPS)
OUT['tests']['rejected_closed_names']=rej

with tempfile.TemporaryDirectory(prefix='rr3_pc11_',dir=HERE) as td:
    folder=Path(td)/'attempt_1';folder.mkdir()
    at={'schema':R.ATTEMPT_SCHEMA,'n':1,'target':'ladder:P0','machine':'synthetic','resume_of':None,'ledger_commit':'a'*40}
    (folder/R.ATTEMPT_FILE).write_bytes(R.canon_bytes(at))
    (folder/R.REJECTED_FILE).write_bytes(R.canon_bytes(base))
    assert R.rejected_in_folder(folder,'synthetic')==base
    rows=[]
    for name in ['ladder_summary.json','p2_wrong_a0.json','run.first_result.json','groups','logs','L01_floor_arm1']:
        p=folder/name;p.write_text('{}',encoding='utf-8')
        try:
            R.rejected_in_folder(folder,'synthetic')
            raise AssertionError(name)
        except R.Stop as e:
            rows.append({'extra':name,'code':e.code});assert e.code=='ATTEMPT_LEDGER_MISMATCH'
        p.unlink()
    OUT['tests']['pc11_rejected_folder']={'normal_accepted':True,'extras_rejected':rows}
    bad_shapes=[{'stop':'x'},{'stop':['x']},{'runs':'x'},{'runs':{}},{'runs':7},{'runs':[1]},
                {'runs':[{'outdir':{}}]},{'runs':[{'outdir':1}]}]
    rows=[]
    for patch in bad_shapes:
        s={'status':'STOPPED','stop':{'code':'TIME_LIMIT','run':'L02_ceiling'},'runs':[]};s.update(patch)
        try:
            R.result_fields(folder,s)
            raise AssertionError(patch)
        except R.Stop as e:
            rows.append({'input':patch,'code':e.code});assert e.code=='ATTEMPT_LEDGER_MISMATCH'
    OUT['tests']['pc11_summary_shapes']=rows
    # Trace must be found in the real arm1 directory despite a self-consistent
    # coedited request for another allowed arm count/output directory.
    trace=folder/'L01_floor_arm1' / R.UNCHECKED_DIR / 'p2_SBE_vgcf100_a0.json'
    trace.parent.mkdir(parents=True);trace.write_text('{}',encoding='utf-8')
    OUT['tests']['pc12_sibling_trace']={str(n):R.stop_trace(folder,'L01_floor',folder/record(n)['outdir']) for n in range(1,9)}
    assert all(OUT['tests']['pc12_sibling_trace'].values())

OUT['tests']['pc11_header_reference']={'end_record_known_callable':callable(R.end_record_known),
 'obsolete_identifier_only_as_explicit_old_name':'옛 글 = 없는 이름 end_rc_known' in R.__doc__}
(HERE/'results.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(OUT,ensure_ascii=False,indent=2))
