from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request, urllib.parse, shutil
R=Path(__file__).resolve().parent
PIN='a20fc1875951bead5fad4a4d387e77b4979b84c6'
UP='3d5c00f20519e6bb6eb6756f51f1ad36564e649d'
def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Codex-readonly-unloading-review'}),timeout=90) as f:return f.read()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for n in ['source','upstream','evidence','notes','probes']:(R/n).mkdir(parents=True,exist_ok=True)
tree=json.loads((R.parent/'gen2_network_reverify6_20261011/tree.json').read_text())
entries={e['path']:e for e in tree['tree'] if e['type']=='blob'}
prefixes=['docs/reviews/dem_unloading_ps45_','docs/data/ps73_compaction_curve_20261006/','docs/data/ps73_damping_branch_20261007/','docs/data/ps45_plane_load_20261007/','docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/']
exact=['docs/reviews/codex_dem_unloading_prereg_request_20261009.md','docs/reviews/codex_review_springback_loadshare_20261009.md','docs/resume_ckpt_procedure_20260927.md','scripts/plane_load_share.py','scripts/resume_ckpt.sh','CLAUDE.md','AGENTS.md','docs/reviews/codex_ps45_porosity_evidence_20261001/reference/normal_model_hooke_hysteresis.h']
paths=[p for p in entries if p in exact or (any(p.startswith(s) for s in prefixes) and not any(s in p for s in ['/previews/','/render3d','/origin/']) and not p.endswith(('.png','.svg','.tgz')))]
paths+=['docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz']
def get(p):
    e=entries[p];dest=R/'source'/p
    if dest.is_file() and blob(dest.read_bytes())==e['sha']:b=dest.read_bytes()
    else:
        b=fetch('https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/'+PIN+'/'+urllib.parse.quote(p));assert blob(b)==e['sha'],p
        dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
    return dict(path=p,blob_sha=e['sha'],sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:rows=list(pool.map(get,sorted(set(paths))))
(R/'source_manifest.json').write_text(json.dumps(dict(pin=PIN,files=rows),ensure_ascii=False,indent=2),encoding='utf8')
upfiles=['normal_model_hooke_hysteresis.h','pair_gran.cpp','pair_gran.h','fix_contact_history.cpp','fix_contact_history.h','fix_contact_history_mesh.cpp','fix_contact_history_mesh.h','fix_wall_gran.cpp','fix_wall_gran.h','fix_mesh.cpp','fix_mesh_surface.cpp','fix_mesh_surface.h','fix_mesh_surface_stress.cpp','fix_move_mesh.cpp','fix_move_mesh.h','compute_pair_gran_local.cpp','compute_pair_gran_local.h','fix_gravity.cpp','fix_viscous.cpp','modify.cpp','read_restart.cpp','verlet.cpp','tangential_model_history.h','fix_property_atom.cpp','mesh_mover_linear.h','mesh_mover.h','contact_models.h','contact_interface.h']
def getup(p):
    dest=R/'upstream'/p
    try:
        b=dest.read_bytes() if dest.exists() else fetch('https://raw.githubusercontent.com/CFDEMproject/LIGGGHTS-PUBLIC/'+UP+'/src/'+p)
        dest.write_bytes(b);return dict(path=p,sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
    except Exception as ex:return dict(path=p,error=str(ex))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:ur=list(pool.map(getup,upfiles))
(R/'upstream_manifest.json').write_text(json.dumps(dict(pin=UP,files=ur),indent=2),encoding='utf8')
shutil.copy2('C:/Users/Administrator/Downloads/codex_dem_unloading_prereg_request_20261009.md',R/'submitted_request.md')
print(json.dumps(dict(pin=PIN,repo_files=len(rows),repo_bytes=sum(x['bytes'] for x in rows),upstream_files=len(ur),errors=[x for x in ur if 'error' in x]),indent=2))
