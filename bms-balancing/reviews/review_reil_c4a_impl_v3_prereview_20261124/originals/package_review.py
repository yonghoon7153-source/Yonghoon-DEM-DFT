import binascii,hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath
root=Path(__file__).resolve().parent
prior=root.parent/'reil_c4a_impl_v2_prereview_20261108'
attachment=Path('C:/Users/Administrator/Downloads/REIL_C4A_v3_SEND_READY.txt')
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b)}
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
selected=[attachment]+[prior/f for f in ['CODEX_REPLY_KO.txt','REVIEW_KO.txt','REVIEW_DECISION.json','DELIVERY_RECEIPT.json','REIL_C4A_IMPL_V2_PREREVIEW_20261108.zip']]
before=[ident(p) for p in selected]
assert before[0]['sha256']=='ebd14f641cf2132c8ab8f39befbe6ae008b03273cee85a46a9f68375df3cd847'
assert attachment.read_bytes()==(root/'input'/attachment.name).read_bytes()
assert before[-1]['sha256']=='3d346f331b1a89ffa906993f8dd7f75d895fc7af5d05b71d562bf785c2d168e2'
basis=root/'basis/prior_v2_review';basis.mkdir(parents=True,exist_ok=True)
for p in selected[1:-1]:(basis/p.name).write_bytes(p.read_bytes())
dump(root/'SELECTED_LOCAL_INPUTS.json',{'kind':'REVIEW_SELECTED_LOCAL_INPUTS','boundary':'After substantive static review; before review packaging. Not an initial whole-session snapshot.','files':before})
compare=json.loads((root/'SOURCE_COMPARISON.json').read_text('utf-8'))
assert len(compare)==27 and sum(x['matches_prior'] is True for x in compare)==23
audit=json.loads((root/'STATIC_AUDIT.json').read_text('utf-8'));assert audit['ledger_previous_exact_prefix']
request=(root/'input/REIL_C4A_IMPL_REQUEST_v3_20261124.md').read_bytes()
assert len(request)==96546 and sha(request)=='2156f12d35c05c3a41307c4c254ce0bf836f9bdcbc33485c1eba2bb995d71c5b'
decision=json.loads((root/'REVIEW_DECISION.json').read_text('utf-8'));assert sum(x['status'].startswith('CLOSED') for x in decision['closure_map'])==11
cap=json.loads((root/'capture/COMPARE_PIN_TO_SUBMISSION.json').read_text('utf-8'))
cs=cap.get('structuredContent',{})
commit=json.loads((root/'capture/SUBMISSION_COMMIT.json').read_text('utf-8')).get('structuredContent',{})
dump(root/'FETCH_PROVENANCE.json',{'kind':'FIXED_GITHUB_READ_ONLY_PROVENANCE','repository':decision['repository'],'submission_commit':decision['submission_commit'],'prior_pin':decision['prior_pin'],'request':decision['request'],'fetched_references':27,'git_blob_hashes_verified':True,'prior_exact_matches':23,'ledger_exact_old_prefix':True,'comparison_limit':'Compare response includes 300 file entries; absence from that response is not proof that any other path is unchanged. No whole-tree equality claim.','captures':'Original fetch responses stored under capture; source decoding is reviewed metadata work, not target import.','attachment_and_repository_send_are_distinct':True})
names=[]
for d in ['input','source','basis','capture']:
 names.extend(p.relative_to(root).as_posix() for p in (root/d).rglob('*') if p.is_file())
names += ['REVIEW_KO.txt','CODEX_REPLY_KO.txt','REVIEW_DECISION.json','REVIEW_TOOL_NOTE.json','SOURCE_COMPARISON.json','STATIC_AUDIT.json','FETCH_PROVENANCE.json','SELECTED_LOCAL_INPUTS.json','decode_sources.py','static_audit.py','package_review.py']
names=sorted(names)
assert len(names)==len(set(n.casefold() for n in names))
for n in names:
 p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and '\\' not in n and ':' not in n
manifest={'kind':'REIL_C4A_V3_REVIEW_PACKAGE_MANIFEST','files':[{'path':n,'bytes':(root/n).stat().st_size,'sha256':sha((root/n).read_bytes())} for n in names],'target_execution':0,'pytest_collection':0,'tests':0}
dump(root/'PACKAGE_MANIFEST.json',manifest)
archive=root/'REIL_C4A_IMPL_V3_PREREVIEW_20261124.zip'
assert not archive.exists(),'Do not overwrite an existing sealed review ZIP'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names+['PACKAGE_MANIFEST.json']:z.write(root/n,n)
with zipfile.ZipFile(archive) as z:
 assert set(z.namelist())==set(names+['PACKAGE_MANIFEST.json'])
 for i in z.infolist():
  assert not stat.S_ISLNK(i.external_attr>>16)
  b=z.read(i.filename);assert len(b)==i.file_size and (binascii.crc32(b)&0xffffffff)==i.CRC
  assert b==(root/i.filename).read_bytes()
 for r in manifest['files']:
  b=z.read(r['path']);assert len(b)==r['bytes'] and sha(b)==r['sha256']
after=[ident(p) for p in selected];assert after==before
post={'kind':'REVIEW_POST_PACKAGE_SELECTED_LOCAL_INPUTS','files':after,'all_match':True,'scope':'Six named existing local inputs only. Fixed remote-source byte checks are separate; not a remote runtime or whole-filesystem audit.'}
dump(root/'SELECTED_LOCAL_SOURCES_POST_PACKAGE.json',post)
receipt={'kind':'REIL_C4A_V3_REVIEW_DELIVERY_RECEIPT','recipient':None,'archive':ident(archive),'manifest':ident(root/'PACKAGE_MANIFEST.json'),'payload_count':len(names),'entries':len(names)+1,'verification':'Exact member set, safe case-unique relative paths, non-link metadata, decompressed size/SHA256 and independently recomputed CRC32 matched.','selected_local_inputs_preserved':len(after),'fixed_reference_files':27,'prior_reference_files_exact_match':23,'prior_ledger_is_exact_prefix':True,'decision':decision['decision'],'closed_subissues':11,'open_subissues':1,'C2':'CLOSED_DOCUMENT_SCOPE','target_import_or_execution':0,'pytest_collection':0,'functional_tests':0,'COMSOL':0,'COMSOL_policy':'PAUSED_BY_USER','implementation_or_execution_approved':False,'numeric_review_budget_seconds':None,'whole_review_elapsed_claim':None,'boundary':'After review ZIP readback and six selected local input rehashes; before receipt write/readback and actual tool return.'}
dump(root/'DELIVERY_RECEIPT.json',receipt)
assert json.loads((root/'DELIVERY_RECEIPT.json').read_text('utf-8'))==receipt
print(json.dumps({'kind':'REIL_C4A_V3_REVIEW_PACKAGE_RETURN','archive':ident(archive),'receipt':ident(root/'DELIVERY_RECEIPT.json'),'post_package':ident(root/'SELECTED_LOCAL_SOURCES_POST_PACKAGE.json'),'payload_count':len(names),'entries':len(names)+1,'decision':decision['decision'],'closed_subissues':11,'open_subissues':1,'C2':'CLOSED_DOCUMENT_SCOPE','target_execution':0,'pytest_collection':0,'functional_tests':0,'COMSOL':0,'COMSOL_policy':'PAUSED_BY_USER','boundary':'After review ZIP/receipt readback and selected input rehashes; before this actual return and its subsequent transcription.'},ensure_ascii=False,indent=2))
