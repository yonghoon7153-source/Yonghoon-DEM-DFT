"""Run immutable tests; optionally current tests against baseline production modules."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
R=Path(__file__).resolve().parents[1]
BASE=R.parent/'rint_g2_impl_reverify_20261015/source'
mode=sys.argv[1] if len(sys.argv)>1 else 'new'
if mode=='exec-old':
    # Current assertions, old __file__ location/import tree; no old file written.
    test=sys.argv[2]
    text=(R/'source/scripts'/test).read_text(encoding='utf8')
    virtual=BASE/'scripts'/test
    sys.path.insert(0,str(BASE/'scripts'))
    sys.argv=[str(virtual)]
    exec(compile(text,str(virtual),'exec'),dict(__name__='__main__',__file__=str(virtual)))
    raise SystemExit()

paths=[R/'support',R/'source/scripts',
       R.parent/'lhs_coverage_review_20260930/deps',
       R.parent/'gen2_network_reverify3_20261007/deps']
env=dict(os.environ)
env.update(PYTHONPATH=os.pathsep.join(map(str,paths)),PYTHONDONTWRITEBYTECODE='1',
           PYTHONUTF8='1',PYTHONIOENCODING='utf-8',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',
           MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1',TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'),
           SUPABASE_URL='',SUPABASE_KEY='')
for key,sub in [('WEBAPP_UPLOAD_FOLDER','uploads'),('WEBAPP_RESULTS_FOLDER','results'),
                ('WEBAPP_ARCHIVE_FOLDER','archive'),('WEBAPP_MPM_LAB_FOLDER','mpm_lab'),('MPLCONFIGDIR','mpl')]:
    env[key]=str(R/'tmp'/sub)
if mode=='old':
    tasks=[['test_rint_g2_join.py'],['test_rint_g2_am_iface.py'],['test_rint_g2_rrm.py']]
else:
    tasks=[['test_rint_g2_join.py'],['test_rint_g2_am_iface.py'],['test_rint_g2_rrm.py'],
           ['test_rint_t4_census.py'],['test_rint_t43_order.py'],['test_rint_t2_dev.py'],
           ['step3_sigma.py','--selftest'],['step3_sigma.py','--selftest-rint'],
           ['rint_t41_census.py','--selftest']]
rows=[]
for args in tasks:
    cmd=[sys.executable,'-X','utf8','-B']
    if mode=='old': cmd += [str(Path(__file__).resolve()),'exec-old',args[0]]
    else: cmd += [str(R/'source/scripts'/args[0]),*args[1:]]
    start=time.monotonic()
    p=subprocess.run(cmd,cwd=BASE if mode=='old' else R/'source',env=env,capture_output=True,timeout=600)
    label='_'.join(args).replace('.py','').replace('--','')
    data=p.stdout+p.stderr
    (R/'evidence'/f'submitted_{mode}_{label}.log').write_bytes(data)
    row=dict(mode=mode,command=cmd,rc=p.returncode,seconds=time.monotonic()-start,
             log_sha256=hashlib.sha256(data).hexdigest(),tail=data.decode('utf8','replace').splitlines()[-8:])
    rows.append(row)
    (R/'evidence'/f'submitted_{mode}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(row,ensure_ascii=False),flush=True)
