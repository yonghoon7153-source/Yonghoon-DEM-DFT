# -*- coding: utf-8 -*-
"""탐침 A1b — A1 을 생산 단위로: vox 0.15 µm · r_f 0.075 · tol_ff 0.03 · L_par 0.30 · r_port 0.30 · 점 간격 0.05 µm ·
끊기 틈 0.12 µm (> gap_tol 2 × 중앙 간격 0.05) · s_min 0.3 µm (가정 값 — 등록 전 · 시험용).
두 끝이 같은 셀 (z 셀 3 = [0.45, 0.60)) · 면 인접 셀 ((1,1,2)|(1,1,3)) 두 꼴 · σ_VGCF 7853.98 (직경 보존) · 옛 경로 (접합 끔) 대조."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

VOX = 0.15
N = (3, 3, 8)
out = {}


def col(z0, z1, step=0.05):
    return densify([(0.225, 0.225, z0), (0.225, 0.225, z1)], step)


def run(tag, z_end, z_start, s_min):
    pts = np.vstack([col(0.075, z_end), col(z_start, 1.125)])
    P = rows_pts([pts], fids=[10])
    sid, _ = bed(P, N, vox=VOX)
    reg = registry(sid, P, vox=VOX, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30, r_port_um=0.30, s_min_um=s_min)
    sig = sig_e(s_vgcf=7853.98, s_am=0.0041)
    r = solve(sid, sig, N, plan(reg, 1e6), vox=VOX)
    with direct_solver():
        rl = quiet(S3.solve_sigma_z, sid, sig, VOX, z_top_um=float(N[2]) * VOX, z_bot_um=0.0)
    c = reg['census']
    d = {'gap_um': round(z_start - z_end, 6), 'n_pieces': c.get('n_pieces'), 'n_self_candidates': c.get('n_self_candidates'),
         'n_self_revisits_path_only': c.get('n_self_revisits_path_only'), 'n_self_fused_faces': c.get('n_self_fused_faces'),
         'self_s_um': c.get('self_s_um'), 'sigma_cjunc': r['sigma_eff'], 'reason': r.get('reason'),
         'sigma_legacy_off': rl['sigma_eff']}
    out[tag] = d
    print(tag, d)


run('same_cell (ends z 0.47 · 0.59)', 0.47, 0.59, 0.3)
run('face_adjacent (ends z 0.40 · 0.52)', 0.40, 0.52, 0.3)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_gap_revisit_prod.json'), out)
