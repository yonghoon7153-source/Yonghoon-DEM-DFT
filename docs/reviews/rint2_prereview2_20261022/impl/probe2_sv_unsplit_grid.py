# -*- coding: utf-8 -*-
"""탐침 2-A‴ — payload 끝-끝 결과 (두 섬유 꼴 = ∞ · 대조 = 다리 0 · 비 1.0) 를 풀기: payload 와 같은 좌표 (µm) · SE 점 · SDCP 점 스탬프로
`rasterize` 를 직접 불러 A (x 24) · B (x 26) 기둥의 z 10–14 셀 sid 와 SDCP 셀 위치 · 원장 census 를 본다."""
import contextlib
import io
import json
import os
import sys
import numpy as np
REPO = os.environ.get('PRE_REPO')
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import step3_sigma as S3        # noqa: E402
import carbon_junction as CJ    # noqa: E402


def line(a, b, n):
    a = np.asarray(a, np.float64); b = np.asarray(b, np.float64)
    return a[None] + np.linspace(0.0, 1.0, n)[:, None] * (b - a)[None]


def build(b_start_z, with_se=True, bridge=None):
    A = line((24.5, 24.5, 0.3), (24.5, 24.5, 18.5), 73)
    B = line((26.5, 24.5, b_start_z), (26.5, 24.5, 23.2), 69)
    SD = np.array([[24.5, 24.5, 12.5], [25.5, 24.5, 12.5], [26.5, 24.5, 12.5]])
    P = np.vstack([A, B, SD]); PH = np.r_[np.full(len(A), 2), np.full(len(B), 2), np.full(3, 5)].astype(np.int64)
    F = np.r_[np.full(len(A), 0), np.full(len(B), 1), np.full(3, -1)].astype(np.int64)
    K = np.r_[np.ones(len(A)), np.ones(len(B)), np.zeros(3)].astype(np.int64)
    g = np.arange(12.0, 36.01, 0.75); gz = np.arange(0.3, 23.2, 0.75)
    se = np.array([[x, y, z] for x in g for y in g for z in gz], np.float64) if with_se else None
    am = (np.array([[14.0 * 54.34782608695652 / 54.34782608695652, 14.0, 12.0]]) * 0 + np.array([[1e3, 1e3, 1e3]]), np.array([0.3]),
          np.array([2]))
    kw = {} if bridge is None else {'bridge_um': bridge}
    sid, _ = S3.rasterize(np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64), P, PH, (0.0, 0.0, 0.0), (48.0, 48.0, 23.5), 1.0,
                          se_pts=se, add_fid=F, add_kind=K, **kw)
    col = {f'A z{z}': int(sid[24, 24, z]) for z in range(10, 15)}
    col.update({f'mid z{z}': int(sid[25, 24, z]) for z in range(11, 14)})
    col.update({f'B z{z}': int(sid[26, 24, z]) for z in range(10, 15)})
    with contextlib.redirect_stdout(io.StringIO()):
        reg = CJ.cjunc_registry(sid, (0.0, 0.0, 0.0), 1.0, P, PH, F, K, r_f_um=0.075, tol_ff_um=0.5, L_par_um=0.3, r_port_um=0.3,
                                s_min_um=0.5)
    c = reg['census']
    return {'cells': col, 'n_sdcp_cells': int((sid == 5).sum()),
            'census': {k: c.get(k) for k in ('n_sdcp_components_touching', 'n_bridging_components', 'n_unsplit_bridging_components',
                                             'n_sv_faces_cut_rows', 'n_pieces')}}


out = {}
for tag, bz, se, br in (('two_fibres · SE · bridge 기본', 6.5, True, None), ('control · SE · bridge 기본', 12.5, True, None),
                        ('two_fibres · SE 없음', 6.5, False, None), ('two_fibres · SE · bridge 0', 6.5, True, 0.0)):
    try:
        out[tag] = build(bz, se, br)
    except Exception as e:      # noqa: BLE001
        out[tag] = {'error': f'{type(e).__name__}: {e}'}
    print(tag, json.dumps(out[tag], ensure_ascii=False))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_sv_unsplit_grid.json'), 'w'), ensure_ascii=False, indent=1)
