"""Synthetic bound gate fixtures; real build/check; tau-only upstream is a stub.
This does not certify any real 194 batch or its values.
"""
from pathlib import Path
import sys,json,copy,contextlib,io,tempfile
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];S=R/'source';E=R/'evidence';P=E/'release_gate';P.mkdir(exist_ok=True);D=Path(tempfile.mkdtemp(prefix='run_',dir=P))
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
p=S/'scripts/test_lhs_release_v13.py';ns={'__file__':str(p),'__name__':'review_fixture'}
exec(compile(p.read_text(encoding='utf8').split("print('V0  API')")[0],str(p),'exec'),ns)
lb=ns['LRB'];hd=ns['make_g2_handover_dir'](str(D/'handover'));verdict=D/'TEST_ONLY_NOT_A_GO.md';verdict.write_text('SYNTHETIC TEST ONLY\n',encoding='utf8')
cases=[]
for label in ('control','absent_reread','null_nfail','failed_audit','wrong_manifest','reread_checks_false','reread_cases_missing','audit_observation_failed'):
 br=Path(ns['make_batch_root'](str(D/label)))
 rr=json.loads((br/'reread.json').read_text());aa=json.loads((br/'seal_audit.json').read_text())
 rr.update(meta=[dict(name='M2 all completed',ok=True,detail='synthetic gate-only fixture')],
           cases=[dict(case=c,cohort=h,checks=[dict(name='K1',ok=True,detail='synthetic gate-only fixture')]) for c,h in ns['PROD194']])
 if label=='absent_reread':(br/'reread.json').unlink()
 if label=='null_nfail':rr['n_fail']=None
 if label=='failed_audit':aa['input_problems']=['raw bytes mismatch']
 if label=='wrong_manifest':rr['manifest_sha256']='0'*64
 if label=='reread_checks_false':
  rr['meta'][0].update(ok=False,detail='explicit failure')
 if label=='reread_cases_missing':rr['cases']=[];rr['meta']=[]
 if label=='audit_observation_failed':aa['import_observation']={'problems':['log truncated'],'outside':['scripts/unsealed.py']}
 if label!='absent_reread':(br/'reread.json').write_text(json.dumps(rr),encoding='utf8')
 (br/'seal_audit.json').write_text(json.dumps(aa),encoding='utf8')
 log=io.StringIO()
 with patch.object(lb,'v13_reread_tau',lambda *a,**k:[]),contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  try:
   rep=lb.build_v13(out_dir=str(br/'out'),handover_dir=hd,batch_root=str(br),date='20991231',codex_verdict=str(verdict))
   check=lb.check_v13(str(br/'out'),hd);row=dict(label=label,accepted=True,check=check)
  except Exception as ex:row=dict(label=label,accepted=False,error=f'{type(ex).__name__}: {ex}')
 cases.append(row);(br/'build.log').write_text(log.getvalue(),encoding='utf8');print(json.dumps(row,ensure_ascii=False),flush=True)
(E/'release_gate.json').write_text(json.dumps(dict(scope=__doc__,artifact_root=str(D),cases=cases),ensure_ascii=False,indent=2),encoding='utf8')
