"""Immutable read-only GitHub intake; no git operations or simulator execution."""
from pathlib import Path
import concurrent.futures,hashlib,json,os,sys,time,urllib.request,urllib.parse
R=Path(__file__).resolve().parent
OLD=R.parent/'rint_g2_impl_review_20261014'
PIN='dcb97f1ed942f622d9189eee1a1e9432dc05a655'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
def fetch(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Read-only-review'}),timeout=90) as f:return f.read()
        except Exception:
            if attempt==3:raise
            time.sleep(attempt+1)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
for name in ('source','source_prior','evidence','probes','notes','tmp','support','submitted'):(R/name).mkdir(parents=True,exist_ok=True)
tp=R/'evidence/tree.json'
if not tp.exists():tp.write_bytes(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1'))
t=json.loads(tp.read_text(encoding='utf-8'));assert not t.get('truncated')
es={x['path']:x for x in t['tree'] if x['type']=='blob'}
oldmf=json.loads((OLD/'source_manifest.json').read_text(encoding='utf-8'))
paths={x['path'] for x in oldmf['files'] if x['path'] in es}
paths|={p for p in es if p.startswith(('docs/reviews/rint_g2_impl_fix_evidence_20261015/','docs/data/rint_t2_dev_20261013/'))
        or p.startswith('docs/reviews/') and ('rint_g2_impl_fix' in p or 'rint_g2_impl_reverify' in p)}
paths|={'AGENTS.md','CLAUDE.md','docs/reviews/findings.json','scripts/seal_s3_prerun.py','scripts/run_network_194_parallel.py'}
paths|=set(sys.argv[1:])
def one(p):
    x=es[p];b=None;reused=False
    for root in (R/'source',OLD/'source'):
        q=long(root/p)
        if q.is_file():
            raw=q.read_bytes()
            if blob(raw)==x['sha']:b=raw;reused=True;break
    if b is None:b=fetch(f'https://raw.githubusercontent.com/{REPO}/{PIN}/'+urllib.parse.quote(p))
    assert blob(b)==x['sha'],p
    q=long(R/'source'/p);q.parent.mkdir(parents=True,exist_ok=True)
    if not q.exists():q.write_bytes(b)
    else:assert q.read_bytes()==b,p
    return {'path':p,'git_blob':x['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'reused':reused}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:rows=list(pool.map(one,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps({'pin':PIN,'repo':REPO,'files':rows},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pin':PIN,'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'reused':sum(x['reused'] for x in rows),'requests':[x['path'] for x in rows if x['path'].startswith('docs/reviews/codex_rint') and '20261015' in x['path']]},ensure_ascii=False,indent=2))
