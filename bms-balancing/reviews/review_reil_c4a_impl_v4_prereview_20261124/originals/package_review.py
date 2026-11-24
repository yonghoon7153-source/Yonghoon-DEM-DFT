import binascii,hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath
root=Path(__file__).resolve().parent; prior=root.parent/'reil_c4a_v3_review_20261124'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
attachment=Path('C:/Users/Administrator/Downloads/REIL_C4A_v4_SEND_READY.txt')
selected=[attachment]+[prior/f for f in ['CODEX_REPLY_KO.txt','REVIEW_KO.txt','REVIEW_DECISION.json','DELIVERY_RECEIPT.json','REIL_C4A_IMPL_V3_PREREVIEW_20261124.zip']]
before=[ident(p) for p in selected]
assert attachment.read_bytes()==(root/'input'/attachment.name).read_bytes()
assert before[-1]['bytes']==1467669 and before[-1]['sha256']=='a1202b694048e31a6c21956b825c40a9c534dfd382c1c56a2823edfcc8b53a7a'
basis=root/'basis/prior_v3_review';basis.mkdir(parents=True,exist_ok=True)
for p in selected[1:-1]:(basis/p.name).write_bytes(p.read_bytes())
dump(root/'SELECTED_LOCAL_INPUTS.json',{'kind':'V4_REVIEW_SELECTED_LOCAL_INPUTS','boundary':'After substantive document review; before review packaging. Not a whole-session before snapshot.','files':before})
intake=json.loads((root/'INTAKE.json').read_text('utf-8'));checks=json.loads((root/'PRESERVATION_CHECK.json').read_text('utf-8'))
assert intake['v3_preserved'] and intake['ledger_prior_exact_prefix'] and intake['changed_hunks']==8
assert len(checks['preserved_requests'])==2 and all(x['matches_prior'] for x in checks['preserved_requests'])
decision=json.loads((root/'REVIEW_DECISION.json').read_text('utf-8'))
b=(root/'input/REIL_C4A_IMPL_REQUEST_v4_20261124.md').read_bytes();assert len(b)==decision['request']['bytes'] and sha(b)==decision['request']['sha256']
names=sorted([p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()])
assert len(names)==len({n.casefold() for n in names})
for n in names:
 p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n
manifest={'kind':'REIL_C4A_V4_REVIEW_MANIFEST','files':[{'path':n,'bytes':(root/n).stat().st_size,'sha256':sha((root/n).read_bytes())} for n in names],'target_execution':0,'COMSOL_policy':'PAUSED_BY_USER'}
dump(root/'PACKAGE_MANIFEST.json',manifest)
archive=root/'REIL_C4A_IMPL_V4_PREREVIEW_20261124.zip';assert not archive.exists()
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names+['PACKAGE_MANIFEST.json']:z.write(root/n,n)
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==set(names+['PACKAGE_MANIFEST.json'])
 for i in z.infolist():
  assert not stat.S_ISLNK(i.external_attr>>16)
  b=z.read(i.filename);assert len(b)==i.file_size and binascii.crc32(b)&0xffffffff==i.CRC and b==(root/i.filename).read_bytes()
 for r in manifest['files']:
  b=z.read(r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
after=[ident(p) for p in selected];assert after==before
dump(root/'SELECTED_LOCAL_SOURCES_POST_PACKAGE.json',{'kind':'V4_REVIEW_POST_PACKAGE_SELECTED_LOCAL_INPUTS','files':after,'all_match':True,'scope':'Six selected local originals only; not a remote runtime or whole-filesystem audit.'})
receipt={'kind':'REIL_C4A_V4_REVIEW_DELIVERY_RECEIPT','recipient':None,'archive':ident(archive),'manifest':ident(root/'PACKAGE_MANIFEST.json'),'payload_count':len(names),'entries':len(names)+1,'verification':'Exact member set, safe case-unique relative paths, non-link metadata, decompressed sizes/SHA256 and independently recomputed CRC32 matched.','selected_local_inputs_preserved':len(after),'decision':decision['decision'],'V3_N1':'CLOSED_DOCUMENT_SCOPE','new_blocking_findings':0,'target_execution':0,'pytest_collection':0,'functional_tests':0,'COMSOL':0,'COMSOL_policy':'PAUSED_BY_USER','implementation_or_execution_approved':False,'numeric_review_budget_seconds':None,'whole_review_elapsed_claim':None,'boundary':'After ZIP readback and selected local original rehashes; before receipt write/readback and actual tool return.'}
dump(root/'DELIVERY_RECEIPT.json',receipt);assert json.loads((root/'DELIVERY_RECEIPT.json').read_text('utf-8'))==receipt
print(json.dumps({'kind':'REIL_C4A_V4_REVIEW_PACKAGE_RETURN','archive':ident(archive),'receipt':ident(root/'DELIVERY_RECEIPT.json'),'post_package':ident(root/'SELECTED_LOCAL_SOURCES_POST_PACKAGE.json'),'payload_count':len(names),'entries':len(names)+1,'decision':decision['decision'],'V3_N1':'CLOSED_DOCUMENT_SCOPE','new_blocking_findings':0,'target_execution':0,'pytest_collection':0,'functional_tests':0,'COMSOL':0,'COMSOL_policy':'PAUSED_BY_USER','boundary':'After review ZIP/receipt readback and local original preservation checks; before this actual return and its subsequent transcription.'},ensure_ascii=False,indent=2))
