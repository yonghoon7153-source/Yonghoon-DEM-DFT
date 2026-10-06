#!/usr/bin/env python3
"""designC1 — first-order (Thomson) proxy of fixes (1) and (2) on the 194 released LHS beds, from the
committed batch metrics only (docs/data/lhs_network194_11fcf91e8/merged/{lhs,lhsx}/metrics_flat.csv —
raw contacts are not in the repo).  Calibrated on the two committed raw beds (net_beds_diag.json):
the Thomson estimate with the POWER-weighted psi reproduces the exact solve to 1 % (real14 1.3254 vs
1.3387 · case15 1.1090 vs 1.1093) but per-bed power-weighted s is not stored -> bracket with
s_eff = k * s_A (s_A = sqrt(area_SE_SE_mean/pi)/r_SE, mean geometric disc) for k in {0.35, 0.72, 1.0}
(case15 needs k~0.35 · real14 k~0.72).
  sigma_H1/sigma_H0  ~ 1/(1 - p_c (1 - psi(s_eff)))
  sigma_H12/sigma_H1 ~ 1/(1 + p_b1 (kb - 1)),  p_b1 = bulk power share after (1),  kb = 3/(2 + s_A^2)
  T_CF2 ~ T_CF0 * kb  (all bulk edges scale by kb; exact on the raw beds within 1.5 %)
"""
import csv
import math
import os
import statistics as st

ROOT = '/home/user/Yonghoon-DEM-DFT/docs/data/lhs_network194_11fcf91e8/merged'


def psi(s):
    return max(1.0 - s, 0.0) ** 1.5


def f(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else None
    except (TypeError, ValueError):
        return None


def q(v, p):
    v = sorted(v)
    if not v:
        return None
    k = (len(v) - 1) * p
    i = int(k)
    return v[i] if i + 1 >= len(v) else v[i] + (v[i + 1] - v[i]) * (k - i)


rows = []
for g in ('lhs', 'lhsx'):
    for r in csv.DictReader(open(os.path.join(ROOT, g, 'metrics_flat.csv'))):
        rse = f(r.get('inp.r_SE'))
        rse = rse * 1000 if rse else f(r.get('r_SE'))
        A = f(r.get('area_SE_SE_mean'))
        phi = f(r.get('phi_se'))
        sH, sCF = f(r.get('sigma_full')), f(r.get('sigma_bulk_net'))
        sP = f(r.get('sigma_full_physics'))
        pc = f(r.get('constriction_power_share_ion_hertz'))
        if not (rse and A and phi):
            continue
        sA = math.sqrt(A / math.pi) / rse
        d = dict(g=g, case=r.get('case') or r.get('name'), sA=sA, phi=phi, pc=pc, cn=f(r.get('se_se_cn')),
                 T_H0=(phi / sH) if sH else None, T_CF0=(phi / sCF) if sCF else None,
                 T_P=(phi / sP) if sP else None, qCF0=sCF)
        kb = 3.0 / (2.0 + sA * sA)
        d['kb'] = kb
        if sH and pc is not None:
            for k in (0.35, 0.72, 1.0):
                r1 = 1.0 / (1.0 - pc * (1.0 - psi(k * sA)))
                pc1 = pc * psi(k * sA) * r1        # constriction share after (1), first order
                pb1 = 1.0 - pc1
                r12 = r1 / (1.0 + pb1 * (kb - 1.0))
                d[f'H1_k{k}'] = r1
                d[f'H12_k{k}'] = r12
        if sCF:
            d['T_CF2'] = d['T_CF0'] * kb
        rows.append(d)

for g in ('lhs', 'lhsx'):
    R = [d for d in rows if d['g'] == g]
    print(f'== {g}: n={len(R)}')
    for key in ('sA', 'cn', 'pc', 'T_H0', 'T_CF0', 'kb'):
        v = [d[key] for d in R if d.get(key) is not None]
        print(f'  {key:6s} n={len(v):3d}  min {min(v):.4g}  p10 {q(v,.1):.4g}  med {q(v,.5):.4g}  p90 {q(v,.9):.4g}  max {max(v):.4g}')
    for k in (0.35, 0.72, 1.0):
        v1 = [d[f'H1_k{k}'] for d in R if f'H1_k{k}' in d]
        v12 = [d[f'H12_k{k}'] for d in R if f'H12_k{k}' in d]
        print(f'  k={k}: sigma H1/H0 med {q(v1,.5):.3f} [{min(v1):.3f}-{max(v1):.3f}] -> T x{1/q(v1,.5):.3f} | '
              f'H12/H0 med {q(v12,.5):.3f} [{min(v12):.3f}-{max(v12):.3f}] -> T x{1/q(v12,.5):.3f}')
    cf = [d for d in R if d.get('T_CF0') is not None]
    print(f'  CF computed {len(cf)} · T_CF0<1: {sum(d["T_CF0"] < 1 for d in cf)} · q_CF0>1: {sum(d["qCF0"] > 1 for d in cf)} '
          f'· T_CF2<1 (proxy): {sum(d["T_CF2"] < 1 for d in cf)} · CF missing: {len(R) - len(cf)}')
    if cf:
        v = [d['T_CF2'] for d in cf]
        print(f'  T_CF2 proxy: min {min(v):.3f} med {q(v,.5):.3f}')
    tp = [d for d in R if d.get('T_P') is not None and d['T_P'] < 1]
    if tp:
        print(f'  Physics T<1 rows: {len(tp)} · their T_CF0 {[round(d["T_CF0"],3) if d["T_CF0"] else None for d in tp]}')
        print(f'                     their T_CF2 proxy {[round(d["T_CF2"],3) if d.get("T_CF2") else None for d in tp]}')
        print(f'                     their T_H0 {[round(d["T_H0"],3) for d in tp]} · cn {[round(d["cn"],1) for d in tp]}')
