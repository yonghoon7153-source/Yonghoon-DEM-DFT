# -*- coding: utf-8 -*-
"""탐침 A4b — A4 의 포트 옮김이 SDCP 덮임 (생산 규약 = SDCP 가 VGCF 셀을 덮는다 · PTFE 규약 무관) 에서도 생기는가.
F2 꼴 (A 위끝 ↔ B 아래끝 접점) · SDCP 점 스탬프가 A 위끝 셀 (1,1,3) 을 덮음 → 접합 포트 = (1,1,2) 로 옮김 + SDCP 셀이 A · B 를 SV 면 (융합) 으로 잇는다.
손 회로: ① 옮긴 접합 + SV 융합 두 면 (병렬) ② SV 융합만 (접합 끔 = R_j ∞) — 옮긴 접합이 그 위에 더하는 몫."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N = (5, 3, 8)
F2 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(2.5, 1.5, 3.5), (2.5, 1.5, 7.5)]]
rj = 1e3
P = cat_rows(rows(F2), rows([[(1.5, 1.5, 3.5)]], phase=5, kind=0, fid0=700))
sid, _ = bed(P, N)
reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
inst = reg['instances']; pos = reg['positions']
ports = [(tuple(int(v) for v in pos['ijk'][a]), tuple(int(v) for v in pos['ijk'][b])) for a, b in zip(inst['port_i'], inst['port_j'])]
I_j = I_of(solve(sid, sig_e(), N, plan(reg, rj, ptfe_stamp='face_alpha')), N)
I_inf = I_of(solve(sid, sig_e(), N, plan(reg, math.inf, allow_rj_limits=True, ptfe_stamp='face_alpha')), N)
gsv = 2.0 * SV * 250.0 / (SV + 250.0) * H
# 노드: A0 A1 A2 (1,1,0..2) · S (1,1,3) SDCP · B0..B4 (2,1,3..7)
nA, S, B0 = 3, 3, 4
E = [(0, 1, G_AX), (1, 2, G_AX), (2, S, gsv), (S, B0, gsv)] + [(B0 + i, B0 + i + 1, G_AX) for i in range(4)]
w_sv_only = ref_I(9, E, [(0, G_PL)], [(B0 + 4, G_PL)])
w_sv_plus_relocated = ref_I(9, E + [(2, B0, 1e4 / rj)], [(0, G_PL)], [(B0 + 4, G_PL)])
out = {'sid_A_top': int(sid[1, 1, 3]), 'ports': ports, 'I_Rj_1e3': I_j, 'I_Rj_inf': I_inf,
       'hand_sv_only': w_sv_only, 'hand_sv_plus_relocated_junction': w_sv_plus_relocated,
       'relocated_junction_adds_rel': I_j / I_inf - 1.0}
print(out)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_sdcp_relocate.json'), out)
