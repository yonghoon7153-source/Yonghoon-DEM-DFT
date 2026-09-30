"""Package reviewer-owned evidence. Does not import/execute received programs."""
import hashlib
import json
import stat
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'gate83_review_20260930'
Z=HERE/'GATE84_REVIEW_20260930.zip'
M=HERE/'PACKAGE_MANIFEST.json'
R=HERE/'DELIVERY_RECEIPT.json'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def js(v):
    return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

if any(p.exists() for p in [Z,M,R]):
    raise SystemExit('Output collision; no overwrite.')
decision=json.loads((HERE/'DECISION.json').read_text(encoding='utf-8'))
audit=json.loads((HERE/'STATIC_AUDIT.json').read_text(encoding='utf-8'))
assert audit['pass'] and not decision['implementation_authorized'] and not decision['execution_go']
before=json.loads((HERE/'SELECTED_PRESERVATION.json').read_text(encoding='utf-8'))['before']
after={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
assert before==after
payload=[]
for p in sorted(HERE.rglob('*')):
    if not p.is_file():
        continue
    assert not p.is_symlink()
    name=p.relative_to(HERE).as_posix()
    assert not name.endswith(('.pyc','.zip')) and '__pycache__' not in name
    b=p.read_bytes()
    payload.append((name,b))
assert len({n.casefold() for n,b in payload})==len(payload)
manifest={'scope':'Read-only Gate84 scope/design review; inert references and reviewer-owned data checks. No implementation or execution authorization.',
          'payload_count':len(payload),'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in payload]}
mb=js(manifest)
with M.open('xb') as f:
    f.write(mb)
with zipfile.ZipFile(Z,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n,b in payload:
        z.writestr(n,b)
    z.writestr(M.name,mb)
with zipfile.ZipFile(Z,'r') as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    assert set(names)=={n for n,b in payload}|{M.name}
    assert z.testzip() is None
    assert z.read(M.name)==mb
    for item in z.infolist():
        p=PurePosixPath(item.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in item.filename and ':' not in item.filename
        assert stat.S_IFMT(item.external_attr>>16)!=stat.S_IFLNK
    for row in manifest['files']:
        b=z.read(row['path'])
        assert len(b)==row['bytes'] and sha(b)==row['sha256']
receipt={'created_at_utc':datetime.now(timezone.utc).isoformat(),
         'type':'REVIEWER_GENERATION_RECEIPT','recipient':None,
         'decision':decision['decision'],'package':{'file':Z.name,'bytes':Z.stat().st_size,'sha256':sha(Z.read_bytes())},
         'manifest_sha256':sha(mb),'payload_count':len(payload),'total_entries':len(payload)+1,
         'checks':['exact_set','member_size_sha256','CRC','duplicate_case_path_link'],
         'static_data_checks':len(audit['checks']),'prior_gate83_files_unchanged':len(before),
         'received_code_executed':False,'implementation_authorized':False,'execution_go':False,
         'scope':'Receipt outside ZIP; user/remote runtime state not newly inspected.'}
with R.open('xb') as f:
    f.write(js(receipt))
assert json.loads(R.read_text(encoding='utf-8'))==receipt
print(json.dumps({'status':'REVIEW_PACKAGE_VERIFIED','package':receipt['package'],'payload_count':len(payload),'entries':len(payload)+1,'recipient':None,'implementation_authorized':False,'execution_go':False}))
