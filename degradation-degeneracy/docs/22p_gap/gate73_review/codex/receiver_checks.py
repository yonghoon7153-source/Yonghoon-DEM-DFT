"""Limited exact AST control checks; no project imports, real ledger writes,
restore/class operations or scientific/COMSOL programs. Intercept write sink.
"""
from pathlib import Path
import ast,copy,contextlib,hashlib,json,re,secrets,sys,types,unicodedata
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work/gate26-pydeps'))
import yaml
O=Path(__file__).resolve().parent
DD=Path('C:/Users/Administrator/Documents/Codex/g73_20260925/degradation-degeneracy')
SOURCE=DD/'tools/preserve.py';raw=SOURCE.read_bytes();tree=ast.parse(raw)
names={'PreserveError','_is_hex64','_nonempty_str','_repo_relative_or_refuse','_receipt_core_sha256',
       'read_verification_receipt','_receipt_output_pair','_assert_receipt_bound_to_bundle',
       '_assert_ledger_run_bound','attach_bundle_evidence'}
selected=[]
for n in tree.body:
    if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in names:selected.append(n)
    elif isinstance(n,ast.Assign):
        keys={t.id for t in n.targets if isinstance(t,ast.Name)}
        if keys&{'_HEX64','_HEX16','LIFECYCLE_OWNED_EVIDENCE_KEYS'} or any(k.startswith('VERIFICATION_RECEIPT_') for k in keys):selected.append(n)
assert {n.name for n in selected if isinstance(n,(ast.FunctionDef,ast.ClassDef))}==names
g={'Path':Path,'hashlib':hashlib,'secrets':secrets,'unicodedata':unicodedata,'re':re,'REPO_ROOT':DD}
exec(compile(ast.Module(body=selected,type_ignores=[]),str(SOURCE)+'[SELECTED_ONLY]','exec'),g)
sys.modules['src']=types.ModuleType('src')
io=types.ModuleType('src.io');io.source_digest=lambda:'c2ef1a811e70bb4c';sys.modules['src.io']=io
scratch=O/'receiver_inputs';scratch.mkdir(exist_ok=False)
rp='docs/22p_gap/receipts/paired_fixed5_v4.validate.yaml'
base=yaml.safe_load((DD/rp).read_bytes());leg=base['core']['leg_id']
actualcore=g['read_verification_receipt'](rp,leg,repo_root=DD)
assert actualcore==base['core']
bundle=DD/actualcore['bundle']['uri']
bound=g['_assert_receipt_bound_to_bundle'](actualcore,bundle,leg)
core_sha=g['_receipt_core_sha256'](actualcore)
assert core_sha==base['core_sha256']
idx=bundle/'payload_sha256.yaml';mapping=yaml.safe_load(idx.read_bytes())
members={p.relative_to(bundle).as_posix():p for p in bundle.rglob('*') if p.is_file() and p!=idx}
assert set(mapping)==set(members)
assert all(hashlib.sha256(members[n].read_bytes()).hexdigest()==v for n,v in mapping.items())
b=actualcore['bundle']
assert hashlib.sha256(idx.read_bytes()).hexdigest()==b['payload_index_sha256']
assert hashlib.sha256((bundle/'fits.parquet').read_bytes()).hexdigest()==b['fits_sha256']
assert len(members)+1==b['files']
assert sum(p.stat().st_size for p in members.values())+idx.stat().st_size==b['bytes']
class WriteBoundary(Exception):pass
captured={}
def no_write(path,text):
    captured['proposal']=yaml.safe_load(text)
    raise WriteBoundary('WRITE_SINK_INTERCEPTED_NO_WRITE')
g.update(check_id=lambda value:None,read_verification_receipt=lambda *a,**kw:copy.deepcopy(actualcore),
    _verify_declared_bundle=lambda *a,**kw:[],canonical_ledger=lambda p:p,
    _ledger_lock=lambda p:contextlib.nullcontext(),bundle_content_id=lambda *a,**kw:'f'*64,_atomic_write_text=no_write)
ev={'phases':['grid','fit'],'attempt_id':'receiver-inert','run_spec_digest':'b'*64,
    'attempt_verifier':'receiver-inert','verifier_origin':'receiver-inert','out':bound}
