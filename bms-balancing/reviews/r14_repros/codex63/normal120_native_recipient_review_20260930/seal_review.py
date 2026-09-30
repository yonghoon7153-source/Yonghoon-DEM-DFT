"""Seal recipient-created review only. Never execute or change sender code."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def identity(p):
    with p.open('rb') as f:
        return {'bytes':p.stat().st_size,'sha256':hashlib.file_digest(f,'sha256').hexdigest()}

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

source = []
for record in read(ROOT/'ARCHIVE_AUDIT.json'):
    p = Path(record['file'])
    actual = identity(p)
    assert actual == {k:record[k] for k in ['bytes','sha256']}
    source.append({'path':str(p),**actual,'unchanged':True})
(ROOT/'FINAL_SOURCE_CHECK.json').write_text(json.dumps(source,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

for name in ['NUMERIC_AUDIT.json','RECORDS_AUDIT.json','SUPPLEMENTAL_AUDIT.json']:
    d = read(ROOT/name)
    assert d['status'] == 'PASS' and all(c['pass'] for c in d['checks'])
decision = read(ROOT/'DECISION.json')
assert decision['new_native_execution_approved'] is False
names = [
 'REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_UPDATE_KO.md','DECISION.json',
 'ARCHIVE_AUDIT.json','NUMERIC_AUDIT.json','RECORDS_AUDIT.json','SUPPLEMENTAL_AUDIT.json',
 'USER_SUPPLIED_FINAL_RETURN.json','REVIEWER_PROCESS_NOTE.md','FINAL_SOURCE_CHECK.json',
 'audit_archives.py','audit_numeric.py','audit_records.py','audit_supplemental.py','seal_review.py']
for n in names:
    if n.endswith('.md'):
        prose = (ROOT/n).read_text(encoding='utf-8')
        assert prose.startswith('# ') and '\ufffd' not in prose
        assert not any('\u3040' <= c <= '\u30ff' for c in prose)
manifest = {
 'scope':'Recipient review only. Original raw evidence is not repackaged.',
 'files':[{'file':n,**identity(ROOT/n)} for n in names]}
(ROOT/'REVIEW_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
target = ROOT/'COMSOL63_NORMAL120_NATIVE_RECIPIENT_REVIEW_20260930.zip'
assert not target.exists()
with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n in names+['REVIEW_MANIFEST.json']:
        z.write(ROOT/n,n)
with zipfile.ZipFile(target) as z:
    assert len(z.namelist()) == len(set(z.namelist())) == len(names)+1
    assert set(z.namelist()) == set(names)|{'REVIEW_MANIFEST.json'}
    assert z.testzip() is None
    for e in manifest['files']:
        b = z.read(e['file'])
        assert len(b) == e['bytes'] and hashlib.sha256(b).hexdigest() == e['sha256']
receipt = {
 'created_utc':datetime.now(timezone.utc).isoformat(),
 'scope':'Local independent recipient-review generation; not sender execution receipt',
 'archive':{'path':str(target),**identity(target)},
 'payload_count':len(names),
 'manifest_sha256':identity(ROOT/'REVIEW_MANIFEST.json')['sha256'],
 'zip_verified':True,
 'new_native_execution_approved':False}
(ROOT/'REVIEW_DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))
