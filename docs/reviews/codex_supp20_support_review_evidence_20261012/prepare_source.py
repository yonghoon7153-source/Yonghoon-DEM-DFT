from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, urllib.parse, difflib
R=Path(__file__).resolve().parent
OLD=R.parent/'gen2_network_reverify7_20261012'
REF='b429c3c1d'
BASE='3cedd40a5911d0606bf33ed2085d5cb93c4db2e0'
API='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
RAW='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-read-only-review'}),timeout=90) as f:return f.read()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for n in ('source','evidence','probes','notes','submitted','tmp','baseline'):(R/n).mkdir(parents=True,exist_ok=True)
commit=json.loads(fetch(API+'commits/'+REF));PIN=commit['sha']
tree=json.loads(fetch(API+'git/trees/'+PIN+'?recursive=1'));assert not tree.get('truncated')
compare=json.loads(fetch(API+'compare/'+BASE+'...'+PIN))
for name,value in [('commit',commit),('tree',tree),('compare',compare)]:
    (R/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf8')
entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
old=json.loads((OLD/'source_manifest.json').read_text())
paths={e['path'] for e in old['files'] if e['path'] in entries}
paths.update(e['filename'] for e in compare['files'] if e['filename'] in entries)
paths.update(p for p in entries if p.startswith(('docs/data/lhs_supp','docs/data/lhss','docs/data/lhsx_design','docs/data/lhs_design')))
paths.update(p for p in entries if p.startswith('scripts/') and ('supp' in p or 'lhss' in p))
paths.update(p for p in entries if p.startswith('docs/reviews/') and (('supp20' in p) or ('reverify7' in p and p.endswith('.md'))))
def get(p):
    e=entries[p];src=OLD/'source'/p;dst=Path('\\\\?\\'+str(R/'source'/p))
    reuse=src.is_file() and blob(src.read_bytes())==e['sha']
    b=src.read_bytes() if reuse else fetch(RAW+PIN+'/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'] and len(b)==e['size'],p
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reuse)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,base=BASE,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
for p in sorted(paths):
    if p.startswith('scripts/') and (OLD/'source'/p).is_file() and (OLD/'source'/p).read_bytes()!=(R/'source'/p).read_bytes():
        dst=R/'baseline'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((OLD/'source'/p).read_bytes())
        patch=''.join(difflib.unified_diff(dst.read_text(encoding='utf8').splitlines(True),(R/'source'/p).read_text(encoding='utf8').splitlines(True),fromfile=BASE+'/'+p,tofile=PIN+'/'+p))
        (R/'evidence'/(Path(p).stem+'.diff')).write_text(patch,encoding='utf8')
attachment=Path('C:/Users/Administrator/Downloads/codex_supp20_support_review_request_20261012.md')
(R/'submitted/request.md').write_bytes(attachment.read_bytes())
receipt=dict(pin=PIN,base=BASE,files=len(rows),reused=sum(r['reused'] for r in rows),attachment_sha256=hashlib.sha256(attachment.read_bytes()).hexdigest(),changed_paths=[e['filename'] for e in compare['files']])
(R/'evidence/pin_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False))
