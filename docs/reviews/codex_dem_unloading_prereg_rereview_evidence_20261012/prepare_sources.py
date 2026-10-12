from pathlib import Path
import concurrent.futures,hashlib,json,urllib.request,urllib.parse,shutil
R=Path(__file__).resolve().parent;OLD=R.parent/'dem_unloading_review_20261011'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT';REQ='docs/reviews/codex_dem_unloading_prereg_rereview_request_20261011.md';REG='docs/reviews/dem_unloading_ps45_prereg_20261009.md'
UP='3d5c00f20519e6bb6eb6756f51f1ad36564e649d'
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-readonly-unloading-rereview'}),timeout=45) as f:return f.read()
def h(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
commits=json.loads(fetch('https://api.github.com/repos/'+REPO+'/commits?sha=claude%2Fstoic-knuth-NObVQ&path='+urllib.parse.quote(REQ,safe='')+'&per_page=3'))
pin=commits[0]['sha'];(R/'evidence/request_commits.json').write_text(json.dumps(commits,ensure_ascii=False,indent=2),encoding='utf8')
tree=json.loads(fetch('https://api.github.com/repos/'+REPO+'/git/trees/'+pin+'?recursive=1'))
(R/'tree.json').write_text(json.dumps(tree,ensure_ascii=False,indent=2),encoding='utf8')
ent={x['path']:x for x in tree['tree'] if x['type']=='blob'}
oldm=json.loads((OLD/'source_manifest.json').read_text(encoding='utf8'))
paths={x['path'] for x in oldm['files']}|{REQ,REG,'docs/reviews/dem_unloading_ul_fix_plan_20261011.md','docs/reviews/codex_review_dem_unloading_prereg_20261011.md'}
def get(p):
    e=ent[p];prev=OLD/'source'/p
    reuse=prev.exists() and blob(prev.read_bytes())==e['sha']
    b=prev.read_bytes() if reuse else fetch('https://raw.githubusercontent.com/'+REPO+'/'+pin+'/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'],p
    dst=R/'source'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return {'path':p,'blob_sha':e['sha'],'sha256':h(b),'bytes':len(b),'reused':reuse}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:files=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps({'pin':pin,'files':files},ensure_ascii=False,indent=2),encoding='utf8')
upfiles={p.name for p in (OLD/'upstream').glob('*') if p.is_file()}|{'dump_custom.cpp','dump_custom.h','dump.cpp','write_dump.cpp','run.cpp','dump_local.cpp','write_restart.cpp','normal_model_hooke.h','surface_model_default.h','rolling_model_cdt.h'}
def getup(p):
    prev=OLD/'upstream'/p;reused=prev.exists()
    try:b=prev.read_bytes() if reused else fetch('https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/'+UP+'/src/'+p)
    except Exception as ex:return {'path':p,'error':str(ex)}
    dst=R/'upstream'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return {'path':p,'sha256':h(b),'bytes':len(b),'reused':reused}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:up=list(pool.map(getup,sorted(upfiles)))
(R/'upstream_manifest.json').write_text(json.dumps({'pin':UP,'files':up},indent=2),encoding='utf8')
receipt={'pin':pin,'upstream_pin':UP,'request_date':commits[0]['commit']['committer']['date'],
 'request_attachment_equals_pin':(R/'submitted/request.md').read_bytes()==(R/'source'/REQ).read_bytes(),
 'prereg_attachment_equals_pin':(R/'submitted/prereg.md').read_bytes()==(R/'source'/REG).read_bytes(),
 'attachment_sha256':{p.name:h(p.read_bytes()) for p in (R/'submitted').glob('*.md')},
 'source_files':len(files),'upstream_files':len(up),'upstream_errors':[x for x in up if 'error' in x]}
(R/'evidence/pin_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False))
