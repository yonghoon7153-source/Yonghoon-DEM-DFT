"""Bounded reviewer checks: selected exact AST readers and inert attach boundary.

No project module import, ledger mutation, restore, class change, scientific run.
The actual attach body is evaluated with explicit inert collaborators; its write
sink raises before any write. This is NOT a full production attach invocation.
"""
from pathlib import Path
import ast, copy, contextlib, hashlib, json, re, secrets, sys, types, unicodedata
import yaml
OUT=Path(__file__).resolve().parent
DD=Path('C:/Users/Administrator/Documents/Codex/g72_20260925/degradation-degeneracy')
SOURCE=DD/'tools/preserve.py'
raw=SOURCE.read_bytes(); tree=ast.parse(raw,filename=str(SOURCE))
names={'PreserveError','_is_hex64','_nonempty_str','_repo_relative_or_refuse','_receipt_core_sha256',
       'read_verification_receipt','_receipt_output_pair','_assert_receipt_bound_to_bundle','attach_bundle_evidence'}
selected=[]
for n in tree.body:
    if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names: selected.append(n)
    elif isinstance(n,ast.Assign):
        keys={t.id for t in n.targets if isinstance(t,ast.Name)}
        if keys&{'_HEX64','_HEX16','LIFECYCLE_OWNED_EVIDENCE_KEYS'} or any(k.startswith('VERIFICATION_RECEIPT_') for k in keys):selected.append(n)
