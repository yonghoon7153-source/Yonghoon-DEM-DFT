from pathlib import Path
import os,sys,subprocess,json,time,concurrent.futures
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence'
sys.stdout.reconfigure(encoding='utf8');(R/'tmp').mkdir(exist_ok=True);E.mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
ENV['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps'),str(S/'scripts'),str(S/'webapp')])
ENV.update(TMP=str(R/'tmp'),TEMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
tests={'release':['scripts/test_lhs_release_v13.py'],'reread':['scripts/g2_network_reread.py','--selftest'],
       'publication':['webapp/test_gen2_publication_handover.py'],'role':['scripts/test_gen2_role_contract.py']}
EXTRA=[]
def run(name):
    argv=tests.get(name,[str(R/'probes'/f'{name}.py')])+EXTRA;start=time.monotonic()
    p=subprocess.run([sys.executable,'-B',*argv],cwd=S,env=ENV,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=600)
    (E/f'{name}.log').write_text(p.stdout+p.stderr,encoding='utf8')
    row=dict(name=name,argv=argv,rc=p.returncode,seconds=time.monotonic()-start,tail=(p.stdout+p.stderr).splitlines()[-4:]);print(json.dumps(row,ensure_ascii=False),flush=True);return row
if __name__=='__main__':
    names=sys.argv[1:] or list(tests)
    if '--' in names:
        pos=names.index('--');EXTRA=names[pos+1:];names=names[:pos]
        assert len(names)==1,'Forwarded arguments require one probe'
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,names))
    (E/('runs_'+'_'.join(names)+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
    sys.exit(any(x['rc']!=0 for x in rows))
