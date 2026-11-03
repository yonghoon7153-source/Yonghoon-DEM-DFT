"""Reviewer-owned data capture linkage, never imports received programs."""
import hashlib,json,pathlib,re
root=pathlib.Path(__file__).resolve().parent
prior=root.parent/'reil_c4e_e1_0b_v2_prereview_20261103'
old=root.parent/'reil_c4e_e1_0b_prereview_20261030'
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
manifest={r['path']:r for r in json.loads((prior/'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))['files']}
changed={r['filename'] for r in json.loads((root/'COMPARE_FROM_PRIOR.json').read_text(encoding='utf-8'))['files']}
meta=json.loads((root/'source/bms-balancing/evidence/reil_c4e1_0b_20261103/01_red_e1_0b.meta.json').read_text(encoding='utf-8'))
start=(root/'source/bms-balancing/evidence/reil_c4e1_0b_20261103/00_start.txt').read_text(encoding='utf-8')
startrows=re.findall(r'^([0-9a-f]{64})  /home/user/Yonghoon-DEM-DFT/(.+)$',start,re.M)
targets=set(meta['source_start'])|{n for h,n in startrows}
selected=[];bindings=[]
for name in sorted(targets):
    current=root/'source'/name
    if current.is_file():
        bindings.append({'path':name,**ident(current.read_bytes()),'capture':current.relative_to(root).as_posix(),'scope':'current_pin_exact_blob'})
        continue
    assert name not in changed,name
    options=[prior/'source'/name,prior/'basis/unchanged_at_pin'/name]
    src=next(p for p in options if p.is_file());b=src.read_bytes();sig=ident(b)
    expected=manifest[src.relative_to(prior).as_posix()]
    assert sig=={k:expected[k] for k in sig},name
    dst=root/'basis/unchanged_at_pin'/name;dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as f:f.write(b)
    assert dst.read_bytes()==b
    selected.append({'path':str(src),**sig,'copy':dst.relative_to(root).as_posix(),'scope':'prior_captured_blob_unchanged_in_commit_compare'})
    bindings.append({'path':name,**sig,'capture':dst.relative_to(root).as_posix(),'scope':'prior_capture_plus_unchanged_commit_compare'})
by={x['path']:x for x in bindings}
assert len(meta['source_start'])==14 and meta['source_start']==meta['source_end']
for p,v in meta['source_start'].items():assert v=={k:by[p][k] for k in v},p
assert len(startrows)==10
for h,p in startrows:assert by[p]['sha256']==h,p
for folder,names,label in [(prior,['REVIEW_KO.txt','REVIEW_DECISION.json','PACKAGE_MANIFEST.json','STATIC_AUDIT.json'],'prior_v2_review'),(old,['REVIEW_KO.txt','Q4_STATIC_REVIEW.json','REVIEW_DECISION.json'],'prior_v1_review')]:
    pm={r['path']:r for r in json.loads((folder/'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))['files']}
    for name in names:
        src=folder/name;b=src.read_bytes();sig=ident(b)
        if name in pm:assert sig=={k:pm[name][k] for k in sig},name
        dst=root/'basis'/label/name;dst.parent.mkdir(parents=True,exist_ok=True)
        with dst.open('xb') as f:f.write(b)
        selected.append({'path':str(src),**sig,'copy':dst.relative_to(root).as_posix(),'scope':'prior_review_read_only'})
for row in selected:assert ident(pathlib.Path(row['path']).read_bytes())=={k:row[k] for k in ('bytes','sha256')}
prevstatus=(prior/'source/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes()
assert (root/'source/bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md').read_bytes().startswith(prevstatus)
out={'kind':'PINNED_CAPTURE_BASIS_LINKAGE','bindings':bindings,'source_count':14,'source_start_end_current_or_unchanged_capture_match':True,'start_record_count':10,'start_record_hashes_match':True,'prior_status_exact_prefix_preserved':True,'selected_local_basis':selected,'scope':'Byte/JSON comparison only; no target execution or remote worktree measurement.'}
(root/'BASIS_LINKAGE.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'bindings':len(bindings),'source_count_match':14,'start_count_match':10,'selected_local_basis':len(selected),'prior_status_prefix':True}))
