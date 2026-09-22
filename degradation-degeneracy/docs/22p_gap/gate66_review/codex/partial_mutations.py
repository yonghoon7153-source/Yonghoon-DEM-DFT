"""Supplemental Windows test replay with --noconftest, NOT official replay coverage.
Applies registered text mutations only in fresh disposable copies, never target.
"""
import hashlib,json,os,pathlib,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[1]/'work/gate66-head/degradation-degeneracy'
sys.path.insert(0,str(ROOT/'docs/22p_gap'))
import mutation_replay as mr
dest=HERE/'partial_mutations';dest.mkdir(exist_ok=False)
env=dict(os.environ)
for key in ('PYTHONPATH','PYTHONNOUSERSITE'):env.pop(key,None)
env.update(PYTHONIOENCODING='utf-8',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
summary=[]
for name,source,old,new,selector in mr.MUTANTS:
 if not name.endswith('-g65'):continue
 work=mr._make_sandbox()
 path=work/source.relative_to(ROOT)
 before=path.read_text(encoding='utf-8')
 assert before.count(old)==1,(name,before.count(old))
 # Mechanical registered mutation in the review sandbox, not a production edit.
 path.write_text(before.replace(old,new,1),encoding='utf-8')
 report=dest/(name+'.pytest.json')
 command=[sys.executable,'-m','pytest','tests/test_gate65_defensive.py','tests/test_gate64_defensive.py',
   '--noconftest','-q','-p','no:cacheprovider','-k',selector,'--json-report','--json-report-file='+str(report)]
 start=time.monotonic()
 run=subprocess.run(command,cwd=work,env=env,capture_output=True,timeout=300)
 (dest/(name+'.stdout.bin')).write_bytes(run.stdout)
 (dest/(name+'.stderr.bin')).write_bytes(run.stderr)
 data=json.loads(report.read_text(encoding='utf-8')) if report.exists() else {}
 failed={t['nodeid']:t for t in data.get('tests',[]) if t['outcome']=='failed'}
 skipped=[t['nodeid'] for t in data.get('tests',[]) if t['outcome']=='skipped']
 expected=mr.EXPECT[name]
 rec=dict(name=name,cwd=str(work),command=command,rc=run.returncode,seconds=time.monotonic()-start,
   registered_expected=expected,observed_failed=list(failed),skipped=skipped,summary=data.get('summary'),
   expected_failure_set_matches=set(failed)==set(expected['fail']),
   observed_call_witness_matches={node:expected.get('witness',{}).get(node,'__NO_EXPECT__') in str(t.get('call',{}).get('longrepr','')) for node,t in failed.items()},
   fail_phases={node:[p for p in ('setup','call','teardown') if t.get(p,{}).get('outcome')=='failed'] for node,t in failed.items()},
   mutation_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),target_unchanged=source.read_text(encoding='utf-8')==before,
   limitation='--noconftest supplemental check; no official replay/coverage certification; Linux skips remain unmeasured')
 (dest/(name+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
 summary.append(rec)
 print(json.dumps({k:rec[k] for k in ('name','rc','summary','expected_failure_set_matches','observed_call_witness_matches')},ensure_ascii=True),flush=True)
(dest/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
