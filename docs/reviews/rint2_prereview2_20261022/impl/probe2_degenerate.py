# -*- coding: utf-8 -*-
"""탐침 2-옆 (Q-A · Q-B 옆 자리) — 0 길이 선분 (같은 점 두 번) · 셀 경계 위 꼭짓점 · 셋 이상 재방문 (같은 셀을 세 번 지나는 섬유).
① · ② 정답 = 그 점이 없는 같은 기하의 직선 섬유 (손 사슬 8 셀) — 원장이 가짜 자기 접합 · 끊김을 만들면 σ 가 다르다.
③ 세 번 지남 (먼 길로 돌아 같은 셀 (1,1,3) 을 세 번 · 서로 중심선 0.1 · 0.2 떨어짐 · s 큼) — 같은 셀 가지 셋 · 쌍마다 d ≤ D 면 접합 셋 ·
   기대 = 쌍마다 자기 접합 (합치지 않음) · σ = 손 회로 (가지 셋 · 접합 간선 셋 · 축방향 사슬)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N = (3, 3, 8)
out = {}
base_pts = densify([(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)])
I_hand = chain_I([G_PL] + [G_AX] * 7 + [G_PL])


def solve_pts(pts, tag, **rk):
    P = rows_pts([pts], fids=[10])
    sid, _ = bed(P, N)
    reg = registry(sid, P, **rk)
    r = solve(sid, sig_e(), N, plan(reg, 1e3))
    I = I_of(r, N)
    c = reg['census']
    d = {'I': I, 'I_hand': I_hand, 'rel': rel(I, I_hand), 'reason': r.get('reason'), 'n_pieces': c.get('n_pieces'),
         'n_instances': c.get('n_instances'), 'n_self_candidates': c.get('n_self_candidates'), 'n_revisit_pairs': c.get('n_revisit_pairs'),
         'rejections': [x.get('code') for x in reg['rejections']]}
    out[tag] = d
    print(tag, d)


# ① 0 길이 선분 — 가운데 점 하나를 두 번
i = len(base_pts) // 2
solve_pts(np.vstack([base_pts[:i + 1], base_pts[i:]]), 'zero_length_segment')
# ①b 0 길이 선분 셋 연속
solve_pts(np.vstack([base_pts[:i + 1], base_pts[i:i + 1], base_pts[i:i + 1], base_pts[i:]]), 'zero_length_x3')
# ② 셀 경계 위 꼭짓점 (z 3.0 · 4.0 정확히) — densify 가 이미 0.25 간격이라 z 3.0 은 꼭짓점
solve_pts(densify([(1.5, 1.5, 0.5), (1.5, 1.5, 3.0), (1.5, 1.5, 4.0), (1.5, 1.5, 7.5)], 0.5), 'vertex_on_cell_faces')
# ② b 꼭짓점이 셀 모서리 (x 1.0 · z 3.0) 위 — 섬유가 모서리를 스친다 (기울어진 두 선분)
solve_pts(densify([(1.5, 1.5, 0.5), (1.0, 1.5, 3.0), (1.5, 1.5, 7.5)], 0.25), 'vertex_on_cell_edge (bent · hand = n/a)')
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_degenerate.json'), out)
