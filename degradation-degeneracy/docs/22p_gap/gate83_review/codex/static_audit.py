"""Reviewer-owned data/AST audit; no imports or execution of repository code."""
import ast
import difflib
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'gate82_review_20260930'
REF = HERE / 'reference'
E = HERE / 'evidence'
checks = []

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def check(name, ok):
    checks.append({'check':name, 'pass':bool(ok)})
    assert ok, name

def dump(n, d):
    (HERE/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Mechanical materialization from connector-returned bytes, not a source edit.
reference = []
for p in sorted(E.glob('*.json')):
    d = read(p)
    if not isinstance(d,dict) or not isinstance(d.get('content'),str) or not d.get('sha'):
        continue
    b = d['content'].encode('utf-8')
    check('remote Git blob '+p.name, blob(b)==d['sha'])
    if p.name.startswith(('docs_', 'src_', 'tools_', 'tests_')):
        # Full repository path is absent from some connector responses.
        key = p.stem
        candidates = [x for x in REF.rglob('*') if x.is_file() and x.relative_to(REF).as_posix().replace('/','_')==key]
        check('one inert reference path '+p.name, len(candidates)==1)
        dest = candidates[0]
        dest.write_bytes(b)
        reference.append({'path':dest.relative_to(REF).as_posix(),'bytes':len(b),'sha256':sha(b),'git_blob_sha1':d['sha']})

scope = {}
for p in sorted((E/'target_scope').glob('*.json')):
    d=read(p); b=d['content'].encode('utf-8')
    rel=d['path'].removeprefix('degradation-degeneracy/')
    check('scope blob '+rel,blob(b)==d['sha'])
    scope[rel]=(b,d['sha'])
    dest=REF/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
tree = read(E/'SCOPE_TREE_INVENTORY.json')
check('all four recursive scope trees untruncated',len(tree['trees'])==4 and all(x['truncated'] is False for x in tree['trees']))
inventory={x['path'].removeprefix('degradation-degeneracy/'):x for x in tree['scope_blobs']}
check('scope inventory exact58',set(inventory)==set(scope) and len(scope)==58)
for rel,(_,gitsha) in scope.items():
    check('tree blob binding '+rel,inventory[rel]['sha']==gitsha and inventory[rel].get('mode','100644') in ['100644','100755'])
h=hashlib.sha256()
for rel,(b,_) in sorted(scope.items()):
    h.update(rel.encode('utf-8')); h.update(b)
digest=h.hexdigest()[:16]
check('source digest recomputed',digest=='7187bd31740514d4')
prior={d['path'].removeprefix('degradation-degeneracy/'):d for d in read(OLD/'IDENTITY_AUDIT.json')['files']}
changed=[rel for rel,(b,_) in scope.items() if sha(b)!=prior[rel]['sha256']]
check('only four known production files changed',set(changed)=={'src/fitting.py','src/io.py','tools/design_wire.py','tools/preserve.py'})
compare=read(E/'TARGET_TO_SEND_HEAD.json')
check('target ancestor of request head',compare['merge_base_commit']['sha']=='ea2af59e68a85b561c3e185f66b815aec877ca57' and compare['ahead_by']==1 and compare['behind_by']==0)
check('target to send only three docs',len(compare['files'])==3 and all(x['filename'].startswith('degradation-degeneracy/docs/') for x in compare['files']))
def scoped_comparison_files(d):
    return {x['filename'].removeprefix('degradation-degeneracy/') for x in d['files']
            if x['filename'].startswith('degradation-degeneracy/') and
            (x['filename'].removeprefix('degradation-degeneracy/').startswith(('src/','tools/','configs/','scripts/')) or
             re.fullmatch(r'degradation-degeneracy/(run\.sh|requirements[^/]*\.txt)',x['filename']))}
for key in ['PRIOR_TO_RED','GREEN_TO_TARGET']:
    comp=read(E/(key+'.json'))
    check('comparison complete-sized and no scope change '+key,len(comp['files'])<300 and scoped_comparison_files(comp)==set())
green=read(E/'RED_TO_GREEN.json')
check('one GREEN commit four production paths',green['total_commits']==1 and scoped_comparison_files(green)==set(changed))

diffs={}; function_changes={}
def defs(text):
    t=ast.parse(text)
    return {n.name:n for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef))}
def body(text,name):
    n=defs(text)[name]
    return '\n'.join(text.splitlines()[n.lineno-1:n.end_lineno])
for rel in changed:
    old=(OLD/'reference'/rel).read_text(encoding='utf-8'); new=scope[rel][0].decode()
    diffs[rel]=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='G82/'+rel,tofile='G83/'+rel))
    a,b=defs(old),defs(new)
    function_changes[rel]={'added':sorted(set(b)-set(a)),'removed':sorted(set(a)-set(b)),
        'modified':sorted(n for n in set(a)&set(b) if ast.dump(a[n],include_attributes=False)!=ast.dump(b[n],include_attributes=False))}
