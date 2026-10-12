"""Package reviewer records and unchanged evidence; execute no received code."""
import hashlib
import json
import pathlib
import stat
import zipfile

R=pathlib.Path(__file__).resolve().parent
name='COMSOL_MICROSHORT_S1_OPEN_CONNECTION_R1_REVIEW_20261011.zip'
archive=R/name
manifest_path=R/'REVIEW_PACKAGE_MANIFEST.json'
receipt_path=R/'REVIEW_DELIVERY_RECEIPT.json'
for p in (archive,manifest_path,receipt_path):
    if p.exists(): raise SystemExit('STOP_OUTPUT_EXISTS: '+str(p))
def sha(b): return hashlib.sha256(b).hexdigest()
paths=sorted(p for p in R.rglob('*') if p.is_file())
rows=[]
for p in paths:
    if p.is_symlink(): raise SystemExit('STOP_SYMLINK: '+str(p))
    b=p.read_bytes();rows.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)})
assert len({x['path'].casefold() for x in rows})==len(rows)
manifest={'kind':'REVIEW_PACKAGE_MANIFEST','self_excluded':True,'payload_count':len(rows),'files':rows}
mb=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
manifest_path.write_bytes(mb)
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for x in rows:z.write(R/x['path'],x['path'])
    z.write(manifest_path,manifest_path.name)
with zipfile.ZipFile(archive) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len(rows)+1
    assert set(names)=={x['path'] for x in rows}|{manifest_path.name}
    assert z.testzip() is None
    assert z.read(manifest_path.name)==mb
    for x in rows:
        b=z.read(x['path']);assert len(b)==x['bytes'] and sha(b)==x['sha256']
incoming=pathlib.Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_CONNECTION_R1_20261010.zip')
assert incoming.stat().st_size==4011062 and sha(incoming.read_bytes())=='c9cf85b30f48fce0a8e747a8428b74b22a2d4c101498e2c0306720ed571fee0b'
b=archive.read_bytes()
receipt={'kind':'REVIEWER_PACKAGE_RECEIPT','recipient':None,'status':'STATIC_CORRECTIONS_ACCEPTED_WITH_PLAN_METADATA_CONDITIONS','zip':{'path':str(archive),'bytes':len(b),'sha256':sha(b)},'manifest':{'bytes':len(mb),'sha256':sha(mb)},'payload_count':len(rows),'entries':len(rows)+1,'readback':'EXACT_SET_SIZE_SHA_CRC_MATCHED','incoming_archive_unchanged':True,'candidate_tests_run':0,'COMSOL_calls':0,'native_approved':False,'outbound_delivery':'NOT_SENT'}
receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert json.loads(receipt_path.read_text(encoding='utf-8'))==receipt
print(json.dumps(receipt,ensure_ascii=False))
