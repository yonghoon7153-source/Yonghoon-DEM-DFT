"""Drive real build_v13/check_v13 with author synthetic handover fixture.
Only upstream tau-row re-read is a controlled stub, equally in control/mutants;
we do NOT claim a real 194 batch passed. Gate and release code are unmodified.
"""
from pathlib import Path
import sys,ast,json,copy,contextlib,io,os
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];S=R/'source';D=R/'evidence/release_gate';D.mkdir(exist_ok=True)
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
p=S/'scripts/test_lhs_release_v13.py';code=p.read_text(encoding='utf8');prefix=code.split("print('V0  API')")[0]
ns={'__file__':str(p),'__name__':'review_fixture'};exec(compile(prefix,str(p),'exec'),ns)
lb=ns['LRB'];hd=ns['make_g2_handover_dir'](str(D/'handover'));verdict=D/'TEST_ONLY_NOT_A_GO.md';verdict.write_text('Synthetic gate test. NOT production approval.\n',encoding='utf8')
cases=[]
for label in ['pass_control','explicit_failure','absent_reread','invalid_reread','empty_reread','null_nfail','refused_audit','unsealed_audit']:
 rr=copy.deepcopy(ns['RR_OK'])
 if label=='explicit_failure':rr['n_fail']=1
 if label=='empty_reread':rr={}
 if label=='null_nfail':rr['n_fail']=None
 if label=='absent_reread':rr=None
 br=Path(ns['make_batch_root'](str(D/label),reread=rr))
 if label=='invalid_reread':(br/'reread.json').write_text('{',encoding='utf8')
 aj=dict(refused=False,eligibility=dict(kind='current'),verdicts=dict(SEALED=194))
 if label=='refused_audit':aj=dict(refused=True,eligibility=dict(kind='invalid',problems=['G2RR2-01 missing input_digest']))
 if label=='unsealed_audit':aj=dict(refused=False,eligibility=dict(kind='current'),verdicts=dict(UNSEALED=194),generation_problems=['not g2'])
 (br/'seal_audit.json').write_text(json.dumps(aj),encoding='utf8')
 out=br/'output';log=io.StringIO();calls=[]
 with patch.object(lb,'v13_reread_tau',lambda ds,*args:calls.append(ds) or []),contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  try:
   report=lb.build_v13(out_dir=str(out),handover_dir=hd,batch_root=str(br),date='20991231',codex_verdict=str(verdict))
   check=lb.check_v13(str(out),hd);result=dict(label=label,accepted=True,check=check,report=report,tau_stub_calls=calls)
  except Exception as ex:result=dict(label=label,accepted=False,error=f'{type(ex).__name__}: {ex}',tau_stub_calls=calls)
 (br/'build.log').write_text(log.getvalue(),encoding='utf8');cases.append(result);print(label,result['accepted'],result.get('error'),result.get('check'),flush=True)
(R/'evidence/release_gate.json').write_text(json.dumps(dict(scope=__doc__,cases=cases),ensure_ascii=False,indent=2),encoding='utf8')
