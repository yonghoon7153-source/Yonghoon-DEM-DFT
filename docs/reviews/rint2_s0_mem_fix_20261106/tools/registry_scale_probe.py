#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""원장 규모 탐침 (2026-11-06 · `SELF-155` 고침 뒤) — 실침대 밀도 합성 침대에서 `cjunc_registry` 전체 (새 판) 의 시간 · 최대 RSS · 단계별
누적 시간 (cProfile) 을 잰다.  옛 판은 이 단계에 닿은 적이 없다 (후보 검색에서 멈췄다) — 고친 뒤 다른 단계가 터지지 않는지 보는 탐침.

침대 (가정 · 실측 아님): VGCF 점 밀도 = 실침대 SBE (1,643,483 점 / 50.0 × 50.0 × 72.5 µm³ ≈ 9.06 /µm³) · 점 간격 0.1 µm (가정) ·
섬유 40 점 · PTFE 점 밀도 = 실침대 (235,046 점 ≈ 1.30 /µm³) · 섬유 53 점 · 상자 BOX µm 정육면체 · vox 0.15 · r_f 0.075 · tol_ff 0.05.

  python3 docs/reviews/rint2_s0_mem_fix_20261106/tools/registry_scale_probe.py <BOX_um> <out.json>
"""
import cProfile
import io
import json
import os
import pstats
import resource
import sys
import time

import numpy as np

W = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, W + '/scripts')
import carbon_junction as CJ  # noqa: E402
import step3_sigma as S3      # noqa: E402

BOX = float(sys.argv[1])
OUT = sys.argv[2]
VOX = 0.15
RHO_V, RHO_P = 1643483 / (50.0082 * 50.0082 * 72.534), 235046 / (50.0082 * 50.0082 * 72.534)


def walk(rng, nf, npts, step, persist):
    polys = []
    for _ in range(nf):
        p = rng.uniform(0.3, BOX - 0.3, 3)
        d = rng.normal(size=3)
        d /= np.linalg.norm(d)
        pts = [p.copy()]
        for _ in range(npts - 1):
            d = d + persist * rng.normal(size=3)
            d /= np.linalg.norm(d)
            p = p + step * d
            pts.append(p.copy())
        polys.append(np.clip(np.asarray(pts), 0.05, BOX - 0.05))
    return polys


rng = np.random.default_rng(7)
V = BOX ** 3
nfv = int(round(RHO_V * V / 40))
nfp = int(round(RHO_P * V / 53))
vg = walk(rng, nfv, 40, 0.1, 0.1)
for _ in range(4):                                         # 긴 두 점 섬유 (8 µm 또는 상자 안)
    p = rng.uniform(0.3, BOX - 0.3, 3)
    d = rng.normal(size=3)
    d /= np.linalg.norm(d)
    vg.append(np.clip(np.asarray([p, p + min(8.0, 0.6 * BOX) * d]), 0.05, BOX - 0.05))
pt = walk(rng, nfp, 53, 0.1, 0.2)
P, PH, F, K = [], [], [], []
for x, q in enumerate(vg):
    P.append(q); PH.append(np.full(len(q), 2)); F.append(np.full(len(q), 10 + x)); K.append(np.ones(len(q), int))
for x, q in enumerate(pt):
    P.append(q); PH.append(np.full(len(q), 4)); F.append(np.full(len(q), 10 ** 6 + x)); K.append(np.ones(len(q), int))
P = np.vstack(P); PH = np.concatenate(PH).astype(np.int64); F = np.concatenate(F).astype(np.int64); K = np.concatenate(K).astype(np.int64)
m = PH != 4
t0 = time.time()
sid, _ = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P[m], PH[m], (0.0, 0.0, 0.0), (BOX, BOX, BOX), VOX,
                      add_fid=F[m], add_kind=K[m])
t_r = time.time() - t0
rss0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
pr = cProfile.Profile()
t0 = time.time()
pr.enable()
reg = CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), VOX, P, PH, F, K, r_f_um=0.075, tol_ff_um=0.05, L_par_um=0.3, r_port_um=0.3,
                        s_min_um=None, gap_tol=2.0, tol_P_um=0.05, tol_sj_um=0.05, r_ptfe_um=0.124, r_sdcp_um=0.15)
pr.disable()
el = time.time() - t0
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats('cumulative').print_stats(28)
top = [ln for ln in s.getvalue().splitlines() if 'carbon_junction.py' in ln][:22]
I = reg['instances']
rec = {'box_um': BOX, 'grid': list(sid.shape), 'n_vgcf_points': int(m.sum()), 'n_ptfe_points': int((~m).sum()),
       'n_segments': int(len(reg['segments']['P0'])), 'n_instances': int(len(I['fi'])), 'n_self': int(np.sum(I['self'])),
       'n_subedges': int(len(reg['subedges']['inst'])), 'n_faces': int(len(reg['faces']['lin'])),
       'raster_s': round(t_r, 2), 'registry_s': round(el, 2), 'maxrss_before_kb': int(rss0),
       'maxrss_after_kb': int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
       'pair_search': {k: dict(v) for k, v in CJ._PAIR_SEARCH_LAST.items()}, 'profile_top_carbon_junction': top}
with open(OUT, 'w', encoding='utf-8') as fh:
    json.dump(rec, fh, ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in rec.items() if k != 'profile_top_carbon_junction'}, ensure_ascii=False))
print('\n'.join(top))
