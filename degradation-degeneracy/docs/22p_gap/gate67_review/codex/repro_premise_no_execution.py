"""Exercise the two COMMITTED g66_08 parameter values with inherited pytest options.
Real subprocess failures/collection; no fake CompletedProcess and no target edits.
"""
import argparse, importlib.util, json, os, pathlib, sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True)
a=p.parse_args();root=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
sp=importlib.util.spec_from_file_location('g67_subject_test',root/'tests/test_gate66_defensive.py')
tm=importlib.util.module_from_spec(sp);sp.loader.exec_module(tm)
initial=dict(os.environ);rows=[]
try:
 for mode in ('usage_error','collect_only'):
  for label,extra in [('clean',{}),('nousersite',{'PYTHONNOUSERSITE':'1'})]:
   name=mode+'_'+label;report=out/(name+'.pytest.json')
   opts='--g67-option-does-not-exist' if mode=='usage_error' else '--collect-only --json-report --json-report-file="'+report.as_posix()+'"'
   os.environ['PYTEST_ADDOPTS']=opts
   q=tm._premise_run(sys.executable,extra)
   (out/(name+'.stdout.bin')).write_bytes(q.stdout.encode('utf-8'));(out/(name+'.stderr.bin')).write_bytes(q.stderr.encode('utf-8'))
   caught=None
   try:tm.test_g66_08_the_premise_test_does_not_fail_on_an_inherited_env(extra)
   except Exception as e:caught=type(e).__name__+': '+str(e)
   data=json.loads(report.read_text(encoding='utf-8')) if report.exists() else None
   rec=dict(case=name,committed_parameter=extra,inherited_PYTEST_ADDOPTS=opts,child_rc=q.returncode,
    child_stdout=q.stdout,child_stderr=q.stderr,report_summary=data.get('summary') if data else None,
    call_phase_count=sum('call' in t for t in data.get('tests',[])) if data else None,
    committed_test_returned_normally=caught is None,committed_test_exception=caught)
   rows.append(rec);print(json.dumps(rec,ensure_ascii=True),flush=True)
finally:os.environ.clear();os.environ.update(initial)
(out/'observations.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
