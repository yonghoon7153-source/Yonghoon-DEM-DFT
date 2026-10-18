"""Documented re-use of previous independent receipt probe and small regressions."""
from pathlib import Path
import base64, hashlib, json, os, subprocess, sys, time
R=Path(__file__).resolve().parents[1]
E=R/'evidence'
env=os.environ.copy()
env.update(PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONIOENCODING='utf-8',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',TEMP=str(R/'tmp'),TMP=str(R/'tmp'))
env['PYTHONPATH']=os.pathsep.join(map(str,[R/'source/scripts',R/'source/webapp',R.parent/'lhs_coverage_review_20260930/deps',R.parent/'gen2_network_reverify3_20261007/deps']))
old=R.parent/'lhs214_fix_reverify_20261015/probes/receipt_identity.py'
bundled=R/'probes/receipt_identity_original.py.b64'
expected='c73e685d4090a867333d133260def1c1f8d8557900558a84b9deda8acef6eda1'
payload=(base64.b64decode(bundled.read_text(encoding='ascii'),validate=True)
         if '--verify-bundle' in sys.argv or not old.is_file() else old.read_bytes())
assert hashlib.sha256(payload).hexdigest()==expected
s=payload.decode('utf8').replace('\r\n','\n').replace('\r','\n')
if '--verify-bundle' in sys.argv:
    compile(s,str(old),'exec')
    print(json.dumps({'bundle_sha256':expected,'syntax_valid':True}))
    sys.exit(0)
replacements=[('9e3ef54ca228111360bfe5f6d9dad4ebe26d54af','60ba39e224aff48a030dccfe750342f3bf9db61f'),("assert out['variants']['minimal_activate_section3']['bad']==['R0','D1']","assert out['variants']['minimal_activate_section3']['bad']==[]")]
for a,b in replacements:
    assert a in s;s=s.replace(a,b)
# __file__ is this script under new/probes, so old independent probe uses new snapshots.
ns={'__file__':str(__file__),'__name__':'receipt_recheck'}
os.environ.update(env)
log=E/'root_receipt.log'
import contextlib
with log.open('w',encoding='utf8') as f,contextlib.redirect_stdout(f),contextlib.redirect_stderr(f):
    exec(compile(s,str(old),'exec'),ns)
(E/'receipt_probe_adaptation.json').write_text(json.dumps({'original':str(old),'sha256':expected,'replacements':replacements,'paths':'__file__ points to new review probes; algorithms and seven mutations unchanged'},indent=2),encoding='utf8')
print('Receipt probe complete',flush=True)
tasks=[('provenance',['webapp/test_pipeline_provenance.py']),('reread',['scripts/g2_network_reread.py','--selftest']),('reread_v12',['scripts/test_reread_v12.py'])]
rows=[]
for name,args in tasks:
    t=time.monotonic();p=subprocess.run([sys.executable,'-X','utf8','-B',*args],cwd=R/'source',env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=900)
    (E/f'root_{name}.log').write_bytes(p.stdout)
    row={'name':name,'command':args,'rc':p.returncode,'seconds':time.monotonic()-t};rows.append(row)
    print(json.dumps(row),flush=True)
    (E/'root_checks.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
