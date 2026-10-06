"""Plane-crossing stress σ_zz = Σ|F_z|/A_box for (a) the DEM's own normal forces and (b) the HEAD
Physics reconstruction F = (4/3)E*_AM-SE √R* δ^1.5 (real E), on horizontal planes through the bed."""
import sys, os, math
import numpy as np
from g2lib import PC, load_bed, pair_kind

bed = sys.argv[1]
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', bed)
files = {'real14': ('atom_2060000.liggghts', 'contact_2060000.liggghts', 'input_real_14.liggghts', 'mesh_2060000.stl'),
         'case15': ('atom_1710000.liggghts', 'contact_1710000.liggghts', 'input_case15.liggghts', 'mesh_v4_1710000.stl')}[bed]
atoms, contacts, tm, pz, box = load_bed(*[os.path.join(D, f) for f in files])
A_box_real = box[0] * box[1] * 1e-6          # m² (sim m → real m = ×1e-3)
for frac in (0.25, 0.5, 0.75):
    z0 = frac * pz
    s_dem = s_head = 0.0; n = 0
    for c in contacts:
        a1, a2 = atoms.get(c['id1']), atoms.get(c['id2'])
        if a1 is None or a2 is None or c['delta'] <= 0:
            continue
        if not ((a1['z'] - z0) * (a2['z'] - z0) < 0):
            continue
        v = np.array([a2['x'] - a1['x'], a2['y'] - a1['y'], a2['z'] - a1['z']])
        v[0] -= box[0] * round(v[0] / box[0]); v[1] -= box[1] * round(v[1] / box[1])
        nz = abs(v[2]) / np.linalg.norm(v)
        n += 1
        s_dem += abs(c['fn'][2]) * 1e-3                       # N (real)
        r1, r2 = a1['radius'] * 1e-3, a2['radius'] * 1e-3     # m (real)
        Rs = r1 * r2 / (r1 + r2); d = c['delta'] * 1e-3
        s_head += (4 / 3) * PC.E_STAR_AM_SE * math.sqrt(Rs) * d ** 1.5 * nz
    print(f'[{bed}] z={frac:.2f}·plate  contacts crossing {n:5d}  σ_zz(DEM) = {s_dem / A_box_real / 1e6:7.1f} MPa'
          f'   σ_zz(HEAD real-E reconstruction) = {s_head / A_box_real / 1e6:7.1f} MPa   ratio {s_head / s_dem:.2f}')
