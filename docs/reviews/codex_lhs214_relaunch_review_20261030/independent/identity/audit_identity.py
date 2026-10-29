"""Offline pinned-tree/source audit; no product imports, git, or simulations."""
import ast, base64, difflib, hashlib, json, re, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
REPO = BASE / 'repo'
META = HERE / 'metadata'
SOURCES = HERE / 'sources'
PINS = {'B7': '35f0327377a4213774010a090df4d224e50d29e1', 'review': 'bf8cf21c6466cdb9411f9320711b871c2d1c651e'}

def readj(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def blobsha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

for f in SOURCES.rglob('*.b64.json'):
    payload=readj(f)
    data=base64.b64decode(payload['content'])
    assert blobsha(data)==payload['sha'], f
    (SOURCES/payload['path']).write_bytes(data)

def tree(pin, part):
    path = META / f'{pin}_{part}.json'
    d = readj(path)
    assert d['truncated'] is False, path
    return d

def tree_sha(entries):
    parts=[]
    for e in sorted(entries,key=lambda e:(e['path']+('/' if e['type']=='tree' else '')).encode('utf-8')):
        parts.append(e['mode'].lstrip('0').encode()+b' '+e['path'].encode('utf-8')+b'\0'+bytes.fromhex(e['sha']))
    data=b''.join(parts)
    return hashlib.sha1(b'tree '+str(len(data)).encode()+b'\0'+data).hexdigest()

TREE_CHECKS=[]
for pin,sha in PINS.items():
    commit=readj(META/f'commit_{sha}.json')
    for part in ['root','scripts','webapp','docs','docs_data','docs_reviews']:
        d=tree(pin,part)
        expected=commit['tree']['sha'] if part=='root' else d['sha']
        actual=tree_sha(d['tree'])
        TREE_CHECKS.append({'pin':pin,'part':part,'expected':expected,'actual':actual,'equal':expected==actual})
        assert expected==actual,(pin,part,expected,actual)

def index(pin):
    root = tree(pin, 'root')
    out = {e['path']: e for e in root['tree']}
    for part in ['scripts','webapp','docs','docs_data','docs_reviews']:
        d = tree(pin, part)
        prefix = part.replace('_','/')
        assert out[prefix]['sha'] == d['sha'], prefix
        out.update({prefix + '/' + e['path']: e for e in d['tree']})
    return out

IDX = {p:index(p) for p in PINS}
for name,prefix in [('lhs214_wsl_preflight_35f032737_1028','docs/reviews/lhs214_wsl_preflight_35f032737_1028'),('codex_lhs214_pin_syntax_review_20261028','docs/reviews/codex_lhs214_pin_syntax_review_20261028'),('bundle','docs/reviews/lhs214_wsl_preflight_35f032737_1028/bundle')]:
    d=readj(META/f'review_archive_{name}.json')
    assert d['truncated'] is False
    actual=tree_sha(d['tree'])
    expected=IDX['review'][prefix]['sha']
    assert actual==expected==d['sha']
    TREE_CHECKS.append({'pin':'review','part':prefix,'expected':expected,'actual':actual,'equal':True})
    IDX['review'].update({prefix+'/'+e['path']:e for e in d['tree']})
USED = {}
MISSING = {}

def source(pin, rel):
    expected = IDX[pin][rel]['sha']
    dst = SOURCES / rel
    for folder in [SOURCES, REPO]:
        f = folder / rel
        if f.is_file():
            b = f.read_bytes()
            if blobsha(b) == expected:
                if folder != SOURCES:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    dst.write_bytes(b)
                USED[rel] = {'git_sha': expected, 'sha256':hashlib.sha256(b).hexdigest(), 'size': len(b)}
                return b.decode('utf-8')
    MISSING[rel] = {'path':rel, 'pin':PINS[pin], 'git_sha':expected}
    return None

def consts(pin):
    mod=ast.parse(source(pin, 'scripts/run_network_194_parallel.py'))
    return {n.targets[0].id:ast.literal_eval(n.value) for n in mod.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('CODE_FILES','HANDOVER_FILES')}

def closure(pin):
    c=consts(pin)
    start=list(c['CODE_FILES']) + ['scripts/run_network_194_parallel.py','scripts/supp20_input_receipt.py','scripts/wsl_network_smoke.py','scripts/g2_network_reread.py','scripts/lhs_design_dataset.py','scripts/lhs_release_build.py']
    seen=set(); todo=list(start); edges=[]; unresolved=[]; special=[]
    while todo:
        rel=todo.pop()
        if rel in seen: continue
        seen.add(rel)
        s=source(pin,rel)
        if s is None: continue
        for n in ast.walk(ast.parse(s)):
            names=[]
            if isinstance(n,ast.Import): names=[a.name for a in n.names]
            elif isinstance(n,ast.ImportFrom) and n.module and n.level==0: names=[n.module]
            elif isinstance(n,ast.Call) and getattr(n.func,'attr','')=='import_module' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str): names=[n.args[0].value]
            if isinstance(n,ast.ImportFrom) and n.level: special.append({'file':rel,'line':n.lineno,'kind':'relative import','code':ast.get_source_segment(s,n)})
            if isinstance(n,ast.Call) and (getattr(n.func,'attr','') in ('import_module','spec_from_file_location') or getattr(n.func,'id','') in ('__import__','import_module')): special.append({'file':rel,'line':n.lineno,'kind':'dynamic import','code':ast.get_source_segment(s,n)})
            for name in names:
                top=name.split('.')[0]; candidates=[p+'/'+top+'.py' for p in ('scripts','webapp') if p+'/'+top+'.py' in IDX[pin]]
                if candidates:
                    q=candidates[0]; edges.append({'from':rel,'line':n.lineno,'name':name,'to':q,'candidates':candidates});todo.append(q)
                else: unresolved.append({'from':rel,'line':n.lineno,'name':name})
    return {'count':len(seen),'files':sorted(seen),'edges':edges,'unresolved':unresolved,'special':special}

