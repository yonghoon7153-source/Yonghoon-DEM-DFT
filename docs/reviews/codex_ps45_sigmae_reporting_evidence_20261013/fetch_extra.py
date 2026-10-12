from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request
R=Path(__file__).resolve().parent
PIN='46cd0bdb872e7d6c85ca50ec4172e98377253130'
tree={x['path']:x for x in json.loads((R/'code_tree.json').read_text(encoding='utf8'))['tree'] if x['type']=='blob'}
paths=[p for p in tree if p.startswith('dem_scripts/ps_sweep_6mah_20260914/in.ps_') and p.endswith('_r45.liggghts')]
paths += [p for p in tree if p.startswith('docs/data/ps45_dh_transfer_20260926/kits/') and p.endswith('__am_scaffold.csv.gz')]
paths += ['scripts/build_ps45_kits.py']
def get(p):
    req=urllib.request.Request('https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'+p,headers={'User-Agent':'read-only-review'})
    b=urllib.request.urlopen(req,timeout=40).read()
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert blob==tree[p]['sha'],p
    f=R/'source'/p;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
    return {'path':p,'bytes':len(b),'git_blob':blob,'sha256':hashlib.sha256(b).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as p: rows=list(p.map(get,paths))
(R/'evidence/extra_source_manifest.json').write_text(json.dumps({'pin':PIN,'files':rows},indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
