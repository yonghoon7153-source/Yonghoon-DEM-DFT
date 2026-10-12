from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, urllib.parse, shutil, difflib
R=Path(__file__).resolve().parent
OLD=R.parent/'gen2_network_reverify6_20261011'
PIN='3cedd40a5911d0606bf33ed2085d5cb93c4db2e0'
FIX='ec9c51149'; PARENT='821f0e151'
API='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
RAW='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-read-only-review'}),timeout=90) as f:return f.read()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for n in ('source','evidence','probes','notes','submitted','tmp','parent'):(R/n).mkdir(parents=True,exist_ok=True)
tree=json.loads(fetch(API+'git/trees/'+PIN+'?recursive=1'));assert not tree.get('truncated')
(R/'tree.json').write_text(json.dumps(tree),encoding='utf8')
entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
old=json.loads((OLD/'source_manifest.json').read_text())
paths={e['path'] for e in old['files'] if e['path'] in entries}
paths.update(p for p in entries if p.startswith('docs/reviews/codex_gen2_network_reverify6_evidence_20261011/'))
paths.update(['docs/reviews/codex_gen2_network_reverify7_request_20261011.md','docs/reviews/codex_review_gen2_network_reverify6_20261011.md','docs/reviews/g2rr6_fix_plan_20261011.md'])
def get(p):
    e=entries[p];src=OLD/'source'/p;dst=Path('\\\\?\\'+str(R/'source'/p))
    reuse=src.is_file() and blob(src.read_bytes())==e['sha']
    b=src.read_bytes() if reuse else fetch(RAW+PIN+'/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'] and len(b)==e['size'],p
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reuse)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
for ref in (PIN,FIX,PARENT):
    (R/'evidence'/('commit_'+ref+'.json')).write_bytes(fetch(API+'commits/'+ref))
compare=json.loads(fetch(API+'compare/'+old['pin']+'...'+PIN))
(R/'evidence/compare_r6_r7.json').write_text(json.dumps(compare,ensure_ascii=False,indent=2),encoding='utf8')
for p in ('scripts/g2_network_reread.py','scripts/wsl_network_smoke.py'):
    b=fetch(RAW+PARENT+'/'+p);dst=R/'parent'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    patch=''.join(difflib.unified_diff(b.decode().splitlines(True),(R/'source'/p).read_text(encoding='utf8').splitlines(True),fromfile=PARENT+'/'+p,tofile=PIN+'/'+p))
    (R/'evidence'/(Path(p).stem+'.diff')).write_text(patch,encoding='utf8')
attachment=Path('C:/Users/Administrator/Downloads/codex_gen2_network_reverify7_request_20261011.md')
shutil.copy2(attachment,R/'submitted/request.md')
rp=R/'source/docs/reviews/codex_gen2_network_reverify7_request_20261011.md'
assert attachment.read_bytes()==rp.read_bytes()
receipt=dict(pin=PIN,attachment_sha256=hashlib.sha256(attachment.read_bytes()).hexdigest(),files=len(rows),reused=sum(r['reused'] for r in rows),changed_paths=[e['filename'] for e in compare['files']])
(R/'evidence/pin_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False))
