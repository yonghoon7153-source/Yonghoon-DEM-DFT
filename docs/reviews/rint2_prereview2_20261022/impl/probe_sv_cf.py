# -*- coding: utf-8 -*-
"""탐침 A5 (RCA-06 옆 자리) — SV 반사실 대조 (SV 면 = VGCF|SDCP 면을 전부 끊는다) 가 재는 것.
설계 뜻 = 'SV 융합 우회가 VV 접합을 대신하는가' 의 크기.  그런데 SDCP 구가 섬유 셀을 덮으면 (생산 규약 = SDCP 가 VGCF 를 덮는다)
그 섬유의 연속 자체가 SV 면을 지난다 → 접합 우회가 0 이어도 비 = ∞ (no_through_without_sv).
 ① 섬유 하나 (접합 0) · 가운데 SDCP 구가 섬유 셀을 덮음 → 비?
 ② F1 (접합 하나) + SDCP 구가 A 가닥 아래쪽 (접합에서 먼 곳) 셀을 덮음 → 비?  (우회 아님 · 접합은 그대로 지남)"""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

out = {}
rj = 1e3


def run(tag, polys, sdcp_pts, n, d_sdcp):
    P = rows(polys)
    if sdcp_pts:
        P = cat_rows(P, rows([[p] for p in sdcp_pts], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, n, sdcp_sphere_d_um=d_sdcp)
    reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
    r = solve(sid, sig_e(), n, plan(reg, rj, sv_counterfactual={'threshold': 2.0}))
    cj = r.get('cjunc') or {}
    cf = cj.get('sv_counterfactual') or {}
    d = {'n_sdcp_cells': int((sid == 5).sum()), 'n_instances': int(len(reg['instances']['fi'])),
         'n_junction_edges': cj.get('n_junction_edges'), 'I': I_of(r, n), 'reason': r.get('reason'),
         'cf_status': cf.get('status'), 'cf_ratio': cf.get('sv_counterfactual_ratio'), 'cf_flag': cf.get('flag'),
         'n_sv_faces_cut': cf.get('n_sv_faces_cut'), 'sv_local_dissipation': cj.get('sv_local_dissipation')}
    out[tag] = d
    print(tag, d)


# ① 섬유 하나 (아래 판 → 위 판) · 가운데 (z 3.5) SDCP 구 (지름 1.0 = 셀 하나 · 그 셀 = sid 5)
run('single_fibre_sdcp_on_path', [[(1.5, 1.5, 0.5), (1.5, 1.5, 7.5)]], [(1.5, 1.5, 3.5)], (3, 3, 8), 0.0)
# ② F1 (A 아래 판 (1,1,0..3) → B (1..4,1,3) → (4,1,4..7) 위 판 · 접합 하나 (교차 셀)) · SDCP 구 = A 의 (1,1,1) 셀 (접합에서 먼 곳)
F1 = [[(1.5, 1.5, 0.5), (1.5, 1.5, 3.5)], [(1.5, 1.5, 3.5), (4.5, 1.5, 3.5), (4.5, 1.5, 7.5)]]
run('F1_junction_sdcp_on_A_far', F1, [(1.5, 1.5, 1.5)], (6, 3, 8), 0.0)
run('F1_junction_no_sdcp', F1, [], (6, 3, 8), 0.0)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_sv_cf.json'), out)
