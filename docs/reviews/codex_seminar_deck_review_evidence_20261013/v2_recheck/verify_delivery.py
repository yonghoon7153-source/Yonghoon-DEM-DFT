"""Saved-output verification only; no DEM/MPM/network/FV solver execution."""
from pathlib import Path
import hashlib, json, subprocess, sys, shutil, csv
R=Path(__file__).resolve().parent
O=R.parent/'seminar_review_20261013'
I=R/'input/docs/seminar_20261013'
S=O/'sources/code'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
data=json.loads((R/'evidence/pptx.json').read_text(encoding='utf8'))
oldfigs=R.parent/'seminar_review_v3_20261013/v3/docs/seminar_20261013/figs'
csvchecks={p.name:{'old_sha256':sha(oldfigs/p.name),'new_sha256':sha(p),'byte_identical':p.read_bytes()==(oldfigs/p.name).read_bytes()} for p in (I/'figs').glob('*.csv')}
assert all(x['byte_identical'] for x in csvchecks.values())
media={m['sha256'] for m in data['slides'][14]['media']}
images={n:{'sha256':sha(S/f'docs/report_20261021/previews/{n}.png'),'present_in_slide15':sha(S/f'docs/report_20261021/previews/{n}.png') in media} for n in ['G5a','G3']}
assert all(x['present_in_slide15'] for x in images.values())
counts={}
for group in ['lhs','lhsx']:
    path=S/f'docs/data/lhs_release_20261006_v12/{group}_release_20261006_v12.csv'
    rows=list(csv.DictReader(path.open(encoding='utf8')))
    tau=[float(x['tortuosity_SE_wall']) for x in rows if x['tortuosity_SE_wall']]
    counts[group]={'rows':len(rows),'finite_tau':len(tau),'tau_min':min(tau),'tau_max':max(tau)}
actual='\n'.join('\n'.join(s['texts']+s['notes']) for s in data['slides'])
markers=[{'slide':s['slide'],'text':t} for s in data['slides'] for t in s['texts'] if t.startswith('Figure pending:')]
assert len(markers)==5
mathrun=subprocess.run([sys.executable,'-X','utf8','-B',str(O/'verify_results.py')],capture_output=True,text=True,encoding='utf8',check=True)
(R/'evidence/arithmetic_rerun.txt').write_text(mathrun.stdout,encoding='utf8')
selected=[
 'docs/reviews/fam_platen_prereg_20260812.md','docs/mpm3d_calibration.md','CLAUDE.md',
 'docs/data/ps45_r45_network_g2_20261007/README.md',
 'docs/data/lhs_release_20261006_v12/lhs_release_20261006_v12.csv',
 'docs/data/lhs_release_20261006_v12/lhsx_release_20261006_v12.csv',
 'docs/report_20261021/summary.json','docs/report_20261021/previews/G3.png','docs/report_20261021/previews/G5a.png']
source_manifest=[]
for relative in selected:
    p=S/relative;dst=R/'references/code'/relative;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
    source_manifest.append({'path':dst.relative_to(R).as_posix(),'sha256':sha(p),'source_code_pin':'a0439bdf8156236f454bd3f8b5bf4d044e127039'})
lp=O/'sources/lit/litdb/papers/bazzoun2026_dem_fem_rnm_ionic.md'
dst=R/'references/lit'/lp.name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(lp,dst)
source_manifest.append({'path':dst.relative_to(R).as_posix(),'sha256':sha(lp),'source_lit_pin':'6e568c4f0bb7df299959fd0e77e349838ad8ac98'})
out={'unchanged_F2_F3_F4_csv':csvchecks,'slide15_exact_reused_images':images,'cohort_counts':counts,'figure_pending_count':len(markers),'figure_pending':markers,'independent_arithmetic_returncode':mathrun.returncode,'source_manifest':source_manifest,'scope':'Saved-artifact and arithmetic checks. No solver run; DFT source tensors not available; no native PowerPoint rendering.'}
(R/'evidence/recheck_proof.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in out.items() if k!='source_manifest'},ensure_ascii=False,indent=2))
