"""Independent probes of registration R 3rd edition (docs/reviews/rint_carbon_additive_registration_R_draft_20261020.md).

My own implementation of the procedure TEXT (3-1, 3-2, 3-2b, 4-2, 5-0..5-6a) - no repository code is imported.
Responses are passive-network forms A + sum B_k/(r + C_k) with positive coefficients (parallel branches,
each a series path whose resistance grows with r = R_j / scale), so every response is monotone non-increasing
in R_j exactly as Rayleigh guarantees for one edge class.

Run:  python3 -I probe_registration_v3.py   (writes probe_registration_v3.json next to this file, < 1 s)
"""
import json
import math
import os

T = 1.63                 # SBE target mS/cm
TP, TM = T * 1.02, T * 0.98
DBE = 4.68
G0 = math.log(4.68 / 1.8877)
W_PASS, W_WEAK = G0 / 2, G0
TAU_MONO = 1e-3
STEP_MAX = 10 ** 0.5
INF = float('inf')


def grade(lo, hi, target=DBE):
    """5-5 single-law case (E = U = [lo, hi]), positive interval."""
    w = math.log(hi / lo)
    if not lo <= target <= hi:
        return w, 'FAIL'
    if w <= W_PASS:
        return w, 'PASS_INFORMATIVE'
    if w <= W_WEAK:
        return w, 'CONSISTENT_WEAK'
    return w, 'UNINFORMATIVE'


class Ladder:
    """3-1 / 3-2 / 3-2b as written.  S(R) = SBE response (mS/cm) of R_j [Ohm].  Points counted per 3-2."""

    def __init__(self, S, floor, ceiling, start=(1e4, 1e6, 1e8)):
        self.S, self.floor, self.ceiling = S, floor, ceiling
        self.pts = {}            # R -> sigma (finite positive R)
        self.n = 2               # floor + ceiling counted (3-2: "바닥 · 천장 · 시작 셋 ...")
        self.log = []
        self.start = start

    def get(self, R, why):
        if R not in self.pts:
            self.pts[R] = self.S(R)
            self.n += 1
            self.log.append((why, R, self.pts[R]))
        return self.pts[R]

    def nonmonotone_check(self):
        ps = sorted(self.pts.items())
        flat = []
        for (ra, sa), (rb, sb) in zip(ps, ps[1:]):
            d = math.log(sb) - math.log(sa)
            if d > TAU_MONO:
                return 'CALIB_NONMONOTONE', flat
            if d > 0:
                flat.append((ra, rb, d))
        return None, flat

    def bracket(self, X):
        """Adjacent measured pair with s(Ra) >= X >= s(Rb), Ra < Rb; extend x100 on the needed side; bisect (log mid) to ratio <= 10^0.5."""
        for _ in range(200):
            ps = sorted(self.pts.items())
            br = None
            for (ra, sa), (rb, sb) in zip(ps, ps[1:]):
                if sa >= X >= sb:
                    br = (ra, rb)
                    break
            if br is None:
                if all(s > X for _, s in ps):
                    self.get(ps[-1][0] * 100.0, f'extend+ for {X:.6g}')
                elif all(s < X for _, s in ps):
                    self.get(ps[0][0] / 100.0, f'extend- for {X:.6g}')
                else:
                    raise RuntimeError('non-monotone measured set (not covered by the text)')
                continue
            ra, rb = br
            if rb / ra <= STEP_MAX * (1 + 1e-12):
                return ra, rb
            self.get(math.sqrt(ra * rb), f'bisect for {X:.6g}')
        raise RuntimeError('bracket loop')

    def interp(self, ra, rb, X):
        sa, sb = self.pts[ra], self.pts[rb]
        f = (math.log(sa) - math.log(X)) / (math.log(sa) - math.log(sb))
        return math.exp(math.log(ra) + f * (math.log(rb) - math.log(ra)))

    def run(self):
        out = {}
        if not (self.floor <= T <= self.ceiling):
            return {'name': 'CALIB_IMPOSSIBLE'}
        if abs(self.floor / T - 1) <= 0.02 or abs(self.ceiling / T - 1) <= 0.02:
            return {'name': 'CALIB_EDGE'}
        for R in self.start:
            self.get(R, 'start')
        ra, rb = self.bracket(T)
        sa, sb = self.pts[ra], self.pts[rb]
        out['e_local'] = abs(math.log(sa / sb) / math.log(rb / ra))
        out['e_min'] = 0.02 / math.log(math.sqrt(10))
        r0 = float(f'{self.interp(ra, rb, T):.3g}')
        ok = False
        for attempt in range(3):           # first confirm + at most two re-interpolations
            s0 = self.get(r0, 'confirm R0')
            if abs(s0 / T - 1) <= 0.02:
                ok = True
                break
            if attempt == 2:
                break
            ra, rb = self.bracket(T)
            r0 = float(f'{self.interp(ra, rb, T):.3g}')
        if not ok:
            return {'name': 'CALIB_UNCONFIRMED'}
        out['R0'] = r0
        out['delta_R0'] = math.log(self.pts[r0] / T)
        # 3-2b ends
        for tag, X in (('lo', TP), ('hi', TM)):
            ra, rb = self.bracket(X)
            cand = self.interp(ra, rb, X)
            sc = self.get(cand, f'confirm end {tag}')
            if tag == 'lo':
                end = cand if sc >= TP else max(R for R, s in self.pts.items() if s >= TP)
            else:
                end = cand if sc <= TM else min(R for R, s in self.pts.items() if s <= TM)
            out[f'R_{tag}'] = end
            out[f'R_{tag}_candidate'] = cand
            out[f'R_{tag}_candidate_confirmed'] = (end == cand)
        nm, flat = self.nonmonotone_check()
        out['nonmonotone'] = nm
        out['flat_pairs'] = flat
        out['n_points'] = self.n
        out['name'] = 'CALIBRATED'
        return out


