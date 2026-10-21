# -*- coding: utf-8 -*-
"""탐침 A2 (RCA-03 · 04 옆 자리) — 자기 접합 (같은 fid) 탐지 = 셀 인접 (같은 셀 · 면) · 서로 다른 섬유 = 중심선 거리 ≤ D = 2 r_f + tol_ff.
같은 두 가닥 기하에서 fid 가 같은지 다른지로 접합 유무가 갈리는가.
 (i)  두 다리 중심선 거리 1.2 > D 1.1 (닿지 않음 · 면 인접 셀) — 같은 fid = R_j 접합 · 다른 fid = instance 0 (미등록 면 · cut)
 (ii) 두 다리 중심선 거리 0.1414 < 2 r_f = 1.0 (닿음 · 모서리 인접 셀 · 공유 면 없음) — 같은 fid = 접합 0 · 다른 fid = instance 1"""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

out = {}
rj = 1e3
# (i) KW (시험 KINK 의 U · 다리 2 x 2.7) — 같은 fid
KU_N = (6, 3, 8)
KW = [[(1.5, 1.5, 0.5), (1.5, 1.5, 4.5), (2.7, 1.5, 4.5), (2.7, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]]
P = rows(KW)
sid, _ = bed(P, KU_N)
reg = registry(sid, P, s_min_um=1.0)
I_j = I_of(solve(sid, sig_e(), KU_N, plan(reg, rj)), KU_N)
I_inf = I_of(solve(sid, sig_e(), KU_N, plan(reg, math.inf, allow_rj_limits=True)), KU_N)
inst = reg['instances']
out['i_same_fid'] = {'n_self_instances': int(inst['self'].sum()), 'Lc': inst['Lc'].tolist(), 'mult': inst['mult'].tolist(),
                     'centreline_gap_um': 1.2, 'D_um': 2 * RF + TOL, 'I_Rj_1e3': I_j, 'I_Rj_inf': I_inf,
                     'junction_effect_rel': (I_j - I_inf) / I_inf}
# (i) 같은 다리 둘 = 다른 fid (다리 1 = 아래 판 → z 4.5 끝 · 다리 2 = z 4.5 → 1.5 → 오른쪽 → 위 판) — 위 가로를 끊은 꼴 (위상 다름 · 판정만 본다)
A = [(1.5, 1.5, 0.5), (1.5, 1.5, 4.5)]
B = [(2.7, 1.5, 4.5), (2.7, 1.5, 1.5), (4.5, 1.5, 1.5), (4.5, 1.5, 7.5)]
P2 = rows([A, B])
sid2, _ = bed(P2, KU_N)
reg2 = registry(sid2, P2, s_min_um=1.0)
i2 = reg2['instances']
out['i_distinct_fids'] = {'n_instances': int(len(i2['fi'])), 'n_unreg_faces': reg2['census'].get('n_unreg_faces'),
                          'n_cut_site_faces': reg2['census'].get('n_cut_site_faces'), 'd0': i2['d0'].tolist()}
# (ii) 모서리 인접 두 다리 (중심선 0.1414 · 닿음) — 같은 fid: 다리 1 (1.95,1.95) 위로 → 먼 길 (y +) 로 돌아 → 다리 2 (2.05, 2.05) 아래로
N2 = (5, 8, 8)
SF = [[(1.95, 1.95, 0.5), (1.95, 1.95, 3.5), (1.95, 6.5, 3.5), (1.95, 6.5, 6.5), (2.05, 6.5, 6.5), (2.05, 6.5, 6.6),
       (3.5, 6.5, 6.6), (3.5, 2.05, 6.6), (2.05, 2.05, 6.6), (2.05, 2.05, 1.5)]]
P3 = rows(SF)
sid3, _ = bed(P3, N2)
reg3 = registry(sid3, P3, s_min_um=1.0)
i3 = reg3['instances']
# 다리 1 · 다리 2 사이 기하 최근접 (중심선)
seg = reg3['segments']
leg1 = (seg['P0'][:, 0] == 1.95) & (seg['P1'][:, 0] == 1.95) & (seg['P0'][:, 1] == 1.95) & (seg['P1'][:, 1] == 1.95)
leg2 = (seg['P0'][:, 0] == 2.05) & (seg['P1'][:, 0] == 2.05) & (seg['P0'][:, 1] == 2.05) & (seg['P1'][:, 1] == 2.05)
d_min = None
if leg1.any() and leg2.any():
    a = np.flatnonzero(leg1); b = np.flatnonzero(leg2)
    ia = np.repeat(a, len(b)); ib = np.tile(b, len(a))
    d, *_ = CJ.seg_seg_closest(seg['P0'][ia], seg['P1'][ia], seg['P0'][ib], seg['P1'][ib])
    d_min = float(d.min())
# 다리 2 근처 자기 instance 가 있는가 (포트 셀이 x 1 · 2 기둥 (1,1,*) ↔ (2,2,*) 인 자기 instance)
pos = reg3['positions']
pairs = []
for q in range(len(i3['fi'])):
    pi, pj = int(i3['port_i'][q]), int(i3['port_j'][q])
    if pi >= 0 and pj >= 0:
        pairs.append((bool(i3['self'][q]), tuple(int(v) for v in pos['ijk'][pi]), tuple(int(v) for v in pos['ijk'][pj]),
                      float(i3['s'][q]) if i3['self'][q] else None))
legpair = [p for p in pairs if {p[1][:2], p[2][:2]} == {(1, 1), (2, 2)}]
out['ii_same_fid'] = {'leg_centreline_min_um': d_min, '2rf': 2 * RF, 'self_instances_between_legs': legpair,
                      'all_instances': pairs}
# (ii) 다른 fid — 다리 1 (아래 판 → z 3.5) · 다리 2 (z 6.6 → 1.5 아래로 · 위 판 쪽으로는 이어진 가로 · 같은 기하)
A3 = SF[0][:2]
B3 = SF[0][8:]
P4 = rows([A3, B3])
sid4, _ = bed(P4, N2)
reg4 = registry(sid4, P4, s_min_um=1.0)
i4 = reg4['instances']
out['ii_distinct_fids'] = {'n_instances': int(len(i4['fi'])), 'd0': i4['d0'].tolist(), 'Lc': i4['Lc'].tolist()}
for k, v in out.items():
    print(k, v)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_self_vs_distinct.json'), out)
