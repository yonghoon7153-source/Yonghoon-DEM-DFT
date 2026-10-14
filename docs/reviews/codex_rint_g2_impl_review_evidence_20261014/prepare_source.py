from pathlib import Path
import concurrent.futures, hashlib, json, os, sys, urllib.request, urllib.parse
R=Path(__file__).resolve().parent
PIN='1087a9b2f4a93aa6a3b0debc698a14fffa13488d'
API='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
RAW='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Read-only-review'}),timeout=120) as r:return r.read()
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for sub in ('source','evidence','probes','notes','tmp','submitted'):(R/sub).mkdir(parents=True,exist_ok=True)
tree_path=R/'evidence/tree.json'
if not tree_path.exists():tree_path.write_bytes(fetch(API+'git/trees/'+PIN+'?recursive=1'))
t=json.loads(tree_path.read_text(encoding='utf8'));assert not t.get('truncated')
es={e['path']:e for e in t['tree'] if e['type']=='blob'}
if sys.argv[1:] == ['list']:
    print('\n'.join(f"{e['size']:9d} {p}" for p,e in es.items() if ('rint' in p.lower() and (p.startswith('scripts/') or p.startswith('docs/data/') or p.startswith('docs/reviews/'))) or 'contact_resistance_pipeline_draft_v' in p))
    sys.exit()
paths=set(sys.argv[1:])
if not paths:
    paths={p for p in es if (p.startswith('scripts/') and '/' not in p[8:] and p.endswith('.py'))
        or p in ('AGENTS.md','CLAUDE.md')
        or (p.startswith('docs/reviews/') and ('contact_resistance_pipeline_draft_v' in p or 'rint' in p.lower()))
        or p.startswith(('docs/data/rint_t41_census_20261013/','docs/data/rint_t43_order_20261013/','docs/data/rint_t2_dev_20261013/'))}
cache_roots=[R/'source',R.parent/'supr_reverify_20261014/source',R.parent/'rint_g2_v3_review_20261007/source',R.parent/'sup20_fix_reverify_20261014/source']
def get(p):
    e=es[p]; b=None;reuse=False
    for c in cache_roots:
        f=long(c/p)
        if f.is_file():
            x=f.read_bytes()
            if blob(x)==e['sha']:b=x;reuse=True;break
    if b is None:b=fetch(RAW+urllib.parse.quote(p))
    assert blob(b)==e['sha'] and len(b)==e['size'],p
    dest=long(R/'source'/p);dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():dest.write_bytes(b)
    else:assert dest.read_bytes()==b
    return dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reuse)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(get,sorted(paths)))
mf=R/'source_manifest.json'; existing=json.loads(mf.read_text())['files'] if mf.exists() else []
joined={r['path']:r for r in existing+rows}
mf.write_text(json.dumps(dict(pin=PIN,files=[joined[p] for p in sorted(joined)]),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(pin=PIN,downloaded=len(rows),total=len(joined),reused=sum(r['reused'] for r in rows))))
