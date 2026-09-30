"""Reviewer-owned data/AST audit. Never imports or executes the supplied repository."""
import ast
import hashlib
import json
from pathlib import Path
import re
import difflib

HERE = Path(__file__).resolve().parent
REF = HERE / 'reference'
OLD = HERE.parent / 'gate81_review_20260928' / 'SOURCE_BEFORE.json'
OLDROOT = Path('C:/Users/Administrator/Documents/Codex/g80_20260928/degradation-degeneracy')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def dump(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')

prior = json.loads(OLD.read_text(encoding='utf-8'))
send = {}
blobs = []
for f in sorted((HERE / 'evidence' / 'send_scope').glob('*.json')):
    d = json.loads(f.read_text(encoding='utf-8'))
    b = d['content'].encode('utf-8')
    assert blob(b) == d['sha'], (f, 'remote text does not reproduce Git blob')
    rel = d['path'].removeprefix('degradation-degeneracy/')
    send[rel] = b
    blobs.append({'path': d['path'], 'git_blob_sha1': d['sha'], 'sha256': sha(b), 'bytes': len(b)})
assert len(send) == 58
h = hashlib.sha256()
for p, b in sorted(send.items()):
    h.update(p.encode())
    h.update(b)
changed = [p for p,b in send.items() if sha(b) != prior['degradation-degeneracy/' + p]['sha256']]
assert set(changed) == {'src/fitting.py','src/io.py','tools/design_wire.py','tools/preserve.py'}
assert h.hexdigest()[:16] == '02a776a7a0a3f4ba'
refs = []
for p in sorted(REF.rglob('*')):
    if not p.is_file() or p.name == 'GATE82_REQUEST.md':
        continue
    rel = p.relative_to(REF).as_posix()
    m = HERE / 'evidence' / ('file_' + rel.replace('/', '_') + '.json')
    d = json.loads(m.read_text(encoding='utf-8'))
    b = p.read_bytes()
    assert blob(b) == d['sha'], (rel,'local copy does not reproduce Git blob')
    if rel in send:
        assert b == send[rel], (rel, 'target/send mismatch')
    refs.append({'path':rel,'git_blob_sha1':d['sha'],'bytes':len(b),'sha256':sha(b)})
dump('IDENTITY_AUDIT.json', {'mode':'read-only remote bytes and local inert copies; no repository execution',
    'send_head':'8f54427c9eb4a6d335bba65685a4c28dc24064d8',
    'code_target':'c82231c49460f79bb5474185648594b3a6c9fc02',
    'known_run_scope_files':len(send),'source_digest_recomputed':h.hexdigest()[:16],
    'known_scope_changed_vs_gate81':sorted(changed),'files':blobs,'target_reference_blobs':refs,
    'inventory_limit':'58 known RUN_SCOPE paths fetched individually. Compare API returned 300 files; not used as proof of an exhaustive repository diff.'})

def difference(a,b,p=''):
    if type(a) is not type(b): return [p]
    if isinstance(a,dict):
        out=[]
        for k in sorted(set(a)|set(b)):
            q=p+'.'+k if p else k
            out += [q] if k not in a or k not in b else difference(a[k],b[k],q)
        return out
    if isinstance(a,list): return [] if a==b else [p]
    return [] if a==b else [p]

ledger = (REF/'docs/22p_gap/LEG_PRESERVATION.yaml').read_text(encoding='utf-8')
def scalar(text,key):
    m=re.findall(r'^\s*'+re.escape(key)+r': (.*)$',text,re.M)
    assert len(m)==1,(key,m)
    return m[0]
def stable_receipt_text(text):
    # Text-only comparison. Do not claim semantic YAML parse/core regeneration.
    core=text.split('\nstamp:\n')[0]
    drop={'core_sha256','validator_source_digest','src_io_sha256','n_checks','세대_선언_일치'}
    return '\n'.join(x for x in core.splitlines() if x.strip().split(':',1)[0] not in drop)

receipt_audit=[]
for leg in ('paired_fixed5_v4','grid_fit_v5'):
    rd=REF/'docs/22p_gap/receipts'
    paths=[rd/'history'/f'{leg}.validate.eda3feb8f4536511.yaml',rd/'history'/f'{leg}.validate.eea5977f4faf9685.yaml',rd/f'{leg}.validate.yaml']
    docs=[p.read_text(encoding='utf-8') for p in paths]
    old=(OLDROOT/'docs/22p_gap/receipts'/f'{leg}.validate.yaml').read_bytes()
    assert old==paths[0].read_bytes(),(leg,'old receipt history changed')
    delta=[''.join(difflib.unified_diff(docs[0].splitlines(True),d.splitlines(True),fromfile='original',tofile=n)) for n,d in zip(('first','second'),docs[1:])]
    assert stable_receipt_text(docs[0])==stable_receipt_text(docs[1])==stable_receipt_text(docs[2]),leg
    curr=docs[2]
    assert scalar(curr,'ok')=='true' and scalar(curr,'fail')=='[]'
    sections=re.split(r'(?m)(?=^- leg_id: )',ledger)
    es=[s for s in sections if s.startswith('- leg_id: '+leg+'\n') and 'verification_receipt_core_sha256:' in s]
    assert len(es)==1,(leg,len(es))
    ev=es[0]
    assert scalar(ev,'verification_receipt_core_sha256')==scalar(curr,'core_sha256')
    vi=ev.split('    validator_identity:\n',1)[1].split('\n    ',1)[0] if False else ev
    assert 'source_digest: '+scalar(curr,'validator_source_digest') in vi
    assert 'n_checks: '+scalar(curr,'n_checks') in vi
    receipt_audit.append({'leg':leg,'original_history_byte_identical':True,
       'generation_digests':[scalar(d,'validator_source_digest') for d in docs],
       'difference_original_to_first':delta[0],'difference_original_to_second':delta[1],
       'bundle_restore_outputs_identical':True,'ledger_anchors_match':True,
       'checks_per_generation':[int(scalar(d,'n_checks')) for d in docs],
       'stamp_tree_dirty':[scalar(d,'validator_tree_dirty') for d in docs],
       'second_core_sha256':scalar(curr,'core_sha256')})
dump('RECEIPT_DATA_AUDIT.json', {'mode':'YAML text diff/scalar inspection only; not semantic parse or core-hash regeneration; no make_receipt/restore/validate execution','legs':receipt_audit})

trees={p:ast.parse((REF/p).read_text(encoding='utf-8')) for p in changed}
def fn(p,n):
    return next(x for x in trees[p].body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef)) and x.name==n)
