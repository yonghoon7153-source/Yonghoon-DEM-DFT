"""Drive the scratch prototype on Codex cases, probe beds and timing grids."""
import sys
import time

import numpy as np

sys.dont_write_bytecode = True
SCR = sys.argv[1]
sys.path.insert(0, SCR)
sys.path.insert(0, '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaB')
import step3_conv_cert as CC  # noqa: E402
import step3_sigma as S3  # noqa: E402
import tc_proto as TP  # noqa: E402
from repro_codex import chain  # noqa: E402

S3.GPU_SOLVE = False
S3.AMG_SOLVE = False
TAU = 1e-4


def judge(br, G):
    lo, hi = br['lo'], br['hi']
    eb = max(hi - G, G - lo) / G
    w = (hi - lo) / G
    return eb, w, (lo <= G <= hi)


print('== Codex chains')
S3.CG_MAXITER = 1000
for which in ('main', 'connected', 'iter23'):
    L, b, n, k, G, true = chain(which)
    phi, info = S3._solve_cg(L, b, rtol=1e-12)
    Ab, gb, At, gt = np.array([0, n]), np.array([k[0], G]), np.array([n - 1]), np.array([k[-1]])
    Ib, It = CC.plate_currents(phi, Ab, gb, At, gt)
    for tree in (True, False):
        br = TP.bracket(L, b, phi, Ab, gb, At, gt, tree=tree)
        eb, w, inb = judge(br, Ib)
        print(f'  {which:9s} tree={tree!s:5s} lo {br["lo"]:.16e} hi {br["hi"]:.16e} true {true:.16e} contains {br["lo"] <= true <= br["hi"]} '
              f'G {Ib:.6e} errbound {eb:.3e} width {w:.3e} inbracket {inb} kcl_raw {br["kcl_raw"]:.2e} D {br["Dp"]+br["Dm"]:.2e}')
    br = TP.bracket(L, b, phi, Ab, gb, At, gt, tree=False, defect_term=False)
    print(f'     naive-no-defect lo {br["lo"]:.16e} (> true? {br["lo"] > true})')

print('== warm candidate')
from scipy.sparse import csr_matrix  # noqa: E402
Gs = 1e15
L = csr_matrix([[2., -1., 0.], [-1., 2., 0.], [0., 0., Gs]])
b = np.array([1., 0., Gs]); p = np.array([.75, .25, 1.])
br = TP.bracket(L, b, p, np.array([0, 2]), np.array([1., Gs]), np.array([1]), np.array([1.]))
print('  ', br['lo'], br['hi'], 1 / 3, br['lo'] - 1 / 3)

print('== crafted naive-invalid')
L = csr_matrix([[2.]]); b = np.array([1.]); p = np.array([0.])
for tree, dt in ((True, True), (False, True), (False, False)):
    br = TP.bracket(L, b, p, np.array([0]), np.array([1.]), np.array([0]), np.array([1.]), tree=tree, defect_term=dt)
    print('  tree', tree, 'defect', dt, 'lo', br['lo'], 'hi', br['hi'], '(G* 0.5)')

print('== probe beds (seed 0)')
old_mi = S3.CG_MAXITER
S3.CG_MAXITER = 400000
for seed in (0,):
    sid = CC.probe_bed(seed)
    base = CC.probe_system(sid, CC.probe_sigma_table(), s3=S3)
    for variant, sysd in (('plain', base), ('junction', CC.junction_variant(base, sid))):
        L, b = sysd['L'], sysd['b']
        Ib0, _ = CC.plate_currents(sysd['phi_direct'], sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
        for rt in (1e-8, 1e-10, 1e-12, 1e-14):
            t0 = time.time()
            phi, info = S3._solve_cg(L, b, rtol=rt)
            t1 = time.time()
            Ib, It = CC.plate_currents(phi, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
            br = TP.bracket(L, b, phi, sysd['Ab'], sysd['gb'], sysd['At'], sysd['gt'])
            t2 = time.time()
            eb, w, inb = judge(br, Ib)
            err = abs(Ib - Ib0) / abs(Ib0)
            print(f'  {variant:8s} rt {rt:.0e} info {info} err_vs_direct {err:.3e} errbound {eb:.3e} width {w:.3e} inbracket {inb} '
                  f'pass {eb <= TAU and w <= TAU} direct_in {br["lo"] <= Ib0 <= br["hi"]} levels {br["levels"]} cg {t1-t0:.2f}s tc {t2-t1:.2f}s n {L.shape[0]}')
S3.CG_MAXITER = old_mi
