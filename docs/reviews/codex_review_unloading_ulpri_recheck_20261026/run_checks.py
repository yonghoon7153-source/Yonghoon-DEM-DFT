from pathlib import Path
import os,sys,json,subprocess,time,hashlib
R=Path(__file__).resolve().parent;K=R/'snapshot/docs/data/ps45_unload_20261009';O=R/'evidence/checks';O.mkdir(exist_ok=False)
env=dict(os.environ,TEMP=str(R/'tmp'),TMP=str(R/'tmp'),TMPDIR=str(R/'tmp'),OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONUTF8='1');env['PATH']=r'C:\Program Files\Git\bin;'+env['PATH']
cmds=[('seal_selftest','seal_kit.py','--selftest'),('seal_check','seal_kit.py','--check'),('deck_check','make_unload_decks.py','--check'),('history_deck_check','history_test/make_history_decks.py','--check')];results=[]
for n,s,arg in cmds:
 cmd=[sys.executable,'-I','-X','utf8','-B',str(K/s),arg];p=subprocess.run(cmd,cwd=K,env=env,capture_output=True,timeout=240);(O/(n+'.log')).write_bytes(p.stdout+p.stderr);results.append(dict(name=n,command=cmd,rc=p.returncode,last=(p.stdout+p.stderr).decode('utf8','replace').splitlines()[-3:]));print(results[-1],flush=True)
(O/'result.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
