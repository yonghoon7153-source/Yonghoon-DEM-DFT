import base64,hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
prior=root.parent/'reil_c4a_impl_v2_prereview_20261108'/'source'
rows=[]
captures=['REFERENCED_FILES_BASE64.json','EXTRA_FILES_BASE64.json']
for r in sum([json.loads((root/'capture'/f).read_text('utf-8')) for f in captures],[]):
    assert r['status']=='fulfilled'
    v=r['value']; s=v['result']['structuredContent']; b=base64.b64decode(''.join(s['content'].split()),validate=True)
    sha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert sha==s['sha'],v['path']
    rel=v['path']; p=root/'source'/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
    old=prior/rel
    rows.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha':sha,'prior_exists':old.is_file(),'matches_prior':old.read_bytes()==b if old.is_file() else None})
(root/'SOURCE_COMPARISON.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False))
