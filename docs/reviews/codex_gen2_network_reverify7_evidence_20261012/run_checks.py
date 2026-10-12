from pathlib import Path
import os,sys,subprocess,json,time,concurrent.futures
R=Path(__file__).resolve().parent;S=R/'source';E=R/'evidence'
(R/'tmp').mkdir(exist_ok=True)
ENV=dict(os.environ,PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MPLBACKEND='Agg')
ENV['PYTHONPATH']=os.pathsep.join([str(R.parent/'lhs_coverage_review_20260930/deps'),str(R.parent/'gen2_network_reverify3_20261007/deps'),str(S/'scripts'),str(S/'webapp')])
ENV.update(TMP=str(R/'tmp'),TEMP=str(R/'tmp'),TMPDIR=str(R/'tmp'))
tests={'reread':['scripts/g2_network_reread.py','--selftest'],'smoke':['scripts/wsl_network_smoke.py','--selftest'],
       'smoke_real':['scripts/wsl_network_smoke.py','--selftest-real']}
def run(name):
    argv=tests.get(name,[str(R/'probes'/f'{name}.py')]);start=time.monotonic()
    try:
        p=subprocess.run([sys.executable,'-X','utf8','-B',*argv],cwd=S,env=ENV,capture_output=True,text=True,encoding='utf8',errors='replace',timeout=600)
        output=p.stdout+p.stderr;rc=p.returncode
    except subprocess.TimeoutExpired as ex:
        output=str(ex.stdout)+str(ex.stderr);rc=124
    (E/f'{name}.log').write_text(output,encoding='utf8')
    row=dict(name=name,argv=argv,rc=rc,seconds=time.monotonic()-start,tail=output.splitlines()[-7:])
    (E/f'run_{name}.json').write_text(json.dumps(row,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(row,ensure_ascii=False),flush=True);return row
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,sys.argv[1:] or ['reread','smoke']))
    sys.exit(any(r['rc']!=0 for r in rows))
