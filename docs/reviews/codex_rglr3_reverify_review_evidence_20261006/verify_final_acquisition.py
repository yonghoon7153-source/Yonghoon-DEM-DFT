from pathlib import Path
import hashlib,json,shutil
R=Path(__file__).resolve().parent
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
got=json.loads((R/'incoming_manifest.json').read_text(encoding='utf8'))
exp=json.loads((R/'incoming_git_blobs.json').read_text(encoding='utf8'))
eb={x['path']:x['sha'] for x in exp['files']}
for x in got['files']:
 assert x['git_blob']==eb[x['path']],x
 src=R/'incoming'/x['path']
 if not src.exists():src=R/'source'/x['path']
 assert blob(src.read_bytes())==eb[x['path']],x['path']
 p=R/'source'/x['path'];p.parent.mkdir(parents=True,exist_ok=True)
 if src!=p:shutil.copyfile(src,p)
rows=[]
acq=R/'final_acquisition.json'
if not acq.exists():acq=R/'final_acquisition_partial.json'
if acq.exists():
 for x in json.loads(acq.read_text(encoding='utf8'))['files']:
  assert not x.get('error'),x
  p=R/'final_raw'/x['path']
  if not p.exists():p=R/'source'/x['path']
  b=p.read_bytes()
  lf=b.replace(b'\r\n',b'\n')
  candidates=[b,b[:-1],lf,lf[:-1],lf.replace(b'\n',b'\r\n'),lf[:-1].replace(b'\n',b'\r\n')]
  exact=next((v for v in candidates if blob(v)==x['sha']),None)
  assert exact is not None,x
  dest=R/'source'/x['path'];dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(exact)
  rows.append(dict(path=x['path'],git_blob=x['sha'],sha256=hashlib.sha256(exact).hexdigest()))
out=dict(commit=exp['commit'],zip_git_matches=len(got['files']),fetched_verified=len(rows),files=rows)
(R/'evidence/final_integrity.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print({k:v for k,v in out.items() if k!='files'})
