"""L1-08 ④ : is the reconstructed 'real' Hertz force compatible with the DEM force at the same contact?
Scaled-SI deck: lengths ×1e3, moduli ÷1e3  ⇒ F_real = F_sim·1e-3 N, A_real = A_sim·1e-6 m², p_real = 1e3·F_sim/A_sim."""
import sys, os, math
import numpy as np
from g2lib import PC, load_bed, pair_kind, area_variant

bed = sys.argv[1]
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', bed)
files = {'real14': ('atom_2060000.liggghts', 'contact_2060000.liggghts', 'input_real_14.liggghts', 'mesh_2060000.stl'),
         'case15': ('atom_1710000.liggghts', 'contact_1710000.liggghts', 'input_case15.liggghts', 'mesh_v4_1710000.stl')}[bed]
atoms, contacts, tm, pz, box = load_bed(*[os.path.join(D, f) for f in files])
rows = {'SE_SE': [], 'AM_SE': [], 'AM_AM': []}
for c in contacts:
    a1, a2 = atoms.get(c['id1']), atoms.get(c['id2'])
    if a1 is None or a2 is None or c['delta'] <= 0 or c['contact_area'] <= 0:
        continue
    P = pair_kind(a1['type'], a2['type'], tm)
    Fn = float(np.linalg.norm(c['fn']))            # sim N
    r1, r2 = a1['radius'] * 1e3, a2['radius'] * 1e3  # µm
    d = c['delta'] * 1e3
    ligg = c['contact_area'] * 1e6                  # µm²
    p_real = 1e3 * Fn / c['contact_area']           # Pa
    A_tab_DEM = (Fn * 1e-3) / PC.H_REAL_SE * 1e12   # µm²  (Tabor with the DEM's own normal force)
    Rs = r1 * r2 / (r1 + r2)
    A_tab_HEAD = (4 / 3) * PC.E_STAR_AM_SE * math.sqrt(Rs) * d ** 1.5 / PC.H_REAL_SE
    rows[P].append((p_real, A_tab_DEM / ligg, A_tab_HEAD / ligg, A_tab_HEAD / A_tab_DEM))
for P, v in rows.items():
    if not v:
        continue
    a = np.array(v)
    q = lambda col: [round(float(np.percentile(a[:, col], x)), 4) for x in (10, 50, 90)]
    print(f'[{bed}] {P:6s} n={len(a):6d}  p_contact (MPa) p10/50/90 = {[round(x/1e6,1) for x in np.percentile(a[:,0],(10,50,90))]}'
          f'  frac p≥H {100*float((a[:,0]>=PC.H_REAL_SE).mean()):.2f}%'
          f'  A_tabor(F_DEM)/A_ligg {q(1)}  A_tabor(HEAD real-E)/A_ligg {q(2)}  HEAD/F_DEM {q(3)}')
