"""Boundary probe: actual ResumeRunner._copy followed by synthetic hard-parent interruption.
No real process is killed. The differing case explicitly injects one copied-payload byte fault;
this is NOT proof that ordinary copytree/disk-full itself corrupts completed payload bytes.
"""
import sys,os,json,tempfile,contextlib,io,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent
REPO=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else OUT.parent/'package'/'repo'
sys.path.insert(0,str(REPO/'scripts'))
import rint_r_chain as R
import test_rint_r_chain as T
if not hasattr(os,'O_NONBLOCK'): os.O_NONBLOCK=0
T.RR=R; T.TD=tempfile.mkdtemp(prefix='copyboundary_',dir=OUT)
report={}
for mutate in (False,True):
 base=Path(T.TD)/str(mutate); a1=T.rr4_first(base); src=a1[0]; dst=T.rr4_att(base/'attempt_2',2,1)
 runner=R.ResumeRunner('UNUSED',src,dst,{},None,0,{},parent_env={},prefix='L',src=src,src_n=1,machine=T.MACH)
 runner.env_delta=lambda *_a:{}
 class SimulatedParentDeath(BaseException): pass
 def interruption(outdir,*a,**kw):
  if mutate: (Path(outdir)/T.RR4_FN).write_bytes(R.canon_bytes({'synthetic':'single copied payload byte fault'}))
  raise SimulatedParentDeath()
 try:
  with T.rc_patch(read_run=interruption),contextlib.redirect_stdout(io.StringIO()):
   runner.run(T.SBE_KIT,'floor','P0',None,'inf',1)
 except SimulatedParentDeath: pass
 atts=[a1,(dst,None)]; st=T.rr4_state(atts); nx=T.rr4_next(st)
 result,why=R.attempt_result(2,dst,None,'probe',st)
 nxt=R.ResumeRunner('UNUSED',dst,base/'attempt_3',{},None,0,{},parent_env={},prefix='L',src=dst,src_n=2,machine=T.MACH)
 od=R.record_outdir(T.rr4_req(1)); source=(src/od/T.RR4_FN).read_bytes(); target=(dst/od/T.RR4_FN).read_bytes()
 report[str(mutate)]={'payload_equal_source':source==target,'source_sha':hashlib.sha256(source).hexdigest(),'copied_sha':hashlib.sha256(target).hexdigest(),
 'summary_state':R.stage_summary_read(dst)[1], 'groups_problem':R.attempt_groups_problem(dst),'writer_result':result,'writer_reason':why,
 'next_order':R.attempt_order_problem(st,nx,T.RR4_PLAN),'presolve_chain':R.resume_chain_problem(st,nx,3,base),'next_src_done_L01':nxt._src_done(T.RR4_N1,od),
 'interpretation':'single payload fault injected' if mutate else 'honest interrupted copy control', 'folder':str(dst)}
(OUT/'copy_boundary_results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
