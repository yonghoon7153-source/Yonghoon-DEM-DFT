"""PROPOSED (not applied) — gen-2 Physics contact area, to sit NEXT TO the legacy
`plastic_coverage.film_area_from_overlap` and `film_area_physics_v2` (both left bit-identical).

Decisions encoded (each is an author decision — see report):
  ① L1-02  V = exact two-sphere lens  (`lens_volume`)
  ② L1-01  rule B: caps bound only the plastic EXTENSION; floor = DEM geometric disc (c_cpl[22], the
           Hertz-mode area) at EVERY δ — no elastic branch, no jump at DR_YIELD_ONSET
  ③ L1-03  pair-specific E* from the module's own constants; AM–AM unsupported (no NCM hardness
           anchor) → native disc; unknown pair → ValueError
  DESC-03  h_film in the same length unit as δ, r (`length_scale` = length units per metre; µm → 1e6)
  S1/AREA-12  transport cap π r_min² (disc) vs surface cap 2π r_min² (hemisphere)
"""
import math
from plastic_coverage import (lens_volume, E_STAR_AM_SE, E_REAL_SE, POISSON_SE, H_REAL_SE,
                              H_FILM_MIN, DR_YIELD_ONSET, DR_FULLY_PLASTIC)

AREA_RULE_G2 = 'physics_g2'
PAIR_ESTAR_G2 = {
    'AM_SE': E_STAR_AM_SE,                                   # unchanged
    'SE_SE': 1.0 / (2.0 * (1.0 - POISSON_SE ** 2) / E_REAL_SE),   # 13.1868 GPa (L1-03)
}
CONSUMER_CAP = {'transport': math.pi, 'surface': 2.0 * math.pi}


def geom_disc(r1, r2, delta):
    """Analytic two-sphere intersection disc (what LIGGGHTS c_cpl[22] reports) — fallback only."""
    d = r1 + r2 - delta
    if d <= abs(r1 - r2):
        return math.pi * min(r1, r2) ** 2
    x = (d * d + r1 * r1 - r2 * r2) / (2.0 * d)
    return max(math.pi * (r1 * r1 - x * x), 0.0)


def film_area_g2(delta, r1, r2, *, pair, ligg_area, length_scale, consumer):
    """→ (A, binding).  δ, r1, r2 in one length unit (1 m = `length_scale` units); A in that unit².
    binding ∈ {'none','floor','tabor','volume','cap','native_unsupported_pair'}."""
    for name, x in (('delta', delta), ('r1', r1), ('r2', r2), ('length_scale', length_scale)):
        if not (isinstance(x, (int, float)) and math.isfinite(x)):
            raise ValueError(f'{name} not finite: {x!r}')
    if r1 <= 0 or r2 <= 0 or length_scale <= 0 or delta >= r1 + r2:
        raise ValueError('outside contact geometry')
    if consumer not in CONSUMER_CAP:
        raise ValueError(f'consumer {consumer!r}')
    floor = ligg_area if (ligg_area is not None and ligg_area > 0) else geom_disc(r1, r2, delta)
    if delta <= 0:
        return floor, 'none'
    if pair == 'AM_AM':
        return floor, 'native_unsupported_pair'
    if pair not in PAIR_ESTAR_G2:
        raise ValueError(f'unsupported pair {pair!r}')
    R_star = r1 * r2 / (r1 + r2)
    A_tab = (4.0 / 3.0) * PAIR_ESTAR_G2[pair] * math.sqrt(R_star) * delta ** 1.5 / H_REAL_SE
    A_vol = lens_volume(r1, r2, delta) / (H_FILM_MIN * length_scale)
    A_cap = CONSUMER_CAP[consumer] * min(r1, r2) ** 2
    U = min(A_tab, A_vol, A_cap)
    if floor >= U:
        return floor, 'floor'          # ← old 'cap_conflict' (L > U): no plastic extension
    return U, ('tabor' if U == A_tab else 'volume' if U == A_vol else 'cap')


if __name__ == '__main__':   # self-check against the scratch variants used for the numbers
    import random
    from g2lib import area_variant
    random.seed(0); bad = 0
    for _ in range(20000):
        r1 = random.choice([0.5, 1.0, 2.0, 6.0]); r2 = random.choice([0.5, 1.0, 2.0, 6.0])
        P = 'SE_SE' if (r1 == 0.5 and r2 == 0.5) else random.choice(['AM_SE', 'AM_AM'])
        Rs = r1 * r2 / (r1 + r2); d = Rs * 10 ** random.uniform(-4, -0.3)
        lg = geom_disc(r1, r2, d)
        A, _ = film_area_g2(d, r1, r2, pair=P, ligg_area=lg, length_scale=1e6, consumer='transport')
        B = area_variant(d, r1, r2, lg, P, var='ULBP')[0]
        As, _ = film_area_g2(d, r1, r2, pair=P, ligg_area=lg, length_scale=1e6, consumer='surface')
        Bs = area_variant(d, r1, r2, lg, P, var='ULBPs')[0]
        bad += (abs(A / B - 1) > 1e-12) + (abs(As / Bs - 1) > 1e-12)
        # unit invariance (DESC-03): same contact in mm with length_scale 1e3
        Am, bm = film_area_g2(d * 1e-3, r1 * 1e-3, r2 * 1e-3, pair=P, ligg_area=lg * 1e-6,
                              length_scale=1e3, consumer='transport')
        bad += abs(Am * 1e6 / A - 1) > 1e-9
    print('mismatches vs scratch variants / unit invariance:', bad)
