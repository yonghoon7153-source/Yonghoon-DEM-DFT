"""Data-only prior-package, registry, plan and source evidence checks."""
from pathlib import Path
import ast, hashlib, io, json, zipfile
import yaml
OUT=Path(__file__).resolve().parent
BASE=OUT.parent
DD=Path('C:/Users/Administrator/Documents/Codex/g72_20260925/degradation-degeneracy')
OLD=Path('C:/Users/Administrator/Documents/Codex/g71_20260925/degradation-degeneracy')
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
prior=BASE/'gate71_review_20260925/GATE71_REVIEW_20260925.zip'
sent=DD/'docs/22p_gap/gate71_review/e65ab85f-GATE71_REVIEW_20260925.zip'
assert prior.read_bytes()==sent.read_bytes()
manifest=yaml.safe_load((DD/'docs/22p_gap/gate71_review/codex/MANIFEST.json').read_bytes())
for row in manifest['payload']:
    p=DD/'docs/22p_gap/gate71_review/codex'/row['path']
    assert ident(p.read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']}
with zipfile.ZipFile(io.BytesIO(sent.read_bytes())) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))
oldreg={p.name:ident(p.read_bytes()) for p in (OLD/'docs/22p_gap/_exec_class').glob('*.json')}
newreg={p.name:ident(p.read_bytes()) for p in (DD/'docs/22p_gap/_exec_class').glob('*.json')}
assert oldreg==newreg and len(newreg)==367
ledger=yaml.safe_load((DD/'docs/22p_gap/LEG_PRESERVATION.yaml').read_bytes())
def find_values(obj,target,where='$'):
    out=[]
    if isinstance(obj,dict):
        for k,v in obj.items():out.extend(find_values(v,target,where+'.'+str(k)))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):out.extend(find_values(v,target,where+f'[{i}]'))
    elif obj==target:out.append(where)
    return out
target_mentions=find_values(ledger,'grid_fit_v5')
assert not target_mentions
tests=ast.parse((DD/'tests/test_gate71_defensive.py').read_bytes())
test_nodes=[{'name':n.name,'line':n.lineno} for n in tests.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
assert len(test_nodes)==14
full=[]
for leg in ledger['legs']:
    if leg.get('preservation_status')=='full_bundle':
        full.append({'leg_id':leg['leg_id'],'out_present':'out' in leg.get('evidence',{}),'out':leg.get('evidence',{}).get('out'),
                     'receipt':leg.get('evidence',{}).get('verification_receipt')})
report={'prior_g71_zip_byte_identical':ident(sent.read_bytes()),'prior_manifest_verified_payloads':len(manifest['payload']),
        'registry_367_current_equals_g71_bytes':True,'grid_fit_v5_exact_ledger_values':target_mentions,
        'interpretation':'No prospective grid_fit_v5 entry observed; not authorizing plan creation',
        'new_test_definitions_static_count':len(test_nodes),'new_test_definitions':test_nodes,
        'actual_existing_full_bundle_ledger_observations':full,'tests_run':0,'restores':0,'class_changes':0}
(OUT/'DATA_AUDIT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
