#!/usr/bin/env python3
"""STEP4 near-null 선형계 진단 + 전처리 후보 실측 비교.

실패 덤프(MPM_S4_DUMP_FAIL=1이 저장한 step4_cg_fail_L.npz + step4_cg_fail.npz)에서
실제 4.4M dof 행렬을 로드 → near-null-space를 LOBPCG로 특성화 → 여러 전처리로 CG
수렴을 실측 → ★수렴하는 전처리를 찾아 step4_dyn.py에 심는다.

배경: 후막+저율(0.2C)에서 전자망↔이온망 BV 결합이 약해 near-null 모드가 생김 →
unscaled-AMG는 발산, Jacobi는 ~1e-12서 정체(목표 ~1e-14 미달) → Newton 정체 →
galvanostatic 전류 못 pin(29% miss) → 하드페일.  근본해결 = near-null 잡는 전처리.

사용법 (GPU 박스, run 디렉토리에서):
  python3 <repo>/scripts/diag_step4_nearnull.py            # 현재 폴더 덤프 자동
  python3 scripts/diag_step4_nearnull.py L.npz bxr.npz     # 경로 지정
소요: ~30-50분 (AMG 빌드 ~1분×후보 + LOBPCG).  pyamg 필요.
"""
import sys
import time

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import LinearOperator, cg, lobpcg


