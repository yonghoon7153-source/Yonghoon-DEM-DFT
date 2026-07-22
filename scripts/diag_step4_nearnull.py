#!/usr/bin/env python3
"""STEP4 near-null 실패-덤프 진단 — ★대각 정규화(Levenberg-Marquardt) 스윕 우선★.

실패 덤프(step4_cg_fail_L.npz + step4_cg_fail.npz)의 실제 4.4M dof 행렬에서:
진단 결과 near-null(λmin~1e-11, 대각 7e-12 = 거의 고립 노드)이 확인됨. 표준 전처리
(Jacobi/AMG)는 ||b|| 근처서 정체 → RHS가 near-null에 갇힘.

처방 = J에 εI 추가(J+εI): 거의 고립 노드를 살짝 접지 → near-null 제거 → 조건수 급감.
★Jacobian에만 ε를 더하므로 Newton 고정점(F=0)은 불변 = 물리 해 안 바뀜(LM 감쇠).
가장 작은(=물리충실) ε로 수렴하는 지점을 찾는다.  선택: 무거운 near-null-B AMG(--full).

사용법 (GPU 박스 or WSL, CPU 전용):
  python3 scripts/diag_step4_nearnull.py <L.npz> <bxr.npz>
  python3 scripts/diag_step4_nearnull.py <L.npz> <bxr.npz> --full   # +near-null-B/deflation(느림)
소요: 정규화 스윕 ~5-15분 (AMG는 잘-조건된 J+εI라 빠름).
"""
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, cg


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    full = '--full' in sys.argv
    Lpath = args[0] if len(args) > 0 else 'step4_cg_fail_L.npz'
    bpath = args[1] if len(args) > 1 else 'step4_cg_fail.npz'
    L = sp.load_npz(Lpath).tocsr().astype(np.float64)
    dd = np.load(bpath)
    b = dd['b'].astype(np.float64)
    N = L.shape[0]
    d = L.diagonal()
    bn = float(np.linalg.norm(b))
    print(f"=== 덤프: N={N:,}  nnz={L.nnz:,}  ||b||={bn:.3e}  "
          f"대각 {d.min():.2e}..{d.max():.2e} (동적범위 {d.max()/max(abs(d.min()),1e-300):.1e}) ===")
    tgt = max(1e-13, 1e-3 * bn)   # ||b|| 대비 1e-3 아래로 내려가면 '수렴'(Newton 진행 가능)
    print(f"    목표 best ≤ {tgt:.2e}  (표준전처리는 ||b||≈{bn:.1e}서 정체 = 실패)")

    I = sp.eye(N, format='csr')

    def run(name, A, M, maxit=800):
        st = {'n': 0, 'best': np.inf, 'bad': 0}

        class _S(Exception):
            pass

        def cb(xk):
            st['n'] += 1
            if st['n'] % 10:
                return
            r = float(np.linalg.norm(b - A @ xk))
            if r <= tgt or r > 100 * bn:
                st['best'] = min(st['best'], r)
                raise _S()
            if r < 0.9 * st['best']:
                st['best'] = r
                st['bad'] = 0
            else:
                st['bad'] += 1
                if st['bad'] >= 4:
                    raise _S()
        t0 = time.time()
        try:
            try:
                cg(A, b, rtol=1e-12, atol=1e-16, maxiter=maxit, M=M, callback=cb)
            except TypeError:
                cg(A, b, tol=1e-12, maxiter=maxit, M=M, callback=cb)
        except _S:
            pass
        except Exception as e:
            print(f"  {name:32s} EXC {type(e).__name__}: {e}")
            return None
        r = st['best']
        v = '✅수렴' if r <= tgt else ('… 정체' if r <= bn else '❌발산')
        print(f"  {name:32s} best={r:.2e}  its≈{st['n']:4d}  {time.time()-t0:5.0f}s  {v}")
        return r

    # ── ★대각 정규화 스윕 (J+εI): Jacobi & AMG ──
    print(f"\n=== ★대각 정규화 J+εI 스윕 (가장 작은 ε로 수렴 = 답) ===")
    try:
        import pyamg
        have_amg = True
    except ImportError:
        have_amg = False
        print("  (pyamg 없음 — Jacobi만)")
    for eps in (1e-6, 1e-7, 1e-8, 1e-9, 1e-10):
        A = (L + eps * I).tocsr()
        dA = A.diagonal()
        run(f"J+{eps:.0e}I · Jacobi", A, sp.diags(1.0 / dA))
        if have_amg:
            try:
                ml = pyamg.smoothed_aggregation_solver(A, max_coarse=500).aspreconditioner('V')
                run(f"J+{eps:.0e}I · AMG", A, ml)
            except Exception as e:
                print(f"  J+{eps:.0e}I · AMG EXC: {type(e).__name__}: {e}")

    # ── 해 안정성: ε를 줄여도 해가 안 바뀌면 물리충실 (near-null 노드는 전류 ~0이라 기대) ──
    print(f"\n=== 해 안정성 (ε=1e-6 vs 1e-8 해 차이 — 작으면 물리 불변 확인) ===")
    try:
        from scipy.sparse.linalg import cg as _cg
        x6 = _cg((L + 1e-6 * I).tocsr(), b, rtol=1e-10, maxiter=800,
                 M=sp.diags(1.0 / (d + 1e-6)))[0]
        x8 = _cg((L + 1e-8 * I).tocsr(), b, rtol=1e-10, maxiter=800,
                 M=sp.diags(1.0 / (d + 1e-8)))[0]
        rel = float(np.linalg.norm(x6 - x8) / max(np.linalg.norm(x8), 1e-300))
        print(f"  ||x(1e-6)-x(1e-8)||/||x(1e-8)|| = {rel:.2e}  "
              f"({'✅ 물리 불변(ε 무해)' if rel < 0.05 else '⚠ ε 민감 — 더 작은 ε 필요'})")
    except Exception as e:
        print(f"  안정성 체크 EXC: {type(e).__name__}: {e}")

    if full:
        print(f"\n=== (--full) near-null-B AMG + deflation (무거움) ===")
        from scipy.sparse.linalg import lobpcg
        Minv = sp.diags(1.0 / np.where(d > 0, d, 1.0))
        rng = np.random.default_rng(0)
        ev, V = lobpcg(L, rng.standard_normal((N, 3)), M=Minv, largest=False, tol=1e-4, maxiter=60)
        print(f"  near-null λ: {np.array2string(np.sort(ev), precision=2)}")
        AV = L @ V
        E = np.linalg.inv(V.T @ AV)
        run("deflated Jacobi (span V, k=3)",
            L, LinearOperator(L.shape, matvec=lambda r, _V=V, _E=E, _M=Minv: _M @ r + _V @ (_E @ (_V.T @ r))))
        try:
            import pyamg
            B = np.hstack([np.ones((N, 1)), V])
            run("AMG B=near-null (k=3)", L,
                pyamg.smoothed_aggregation_solver(L, B=B, max_coarse=800).aspreconditioner('V'))
        except Exception as e:
            print(f"  AMG-B EXC: {type(e).__name__}: {e}")

    print(f"\n=== 판정 ===")
    print(f"  ✅수렴 뜬 가장 작은 ε = 답.  그 ε를 step4_dyn._cg에 J+εI로 심는다(LM 감쇠, 해 불변).")
    print(f"  해 안정성이 '물리 불변'이면 ε는 무해.  이 출력 그대로 붙여줘.")


if __name__ == '__main__':
    main()
