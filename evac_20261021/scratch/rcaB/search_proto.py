"""Bounded random search (Codex generator) for prototype soundness + timing grid."""
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaB')
from scipy.sparse import csr_matrix  # noqa: E402
import step3_sigma as S3  # noqa: E402
import step3_conv_cert as CC  # noqa: E402
import tc_proto as TP  # noqa: E402

S3.GPU_SOLVE = False
S3.AMG_SOLVE = False
S3.CG_MAXITER = 300
N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
for variant in ('deadend', 'connected'):
    rng = np.random.default_rng(611)
    t0 = time.time()
    n_bad = n_false_d = n_not_contain = n_pass_d = n_abc_false = 0
    worst_bad = 0.0
    for s in range(N):
        n = int(rng.integers(6, 26))
        k = 10. ** rng.uniform(-5, 5, n + 1)
        G = 10. ** rng.uniform(6, 17)
        A = np.zeros((n + 1, n + 1)); b = np.zeros(n + 1); b[0] = k[0]; b[-1] = G
        A[0, 0] += k[0]; A[n - 1, n - 1] += k[-1]; A[-1, -1] = G
        for j in range(n - 1):
            A[j, j] += k[j + 1]; A[j + 1, j + 1] += k[j + 1]
            A[j, j + 1] -= k[j + 1]; A[j + 1, j] -= k[j + 1]
        eps = float(k.min() * 10. ** rng.uniform(-3, 2)) if variant == 'connected' else 0.0
        if eps:
            A[-1, -1] += eps; A[0, 0] += eps; A[-1, 0] -= eps; A[0, -1] -= eps
        L = csr_matrix(A)
        phi, info = S3._solve_cg(L, b, rtol=1e-12)
        Ab, gb, At, gt = np.array([0, n]), np.array([k[0], G]), np.array([n - 1]), np.array([k[-1]])
        Ib, It = CC.plate_currents(phi, Ab, gb, At, gt)
        keff = k.copy(); keff[0] += G * eps / (G + eps)
        true = 1 / np.sum(1 / keff)
        err = abs(Ib - true) / true
        br = TP.bracket(L, b, phi, Ab, gb, At, gt)
        if br.get('problem') or br.get('topology') != 'through':
            print('PROBLEM', s, br)
            continue
        lo, hi = br['lo'], br['hi']
        if not (lo <= true <= hi):
            n_not_contain += 1
            print('NOT CONTAIN', variant, s, lo, true, hi)
        eb = max(hi - Ib, Ib - lo) / Ib if Ib > 0 else np.inf
        w = (hi - lo) / Ib if Ib > 0 else np.inf
        pd = (eb <= 1e-4 and w <= 1e-4)
        n_pass_d += pd
        if info == 0 and err > 1e-4:
            n_bad += 1
            worst_bad = max(worst_bad, err)
            if pd:
                n_false_d += 1
        imb = abs(Ib - It) / abs(Ib) if Ib else np.inf
        if info == 0 and imb <= 1e-4 and err > 1e-4:
            n_abc_false += 1          # A + B pass with error > 1e-4 (C not run here)
    print(f'{variant}: N {N} {time.time()-t0:.1f}s  info0&err>1e-4 {n_bad} (worst {worst_bad:.2e})  A+B pass&err>1e-4 {n_abc_false}  '
          f'd pass {n_pass_d}  d false-accept {n_false_d}  bracket miss {n_not_contain}')

# timing grid
for shp in ((64, 64, 64), (96, 96, 128)):
    rng = np.random.default_rng(1)
    sid = np.where(rng.random(shp) < 0.7, 1, 3).astype(np.int8)
    tab = S3.electronic_sigma_table(0.01, 0.005, 100.0, 10.0, 250.0)
    cap = {}
    old = S3._solve_cg

    def _rec(L, b, *a, **kw):
        cap['L'] = L; cap['b'] = b
        x, i = old(L, b, rtol=1e-10)
        cap['phi'] = x
        return x, i
    S3._solve_cg = _rec
    try:
        t0 = time.time()
        res = S3.solve_sigma_z(sid, tab, 0.15, z_top_um=shp[2] * 0.15, z_bot_um=0.0)
        t1 = time.time()
    finally:
        S3._solve_cg = old
    (cb, gbb, _), (ct, gtt, _) = res['plate_edges']['bot'], res['plate_edges']['top']
    # plate edge indices in dof space
    cond = tab[sid] > 0
    idx = -np.ones(sid.shape, np.int64); idx[cond] = np.arange(int(cond.sum()))
    Abb = idx[cb[0], cb[1], cb[2]]; Att = idx[ct[0], ct[1], ct[2]]
    t2 = time.time()
    br = TP.bracket(cap['L'], cap['b'], cap['phi'], Abb, gbb, Att, gtt)
    t3 = time.time()
    Ib, It = CC.plate_currents(cap['phi'], Abb, gbb, Att, gtt)
    print(f'grid {shp} n {cap["L"].shape[0]} nnz {cap["L"].nnz} solve {t1-t0:.1f}s bracket {t3-t2:.2f}s levels {br["levels"]} '
          f'width {(br["hi"]-br["lo"])/Ib:.2e} errbound {max(br["hi"]-Ib, Ib-br["lo"])/Ib:.2e}')
