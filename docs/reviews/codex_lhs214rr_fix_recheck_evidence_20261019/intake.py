"""Read-only remote snapshot intake, hash verified; never invokes git."""
from pathlib import Path
import concurrent.futures, hashlib, json, os, time, urllib.request, urllib.parse, shutil
R=Path(__file__).resolve().parent
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
PIN='77d8fd44545c33cd10ab18fc250c7ad3023833ea'
OLD=R.parent/'lhs214r_fix_recheck_20261017'
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'read-only-review'}),timeout=45) as f:return f.read()
        except Exception:
            if i==3:raise
            time.sleep(i+1)
def jp(name,url):
    p=R/'evidence'/name
    if not p.exists():p.write_bytes(get(url))
    return json.loads(p.read_text(encoding='utf8'))
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for d in ['source','evidence','probes','notes','tmp','submitted']:(R/d).mkdir(parents=True,exist_ok=True)
shutil.copyfile('C:/Users/Administrator/.codex/attachments/76443b79-8dc0-4633-9dc6-445b46f995d8/붙여넣은 텍스트.txt',R/'submitted/request.txt')
c=jp('commit.json',f'https://api.github.com/repos/{REPO}/commits/{PIN}')
t=jp('tree.json',f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1');assert not t.get('truncated')
cmp=jp('compare_60ba.json',f'https://api.github.com/repos/{REPO}/compare/60ba39e22...{PIN}')
latest=jp('request_history.json',f'https://api.github.com/repos/{REPO}/commits?sha={PIN}&path=docs/reviews/codex_lhs214rr_fix_recheck_request_20261018.md&per_page=1')
print(json.dumps({'pin':PIN,'message':c['commit']['message'],'request_commit':latest[0]['sha'],'changed':[x['filename'] for x in cmp['files'] if x['filename'].startswith(('scripts/','webapp/'))]},ensure_ascii=False),flush=True)
es={e['path']:e for e in t['tree'] if e['type']=='blob'}
paths={x['path'] for x in json.loads((OLD/'source_manifest.json').read_text(encoding='utf8'))['files'] if x['path'] in es}
paths|={p for p in es if p.startswith(('scripts/','webapp/')) and p.endswith(('.py','.js','.html','.sh','.yml'))}
paths|={p for p in es if 'lhs214rr' in p or 'lhs214r_fix_evidence_20261016' in p or p.endswith('AGENTS.md')}
paths|={p for p in es if p in ('CLAUDE.md','docs/reviews/codex_review_lhs214r_fix_recheck_20261017.md','docs/reviews/codex_lhs214r_evidence_supplement_20261017.md')}
caches=[R/'source',OLD/'source',OLD/'base',R.parent/'lhs214r_supplement_a4a1e52c0_20261017/submitted/lhs214r_recheck_a4a1e52c0']
def one(p):
    b=None;reused=False
    for root in caches:
        q=long(root/p)
        if q.is_file():
            v=q.read_bytes()
            if blob(v)==es[p]['sha']:b=v;reused=True;break
    if b is None:b=get(f'https://raw.githubusercontent.com/{REPO}/{PIN}/'+urllib.parse.quote(p))
    assert blob(b)==es[p]['sha'],p
    q=long(R/'source'/p);q.parent.mkdir(parents=True,exist_ok=True)
    if q.exists():assert q.read_bytes()==b,p
    else:q.write_bytes(b)
    return {'path':p,'git_blob':es[p]['sha'],'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'reused':reused}
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:rows=list(pool.map(one,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps({'pin':PIN,'files':rows},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'files':len(rows),'bytes':sum(x['bytes'] for x in rows),'reused':sum(x['reused'] for x in rows)}),flush=True)
