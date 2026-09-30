"""Reviewer-owned byte/AST/data audit. Never imports or runs received programs."""
import ast
import difflib
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
E, REF = HERE / 'evidence', HERE / 'reference'
OLD = HERE.parent / 'gate84_review_20260930'
HEAD = 'b49c24fabe94be7a5986bdc54de2d4278c4ebf65'
TARGET = 'f89b1401fb1ab21371bd7755289e64281681b5be'
checks = []

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def gitsha(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def check(name, ok):
    checks.append({'check': name, 'pass': bool(ok)})
    if not ok:
        raise AssertionError(name)

def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

before = {p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
refs = []
for p in sorted(E.glob('*.json')):
    d = read(p)
    if not isinstance(d, dict) or not isinstance(d.get('content'), str) or not d.get('sha'):
        continue
    b = d['content'].encode('utf-8')
    check('Git blob ' + p.name, gitsha('blob', b) == d['sha'])
    if '__' in p.stem:
        rel = p.stem.replace('__', '/')
        check('Pinned HEAD ' + rel, '/' + HEAD + '/' in d['display_url'])
    elif p.stem == 'receiptcode':
        rel = d['requested_path']
    else:
        rel = 'before_test_fixes/' + p.stem + '.py'
    dest = REF / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Mechanical exact-byte materialization, not editing the production source.
    dest.write_bytes(b)
    refs.append({'path':rel, 'bytes':len(b), 'sha256':sha(b), 'git_blob_sha1':d['sha'], 'url':d['display_url']})

head_entries = {x['name']:x for x in json.loads(read(E/'HEAD_DIRECTORY.json')['content'])}
prior_tree=read(HERE.parent/'gate83_review_20260930/evidence/SCOPE_TREE_INVENTORY.json')
mode_map={t['dir']+'/'+x['path']:x['mode'].lstrip('0') for t in prior_tree['trees'] for x in t['tree'] if x['type']=='blob'}
inventory = {}
for directory in ['src', 'tools', 'configs', 'scripts']:
    entries = json.loads(read(E / ('DIR_' + directory + '.json'))['content'])
    check('Flat complete directory ' + directory, all(x['type'] == 'file' for x in entries))
    body = b''.join((mode_map[directory+'/'+x['name']]+' '+x['name']).encode() + b'\0' + bytes.fromhex(x['sha']) for x in sorted(entries, key=lambda x:x['name'].encode()))
    check('Reconstructed Git tree ' + directory, gitsha('tree', body) == head_entries[directory]['sha'])
    inventory.update({directory+'/'+x['name']:x['sha'] for x in entries})
for name in ['run.sh', 'requirements.txt', 'requirements-gpu.txt']:
    inventory[name] = head_entries[name]['sha']
scope = {}
changed = []
for rel, blobsha in sorted(inventory.items()):
    old = (OLD/'reference'/rel).read_bytes()
    b = (REF/rel).read_bytes() if rel in ['src/fitting.py', 'src/io.py', 'tools/preserve.py'] else old
    check('Current scope blob ' + rel, gitsha('blob',b) == blobsha)
    if b != old:
        changed.append(rel)
    dest = REF/rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)
    scope[rel] = b
check('Exact RUN_SCOPE 58 files', len(scope) == 58)
check('Exactly three changed production files', changed == ['src/fitting.py','src/io.py','tools/preserve.py'])
h = hashlib.sha256()
for rel,b in sorted(scope.items()):
    h.update(rel.encode()); h.update(b)
check('Independent source_digest', h.hexdigest()[:16] == 'ba51cd20caa10b7b')

def in_scope(name):
    rel = name.removeprefix('degradation-degeneracy/')
    return rel in inventory

comp = read(E/'TARGET_COMPARE.json')
check('Target ancestry', comp['merge_base_commit']['sha'] == TARGET and comp['behind_by'] == 0)
check('Target to HEAD RUN_SCOPE diff zero', not any(in_scope(x['filename']) for x in comp['files']))
check('GREEN to target RUN_SCOPE diff zero', not any(in_scope(x['filename']) for x in read(E/'GREEN_TO_TARGET.json')['files']))
redgreen = [x for x in read(E/'RED_TO_GREEN.json')['files'] if in_scope(x['filename'])]
check('GREEN change counts', (sum(x['additions'] for x in redgreen),sum(x['deletions'] for x in redgreen)) == (167,40))
dump('SOURCE_IDENTITIES.json', {'request_head':HEAD,'code_target':TARGET,'source_digest':h.hexdigest()[:16], 'scope_count':len(scope),'scope':[{'path':k,'git_blob_sha1':inventory[k],'sha256':sha(v)} for k,v in scope.items()], 'changed':changed,'references':refs,'broad_compare_300_file_result_not_used':True})

for name in ['PACKAGE_MANIFEST.json','DECISION.json']:
    check('Prior Gate84 embedded identity ' + name, (REF/'docs/22p_gap/gate84_review/codex'/name).read_bytes() == (OLD/name).read_bytes())

trees = {rel:ast.parse(b.decode('utf-8')) for rel,b in scope.items() if rel.endswith('.py')}
def func(rel, name):
    return [x for x in trees[rel].body if isinstance(x,ast.FunctionDef) and x.name == name][-1]
def body(rel, name):
    n=func(rel,name)
    return '\n'.join(scope[rel].decode().splitlines()[n.lineno-1:n.end_lineno])
def ast_body(n):
    return ast.dump(n,include_attributes=False)

check('One active normalize definition',len([n for n in trees['src/fitting.py'].body if isinstance(n,ast.FunctionDef) and n.name=='normalize_restart_record'])==1)
numerical = []
oldtree=ast.parse((OLD/'reference/src/fitting.py').read_text(encoding='utf-8'))
for name in ['_minimize_until_stable','_fit_one','normalize_restart_record']:
    prior=[n for n in oldtree.body if isinstance(n,ast.FunctionDef) and n.name==name][-1]
    check('Unchanged active AST ' + name, ast_body(prior)==ast_body(func('src/fitting.py',name)))
    numerical.append(name)
locked=func('src/fitting.py','_run_fit_locked')
call_lines={name:sorted(n.lineno for n in ast.walk(locked) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==name) for name in ['_stage3_preflight','_fit_one','_prepare_stage3']}
check('Preflight lexical order before halfcell fit',call_lines['_stage3_preflight'][0] < call_lines['_fit_one'][0] < call_lines['_prepare_stage3'][0])
check('Legacy branch skips preflight', 'if stage3 is not None else None' in body('src/fitting.py','_run_fit_locked'))
check('Hex16 prefix of full closure', 'return closure_sha256_from_parts(_config_closure_parts(path, repo_root))[:16]' in body('src/fitting.py','_config_closure_digest'))
check('Preflight source/config/reference controls',all(x in body('src/fitting.py','_stage3_preflight') for x in ['if reference != "grid"','if env["source_digest"] != run_source_digest','if inp.get("reference") != reference','if want is None','if want != got']))
check('v2 finite/count separated','math.isfinite(float(_J))' in body('src/io.py','realized_from_fits') and 'e.get("converged") is True' in body('src/io.py','realized_from_fits'))

io=scope['src/io.py'].decode()
closure=io[io.index('    # ★ 84차 G84-N1 — base-config closure'):io.index('\ndef validate_provenance')]
check('Closure branch chooses submitted keys','keys = s3.get("base_config_closure_keys")' in closure)
check('Closure branch does not reconstruct dependency graph', not any(s in closure for s in ['config_dependencies(', 'get("base_config")', '["base_config"]','extends']))
test=(REF/'tests/test_gate84_round2a.py').read_text(encoding='utf-8')
testtree=ast.parse(test)
testnames=[n.name for n in testtree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
check('16 submitted new test nodes',len(testnames)==16)
dump('STATIC_SOURCE_FACTS.json',{'unchanged_active_AST':numerical,'call_lines':call_lines,'tests':testnames,'closure_recalculation_lines':[1949,1974],'closure_membership_not_reconstructed':True,'received_code_imported_or_executed':False})

mutation_tree=ast.parse((REF/'docs/22p_gap/mutation_replay.py').read_text(encoding='utf-8'))
mutations=[]
for n in ast.walk(mutation_tree):
    if isinstance(n,ast.Tuple) and len(n.elts)==5 and isinstance(n.elts[0],ast.Constant) and isinstance(n.elts[0].value,str) and n.elts[0].value.endswith('-g84'):
        name=n.elts[0].value
        rel={'FITTING':'src/fitting.py','IO':'src/io.py','PRESERVE':'tools/preserve.py'}[n.elts[1].id]
        preimage=ast.literal_eval(n.elts[2])
        occurrences=scope[rel].decode().count(preimage)
        check('g84 static preimage '+name,occurrences==1)
        mutations.append({'name':name,'file':rel,'preimage_count':occurrences,'registration_line':n.lineno})
check('Twelve new mutation definitions inspected',len(mutations)==12)
dump('MUTATION_REGISTRATION_STATIC.json',{'scope':'AST/literal and text occurrence only. No mutations applied or replayed; kill counts remain sender-reported.','mutations':mutations})

# Pure reviewer-owned arithmetic model; NOT a call of any production validator.
files={'configs/base.yaml':b'physics: fixed\n','configs/leaf.yaml':b'extends: base.yaml\nnote: leaf\n','configs/unrelated.yaml':b'note: not a parent\n'}
parts={k:sha(v) for k,v in files.items()}
def closure_hash(keys):
    return sha('\n'.join(k+'='+parts[k] for k in sorted(set(keys))).encode())
actual=['configs/base.yaml','configs/leaf.yaml']
cases=[]
for name,keys in [('positive',actual),('parent_omitted',['configs/leaf.yaml']),('leaf_omitted',['configs/base.yaml']),('extra_member',list(files)),('duplicate_member',actual+[actual[0]])]:
    calculated=closure_hash(keys)
    declared_plan=calculated
    declared_run=calculated
    cases.append({'name':name,'submitted_keys':keys,'calculated':calculated,'declared_plan':declared_plan,'declared_run':declared_run,'all_selected_snapshots_unchanged':True,'both_digest_equalities_hold':calculated==declared_plan==declared_run,'exact_unique_dependency_members':len(keys)==len(set(keys)) and set(keys)==set(actual),'actual_full_closure':closure_hash(actual)})
check('Model: omitted parent differs but submitted equalities hold', cases[1]['calculated']!=cases[1]['actual_full_closure'] and cases[1]['both_digest_equalities_hold'])
dump('CLOSURE_COUNTERMODEL.json',{'scope':'Reviewer-owned SHA/set arithmetic only. Models the local closure predicate, NOT full validate_provenance, fitting, restore or native execution. Full artifact reseal/validator reproduction was not run.','files':{k:{'utf8':v.decode(),'sha256':parts[k]} for k,v in files.items()},'actual_root':'configs/leaf.yaml','independently_defined_dependency_members':actual,'cases':cases})

changes=[]
for rel in changed:
    a=(OLD/'reference'/rel).read_text(encoding='utf-8').splitlines(True)
    b=scope[rel].decode().splitlines(True)
    changes += list(difflib.unified_diff(a,b,fromfile='gate84/'+rel,tofile=HEAD+'/'+rel))
(HERE/'PRODUCTION.diff').write_text(''.join(changes),encoding='utf-8')
fixdiff=[]
for key,rel in [('pre54','tests/test_docs_lint.py'),('pre59exec','tests/test_exec_class_capability_59.py'),('pre59handle','tests/test_handle_carry_59.py'),('pre61','tests/test_evidence_receipt_61.py')]:
    a=read(E/(key+'.json'))['content'].splitlines(True)
    b=(REF/rel).read_text(encoding='utf-8').splitlines(True)
    fixdiff += list(difflib.unified_diff(a,b,fromfile=key+'/'+rel,tofile=HEAD+'/'+rel))
(HERE/'HISTORICAL_TEST_FIXES.diff').write_text(''.join(fixdiff),encoding='utf-8')

receipts=[]
for leg,nchecks in [('paired_fixed5_v4',35),('grid_fit_v5',34)]:
    hist=REF/('docs/22p_gap/receipts/history/'+leg+'.validate.7187bd31740514d4.yaml')
    now=REF/('docs/22p_gap/receipts/'+leg+'.validate.yaml')
    old=OLD/'reference'/('docs/22p_gap/receipts/'+leg+'.validate.yaml')
    if not old.exists():
        old=HERE.parent/'gate83_review_20260930/reference'/('docs/22p_gap/receipts/'+leg+'.validate.yaml')
    check('Exact historical receipt '+leg,hist.read_bytes()==old.read_bytes())
    a=hist.read_text(encoding='utf-8')
    b=now.read_text(encoding='utf-8')
    def invariant_core(t):
        t=t.split('\ncore:\n',1)[1].split('\nstamp:\n',1)[0]
        return '\n'.join(line for line in t.splitlines() if not re.match(r'\s*(validator_source_digest|src_io_sha256):',line))
    def scalar(t,k):
        vals=re.findall(r'^\s*'+re.escape(k)+r':\s*(\S+)\s*$',t,re.M)
        check('One receipt scalar '+leg+'/'+k,len(vals)==1)
        return vals[0]
    check('Receipt invariant core text '+leg,invariant_core(a)==invariant_core(b))
    check('Receipt new validator '+leg,scalar(b,'validator_source_digest')=='ba51cd20caa10b7b')
    check('Receipt n_checks '+leg,int(scalar(b,'n_checks'))==nchecks)
    core_sha=scalar(b,'core_sha256')
    ledger=(REF/'docs/22p_gap/LEG_PRESERVATION.yaml').read_text(encoding='utf-8')
    check('Current receipt core linked from ledger '+leg,core_sha in ledger)
    receipts.append({'leg':leg,'declared_core_sha256':core_sha,'receipt_sha256':sha(now.read_bytes()),'n_checks':nchecks,'stamp_text':b.split('\nstamp:\n',1)[1],'core_text_unchanged_except_validator_identity':True})
dump('RECEIPT_COMPARISON.json',{'receipts':receipts,'scope':'Existing exact receipt bytes, text core and ledger anchor comparison only; YAML core canonical hash not independently regenerated. No bundle restore, validation or receipt regeneration. Dirty stamp is preserved and is not replaced by clean-start claim.'})
after={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
check('Prior Gate84 selected files unchanged',before==after)
dump('SELECTED_PRESERVATION.json',{'scope':'Local Gate84 review files only; not remote OS/runtime or all historical evidence.','before':before,'after':after,'pass':before==after})
dump('STATIC_AUDIT.json',{'pass':True,'checks':checks,'source_digest':h.hexdigest()[:16],'received_program_executions':0,'project_tests':0,'mutations':0,'restore':0,'COMSOL':0,'limitation':'PASS refers to reviewer byte/AST/data checks, not Round2a acceptance or runtime behavior.'})
print(json.dumps({'status':'REVIEWER_STATIC_DATA_AUDIT_COMPLETED','checks':len(checks),'source_digest':h.hexdigest()[:16],'countermodel':'LOCAL_PREDICATE_ONLY','production_executions':0}))
