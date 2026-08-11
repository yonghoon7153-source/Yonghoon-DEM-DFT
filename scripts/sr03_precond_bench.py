#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SR-03 근거 측정 — STEP3 Kirchhoff CG: 느린 원인이 **반복수**인가, 그리고 전처리를
바꾸면 **σ_eff 가 변하는가**(해-불변인가).

배선 前 측정이다.  STEP3 의 실제 경로 `solve_sigma_z` 를 그대로 돌리되 `_solve_cg` 만
Jacobi / AMG 로 갈아끼워, 같은 계에서 (반복수 · 시간 · **σ_eff**) 를 비교한다.
σ_eff 는 φ 의 범함수라 ‖Δφ‖ 보다 이것이 판단 대상이다.

대비 (실측 arm A, 전자 채널): 2,713,168 dof · resid 1.0e-08 · CPU 3,485 s.
"""
import sys, time, os
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg

sys.path.insert(0, os.environ.get('DEM_SCRIPTS', '/home/user/Yonghoon-DEM-DFT/scripts'))
import step3_sigma as S3

SIG = np.zeros(9, np.float64)                               # 전자 채널 σ (S/cm)
SIG[1], SIG[2], SIG[3], SIG[6] = 0.010, 0.005, 1000.0, 0.0  # AM_S · AM_P · VGCF · SE(절연)
VOX = 0.4


def make_bed(n, seed=0, am_frac=0.55):
    rng = np.random.default_rng(seed)
    sid = np.full((n, n, n), 6, np.int8)
    zz, yy, xx = np.meshgrid(*[np.arange(n)] * 3, indexing='ij')
    while int((sid != 6).sum()) < am_frac * n ** 3:
        r = rng.uniform(4, 12) * (n / 128)
        c = rng.uniform(0, n, 3)
        sid[((xx - c[0]) ** 2 + (yy - c[1]) ** 2 + (zz - c[2]) ** 2) < r * r] = \
            1 if rng.random() < 0.5 else 2
    for _ in range(n * 4):                                  # VGCF 섬유 (선분)
        p0 = rng.uniform(0, n, 3); d = rng.normal(size=3); d /= np.linalg.norm(d)
        t = np.arange(0, rng.uniform(10, 40) * (n / 128), 0.5)
        p = np.clip((p0[None, :] + t[:, None] * d[None, :]).astype(int), 0, n - 1)
        sid[p[:, 0], p[:, 1], p[:, 2]] = 3
    return sid


def make_solver(kind, rtol, stats):
    """`step3_sigma._solve_cg` 대체물 — 반복수/시간/구축시간을 stats 에 남긴다."""
    def solve(L, b):
        it = [0]
        if kind == 'jacobi':
            M, build = sparse.diags(1.0 / L.diagonal()), 0.0
        else:
            import pyamg
            t0 = time.time()
            M = pyamg.smoothed_aggregation_solver(
                sparse.csr_matrix(L), max_coarse=500).aspreconditioner(cycle='V')
            build = time.time() - t0
        t0 = time.time()
        try:
            x, info = cg(L, b, rtol=rtol, maxiter=30000, M=M, callback=lambda _: it.__setitem__(0, it[0] + 1))
        except TypeError:
            x, info = cg(L, b, tol=rtol, maxiter=30000, M=M, callback=lambda _: it.__setitem__(0, it[0] + 1))
        stats.update(it=it[0], build=build, solve=time.time() - t0, nnz=L.nnz)
        return x, info
    return solve


def main():
    sizes = [int(s) for s in (sys.argv[1:] or ['48', '64', '96'])]
    rtols = [float(x) for x in os.environ.get('RTOLS', '1e-8').split(',')]
    print(f'{"n":>4} {"dof":>10} {"rtol":>7} | {"solver":>7} {"iter":>6} {"build":>7} {"solve":>8} '
          f'{"total":>8} {"resid":>9} {"sigma_eff":>12} | Δσ vs jacobi')
    for n in sizes:
        sid = make_bed(n)
        for rtol in rtols:
            base = None
            for kind in ('jacobi', 'amg'):
                st = {}
                orig = S3._solve_cg
                S3._solve_cg = make_solver(kind, rtol, st)
                try:
                    out = S3.solve_sigma_z(sid, SIG, VOX, z_bot_um=0.0, z_top_um=n * VOX)
                finally:
                    S3._solve_cg = orig
                s = out['sigma_eff']
                if kind == 'jacobi':
                    base = s
                    head = f'{n:>4} {out["n_dof"]:>10,} {rtol:>7.0e} |'
                    d = ''
                else:
                    head = ' ' * 24 + '|'
                    d = f' {abs(s - base) / max(base, 1e-30) * 100:.4f} %'
                print(f'{head}{kind:>8} {st["it"]:>6} {st["build"]:>6.1f}s {st["solve"]:>7.1f}s '
                      f'{st["build"] + st["solve"]:>7.1f}s {out["resid"]:>9.1e} {s:>12.6g} |{d}')
                sys.stdout.flush()


if __name__ == '__main__':
    main()
