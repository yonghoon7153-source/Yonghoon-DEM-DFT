from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request
R=Path(__file__).resolve().parent
PIN='e739c9730f8758d2d61b2db22d940ee9a2440897'
tree={e['path']:e for e in json.loads((R/'lit_tree.json').read_text(encoding='utf8'))['tree'] if e['type']=='blob'}
groups={
 'wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni':['fig_1.png','fig_4.png','fig_S2.png','fig_S8.png','figures.json'],
 'asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity':['fig_1.png','fig_3.png','fig_4.png','tab_1.png','tab_2.png','figures.json'],
 'minnmann2021_jes_charge_transport_bottlenecks':['fig_2.png','tab_S1.png','tab_S2.png','tab_S5.png','figures.json']}
def get(path):
    entry=tree[path]
    url='https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'+path
    with urllib.request.urlopen(url,timeout=35) as f:raw=f.read()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==entry['sha']
    dst=R/'literature_figures'/path;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
    print(path,flush=True)
    return {'path':path,'url':url,'bytes':len(raw),'sha':entry['sha'],'sha256':hashlib.sha256(raw).hexdigest()}
paths=['litdb/figures/'+slug+'/'+name for slug,names in groups.items() for name in names]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,paths))
(R/'evidence/literature_figures_manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
