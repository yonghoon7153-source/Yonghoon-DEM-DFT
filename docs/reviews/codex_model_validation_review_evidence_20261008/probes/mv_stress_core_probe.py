"""Synthetic post-processing controls only; never runs the DEM engine."""
from pathlib import Path
import copy
import contextlib
import io
import json
import sys
import tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'tmp').mkdir(exist_ok=True)
(ROOT / 'evidence').mkdir(exist_ok=True)
tempfile.tempdir = str((ROOT / 'tmp').resolve())
# Optional review-machine dependency cache. A distributed package uses its
# installed Python environment; this sibling folder is never required/shipped.
review_deps = ROOT.parent / 'lhs_coverage_review_20260930/deps'
if review_deps.is_dir():
    sys.path.insert(0, str(review_deps))
sys.path.insert(0, str(ROOT / 'source/scripts'))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import dem_analysis_core as core
import plane_load_share as pls

out = {'scope': 'Synthetic inputs to actual pinned post-processing code; not a raw data reconstruction.'}
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    passed = pls.selftest()
out['plane_load_share_selftest'] = {'passed': passed, 'output': buf.getvalue()}
assert passed, 'Existing plane_load_share selftest did not pass; inspect its output.'

def atom(typ, x, y, z=.5, r=.1):
    return dict(type=typ, x=x, y=y, z=z, radius=r)
def contact(a, b, f, cp):
    return dict(id1=a, id2=b, **dict(zip(['fx','fy','fz'], f)),
                **dict(zip(['fn_x','fn_y','fn_z'], f)), ft_x=0., ft_y=0., ft_z=0.,
                **dict(zip(['cp_x','cp_y','cp_z'], cp)))
def run(at, ct):
    return core.calc_love_weber_stress(at, ct, {1:'AM',3:'SE'}, 1., return_arrays=True)
def decorate_virial(at, lw):
    at=copy.deepcopy(at)
    for i, aid in enumerate(lw['ids']):
        for k, nm in enumerate(['sigma_xx','sigma_yy','sigma_zz']):
            at[aid][nm] = float(lw['tensor'][i,k,k])
    return at

at = {1:atom(1,.2,.2), 2:atom(1,.38,.2), 3:atom(3,.2,.6), 4:atom(3,.38,.6)}
ct = [contact(1,2,[-1.,0.,0.],[.29,.2,.5]), contact(3,4,[-3.,0.,0.],[.29,.6,.5])]
base = run(at,ct)
assert base['status']=='OK'
atref=decorate_virial(at,base)
swapped = [contact(1,2,[-3.,0.,0.],[.29,.2,.5]), contact(3,4,[-1.,0.,0.],[.29,.6,.5])]
wrong=run(atref,swapped)
out['global_sum_false_assurance_control'] = {
    'baseline_status':base['status'], 'swapped_status':wrong['status'],
    'swapped_virial_relative_error':wrong['checks']['virial_total_rel'],
    'baseline_phase_vm':base['type_stress'], 'swapped_phase_vm':wrong['type_stress'],
    'meaning':'Global diagonal virial gate accepts a phase-changing permutation of contact forces.'}
assert wrong['status']=='OK' and wrong['checks']['virial_total_rel'] < 1e-12

at2={1:atom(1,.2,.5),2:atom(3,.36,.5)}
ct2=[contact(1,2,[-1.,0.,0.],[.28,.5,.5])]
base2=run(at2,ct2)
badcp=[contact(1,2,[-1.,0.,0.],[.26,.5,.5])]
cp2=run(decorate_virial(at2,base2),badcp)
out['contact_point_false_assurance_control'] = {
    'baseline_status':base2['status'],'changed_cp_status':cp2['status'],
    'changed_cp_checks':cp2['checks'],'baseline_phase_vm':base2['type_stress'],
    'changed_cp_phase_vm':cp2['type_stress'],
    'meaning':'Moving contact point inside both overlapping spheres passes current checks while changing phase allocation.'}
assert cp2['status']=='OK' and cp2['checks']['virial_total_rel'] < 1e-12

# Horizontal rotation with no periodic image ambiguity: validate actual tensor code.
ang=.37
Q=np.array([[np.cos(ang),-np.sin(ang),0],[np.sin(ang),np.cos(ang),0],[0,0,1.]])
rotat=copy.deepcopy(at)
rotct=copy.deepcopy(ct)
origin=np.array([.5,.5,.5])
shift=np.array([.01,-.03,0.])
for a in rotat.values():
    p=np.array([a[k] for k in ['x','y','z']])
    p=Q@(p-origin)+origin+shift
    a.update(zip(['x','y','z'],p))
for c in rotct:
    cp=np.array([c[k] for k in ['cp_x','cp_y','cp_z']])
    cp=Q@(cp-origin)+origin+shift
    f=Q@np.array([c[k] for k in ['fx','fy','fz']])
    c.update(zip(['cp_x','cp_y','cp_z'],cp))
    c.update(zip(['fx','fy','fz'],f))
    c.update(zip(['fn_x','fn_y','fn_z'],f))
rot=run(rotat,rotct)
expect=np.einsum('ij,njk,lk->nil',Q,base['tensor'],Q)
out['actual_tensor_rotation_translation']={
    'status':rot['status'], 'tensor_relative_max_error':float(np.max(np.abs(rot['tensor']-expect))/np.max(np.abs(expect))),
    'vm_relative_max_error':float(np.max(np.abs(rot['arrays_vm']-base['arrays_vm']))/np.max(base['arrays_vm']))}
assert rot['status']=='OK' and out['actual_tensor_rotation_translation']['tensor_relative_max_error']<1e-12

boostat=copy.deepcopy(at)
for a in boostat.values():
    a.update(vx=100.,vy=-22.,vz=8.)
boost=run(boostat,ct)
out['actual_contact_stress_ignores_velocity']={
    'status':boost['status'], 'tensor_difference':float(np.max(np.abs(boost['tensor']-base['tensor']))),
    'meaning':'Expected for contact-only stress; not certification of total kinetic stress or viscous-damped dynamics.'}
assert out['actual_contact_stress_ignores_velocity']['tensor_difference']==0.

(ROOT/'evidence/mv_stress_core_controls.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='plane_load_share_selftest'},ensure_ascii=False,indent=2))
print(buf.getvalue().splitlines()[-1])
