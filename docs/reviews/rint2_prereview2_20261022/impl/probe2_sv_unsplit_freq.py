# -*- coding: utf-8 -*-
"""탐침 2-A′ (PRE2-impl-01 빈도 어림 · 합성 · 실침대 아님) — 생산 단위 (vox 0.15 · VGCF Ø0.15 중심선 · 점 간격 0.05) 침대에
SDCP 덩어리 (Ø1.0 µm 구 스탬프 = DBE 'SDCP 평균 1 µm' 의 덩어리 크기 흉내) 를 뿌려 원장 census 의
n_bridging_components (다리 = 둘 이상 무리) 중 n_unsplit_bridging_components (지나는 무리 둘 이상 = 반사실이 안 끊는 다리) 몫을 센다.
⚠ 어림 — VGCF 3 vol% · SDCP 2–5 vol% 는 가정 (실침대 조성 · 덩어리 꼴 · 섬유 굽힘 미반영)."""
import contextlib
import io
import json
import os
import sys
import numpy as np
REPO = os.environ.get('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d')
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import step3_sigma as S3        # noqa: E402
import carbon_junction as CJ    # noqa: E402

VOX = 0.15
NBOX = 24
BOX = NBOX * VOX


def fibre(rng):
    p = rng.uniform(0.0, BOX, 3)
    d = rng.normal(size=3); d /= np.linalg.norm(d)
    L = rng.uniform(2.0, 3.5)
    pts = []
    n = int(L / 0.05) + 1
    for t in np.linspace(0.0, L, n):
        d = d + rng.normal(scale=0.02, size=3); d /= np.linalg.norm(d)   # 약한 굽힘
        p = p + d * (L / (n - 1)) if t > 0 else p
        pts.append(p.copy())
    pts = np.asarray(pts)
    keep = np.all((pts > 0.01) & (pts < BOX - 0.01), axis=1)
    # 상자 안 가장 긴 연속 구간
    best, cur, bi = (0, 0), 0, 0
    for i, k in enumerate(keep):
        if k:
            cur += 1
            if cur > best[1] - best[0]:
                best = (i - cur + 1, i + 1)
        else:
            cur = 0
    seg = pts[best[0]:best[1]]
    return seg if len(seg) >= 4 else None


def bed(seed, n_fib, n_sdcp):
    rng = np.random.default_rng(seed)
    P, PH, F, K = [], [], [], []
    f = 100
    while f < 100 + n_fib:
        s = fibre(rng)
        if s is None:
            continue
        P.append(s); PH.append(np.full(len(s), 2)); F.append(np.full(len(s), f)); K.append(np.ones(len(s), int))
        f += 1
    sd = rng.uniform(0.5, BOX - 0.5, (n_sdcp, 3))
    P.append(sd); PH.append(np.full(n_sdcp, 5)); F.append(np.arange(n_sdcp) + 900); K.append(np.zeros(n_sdcp, int))
    P = np.vstack(P); PH = np.concatenate(PH).astype(np.int64); F = np.concatenate(F).astype(np.int64)
    K = np.concatenate(K).astype(np.int64)
    am = (np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64))
    sid, _pid = S3.rasterize(am[0], am[1], am[2], P, PH, (0.0, 0.0, 0.0), (BOX, BOX, BOX), VOX, sdcp_sphere_d_um=1.0,
                             add_fid=F, add_kind=K, bridge_um=0.48)
    with contextlib.redirect_stdout(io.StringIO()):
        reg = CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), VOX, P, PH, F, K, r_f_um=0.075, tol_ff_um=0.03, L_par_um=0.30,
                                r_port_um=0.30, s_min_um=0.3, tol_sj_um=0.03, r_sdcp_um=0.15)
    c = reg['census']
    vg = float(np.mean(sid == 3)); sdv = float(np.mean(sid == 5))
    return {'vgcf_cell_frac': vg, 'sdcp_cell_frac': sdv, 'n_sdcp_components_touching': c.get('n_sdcp_components_touching'),
            'n_bridging_components': c.get('n_bridging_components'), 'n_unsplit_bridging_components': c.get('n_unsplit_bridging_components'),
            'n_sv_faces_cut_rows': c.get('n_sv_faces_cut_rows'), 'n_sdcp_bridging_components (fid 기준)': c.get('n_sdcp_bridging_components')}


out = {}
tot_b = tot_u = 0
for n_fib, n_sdcp in ((30, 3), (30, 6)):
    for seed in range(4):
        r = bed(seed, n_fib, n_sdcp)
        out[f'fib{n_fib}_sdcp{n_sdcp}_s{seed}'] = r
        tot_b += r['n_bridging_components'] or 0
        tot_u += r['n_unsplit_bridging_components'] or 0
        print(n_fib, n_sdcp, seed, r)
out['total'] = {'bridging': tot_b, 'unsplit': tot_u, 'unsplit_share': (tot_u / tot_b if tot_b else None)}
print('total', out['total'])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_sv_unsplit_freq.json'), 'w'), ensure_ascii=False, indent=1)
