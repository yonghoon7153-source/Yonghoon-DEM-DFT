"""Probe A — registration R 4th-edition number examples, fed to the REAL chain functions at 93d93bc02.

Run:  python3 -I probe_A_reg_numbers.py <worktree>      (writes probe_A_reg_numbers.json next to this file, < 2 s)
No repository file is written.  Chain functions used: Ladder · judge · Predict · dbe_origin_ok · w_pos_of.
"""
import json
import math
import os
import sys

WT = sys.argv[1]
sys.path.insert(0, os.path.join(WT, 'scripts'))
import rint_r_chain as RR  # noqa: E402

OUT = {}
T = 1.63
TP, TM = T * 1.02, T * 0.98


def fetch_of(S_mS, err=0.0, read=1.0):
    def fetch(role, key, arms):
        R = RR.rj_float(key)
        idx = list(range(arms)) if isinstance(arms, int) else list(arms)
        return [{'sigma': S_mS(R, i) * 1e-3 * read, 'state': 'positive', 'err_rel': err} for i in idx]
    return fetch


def run_ladder(S, err=0.0, read=1.0, cap=12):
    lad = RR.Ladder(fetch_of(S, err, read), max_points=cap, ratio_max='none')
    status = 'CALIBRATED'
    try:
        lad.run()
        lad.origin()
    except RR.Stop as e:
        status = e.code
    return lad, status


def bisect_inv(f, X, lo=1e-9, hi=1e30):
    a, b = math.log(lo), math.log(hi)
    for _ in range(400):
        m = 0.5 * (a + b)
        if f(math.exp(m)) >= X:
            a = m
        else:
            b = m
    return math.exp(0.5 * (a + b))


