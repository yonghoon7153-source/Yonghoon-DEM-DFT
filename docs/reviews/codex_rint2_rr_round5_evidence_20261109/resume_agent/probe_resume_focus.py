"""Independent focused source/API probes. No solver, process-group or remote execution.
Production ResumeRunner is exercised using repository fixture fake_execute/read_run only.
Windows host identifiers remain actual None values; only O_NONBLOCK=0 regular-file shim; no host mock or POSIX qualification.
"""
import sys, json, hashlib, copy, tempfile, os
from pathlib import Path
OUT=Path(__file__).resolve().parent
REPO=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else OUT.parent/'package'/'repo'
sys.path.insert(0,str(REPO/'scripts'))
import rint_r_chain as R
import test_rint_r_chain as T
if not hasattr(os, 'O_NONBLOCK'): os.O_NONBLOCK=0 # Windows regular-file compatibility only; no FIFO/POSIX qualification
T.RR=R
T.TD=tempfile.mkdtemp(prefix='focused_',dir=OUT)
rows={}
def observe(name, maker):
    aa=maker(name); f,s=aa[-1]; n=len(aa); st=T.rr4_state(aa)
    d={}
    try:
        result,why=R.attempt_result(n,f,s,'independent-probe',st)
        d['writer']={'resume_ok':result['resume_ok'],'cause':result['cause'],'reason':why}
        d['recount']=R.result_line_problem(n,f,result,st=st,found=R._attempt_folders([Path(f).parent]))
    except R.Stop as e:
        d['writer']={'stop':e.code,'reason':e.cause}
    nx=T.rr4_next(st)
    d['next_order']=R.attempt_order_problem(st,nx,T.RR4_PLAN)
    d['presolve_chain']=R.resume_chain_problem(st,nx,n+1,Path(f).parent)
    d['common']=R.resume_provenance_problem(st,n,f,s)
    d['fixture']=str(f)
    rows[name]=d
for nm,fn in [
 ('original_R1',lambda t:T.rr4_edit(T.rr4_two(t,'changed-ceiling'),T.rr4_r1)),
 ('original_R2',lambda t:T.rr4_edit(T.rr4_two(t,'changed-ceiling'),T.rr4_r2)),
 ('original_attempt_null',lambda t:T.rr4_edit(T.rr4_two(t,'changed-ceiling'),T.rr4_null,att={'resume_of':None})),
 ('original_three_attempt_from',lambda t:T.rr4_edit(T.rr4_three(t,'source-ceiling'),T.rr4_rebind)),
 ('honest_two',lambda t:T.rr4_two(t,'source-ceiling')),
 ('honest_three',lambda t:T.rr4_three(t,'newer-different-ceiling')),
 ('honest_partial',lambda t:T.rr4_two(t,'partial',rc=1)),
 ('honest_before_rerun',lambda t:T.rr4_two(t,None,before=True)),
 ('honest_mismatch',lambda t:T.rr4_two(t,'changed-ceiling')),
 ('summaryless_mismatch',lambda t:T.rr5_orphan(T.rr4_two(t,'changed-ceiling'))),
 ('summaryless_same',lambda t:T.rr5_orphan(T.rr4_two(t,'source-ceiling'))),
 ('summaryless_bool',lambda t:T.rr5_orphan(T.rr4_edit(T.rr4_two(t,'source-ceiling'),att={'resume_of':True}))),
 ('summaryless_float',lambda t:T.rr5_orphan(T.rr4_edit(T.rr4_two(t,'source-ceiling'),att={'resume_of':1.0}))),
 ('outdir_alias',lambda t:T.rr4_edit(T.rr4_two(t,'changed-ceiling'),T.rr5_relabel_post)),
 ('skip_rerun',lambda t:T.rr4_edit(T.rr4_two(t,'source-ceiling'),T.rr5_skip_rerun)),
 ('source_not_started',T.rr5_src_no_launch),
 ('signal_after_diff',lambda t:T.rr5_sigafter_real(t,'changed-ceiling')),
 ('signal_after_same',lambda t:T.rr5_sigafter_real(t,'source-ceiling')),
 ('signal_after_missing_folder',lambda t:T.rr5_sigafter_real(t,'changed-ceiling',no_folder=True)),
]: observe(nm,fn)
# Independently composed copied-payload and group-record perturbations.
def changed_copy(t,summaryless=False,field=None):
    a=T.rr4_two(t,'source-ceiling'); f=a[-1][0]
    if field:
        p=f/'groups'/(T.RR4_N1+'.'+field+'.json'); v=json.loads(p.read_text()); v['extra']='changed'; p.write_bytes(R.canon_bytes(v))
    else:
        (f/R.record_outdir(T.rr4_req(1))/T.RR4_FN).write_bytes(b'{"synthetic":"changed copied payload"}')
    return T.rr5_orphan(a) if summaryless else a
observe('copy_payload_changed_summary',lambda t:changed_copy(t))
observe('copy_payload_changed_no_summary',lambda t:changed_copy(t,True))
observe('copy_launch_changed_summary',lambda t:changed_copy(t,field='launch'))
observe('copy_launch_changed_no_summary',lambda t:changed_copy(t,True,field='launch'))
# Missing source and restoration, unchanged destination, same synthetic ledger.
a=T.rr4_two('moved_source','source-ceiling'); st=T.rr4_state(a); f,s=a[-1]; old=a[0][0]; archived=old.with_name('archived_source')
old.rename(archived)
d={}
try: R.attempt_result(2,f,s,'probe',st); d['while_missing']='unexpected_return'
except R.ResultHeld as e: d['while_missing']={'type':type(e).__name__,'stop':e.code,'reason':e.cause}
archived.rename(old)
r,w=R.attempt_result(2,f,s,'probe',st); d['after_restore']={'resume_ok':r['resume_ok'],'reason':w}
rows['moved_source_restored']=d
# Invalid shape regressions use actual next-resume APIs and guard against traceback.
for nm,mut in [('runs_number',lambda s:s.update(runs=5)),('stop_string',lambda s:s.update(stop='invalid'))]:
    rows[nm]=T.rr5_shape(nm,mut)
report={'pin':'abf0911ebc994167ac50132c78207c6c8d4421f1','platform':sys.platform,'python':sys.version,'host_ident':R.host_ident(),
'production_source_sha256':hashlib.sha256((REPO/'scripts/rint_r_chain.py').read_bytes()).hexdigest(),
'fixture_source_sha256':hashlib.sha256((REPO/'scripts/test_rint_r_chain.py').read_bytes()).hexdigest(),
'limits':'Actual API calls and ResumeRunner copy/comparison; fixture fake_execute/read_run; no CLI process launch, no POSIX claim, no research or remote run.', 'rows':rows}
(OUT/'probe_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for k,v in rows.items():
    if isinstance(v,dict) and 'writer'in v: print(k, 'writer=',v['writer'].get('resume_ok',v['writer'].get('stop')),'order=',bool(v.get('next_order')),'chain=',bool(v.get('presolve_chain')),'common=',T.rr4_tag(v.get('common')))
    else: print(k,json.dumps(v,ensure_ascii=False))

