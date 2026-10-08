"""Package review documents/evidence only. No received program imports."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json,zipfile
ROOT=Path(__file__).resolve().parent
SRC=Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_R1_003_VALIDATION_STOP_20261008.zip')
PIN='11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b'
OUT=ROOT/'COMSOL_MICROSHORT_S1O_R1_003_STOP_REVIEW_20261008.zip'
MANIFEST=ROOT/'REVIEW_MANIFEST.json'
RECEIPT=ROOT/'REVIEW_DELIVERY_RECEIPT.json'
def sha(b):return sha256(b).hexdigest()
for p in (OUT,MANIFEST,RECEIPT):
    if p.exists():raise SystemExit('STOP_EXISTING_OUTPUT: '+str(p))
assert sha(SRC.read_bytes())==PIN
with zipfile.ZipFile(SRC) as original:
    assert set(original.namelist())=={p.relative_to(ROOT/'received').as_posix() for p in (ROOT/'received').rglob('*') if p.is_file()}
    for name in original.namelist():assert original.read(name)==(ROOT/'received'/name).read_bytes()
docs=['README_KO.md','REVIEW_KO.md','CLAUDE_REPLY_KO.md','NEXT_LIMITED_APPROVAL_DRAFT_KO.md',
      'DECISION.json','INPUT_CHECK.json','RECORD_AUDIT.json','USER_SUPPLIED_DELIVERY_RECORDS.json',
      'inspect_archive.py','audit_records.py','package_review.py']
files={name:(ROOT/name).read_bytes() for name in docs}
for folder in ('notes','received'):
    for p in (ROOT/folder).rglob('*'):
        if p.is_file():files[p.relative_to(ROOT).as_posix()]=p.read_bytes()
assert len(files)==len({n.casefold() for n in files})
decision=json.loads(files['DECISION.json'])
assert decision['new_validation_approved'] is False and decision['native_approved'] is False
assert decision['observed_submitted_counts']=={'PASS':127,'HARNESS_FAILURE_BEFORE_TARGET':1,'NOT_RUN_AFTER_FIRST_FAILURE':2}
manifest={'kind':'REVIEW_MANIFEST','date_kst':'2026-10-08','self_excluded':True,'payload_count':len(files),
          'input_archive_sha256':PIN,'files':[{'path':name,'bytes':len(b),'sha256':sha(b)} for name,b in sorted(files.items())]}
mb=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
with MANIFEST.open('xb') as f:f.write(mb)
with zipfile.ZipFile(OUT,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name,b in sorted(files.items()):z.writestr(name,b)
    z.writestr(MANIFEST.name,mb)
with zipfile.ZipFile(OUT) as z:
    assert len(z.namelist())==len(files)+1 and set(z.namelist())==set(files)|{MANIFEST.name}
    for name,b in files.items():assert z.read(name)==b,name
    assert z.read(MANIFEST.name)==mb and z.testzip() is None
assert sha(SRC.read_bytes())==PIN
raw=OUT.read_bytes()
receipt={'kind':'REVIEW_PACKAGE_RECEIPT','created_utc':datetime.now(timezone.utc).isoformat(),'recipient':None,
         'package':{'file':OUT.name,'bytes':len(raw),'sha256':sha(raw)},'payload_count':len(files),'entries':len(files)+1,
         'manifest_sha256':sha(mb),'package_set_bytes_sha_crc_verified':True,'received_evidence_unchanged':True,
         'decision':decision['status'],'new_validation_approved':False,'native_approved':False,
         'reviewer_received_program_calls':0,'reviewer_COMSOL_calls':0,
         'scope':'Independent review package verification, not original engine or delivery replay'}
with RECEIPT.open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,ensure_ascii=False,indent=2);f.write('\n')
assert json.loads(RECEIPT.read_text(encoding='utf-8'))==receipt
print(json.dumps(receipt,ensure_ascii=False))
