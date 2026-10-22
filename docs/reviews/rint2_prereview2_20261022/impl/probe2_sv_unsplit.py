# -*- coding: utf-8 -*-
"""탐침 2-A (Q-D 옆 자리) — SV 반사실이 '못 가른 다리' (서로 다른 두 섬유가 같은 SDCP 성분을 지남) 를 그대로 두고 비를 'computed' 로 내는가.
등록 R 4판 §5-6 SV 행: 끊는 것 = 한 SDCP 성분을 거쳐 다른 섬유로 넘어가는 길.  대조를 못 하면 SV_UNCHECKED.
회로 (vox 1 · 셀 단위 · 손으로 풀림):
  A = 아래 판 (z 0.5) → z 6.5 끝 (위 판에 안 닿음) · B = z 2.5 끝 → 위 판 (z 8.5) · A ↔ B 중심선 2.0 > D 1.1 (접합 없음).
  SDCP 성분 = (1,1,4) (2,1,4) (3,1,4) 세 셀 — A · B 둘 다 그 성분을 지난다 (z 4 셀이 SDCP 로 덮임).
  ⇒ 아래 → 위 길은 A → SDCP 셋 → B 하나뿐.  다른 섬유 사이 SV 우회를 끊으면 G_cut = 0 → 비 = +∞ (참).
 대조 ① B 가 성분 안에서 시작 (B = z 4.5 → 8.5) — A 만 지남 · B 는 지나지 않음 → B 쪽 SV 면을 끊는다 → 비 +∞.
 대조 ② 같은 회로 + A · B 를 SDCP 밖에서 잇는 접합 (B 아래 끝을 A 옆까지) — 우회와 병렬 길이 있다 → 비 유한 > 1."""
import math
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import rint_r_chain as RRC     # noqa: E402
import ca_ext_svcf as SVCF     # noqa: E402

out = {}
rj = 1e3
N = (5, 3, 9)


def run(tag, polys, sdcp_pts):
    P = rows(polys)
    P = cat_rows(P, rows([[p] for p in sdcp_pts], phase=5, kind=0, fid0=700))
    sid, _ = bed(P, N, sdcp_sphere_d_um=0.0)
    reg = registry(sid, P, tol_sj_um=0.1, r_sdcp_um=0.5)
    r = solve(sid, sig_e(), N, plan(reg, rj, sv_counterfactual={'threshold': None}))
    cj = r.get('cjunc') or {}
    cf = cj.get('sv_counterfactual') or {}
    proj = SVCF.sv_cf_record(cf)
    view = SVCF.chain_view(proj)
    # 사슬의 SV 판정 (문턱 2.0 · R_j,0 만) — 이 모서리 하나
    flags, per = RRC.sv_assess({('1', 'P0', 'R_j0'): {'sv_cf': view}}, 2.0, 'R_j0')
    cen = reg['census']
    d = {'sid_at_A_z4': int(sid[1, 1, 4]), 'sid_at_B_z4': int(sid[3, 1, 4]), 'n_sdcp_cells': int((sid == 5).sum()),
         'n_instances': int(len(reg['instances']['fi'])), 'I_full': I_of(r, N), 'reason': r.get('reason'),
         'cf_status': cf.get('status'), 'cf_ratio': cf.get('sv_counterfactual_ratio'), 'n_sv_faces_cut': cf.get('n_sv_faces_cut'),
         'n_bridging_components': cf.get('n_bridging_components'), 'n_unsplit_bridging_components': cf.get('n_unsplit_bridging_components'),
         'census_n_sdcp_bridging_components': cen.get('n_sdcp_bridging_components'),
         'chain_view': view, 'chain_flags_threshold_2': flags}
    out[tag] = d
    print(tag, d)


SD = [(1.5, 1.5, 4.5), (2.5, 1.5, 4.5), (3.5, 1.5, 4.5)]
A = [(1.5, 1.5, 0.5), (1.5, 1.5, 6.5)]
B = [(3.5, 1.5, 2.5), (3.5, 1.5, 8.5)]
run('two_fibres_pass_same_sdcp (truth ratio = +inf)', [A, B], SD)
B1 = [(3.5, 1.5, 4.5), (3.5, 1.5, 8.5)]
run('control1_only_A_passes (truth ratio = +inf)', [A, B1], SD)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_sv_unsplit.json'), out)
