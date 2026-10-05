"""Explicit environment-only adapters; never claim native/WSL test coverage."""
import hashlib,json,os,runpy,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1]; S=R/'source'
sys.path[:0]=[str(S/'scripts'),str(S/'webapp')]
kind=sys.argv[1]
if kind=='batch':
 def hardlink_instead(self,target,target_is_directory=False):
  if target_is_directory or not Path(target).is_file(): raise RuntimeError('adapter covers fixture files only')
  os.link(target,self)
 Path.symlink_to=hardlink_instead
 print('ENV ADAPTER: Windows symlink privilege unavailable; file-only hardlinks for immutable temporary fixtures. Not native symlink/WSL validation.',flush=True)
 target=S/'scripts/lhs_webapp_batch.py'; sys.argv=[str(target),'--selftest']
elif kind=='labels':
 refs=json.loads((Path(__file__).parent/'column_blobs.json').read_text())
 original=subprocess.run
 def pinned_git(cmd,*args,**kwargs):
  if len(cmd)>4 and cmd[0]=='git' and cmd[1]=='-C' and Path(cmd[2]).resolve()==S.resolve() and cmd[3]=='show' and str(cmd[4]).startswith('HEAD:'):
   p=cmd[4][5:].replace('\\','/'); b=(S/p).read_bytes()
   got=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
   if got!=refs['files'].get(p): raise RuntimeError('Pinned blob verification failed: '+p)
   print('ENV ADAPTER: HEAD:'+p+' -> verified pinned commit blob '+got,flush=True)
   return subprocess.CompletedProcess(cmd,0,b,b'')
  return original(cmd,*args,**kwargs)
 subprocess.run=pinned_git
 print('ENV ADAPTER: standalone snapshot has no .git. Only HEAD:columns lookups substituted with independently SHA1-verified pinned Git blobs.',flush=True)
 target=S/'webapp/test_tau_labels.py'; sys.argv=[str(target)]
else: raise ValueError(kind)
runpy.run_path(str(target),run_name='__main__')
