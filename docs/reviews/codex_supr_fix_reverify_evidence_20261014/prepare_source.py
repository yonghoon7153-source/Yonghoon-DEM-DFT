from pathlib import Path
import concurrent.futures
import difflib
import hashlib
import json
import urllib.request
import urllib.parse

R=Path(__file__).resolve().parent
OLD=R.parent/'sup20_fix_reverify_20261014'
SHORT='df647d4e3'
BASE='a9422d2e772f28417a6e0a5167aaab8d987bf27a'
API='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
RAW='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-read-only-review'}),timeout=90) as f:return f.read()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for n in ('source','baseline','evidence','probes','notes','submitted','tmp'):(R/n).mkdir(parents=True,exist_ok=True)
commit=json.loads(fetch(API+'commits/'+SHORT));PIN=commit['sha'];assert PIN.startswith(SHORT)
tree=json.loads(fetch(API+'git/trees/'+PIN+'?recursive=1'));assert not tree.get('truncated')
compare=json.loads(fetch(API+'compare/'+BASE+'...'+PIN))
for n,v in [('pin_commit',commit),('tree',tree),('compare',compare)]:
    (R/'evidence'/(n+'.json')).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf8')
entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
old=json.loads((OLD/'source_manifest.json').read_text())
paths={e['path'] for e in old['files'] if e['path'] in entries}
paths.update(['docs/reviews/codex_supr_fix_reverify_request_20261014.md','docs/reviews/supr_fix_plan_20261014.md',
 'docs/reviews/codex_review_sup20_fix_reverify_20261014.md'])
paths.update(p for p in entries if p.startswith('docs/reviews/codex_sup20_fix_reverify_evidence_20261014/evidence/receipt_extra/'))
def get(p):
    e=entries[p];src=Path('\\\\?\\'+str(OLD/'source'/p));dst=Path('\\\\?\\'+str(R/'source'/p))
    b=src.read_bytes() if src.is_file() else b''
    reuse=blob(b)==e['sha']
    if not reuse:b=fetch(RAW+PIN+'/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'] and len(b)==e['size'],p
    dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reuse)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,base=BASE,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
for p in ['scripts/run_network_194_parallel.py','scripts/supp20_input_receipt.py',
 'docs/reviews/lhs_network_batch_registration_20261012_supp20.md','docs/reviews/lhs_network_batch_registration_20261007_g2.md']:
    b=(OLD/'source'/p).read_bytes();dst=R/'baseline'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    patch=''.join(difflib.unified_diff(b.decode('utf8').splitlines(True),(R/'source'/p).read_text(encoding='utf8').splitlines(True),fromfile=BASE+'/'+p,tofile=PIN+'/'+p))
    (R/'evidence'/(Path(p).stem+'.diff')).write_text(patch,encoding='utf8')
(R/'submitted/request.txt').write_bytes(Path('C:/Users/Administrator/.codex/attachments/6979eb4d-1a0b-431f-8098-d16a80c47739/붙여넣은 텍스트.txt').read_bytes())
print(json.dumps(dict(pin=PIN,files=len(rows),reused=sum(r['reused'] for r in rows)),ensure_ascii=False))
