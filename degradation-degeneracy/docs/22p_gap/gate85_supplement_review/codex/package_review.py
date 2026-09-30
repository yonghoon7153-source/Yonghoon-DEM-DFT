"""Package this reviewer supplement only. No submitted script execution."""
import hashlib,json,stat,zipfile
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
H=Path(__file__).resolve().parent
O=H.parent/'gate85_review_20261001'
Z=H/'GATE85_EVIDENCE_SUPPLEMENT_REVIEW_20261001.zip'
M=H/'PACKAGE_MANIFEST.json'
R=H/'DELIVERY_RECEIPT.json'
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
assert not any(p.exists() for p in [Z,M,R])
old=json.loads((H/'SELECTED_PRESERVATION.json').read_text(encoding='utf-8'))['before']
assert old=={p.relative_to(O).as_posix():sha(p.read_bytes()) for p in O.rglob('*') if p.is_file()}
decision=json.loads((H/'DECISION.json').read_text(encoding='utf-8'))
assert not decision['received_code_executed'] and not decision['execution_go']
rows=[]
for p in sorted(H.rglob('*')):
    if p.is_file():
        assert not p.is_symlink() and p.suffix not in ['.zip','.pyc']
        rows.append((p.relative_to(H).as_posix(),p.read_bytes()))
assert len({n.casefold() for n,b in rows})==len(rows)
m={'scope':'Gate85 evidence supplement only; prior P1 open. All source copies are inert review material.',
   'payload_count':len(rows),'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in rows]}
mb=enc(m)
with M.open('xb') as f:f.write(mb)
with zipfile.ZipFile(Z,'x',zipfile.ZIP_DEFLATED) as z:
    for n,b in rows:z.writestr(n,b)
    z.writestr(M.name,mb)
with zipfile.ZipFile(Z) as z:
    ns=z.namelist()
    assert len(ns)==len(set(ns))==len({n.casefold() for n in ns})
    assert set(ns)=={n for n,b in rows}|{M.name} and z.testzip() is None
    assert z.read(M.name)==mb
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and '\\' not in i.filename
        assert stat.S_IFMT(i.external_attr>>16)!=stat.S_IFLNK
    for row in m['files']:
        b=z.read(row['path'])
        assert len(b)==row['bytes'] and sha(b)==row['sha256']
r={'created_utc':datetime.now(timezone.utc).isoformat(),'recipient':None,
   'package':{'file':Z.name,'bytes':Z.stat().st_size,'sha256':sha(Z.read_bytes())},
   'manifest_sha256':sha(mb),'payload_count':len(rows),'entries':len(rows)+1,
   'checks':['exact_set','size_sha256','CRC','case_path_link'],
   'prior_gate85_files_unchanged':len(old),'decision':decision['decision'],
   'G85_N1':'OPEN_P1','round2a_closed':False,'received_code_executed':False,'execution_go':False}
with R.open('xb') as f:f.write(enc(r))
assert json.loads(R.read_text(encoding='utf-8'))==r
print(json.dumps({'status':'REVIEW_SUPPLEMENT_PACKAGE_VERIFIED','package':r['package'],'payload_count':len(rows),'prior_files_unchanged':len(old),'G85_N1':'OPEN_P1','execution_go':False}))
