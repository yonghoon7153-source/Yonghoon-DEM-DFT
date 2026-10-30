from pathlib import Path, PurePosixPath
import zipfile, tarfile, hashlib, re, json
root=Path('C:/Users/Administrator/Documents/Codex/d07scope30')
src=Path('C:/Users/Administrator/Downloads/codex-kg50-d07-scoped-go-09ae533d0.zip')
root.mkdir(parents=True,exist_ok=True)
records=[]
def valid(n):
 p=PurePosixPath(n)
 assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n,n
 return p
with zipfile.ZipFile(src) as z:
 seen=set()
 for i in z.infolist():
  p=valid(i.filename);assert i.filename.casefold() not in seen;seen.add(i.filename.casefold())
  assert ((i.external_attr>>16)&0o170000)!=0o120000
  if i.is_dir():continue
  b=z.read(i);t=root/p;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b)
  records.append({'path':i.filename,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()})
man=(root/'MANIFEST.sha256').read_text(encoding='utf-8-sig')
checks=[]
for line in man.splitlines():
 m=re.match(r'^([a-f0-9]{64})\s+\*?(.+)$',line)
 if m:
  h,n=m.groups();p=valid(n);actual=hashlib.sha256((root/p).read_bytes()).hexdigest();assert h==actual,(n,h,actual);checks.append(n)
tarrows=[];duplicates=[]
for p in root.rglob('*.tgz'):
 dest=root/'trial';dest.mkdir(exist_ok=True)
 with tarfile.open(p) as t:
  seen={}
  for i in t.getmembers():
   n=valid(i.name); assert not(i.issym() or i.islnk());assert i.isdir() or i.isfile()
   if i.isdir():continue
   b=t.extractfile(i).read();h=hashlib.sha256(b).hexdigest();key=str(n).casefold()
   if key in seen:
    assert seen[key]==h,(n,'different bytes at duplicate path')
    duplicates.append({'path':str(n),'sha256':h,'identical':True});continue
   seen[key]=h
   v=dest/n;v.parent.mkdir(parents=True,exist_ok=True);v.write_bytes(b)
   tarrows.append({'path':str(n),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
out={'zip_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'zip':records,'manifest_verified_count':len(checks),'trial_files':tarrows,'identical_tar_duplicates':duplicates}
(root/'intake.json').write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'zip_files':len(records),'manifest_checks':len(checks),'tar_files':len(tarrows),'files':[r['path'] for r in records],'trial':[r['path'] for r in tarrows]},ensure_ascii=False,indent=2))