def main():
    Lpath = sys.argv[1] if len(sys.argv) > 1 else 'step4_cg_fail_L.npz'
    bpath = sys.argv[2] if len(sys.argv) > 2 else 'step4_cg_fail.npz'
    L = sp.load_npz(Lpath).tocsr().astype(np.float64)
    dd = np.load(bpath)
    b = dd['b'].astype(np.float64)
    N = L.shape[0]
    d = L.diagonal()
    bn = float(np.linalg.norm(b))
    r_start = float(dd['r_start']) if 'r_start' in dd else bn
    r_x = float(dd['r_x']) if 'r_x' in dd else float('nan')
    print(f"=== 덤프 로드: N={N:,}  nnz={L.nnz:,}  ||b||={bn:.3e} ===")
    print(f"    덤프 기록: r_start={r_start:.2e}  r_x(실패해)={r_x:.2e}  "
          f"({'발산 확인(r_x≫r_start)' if r_x > 10 * r_start else '?'})")
    print(f"    대각 {d.min():.3e}..{d.max():.3e}  min>0={bool(d.min() > 0)}  "
          f"동적범위={d.max() / max(abs(d.min()), 1e-300):.2e}")

    Minv = sp.diags(1.0 / np.where(d > 0, d, 1.0))
    tgt = 1e-13          # 이보다 내려가면 '수렴'(Jacobi 정체 ~1e-12보다 10× 좋음 = Newton 진행 가능)

    # ── near-null 고유벡터 (LOBPCG + Jacobi 전처리) ──
    print(f"\n=== near-null 특성화 (LOBPCG, 최소 6개) ===")
    V = None
    try:
        rng = np.random.default_rng(0)
        X0 = rng.standard_normal((N, 6))
        t0 = time.time()
        ev, V = lobpcg(L, X0, M=Minv, largest=False, tol=1e-4, maxiter=80)
        order = np.argsort(ev)
        ev, V = ev[order], V[:, order]
        print(f"    최소 고유값: {np.array2string(ev, precision=3)}  ({time.time() - t0:.0f}s)")
        evmax = lobpcg(L, rng.standard_normal((N, 1)), M=Minv, largest=True,
                       tol=1e-3, maxiter=40)[0][0]
        print(f"    λmax≈{evmax:.3e}  → κ≈{evmax / max(ev.min(), 1e-300):.2e}  "
              f"(near-null gap λmin={ev.min():.3e})")
    except Exception as e:
        print(f"    LOBPCG 실패({type(e).__name__}: {e}) — near-null 벡터 없이 (4)(5)(7) 생략")

    # ── 전처리 후보 실측 (조기정지: 수렴/정체/발산) ──
    def run(name, M, maxit=700):
        st = {'n': 0, 'best': np.inf, 'bad': 0}

        class _S(Exception):
            pass

        def cb(xk):
            st['n'] += 1
            if st['n'] % 10:
                return
            r = float(np.linalg.norm(b - L @ xk))
            if r <= tgt or r > 100 * bn:
                st['best'] = min(st['best'], r)
                raise _S()
            if r < 0.98 * st['best']:
                st['best'] = r
                st['bad'] = 0
            else:
                st['bad'] += 1
                if st['bad'] >= 4:
                    raise _S()
        t0 = time.time()
        try:
            try:
                cg(L, b, rtol=1e-12, atol=1e-15, maxiter=maxit, M=M, callback=cb)
            except TypeError:
                cg(L, b, tol=1e-12, maxiter=maxit, M=M, callback=cb)
        except _S:
            pass
        except Exception as e:
            print(f"  {name:34s} EXC {type(e).__name__}: {e}")
            return
        r = st['best']
        verdict = '✅수렴' if r <= tgt else ('… 정체' if r <= bn else '❌발산')
        print(f"  {name:34s} best={r:.2e}  its≈{st['n']:4d}  {time.time() - t0:5.0f}s  {verdict}")

    print(f"\n=== 전처리 후보 (목표 best ≤ {tgt:.0e}; Jacobi 정체≈1e-12 기준) ===")
    run("(1) Jacobi (SPD-safe baseline)", Minv)
    try:
        import pyamg
        run("(2) AMG 기본 unscaled (발산 재현)",
            pyamg.smoothed_aggregation_solver(L, max_coarse=500).aspreconditioner('V'))
        s = 1.0 / np.sqrt(np.maximum(np.abs(d), 1e-300))
        Ls = (sp.diags(s) @ L @ sp.diags(s)).tocsr()
        mls = pyamg.smoothed_aggregation_solver(Ls, max_coarse=500).aspreconditioner('V')
        run("(3) sym-scaled AMG",
            LinearOperator(L.shape, matvec=lambda r, _s=s, _m=mls: _s * _m.matvec(_s * r)))
        if V is not None:
            B = np.hstack([np.ones((N, 1)), V])              # 상수 + near-null 모드 = AMG 후보공간
            run("(4) ★AMG B=near-null",
                pyamg.smoothed_aggregation_solver(L, B=B, max_coarse=500).aspreconditioner('V'))
            #   scaled system Ls=S·L·S, y=x/s.  L v≈0 ⇒ Ls(v/s)≈0 → Ls의 near-null = B/s (열별 1/s).
            Bs = B / s[:, None]
            mlbs = pyamg.smoothed_aggregation_solver(Ls, B=Bs, max_coarse=500).aspreconditioner('V')
            run("(5) ★sym-scaled AMG B=near-null",
                LinearOperator(L.shape, matvec=lambda r, _s=s, _m=mlbs: _s * _m.matvec(_s * r)))
        run("(6) AMG Chebyshev smoother",
            pyamg.smoothed_aggregation_solver(
                L, max_coarse=500, presmoother=('chebyshev', {'degree': 3}),
                postsmoother=('chebyshev', {'degree': 3})).aspreconditioner('V'))
    except ImportError:
        print("  pyamg 미설치 → AMG 후보 생략 (python3 -m pip install pyamg)")
    except Exception as e:
        print(f"  AMG 후보 중 예외: {type(e).__name__}: {e}")
    if V is not None:                                        # (7) 2-level 디플레이션(Jacobi + coarse span(V))
        try:
            AV = L @ V
            E = V.T @ AV
            Einv = np.linalg.inv(E)

            def defl(r, _V=V, _Ei=Einv, _M=Minv):
                return _M @ r + _V @ (_Ei @ (_V.T @ r))
            run("(7) deflated Jacobi (span near-null)",
                LinearOperator(L.shape, matvec=defl))
        except Exception as e:
            print(f"  deflated EXC: {type(e).__name__}: {e}")

    print(f"\n=== 판정 ===")
    print(f"  ✅수렴(best≤{tgt:.0e}) 뜬 것 = 승자.  (4)/(5) near-null-AMG 또는 (7) deflation이")
    print(f"  이기면 그걸 step4_dyn._cg에 심는다.  아무것도 안 되면 앵커를 더 촘촘히/다른 후보.")
    print(f"  이 출력을 그대로 붙여주면 어느 전처리를 심을지 확정한다.")


if __name__ == '__main__':
    main()