results=[]
def check(name,status,mode,value=None,other=False,real=False):
    if real:
        initial=(DD/'docs/22p_gap/LEG_PRESERVATION.yaml').read_bytes()
        doc=yaml.safe_load(initial)
        target=next(e for e in doc['legs'] if e['leg_id']==leg)
        assert target['preservation_status']=='full_bundle' and 'out' not in target['evidence']
    else:
        evidence=copy.deepcopy(ev)
        if mode=='missing':evidence.pop('out')
        elif mode=='wrong':evidence['out']='results/OTHER_RUN'
        elif mode=='invalid':evidence['out']=value
        if status=='full_bundle':evidence.update(verification_receipt_core_sha256=('0'*64 if other else core_sha),verification_receipt=rp)
        doc={'legs':[{'leg_id':leg,'preservation_status':status,'evidence':evidence}]}
        initial=yaml.safe_dump(doc,allow_unicode=True,sort_keys=False).encode()
    p=scratch/(name+'.yaml');p.write_bytes(initial);captured.clear()
    result={'id':name,'status':status,'out_mode':mode,'invalid_value':value,'original_sha256':hashlib.sha256(initial).hexdigest()}
    try:
        result.update(outcome='RETURNED',return_value=g['attach_bundle_evidence'](leg,rp,ledger=p,repo_root=DD))
    except WriteBoundary:
        target=captured['proposal']['legs'][0]
        result.update(outcome='REACHED_WRITE_SINK_NO_WRITE',proposed_status=target['preservation_status'],proposed_validation=target['validation_status'])
    except g['PreserveError'] as exc:result.update(outcome='REJECTED',reason=str(exc))
    assert p.read_bytes()==initial
    if real:assert (DD/'docs/22p_gap/LEG_PRESERVATION.yaml').read_bytes()==initial
    if mode=='match':
        assert result['outcome']==('RETURNED' if status=='full_bundle' else 'REACHED_WRITE_SINK_NO_WRITE')
        if status=='full_bundle':assert result['return_value']['idempotent'] is True
    else:
        assert result['outcome']=='REJECTED'
        assert 'evidence.out' in result['reason']
        if mode in ('missing','invalid'):assert '미결속' in result['reason']
    result['fixture_bytes_unchanged']=True;results.append(result)
for name,status,mode in [('A00','preservation_pending','match'),('A01','preservation_pending','wrong'),
    ('A02','preservation_pending','missing'),('A03','full_bundle','match'),('A04','full_bundle','wrong'),('A05','full_bundle','missing')]:check(name,status,mode)
for status in ('preservation_pending','full_bundle'):
    for i,value in enumerate(['','   ',17,['results/L']]):check(f'A02b_{status}_{i}',status,'invalid',value)
check('A06_missing_out_different_receipt','full_bundle','missing',other=True)
check('A07_actual_historical_copy','full_bundle','missing',real=True)
report={'scope':'Exact selected helpers and attach AST body, inert lock/entry collaborators and blocked write sink. Not full Linux attach/pytest/OS concurrency validation.',
    'source_sha256':hashlib.sha256(raw).hexdigest(),
    'selected_definitions':[{'name':n.name,'line':n.lineno,'end_line':n.end_lineno} for n in selected if hasattr(n,'name')],
    'real_receipt_reader_and_bundle_control':'ACCEPTED','actual_bundle_index_members':len(mapping),'actual_bundle_set_size_sha_agree':True,
    'attach_cases':results,'case_count':len(results),
    'stubs':['check_id','read_verification_receipt (real control checked separately)','_verify_declared_bundle (bytes checked independently)','canonical_ledger','_ledger_lock','bundle_content_id','_atomic_write_text (raises before writing)','src.io.source_digest (independent measured value)'],
    'project_module_imports':0,'subject_ledger_writes':0,'restores':0,'class_changes':0,'scientific_COMSOL_runs':0}
with (O/'RECEIVER_CHECKS.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'real_control':'ACCEPTED','case_count':len(results),'cases':[{k:r[k] for k in ('id','outcome','fixture_bytes_unchanged')} for r in results],'subject_writes':0},ensure_ascii=False))
