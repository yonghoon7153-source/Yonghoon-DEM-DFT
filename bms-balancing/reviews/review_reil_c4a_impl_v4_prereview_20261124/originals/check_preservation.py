import base64,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent; prior=root.parent/'reil_c4a_v3_review_20261124'
rows=[]
for r in json.loads((root/'capture/PRESERVED_REQUESTS_BASE64.json').read_text('utf-8')):
 assert r['status']=='fulfilled'
 v=r['value'];s=v['result']['structuredContent'];b=base64.b64decode(''.join(s['content'].split()),validate=True)
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['sha']
 p=root/'input'/Path(v['path']).name;p.write_bytes(b)
 old=prior/'source'/v['path'];assert old.read_bytes()==b
 rows.append({'repository_path':v['path'],'local_path':p.relative_to(root).as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha':s['sha'],'matches_prior':True})
cap=json.loads((root/'capture/SUBMISSION_COMMIT.json').read_text('utf-8'))['structuredContent']['commit']
files=cap.get('files',[])
out={'kind':'V4_PRESERVATION_CHECK','preserved_requests':rows,'submission_commit':cap['sha'],'submission_changed_files':[{k:f.get(k) for k in ['filename','status','additions','deletions']} for f in files],'scope':'Fixed request and ledger byte checks; no new whole-source-tree audit or runtime execution.'}
(root/'PRESERVATION_CHECK.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,ensure_ascii=False))
