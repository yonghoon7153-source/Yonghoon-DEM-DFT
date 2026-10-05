from pathlib import Path
import os, subprocess, sys, json
ROOT=Path(__file__).resolve().parents[1]
env=os.environ.copy()
env['PYTHONUTF8']='1'; env['PYTHONIOENCODING']='utf-8'; env['PYTHONDONTWRITEBYTECODE']='1'
env['PYTHONPATH']=str(ROOT.parent/'lhs_coverage_review_20260930/deps')+os.pathsep+str(ROOT/'source/scripts')
jobs=[('step3_rint',['scripts/step3_sigma.py','--selftest-rint']),
      ('receipt_integration',['scripts/test_rint_receipts.py']),
      ('rint03',['scripts/rint03_je_compare.py','--selftest'])]
summary=[]
for name,args in jobs:
    r=subprocess.run([sys.executable,*args],cwd=ROOT/'source',env=env,text=True,encoding='utf-8',capture_output=True,timeout=1200)
    log=r.stdout+r.stderr
    (ROOT/'evidence_g1'/f'{name}.log').write_text(log,encoding='utf-8')
    summary.append({'name':name,'exit':r.returncode,'last_lines':log.splitlines()[-12:]})
    print(json.dumps(summary[-1],ensure_ascii=False),flush=True)
(ROOT/'evidence_g1/baselines.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
