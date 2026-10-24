#!/usr/bin/env python3
"""Round-4 probe — (1) shadow runs + unsealed assignment = machine choice after seeing σ (design L134 · L141 · Q-G);
(2) ladder-stage nominal-vs-threshold points that rev 3's knife list (L135–L136, '전부') does not name, now that rev 3 runs the two
ladders on two machines (L58 · L171).  Uses the REAL chain functions (`judge`, `sig3`, `interp_lnln`, `CONFIRM_TOL`, `sbe_origin_ok`).
Machine bit differences are modelled as relative 1e-10 (design §3-1 L55: measured 1.3e-10 – 5.8e-10 between BLAS paths).
"""
import json
import sys

sys.path.insert(0, sys.argv[1])
import rint_r_chain as C  # noqa: E402

D = 2e-10
out = {}
# (1) one unit's σ sits on the 4.68 mS/cm edge; the other 11 corners are inside a narrow band below it
base = {('0', 'P0', 'R_j_lo'): 4.40, ('0', 'P0', 'R_j0'): 4.35, ('0', 'P0', 'R_j_hi'): 4.30,
        ('1', 'P0', 'R_j_lo'): 4.62, ('1', 'P0', 'R_j0'): 4.60, ('1', 'P0', 'R_j_hi'): 4.45,
        ('0', 'P1', 'R_j_lo'): 4.10, ('0', 'P1', 'R_j0'): 4.05, ('0', 'P1', 'R_j_hi'): 4.00,
        ('1', 'P1', 'R_j_lo'): 4.20, ('1', 'P1', 'R_j0'): 4.15, ('1', 'P1', 'R_j_hi'): 4.10}
edge_unit = ('1', 'P0', 'R_j_lo')
for mach, f in (('kgy', 1 - D), ('gabia', 1 + D)):
    v = dict(base)
    v[edge_unit] = C.EXP_DBE_MS * f
    J = C.judge(v)
    out[f'shadow_{mach}'] = {'edge_unit_mScm': repr(v[edge_unit]), 'verdict': J['verdict'], 'in_U': J['in_U'], 'W': J['W']}
out['shadow_note'] = ('run U(c1,P0,R_j_lo) outside the ledger on both machines (L134 allows it) → commit ONE ledger entry on the machine '
                      'whose verdict you prefer → it is the first attempt, order/start-sha/prefix checks pass, nothing after it')
# (2a) ladder R_j,0 = sig3(interp_lnln(...)) — rounding boundary
Ra, Rb, sb = 1.0e6, 1.0e7, 1.50e-3
T = C.TARGET_SBE_MS * 1e-3
# choose sa so that the interpolated R lands just on a 3-digit rounding boundary (1.235e6), then shift sa by ±D
import math  # noqa: E402
target_R = 1.235e6
t = (math.log(target_R) - math.log(Ra)) / (math.log(Rb) - math.log(Ra))
sa = math.exp((math.log(T) - t * math.log(sb)) / (1 - t))
r = {}
for mach, f in (('kgy', 1 - D), ('gabia', 1 + D)):
    R = C.interp_lnln(Ra, sa * f, Rb, sb, T)
    r[mach] = {'interp_R': repr(R), 'R_j0 = sig3': C.sig3(R)}
out['ladder_sig3_rounding'] = r
# (2b) ladder confirm `abs(s0/T - 1) <= CONFIRM_TOL` (no guard band, unlike edge_hit/outside_band)
c = {}
for mach, f in (('kgy', 1 - D), ('gabia', 1 + D)):
    s0 = T * (1 + C.CONFIRM_TOL) * f
    c[mach] = abs(s0 / T - 1.0) <= C.CONFIRM_TOL
out['ladder_confirm_tol'] = c
# (2c) SBE origin check (blocking flag CALIB_ORIGIN_SENSITIVE when it fails) — ln(max/min) <= 0.02
o = {}
for mach, f in (('kgy', 1 - D), ('gabia', 1 + D)):
    vals = [1.0, 1.0, math.exp(C.ORIGIN_SBE_MAX) * f]
    o[mach] = C.sbe_origin_ok(vals)[0]
out['ladder_sbe_origin_0.02'] = o
print(json.dumps(out, ensure_ascii=False, indent=1))
