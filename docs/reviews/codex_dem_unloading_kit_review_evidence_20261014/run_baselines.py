from pathlib import Path
import subprocess,sys,json,concurrent.futures,time,os
R=Path(__file__).resolve().parent; K=R/'source/docs/data/ps45_unload_20261009'; E=R/'evidence';E.mkdir(exist_ok=True)
TEMP=R/'tmp_baseline';TEMP.mkdir(exist_ok=True)
ENV=dict(os.environ,TMP=str(TEMP),TEMP=str(TEMP),TMPDIR=str(TEMP),PYTHONUTF8='1')
ENV['PATH']='C:/Program Files/Git/bin;C:/Program Files/Git/usr/bin;'+str(Path(sys.executable).parent)+';'+ENV['PATH']
jobs=[(x,['--selftest']) for x in ['ul_lib','ul_s3','ul_observers','ul_gates','ul_reader','seal_kit','make_unload_decks','ul_runner_test','history_test/make_history_decks','history_test/read_history']]
jobs += [('make_unload_decks',['--check']),('seal_kit',['--check']),('seal_kit',['--rules']),('history_test/make_history_decks',['--check'])]
def run(job):
    x,args=job;tag=x.replace('/','_')+'_'+args[0].strip('-');start=time.time()
    cmd=[sys.executable,'-X','utf8','-B','-I',str(K/(x+'.py')),*args]
    try:
        p=subprocess.run(cmd,cwd=R/'source',capture_output=True,text=True,encoding='utf8',errors='replace',timeout=180,env=ENV)
        out=p.stdout+'\nSTDERR\n'+p.stderr; rc=p.returncode
    except Exception as ex:out=repr(ex);rc=None
    (E/(tag+'.log')).write_text(out,encoding='utf8')
    return {'name':tag,'argv':cmd,'rc':rc,'seconds':time.time()-start,'tail':out.splitlines()[-8:]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run,jobs))
(E/'baseline.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
for r in results:print(r['name'],r['rc'],r['tail'])
