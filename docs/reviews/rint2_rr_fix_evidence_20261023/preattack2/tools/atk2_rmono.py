"""Round-2 C3/C4 probe: Predict with a fake fetch whose arm records carry certificate fields (target_lo/hi, scale, err_rel).
Independent of the resident U19/U20 helpers.  Prints JSON."""
import json, math, os, sys
from fractions import Fraction as F
SRC = os.environ['RINT_REVIEW_SOURCE']
sys.path.insert(0, os.path.join(SRC, 'scripts'))
import rint_r_chain as RR
import step3_conv_cert as CC

LADS = {law: {'R_j_lo': '0.5', 'R_j0': '1.0', 'R_j_hi': '2.0', 'r0_sigma': 1.63e-3} for law in RR.LAWS}
ROLE_OF = {'0.5': 'R_j_lo', '1.0': 'R_j0', '2.0': 'R_j_hi'}


def rec(sig_mS, half=1e-4, G=1.0):
    """arm record: posted plate current G (code units), cert target interval [G(1-half), G(1+half)], scale = sigma/G, err_rel via target_judge."""
    s = sig_mS * 1e-3
    lo, hi = G * (1 - half), G * (1 + half)
    jd = CC.target_judge(lo, hi, G)
    return {'sigma': s, 'state': 'positive', 'n_sdcp_near': 3, 'err_rel': jd['target_err_bound_rel'], 'target_lo': lo, 'target_hi': hi,
            'scale': s / G}


def make_fetch(table, default=(5.0, 4.7, 4.4)):
    """table[(role, c, law, arm)] = sigma mS (override) — default by R role."""
    dflt = dict(zip(('R_j_lo', 'R_j0', 'R_j_hi'), default))

    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        if kit == RR.SBE_KIT:
            return [{'sigma': 1.63e-3, 'n_sdcp_near': 0, 'state': 'positive', 'err_rel': 0.0, 'target_lo': 1.0, 'target_hi': 1.0,
                     'scale': 1.63e-3}]
        rr = ROLE_OF[str(rj)]
        idx = list(range(arms)) if isinstance(arms, int) else list(arms)
        tag = {'corner': 'corner', 'origin': 'origin', 'origin8': 'origin8'}[role]
        return [rec(table.get((tag, c, law, rr, i), dflt[rr])) for i in idx]
    return fetch


def run(table, **kw):
    pr = RR.Predict(make_fetch(table, **kw), LADS, None)
    try:
        pr.run()
        return 'PREDICTED', None, pr
    except RR.Stop as e:
        return e.code, e.cause[:200], pr


out = {}
# R1: non-overflow corner, origin arm 1 non-monotone 4.80 / 4.85 / 4.40 (others monotone default)
t = {('origin', '0', 'P0', 'R_j_lo', 1): 4.80, ('origin', '0', 'P0', 'R_j0', 1): 4.85, ('origin', '0', 'P0', 'R_j_hi', 1): 4.40}
st, why, pr = run(t)
out['R1 arm1 4.80/4.85/4.40 (no overflow)'] = [st, why, [o.get('status') for o in pr.origin]]
# R1c: overflow corner (force adjust via origin arm 2 spread at R_lo), corner arm0 4.6/4.7/4.4
t = {('corner', '1', 'P1', 'R_j_lo', 0): 4.6, ('corner', '1', 'P1', 'R_j0', 0): 4.7, ('corner', '1', 'P1', 'R_j_hi', 0): 4.4,
     ('origin', '1', 'P1', 'R_j_lo', 2): 6.5}
st, why, pr = run(t)
out['R1c adjusted corner arm0 4.6/4.7/4.4'] = [st, why, [o.get('status') for o in pr.origin]]
# R1d: overflow corner, origin8 arm 3 4.4/4.7/4.4
t = {('origin', '1', 'P1', 'R_j_lo', 2): 6.5, ('origin8', '1', 'P1', 'R_j_lo', 3): 4.4, ('origin8', '1', 'P1', 'R_j0', 3): 4.7,
     ('origin8', '1', 'P1', 'R_j_hi', 3): 4.4}
