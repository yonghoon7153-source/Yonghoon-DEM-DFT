from pathlib import Path
import sys,subprocess,json,contextlib,io
from unittest.mock import patch
R=Path(__file__).resolve().parent;K=R/'snapshot/docs/data/ps45_unload_20261009';sys.path.insert(0,str(K));sys.dont_write_bytecode=True;import make_unload_decks as m
run=subprocess.run
def utf8(args,*a,**kw):
 args=list(args)
 if args and args[0]==sys.executable and '-X' not in args:args[1:1]=['-X','utf8']
 return run(args,*a,**kw)
buf=io.StringIO()
with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf),patch('subprocess.run',side_effect=utf8):rc=m.check()
(R/'evidence/checks/deck_check_utf8.log').write_text(buf.getvalue(),encoding='utf8');print('adapted_deck_check_rc=',rc);print(buf.getvalue())
