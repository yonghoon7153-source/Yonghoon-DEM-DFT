# -*- coding: utf-8 -*-
"""탐침 B4 (RCA-07 생존성) — 대비 1.9e6 (σ_VGCF 7853.98 ↔ σ_AM 0.0041) 무작위 관통 침대에서 생산 CG (rtol 1e-12) + 증서 ⓐ–ⓓ.
정상 수렴 해를 ⓓ 가 거부하지 않는가 (거짓 음성 · 게시 불가가 되면 캠페인이 멈춘다) · 직접해 G* 대비 게시 오차."""
import contextlib
import io
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

S3.CONV_CERT = True
S3.CG_RTOL = 1e-12
out = {}


def bed_r(seed):
    rng = np.random.default_rng(seed)
    vox = 0.25; n = (24, 24, 32); box = np.array(n, float) * vox
    na = 90
    am_c = rng.uniform([0.5] * 3, box - 0.5, (na, 3)); am_r = rng.uniform(0.9, 1.4, na); am_t = rng.integers(1, 3, na)
    P, PH, F, K = [], [], [], []
    for i in range(12):
        p0 = rng.uniform(0.2, box - 0.2); d = rng.normal(size=3); d /= np.linalg.norm(d)
        p1 = np.clip(p0 + d * rng.uniform(2.0, 5.0), 0.05, box - 0.05)
        m = max(2, int(np.ceil(np.linalg.norm(p1 - p0) / 0.1)) + 1)
        pts = p0 + (p1 - p0) * np.linspace(0, 1, m)[:, None]
        P.append(pts); PH.append(np.full(m, 2)); F.append(np.full(m, 100 + i)); K.append(np.ones(m, int))
    P = np.vstack(P); PH = np.concatenate(PH); F = np.concatenate(F); K = np.concatenate(K)
    sid, pid = S3.rasterize(am_c, am_r, am_t, P, PH, (0., 0., 0.), tuple(box), vox, add_fid=F, add_kind=K, bridge_um=0.3)
    return sid, vox, box


for seed in (11, 12):
    sid, vox, box = bed_r(seed)
    sig = S3.electronic_sigma_table(0.0041, 0.0041, 7853.98, 10.0, 256.6)
    with contextlib.redirect_stdout(io.StringIO()):
        r = S3.solve_sigma_z(sid, sig, vox, z_top_um=float(box[2]), z_bot_um=0.0)
    with direct_solver():
        rd = quiet(S3.solve_sigma_z, sid, sig, vox, z_top_um=float(box[2]), z_bot_um=0.0)
    c = r.get('conv_cert') or {}
    out[str(seed)] = {'n_dof': r.get('n_dof'), 'sigma': r['sigma_eff'], 'sigma_direct': rd['sigma_eff'],
                      'rel_err_vs_direct': r['sigma_eff'] / rd['sigma_eff'] - 1.0 if rd['sigma_eff'] else None,
                      'status': c.get('status'), 'ok': c.get('ok'),
                      'pass': [c.get('pass_a'), c.get('pass_b'), c.get('pass_c'), c.get('pass_d')],
                      'err_bound_rel': c.get('target_err_bound_rel'), 'width_rel': c.get('target_width_rel'),
                      'why': c.get('target_why'), 'iters': c.get('iters')}
    print(seed, out[str(seed)])
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe_cert_liveness.json'), out)
