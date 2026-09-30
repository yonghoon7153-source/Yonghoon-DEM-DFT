"""Package only recipient review materials; no supplied module is imported."""
import datetime
import hashlib
import json
import zipfile
from pathlib import Path

root=Path(__file__).resolve().parent
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def jb(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

audit=json.loads((root/'ARCHIVE_AUDIT.json').read_bytes())
preserved=[]
for record in audit:
    p=Path('C:/Users/Administrator/Downloads')/record['file']
    assert p.stat().st_size==record['bytes'] and sha(p)==record['sha256']
    preserved.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p),'unchanged':True})
(root/'INPUT_ZIPS_PRESERVATION.json').write_bytes(jb(preserved))
own=['REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_UPDATE_KO.md','DECISION.json',
     'RECIPIENT_AUDIT_NOTE.md','ARCHIVE_AUDIT.json','STATIC_DATA_AUDIT.json','INPUT_ZIPS_PRESERVATION.json',
     'audit_package.py','audit_static.py','seal_review.py']
source=['CODE_MANIFEST.json','CONTRACT.json','LITERAL_CHANGE_MAP.json','COMMAND_MAP.json',
        'LIMITED_VALIDATION_PLAN.json','VALIDATION_REQUEST_KO.md','BASELINE_IDENTITIES.json',
        'PREPARATION_KO.md','CHANGE_BOUNDARIES.json','NATIVE_APPROVAL_FIELD_SPEC.json',
        'NATIVE60_APPROVAL_DRAFT_KO.md','RESOURCE_BUDGET_KO.md','PRESERVATION_BEFORE.json',
        'PRESERVATION_AFTER.json','STATIC_AUDIT.json','FINAL_STATIC_BINDING.json',
        'PARENT_COMMAND.ps1','src/Normal60Candidate.java','src/candidate_entry.py','src/diagnostic_consumer.py',
        'basis/source30/CODE_MANIFEST.json','basis/source30/CONTRACT.json',
        'basis/source30/PARENT_COMMAND.ps1','basis/source30/src/Normal30Candidate.java',
        'basis/source30/src/candidate_entry.py','basis/source30/src/diagnostic_consumer.py']
files={f:root/f for f in own}
files.update({'reference/'+f:root/'received'/f for f in source})
files.update({'reference/delivery/'+f:root/'supplement'/f for f in ('DELIVERY_RECEIPT.json','PACKAGING_TOOL_RETURN.json')})
manifest={'scope':'Recipient review and inert reference copies, not execution instructions',
          'files':[{'file':n,'bytes':p.stat().st_size,'sha256':sha(p)} for n,p in files.items()]}
raw=jb(manifest)
(root/'REVIEW_MANIFEST.json').write_bytes(raw)
out=root/'COMSOL63_NORMAL60_PREPARATION_RECIPIENT_REVIEW_20260930.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,p in files.items():z.write(p,n)
    z.writestr('REVIEW_MANIFEST.json',raw)
with zipfile.ZipFile(out) as z:
    assert len(z.namelist())==len(set(z.namelist()))==len(files)+1
    assert set(z.namelist())==set(files)|{'REVIEW_MANIFEST.json'}
    assert z.testzip() is None
    assert z.read('REVIEW_MANIFEST.json')==raw
    for r in manifest['files']:
        b=z.read(r['file'])
        assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'scope':'Independent offline recipient review, not native/test authorization',
         'package':{'file':out.name,'bytes':out.stat().st_size,'sha256':sha(out)},
         'payload_count':len(files),'manifest_sha256':hashlib.sha256(raw).hexdigest(),
         'package_set_size_sha_crc_verified':True,'input_zip_preservation':preserved,
         'offline_preparation':'ACCEPTED','functional_tests_run':0,'native60_approved':False}
(root/'RECIPIENT_DELIVERY_RECEIPT.json').write_bytes(jb(receipt))
assert json.loads((root/'RECIPIENT_DELIVERY_RECEIPT.json').read_bytes())==receipt
print(json.dumps(receipt,ensure_ascii=False,indent=2))
