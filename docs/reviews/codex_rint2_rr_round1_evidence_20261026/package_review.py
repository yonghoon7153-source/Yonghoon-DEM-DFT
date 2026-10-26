from pathlib import Path
import os,json,hashlib,zipfile
R0=Path(__file__).absolute().parent
s=str(R0);R=Path('\\\\?\\'+s) if os.name=='nt' and not s.startswith('\\\\?\\') else R0

def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
checks=[]
for e in json.loads((R/'evidence/zip_pin_checks.json').read_text('utf8')):
 b=(R/'repo'/e['path']).read_bytes();checks.append({'origin':'zip','path':e['path'],'ok':blob(b)==e['git_blob']})
for name in ['source_manifest.json','extra_source_manifest.json']:
 for e in json.loads((R/'evidence'/name).read_text('utf8'))['files']:
  b=(R/e['side']/e['path']).read_bytes();checks.append({'origin':name,'path':e['side']+'/'+e['path'],'ok':blob(b)==e['git_blob'] and hashlib.sha256(b).hexdigest()==e['sha256']})
assert all(x['ok'] for x in checks)
res={'pin':'9bec6b7646374daed0d3edbb9647f9f46d302750','checks':len(checks),'mismatches':0,'all_downloaded_source_and_original_zip_blobs_unchanged':True,'details':checks}
(R/'evidence/final_integrity.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf8')
files=[]
for p in R.rglob('*'):
 if not p.is_file():continue
 rel=p.relative_to(R).as_posix()
 if rel.startswith('tmp/') or '/__pycache__/' in rel or p.suffix in ('.pyc','.zip') or p.name=='MANIFEST.sha256':continue
 files.append((rel,p))
files.sort()
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+rel+'\n' for rel,p in files)
(R/'MANIFEST.sha256').write_text(manifest,encoding='utf8')
files.append(('MANIFEST.sha256',R/'MANIFEST.sha256'))
zpath=R0.parent/'codex_rint2_rr_round1_review_20261026.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as z:
 for rel,p in files:z.write(p,'rint2_rr_round1_review_20261026/'+rel)
with zipfile.ZipFile(zpath) as z:assert z.testzip() is None
b=zpath.read_bytes();receipt={'zip':str(zpath),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'files':len(files),'source_checks':len(checks),'source_mismatches':0}
(zpath.with_suffix('.receipt.json')).write_text(json.dumps(receipt,indent=2),encoding='utf8')
print(json.dumps(receipt,indent=2))
