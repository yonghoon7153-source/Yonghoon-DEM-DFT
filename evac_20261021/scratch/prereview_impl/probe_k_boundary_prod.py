# -*- coding: utf-8 -*-
"""탐침 A3b — A3 (k 경계 σ 뜀) 크기를 생산 단위로: vox 0.15 · r_f 0.075 · L_par 0.30 · r_port 0.30 · σ_VGCF 7853.98 ·
R_j ∈ {1e2, 1e4, 1e6} Ω (사다리 출발 1e4 · 1e6 · 1e8 · ×100 연장).  깊은 교차를 90° → 89.99° 로 기울여 k 1 → 2."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

VOX = 0.15
N = (9, 3, 10)
out = {}


def run(theta_deg, rj):
    th = math.radians(theta_deg)
    C = np.array([3.5, 1.5, 3.5]) * VOX
    u = np.array([math.sin(th), 0.0, math.cos(th)])
    b0 = C - 3.0 * VOX * u
    b1 = C + 3.0 * VOX * u
    A = [(3.5 * VOX, 1.5 * VOX, 0.5 * VOX), (3.5 * VOX, 1.5 * VOX, 5.5 * VOX)]
    B = [tuple(b0), tuple(b1), (b1[0], 1.5 * VOX, 9.5 * VOX)]
    P = rows([A, B], step=0.05)
    sid, _ = bed(P, N, vox=VOX)
    reg = registry(sid, P, vox=VOX, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30, r_port_um=0.30, s_min_um=3.0)
    r = solve(sid, sig_e(s_vgcf=7853.98, s_am=0.0041), N, plan(reg, rj), vox=VOX)
    return int(reg['instances']['nsub'][0]), r['sigma_eff'], hash(sid.tobytes())


for rj in (1e2, 1e4, 1e6):
    k0, s0, h0 = run(90.0, rj)
    k1, s1, h1 = run(89.99, rj)
    out[f'Rj_{rj:g}'] = {'k_90': k0, 'k_89.99': k1, 'sigma_90': s0, 'sigma_89.99': s1, 'jump_rel': s1 / s0 - 1.0,
                         'same_sid': h0 == h1}
    print(rj, out[f'Rj_{rj:g}'])
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_k_boundary_prod.json'), out)
