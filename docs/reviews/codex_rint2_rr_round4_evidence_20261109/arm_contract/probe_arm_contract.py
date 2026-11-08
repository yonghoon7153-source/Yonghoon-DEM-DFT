"""Independent round-4 ARM_PUBLIC review; no research inputs or process groups.

Actual rint_r_chain functions are used. Synthetic payload generation alone reuses
the submitted FAKE_SRC/record_templates; no submitted test assertion or full
fixture/gate is run. run_in_group is replaced by a plain Python invocation of
that deterministic tiny fake writer. O_NONBLOCK=0 applies only to our regular
Windows files. No OS, GPU, physical-model, or host qualification is claimed.
"""
import ast
import contextlib
import copy
import hashlib
import io
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get('RINT_REVIEW_REPO', str(HERE.parent / 'package' / 'repo'))).resolve()
sys.path.insert(0, str(REPO / 'scripts'))
import rint_r_chain as R
import test_rint_r_chain as T

if not hasattr(os, 'O_NONBLOCK'):
    os.O_NONBLOCK = 0
OUT = {'pin': '1f9f3607eb2f0118d322eeff780bba6eb17b85a2',
       'python': sys.version,
       'source_sha256': hashlib.sha256(Path(R.__file__).read_bytes()).hexdigest(),
       'scope': __doc__, 'checks': {}, 'unexpected': []}

def check(label, condition, details=None):
    OUT['checks'][label] = {'ok': bool(condition), 'details': details}
    if not condition:
        OUT['unexpected'].append(label)

def public(i=0, kit=R.SBE_KIT, state='positive'):
    return {'file': f'p2_{kit[4:]}_synthetic_a{i}.json', 'index': i,
            'sha256': hashlib.sha256(f'{kit}/{i}'.encode()).hexdigest(),
            'protocol_id': 'p3ca-0123456789abcdef', 'state': state,
            'cg_info': 0 if state == 'positive' else None,
            'cg_resid': 0.0 if state == 'positive' else None,
            'imbalance': None, 'cert_pass': [True]*4 if state == 'positive' else [None]*4,
            'sid_fp': 'f'*32, 'cg_iters': None, 'resolve_iters': 0,
            'sv_cf_status': None, 'err_rel': 0.0}

def req_for(indices, kit=R.SBE_KIT, role='floor', c=None, sv=False, variant=None):
    arms = len(indices) if indices == list(range(len(indices))) else list(indices)
    return R.run_request('L', 1, kit, role, 'P0', '' if c is None else c, R.rj_key(0.0), arms, sv, variant)[1]

def record(req, ar):
    return dict(req, outdir=req['name'] + R.run_outdir_suffix(req['arms'], req['arm_list']),
                arms_read=copy.deepcopy(ar), rc=0, group_cause=None)

def summ(rec):
    return {'status':'STOPPED', 'stop': {'code':'TIME_LIMIT','run':'L02_ceiling','reason':None}, 'runs':[rec]}

def classify(ar, rec):
    try:
        return R.arms_read_kind(ar, rec)[0]
    except Exception as exc:
        return f'EXC:{type(exc).__name__}:{str(exc)[:150]}'

def mock_ends(gdir, name):
    gdir = Path(gdir); gdir.mkdir(parents=True, exist_ok=True)
    launch = {'schema': R.GROUP_SCHEMA, 'name':name, 'token':'a'*32}
    end = dict(launch, by='chain', cause=None, rc=0, confirmed=True)
    (gdir/f'{name}.launch.json').write_text(json.dumps(launch), encoding='utf-8')
    (gdir/f'{name}.end.json').write_text(json.dumps(end), encoding='utf-8')
    return end

PLAN = {'schema':'rint-r-plan-v3', 'len_law':'len_scaled_v0', 'unreg_law':'cut',
        's_min_um':0.6, 'tol_ff_um':0.05, 'step3_rtol':1e-12,
        'p2_extra':'--step3-maxiter 60000', 'max_ladder_points':16,
        'calib_rj_ratio_max':'none', 'sv_cf_threshold':2.0, 'sv_cf_scope':'R_j0'}

