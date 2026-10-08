"""Conditional static contact-force reweighting; no DEM and no equilibrium prediction.

When coordinates, topology and all histories are held fixed and velocity forces
vanish, the pinned Hooke/hysteresis law is homogeneous in its common stiffness
factor. This probe illustrates that conditional limit using observed total-force
shares; it does not establish that damping in the input snapshot is negligible.
"""
import hashlib
import json
from pathlib import Path

src = Path(__file__).resolve().parents[1] / 'source/docs/data/ps45_plane_load_20261007/ps45_v2/plane_load.json'
raw = src.read_bytes()
case = json.loads(raw)['cases']['7:3']
groups = ('AM–AM', 'AM–SE', 'SE–SE')
cuts = case['cuts']
loads = {g: sum(c['load_mpa'] * c['share_group_pct'][g] / 100 for c in cuts) / len(cuts) for g in groups}
Y0 = 1 / ((1-.25**2) / 1.4e8 + (1-.30**2) / 1.35e6)
rows = []
for q in (1, 2, 4, 24/1.35):
    Y = 1 / ((1-.25**2) / 1.4e8 + (1-.30**2) / (1.35e6*q))
    scales = dict(zip(groups, (1, (Y/Y0)**.8, q**.8)))
    reweighted = {g: scales[g]*loads[g] for g in groups}
    total = sum(reweighted.values())
    rows.append({'E_SE_real_GPa': 1.35*q, 'conditional_share_pct': {g: 100*reweighted[g]/total for g in groups},
                 'conditional_mean_cut_load_MPa': total, 'total_force_ratio': total/sum(loads.values())})
print(json.dumps({'scope': 'conditional static force-law illustration, not a simulation or equilibrium result',
                  'input_sha256': hashlib.sha256(raw).hexdigest(), 'case': '7:3',
                  'baseline_mean_cut_load_MPa': sum(loads.values()), 'rows': rows,
                  'limitations': ['uses total contact-force shares; neglect of velocity-force terms is an explicit unverified assumption',
                                  'holds geometry/topology/history fixed and imposes no equilibrium or pressure constraint',
                                  'does not predict equilibrated V4 shares or alpha; no extrapolation of measured slope']}, indent=2, ensure_ascii=False))
