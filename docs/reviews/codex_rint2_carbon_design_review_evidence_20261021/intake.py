"""Read-only pinned retrieval. No git checkout or remote writes."""
from pathlib import Path
import concurrent.futures, hashlib, json, os, urllib.request, urllib.parse, time
R=Path(__file__).resolve().parent
W=R.parent
PIN='5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def long(p): return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Pinned-read-only-review'}),timeout=45) as f: return f.read()
        except Exception:
            if i==3: raise
            time.sleep(i+1)
def metadata(name,url):
    p=R/'evidence'/name
    if not p.exists(): p.write_bytes(get(url))
    return json.loads(p.read_text(encoding='utf8'))
for d in ('source','evidence','notes','probes','tmp'): (R/d).mkdir(exist_ok=True)
c=metadata('commit.json',f'https://api.github.com/repos/{REPO}/commits/{PIN}')
assert c['sha']==PIN
t=metadata('tree.json',f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1')
assert not t.get('truncated')
es={e['path']:e for e in t['tree'] if e['type']=='blob'}
old=json.loads((W/'rint_join_q7_recheck_20261020/source_manifest.json').read_text(encoding='utf8'))
paths={e['path'] for e in old['files'] if e['path'] in es}
paths|={p for p in es if p.endswith('AGENTS.md') or p=='CLAUDE.md'}
paths|={p for p in es if p.startswith('scripts/') and p.endswith('.py')}
paths|={p for p in es if p.startswith('docs/reviews/') and any(q in p for q in ('rint_carbon','rint2_','rimprr','step3_conv'))}
paths|={p for p in es if p.startswith('docs/data/heckel_sweep_scaffolds/')}
paths|={p.relative_to(R/'repo').as_posix() for p in (R/'repo').rglob('*') if p.is_file() and '__pycache__' not in str(p)}
paths&=es.keys()
caches=[R/'source',R/'repo',W/'rint_join_q7_recheck_20261020/source',W/'lhs214cx_recheck_20261020/source',W/'rint_g2_impl_reverify_20261015/source']
def one(p):
    b=None
    for cache in caches:
        q=long(cache/p)
        if q.is_file():
            v=q.read_bytes()
            if blob(v)==es[p]['sha']: b=v; break
    reused=b is not None
    if b is None: b=get(f'https://raw.githubusercontent.com/{REPO}/{PIN}/'+urllib.parse.quote(p))
    assert blob(b)==es[p]['sha'],p
    dst=long(R/'source'/p); dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists(): assert dst.read_bytes()==b,p
    else: dst.write_bytes(b)
    return dict(path=p,git_blob=es[p]['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reused)
print(json.dumps({'pin':PIN,'files':len(paths)}),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool: rows=list(pool.map(one,sorted(paths)))
zip_match=[]
for q in (R/'repo').rglob('*'):
    if not q.is_file() or '__pycache__' in str(q): continue
    p=q.relative_to(R/'repo').as_posix()
    zip_match.append(dict(path=p,in_pin=p in es,same=p in es and blob(q.read_bytes())==es[p]['sha']))
(R/'evidence/zip_pin_comparison.json').write_text(json.dumps(zip_match,indent=2),encoding='utf8')
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'reused':sum(x['reused'] for x in rows),'zip_files':len(zip_match),'zip_mismatches':[x for x in zip_match if not x['same']]}),flush=True)