def main(td):
    T.RR = R
    T.TD = str(td)
    T.FX['plan_obj'] = PLAN
    fake = td/'fake.py'; fake.write_text(T.FAKE_SRC, encoding='utf-8')
    summary_folder = td/'summary_cases'/'attempt_1'
    (summary_folder/'logs').mkdir(parents=True)
    marker = summary_folder/'L00_prev_arm1'/'.unchecked'/'p2_marker.json.first_result.json'
    marker.parent.mkdir(parents=True); marker.write_text('{}', encoding='utf-8')

    # The full canonical request domain (8 count forms + 247 nonprefix sets)
    # is independently enumerated. Both registered success states are covered.
    forms = [list(c) for n in range(1,9) for c in itertools.combinations(range(8), n)]
    rows=[]
    for state, indices in itertools.product(('positive','zero'), forms):
        req=req_for(indices)
        ar=[public(i, state=state) for i in indices]
        rec=record(req, ar)
        rows.append({'state':state,'indices':indices,'kind':classify(ar,rec),
                     'prior_problem':R.prior_runs_problem(summ(rec),'TIME_LIMIT','L02_ceiling',None)})
    check('canonical_requests_both_states', all(x['kind']=='verified' and x['prior_problem'] is None for x in rows),
          {'rows':len(rows),'rejected':[x for x in rows if x['kind']!='verified' or x['prior_problem']]})

    req=req_for([0]); base=public(); rec=record(req,[base])
    structural=[('none',None,'bad'),('dict',{},'bad'),('tuple',tuple([base]),'bad'),
                ('empty',[],'empty'),('nonobject',[1],'bad'),
                ('ids',[{k:base[k] for k in ('file','index','sha256')}],'file_ids'),
                ('mixed',[base,{k:base[k] for k in ('file','index','sha256')}],'bad'),
                ('duplicate',[base,base],'bad')]
    structural += [('missing_'+k,[{kk:vv for kk,vv in base.items() if kk!=k}],'bad') for k in base]
    structural += [('extra',[dict(base,extra=None)],'bad'), ('wrong_index',[dict(base,index=1)],'bad'),
                   ('bool_index',[dict(base,index=False)],'bad'), ('float_index',[dict(base,index=0.0)],'bad')]
    for key, values in {'file':['p2_other_a0.json','../'+base['file'],base['file']+'/x','C:\\'+base['file'],base['file']+'\n'],
                        'sha256':['A'*64,'g'*64,'f'*63,'f'*65,'f'*64+'\n',None,0]}.items():
        structural += [(key+str(i),[dict(base,**{key:v})],'bad') for i,v in enumerate(values)]
    sr=[]
    for nm, ar, expected in structural:
        got=classify(ar,rec); s=summ(record(req,ar)); prior=R.prior_runs_problem(s,'TIME_LIMIT','L02_ceiling',None)
        sr.append({'name':nm,'kind':got,'expected':expected,'prior_rejected':prior is not None})
    check('structural_rejects',all(x['kind']==x['expected'] and x['prior_rejected'] for x in sr),sr)

    # JSON-domain malformed scalars/containers, including the largest supported
    # integer text and IEEE overflow tokens. No custom Python magic methods.
    values=[('null',None),('false',False),('true',True),('zero_int',0),('neg_int',-1),('one_int',1),
            ('zero_float',0.0),('neg_zero',-0.0),('one_float',1.0),('small',1e-12),
            ('tau',1e-4),('above_tau',math.nextafter(1e-4,math.inf)),
            ('subnormal',math.nextafter(0.0,1.0)),('inf',math.inf),('ninf',-math.inf),('nan',math.nan),
            ('big',10**400),('negbig',-(10**400)),('maxjson',10**4299),('negmaxjson',-(10**4299)),
            ('emptystr',''),('space',' '),('text','0'),('list',[]),('dict',{}),('nested',[{'v':1}])]
    matrix=[]
    declared={'imbalance','sv_cf_status'}
    for state in ('positive','zero'):
        for key in R.ARM_PUBLIC:
            for lab,value in values:
                a=public(state=state); a[key]=value; rr=record(req,[a])
                got=classify([a],rr)
                matrix.append({'state':state,'key':key,'value':lab,'kind':got})
    check('json_value_matrix_no_exception',not any(x['kind'].startswith('EXC:') for x in matrix),
          {'rows':len(matrix),'exceptions':[x for x in matrix if x['kind'].startswith('EXC:')],
           'accepted':[x for x in matrix if x['kind']=='verified']})
    (HERE/'value_matrix.json').write_text(json.dumps(matrix,indent=2),encoding='utf-8')

    targeted=[('positive',{},'verified'),('zero',{},'verified'),
              ('positive',{'protocol_id':'p3ca-'},'bad'),('positive',{'sid_fp':' '},'bad'),
              ('positive',{'err_rel':math.nextafter(1e-4,math.inf)},'bad'),
              ('positive',{'err_rel':1e-4},'verified'),('positive',{'err_rel':0},'bad'),
              ('positive',{'cg_resid':10**400},'bad'),('positive',{'cg_resid':-(10**400)},'bad'),
              ('positive',{'cg_resid':10**4299},'bad'),('positive',{'cg_info':10**4299},'bad'),
              ('positive',{'cg_iters':10**4299},'verified'),('zero',{'cg_resid':10**4299},'verified'),
              ('zero',{'cert_pass':[False,{},2,'x']},'verified')]
    tr=[]
    for state,kw,expected in targeted:
        a=dict(public(state=state),**kw); rr=record(req,[a]); s=summ(rr)
        k,why=R.arms_read_kind([a],rr)
        (summary_folder/'ladder_summary.json').write_bytes(R.canon_bytes(s))
        recount=R.result_recount(summary_folder)
        fields=R.result_fields(summary_folder,s)
        tr.append({'state':state,'fields_changed':list(kw),'kind':k,'expected':expected,
                   'resume_ok':recount['resume_ok'],'direct_recount_equal':fields==recount,
                   'why_length':len(why or '')})
    check('targeted_summary_json_recount',all(x['kind']==x['expected'] and x['resume_ok']==(x['expected']=='verified') and x['direct_recount_equal'] for x in tr),tr)
    # >4300 digit JSON rejects before the ARM classifier on this interpreter.
    txt=R.canon_bytes(summ(record(req,[public()]))).decode()
    txt=txt.replace('"cg_resid": 0.0','"cg_resid": '+'1'+'0'*4300)
    (summary_folder/'ladder_summary.json').write_text(txt,encoding='utf-8')
    parsed,status=R.stage_summary_read(summary_folder)
    check('json_4301_digits_rejected',parsed is None and status=='unreadable',{'status':status})

    # Real successful read_run (RealContract), plus producer/copy/merge paths.
    producer_rows=[]; real=[]
    scenarios=[('sbe_pos',R.SBE_KIT,[0],None,False,None,'positive'),
               ('sbe_zero',R.SBE_KIT,[0],None,False,None,'zero'),
               ('sbe_eight',R.SBE_KIT,list(range(8)),None,False,None,'positive'),
               ('sbe_sel',R.SBE_KIT,[1,3,7],None,False,None,'positive'),
               ('dbe_sv',R.DBE_KIT,[0,2,5],'1',True,None,'positive'),
               ('dbe_zero',R.DBE_KIT,[0],'0',False,None,'zero')]
    scenarios += [(f'variant_{v}',R.DBE_KIT,[0],'0',False,v,'positive') for v in ('GRID','FIBRE','UNREG','SVORDER')]
    for tag,kit,indices,c,sv,variant,state in scenarios:
        request=req_for(indices,kit,'floor',c,sv,variant)
        folder=td/tag/'attempt_1'; folder.mkdir(parents=True)
        outdir=folder/(request['name']+R.run_outdir_suffix(request['arms'],request['arm_list']))
        world=T.world(tag,states=[{'state':'zero'}] if state=='zero' else [])
        rn=R.Runner('unused.sh',folder,folder,PLAN,variant,time.time()+120,R.RealContract(),parent_env=os.environ)
        delta=R.runner_env_delta(PLAN,variant,request,outdir)
        def group(argv,cwd,env,logf,left,gdir,name):
            child=subprocess.run([sys.executable,'-I','-X','utf8','-B',str(fake)],
                                 env=dict(env,FAKE_WORLD=world),capture_output=True,text=True,encoding='utf-8')
            logf.write(child.stdout+child.stderr)
            if child.returncode:
                raise RuntimeError(f'synthetic writer failed: {child.stderr}')
            return 0,None,mock_ends(gdir,name)
        old=R.run_in_group; R.run_in_group=group
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                arms=rn._execute(request['name'],request,outdir,delta)
        finally:
            R.run_in_group=old
        rec1=rn.records[0]; kind=classify(rec1['arms_read'],rec1)
        real.append((tag,request,folder,outdir,arms,rec1))
        producer_rows.append({'name':tag,'producer':'Runner._execute','arms':len(arms),'kind':kind,
                              'state':[a['state'] for a in arms]})
        dest=td/tag/'attempt_2'; dest.mkdir()
        cp=R.ResumeRunner('unused.sh',folder,dest,PLAN,variant,time.time()+120,R.RealContract(),parent_env={},src=folder,src_n=1)
        with contextlib.redirect_stdout(io.StringIO()):
            cp._copy(request['name'],request,dest/outdir.name)
        rec2=cp.records[0]
        producer_rows.append({'name':tag,'producer':'ResumeRunner._copy','kind':classify(rec2['arms_read'],rec2),
                              'same_public':rec1['arms_read']==rec2['arms_read'],'copied':cp.resume['copied']})
        # Construct only the fetch input needed by its real .run method; source
        # payload bytes and read_run/sha checking remain real, ledger opening is
        # not invoked and is not counted as tested.
        merge=object.__new__(R.MergeFetch)
        merge.n=0; merge.keys=set(); merge.variant=variant; merge.records=[]
        merge.plan=PLAN; merge.contract=R.RealContract(); merge.sid_reg={}
        merge.s0_grid={}; merge.s0_census={}; merge.graph_src=None; merge.out=td/tag
        merge.lads={'P0':{'lo':0.0}}
        merge._role_of=lambda *args:'lo'
        unitname=R.unit_name(request['c'],'P0','lo'); target=R.unit_target('unit',variant,unitname)
        iname=f'{R.UNIT_PREFIX}{R.UNIT_RUN_INDEX.get("floor",0):02d}_floor'
        src_rec=dict(rec1,name=iname,outdir=iname+R.run_outdir_suffix(request['arms'],request['arm_list']))
        # run() requires the unit source directory prefix; copy payload once.
        unitrel='merge_source'; unitdir=td/tag/unitrel; unitdir.mkdir()
        shutil.copytree(outdir,unitdir/src_rec['outdir'])
        merge.opened={target:{'runs':{iname:src_rec},'sum':{},'consumed':set(),
                              'rel':unitrel,'machine':'synthetic','n':1}}
        with contextlib.redirect_stdout(io.StringIO()):
            merge.run(kit,'floor','P0',request['c'],request['rj'],request['arms'] if request['arm_list'] is None else request['arm_list'],sv)
        mr=merge.records[0]
        producer_rows.append({'name':tag,'producer':'MergeFetch.run','kind':classify(mr['arms_read'],mr),
                              'same_public':rec1['arms_read']==mr['arms_read']})
    check('actual_producer_copy_merge_success',all(x['kind']=='verified' and x.get('same_public',True) for x in producer_rows),producer_rows)

    # Actual read_run calls the shared value predicate on a normal output.
    tag,request,folder,outdir,arms,rec1=real[0]
    orig=R.arm_public_value_problem
    called=[]
    def reject(a):
        called.append(set(a)); return 'independent_selfcheck_sentinel'
    R.arm_public_value_problem=reject
    try:
        try:
            R.read_run(outdir,request,PLAN,R.RealContract(),{})
            stop=None
        except R.Stop as exc:
            stop={'code':exc.code,'sentinel': 'independent_selfcheck_sentinel' in exc.cause}
    finally:
        R.arm_public_value_problem=orig
    check('real_read_run_shared_selfcheck',len(called)==1 and stop=={'code':'ARM_UNREADABLE','sentinel':True},stop)

    # Failed reading in all three producers leaves file identities, and the
    # unchanged run record cannot promote into an eligible prior run.
    failures=[]
    badfolder=td/'bad_source'/'attempt_1'; badfolder.mkdir(parents=True)
    request=req_for([0]); badout=badfolder/'L01_floor_arm1'
    rn=R.Runner('unused.sh',badfolder,badfolder,PLAN,None,time.time()+60,R.RealContract(),parent_env={})
    def badgroup(argv,cwd,env,logf,left,gdir,name):
        badout.mkdir(); (badout/'p2_wrong_kit_a0.json').write_text('{}',encoding='utf-8')
        return 0,None,mock_ends(gdir,name)
    old=R.run_in_group; R.run_in_group=badgroup
    try:
        try: rn._execute(request['name'],request,badout,{})
        except R.Stop as exc: failures.append({'producer':'Runner._execute','stop':exc.code,'kind':classify(rn.records[0]['arms_read'],rn.records[0])})
    finally: R.run_in_group=old
    badrec=rn.records[0]
    edited=summ(badrec)
    fl=R.result_fields(badfolder,edited)
    failures[0]['edited_resume_ok']=fl['resume_ok']
    dest=td/'bad_source'/'attempt_2'; dest.mkdir()
    rr=R.ResumeRunner('unused.sh',badfolder,dest,PLAN,None,time.time()+60,R.RealContract(),parent_env={},src=badfolder,src_n=1)
    try: rr._copy(request['name'],request,dest/badout.name)
    except R.Stop as exc: failures.append({'producer':'ResumeRunner._copy','stop':exc.code,'kind':classify(rr.records[0]['arms_read'],rr.records[0])})
    # Reuse last successful merge object's already bound tiny input, damage only
    # the basename so real read_run rejects before any payload interpretation.
    merge.n=0; merge.keys=set(); merge.records=[]
    u=next(iter(merge.opened.values())); u['consumed']=set()
    r0=next(iter(u['runs'].values())); od=merge.out/u['rel']/r0['outdir']
    payload=next(od.glob('p2_*.json')); payload.rename(od/'p2_wrong_kit_a0.json')
    try: merge.run(r0['kit'],'floor','P0',r0['c'],r0['rj'],1,False)
    except R.Stop as exc: failures.append({'producer':'MergeFetch.run','stop':exc.code,'kind':classify(merge.records[0]['arms_read'],merge.records[0])})
    check('actual_producer_copy_merge_failure',len(failures)==3 and all(x['kind']=='file_ids' and x['stop']=='ARM_JSON_COUNT' for x in failures)
          and failures[0]['edited_resume_ok'] is False,failures)

    # Function-call graph, independently extracted from the AST.
    callers={}
    def walk(node,path=''):
        for child in ast.iter_child_nodes(node):
            if isinstance(child,ast.ClassDef): walk(child,path+child.name+'.')
            elif isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)):
                name=path+child.name
                for call in ast.walk(child):
                    if isinstance(call,ast.Call) and isinstance(call.func,ast.Name):
                        callers.setdefault(call.func.id,set()).add(name)
                walk(child,name+'.')
            else: walk(child,path)
    walk(ast.parse(Path(R.__file__).read_text(encoding='utf-8')))
    shared={k:sorted(callers.get(k,set())) for k in ('arm_file_prefix','arm_public_value_problem','arms_read_record','arms_read_kind')}
    check('shared_contract_call_sites',shared=={
        'arm_file_prefix':['RunnerGraphSource._run','arms_read_kind','read_run'],
        'arm_public_value_problem':['arms_read_kind','read_run'],
        'arms_read_record':['MergeFetch.run','ResumeRunner._copy','Runner._execute'],
        'arms_read_kind':['prior_runs_problem']},shared)

if __name__=='__main__':
    try:
        with tempfile.TemporaryDirectory(prefix='independent_arm_',dir=HERE) as tmp:
            main(Path(tmp))
    except Exception as exc:
        import traceback
        OUT['fatal']={'type':type(exc).__name__,'message':str(exc),'traceback':traceback.format_exc()}
        OUT['unexpected'].append('fatal')
    (HERE/'results.json').write_text(json.dumps(OUT,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'checks':len(OUT['checks']),'unexpected':OUT['unexpected'],'fatal':OUT.get('fatal')},ensure_ascii=False))
    sys.exit(bool(OUT['unexpected']))
