"""LHS-25 prototype: per-AM coverage = sum-and-clip (HEAD coverage_physics_vs_hertzian rule)
vs union of equal-area spherical caps on the AM surface (overlap counted once, AM–AM occlusion removed).
Areas: Hertz-geom (c_cpl[22]) · Physics G1 (HEAD legacy) · Physics gen-2 surface rule (ULBPs)."""
import sys, os, math, json, time
import numpy as np
from collections import defaultdict
from g2lib import PC, load_bed, area_variant, pair_kind

bed = sys.argv[1]
NPT = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', bed)
files = {'real14': ('atom_2060000.liggghts', 'contact_2060000.liggghts', 'input_real_14.liggghts', 'mesh_2060000.stl'),
         'case15': ('atom_1710000.liggghts', 'contact_1710000.liggghts', 'input_case15.liggghts', 'mesh_v4_1710000.stl')}[bed]
t0 = time.time()
atoms, contacts, tm, pz, box = load_bed(*[os.path.join(D, f) for f in files])
S = 1000.0  # sim → µm


def fib(n):
    i = np.arange(n) + 0.5
    z = 1 - 2 * i / n
    rho = np.sqrt(1 - z * z)
    phi = math.pi * (1 + 5 ** 0.5) * i
    return np.stack([rho * np.cos(phi), rho * np.sin(phi), z], 1)


U = fib(NPT)
am_ids = [a for a, v in atoms.items() if tm[v['type']] != 'SE']
VARS = ('HERTZ', 'G1', 'ULBPs')
per = {a: {'se': [], 'am': []} for a in am_ids}   # (dir, {var: area µm²})
seen = set()
for c in contacts:
    i1, i2 = c['id1'], c['id2']
    if i1 not in atoms or i2 not in atoms:
        continue
    key = (min(i1, i2), max(i1, i2))
    if key in seen:
        continue
    seen.add(key)
    a1, a2 = atoms[i1], atoms[i2]
    P = pair_kind(a1['type'], a2['type'], tm)
    if P == 'SE_SE':
        continue
    r1, r2 = a1['radius'] * S, a2['radius'] * S
    d = c['delta'] * S
    ligg = c['contact_area'] * S * S
    ar = {'HERTZ': ligg}
    if d > 0:
        ar['G1'] = area_variant(d, r1, r2, ligg, P, var='G1')[0]
        ar['ULBPs'] = area_variant(d, r1, r2, ligg, P, var='ULBPs')[0]
    else:
        ar['G1'] = ar['ULBPs'] = ligg
    for me, other in ((i1, i2), (i2, i1)):
        if me not in per:
            continue
        p, q = atoms[me], atoms[other]
        v = np.array([q['x'] - p['x'], q['y'] - p['y'], q['z'] - p['z']])
        v[0] -= box[0] * round(v[0] / box[0]); v[1] -= box[1] * round(v[1] / box[1])
        n = v / np.linalg.norm(v)
        per[me]['se' if P == 'AM_SE' else 'am'].append((n, ar))

rows = []
for aid in am_ids:
    R = atoms[aid]['radius'] * S
    surf = 4 * math.pi * R * R
    lab = tm[atoms[aid]['type']]
    am_l = per[aid]['am']; se_l = per[aid]['se']
    # occlusion by AM neighbours (always Hertz-geom area, as the HEAD denominator does)
    occl = np.zeros(NPT, bool)
    am_sum = 0.0
    for n, ar in am_l:
        A = ar['HERTZ']; am_sum += A
        cth = 1 - min(A / (2 * math.pi * R * R), 2.0)
        occl |= (U @ n) >= cth
    free_sum = max(surf - am_sum, 0.0)
    free_union = (~occl).mean()
    row = {'id': aid, 'lab': lab, 'R': R, 'n_se': len(se_l)}
    for var in VARS:
        Asum = sum(ar[var] for _, ar in se_l)
        row[f'sumclip_{var}'] = min(Asum / free_sum * 100, 100.0) if free_sum > 0 else 0.0
        row[f'rawsum_{var}'] = Asum / free_sum * 100 if free_sum > 0 else float('nan')
        cov = np.zeros(NPT, bool)
        for n, ar in se_l:
            A = ar[var]
            cth = 1 - min(A / (2 * math.pi * R * R), 2.0)
            cov |= (U @ n) >= cth
        row[f'union_{var}'] = ((cov & ~occl).mean() / free_union * 100) if free_union > 0 else 0.0
    rows.append(row)

out = {'bed': bed, 'npt': NPT}
print(f'[{bed}] AM {len(rows)}  (N_pts {NPT})  {time.time()-t0:.0f}s')
for grp in sorted(set(r['lab'] for r in rows)) + ['ALL']:
    rs = [r for r in rows if grp == 'ALL' or r['lab'] == grp]
    g = {'n': len(rs)}
    for var in VARS:
        sc = np.array([r[f'sumclip_{var}'] for r in rs]); un = np.array([r[f'union_{var}'] for r in rs])
        raw = np.array([r[f'rawsum_{var}'] for r in rs])
        g[var] = {'sumclip_mean': round(float(sc.mean()), 3), 'union_mean': round(float(un.mean()), 3),
                  'union/sumclip': round(float(un.mean() / sc.mean()), 4),
                  'clip100_pct': round(100 * float((raw >= 100).mean()), 2),
                  'union_ge99_pct': round(100 * float((un >= 99).mean()), 2),
                  'rawsum_p50_p90_max': [round(float(np.nanpercentile(raw, q)), 2) for q in (50, 90, 100)]}
    out[grp] = g
    print(grp, json.dumps(g, ensure_ascii=False))
out["rows"] = rows
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'cov_{bed}.json'), 'w'), indent=1)
