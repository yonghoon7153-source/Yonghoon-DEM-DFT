"""Package this recipient review only; no original artifact modifications."""
import hashlib,json,zipfile
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def identity(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
source=[]
for record in json.loads((ROOT/'ARCHIVE_AUDIT.json').read_text(encoding='utf-8')):
    p=Path(record['file']);actual=identity(p)
    assert actual=={k:record[k] for k in ['bytes','sha256']}
    source.append({'path':str(p),**actual,'unchanged':True})
(ROOT/'FINAL_SOURCE_CHECK.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for name in ['NUMERIC_AUDIT.json','RECORDS_AUDIT.json','SUPPLEMENTAL_AUDIT.json']:
    d=json.loads((ROOT/name).read_text(encoding='utf-8'));assert d['status']=='PASS' and all(c['pass'] for c in d['checks'])
names=['REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_UPDATE_KO.md','DECISION.json','ARCHIVE_AUDIT.json','NUMERIC_AUDIT.json','RECORDS_AUDIT.json','SUPPLEMENTAL_AUDIT.json','REVIEWER_PROCESS_NOTE.md','FINAL_SOURCE_CHECK.json','audit_archives.py','audit_numeric.py','audit_records.py','audit_supplemental.py','seal_review.py']
for n in names:
    if n.endswith('.md'):
        text=(ROOT/n).read_text(encoding='utf-8');assert text.startswith('# ') and '\ufffd' not in text and '初期' not in text
manifest={'scope':'Recipient review only; original raw evidence retained at source ZIP identities','files':[{'file':n,**identity(ROOT/n)} for n in names]}
(ROOT/'REVIEW_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target=ROOT/'COMSOL63_NORMAL60_NATIVE_RECIPIENT_REVIEW_20260930.zip'
assert not target.exists()
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in names+['REVIEW_MANIFEST.json']:z.write(ROOT/n,n)
with zipfile.ZipFile(target) as z:
    assert set(z.namelist())==set(names)|{'REVIEW_MANIFEST.json'} and z.testzip() is None
    for e in manifest['files']:
        raw=z.read(e['file']);assert len(raw)==e['bytes'] and hashlib.sha256(raw).hexdigest()==e['sha256']
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Local recipient review generation, not sender native execution receipt','archive':{'path':str(target),**identity(target)},'payload_count':len(names),'manifest_sha256':sha(ROOT/'REVIEW_MANIFEST.json'),'zip_verified':True,'new_native_execution_approved':False}
(ROOT/'REVIEW_DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
