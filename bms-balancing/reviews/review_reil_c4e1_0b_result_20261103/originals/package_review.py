"""Reviewer-owned packaging/data integrity only; received code is never imported."""
import hashlib,json,pathlib,stat,zipfile,zlib
root=pathlib.Path(__file__).resolve().parent
archive_name='REIL_C4E1_0B_RESULT_REVIEW_20261103.zip'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def readj(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with (root/n).open('xb') as f:f.write(b)
    assert (root/n).read_bytes()==b
    return ident(b)
decision=readj(root/'REVIEW_DECISION.json')
assert decision['decision']=='STOP_HANDLING_ACCEPTED_E1_0B_INCOMPLETE_TEST_CORRECTION_REQUIRED'
assert readj(root/'BRANCH_AT_CLOSE.json')['match'] is True
red=readj(root/'RED_RESULT_REVIEW.json')
assert red['common_checks_all_pass'] and sum(x['match'] for x in red['failure_checks'])==8
assert len(red['failure_checks'])==9 and red['node_sets']['FAILED']['match'] and red['node_sets']['PASSED']['match']
assert readj(root/'L33_CAUSE_REVIEW.json')['conclusion']=='CONFIRMED_TEST_FIXTURE_DEFECT'
proc=readj(root/'PROCEDURE_REVIEW.json')
assert all(x['equals_EXPECT'] and x['source_start_equals_EXPECT'] and x['source_end_equals_EXPECT'] for x in proc['source_checks'])
assert proc['all_10_start_hashes_match_applicable_capture']
linkage=readj(root/'BASIS_LINKAGE.json')
selected=[dict(x) for x in linkage['selected_local_basis']]
prior=root.parent/'reil_c4e_e1_0b_v2_prereview_20261103'
src=prior/'L23_STATIC_REVIEW.json';b=src.read_bytes();sig=ident(b)
pm={x['path']:x for x in readj(prior/'PACKAGE_MANIFEST.json')['files']}
assert sig=={k:pm[src.name][k] for k in sig}
dst=root/'basis/prior_v2_review'/src.name
with dst.open('xb') as f:f.write(b)
selected.append({'path':str(src),**sig,'copy':dst.relative_to(root).as_posix(),'scope':'prior_review_read_only'})
for row in readj(root/'SOURCE_IDENTITIES.json')['files']:
    selected.append({'path':str(root/'source'/row['path']),'bytes':row['bytes'],'sha256':row['sha256'],'scope':'pinned_Git_blob_capture'})
att=pathlib.Path('C:/Users/Administrator/Downloads/REIL_C4E1_0B_RESULT_REVIEW_SEND_20261103.md')
selected.append({'path':str(att),**ident((root/'input'/att.name).read_bytes()),'scope':'user_local_attachment'})
assert len({x['path'].casefold() for x in selected})==len(selected)
for x in selected:assert ident(pathlib.Path(x['path']).read_bytes())=={k:x[k] for k in ('bytes','sha256')},x['path']
save('SELECTED_INPUTS_POST_REVIEW.json',{'kind':'LOCAL_REVIEW_SELECTED_INPUT_READBACK','count':len(selected),'all_match':True,'files':selected,'scope':'Named local attachment, captures, and prior review sources only; not additional remote original files or remote worktree audit.'})
payload={}
excluded={archive_name,'PACKAGE_MANIFEST.json','DELIVERY_RECEIPT.json','PACKAGE_TOOL_RETURN.json','DELIVERY_RECORDS.json','PACKAGE_READBACK.json'}
for p in sorted(root.rglob('*')):
    if not p.is_file() or p.name in excluded:continue
    assert not p.is_symlink()
    name=p.relative_to(root).as_posix()
    assert '..' not in pathlib.PurePosixPath(name).parts and ':' not in name and '\\' not in name
    payload[name]=p.read_bytes()
assert len(set(n.casefold() for n in payload))==len(payload)
rows=[{'path':n,**ident(b),'crc32':format(zlib.crc32(b)&0xffffffff,'08x')} for n,b in payload.items()]
manifest=save('PACKAGE_MANIFEST.json',{'kind':'E1_0B_RESULT_REVIEW_PACKAGE','payload_count':len(rows),'files':rows,'decision':decision['decision'],'target_execution_by_reviewer':0})
entries={**payload,'PACKAGE_MANIFEST.json':(root/'PACKAGE_MANIFEST.json').read_bytes()}
with zipfile.ZipFile(root/archive_name,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for n,b in entries.items():z.writestr(n,b)
with zipfile.ZipFile(root/archive_name) as z:
    assert len(z.namelist())==len(entries) and set(z.namelist())==set(entries)
    assert len({n.casefold() for n in z.namelist()})==len(entries)
    for info in z.infolist():
        assert not stat.S_ISLNK(info.external_attr>>16)
        b=z.read(info.filename)
        assert b==entries[info.filename] and info.file_size==len(b)
        assert info.CRC==zlib.crc32(b)&0xffffffff
for x in selected:assert ident(pathlib.Path(x['path']).read_bytes())=={k:x[k] for k in ('bytes','sha256')}
archive=ident((root/archive_name).read_bytes())
receipt=save('DELIVERY_RECEIPT.json',{'kind':'E1_0B_STOPPED_RESULT_REVIEW_DELIVERY_RECEIPT','recipient':None,'archive':{'name':archive_name,**archive},'manifest':{'name':'PACKAGE_MANIFEST.json',**manifest},'payload_count':len(rows),'entries':len(entries),'verification':'Exact member set, safe unique paths, sizes, decompressed SHA-256 and independently computed CRC32 matched.','selected_local_input_paths_rechecked':len(selected),'all_selected_match':True,'pinned_commit':decision['pinned_commit'],'decision':decision['decision'],'required_correction':'E1_0B_RESULT_N1','prior_review_correction_included':True,'target_execution_by_reviewer':0,'functional_tests_by_reviewer':0,'new_execution_authorized':False,'external_transmission':False,'whole_work_elapsed_claim':None,'boundary':'After archive readback and selected input rehash; before receipt write/readback and tool return.'})
print(json.dumps({'kind':'E1_0B_RESULT_REVIEW_PACKAGE_RETURN','archive':{'name':archive_name,**archive},'manifest':manifest,'receipt':receipt,'payload_count':len(rows),'entries':len(entries),'selected_local_input_paths_matched':len(selected),'decision':decision['decision'],'target_execution_by_reviewer':0,'new_execution_authorized':False,'boundary':'After receipt write/readback; before tool return and its later transcript.'},ensure_ascii=False))
