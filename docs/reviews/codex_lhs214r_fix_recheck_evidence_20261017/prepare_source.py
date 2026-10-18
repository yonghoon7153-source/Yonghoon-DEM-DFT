"""Immutable intake; no repository/git operations and no production execution."""
from pathlib import Path
import concurrent.futures, hashlib, json, os, time, urllib.request, urllib.parse
R=Path(__file__).resolve().parent
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
def fetch(url):
    for a in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'read-only-review'}),timeout=60) as f:return f.read()
        except Exception:
            if a==3:raise
            time.sleep(a+1)
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
for d in ('source','base','evidence','probes','notes','tmp','submitted'):(R/d).mkdir(parents=True,exist_ok=True)
submission=Path('C:/Users/Administrator/Downloads/codex_lhs214r_fix_recheck_request_20261016.md')
(R/'submitted'/submission.name).write_bytes(submission.read_bytes())
old=R.parent/'lhs214_fix_reverify_20261015'
oldmf=json.loads((old/'source_manifest.json').read_text(encoding='utf8'))
for short,folder in [('60ba39e22','source'),('6cb256956','base')]:
    cp=R/'evidence'/f'commit_{short}.json'
    if not cp.exists():cp.write_bytes(fetch(f'https://api.github.com/repos/{REPO}/commits/{short}'))
    c=json.loads(cp.read_text(encoding='utf8')); pin=c['sha']
    tp=R/'evidence'/f'tree_{short}.json'
    if not tp.exists():tp.write_bytes(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{pin}?recursive=1'))
    tree=json.loads(tp.read_text(encoding='utf8'));assert not tree.get('truncated')
    es={x['path']:x for x in tree['tree'] if x['type']=='blob'}
    paths={x['path'] for x in oldmf['files'] if x['path'] in es}
    paths|={p for p in es if p.startswith(('scripts/','webapp/')) and p.endswith(('.py','.js','.html','.sh','.yml'))}
    paths|={p for p in es if 'lhs214r' in p or p.endswith('AGENTS.md')}
    paths|={p for p in es if p in ('CLAUDE.md','docs/reviews/lhs214r_fix_plan_20261016.md')}
    if folder=='base':paths={p for p in paths if p.startswith(('scripts/','webapp/')) or p in ('AGENTS.md','CLAUDE.md')}
    caches=[R/folder,old/'source',old/'base',R.parent/'lhs214_failures_review_20261014/source',R.parent/'rint_g2_impl_reverify_20261015/source']
    def one(p):
        e=es[p]; b=None; reused=False
        for root in caches:
            q=long(root/p)
            if q.is_file():
                data=q.read_bytes()
                if blob(data)==e['sha']:b=data;reused=True;break
        if b is None:b=fetch(f'https://raw.githubusercontent.com/{REPO}/{pin}/'+urllib.parse.quote(p))
        assert blob(b)==e['sha'],p
        q=long(R/folder/p);q.parent.mkdir(parents=True,exist_ok=True)
        if q.exists():assert q.read_bytes()==b,p
        else:q.write_bytes(b)
        return {'path':p,'git_blob':e['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'reused':reused}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:rows=list(pool.map(one,sorted(paths)))
    (R/f'{folder}_manifest.json').write_text(json.dumps({'pin':pin,'repo':REPO,'files':rows},ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps({'folder':folder,'pin':pin,'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'reused':sum(x['reused'] for x in rows)}),flush=True)
