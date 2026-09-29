"""Package this recipient review only; no target code execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
inputs=[
 ('C:/Users/Administrator/Downloads/COMSOL63_NORMAL30_LIMITED_VALIDATION_COMPLETE_20260930.zip','0854dbd1db8433c4d22def4984af7b535c36c3e7ab6c65b6b9d013d1ab0f29ea'),
 ('C:/Users/Administrator/Downloads/COMSOL63_NORMAL30_DELIVERY_SUPPLEMENT_20260930.zip','5f5b4dfe47eec3a4a6d94dac72f08f03716b0de2ab15ea8aff95409d2414ba22')]
source=[]
for path,expected in inputs:
 b=Path(path).read_bytes();assert sha(b)==expected
 source.append(dict(path=path,bytes=len(b),sha256=sha(b),unchanged_from_recipient_initial_read=True))
(R/'SOURCE_PRESERVATION.json').write_text(json.dumps({'scope':'Two local received ZIPs only; no remote current inventory claim','files':source},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
names=['README_SEND_KO.md','REVIEW_KO.md','NEXT_CODEX_REPLY_KO.md','CLAUDE_UPDATE_KO.md','DECISION.json','REVIEWER_NOTES.json',
 'PACKAGE_AUDIT.json','EVIDENCE_AUDIT.json','EVIDENCE_AUDIT_FIRST_PASS.json','SUPPLEMENT_AUDIT.json','INDEPENDENT_SOURCE_DIFF.patch',
 'SOURCE_PRESERVATION.json','audit_package.py','audit_evidence.py','audit_supplement.py','package_review.py']
for n in names:
 if n.endswith('.json'):json.loads((R/n).read_bytes())
payload=[dict(file=n,bytes=(R/n).stat().st_size,sha256=sha((R/n).read_bytes())) for n in names]
manifest=(json.dumps(dict(scope='Independent recipient review; no native permission',files=payload),ensure_ascii=False,indent=2)+'\n').encode()
(R/'REVIEW_MANIFEST.json').write_bytes(manifest)
out=R/'COMSOL63_NORMAL30_VALIDATION_RECIPIENT_REVIEW_20260930.zip'
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED) as z:
 for n in names:z.write(R/n,n)
 z.write(R/'REVIEW_MANIFEST.json','REVIEW_MANIFEST.json')
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None and set(z.namelist())==set(names)|{'REVIEW_MANIFEST.json'}
 assert len(z.namelist())==len(set(n.casefold() for n in z.namelist()))
 for r in payload:
  b=z.read(r['file']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
raw=out.read_bytes()
receipt=dict(created_utc=datetime.now(timezone.utc).isoformat(),scope='Recipient review package generation',file=out.name,bytes=len(raw),sha256=sha(raw),payload_count=len(names),entries=len(names)+1,manifest_sha256=sha(manifest),size_sha_crc_exact_set_verified=True,target_executions=0,native30_approved=False)
(R/'REVIEW_DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False))
