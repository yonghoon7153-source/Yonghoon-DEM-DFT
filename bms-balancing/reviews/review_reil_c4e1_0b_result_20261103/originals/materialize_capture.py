import base64, hashlib, json, pathlib, shutil
root=pathlib.Path(__file__).resolve().parent
c=json.loads((root/'capture_base64.json').read_text(encoding='utf-8'))
ids=[]
for f in c['files']:
    b=base64.b64decode(''.join(f['content'].split()),validate=True)
    p=pathlib.Path(f['path'])
    assert not p.is_absolute() and '..' not in p.parts
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert blob==f['sha'], (f['path'],blob,f['sha'])
    dst=root/'source'/p; dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    ids.append({'path':f['path'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'git_blob_sha1':blob,'url':f.get('display_url')})
local=pathlib.Path('C:/Users/Administrator/Downloads/REIL_C4E1_0B_RESULT_REVIEW_SEND_20261103.md')
(root/'input').mkdir(exist_ok=True)
shutil.copyfile(local,root/'input'/local.name)
assert local.read_bytes()==(root/'source/bms-balancing/docs'/local.name).read_bytes()
(root/'SOURCE_IDENTITIES.json').write_text(json.dumps({'repository':c['repository'],'ref':c['ref'],'files':ids,'attachment_exact_match':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'captured':len(ids),'attachment_exact_match':True,'evidence_count':sum('/evidence/' in x['path'] for x in ids),'evidence_bytes':sum(x['bytes'] for x in ids if '/evidence/' in x['path'])}))
