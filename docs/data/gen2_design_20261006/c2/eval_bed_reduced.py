"""Per-edge area variants + network σ on a committed real bed (HEAD snapshot, read-only)."""
import sys, os, math, json, time
import numpy as np
from collections import Counter, defaultdict
from g2lib import (PC, NC, load_bed, build_nets, area_variant, edge_sigk, rc_from_area, solve,
                   pair_kind, geom_disk)

bed = sys.argv[1]           # real14 | case15
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', bed)
files = {'real14': ('atom_2060000.liggghts', 'contact_2060000.liggghts', 'input_real_14.liggghts', 'mesh_2060000.stl'),
         'case15': ('atom_1710000.liggghts', 'contact_1710000.liggghts', 'input_case15.liggghts', 'mesh_v4_1710000.stl')}[bed]
t0 = time.time()
atoms, contacts, tm, pz, box = load_bed(*[os.path.join(D, f) for f in files])
print(f'[{bed}] atoms {len(atoms)} contacts {len(contacts)} type_map {tm} plate_z {pz} box {box}  ({time.time()-t0:.1f}s)')
nets = build_nets(atoms, contacts, tm, pz, box)
for ch, n in nets.items():
    print(f'  {ch}: nodes {len(n["nodes"])} edges {len(n["edges"])} bottom {len(n["bottom"])} top {len(n["top"])}')

SCALE = 1000.0
VARS = ['G1', 'U', 'UL', 'ULA', 'ULB', 'ULBP']
out = {'bed': bed, 'type_map': {str(k): v for k, v in tm.items()}}

# ---------- per-edge areas on the thermal net (all contacts) ----------
th = nets['thermal']['edges']
pk = [pair_kind(e['type1'], e['type2'], tm) for e in th]
areas = {v: np.empty(len(th)) for v in VARS}
binds = {v: [] for v in VARS}
confl = {v: np.zeros(len(th), bool) for v in VARS}
dr = np.empty(len(th)); dum = np.empty(len(th)); ligg = np.empty(len(th)); rmin = np.empty(len(th))
maxdev = 0.0
for i, e in enumerate(th):
    d = e['delta'] * SCALE
    dum[i] = d; ligg[i] = e['A_hertzian']; rmin[i] = min(e['r1'], e['r2'])
    dr[i] = e['delta_over_R']
    for v in VARS:
        A, b, c = area_variant(d, e['r1'], e['r2'], e['A_hertzian'], pk[i], var=v)
        areas[v][i] = A; binds[v].append(b); confl[v][i] = c
    if e['A_physics'] > 0:
        maxdev = max(maxdev, abs(areas['G1'][i] / e['A_physics'] - 1))
    areas['G1'][i] = e['A_physics']        # use HEAD value bit-for-bit
print(f'  G1 recompute vs HEAD A_physics: max rel dev {maxdev:.2e}')
pk = np.array(pk)
summ = {}
for P in ('SE_SE', 'AM_SE', 'AM_AM'):
    m = pk == P
    if not m.any():
        continue
    row = {'n': int(m.sum()),
           'delta_over_Rstar_p10_50_90': [float(np.percentile(dr[m], q)) for q in (10, 50, 90)],
           'delta_nm_p10_50_90': [float(np.percentile(dum[m] * 1e3, q)) for q in (10, 50, 90)]}
    for v in VARS:
        bc = Counter(np.array(binds[v])[m])
        ratio = areas[v][m] / areas['G1'][m]
        s = np.minimum(np.sqrt(areas[v][m] / math.pi) / rmin[m], 1.0)
        row[v] = {'binding_pct': {k: round(100 * c / m.sum(), 3) for k, c in bc.most_common()},
                  'cap_conflict_pct': round(100 * confl[v][m].mean(), 3),
                  'A_over_G1_p10_50_90': [round(float(np.percentile(ratio, q)), 4) for q in (10, 50, 90)],
                  'frac_A_changed_gt1e-9': round(float((np.abs(ratio - 1) > 1e-9).mean()), 5),
                  'A_below_ligg_pct': round(100 * float((areas[v][m] < ligg[m] * (1 - 1e-12)).mean()), 3),
                  's_eq_1_pct (clamp_zero)': round(100 * float((s >= 1.0).mean()), 3),
                  'floor_only_pct': round(100 * float(((s < 1.0) & ((1 - s) ** 1.5 <= 1e-4)).mean()), 4)}
    summ[P] = row
