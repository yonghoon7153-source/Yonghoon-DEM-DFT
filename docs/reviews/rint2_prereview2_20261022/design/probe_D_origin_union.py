"""Probe D — registration R §3-2b ③′ (Q-E: SBE end = union of the three origins arm 0 · 1 · 2) on the REAL chain lattice.

D1  Does the Q-E push change the grade ON THE LADDER LATTICE?  PRE-design-01 SBE responses (arm 0 S = 1.43 + 0.2/r ·
    arms 1–7 S = 1.53 + 0.1/r · r = R/1e6) with a flatter DBE D = 4 + 1/r (origin independent):
    grade from arm-0-only ends (the push switched off by reading `arm0_end`) vs the chain's union ends.
D2  R4-Q1 (three origins enough?) — arms 1·2 identical to arm 0 but arms 3–7 differ: small search over (a1, d1) for a case where
    the chain (three-origin union) grades PASS_INFORMATIVE while the same chain ladder run on the 8-arm mean response grades worse.
Run:  python3 -I probe_D_origin_union.py <worktree>      (writes probe_D_origin_union.json · < 30 s)
"""
import json
import math
import os
import sys

WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, 'scripts'))
import rint_r_chain as RR  # noqa: E402

OUT = {}


def fetch_of(S_mS):
    def fetch(role, key, arms):
        R = RR.rj_float(key)
        idx = list(range(arms)) if isinstance(arms, int) else list(arms)
        return [{'sigma': S_mS(R, i) * 1e-3, 'state': 'positive', 'err_rel': 0.0} for i in idx]
    return fetch


def ladder(S, cap=40):
    lad = RR.Ladder(fetch_of(S), max_points=cap, ratio_max='none')
    try:
        lad.run()
        lad.origin()
        return lad, 'CALIBRATED'
    except RR.Stop as e:
        return lad, e.code


def grade_ends(D, lo, r0, hi):
    J = RR.judge({('0', 'P0', 'R_j_lo'): D(lo), ('0', 'P0', 'R_j0'): D(r0), ('0', 'P0', 'R_j_hi'): D(hi)})
    return J['verdict'], J['W']


def two_family(a0, b0, a1, b1, split):
    """arms < split: a0 + b0/r · arms ≥ split: a1 + b1/r (r = R/1e6)."""
    def S(R, i):
        if R == math.inf:
            return a0 if i < split else a1
        r = max(R / 1e6, 1e-9)
        return (a0 + b0 / r) if i < split else (a1 + b1 / r)
    return S


# D1
S = two_family(1.43, 0.2, 1.53, 0.1, 1)
D = lambda R: 4.0 + 1.0 / (R / 1e6)                                  # noqa: E731
lad, st = ladder(S)
e = lad.st['ends']
r = {k: RR.rj_float(lad.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
g_union = grade_ends(D, r['R_j_lo'], r['R_j0'], r['R_j_hi'])
g_arm0 = grade_ends(D, RR.rj_float(e['lo']['arm0_end']), r['R_j0'], RR.rj_float(e['hi']['arm0_end']))
OUT['D1_lattice'] = {'status': st, 'union_ends': [r['R_j_lo'], r['R_j_hi']], 'arm0_ends': [e['lo']['arm0_end'], e['hi']['arm0_end']],
                     'pushes': [e['lo']['origin_pushes'], e['hi']['origin_pushes']], 'grade_union': g_union, 'grade_arm0_only': g_arm0}
D1b = lambda R: 3.9 + 1.0 / (R / 1e6)                                 # noqa: E731
OUT['D1b_lattice_D=3.9+1/r'] = {'grade_union': grade_ends(D1b, r['R_j_lo'], r['R_j0'], r['R_j_hi']),
                                'grade_arm0_only': grade_ends(D1b, RR.rj_float(e['lo']['arm0_end']), r['R_j0'], RR.rj_float(e['hi']['arm0_end']))}

# D2 search
best = []
n_valid = 0
n_pass3 = 0
for a1 in (1.55, 1.57, 1.58, 1.59, 1.60, 1.605, 1.61):
    b1 = 1.63 - a1
    for d1 in (0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0):
        Sx = two_family(1.43, 0.2, a1, b1, 3)                       # arms 0·1·2 steep · arms 3–7 flat
        Dx = lambda R, d1=d1: 4.0 + d1 / (R / 1e6)                  # noqa: E731
        l1, s1 = ladder(Sx)
        if s1 != 'CALIBRATED':
            continue
        r1 = {k: RR.rj_float(l1.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
        g1 = grade_ends(Dx, r1['R_j_lo'], r1['R_j0'], r1['R_j_hi'])
        Sm = lambda R, i, a1=a1, b1=b1: (3 * two_family(1.43, 0.2, a1, b1, 3)(R, 0) + 5 * two_family(1.43, 0.2, a1, b1, 3)(R, 7)) / 8  # noqa: E731
        l2, s2 = ladder(Sm)
        if s2 != 'CALIBRATED':
            g2 = (s2, None)
        else:
            r2 = {k: RR.rj_float(l2.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
            g2 = grade_ends(Dx, r2['R_j_lo'], r2['R_j0'], r2['R_j_hi'])
        n_valid += 1
        n_pass3 += g1[0] == 'PASS_INFORMATIVE'
        rec = {'a1': a1, 'b1': round(b1, 6), 'd1': d1, 'chain_3origin': g1, 'chain_on_mean8': g2,
               'ends_3origin': [r1['R_j_lo'], r1['R_j_hi']], 'R0_origin': l1.st['origin']['status']}
        if g1[0] == 'PASS_INFORMATIVE' and g2[0] != 'PASS_INFORMATIVE':
            best.append(rec)
OUT['D2_three_origins_vs_mean8'] = {'n_valid': n_valid, 'n_3origin_PASS': n_pass3, 'n_found': len(best), 'cases': best[:5]}
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_D_origin_union.json')
json.dump(OUT, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print(json.dumps(OUT, ensure_ascii=False, default=str)[:3000])
