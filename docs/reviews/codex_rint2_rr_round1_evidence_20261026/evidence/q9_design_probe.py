"""Small process/decision probes only. No physical solver or campaign."""
from pathlib import Path
import contextlib, io, json, math, os, runpy, subprocess, sys, time, uuid
ROOT=Path(__file__).absolute().parents[1];WORK=ROOT.parent
sys.path[:0]=[str(ROOT/'repo/scripts'),str(WORK/'lhs_coverage_review_20260930/deps'),str(WORK/'gen2_network_reverify3_20261007/deps')]
os.environ['OPENBLAS_NUM_THREADS']=os.environ['OMP_NUM_THREADS']='1'
import rint_r_chain as r
out={'scope':'Design acceptance probes; not an implemented unit merger or physical solver','python':sys.version}
buf=io.StringIO()
with contextlib.redirect_stdout(buf):runpy.run_path(str(ROOT/'repo/docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.py'))
actual=json.loads(buf.getvalue());submitted=json.loads((ROOT/'repo/docs/reviews/rint2_rr_fix_evidence_20261023/q9_time_budget.json').read_text('utf8'))
out['time_budget']={'same_as_submitted':actual==submitted,'recomputed':actual}
bound=r.GRADE_INFORMATIVE_MAX
out['one_ulp_grade_boundary']={'scope':'Actual grade_W at boundary and one ULP above; not measured cross-platform libm difference','width_at':bound,'at':r.grade_W(bound),'width_above':math.nextafter(bound,math.inf),'above':r.grade_W(math.nextafter(bound,math.inf)),'same_p_lower_log_bound':math.log((1-1e-4)/(1+1e-4))}
tmp=ROOT/'tmp'/('parent_death_'+uuid.uuid4().hex);tmp.mkdir(parents=True)
child="from pathlib import Path;import sys,time;time.sleep(1.5);Path(sys.argv[1]).write_text('synthetic marker; no solve',encoding='utf8')"
parent="import subprocess,sys,time;from pathlib import Path;p=subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2]],creationflags=(0x08000000 if sys.platform=='win32' else 0));Path(sys.argv[3]).write_text(str(p.pid),encoding='ascii');time.sleep(10)"
kw={'creationflags':0x08000000|0x00000200} if os.name=='nt' else {'start_new_session':True}
p=subprocess.Popen([sys.executable,'-c',parent,child,str(tmp/'marker'),str(tmp/'child.pid')],**kw)
try:
 deadline=time.monotonic()+5
 while not (tmp/'child.pid').exists() and time.monotonic()<deadline:time.sleep(.01)
 assert (tmp/'child.pid').exists(),'child handshake missing'
 p.kill();p.wait(timeout=3);before=(tmp/'marker').exists();deadline=time.monotonic()+5
 while not (tmp/'marker').exists() and time.monotonic()<deadline:time.sleep(.01)
 out['parent_death']={'platform':sys.platform,'parent_exited':p.poll() is not None,'marker_immediately_after_parent_death':before,'marker_written_later_by_child':(tmp/'marker').exists(),'meaning':'Parent death and no current marker do not prove whole-group quiescence. Design already requires quiescence; implementation must enforce it.'}
finally:
 if p.poll() is None:p.kill();p.wait(timeout=3)
assert out['time_budget']['same_as_submitted']
assert out['parent_death']['marker_written_later_by_child']
(ROOT/'evidence/q9_design_probe.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(out,ensure_ascii=False,indent=2))
