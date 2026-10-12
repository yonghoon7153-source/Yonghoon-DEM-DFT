from pathlib import Path
import ast, concurrent.futures, hashlib, json, sys, urllib.request, urllib.parse

R=Path(__file__).resolve().parent
PIN='46cd0bdb872e7d6c85ca50ec4172e98377253130'
LIT='e739c9730f8758d2d61b2db22d940ee9a2440897'
API='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
RAW='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'
for n in ('source','literature_cards','literature','evidence','notes','probes','tmp'):(R/n).mkdir(parents=True,exist_ok=True)
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-read-only-review'}),timeout=60) as r:return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
trees={}
for name,pin in [('code',PIN),('lit',LIT)]:
    tree=json.loads(fetch(API+'git/trees/'+pin+'?recursive=1'));assert not tree.get('truncated')
    (R/(name+'_tree.json')).write_text(json.dumps(tree,ensure_ascii=False,indent=2),encoding='utf8')
    trees[name]={x['path']:x for x in tree['tree'] if x['type']=='blob'}
    (R/(name+'_commit.json')).write_bytes(fetch(API+'commits/'+pin))
manifest=[]
def get(path,kind='code'):
    pin=PIN if kind=='code' else LIT
    entry=trees[kind][path]
    root=R/'source' if kind=='code' else R/'literature_cards'
    dst=root/path
    if dst.exists():return
    old=R.parent/'supp20_support_review_20261012/source'/path
    b=old.read_bytes() if kind=='code' and old.exists() else b''
    blob=lambda x:hashlib.sha1(b'blob '+str(len(x)).encode()+b'\0'+x).hexdigest()
    if blob(b)!=entry['sha']:b=fetch(RAW+pin+'/'+urllib.parse.quote(path))
    assert blob(b)==entry['sha'] and len(b)==entry['size'],path
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    manifest.append({'kind':kind,'path':path,'sha':entry['sha'],'sha256':sha(b),'bytes':len(b)})
    print(kind,path,flush=True)
paths=['AGENTS.md','CLAUDE.md','scripts/network_conductivity.py','scripts/plastic_coverage.py',
       'scripts/test_network_generation2.py','scripts/test_network_dirichlet.py',
       'scripts/test_network_solve_certificate.py','scripts/test_physics_area_g2.py',
       'docs/reviews/findings.json','docs/reviews/claims.json']
paths += [p for p in trees['code'] if p.startswith('docs/data/ps45_r45_network_g2_20261007/')]
paths += [p for p in trees['code'] if p.startswith('docs/reviews/') and ('ps45' in p.lower() and ('sigma' in p.lower() or 'electro' in p.lower()))]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,[p for p in paths if p in trees['code']]))
for _ in range(6):
    needs=set()
    for src in (R/'source/scripts').glob('*.py'):
        try:a=ast.parse(src.read_text(encoding='utf8'))
        except (SyntaxError,UnicodeError):continue
        for node in ast.walk(a):
            names=[x.name for x in node.names] if isinstance(node,ast.Import) else [node.module] if isinstance(node,ast.ImportFrom) and node.module else []
            for name in names:
                path='scripts/'+name.replace('.','/')+'.py'
                if path in trees['code'] and not (R/'source'/path).exists():needs.add(path)
    if not needs:break
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(get,sorted(needs)))
litpaths=[p for p in trees['lit'] if p.startswith('litdb/papers/') and p.endswith('.md') and any(k in p.lower() for k in ['ketter2025_resistor','minnmann2021','asano2017','wang2018','trevisanello'])]
for p in litpaths:get(p,'lit')
(R/'source_manifest.json').write_text(json.dumps({'pin':PIN,'lit_pin':LIT,'files':manifest},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'pin':PIN,'lit_pin':LIT,'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest)},indent=2))
