"""Verify review snapshot against Git blobs; normalize only proven transport newline."""
import hashlib,json,difflib
from pathlib import Path
R=Path(__file__).resolve().parent;S=R/'source';OLD=R.parent/'rglr_reverify_20261005/source'
old=json.loads((R/'unchanged_files.json').read_text(encoding='utf8'));new=json.loads((R/'acquisition.json').read_text(encoding='utf8'))
expect={x['path']:x['sha'] for x in old['files']+new['files']};fetched={x['path'] for x in new['files']};rows=[]
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for path,target in sorted(expect.items()):
 p=S/path;b=p.read_bytes();normalized=False
 if blob(b)!=target:
  for v in (b[:-1],b.replace(b'\r\n',b'\n'),b.replace(b'\r\n',b'\n')[:-1]):
   if blob(v)==target:p.write_bytes(v);b=v;normalized=True;break
 rows.append(dict(path=path,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=blob(b),expected=target,verified=blob(b)==target,transport_normalized=normalized,origin='fetched_at_pin' if path in fetched else 'unchanged_complete_253_file_compare'))
 if path in fetched and (OLD/path).is_file() and path.startswith(('scripts/','webapp/')):
  diff=''.join(difflib.unified_diff((OLD/path).read_text(encoding='utf8').splitlines(True),b.decode('utf8').splitlines(True),fromfile='before/'+path,tofile='after/'+path))
  (R/'diffs'/path.replace('/','__')).write_text(diff,encoding='utf8')
bad=[r for r in rows if not r['verified']]
(R/'source_manifest.json').write_text(json.dumps(dict(commit=new['commit'],base=old['base'],files=rows),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(files=len(rows),verified=len(rows)-len(bad),bad=bad),ensure_ascii=False));raise SystemExit(bool(bad))
