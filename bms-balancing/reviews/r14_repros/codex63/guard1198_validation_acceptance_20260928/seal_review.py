"""Package recipient review; only copies/compares bytes, never executes subject code."""
from pathlib import Path
import json,hashlib,zipfile
from datetime import datetime,timezone
O=Path(__file__).resolve().parent; R=O/'received'
Z=Path('C:/Users/Administrator/Downloads/COMSOL63_GUARD1198_LIMITED_VALIDATION_PASS_20260928.zip')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def raw(v):return (json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
source=Z.read_bytes();assert ident(source)['sha256']=='6af5463ed0d395353de1a9935088c1d6f9503e476d0b5bc1fc9fb65ab80903d1'
files={}
for n in ['REVIEW_KO.md','NEXT_PREEXEC_DIRECTIVE_KO.md','CLAUDE_AND_CODEX_REPLY_KO.md','DECISION.json',
          'PACKAGE_AUDIT.json','EVIDENCE_AUDIT.json','HARNESS_NORMALIZED.diff','CANDIDATE_NORMALIZED.diff',
          'REVIEWER_DIAGNOSTIC_NOTE.json','audit_received.py','audit_evidence.py','seal_review.py']:
    files[n]=(O/n).read_bytes()
    files[n].decode('utf-8')
    if n.endswith('.json'):json.loads(files[n])
references=['candidate/CODE_MANIFEST.json','candidate/CONTRACT.json','candidate/PARENT_COMMAND.ps1',
            'candidate/src/trigger_consumer.py','candidate/src/candidate_entry.py','candidate/src/Guard1198Candidate.java',
            'tests/run_python.py','tests/run_parent.ps1','tests/GuardHarness.java','tests/JAVA_SOURCE_BINDING.json',
            'PRE_TEST_SEAL.json','FINAL_SOURCE_BINDING.json','RESULTS.json','CASE_MAP.json','CORRECTION.json',
            'records/PYTHON_RESULT.json','records/PS_RESULT.json','records/PYTHON_TOOL_RETURN.json',
            'records/JAVA_COMPILE_TOOL_RETURN.json','records/JAVA_STUB_TOOL_RETURN.json','records/POWERSHELL_TOOL_RETURN.json']
with zipfile.ZipFile(Z) as z:
    assert z.testzip() is None
    for n in z.namelist():assert z.read(n)==(R/n).read_bytes(),n
    for n in references:files['reference/'+n]=z.read(n)
manifest=raw({'scope':'Recipient review with selected inert evidence; subject execution not authorized',
              'input_zip_sha256':ident(source)['sha256'],
              'files':[{'file':n,**ident(b)} for n,b in sorted(files.items())]})
p=O/'COMSOL63_GUARD1198_VALIDATION_ACCEPTANCE_REVIEW_20260928.zip'
with zipfile.ZipFile(p,'x',zipfile.ZIP_DEFLATED) as z:
    for n,b in sorted(files.items()):z.writestr(n,b)
    z.writestr('REVIEW_PACKAGE_MANIFEST.json',manifest)
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(files)|{'REVIEW_PACKAGE_MANIFEST.json'}
    assert len(z.namelist())==len({n.casefold() for n in z.namelist()})
    for n,b in files.items():assert z.read(n)==b
    assert z.read('REVIEW_PACKAGE_MANIFEST.json')==manifest
assert Z.read_bytes()==source
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Reviewer delivery, not native approval',
         'package':{'path':str(p),**ident(p.read_bytes())},'payloads':len(files),'entries':len(files)+1,
         'manifest':ident(manifest),'exact_set_size_sha_crc_verified':True,
         'source_zip_and_all_extracted_members_unchanged':True,'recipient':None,
         'subject_code_executions':0,'native_1198_approved':False,'run_30s_approved':False}
with (O/'REVIEW_DELIVERY_RECEIPT.json').open('xb') as f:f.write(raw(receipt))
assert json.loads((O/'REVIEW_DELIVERY_RECEIPT.json').read_bytes())==receipt
print(json.dumps(receipt,ensure_ascii=False))
