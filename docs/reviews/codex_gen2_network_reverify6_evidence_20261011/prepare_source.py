from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, shutil, tarfile
R=Path(__file__).resolve().parent
OLD=R.parent/'gen2_network_reverify5_20261007'
PIN='a20fc1875951bead5fad4a4d387e77b4979b84c6'
BASE='https://api.github.com/repos/yonghoon7153-source/Yonghoon-DEM-DFT/'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-read-only-review'}),timeout=90) as f:return f.read()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for name in ('source','evidence','probes','submitted','tmp','notes'):(R/name).mkdir(parents=True,exist_ok=True)
tree=json.loads(fetch(BASE+'git/trees/'+PIN+'?recursive=1'))
assert not tree.get('truncated')
(R/'tree.json').write_text(json.dumps(tree),encoding='utf8')
entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
paths={x['path'] for x in json.loads((OLD/'source_manifest.json').read_text()) if x['path'] in entries}
paths.update(p for p in entries if p.startswith('docs/reviews/codex_gen2_network_reverify6_precheck_20261009/'))
paths.update(p for p in entries if p.startswith('docs/reviews/codex_g2rr5_fix_probe_rerun_20261008/'))
paths.update(['docs/reviews/codex_gen2_network_reverify6_request_20261009.md','docs/reviews/codex_review_gen2_network_reverify5_20261007.md','docs/reviews/g2rr5_fix_plan_20261008.md','docs/reviews/lhs_network_batch_registration_20261007_g2.md','docs/reviews/lhs_supp_thick_registration_20261006.md','docs/reviews/lhs_v13_plan_20261006.md','docs/reviews/selftest_inventory.tsv'])
paths={p for p in paths if p in entries}
def get(p):
    e=entries[p];src=OLD/'source'/p;dest=R/'source'/p
    reused=src.is_file() and blob(src.read_bytes())==e['sha']
    b=src.read_bytes() if reused else fetch('https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'] and len(b)==e['size'],p
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    return dict(path=p,sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),reused=reused)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
archive=Path('C:/Users/Administrator/Downloads/g2rr6_956173e1c_1009_2113.tar.gz')
sha=hashlib.sha256(archive.read_bytes()).hexdigest();assert sha=='b147dcd5babefcad7897d7bba8dbe0ecbdffa3453edb96d45a86a2dd659a2cab'
shutil.copy2(archive,R/'submitted'/archive.name)
with tarfile.open(archive) as tf:
    ms=tf.getmembers();dest=R/'submitted'
    for m in ms:
        assert (dest/m.name).resolve().is_relative_to(dest.resolve()) and (m.isfile() or m.isdir()),m.name
    for m in ms:
        target=dest/m.name
        if m.isdir():target.mkdir(parents=True,exist_ok=True)
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            with tf.extractfile(m) as a,target.open('wb') as b:shutil.copyfileobj(a,b)
(R/'evidence/archive_inventory.json').write_text(json.dumps(dict(sha256=sha,entries=[dict(name=m.name,size=m.size) for m in ms]),indent=2),encoding='utf8')
shutil.copy2('C:/Users/Administrator/Downloads/codex_gen2_network_reverify6_request_20261009.md',R/'submitted/request.md')
print('PIN',PIN,'files',len(rows),'reused',sum(x['reused'] for x in rows),'new',sum(not x['reused'] for x in rows),'archive entries',len(ms),flush=True)
print('Changed/new:',json.dumps([x['path'] for x in rows if not x['reused']],ensure_ascii=False),flush=True)
