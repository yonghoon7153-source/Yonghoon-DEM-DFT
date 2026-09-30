"""Package only recipient-authored review outputs. Never execute received code."""
import hashlib, json, zipfile
from datetime import datetime, timezone
from pathlib import Path

root=Path(__file__).resolve().parent
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def ident(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,obj):
    raw=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with p.open('xb') as f:f.write(raw)
    assert p.read_bytes()==raw
records=json.loads((root/'RECORDS_AUDIT.json').read_bytes())
numeric=json.loads((root/'NUMERIC_AUDIT.json').read_bytes())
decision=json.loads((root/'DECISION.json').read_bytes())
assert records['status']==numeric['status']=='PASS'
assert all(c['pass'] for c in records['checks']+numeric['checks'])
assert sum(x['matched_prior_or_current_copy'] for x in records['historical_validation_references'])==decision['historical_validation_refs_directly_matched']==11
assert decision['new_native_approved'] is False and decision['original_overall']=='INCOMPLETE'
source_checks=[]
for a in json.loads((root/'ARCHIVE_AUDIT.json').read_bytes()):
    p=Path('C:/Users/Administrator/Downloads')/a['file']
    current=ident(p)
    assert all(current[k]==a[k] for k in ['bytes','sha256'])
    source_checks.append({'path':str(p),**current,'unchanged':True})
write(root/'SOURCE_PRESERVATION.json',source_checks)
# Recheck every extracted payload against original manifest by using zip member bytes as the baseline.
# Hash-only, no code evaluation or imports from those directories.
received_checks=[]
for folder,archive in [('received',source_checks[0]['path']),('supplement',source_checks[1]['path'])]:
    count=0
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            p=root/folder/info.filename
            with z.open(info) as f:h=hashlib.file_digest(f,'sha256').hexdigest()
            assert p.stat().st_size==info.file_size and sha(p)==h,info.filename
            count+=1
    received_checks.append({'folder':folder,'all_entries_unchanged':True,'entries':count})
write(root/'FINAL_SOURCE_CHECK.json',received_checks)
files=['REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_UPDATE_KO.md','DECISION.json','README_SEND_KO.md',
       'ARCHIVE_AUDIT.json','NUMERIC_AUDIT.json','RECORDS_AUDIT.json','RECIPIENT_AUDIT_NOTE.md',
       'audit_archives.py','audit_numeric.py','audit_records.py','seal_review.py',
       'SOURCE_PRESERVATION.json','FINAL_SOURCE_CHECK.json']
entries=[{'file':n,**ident(root/n)} for n in files]
write(root/'REVIEW_MANIFEST.json',{'schema':1,'scope':'recipient review only, no native authorization','payloads':entries})
out=root/'COMSOL63_NORMAL30_NATIVE_RECIPIENT_REVIEW_20260930.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in files+['REVIEW_MANIFEST.json']:z.write(root/n,n)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(files+['REVIEW_MANIFEST.json'])
    for x in entries:
        raw=z.read(x['file'])
        assert len(raw)==x['bytes'] and hashlib.sha256(raw).hexdigest()==x['sha256']
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'review_date_local':'2026-09-30',
         'scope':'Separate recipient review package, not native-run or future execution authorization',
         'package':{'file':out.name,**ident(out)},'payload_count':len(files),
         'manifest_sha256':sha(root/'REVIEW_MANIFEST.json'),'size_sha_crc_exact_set_verified':True,
         'original_inputs_unchanged':True,'received_code_executed':False,'new_COMSOL_calls':0,
         'new_native_approved':False}
write(root/'REVIEW_DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,ensure_ascii=False))
