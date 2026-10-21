# -*- coding: utf-8 -*-
"""탐침 A4 (Z3 · Rayleigh 단조 옆 자리) — PTFE 를 늘리면 σ 가 커지면 안 된다 (절연체 추가).
centerline 스탬프 (P0 · 접합과 함께 허용) 에서 PTFE 피브릴이 접합 포트 셀 (A 의 위끝 셀) 을 덮으면 그 셀이 sid 7 → 포트가 r_port 안
다른 셀로 옮겨진다.  A 의 축 면 하나가 빠진 짧은 길로 접합이 다시 붙으면 σ 가 **오른다** (Rayleigh 위반).
F2 꼴: A (1,1,0..3) 아래 판 · B (2,1,3..7) 위 판 · 접점 = A 위끝 ↔ B 아래끝 (면 인접 · 중심선 1.0 = 2 r_f).
손 회로: 전 = 판 + A 3 면 + R_j + B 4 면 + 판 · 후 = 판 + A 2 면 + R_j + B 4 면 + 판."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N = (5, 3, 8)
F2 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(2.5, 1.5, 3.5), (2.5, 1.5, 7.5)]]
PT = [[(1.5, 0.5, 3.5), (1.5, 2.5, 3.5)]]           # A 위끝 셀 (1,1,3) 을 지나는 PTFE 피브릴 (y 방향) — B 셀은 안 덮는다
rj = 1e3
out = {}
for tag, with_ptfe in (('no_ptfe', False), ('ptfe_centerline_on_port_cell', True)):
    P = rows(F2)
    if with_ptfe:
        P = cat_rows(P, rows(PT, phase=4, fid0=900))
    sid, _ = bed(P, N)
    reg = registry(sid, P)
    inst = reg['instances']; pos = reg['positions']
    pl = plan(reg, rj, ptfe_stamp='centerline', ptfe_jlaw='P0')
    r = solve(sid, sig_e(), N, pl)
    ports = [(tuple(int(v) for v in pos['ijk'][a]), tuple(int(v) for v in pos['ijk'][b])) for a, b in zip(inst['port_i'], inst['port_j'])]
    out[tag] = {'n_ptfe_cells': int((sid == 7).sum()), 'A_top_cell_sid': int(sid[1, 1, 3]), 'ports': ports,
                'realized': inst['realized'].tolist(), 'I': I_of(r, N), 'reason': r.get('reason')}
    print(tag, out[tag])
w_before = chain_I([G_PL] + [G_AX] * 3 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
w_after_relocated = chain_I([G_PL] + [G_AX] * 2 + [1e4 / rj] + [G_AX] * 4 + [G_PL])
out['hand'] = {'before': w_before, 'after_if_port_relocated': w_after_relocated}
out['sigma_increase_rel'] = out['ptfe_centerline_on_port_cell']['I'] / out['no_ptfe']['I'] - 1.0
print('hand', out['hand'], 'σ 변화 (PTFE 추가 뒤 / 전 − 1)', out['sigma_increase_rel'])
# 같은 침대 · cjunc 끔 (옛 경로) — PTFE 추가로 σ 가 줄어드는지 (대조)
with direct_solver():
    for tag, with_ptfe in (('legacy_no_ptfe', False), ('legacy_ptfe', True)):
        P = rows(F2)
        if with_ptfe:
            P = cat_rows(P, rows(PT, phase=4, fid0=900))
        sid, _ = bed(P, N)
        r = quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(N[2]), z_bot_um=0.0)
        out[tag] = {'I': I_of(r, N), 'reason': r.get('reason')}
        print(tag, out[tag])
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_ptfe_monotone.json'), out)
