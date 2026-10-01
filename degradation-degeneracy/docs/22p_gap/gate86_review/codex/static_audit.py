"""Reviewer-owned byte/AST/log audit. Does not import or execute received code."""
import ast
import difflib
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
E, REF = HERE / 'evidence', HERE / 'reference'
OLD = HERE.parent / 'gate85_review_20261001'
HEAD = '27bfeed68ea516e5c5a50f2475c8cc2b4f80ff3b'
TARGET = 'b4876b0b2098c9e87630fc715b44ab65336b73a2'
checks = []

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(b):
    return hashlib.sha256(b).hexdigest()

def gitsha(kind, b):
    return hashlib.sha1(kind.encode() + b' ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def dump(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def check(name, ok):
    checks.append({'check':name, 'pass':bool(ok)})
    if not ok:
        dump('AUDIT_FAILURE.json', {'checks':checks})
        raise AssertionError(name)

before = {p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
refs = []
for p in sorted(E.glob('*.json')):
    d = read(p)
    if not isinstance(d, dict) or not isinstance(d.get('content'), str) or not d.get('sha'):
        continue
    b = d['content'].encode('utf-8')
    check('Git blob ' + p.name, gitsha('blob', b) == d['sha'])
    rel = p.stem.replace('__', '/')
    check('Pinned reference ' + rel, '/' + HEAD + '/' in d['display_url'])
    dest = REF / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(b)  # Mechanical exact-byte materialization, not source editing.
    refs.append({'path':rel,'bytes':len(b),'sha256':sha(b),'git_blob_sha1':d['sha'],'url':d['display_url']})

head_entries = {x['name']:x for x in json.loads(read(E/'HEAD_DIRECTORY.json')['content'])}
prior_tree = read(HERE.parent/'gate83_review_20260930/evidence/SCOPE_TREE_INVENTORY.json')
modes = {t['dir']+'/'+x['path']:x['mode'].lstrip('0') for t in prior_tree['trees'] for x in t['tree'] if x['type']=='blob'}
inventory = {}
for directory in ['src','tools','configs','scripts']:
    ents = json.loads(read(E/('DIR_'+directory+'.json'))['content'])
    check('Complete flat directory '+directory, all(x['type']=='file' for x in ents))
    body = b''.join((modes[directory+'/'+x['name']]+' '+x['name']).encode()+b'\0'+bytes.fromhex(x['sha']) for x in sorted(ents,key=lambda x:x['name'].encode()))
    check('Git tree reconstruction '+directory, gitsha('tree',body)==head_entries[directory]['sha'])
    inventory.update({directory+'/'+x['name']:x['sha'] for x in ents})
for name in ['run.sh','requirements.txt','requirements-gpu.txt']:
    inventory[name] = head_entries[name]['sha']
scope = {}
changed = []
for rel, blobsha in sorted(inventory.items()):
    old = (OLD/'reference'/rel).read_bytes()
    b = (REF/rel).read_bytes() if rel=='src/io.py' else old
    check('Current scope blob '+rel, gitsha('blob',b)==blobsha)
    if b != old:
        changed.append(rel)
    dest=REF/rel
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(b)
    scope[rel]=b
check('Exact scope 58 files',len(scope)==58)
check('Only production io changed',changed==['src/io.py'])
h=hashlib.sha256()
for rel,b in sorted(scope.items()):
    h.update(rel.encode()); h.update(b)
check('Independent source_digest',h.hexdigest()[:16]=='f1f4378f46610f08')

def in_scope(name):
    return name.removeprefix('degradation-degeneracy/') in inventory

for name in ['TARGET_COMPARE','GREEN_TO_TARGET','AUTH_TO_HEAD','RED_TO_GREEN']:
    d=read(E/(name+'.json'))
    check('Untruncated compare '+name,not d.get('too_large') and len(d['files'])<300)
    check('Forward ancestry '+name,d['behind_by']==0)
    if name in ['TARGET_COMPARE','GREEN_TO_TARGET']:
        check('Scope diff zero '+name,not any(in_scope(x['filename']) for x in d['files']))
green=[x for x in read(E/'RED_TO_GREEN.json')['files'] if in_scope(x['filename'])]
check('Exact GREEN delta',len(green)==1 and green[0]['filename'].endswith('/src/io.py') and (green[0]['additions'],green[0]['deletions'])==(77,2))
auth=read(E/'AUTH_TO_HEAD.json')
check('No tracked class/claim/cohort delta',not any('/_exec_class/' in x['filename'] or '/_claims/' in x['filename'] or x['filename'].endswith('/COHORT_LIFECYCLE.jsonl') for x in auth['files']))
dump('SOURCE_IDENTITIES.json',{'head':HEAD,'target':TARGET,'source_digest':h.hexdigest()[:16],'scope_count':len(scope),'changed':changed,'scope':[{'path':k,'sha256':sha(v),'git_blob_sha1':inventory[k]} for k,v in scope.items()],'references':refs})
diff=''.join(difflib.unified_diff((OLD/'reference/src/io.py').read_text(encoding='utf-8').splitlines(True),scope['src/io.py'].decode().splitlines(True),fromfile='Gate85/src/io.py',tofile=HEAD+'/src/io.py'))
(HERE/'PRODUCTION.diff').write_text(diff,encoding='utf-8')

old_tree=ast.parse((OLD/'reference/src/io.py').read_text(encoding='utf-8'))
tree=ast.parse(scope['src/io.py'].decode())
oldf={n.name:n for n in old_tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
newf={n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
changed_funcs=[k for k in oldf if ast.dump(oldf[k],include_attributes=False)!=ast.dump(newf[k],include_attributes=False)]
check('Only existing _stage3_checks AST changed',changed_funcs==['_stage3_checks'])
check('One added function',set(newf)-set(oldf)=={'base_config_closure_members'})
check('No function removed',not set(oldf)-set(newf))
io=scope['src/io.py'].decode()
def body(name):
    n=newf[name]
    return '\n'.join(io.splitlines()[n.lineno-1:n.end_lineno])
helper=body('base_config_closure_members')
closure=body('_stage3_checks').split('    # ★ 84차 G84-N1')[1]
facts={
 'derive_from_root':'base_config_closure_members(spec0.get("base_config"), sealed, run_dir / "_inputs")' in closure,
 'cycle':'if norm in order:' in helper,
 'outside_repo':'posixpath.isabs(norm) or norm == ".." or norm.startswith("../")' in helper,
 'depth':'if len(order) >= _CLOSURE_MAX_DEPTH:' in helper and '_CLOSURE_MAX_DEPTH = 32' in io,
 'unsealed_parent':'if not dig:' in helper,
 'missing_snapshot':'if not snap.is_file():' in helper,
 'yaml_and_utf8':'except (yaml.YAMLError, UnicodeDecodeError)' in helper,
 'mapping':'if not isinstance(doc, dict):' in helper,
 'nonstring_extends':'elif not isinstance(ext, str) or not ext:' in helper,
 'normalized_relative_join':'key = posixpath.join(posixpath.dirname(norm), ext)' in helper,
 'unique':'keys.count(k) > 1' in closure,
 'missing':'set(members) - set(keys)' in closure,
 'extra':'set(keys) - set(members)' in closure,
 'derived_hash_material':'for k in (members if not bc_bad else []):' in closure,
 'actual_snapshot_sha':'hashlib.sha256(snap.read_bytes()).hexdigest()' in closure,
 'dual_compare':all(s in closure for s in ['got = closure_sha256_from_parts(parts)','run_spec.stage3.base_config_closure_sha256','계획 inputs.base_config_digest']),
 'no_live_loader_call':not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ['load_config','config_dependencies'] for n in ast.walk(newf['base_config_closure_members'])),
}
for name,ok in facts.items(): check('Static predicate '+name,ok)
test=(REF/'tests/test_gate85_closure_members.py').read_text(encoding='utf-8')
t=ast.parse(test)
tests=[n.name for n in t.body if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
check('Seven named test functions',len(tests)==7)
for needle in ['IO.validate_provenance(out)','assert G81._fails(v) == [CHECK]','_resign(out)','fits["run_sig"] = sig','G82._reseal_fits(out)','env_mutate=lambda e: e["inputs"].update(base_config_digest=digest)']:
    check('Test coupling '+needle,needle in test)
dump('STATIC_SOURCE_FACTS.json',{'facts':facts,'changed_existing_functions':changed_funcs,'tests':tests,'no_source_import_or_execution':True,'helper_dynamic_boundary_cases':['cycle','unsealed parent','missing snapshot','outside path','nonstring extends','missing root'],'static_only_boundary_cases':['depth 32','malformed YAML','nonmapping YAML','UTF8 decode failure'],'notes':['Full validator snapshot-hash and input-crossbinding checks remain unchanged. Helper alone is not a complete seal verifier.','No basename fallback is provided; this is a deliberately narrower accepted path set, not universal load_config equivalence.']})

mtree=ast.parse((REF/'docs/22p_gap/mutation_replay.py').read_text(encoding='utf-8'))
mut=[]
for n in ast.walk(mtree):
    if isinstance(n,ast.Tuple) and len(n.elts)==5 and isinstance(n.elts[0],ast.Constant) and isinstance(n.elts[0].value,str) and n.elts[0].value.endswith('-g85'):
        pre=ast.literal_eval(n.elts[2])
        count=io.count(pre)
        check('Mutation preimage '+n.elts[0].value,count==1)
        mut.append({'name':n.elts[0].value,'line':n.lineno,'preimage_count':count})
check('Seven mutation registrations',len(mut)==7)
dump('MUTATION_STATIC.json',{'registrations':mut,'replayed_by_reviewer':False})

readme=(REF/'docs/22p_gap/gate86_evidence/README.md').read_text(encoding='utf-8')
rows=re.findall(r'\| `([^`]+)` \| (\d+) \| `([0-9a-f]{64})` \|',readme)
check('Twelve source-log rows',len(rows)==12)
logs=[]
base=REF/'docs/22p_gap/gate86_evidence'
for rel,size,dig in rows:
    b=(base/rel).read_bytes()
    check('Evidence size '+rel,len(b)==int(size))
    check('Evidence full SHA '+rel,sha(b)==dig)
    logs.append({'path':rel,'bytes':len(b),'sha256':sha(b)})
replay=(base/'final_0be169b1/g86_replay_all.txt').read_text(encoding='utf-8')
counts={'hit':len(re.findall(r'^물었다\s',replay,re.M)),'survived':len(re.findall(r'^★ 안 물었다',replay,re.M)),'error':len(re.findall(r'^★ 실행오류',replay,re.M))}
check('Full replay 352/0/0',counts=={'hit':352,'survived':0,'error':0})
red=(base/'red_green/red_gate85.txt').read_text(encoding='utf-8')
check('RED all-validator [] four cases',red.count('assert \'base_config_결속\' in []')==4)
check('RED summary','5 failed, 2 passed' in red)
check('GREEN summary','23 passed' in (base/'red_green/green_gate85.txt').read_text(encoding='utf-8'))
check('Initial final one failure','1 failed, 2045 passed, 1 xfailed' in (base/'final_0be169b1/g86_pytest_full.txt').read_text(encoding='utf-8'))
wrapper=(base/'final_0be169b1/g86_final.log').read_text(encoding='utf-8')
check('Wrapper distinct return codes',all(s in wrapper for s in ['pytest rc=1','smoke rc=0','replay rc=0','source_digest f1f4378f46610f08']))
fix=(base/'witness_fix/g86_witness_fix.log').read_text(encoding='utf-8')
check('Clean target witness fix',all(s in fix for s in ['17 passed','replay rc=0','START_HEAD='+TARGET+' status=0','END_HEAD='+TARGET+' status=0']))
stray=read(next((base/'stray_exec_class').glob('*.json')))
check('Stray explicitly canonical sealed',stray['execution_class']=='canonical' and stray['sealed'] is True)
dump('LOG_AUDIT.json',{'files':logs,'readme_sha256':sha((base/'README.md').read_bytes()),'full_replay':counts,'original_full_run_commit':'0be169b18ed40f64c6aae4ca7e364e45ba46fa32','original_full_pytest':{'failed':1,'passed':2045,'xfailed':1},'target_witness_fix_observed_in_logs':True,'final_request_2046_suite':'USER_MESSAGE_REPORTED; raw source logs not in fixed HEAD evidence','first_RED':'Overwritten per evidence README, not independently recovered','stray_record':stray,'remote_runtime_observed':False})

receipts=[]
ledger=(REF/'docs/22p_gap/LEG_PRESERVATION.yaml').read_text(encoding='utf-8')
for leg,ncheck in [('paired_fixed5_v4',35),('grid_fit_v5',34)]:
    rel='docs/22p_gap/receipts/'+leg+'.validate.yaml'
    now=(REF/rel).read_bytes()
    hist=(REF/('docs/22p_gap/receipts/history/'+leg+'.validate.ba51cd20caa10b7b.yaml')).read_bytes()
    check('Exact history '+leg,hist==(OLD/'reference'/rel).read_bytes())
    a,b=hist.decode(),now.decode()
    def core_invariant(s):
        c=s.split('\ncore:\n',1)[1].split('\nstamp:\n',1)[0]
        return '\n'.join(l for l in c.splitlines() if not re.match(r'\s*(validator_source_digest|src_io_sha256):',l))
    check('Receipt core only validator changes '+leg,core_invariant(a)==core_invariant(b))
    def scalar(k):
        vals=re.findall(r'^\s*'+re.escape(k)+r':\s*(\S+)\s*$',b,re.M)
        check('Unique scalar '+leg+'/'+k,len(vals)==1)
        return vals[0]
    check('Current validator '+leg,scalar('validator_source_digest')=='f1f4378f46610f08')
    check('IO SHA matches '+leg,sha(scope['src/io.py']).startswith(scalar('src_io_sha256')))
    check('Receipt check count '+leg,int(scalar('n_checks'))==ncheck)
    core=scalar('core_sha256')
    check('Ledger core anchor '+leg,core in ledger)
    check('Dirty stamp preserved '+leg,a.split('validator_tree_dirty:')[1].splitlines()[0]==b.split('validator_tree_dirty:')[1].splitlines()[0])
    receipts.append({'leg':leg,'core_sha256_declared':core,'file_sha256':sha(now),'n_checks':ncheck,'stamp':b.split('\nstamp:\n')[1],'core_text_except_validator_identity_unchanged':True})
    (HERE/(leg+'_RECEIPT.diff')).write_text(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='history/'+leg,tofile='current/'+leg)),encoding='utf-8')
dump('RECEIPT_COMPARISON.json',{'receipts':receipts,'scope':'Exact bytes, text and declared ledger anchor only; canonical YAML core hash NOT independently regenerated. No restore/revalidation/re-receipting.'})
for name in ['DECISION.json','PACKAGE_MANIFEST.json']:
    check('Embedded Gate85 exact '+name,(REF/'docs/22p_gap/gate85_review/codex'/name).read_bytes()==(OLD/name).read_bytes())
after={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
check('Prior local review preserved',before==after)
dump('SELECTED_PRESERVATION.json',{'scope':'Local Gate85 review files only, not remote runtime','before':before,'after':after,'pass':before==after})
dump('STATIC_AUDIT.json',{'pass':True,'checks':checks,'source_digest':h.hexdigest()[:16],'received_program_executions':0,'project_tests':0,'mutations':0,'restore':0,'COMSOL':0,'scope':'Reviewer-owned bytes/AST/log data checks, not recipient functional execution.'})
print(json.dumps({'status':'STATIC_DATA_REVIEW_COMPLETE','checks':len(checks),'source_digest':h.hexdigest()[:16],'logs_verified':len(logs),'full_replay_markers':counts,'received_code_executions':0}))