# ── (1) RCA-01 circuit · §3-2b ⑧ expectation ──
SC = 10 ** 4.75
S1 = lambda R, i=0: 1.597 if R == math.inf else 1.597 + 0.0363 / (R / SC + 0.1)   # noqa: E731
D1 = lambda R: 3.0 + 1.0 / (R / SC + 0.1)                                          # noqa: E731
lad, st = run_ladder(S1)
R = {k: RR.rj_float(lad.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
J = RR.judge({('0', 'P0', k): D1(v) for k, v in R.items()})
cand_hi = float(lad.st['ends']['hi']['candidate'])
s_cand_hi = S1(cand_hi)
d = 1.0 - s_cand_hi / TM
OUT['1_rca01'] = {'status': st, 'R': R, 'ratio': lad.st['R_ratio'], 'n_runs': lad.st['n_runs'], 'e': lad.sealed['e'],
                  'confirm_delta_pct': 100 * (math.exp(lad.sealed['delta']) - 1), 'verdict': J['verdict'], 'W': J['W'],
                  'interval': J['interval_mScm'], 'cand_lo': lad.st['ends']['lo']['candidate'], 'cand_hi': cand_hi,
                  'd_hi_rel_below_Tminus': d, 'boundary_e=d/(1-d)': d / (1 - d),
                  'true_lo': bisect_inv(lambda r: S1(r), TP), 'true_hi': bisect_inv(lambda r: S1(r), TM),
                  'registration_says': 'R0 64,000 · lo 10,000 · hi 5,990,349.75 · ratio 599.03 · DBE [3.0094, 6.5994] · W 0.785238 · '
                                       'CONSISTENT_WEAK · 12 points · d 3.728247e-5 · boundary 3.72839e-5'}
# e boundary sweep (registration: 3.72838e-5 = candidate · 3.72840e-5 = outer neighbour 1e7)
bnd = d / (1 - d)
sweep = {}
for e in (0.0, 3.7e-5, 3.728e-5, 3.72838e-5, bnd * (1 - 1e-9), bnd * (1 + 1e-9), 3.72840e-5, 3.8e-5, 1e-4):
    l2, s2 = run_ladder(S1, err=e)
    if s2 != 'CALIBRATED':
        sweep[repr(e)] = s2
        continue
    R2 = {k: RR.rj_float(l2.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
    J2 = RR.judge({('0', 'P0', k): D1(v) for k, v in R2.items()})
    sweep[repr(e)] = {'R_hi': R2['R_j_hi'], 'ratio': l2.st['R_ratio'], 'W': J2['W'], 'verdict': J2['verdict'],
                      'hi_source': l2.st['ends']['hi']['source'], 'n_runs': l2.st['n_runs']}
OUT['1b_e_boundary_sweep'] = sweep
# mutants M1-M3 (registration numbers) with the real judge
lo_c = float(lad.st['ends']['lo']['candidate'])
e_loc = lad.sealed['e']
hi_2nd = R['R_j0'] * math.exp(-math.log(0.98) / e_loc)
muts = {'M1_failed_candidates': (lo_c, cand_hi), 'M2_inner_lo_31622.78': (10 ** 4.5, R['R_j_hi']),
        'M3_old_interp_hi_only': (R['R_j_lo'], hi_2nd)}
OUT['1c_mutants'] = {}
for k, (rl, rh) in muts.items():
    Jm = RR.judge({('0', 'P0', 'R_j_lo'): D1(rl), ('0', 'P0', 'R_j0'): D1(R['R_j0']), ('0', 'P0', 'R_j_hi'): D1(rh)})
    OUT['1c_mutants'][k] = {'ratio': rh / rl, 'W': Jm['W'], 'verdict': Jm['verdict']}
OUT['1c_mutants']['registration_says'] = 'M1 223.87 W 0.4536 PASS · M2 189.43 W 0.4045 FAIL · M3 18.68 CONSISTENT_WEAK'

# ── (2) PRE-design-01 circuit (Q-E union) — registration: continuous union r [0.7541, 1.4837] · DBE [3.696, 6.304] W 0.5339 WEAK ──
def S2(R, i):
    if R == math.inf:
        return 1.43 if i == 0 else 1.53
    r = max(R / 1e6, 1e-6)
    return (1.43 + 0.2 / r) if i == 0 else (1.53 + 0.1 / r)


D2 = lambda R: 1.0 + 4.0 / (R / 1e6)                                                # noqa: E731
lad2, st2 = run_ladder(S2, cap=40)
if st2 == 'CALIBRATED':
    R2 = {k: RR.rj_float(lad2.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
    J2 = RR.judge({('0', 'P0', k): D2(v) for k, v in R2.items()})
    arm0_only = {'lo': lad2.st['ends']['lo']['arm0_end'], 'hi': lad2.st['ends']['hi']['arm0_end']}
    Ja0 = RR.judge({('0', 'P0', 'R_j_lo'): D2(RR.rj_float(arm0_only['lo'])), ('0', 'P0', 'R_j0'): D2(R2['R_j0']),
                    ('0', 'P0', 'R_j_hi'): D2(RR.rj_float(arm0_only['hi']))})
    OUT['2_predes01_union'] = {'status': st2, 'R': R2, 'n_runs': lad2.st['n_runs'], 'pushes': {s: lad2.st['ends'][s]['origin_pushes'] for s in ('lo', 'hi')},
                               'origin_R0': lad2.st['origin'], 'verdict': J2['verdict'], 'W': J2['W'], 'interval': J2['interval_mScm'],
                               'arm0_ends_only': {'R': arm0_only, 'verdict': Ja0['verdict'], 'W': Ja0['W']},
                               'r_union_cont': [0.1 / (TP - 1.53), 0.1 / (TM - 1.53)]}
else:
    OUT['2_predes01_union'] = {'status': st2, 'n_runs': lad2.st['n_runs']}

# ── (2b) sibling: arms 1-2 identical to arm 0, arms 3-7 differ (union of three origins = arm 0 set) ──
def S2b(R, i):
    if R == math.inf:
        return 1.43 if i <= 2 else 1.53
    r = max(R / 1e6, 1e-6)
    return (1.43 + 0.2 / r) if i <= 2 else (1.53 + 0.1 / r)


lad3, st3 = run_ladder(S2b, cap=40)
R3 = {k: RR.rj_float(lad3.st[k]) for k in ('R_j_lo', 'R_j0', 'R_j_hi')}
J3 = RR.judge({('0', 'P0', k): D2(v) for k, v in R3.items()})
mean8 = lambda r: (3 * (1.43 + 0.2 / r) + 5 * (1.53 + 0.1 / r)) / 8                 # noqa: E731
r_lo8, r_hi8 = bisect_inv(lambda r: mean8(r), TP, 1e-6, 1e6), bisect_inv(lambda r: mean8(r), TM, 1e-6, 1e6)
OUT['2b_arms12_equal_arm0'] = {'status': st3, 'R': R3, 'pushes': {s: lad3.st['ends'][s]['origin_pushes'] for s in ('lo', 'hi')},
                               'origin_R0': lad3.st['origin'], 'verdict': J3['verdict'], 'W': J3['W'],
                               'mean8_admissible_r': [r_lo8, r_hi8],
                               'mean8_DBE_W': math.log(D2(r_lo8 * 1e6) / D2(r_hi8 * 1e6)),
                               'mean8_grade': RR.grade_W(math.log(D2(r_lo8 * 1e6) / D2(r_hi8 * 1e6)))}

# ── (3) §4-2 W₊ / states differ — registration [3.0, 5.25] W 0.5596 ──
def fetch13(spec):
    def fetch(kit, role, law, c, rj, arms, sv_cf=False):
        if kit == RR.SBE_KIT:
            return [{'sigma': 1.63e-3, 'n_sdcp_near': 0, 'state': 'positive', 'err_rel': 0.0}]
        (a0, s0), (o12, so), o8 = spec[(c, law)]
        out = []
        idx = list(range(arms)) if isinstance(arms, int) else list(arms)
        for i in idx:
            v, s_ = (a0, s0) if i == 0 else ((o8, 'positive') if isinstance(arms, int) else (o12, so))
            out.append({'sigma': v * 1e-3, 'state': s_, 'n_sdcp_near': 7, 'err_rel': 0.0})
        return out
    return fetch


LADS = {law: {'R_j_lo': '0.5', 'R_j0': '1.0', 'R_j_hi': '2.0', 'r0_sigma': 1.63e-3} for law in ('P0', 'P1')}
spec = {('0', 'P0'): ((0.0, 'zero'), (6.0, 'positive'), 6.0), ('1', 'P0'): ((3.0, 'positive'), (3.0, 'positive'), 3.0),
        ('0', 'P1'): ((3.5, 'positive'), (3.5, 'positive'), 3.5), ('1', 'P1'): ((4.0, 'positive'), (4.0, 'positive'), 4.0)}
pr = RR.Predict(fetch13(spec), LADS, None, sv_scope=None)
try:
    pr.run()
    J4 = RR.judge({k: v * 1e3 for k, v in pr.values().items()})
    OUT['3_W_pos_states'] = {'verdict': J4['verdict'], 'interval': J4['interval_mScm'], 'W': J4['W'],
                             'origin': {f'c{o["c"]}_{o["law"]}': o['status'] for o in pr.origin}}
except RR.Stop as e:
    OUT['3_W_pos_states'] = {'stop': e.code, 'cause': e.cause}
# registration example uses c0P0 zero but c1P0 = 3.0 < c0P0 — is the same-P consistency (c1 >= c0 - tau) honoured? c0=0 -> c1 3 fine.

# ── (4) §5-1 RCA-08 · §5-6 RCA-09 · §4-2 RCA-02 numbers with the real judge ──
J8 = RR.judge({('0', 'P0', 'R_j_lo'): 3.8, ('0', 'P0', 'R_j_hi'): 4.0, ('0', 'P1', 'R_j_lo'): 5.2, ('0', 'P1', 'R_j_hi'): 5.4})
OUT['4a_rca08'] = {'verdict': J8['verdict'], 'W': J8['W'], 'reg': 'GAP_ENVELOPE_ONLY · W 0.3513978868'}
J9a = RR.judge({('0', 'P0', 'R_j_lo'): 4.30, ('0', 'P0', 'R_j0'): 4.40, ('1', 'P0', 'R_j0'): 4.45, ('0', 'P1', 'R_j0'): 4.50,
                ('1', 'P1', 'R_j0'): 4.55, ('1', 'P1', 'R_j_hi'): 4.80})
J9b = RR.judge({('0', 'P0', 'R_j0'): 4.40, ('1', 'P0', 'R_j0'): 4.45, ('0', 'P1', 'R_j0'): 4.50, ('1', 'P1', 'R_j0'): 4.55})
OUT['4b_rca09'] = {'main': [J9a['verdict'], J9a['W']], 'centre4': [J9b['verdict'], J9b['W']], 'reg': 'PASS W 0.1100008952 · FAIL W 0.0335226920'}

# ── (5) §3-2b ③″ example — F = T⁻(1 − 5e-5) · S = F + 0.05/(r + 0.1) · r = R/1e5 ──
F = TM * (1 - 5e-5)
S5 = lambda R, i=0: F if R == math.inf else F + 0.05 / (R / 1e5 + 0.1)              # noqa: E731
D5 = lambda R: 0.5 + 300.0 / (R / 1e5 + 300.0)                                     # noqa: E731
true_hi = (0.05 / (TM - F) - 0.1) * 1e5
low_hi = bisect_inv(lambda R: S5(R) * (1 - 1e-4), TM, 1.0, 1e30)
res5 = {}
for e, read in ((1e-4, 1.0), (4e-5, 1.0), (4e-5, 1 - 4e-5), (0.0, 1 - 1e-4)):
    l5, s5 = run_ladder(S5, err=e, read=read, cap=24)
    res5[f'e={e:g} read={read:.6g}'] = {'status': s5, 'n_runs': l5.st['n_runs'], 'R_j_hi': l5.st.get('R_j_hi')}
OUT['5_guard_band'] = {'abs_F_over_T_minus_1': abs(F / T - 1), 'true_R_hi': true_hi, 'low_reading_R_hi': low_hi,
                       'ratio_true_over_low': true_hi / low_hi, 'lnD_shift': math.log(D5(low_hi) / D5(true_hi)), 'runs': res5,
                       'reg': 'true 6.259e7 · low reading 2.086e7 (×3.0) · ln 0.2797 · e 1e-4 -> CALIB_EDGE · e 4e-5 -> not EDGE'}

# ── (6) §6 RCA-12 numbers ──
RS, RD = 7.016, 2.178
Rc = 1.0
thr = math.log(1 + Rc / (RD - Rc)) / math.log(1 + Rc / (RS - Rc))
OUT['6_rca12'] = {'threshold_Rc1': thr, 'SBE_shift_pct': 100 * (RS / (RS - Rc) - 1), 'reg': '3.9967891509 · +16.62 %'}

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_A_reg_numbers.json')
with open(path, 'w', encoding='utf-8') as f:
    json.dump(OUT, f, ensure_ascii=False, indent=1, default=str)
for k, v in OUT.items():
    print('==', k)
    print(json.dumps(v, ensure_ascii=False, default=str)[:1500])
