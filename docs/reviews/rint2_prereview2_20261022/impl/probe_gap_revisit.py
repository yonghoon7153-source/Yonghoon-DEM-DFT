# -*- coding: utf-8 -*-
"""탐침 A1 (RCA-03 옆 자리) — 같은 fid 의 끊기 (fibre_pieces gap) 두 끝이 같은 셀 / 면 인접 셀에 놓일 때.
설계 문장: s < s_min = '같은 가닥의 연속 (접합 아님 · 면 = 옛 융합 그대로)' · 재방문 = '경로로만 이어진다'.
끊긴 조각 사이에는 경로 (축방향 간선) 가 없다 → 같은 셀이면 이음이 없어진다 (면 인접이면 옛 융합).
기대 (설계 문장 기준) = 두 꼴 모두 같은 가닥의 연속 = 옛 경로 (cjunc 끔) 와 같은 사슬.  손 회로 = 8 셀 직렬 사슬."""
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N = (3, 3, 8)
out = {}


def column(z0, z1, step=0.25):
    return densify([(1.5, 1.5, z0), (1.5, 1.5, z1)], step)


def run(tag, p1_end, p2_start, s_min):
    pts = np.vstack([column(0.5, p1_end), column(p2_start, 7.5)])
    P = rows_pts([pts], fids=[10])
    sid, _ = bed(P, N)
    reg = registry(sid, P, s_min_um=s_min)
    cen = reg['census']
    pl = plan(reg, 1e3)
    try:
        r = solve(sid, sig_e(), N, pl)
        I = I_of(r, N); why = r.get('reason')
    except Exception as e:                       # noqa: BLE001
        I, why = None, f'{type(e).__name__}: {e}'
    with direct_solver():
        rl = quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(N[2]), z_bot_um=0.0)
    I_leg = I_of(rl, N)
    I_chain = chain_I([G_PL] + [G_AX] * 7 + [G_PL])
    I_rj = chain_I([G_PL] + [G_AX] * 7 + [G_PL] + [1e4 / 1e3])   # 같은 셀 두 위치 사이 R_j 간선 하나 (직렬)
    d = {'pieces': int(len(set(reg['positions']['piece'].tolist()))),
         'gap_um': p2_start - p1_end, 's_min': s_min,
         'census': {k: cen.get(k) for k in ('n_self_candidates', 'n_self_kept', 'n_self_filtered', 'n_self_fused_faces',
                                            'n_self_revisits_path_only', 'n_revisit_pairs', 'self_s_um')},
         'I_cjunc': I, 'reason': why, 'I_legacy_cjunc_off': I_leg, 'I_hand_chain': I_chain, 'I_hand_chain_plus_Rj': I_rj}
    out[tag] = d
    print(tag, d)


# 같은 셀 (1,1,3) 에 두 끝 (z 3.15 · 3.85 · 틈 0.70 > 2 × 중앙 간격)
run('same_cell_gap_s<s_min', 3.15, 3.85, 3.0)
run('same_cell_gap_s>=s_min', 3.15, 3.85, 0.5)
# 면 인접 셀 (1,1,2)|(1,1,3) 에 두 끝 (z 2.85 · 3.5 · 틈 0.65)
run('face_adjacent_gap_s<s_min', 2.85, 3.5, 3.0)
run('face_adjacent_gap_s>=s_min', 2.85, 3.5, 0.5)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_gap_revisit.json'), out)
