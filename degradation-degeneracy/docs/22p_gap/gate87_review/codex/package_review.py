"""Package only this review. Never executes contained source material."""
import datetime
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

H=Path(__file__).resolve().parent
Z=H/'GATE87_REVIEW_20261003.zip'
M=H/'PACKAGE_MANIFEST.json'
RC=H/'DELIVERY_RECEIPT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert not Z.exists(), 'Never overwrite an existing delivery ZIP'
pres=json.loads((H/'PRESERVATION.json').read_text(encoding='utf-8'))
old=Path(pres['selected_directory'])
now={p.relative_to(old).as_posix():sha(p.read_bytes()) for p in old.rglob('*') if p.is_file()}
assert now==pres['before'], 'Prior review changed'
files=[p for p in H.rglob('*') if p.is_file() and p not in (Z,M,RC) and '__pycache__' not in p.parts]
entries=[]
for p in sorted(files):
    assert not p.is_symlink()
    rel=p.relative_to(H).as_posix();b=p.read_bytes()
    entries.append({'path':rel,'bytes':len(b),'sha256':sha(b)})
dump(M,{'schema':'recipient-review-package/v1','review':'GATE87','decision':'REQUEST_CHANGES_ROUND2B_NOT_CLOSED','self_excluded':True,'payload_count':len(entries),'files':entries})
with zipfile.ZipFile(Z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files+[M]:z.write(p,p.relative_to(H).as_posix())
with zipfile.ZipFile(Z) as z:
    infos=z.infolist(); names=[x.filename for x in infos]
    assert len(names)==len(set(names))==len({x.casefold() for x in names})
    assert set(names)=={e['path'] for e in entries}|{'PACKAGE_MANIFEST.json'}
    for i in infos:
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename
        assert not stat.S_ISLNK(i.external_attr >> 16)
    assert z.testzip() is None
    for e in entries:
        b=z.read(e['path']);assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert z.read('PACKAGE_MANIFEST.json')==M.read_bytes()
b=Z.read_bytes()
r={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Generation of Gate87 independent static review package, not source execution','recipient':None,'package':{'path':str(Z),'bytes':len(b),'sha256':sha(b)},'manifest_sha256':sha(M.read_bytes()),'payload_count':len(entries),'entry_count':len(entries)+1,'exact_set_size_sha_crc_path_case_link_checks':True,'prior_review_files_unchanged':len(now),'decision':'REQUEST_CHANGES_ROUND2B_NOT_CLOSED','P1':1,'received_program_executions':0,'COMSOL_calls':0,'external_send':False}
dump(RC,r)
assert json.loads(RC.read_text(encoding='utf-8'))==r
print(json.dumps(r,ensure_ascii=False))