out['edges'] = summ
print(json.dumps(summ, indent=1, ensure_ascii=False)[:6000])

# ---------- network σ per variant × placement ----------
def run(net_key, var, placement, floor=True, h_nm=5.0, mode_area=None):
    net = nets[net_key]
    mode = 'thermal' if net_key == 'thermal' else net_key
    saved = [(e['R_constriction'], e['R_total']) for e in net['edges']]
    nzero = 0
    for e in net['edges']:
        if var == 'HERTZ':
            a = math.sqrt(e['A_hertzian'] / math.pi) if e['A_hertzian'] > 0 else 0
            Rc = 1.0 / (edge_sigk(e, tm, mode) * 2 * a) if a > 0 else 1e12
        else:
            if var == 'G1':
                A = e['A_physics']
            else:
                A, _, _ = area_variant(e['delta'] * SCALE, e['r1'], e['r2'], e['A_hertzian'],
                                       pair_kind(e['type1'], e['type2'], tm), var=var, h_nm=h_nm)
            Rc, s, psi = rc_from_area(A, e['r1'], e['r2'], edge_sigk(e, tm, mode), placement, floor=floor)
        nzero += (Rc == 0.0)
        e['R_constriction'] = Rc
        e['R_total'] = e['R_bulk'] + Rc
    sr = solve(net)
    for e, (rc, rt) in zip(net['edges'], saved):
        e['R_constriction'] = rc; e['R_total'] = rt
    return sr, nzero / max(len(net['edges']), 1)

# sanity: G1 + divide must equal HEAD build (R_c recomputed) — compare with untouched solve
res = {}
for ch in ('ionic', 'electronic', 'thermal'):
    base = solve(nets[ch])
    g1d, _ = run(ch, 'G1', 'divide')
    print(f'  [{ch}] HEAD solve σ_ratio={base:.9g}  G1/divide recomputed={g1d:.9g}  rel {abs(g1d/base-1):.2e}')
    res[ch] = {'HEAD_divide': base}
    res[ch]['HERTZ'] = run(ch, 'HERTZ', None)
    for v in VARS:
        res[ch][f'{v}|multiply'] = run(ch, v, 'multiply')
    res[ch]['ULBP|divide'] = run(ch, 'ULBP', 'divide')
    res[ch]['ULBP|multiply|nofloor'] = run(ch, 'ULBP', 'multiply', floor=False)
    print(f'  [{ch}] done ({time.time()-t0:.0f}s)')
out['sigma'] = {ch: {k: (list(v) if isinstance(v, tuple) else v) for k, v in d.items()} for ch, d in res.items()}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'evalR_{bed}.json'), 'w'),
          indent=1, ensure_ascii=False)
print('\nσ_ratio table (σ/σ_bulk; [σ, frac R_c=0])')
for ch, d in res.items():
    g1m = d['G1|multiply'][0]
    print(f'--- {ch}  (HERTZ {d["HERTZ"][0]:.6g})')
    for k, v in d.items():
        if isinstance(v, tuple):
            print(f'   {k:28s} σ={v[0]:.6g}  Rc0={100*v[1]:.3f}%  vs G1|multiply {100*(v[0]/g1m-1):+.3f}%')
        else:
            print(f'   {k:28s} σ={v:.6g}')
print(f'total {time.time()-t0:.0f}s')