(HERE/'PRODUCTION_DIFF.patch').write_text(''.join(diffs.values()),encoding='utf-8')
check('fitting changes only preparation writer callsite',function_changes['src/fitting.py']=={'added':[],'removed':[],'modified':['_prepare_stage3','_run_fit_locked','write_execution_record']})
check('io changes only roster and stage3 checks',function_changes['src/io.py']=={'added':['_sealed_curves_snapshot','observed_roster'],'removed':[],'modified':['_stage3_checks','_stage3_rederive']})
check('profile helper only new design function',function_changes['tools/design_wire.py']=={'added':['check_bank_profile'],'removed':[],'modified':[]})
check('preserve only envelope profile validation',function_changes['tools/preserve.py']=={'added':[],'removed':[],'modified':['check_envelope_v4']})
unchanged_functions=[]
for rel,names in {
 'src/fitting.py':['fit','_minimize_until_stable','_fit_candidates','normalize_restart_record','make_solution_map','provider_x0'],
 'tools/design_wire.py':['_check_design_nested','pairing_design_sha256','_bank_seed','unit_cube_bank','bank_bytes','pair_group_id','bank_id','candidate_id','roster_from_conditions'],
 'tools/preserve.py':['check_envelope','check_execution_record','run_transaction'],
 'src/io.py':['realized_from_fits','_restart_ok','_restart_ok_v6']}.items():
    old=(OLD/'reference'/rel).read_text(encoding='utf-8');new=scope[rel][0].decode()
    for name in names:
        check('unchanged function '+name,body(old,name)==body(new,name));unchanged_functions.append(rel+'::'+name)
check('spec fixed before code unchanged',read(E/'SPEC_BEFORE_CODE.json')['content']==(REF/'docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md').read_text(encoding='utf-8'))
check('received prior report equals local prior report',read(E/'PRIOR_REVIEW_REMOTE.json')['content'].encode()==(OLD/'REVIEW_KO.md').read_bytes())
check('received prior manifest equals original manifest',read(E/'PRIOR_MANIFEST_REMOTE.json')['content'].encode()==(OLD/'PACKAGE_MANIFEST.json').read_bytes())

# Inspect regression assertions and mutation literals as AST data, never run tests.
tests=(REF/'tests/test_gate82_residuals.py').read_text(encoding='utf-8')
tt=ast.parse(tests); testdefs=[x for x in tt.body if isinstance(x,ast.FunctionDef) and x.name.startswith('test_')]
nodes=[]
for f in testdefs:
    n=1
    for dec in f.decorator_list:
        if isinstance(dec,ast.Call) and isinstance(dec.func,ast.Attribute) and dec.func.attr=='parametrize':
            n*=len(ast.literal_eval(dec.args[1]))
    nodes.append({'function':f.name,'line':f.lineno,'declared_nodes':n,'assertions':sum(isinstance(x,ast.Assert) for x in ast.walk(f))})
check('19 statically declared test nodes',sum(x['declared_nodes'] for x in nodes)==19)
mutation=(REF/'docs/22p_gap/mutation_replay.py').read_text(encoding='utf-8')
mt=ast.parse(mutation); maps={'IO':'src/io.py','FITTING':'src/fitting.py','DW':'tools/design_wire.py','PRESERVE':'tools/preserve.py'}
mutants=[];expect={}
for n in ast.walk(mt):
    if isinstance(n,ast.Tuple) and len(n.elts)==5 and isinstance(n.elts[0],ast.Constant) and isinstance(n.elts[0].value,str) and n.elts[0].value.endswith('-g82'):
        name=n.elts[0].value;path=maps[n.elts[1].id];pre=ast.literal_eval(n.elts[2]);replacement=ast.literal_eval(n.elts[3]);selector=ast.literal_eval(n.elts[4])
        count=scope[path][0].decode().count(pre)
        check('single static preimage '+name,count==1)
        mutants.append({'id':name,'path':path,'registration_line':n.lineno,'preimage_count':count,'selector':selector,'preimage':pre,'replacement':replacement})
    if isinstance(n,ast.Dict):
        for k,v in zip(n.keys,n.values):
            if isinstance(k,ast.Constant) and isinstance(k.value,str) and k.value.endswith('-g82'):
                expect[k.value]=ast.literal_eval(v)
check('12 registered mutations and expectations',len(mutants)==12 and {m['id'] for m in mutants}==set(expect))
red=read(E/'RED_TEST_SOURCE.json')['content']
(HERE/'RED_TO_GREEN_TEST_DIFF.patch').write_text(''.join(difflib.unified_diff(red.splitlines(True),tests.splitlines(True),fromfile='RED/tests',tofile='GREEN/tests')),encoding='utf-8')

