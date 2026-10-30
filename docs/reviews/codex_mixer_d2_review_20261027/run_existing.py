from pathlib import Path
import sys, os, subprocess, runpy, json, traceback
ROOT=Path(__file__).resolve().parent
TAG, SCRIPT=sys.argv[1:3]
snapshot=ROOT/TAG/'snapshot'; evidence=ROOT/TAG/'evidence'
(ROOT/'tmp').mkdir(exist_ok=True)
os.environ['TMP']=os.environ['TEMP']=str(ROOT/'tmp')
os.chdir(snapshot);sys.path.insert(0,str(snapshot/'scripts'))
# Test-only Windows adaptation: spawned Python processes receive explicit UTF-8.
# Production source bytes and evaluated guards are unchanged.
original=subprocess.Popen
class UTF8Popen(original):
 def __init__(self,args,*a,**kw):
  if isinstance(args,(list,tuple)) and args and Path(str(args[0])).resolve()==Path(sys.executable).resolve():
   args=[args[0],'-X','utf8',*args[1:]]
  super().__init__(args,*a,**kw)
subprocess.Popen=UTF8Popen
sys.argv=[str(snapshot/'scripts'/SCRIPT),*sys.argv[3:]]
runpy.run_path(sys.argv[0],run_name='__main__')
