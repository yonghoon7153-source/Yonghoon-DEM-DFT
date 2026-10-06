from pathlib import Path
import json,hashlib,urllib.request
R=Path(__file__).resolve().parent
for d in ('probes','evidence','inputs'): (R/d).mkdir(exist_ok=True)
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
rows=[]
for mf in ('acquisition.json','acquisition_extra.json','raw_manifest.json','acquisition_web.json','acquisition_security.json'):
 for r in json.loads((R/mf).read_text(encoding='utf8')):
  if 'error' in r: continue
  p=R/'source'/r['path'];b=p.read_bytes() if p.exists() else b''
  if len(b)<2:
   url='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+r['ref']+'/'+r['path']
   with urllib.request.urlopen(url,timeout=90) as resp:b=resp.read()
   assert blob(b)==r['sha'],r['path']
   p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
  if blob(b)!=r['sha']:
   c=b.replace(b'\r\n',b'\n')
   opts=[b[:-1],c,c[:-1],c.replace(b'\n',b'\r\n'),c[:-1].replace(b'\n',b'\r\n')]
   hit=next((v for v in opts if blob(v)==r['sha']),None)
   if hit is None: raise ValueError(r['path'])
   p.write_bytes(hit);b=hit
  assert blob(b)==r['sha']
  rows.append(dict(r,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b)))
(R/'source_manifest.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')
print('Verified',len(rows),'pinned Git blobs')
