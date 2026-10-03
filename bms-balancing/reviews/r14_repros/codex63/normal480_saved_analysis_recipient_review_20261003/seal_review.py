from pathlib import Path
import hashlib,json,zipfile,datetime
ROOT=Path(__file__).resolve().parent
def digest(b):return hashlib.sha256(b).hexdigest()
names=['REVIEW_KO.md','CLAUDE_REPLY_KO.md','NEXT_CODEX_REPLY_KO.md','DECISION.json','REVIEWER_NOTE.md','ARCHIVE_AUDIT.json','NUMERIC_AUDIT.json','CONTEXT_AUDIT.json','audit_archive.py','audit_data.py','audit_context.py','seal_review.py']
for n in ['ARCHIVE_AUDIT.json','NUMERIC_AUDIT.json','CONTEXT_AUDIT.json']:
    assert json.loads((ROOT/n).read_bytes())['status']=='PASS'
for n in ['REVIEW_KO.md','CLAUDE_REPLY_KO.md','NEXT_CODEX_REPLY_KO.md']:
    txt=(ROOT/n).read_text(encoding='utf-8')
    assert 'INCOMPLETE' in txt and '960' in txt
manifest={'scope':'Recipient saved-data analysis review. Original received PDF/ZIP and native evidence are referenced, not repackaged. No simulation or new approval.','files':[{'file':n,'bytes':(ROOT/n).stat().st_size,'sha256':digest((ROOT/n).read_bytes())} for n in names]}
(ROOT/'REVIEW_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=ROOT/'NORMAL480_SAVED_ANALYSIS_RECIPIENT_REVIEW_20261003.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n in names+['REVIEW_MANIFEST.json']:z.write(ROOT/n,n)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())==set(names)|{'REVIEW_MANIFEST.json'}
    assert len(z.infolist())==len(names)+1 and z.testzip() is None
    for e in manifest['files']:
        b=z.read(e['file']);assert len(b)==e['bytes'] and digest(b)==e['sha256']
receipt={'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'REVIEW_PACKAGE_VERIFIED','package':{'file':archive.name,'bytes':archive.stat().st_size,'sha256':digest(archive.read_bytes())},'payload_count':len(names),'manifest_sha256':digest((ROOT/'REVIEW_MANIFEST.json').read_bytes()),'recipient':None,'scope':'Generation of independent recipient review package; not a new COMSOL execution receipt','new_execution_approved':False}
(ROOT/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt))