st, why, pr = run(t)
out['R1d adjusted corner origin8 a3 4.4/4.7/4.4'] = [st, why, [o.get('status') for o in pr.origin]]
# R1e: overflow corner, origin8 arm 0 non-monotone (same origin as corner a0 but a different run)
t = {('origin', '1', 'P1', 'R_j_lo', 2): 6.5, ('origin8', '1', 'P1', 'R_j_lo', 0): 4.4, ('origin8', '1', 'P1', 'R_j0', 0): 4.7}
st, why, pr = run(t)
out['R1e adjusted corner origin8 a0 4.4/4.7/(4.4)'] = [st, why]
# N0: all monotone → PREDICTED; records of origins
st, why, pr = run({})
out['N0 monotone default'] = [st, why, [(x['law'], x['c'], x['ok'], x['estimator'], len(x['origins'] or [])) for x in pr.checks['r_monotone']]]
# N1: flat (all equal) → PREDICTED
st, why, pr = run({}, default=(4.7, 4.7, 4.7))
out['N1 flat 4.7/4.7/4.7'] = [st, why]

# C4 band knife: two R with intervals that touch exactly / are separated by 1 ulp (in code units, same scale)
def band_case(lo_a, hi_a, lo_b, hi_b, Ga, Gb, scale=1e-3):
    A = {'sigma': Ga * scale, 'state': 'positive', 'err_rel': CC.target_judge(lo_a, hi_a, Ga)['target_err_bound_rel'],
         'target_lo': lo_a, 'target_hi': hi_a, 'scale': scale}
    B = {'sigma': Gb * scale, 'state': 'positive', 'err_rel': CC.target_judge(lo_b, hi_b, Gb)['target_err_bound_rel'],
         'target_lo': lo_b, 'target_hi': hi_b, 'scale': scale}
    try:
        pts = [(0.5, 'a', RR.arm_band(A)), (1.0, 'b', RR.arm_band(B))]
        return RR.r_monotone_problem(pts)
    except RR.Stop as e:
        return f'STOP {e.code}'


x = 1.4656880073121192
out['C4 touch (hi_a == lo_b, R_a<R_b)'] = band_case(1.4656491487242123, x, x, 1.4657035569138221, 1.4656500700997732, 1.4657027350682457)
out['C4 1-ulp gap (hi_a < lo_b)'] = band_case(1.4656491487242123, math.nextafter(x, 0), x, 1.4657035569138221, 1.4656500700997732,
                                             1.4657027350682457)
# scale differs between the two R (same code interval): band in sigma units must use each scale
out['C4 scale differs a 1e-3 vs b 1.0000000001e-3 (equal code intervals)'] = None
A = {'sigma': 1e-3, 'state': 'positive', 'err_rel': 0.0, 'target_lo': 1.0, 'target_hi': 1.0, 'scale': 1e-3}
B = dict(A, scale=1.0000000001e-3, sigma=1.0000000001e-3)
out['C4 scale differs a 1e-3 vs b 1.0000000001e-3 (equal code intervals)'] = RR.r_monotone_problem([(0.5, 'a', RR.arm_band(A)), (1.0, 'b', RR.arm_band(B))])
# field form attacks on arm_band (sigma > 0)
base = {'sigma': 1e-3, 'state': 'positive', 'err_rel': 1e-5, 'target_lo': 0.9999, 'target_hi': 1.0001, 'scale': 1e-3}
forms = {}
for nm, upd in {'scale True': {'scale': True}, 'scale 0': {'scale': 0.0}, 'scale -1e-3': {'scale': -1e-3}, 'scale NaN': {'scale': float('nan')},
                'scale inf': {'scale': float('inf')}, 'scale "1e-3"': {'scale': '1e-3'}, 'lo > hi': {'target_lo': 1.0002},
                'lo 0': {'target_lo': 0.0}, 'lo None': {'target_lo': None}, 'hi 10**400 int': {'target_hi': 10 ** 400},
                'err_rel None': {'err_rel': None}, 'sigma NaN': {'sigma': float('nan')}, 'sigma True': {'sigma': True},
                'sigma 0 but fields junk': {'sigma': 0.0, 'target_lo': 'junk', 'scale': -5},
                'sigma outside band (σ 10x)': {'sigma': 1e-2}, 'lo int 1': {'target_lo': 1, 'target_hi': 1, 'scale': 1e-3}}.items():
    r = dict(base, **upd)
    try:
        b = RR.arm_band(r)
        forms[nm] = ['band', float(b[0]), float(b[1])]
    except RR.Stop as e:
        forms[nm] = f'STOP {e.code}'
    except Exception as e:  # noqa: BLE001
        forms[nm] = f'EXC {type(e).__name__}: {e}'
out['C4 arm_band field forms'] = forms
print(json.dumps(out, ensure_ascii=False, indent=1, default=str))