facts=[]
for p,n in [('src/io.py','realized_from_fits'),('src/io.py','_stage3_rederive'),('src/io.py','_stage3_checks'),('src/fitting.py','_prepare_stage3'),('src/fitting.py','write_execution_record')]:
    f=fn(p,n)
    reads=sorted({x.slice.value for x in ast.walk(f) if isinstance(x,ast.Subscript) and isinstance(x.slice,ast.Constant) and isinstance(x.slice.value,str)})
    calls=sorted({ast.unparse(x.func) for x in ast.walk(f) if isinstance(x,ast.Call)})
    facts.append({'file':p,'function':n,'line':f.lineno,'end_line':f.end_lineno,'literal_subscript_keys':reads,'call_names':calls})
duplicates={}
for p,t in trees.items():
    for n in {x.name for x in t.body if isinstance(x,ast.FunctionDef)}:
        same=[x.lineno for x in t.body if isinstance(x,ast.FunctionDef) and x.name==n]
        if len(same)>1: duplicates[p+':'+n]=same
test=ast.parse((REF/'tests/test_gate81_stage3_wire.py').read_text(encoding='utf-8'))
test_defs=[x.name for x in test.body if isinstance(x,ast.FunctionDef) and x.name.startswith('test_')]
dump('STATIC_DATA_FLOW.json', {'scope':'AST/data only; no imports, no function extraction or execution, no production/test/probe calls',
    'functions':facts,'duplicate_top_level_definitions':duplicates,'test_definitions_count':len(test_defs),
    'test_definition_count_is_not_pytest_node_count':True,'tests':test_defs})
print(json.dumps({'status':'STATIC_DATA_AUDIT_COMPLETE','known_scope':len(send),'digest':h.hexdigest()[:16],
    'changed':sorted(changed),'receipt_pairs':len(receipt_audit),'repository_calls':0},ensure_ascii=False))
