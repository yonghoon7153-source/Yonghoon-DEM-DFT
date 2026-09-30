"""Package the reviewer-created documents and inert evidence, never execute evidence."""
import hashlib
import json
import zipfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLDROOT=Path('C:/Users/Administrator/Documents/Codex/g80_20260928')
def sha(b): return hashlib.sha256(b).hexdigest()
def data(v): return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
before=json.loads((HERE.parent/'gate81_review_20260928/SOURCE_BEFORE.json').read_text(encoding='utf-8'))
scope=json.loads((HERE/'IDENTITY_AUDIT.json').read_text(encoding='utf-8'))['files']
preservation=[]
for entry in scope:
    key=entry['path']
    b=(OLDROOT/key).read_bytes()
    same=len(b)==before[key]['bytes'] and sha(b)==before[key]['sha256']
    assert same, ('prior known source changed',key)
    preservation.append({'path':str(OLDROOT/key),'bytes':len(b),'sha256':sha(b),'matches_prior_inventory':same})
(HERE/'PRIOR_SOURCE_PRESERVATION.json').write_bytes(data({'scope':'58 known files in the pre-existing local G80 checkout versus prior G81 recorded identities; not whole repository/remote history verification','files':preservation}))
name='GATE82_REVIEW_20260930.zip'
target=HERE/name
assert not target.exists(), 'Do not overwrite an existing review ZIP'
exclude={name,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json'}
payload={p.relative_to(HERE).as_posix():p.read_bytes() for p in sorted(HERE.rglob('*')) if p.is_file() and p.name not in exclude}
payload['prior/GATE81_REVIEW_KO.md']=(HERE.parent/'gate81_review_20260928/REVIEW_KO.md').read_bytes()
payload['prior/GATE81_SOURCE_BEFORE.json']=(HERE.parent/'gate81_review_20260928/SOURCE_BEFORE.json').read_bytes()
manifest={'format':'review-payload/v1','members':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payload.items())]}
mb=data(manifest)
(HERE/'PACKAGE_MANIFEST.json').write_bytes(mb)
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n,b in sorted(payload.items()): z.writestr(n,b)
    z.writestr('PACKAGE_MANIFEST.json',mb)
with zipfile.ZipFile(target) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
    assert set(names)==set(payload)|{'PACKAGE_MANIFEST.json'}
    assert z.testzip() is None
    for n,b in payload.items():
        assert z.read(n)==b
        assert not (n.startswith('/') or ':' in n or '\\' in n or '..' in n.split('/'))
    assert z.read('PACKAGE_MANIFEST.json')==mb
b=target.read_bytes()
receipt={'scope':'review generation and local ZIP readback, no recipient verification','recipient':None,
    'file':name,'bytes':len(b),'sha256':sha(b),'payload_count':len(payload),'total_entries':len(payload)+1,
    'manifest_sha256':sha(mb),'exact_set_size_sha_crc_verified':True,
    'review_result':'PARTIAL_ACCEPTANCE_ROUND1_CLOSURE_DEFERRED','p1':2,'p2':1,
    'supplied_code_executed':False,'execution_go':False,'round2_authorized':False}
(HERE/'DELIVERY_RECEIPT.json').write_bytes(data(receipt))
print(json.dumps(receipt,ensure_ascii=False))
