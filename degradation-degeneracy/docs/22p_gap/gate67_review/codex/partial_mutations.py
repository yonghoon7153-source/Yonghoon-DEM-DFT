"""Supplemental Windows replay, not official mutation coverage.
Registered preimages only, fresh sandbox for each; baseline then mutant.
"""
import argparse, hashlib, json, os, pathlib, subprocess, sys, tempfile, time
p=argparse.ArgumentParser();p.add_argument('--repo',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True)
a=p.parse_args();root=a.repo.resolve();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(root/'docs/22p_gap'));import mutation_replay as mr
names={
 'parent-compares-the-loaded-origin-g66','the-premise-uses-a-controlled-env-g66','the-replay-context-is-measured-once-g66',
 'parent-customization-uses-the-path-finder-g63','usercustomize-follows-the-startup-activation-g64',
 'search-path-comes-from-the-replay-context-g65','the-fixture-measures-its-premise-g65',
 'explicit-import-is-an-ordinary-import-g65','namespace-is-loaded-code-free-not-absent-g65',
}
env=dict(os.environ)
for k in ('PYTHONPATH','PYTHONNOUSERSITE','PYTEST_ADDOPTS'):env.pop(k,None)
env.update(PYTHONIOENCODING='utf-8',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
# gate63 imports fcntl at module scope: it is not collected on Windows.
# F3's receipt_62 control remains executable, but is only partial EXPECT coverage.
tests=['tests/test_evidence_receipt_62.py','tests/test_gate64_defensive.py','tests/test_gate65_defensive.py','tests/test_gate66_defensive.py']
summary=[]
for name,source,old,new,selector in mr.MUTANTS:
 if name not in names:continue
 work=mr._make_sandbox();path=work/source.relative_to(root);before=path.read_bytes()
 assert before.count(old.encode('utf-8'))==1,name
 phases={}
 for phase in ('baseline','mutant'):
  if phase=='mutant':path.write_bytes(before.replace(old.encode('utf-8'),new.encode('utf-8'),1))
  report=out/(name+'.'+phase+'.pytest.json')
  temp=pathlib.Path(tempfile.mkdtemp(prefix='g67pt_'))
  phase_env=dict(env, PYTEST_DEBUG_TEMPROOT=str(temp))
  cmd=[sys.executable,'-m','pytest',*tests,'--noconftest','-q','-p','no:cacheprovider','-k',selector,'--json-report','--json-report-file='+str(report)]
  t=time.monotonic();r=subprocess.run(cmd,cwd=work,env=phase_env,capture_output=True,timeout=300)
  (out/(name+'.'+phase+'.stdout.bin')).write_bytes(r.stdout);(out/(name+'.'+phase+'.stderr.bin')).write_bytes(r.stderr)
  data=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
  failed={x['nodeid']:x for x in data.get('tests',[]) if x['outcome']=='failed'}
  expected=mr.EXPECT[name]
  phases[phase]=dict(command=cmd,pytest_temp_root=str(temp),rc=r.returncode,seconds=time.monotonic()-t,summary=data.get('summary'),
   observed_failed=list(failed),skipped=[x['nodeid'] for x in data.get('tests',[]) if x['outcome']=='skipped'],
   expected_failure_set_matches=set(failed)==set(expected['fail']),
   call_witness_matches={node:expected.get('witness',{}).get(node,'__NONE__') in str(x.get('call',{}).get('longrepr','')) for node,x in failed.items()},
   failure_phases={node:[s for s in ('setup','call','teardown') if x.get(s,{}).get('outcome')=='failed'] for node,x in failed.items()})
 rec=dict(name=name,cwd=str(work),registered_expected=expected,phases=phases,target_unchanged=source.read_bytes()==before,
   scope='--noconftest supplemental check, no official replay/coverage claim; Linux kernel not substituted')
 (out/(name+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8');summary.append(rec)
 print(json.dumps({'name':name,'baseline':phases['baseline']['summary'],'mutant':phases['mutant']['summary'],'exact':phases['mutant']['expected_failure_set_matches'],'witness':phases['mutant']['call_witness_matches']},ensure_ascii=True),flush=True)
assert len(summary)==len(names),(len(summary),len(names))
(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