def bisect_inverse(S, X, lo=1e-12, hi=1e30):
    """Exact (to 1e-12 in log R) inverse of a monotone decreasing S."""
    a, b = math.log(lo), math.log(hi)
    for _ in range(300):
        m = 0.5 * (a + b)
        if S(math.exp(m)) >= X:
            a = m
        else:
            b = m
    return math.exp(0.5 * (a + b))


def pn(A, terms, scale):
    """Passive form: A + sum B/(R/scale + C)."""
    return lambda R: A + sum(B / (R / scale + C) for B, C in terms)


def case(name, S, floor, ceiling, D, note):
    lad = Ladder(S, floor, ceiling)
    res = lad.run()
    rec = {'case': name, 'note': note, 'ladder': {k: v for k, v in res.items() if k != 'flat_pairs'}}
    if res.get('name') != 'CALIBRATED':
        return rec
    true_lo, true_hi = bisect_inverse(S, TP), bisect_inverse(S, TM)
    rec['true_R_lo'], rec['true_R_hi'] = true_lo, true_hi
    rec['outer_wrap_holds'] = res['R_lo'] <= true_lo * (1 + 1e-12) and res['R_hi'] >= true_hi * (1 - 1e-12)
    rec['procedure_ratio'] = res['R_hi'] / res['R_lo']
    rec['true_ratio'] = true_hi / true_lo
    w_proc, g_proc = grade(D(res['R_hi']), D(res['R_lo']))
    w_true, g_true = grade(D(true_hi), D(true_lo))
    rec['DBE_procedure'] = [D(res['R_hi']), D(res['R_lo']), w_proc, g_proc]
    rec['DBE_true_set'] = [D(true_hi), D(true_lo), w_true, g_true]
    rec['code_2nd_ed_rule_e_lt_emin_would_stop'] = res['e_local'] < res['e_min']
    return rec


