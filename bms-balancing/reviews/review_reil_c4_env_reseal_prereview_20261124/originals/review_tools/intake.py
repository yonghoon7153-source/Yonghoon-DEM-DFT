import pathlib,json,base64,hashlib
root=pathlib.Path(__file__).parent
rows=[]
for capture,dest,expected_n,expected_h in [('request.json','docs/REIL_C4_ENV_RESEAL_REQUEST_20261124.md',47551,'ae25f895051ec28f06aebf0bf43f07a9e58b77cb24e3a7abb6448572ed0e0791'),('checker.json','scripts/reil_c4_env_reseal_check.py',32342,'8cf10f3c910a46d4ffcf9eb933760178c439fcbec8636189776cb2bea2dbedb0')]:
    obj=json.loads((root/'capture'/capture).read_text(encoding='utf-8'))
    raw=base64.b64decode(''.join(obj['content'].split()),validate=True)
    h=hashlib.sha256(raw).hexdigest()
    assert len(raw)==expected_n and h==expected_h
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==obj['sha']
    out=root/'source'/'bms-balancing'/dest
    out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(raw)
    rows.append(dict(path=str(out),bytes=len(raw),sha256=h,git_blob=obj['sha']))
(root/'INTAKE_IDENTITIES.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rows,indent=2))
