from pathlib import Path
import sys,subprocess,tempfile,json,contextlib,io
from unittest.mock import patch
R=Path(__file__).resolve().parent;K=R/'snapshot/docs/data/ps45_unload_20261009';O=R/'evidence/utf8_selftest';O.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(K));sys.dont_write_bytecode=True;tempfile.tempdir=str(R/'tmp');import ul_reader as u
real_run=subprocess.run;calls=[]
def utf8_child(args,*a,**kw):
 cmd=list(args) if isinstance(args,(list,tuple)) else args
 if isinstance(cmd,list) and cmd and cmd[0]==sys.executable and '-X' not in cmd:
  cmd[1:1]=['-X','utf8'];calls.append(cmd)
 return real_run(cmd,*a,**kw)
buf=io.StringIO()
with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf),patch('subprocess.run',side_effect=utf8_child):rc=u.selftest()
txt=buf.getvalue();(O/'reader.log').write_text(txt,encoding='utf8')
report={'adaptation':'child interpreter -X utf8 only; target functions/files unchanged; not raw CLI reproduction','rc':rc,'pass':sum(x.lstrip().startswith('✓') for x in txt.splitlines()),'fail':sum(x.lstrip().startswith('✗') for x in txt.splitlines()),'fail_lines':[x for x in txt.splitlines() if x.lstrip().startswith('✗')],'child_calls':calls}
(O/'result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print({k:report[k] for k in ['rc','pass','fail']})
