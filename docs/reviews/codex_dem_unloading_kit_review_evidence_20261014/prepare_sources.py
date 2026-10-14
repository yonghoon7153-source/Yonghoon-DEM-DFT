from pathlib import Path
import concurrent.futures,hashlib,json,urllib.request,urllib.parse,shutil
R=Path(__file__).resolve().parent; OLD=R.parent/'dem_unloading_rereview_20261012'
REPO='yonghoon7153-source/Yonghoon-DEM-DFT'; PIN='2783061ea'; UP='3d5c00f20519e6bb6eb6756f51f1ad36564e649d'
def fetch(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Codex-readonly-unloading-kit-review'}),timeout=60) as f:return f.read()
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for d in ['source','upstream','evidence','notes','probes','submitted']:(R/d).mkdir(exist_ok=True)
commit=json.loads(fetch('https://api.github.com/repos/'+REPO+'/commits/'+PIN));pin=commit['sha']
(R/'evidence/pin_commit.json').write_text(json.dumps(commit,ensure_ascii=False,indent=2),encoding='utf8')
tree=json.loads(fetch('https://api.github.com/repos/'+REPO+'/git/trees/'+pin+'?recursive=1'));assert not tree.get('truncated')
(R/'tree.json').write_text(json.dumps(tree,ensure_ascii=False,indent=2),encoding='utf8');ent={x['path']:x for x in tree['tree'] if x['type']=='blob'}
paths={x['path'] for x in json.loads((OLD/'source_manifest.json').read_text(encoding='utf8'))['files'] if x['path'] in ent}
paths|={p for p in ent if p.startswith(('docs/data/ps45_unload_20261009/','docs/reviews/dem_unloading_history_test_20261014/'))}
paths|={p for p in ent if p.startswith('docs/reviews/') and ('unloading' in p) and p.endswith('.md') and p.count('/')==2}
paths|={p for p in ent if p=='AGENTS.md' or p.endswith('/AGENTS.md') and (p.startswith('docs/') or p.startswith('scripts/'))}
for p in sorted(paths): (R/'source'/p).parent.mkdir(parents=True,exist_ok=True)
def get(p):
    e=ent[p];prev=OLD/'source'/p;reuse=prev.exists() and blob(prev.read_bytes())==e['sha']
    b=prev.read_bytes() if reuse else fetch('https://raw.githubusercontent.com/'+REPO+'/'+pin+'/'+urllib.parse.quote(p))
    assert blob(b)==e['sha'],p
    dst=R/'source'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(b)
    return {'path':p,'blob_sha':e['sha'],'sha256':sha(b),'bytes':len(b),'reused':reuse}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:files=list(pool.map(get,sorted(paths)))
(R/'source_manifest.json').write_text(json.dumps({'pin':pin,'files':files},ensure_ascii=False,indent=2),encoding='utf8')
upfiles={p.name for p in (OLD/'upstream').glob('*') if p.is_file()}|{'input.cpp','input.h','dump.cpp','dump_local.cpp','fix_ave_time.cpp','fix_ave_time.h','output.cpp','variable.cpp','mesh_mover_linear.h','mesh_mover.h','fix_move_mesh.cpp','fix_mesh_surface.cpp'}
def getup(p):
    prev=OLD/'upstream'/p
    b=prev.read_bytes() if prev.exists() else fetch('https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/'+UP+'/src/'+p)
    dst=R/'upstream'/p;dst.write_bytes(b)
    return {'path':p,'sha256':sha(b),'bytes':len(b)}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:up=list(pool.map(getup,sorted(upfiles)))
(R/'upstream_manifest.json').write_text(json.dumps({'pin':UP,'files':up},indent=2),encoding='utf8')
shutil.copyfile(Path('C:/Users/Administrator/.codex/attachments/dc318746-6524-4bf8-9429-d9f4eee8efe5/붙여넣은 텍스트.txt'),R/'submitted/request.txt')
print(json.dumps({'pin':pin,'files':len(files),'upstream':len(up),'history_evidence':[x for x in files if 'dem_unloading_history_test_20261014/' in x['path']]},ensure_ascii=False,indent=2))
