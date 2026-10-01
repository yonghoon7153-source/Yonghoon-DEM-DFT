"""Reviewer-owned archive builder; never imports submitted modules."""
import hashlib
import json
import stat
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

H=Path(__file__).resolve().parent
OLD=H.parent/'gate85_review_20261001'
Z=H/'GATE86_REVIEW_20261001.zip'
M=H/'PACKAGE_MANIFEST.json'
R=H/'DELIVERY_RECEIPT.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def js(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def read(p): return json.loads(p.read_text(encoding='utf-8'))
if any(p.exists() for p in [Z,M,R]): raise SystemExit('Output collision: no overwrite.')
d=read(H/'DECISION.json')
a=read(H/'STATIC_AUDIT.json')
s=read(H/'SUPPLEMENT_AUDIT.json')
assert a['pass'] and s['pass']
assert d['reviewer_data_checks']==len(a['checks'])+len(s['checks'])==273
assert not any(d['authorized_actions'].values())
pres=read(H/'SELECTED_PRESERVATION.json')['before']
now={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
assert pres==now
payload=[]
for p in sorted(H.rglob('*')):
    if not p.is_file(): continue
    assert not p.is_symlink()
    n=p.relative_to(H).as_posix()
    assert '__pycache__' not in n and not n.endswith(('.zip','.pyc'))
    payload.append((n,p.read_bytes()))
assert len(payload)==len({n.casefold() for n,b in payload})
manifest={'scope':'Gate86 independent static/source-log review. No execution or implementation authorization.','payload_count':len(payload),'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in payload]}
mb=js(manifest)
with M.open('xb') as f: f.write(mb)
with zipfile.ZipFile(Z,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,b in payload: z.writestr(n,b)
    z.writestr(M.name,mb)
with zipfile.ZipFile(Z,'r') as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    assert set(names)=={n for n,b in payload}|{M.name}
    assert z.testzip() is None and z.read(M.name)==mb
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert stat.S_IFMT(i.external_attr>>16)!=stat.S_IFLNK
    for row in manifest['files']:
        b=z.read(row['path'])
        assert len(b)==row['bytes'] and sha(b)==row['sha256']
receipt={'created_at_utc':datetime.now(timezone.utc).isoformat(),'recipient':None,'type':'REVIEWER_GENERATION_RECEIPT','verdict':d['verdict'],
         'package':{'file':Z.name,'bytes':Z.stat().st_size,'sha256':sha(Z.read_bytes())},'manifest_sha256':sha(mb),'payload_count':len(payload),'total_entries':len(payload)+1,
         'checks':['exact_set','every_payload_size_SHA256','CRC','duplicate_case_path_link'],'reviewer_data_checks':273,'prior_gate85_local_files_unchanged':len(pres),
         'received_code_executed':False,'project_tests_run':0,'mutation_replays':0,'COMSOL_calls':0,'round2b_approved':False,'execution_go':False,
         'scope':'Reviewer-generation receipt outside ZIP; source-log observations are not direct remote OS observations.'}
with R.open('xb') as f: f.write(js(receipt))
assert read(R)==receipt
print(json.dumps({'status':'REVIEW_PACKAGE_VERIFIED','package':receipt['package'],'payload_count':len(payload),'entries':len(payload)+1,'preserved_prior_files':len(pres),'verdict':d['verdict'],'execution_go':False}))
