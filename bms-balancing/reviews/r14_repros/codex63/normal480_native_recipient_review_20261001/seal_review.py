"""Seal recipient review only; originals remain unchanged."""
import hashlib,json,zipfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def identity(p):
    with p.open('rb') as f:return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(f,'sha256').hexdigest()}
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
source=[]
for record in read(ROOT/'ARCHIVE_AUDIT.json'):
    p=Path(record['file']); actual=identity(p)
    assert actual=={k:record[k] for k in ['bytes','sha256']}
    source.append({'path':str(p),**actual,'unchanged':True})
(ROOT/'FINAL_SOURCE_CHECK.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for n in ['NUMERIC_AUDIT.json','RECORDS_AUDIT.json','SUPPLEMENTAL_AUDIT.json','ADDITIONAL_AUDIT.json']:
    d=read(ROOT/n)
    assert d['status']=='PASS' and all(c['pass'] for c in d['checks'])
d=read(ROOT/'DECISION.json')
assert d['new_native_execution_approved'] is False and d['overall']=='INCOMPLETE'
n=read(ROOT/'NUMERIC_AUDIT.json')
assert d['data']['stored_times']==n['stored_times'] and d['data']['profile_rows']==n['profile_rows']
assert d['data']['normal240_max_voltage_delta_V']==n['comparisons']['normal240']['voltage_difference_V']['exact_common']
assert d['data']['Li_relative_drift']==n['maximum_Li_relative_drift']
names=['REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_UPDATE_KO.md','DECISION.json',
 'ARCHIVE_AUDIT.json','NUMERIC_AUDIT.json','RECORDS_AUDIT.json','SUPPLEMENTAL_AUDIT.json',
 'ADDITIONAL_AUDIT.json','USER_SUPPLIED_FINAL_RETURN.json','REVIEWER_PROCESS_NOTE.md','FINAL_SOURCE_CHECK.json',
 'audit_archives.py','audit_numeric.py','audit_records.py','audit_supplemental.py','audit_additional.py','seal_review.py']
for name in names:
    if name.endswith('.md'):
        text=(ROOT/name).read_text(encoding='utf-8')
        assert text.startswith('# ') and '\ufffd' not in text
manifest={'scope':'Independent recipient review, no original raw evidence repackaged.',
 'files':[{'file':name,**identity(ROOT/name)} for name in names]}
(ROOT/'REVIEW_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=ROOT/'COMSOL63_NORMAL480_NATIVE_RECIPIENT_REVIEW_20261001.zip'
assert not target.exists()
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in names+['REVIEW_MANIFEST.json']:z.write(ROOT/name,name)
with zipfile.ZipFile(target) as z:
    assert len(z.namelist())==len(set(z.namelist()))==len(names)+1
    assert set(z.namelist())==set(names)|{'REVIEW_MANIFEST.json'}
    assert z.testzip() is None
    for item in manifest['files']:
        b=z.read(item['file'])
        assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256']
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Independent recipient-review generation, not sender execution receipt',
 'archive':{'path':str(target),**identity(target)},'payload_count':len(names),
 'manifest_sha256':identity(ROOT/'REVIEW_MANIFEST.json')['sha256'],
 'zip_verified':True,'source_ZIPs_unchanged':True,'new_native_execution_approved':False}
(ROOT/'REVIEW_DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