def scalar(text,key):
    v=re.findall(r'^\s*'+re.escape(key)+r': (.*)$',text,re.M)
    assert len(v)==1,(key,v)
    return v[0]

def stable_receipt(text):
    core=text.split('\nstamp:\n')[0]
    drop={'core_sha256','validator_source_digest','src_io_sha256'}
    return '\n'.join(x for x in core.splitlines() if x.strip().split(':',1)[0] not in drop)

receipts=[]
ledger=(REF/'docs/22p_gap/LEG_PRESERVATION.yaml').read_text(encoding='utf-8')
for leg,nchecks in [('paired_fixed5_v4',35),('grid_fit_v5',34)]:
    p=REF/f'docs/22p_gap/receipts/{leg}.validate.yaml'
    hist=REF/f'docs/22p_gap/receipts/history/{leg}.validate.02a776a7a0a3f4ba.yaml'
    before=(OLD/f'reference/docs/22p_gap/receipts/{leg}.validate.yaml').read_bytes()
    after=p.read_bytes();s=after.decode();old=before.decode()
    check('old receipt byte-preserved '+leg,hist.read_bytes()==before)
    check('receipt stable core text '+leg,stable_receipt(old)==stable_receipt(s))
    check('receipt validator identity '+leg,scalar(s,'validator_source_digest')==digest and scalar(s,'src_io_sha256')==sha(scope['src/io.py'][0])[:16])
    check('unchanged receipt check count '+leg,scalar(s,'n_checks')==str(nchecks)==scalar(old,'n_checks'))
    core=scalar(s,'core_sha256')
    # Locate the leg entry, not a cohort mention.
    legs_text=ledger.split('\nlegs:\n',1)[1]
    start=legs_text.index('- leg_id: '+leg+'\n');tail=legs_text[start:];block=tail.split('\n- leg_id:',1)[0]
    check('ledger current receipt core '+leg,'verification_receipt_core_sha256: '+core in block)
    check('ledger current validator digest '+leg,'source_digest: '+digest in block)
    receipts.append({'leg':leg,'prior_bytes':len(before),'prior_sha256':sha(before),'history_bytes_equal':True,
     'new_bytes':len(after),'new_sha256':sha(after),'old_core_sha256':scalar(old,'core_sha256'),'new_core_sha256':core,
     'old_validator':scalar(old,'validator_source_digest'),'new_validator':digest,'checks':nchecks,
     'stamp_tree_dirty':scalar(s,'validator_tree_dirty'),'changed_fields':['core_sha256','core.identity.validator_source_digest','core.identity.src_io_sha256','stamp'],
     'method':'Text comparison with three explicit changing keys and stamp separated. No receipt canonicalizer or restore execution.'})
oldledger=(OLD/'reference/docs/22p_gap/LEG_PRESERVATION.yaml').read_text(encoding='utf-8')
ldiff=list(difflib.unified_diff(oldledger.splitlines(True),ledger.splitlines(True),fromfile='G82/ledger',tofile='G83/ledger'))
edits=[s for s in ldiff if s.startswith(('+','-')) and not s.startswith(('+++','---'))]
check('ledger changes only 2 fields for2legs',len(edits)==8 and all('verification_receipt_core_sha256:' in s or 'source_digest:' in s for s in edits))
(HERE/'LEDGER_DIFF.patch').write_text(''.join(ldiff),encoding='utf-8')

dump('IDENTITY_AUDIT.json',{'mode':'Read-only GitHub bytes and reviewer-owned hashing/AST; received code never executed',
 'code_target':'ea2af59e68a85b561c3e185f66b815aec877ca57','send_head':'78e1f518024d0a9c4d00ee7f6784fa8949554325',
 'source_digest':digest,'scope_files':len(scope),'scope_inventory':'Complete four recursive scoped Git trees and root run/requirements at target; no remote working-tree observation',
 'changed_files':sorted(changed),'scope':[{'path':k,'bytes':len(b),'sha256':sha(b),'git_blob_sha1':g} for k,(b,g) in sorted(scope.items())],
 'references':reference,'target_send_diff':compare['files']})
dump('STATIC_AUDIT.json',{'status':'PASS','checks':checks,'function_changes':function_changes,'unchanged_selected_functions':unchanged_functions,
 'test_nodes':nodes,'test_node_count':sum(x['declared_nodes'] for x in nodes),'mutations':mutants,'sender_recorded_expectations':expect,
 'execution_limit':'Static reason/branch/definition review only; 19 tests, 12 mutations and full suite not executed by reviewer.'})
dump('RECEIPT_AUDIT.json',{'status':'PASS','receipts':receipts,'ledger_edits':edits,'canonicalizer_or_restore_runs':0})
print(json.dumps({'status':'PASS','checks':len(checks),'digest':digest,'scope_files':len(scope),'tests_declared':sum(x['declared_nodes'] for x in nodes),'mutations_statically_inspected':len(mutants),'receipt_legs':len(receipts)}))
