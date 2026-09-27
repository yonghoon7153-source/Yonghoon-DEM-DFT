from pathlib import Path
import hashlib,json,zipfile
H=Path(__file__).resolve().parent
files=['REVIEW_KO.md','CLAUDE_UPDATE_KO.md','CODEX_NEXT_TASK_KO.md','AUDIT.json','PDF_TEXT.txt','pdf-page-1.png','audit.py','package_review.py']
def ident(p):
    with p.open('rb') as f:h=hashlib.file_digest(f,'sha256').hexdigest()
    return {'bytes':p.stat().st_size,'sha256':h}
inputs=json.loads((H/'AUDIT.json').read_bytes())['inputs']
assert all(ident(Path('C:/Users/Administrator/Downloads')/name)==v for name,v in inputs.items())
manifest={f:ident(H/f) for f in files}
mb=(json.dumps({'scope':'Reviewer report and two sendable documents; no new execution approval','files':manifest},ensure_ascii=False,indent=2)+'\n').encode()
p=H/'B020_VOLTAGE_REVIEW_AND_HANDOFF_20260928.zip'
with zipfile.ZipFile(p,'x',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(H/f,f)
    z.writestr('MANIFEST.json',mb)
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None and set(z.namelist())==set(files)|{'MANIFEST.json'}
    for f,record in manifest.items():
        b=z.read(f);assert len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256']
r={'status':'REVIEW_AND_DOCUMENTS_COMPLETE','decision':'ACCEPT_BOUNDED_ALGEBRAIC_DECOMPOSITION','P1':0,'P2':0,'package':{'file':p.name,**ident(p)},'payload_count':len(files),'manifest_sha256':hashlib.sha256(mb).hexdigest(),'recipient':None,'COMSOL_JVM_received_program_calls':0,'inputs_preserved':True,'B_or_long_run_approved':False,'external_delivery_performed':False,'visual_review':'One PDF page independently rendered and inspected; labels, signs, table and notes readable; no clipping observed. Poppler Symbol/ArialUnicode display-font warnings did not prevent rendering.'}
(H/'REVIEW_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(r,ensure_ascii=False))
