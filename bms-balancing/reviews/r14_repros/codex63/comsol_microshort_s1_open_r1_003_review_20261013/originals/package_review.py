"""Review artifact packaging only. No received executable is imported/run."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def encode(o): return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def create(n,b):
    with (R/n).open('xb') as f: f.write(b)
generated=['INPUTS.json','PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','COMSOL_MICROSHORT_S1_OPEN_R1_003_REVIEW_REPLY_20261013.zip']
assert all(not (R/n).exists() for n in generated), 'No overwrite permitted'
inputs=[]
specs=[
 ('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_R1_VALIDATION_003_20261013.zip',665105,'6458419127231ce44203ddef9d10981954ae877fdbf990faab5d3649db172bb3'),
 ('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_R1_PYTHON_PREFLIGHT_20261013.zip',53751,'45bdff07b0db0d24f96766e6224807822ddae6278405a663924c4080edbb8fe8'),
 ('C:/Users/Administrator/.codex/attachments/76a81b79-7d12-4f4c-a60d-79b054a5e148/붙여넣은 텍스트.txt',34659,'b22417b5f8a42da934f58bc73941c40eb1fd35d557a7e3eaaa2c347652757e4d')]
for p,size,h in specs:
    b=Path(p).read_bytes(); assert len(b)==size and sha(b)==h,p
    inputs.append({'path':p,'bytes':size,'sha256':h,'unchanged_at_review_packaging':True})
decision=json.loads((R/'DECISION.json').read_text(encoding='utf-8'))
assert decision['case_evidence']['pass']==93 and decision['state_preserved']['native_ready']==False
assert decision['preservation']['prior001_error_raw_verified']
create('INPUTS.json',encode({'kind':'REVIEW_INPUT_IDENTITIES','files':inputs,'scope':'Read-only source attachments; no remote live filesystem observation.'}))
names=['REVIEW_KO.md','CLAUDE_REPLY_KO.md','DECISION.json','INTAKE_CHECK.json','INPUTS.json',
 'POST_PACKAGE_SELECTED_SOURCES_AFTER.json','USER_SIDECAR_RECONCILIATION.json','REVIEW_ACTIVITY_NOTE.json',
 'notes/CASE_RECONCILIATION.json','notes/PYTHON_AUDIT.json','notes/JAVA_AUDIT.json','notes/PROVENANCE_AUDIT.json',
 'notes/PROVENANCE_SUPPLEMENT_AUDIT.json','review_intake.py','review_counts.py','package_review.py']
payload={n:(R/n).read_bytes() for n in names}
for n,b in payload.items():
    if n.endswith('.json'): json.loads(b)
manifest={'kind':'REVIEW_REPLY_MANIFEST','scope':'Review decision/notes and reviewer data utilities. Not a native approval, test execution package or scientific result.',
 'files':[{'path':n,'bytes':len(b),'sha256':sha(b)} for n,b in sorted(payload.items())]}
create('PACKAGE_MANIFEST.json',encode(manifest))
payload['PACKAGE_MANIFEST.json']=(R/'PACKAGE_MANIFEST.json').read_bytes()
archive=R/generated[-1]
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for n,b in payload.items(): z.writestr(n,b)
with zipfile.ZipFile(archive) as z:
    assert set(z.namelist())==set(payload) and len(z.namelist())==len(payload)
    assert len({n.casefold() for n in z.namelist()})==len(payload)
    assert z.testzip() is None
    for n,b in payload.items(): assert z.read(n)==b,n
b=archive.read_bytes()
receipt={'kind':'INDEPENDENT_REVIEW_DELIVERY_RECEIPT','recipient':None,
 'zip':{'path':str(archive),'bytes':len(b),'sha256':sha(b)},'payload_count':len(names),'entries':len(payload),
 'verification':'Exact set,size,SHA,CRC and byte-for-byte readback',
 'functional_validation':'ACCEPTED_WITH_DOCUMENTED_SCOPE','native_ready':False,
 'scope':'Review reply only. No user approval/release/runtime/token. No retest, engine probe or COMSOL run.'}
create('DELIVERY_RECEIPT.json',encode(receipt))
print(json.dumps(receipt,ensure_ascii=False))
