"""Read-only review intake: verified archive, then immutable pinned Git blobs."""
from pathlib import Path, PurePosixPath
import concurrent.futures, hashlib, json, os, stat, urllib.request, urllib.parse, time, sys
R=Path(__file__).resolve().parent
W=R.parent
PIN='0b3012460fb8e8b7d53484b0efe399e2dc506aec'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
ARCHIVE=Path('C:/Users/Administrator/Downloads/codex_rint2_rereview_0b3012460.zip')
def long(p):
    s=str(p.absolute())
    return Path(s if s.startswith('\\\\?\\') else '\\\\?\\'+s) if os.name=='nt' else p
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(p,b):
    p=long(p); p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists(): assert p.read_bytes()==b,str(p)
    else: p.write_bytes(b)
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Pinned-read-only-review'}),timeout=45) as f: return f.read()
        except Exception:
            if i==3: raise
            time.sleep(i+1)
def meta(name,url):
    p=R/'evidence'/name
    if not p.exists(): save(p,get(url))
    return json.loads(p.read_text(encoding='utf8'))
for d in ('repo','source','evidence','probes','tmp'): (R/d).mkdir(exist_ok=True)
if '--zip' in sys.argv:
    import zipfile
    with zipfile.ZipFile(ARCHIVE) as z:
        seen=set()
        for i in z.infolist():
            p=PurePosixPath(i.filename)
            assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
            assert not stat.S_ISLNK(i.external_attr>>16)
            assert i.filename.casefold() not in seen
            seen.add(i.filename.casefold())
            if not i.is_dir(): save(R/'repo'/i.filename,z.read(i))
        rows=[]
        for line in z.read('MANIFEST.sha256').decode('utf8').splitlines():
            if not line.strip(): continue
            sha,p=line.split(None,1); p=p.strip().lstrip('*')
            b=z.read(p); assert hashlib.sha256(b).hexdigest()==sha,p
            rows.append(dict(path=p,sha256=sha,bytes=len(b)))
    summary=dict(zip_sha256=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),manifest_count=len(rows),files=rows)
    save(R/'evidence/zip_integrity.json',json.dumps(summary,indent=2).encode())
    print(json.dumps({k:v for k,v in summary.items() if k!='files'}))
    sys.exit()
c=meta('commit.json',f'https://api.github.com/repos/{REPO}/commits/{PIN}'); assert c['sha']==PIN
t=meta('tree.json',f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1'); assert not t.get('truncated')
es={e['path']:e for e in t['tree'] if e['type']=='blob'}
old=json.loads((W/'rint2_carbon_design_review_20261021/source_manifest.json').read_text(encoding='utf8'))
paths={e['path'] for e in old['files'] if e['path'] in es}
paths|={p for p in es if p.endswith('AGENTS.md') or p=='CLAUDE.md'}
paths|={p for p in es if p.startswith('scripts/') and p.endswith('.py')}
paths|={p for p in es if p.startswith('docs/reviews/') and any(q in p for q in ('rint_carbon','rint2_','step3_conv'))}
rows=json.loads((R/'evidence/zip_integrity.json').read_text())['files']
paths|={e['path'] for e in rows if e['path'] in es}
paths&=es.keys()
caches=[R/'source',R/'repo',W/'rint2_carbon_design_review_20261021/source']
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
    save(R/'source'/p,b)
    return dict(path=p,git_blob=es[p]['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reused)
print(json.dumps(dict(pin=PIN,files=len(paths))),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool: out=list(pool.map(one,sorted(paths)))
checks=[]
for e in rows:
    p=e['path']
    checks.append(dict(path=p,in_pin=p in es,same=p in es and blob(long(R/'repo'/p).read_bytes())==es[p]['sha']))
save(R/'evidence/zip_pin_comparison.json',json.dumps(checks,indent=2).encode())
save(R/'source_manifest.json',json.dumps(dict(pin=PIN,files=out),indent=2).encode())
print(json.dumps(dict(files=len(out),bytes=sum(e['bytes'] for e in out),reused=sum(e['reused'] for e in out),zip_mismatches=[e for e in checks if not e['same']])),flush=True)
