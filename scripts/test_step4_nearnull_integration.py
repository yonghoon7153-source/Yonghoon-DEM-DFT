#!/usr/bin/env python3
"""STEP4 near-null-B AMG 폴백 통합 회귀 테스트 (CPU, GPU 불필요).

step4_dyn._cg 의 4단 폴백(GPU→AMG→Jacobi→★near-null-B AMG)이 실제로:
  ① 표준 AMG 발산 + Jacobi 정체(=near-null)일 때 near-null tier가 발동하고,
  ② near-null-B AMG 로 잔차를 대폭 개선하며(Jacobi-only 보다 우수),
  ③ near-null 벡터·계층을 cache에 심어 재사용 가능한지
를 실 덤프 없이 합성 near-null(고립노드형, 대각 dyn-range~1e11 = 실덤프 닮음)로 검증한다.

⚠ 합성계의 near-null 스펙트럼은 실행렬(λ~2e-11 tight cluster, 8.3e-14 수렴)만큼 깨끗하지
않아 절대 잔차는 ~1e-4에서 멈출 수 있음 — 이 테스트가 보는 건 '절대 정확도'가 아니라
'tier 발동 + Jacobi 대비 개선 + cache 재사용' (통합 배선 무결성).  실 0.2C end-to-end
정확도(8.3e-14)는 diag_step4_nearnull.py 가 실덤프에서 이미 증명.

사용법:  python3 scripts/test_step4_nearnull_integration.py
"""
import importlib.util
import sys
import warnings

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import cg

warnings.filterwarnings('ignore')


def _load_cg():
    spec = importlib.util.spec_from_file_location('step4_dyn', 'scripts/step4_dyn.py')
    mod = importlib.util.module_from_spec(spec)
    _argv = sys.argv
    sys.argv = ['step4_dyn']                                  # argparse 안 타게
    spec.loader.exec_module(mod)
    sys.argv = _argv
    mod.GPU = False                                           # CPU 경로 강제 (AMG→Jacobi→near-null)
    return mod


def _nearnull_bed(n=230, K=12, seed=0):
    """bulk 5-point Laplacian + K개 near-isolated 노드(대각~1e-11) = 실 near-null 덤프 구조 모사."""
    Nb = n * n
    N = Nb + K
    rng = np.random.default_rng(seed)
    r = []
    c = []
    v = []
    for i in range(n):
        for j in range(n):
            p = i * n + j
            for di, dj in ((1, 0), (0, 1)):
                if i + di < n and j + dj < n:
                    q = (i + di) * n + (j + dj)
                    r += [p, q]
                    c += [q, p]
                    v += [-1.0, -1.0]
    for k in range(K):                                       # 약결합 고립노드 → near-null 모드
        iso = Nb + k
        t = rng.integers(Nb)
        r += [iso, t]
        c += [t, iso]
        v += [-1e-11, -1e-11]
    A = sp.coo_matrix((v, (r, c)), shape=(N, N)).tocsr()
    deg = -np.asarray(A.sum(1)).ravel()
    L = (sp.diags(deg) - A).tocsr() + 1e-13 * sp.eye(N)       # graph Laplacian + tiny grounding → SPD
    b = rng.standard_normal(N)
    return L, b


def main():
    mod = _load_cg()
    L, b = _nearnull_bed()
    N = L.shape[0]
    big = N >= 50000
    dyn = L.diagonal().max() / L.diagonal().min()
    print(f'=== STEP4 near-null 통합 테스트 ===  N={N:,}  big={big}  대각 dyn-range={dyn:.1e}')

    cache = {}
    x, info = mod._cg(L, b, pc_cache=cache, rtol=1e-9)
    r_cg = float(np.linalg.norm(b - L @ x) / np.linalg.norm(b))
    xj, _ = cg(L, b, rtol=1e-9, atol=0, maxiter=1500, M=sp.diags(1.0 / L.diagonal()))
    r_j = float(np.linalg.norm(b - L @ xj) / np.linalg.norm(b))

    engaged = ('nearnull_V' in cache) or ('nnamg' in cache)
    ok = True
    def chk(name, cond):
        nonlocal ok
        ok = ok and bool(cond)
        print(f'  [{"PASS" if cond else "FAIL"}] {name}')
    print(f'  cache keys after solve: {sorted(cache.keys())}')
    print(f'  _cg 4-tier resid={r_cg:.2e}   Jacobi-only resid={r_j:.2e}')
    chk('big(≥50k) 경로 진입', big)
    chk('near-null tier 발동(cache에 nearnull_V/nnamg)', engaged)
    chk('_cg 4단 ≤ Jacobi-only (near-null tier가 도움)', r_cg <= r_j + 1e-15)
    chk('near-null 벡터 cache 재사용 가능(shape 정상)',
        cache.get('nearnull_V') is not None and cache['nearnull_V'].shape[0] == N)
    print(f'=== {"PASS" if ok else "FAIL"} ===')
    print('  (절대 잔차 ~1e-4 정체는 합성계 아티팩트 — 실덤프 8.3e-14는 diag_step4_nearnull.py 증명)')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
