"""Fetch immutable review inputs; never alter a checkout."""
from pathlib import Path
import concurrent.futures, hashlib, json, shutil, urllib.parse, urllib.request
R=Path(__file__).resolve().parent
OLD=R.parent/'dem_unloading_kit_reverify_20261014'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'
PIN='eaecfba2a2dfbff6f13222f6afeb01d8ebeb5a84'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-readonly-review'}),timeout=60) as f: return f.read()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for d in ('source','notes','probes','evidence','submitted','tmp'): (R/d).mkdir(exist_ok=True)
tree=json.loads(fetch(f'https://api.github.com/repos/{REPO}/git/trees/{PIN}?recursive=1'))
assert not tree.get('truncated')
(R/'tree.json').write_text(json.dumps(tree,indent=2),encoding='utf-8')
ent={e['path']:e for e in tree['tree'] if e['type']=='blob'}
paths={x['path'] for x in json.loads((OLD/'source_manifest.json').read_text(encoding='utf-8'))['files'] if x['path'] in ent}
paths|={p for p in ent if p.startswith(('docs/data/ps45_unload_20261009/','docs/reviews/dem_unloading_kit_reverify_fix_evidence_20261014/'))}
paths|={p for p in ent if p.startswith('docs/reviews/') and p.count('/')==2 and 'unloading' in p and p.endswith('.md')}
def get(p):
    prev=OLD/'source'/p
    b=prev.read_bytes() if prev.exists() else b''
    if blob(b)!=ent[p]['sha']: b=fetch(f'https://raw.githubusercontent.com/{REPO}/{PIN}/'+urllib.parse.quote(p))
    assert blob(b)==ent[p]['sha'],p
    dst=R/'source'/p
    if dst.exists(): assert dst.read_bytes()==b,p
    else:
        dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return dict(path=p,blob_sha=ent[p]['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: files=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,files=files),indent=2),encoding='utf-8')
shutil.copyfile('C:/Users/Administrator/Downloads/codex_dem_unloading_kit_reverify_fix_recheck_request_20261014.md',R/'submitted/request.md')
shutil.copyfile(OLD/'codex_review_dem_unloading_kit_reverify_20261014.md',R/'submitted/previous_verdict.md')
print(json.dumps(dict(pin=PIN,files=len(files),bytes=sum(e['bytes'] for e in files))))
