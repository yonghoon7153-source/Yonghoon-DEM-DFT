"""Reviewer-owned byte/tree/AST/log audit. No received module imports or execution."""
import ast
import difflib
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
E, REF = HERE / 'evidence', HERE / 'reference'
OLD = HERE.parent / 'gate86_review_20261001'
HEAD = '672ab83b209c925c3d83ab0fca9b39b90d87f1fd'
TARGET = 'b8d4b69338f00083ece7e554660888b41d1b4905'
checks = []
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(b): return hashlib.sha256(b).hexdigest()
def gitsha(kind,b): return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def check(name,ok):
    checks.append({'check':name,'pass':bool(ok)})
    if not ok:
        dump('MATERIALIZE_FAILURE.json',{'checks':checks})
        raise AssertionError(name)
before={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
refs=[]
for p in sorted(E.glob('*.json')):
    d=read(p)
    if not isinstance(d,dict) or not isinstance(d.get('content'),str) or not d.get('sha'): continue
    b=d['content'].encode('utf-8')
    check('Git blob '+p.name,gitsha('blob',b)==d['sha'])
    rel='docs/22p_gap/GATE87_REQUEST.md' if p.stem=='request' else p.stem.replace('__','/')
    check('Pinned ref '+rel,'/'+HEAD+'/' in d['display_url'] or '/672ab83b2/' in d['display_url'])
    dest=REF/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
    refs.append({'path':rel,'bytes':len(b),'sha256':sha(b),'git_blob_sha1':d['sha'],'url':d['display_url']})
root={x['name']:x for x in json.loads(read(E/'HEAD_DIRECTORY.json')['content'])}
prior_tree=read(HERE.parent/'gate83_review_20260930/evidence/SCOPE_TREE_INVENTORY.json')
modes={t['dir']+'/'+x['path']:x['mode'].lstrip('0') for t in prior_tree['trees'] for x in t['tree'] if x['type']=='blob'}
inventory={}
for directory in ['src','tools','configs','scripts']:
    ents=json.loads(read(E/('DIR_'+directory+'.json'))['content'])
    check('Flat complete directory '+directory,all(x['type']=='file' for x in ents))
    body=b''.join((modes[directory+'/'+x['name']]+' '+x['name']).encode()+b'\0'+bytes.fromhex(x['sha']) for x in sorted(ents,key=lambda x:x['name'].encode()))
    check('Git tree '+directory,gitsha('tree',body)==root[directory]['sha'])
    inventory.update({directory+'/'+x['name']:x['sha'] for x in ents})
for name in ['run.sh','requirements.txt','requirements-gpu.txt']: inventory[name]=root[name]['sha']
scope={}; changed=[]
for rel,blob in sorted(inventory.items()):
    old=(OLD/'reference'/rel).read_bytes()
    b=(REF/rel).read_bytes() if rel in ['src/fitting.py','tools/preserve.py','run.sh'] else old
    check('Scope blob '+rel,gitsha('blob',b)==blob)
    if b!=old: changed.append(rel)
    dest=REF/rel; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
    scope[rel]=b
check('Scope 58',len(scope)==58)
check('Exact 3 production files',changed==['run.sh','src/fitting.py','tools/preserve.py'])
h=hashlib.sha256()
for rel,b in sorted(scope.items()): h.update(rel.encode()); h.update(b)
check('Digest 864edfb73b9695a1',h.hexdigest()[:16]=='864edfb73b9695a1')
for name in ['TARGET_COMPARE','AUTH_TO_HEAD']:
    d=read(E/(name+'.json'))
    check('Complete compare '+name,not d.get('too_large') and len(d['files'])<300 and d['behind_by']==0)
    delta=[f['filename'].removeprefix('degradation-degeneracy/') for f in d['files'] if f['filename'].removeprefix('degradation-degeneracy/') in inventory]
    check('Compare scope '+name,sorted(delta)==([] if name=='TARGET_COMPARE' else changed))
auth=read(E/'AUTH_TO_HEAD.json')
check('No tracked class claim cohort change',not any('/_exec_class/' in f['filename'] or '/_claims/' in f['filename'] or f['filename'].endswith('/COHORT_LIFECYCLE.jsonl') for f in auth['files']))
dump('SOURCE_IDENTITIES.json',{'head':HEAD,'target':TARGET,'source_digest':h.hexdigest()[:16],'scope_count':len(scope),'changed':changed,'scope':[{'path':p,'sha256':sha(b),'git_blob_sha1':inventory[p]} for p,b in scope.items()],'references':refs})
diff=''
ast_changes={}
for rel in changed:
    old=(OLD/'reference'/rel).read_text(encoding='utf-8'); new=scope[rel].decode()
    diff+=''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='Gate86/'+rel,tofile=HEAD+'/'+rel))
    if rel.endswith('.py'):
        a={n.name:n for n in ast.parse(old).body if isinstance(n,ast.FunctionDef)}
        b={n.name:n for n in ast.parse(new).body if isinstance(n,ast.FunctionDef)}
        ast_changes[rel]={'added':sorted(set(b)-set(a)),'removed':sorted(set(a)-set(b)),'modified':[k for k in a.keys()&b.keys() if ast.dump(a[k],include_attributes=False)!=ast.dump(b[k],include_attributes=False)]}
(HERE/'PRODUCTION.diff').write_text(diff,encoding='utf-8')
dump('AST_CHANGES.json',ast_changes)
readme=(REF/'docs/22p_gap/gate87_evidence/README.md').read_text(encoding='utf-8')
logs=[]
rows=re.findall(r'^([a-f0-9]{64})  (\d+)  (\S+\.log)$',readme,re.M)
check('13 log identifiers',len(rows)==13)
for dig,size,rel in rows:
    b=(REF/'docs/22p_gap/gate87_evidence'/rel).read_bytes()
    check('Log size '+rel,len(b)==int(size));check('Log SHA '+rel,sha(b)==dig)
    logs.append({'file':rel,'bytes':len(b),'sha256':dig,'CR_count':b.count(b'\r')})
dump('LOG_IDENTITIES.json',logs)
after={p.relative_to(OLD).as_posix():sha(p.read_bytes()) for p in OLD.rglob('*') if p.is_file()}
check('Prior review unchanged',before==after)
dump('PRESERVATION.json',{'selected_directory':str(OLD),'count':len(before),'before':before,'after_equal':before==after})
dump('MATERIALIZE_AUDIT.json',{'checks':checks,'passed':sum(c['pass'] for c in checks),'source_execution':False})
print(json.dumps({'checks':len(checks),'source_digest':h.hexdigest()[:16],'changed':changed,'ast_changes':ast_changes}))
