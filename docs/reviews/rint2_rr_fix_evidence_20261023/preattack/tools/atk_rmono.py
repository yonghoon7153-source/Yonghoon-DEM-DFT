"""Pre-attack: DBE R-monotone defence (Predict._r_monotone) — scope and knife edge.  No source edits."""
import json, math, os, random, sys
from fractions import Fraction as F
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import rint_r_chain as rr
import step3_conv_cert as cc

out = {}
LIM = (0.5, 1.0, 2.0)
KEYS = dict(zip(rr.RJ_ROLES, map(rr.rj_key, LIM)))
LADS = {law: dict(KEYS, r0_sigma=1.63e-3) for law in rr.LAWS}


def arm(s, err=0.0):
    return {'sigma': float(s), 'err_rel': float(err), 'state': 'zero' if s == 0 else 'positive', 'n_sdcp_near': 0}


def ids(arms):
    return range(arms) if isinstance(arms, int) else arms


def run_predict(func):
    """func(r, i, law, c) -> (sigma S/cm, err_rel)."""
    calls = []

    def fetch(kit, role, law, c, key, arms, sv_cf=False):
        calls.append(role)
        if kit == rr.SBE_KIT:
            return [arm(1.63e-3) for _ in ids(arms)]
        r = rr.rj_float(key)
        return [arm(*func(r, i, law, c)) for i in ids(arms)]
    p = rr.Predict(fetch, LADS, None)
    try:
        p.run()
        st = 'PREDICTED'
    except rr.Stop as e:
        st = f'STOP {e.code}'
    return st, p, calls


# ---------------- R1: per-origin non-monotone values (already solved) are not checked when the corner is not adjusted
base = {0.5: 5.0, 1.0: 4.7, 2.0: 4.4}


def f_r1(r, i, law, c):
    s = base[r] * (1.5 if c == '1' else 1.0)
    if i == 1:                      # arm 1: 4.80 at R .5 · 4.85 at R 1 (rises with R) · same at R 2
        s = {0.5: 4.80, 1.0: 4.85, 2.0: 4.4}[r] * (1.5 if c == '1' else 1.0)
    return s * 1e-3, 0.0
st, p, calls = run_predict(f_r1)
out['R1 arm1 non-monotone (bands disjoint, e=0), corner not adjusted'] = {
    'expected (if "same origin" = every solved origin)': 'STOP R_MONOTONE_VIOLATION',
    'got': st, 'n_adjusted': len(p.adj), 'checks_r_monotone_estimators': sorted({x['estimator'] for x in p.checks['r_monotone']}),
    'origin_status': [o['status'] for o in p.origin]}


# ---------------- R1b: adjusted corner — one of the 8 origins non-monotone, 8-mean monotone
def f_r1b(r, i, law, c):
    s = base[r]
    if i in (1, 2) and r == 2.0:     # force origin overflow at R 2 for every corner
        s = s * 1.3
    if i == 3:                        # origin 3 (only in origin8 runs): 4.2 / 4.7 / 4.4 (impossible order)
        s = {0.5: 4.2, 1.0: 4.7, 2.0: 4.4}[r]
    return s * (1.5 if c == '1' else 1.0) * 1e-3, 0.0
st, p, calls = run_predict(f_r1b)
out['R1b origin 3 non-monotone inside an adjusted corner (mean8 monotone)'] = {
    'expected (if "same origin" = every solved origin)': 'STOP R_MONOTONE_VIOLATION', 'got': st, 'n_adjusted': len(p.adj),
    'estimators': sorted({x['estimator'] for x in p.checks['r_monotone']}),
    'fetch_roles_count': {k: calls.count(k) for k in set(calls)}}


# ---------------- R2: knife edge — exact certificate intervals touch (consistent with monotone at one point) but rounded bands are disjoint
random.seed(11)
found = None
for _ in range(200000):
    Ga = 1.0 + random.random()
    ha = Ga * (1.0 + random.uniform(1e-6, 5e-5))
    la = Ga * (1.0 - random.uniform(1e-7, 1e-6))
    ja = cc.target_judge(la, ha, Ga)
    if not ja['pass_d']:
        continue
    ea_f = ja['target_err_bound_rel']
    ea_x = max(F(ha) - F(Ga), F(Ga) - F(la)) / F(Ga)
    if not F(ea_f) < ea_x:
        continue
    lb = ha                                   # b's lower certificate end = a's upper certificate end (exact touch)
    Gb = lb * (1.0 + random.uniform(1e-6, 5e-5))
    hb = Gb * (1.0 + random.uniform(1e-7, 1e-6))
    jb = cc.target_judge(lb, hb, Gb)
    if not jb['pass_d']:
        continue
    eb_f = jb['target_err_bound_rel']
    eb_x = max(F(hb) - F(Gb), F(Gb) - F(lb)) / F(Gb)
    if not F(eb_f) < eb_x:
        continue
    A = {'sigma': Ga, 'err_rel': ea_f}
    B = {'sigma': Gb, 'err_rel': eb_f}
    ba, bb = rr.arm_band(A), rr.arm_band(B)
    bad = rr.r_monotone_problem([(0.5, 'R_j_lo', ba), (1.0, 'R_j0', bb)])
    if bad:
        found = {'a': {'G': Ga, 'lo': la, 'hi': ha, 'err_rel': ea_f, 'band_hi': float(ba[1]), 'band_hi<cert_hi': ba[1] < F(ha)},
                 'b': {'G': Gb, 'lo': lb, 'hi': hb, 'err_rel': eb_f, 'band_lo': float(bb[0]), 'band_lo>cert_lo': bb[0] > F(lb)},
                 'exact cert intervals intersect': F(ha) >= F(lb), 'monotone-consistent point': F(ha),
                 'r_monotone_problem': bad}
        break
out['R2 knife edge (R_a<R_b, exact cert intervals touch, rounded bands disjoint)'] = found

print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
