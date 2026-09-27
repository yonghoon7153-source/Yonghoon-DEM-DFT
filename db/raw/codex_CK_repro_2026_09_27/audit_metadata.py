"""Read-only CI identity/geometry/native-selftest audit. Requires numpy and ASE.
Run: python audit_metadata.py --source CHECKOUT --prompt CI_PROMPT [--previous CG_CHECKOUT]
No VASP/UMA/QE execution. The native selftest needs simple-dftd3 and bash.
"""
import argparse, contextlib, hashlib, importlib.util, io, json, re, sys
from pathlib import Path
import numpy as np
from ase.io import read
ap=argparse.ArgumentParser()
ap.add_argument('--source',type=Path,required=True)
ap.add_argument('--prompt',type=Path,required=True)
ap.add_argument('--previous',type=Path)
a=ap.parse_args();src=a.source.resolve();pkg=src/'db/inputs/wad_aprime_v5_vasp_2026_09_27'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('ci_meta',src/'tools/wad/build_v5_vasp_package.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out={}
declared=re.findall(r'^((?:db|tools|kb)/\S+)\s+([0-9a-f]{64})$',a.prompt.read_text(encoding='utf-8'),re.M)
out['declared_hashes']={p:sha(src/p)==h for p,h in declared}
meta=json.loads((pkg/'jobs.json').read_text())
out['generated_runner_matches']=(pkg/'run_all.sh').read_text()==m.run_all_text()
out['tool_hash_matches']=sha(src/'tools/wad/build_v5_vasp_package.py')==meta['tool_sha256']
out['geometry']=[]
for j in meta['jobs']:
    original=src/meta['source_package']/'structures'/(j['structure']+'.extxyz')
    at=read(original);vs=read(pkg/'jobs'/j['dir']/'POSCAR',format='vasp')
    _,order,_=m.poscar_text(at,'review')
    out['geometry'].append({'job':j['dir'],'source_sha_ok':sha(original)==j['structure_sha256'],
      'max_pos_diff_A':float(np.max(np.abs(at.positions[order]-vs.positions))),
      'max_cell_diff_A':float(np.max(np.abs(at.cell.array-vs.cell.array))),
      'order_ok':order==j['poscar_order_to_original_index']})
if a.previous:
    old=a.previous/'db/inputs/wad_aprime_v5_vasp_2026_09_27'
    paths=[p.relative_to(pkg).as_posix() for p in (pkg/'jobs').rglob('*') if p.is_file()]
    oldmeta=json.loads((old/'jobs.json').read_text())
    oldj={j['dir']:j for j in oldmeta['jobs']}
    out['cg_comparison']={'inputs':len(paths),'changed_inputs':[p for p in paths if sha(pkg/p)!=sha(old/p)],
      'd3_changed':[j['dir'] for j in meta['jobs'] if j['d3_2body_eV_ref']!=oldj[j['dir']]['d3_2body_eV_ref']]}
log=io.StringIO()
try:
    with contextlib.redirect_stdout(log): rc=m._selftest()
    out['native_selftest']={'rc':rc,'log':log.getvalue()}
except Exception as e:
    out['native_selftest']={'not_completed':repr(e),'log':log.getvalue()}
Path(__file__).with_name('metadata_ci.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=False,indent=2))
