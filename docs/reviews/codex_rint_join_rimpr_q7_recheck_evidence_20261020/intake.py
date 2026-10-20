"""Read-only pinned GitHub retrieval. Never changes a checkout or tracked file."""
from pathlib import Path
import concurrent.futures, hashlib, json, os, shutil, sys, time, urllib.request, urllib.parse
R = Path(__file__).resolve().parent
W = R.parent
OLD = W / 'rint_g2_impl_reverify_20261015'
PIN = '2b9efa253edbf455c2e1abfef1d60e51818e01f8'
BASE = 'dcb97f1ed942f622d9189eee1a1e9432dc05a655'
REPO = 'yonghoon7153-source/Yonghoon-DEM-DFT'

def long(p):
    s = str(p)
    return Path('\\\\?\\'+s) if os.name == 'nt' and not s.startswith('\\\\?\\') else p

def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Read-only-review'}),timeout=45) as f:
                return f.read()
        except Exception:
            if i == 3: raise
            time.sleep(i+1)

def blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def metadata(name,url):
    p=R/'evidence'/name
    if not p.exists(): p.write_bytes(get(url))
    return json.loads(p.read_text(encoding='utf8'))

for name in ('source','evidence','probes','notes','tmp','submitted'):
    (R/name).mkdir(parents=True,exist_ok=True)
shutil.copyfile('C:/Users/Administrator/Downloads/codex_rint_join_rimpr_q7_recheck_request_20261020_send.md',
               R/'submitted/codex_rint_join_rimpr_q7_recheck_request_20261020_send.md')
c=metadata('commit.json',f'https://api.github.com/repos/{REPO}/commits/{PIN}')
assert c['sha']==PIN
t=metadata('tree.json',f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1')
bt=metadata('base_tree.json',f'https://api.github.com/repos/{REPO}/git/trees/{BASE}?recursive=1')
assert not t.get('truncated') and not bt.get('truncated')
es={x['path']:x for x in t['tree'] if x['type']=='blob'}
bs={x['path']:x for x in bt['tree'] if x['type']=='blob'}
changed=[p for p in es if p not in bs or es[p]['sha']!=bs[p]['sha']]
(R/'evidence/tree_diff.json').write_text(json.dumps(dict(changed=changed,deleted=[p for p in bs if p not in es]),ensure_ascii=False,indent=2),encoding='utf8')
oldmf=json.loads((OLD/'source_manifest.json').read_text(encoding='utf8'))
paths={x['path'] for x in oldmf['files'] if x['path'] in es}
paths|={p for p in es if p.endswith('AGENTS.md')}
paths|={p for p in es if p.startswith(('docs/reviews/','docs/data/')) and
        ('rint_join' in p or 'rimpr' in p or 'rint_g2_impl_fix' in p)}
paths|={p for p in es if p.startswith('scripts/') and p.endswith('.py') and
        ('rint' in p or 'sigma' in p)}
paths|={'scripts/step3_sigma.py','scripts/run_network_194_parallel.py','scripts/seal_s3_prerun.py','docs/reviews/findings.json'}
paths|=set(sys.argv[1:])
print(json.dumps(dict(pin=PIN,base=BASE,files=len(paths),changed_code=[p for p in changed if p.startswith(('scripts/','webapp/'))]),ensure_ascii=False),flush=True)
caches=[R/'source',OLD/'source',W/'lhs214s_recheck_20261019/source',W/'rint_g2_impl_review_20261014/source']
def one(p):
    b=None; reused=False
    for cache in caches:
        q=long(cache/p)
        if q.is_file():
            raw=q.read_bytes()
            if blob(raw)==es[p]['sha']:
                b=raw; reused=True; break
    if b is None: b=get(f'https://raw.githubusercontent.com/{REPO}/{PIN}/'+urllib.parse.quote(p))
    assert blob(b)==es[p]['sha'],p
    dest=R/'source'/p
    if not long(dest.parent).is_dir():
        try: dest.parent.mkdir(parents=True,exist_ok=True)
        except OSError: long(dest.parent).mkdir(parents=True,exist_ok=True)
    dest=long(dest)
    if dest.exists(): assert dest.read_bytes()==b,p
    else: dest.write_bytes(b)
    return dict(path=p,git_blob=es[p]['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reused)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
    rows=list(pool.map(one,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,base=BASE,repo=REPO,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(dict(files=len(rows),bytes=sum(x['bytes'] for x in rows),reused=sum(x['reused'] for x in rows))),flush=True)
