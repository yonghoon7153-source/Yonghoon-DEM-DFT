"""Characterize Windows-only child encoding failures without editing the target."""
from pathlib import Path
import sys,subprocess,tempfile,json,contextlib,io,types
from unittest.mock import patch
R=Path(__file__).resolve().parent;K=R/'repo/docs/data/ps45_unload_20261009';O=R/'evidence/windows_diagnostic';O.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(K));sys.dont_write_bytecode=True;tempfile.tempdir=str(R/'tmp');import ul_reader as u
# Only interpreter encoding changes. All target functions and fixture bytes remain unchanged.
real_run=subprocess.run;calls=[]
def utf8_child(args,*a,**kw):
 cmd=list(args) if isinstance(args,(list,tuple)) else args
 if isinstance(cmd,list) and cmd and cmd[0]==sys.executable and '-X' not in cmd:
  cmd[1:1]=['-X','utf8'];calls.append(cmd)
 return real_run(cmd,*a,**kw)
results=[]
for side in ['baseline','repo']:
 kit=R/side/'docs/data/ps45_unload_20261009';mod=types.ModuleType('reader_'+side);mod.__file__=str(kit/'ul_reader.py');exec(compile((kit/'ul_reader.py').read_bytes(),mod.__file__,'exec'),mod.__dict__)
 # Imported kit libraries are byte-identical on both sides. For native fixture identity, each module HERE still points to its own kit.
 buf=io.StringIO()
 with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf),patch('subprocess.run',side_effect=utf8_child):rc=mod.selftest()
 txt=buf.getvalue();(O/(side+'_reader.log')).write_text(txt,encoding='utf8');results.append({'side':side,'rc':rc,'pass':sum(x.lstrip().startswith('✓') for x in txt.splitlines()),'fail':sum(x.lstrip().startswith('✗') for x in txt.splitlines()),'fail_lines':[x for x in txt.splitlines() if x.lstrip().startswith('✗')]})
(O/'results.json').write_text(json.dumps({'adaptation':'subprocess interpreter -X utf8 only; not unmodified CLI reproduction','results':results,'child_calls':calls},ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(results,ensure_ascii=False,indent=2))
