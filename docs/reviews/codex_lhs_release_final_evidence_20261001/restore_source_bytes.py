"""Restore transport-normalized line endings ONLY when bytes match the pinned Git blob."""
import pathlib,json,hashlib
R=pathlib.Path(__file__).resolve().parent;S=R/'snapshot'
tree={x['path']:x['sha'] for x in json.loads((R/'tree.json').read_text()) if x['type']=='blob'}
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
restored=[]
for p in S.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(S).as_posix()
    if rel not in tree:continue
    b=p.read_bytes()
    if blob(b)==tree[rel]:continue
    lf=b.replace(b'\r\n',b'\n')
    variants=[lf,lf.rstrip(b'\n'),lf.replace(b'\n',b'\r\n'),lf.rstrip(b'\n').replace(b'\n',b'\r\n')]
    hits=[v for v in variants if blob(v)==tree[rel]]
    if not hits:raise RuntimeError('No byte-identical transport restoration: '+rel)
    p.write_bytes(hits[0]);restored.append(rel)
(R/'evidence/source_byte_restoration.json').write_text(json.dumps(restored,indent=2),encoding='utf-8')
print('Restored exact Git bytes:',len(restored))
