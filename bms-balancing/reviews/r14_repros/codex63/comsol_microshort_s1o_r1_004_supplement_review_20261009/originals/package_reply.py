"""Package new review documents with unmodified evidence; no candidate execution."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
NAME='COMSOL_MICROSHORT_S1O_R1_004_SUPPLEMENT_REVIEW_20261009.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
audit=json.loads((R/'SUPPLEMENT_CHECK.json').read_text(encoding='utf-8'))
decision=json.loads((R/'DECISION.json').read_text(encoding='utf-8'))
assert decision['status']=='LIMITED_VALIDATION_CLOSED_WITH_DOCUMENTED_SCOPE'
assert decision['native_ready'] is False and decision['native_approved'] is False
assert decision['original_reused']+decision['original_newly_satisfied']==130 and decision['auxiliary_positive_new']==4
assert decision['overall_snapshot_s']==614.4801189 and decision['delivery_snapshot_s']==161.3691145
assert not (R/NAME).exists() and not (R/'REVIEW_MANIFEST.json').exists()
payload={p.relative_to(R).as_posix():p.read_bytes() for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
for item in audit['inputs']:
    p=Path(item['path']);b=p.read_bytes()
    assert len(b)==item['bytes'] and sha(b)==item['sha256']
    payload['inputs/'+p.name]=b
prior=audit['previous_review_archive'];b=Path(prior['path']).read_bytes()
assert len(b)==prior['bytes'] and sha(b)==prior['sha256']
payload['reference/PRIOR_REVIEW.zip']=b
assert len(payload)==len({n.casefold() for n in payload})
manifest={'self_excluded':True,'kind':'SUPPLEMENT_REVIEW_MANIFEST','payload_count':len(payload),'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payload.items())]}
mb=json.dumps(manifest,ensure_ascii=False,indent=2).encode()
with (R/'REVIEW_MANIFEST.json').open('xb') as f:f.write(mb)
with zipfile.ZipFile(R/NAME,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in sorted(payload.items()):z.writestr(n,b)
    z.writestr('REVIEW_MANIFEST.json',mb)
with zipfile.ZipFile(R/NAME) as z:
    assert z.testzip() is None and set(z.namelist())==set(payload)|{'REVIEW_MANIFEST.json'}
    for n,b in payload.items():assert z.read(n)==b
receipt={'status':'SUPPLEMENT_REVIEW_PACKAGE_VERIFIED','decision':decision['status'],'zip':{'path':str(R/NAME),'bytes':(R/NAME).stat().st_size,'sha256':sha((R/NAME).read_bytes())},'payload_count':len(payload),'entries':len(payload)+1,'manifest_sha256':sha(mb),'inputs_and_prior_review_unchanged':True,'native_ready':False,'native_approved':False,'reviewer_candidate_execution':0,'recipient':None}
for item in audit['inputs']+[prior]:
    b=Path(item['path']).read_bytes();assert len(b)==item['bytes'] and sha(b)==item['sha256']
with (R/'REVIEW_DELIVERY_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
print(json.dumps(receipt,ensure_ascii=False))