assert {n.name for n in selected if isinstance(n,(ast.FunctionDef,ast.ClassDef))}==names
g={'Path':Path,'hashlib':hashlib,'secrets':secrets,'unicodedata':unicodedata,'re':re,'REPO_ROOT':DD}
exec(compile(ast.Module(body=selected,type_ignores=[]),str(SOURCE)+'[SELECTED_ONLY]','exec'),g)
sys.modules['src']=types.ModuleType('src')
io=types.ModuleType('src.io');io.source_digest=lambda:'518d4f63076b77e3';sys.modules['src.io']=io
scratch=OUT/'receiver_inputs';scratch.mkdir(exist_ok=False)
base=yaml.safe_load((DD/'docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml').read_bytes())
leg=base['core']['leg_id']; bundle=DD/base['core']['bundle']['uri']
results=[]
def reader_case(name, mutate=None):
    rec=copy.deepcopy(base)
    if mutate:mutate(rec['core'])
    rec['core_sha256']=g['_receipt_core_sha256'](rec['core'])
    p=scratch/(name+'.yaml');p.write_bytes(yaml.safe_dump(rec,allow_unicode=True,sort_keys=False,width=100).encode('utf-8'))
    item={'id':name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    try:
        core=g['read_verification_receipt'](p.name,leg,repo_root=scratch)
        item['reader']='ACCEPTED'
        try:
            item['bound_run']=g['_assert_receipt_bound_to_bundle'](core,bundle,leg)
            item['bundle_binding']='ACCEPTED'
        except g['PreserveError'] as exc:item.update(bundle_binding='REJECTED',reason=str(exc))
    except g['PreserveError'] as exc:item.update(reader='REJECTED',reason=str(exc))
    results.append(item)
    return item
reader_case('R00_real_receipt_control')
reader_case('R01_wrong_leg_control',lambda c:c.update(leg_id='different_leg'))
reader_case('R03_validator_fail_control',lambda c:c['validation'].update(ok=False))
reader_case('R04_missing_sealed_summary',lambda c:c.update(outputs=[c['outputs'][0]]))
reader_case('R05_disagreeing_pair',lambda c:c['outputs'][1].update(semantic_sha256='0'*64))
reader_case('R05b_duplicate_role',lambda c:c.update(outputs=[c['outputs'][0],dict(c['outputs'][0])]))
reader_case('R06_wrong_source_fits',lambda c:c['outputs'][0].update(source_file_sha256='0'*64))
reader_case('R07_wrong_restore_run',lambda c:c['restore'].update(run_dir_relative='results/ANOTHER_RUN'))
reader_case('R08_nonhex_semantic',lambda c:c['outputs'][0].update(semantic_sha256='not-a-digest'))
reader_case('R09_missing_source_fits',lambda c:c['outputs'][0].pop('source_file_sha256'))
reader_case('R10_identity_null',lambda c:c['identity'].update(make_receipt_sha256=None))
reader_case('R11_wrong_sealed_file',lambda c:c['outputs'][1].update(file_sha256='0'*64))
reader_case('R12_wrong_canonicalizer',lambda c:c['outputs'][1].update(canonicalizer='different'))
reader_case('R13_missing_restore_run',lambda c:c['restore'].update(run_dir_relative=''))
assert results[0]['reader']==results[0]['bundle_binding']=='ACCEPTED'
assert all(x.get('reader')=='REJECTED' or x.get('bundle_binding')=='REJECTED' for x in results[1:])

# Independently inspect actual bundle index/member bytes, not archive/restore code.
idx=bundle/'payload_sha256.yaml';mapping=yaml.safe_load(idx.read_bytes())
assert isinstance(mapping,dict) and mapping
members={p.relative_to(bundle).as_posix():p for p in bundle.rglob('*') if p.is_file() and p!=idx}
assert set(mapping)==set(members)
assert all(hashlib.sha256(members[n].read_bytes()).hexdigest()==v for n,v in mapping.items())
b=base['core']['bundle']
assert hashlib.sha256(idx.read_bytes()).hexdigest()==b['payload_index_sha256']
assert hashlib.sha256((bundle/'fits.parquet').read_bytes()).hexdigest()==b['fits_sha256']
assert len(members)+1==b['files']
assert sum(p.stat().st_size for p in members.values())+idx.stat().st_size==b['bytes']

# Exact attach body, but validation entry/OS lock/content-id/write boundary are
# inert. Real receipt pair/bundle binding remain the actual selected helpers.
# No ledger file is modified by the subject function.
class WriteBoundary(Exception):pass
captured={}
def no_write(path,text):
    captured['proposed_document']=yaml.safe_load(text)
    raise WriteBoundary('WRITE_SINK_INTERCEPTED_NO_WRITE')
g.update(check_id=lambda value: None,
         read_verification_receipt=lambda *a,**kw:copy.deepcopy(base['core']),
         _verify_declared_bundle=lambda *a,**kw:[],canonical_ledger=lambda p:p,
         _ledger_lock=lambda p:contextlib.nullcontext(),bundle_content_id=lambda *a,**kw:'f'*64,
         _atomic_write_text=no_write)
ev={'phases':['grid','fit'],'attempt_id':'reviewer-inert','run_spec_digest':'b'*64,
    'attempt_verifier':'reviewer-inert','verifier_origin':'reviewer-inert',
    'out':base['core']['restore']['run_dir_relative']}
core_sha=g['_receipt_core_sha256'](base['core'])
receipt_path='docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml'
attach_results=[]
for name,status,mode in (
    ('A00_pending_matching_out','preservation_pending','match'),
    ('A01_pending_wrong_out','preservation_pending','wrong'),
    ('A02_pending_missing_out','preservation_pending','missing'),
    ('A03_full_matching_out','full_bundle','match'),
    ('A04_full_wrong_out','full_bundle','wrong'),
    ('A05_full_missing_out','full_bundle','missing'),
):
    evidence=copy.deepcopy(ev)
    if mode=='wrong':evidence['out']='results/OTHER_RUN'
    if mode=='missing':evidence.pop('out')
    if status=='full_bundle':evidence.update(verification_receipt_core_sha256=core_sha,verification_receipt=receipt_path)
    doc={'legs':[{'leg_id':leg,'preservation_status':status,'evidence':evidence}]}
    p=scratch/(name+'.yaml');p.write_bytes(yaml.safe_dump(doc,allow_unicode=True,sort_keys=False).encode('utf-8'))
    before=p.read_bytes();captured.clear()
    result={'id':name,'original_fixture_sha256':hashlib.sha256(before).hexdigest(),'out_mode':mode,'status':status}
    try:
        ret=g['attach_bundle_evidence'](leg,receipt_path,ledger=p,repo_root=DD)
        result.update(outcome='RETURNED',return_value=ret)
    except WriteBoundary:
        proposal=captured['proposed_document']['legs'][0]
        result.update(outcome='REACHED_WRITE_SINK_NO_WRITE',proposed_preservation_status=proposal['preservation_status'],proposed_validation_status=proposal['validation_status'])
    except g['PreserveError'] as exc:result.update(outcome='REJECTED',reason=str(exc))
    assert p.read_bytes()==before
    result['fixture_bytes_unchanged']=True
    attach_results.append(result)
assert [x['outcome'] for x in attach_results]==['REACHED_WRITE_SINK_NO_WRITE','REJECTED','REACHED_WRITE_SINK_NO_WRITE','RETURNED','RETURNED','RETURNED']
report={'scope':'Exact selected AST readers/helpers; source_digest stubbed to independent byte measurement. Attach body has explicit inert collaborators and intercepted write sink. Not full production attach/pytest/restore/class execution.',
        'source_sha256':hashlib.sha256(raw).hexdigest(),'selected_definitions':[{'name':n.name,'line':n.lineno,'end_line':n.end_lineno} for n in selected if hasattr(n,'name')],
        'reader_and_bundle_cases':results,'actual_bundle_index_members':len(mapping),'actual_bundle_set_size_sha_agree':True,
        'attach_control_flow_cases':attach_results,'attach_stubs':['check_id','read_verification_receipt (already separately checked)','_verify_declared_bundle (data checked separately)','canonical_ledger','_ledger_lock','bundle_content_id','_atomic_write_text (raises before writing)'],
        'project_module_imports':0,'subject_ledger_writes':0,'restores':0,'class_changes':0,'scientific_runs':0}
(OUT/'RECEIVER_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'reader_cases':results,'attach_cases':attach_results,'subject_ledger_writes':0},ensure_ascii=False,indent=2))