CL={p:closure(p) for p in PINS}
CORE={p:sorted(list(consts(p)['CODE_FILES']) + list(consts(p)['HANDOVER_FILES']) + ['scripts/lhs_release_build.py','scripts/run_network_194_parallel.py','scripts/supp20_input_receipt.py','scripts/wsl_network_smoke.py','docs/reviews/lhs_network_batch_registration_20261007_g2.md','docs/reviews/lhs_network_batch_registration_20261012_supp20.md']) for p in PINS}
request=(REPO/'docs/reviews/codex_lhs214_relaunch_check_request_20261028.md').read_text(encoding='utf-8')
INPUT=re.search(r'^IN="([^"]+)"',request,re.M).group(1).split()

def compare(paths):
    out=[]
    for p in paths:
        a,b=IDX['B7'].get(p),IDX['review'].get(p)
        out.append({'path':p,'B7_sha':a and a['sha'],'review_sha':b and b['sha'],'type':b and b['type'],'equal':bool(a and b and (a['sha'],a['mode'],a['type'])==(b['sha'],b['mode'],b['type']))})
    return out

code=list(consts('review')['CODE_FILES'])
for p in CORE['review']: source('review',p)
fp=hashlib.sha256(json.dumps(sorted((p,USED[p]['sha256']) for p in code),separators=(',',':')).encode()).hexdigest()
changed=compare(sorted(p for p in set(IDX['B7'])|set(IDX['review']) if p.startswith(('scripts/','webapp/')) and p.endswith('.py')))
GATES={}
for rel in ['scripts/check_all.sh','docs/reviews/selftest_inventory.tsv']:
    texts={}
    for pin in PINS:
        payload=readj(HERE/'gate_inputs'/pin/(rel+'.b64.json'))
        b=base64.b64decode(payload['content'])
        assert blobsha(b)==IDX[pin][rel]['sha']==payload['sha']
        p=HERE/'gate_inputs'/pin/rel
        p.write_bytes(b)
        texts[pin]=b.decode('utf-8')
    dl=list(difflib.ndiff(texts['B7'].splitlines(),texts['review'].splitlines()))
    added=[s[2:] for s in dl if s.startswith('+ ')]
    removed=[s[2:] for s in dl if s.startswith('- ')]
    GATES[rel]={'added_count':len(added),'removed_count':len(removed),'added':added,'removed':removed}
    if rel.endswith('.tsv'):
        pat=r'^scripts/(run_network_194_parallel|supp20_input_receipt|wsl_network_smoke|g2_network_reread|lhs_design_dataset|lhs_release_build)\.py'
        rows={pin:[s for s in texts[pin].splitlines() if re.match(pat,s)] for pin in PINS}
        GATES[rel]['lhs_rows']=rows
        GATES[rel]['lhs_rows_equal']=rows['B7']==rows['review']
        GATES[rel]['lhs7_sha256']={pin:hashlib.sha256(('\n'.join(rows[pin])+'\n').encode()).hexdigest() for pin in PINS}
        GATES[rel]['lhs7_first4_sha256']={pin:hashlib.sha256(('\n'.join('\t'.join(row.split('\t')[:4]) for row in rows[pin])+'\n').encode()).hexdigest() for pin in PINS}
    else:
        GATES[rel]['fast_driver_lines']={pin:[{'line':i,'text':s} for i,s in enumerate(texts[pin].splitlines(),1) if 'check_selftest_inventory.py --run-fast' in s] for pin in PINS}
