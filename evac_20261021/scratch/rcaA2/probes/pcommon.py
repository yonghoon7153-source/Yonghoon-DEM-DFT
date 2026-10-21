# -*- coding: utf-8 -*-
"""사전 리뷰 (impl) 공용 도우미 — 리포 함수를 그대로 부르고, 기대값은 손 회로 (독립 구현) 로 만든다.
REPO = 검토 작업 트리 (a76f59d0d).  python -I 로 돌리므로 sys.path 를 직접 넣는다."""
import contextlib
import io
import json
import math
import os
import sys

REPO = os.environ.get('PRE_REPO', '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a55035d4ca989cec4')
sys.path.insert(0, os.path.join(REPO, 'scripts'))

import numpy as np                     # noqa: E402
import step3_sigma as S3               # noqa: E402
import carbon_junction as CJ           # noqa: E402

H = 1.0
RF = 0.5
TOL = 0.1
LPAR = 2.0 * (RF + RF)
RPORT = 2.0
SV = 100.0
G_AX = SV * H
G_PL = SV * H * H / (0.5 * H)
NO_AM = (np.zeros((0, 3)), np.zeros(0), np.zeros(0, np.int64))


def quiet(fn, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*a, **k)


@contextlib.contextmanager
def direct_solver():
    from scipy.sparse.linalg import spsolve
    old = S3._solve_cg

    def _direct(L, b, *a, **k):
        return spsolve(L.tocsc(), b), 0
    S3._solve_cg = _direct
    try:
        yield
    finally:
        S3._solve_cg = old


def sig_e(s_vgcf=SV, s_am=0.010, s_sdcp=250.0):
    return S3.electronic_sigma_table(s_am, s_am * 0.5, s_vgcf, 10.0, s_sdcp)


def densify(verts, step=0.25):
    V = np.asarray(verts, np.float64)
    out = [V[0]]
    for a, b in zip(V[:-1], V[1:]):
        n = max(1, int(math.ceil(np.linalg.norm(b - a) / step - 1e-12)))
        for i in range(1, n + 1):
            out.append(a + (b - a) * (i / n))
    return np.asarray(out)


def rows_pts(point_lists, phase=2, kind=1, fids=None, fid0=10):
    """이미 만든 점열 목록 → (P, PH, F, K)."""
    P, PH, F, K = [], [], [], []
    for i, pts in enumerate(point_lists):
        pts = np.asarray(pts, np.float64).reshape(-1, 3)
        f = fids[i] if fids is not None else fid0 + 10 * i
        P.append(pts); PH.append(np.full(len(pts), phase)); F.append(np.full(len(pts), f)); K.append(np.full(len(pts), kind))
    return (np.vstack(P), np.concatenate(PH).astype(np.int64), np.concatenate(F).astype(np.int64),
            np.concatenate(K).astype(np.int64))


def rows(polys, phase=2, kind=1, fids=None, fid0=10, step=0.25):
    return rows_pts([densify(v, step) if len(v) > 1 else np.asarray(v, np.float64) for v in polys], phase, kind, fids, fid0)


def cat_rows(*rs):
    return tuple(np.concatenate([r[i] for r in rs]) for i in range(4))


def bed(addr, n, am=NO_AM, stamp=None, vox=H, lo=(0.0, 0.0, 0.0), **kw):
    P, PH, F, K = addr
    m = np.ones(len(P), bool) if stamp is None else stamp
    lo = tuple(float(x) for x in lo)
    hi = tuple(lo[i] + float(n[i]) * vox for i in range(3))
    sid, pid = S3.rasterize(am[0], am[1], am[2], P[m], PH[m], lo, hi, vox, add_fid=F[m], add_kind=K[m], **kw)
    return sid, pid


def registry(sid, addr, vox=H, lo=(0.0, 0.0, 0.0), **kw):
    P, PH, F, K = addr
    k = dict(r_f_um=RF, tol_ff_um=TOL, L_par_um=LPAR, r_port_um=RPORT, gap_tol=2.0, s_min_um=3.0)
    k.update(kw)
    return quiet(CJ.cjunc_registry, sid, tuple(float(x) for x in lo), vox, P, PH, F, K, **k)


def plan(reg, rj, **kw):
    k = dict(unreg_law='cut', ptfe_stamp='off')
    k.update(kw)
    return CJ.cjunc_plan(reg, rj, **k)


def solve(sid, sig, n, cj=None, vox=H, **kw):
    with direct_solver():
        return quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(n[2]) * vox, z_bot_um=0.0, cjunc=cj, **kw)


def I_of(res, n, vox=H):
    if 'plate_z_um' not in res:
        return float(res.get('sigma_eff', 0.0))
    zb, zt = res['plate_z_um']
    return res['sigma_eff'] * (n[0] * n[1] * vox * vox) / (zt - zb)


def chain_I(gs):
    return 1.0 / sum(1.0 / g for g in gs)


def ref_I(nn, edges, bot, top):
    used = sorted({i for i, _, _ in edges} | {j for _, j, _ in edges} | {i for i, _ in bot} | {i for i, _ in top})
    if len(used) < nn:
        m = {v: k for k, v in enumerate(used)}
        return ref_I(len(used), [(m[i], m[j], g) for i, j, g in edges], [(m[i], g) for i, g in bot],
                     [(m[i], g) for i, g in top])
    L = np.zeros((nn, nn)); b = np.zeros(nn)
    for i, j, g in edges:
        L[i, i] += g; L[j, j] += g; L[i, j] -= g; L[j, i] -= g
    for i, g in bot:
        L[i, i] += g; b[i] += g
    for i, g in top:
        L[i, i] += g
    phi = np.linalg.solve(L, b)
    return float(sum(g * (1.0 - phi[i]) for i, g in bot))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def seq_cells_pts(pts, vox=H):
    from fibre_segment_raster import segment_cells
    pts = np.asarray(pts, np.float64)
    cs = np.vstack([segment_cells(pts[i], pts[i + 1], vox) for i in range(len(pts) - 1)])
    keep = np.ones(len(cs), bool)
    keep[1:] = np.any(cs[1:] != cs[:-1], axis=1)
    return [tuple(int(v) for v in c) for c in cs[keep]]


def jdump(path, obj):
    def conv(x):
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating,)):
            return float(x)
        if isinstance(x, np.ndarray):
            return x.tolist()
        if isinstance(x, (set, tuple)):
            return list(x)
        return str(x)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1, default=conv)
