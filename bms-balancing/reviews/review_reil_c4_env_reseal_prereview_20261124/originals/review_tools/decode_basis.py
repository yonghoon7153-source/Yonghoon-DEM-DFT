import pathlib,json,base64,hashlib
root=pathlib.Path(__file__).parent
rows=[]
for cap in sorted((root/'capture').glob('basis_batch_*.json')):
    for obj in json.loads(cap.read_text(encoding='utf-8')):
        raw=base64.b64decode(''.join(obj['content'].split()),validate=True)
        assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==obj['sha'],obj['path']
        out=root/'source'/obj['path'];out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
        rows.append(dict(path=obj['path'],bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),git_blob=obj['sha']))
(root/'BASIS_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print('Read-only basis decoded; Git blob verified:',len(rows))