def main():
    out = {}
    sc = 10 ** 4.75
    # (a) RCA-01 circuit (Codex): S = 1.597 + 0.0363/(r + 0.1), D = 3 + 1/(r + 0.1)
    S_a = pn(1.597, [(0.0363, 0.1)], sc)
    D_a = pn(3.0, [(1.0, 0.1)], sc)
    out['a_rca01'] = case('RCA-01 kink near floor', S_a, 1.597, S_a(0.0), D_a,
                          'Codex RCA-01 circuit; 2nd-ed interpolation gave PASS W 0.4194')
    # (b) flat: log-like decline - 7 parallel branches b*10^k/(r + 10^k) (each a series path, positive) -> e ~ b/(S ln10)
    b = 0.04
    terms_b = [(b * 10.0 ** k, 10.0 ** k) for k in range(7)]
    A_b = 1.49
    S_b0 = pn(A_b, terms_b, 1e2)
    D_b = pn(3.7, [(0.3 * 10.0 ** k, 10.0 ** k) for k in range(7)], 1e2)
    out['b_flat'] = case('flat (e < e_min)', S_b0, A_b, S_b0(0.0), D_b,
                         'positive 7-branch network, elasticity ~0.011 < e_min over decades')
    # (b2) same flat SBE, but DBE strongly R-dependent there -> wide but honest interval
    D_b2 = pn(1.0, [(2.0 * 10.0 ** k, 10.0 ** k) for k in range(7)], 1e2)
    out['b2_flat_sensitive_DBE'] = case('flat SBE, sensitive DBE', S_b0, A_b, S_b0(0.0), D_b2,
                                        'R_j unidentified AND prediction sensitive -> should not be PASS')
    # (c) kink near ceiling: plateau just above T+ at small R -> T+ end needs downward x100 extensions
    S_c = pn(1.40, [(0.2662, 1.0)], 1e5)          # ceiling S(0) = 1.6662 (just above T+ = 1.6626)
    D_c = pn(3.0, [(2.0, 1.0)], 1e5)
    out['c_ceiling_kink'] = case('kink near ceiling', S_c, 1.40, S_c(0.0), D_c,
                                 'T+ end close to the ceiling plateau; counts points against the 2nd-ed cap 12')
    # (d) SBE-side origin x R interaction (adjacent class to RCA-02, R3-Q4 open): arm 0 vs mean of 8 arms
    #     arm0: 1.43 + 0.2/r ; arms1..7: 1.53 + 0.1/r  (all equal 1.63 at r = 1) ; DBE origin-insensitive D = 1 + 4/r
    s_arm0 = lambda r: 1.43 + 0.2 / r
    s_oth = lambda r: 1.53 + 0.1 / r
    s_mean = lambda r: (s_arm0(r) + 7 * s_oth(r)) / 8
    d_all = lambda r: 1.0 + 4.0 / r
    inv = lambda f, X: bisect_inverse(f, X, 1e-9, 1e9)
    lo0, hi0 = inv(s_arm0, TP), inv(s_arm0, TM)
    lom, him = inv(s_mean, TP), inv(s_mean, TM)
    centre_spread = math.log(max(s_arm0(1), s_oth(1)) / min(s_arm0(1), s_oth(1)))
    out['d_sbe_origin'] = {
        'centre_SBE_arm0_arm1_arm2': [s_arm0(1.0), s_oth(1.0), s_oth(1.0)],
        'centre_ln_spread': centre_spread, 'CALIB_ORIGIN_SENSITIVE_fires (>0.02)': centre_spread > 0.02,
        'arm0_admissible_r': [lo0, hi0], 'mean8_admissible_r': [lom, him],
        'DBE_from_arm0_set': list(grade(d_all(hi0), d_all(lo0))) + [d_all(hi0), d_all(lo0)],
        'DBE_from_mean8_set': list(grade(d_all(him), d_all(lom))) + [d_all(him), d_all(lom)],
        'SBE_end_spread_at_arm0_lo_hi': [math.log(s_oth(lo0) / s_arm0(lo0)), math.log(s_arm0(hi0) / s_oth(hi0))],
    }
    # (e) near-edge certified noise: floor 5e-5 (relative) below T-; certified values within +-1e-4 of the true response
    F = TM * (1 - 5e-5)
    S_true = pn(F, [(0.05, 0.1)], 1e5)
    D_e = pn(0.5, [(300.0, 300.0)], 1e5)              # DBE junction branch with a long series path: still varies where SBE is flat
    true_hi = bisect_inverse(S_true, TM)
    # a certified reading may report any value within +-1e-4 of S_true; worst case for the hi end: low readings
    S_low = lambda R: S_true(R) * (1 - 1e-4)
    S_high = lambda R: S_true(R) * (1 + 1e-4)
    hi_low = bisect_inverse(S_low, TM)               # earliest R where a low reading can say sigma <= T-
    out['e_near_edge'] = {
        'floor_rel_to_Tminus': F / TM - 1, 'CALIB_EDGE_fires': abs(F / T - 1) <= 0.02,
        'true_R_hi': true_hi, 'earliest_R_hi_reachable_with_low_reading': hi_low,
        'ratio_true_over_reachable': true_hi / hi_low,
        'high_readings_never_reach_Tminus': S_high(1e30) > TM,
        'D_at_true_R_hi': D_e(true_hi), 'D_at_reachable_R_hi': D_e(hi_low),
        'ln_D_shift_at_lower_end': math.log(D_e(hi_low) / D_e(true_hi)),
        'certified_nonmonotone_max': 2e-4, 'tau_mono_registered': TAU_MONO,
    }
    # (f) origin rule (4-2) with a zero corner: W_first = +inf -> 0.1 W = inf -> no corner switches
    corners_arm0 = {'c0P0': 0.0, 'c1P0': 3.0, 'c0P1': 3.5, 'c1P1': 4.0}     # same at all three R for brevity
    arms12 = {'c0P0': 6.0, 'c1P0': 3.0, 'c0P1': 3.5, 'c1P1': 4.0}
    mean8 = {'c0P0': (0.0 + 7 * 6.0) / 8, 'c1P0': 3.0, 'c0P1': 3.5, 'c1P1': 4.0}
    lo, hi = min(corners_arm0.values()), max(corners_arm0.values())
    W_first = INF if lo == 0.0 else math.log(hi / lo)
    switched = {}
    for k in corners_arm0:
        vals = [corners_arm0[k], arms12[k], arms12[k]]
        spread = INF if min(vals) == 0.0 else math.log(max(vals) / min(vals))
        switched[k] = not (spread <= 0.1 * W_first)
    final = {k: (mean8[k] if switched[k] else corners_arm0[k]) for k in corners_arm0}
    flo, fhi = min(final.values()), max(final.values())
    out['f_origin_zero_corner'] = {
        'W_first': 'inf' if W_first == INF else W_first, 'switched': switched,
        'verdict_with_rule': ('FAIL (4.68 > max %.3g, model low)' % fhi) if fhi < DBE else 'in E',
        'if_switched_c0P0_to_mean8': [min(mean8.values()), max(mean8.values()),
                                      grade(min(mean8.values()), max(mean8.values()))],
    }
    # (g) origin threshold 0.1 W near the 0.454 boundary: tolerated spread moves both ends
    #     arm0 ends: lo = 4.20, hi = 4.20*e^0.44 ; arms 1,2 at hi end higher by 0.099 W, at lo end lower by 0.099 W
    W0 = 0.44
    lo0g, hi0g = 4.20, 4.20 * math.exp(W0)
    eps = 0.099 * W0
    hi8 = (hi0g + 7 * hi0g * math.exp(eps)) / 8
    lo8 = (lo0g + 7 * lo0g * math.exp(-eps)) / 8
    out['g_origin_threshold_boundary'] = {
        'arm0': [lo0g, hi0g, grade(lo0g, hi0g)],
        'arm_spread_ln_each_end': eps, 'threshold_0.1W': 0.1 * W0, 'switch_fires': eps > 0.1 * W0,
        'mean8_if_switched': [lo8, hi8, grade(lo8, hi8)],
    }
    # (h) verdict-name precedence: 3-2c list order vs 5-0 step 1
    calib_order = ['CALIB_IMPOSSIBLE', 'CALIB_EDGE', 'CALIB_UNIDENTIFIED', 'CALIB_UNCONFIRMED',
                   'CALIB_NONMONOTONE', 'CALIB_LADDER_EXHAUSTED', 'NOT_COMPUTED']
    laws = {'P0': 'NOT_COMPUTED', 'P1': 'CALIB_EDGE'}
    out['h_name_precedence'] = {
        'laws': laws,
        'by_3_2c_list_order': min(laws.values(), key=calib_order.index),
        'by_5_0_step1_any_NOT_COMPUTED': 'NOT_COMPUTED' if 'NOT_COMPUTED' in laws.values() else None,
    }
    # (i) P as discrete laws vs a continuous attenuation family: gap fills if beta in [0, 1] exists
    #     toy: per-law DBE prediction after recalibration moves continuously with beta (linear in ln for the toy)
    I_P0, I_P1 = (3.8, 4.0), (5.2, 5.4)
    lo_b = lambda bb: math.exp((1 - bb) * math.log(I_P0[0]) + bb * math.log(I_P1[0]))
    hi_b = lambda bb: math.exp((1 - bb) * math.log(I_P0[1]) + bb * math.log(I_P1[1]))
    b_star = (math.log(DBE) - math.log(I_P0[0])) / (math.log(I_P1[0]) - math.log(I_P0[0]))   # lo(b*) = 4.68
    out['i_P_discrete_vs_continuous'] = {
        'discrete_union_contains_4.68': any(a <= DBE <= bb for a, bb in (I_P0, I_P1)),
        'beta_where_lower_end_is_4.68': b_star, 'interval_at_beta_star': [lo_b(b_star), hi_b(b_star)],
        'continuous_union_contains_4.68': lo_b(b_star) <= DBE <= hi_b(b_star),
        'note': 'toy continuity only - shows the GAP state depends on declaring P discrete (c is declared continuous)',
    }
    # (j) certificate (d) literal rule vs first-order plate current: two-edge chain
    g = [1.0, 1.0]
    for delta in (1e-6, 1e-9):
        phi1 = 0.5 - delta
        I_bot = g[0] * (phi1 - 0.0)
        U = g[0] * phi1 ** 2 + g[1] * (1 - phi1) ** 2
        L = 1.0 / (1 / g[0] + 1 / g[1])           # series chain: the unit flow is unique -> exact
        Gs = L
        out[f'j_cert_literal_delta_{delta:g}'] = {
            'I_bot': I_bot, 'L': L, 'U': U, 'G_true': Gs,
            'rel_error_of_published_G': (I_bot - Gs) / Gs,
            'width_rel': (U - L) / I_bot,
            'literal_rule_G_in_[L,U]': L <= I_bot <= U,
            'guarantee_rule_max_dist_rel': max(abs(I_bot - L), abs(I_bot - U)) / I_bot,
        }
    # (k) RCA-02 circuit under the 3rd-edition origin rule (4-2): all three R checked, a corner that exceeds -> 8-arm mean at all three R
    arm0 = lambda r: 3.02 + 1.0 / (r + 0.1)
    oth = lambda r: 1.02 + 3.2 / (r + 0.1)
    Rs = (0.5, 1.0, 2.0)
    a0_vals = [arm0(r) for r in Rs]
    W_first = math.log(max(a0_vals) / min(a0_vals))
    spreads = [math.log(max(arm0(r), oth(r)) / min(arm0(r), oth(r))) for r in Rs]
    switch = any(s > 0.1 * W_first for s in spreads)
    vals = [(arm0(r) + 7 * oth(r)) / 8 for r in Rs] if switch else a0_vals
    out['k_rca02_3rd_ed_rule'] = {
        'W_first_arm0': W_first, 'spreads_lo_0_hi': spreads, 'threshold_0.1W': 0.1 * W_first, 'corner_switched': switch,
        'final_interval': [min(vals), max(vals)], 'grade': grade(min(vals), max(vals)),
        'second_ed_rule_interval (shift by centre log-diff = 0)': [min(a0_vals), max(a0_vals)],
    }
    # (l) mutants of the 3-2b end rule on the RCA-01 circuit vs the registered test (3-2b item 8: "R ratio ~200 or incomplete; PASS = fail")
    a = out['a_rca01']
    R0 = a['ladder']['R0']
    lo_c, hi_c = a['ladder']['R_lo_candidate'], a['ladder']['R_hi_candidate']
    e_loc = a['ladder']['e_local']
    r0x = R0
    lo_2nd = r0x * math.exp(-math.log(1.02) / e_loc)        # 2nd-ed interpolation from R0 with local secant
    hi_2nd = r0x * math.exp(-math.log(0.98) / e_loc)
    muts = {
        'correct_doc_rule': (a['ladder']['R_lo'], a['ladder']['R_hi']),
        'M1_no_fallback_use_failed_candidate': (lo_c, hi_c),
        'M2_inner_bracket_neighbour_lo': (10 ** 4.5, a['ladder']['R_hi']),
        'M3_old_interp_hi_only': (a['ladder']['R_lo'], hi_2nd),
        'M4_old_interp_both': (lo_2nd, hi_2nd),
    }
    mres = {}
    for k, (rl, rh) in muts.items():
        w, gname = grade(D_a(rh), D_a(rl))
        mres[k] = {'R_lo': rl, 'R_hi': rh, 'ratio': rh / rl, 'W': w, 'grade': gname,
                   'caught_by_not_PASS_check': gname == 'PASS_INFORMATIVE',
                   'caught_by_ratio_ge_199.95_check': rh / rl < 199.95}
    out['l_end_rule_mutants'] = mres
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_registration_v3.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    for k, v in out.items():
        print('==', k)
        print(json.dumps(v, ensure_ascii=False, default=str)[:1600])


if __name__ == '__main__':
    main()
