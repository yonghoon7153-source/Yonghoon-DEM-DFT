"""Package read-only review evidence; never modify source/base or existing ZIP."""
from pathlib import Path
import ast, base64, datetime, hashlib, json, os, zipfile

R=Path(__file__).resolve().parent
def lp(p):
    return Path('\\\\?\\'+str(p.resolve())) if os.name=='nt' else p
def read(p): return lp(p).read_bytes()
receipt_original=R.parent/'lhs214_fix_reverify_20261015/probes/receipt_identity.py'
raw=read(receipt_original)
assert hashlib.sha256(raw).hexdigest()=='c73e685d4090a867333d133260def1c1f8d8557900558a84b9deda8acef6eda1'
(R/'probes/receipt_identity_original.py.b64').write_text(base64.b64encode(raw).decode('ascii'),encoding='ascii')
# Intake history is included for offline inspection of the old-to-base comparison.
oldtree=R.parent/'lhs214_fix_reverify_20261015/evidence/tree_9e3ef54ca.json'
(R/'evidence/tree_9e3ef54ca.json').write_bytes(read(oldtree))
integrity={}
for label in ('source','base'):
    m=json.loads(read(R/f'{label}_manifest.json'));bad=[]
    for row in m['files']:
        b=read(R/label/row['path'])
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=row['git_blob']:
            bad.append(row['path'])
    integrity[label]={'files':len(m['files']),'mismatches':bad,'pin':m['pin']}
    assert not bad,(label,bad)
(R/'integrity.json').write_text(json.dumps(integrity,indent=2),encoding='utf8')
syntax=[]
for p in (R/'probes').glob('*.py'):
    ast.parse(read(p).decode('utf-8-sig'),filename=str(p));syntax.append(p.name)
(R/'evidence/package_validation.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'integrity':integrity,'probe_syntax':syntax,'production_changes':False},indent=2),encoding='utf8')
manifest_name='PACKAGE_MANIFEST.json'
items=[]
for folder,dirs,files in os.walk(lp(R)):
    dirs[:]=sorted(d for d in dirs if d not in ('__pycache__','.git'))
    for name in sorted(files):
        p=Path(folder)/name
        rel=p.relative_to(lp(R)).as_posix()
        if rel==manifest_name or rel.endswith(('.pyc','.pyo')):continue
        b=p.read_bytes();items.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'schema':'review_package_manifest/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'code_pin':integrity['source']['pin'],'base_pin':integrity['base']['pin'],'files':items,'excluded':['__pycache__','.git','*.pyc','*.pyo',manifest_name]}
(R/manifest_name).write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
dest=R.parent/'codex_lhs214r_fix_recheck_20261017.zip'
with zipfile.ZipFile(dest,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for row in items:
        z.write(lp(R/row['path']),R.name+'/'+row['path'])
    z.write(lp(R/manifest_name),R.name+'/'+manifest_name)
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    names=z.namelist();assert len(names)==len(set(names))
    assert all(not n.startswith(('/','\\')) and '..' not in Path(n).parts for n in names)
    for row in items:
        b=z.read(R.name+'/'+row['path']);assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
receipt={'schema':'review_delivery/v1','file':dest.name,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(read(dest)).hexdigest(),'zip_entries':len(names),'crc':'PASS','file_sha256_checks':'PASS','source_integrity':integrity,'verdict':'HOLD','scope':'Pinned code recheck; no production run or code changes. Source request/evidence commit unresolved; exact tested code pin in report.'}
dest.with_suffix('.receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
