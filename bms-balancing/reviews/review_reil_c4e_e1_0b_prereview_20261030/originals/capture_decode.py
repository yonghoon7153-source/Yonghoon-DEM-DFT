import base64, hashlib, json
from pathlib import Path, PurePosixPath
r=Path(__file__).resolve().parent
rows=json.loads((r/'capture_base64.json').read_text(encoding='utf-8'))
out=[]
for row in rows:
    p=PurePosixPath(row['path'])
    assert not p.is_absolute() and '..' not in p.parts and '\\\\' not in str(p) and ':' not in str(p)
    b=base64.b64decode(row['base64'],validate=True)
    gitsha=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert gitsha==row['blob_sha'], (row['path'],gitsha,row['blob_sha'])
    dest=r/'source'/str(p)
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f: f.write(b)
    out.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'blob_sha':gitsha,'url':row['url']})
(r/'SOURCE_IDENTITIES.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'captured':len(out),'git_blob_SHA1_verified':True,'target_execution':0}))
