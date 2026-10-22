# -*- coding: utf-8 -*-
"""탐침 A6 (RCA-03 옆 자리 · 닫힌 고리) — 첫 점 = 끝 점인 섬유 (연속 고리).  이음매 셀에 첫 위치 · 끝 위치 = 같은 셀 재방문 (s = 고리 길이).
s ≥ s_min 이면 이음매가 R_j 접합이 된다 (연속 가닥인데) · 옛 (cell, fid) = 한 dof (연속).
고리: 왼 다리 x 1.5 (z 0.5 → 7.5) · 위 가로 · 오른 다리 x 3.5 · 아래 가로 · 이음매 = 왼 다리 가운데 z 4.2.
손 회로 (연속 고리) = 셀 열 직렬 사슬을 고리로 닫은 것 + 아래 · 위 판 (각 다리 맨 아래 · 맨 위 셀)."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N = (5, 3, 8)
RING = [(1.5, 1.5, 4.2), (1.5, 1.5, 7.5), (3.5, 1.5, 7.5), (3.5, 1.5, 0.5), (1.5, 1.5, 0.5), (1.5, 1.5, 4.2)]
P = rows([RING])
sid, _ = bed(P, N)
out = {}
for tag, smin in (('s_min_3 (s ≥ s_min)', 3.0), ('s_min_100 (s < s_min)', 100.0)):
    reg = registry(sid, P, s_min_um=smin)
    c = reg['census']
    r = solve(sid, sig_e(), N, plan(reg, 1e3))
    out[tag] = {'n_self_instances': int(reg['instances']['self'].sum()), 'self_s': c.get('self_s_um'),
                'n_revisit_pairs': c.get('n_revisit_pairs'), 'path_only': c.get('n_self_revisits_path_only'),
                'I': I_of(r, N), 'reason': r.get('reason')}
with direct_solver():
    rl = quiet(S3.solve_sigma_z, sid, sig_e(), H, z_top_um=float(N[2]), z_bot_um=0.0)
out['legacy_off'] = {'I': I_of(rl, N)}
# 손 회로 — 연속 고리 (셀 = 고리 셀 열 · 이웃 축 면) · 판 = z 0 셀 (아래) · z 7 셀 (위) 전부 (셀 중심이 판에서 h/2)
cells = []
from fibre_segment_raster import segment_cells
pts = densify(RING)
for i in range(len(pts) - 1):
    for cc in segment_cells(pts[i], pts[i + 1], H):
        t = tuple(int(v) for v in cc)
        if not cells or cells[-1] != t:
            cells.append(t)
uniq = sorted(set(cells))
ix = {c: i for i, c in enumerate(uniq)}
E = set()
for a, b in zip(cells[:-1], cells[1:]):
    if a != b:
        E.add(tuple(sorted((ix[a], ix[b]))))
edges = [(a, b, G_AX) for a, b in E]
bot = [(ix[c], G_PL) for c in uniq if c[2] == 0]
top = [(ix[c], G_PL) for c in uniq if c[2] == N[2] - 1]
out['hand_continuous_ring'] = ref_I(len(uniq), edges, bot, top)
for k, v in out.items():
    print(k, v)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_closed_loop.json'), out)
