"""Synthetic pairs δ/R* 1e-3..0.2 (+0.3, 0.5), radius ratio 1:1..1:12 — area rules & multiply R_c monotonicity."""
import math
import numpy as np
from g2lib import area_variant, rc_from_area, geom_disk, PC

pairs = [('SE_SE', 0.5, 0.5), ('AM_SE', 0.5, 1.0), ('AM_SE', 0.5, 2.0), ('AM_SE', 0.5, 5.0), ('AM_SE', 0.5, 6.0),
         ('AM_AM', 2.0, 6.0), ('AM_AM', 6.0, 6.0)]
drs = np.unique(np.concatenate([np.geomspace(1e-3, 0.2, 400), [PC.DR_YIELD_ONSET * (1 - 1e-9),
                                                               PC.DR_YIELD_ONSET * (1 + 1e-9), 0.3, 0.5]]))
rules = ['G1', 'U', 'UL', 'ULA', 'ULB', 'ULBP']
print('pair  r1 r2 | rule: nonmono_A  nonmono_Rc(mult)  jumpA@onset(×)  A/A_ligg[min,max]  A/A_G1[min,max]')
for P, r1, r2 in pairs:
    Rs = r1 * r2 / (r1 + r2)
    base = {}
    for rule in rules:
        A = []; Rc = []
        for dr in drs:
            d = dr * Rs
            lg = geom_disk(r1, r2, d)
            a, _, _ = area_variant(d, r1, r2, lg, P, var=rule)
            A.append(a); Rc.append(rc_from_area(a, r1, r2, 1.0, 'multiply')[0])
        A = np.array(A); Rc = np.array(Rc)
        base[rule] = A
        lg = np.array([geom_disk(r1, r2, dr * Rs) for dr in drs])
        i0 = np.searchsorted(drs, PC.DR_YIELD_ONSET) - 1
        nmA = int((np.diff(A) < -1e-12 * A[1:]).sum())
        nmR = int((np.diff(Rc) > 1e-12 * np.maximum(Rc[1:], 1e-30)).sum())
        print(f'{P} {r1:>3} {r2:>3} | {rule:5s} {nmA:4d} {nmR:4d}  {A[i0+1]/A[i0]:8.4f}  '
              f'[{(A/lg).min():.3f},{(A/lg).max():.3f}]  [{(A/base["G1"]).min():.3f},{(A/base["G1"]).max():.3f}]')
