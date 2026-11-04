import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).parent
PREV=ROOT.parent/'reil_c4e1_0b_a2_result_review_20261104'
ZIP=ROOT/'REIL_C4E_E1_1_3_SCOPE_REVIEW_20261104.zip'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'name':p.name,'bytes':len(b),'sha256':sha(b)}
def writej(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for n in ['SOURCE_IDENTITIES.json','ADDITIONAL_IDENTITIES.json']:
 dst=ROOT/'basis'/('PRIOR_'+n)
 assert not dst.exists()
 shutil.copyfile(PREV/n,dst)
inp=ROOT/'input/REIL_C4E_E1_1_3_SCOPE_20261104.md'
orig=Path('C:/Users/Administrator/Downloads')/inp.name
assert orig.read_bytes()==inp.read_bytes()
d=json.loads((ROOT/'REVIEW_DECISION.json').read_text(encoding='utf-8'))
assert d['required_document_corrections']==3 and not d['e1_1_3_execution_authorized']
assert not ZIP.exists()
excluded={'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json',ZIP.name}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name not in excluded)
members=[]
for p in files:
 assert not p.is_symlink()
 n=p.relative_to(ROOT).as_posix()
 assert n and not n.startswith('/') and '..' not in Path(n).parts
 b=p.read_bytes();members.append({'name':n,'bytes':len(b),'sha256':sha(b)})
assert len({r['name'].casefold() for r in members})==len(members)
manifest={'kind':'REIL_SCOPE_REVIEW_PACKAGE_MANIFEST','self_excluded':True,'members':members}
mp=ROOT/'PACKAGE_MANIFEST.json';writej(mp,manifest)
with zipfile.ZipFile(ZIP,'x',zipfile.ZIP_DEFLATED) as z:
 for p in files+[mp]:z.write(p,p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ZIP) as z:
 assert set(z.namelist())=={r['name'] for r in members}|{'PACKAGE_MANIFEST.json'}
 assert len(z.namelist())==len(members)+1
 assert z.testzip() is None
 for r in members:
  b=z.read(r['name']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
 assert z.read('PACKAGE_MANIFEST.json')==mp.read_bytes()
receipt={'kind':'REIL_E1_1_3_SCOPE_REVIEW_DELIVERY_RECEIPT','recipient':None,'archive':ident(ZIP),'manifest':ident(mp),
 'payload_count':len(members),'entry_count':len(members)+1,
 'verification':'Exact member set, case uniqueness, safe relative paths, bytes, SHA256 and ZIP readback CRC checked.',
 'decision':d['decision'],'required_document_corrections':3,
 'source_attachment_preserved':orig.read_bytes()==inp.read_bytes(),
 'received_code_execution':0,'test_execution':0,'detach_probe_execution':0,'e1_1_3_execution_authorized':False,
 'branch_at_close':json.loads((ROOT/'BRANCH_AT_CLOSE.json').read_text(encoding='utf-8')),
 'whole_work_elapsed_claim':None,'numeric_review_budget':None,
 'boundary':'After review ZIP readback; before receipt write and this tool return. A later transcript preserves this tool result.'}
rp=ROOT/'DELIVERY_RECEIPT.json';assert not rp.exists();writej(rp,receipt)
assert json.loads(rp.read_text(encoding='utf-8'))==receipt
print(json.dumps({'kind':'REIL_SCOPE_REVIEW_PACKAGE_RETURN','archive':ident(ZIP),'receipt':ident(rp),'manifest':ident(mp),
 'payload_count':len(members),'entry_count':len(members)+1,'decision':d['decision'],'required_document_corrections':3,
 'received_code_execution':0,'test_execution':0,'detach_probe_execution':0,
 'boundary':'After ZIP and receipt readback; before tool return and its later transcription.'},ensure_ascii=False,indent=2))

