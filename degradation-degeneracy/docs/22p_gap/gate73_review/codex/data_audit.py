"""Data-only prior package, registry, plan, mutation and structural-scan audit."""
from pathlib import Path
import ast,hashlib,json,sys,zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'work/gate26-pydeps'))
import yaml
O=Path(__file__).resolve().parent
DD=Path('C:/Users/Administrator/Documents/Codex/g73_20260925/degradation-degeneracy')
OLD=Path('C:/Users/Administrator/Documents/Codex/g72_20260925/degradation-degeneracy')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
prior=O.parent/'gate72_review_20260925/GATE72_REVIEW_20260925.zip'
sent=DD/'docs/22p_gap/gate72_review/f8ca8174-GATE72_REVIEW_20260925.zip'
assert prior.read_bytes()==sent.read_bytes()
assert ident(sent.read_bytes())['sha256']=='9ae5356c96e26de3f2cc87ff521337e7c67b58e67951f1d8030bdc0a5df59d91'
root=DD/'docs/22p_gap/gate72_review/codex'
m=json.loads((root/'MANIFEST.json').read_bytes())
assert m['payload_count']==len(m['files'])==48
with zipfile.ZipFile(sent) as z:
    assert z.testzip() is None and len(z.namelist())==len(set(z.namelist()))==49
    assert set(z.namelist())==set(m['files'])|{'MANIFEST.json'}
    assert z.read('MANIFEST.json')==(root/'MANIFEST.json').read_bytes()
    for name,row in m['files'].items():
        assert ident((root/name).read_bytes())==row
        assert z.read(name)==(root/name).read_bytes()
oldreg={p.name:ident(p.read_bytes()) for p in (OLD/'docs/22p_gap/_exec_class').glob('*.json')}
newreg={p.name:ident(p.read_bytes()) for p in (DD/'docs/22p_gap/_exec_class').glob('*.json')}
assert oldreg==newreg and len(newreg)==367
ledger=yaml.safe_load((DD/'docs/22p_gap/LEG_PRESERVATION.yaml').read_bytes())
def mentions(v):
    if isinstance(v,dict):return sum((mentions(x) for x in v.values()),0)
    if isinstance(v,list):return sum((mentions(x) for x in v),0)
    return int(v=='grid_fit_v5')
assert mentions(ledger)==0
hist=next(e for e in ledger['legs'] if e['leg_id']=='paired_fixed5_v4')
assert 'out' not in hist['evidence'] and hist['preservation_status']=='full_bundle'
oldledger=yaml.safe_load((OLD/'docs/22p_gap/LEG_PRESERVATION.yaml').read_bytes())
# Only the declared receipt core and validator identity are updated, not out/class.
oldhist=next(e for e in oldledger['legs'] if e['leg_id']=='paired_fixed5_v4')
oldhist['evidence']['verification_receipt_core_sha256']=hist['evidence']['verification_receipt_core_sha256']
oldhist['evidence']['validator_identity']['source_digest']=hist['evidence']['validator_identity']['source_digest']
assert oldledger==ledger
excluded=[];scanned=[];bad=[];parse_errors=[]
for py in sorted(DD.rglob('*.py')):
    if '__pycache__' in str(py) or py.name.startswith('test_'):continue
    rel=py.relative_to(DD).as_posix()
    if rel=='tools/preserve.py':continue
    if rel.startswith('docs/22p_gap/gate') and '_review/' in rel:
        assert rel.split('/')[0] not in ('src','tools','configs','scripts')
        excluded.append(rel);continue
    scanned.append(rel)
    try:tree=ast.parse(py.read_bytes(),filename=str(py))
    except (SyntaxError,UnicodeDecodeError) as exc:parse_errors.append({'path':rel,'error':str(exc)});continue
    for n in ast.walk(tree):
        if isinstance(n,ast.Call):
            fn=n.func;name=fn.id if isinstance(fn,ast.Name) else fn.attr if isinstance(fn,ast.Attribute) else None
            if name=='_record_execution_class':bad.append({'path':rel,'line':n.lineno})
        elif isinstance(n,ast.ImportFrom):
            if any(a.name=='_record_execution_class' for a in n.names):bad.append({'path':rel,'line':n.lineno})
assert not bad
assert 'docs/22p_gap/gate72_review/codex/reference/tools/preserve.py' in excluded
tests=ast.parse((DD/'tests/test_gate72_defensive.py').read_bytes())
defs=[n for n in tests.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
assert len(defs)==7
new_count=0
for n in defs:
    factor=1
    for d in n.decorator_list:
        if isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and d.func.attr=='parametrize':factor=len(ast.literal_eval(d.args[1]))
    new_count+=factor
assert new_count==10
mutation=(DD/'docs/22p_gap/mutation_replay.py').read_text(encoding='utf-8')
source=(DD/'tools/preserve.py').read_text(encoding='utf-8')
mt=ast.parse(mutation);mutations=[]
wanted={'attach-binds-the-ledger-run-location-g71','ledger-run-location-is-mandatory-g72'}
for n in ast.walk(mt):
    if isinstance(n,ast.Tuple) and len(n.elts)==5 and isinstance(n.elts[0],ast.Constant) and n.elts[0].value in wanted:
        name=ast.literal_eval(n.elts[0]);pre=ast.literal_eval(n.elts[2]);post=ast.literal_eval(n.elts[3]);selector=ast.literal_eval(n.elts[4])
        assert source.count(pre)==1
        mutations.append({'id':name,'line':n.lineno,'preimage_occurrences':1,'preimage':pre,'replacement':post,'test_selector':selector})
assert len(mutations)==2
report={'prior_g72_raw_zip_identical':ident(sent.read_bytes()),'repository_filename_prefix_is_not_sha':sent.name,
 'prior_payload_bytes_verified':48,'registry_367_equals_prior_bytes':True,
 'grid_fit_v5_exact_ledger_mentions':0,'historical_full_bundle_out_absent':True,
 'ledger_changes_limited_to_reported_receipt_and_validator':True,
 'structural_scan':{'scope':'Independent AST data scan, not subject pytest function execution','newly_excluded':excluded,
    'scanned_files':scanned,'bad_raw_sink_calls':bad,'parse_errors':parse_errors,'new_skip_intersects_RUN_SCOPE':False},
 'new_static_test_function_count':len(defs),'new_static_parametrized_node_count':new_count,
 'new_test_definitions':[{'name':n.name,'line':n.lineno} for n in defs],
 'mutation_preimages':mutations,'mutation_replay_executed':False,
 'interpretation':'g72 mutation replaces validation with False and some failures are unexpected TypeError, not accepted bad ledgers; evidence is limited accordingly.',
 'full_pytest_smoke_main_restore_class_execution':0}
with (O/'DATA_AUDIT.json').open('x',encoding='utf-8') as f:json.dump(report,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'prior_payload':48,'registry':367,'prospective':0,'structural_scanned':len(scanned),'review_copies_excluded':len(excluded),'bad_calls':bad,'parse_errors':parse_errors,'new_test_nodes':new_count,'mutation_preimages':len(mutations)},ensure_ascii=False))