GATES['fast_driver_blob']=compare(['scripts/check_selftest_inventory.py'])
ARCHIVE=[]
for f in sorted(REPO.rglob('*')):
    if not f.is_file():continue
    rel=f.relative_to(REPO).as_posix();b=f.read_bytes();actual=blobsha(b);e=IDX['review'].get(rel)
    ARCHIVE.append({'path':rel,'expected_git_sha':e and e['sha'],'actual_git_sha':actual,'equal':bool(e and e['sha']==actual),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
CMP=readj(META/'compare.json')
assert CMP['base']==PINS['B7'] and CMP['head']==PINS['review'] and CMP['merge_base_commit']['sha']==PINS['B7']
result={'pins':PINS,'commit_comparison':{k:CMP[k] for k in ('status','ahead_by','behind_by','total_commits','merge_base_commit')},'tree_hash_checks':TREE_CHECKS,'archive':{'files':len(ARCHIVE),'verified':sum(x['equal'] for x in ARCHIVE),'entries':ARCHIVE},'core':{'counts':{p:len(CORE[p]) for p in PINS},'same_set':CORE['B7']==CORE['review'],'entries':compare(CORE['review'])},'closure':{'counts':{p:CL[p]['count'] for p in PINS},'same_set':CL['B7']['files']==CL['review']['files'],'entries':compare(CL['review']['files']),'graph':CL},'inputs':{'count':len(INPUT),'entries':compare(INPUT)},'code_fp':fp,'changed_scripts_webapp_py':[x for x in changed if not x['equal']],'source_blobs':USED,'missing_sources':list(MISSING.values()),'gates':GATES}
(HERE/'identity_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'missing_sources.json').write_text(json.dumps(list(MISSING.values()),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'input16.json').write_text(json.dumps(result['inputs'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(HERE/'gate_results.json').write_text(json.dumps(GATES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={'tree_hash_checks':len(TREE_CHECKS),'archive':{'files':len(ARCHIVE),'verified':sum(x['equal'] for x in ARCHIVE)},'core':result['core']['counts'],'core_equal':all(x['equal'] for x in result['core']['entries']),'closure':result['closure']['counts'],'closure_equal':all(x['equal'] for x in result['closure']['entries']),'input16_equal':all(x['equal'] for x in result['inputs']['entries']),'missing':len(MISSING),'missing_files':list(MISSING),'code_fp':fp,'changed_py':len(result['changed_scripts_webapp_py']),'gate_counts':{p:{k:v for k,v in x.items() if k.endswith('_count') or k=='lhs_rows_equal'} for p,x in GATES.items() if isinstance(x,dict)}}
(HERE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
assert not MISSING
assert all(x['equal'] for x in ARCHIVE)
assert result['core']['same_set'] and result['closure']['same_set']
assert summary['core_equal'] and summary['closure_equal'] and summary['input16_equal']
