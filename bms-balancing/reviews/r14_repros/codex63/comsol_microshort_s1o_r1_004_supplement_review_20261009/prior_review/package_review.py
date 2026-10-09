"""Package reviewer artifacts only; no received scripts executed."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
SRC=Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_R1_004_VALIDATION_RESULT_20261009.zip')
NAME='COMSOL_MICROSHORT_S1O_R1_004_VALIDATION_REVIEW_20261009.zip'
def sha(b): return hashlib.sha256(b).hexdigest()
assert not (ROOT/NAME).exists() and not (ROOT/'REVIEW_MANIFEST.json').exists()
raw=SRC.read_bytes()
assert len(raw)==796501 and sha(raw)=='cb85fa123395caf9ea323b0c531144bf30754322ba9b0362f1bbac3e5bc8ff2c'
audit=json.loads((ROOT/'RECORD_AUDIT.json').read_text(encoding='utf-8'))
decision=json.loads((ROOT/'DECISION.json').read_text(encoding='utf-8'))
assert len(audit['checks'])==565 and all(x['pass'] for x in audit['checks'])
assert decision['original_cases']==130 and decision['prior_reused']==127 and decision['original_newly_satisfied']==3 and decision['auxiliary_positive_new']==4
assert decision['native_ready'] is False and decision['native_approved'] is False
payload={p.relative_to(ROOT).as_posix():p.read_bytes() for p in ROOT.rglob('*') if p.is_file() and p.name not in (NAME,'REVIEW_MANIFEST.json','REVIEW_DELIVERY_RECEIPT.json') and '__pycache__' not in p.parts}
payload['reference/ORIGINAL_R1_004_RESULT.zip']=raw
assert len(payload)==len({n.casefold() for n in payload})
manifest={'self_excluded':True,'kind':'REVIEW_ARTIFACT_MANIFEST','files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payload.items())]}
mb=json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8')
with (ROOT/'REVIEW_MANIFEST.json').open('xb') as f:f.write(mb)
with zipfile.ZipFile(ROOT/NAME,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in sorted(payload.items()):z.writestr(n,b)
    z.writestr('REVIEW_MANIFEST.json',mb)
with zipfile.ZipFile(ROOT/NAME) as z:
    assert set(z.namelist())==set(payload)|{'REVIEW_MANIFEST.json'} and z.testzip() is None
    for n,b in payload.items():assert z.read(n)==b
zraw=(ROOT/NAME).read_bytes()
receipt={'status':'REVIEW_DELIVERY_VERIFIED','decision':decision['status'],'zip':{'path':str(ROOT/NAME),'bytes':len(zraw),'sha256':sha(zraw)},'payload_count':len(payload),'entries':len(payload)+1,'manifest_sha256':sha(mb),'source_archive_after_review_unchanged':SRC.read_bytes()==raw,'candidate_code_or_test_execution':0,'native_approved':False,'recipient':None}
with (ROOT/'REVIEW_DELIVERY_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
print(json.dumps(receipt,ensure_ascii=False))
