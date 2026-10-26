"""Run an unchanged supplied Python harness; child UTF-8 encoding only on Windows."""
import sys,subprocess,runpy
from unittest.mock import patch
original=subprocess.run
calls=[]
def child_utf8(args,*a,**kw):
 args=list(args)
 if args and str(args[0]).lower()==sys.executable.lower() and '-X' not in args:args[1:1]=['-X','utf8']
 return original(args,*a,**kw)
script,*argv=sys.argv[1:];sys.argv=[script,*argv]
with patch('subprocess.run',side_effect=child_utf8):runpy.run_path(script,run_name='__main__')
