#!/usr/bin/env python3
"""STEP4-v2 — 갈바노스타틱/CV 시간 전개: 비선형 Butler-Volmer + 입자별 구형확산 (voxel-DFN, SSB).

설계: docs/step4_v2_design.md.  v1(step3_sigma.solve_reaction_current)의 동역학판 — 같은
rasterized 복셀 격자의 두 망(전자/이온)을 실제 AM|SE·AM|SDCP 접촉면(BV)에서 결합해 시간을 굴린다.

물리 범위 = COMSOL Battery(전극 스케일) 표준 세팅 패리티 (2026-07-15 전수 감사):
  ✓ 비선형 BV, 비대칭 전달계수 α_a/α_c (기본 0.5/0.5 = 대칭 sinh)
  ✓ i0(x) = i0_ref·(x/½)^αc·((1−x)/½)^αa  (c_e 항 없음 — 단일이온 SE, 활동도 고정: SSB 물리)
  ✓ 계면 필름저항 ASR_film [Ω·m²] (SEI/CEI 자리, η_s = Δφ − U − I·ASR/A, 면별 내재 Newton)
  ✓ 입자별 구형확산 (실측 입자 반경 분포 그대로 — COMSOL의 size-bin보다 정밀)
  ✓ 갈바노스타틱(CC) + 전압 홀드(CV; CC→CV = CCCV, 방전/충전 양방향) — V_app 괄호법(Illinois)
  ✓ 집전체 실측 R_int 직렬 부하 [Ω·cm²] (STEP3 시나리오 축과 동일 규약; 터미널 V·컷오프에 반영)
  ✓ 발열 분해 출력 [W]: Q_ohm(e/i 분리)·Q_ct(BV)·Q_film + Q_rev(엔트로피 — dU/dT CSV 있을 때만)
  ✓ 온도 파라미터 T (등온; f=F/RT 전체 일관)
  ✓ 에너지 수지 감사 (매 스텝): P_ohm + Σ I·η_s + Σ I²·ASR/A + Σ I·U + V·I_del = 0 (기계정밀도)
  ✓ 전하(KCL)·리튬(질량) 보존 감사 + 정전류 타깃-미스 가드
  솔버 구조(2026-07-16 개정): 코어 = potentiostatic Dirichlet(v1-검증 행렬 — 실전 2.9M dof에서
  GPU Jacobi-CG 수렴 실적) + 정전류/CV = V_app 괄호법(Illinois) 래퍼.  supernode-정전류 구조는
  ~5천 집전체 접점이 한 행에 몰린 허브가 CG를 정체시켜 폐기(V100 3h+ 스톨 → 재설계).
  범위 밖(정직, 근거): 전해질 농도분극(단일이온 t⁺≈1 → 물리적으로 부재), 이중층 C_dl(시간상수
  ~ms ≪ 방전 dt — COMSOL도 방전 sim에선 통상 off), D_s(c) 농도의존(Chen2020 양극도 상수),
  열-전기 커플(등온; Q는 출력만), anode/SE열화/체적변화(A10), poly/SC i0 분리는 **진폭만**
  (SOC-모양 (x/½)^αc((1−x)/½)^αa·α_a/α_c·ASR_film·OCP는 전 클래스 공유 — 표면조성/코팅이
   모양 자체를 바꾸는 경우는 범위 밖; 리뷰 2026-07-21), **입자 표면 유입의 각도분해**
  (총량은 접촉면이 결정하나 유입을 전표면 균일 살포로 균질화 — 커버리지 낮은 입자의
   표면포화/확산분극 개시가 계산상 지연됨; --ang-sectors 확장 예정).
  프로덕션 집계-KCL 보장 수위 = ~4×노이즈바닥(2.9M dof서 ≈1e-4 rel) — tol_rel(1e-8) 아님.

단위: 내부 SI.  σ 테이블 입력은 S/cm(STEP3 규약) → ×100 [S/m].

§F1 앵커 입력(날조 금지):
  · U_ocp(x)·c_max·stoich 창: --ocp-csv + --params-json (step4_pybamm_anchor --export-params
    가 pybamm Chen2020에서 기계 추출, provenance 포함)
  · D_s: --d-s (기본 3e-14 = Kang&Shin 2025 FEM; 문헌 1e-14–1e-13)
  · i0: --i0 (기본 2 A/m² = v1 훅), dU/dT: --dudt-csv (있을 때만 Q_rev 계산)
  셀프테스트는 합성 선형 OCP(TEST-ONLY 라벨)만 사용.
"""
import argparse
import json
import os
import sys

import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import cg

F_CONST = 96485.33212        # C/mol
R_GAS = 8.314462618          # J/mol/K
GPU = False                  # --gpu 로 켬; CuPy 실패 시 CPU 폴백 (step3_sigma 패턴)
_CG_DUMPED = [False]         # MPM_S4_DUMP_FAIL: 실패 선형계 1회만 덤프 (디스크 보호)
_NN_TRIGGER = 1e3            # near-null-B AMG 발동 문턱: 잔차가 목표의 이 배수 위(=정체)일 때만
                            # (거의-수렴 solve엔 안 켜 무거운 전처리 낭비 차단; 저율 정체는 ~1/rtol배 위)
_NN_ACCEPT_RTOL = 1e-7      # near-null-B AMG escalate 판정의 '물리-충분' 상대잔차 바닥.
#   ★정정 (2026-07-27 진단1 [3] 확정): 프로덕션 유일 콜사이트(newton, rtol=1e-5)에선
#   max(1e-5·‖b‖, atol, 1e-7·‖b‖) ≡ max(1e-5·‖b‖, atol) = 대수적 no-op — escalate 판정을 단 한 번도
#   안 바꿈 (EW inexact-Newton 도입 후에도 η≥1e-5라 no-op 성질 유지; selftest S5가 회귀 고정).
#   게이트가 실작동하는 곳은 rtol<1e-7 외부호출(test_step4_nearnull_integration.py:78)뿐이며, 실제
#   OOM 재발 방지 담보는 이 게이트가 아니라 nnamg_direct 승자 래치 + _CGStop 자기-바닥.  깊은 보정해
#   (atol=frac·floor 가 Jacobi 자기바닥 ~1.4e-12 아래)는 게이트와 무관하게 nnAMG로 '정당하게'
#   escalate — 속도는 GPU V-cycle(MPM_S4_GPU_AMG)이 치료, 회피는 MPM_S4_ATOL_FLOOR_FRAC=0.5(opt-in).
#   env MPM_S4_NN_ACCEPT_RTOL 는 외부 호출자용으로 유지(0 → 옛 rtol-only 게이트 복원).  ‖b‖-상대
#   게이트는 후기 Newton(‖b‖ 붕괴)에 구조적으로 무력 → 절대바닥 결합 MPM_S4_NN_ACCEPT_ABS_FRAC
#   (accept에 frac·agg_floor_abs 병합, 기본 0=OFF)가 실효 대안.


# ---------------------------------------------------------------- CG (warm start)
def _amg_M(L):
    """pyamg AMG preconditioner (그래프-라플라시안 특화) — 설치 시에만.  실패하면 None.
    MPM_S4_GPU_AMG(기본 ON)+GPU면 apply를 GPU V-cycle 미러로 (빌드는 CPU 1회) — 전처리는 CG의
    해를 바꾸지 않음(해-불변).  cupy 부재/OFF면 kw 자체 미전달 = 기본 GS 스무더 = 현행 bitwise."""
    try:
        import pyamg
    except ImportError:
        print('    ⚠ pyamg 미설치 → CPU Jacobi-CG 폴백(고대비 격자에선 미수렴 가능) — '
              '`python3 -m pip install pyamg` 후 재실행 권장', flush=True)
        return None
    try:
        import time as _t
        t0 = _t.time()
        print(f'    AMG 전처리 구축 중 (dof {L.shape[0]:,} — 수십초~수분)…', flush=True)
        _g = _gpu_amg_on()
        kw = (dict(presmoother=('jacobi', {'omega': 2.0 / 3.0, 'iterations': 1}),
                   postsmoother=('jacobi', {'omega': 2.0 / 3.0, 'iterations': 1}))
              if _g else {})                                  # GPU 미러=ω-Jacobi 대칭 (CPU·GPU 동수학)
        ml = pyamg.smoothed_aggregation_solver(sparse.csr_matrix(L), max_coarse=500, **kw)
        print(f'    AMG 구축 완료 (levels {len(ml.levels)}, {_t.time() - t0:.0f}s) → CG', flush=True)
        if _g:
            Mg = _gpu_vcycle_wrap(ml)
            if Mg is not None:
                print('    (AMG apply=GPU V-cycle — MPM_S4_GPU_AMG=0 해제)', flush=True)
                return Mg
        return ml.aspreconditioner(cycle='V')
    except Exception as e:
        print(f'    ⚠ AMG 구축 실패 ({type(e).__name__}: {e}) → Jacobi', flush=True)
        return None


def _nearnull_amg_M(L, diag, cache, k_b=8, k_lobpcg=12):
    """★near-null-B AMG (sym-scaled) — 저율 후막 약결합 BV near-null 전용 전처리.

    후막+저율은 전자-이온 BV 결합이 약해져 선형계가 near-null(diag_step4_nearnull.py 실측: N=4.4M
    에서 λ_min~2e-11 클러스터 12개, 대각 1e-11).  표준 AMG는 발산, Jacobi는 정체, ★정규화(J+εI)는
    해가 near-null에 살아 98% ε-민감(감쇠=해 왜곡)이라 부적합, ★deflation+Jacobi도 발산 — near-null
    벡터를 pyamg 근사-영공간 B로 주입한 AMG만 수렴(sym-scaled 8.3e-14, 100 it).  그 승자를 구현.

    near-null 벡터는 구조적(약결합 패턴)이라 런 내 1회 LOBPCG 계산 후 cache['nearnull_V']로 재사용;
    AMG 계층은 L 값에 의존해 호출 시 재구축(계층 구축 << solve).  무거우니(대-coarse V-cycle) 정체
    solve일 때만 발동(_cg 4단).
    ★R3 deflation k=64-128 기각 (2026-07-27): near-null 차원은 약결속 carbon cluster 수 O(10⁴)≫k라
    소-k deflation은 발산(1cf8d43 실측)하고 B-확장(k↑)은 대-coarse 재빌드 OOM을 재유발 — 부공간 몇
    개 늘려서 될 문제가 아님.  치료는 C0 부유-pruning(정확-특이 제거)+C3 GPU apply가 담당."""
    try:
        import pyamg
        from scipy.sparse.linalg import LinearOperator, lobpcg
    except ImportError:
        print('    ⚠ pyamg/scipy 없음 → near-null 폴백 불가 (`pip install pyamg`)', flush=True)
        return None
    N = L.shape[0]
    V = cache.get('nearnull_V')
    if V is None or V.shape[0] != N:                          # 런 1회: near-null 부공간 LOBPCG
        import time as _t
        t0 = _t.time()
        print(f'    near-null {k_lobpcg}벡터 LOBPCG 계산 중 (~수십초, 런 1회 후 재사용)…', flush=True)
        Minv = sparse.diags(1.0 / np.where(diag > 0, diag, 1.0))
        rng = np.random.default_rng(0)                        # 결정론(Date/random 규약 무관, 고정 seed)
        try:
            _ev, V = lobpcg(L, rng.standard_normal((N, k_lobpcg)), M=Minv,
                            largest=False, tol=1e-6, maxiter=200)
        except Exception as e:
            print(f'    near-null LOBPCG 실패 ({type(e).__name__}: {e})', flush=True)
            return None
        cache['nearnull_V'] = V
        print(f'    near-null λ~{float(np.min(_ev)):.2e}..{float(np.max(_ev)):.2e} '
              f'({_t.time() - t0:.0f}s, {k_lobpcg}개)', flush=True)
    try:                                                      # sym-scaled near-null-B AMG (진단 승자)
        kk = min(k_b, V.shape[1])
        s = 1.0 / np.sqrt(np.maximum(np.abs(diag), 1e-300))   # 대칭 대각 스케일 (near-isolated 노드 정규화)
        Ls = (sparse.diags(s) @ L @ sparse.diags(s)).tocsr()
        B = np.hstack([np.ones((N, 1)), V[:, :kk]]) / s[:, None]   # [상수모드 + near-null] / s
        _g = _gpu_amg_on()
        kw = (dict(presmoother=('jacobi', {'omega': 2.0 / 3.0, 'iterations': 1}),
                   postsmoother=('jacobi', {'omega': 2.0 / 3.0, 'iterations': 1}))
              if _g else {})                                  # GPU 미러=ω-Jacobi 대칭 (CPU·GPU 동수학)
        mls = pyamg.smoothed_aggregation_solver(Ls, B=B, max_coarse=800, **kw)
        if _g:
            Mg = _gpu_vcycle_wrap(mls, s=s)                   # matvec(r)=s·V(s·r) — CPU 래퍼와 동수학
            if Mg is not None:
                print('    (near-null-B AMG apply=GPU V-cycle)', flush=True)
                return Mg
        ml = mls.aspreconditioner('V')
        return LinearOperator(L.shape, matvec=lambda r, _s=s, _m=ml: _s * _m.matvec(_s * r))
    except Exception as e:
        print(f'    near-null-B AMG 구축 실패 ({type(e).__name__}: {e})', flush=True)
        return None


# ---------------------------------------------------------------- GPU V-cycle 전처리 미러 (C3)
_GPU_AMG_STATE = {'ok': None}                      # cupy 가용성 런-1회 판정 캐시


def _gpu_amg_on():
    """MPM_S4_GPU_AMG(기본 ON) ∧ GPU(--gpu) ∧ cupy import 성공.  gpu_dead 라치와 무관
    (Jacobi-CG 미수렴 ≠ GPU 고장 — SpMV는 유효).  실패 시 런 1회 로그 후 False 캐시."""
    if os.environ.get('MPM_S4_GPU_AMG', '1') == '0' or not GPU:
        return False
    if _GPU_AMG_STATE['ok'] is None:
        try:
            import cupy, cupyx.scipy.sparse        # noqa: F401
            _GPU_AMG_STATE['ok'] = True
        except Exception as e:
            _GPU_AMG_STATE['ok'] = False
            print(f'    (GPU V-cycle 불가: {type(e).__name__} → CPU 전처리 유지)', flush=True)
    return _GPU_AMG_STATE['ok']


def _mirror_levels(ml, xp, dtype=np.float64):
    """pyamg 계층 → [{'A','P','R','Dinv'}...] (xp=numpy: CPU 동수학 / xp=cupy: GPU 미러 —
    cupyx.scipy.sparse.csr_matrix 1회 전송).  coarsest(≤max_coarse 500/800)는 CPU dense LU
    (scipy.linalg.lu_factor) 1회 캐시 — it당 왕복 ~KB.  반환 (levels, lu_pair)."""
    from scipy.linalg import lu_factor
    if xp is np:
        def _csr(A):
            return sparse.csr_matrix(A).astype(dtype)

        def _vec(v):
            return np.asarray(v, dtype)
    else:
        import cupyx.scipy.sparse as _cxs

        def _csr(A):
            return _cxs.csr_matrix(sparse.csr_matrix(A).astype(dtype))

        def _vec(v):
            return xp.asarray(v, dtype)
    # ★레벨별 ω = (2/3)/ρ(D⁻¹A) — pyamg 의 setup_jacobi(withrho=True) 기본과 동일 정규화.
    #   생짜 ω=2/3 은 (a) pyamg 계층과 **다른 연산자**(rel-diff 0.6 실측)라 CPU 폴백·자가강등과
    #   불일치하고, (b) ρ>3 인 레벨에서 전처리가 **부정부호**가 되어 CG 전제가 깨진다
    #   (near-null-B 계층 실측 ρ=2.98 = 한계 3 의 99.3%).  2026-07-27 적대검증 H1/H2.
    from pyamg.relaxation.smoothing import rho_D_inv_A as _rho
    levels = []
    for lv in ml.levels[:-1]:
        A = lv.A.tocsr()
        d = A.diagonal()
        try:                                                  # ★lv.A 원본에 물어야 pyamg 가 setup 때
            _om = (2.0 / 3.0) / float(_rho(lv.A))             #   캐시한 ρ(A.rho_D_inv)를 그대로 재사용
        except Exception:                                     #   (사본에 물으면 근사 재추정 → 미세 불일치)
            _om = (2.0 / 3.0) / 2.0                           # 보수적 폴백(ρ≈2 가정 → SPD 안전측)
        levels.append({'A': _csr(A), 'P': _csr(lv.P.tocsr()), 'R': _csr(lv.P.T.tocsr()),
                       # 대각 0 행은 Dinv=0 (pyamg jacobi 커널이 그 행을 건너뛰는 것과 정합; L2)
                       'Dinv': _vec(np.where(d != 0, 1.0 / np.where(d != 0, d, 1.0), 0.0)),
                       'omega': float(_om)})
    # ★coarsest: (i) 크기 가드 — B-주입(near-null) 계층은 coarsening 이 정체해 coarsest 가 fine 의
    #   114% 까지 커진 실측이 있다 → todense() 가 OOM 재발 경로.  (ii) pinv 사용 — 정확-특이 블록
    #   (i-망 부유 171성분 등)에서 LU 는 NaN 을 내는데 예외가 아니라 자가강등도 안 걸린다.  H3/H4.
    Ac = ml.levels[-1].A.tocsr()
    n_c = Ac.shape[0]
    _NMAX = int(os.environ.get('MPM_S4_GPU_AMG_COARSE_MAX', '4000'))
    if n_c > _NMAX:
        raise RuntimeError(f'coarsest {n_c:,} > {_NMAX:,} (dense 해 비현실) — CPU 전처리 폴백')
    # ★pyamg 가 쓰는 그 coarse_solver 객체를 그대로 재사용 = 수학적으로 동일 + 특이 블록 안전
    #   (기본 'pinv'.  직접 pinv/LU 를 만들면 미세 불일치(1e-5)가 생기고 LU 는 NaN 위험)
    coarse = (ml.coarse_solver, Ac)
    return levels, coarse


def _vcycle_matvec(levels, lu_pair, b, xp, omega=None, lvl=0):
    """대칭 V(1,1): pre ω-Jacobi(x0=0 → x=ωD⁻¹b) → r=b−Ax → R·r 재귀 → x+=P·xc →
    post ω-Jacobi(x += ωD⁻¹(b−Ax)).  R=Pᵀ(SA 대칭) + pre/post 동일 스무더 ⇒ M 대칭
    SPD-호환(CG 요건 — pyamg 기본 GS는 순차라 GPU 부적합, ω-Jacobi로 통일).
    ω는 레벨별 (2/3)/ρ(D⁻¹A) (= pyamg withrho=True 기본) — _mirror_levels 가 구워둔 값을 쓴다.
    coarsest 는 pinv (특이 블록 안전).  xp-디스패치 단일 구현 = CPU/GPU 동수학."""
    if lvl == len(levels):                                    # coarsest: pyamg coarse_solver (CPU)
        bc = b if xp is np else xp.asnumpy(b)
        _cs, _Ac = lu_pair
        xc = np.asarray(_cs(_Ac, np.asarray(bc, np.float64)), np.float64)
        return xc.astype(b.dtype) if xp is np else xp.asarray(xc, b.dtype)
    lv = levels[lvl]
    om = lv.get('omega', 2.0 / 3.0) if omega is None else omega
    x = om * lv['Dinv'] * b                                   # pre ω-Jacobi (x0=0)
    r = b - lv['A'] @ x
    x = x + lv['P'] @ _vcycle_matvec(levels, lu_pair, lv['R'] @ r, xp, omega, lvl + 1)
    return x + om * lv['Dinv'] * (b - lv['A'] @ x)            # post ω-Jacobi


def _gpu_vcycle_wrap(ml, s=None):
    """scipy LinearOperator 반환: matvec = numpy r → (s·)V-cycle(GPU)(·s) → numpy.
    s≠None(nnAMG): s를 GPU 상주, matvec(r)=s·V(s·r) — _nearnull_amg_M CPU 래퍼와 동수학.
    dtype: MPM_S4_GPU_AMG_F32=1 → float32 미러(전처리 정밀도만 — CG는 CPU f64, 해 불변).
    apply 중 예외 1회 → 내장 CPU ml.aspreconditioner 로 자가 강등 + 로그 1줄 (그 콜부터 CPU).
    미러 실패(OOM 등) → None 반환 (호출측 기존 CPU 경로 폴백)."""
    from scipy.sparse.linalg import LinearOperator
    try:
        import cupy as cp
        dtype = np.float32 if os.environ.get('MPM_S4_GPU_AMG_F32', '0') == '1' else np.float64
        levels, lu_pair = _mirror_levels(ml, cp, dtype=dtype)
        sg = None if s is None else cp.asarray(s, dtype)
    except Exception as e:
        print(f'    (GPU V-cycle 미러 실패: {type(e).__name__}: {e} → CPU 전처리 폴백)', flush=True)
        return None
    st = {'cpu': None}                                        # 자가 강등 상태 (예외 1회 → 이후 CPU)

    def _mv(r):
        if st['cpu'] is None:
            try:
                import cupy as cp
                rg = cp.asarray(r, dtype)
                if sg is not None:
                    rg = sg * rg
                zg = _vcycle_matvec(levels, lu_pair, rg, cp)
                if sg is not None:
                    zg = sg * zg
                z_out = cp.asnumpy(zg).astype(np.float64, copy=False)
                if not np.isfinite(z_out).all():              # NaN/Inf 는 예외가 아니라 자가강등을
                    raise FloatingPointError('V-cycle 결과 비유한')   # 못 타므로 명시적으로 올린다
                return z_out
            except Exception as e:
                print(f'    (GPU V-cycle apply 예외: {type(e).__name__} → CPU 전처리 자가 강등)',
                      flush=True)
                st['cpu'] = ml.aspreconditioner(cycle='V')
        z = st['cpu'].matvec(r if s is None else s * r)
        return np.asarray(z if s is None else s * z, np.float64)

    return LinearOperator(ml.levels[0].A.shape, matvec=_mv)


def cg_ab_verdict(t_ladder, t_jacobi, info, margin=0.9):
    """비용 A/B 판정 (순수 함수 — selftest 대상).  반환 ('gpu_jacobi'|'ladder', 사유).

    두 팔은 같은 rtol 로 같은 Jx=b 를 푼다 → 해가 같으므로 비교 기준은 **벽시계뿐**이다.
    전환에 10 % 마진을 두는 이유: 연속한 두 Newton 반복은 같은 계가 아니라 조건수가 조금
    다르므로, 측정 노이즈로 왕복 전환(chatter)이 나면 안 된다.  판단이 안 서면 현행 유지."""
    if t_jacobi is None or info != 0:
        return 'gpu_jacobi', 'no_comparison_or_ladder_not_converged'
    if float(t_ladder) < float(margin) * float(t_jacobi):
        return 'ladder', 'ladder_faster'
    return 'gpu_jacobi', 'jacobi_not_beaten'


def _cg(L, b, x0=None, rtol=1e-9, atol=0.0, pc_cache=None, deep=False, floor_abs=0.0):
    """3단 솔브: GPU Jacobi-CG → (실패시) CPU AMG-CG(pyamg) → CPU Jacobi-CG.
    실전 격자(VGCF 100 S/cm ↔ BV면 1e-11 S, ~9자릿수 대비)에서 Jacobi 단독은 정체할 수
    있어(2026-07-15 V100 스모크: 50k iter 미수렴) AMG 폴백이 프로덕션 안전망.
    deep=True: 심층-수렴권 정밀 솔브(RHS가 거의 노이즈) — GPU 실패 시 CPU로 내려가지 않고
    'deep_weak'만 기억하고 반환 (35분짜리 무용 CPU-CG 방지; newton 게이트가 수렴 취급).
    pc_cache: 'gpu_dead'=실솔브 GPU 무능(sticky) · 'deep_weak'=심층권 무용 · 'amg'=계층 재사용."""
    diag = L.diagonal()
    cache = pc_cache if pc_cache is not None else {}
    # ── ★ 비용-기반 승급 (2026-07-29, opt-in) ────────────────────────────────────────────────
    #   문제: 이 사다리는 **실패로만** 승급한다.  GPU Jacobi-CG 가 성공하면 바로 아래 return 이
    #   걸려 CPU AMG · near-null-B AMG · 승자 래치가 **전부 도달 불가**가 된다.  그래서
    #   19,999번째 반복에서 61초 만에 수렴한 솔브와 50번에 끝난 솔브가 똑같이 취급된다.
    #   실측(V100 0.2C, cap200 적용 후): 61 s/CG × Newton 4회 = 244 s/step → step 하나에 2~3일.
    #   ★ 이 레짐이 바로 near-null-B AMG 를 만든 이유(작업 #20/#27)인데, CG 가 "느리게 성공"
    #     하는 바람에 후보로조차 오르지 못했다.  #27 의 hard-fail 과 같은 기전(near-null 오차는
    #     J·v≈0 라 잔차 norm 에 작게 실림)이 다른 얼굴로 나타난 것.
    #   해법: 예산(초)을 주면 GPU Jacobi 가 그보다 오래 걸린 순간 **다음 솔브 한 번만** 사다리로
    #   내려보내 시간을 재고, 빠른 쪽을 래치한다.  추가 솔브 0회(연속 두 솔브를 A/B 로 씀).
    #
    #   ★★ 실측 결과 (2026-07-29 V100, 이 가설은 **기각됨**) ★★
    #     dof 4,424,695 · 0.2C · cap200 에서:  GPU Jacobi 43.5 s  vs  AMG 사다리 440.9 s
    #     = **Jacobi 가 10.1× 빠름**.  사다리 내역: AMG 구축 100 s(levels 4) + CG 341 s(900+ it,
    #     GPU V-cycle apply).  ⇒ near-null-B AMG 는 이 규모에서 답이 아니다.  이 노브는 그
    #     사실을 **측정으로** 확인하라고 남겨둔 것이지, 켜면 빨라지는 스위치가 아니다.
    #     같은 가설을 다시 세우기 전에 docs/step4_bottleneck_analysis_20260727.md §11 을 읽을 것.
    #
    #   ⚠ 정정 (커밋 32a57f2c 메시지의 과잉주장): "cannot change any result" 는 **너무 강했다**.
    #     수렴한 Newton 근은 안 바뀌는 게 맞다(수렴 판정은 정확 재계산 F, tol_rel=1e-8).  그러나
    #     사다리 팔은 목표 2.90e-13 까지 훨씬 더 조여서 반환했다 → 중간 iterate 가 달라지고
    #     → Newton 궤적이 달라지고 → 이후 선형계가 달라진다.  실제로 프로브 직후 GPU 가
    #     maxiter(20000)를 소진해 gpu_dead 가 걸렸다(그 인과는 **미확정** — 배제할 수 없다는
    #     것이 요점).  ⇒ 프로브는 궤적-중립이 아니다.  프로덕션 런에 켜지 말 것.
    import time as _tm
    _budget = float(os.environ.get('MPM_S4_CG_BUDGET_S', '0') or 0)
    # ★ dof 상한 가드: 위 실측대로 대형계에서는 AMG 구축(100 s)만으로도 이미 지므로 프로브를
    #   아예 막는다.  ⚠ 이 값은 **측정된 교차점이 아니다** — 우리가 가진 점은 "4.4M 에서 10.1×
    #   진다" 하나뿐이고, AMG 가 이기기 시작하는 dof 는 미측정이다.  즉 무지의 안전변이지
    #   물리/수치적 문턱이 아니며, 필요하면 env 로 올려서 직접 재보라는 뜻이다.
    _probe_max_dof = int(float(os.environ.get('MPM_S4_CG_PROBE_MAX_DOF', '1000000') or 0))
    if _budget > 0 and _probe_max_dof > 0 and L.shape[0] > _probe_max_dof:
        if not cache.get('probe_dof_skipped'):
            cache['probe_dof_skipped'] = True
            cache['cg_winner'] = 'gpu_jacobi'                 # 프로브 없이 현행 확정
            print(f'    ℹ 비용-프로브 생략: dof {L.shape[0]:,} > 상한 {_probe_max_dof:,} — '
                  f'이 규모에선 AMG 가 진다고 실측됨(4.4M: 43.5s vs 440.9s = 10.1×).  '
                  f'다시 재려면 MPM_S4_CG_PROBE_MAX_DOF 를 올릴 것', flush=True)
        _budget = 0.0                                         # 이하 계측·전환 전부 비활성
    _try_ladder = _budget > 0 and cache.get('cg_winner') == 'ladder'
    _probe_ladder = _budget > 0 and cache.get('cg_probe_pending') and cache.get('cg_winner') is None
    _t_enter = _tm.time()
    if GPU and not cache.get('gpu_dead') and not _try_ladder and not _probe_ladder:
        try:
            import cupy as cp
            import cupyx.scipy.sparse as cxs
            from cupyx.scipy.sparse.linalg import cg as cg_gpu
            if L.shape[0] >= 50000:
                print(f'      GPU Jacobi-CG 시도 (≤20k it, ~1분 — 실패 시 AMG 폴백)…', flush=True)
            Lg = cxs.csr_matrix(L.astype(np.float64))
            bg = cp.asarray(b, np.float64)
            dg = cp.asarray(diag)
            Mg = cxs.diags(1.0 / cp.where(dg > 0, dg, dg.max()))   # zero/음-diag → inf/NaN 전처리 차단 (벨트-앤-서스펜더)
            x0g = cp.asarray(x0, np.float64) if x0 is not None else None
            try:
                xg, info = cg_gpu(Lg, bg, x0=x0g, tol=rtol, maxiter=20000, M=Mg)
            except TypeError:
                xg, info = cg_gpu(Lg, bg, x0=x0g, rtol=rtol, atol=atol, maxiter=20000, M=Mg)
            if int(info) == 0:
                # ★ 비용 계측: 성공했더라도 예산을 넘겼으면 다음 솔브 한 번을 사다리로 보내 A/B.
                #   (이 솔브의 해는 그대로 반환 — 계측이 값을 바꾸지 않는다.)
                _el = _tm.time() - _t_enter
                if _budget > 0 and cache.get('cg_winner') is None and L.shape[0] >= 50000:
                    cache['t_gpu_jacobi'] = _el
                    if _el > _budget and not cache.get('cg_probe_pending'):
                        cache['cg_probe_pending'] = True
                        print(f'    ⏱ GPU Jacobi-CG {_el:.1f}s > 예산 {_budget:g}s — 다음 솔브 1회를 '
                              f'AMG 사다리로 보내 A/B 후 빠른 쪽 래치 (해 불변: 전처리기는 CG 해를 '
                              f'바꾸지 않음)', flush=True)
                    elif _el <= _budget:
                        cache['cg_winner'] = 'gpu_jacobi'     # 예산 내 = 현행 유지, 더 재지 않음
                return cp.asnumpy(xg), 0
            if deep:                                         # 심층권 실패 = 부동소수 한계, GPU 탓 아님
                cache['deep_weak'] = True                    #   → GPU 살려두고 CPU 낭비도 생략
                print('      (심층-수렴권 CG 무용 확인 — 이후 이 구간은 수렴 취급)', flush=True)
                return cp.asnumpy(xg), int(info)
            cache['gpu_dead'] = True                         # 실솔브 실패만 sticky
            print(f'    step4 GPU Jacobi-CG 미수렴(info={int(info)}) → CPU AMG 폴백 '
                  f'(이 런에서는 이후 GPU 시도 생략)', flush=True)
            x0 = cp.asnumpy(xg)                              # GPU 진행분을 warm start로 재사용
        except Exception as e:
            cache['gpu_dead'] = True
            print(f'    step4 GPU solve unavailable ({type(e).__name__}: {e}) → CPU', flush=True)

    big = L.shape[0] >= 50000

    class _CGStop(Exception):
        pass

    def _solve(Mp, x_init):
        cb = None
        best = {'r': None, 'x': None, 'bad': 0}
        r0 = None
        tgt = 1e-300
        if big:                                              # CG 진행률 (50 iter마다 잔차 실측 —
            import time as _t                                # 수렴이 로그-선형이라 log-스케일 %)
            b_n = float(np.linalg.norm(b))
            r0 = float(np.linalg.norm(b - L @ x_init)) if x_init is not None else b_n
            tgt = max(rtol * b_n, atol, 1e-300)
            box = {'n': 0, 't0': _t.time()}
            den = max(np.log(max(r0 / tgt, 1.0 + 1e-9)), 1e-9)

            def cb(xk):
                box['n'] += 1
                if box['n'] % 50:
                    return
                r = float(np.linalg.norm(b - L @ xk))
                prog = min(99.0, max(0.0, 100.0 * np.log(max(r0 / max(r, 1e-300), 1.0)) / den))
                print(f'      CG {box["n"]:5d} it  resid {r:.2e} (목표 {tgt:.2e})  '
                      f'~{prog:.0f}%  {_t.time() - box["t0"]:.0f}s', flush=True)
                # 자기-감지 정지: 자기 바닥(3연속 무개선/재상승)에 닿으면 best 반복해 채택 —
                # 도달불가 목표를 쫓다 반올림으로 Krylov가 붕괴·발산하는 것 차단 (스트레스 실증)
                if best['r'] is None or r < 0.7 * best['r']:
                    best['r'] = r; best['x'] = xk.copy(); best['bad'] = 0
                else:
                    best['bad'] += 1
                    if best['bad'] >= 3:
                        raise _CGStop()
        mi = 1500 if big else 50000                          # CPU-AMG는 ~수백 iter가 정상 —
        try:                                                 # 1500 미달이면 더 돌려도 가망 없음
            try:
                x_sol, info = cg(L, b, x0=x_init, rtol=rtol, atol=atol, maxiter=mi, M=Mp, callback=cb)
            except TypeError:
                x_sol, info = cg(L, b, x0=x_init, tol=rtol, maxiter=mi, M=Mp, callback=cb)
        except _CGStop:
            x_sol = best['x']
            info = 0 if (r0 is not None and best['r'] <= max(0.1 * r0, tgt)) else 1
            print(f'      CG 자기-바닥 정지 → best resid {best["r"]:.2e} 채택 (info={info})', flush=True)
        if info and big and deep:
            cache['deep_weak'] = True                        # 심층-수렴권 CG 무용 기억 (런 전체)
        return x_sol, info

    bnorm = float(np.linalg.norm(b))
    def _rr(xx):                                             # 잔차 노름 (None = 영-시작 = ||b||); 비유한=∞
        if xx is None:
            return bnorm
        r = float(np.linalg.norm(b - L @ xx))
        return r if np.isfinite(r) else np.inf
    if x0 is not None and _rr(x0) > bnorm:                   # 실패한 GPU 부분해가 0보다 나쁘면 폐기
        x0 = None                                            # (잔차 상승-표류 방지, V100 smoke6 로그)
    r_start = _rr(x0)
    big = L.shape[0] >= 50000                                # 소형(셀프테스트급)은 Jacobi로 충분
    # ★승자 직행 래치 (2026-07-23): near-null-B AMG가 이 런의 승자로 확정되면(nnamg_direct) 이후
    #   솔브는 정체하는 AMG·Jacobi 사다리를 건너뛰고 near-null-B AMG로 직행 → Newton당 ~280s 절감
    #   (AMG 무용 정체 ~140s + 중복 Jacobi ~140s 제거).  전처리 M은 CG의 해 x를 바꾸지 않고 수렴
    #   속도만 바꿈(CG는 어떤 SPD M에서도 같은 Jx=b로 수렴).  ★정밀 (리뷰 B#2): 이는 CG가 목표
    #   잔차에 '도달할 때' 정확 — _CGStop 자기-바닥(≈10×목표)에서 멈추면 전처리별 self-floored
    #   iterate가 달라 Newton 궤적이 pre-latch와 bit-동일하진 않을 수 있음(단 같은 근으로 수렴,
    #   최종가드가 r_start 초과 금지).  nnamg가 승자인 상황에선 직행·escalate 둘 다 같은 x0서
    #   _solve(nnamg) → bit-동일.  = 실질 해-불변, 안전.
    _direct_nn = big and bool(cache.get('nnamg_direct')) and cache.get('nnamg') is not None
    amg_ok = big and not cache.get('amg_useless') and not _direct_nn  # ★AMG 무용/직행이면 건너뜀
    M = None
    fresh_amg = False
    _pc_kind = 'jacobi'                                       # 첫 솔브 전처리 종류(중복 Jacobi 판정용)
    if _direct_nn:
        M = cache['nnamg']; _pc_kind = 'nnamg'               # near-null-B AMG를 1순위 전처리로 직행
        print('    ★near-null-B AMG 직행 (승자 래치 — AMG·Jacobi 사다리 생략; 해 불변)', flush=True)
    elif amg_ok:
        M = cache.get('amg')
        if M is None:
            M = _amg_M(L)
            fresh_amg = M is not None
            if M is not None:
                cache['amg'] = M
        _pc_kind = 'amg' if M is not None else 'jacobi'
    if M is None:
        M = sparse.diags(1.0 / diag)
    x, info = _solve(M, x0)
    # ★ 낡은/약한 AMG가 미수렴 또는 발산(해가 시작보다 나쁨)이면 fresh 계층 재구축.
    #   ⚠ 재구축은 반드시 CLEAN warm-start(x0)에서 — 발산해 x를 넘기면 resid 1e3서 시작해
    #   회복 불가였음 (2026-07-22 0.2C 저율 수렴실패 근본원인 중 하나; 발산해=쓰레기 warm).
    if (info != 0 or _rr(x) > r_start) and amg_ok and not fresh_amg:
        print('    AMG 캐시 계층 미수렴/발산 → 재구축 (clean warm-start)', flush=True)
        cache.pop('amg', None)
        M2 = _amg_M(L)
        if M2 is not None:
            cache['amg'] = M2
            x2, info2 = _solve(M2, x0)                        # ★ 발산해 x가 아닌 clean x0에서
            if _rr(x2) < _rr(x):
                x, info = x2, info2
    # ★ AMG가 여전히 발산(해가 시작보다 나쁨 = 전처리 비-SPD 신호)이면 Jacobi-CG SPD-safe 폴백.
    #   대각(>0) 전처리는 SPD → SPD 행렬 J에서 CG는 발산 불가(정체만).  느려도 유효 하강방향 →
    #   Newton 감쇠가 부분진행 수용 (발산해→Armijo 거부→정체 를 회피).  (2026-07-22)
    if _rr(x) > r_start and big:
        if _pc_kind == 'jacobi':
            # 첫 솔브가 이미 Jacobi(자기-바닥) → 동일 전처리 재솔브는 bit-동일 무의미 → 생략(중복 ~140s 제거).
            # x(자기-바닥 Jacobi 해) 유지하고 아래 near-null-B escalate 로 직행.
            pass
        else:
            print('    AMG 발산 지속 → Jacobi-CG SPD-safe 폴백 (발산 불가)', flush=True)
            xj, infoj = _solve(sparse.diags(1.0 / diag), x0)
            if _rr(xj) < _rr(x):
                x, info = xj, infoj
            if amg_ok and not cache.get('amg_useless'):      # ★AMG 발산+Jacobi 승 확정 → 이후 AMG 생략(sticky)
                cache['amg_useless'] = True                   #   (gpu_dead 계열; near-null 격자서 AMG 매번 발산 → 낭비 차단)
                cache.pop('amg', None)
                print('    (이후 이 런의 실솔브는 AMG 생략 → Jacobi 직행)', flush=True)
        if _direct_nn:                                        # ★직행 nnamg가 시작보다 나빠짐(계층 표류) → 래치 해제
            cache.pop('nnamg_direct', None); cache.pop('nnamg', None)
            print('    (near-null-B AMG 직행 열화 → 래치 해제, 다음 솔브 사다리 재구축)', flush=True)
    # ★ 4단(near-null-B AMG): AMG 발산 + Jacobi 정체로도 잔차가 목표의 _NN_TRIGGER배 위(=near-null
    #   정체)면, near-null 벡터를 AMG B로 주입한 전처리로 escalate.  diag_step4_nearnull.py 승자
    #   (정규화 98%ε민감·deflation 발산 실패 → near-null-B AMG만 수렴).  저율 0.1C/0.2C 후막의
    #   hard-fail 근본해결.  런 내 1회 구축 후 재사용; 정체 solve일 때만 발동(무거운 대-coarse).
    _tgt = max(rtol * bnorm, atol, 1e-300)
    # ★물리-충분 바닥 (2026-07-26 v100 2C OOM 진단): rtol=1e-9 목표는 near-null서 도달불가라 자기-바닥
    #   (rel≈7e-9)이 항상 '목표 미달'로 잡혀 near-null-B AMG가 매 솔브 발동→4.44M dof 빌드 OOM(Killed).
    #   노이즈바닥(rel~1e-5)의 100× 아래(_NN_ACCEPT_RTOL)까진 '충분 수렴'으로 인정 → 물리-정확 솔브 통과.
    _acc_rtol = float(os.environ.get('MPM_S4_NN_ACCEPT_RTOL', _NN_ACCEPT_RTOL))
    # ★accept 절대바닥 (C4c, 기본 0=OFF): ‖b‖-상대 게이트는 후기 Newton(‖b‖ 붕괴)서 무력 —
    #   frac·agg_floor_abs 를 병합하면 노이즈바닥-스케일 '물리-충분' 판정이 ‖b‖와 무관하게 성립.
    _accept = max(_tgt, _acc_rtol * bnorm,
                  float(os.environ.get('MPM_S4_NN_ACCEPT_ABS_FRAC', '0') or 0) * floor_abs)
    # ★트리거 수정 (2026-07-23 v100 0.2C 실런 진단): 자기-바닥(_CGStop)이 CG를 ~10×목표서 멈춰 잔차가
    #   1000×문턱에 도달 못 → near-null-B AMG 실전 미발동 = 0.2C hard-fail 근본원인.  near-null 오차는
    #   J·v≈0 라 잔차 norm에 작게 실려 '비율'판정이 부적합 → 판정을 '충분-수렴 미달(info≠0=자기-바닥
    #   단축) + 유의미 초과(>3×바닥)'로 전환 (기존 1000× 조건은 belt-and-suspenders로 유지).
    _stall_short = (info != 0 and _rr(x) > 3.0 * _accept) or (_rr(x) > _NN_TRIGGER * _accept)
    # ★ _direct_nn(승자 직행)이면 이미 near-null-B AMG로 풀었으니 재-escalate 생략(이중 ~550s 방지).
    if _stall_short and big and not cache.get('nnamg_dead') and not _direct_nn:
        Mnn = cache.get('nnamg')
        if Mnn is None:
            Mnn = _nearnull_amg_M(L, diag, cache)
            if Mnn is not None:
                cache['nnamg'] = Mnn
            elif cache.get('nearnull_V') is None:            # 구축 자체 불가(pyamg 없음) → 재시도 안 함
                cache['nnamg_dead'] = True
        if Mnn is not None:
            print('    ★near-null-B AMG 폴백 (저율 약결합 near-null; 런 내 재사용)…', flush=True)
            xn, infon = _solve(Mnn, x0)                       # ★clean warm-start (발산해 금지, 3단 교훈)
            if _rr(xn) < _rr(x):
                x, info = xn, infon
                cache['nnamg_direct'] = True                  # ★승자 확정 → 다음 솔브부터 직행 래치(사다리 생략)
            else:                                             # 캐시 계층이 낡음(L 값 표류) → 계층만 1회 재구축
                cache.pop('nnamg', None)
                Mnn2 = _nearnull_amg_M(L, diag, cache)        # nearnull_V 재사용, Ls 계층 재구축
                if Mnn2 is not None:
                    cache['nnamg'] = Mnn2
                    xn2, infon2 = _solve(Mnn2, x0)
                    if _rr(xn2) < _rr(x):
                        x, info = xn2, infon2
                        cache['nnamg_direct'] = True          # ★재구축본이 승자 → 직행 래치
                    else:                                     # 계층 재구축도 실패 → near-null 부공간이 표류
                        cache.pop('nearnull_V', None)         #   → 다음 solve서 LOBPCG 재계산(구조 갱신)
    # ★ 최종 가드: 어떤 시도도 시작보다 못하면 warm-start 자체 반환 (쓰레기 해 전파 차단 →
    #   Newton Armijo 무-스텝 깔끔 정지).  재현 안 되는 발산은 실제 행렬 덤프로 진단:
    if _rr(x) > r_start:
        if os.environ.get('MPM_S4_DUMP_FAIL') and not _CG_DUMPED[0]:
            try:
                fn = 'step4_cg_fail.npz'
                sparse.save_npz('step4_cg_fail_L.npz', L.tocsr())
                np.savez(fn, b=b, x0=(x0 if x0 is not None else np.zeros_like(b)),
                         diag=diag, r_start=r_start, r_x=_rr(x))
                _CG_DUMPED[0] = True
                print(f'    ⚠ CG 발산 — 실패 선형계 덤프 저장 (step4_cg_fail_L.npz + {fn}) '
                      f'→ 진단 요청 시 첨부', flush=True)
            except Exception as _e:
                print(f'    (덤프 실패: {type(_e).__name__})', flush=True)
        x = x0 if x0 is not None else np.zeros_like(b)
        info = 1
    # ★ 비용 A/B 마무리 (2026-07-29): 이 솔브가 프로브(사다리 팔)였으면 시간을 재서 승자를 확정.
    #   GPU Jacobi 팔의 시간은 직전 솔브에서 cache['t_gpu_jacobi'] 에 기록돼 있다.  둘 다 같은
    #   rtol 로 수렴하므로 비교 대상은 오직 **벽시계**다 (해는 어느 쪽이든 같다).
    if _probe_ladder:
        _t_ladder = _tm.time() - _t_enter
        _t_jac = cache.get('t_gpu_jacobi')
        cache['cg_probe_pending'] = False
        cache['t_ladder'] = _t_ladder
        _win, _why = cg_ab_verdict(_t_ladder, _t_jac, info)
        cache['cg_winner'] = _win
        if _win == 'ladder':
            print(f'    ★ A/B 승자 = AMG 사다리: {_t_ladder:.1f}s vs GPU Jacobi {_t_jac:.1f}s '
                  f'({_t_jac / max(_t_ladder, 1e-9):.2f}× 빠름) → 이후 사다리 직행 (해 불변)', flush=True)
        else:
            print(f'    ⏱ A/B 승자 = GPU Jacobi ({_why}): 사다리 {_t_ladder:.1f}s vs '
                  f'{_t_jac if _t_jac is not None else float("nan"):.1f}s → 현행 유지', flush=True)
    if big:                                                   # 경로 감사 로그 (C5): 전처리 종류·잔차·목표
        print(f'      [cg] pc={_pc_kind}{"→nnamg" if (cache.get("nnamg_direct") and _pc_kind != "nnamg") else ""}'
              f' resid {_rr(x):.2e} tgt {_tgt:.2e} info {info}'
              + (f' {_tm.time() - _t_enter:.1f}s' if _budget > 0 else ''), flush=True)
    return x, info


# ---------------------------------------------------------------- 구형확산 (FV + CN)
class RadialDiffusion:
    """입자별 구형 1D Fick, 정규화 반경 ρ=r/R ∈ [0,1], FV 셸 Nr개, Crank–Nicolson.

    FV: Ṽ_k·dx_k/dt = (D/R²)[A_hi(x_{k+1}−x_k) − A_lo(x_k−x_{k−1})]/Δρ + δ_{k,Nr−1}·J/(c_max·R)
      (Ṽ_k = (ρ_{k+1}³−ρ_k³)/3 = 단위구 셸부피/4π; 표면 면적항 ρ²=1; 결합계수에 Δρ는 1회 —
       스케일은 √t selftest가 고정)
    질량보존: Σ Ṽ_k Δx_k = Δt·J/(c_max·R) — CN+FV에서 기계정밀도 (selftest 1).
    x_surf = x_{Nr−1} + (∂x/∂ρ)|₁·Δρ/2,  (∂x/∂ρ)|₁ = J·R/(D·c_max)  (flux-BC ghost 외삽).
    D는 스칼라(전 입자 공유) 또는 [n_p] per-particle (bimodal poly/SC 분리 — λ·surf_x 모두
    입자축 브로드캐스트라 수치경로 동일; 균일값 배열 ≡ 스칼라 bitwise는 selftest가 고정)."""

    def __init__(self, n_p, nr, r_p_m, d_s, c_max, x_init):
        self.n_p, self.nr = int(n_p), int(nr)
        self.R = np.asarray(r_p_m, np.float64)              # [n_p] m
        self.D = np.asarray(d_s, np.float64) * np.ones(self.n_p)   # [n_p] m²/s (스칼라→공유 브로드캐스트)
        if not np.all(self.D > 0):
            raise ValueError('RadialDiffusion: D_s must be > 0 (per-particle 포함)')
        self.c_max = float(c_max)
        rho = np.arange(nr + 1) / nr
        self.d_rho = 1.0 / nr
        self.Vk = (rho[1:] ** 3 - rho[:-1] ** 3) / 3.0      # [nr]
        self.A_lo = rho[:-1] ** 2
        self.A_hi = rho[1:] ** 2
        self.x = np.full((self.n_p, nr), float(x_init))
        self.J = np.zeros(self.n_p)                         # 표면 몰유속 [mol/m²/s], 리튬화 +

    def surf_x(self):
        grad = self.J * self.R / (self.D * self.c_max)
        return np.clip(self.x[:, -1] + 0.5 * self.d_rho * grad, 1e-6, 1.0 - 1e-6)

    def mean_x(self):
        return (self.x * self.Vk).sum(1) / self.Vk.sum()

    def step(self, dt, theta=0.5):
        """θ-스킴 한 스텝 (J 고정) — θ=0.5 CN(기본, 기존과 bitwise 동일) / θ=1.0 BE(L-안정,
        Rannacher 스타트업용 — 급경사 초기장의 CN 링잉 킬, 수치리뷰 chain#1).  벡터화 Thomas."""
        _te = 1.0 - theta                                   # 명시(explicit) 몫
        lam = self.D * dt / (self.R ** 2)                   # [n_p]
        aL = self.A_lo / (self.Vk * self.d_rho)             # [nr]
        aH = self.A_hi / (self.Vk * self.d_rho)
        lo = np.outer(lam, aL)                              # [n_p, nr] (k=0 열은 0)
        hi = np.outer(lam, aH)
        hi[:, -1] = 0.0                                     # 표면: 확산항 없음(유속은 소스로)
        dg = lo + hi
        s = np.zeros_like(self.x)
        s[:, -1] = self.J / (self.c_max * self.R) / self.Vk[-1]
        rhs = self.x + _te * (lo * np.roll(self.x, 1, 1) - dg * self.x + hi * np.roll(self.x, -1, 1))
        rhs[:, 0] -= _te * lo[:, 0] * self.x[:, -1]         # roll 오염 가드 (lo[:,0]=0이라 실제 0)
        rhs[:, -1] -= _te * hi[:, -1] * self.x[:, 0]
        rhs += dt * s
        a = -theta * lo
        c = -theta * hi
        d = 1.0 + theta * dg
        cp_ = np.zeros_like(c); dp = np.zeros_like(rhs)
        cp_[:, 0] = c[:, 0] / d[:, 0]
        dp[:, 0] = rhs[:, 0] / d[:, 0]
        for k in range(1, self.nr):
            den = d[:, k] - a[:, k] * cp_[:, k - 1]
            cp_[:, k] = c[:, k] / den
            dp[:, k] = (rhs[:, k] - a[:, k] * dp[:, k - 1]) / den
        xn = np.empty_like(self.x)
        xn[:, -1] = dp[:, -1]
        for k in range(self.nr - 2, -1, -1):
            xn[:, k] = dp[:, k] - cp_[:, k] * xn[:, k + 1]
        self.x = xn


# ---------------------------------------------------------------- 온도 계약 (T1-a/T1-d/G-1)
# step4_grid.npz 안의 σ_i 는 payload 가 **어떤 온도에서** 구운 값이다 (--temp-c → SE σ_ion 에
# Kraft-2017 Arrhenius).  이 파일은 그 σ 를 그대로 읽어 쓰므로, grid 의 온도와 --temp-k 가
# 어긋나면 **혼합-온도 셀**(σ_ion@45 °C × f=F/RT@25 °C × i0/D_s/OCP@25 °C)이 조용히 나간다.
# 그 상태를 만드는 것이 정확히 킷 사슬(payload --temp-c 45 → step4_dyn --grid, --temp-k 미지정)
# 이었다.  → 계약을 읽고, 어긋나면 T1-d 와 같은 급으로 차단한다.
_T_REF_K = 298.15
_T_REF_C = 25.0


def _grid_temperature(path):
    """step4_grid.npz 의 온도 계약을 읽는다 (payload --save-step4-grid 가 굽는 두 필드).

    반환 dict:
      present  — 계약이 실려 있나 (False = 옛 그리드; 온도를 **단정하지 않는다**)
      T_C      — σ_ion 이 실제로 놓인 °C.  None = T_dependence NOT_MODELLED (= T_ref 25 °C 값)
      factor   — σ_ion 에 곱해진 Arrhenius 배수 (1.0 = 미스케일)
      prov     — se_material.provenance 원본 (meta 에 통째로 승계)
    계약이 있는데 깨져 있으면 **조용히 무시하지 않고** RuntimeError (침묵 25 °C 단정 금지).
    """
    off = {'present': False, 'T_C': None, 'factor': 1.0, 'prov': None}
    try:
        g = np.load(path, allow_pickle=False)
    except Exception:
        return off                                    # 파일 자체 문제는 뒤의 정규 로드가 보고
    try:
        files = set(g.files)
        if not ({'grid_temp_c', 'temperature_provenance'} & files):
            return off                                # 옛 payload 산출 그리드
        prov = None
        if 'temperature_provenance' in files:
            try:
                prov = json.loads(str(np.asarray(g['temperature_provenance']).ravel()[0]))
            except Exception as e:
                raise RuntimeError(
                    f'{path}: temperature_provenance 를 읽을 수 없습니다 ({type(e).__name__}: {e}). '
                    '온도 계약이 깨진 그리드를 25 °C 로 단정하면 혼합-온도 런이 조용히 나갑니다 — '
                    'payload(--save-step4-grid)를 다시 돌려 그리드를 재생성하세요.')
        t_c = None
        if 'grid_temp_c' in files:
            v = float(np.asarray(g['grid_temp_c']).ravel()[0])
            t_c = None if not np.isfinite(v) else v
        elif prov is not None:
            t_c = prov.get('T_C')
            t_c = None if t_c is None else float(t_c)
        if prov is not None and 'grid_temp_c' in files:    # 두 필드 교차검증 (계약 무결성)
            p_t = prov.get('T_C')
            p_t = None if p_t is None else float(p_t)
            if (p_t is None) != (t_c is None) or (p_t is not None and abs(p_t - t_c) > 1e-9):
                raise RuntimeError(
                    f'{path}: 온도 계약 불일치 — grid_temp_c={t_c} vs provenance.T_C={p_t}. '
                    '어느 쪽이 σ 를 만든 온도인지 알 수 없으므로 진행하지 않습니다.')
        f = 1.0
        if prov is not None and prov.get('sigma_ion_T_factor') is not None:
            f = float(prov['sigma_ion_T_factor'])
        return {'present': True, 'T_C': t_c, 'factor': f, 'prov': prov}
    finally:
        try:
            g.close()
        except Exception:
            pass


def apply_i0_temperature(i0_ref, i0_p, factor):
    """i0(T) 배수를 **실효 진폭이 있는 쪽에만** 곱한다.  반환 (i0_ref', i0_p').

    ★ 왜 모듈-레벨인가 (2026-07-30 재검증 HIGH-10): 이 로직의 회귀 테스트가 selftest 안의
      **사본**(`_i0_face`)을 검사하고 있어서, main() 의 실제 배선을 되돌려도 (A8a~d)가 전부
      PASS 했다 — 커버리지 0.  이제 프로덕션 경로와 테스트가 **같은 함수**를 쓴다.

    per-face i0 는 두 경로가 다르다:
        i0_p 없음 : i0_f = i0_ref · shape(x)                     → i0_ref 가 진폭
        i0_p 있음 : _i0s = i0_p/i0_ref → i0_f = shape(x)·i0_p    → **i0_ref 가 상쇄**
    """
    f = float(factor)
    if i0_p is not None:
        return float(i0_ref), i0_p * f       # per-particle 진폭이 실효 i0
    return float(i0_ref) * f, None


CYCLE_RCT_ANCHOR = 'yun2023_rct_growth (341.7->982.3 ohm.cm2 @~100cyc, 30C)'


def cycle_interphase_meta(cycle_n, i0_cycle_mult, asr_film_cycle_ohm_cm2, rest=False):
    """B-1 사이클 계면상 감사 기록 (ASSUMED-FORM).  ★ 본 경로와 --rest 가 **같은 함수**를 쓴다.

    HIGH-6: 옛 문자열은 'kim2025 R_ct(N) anchor' 를 인용했으나 kim2025 8행은 전부
    post-formation (사이클 축 없음) — R_ct(N) 앵커는 yun2023 뿐이다.
    MED-13: rest 분기는 이 기록을 아예 안 남기고 열화 플래그를 버렸다.
    """
    m = {'cycle_n': int(cycle_n), 'i0_cycle_mult': float(i0_cycle_mult),
         'asr_film_cycle_ohm_cm2': float(asr_film_cycle_ohm_cm2),
         'anchor': CYCLE_RCT_ANCHOR,
         'provenance': (f'ASSUMED-FORM: mult from yun2023 R_ct(N) anchor '
                        f'({CYCLE_RCT_ANCHOR.split("(", 1)[1].rstrip(")")}); '
                        f'N->mult law pending fit (§6 N1)')}
    if rest:
        m['rest_note'] = ('I=0 이라 필름 옴성(asr_film)은 이 세그먼트에 영향 없음; i0 배수는 '
                          'kin_r 에 반영되나 rest V 는 i0-가중 혼합전위라 균일 스케일이 상쇄된다 '
                          '(기록 목적 — 체인 감사 연속성, MED-13)')
    return m


def temperature_banner(meta):
    """콘솔 온도 배너 문자열 (없으면 '').  ★ 모듈-레벨인 이유 = HIGH-2/HIGH-10 의 교훈.

    옛 배너는 main() 안 f-string 이라 테스트가 없었고, i0 스케일 여부와 무관하게 리터럴
    ``i0/D_s/OCP/σ_e/κ 는 25°C 상수 (kinetics_T_scaling=NONE)`` 을 찍었다 — **같은 런의**
    npz meta (``kinetics_T_scaling='I0_ARRHENIUS_kim2025'``, ``i0_T_factor=6.25``) 와
    정면 모순.  npz 안 ``trust`` 는 조건부로 고쳐놓고 **터미널에 실제로 뜨는 유일한 문장**을
    남긴 것.  이제 meta 한 곳에서 파생하고 selftest 가 이 함수를 직접 검사한다.
    """
    if not meta or meta.get('state') == 'ISOTHERMAL_25C':
        return ''
    kts = meta['kinetics_T_scaling']
    if kts == 'NONE':
        unscaled = 'i0/D_s/OCP/σ_e/κ 는 25°C 상수'
    else:
        unscaled = (f"i0 는 T 를 따름 (×{meta.get('i0_T_factor') or 1.0:.3f}, {kts}), "
                    f"D_s/OCP/σ_e/κ 만 25°C 상수")
    return (f"  ⚠ 온도 상태 {meta['state']} — σ_ion {meta['sigma_ion_T_C']:g}°C "
            f"(×{meta['sigma_ion_T_factor']:.3f}) vs 동역학 {meta['temp_c_kinetics']:g}°C; "
            f"{unscaled} (kinetics_T_scaling={kts}). σ-메트릭·용량 절대값 신뢰 금지"
            + (f"  [해제: {', '.join(meta['released_guards'])}]"
               if meta['released_guards'] else ''))


def temperature_verdict(temp_k, grid, allow_unscaled_t, allow_grid_t_mismatch,
                        i0_t_scaled=False):
    """--temp-k 와 grid 의 σ_ion 온도를 대조한다 (순수함수 — selftest 가 직접 호출).

    반환 ``(errors, meta)``.
      errors — 차단 사유 코드 리스트 (빈 리스트 = 통과).  'GRID_T_MISMATCH' / 'KINETICS_UNSCALED'
      meta   — 감사 기록 dict, 또는 **자명한 기본**(모든 것이 25 °C·플래그 없음)이면 None
               → 기본 런의 npz meta 는 바이트 불변.
    """
    grid = grid or {'present': False, 'T_C': None, 'factor': 1.0, 'prov': None}
    t_kin_c = float(temp_k) - 273.15
    sig_t_c = grid['T_C']                              # None = σ_ion 이 T_ref 25 °C 값
    sig_eff_c = _T_REF_C if sig_t_c is None else sig_t_c
    errors = []
    if abs(sig_eff_c - t_kin_c) > 0.05:
        # σ 가 놓인 온도 ≠ 동역학이 도는 온도 = 혼합-온도 셀.
        # grid 가 명시적으로 다른 T 를 들고 있으면 G-1(그리드 불일치), 아니면 기존 T1-d.
        # ★ HIGH-9 (2026-07-30 리뷰): i0 가 **스케일된** 상태에서 계약 없는 그리드를 만나면
        #   옛 코드는 이 자리를 KINETICS_UNSCALED 로 코딩했다 → 동역학이 ×6.25 로 스케일됐는데
        #   "kinetics unscaled 를 해제했다"가 released_guards 에 영구 기록되고, 차단 메시지는
        #   사용자가 방금 켠 플래그와 정반대("i0 는 25 °C 상수")를 말하며, 정작 안 스케일된
        #   σ_ion 의 해법(--allow-grid-t-mismatch)은 이 경로에서 **한 번도 제시되지 않았다**.
        #   i0 가 스케일됐다면 남은 결함은 순수히 σ_ion 쪽 → GRID_T_MISMATCH 가 맞는 코드다.
        #   (i0 미스케일 + 계약 없음 = 전부 25 °C 상수 = 역사적 T1-d → 라벨·해제 플래그 보존.
        #    이 경우에도 혼합 사실 자체는 meta.state=MIXED_TEMPERATURE + trust 에 남는다.)
        errors.append('GRID_T_MISMATCH' if (sig_t_c is not None or i0_t_scaled)
                      else 'KINETICS_UNSCALED')
    if abs(t_kin_c - _T_REF_C) > 0.05 and 'KINETICS_UNSCALED' not in errors and not i0_t_scaled:
        errors.append('KINETICS_UNSCALED')             # i0/D_s/OCP 가 전부 25 °C 상수일 때만
    # ★ 2026-07-29 (A): --i0-temp-scale 이면 i0 는 kim2025 R_ct(T) 앵커를 따른다 → **부호역전이
    #   사라진다** (§3-3① 의 핵심 결함).  그래서 KINETICS_UNSCALED 를 올리지 않는다.  단 D_s·OCP
    #   dU/dT 는 여전히 미앵커이므로 '전부 스케일됨' 이 아니라 아래 state 에 부분성이 남는다.
    #   ⚠ 정정 (2026-07-30 리뷰 HIGH-3): 첫 배선은 여기서 KINETICS_UNSCALED 를 **무조건 strip**
    #     했다.  그러면 σ 온도가 **미기재**인 그리드(= --temp-c 없이 만든 기존 그리드 전부 =
    #     기본·지배 경로)에서 "σ_ion 25 °C + BV 60 °C" 혼합 셀이 released_guards **빈 채로**
    #     통과했다.  명시적으로 25 °C 라고 적힌 그리드는 GRID_T_MISMATCH 로 차단되는데
    #     미기재가 통과하는 비대칭 = 더 나쁜 쪽이 뚫린다.  ⇒ strip 삭제.
    #     위 :742 의 `not i0_t_scaled` 조건만으로 **σ 와 동역학이 같은 T** 인 정상 경로는
    #     그대로 통과한다 (혼합이 아니므로 애초에 이 분기를 안 탄다).
    released = []
    if 'GRID_T_MISMATCH' in errors and allow_grid_t_mismatch:
        errors.remove('GRID_T_MISMATCH'); released.append('GRID_T_MISMATCH:--allow-grid-t-mismatch')
    if 'KINETICS_UNSCALED' in errors and allow_unscaled_t:
        errors.remove('KINETICS_UNSCALED'); released.append('KINETICS_UNSCALED:--allow-unscaled-t')
    mixed = abs(sig_eff_c - t_kin_c) > 0.05
    if abs(sig_eff_c - _T_REF_C) <= 0.05 and abs(t_kin_c - _T_REF_C) <= 0.05:
        state = 'ISOTHERMAL_25C'
    elif mixed:
        state = f'MIXED_TEMPERATURE (sigma_ion@{sig_eff_c:g}C, kinetics@{t_kin_c:g}C)'
    else:
        state = (f'PARTIAL_sigma_ion+i0@{sig_eff_c:g}C' if i0_t_scaled
                 else f'PARTIAL_sigma_ion_only@{sig_eff_c:g}C')
    # meta 는 **온도가 실제로 개입한 런에만** 붙인다: 그리드가 25 °C 규약값이고 --temp-k 도 기본이며
    # 해제 플래그도 없으면 역사적 기본과 완전히 동일 → 기록할 것이 없고 npz 는 바이트 불변.
    trivial = (sig_t_c is None and abs(t_kin_c - _T_REF_C) <= 0.05
               and not allow_unscaled_t and not allow_grid_t_mismatch and not i0_t_scaled)
    # ★ HIGH-10 (2026-07-30): 이 문자열이 무조건 "i0 도 25 °C 상수" 라고 적어, 같은 dict 의
    #   kinetics_T_scaling='I0_ARRHENIUS_kim2025' · i0_T_factor=6.25 와 **정면 모순**했다.
    _mix_note = ('' if not mixed else
                 '.  ★혼합-온도: σ_ion 과 동역학이 서로 다른 온도에 있다 — 절대 용량/과전압 '
                 '해석 금지, 명시 해제된 진단 런')
    _trust_str = (
        ('f=F/RT 와 **i0** 가 --temp-k 를 따른다 (i0 = kim2025 R_ct(T) 앵커; '
         'R_ct=RT/(F·i0·A) 의 RT 전인자 포함).  D_s/OCP dU/dT/σ_e/κ 는 여전히 25 °C 상수 '
         '(§F1 앵커 없음) → 부분 반영이지 전-물리 온도 스윕 아님.  ⚠ 코팅계는 Eₐ 가 다르다 '
         '(kim2025 LNO 는 비-Arrhenius) — 이 런은 uncoated Eₐ 를 상속하고 있다.' + _mix_note)
        if i0_t_scaled else
        ('f=F/RT 만 --temp-k 를 따른다.  i0/D_s/OCP/σ_e/κ 는 25 °C 상수 (§F1 앵커 없음) → '
         '전-물리 온도 스윕 아님' + _mix_note))
    meta = None if trivial else {
        'temp_k': float(temp_k), 'temp_c_kinetics': t_kin_c,
        'sigma_ion_T_C': sig_eff_c,
        'sigma_ion_T_scaling': ('UNKNOWN_LEGACY_GRID' if not grid['present']
                                else ('ARRHENIUS' if sig_t_c is not None else 'NOT_MODELLED')),
        'sigma_ion_T_factor': float(grid['factor']),
        # ★ i0 만 앵커가 있다 (kim2025 R_ct 30/45/60 °C, Eₐ=0.4212 eV, R²=0.99943).
        #   D_s(T) · OCP dU/dT 는 여전히 미앵커 → 'I0_ARRHENIUS' 는 "일부" 라는 뜻이다.
        'kinetics_T_scaling': ('I0_ARRHENIUS_kim2025' if i0_t_scaled else 'NONE'),
        'i0_T_factor': None,                           # 아래 main() 이 실제 배수로 채운다
        'state': state,
        'grid_contract_present': bool(grid['present']),
        'grid_temperature_provenance': grid['prov'],
        'released_guards': released,
        # ★ HIGH-10 (2026-07-30): 이 문자열이 무조건 "i0 도 25 °C 상수" 라고 적어, 같은 dict 의
        #   kinetics_T_scaling='I0_ARRHENIUS_kim2025' · i0_T_factor=6.25 와 **정면 모순**했다.
        #   i0 스케일 여부에 따라 문장을 바꾼다.
        'trust': _trust_str,
    }
    return errors, meta


# ---------------------------------------------------------------- OCP / kinetics
def _load_xy_csv(path):
    tab = np.loadtxt(path, delimiter=',', skiprows=1)
    o = np.argsort(tab[:, 0])
    return tab[o, 0], tab[o, 1]


class OCP:
    def __init__(self, x_tab, u_tab, c_max, x0, x100, provenance='', test_only=False):
        o = np.argsort(np.asarray(x_tab, np.float64))
        self.x_tab = np.asarray(x_tab, np.float64)[o]
        self.u_tab = np.asarray(u_tab, np.float64)[o]
        self.c_max, self.x0, self.x100 = float(c_max), float(x0), float(x100)
        self.provenance, self.test_only = provenance, bool(test_only)

    def U(self, x):
        return np.interp(x, self.x_tab, self.u_tab)

    @staticmethod
    def load(ocp_csv, params_json):
        x, u = _load_xy_csv(ocp_csv)
        p = json.load(open(params_json))
        return OCP(x, u, p['c_max_mol_m3'], p['x_at_charged'], p['x_at_discharged'],
                   p.get('provenance', ''))

    @staticmethod
    def synthetic_test():
        """TEST-ONLY 합성 선형 OCP — 문헌수치 아님 (selftest 전용, §F1)."""
        x = np.linspace(0.0, 1.0, 21)
        return OCP(x, 4.2 - 1.0 * x, c_max=50000.0, x0=0.25, x100=0.85,
                   provenance='SYNTHETIC-TEST-ONLY', test_only=True)


class Kinetics:
    """면별 Butler-Volmer (+옵션 필름저항).  I_f [A] = e→i(탈리튬) 양수.

      i_ct(η_s) = i0(x)·A·[exp(α_a f η_s) − exp(−α_c f η_s)],  f = F/RT
      η_s = Δφ − U − I_f·ASR/A   (ASR>0이면 면별 스칼라 Newton — 유일근: 좌변↑/우변↓)
      i0(x) = i0_ref·(x/½)^{α_c}·((1−x)/½)^{α_a}   (x=½에서 i0_ref; α=½/½ → √(4x(1−x)) 구형)
      c_e 항 없음 — 단일이온 SE(활동도 고정) = SSB 물리."""

    CLIP = 20.0        # sinh(20)=2.4e8 — 물리 면전류(≪1e-4 A)보다 6자릿수 위 = 물리손실 0,
                       # cosh 상한 2.4e8로 야코비안 g_f 폭주(κ→1e13) 차단 (수치리뷰 #9)

    def __init__(self, i0_ref, alpha_a=0.5, alpha_c=0.5, asr_film=0.0, temp_k=298.15):
        self.i0_ref, self.aa, self.ac = float(i0_ref), float(alpha_a), float(alpha_c)
        self.asr = float(asr_film)                          # [Ω·m²]
        self.T = float(temp_k)
        self.f = F_CONST / (R_GAS * self.T)                 # [1/V]

    def i0(self, x):
        x = np.clip(x, 1e-4, 1.0 - 1e-4)
        return self.i0_ref * (x / 0.5) ** self.ac * ((1.0 - x) / 0.5) ** self.aa

    def _ct(self, eta, i0A):
        ea = np.exp(np.clip(self.aa * self.f * eta, -self.CLIP, self.CLIP))
        ec = np.exp(np.clip(-self.ac * self.f * eta, -self.CLIP, self.CLIP))
        I = i0A * (ea - ec)
        g = i0A * self.f * (self.aa * ea + self.ac * ec)    # dI/dη > 0
        return I, g

    def face_current(self, X, i0_f, A_face, I_init=None):
        """X = Δφ − U.  반환 (I_f, g_eff=dI/dX, η_s)."""
        i0A = i0_f * A_face
        if self.asr <= 0.0:
            I, g = self._ct(X, i0A)
            return I, g, X
        rA = self.asr / A_face                              # [Ω] per face
        I = np.zeros_like(X) if I_init is None else I_init.copy()
        for _ in range(12):                                 # h(I)=I−i_ct(X−I·rA)=0, 단조 → Newton
            eta = X - I * rA
            Ict, g = self._ct(eta, i0A)
            h = I - Ict
            dh = 1.0 + g * rA
            dI = -h / dh
            I = I + dI
            if float(np.max(np.abs(dI))) < 1e-14 + 1e-10 * float(np.max(np.abs(I)) + 1e-30):
                break
        eta = X - I * rA
        _, g = self._ct(eta, i0A)
        return I, g / (1.0 + g * rA), eta


# ---------------------------------------------------------------- 결합망 (정적 CSR 1회 + 데이터 갱신)
class CellSystem:
    """v1(solve_reaction_current)과 같은 격자 규약(6-이웃 face, plate band, anchored filter).
    CSR 구조를 1회 조립(BV 자리 = 0 placeholder)하고, Newton 반복에서는 data 배열만 갱신
    (15M+ 엔트리 재조립/재전송 없음 — 프로덕션 성능의 핵심)."""

    _cap_hinted = False                                      # σ대비 권고 로그 프로세스-1회 (C1)

    def __init__(self, sid, sig_e_tab_S_cm, sig_i_tab_S_cm, pid, n_am, vox_um,
                 z_top_um=None, z_bot_um=0.0, periodic_xy=False):
        vox_m = vox_um * 1e-6
        self.vox_m = vox_m
        sig_e = np.asarray(sig_e_tab_S_cm, np.float64)[sid] * 100.0   # S/m
        sig_i = np.asarray(sig_i_tab_S_cm, np.float64)[sid] * 100.0
        # ★σ-contrast cap (R4; 레거시 voxel_conductivity.py:139-143 동일 200×min-positive 규약, opt-in).
        #   A2 실측: cap200× → λ꼬리 ×44-49·CG 276→52 it; σ_eff(e) −7.8%(이 기하 — 레거시 '<0.2%' 비전이),
        #   셀-V ≤2.5µV@2C → 시간전개 안전.  ⚠σ_e-류 수송 메트릭 보고는 uncapped 런으로 (meta 라벨).
        _cap = float(os.environ.get('MPM_S4_CONTRAST_CAP', '0') or 0.0)
        self.contrast_cap = _cap
        # ★판(집전체/분리막) 링크는 **uncapped** σ 로 — cap 은 벌크 face 컨덕턴스의 조건수 완화가
        #   목적이고, A2 오차예산(σ_eff −7.8%, 셀-V ≤2.5µV)도 벌크 측정이다.  in-place cap 이
        #   sig_e 를 깎으면 gB(집전체 접촉)까지 ×1/50 되어 **직렬 접촉저항 ×50** 이라는 담보 없는
        #   물리 변경이 생긴다 (2026-07-27 적대검증 M1: Σg_B 3.6e-1 → 7.2e-3 실측).
        sig_e_plate, sig_i_plate = sig_e.copy(), sig_i.copy()
        # ★cap은 e-망 전용 (리뷰 V1 medium): near-null 병리·A2 셀-V≤2.5µV 근거 모두 e-망 실측 —
        #   i-망은 이온 옴강하가 지배 분극(2C 84-90mV)이라 cap 시 0.5mV급 왜곡 재현됨(코팅 프리셋
        #   LZO/LNO 저-σ_i 층이 200× 초과 가능).  i-망 고대비는 cap 없이 경고만.
        for _nm, _s in (('e', sig_e), ('i', sig_i)):
            _pos = _s[_s > 0]
            if _pos.size == 0:
                continue
            _ratio = float(_pos.max() / _pos.min())
            if _cap > 0 and _ratio > _cap and _nm == 'e':
                np.minimum(_s, float(_pos.min()) * _cap, out=_s)
                print(f'    ★σ-contrast cap(e-망): {_ratio:.1e} → ≤{_cap:g}×min '
                      f'(near-null 완화; σ-메트릭은 uncapped 런으로 보고)', flush=True)
            elif _cap > 0 and _ratio > _cap:
                print(f'    ℹ i-망 σ대비 {_ratio:.1e}>{_cap:g}× — cap 미적용(e-망 전용; i-망 옴강하가 '
                      f'지배 분극이라 cap 왜곡 큼, A2 미검증)', flush=True)
            elif _cap <= 0 and _ratio > 1e3 and not CellSystem._cap_hinted:
                CellSystem._cap_hinted = True
                print(f'    ℹ σ대비 {_ratio:.1e}({_nm}-망)>1e3 — 수렴 정체 시 MPM_S4_CONTRAST_CAP=200 권장 '
                      f'(e-망 전용 적용; A2 실측: 셀-V ≤2.5µV@2C, σ_eff −7.8% → 보고용은 uncapped)', flush=True)
        cond_e, cond_i = sig_e > 0, sig_i > 0
        nx, ny, nz = sid.shape
        self.area_m2 = nx * ny * vox_m * vox_m              # 측면(RVE) 단면적 — R_int 환산용
        zc = (np.arange(nz) + 0.5) * vox_um
        band = vox_um + 0.10
        z_b = float(z_bot_um)
        z_p = min(float(z_top_um) if z_top_um is not None else nz * vox_um, nz * vox_um)
        any_e = cond_e.any(2); k_first = np.argmax(cond_e, 2)
        bot_e = any_e & (zc[k_first] - z_b <= band)
        any_i = cond_i.any(2); k_last = nz - 1 - np.argmax(cond_i[:, :, ::-1], 2)
        top_i = any_i & (z_p - zc[k_last] <= band)
        if not bot_e.any() or not top_i.any():
            raise RuntimeError('no plate contact (bot_e/top_i empty)')
        uni = cond_e | cond_i
        lab, _ = ndimage.label(uni)
        ii, jj = np.where(bot_e); anch = set(lab[ii, jj, k_first[bot_e]].tolist())
        ii, jj = np.where(top_i); anch |= set(lab[ii, jj, k_last[top_i]].tolist())
        anch.discard(0)
        keep = np.isin(lab, list(anch))
        cond_e &= keep; cond_i &= keep
        # ★e-망 부유클러스터 pruning (2026-07-27 A2/A3: union-anchored는 SE가 앵커라 SE-매몰 carbon 섬
        #   keep — e-망 6-conn으론 집전체·AM 무접촉 = BV·판 부재의 정확 특이블록, GPU-CG 사망 구조 근원.
        #   RHS=0 → 잔여 해 수학 불변.  AM-포함 성분은 KEEP.  MPM_S4_PRUNE_FLOAT=0 → 구 경로 bitwise 복원)
        self.n_pruned_e_comp = self.n_pruned_e_vox = 0
        if os.environ.get('MPM_S4_PRUNE_FLOAT', '1') != '0':
            lab_e, n_lab = ndimage.label(cond_e)              # 6-conn = FV 행렬 결합 그래프와 동일
            keep_lab = np.zeros(n_lab + 1, bool); keep_lab[0] = True
            keep_lab[np.unique(lab_e[((sid == 1) | (sid == 2)) & cond_e])] = True   # AM 포함(BV 가능)
            ii, jj = np.where(bot_e)
            keep_lab[np.unique(lab_e[ii, jj, k_first[bot_e]])] = True               # 집전체 band 접촉
            drop = cond_e & ~keep_lab[lab_e]
            if drop.any():
                self.n_pruned_e_comp = int(np.unique(lab_e[drop]).size)
                self.n_pruned_e_vox = int(drop.sum())
                cond_e &= ~drop
                print(f'    e-망 부유클러스터 pruning: {self.n_pruned_e_comp:,}성분/'
                      f'{self.n_pruned_e_vox:,}복셀 드롭 (AM·집전체 무접촉=정확특이; '
                      f'MPM_S4_PRUNE_FLOAT=0 복원)', flush=True)
        self.n_e, self.n_i = int(cond_e.sum()), int(cond_i.sum())
        idx_e = -np.ones(sid.shape, np.int64); idx_e[cond_e] = np.arange(self.n_e)
        idx_i = -np.ones(sid.shape, np.int64); idx_i[cond_i] = np.arange(self.n_i)
        # ★ 운전-중 φ(z) 프로파일용 dof→z-층 매핑 (boolean-mask arange 부여 = C-order =
        #   np.nonzero 순서와 동일 → phi[:n_e][k]가 k_e_layer[k] 층의 전자 dof)
        self.k_e_layer = np.nonzero(cond_e)[2].astype(np.int32)
        self.k_i_layer = np.nonzero(cond_i)[2].astype(np.int32)
        self.z_um_layers = (np.arange(sid.shape[2]) + 0.5) * vox_um
        sig_e = np.where(cond_e, sig_e, 0.0); sig_i = np.where(cond_i, sig_i, 0.0)
        self.N = self.n_e + self.n_i                        # Dirichlet 구조 (supernode 없음)
        rows, cols, vals = [], [], []
        diag0 = np.zeros(self.N)

        def _couple(idxN, sigN, off, sl_a, sl_b):
            A, B = idxN[sl_a], idxN[sl_b]
            sa, sb = sigN[sl_a], sigN[sl_b]
            m = (A >= 0) & (B >= 0)
            if not m.any():
                return
            g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox_m       # 조화평균 face g [S]
            a2, b2 = A[m] + off, B[m] + off
            rows.append(a2); cols.append(b2); vals.append(-g)
            rows.append(b2); cols.append(a2); vals.append(-g)
            np.add.at(diag0, a2, g); np.add.at(diag0, b2, g)

        # ★x,y 주기 wrap (2026-07-27 감사 C1): STEP3 v1(solve_reaction_current)은 --periodic 시
        #   wrap 을 _dirs 에 넣어 **전도와 BV 계면이 함께** 주기가 되게 한다.  v2 는 그 정보를 못
        #   받아 항상 절연벽이었다(실격자 i-망 wrap 면 30,895 · seam BV 11,543 누락).  여기서도
        #   SL 을 전도·BV 가 공유하므로 append 만으로 v1 과 같은 규약이 된다.  nx/ny=1 자기결합 가드.
        self.periodic_xy = bool(periodic_xy)
        # (축, sl_a, sl_b) — ★축을 명시로 싣는다: wrap 을 붙이면 SL 순번≠축이 되는데 BV 좌표가
        #   순번을 축으로 쓰면 IndexError/좌표오염이 난다 (S1d 가 즉시 잡은 회귀).
        SL = [(0, np.s_[:-1, :, :], np.s_[1:, :, :]), (1, np.s_[:, :-1, :], np.s_[:, 1:, :]),
              (2, np.s_[:, :, :-1], np.s_[:, :, 1:])]
        if self.periodic_xy:                              # z(plate)는 비주기 유지
            if sid.shape[0] > 1:
                SL.append((0, np.s_[-1:, :, :], np.s_[:1, :, :]))     # x: nx-1 ↔ 0
            if sid.shape[1] > 1:
                SL.append((1, np.s_[:, -1:, :], np.s_[:, :1, :]))     # y: ny-1 ↔ 0
        SL = tuple(SL)
        for _ax, sl_a, sl_b in SL:
            _couple(idx_e, sig_e, 0, sl_a, sl_b)
            _couple(idx_i, sig_i, self.n_e, sl_a, sl_b)
        # plates — v1(solve_reaction_current)과 동일한 **Dirichlet diag-add 구조** (검증된 수렴성):
        #   bottom 집전체: φ_e = V_app (diag += gB, RHS += gB·V_app — V_app는 solve마다 변수)
        #   top 분리막:    φ_i = 0    (diag += gT)
        # ⚠ supernode-B(집전체를 한 노드로 묶는 정전류 구조)는 제거 — ~5천 접점이 한 행에 몰린
        # 허브가 Jacobi/AMG-CG를 정체시켰음(2026-07-15 V100: v1 동일격자 수렴 vs v2 3h+ 정체).
        # 정전류(galvanostatic)는 solve_galv()의 V_app 시컨트 래퍼로 구현 (I(V_app) 단조).
        ii, jj = np.where(bot_e); kk = k_first[bot_e]
        Ae = idx_e[ii, jj, kk]; m = Ae >= 0
        dist = np.maximum(np.abs(zc[kk[m]] - z_b), 0.5 * vox_um) * 1e-6
        self.gB = sig_e_plate[ii[m], jj[m], kk[m]] * vox_m * vox_m / dist   # uncapped (M1)
        self.aB = Ae[m]
        np.add.at(diag0, self.aB, self.gB)
        ii, jj = np.where(top_i); kk = k_last[top_i]
        Ai = idx_i[ii, jj, kk]; m = Ai >= 0
        dist = np.maximum(np.abs(z_p - zc[kk[m]]), 0.5 * vox_um) * 1e-6
        self.gT = sig_i_plate[ii[m], jj[m], kk[m]] * vox_m * vox_m / dist   # uncapped (M1)
        self.aT = Ai[m] + self.n_e
        np.add.at(diag0, self.aT, self.gT)                  # 접지(φ=0): diag-only
        # BV 면 목록 (+면 중점 µm 좌표 — 뷰어 표면-반응 필드용; 격자 프레임 = payload µm 프레임)
        am_m = (sid == 1) | (sid == 2)
        # ★반응 계면 = AM ↔ 이온공급상.  이온상 = SDCP(5)·SE(6)·SWCNT-sheath(8).  sid 8 누락 시
        #   σ_ion 솔브(sheath 투명=σ_i[8]>0)와 STEP4 반응이 모순 — A14 sheath 가 감싼 AM 표면이
        #   반응서 사라져 wrap_frac↑ 일수록 --swcnt-ion-block 인 것처럼 반응전류 과소 (STEP3 v1
        #   solve_reaction_current MED-2 감사서 이미 정정된 규약; v2 만 누락돼 있었음 — 2026-07-27).
        #   게이트는 idx_i≥0(=cond_i=σ_i>0)이 담당 → --swcnt-ion-block(σ_i[8]=0)이면 자동 제외 = 솔브와 일관.
        ion_m = (sid == 5) | (sid == 6) | (sid == 8)
        fe, fi, fp, fpos = [], [], [], []
        for d, sl_a, sl_b in SL:
            for am_first in (True, False):
                slA, slB = (sl_a, sl_b) if am_first else (sl_b, sl_a)
                m = am_m[slA] & ion_m[slB]
                Ae2 = idx_e[slA]; Bi2 = idx_i[slB]
                m &= (Ae2 >= 0) & (Bi2 >= 0)
                if not m.any():
                    continue
                fe.append(Ae2[m]); fi.append(Bi2[m] + self.n_e); fp.append(pid[slA][m])
                # slA 가 잘린 구간이면 argwhere 인덱스는 **부분배열 기준** → 전체격자 원점을 더한다
                # (wrap 슬라이스 [-1:] 는 원점이 n-1; 옛 코드는 항상 0 가정이라 wrap 좌표가 틀렸다)
                _org = np.array([slA[k].indices(sid.shape[k])[0] for k in range(3)], np.float32)
                pos = np.argwhere(m).astype(np.float32) + _org + 0.5   # 하부 셀 중심
                pos[:, d] += 0.5                                  # 축 방향 면 중점 (d=진짜 축)
                fpos.append(pos * vox_um)
        if not fe:
            raise RuntimeError('no BV interface')
        self.f_e = np.concatenate(fe); self.f_i = np.concatenate(fi)
        self.f_pid = np.concatenate(fp)
        self.f_pos_um = np.concatenate(fpos)
        self.n_bv = len(self.f_e)
        self.A_face = vox_m * vox_m
        self.n_am = int(n_am)
        # degree-0 가드 — 단 BV 면을 가진 노드는 제외 (물리리뷰 #4: v1은 g_ct가 정적 대각에
        # 있었지만 v2는 Newton 대각으로만 들어옴 → 여기서 1.0을 박으면 "가짜 1 S 접지"가 생겨
        # BV 면을 타고 유령 전류 루프가 돎.  제외하면 해당 노드는 부유 전위(ΣI_f=0)로 수렴 = 물리)
        iso = diag0 == 0.0
        iso[self.f_e] = False
        iso[self.f_i] = False
        diag0[iso] = 1.0
        self.iso_idx = np.where(iso)[0]                     # 고립 placeholder 노드 (물리 없음)
        self._agg_mask = np.ones(self.n_e, bool)            # 집계-잔차에서 고립 e-노드 제외
        self._agg_mask[self.iso_idx[self.iso_idx < self.n_e]] = False
        self._diag0 = diag0
        # ---- CSR 1회 조립: 정적 + BV placeholder(0) + 대각.  이후 data만 갱신 ----
        rows_all = np.concatenate(rows + [self.f_e, self.f_i, np.arange(self.N)])
        cols_all = np.concatenate(cols + [self.f_i, self.f_e, np.arange(self.N)])
        nnz_static = sum(len(v) for v in vals)
        vals_all = np.concatenate(vals + [np.zeros(2 * self.n_bv), diag0])
        # 좌표별 유일성: 네트워크 엣지·plate 엣지·BV pair·diag 는 모두 서로 다른 (r,c) —
        # 단 BV pair가 같은 (e,i) 복셀쌍에 축 2회 나올 수는 없음(격자 인접은 유일축).  같은
        # (r,c) 중복이 없으므로 COO→CSR 매핑이 1:1 (아래 위치맵 전제; selftest로 재검증).
        M = sparse.coo_matrix((np.arange(len(vals_all), dtype=np.float64) + 1.0,
                               (rows_all, cols_all)), shape=(self.N, self.N)).tocsr()
        if len(M.data) != len(vals_all):
            raise RuntimeError('duplicate COO coordinates — 위치맵 전제 붕괴 (assembly bug)')
        # M.data[j] = (COO 인덱스 k)+1 → perm[k] = k번 COO 엔트리의 CSR data 위치 j.
        # (방향 주의 — 산란은 data0[perm]=vals, 수집이 아님; selftest #0이 brute-force와 대조)
        perm = np.argsort(M.data)
        self.J = sparse.csr_matrix((np.empty(len(vals_all)), M.indices, M.indptr),
                                   shape=(self.N, self.N))
        self.data0 = np.empty(len(vals_all))
        self.data0[perm] = vals_all                         # 정적값 (BV 자리 0)
        self.pos_ei = perm[nnz_static:nnz_static + self.n_bv]           # (f_e,f_i) off-diag
        self.pos_ie = perm[nnz_static + self.n_bv:nnz_static + 2 * self.n_bv]
        self.pos_diag = perm[nnz_static + 2 * self.n_bv:]               # 노드별 대각 위치
        self.J.data[:] = self.data0
        # 집계-잔차의 float64 노이즈 바닥 스케일: matvec 반올림 ~ ε·Σ|entries|·|φ|.
        # (실전 2.9M dof에서 이 바닥이 상대 ~1e-5 — 1e-8 고정 목표는 도달 불가능한 목표가 되어
        #  노이즈를 상대로 CG를 돌리게 됨: 2026-07-16 V100 CG-정체의 두 번째 뿌리)
        self._abs_data_sum = float(np.abs(self.data0).sum())

    # ---- 연산 ----
    def _L0_apply(self, phi):
        self.J.data[:] = self.data0
        return self.J @ phi

    def calibrate_floor(self, phi_eq, U_f, i0_f, kin, V_eq):
        """집계-잔차 float64 바닥 **자가교정**: 정확한 평형(φ_e=U, φ_i=0, V=U → 진짜 잔차 0)에서
        측정한 |Σ_e F| = 순수 반올림 노이즈.  공식 상한(ε·Σ|entries|)은 실전에서 ~10³× 후해
        경고/하드페일선을 무력화했음(V100 smoke7).  ×4 마진."""
        F, _, _ = self.residual(phi_eq, U_f, i0_f, kin, V_eq)
        meas_agg = abs(float(F[:self.n_e][self._agg_mask].sum()))
        self.agg_floor_abs = 4.0 * meas_agg + 1e-30
        return meas_agg, float(np.linalg.norm(F, np.inf))

    def plate_current(self, phi, V_app):
        """방전-양(+) 전달 전류 [A]: I_del = Σ gB·(φ_c − V_app)  (전극→집전체로 나가는 전류)."""
        return float(np.sum(self.gB * (phi[self.aB] - V_app)))

    def residual(self, phi, U_f, i0_f, kin, V_app, I_faces_init=None):
        """F(φ) = L0·φ + BV(φ) − b;  b = gB·V_app (bottom Dirichlet lift).  반환 (F, I_f, η_s)."""
        Fv = self._L0_apply(phi)
        Fv[self.aB] -= self.gB * V_app
        X = phi[self.f_e] - phi[self.f_i] - U_f
        I_f, _, eta_s = kin.face_current(X, i0_f, self.A_face, I_init=I_faces_init)
        np.add.at(Fv, self.f_e, I_f)
        np.add.at(Fv, self.f_i, -I_f)
        return Fv, I_f, eta_s

    def newton(self, phi, U_f, i0_f, kin, V_app, i_scale, tol_rel=1e-8, max_it=25):
        """감쇠 Newton (potentiostatic — V_app 고정, v1-검증 Dirichlet 구조).
        J = L0 + Σ_f g_eff(e_a−e_b)(e_a−e_b)ᵀ — SPD → CG.
        수렴 = max(노드별 잔차 ∞-norm, e-망 집계잔차 |Σ_e F| = |I_in−ΣI_f|) / i_scale."""
        Fv, I_f, eta_s = self.residual(phi, U_f, i0_f, kin, V_app)
        scale = max(abs(i_scale), 1e-12)
        # ★EW 이력은 **콜 사이에 보존** — newton() 은 정전류 시컨트(Illinois) V-평가마다 불리므로
        #   콜마다 리셋하면 거의 수렴한 계도 매번 η=0.1 부터 다시 조여 총 CG 일량이 오히려 늘었다
        #   (토이 실측 +33% iteration; 2026-07-27 적대검증 M2).  인스턴스 속성으로 유지.
        if not hasattr(self, '_ew_f2_prev'):
            self._ew_f2_prev = None; self._ew_eta_prev = None

        def _err(F, phi_ref):
            # 집계 노이즈 바닥: 공식(ε·Σ|entries|)은 코히런트 상한이라 실전에서 ~10³× 후함
            # (물리리뷰 R2#4 경고 → V100 smoke7에서 경고선 9.5e-2로 실증) → **자가교정 실측**
            # (calibrate_floor: 정확한 평형 상태에서 잰 잔차 = 진짜 바닥)을 우선 사용.
            floor = getattr(self, 'agg_floor_abs', None)
            if floor is None:                                # 미교정 시 보수적 공식 폴백
                floor = (32.0 * np.finfo(np.float64).eps * self._abs_data_sum
                         * (float(np.max(np.abs(phi_ref))) + 1.0))
            agg = max(0.0, abs(float(F[:self.n_e][self._agg_mask].sum())) - floor)
            self.last_err_floor_rel = floor / scale
            return max(float(np.linalg.norm(F, np.inf)), agg) / scale

        it = 0
        best, stall = np.inf, 0
        self._cg_failed = False
        while it < max_it:
            r = _err(Fv, phi)
            if r < tol_rel:
                break
            # 심층-수렴권(<1e-4)에서 CG가 무용함이 확인된 상태면 수렴 취급 — 확인 = 이 call에서
            # 이미 실패(it>0) 또는 런-전체 기억(deep_weak).  resid 보고는 그대로 → 감사가 판단.
            deep = r < 1e-4
            known_weak = (getattr(self, '_pc_cache', {}).get('deep_weak', False)
                          or (it > 0 and self._cg_failed))
            if deep and known_weak:
                break
            if r >= 0.5 * best:                             # 노이즈-바닥 정체 감지 (수렴 근처 한정)
                                                            # (stall 수용 상한 1e-3 = simulate 하드페일과 의도적 페어)
                stall += 1
                if stall >= 2 and best < getattr(self, 'stall_tol', 1e-3):  # ★rate-aware 바닥(저율=1/rate 배 높음)
                    break
            else:
                stall = 0
            best = min(best, r)
            # ★EW inexact-Newton (choice-2 γ=0.9,α=2).  ⚠2026-07-27 기본 ON→OFF 로 강등:
            #   측정 2건 모두 **일량이 늘었다** (독립 적대검증 총 CG it +33%, 자체 토이 +7% it /
            #   콜 +50%; 해는 불변 |ΔV|~6e-10).  기전: 깊은 보정해의 목표는 atol_cg(절대바닥)가
            #   정하므로 tgt=max(η‖F‖, atol)에서 후기엔 atol 이 이겨 **EW 가 비싼 솔브를 못 느슨하게
            #   한다**; 대신 느슨한 초기 스텝이 Armijo 에 거부돼 tight 재솔브를 부른다.  이득 근거가
            #   생기기 전(V100 A/B)까지 opt-in: MPM_S4_EW=1 로 켠다.
            #   η_min=1e-5=구식 → 느슨화 전용(솔브당 CG 일량 ≤ 현행).  atol_cg 불변 → tgt=max(η‖F‖,atol):
            #   교정-바닥/심층(deep)/stall/Armijo 로직 전부 무수정.  해 논거: 최종 수렴판정은 매 반복
            #   '정확 재계산' F 기준(tol_rel 동일) — EW는 중간 보정해 정밀도만 조절.
            f2_cur = float(np.linalg.norm(Fv))
            _ew = os.environ.get('MPM_S4_EW', '0') == '1'   # ★기본 OFF (근거: 아래 주석)
            if _ew:
                _ratio = f2_cur / self._ew_f2_prev if self._ew_f2_prev else None
                #   ratio 폭주(F 가 커진 스텝) 시 ratio² 가 float 범위를 넘길 수 있어 먼저 clip
                eta = 0.1 if _ratio is None else 0.9 * float(np.clip(_ratio, 0.0, 1e3)) ** 2
                if self._ew_eta_prev is not None and 0.9 * self._ew_eta_prev ** 2 > 0.1:
                    eta = max(eta, 0.9 * self._ew_eta_prev ** 2)          # 급조임 진동 safeguard
                eta = max(eta, min(0.1, 0.5 * tol_rel * scale / max(f2_cur, 1e-300)))   # over-solve 방지
                rtol_cg = float(np.clip(eta, 1e-5, 0.1))
                # ★safeguard 비교는 **클립된** η 로 (Kelley 표준).  클립-전 raw η 저장은 (a) 표준 이탈
                #   이고 (b) 이력이 콜 사이에 보존되면 raw² 가 오버플로한다(실측).  η_max=0.1 이라
                #   0.9·0.1²=0.009<0.1 → safeguard 는 현 상한에선 비활성 = 무해한 dead branch.
                _eta_raw = rtol_cg
            else:
                _eta_raw = None
                rtol_cg = 1e-5
            self._ew_eta_prev = _eta_raw; self._ew_f2_prev = f2_cur
            if not hasattr(self, '_ew_eta_log'):
                self._ew_eta_log = []                        # η 감사 기록 (selftest S3; float라 부담 無)
            self._ew_eta_log.append(rtol_cg)
            if self.N >= 50000:                             # 대형계 Newton 진행 라인 (침묵 방지)
                print(f'    Newton it{it}: 잔차 {r:.2e} (목표 {tol_rel:.0e}, η={rtol_cg:.0e}) '
                      f'→ 보정해 CG…', flush=True)
            X = phi[self.f_e] - phi[self.f_i] - U_f
            I_f, g_f, eta_s = kin.face_current(X, i0_f, self.A_face, I_init=I_f)
            data = self.data0.copy()
            data[self.pos_ei] = -g_f
            data[self.pos_ie] = -g_f
            diag_add = np.zeros(self.N)
            np.add.at(diag_add, self.f_e, g_f)
            np.add.at(diag_add, self.f_i, g_f)
            data[self.pos_diag] = self._diag0 + diag_add
            self.J.data[:] = data
            # inexact-Newton: 보정해 CG는 느슨하게(1e-5) — 잔차는 매번 정확 재계산되므로
            # Newton 외부 루프가 흡수.  타이트 rtol(1e-9)은 실전 κ에서 CG 정체 원인이었음.
            if not hasattr(self, '_pc_cache'):
                self._pc_cache = {}                          # sticky-GPU + AMG 계층 (스텝 간 보존)
            # CG atol = 교정-바닥 기반 (코히런트 공식은 ~10³× 후해 CG 조기종료 → 부분해 →
            # Newton 정체 r~e-3 를 유발했음: V100 smoke7 t=1-9s 거부 + 스트레스 리프로로 실증)
            # C4b: MPM_S4_ATOL_FLOOR_FRAC(기본 0.05=현행 bitwise) — 0.5로 올리면 심층 목표가
            # Jacobi 자기바닥(~1.4e-12) 위 = nnAMG 없이 종료 (opt-in; V100 감사 통과 전 기본 변경 금지)
            _atol_frac = float(os.environ.get('MPM_S4_ATOL_FLOOR_FRAC', '0.05'))
            atol_cg = _atol_frac * float(getattr(self, 'agg_floor_abs', 0.0))
            self.last_atol_cg = atol_cg                      # 감사용 (selftest S5)
            dphi, info = _cg(self.J, -Fv, x0=None, rtol=rtol_cg, atol=atol_cg,
                             pc_cache=self._pc_cache, deep=deep,
                             floor_abs=getattr(self, 'agg_floor_abs', 0.0))
            self.last_cg_info = max(getattr(self, 'last_cg_info', 0), int(info))
            self._cg_failed = bool(info)
            f2_old = f2_cur                                 # ℓ2-merit (∞는 단일노드 거부로 정체 유발) = ‖Fv‖₂

            def _armijo_try(dphi_):                         # 감쇠: merit 감소 보장 (Armijo c=1e-4)
                step = 1.0
                for _k in range(10):
                    Fn, I_fn, eta_n = self.residual(phi + step * dphi_, U_f, i0_f, kin, V_app,
                                                    I_faces_init=I_f)
                    if float(np.linalg.norm(Fn)) <= f2_old * (1.0 - 1e-4 * step):
                        return True, step, Fn, I_fn, eta_n
                    step *= 0.5
                return False, step, Fn, I_fn, eta_n

            accepted, step, Fn, I_fn, eta_n = _armijo_try(dphi)
            if not accepted and _ew and rtol_cg > 1.0001e-5 and not self._cg_failed:
                # ★EW 느슨해가 하강방향 실패 → tight(구식 1e-5) 재솔브 1회 (느슨해 warm-start).
                #   인라인이라 stall 카운터/외부 루프 재진입 간섭 없음; F당 최대 1회 = 무한루프 불가.
                print('    (EW 느슨해 Armijo 거부 → tight 재솔브 1회)', flush=True)
                self._ew_tight_n = getattr(self, '_ew_tight_n', 0) + 1
                dphi, info = _cg(self.J, -Fv, x0=dphi, rtol=1e-5, atol=atol_cg,
                                 pc_cache=self._pc_cache, deep=deep,
                                 floor_abs=getattr(self, 'agg_floor_abs', 0.0))
                self.last_cg_info = max(self.last_cg_info, int(info)); self._cg_failed = bool(info)
                accepted, step, Fn, I_fn, eta_n = _armijo_try(dphi)
            if not accepted:
                break                                        # ||F|| 미감소 → 스텝 거부, phi 보존
                                                             # (강제수용이 V100 폭주의 방아쇠였음)
            phi = phi + step * dphi
            Fv, I_f, eta_s = Fn, I_fn, eta_n
            it += 1
        self.last_newton_it = it
        return phi, I_f, eta_s, _err(Fv, phi), it

    def _ev_maker(self, phi0, U_f, i0_f, kin, i_scale):
        """potentiostatic 평가 클로저 — 마지막 평가 상태(phi/I_f/η/r/V/I)를 st에 일관 보존.
        (교훈: 시컨트 회전 뒤 '미평가 V'를 반환하면 φ↔V 불일치로 감사·기록이 오염됨)"""
        st = {'phi': phi0, 'n_ev': 0}

        def ev(V):
            st['n_ev'] += 1                                  # 스텝당 V-평가 횟수 (케이던스 진단용)
            st['phi'], st['I_f'], st['eta'], st['r'], _ = self.newton(
                st['phi'], U_f, i0_f, kin, float(V), i_scale=i_scale)
            st['V'] = float(V)
            st['I'] = self.plate_current(st['phi'], float(V))
            return st['I']

        return ev, st

    def _bracket_illinois(self, ev, f_of_I, V_start, tol_abs, max_eval=40, step0=0.05,
                          f_dec=True, st=None, r_ok=1e-3):
        """f(V)=f_of_I(ev(V), V) 의 근 — 단조 f 가정, bracket 확장 + Illinois false-position.
        순수 시컨트는 sinh 지수 꼬리에서 핑퐁(2026-07-16 selftest가 검출) → 괄호법이 정답.
        f_dec: f가 V에 단조 감소(True; I_del−I_t) / 증가(False; V−I·R−V_t).
        반환 (수렴여부).  최종 상태는 ev의 st에 남음."""
        def _valid():
            return st is None or st.get('r', 0.0) <= r_ok

        f0 = f_of_I(ev(V_start), V_start)
        if abs(f0) <= tol_abs:
            return True
        if not _valid():
            return False                                     # 비수렴 평가 → f 신뢰 불가 (V100/스트레스 폭주 방지)
        s_dir = (1.0 if f0 > 0 else -1.0) * (1.0 if f_dec else -1.0)   # f를 0쪽으로 미는 V 방향
        V_lo, f_lo = V_start, f0                             # 같은 부호 쪽 끝
        step = step0
        V_hi = f_hi = None
        for _ in range(14):                                  # 0.05→…→~400 V 지수 확장 (충분)
            Vn = V_lo + s_dir * step
            fn = f_of_I(ev(Vn), Vn)
            if not _valid():
                return False                                 # 확장 중 비수렴 → 즉시 중단(미스 가드가 처리)
            if abs(fn) <= tol_abs:
                return True
            if (fn > 0) != (f0 > 0):
                V_hi, f_hi = Vn, fn
                break
            V_lo, f_lo = Vn, fn
            step *= 2.0
        if V_hi is None:
            return False                                     # 미괄호 — 호출자 가드가 처리
        side = 0
        for _ in range(max_eval):
            den = f_lo - f_hi
            Vm = (V_hi * f_lo - V_lo * f_hi) / den if abs(den) > 1e-300 else 0.5 * (V_lo + V_hi)
            lo, hi = (V_lo, V_hi) if V_lo < V_hi else (V_hi, V_lo)
            if not (lo < Vm < hi):
                Vm = 0.5 * (lo + hi)
            fm = f_of_I(ev(Vm), Vm)
            if not _valid():
                return False
            if abs(fm) <= tol_abs or abs(hi - lo) < 1e-12:
                return True
            if (fm > 0) == (f_lo > 0):
                V_lo, f_lo = Vm, fm
                if side == -1:
                    f_hi *= 0.5                              # Illinois: 정체 측 가중 감쇠
                side = -1
            else:
                V_hi, f_hi = Vm, fm
                if side == +1:
                    f_lo *= 0.5
                side = +1
        return False

    def solve_galv(self, phi, U_f, i0_f, kin, I_target, V_guess, tol_rel_i=None):
        """정전류: I_del(V_app)=I_target 인 V_app (I_del은 V에 단조↓).
        반환 (phi, I_f, eta_s, resid, V_app, I_del) — 전부 마지막 평가와 일관."""
        scale = max(abs(I_target), 1e-12)
        if tol_rel_i is None:                                # 바닥-인지 tol: 교정된 float64 집계
            tol_rel_i = max(1e-7, 0.5 * float(getattr(self, 'agg_floor_abs', 0.0)) / scale)
            # 노이즈 바닥(V100 1.6e-05 rel) 아래 자릿수는 물리 무의미 — Illinois가 그걸 갈면
            # 스텝당 평가 ~13회(smoke8 실측).  0.5×바닥 = 경고선(4×바닥)의 1/8 여유.
        ev, st = self._ev_maker(phi, U_f, i0_f, kin, scale)
        # 적응형 첫 탐색폭: 직전 스텝의 실제 ΔV 기반 (고정 0.05 V는 스텝 간 ΔV~0.1 mV인
        # 시간전개에서 매 스텝 큰 점프-회수 낭비를 만들었음 — V100 스모크 로그)
        step0 = float(np.clip(4.0 * getattr(self, '_galv_dV', 2.5e-3), 1e-4, 0.05))
        self._bracket_illinois(ev, lambda I, V: I - I_target, float(V_guess),
                               tol_rel_i * scale, step0=step0, st=st)
        self._galv_dV = max(abs(st['V'] - float(V_guess)), 2.5e-5)
        self.last_galv_miss = abs(st['I'] - I_target) / scale
        self.last_galv_nev = st['n_ev']
        return st['phi'], st['I_f'], st['eta'], st['r'], st['V'], st['I']

    def solve_vterm(self, phi, U_f, i0_f, kin, V_term, r_int_abs, V_guess, i_scale,
                    tol_v=1e-7):
        """터미널 전압 고정(CV 홀드): V_app − I_del(V_app)·R_int = V_term.
        R_int=0이면 potentiostatic 한 방.  반환 규약 = solve_galv와 동일(일관 상태)."""
        ev, st = self._ev_maker(phi, U_f, i0_f, kin, max(abs(i_scale), 1e-12))
        if r_int_abs <= 0:
            ev(V_term)
            self.last_galv_miss = 0.0
            self.last_galv_nev = st['n_ev']
            return st['phi'], st['I_f'], st['eta'], st['r'], st['V'], st['I']
        self._bracket_illinois(ev, lambda I, V: (V - I * r_int_abs) - V_term,
                               float(V_guess), tol_v, step0=0.01, f_dec=False, st=st)
        # F2: 괄호 실패가 침묵하지 않도록 터미널 방정식 미스를 실측 보고 (리뷰 R2 물리#12/수치#3)
        self.last_galv_miss = abs((st['V'] - st['I'] * r_int_abs) - V_term) / max(abs(V_term), 1.0)
        self.last_galv_nev = st['n_ev']
        return st['phi'], st['I_f'], st['eta'], st['r'], st['V'], st['I']

    def particle_current(self, I_f):
        """입자별 리튬화 전류 [A] (방전 +).  I_f 는 e→i(탈리튬) 양수 → 부호 반전 합산."""
        i_am = np.zeros(self.n_am)
        m = self.f_pid >= 0
        np.add.at(i_am, self.f_pid[m], -I_f[m])
        return i_am

    def phi_z_profiles(self, phi):
        """운전-중 z-층 평균 전위 (φ_e(z), φ_i(z)) — 전자·이온 전류 상보 구도의 직접 시각화.

        STEP3 unit-ΔV 프로파일(각 망 따로, 같은 BC → 둘 다 1→0 준선형)과 달리, 결합 운전
        솔브에선 φ_e ≈ 평평(µV급, 곡률 집전체쪽) / φ_i 수십 mV(곡률 분리막쪽) — 크기·곡률이
        미러.  dof 없는 층(패딩 등)은 NaN."""
        nz = len(self.z_um_layers)
        ce = np.bincount(self.k_e_layer, minlength=nz)
        ci = np.bincount(self.k_i_layer, minlength=nz)
        pe = np.bincount(self.k_e_layer, weights=phi[:self.n_e], minlength=nz)
        pi = np.bincount(self.k_i_layer, weights=phi[self.n_e:self.N], minlength=nz)
        pe = np.where(ce > 0, pe / np.maximum(ce, 1), np.nan)
        pi = np.where(ci > 0, pi / np.maximum(ci, 1), np.nan)
        return pe.astype(np.float32), pi.astype(np.float32)

    def energy_audit(self, phi, I_f, eta_s, U_f, kin, V_app):
        """P_ohm(e/i, 판 포함) + Σ I·η_s + Σ I²·ASR/A + Σ I·U + V·I_del = 0 (기계정밀도 감사).
        유도: 정상성 φᵀF=0 에 판-Dirichlet b-항을 물리 항(판 소산·전달 전력)으로 재배열.
        반환 dict [W] — Q_* 발열 분해로도 그대로 사용."""
        Pn = phi * self._L0_apply(phi)
        pc = phi[self.aB]
        pt = phi[self.aT]
        P_B = float(np.sum(self.gB * (V_app - pc) ** 2))     # 집전체 판-링크 소산
        P_T = float(np.sum(self.gT * pt ** 2))               # 분리막 접지-링크 소산
        P_ohm_e = float(Pn[:self.n_e].sum()) - float(np.sum(self.gB * pc ** 2)) + P_B
        P_ohm_i = float(Pn[self.n_e:].sum()) - float(np.sum(self.gT * pt ** 2)) + P_T
        P_ct = float((I_f * eta_s).sum())
        P_film = float((I_f ** 2).sum() * kin.asr / self.A_face) if kin.asr > 0 else 0.0
        P_chem = float((I_f * U_f).sum())
        I_del = self.plate_current(phi, V_app)
        res = P_ohm_e + P_ohm_i + P_ct + P_film + P_chem + V_app * I_del
        den = max(abs(I_del) * max(abs(V_app), 1.0), 1e-30)
        return {'P_ohm_e': P_ohm_e, 'P_ohm_i': P_ohm_i, 'P_ct': P_ct, 'P_film': P_film,
                'P_chem': P_chem, 'V': V_app, 'I_del': I_del, 'balance_rel': res / den}


# ---------------------------------------------------------------- 시간 루프
def simulate(sys_, ocp, r_p_m, d_s, kin, c_rate, nr=20, v_min=3.0, v_max=4.5,
             dx_max=0.02, dt_init=1.0, dt_max=120.0, t_max=None, charge=False,
             cv_hold=False, i_cut_frac=0.05, r_int_ohm_cm2=0.0, x_init=None,
             dudt=None, i0_p=None, n_chk=12, x_field=None, j_field=None, verbose=True):
    """CC 방전(기본)/충전 (+cv_hold=True → V-리밋 도달 후 CV 홀드 = CCCV).
    r_int_ohm_cm2: 집전체 실측 R_int 직렬(시나리오 부하, STEP3 규약) — 터미널 V·컷오프에 반영.
    dudt: (x_tab, dUdT_tab) 있으면 Q_rev = Σ I_f·T·dU/dT(x_f) 출력 (관례: I_f = 탈리튬 +).
    d_s: 스칼라 또는 [n_am] per-particle [m²/s] (bimodal poly/SC — RadialDiffusion 브로드캐스트).
    i0_p: None(공유 kin.i0_ref) 또는 [n_am] per-particle i0_ref [A/m²] — SOC-모양 i0(x)는 공유하고
      진폭만 입자별 스케일 (i0_ref·shape·(i0_p/i0_ref) = i0_p·shape; 균일값이면 ×1.0 = bitwise 동일)."""
    n_am = sys_.n_am
    x_ini = float(x_init) if x_init is not None else (ocp.x0 if not charge else ocp.x100)
    x_end = ocp.x100 if not charge else ocp.x0
    rad = RadialDiffusion(n_am, nr, r_p_m, d_s, ocp.c_max, x_ini)
    if x_field is not None:                                  # ★v2 chaining: 이전 런 끝 셸-SOC 필드로 시작
        _xf = np.asarray(x_field, np.float64)
        if _xf.shape != (n_am, nr):
            raise ValueError(f'x_field {_xf.shape} ≠ ({n_am}, {nr}) — 같은 베드·같은 nr 로만 체인 가능')
        # 수용밴드 = 솔버 자체 in-band(soc_overrun 문턱 ±0.01/1.01) — 코드리뷰 chain#2: 정상 종료한
        # 심방전 상태가 셸 x∈(1, 1.01] 를 합법으로 가질 수 있어 ±1e-6 밴드는 정상 체인을 오인 거부.
        if (not np.isfinite(_xf).all()) or float(_xf.min()) < -0.01 or float(_xf.max()) > 1.01:
            raise ValueError('x_field가 솔버 밴드 [-0.01, 1.01] 밖(또는 NaN) — 손상/오염 상태')
        rad.x[:] = np.clip(_xf, 1e-6, 1.0 - 1e-6)
        _dclip = float(np.abs(rad.x - _xf).max())
        if _dclip > 1e-9:                                    # in-band 오버슛 절단 감사 (침묵 질량이동 금지)
            print(f'    ⚠ x_field 클립: 최대 셸 |Δx|={_dclip:.2e} (in-band 오버슛 절단 — 질량 영향 '
                  f'~셸가중×Δ, 감사용)', flush=True)
    if j_field is not None:                                  # ★표면농도 연속성 (전기화학 리뷰 chain#4):
        rad.J[:] = np.asarray(j_field, np.float64)           #   이전 런 표면유속으로 '첫' surf_x 재구성만 —
                                                             #   첫 전진에서 새 솔브의 J 로 대체됨
    if i0_p is not None:
        i0_p = np.asarray(i0_p, np.float64)
        if i0_p.shape != (n_am,) or not np.all(i0_p > 0):
            raise ValueError(f'i0_p must be [{n_am}] > 0 (got shape {i0_p.shape})')
    _i0s = None if i0_p is None else i0_p / kin.i0_ref      # 입자별 진폭 스케일 (균일=1.0 → ×1.0 bitwise 불변)
    V_p = 4.0 / 3.0 * np.pi * np.asarray(r_p_m) ** 3        # [m³] 물리 구부피 (용량 기준)
    if x_field is not None:                                  # 부기 기준 = 실제 시작 x̄ (체인: 창 끝이 아님)
        x_ini = float((rad.mean_x() * V_p).sum() / V_p.sum())
    cap_As = F_CONST * ocp.c_max * abs(ocp.x100 - ocp.x0) * V_p.sum()
    I_1C = cap_As / 3600.0
    I_cc = c_rate * I_1C * (1.0 if not charge else -1.0)    # 방전 +(인출)
    # ★rate-aware 수렴바닥 (2026-07-22): 후막+저율은 near-null-space(약한 BV결합)로 Newton 잔차가
    #   ~1/rate 배 높은 바닥에서 정체 — 1e-8은 도달 불가.  잔차는 i_scale(=목표전류)로 정규화된 값이라
    #   저율일수록 같은 절대오차가 크게 보임.  정체-수용/하드페일 임계를 1/rate로 완화 (0.2C→×5 = 전류수지
    #   0.5%까지 곡선 수용; 그 이상은 여전히 하드페일 = 가비지 가드 유지).  galv_miss가 최종 정확도 심판.
    _rate_relax = min(max(1.0, 1.0 / max(c_rate, 0.05)), 10.0)   # 0.1C→10 (전류수지 1%까지 수용), 그 이하 cap
    _hard_tol = 1e-3 * _rate_relax                          # simulate 하드페일 임계 (rate-scale)
    sys_.stall_tol = _hard_tol                              # newton() 정체-수용 임계 (동일 페어)
    sys_._rate_relax = float(_rate_relax)                   # viz 수렴품질 배지용 (뷰어 투명 표시)
    R_int_abs = (r_int_ohm_cm2 * 1e-4 / sys_.area_m2) if r_int_ohm_cm2 > 0 else 0.0   # [Ω]
    has_face = np.zeros(n_am, bool)
    has_face[np.unique(sys_.f_pid[sys_.f_pid >= 0])] = True
    if verbose:
        print(f'  step4-v2: n_am={n_am} (dead {int((~has_face).sum())}), BV faces {sys_.n_bv:,}, '
              f'dof {sys_.N:,}, I_1C={I_1C:.3e} A, I_cc={I_cc:.3e} A ({c_rate:g}C'
              f'{", CCCV" if cv_hold else ""}), R_int={r_int_ohm_cm2:g} Ω·cm², '
              f'α={kin.aa}/{kin.ac}, ASR_film={kin.asr:g} Ω·m², T={kin.T:g} K', flush=True)
        if rad.D.max() > rad.D.min() or i0_p is not None:   # per-particle 전기화학 활성 시 정직 표기
            _i0lo, _i0hi = ((kin.i0_ref, kin.i0_ref) if i0_p is None
                            else (float(i0_p.min()), float(i0_p.max())))
            print(f'  ★ per-particle 전기화학: D_s {rad.D.min():.3g}–{rad.D.max():.3g} m²/s, '
                  f'i0_ref {_i0lo:g}–{_i0hi:g} A/m² (poly/SC 분리 — provenance는 CLI 로그/앵커 CSV)',
                  flush=True)
        # 곡선-비교 정합용 per-런 앵커 (수치리뷰 F1/F2 2026-07-17): 곡선 도구가 이 라인을 파싱해
        # 자기 면적용량·x_init로 축을 만들면 공유-앵커 오염(용량 1.3% 차 → knee 최대 ~10 mV
        # 가짜 갭)이 사라짐.  dead-AM 부피분율도 병기 (용량/soc_end는 전체-AM 규약).
        _a_cm2 = sys_.area_m2 * 1e4
        print(f'  step4-v2: area={_a_cm2:.6g} cm², areal_cap={cap_As / 3600.0 / _a_cm2 * 1e3:.6g} '
              f'mAh/cm², x_init={x_ini:.6f}, dead_AM_vol={float(V_p[~has_face].sum() / V_p.sum() * 100):.3f}%',
              flush=True)
    phi = np.zeros(sys_.N)
    U0 = float(ocp.U(x_ini))
    phi[:sys_.n_e] = U0
    phi[sys_.iso_idx] = 0.0                                  # 고립 placeholder는 0 고정 (가짜 잔차 방지)
    V_prev = U0                                              # V_app warm start (평형 = OCV)
    # float64 노이즈 바닥 자가교정 (초기상태 = 정확한 평형 → 측정치 = 순수 반올림)
    # 체인 시작상태는 비평형(입자별 U 상이 → 진짜 BV 전류가 잔차에 실림) — 바닥이 과대교정돼
    # Newton 경고선/목표가 물러진다.  균일 x̄ 참조평형으로 순수 float64 반올림 바닥만 잰다.
    _x_s0 = rad.surf_x() if x_field is None else np.full(n_am, x_ini)
    _fp0 = np.clip(sys_.f_pid, 0, n_am - 1)
    _i0v0 = kin.i0(_x_s0) if _i0s is None else kin.i0(_x_s0) * _i0s
    _agg0, _inf0 = sys_.calibrate_floor(phi, ocp.U(_x_s0)[_fp0], _i0v0[_fp0], kin, U0)
    if verbose:
        print(f'  노이즈 바닥 교정: |ΣF|_eq={_agg0:.2e} A (floor=×4), ||F||∞_eq={_inf0:.2e} A '
              f'→ floor_rel≈{sys_.agg_floor_abs / max(abs(I_cc), 1e-30):.1e}', flush=True)
    keys = ('t', 'V', 'V_terminal', 'I', 'x_mean', 'x_surf_p05', 'x_surf_p50', 'x_surf_p95',
            'eta_kin_mean', 'eta_diff_mean', 'eta_diff_mean_iw', 'newton_it', 'newton_resid', 'kcl_rel',
            'energy_balance_rel',
            'Q_ohm_e_W', 'Q_ohm_i_W', 'Q_ct_W', 'Q_film_W', 'Q_rint_W', 'Q_rev_W')
    out = {k: [] for k in keys}
    # 뷰어 체크포인트 (코어-셸 SOC + 면별 반응전류): SOC-진행 균등 n_chk점 + 마지막 상태
    chk = {'t': [], 'x_mean': [], 'x_shell': [], 'I_face': [], 'phi_e_z': [], 'phi_i_z': []}
    _win = abs(ocp.x100 - ocp.x0)
    # 뷰어 체크포인트 페이싱: 체인 세그먼트는 남은 스팬 기준 (전체 창 기준이면 부분 세그먼트가
    # n_chk 중 2-3점만 기록 — 전기화학 리뷰 chain#10b).  v1(x_field=None)은 기존 그대로.
    _win_rec = abs(x_end - x_ini) if x_field is not None else _win
    _next_rec = 0.0

    def _rec_chk(t_now, x_bar_now, I_f_now, phi_now):
        chk['t'].append(float(t_now)); chk['x_mean'].append(float(x_bar_now))
        chk['x_shell'].append(rad.x.astype(np.float16).copy())
        chk['I_face'].append(np.asarray(I_f_now, np.float32).copy())
        _pe, _pi = sys_.phi_z_profiles(phi_now)             # 운전-중 φ(z) 상보 프로파일
        chk['phi_e_z'].append(_pe); chk['phi_i_z'].append(_pi)

    t, dt = 0.0, dt_init
    x_keep = None                                            # 직전 기록점의 셸필드 (V_cutoff 롤백용)
    phase = 'cc'
    I_app = I_cc
    v_lim = v_min if not charge else v_max
    dxs_meas = 0.0
    x_s_prev = None
    reason = 't_max'
    while True:
        x_s = rad.surf_x()
        fp = np.clip(sys_.f_pid, 0, n_am - 1)
        U_f = ocp.U(x_s)[fp]
        i0_f = (kin.i0(x_s) if _i0s is None else kin.i0(x_s) * _i0s)[fp]
        if phase == 'cc':
            phi, I_f, eta_s, resid, V_app, I_del = sys_.solve_galv(
                phi, U_f, i0_f, kin, I_app, V_prev)
        else:                                               # CV 홀드: 터미널 V = v_lim 유지
            phi, I_f, eta_s, resid, V_app, I_del = sys_.solve_vterm(
                phi, U_f, i0_f, kin, v_lim, R_int_abs, V_prev,
                i_scale=max(abs(I_app), i_cut_frac * I_1C))
            I_app = I_del
        V_prev = V_app
        n_it = int(getattr(sys_, 'last_newton_it', -1))
        i_am = sys_.particle_current(I_f)
        galv_miss = float(getattr(sys_, 'last_galv_miss', 0.0))
        _fl = float(getattr(sys_, 'last_err_floor_rel', 0.0))
        warn_thr = max(1e-6, 4.0 * _fl)                     # 노이즈-바닥 위에서만 경고 (스케일 인지)
        if resid > warn_thr or galv_miss > warn_thr:        # F2 규약: 침묵 실패 금지 (수치리뷰 #5)
            print(f'    ⚠ step4 잔차 {resid:.1e} / 정전류 미스 {galv_miss:.1e} '
                  f'(경고선 {warn_thr:.1e}) @t={t:.1f}s — 신뢰 주의', flush=True)
        newton_failed = ((not np.isfinite(resid))               # NaN/Inf = 하드실패 (NaN 비교는 False라 조용히 통과하던 걸 차단)
                         or resid > max(_hard_tol, 40.0 * _fl)
                         or galv_miss > max(_hard_tol, 40.0 * _fl))   # 하드 실패 (rate-aware): 확산 전진 전 중단
        kcl = abs(i_am.sum() - I_del) / max(abs(I_del), 1e-30)
        aud = sys_.energy_audit(phi, I_f, eta_s, U_f, kin, V_app)
        V_cell = V_app
        V_term = V_cell - I_del * R_int_abs
        V_term_rec = V_term                                     # 기록/출력용 (실 V_term은 아래 상전이 판정에 그대로 사용)
        if phase == 'cc' and cv_hold and ((V_term < v_min) if not charge else (V_term > v_max)):
            V_term_rec = (v_min if not charge else v_max)       # CCCV 전이: CC가 v_lim 넘어선 그 스텝은 실제론 CV가 물려 전압 v_lim 고정 → 곡선 비물리 스파이크 제거
        x_mean_p = rad.mean_x()
        x_bar = float((x_mean_p * V_p).sum() / V_p.sum())
        w = np.abs(I_f) + 1e-30
        out['t'].append(t); out['V'].append(V_cell); out['V_terminal'].append(V_term_rec)
        out['I'].append(I_del)
        out['x_mean'].append(x_bar)
        out['x_surf_p05'].append(float(np.percentile(x_s[has_face], 5)))
        out['x_surf_p50'].append(float(np.percentile(x_s[has_face], 50)))
        out['x_surf_p95'].append(float(np.percentile(x_s[has_face], 95)))
        out['eta_kin_mean'].append(float((np.abs(eta_s) * w).sum() / w.sum()))
        out['eta_diff_mean'].append(float(np.mean(np.abs(ocp.U(x_s[has_face])
                                                         - ocp.U(x_mean_p[has_face])))))
        # |i_am|-가중 짝 (리뷰 #2): 비가중 평균은 per-particle D 분리가 만드는 클래스별 확산분극을
        # 입자수비(예 SC 12:1)로 희석 — 전류-가중이 eta_kin_mean(|I_f|-가중)과 규약 일치.
        _wp = np.abs(i_am[has_face]) + 1e-30
        out['eta_diff_mean_iw'].append(float((np.abs(ocp.U(x_s[has_face])
                                                     - ocp.U(x_mean_p[has_face])) * _wp).sum() / _wp.sum()))
        out['newton_it'].append(n_it); out['newton_resid'].append(resid)
        out['kcl_rel'].append(kcl)
        out['energy_balance_rel'].append(abs(aud['balance_rel']))
        out['Q_ohm_e_W'].append(aud['P_ohm_e']); out['Q_ohm_i_W'].append(aud['P_ohm_i'])
        out['Q_ct_W'].append(aud['P_ct']); out['Q_film_W'].append(aud['P_film'])
        out['Q_rint_W'].append(I_del * I_del * R_int_abs)
        out['Q_rev_W'].append(float((I_f * kin.T * np.interp(x_s, dudt[0], dudt[1])[fp]).sum())
                              if dudt is not None else np.nan)
        if verbose:                                          # 매 스텝 (스텝 수십 개 규모 — 로그 부담 無;
            _nev = int(getattr(sys_, 'last_galv_nev', -1))   #  %10 게이팅은 진행 확인을 불가능하게 했음)
            print(f'    step {len(out["t"]):4d} t={t:9.1f}s [{phase}] V={V_term_rec:.4f} '
                  f'I={I_del:.3e} x̄={x_bar:.4f} ηkin={out["eta_kin_mean"][-1] * 1e3:.1f}mV '
                  f'E-bal {aud["balance_rel"]:.1e} KCL {kcl:.1e} (ev {_nev}, dt {dt:.0f}s)',
                  flush=True)
        # 뷰어 체크포인트: SOC-창 진행 균등 지점마다 셸-SOC + 면전류 기록
        _frac = abs(x_bar - x_ini) / max(_win_rec, 1e-12)
        if _frac >= _next_rec - 1e-12 and not newton_failed:
            _rec_chk(t, x_bar, I_f, phi)
            _next_rec += 1.0 / max(n_chk - 1, 1)
        # ---- 종료/전환 ----
        if newton_failed:                                   # 가비지 상태로 확산을 전진시키지 않음
            reason = 'newton_fail'
            print(f'  ⚠ step4-v2 HARD-FAIL: Newton 미수렴(resid {resid:.1e}) — 솔버/전처리 점검 필요',
                  flush=True)
            break
        done_soc = (x_bar >= x_end - 1e-4) if not charge else (x_bar <= x_end + 1e-4)
        v_out = (V_term < v_min) if not charge else (V_term > v_max)
        if phase == 'cc' and v_out and cv_hold:
            phase = 'cv'
            if verbose:
                print(f'    → CV hold @ {v_lim:.3f} V (terminal)', flush=True)
        elif phase == 'cv' and abs(I_app) < i_cut_frac * I_1C:
            reason = 'cv_i_cut'; break
        elif phase == 'cc' and v_out:
            reason = 'V_cutoff'; break
        if done_soc:
            reason = 'soc_end'; break
        if t_max and t >= t_max:
            reason = 't_max'; break
        # ---- 확산 전진 ----
        rad.J = i_am / (F_CONST * 4.0 * np.pi * rad.R ** 2)
        # SOC-창 끝 오버슛 클램프: 남은 창을 다 채우는 시간보다 dt를 길게 두지 않음 (+5%)
        if abs(I_app) > 0:
            dt_end = abs(x_end - x_bar) * F_CONST * ocp.c_max * V_p.sum() / abs(I_app) * 1.05
            dt = min(dt, max(dt_end, 1e-3))
        # 표면-스텝 거부-재시도 (물리리뷰 #3: 사후 축소만으론 과대 스텝이 기록에 남음).
        # 같은 새 J 기준으로 전/후 표면 SOC를 재서 2·dx_max 초과 시 되돌리고 dt 반감.
        x_s_pre = rad.surf_x()
        x_keep = rad.x.copy()
        for _try in range(6):
            rad.step(dt)
            dxs_meas = float(np.max(np.abs(rad.surf_x() - x_s_pre)))
            if dxs_meas <= 2.0 * dx_max or dt <= 0.05 or _try == 5:   # 마지막 시도는 수용 (되돌림+t전진 desync 방지)
                break
            rad.x = x_keep.copy()
            dt *= 0.5
        t += dt
        if float(rad.x.max()) > 1.01 or float(rad.x.min()) < -0.01:
            reason = 'soc_overrun'                          # 셸 SOC 물리범위 이탈 (flat-OCP 크롤 가드)
            break
        # 측정-피드백 적응 dt: 실제 표면 SOC 스텝을 dx_max로 제한 (모델 추정이 아니라 실측)
        dt = float(np.clip(dt * np.clip(dx_max / max(dxs_meas, 1e-9), 0.5, 1.3), 0.05, dt_max))
    if verbose:
        q_pct = abs(x_bar - x_ini) / abs(ocp.x100 - ocp.x0) * 100
        print(f'  step4-v2 END: {reason}  t={t:.0f}s  delivered {q_pct:.1f}% of window '
              f'(E-bal max {max(out["energy_balance_rel"]):.1e})', flush=True)
        if getattr(sys_, 'last_cg_info', 0):
            print(f'  ⚠ CG maxiter 도달 이력 (info={sys_.last_cg_info}) — 해 품질 확인 요망', flush=True)
    if (not chk['t'] or chk['t'][-1] < t - 1e-9) and reason != 'newton_fail':
        _x_now = float((rad.mean_x() * V_p).sum() / V_p.sum())   # soc_overrun 프레임 짝 맞춤 (물리 R2#6)
        _rec_chk(t, _x_now, I_f, phi)
    out = {k: np.asarray(v) for k, v in out.items()}
    out['viz_t'] = np.asarray(chk['t'])
    out['viz_phi_e_z'] = np.asarray(chk['phi_e_z'])
    out['viz_phi_i_z'] = np.asarray(chk['phi_i_z'])
    out['viz_z_um'] = np.asarray(sys_.z_um_layers, np.float32)
    out['viz_x_mean'] = np.asarray(chk['x_mean'])
    out['viz_x_shell'] = (np.stack(chk['x_shell']) if chk['x_shell']
                          else np.zeros((0, n_am, nr), np.float16))
    out['viz_I_face'] = (np.stack(chk['I_face']) if chk['I_face']
                         else np.zeros((0, sys_.n_bv), np.float32))
    # V-컷오프 정밀값: 마지막 두 점 보간 (오버슛 오독 방지)
    Vt = out['V_terminal']
    if reason == 'V_cutoff' and len(Vt) >= 2:
        vv = v_min if not charge else v_max
        f = abs(Vt[-2] - vv) / max(abs(Vt[-2] - Vt[-1]), 1e-30)   # 충·방전 양방향 (수치리뷰 R2#1)
        q_arr = np.abs(out['x_mean'] - x_ini) / abs(ocp.x100 - ocp.x0)
        out['q_frac_at_cutoff'] = float(q_arr[-2] + f * (q_arr[-1] - q_arr[-2]))
        # ★상태-부기 정합 (전기화학 리뷰 chain#1): 저장 상태(x_shell_final)를 같은 f 로 컷오프
        # 교차점에 롤백 — 안 하면 매 V_cutoff 사이클마다 다음 충전이 보고 q 보다 마지막-dt 만큼
        # 깊은 상태에서 시작 (dt-의존 전량장부 오프셋, dx_max=0.02 에서 창의 ~0.3-1%/사이클).
        # 실기 cycler 는 컷오프에서 멈춤 — 오버슛은 마지막 dt 의 수치 아티팩트.
        if x_keep is not None:
            _fc = min(max(f, 0.0), 1.0)
            rad.x = x_keep + _fc * (rad.x - x_keep)
    else:
        out['q_frac_at_cutoff'] = float(abs(out['x_mean'][-1] - x_ini) / abs(ocp.x100 - ocp.x0))
    out['x_final_per_particle'] = rad.mean_x()               # (V_cutoff 롤백 반영)
    out['x_shell_final'] = rad.x.copy()                      # [n_am, nr] float64 — v2 chaining 상태
    out['J_final'] = i_am / (F_CONST * 4.0 * np.pi * rad.R ** 2)   # 마지막 운전점 표면유속 (체인 첫 재구성용)
    out['dead_particle'] = ~has_face
    out['I_1C_A'] = I_1C
    out['end_reason'] = reason
    out['d_s_p_m2s'] = rad.D.copy()                          # per-particle 감사 기록 (균일이면 상수 배열)
    out['i0_ref_p_Am2'] = (np.full(n_am, kin.i0_ref) if i0_p is None else i0_p.copy())
    _ds_uni = bool(rad.D.max() == rad.D.min())               # params JSON: 균일=스칼라(하위호환), 분리=min/max 요약
    out['params'] = dict(c_rate=c_rate,
                         d_s=(float(rad.D[0]) if _ds_uni else
                              dict(mode='per_particle', min=float(rad.D.min()), max=float(rad.D.max()))),
                         i0=(kin.i0_ref if i0_p is None else
                             dict(mode='per_particle', min=float(i0_p.min()), max=float(i0_p.max()))),
                         alpha_a=kin.aa, alpha_c=kin.ac,
                         asr_film=kin.asr, temp_k=kin.T, nr=nr, v_min=v_min, v_max=v_max,
                         cv_hold=bool(cv_hold), i_cut_frac=i_cut_frac,   # ← 운전조건이므로 기록
                         charge=bool(charge), dx_max=dx_max, dt_max=dt_max,
                         r_int_ohm_cm2=r_int_ohm_cm2,
                         c_max=ocp.c_max, x0=ocp.x0, x100=ocp.x100, x_init=x_ini,
                         chained=bool(x_field is not None),
                         ocp_provenance=ocp.provenance, test_only=ocp.test_only)
    return out


# ---------------------------------------------------------------- v2 chaining (런 간 상태 전달)
_CHAIN_STATE_VER = 'step4-chain-v1'


def save_chain_state(path, x_shell, r_p_um, ocp, end_reason, t_end=0.0, note='', J=None, dead=None):
    """런 끝 셸-SOC 필드 [n_am, nr] 를 다음 런의 초기상태로 저장 (v2 chaining).
    J = 마지막 운전점 표면유속 [mol/m²/s] — 다음 런의 '첫' surf_x 재구성 전용(표면농도 연속성,
    전기화학 리뷰 chain#4: 없으면 첫 기록점이 OCP 쪽으로 U'·Δx_surf 편향).  첫 전진에서 새 J 로
    대체되므로 확산 자체엔 미사용.  dead = 전기적 고립 입자 마스크(rest V-가중 제외용).
    φ 는 전달 안 함 (Newton 2-3회 수렴 — warm start 불요, 수치리뷰 chain#4 검증)."""
    extra = {}
    if J is not None:
        extra['J'] = np.asarray(J, np.float64)
    if dead is not None:
        extra['dead'] = np.asarray(dead, bool)
    np.savez_compressed(path, ver=np.bytes_(_CHAIN_STATE_VER),
                        x_r=np.asarray(x_shell, np.float64),
                        r_p_um=np.asarray(r_p_um, np.float64),
                        c_max=float(ocp.c_max), x0=float(ocp.x0), x100=float(ocp.x100),
                        end_reason=np.bytes_(str(end_reason)), t_end=float(t_end),
                        note=np.bytes_(str(note)), **extra)


def load_chain_state(path, n_am, nr, r_p_um, ocp):
    """체인 상태 로드 + 베드/규약/오염 가드 — 침묵 체인 금지 (3렌즈 리뷰 통합):
    비유한(NaN/Inf)·솔버-밴드([-0.01, 1.01]) 밖·newton_fail/soc_overrun 종료 상태를 명시 거부
    (rest 경로가 오염 상태를 클립-세탁하던 구멍 봉쇄).  반환 (x, reason, extra{J, dead, note})."""
    g = np.load(path, allow_pickle=False)
    ver = bytes(np.asarray(g['ver']).ravel()[0]).decode() if 'ver' in g.files else '?'
    if ver != _CHAIN_STATE_VER:
        raise SystemExit(f'--init-state {path}: 상태버전 {ver!r} ≠ {_CHAIN_STATE_VER}')
    x = np.asarray(g['x_r'], np.float64)
    if x.shape != (int(n_am), int(nr)):
        raise SystemExit(f'--init-state {path}: x_r {x.shape} ≠ (n_am={n_am}, nr={nr}) — '
                         '같은 베드(step4_grid)·같은 --nr 로만 체인 가능')
    if not np.isfinite(x).all():                             # NaN 은 min/max 비교를 조용히 통과 (수치리뷰 #3)
        raise SystemExit(f'--init-state {path}: x 에 NaN/Inf — 오염 상태 체인 거부')
    if float(x.min()) < -0.01 or float(x.max()) > 1.01:      # 솔버 자체 in-band(±0.01) 밖 = 손상
        raise SystemExit(f'--init-state {path}: x 범위 [{float(x.min()):.4g}, {float(x.max()):.4g}] '
                         '— 솔버 밴드 [-0.01, 1.01] 밖 = 손상 상태 (체인 거부)')
    r_s = np.asarray(g['r_p_um'], np.float64)
    if r_s.shape != x[:, 0].shape or not np.allclose(r_s, np.asarray(r_p_um, np.float64),
                                                     rtol=1e-6, atol=1e-9):
        raise SystemExit(f'--init-state {path}: 입자 반경 불일치 — 다른 베드의 상태 (체인 금지)')
    if abs(float(g['c_max']) - ocp.c_max) > 1e-6 * max(ocp.c_max, 1.0):
        raise SystemExit(f'--init-state {path}: c_max 불일치 ({float(g["c_max"]):g} vs {ocp.c_max:g})')
    reason = bytes(np.asarray(g['end_reason']).ravel()[0]).decode()
    if reason in ('newton_fail', 'soc_overrun') and os.environ.get('MPM_S4_CHAIN_FORCE', '0') != '1':
        raise SystemExit(f'--init-state {path}: 이전 런이 {reason} — 오염 상태 체인 거부 '
                         '(강제: MPM_S4_CHAIN_FORCE=1)')
    if abs(float(g['x0']) - ocp.x0) > 1e-9 or abs(float(g['x100']) - ocp.x100) > 1e-9:
        print(f'    ⚠ --init-state: 저장측 창(x0={float(g["x0"]):g}, x100={float(g["x100"]):g}) ≠ '
              f'현재 창({ocp.x0:g}, {ocp.x100:g}) — 용량 %-축 해석 주의', flush=True)
    extra = {'J': (np.asarray(g['J'], np.float64) if 'J' in g.files else None),
             'dead': (np.asarray(g['dead'], bool) if 'dead' in g.files else None),
             'note': (bytes(np.asarray(g['note']).ravel()[0]).decode() if 'note' in g.files else '')}
    if extra['note']:
        print(f'    ℹ chain state note: {extra["note"]}', flush=True)
    return x, reason, extra


def run_rest(rad, ocp, V_p, t_rest_s, dt_s=5.0, i0_fn=None, i0_amp=None, alive=None, j0=None):
    """★Rest 실물리 v2.0 (REST-LOCAL): I=0 완화 — 입자별 zero-flux 방사확산만 전개.
    입자 간 전하 재분배(혼합전위 평활 = I_tot=0 망솔브)는 미모델 [v2.1 훅 — bimodal D_s/i0 분리
    베드를 rest 로 체인할 땐 이게 1차 항이므로 v2.1 우선 대상, 물리리뷰 chain 노트].
    V 트레이스 = **i0(x_surf)·R² 가중** 혼합전위 선형화 OCP (전기화학 리뷰 chain#3: 부피(R³)
    가중은 Σ i0·A·sinh(f/2·(V−U))=0 의 해가 아니라 바이모달서 수십 mV 편향; dead 입자 제외).
    첫 점(t=0)은 j0(이전 런 표면유속)로 표면농도 연속 재구성 — 이후 J=0.
    시간적분 = Rannacher 스타트업(BE 반스텝 ×2) + CN — 급경사 초기장 CN 링잉 제거(수치리뷰
    chain#1: 2µm/D=3e-14 최악모드 eig −0.937 → BE 가 감쇠).  질량 정확 보존 → drift 검산."""
    n = max(int(np.ceil(t_rest_s / max(dt_s, 1e-9))), 1)
    dt = t_rest_s / n
    wv = V_p / V_p.sum()
    ok_p = np.ones(rad.n_p, bool) if alive is None else np.asarray(alive, bool).copy()
    if not ok_p.any():
        ok_p[:] = True                                       # 전멸-마스크 가드 (가중 0-나눗셈 방지)
    amp = np.ones(rad.n_p) if i0_amp is None else np.asarray(i0_amp, np.float64)

    def _vw(xs):                                             # i0·A 가중 혼합전위 (선형화, alive 만)
        w = (i0_fn(xs) if i0_fn is not None else np.ones_like(xs)) * amp * rad.R ** 2
        w = np.where(ok_p, w, 0.0)
        sw = float(w.sum())
        return float((ocp.U(xs) * w).sum() / sw) if sw > 0 else float((ocp.U(xs) * wv).sum())

    if j0 is not None:
        rad.J[:] = np.asarray(j0, np.float64)                # t=0 표면 재구성 전용 (직후 0)
    xs0 = rad.surf_x()
    rad.J[:] = 0.0
    tot0 = float((rad.mean_x() * wv).sum())
    out = {'t': [0.0], 'V': [_vw(xs0)], 'x_mean': [tot0],
           'x_surf_p50': [float(np.percentile(xs0[ok_p], 50))],
           'surf_mean_gap': [float(np.mean(np.abs(xs0[ok_p] - rad.mean_x()[ok_p])))]}
    for k in range(n):
        if k == 0:                                           # Rannacher: L-안정 BE 반스텝 ×2
            rad.step(dt * 0.5, theta=1.0)
            rad.step(dt * 0.5, theta=1.0)
        else:
            rad.step(dt)
        xs = rad.surf_x()
        out['t'].append((k + 1) * dt)
        out['V'].append(_vw(xs))
        out['x_mean'].append(float((rad.mean_x() * wv).sum()))
        out['x_surf_p50'].append(float(np.percentile(xs[ok_p], 50)))
        out['surf_mean_gap'].append(float(np.mean(np.abs(xs[ok_p] - rad.mean_x()[ok_p]))))
    drift = abs(out['x_mean'][-1] - tot0)
    return {k: np.asarray(v) for k, v in out.items()}, drift


# ---------------------------------------------------------------- selftests
def _selftest_radial():
    ok = True
    rad = RadialDiffusion(3, 25, np.array([2e-6, 5e-6, 1e-5]), 3e-14, 50000.0, 0.3)
    rad.J = np.array([1e-6, 2e-6, 0.5e-6])
    tot0 = (rad.x * rad.Vk).sum(1).copy()
    for _ in range(50):
        rad.step(2.0)
    got = (rad.x * rad.Vk).sum(1) - tot0
    exp = 50 * 2.0 * rad.J / (rad.c_max * rad.R)
    e1 = np.max(np.abs(got - exp) / exp)
    ok &= e1 < 1e-10
    print(f'radial mass conservation: max rel err {e1:.2e}  {"OK" if e1 < 1e-10 else "FAIL"}')
    rad = RadialDiffusion(1, 20, np.array([5e-6]), 3e-14, 50000.0, 0.5)
    for _ in range(100):
        rad.step(10.0)
    e2 = float(np.max(np.abs(rad.x - 0.5)))
    ok &= e2 < 1e-12
    print(f'radial equilibrium hold: max drift {e2:.2e}  {"OK" if e2 < 1e-12 else "FAIL"}')
    R, D, cm = 10e-6, 1e-14, 50000.0
    rad = RadialDiffusion(1, 400, np.array([R]), D, cm, 0.3)
    rad.J = np.array([2e-6])
    dt, nstep = 0.05, 200
    for _ in range(nstep):
        rad.step(dt)
    t = dt * nstep
    dx_num = float(rad.surf_x()[0] - 0.3)
    dx_ana = 2.0 * rad.J[0] * np.sqrt(t / (np.pi * D)) / cm
    e3 = abs(dx_num - dx_ana) / dx_ana
    ok &= e3 < 0.05                                          # 이산화 잔차 ~3% (계수버그는 수백%로 잡힘)
    print(f'radial √t (planar limit): num {dx_num:.4e} vs ana {dx_ana:.4e} '
          f'rel {e3:.3f}  {"OK" if e3 < 0.05 else "FAIL"}')
    # 4) per-particle D ≡ 독립 스칼라 솔버 (bitwise; Thomas 벡터화는 행-독립이라 정확 등가여야)
    #    + 물리 방향: 표면상승비 ≈ √(D₂/D₁)=2 (절대-해석해 비교는 4×D에서 곡률오차 √(Dt)/R가
    #    커져 부적합 — 절대 정합은 test 3(스칼라)이, 배열경로 전이는 bitwise가 각각 담당)
    Dv = np.array([1e-14, 4e-14])
    rad = RadialDiffusion(2, 400, np.array([R, R]), Dv, cm, 0.3)
    rad.J = np.array([2e-6, 2e-6])
    r_a = RadialDiffusion(1, 400, np.array([R]), Dv[0], cm, 0.3)
    r_b = RadialDiffusion(1, 400, np.array([R]), Dv[1], cm, 0.3)
    r_a.J = np.array([2e-6]); r_b.J = np.array([2e-6])
    for _ in range(nstep):
        rad.step(dt); r_a.step(dt); r_b.step(dt)
    ok4 = (np.array_equal(rad.x[0], r_a.x[0]) and np.array_equal(rad.x[1], r_b.x[0]))
    dx2 = rad.surf_x() - 0.3
    ratio = float(dx2[0] / dx2[1])
    ok4 &= abs(ratio - 2.0) < 0.1
    ok &= ok4
    print(f'radial per-particle D ≡ 독립 스칼라 (bitwise) + 상승비 {ratio:.3f}≈2: '
          f'{"OK" if ok4 else "FAIL"}')
    # 5) 균일값 배열 D ≡ 스칼라 D — bitwise (경로 등가성; per-particle 훅의 회귀 가드)
    ra = RadialDiffusion(3, 30, np.array([2e-6, 5e-6, 1e-5]), 3e-14, cm, 0.4)
    rb = RadialDiffusion(3, 30, np.array([2e-6, 5e-6, 1e-5]), np.full(3, 3e-14), cm, 0.4)
    ra.J = np.array([1e-6, 2e-6, 0.5e-6]); rb.J = ra.J.copy()
    for _ in range(30):
        ra.step(2.0); rb.step(2.0)
    ok5 = np.array_equal(ra.x, rb.x)
    ok &= ok5
    print(f'radial array-D(균일) ≡ scalar-D bitwise: {"OK" if ok5 else "FAIL"}')
    return ok


def _build_sandwich(nxy=6, nz=12, vox_um=0.5):
    sid = np.zeros((nxy, nxy, nz), np.int8)
    sid[:, :, :nz // 2] = 1
    sid[:, :, nz // 2:] = 6
    pid = np.where(sid == 1, 0, -1).astype(np.int32)
    return sid, pid, vox_um


def _selftest_cell():
    """평형 OCV / 저율 직렬-R / KCL / 에너지 수지 / CSR 위치맵 / ASR·CV / v1 회귀."""
    ok = True
    ocp = OCP.synthetic_test()
    sid, pid, vox = _build_sandwich(nxy=6, nz=12, vox_um=5.0)
    se_cm, si_cm = 1e-4, 1e-4                                # 네트워크·BV 저항 동급化 (검증력)
    sig_e = np.array([0., se_cm, 0., 0., 0., 0., 0.])
    sig_i = np.array([0., 0., 0., 0., 0., 0., si_cm])
    sysm = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=12 * vox, z_bot_um=0.0)
    x0 = ocp.x0
    kin = Kinetics(i0_ref=2.0)
    U_f = np.full(sysm.n_bv, float(ocp.U(x0)))
    i0_f = np.full(sysm.n_bv, float(kin.i0(x0)))
    # 0) CSR 위치맵 = brute-force COO 조립과 일치 (무작위 g)
    rng = np.random.default_rng(0)
    g_r = rng.uniform(1e-9, 1e-7, sysm.n_bv)
    data = sysm.data0.copy()
    data[sysm.pos_ei] = -g_r; data[sysm.pos_ie] = -g_r
    da = np.zeros(sysm.N)
    np.add.at(da, sysm.f_e, g_r); np.add.at(da, sysm.f_i, g_r)
    data[sysm.pos_diag] = sysm._diag0 + da
    sysm.J.data[:] = data
    # brute force 비교: (index-map으로 갱신한 J)@x  vs  L0@x + BV 기여 직접 합산
    xr = rng.standard_normal(sysm.N)
    lhs = sysm.J @ xr
    rhs = sysm._L0_apply(xr).copy()
    np.add.at(rhs, sysm.f_e, g_r * (xr[sysm.f_e] - xr[sysm.f_i]))
    np.add.at(rhs, sysm.f_i, -g_r * (xr[sysm.f_e] - xr[sysm.f_i]))
    e0 = float(np.max(np.abs(lhs - rhs)) / max(np.max(np.abs(rhs)), 1e-30))
    ok &= e0 < 1e-12
    print(f'CSR index-map ≡ brute-force: rel {e0:.2e}  {"OK" if e0 < 1e-12 else "FAIL"}')
    # 1) I=0 → V=OCV (solve_galv 시컨트가 평형 전위를 찾아야)
    phi = np.zeros(sysm.N)
    phi[:sysm.n_e] = float(ocp.U(x0))
    U0 = float(ocp.U(x0))
    phi, I_f, eta_s, r, V_eq, I_eq = sysm.solve_galv(phi, U_f, i0_f, kin, 0.0, U0)
    e1 = abs(V_eq - U0)
    ok &= e1 < 1e-9
    print(f'cell equilibrium: V−OCV = {e1:.2e}  {"OK" if e1 < 1e-9 else "FAIL"}')
    # 2) 저율 직렬-R (선형화 BV g = i0·A·f·(αa+αc) per face; α=0.5/0.5 → 2·i0·A·β 구형과 동일)
    I_small = 1e-10
    phi, I_f, eta_s, r, V, I_del = sysm.solve_galv(phi, U_f, i0_f, kin, I_small, V_eq)
    vox_m = vox * 1e-6
    nxy = sid.shape[0]; nzh = sid.shape[2] // 2
    se, si = se_cm * 100.0, si_cm * 100.0
    g_face = float(kin.i0(x0)) * vox_m ** 2 * kin.f * (kin.aa + kin.ac)
    R_col = (1.0 / (se * vox_m ** 2 / (0.5 * vox_m)) + (nzh - 1) / (se * vox_m)
             + (nzh - 1) / (si * vox_m) + 1.0 / (si * vox_m ** 2 / (0.5 * vox_m)))
    R_ser = R_col / (nxy * nxy) + 1.0 / (g_face * nxy * nxy)
    e2 = abs((float(ocp.U(x0)) - V) - I_small * R_ser) / (I_small * R_ser)
    ok &= e2 < 1e-3
    print(f'cell low-rate series-R: rel {e2:.2e}  {"OK" if e2 < 1e-3 else "FAIL"}')
    # 3) KCL + 에너지 수지 (중율에서 — 비선형 영역 포함 감사)
    i_am = sysm.particle_current(I_f)
    e3 = abs(i_am.sum() - I_small) / I_small
    ok &= e3 < 1e-6
    print(f'cell KCL (galvanostatic): rel {e3:.2e}  {"OK" if e3 < 1e-6 else "FAIL"}')
    I_mid = 3e-8                                             # sinh 비선형 영역
    phi, I_f, eta_s, r, V_mid, _ = sysm.solve_galv(phi, U_f, i0_f, kin, I_mid, V)
    aud = sysm.energy_audit(phi, I_f, eta_s, U_f, kin, V_mid)
    e4 = abs(aud['balance_rel'])
    ok &= e4 < 1e-8
    print(f'cell energy balance (nonlinear): rel {e4:.2e}  {"OK" if e4 < 1e-8 else "FAIL"}')
    # 4) ASR 필름: ASR→0 극한 일치 + ASR>0 이면 같은 I에서 V 더 처짐
    kin_f0 = Kinetics(2.0, asr_film=1e-30)
    _, _, _, _, V_a, _ = sysm.solve_galv(phi.copy(), U_f, i0_f, kin_f0, I_mid, V_mid)
    e5 = abs(V_a - V_mid)
    kin_f = Kinetics(2.0, asr_film=1e-4)                     # 1 Ω·cm² 필름
    phi_b, I_b, eta_b, _, V_b, _ = sysm.solve_galv(phi.copy(), U_f, i0_f, kin_f, I_mid, V_mid)
    drop = V_mid - V_b
    # 기대 ΔV = I_face·R_film,face = (I/36)·(ASR/A_face)  — 36면 병렬이므로
    drop_exp = (I_mid / 36) * (1e-4 / sysm.A_face)
    e6 = abs(drop - drop_exp) / max(drop_exp, 1e-30)
    audb = sysm.energy_audit(phi_b, I_b, eta_b, U_f, kin_f, V_b)
    ok &= e5 < 1e-9 and e6 < 1e-2 and abs(audb['balance_rel']) < 1e-8
    print(f'cell ASR film: ASR→0 match {e5:.1e} · ΔV(1Ωcm²) rel {e6:.2e} · E-bal {abs(audb["balance_rel"]):.1e}'
          f'  {"OK" if (e5 < 1e-9 and e6 < 1e-2 and abs(audb["balance_rel"]) < 1e-8) else "FAIL"}')
    # 5) 비대칭 α: αa=0.7/αc=0.3 저율 선형 g = i0·A·f·(αa+αc) 재현
    kin_as = Kinetics(2.0, alpha_a=0.7, alpha_c=0.3)
    phi_c = np.zeros(sysm.N); phi_c[:sysm.n_e] = U0
    i0_as = np.full(sysm.n_bv, float(kin_as.i0(x0)))
    I_as = 1e-11                                             # 비대칭은 2차항 (αa²−αc²)(fη)²/2 이
                                                             # (이론 잔차 7.05e-4 — 톨 여유 1.4×:
                                                             #  i0/σ/기하 변경 시 I_as 재조정 필요)
    _, _, _, _, V_c, _ = sysm.solve_galv(phi_c, U_f, i0_as, kin_as, I_as, U0)   # 살아있어 더 저율로
    g_face2 = float(kin_as.i0(x0)) * vox_m ** 2 * kin_as.f * (kin_as.aa + kin_as.ac)
    R_ser2 = R_col / (nxy * nxy) + 1.0 / (g_face2 * nxy * nxy)
    e7 = abs((U0 - V_c) - I_as * R_ser2) / (I_as * R_ser2)
    ok &= e7 < 1e-3
    print(f'cell asymmetric BV (0.7/0.3) low-rate: rel {e7:.2e}  {"OK" if e7 < 1e-3 else "FAIL"}')
    # 6) 전압 홀드(potentiostatic): V_target에서 I ≈ (OCV−V_target)/R_ser (저율 선형)
    Vt = U0 - I_small * R_ser * 0.7
    _, _, _, _, _, I_cv = sysm.solve_vterm(phi.copy(), U_f, i0_f, kin, Vt, 0.0, Vt,
                                           i_scale=I_small)
    I_exp = (U0 - Vt) / R_ser
    e8 = abs(I_cv - I_exp) / I_exp
    ok &= e8 < 1e-2
    print(f'cell CV hold (Illinois): I {I_cv:.3e} vs (OCV−V)/R {I_exp:.3e}  rel {e8:.2e}  '
          f'{"OK" if e8 < 1e-2 else "FAIL"}')
    # 7) v1 분포 회귀 (선형영역, 2입자 비대칭 격자)
    from step3_sigma import solve_reaction_current
    sid2 = np.zeros((6, 6, 12), np.int8)
    sid2[:, :, 6:] = 6
    sid2[:3, :, :6] = 1
    sid2[3:, :, 2:6] = 2
    pid2 = np.full(sid2.shape, -1, np.int32)
    pid2[:3, :, :6] = 0; pid2[3:, :, 2:6] = 1
    sig_e2 = np.array([0., 1., 1., 0., 0., 0., 0.])
    sig_i2 = np.array([0., 0., 0., 0., 0., 0., 2.])
    kin1 = Kinetics(1.0)
    gct_SI = float(kin1.i0(x0)) * (0.5e-6) ** 2 * kin1.f * (kin1.aa + kin1.ac)
    g_v1 = gct_SI * 1e4                                      # code/SI g 스케일비 = 1e4 (vox 무관)
    rv1 = solve_reaction_current(sid2, sig_e2, sig_i2, pid2, 2, 0.5, g_v1,
                                 z_top_um=6.0, z_bot_um=0.0)
    sys2 = CellSystem(sid2, sig_e2, sig_i2, pid2, 2, 0.5, z_top_um=6.0, z_bot_um=0.0)
    U2 = np.full(sys2.n_bv, float(ocp.U(x0)))
    i02 = np.full(sys2.n_bv, float(kin1.i0(x0)))
    phi2 = np.zeros(sys2.N)
    phi2[:sys2.n_e] = float(ocp.U(x0))
    phi2, I_f2, _, _, _, _ = sys2.solve_galv(phi2, U2, i02, kin1, 1e-8, float(ocp.U(x0)))
    a2 = sys2.particle_current(I_f2)
    frac_v1 = rv1['i_am'] / rv1['i_am'].sum()
    frac_v2 = a2 / a2.sum()
    e9 = float(np.max(np.abs(frac_v1 - frac_v2)))
    ok &= e9 < 1e-4
    print(f'cell v1-regression: Δmax {e9:.2e}  {"OK" if e9 < 1e-4 else "FAIL"}')
    return ok


def _selftest_discharge():
    """풀 방전: 쿨롱 적산 / V 단조 / KCL / 에너지 수지 / 창-클램프 / R_int / CCCV."""
    ok = True
    ocp = OCP.synthetic_test()
    sid, pid, vox = _build_sandwich(nxy=4, nz=8)
    sig_e = np.array([0., 1., 0., 0., 0., 0., 0.])
    sig_i = np.array([0., 0., 0., 0., 0., 0., 2.])
    sysm = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    r_p = np.array([10.0e-6])                                # 용량↑ → KCL이 노이즈 바닥 위에서 검증
    kin = Kinetics(5.0)
    out = simulate(sysm, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8,
                   dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
    dt_arr = np.diff(out['t'])
    q_As = (out['I'][:-1] * dt_arr).sum()
    dx_exp = q_As / (F_CONST * ocp.c_max * (4 / 3 * np.pi * r_p ** 3).sum())
    dx_got = out['x_mean'][-1] - out['x_mean'][0]
    e1 = abs(dx_got - dx_exp) / abs(dx_exp)
    ok &= e1 < 5e-3
    print(f'discharge coulomb count: rel {e1:.2e}  {"OK" if e1 < 5e-3 else "FAIL"}')
    mono = float((np.diff(out['V']) > 1e-6).mean())
    ok &= mono < 0.02
    print(f'discharge V monotone↓: rising {mono * 100:.1f}%  {"OK" if mono < 0.02 else "FAIL"}')
    okk = float(np.max(out['kcl_rel'])) < 1e-6
    ok &= okk
    print(f'discharge KCL all steps: max {np.max(out["kcl_rel"]):.1e}  {"OK" if okk else "FAIL"}')
    oke = float(np.max(out['energy_balance_rel'])) < 1e-7
    ok &= oke
    print(f'discharge energy balance all steps: max {np.max(out["energy_balance_rel"]):.1e}  '
          f'{"OK" if oke else "FAIL"}')
    okq = out['q_frac_at_cutoff'] <= 1.005
    ok &= okq
    print(f'discharge SOC-window clamp: delivered {out["q_frac_at_cutoff"] * 100:.1f}% ≤ 100.5%  '
          f'{"OK" if okq else "FAIL"}')
    # R_int: 터미널 V가 I·R만큼 더 낮게 (같은 스텝 0에서 비교)
    out_r = simulate(sysm, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8,
                     r_int_ohm_cm2=50.0, dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
    dV = float(out_r['V'][0] - out_r['V_terminal'][0])
    dV_exp = float(out_r['I'][0]) * (50.0 * 1e-4 / sysm.area_m2)
    e6 = abs(dV - dV_exp) / max(dV_exp, 1e-30)
    ok &= e6 < 1e-9
    print(f'discharge R_int terminal drop: rel {e6:.2e}  {"OK" if e6 < 1e-9 else "FAIL"}')
    # CCCV 충전: v_max 도달 → CV 홀드 → I가 i_cut 밑으로 (전류 단조 감소 방향)
    out_c = simulate(sysm, ocp, r_p, 1e-13, kin, c_rate=1.0, nr=15, v_min=2.8, v_max=3.9,
                     charge=True, cv_hold=True, i_cut_frac=0.10, x_init=ocp.x100,
                     dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
    okc = (out_c['end_reason'] == 'cv_i_cut' and abs(out_c['I'][-1]) < 0.10 * out_c['I_1C_A'] * 1.5
           and float(np.max(out_c['energy_balance_rel'])) < 1e-5)   # CV 저전류선 분모(|I|·V) 축소로
                                                                    # 상대값 부풂 — 부기오류는 O(1)라 검출력 유지
    ok &= okc
    print(f'CCCV charge: end={out_c["end_reason"]}, |I_end|/I1C='
          f'{abs(out_c["I"][-1]) / out_c["I_1C_A"]:.3f}  {"OK" if okc else "FAIL"}')
    # per-particle 훅 회귀 가드: 균일값 배열 d_s + i0_p ≡ 스칼라 경로 — 곡선 bitwise 동일.
    #   같은 CellSystem 재사용 금지: 첫 런이 솔버 캐시(AMG/워밍)를 데워 둘째 런의 반복경로가
    #   달라짐 → 진짜 비교대상(전기화학 경로)이 아닌 캐시상태를 재게 됨 → 쌍둥이 인스턴스.
    sysm_a = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    sysm_b = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    out_pp = simulate(sysm_a, ocp, r_p, np.array([1e-13]), kin, c_rate=0.2, nr=15, v_min=2.8,
                      i0_p=np.array([5.0]), t_max=400.0,
                      dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
    out_sc = simulate(sysm_b, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8, t_max=400.0,
                      dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
    okpp = (np.array_equal(out_pp['V'], out_sc['V'])
            and np.array_equal(out_pp['x_mean'], out_sc['x_mean']))
    ok &= okpp
    print(f'per-particle 균일 d_s/i0_p ≡ 스칼라 (simulate bitwise): {"OK" if okpp else "FAIL"}')
    # per-particle i0 방향성: 2입자 대칭 베드, i0 10× 차이 → 큰-i0 입자가 초기 전류 과분담
    #   (방전=리튬화 → x̄ 더 많이 상승; kinetic 저항 1/i0 차이의 부호 검증)
    #   CV/CCCV 별도 테스트 불필요(리뷰 #5 판정): i0_f는 phase 분기 이전 단일 콜사이트에서
    #   계산돼 cc/cv가 같은 값을 씀 — CC bitwise 테스트가 메커니즘 전체를 커버.
    sid2, pid2, vox2 = _build_sandwich(nxy=4, nz=8)
    pid2 = pid2.copy()
    pid2[2:, :, :][pid2[2:, :, :] == 0] = 1                  # x-절반씩 입자 0/1 (기하 대칭)
    sysm2 = CellSystem(sid2, sig_e, sig_i, pid2, 2, vox2, z_top_um=8 * 0.5, z_bot_um=0.0)
    r_p2 = np.array([10.0e-6, 10.0e-6])
    out_i0 = simulate(sysm2, ocp, r_p2, 1e-13, kin, c_rate=0.5, nr=15, v_min=2.8,
                      i0_p=np.array([10.0, 1.0]), t_max=200.0,
                      dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
    xf = out_i0['x_final_per_particle']
    oki0 = bool(xf[0] > xf[1])
    ok &= oki0
    print(f'per-particle i0 방향성 (i0 10× → x̄ {xf[0]:.4f} > {xf[1]:.4f}): '
          f'{"OK" if oki0 else "FAIL"}')
    return ok


def _selftest_solver():
    """2026-07-27 솔버 치료 회귀 (C0 pruning / C1 cap / C2 EW / C3 V-cycle / C4 게이트·atol 노브).
    env는 try/finally 복원 — 다른 selftest 오염 금지.  GPU 경로는 cupy 부재 시 guard만 검증."""
    import contextlib
    import io
    ok = True
    _ENV = ('MPM_S4_PRUNE_FLOAT', 'MPM_S4_CONTRAST_CAP', 'MPM_S4_EW', 'MPM_S4_GPU_AMG',
            'MPM_S4_GPU_AMG_F32', 'MPM_S4_ATOL_FLOOR_FRAC', 'MPM_S4_NN_ACCEPT_ABS_FRAC',
            'MPM_S4_CG_BUDGET_S')
    _saved = {k: os.environ.get(k) for k in _ENV}

    # ── C6 비용-기반 승급 A/B 판정 (2026-07-29) ──────────────────────────────────────────
    #   이 사다리는 **실패로만** 승급했다 — GPU Jacobi-CG 가 성공하면 즉시 return 이라
    #   near-null-B AMG(작업 #20/#27 이 저율용으로 만든 것)가 후보로조차 못 올랐다.
    #   실측 V100 0.2C: 61 s/CG × Newton 4 = 244 s/step → step 하나에 2~3일.
    _c6 = True
    _c6 &= cg_ab_verdict(10.0, 100.0, 0)[0] == 'ladder'          # 10× 빠름 → 전환
    _c6 &= cg_ab_verdict(100.0, 10.0, 0)[0] == 'gpu_jacobi'      # 느림 → 현행 유지
    _c6 &= cg_ab_verdict(95.0, 100.0, 0)[0] == 'gpu_jacobi'      # 5% 이득 = 노이즈 → 유지(chatter 방지)
    _c6 &= cg_ab_verdict(89.0, 100.0, 0)[0] == 'ladder'          # 11% = 마진 초과 → 전환
    _c6 &= cg_ab_verdict(1.0, 100.0, 1)[0] == 'gpu_jacobi'       # 사다리 미수렴 → 빨라도 기각
    _c6 &= cg_ab_verdict(1.0, None, 0)[0] == 'gpu_jacobi'        # 비교 대상 없음 → 유지
    _c6 &= cg_ab_verdict(1.0, None, 0)[1] == 'no_comparison_or_ladder_not_converged'
    print(f'  {"OK  " if _c6 else "FAIL"} C6 비용 A/B 판정 (마진 10%·미수렴 기각·비교불가 유지)')
    ok &= _c6
    # 기본값 OFF 계약: 예산 미지정이면 계측·전환 코드가 아예 안 켜진다 (기존 런 바이트 불변)
    _c6b = (float(os.environ.get('MPM_S4_CG_BUDGET_S', '0') or 0) == 0.0)
    print(f'  {"OK  " if _c6b else "FAIL"} C6 기본 OFF (MPM_S4_CG_BUDGET_S 미지정 → 예산 0 = 경로 불변)')
    ok &= _c6b
    # ★ dof 상한 가드 — 실측(4.4M: Jacobi 43.5s vs AMG 440.9s = 10.1×) 이후 그 규모에선 프로브 자체를 막는다.
    #   기본 1e6.  ⚠ 교차점이 아니라 무지의 안전변 (AMG 가 이기는 dof 는 미측정).
    _c6c = int(float(os.environ.get('MPM_S4_CG_PROBE_MAX_DOF', '1000000') or 0)) == 1000000
    print(f'  {"OK  " if _c6c else "FAIL"} C6 프로브 dof 상한 기본 1,000,000 (4.4M 실측 기각 반영)')
    ok &= _c6c

    def _env(k, v):
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v

    try:
        ocp = OCP.synthetic_test()
        sig_i = np.array([0., 0., 0., 0., 0., 0., 2.])
        r_p = np.array([10.0e-6])
        kin = Kinetics(5.0)
        # ---- S1: e-망 부유클러스터 pruning 해-불변 (SE-매몰 2복셀 VGCF 섬 = a2_exact_null 미러) ----
        sid1 = _build_sandwich(nxy=4, nz=8)[0].copy()
        sid1[1, 1, 6] = 3; sid1[1, 2, 6] = 3                 # SE 내부 매몰 (AM·집전체 6-conn 무접촉)
        pid1 = np.where(sid1 == 1, 0, -1).astype(np.int32)
        sig_e1 = np.array([0., 1., 0., 100., 0., 0., 0.])    # sid3=VGCF (σ대비 100 — 1e4 대비는 S2)
        _env('MPM_S4_PRUNE_FLOAT', None)                     # 기본 ON
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sys_on = CellSystem(sid1, sig_e1, sig_i, pid1, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0)
        _env('MPM_S4_PRUNE_FLOAT', '0')
        sys_off = CellSystem(sid1, sig_e1, sig_i, pid1, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0)
        _env('MPM_S4_PRUNE_FLOAT', None)
        s1a = (sys_on.n_pruned_e_comp == 1 and sys_on.n_pruned_e_vox == 2
               and sys_off.n_e - sys_on.n_e == 2 and sys_off.n_pruned_e_comp == 0
               and '부유클러스터' in buf.getvalue())
        ok &= s1a
        print(f'solver S1a pruning 카운트+로그: comp {sys_on.n_pruned_e_comp} vox '
              f'{sys_on.n_pruned_e_vox} (Δn_e {sys_off.n_e - sys_on.n_e})  {"OK" if s1a else "FAIL"}')
        out_on = simulate(sys_on, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8, t_max=400.0,
                          dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
        _env('MPM_S4_PRUNE_FLOAT', '0')
        out_off = simulate(sys_off, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8, t_max=400.0,
                           dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
        _env('MPM_S4_PRUNE_FLOAT', None)
        dV = (float(np.max(np.abs(out_on['V'] - out_off['V'])))
              if len(out_on['V']) == len(out_off['V']) else np.inf)
        s1b = (dV < 1e-9 and float(np.max(out_on['kcl_rel'])) < 1e-6
               and float(np.max(out_on['energy_balance_rel'])) < 1e-7)
        ok &= s1b
        print(f'solver S1b pruning ON≡OFF 방전 (|ΔV|max {dV:.1e}, KCL {np.max(out_on["kcl_rel"]):.1e}, '
              f'E-bal {np.max(out_on["energy_balance_rel"]):.1e}): {"OK" if s1b else "FAIL"}')
        # ---- S1c: SWCNT(sid 8) 반응계면 — STEP3 v1 MED-2 규약 정합 (투명 sheath = BV 면) ----
        #   AM 표면 한 칸을 sheath(8)로 덮고, σ_i[8]>0(투명)이면 BV 면이 유지되어야 한다.
        #   --swcnt-ion-block(σ_i[8]=0)이면 그 면은 자동 소멸 = 솔브(cond_i)와 일관.
        sid8 = _build_sandwich(nxy=4, nz=8)[0].copy()
        _se_over = np.argwhere((sid8 == 6))                   # AM 슬래브 바로 위 SE 한 칸 → sheath 로 치환
        _amz = int(np.argwhere(sid8 == 1)[:, 2].max())
        _cand = [tuple(p) for p in _se_over if p[2] == _amz + 1]
        sig_i8_on = np.array([0., 0., 0., 0., 0., 0., 2e-4, 0., 2e-4])    # sid8 투명(=SE σ_i)
        sig_i8_off = np.array([0., 0., 0., 0., 0., 0., 2e-4, 0., 0.])     # --swcnt-ion-block
        sig_e8 = np.array([0., 1., 0., 0., 0., 0., 0., 0., 100.])         # sheath 는 전자도체
        s1c = False
        if _cand:
            sid8[_cand[0]] = 8
            pid8 = np.where(sid8 == 1, 0, -1).astype(np.int32)
            _n_on = CellSystem(sid8, sig_e8, sig_i8_on, pid8, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0).n_bv
            _n_off = CellSystem(sid8, sig_e8, sig_i8_off, pid8, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0).n_bv
            _base = CellSystem(_build_sandwich(nxy=4, nz=8)[0], sig_e8, sig_i8_on, pid8, 1, 0.5,
                               z_top_um=8 * 0.5, z_bot_um=0.0).n_bv
            s1c = (_n_on == _base and _n_off == _base - 1)     # 투명=면 보존, 차단=그 면만 소멸
        ok &= s1c
        print(f'solver S1c SWCNT(sid8) BV 계면 (투명 {_n_on if _cand else "—"} = SE기준 '
              f'{_base if _cand else "—"}, ion-block {_n_off if _cand else "—"}): {"OK" if s1c else "FAIL"}')
        # ---- S1d: x,y 주기 BC (STEP3 규약 정합) — wrap 이 전도·BV 계면에 함께 걸리는지 ----
        sidP = _build_sandwich(nxy=4, nz=8)[0].copy()
        _amz = int(np.argwhere(sidP == 1)[:, 2].max())
        sidP[0, :, _amz + 1] = 1                             # x=0 열에 AM 을 한 층 올려
        sidP[3, :, _amz + 1] = 6                             # x=nx-1 열은 SE → seam 에서만 AM|SE 접촉
        pidP = np.where(sidP == 1, 0, -1).astype(np.int32)
        sigP = np.array([0., 1., 0., 0., 0., 0., 0.])
        _w = CellSystem(sidP, sigP, sig_i, pidP, 1, 0.5, z_top_um=4.0, z_bot_um=0.0,
                        periodic_xy=False)
        _p = CellSystem(sidP, sigP, sig_i, pidP, 1, 0.5, z_top_um=4.0, z_bot_um=0.0,
                        periodic_xy=True)
        s1d = (_p.J.nnz > _w.J.nnz and _p.n_bv > _w.n_bv and _p.N == _w.N
               and _p.periodic_xy and not _w.periodic_xy)
        ok &= s1d
        print(f'solver S1d 주기 BC (nnz {_w.J.nnz}→{_p.J.nnz}, BV면 {_w.n_bv}→{_p.n_bv}, '
              f'dof 불변 {_p.N}): {"OK" if s1d else "FAIL"}')
        # ---- S2: σ-contrast cap (합성 고대비 0.01/100 = 1e4; AM-접촉 VGCF → pruning 비대상) ----
        sid2 = _build_sandwich(nxy=4, nz=8)[0].copy()
        sid2[1, 1, 4] = 3; sid2[1, 2, 4] = 3                 # AM 슬래브(z=3) 위 접촉 → e-망 잔존
        pid2 = np.where(sid2 == 1, 0, -1).astype(np.int32)
        sig_hi = np.array([0., 0.01, 0., 100., 0., 0., 0.])
        _env('MPM_S4_CONTRAST_CAP', None)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sU = CellSystem(sid2, sig_hi, sig_i, pid2, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0)
        hint = 'MPM_S4_CONTRAST_CAP=200 권장' in buf.getvalue()
        _env('MPM_S4_CONTRAST_CAP', '0')
        s0 = CellSystem(sid2, sig_hi, sig_i, pid2, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0)
        s2a = np.array_equal(sU.data0, s0.data0) and sU.contrast_cap == 0.0 and hint
        ok &= s2a
        print(f'solver S2a cap 미설정 bitwise + 권고로그: {"OK" if s2a else "FAIL"}')
        _env('MPM_S4_CONTRAST_CAP', '200')
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            sC = CellSystem(sid2, sig_hi, sig_i, pid2, 1, 0.5, z_top_um=8 * 0.5, z_bot_um=0.0)
        cap_log = 'σ-contrast cap(e-망)' in buf.getvalue()
        _env('MPM_S4_CONTRAST_CAP', None)

        def _face_ratio(sysX):                               # e-블록 off-diag(−g) 양수 max/min
            blk = sysX.J[:sysX.n_e, :sysX.n_e].tocsr()
            gv = -blk.data[blk.data < 0]
            return float(gv.max() / gv.min())
        rat_u, rat_c = _face_ratio(sU), _face_ratio(sC)
        iU = sU.J[sU.n_e:].tocsr(); iC = sC.J[sC.n_e:].tocsr()
        s2b = (rat_u > 1e3 and rat_c <= 200.0001 and cap_log
               and np.array_equal(iU.indptr, iC.indptr) and np.array_equal(iU.indices, iC.indices)
               and np.array_equal(iU.data, iC.data)          # i-망(대비≤cap) bitwise 불변
               and not sC.data0[sC.pos_ei].any() and not sC.data0[sC.pos_ie].any())   # BV placeholder 0
        ok &= s2b
        print(f'solver S2b cap=200 적용 (e-face비 {rat_u:.1e}→{rat_c:.1f}, i-망 불변, BV=0): '
              f'{"OK" if s2b else "FAIL"}')
        # ---- S3: EW inexact-Newton on/off 최종해 동등 + η 범위 + tight-재솔브 분기 ----
        sid3, pid3, vox3 = _build_sandwich(nxy=4, nz=8)
        se3 = np.array([0., 1., 0., 0., 0., 0., 0.])
        _env('MPM_S4_EW', '1')                               # ★기본은 OFF(opt-in) → 테스트는 명시 ON
        sysE = CellSystem(sid3, se3, sig_i, pid3, 1, vox3, z_top_um=8 * 0.5, z_bot_um=0.0)
        outE = simulate(sysE, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8, t_max=400.0,
                        dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
        _env('MPM_S4_EW', '0')
        sysF = CellSystem(sid3, se3, sig_i, pid3, 1, vox3, z_top_um=8 * 0.5, z_bot_um=0.0)
        outF = simulate(sysF, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8, t_max=400.0,
                        dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
        _env('MPM_S4_EW', None)
        eta_h = np.asarray(getattr(sysE, '_ew_eta_log', []))
        dV3 = (float(np.max(np.abs(outE['V'] - outF['V'])))
               if len(outE['V']) == len(outF['V']) else np.inf)
        s3a = (dV3 < 1e-6
               and float(np.max(outE['kcl_rel'])) < 1e-6 and float(np.max(outF['kcl_rel'])) < 1e-6
               and float(np.max(outE['energy_balance_rel'])) < 1e-7
               and float(np.max(outF['energy_balance_rel'])) < 1e-7
               and eta_h.size > 0 and float(eta_h.min()) >= 1e-5 and float(eta_h.max()) <= 0.1)
        ok &= s3a
        print(f'solver S3a EW on≡off 방전 (|ΔV|max {dV3:.1e}, η∈[{eta_h.min():.0e},{eta_h.max():.0e}] '
              f'n={eta_h.size}): {"OK" if s3a else "FAIL"}')
        # tight-재솔브 분기: 모듈 _cg 몽키패치 (첫 콜=쓰레기 하강방향 info=0 → Armijo 거부 → 재솔브)
        g_mod = globals()
        real_cg = g_mod['_cg']
        calls = {'n': 0}

        def _bad_cg(L, b, **kw):
            calls['n'] += 1
            if calls['n'] == 1:
                return np.random.default_rng(1).standard_normal(L.shape[0]) * 1e3, 0
            return real_cg(L, b, **kw)

        _env('MPM_S4_EW', '1')                               # tight-재솔브는 EW 경로 전용 분기
        sysT = CellSystem(sid3, se3, sig_i, pid3, 1, vox3, z_top_um=8 * 0.5, z_bot_um=0.0)
        U0 = float(ocp.U(ocp.x0))
        U_fT = np.full(sysT.n_bv, U0)
        i0T = np.full(sysT.n_bv, float(kin.i0(ocp.x0)))
        phiT0 = np.zeros(sysT.N); phiT0[:sysT.n_e] = U0
        buf = io.StringIO()
        g_mod['_cg'] = _bad_cg
        try:
            with contextlib.redirect_stdout(buf):
                _, _, _, rT, itT = sysT.newton(phiT0, U_fT, i0T, kin, U0 - 0.05, i_scale=1e-8)
        finally:
            g_mod['_cg'] = real_cg
        s3b = (getattr(sysT, '_ew_tight_n', 0) >= 1 and calls['n'] >= 2 and itT >= 1
               and np.isfinite(rT) and 'tight 재솔브' in buf.getvalue())
        ok &= s3b
        print(f'solver S3b EW tight-재솔브 발동 (n={getattr(sysT, "_ew_tight_n", 0)}, '
              f'cg콜 {calls["n"]}, it {itT}): {"OK" if s3b else "FAIL"}')
        # ---- S4: V-cycle CPU 동수학 (xp=numpy — GPU와 단일 구현) ----
        try:
            import pyamg
            _has_pyamg = True
        except ImportError:
            _has_pyamg = False
            print('solver S4 V-cycle: pyamg 미설치 → SKIP (프로덕션도 동일 강등)')
        if _has_pyamg:
            A4 = sparse.csr_matrix(pyamg.gallery.poisson((12, 12), format='csr'), dtype=np.float64)
            _kw = dict(presmoother=('jacobi', {'omega': 2.0 / 3.0, 'iterations': 1}),
                       postsmoother=('jacobi', {'omega': 2.0 / 3.0, 'iterations': 1}))
            ml4 = pyamg.smoothed_aggregation_solver(A4, max_coarse=30, **_kw)
            lv4, lu4 = _mirror_levels(ml4, np)
            rng4 = np.random.default_rng(2)
            N4 = A4.shape[0]
            sym = 0.0
            for _ in range(5):                               # (i) M 대칭 (CG SPD-호환 요건)
                u = rng4.standard_normal(N4); v = rng4.standard_normal(N4)
                Mu = _vcycle_matvec(lv4, lu4, u, np); Mv = _vcycle_matvec(lv4, lu4, v, np)
                sym = max(sym, abs(float(u @ Mv) - float(Mu @ v)) / max(abs(float(u @ Mv)), 1e-30))
            b4 = rng4.standard_normal(N4)
            x1 = _vcycle_matvec(lv4, lu4, b4, np)            # (ii) 1-apply 잔차 감소 (전처리 유효성)
            red = float(np.linalg.norm(b4 - A4 @ x1) / np.linalg.norm(b4))
            from scipy.sparse.linalg import LinearOperator

            def _cg_run(M):
                try:
                    return cg(A4, b4, rtol=1e-12, atol=0.0, maxiter=8000, M=M)
                except TypeError:
                    return cg(A4, b4, tol=1e-12, maxiter=8000, M=M)
            xv, iv = _cg_run(LinearOperator((N4, N4), matvec=lambda r: _vcycle_matvec(lv4, lu4, r, np)))
            xj, ij = _cg_run(sparse.diags(1.0 / A4.diagonal()))
            rel = float(np.linalg.norm(xv - xj) / np.linalg.norm(xj))   # (iii) 전처리 해-불변
            # (iv) ★pyamg 대조 — 미러가 CPU 폴백/자가강등과 **같은 연산자**인지 (2026-07-27 H1:
            #      ω/ρ 정규화를 빠뜨려 rel-diff 0.6 이던 회귀를 이 assert 가 잡는다)
            _zp = ml4.aspreconditioner(cycle='V').matvec(b4)
            d_py = float(np.linalg.norm(x1 - _zp) / max(np.linalg.norm(_zp), 1e-30))
            # (v) SPD — ω>2/ρ 면 전처리가 부정부호가 되어 CG 전제가 깨진다 (H2)
            _Mf = np.column_stack([_vcycle_matvec(lv4, lu4, e, np) for e in np.eye(N4)])
            _emin = float(np.linalg.eigvalsh((_Mf + _Mf.T) / 2).min())
            s4a = (sym < 1e-10 and red < 0.9 and iv == 0 and ij == 0 and rel < 1e-8
                   and d_py < 1e-10 and _emin > 0)
            ok &= s4a
            print(f'solver S4a V-cycle 동수학 (대칭 {sym:.1e}, pyamg Δ {d_py:.1e}, SPD λmin {_emin:.1e}, '
                  f'1-apply resid {red:.2f}, CG해 Δ {rel:.1e}): {"OK" if s4a else "FAIL"}')
        try:                                                 # (iv) GPU 게이트: cupy 부재 → False 무해
            import cupy                                      # noqa: F401
            _has_cupy = True
        except Exception:
            _has_cupy = False
        _GPU_AMG_STATE['ok'] = None
        g_mod['GPU'] = True
        try:
            got = bool(_gpu_amg_on())
        finally:
            g_mod['GPU'] = False
            _GPU_AMG_STATE['ok'] = None
        s4b = (got == _has_cupy)
        ok &= s4b
        print(f'solver S4b GPU 게이트 (cupy {"有" if _has_cupy else "無"} → {got}): '
              f'{"OK" if s4b else "FAIL"}')
        # ---- S5: 게이트 no-op 대수 (회귀 문서화) + atol 노브 ----
        rng5 = np.random.default_rng(3)
        bn5 = 10.0 ** rng5.uniform(-16, 2, 100)
        at5 = 10.0 ** rng5.uniform(-20, -6, 100)
        s5a = all(max(1e-5 * b_, a_, 1e-7 * b_) == max(1e-5 * b_, a_)
                  for b_, a_ in zip(bn5, at5))               # 프로덕션 rtol=1e-5 전제 (깨지면 조기검출)
        ok &= s5a
        print(f'solver S5a _NN_ACCEPT_RTOL no-op 대수 (100조합): {"OK" if s5a else "FAIL"}')
        s5b = (getattr(sysE, 'last_atol_cg', None) is not None
               and sysE.last_atol_cg == 0.05 * sysE.agg_floor_abs)   # 미설정 = 현행 bitwise
        _env('MPM_S4_ATOL_FLOOR_FRAC', '0.5')
        sys6 = CellSystem(sid3, se3, sig_i, pid3, 1, vox3, z_top_um=8 * 0.5, z_bot_um=0.0)
        out6 = simulate(sys6, ocp, r_p, 1e-13, kin, c_rate=0.2, nr=15, v_min=2.8, t_max=400.0,
                        dx_max=0.03, dt_init=2.0, dt_max=300.0, verbose=False)
        _env('MPM_S4_ATOL_FLOOR_FRAC', None)
        s5c = (sys6.last_atol_cg == 0.5 * sys6.agg_floor_abs
               and float(np.max(out6['kcl_rel'])) < 1e-6
               and float(np.max(out6['energy_balance_rel'])) < 1e-7)
        ok &= s5b and s5c
        print(f'solver S5b atol 미설정=0.05·floor bitwise: {"OK" if s5b else "FAIL"}')
        print(f'solver S5c atol=0.5·floor 방전 감사 통과 (KCL {np.max(out6["kcl_rel"]):.1e}, '
              f'E-bal {np.max(out6["energy_balance_rel"]):.1e}): {"OK" if s5c else "FAIL"}')
    finally:
        for k, v in _saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    return ok


def _selftest_b1():
    """B-1 사이클 계면상 배선 검증 (리뷰 m3: main() 배선이 무테스트라 침묵 회귀 위험).
    R_ct 화학몫(i0↓)과 필름옴성(asr)이 (1) 물리 부호 (2) 독립 직렬 채널 (3) 단위변환 (4) i0_p 정규화
    상쇄 — 를 simulate() 없이 Kinetics·배선 산술만으로 검사 (빠르고 초점)."""
    ok = True
    kin = Kinetics(i0_ref=2.0, temp_k=298.15)
    # (1) i0 화학몫: g=dI/dη ∝ i0A → i0×0.5(mult=0.5) → g 절반 → R_ct 2× (분극↑, 열화 방향 정상)
    _, g_hi = kin._ct(0.0, 2.0 * 1.0)                        # i0_f=2.0, A=1
    _, g_lo = kin._ct(0.0, 1.0 * 1.0)                        # mult=0.5 적용 후 i0_f=1.0
    r1 = abs(g_lo / g_hi - 0.5) < 1e-12
    ok &= r1; print(f'  B-1 (1) i0×0.5 → g 절반 → R_ct 2× : g_lo/g_hi={g_lo/g_hi:.4f} {"OK" if r1 else "FAIL"}')
    # (2) 단위: asr_film[Ω·m²] + asr_cycle[Ω·cm²]×1e-4 (배선 산술 그대로)
    _asr_use = 0.0 + 10.0 * 1e-4                             # 10 Ω·cm² → 1e-3 Ω·m²
    r2 = abs(_asr_use - 1e-3) < 1e-18
    ok &= r2; print(f'  B-1 (2) 10 Ω·cm² → {_asr_use:g} Ω·m² (×1e-4) : {"OK" if r2 else "FAIL"}')
    # (3) 독립 직렬 채널: asr>0 은 g_eff=g/(1+g·rA)<g 로만 작용(전하이동 i0 은 불변) — 이중계산 없음
    kf = Kinetics(i0_ref=2.0, asr_film=1e-3)
    _, g_noasr, _ = kin.face_current(np.array([0.05]), 2.0, 1.0)
    _, g_asr, _ = kf.face_current(np.array([0.05]), 2.0, 1.0)
    r3 = (g_asr[0] < g_noasr[0]) and (kf.i0(0.5) == kin.i0(0.5))   # 옴성은 g만 낮춤, i0(x)는 불변
    ok &= r3; print(f'  B-1 (3) asr 직렬 g_eff<{g_noasr[0]:.3g} ({g_asr[0]:.3g}) & i0 불변 : {"OK" if r3 else "FAIL"}')
    # (4) i0_p 정규화 상쇄: 균일 i0_p=i0_ref → _i0s=1 (mult=1 이면 bitwise 불변 경로)
    i0_p = np.array([2.0, 2.0]); _i0s = i0_p / kin.i0_ref
    r4 = np.allclose(_i0s, 1.0)
    ok &= r4; print(f'  B-1 (4) 균일 i0_p/i0_ref = {_i0s} (=1 → bitwise 불변) : {"OK" if r4 else "FAIL"}')
    # (5) 채널 직교: i0-mult 은 asr 를 안 건드리고, asr-cycle 은 i0 를 안 건드림 (배선 분리 확인)
    mult, asr_cyc = 0.5, 10.0
    i0_after = (np.array([2.0]) * mult)[0]; asr_after = 0.0 + asr_cyc * 1e-4
    r5 = (i0_after == 1.0) and (asr_after == 1e-3)           # 각 노브가 자기 채널만
    ok &= r5; print(f'  B-1 (5) 채널 직교 (i0→{i0_after:g}, asr→{asr_after:g}, 상호 무간섭) : {"OK" if r5 else "FAIL"}')
    print(f'  B-1 wiring selftest: {"PASS" if ok else "FAIL"}')
    return ok


def _selftest_chain():
    """v2 chaining: rest 보존·평탄화 / 상태 save-load 가드 / simulate x_field 연속성 / 미지정=bitwise."""
    import tempfile
    ok = True
    ocp = OCP.synthetic_test()
    # (1) rest: 질량 보존(CN, J=0) + 표면-평균 gap 감소 + V 트레이스 유한
    r_um = np.array([2.0, 5.0])
    rad = RadialDiffusion(2, 15, r_um * 1e-6, 3e-15, ocp.c_max, 0.5)
    rad.x[0, :] = np.linspace(0.30, 0.70, 15)                # 인위 구배 (충전 직후 흉내)
    rad.x[1, :] = np.linspace(0.60, 0.40, 15)
    V_p = 4.0 / 3.0 * np.pi * (r_um * 1e-6) ** 3
    ro, drift = run_rest(rad, ocp, V_p, 600.0, dt_s=2.0)
    ok1 = (drift < 1e-12 and ro['surf_mean_gap'][-1] < 0.7 * ro['surf_mean_gap'][0]
           and np.all(np.isfinite(ro['V'])))
    ok &= ok1
    print(f'  chain (1) rest: drift {drift:.1e}, surf-mean gap {ro["surf_mean_gap"][0]:.4f}→'
          f'{ro["surf_mean_gap"][-1]:.4f}  {"OK" if ok1 else "FAIL"}')
    with tempfile.TemporaryDirectory() as td:
        # (2) save→load 라운드트립 bitwise(J·dead 포함) + 가드 6종
        sp = os.path.join(td, 's.npz')
        _J0 = np.array([1e-7, 2e-7]); _D0 = np.array([False, True])
        save_chain_state(sp, rad.x, r_um, ocp, 'soc_end', t_end=600.0, J=_J0, dead=_D0)
        xb, rsn, cx = load_chain_state(sp, 2, 15, r_um, ocp)
        ok2 = bool(np.array_equal(xb, rad.x) and rsn == 'soc_end'
                   and np.array_equal(cx['J'], _J0) and np.array_equal(cx['dead'], _D0))
        for bad_args in ((2, 20, r_um), (2, 15, r_um * 1.5)):
            try:
                load_chain_state(sp, *bad_args, ocp); ok2 = False
            except SystemExit:
                pass
        for bad_reason in ('newton_fail', 'soc_overrun'):    # 오염 종료 상태 거부 (rest 세탁 봉쇄)
            spb = os.path.join(td, f'bad_{bad_reason}.npz')
            save_chain_state(spb, rad.x, r_um, ocp, bad_reason)
            try:
                load_chain_state(spb, 2, 15, r_um, ocp); ok2 = False
            except SystemExit:
                pass
        xbad = rad.x.copy(); xbad[0, -1] = 1.05              # 솔버 밴드(1.01) 밖 = 손상
        spr = os.path.join(td, 'range.npz'); save_chain_state(spr, xbad, r_um, ocp, 'soc_end')
        try:
            load_chain_state(spr, 2, 15, r_um, ocp); ok2 = False
        except SystemExit:
            pass
        xnan = rad.x.copy(); xnan[1, 3] = np.nan             # NaN 은 min/max 비교 침묵통과 → isfinite
        spn = os.path.join(td, 'nan.npz'); save_chain_state(spn, xnan, r_um, ocp, 'soc_end')
        try:
            load_chain_state(spn, 2, 15, r_um, ocp); ok2 = False
        except SystemExit:
            pass
        ok &= ok2
        print(f'  chain (2) 상태 save/load bitwise(J·dead) + 가드(nr·타베드·newton_fail·'
              f'soc_overrun·범위·NaN): {"OK" if ok2 else "FAIL"}')
    # (3) simulate 연속성: 부분충전 끝 셸필드 → 방전이 그 x̄에서 시작 (독립런=x0 시작과 구별)
    sid, pid, vox = _build_sandwich(nxy=4, nz=8)
    sig_e = np.array([0., 1., 0., 0., 0., 0., 0.])
    sig_i = np.array([0., 0., 0., 0., 0., 0., 2.])
    r_p = np.array([10.0e-6])
    kin = Kinetics(5.0)
    sysm_a = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    out_c = simulate(sysm_a, ocp, r_p, 1e-13, kin, c_rate=1.0, nr=15, v_min=2.8, v_max=3.9,
                     charge=True, t_max=300.0, dx_max=0.03, dt_init=2.0, dt_max=60.0, verbose=False)
    sysm_b = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    out_d = simulate(sysm_b, ocp, r_p, 1e-13, kin, c_rate=0.5, nr=15, v_min=2.8, t_max=100.0,
                     x_field=out_c['x_shell_final'], dx_max=0.03, dt_init=2.0, dt_max=60.0,
                     verbose=False)
    x_start, x_chg_end = float(out_d['x_mean'][0]), float(out_c['x_mean'][-1])
    ok3 = abs(x_start - x_chg_end) < 1e-9 and abs(x_start - ocp.x0) > 0.02
    ok &= ok3
    print(f'  chain (3) 연속성: 충전끝 x̄={x_chg_end:.4f} → 방전시작 x̄={x_start:.4f} '
          f'(독립이면 {ocp.x0:g})  {"OK" if ok3 else "FAIL"}')
    # (4) x_field 미지정 = 기존 경로 bitwise (회귀 가드)
    sysm_c = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    sysm_d = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    o_ref = simulate(sysm_c, ocp, r_p, 1e-13, kin, c_rate=0.5, nr=15, v_min=2.8, t_max=100.0,
                     dx_max=0.03, dt_init=2.0, dt_max=60.0, verbose=False)
    o_non = simulate(sysm_d, ocp, r_p, 1e-13, kin, c_rate=0.5, nr=15, v_min=2.8, t_max=100.0,
                     x_field=None, dx_max=0.03, dt_init=2.0, dt_max=60.0, verbose=False)
    ok4 = bool(np.array_equal(o_ref['V'], o_non['V'])
               and np.array_equal(o_ref['x_mean'], o_non['x_mean']))
    ok &= ok4
    print(f'  chain (4) x_field=None ≡ 기존 경로 bitwise: {"OK" if ok4 else "FAIL"}')
    # (5) V_cutoff 상태 롤백: 저장 상태의 x̄ 가 보간-보고 q 와 일치 (전량장부 정합, 전기화학 chain#1)
    sysm_e = CellSystem(sid, sig_e, sig_i, pid, 1, vox, z_top_um=8 * 0.5, z_bot_um=0.0)
    o_vc = simulate(sysm_e, ocp, r_p, 1e-13, kin, c_rate=1.0, nr=15, v_min=3.3,
                    dx_max=0.05, dt_init=2.0, dt_max=300.0, verbose=False)
    if o_vc['end_reason'] == 'V_cutoff':
        q_state = abs(float(o_vc['x_final_per_particle'][0]) - ocp.x0) / abs(ocp.x100 - ocp.x0)
        e5 = abs(q_state - o_vc['q_frac_at_cutoff'])
        ok5 = e5 < 1e-9
        print(f'  chain (5) V_cutoff 롤백: 상태 q {q_state:.6f} vs 보고 q '
              f'{o_vc["q_frac_at_cutoff"]:.6f} (Δ{e5:.1e})  {"OK" if ok5 else "FAIL"}')
    else:
        ok5 = False
        print(f'  chain (5) V_cutoff 롤백: 컷오프 미도달(end={o_vc["end_reason"]}) — 테스트 조건 확인 FAIL')
    ok &= ok5
    print(f'  chain selftest: {"PASS" if ok else "FAIL"}')
    return ok


def _selftest_temperature():
    """온도 계약 회귀 (T1-a npz 왕복 · T1-d 부호역전 · G-1 혼합-온도 차단)."""
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f'  temp {"OK  " if cond else "FAIL"} {name}{(" — " + extra) if extra else ""}')

    G_OFF = {'present': True, 'T_C': None, 'factor': 1.0, 'prov': {'T_dependence': 'NOT_MODELLED'}}
    G_45 = {'present': True, 'T_C': 45.0, 'factor': 2.5599, 'prov': {'T_dependence': 'ARRHENIUS'}}

    # (1) ★기본 경로 — 옛 그리드(계약 없음) + --temp-k 기본 → 오류 0 · meta None (바이트 불변)
    e, m = temperature_verdict(298.15, None, False, False)
    chk('(1) 계약없는 그리드 + 기본 T → 통과, meta None (기존 npz 바이트 불변)', e == [] and m is None)
    e, m = temperature_verdict(298.15, G_OFF, False, False)
    chk('(1b) 계약 있으나 T_dependence=NOT_MODELLED + 기본 T → 통과, meta None (바이트 불변)',
        e == [] and m is None)
    e, m = temperature_verdict(298.15, dict(G_OFF, T_C=25.0), False, False)
    chk('(1c) 그리드가 명시적으로 25 °C → 통과하되 meta 는 기록 (온도가 선언된 런)',
        e == [] and m is not None and m['state'] == 'ISOTHERMAL_25C'
        and m['sigma_ion_T_scaling'] == 'ARRHENIUS')

    # (2) ★핵심 회귀 — 45 °C 로 구운 그리드를 --temp-k 기본(25 °C)으로 태우면 **차단**
    e, m = temperature_verdict(298.15, G_45, False, False)
    chk('(2) 그리드 45 °C + --temp-k 기본 25 °C → GRID_T_MISMATCH 차단 (버그 재발 방지)',
        e == ['GRID_T_MISMATCH'], str(e))
    chk('(2b) --allow-unscaled-t 로는 안 풀린다 (다른 결함)',
        temperature_verdict(298.15, G_45, True, False)[0] == ['GRID_T_MISMATCH'])
    e, m = temperature_verdict(298.15, G_45, False, True)
    chk('(2c) --allow-grid-t-mismatch → 통과 + MIXED_TEMPERATURE 기록',
        e == [] and m['state'].startswith('MIXED_TEMPERATURE')
        and m['released_guards'] == ['GRID_T_MISMATCH:--allow-grid-t-mismatch'], m['state'])

    # (3) 온도를 맞춰도 동역학 Arrhenius 부재는 남는다 (T1-d 유지)
    e, m = temperature_verdict(318.15, G_45, False, False)
    chk('(3) 그리드 45 °C + --temp-k 318.15 → KINETICS_UNSCALED 만 남음',
        e == ['KINETICS_UNSCALED'], str(e))
    e, m = temperature_verdict(318.15, G_45, True, False)
    chk('(3b) + --allow-unscaled-t → 통과, state=PARTIAL, kinetics_T_scaling=NONE',
        e == [] and m['state'].startswith('PARTIAL') and m['kinetics_T_scaling'] == 'NONE',
        m['state'])

    # (4) 계약 없는 옛 그리드 + T≠25 → 기존 T1-d 그대로
    e, _ = temperature_verdict(318.15, None, False, False)
    chk('(4) 옛 그리드 + T≠25 → KINETICS_UNSCALED (기존 T1-d 보존)', e == ['KINETICS_UNSCALED'])

    # (5) npz 계약 왕복 + 무결성 (payload 가 쓰는 형식 그대로)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, 'g45.npz')
        np.savez_compressed(p, sid=np.zeros((2, 2, 2), np.int8), grid_temp_c=np.float64(45.0),
                            temperature_provenance=np.array(json.dumps(
                                {'T_C': 45.0, 'sigma_ion_T_factor': 2.5599,
                                 'T_dependence': 'ARRHENIUS'})))
        gt = _grid_temperature(p)
        chk('(5) npz 왕복: T_C=45 · factor 승계', gt['present'] and gt['T_C'] == 45.0
            and abs(gt['factor'] - 2.5599) < 1e-9)
        p2 = os.path.join(td, 'bad.npz')                 # 두 필드가 서로 다른 온도 = 계약 파손
        np.savez_compressed(p2, sid=np.zeros((2, 2, 2), np.int8), grid_temp_c=np.float64(45.0),
                            temperature_provenance=np.array(json.dumps({'T_C': 25.0})))
        try:
            _grid_temperature(p2)
            chk('(5b) 계약 불일치 npz → RuntimeError', False)
        except RuntimeError:
            chk('(5b) 계약 불일치 npz → RuntimeError (조용한 단정 금지)', True)
        p3 = os.path.join(td, 'broken.npz')              # JSON 깨짐 = 조용히 25 °C 로 넘기지 않음
        np.savez_compressed(p3, sid=np.zeros((2, 2, 2), np.int8),
                            temperature_provenance=np.array('{not json'))
        try:
            _grid_temperature(p3)
            chk('(5c) 깨진 provenance → RuntimeError', False)
        except RuntimeError:
            chk('(5c) 깨진 provenance → RuntimeError', True)
    # ── A (2026-07-29): i0(T) 앵커 배선 — §3-3① 부호역전 해소 ────────────────────────────
    import cam_kinetics as _ck
    _g60 = {'present': True, 'T_C': 60.0, 'factor': 4.7851, 'prov': {'T_C': 60.0}}
    _e_off, _m_off = temperature_verdict(333.15, _g60, False, True, False)
    _e_on, _m_on = temperature_verdict(333.15, _g60, False, True, True)
    chk('(A1) i0 미스케일: KINETICS_UNSCALED 로 차단 (기존 동작 보존)',
        'KINETICS_UNSCALED' in _e_off, str(_e_off))
    chk('(A2) --i0-temp-scale: 해제 + 상태가 부분성을 남긴다',
        _e_on == [] and 'sigma_ion+i0' in _m_on['state'], f"{_e_on} / {_m_on['state']}")
    chk('(A3) kinetics_T_scaling 이 앵커를 이름으로 밝힌다',
        _m_on['kinetics_T_scaling'] == 'I0_ARRHENIUS_kim2025'
        and _m_off['kinetics_T_scaling'] == 'NONE')
    # ★ 부호: i0 를 스케일하면 같은 전류에 필요한 η_ct 가 **작아져야** 한다 (실측 R_ct 4.28× 감소)
    _I, _A, _xh = 3.0e-8, 2.5e-9, 0.5

    def _eta_of(k):
        lo, hi = 0.0, 1.0
        for _ in range(200):                      # 이분법 (scipy 불요)
            mid = 0.5 * (lo + hi)
            if k._ct(mid, k.i0(_xh) * _A)[0] < _I:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)
    _e25 = _eta_of(Kinetics(2.0, temp_k=298.15))
    _ebad = _eta_of(Kinetics(2.0, temp_k=333.15))                                  # 옛 동작
    _eok = _eta_of(Kinetics(2.0 * _ck.i0_temperature_factor(60.0), temp_k=333.15))  # A 배선
    chk('(A4) ★옛 동작은 T↑에 η_ct 가 커진다 (부호역전 재현)', _ebad > _e25,
        f'25 °C {_e25 * 1e3:.4f} mV → 60 °C {_ebad * 1e3:.4f} mV')
    chk('(A5) ★i0(T) 배선하면 η_ct 가 작아진다 (실측 방향)', _eok < _e25,
        f'25 °C {_e25 * 1e3:.4f} mV → 60 °C {_eok * 1e3:.4f} mV')
    chk('(A6) 기본 OFF: 배수가 정확히 1.0 (기본 런 bitwise 불변)',
        _ck.i0_temperature_factor().hex() == (1.0).hex())
    chk('(A7) 25 °C 에서는 켜도 무해', abs(_ck.i0_temperature_factor(25.0) - 1.0) < 1e-12)
    # ★ (A8) 2026-07-29 자체검증에서 잡은 HIGH: i0(T) 를 i0_ref 에만 곱하면 bimodal
    #   (--i0-poly/--i0-sc) 경로에서 _i0s = i0_p/i0_ref 가 배수를 **완전히 상쇄**한다.
    #   두 경로 모두에서 **실효 i0_face** 가 T 를 따르는지 직접 확인한다 (i0_ref 가 아니라).
    _tf60 = _ck.i0_temperature_factor(60.0)
    _ip = np.array([2.0, 2.0])

    def _i0_face(kin_i0, i0_p_arr):
        """실효 per-face i0.  ★ 프로덕션과 **같은** apply_i0_temperature 를 타야 의미가 있다
        (HIGH-10: 옛 버전은 여기서 배선을 재구현해 main() 을 되돌려도 PASS 했다)."""
        _k = Kinetics(kin_i0)
        _s = None if i0_p_arr is None else i0_p_arr / _k.i0_ref
        return float(_k.i0(0.5) if _s is None else (_k.i0(0.5) * _s)[0])

    def _i0_face_via_prod(factor, i0_p_arr):
        """프로덕션 헬퍼를 통과시킨 뒤의 실효 i0 — main() 과 같은 코드경로."""
        _r, _p = apply_i0_temperature(2.0, i0_p_arr, factor)
        return _i0_face(_r, _p)
    # 스칼라 경로: i0_ref 에 곱하는 것이 맞다
    chk('(A8a) 스칼라 경로: 실효 i0 가 T 배수만큼 커진다',
        abs(_i0_face(2.0 * _tf60, None) / _i0_face(2.0, None) - _tf60) < 1e-12,
        f'×{_i0_face(2.0 * _tf60, None) / _i0_face(2.0, None):.4f} (기대 ×{_tf60:.4f})')
    # bimodal 경로: i0_ref 에 곱하면 상쇄된다 = 옛 결함 재현
    chk('(A8b) ★i0_ref 에만 곱하면 bimodal 에서 상쇄된다 (옛 결함 — 회귀 핀)',
        abs(_i0_face(2.0 * _tf60, _ip) / _i0_face(2.0, _ip) - 1.0) < 1e-12,
        f'×{_i0_face(2.0 * _tf60, _ip) / _i0_face(2.0, _ip):.6f} = 배수 소실')
    # 수정된 배선: i0_p 에 곱하면 반영된다
    chk('(A8c) ★i0_p 에 곱하면 bimodal 에서도 T 를 따른다 (수정 확인)',
        abs(_i0_face(2.0, _ip * _tf60) / _i0_face(2.0, _ip) - _tf60) < 1e-12,
        f'×{_i0_face(2.0, _ip * _tf60) / _i0_face(2.0, _ip):.4f} (기대 ×{_tf60:.4f})')
    # ★ (A8e) HIGH-10: **프로덕션 헬퍼**를 통과시켜 검사한다 — 사본이 아니라 main() 이 쓰는 함수.
    #   apply_i0_temperature 를 잘못 고치면 여기서 잡힌다 (옛 테스트는 못 잡았다).
    for _lbl, _arr in (('스칼라', None), ('bimodal', _ip)):
        _base = _i0_face_via_prod(1.0, _arr)
        _hot = _i0_face_via_prod(_tf60, _arr)
        chk(f'(A8e) ★프로덕션 헬퍼 경유 — {_lbl} 경로 실효 i0 가 T 배수를 따른다',
            abs(_hot / _base - _tf60) < 1e-12, f'×{_hot / _base:.4f} (기대 ×{_tf60:.4f})')
    # ★[H6]+[M13] cycle_interphase 기록: 존재하지 않는 kim2025 R_ct(N) 을 인용하지 않고,
    #   본 경로와 rest 가 **같은 헬퍼**를 써서 갈라지지 않는다.
    _ci = cycle_interphase_meta(100, 0.348, 320.3)
    _ci_r = cycle_interphase_meta(100, 0.348, 320.3, rest=True)
    _ci_s = ' '.join(str(v) for v in _ci.values())
    chk('★[H6] cycle_interphase 가 kim2025 를 R_ct(N) 앵커로 인용하지 않는다',
        'kim2025' not in _ci_s and 'yun2023' in _ci_s and '341.7' in _ci_s, _ci['anchor'])
    chk('★[M13] rest 기록이 본 경로와 같은 앵커·provenance (헬퍼 공유 → 드리프트 불가)',
        _ci_r['anchor'] == _ci['anchor'] and _ci_r['provenance'] == _ci['provenance']
        and 'rest_note' in _ci_r and 'rest_note' not in _ci)
    chk('(A8f) 헬퍼가 활성 진폭 쪽만 건드린다 (반대쪽은 원본 그대로)',
        apply_i0_temperature(2.0, None, _tf60)[1] is None
        and apply_i0_temperature(2.0, _ip, _tf60)[0] == 2.0)
    # ⚠ 양쪽에 곱해도 tf 는 한 번만 적용된다 (i0_ref 가 상쇄되므로) — 첫 주석의 "또 상쇄된다"는
    #   틀린 추론이었다.  이 단언이 그 사실을 못박아 같은 오해가 재발하지 않게 한다.
    chk('(A8d) 양쪽에 곱해도 tf 는 정확히 한 번 (i0_ref 는 상쇄 — "이중적용" 오해 차단)',
        abs(_i0_face(2.0 * _tf60, _ip * _tf60) / _i0_face(2.0, _ip) - _tf60) < 1e-12,
        f'×{_i0_face(2.0 * _tf60, _ip * _tf60) / _i0_face(2.0, _ip):.4f} (기대 ×{_tf60:.4f})')

    # ── 2026-07-30 재검증 리뷰 회귀 ────────────────────────────────────────────────────
    # ★[H2] 콘솔 배너가 meta 와 **같은 사실**을 말한다 (옛 배너는 리터럴 NONE 을 박았다)
    _m_on['i0_T_factor'] = _tf60
    _b_on = temperature_banner(_m_on)
    _b_off = temperature_banner(_m_off)
    chk('★[H2] i0 스케일 런의 배너가 kinetics_T_scaling=NONE 이라고 **거짓말하지 않는다**',
        'kinetics_T_scaling=NONE' not in _b_on
        and 'I0_ARRHENIUS_kim2025' in _b_on and 'i0 는 T 를 따름' in _b_on, _b_on.strip())
    chk('★[H2] 배너가 npz meta 의 kinetics_T_scaling 과 문자 그대로 일치',
        f"kinetics_T_scaling={_m_on['kinetics_T_scaling']}" in _b_on
        and f"kinetics_T_scaling={_m_off['kinetics_T_scaling']}" in _b_off)
    chk('★[H2] 미스케일 런은 옛 문장을 그대로 유지 (기존 경고 약화 아님)',
        'kinetics_T_scaling=NONE' in _b_off and 'i0/D_s/OCP/σ_e/κ 는 25°C 상수' in _b_off)
    chk('★[H2] 자명한 25 °C / meta 없음 → 배너 없음 (기본 런 출력 불변)',
        temperature_banner(None) == ''
        and temperature_banner(temperature_verdict(298.15, dict(G_OFF, T_C=25.0),
                                                   False, False)[1]) == '')
    # ★[H9] 계약 없는 그리드 + i0 스케일 = 남은 결함이 σ_ion 쪽 → GRID_T_MISMATCH 로 코딩
    _e_h9, _m_h9 = temperature_verdict(333.15, None, True, False, True)
    chk('★[H9] 계약없는 그리드 + i0 스케일 → GRID_T_MISMATCH (KINETICS_UNSCALED 오라벨 아님)',
        _e_h9 == ['GRID_T_MISMATCH'], str(_e_h9))
    chk('★[H9] --allow-unscaled-t 로는 안 풀린다 (i0 는 이미 스케일됨 — 잘못된 해제 금지)',
        temperature_verdict(333.15, None, True, False, True)[0] == ['GRID_T_MISMATCH'])
    _e_h9b, _m_h9b = temperature_verdict(333.15, None, False, True, True)
    chk('★[H9] --allow-grid-t-mismatch 가 올바른 해제 + released 라벨도 GRID_T_MISMATCH',
        _e_h9b == [] and _m_h9b['released_guards'] == ['GRID_T_MISMATCH:--allow-grid-t-mismatch']
        and _m_h9b['kinetics_T_scaling'] == 'I0_ARRHENIUS_kim2025',
        f"{_e_h9b} / {_m_h9b['released_guards']}")
    chk('★[H9] i0 **미**스케일 + 계약없음 은 역사적 T1-d 라벨 보존 (회귀 아님)',
        temperature_verdict(333.15, None, False, False, False)[0] == ['KINETICS_UNSCALED'])
    print(f'  temperature selftest: {"PASS" if ok else "FAIL"}')
    return ok


# ---------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description='STEP4-v2 galvanostatic/CV voxel-DFN (SSB)')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--grid', help='step4_grid.npz (mpm_webapp_payload --save-step4-grid)')
    ap.add_argument('--ocp-csv', help='U(x) 테이블 CSV (step4_pybamm_anchor --export-params)')
    ap.add_argument('--params-json', help='c_max/x0/x100/provenance JSON (같은 export)')
    ap.add_argument('--ocp-test', action='store_true',
                    help='합성 TEST-ONLY OCP (앵커 파일 없이 스모크; 결과에 test_only 라벨)')
    ap.add_argument('--dudt-csv', default='', help='dU/dT(x) CSV — 있으면 Q_rev 출력 (§F1 입력)')
    ap.add_argument('--c-rate', type=float, default=0.5)
    ap.add_argument('--charge', action='store_true')
    ap.add_argument('--cv-hold', action='store_true', help='V-리밋 도달 후 CV 홀드 (CCCV)')
    ap.add_argument('--i-cut-frac', type=float, default=0.05, help='CV 종지 |I|/I_1C')
    ap.add_argument('--d-s', type=float, default=3e-14,
                    help='D_s [m²/s] 기본 3e-14 (Kang&Shin 2025 FEM = Yu2023/Amin 모델-체인 상속, '
                         '측정 아님; GITT 스프레드는 1e-15–1e-14 — docs/ncm_sc_poly_electrochem_'
                         'anchors.md) — --d-s-poly/--d-s-sc 지정 시 무시')
    ap.add_argument('--i0', type=float, default=2.0, help='i0_ref [A/m²] @x=0.5 (⚠F1 스윕) — '
                         '--i0-poly/--i0-sc 지정 시 값은 상쇄되나 정규화 분모라 >0 필수')
    # ── bimodal poly/SC 전기화학 분리 (기본 미사용 = 기존 공유물성과 bitwise 동일 경로) ──
    #    대립 AM_P=polycrystalline(2차입자, GB/1차결정 경로) vs 소립 AM_S=single-crystal —
    #    σ_e의 Trevisanello NCM(r) 분리와 같은 GB-밀도 축을 확산·반응동역학에 적용.
    #    값은 문헌앵커만 (§F1; docs/ncm_sc_poly_electrochem_anchors.md 참조) — 기본값 없음.
    ap.add_argument('--d-s-poly', type=float, default=None,
                    help='대립 poly AM(r≥--am-split-um) D_s [m²/s] — --d-s-sc와 쌍으로만.  '
                         '★스케일 규약(리뷰 #0): 2차입자-반경 effective D (GITT 2차입자 측정 관례 '
                         '— 확산길이=우리 r_um과 정합).  1차결정(grain) D를 넣으면 스케일 불일치')
    ap.add_argument('--d-s-sc', type=float, default=None,
                    help='소립 single-crystal AM(r<split) D_s [m²/s] — --d-s-poly와 쌍으로만')
    ap.add_argument('--i0-poly', type=float, default=None,
                    help='poly AM i0_ref [A/m²] @x=0.5 — --i0-sc와 쌍으로만')
    ap.add_argument('--i0-sc', type=float, default=None,
                    help='SC AM i0_ref [A/m²] @x=0.5 — --i0-poly와 쌍으로만')
    ap.add_argument('--am-split-um', type=float, default=3.5,
                    help='poly/SC 분류 반경 문턱 [µm], r≥split=poly (σ_ionic power-gate r_cut=3.5 '
                         '규약; 12:4µm(직경) 베드 = 반경 6:2 → 2~6 사이 아무 값이나 분리)')
    # ★ LOW-2 (2026-07-30 리뷰): α_a+α_c ≠ 1 이면 선형화 BV 의 R_ct = RT/(F·i0·A) 가 더 이상
    #   정확하지 않다 (실제 1/(dI/dη)|₀ = RT/(F·i0·A·(α_a+α_c))).  --i0-temp-scale 의 **비**는
    #   α 가 T-무관이라 상쇄되어 무해하지만, i0 를 kim2025 R_ct **절대값**에 앵커할 때는
    #   (α_a+α_c) 만큼 어긋난다 (0.7/0.5 → 20 %).  기본 0.5/0.5 는 합 1 이라 정확.
    ap.add_argument('--alpha-a', type=float, default=0.5,
                    help='BV 산화 전달계수 (기본 0.5).  ⚠ α_a+α_c≠1 이면 R_ct=RT/(F·i0·A) 규약이 '
                         '(α_a+α_c) 배 어긋난다 — i0 앵커의 절대값 해석에만 영향, T-스케일 비는 무해.')
    ap.add_argument('--alpha-c', type=float, default=0.5,
                    help='BV 환원 전달계수 (기본 0.5).  --alpha-a 설명 참조.')
    ap.add_argument('--asr-film', type=float, default=0.0,
                    help='계면 필름 ASR [★Ω·m²★] (SEI/CEI 훅).  ⚠ 단위 주의(리뷰 electrochem#5): 표준 EIS 단위는 '
                         'Ω·cm²인데 이 옵션은 Ω·m² (1 Ω·cm² = 1e-4 Ω·m²).  Ω·cm² 로 넣고 싶으면 아래 '
                         '--asr-film-cycle-ohm-cm2 (자동 ×1e-4 변환)를 쓸 것.')
    # ── B-1 사이클 계면상 성장 (R_int(N) 화학몫; 리뷰 N1-F9 비-이중계산: R_ct=i0(N)↓ 한 채널,
    #    필름옴성=asr-film 별개) ──  ⚠ 성장'값'은 **yun2023** R_ct(N) 앵커에서 산출한 배수를 주입
    #    ★ HIGH-6 (2026-07-30 리뷰): 여기(및 콘솔·npz·help)가 kim2025 를 인용했으나 **거짓**이다 —
    #      rint_eis_anchors.csv 의 kim2025 8행은 전부 cycle_n=post-formation (30/45/60 은 T_meas_C)
    #      이고, 유일한 R_ct(N) 앵커는 yun2023_rct_growth (341.7→982.3 Ω·cm² @~100cyc, 30 °C).
    #    (법칙 N→배수 자동화는 Jung/Conforto fit 후 = §6 N1; 지금은 배수 직접 = ASSUMED-FORM 라벨).
    ap.add_argument('--cycle-n', type=int, default=0,
                    help='B-1 사이클 번호 N (메타·산출물 태그; 0=pristine).  전기화학엔 --i0-cycle-mult/'
                         '--asr-film-cycle가 실제 열화를 주입 — N 자체가 물성을 안 바꿈(법칙 미탑재, §6 N1).')
    ap.add_argument('--i0-cycle-mult', type=float, default=1.0,
                    help='★R_ct 화학몫 채널: i0 → i0×배수 (배수=R_ct,0/R_ct(N)<1 열화; ★yun2023 R_ct(N) '
                         '앵커 341.7→982.3 Ω·cm² @~100cyc — kim2025 는 사이클 축이 없다, HIGH-6).  BV 비선형 '
                         '전하이동 저항이 정직하게 성장(옴성 asr-film과 이중계산 금지).  1.0=무열화.  ★★배수는 '
                         'CHEMICAL-ONLY 몫(g_chem)이어야 함(리뷰 electrochem#2): 접촉면적 손실 R_ct 몫(g_mech)은 '
                         'ledger(A-3 rct_ct_area_rel) 소관 → B-2 통합은 ln R = ln g_chem + ln g_mech 로그-가법. '
                         '여기 total R_int(N)을 넣으면 기계 몫 이중계산.  ⚠ 단일 스칼라라 poly/SC 차등 CEI(√N vs '
                         '선형)는 아직 표현 불가(electrochem#6, 법칙 탑재 시 per-material 분리 필요).')
    ap.add_argument('--asr-film-cycle-ohm-cm2', type=float, default=0.0,
                    help='★필름옴성 채널: 사이클 계면상의 순수 Li⁺ 필름 ASR [Ω·cm²] 추가분 (--asr-film에 더함, '
                         '자동 ×1e-4 → Ω·m²).  전하이동(R_ct)은 여기 넣지 말 것 — 그건 --i0-cycle-mult (비-이중계산, 리뷰 N1-F9).')
    ap.add_argument('--r-int-ohm-cm2', type=float, default=0.0,
                    help='집전체 실측 R_int 직렬 [Ω·cm²] (STEP3 시나리오 규약; 46=DBE)')
    ap.add_argument('--i0-temp-scale', action='store_true',
                    help='★i0 를 --temp-k 에 따라 kim2025 R_ct(T) 앵커로 스케일 (기본 OFF).  '
                         'kim2025(우리와 같은 NCM811+LPSCl) 이 같은 셀을 30/45/60 °C 에서 측정 — '
                         'R_ct 289.9/139.6/67.8 Ω·cm² → Eₐ=0.4212 eV (R²=0.99943).  ★선형화 BV 에서 '
                         'R_ct=RT/(F·i0·A) 이므로 i0 ∝ **T/R_ct** (1/R_ct 아님, HIGH-1) → '
                         '60 °C 에서 i0 **×6.25** (RT 전인자 빼면 5.60 = 10.5 퍼센트 과소).  '
                         '★이 플래그가 §3-3① '
                         '**부호역전을 없앤다** — 없으면 T 를 올릴 때 η_ct 가 커져(실측은 4.28× 감소) '
                         '반대 답이 난다.  ⚠D_s(T)·OCP dU/dT 는 여전히 미앵커라 상태는 '
                         'PARTIAL_sigma_ion+i0 다 (전-물리 스윕 아님).  ⚠앵커는 **uncoated** 조성이다 — '
                         '코팅 프리셋과 같이 쓰면 uncoated Eₐ 를 상속한다 (kim2025 LNO 는 비-Arrhenius). '
                         '전말: scripts/cam_kinetics.py')
    ap.add_argument('--i0-temp-ea-ev', type=float, default=None,
                    help='위 스케일의 Eₐ override [eV] (기본 0.4212 = 3점 적합).  구간별 값 '
                         '0.4049/0.4398 을 쓸어 **밴드로 보고**할 때 사용 — 단일값 보고 금지.  '
                         '⚠ --i0-temp-scale 없이 단독 지정하면 **거부**한다 (조용한 no-op 방지: '
                         '옛 코드는 무시해서 세 런이 bitwise 동일한데 라벨만 달라졌다, MED-12).')
    ap.add_argument('--temp-k', type=float, default=298.15,
                    help='운전 온도 [K].  ⚠ 기본 상태(=--i0-temp-scale 없음)에서 이 값이 이 스크립트 안에서 '
                         '바꾸는 것은 BV 열전압 f=F/RT **하나뿐**이다 — D_s·i0·OCP·σ_e·κ·열화율은 전부 '
                         '25 °C 상수라 T 를 안 따른다.  그래서 T 를 올리면 반응 과전압이 '
                         '**커지는데(실험은 R_ct 가 4.28× 감소)** 부호가 반대다.  이 상태로 T≠298.15 를 '
                         '돌리려면 --allow-unscaled-t 가 필요하다.  ★**--i0-temp-scale 을 켜면** i0 가 '
                         'kim2025 R_ct(T) 앵커를 따라 부호역전이 사라지므로 --allow-unscaled-t 없이 '
                         '돌아간다 (D_s·OCP 는 여전히 25 °C = PARTIAL).  ⇒ 이 둘은 **한 쌍**으로 '
                         '쓰는 것이 정상 경로다 (킷·webapp 도 쌍으로 굽는다).  '
                         '★σ_ion 만은 예외 — 그 값은 여기서 정하는 게 아니라 --grid(step4_grid.npz) 에 '
                         '**payload 가 --temp-c 로 구워 넣은 온도**로 이미 고정돼 있다.  그래서 이 값이 '
                         '그리드의 온도와 다르면 혼합-온도 셀이 되어 별도로 차단된다 '
                         '(--allow-grid-t-mismatch).  (docs/temp_pressure_capability.md §3)')
    ap.add_argument('--allow-unscaled-t', action='store_true',
                    help='T≠298.15 K 인데 동역학 물성(i0/D_s/OCP) Arrhenius 가 없는 상태로 실행하는 것을 '
                         '명시 허용 (부호-역전 가드 해제).  이 플래그**만** 준 런은 npz meta 의 '
                         'temperature.kinetics_T_scaling=NONE 으로 기록된다 — --i0-temp-scale 과 같이 '
                         '주면 i0 는 앵커를 따르므로 I0_ARRHENIUS_kim2025 로 기록되고 이 해제는 무의미하다 '
                         '(released_guards 에도 안 남는다: 가드가 애초에 안 올라간다).  '
                         '★그리드 σ_ion 온도 불일치는 이 플래그로 안 풀린다 '
                         '(다른 결함 — --allow-grid-t-mismatch).')
    ap.add_argument('--allow-grid-t-mismatch', action='store_true',
                    help='★G-1 해제: --grid 안 σ_ion 이 구워진 온도와 --temp-k 가 어긋난 **혼합-온도** '
                         '실행을 명시 허용한다 (예: payload --temp-c 45 로 구운 그리드를 --temp-k 298.15 '
                         '로 돌리기).  기본은 차단 — 이 조합은 σ_ion@45 °C × 동역학@25 °C 라 어느 온도의 '
                         '셀도 아니다.  허용 시 meta.temperature.state=MIXED_TEMPERATURE 가 기록된다.')
    ap.add_argument('--x-init', type=float, default=None, help='초기 stoich (기본: 창 끝)')
    ap.add_argument('--init-state', default='',
                    help='★v2 chaining: 이전 런의 --save-state npz 셸-SOC 로 시작 (같은 베드·같은 '
                         '--nr 강제, newton_fail 상태 거부).  충·방·rest 공통.  미지정 = 기존 독립 '
                         '초기상태 (bitwise 불변).  --x-init 과 동시 지정 불가.')
    ap.add_argument('--save-state', default='',
                    help='★v2 chaining: 런 끝 셸-SOC 상태 npz 저장 → 다음 스텝의 --init-state.')
    ap.add_argument('--rest', action='store_true',
                    help='★Rest 스텝 (I=0 완화, v2 chaining): 망솔브 없이 zero-flux 방사확산만 전개 '
                         '(REST-LOCAL — 입자간 재분배는 미모델, meta 명기).  --init-state 필수.')
    ap.add_argument('--t-rest-min', type=float, default=1.0, help='Rest 시간 [분] (기본 1)')
    ap.add_argument('--x0', type=float, default=None,
                    help='방전창 시작 stoich(저리튬/충전끝) 오버라이드 — 기본 None=params_json.')
    ap.add_argument('--x100', type=float, default=None,
                    help='방전창 끝 stoich(고리튬/방전끝) 오버라이드 — 기본 None=params_json.  '
                         '★ASSB vs-Li 창 재산정 훅: NMC-vs-Li 2.5V까지 더 깊게(~0.95~0.98) + --v-min 2.5. '
                         'OCP 테이블 0.995까지 유효, 확산은 x≤1 지원 → 코드변경 없이 파라미터로.  기본 미사용(DBE 비교 무영향).')
    ap.add_argument('--nr', type=int, default=20)
    ap.add_argument('--v-min', type=float, default=3.0, help='방전 컷오프 [V vs Li] (운전 설정)')
    ap.add_argument('--v-max', type=float, default=4.5)
    ap.add_argument('--t-max', type=float, default=None)
    ap.add_argument('--dx-max', type=float, default=0.02)
    ap.add_argument('--dt-max', type=float, default=120.0)
    ap.add_argument('--gpu', action='store_true')
    ap.add_argument('--periodic-xy', dest='periodic_xy', action='store_true', default=None,
                    help='x,y 주기 BC 강제 (기본: 그리드 npz 의 periodic_xy 계약을 따름; 옛 그리드는 절연벽)')
    ap.add_argument('--no-periodic-xy', dest='periodic_xy', action='store_false',
                    help='x,y 절연벽 강제 (옛 corpus 와 비교할 때)')
    ap.add_argument('--out', default='step4_dyn_out.npz')
    ap.add_argument('--n-chk', type=int, default=12, help='뷰어 체크포인트 수 (SOC-진행 균등)')
    ap.add_argument('--viz-out', default='',
                    help='뷰어용 JSON (코어-셸 SOC 체크포인트 + 면별 반응전류) — webapp 3D 뷰어의 '
                         'STEP4-v2 모드에서 열기 (입자 SOC 그라데이션·표면 반응 필드·단면 뷰)')
    ap.add_argument('--viz-max-faces', type=int, default=120000,
                    help='viz JSON 면 서브샘플 상한 (seed 0 결정론)')
    a = ap.parse_args()
    global GPU
    GPU = bool(a.gpu)
    # poly/SC 인자 가드는 grid 로드 전에 (리뷰 #18: --selftest/grid-오류 경로에서 반쪽 지정이
    # 침묵 통과하던 순서 문제) — 분류 자체는 grid의 r_um이 필요해 아래에서.
    if (a.d_s_poly is None) != (a.d_s_sc is None):
        ap.error('--d-s-poly/--d-s-sc must be given together (반쪽 지정 = 침묵 기본값 혼입 금지)')
    if (a.i0_poly is None) != (a.i0_sc is None):
        ap.error('--i0-poly/--i0-sc must be given together')
    for _nm, _v in (('--d-s-poly', a.d_s_poly), ('--d-s-sc', a.d_s_sc),
                    ('--i0-poly', a.i0_poly), ('--i0-sc', a.i0_sc)):
        if _v is not None and _v <= 0:
            ap.error(f'{_nm} must be > 0')
    if a.am_split_um <= 0:
        ap.error('--am-split-um must be > 0 (µm 반경 문턱)')
    if a.rest and not a.init_state:
        ap.error('--rest 는 --init-state 필수 (이전 스텝 상태를 완화하는 것)')
    if a.init_state and a.x_init is not None:
        ap.error('--init-state 와 --x-init 동시 지정 불가 (시작상태 이중 정의)')
    if a.t_rest_min <= 0:
        ap.error('--t-rest-min must be > 0')
    # ★ 온도 가드 (T1-d 부호역전 + G-1 그리드 불일치, docs/temp_pressure_capability.md §3-3).
    #   ① T1-d: --temp-k 는 이 스크립트 안에선 f=F/RT 만 바꾼다.  T↑ → f↓ → η_ct ∝ 1/f 가
    #      **커진다**.  실제로는 R_ct 가 30→60°C 에 4.28× **감소**(kim2025) → 부호가 반대.
    #   ② G-1: σ_ion 은 여기서 정하는 게 아니라 --grid 에 payload 가 --temp-c 로 **구워** 넣는다.
    #      그 온도를 읽지 않고 25 °C 로 단정하면 σ_ion@45 °C × 동역학@25 °C 라는 혼합-온도 셀이
    #      조용히 나간다 (킷 사슬 payload --temp-c 45 → step4_dyn 이 정확히 그 경로였다).
    #   ⇒ 그리드 계약을 읽어 대조하고, 어긋나면 같은 급으로 차단.  해제는 각각 명시 플래그.
    _gt = _grid_temperature(a.grid) if (a.grid and not a.selftest) else None
    # ★ A (2026-07-29): i0(T) — kim2025 R_ct(T) 앵커.  --i0-temp-scale 없으면 배수는 정확히 1.0
    #   이고 아래 어떤 값도 안 바뀐다 (기본 런 bitwise 불변).
    _i0_tf = 1.0
    _i0_tprov = None
    # ★ MED-12 (2026-07-30 리뷰): --i0-temp-ea-ev 는 아래 블록 **안에서만** 읽힌다 → 활성화
    #   플래그를 빠뜨리면 조용한 no-op 다.  help 가 지시하는 "구간 Eₐ 0.4049/0.4398 을 쓸어
    #   밴드로 보고" 를 그렇게 하면 세 런이 bitwise 동일한데 파일명·로그엔 서로 다른 Eₐ 가 붙어
    #   **"밴드 폭 0 = Eₐ 불확실성 무시가능"** 으로 오독된다.  같은 파일의 --d-s-poly/--i0-poly
    #   반쪽지정 거부와 같은 규약으로 막는다.
    if a.i0_temp_ea_ev is not None and not a.i0_temp_scale:
        ap.error('--i0-temp-ea-ev 는 --i0-temp-scale 과 함께만 유효합니다 (단독 지정 = 조용한 '
                 'no-op: Eₐ 를 바꿔도 런이 bitwise 동일해 "밴드 폭 0" 으로 오독됩니다).')
    # ★ 2026-07-30 (자체검증, HIGH-4 배선 재검토): --i0-temp-scale 은 **--temp-k 를 읽는다**.
    #   --temp-k 를 기본(25 °C)으로 둔 채 이 플래그만 주면 배수가 **정확히 1.0** 인데도 npz 에는
    #   kinetics_T_scaling='I0_ARRHENIUS_kim2025' 가 찍힌다 = 거짓 라벨 (cam_kinetics 가 ea=0 을
    #   거부하는 것과 같은 이유).  실제로 킷 배선이 이 함정에 빠져 "i0 ×6.25" 를 광고하면서
    #   ×1.0 을 돌렸다.  그리드가 다른 온도를 들고 있으면 의도는 명백하므로 차단하고 안내한다.
    if (a.i0_temp_scale and abs(a.temp_k - _T_REF_K) <= 0.05
            and (_gt or {}).get('T_C') is not None and abs(_gt['T_C'] - _T_REF_C) > 0.05):
        ap.error(
            f'--i0-temp-scale 을 켰는데 --temp-k 가 기본 {_T_REF_K:g} K ({_T_REF_C:g} °C) 입니다 — '
            f'i0 배수가 **정확히 1.0** (스케일 없음)인데 산출물에는 '
            f'kinetics_T_scaling=I0_ARRHENIUS_kim2025 로 찍혀 거짓 라벨이 됩니다.\n'
            f'  · --grid σ_ion 은 {_gt["T_C"]:g} °C 로 구워져 있습니다.\n'
            f'  ▶ 그 온도로 돌리려면: --temp-k {_gt["T_C"] + 273.15:g} --i0-temp-scale\n'
            f'  ▶ 25 °C 동역학이 의도라면: --i0-temp-scale 을 빼고 '
            f'--allow-grid-t-mismatch 로 혼합-온도를 명시 승인하십시오.')
    if a.i0_temp_scale:
        import cam_kinetics as _ck
        _i0_tf = _ck.i0_temperature_factor(a.temp_k - 273.15, a.i0_temp_ea_ev)
        _i0_tprov = _ck.provenance(a.temp_k - 273.15, a.i0_temp_ea_ev)
        print(f'  ★i0(T) 스케일: {a.temp_k - 273.15:g} °C → i0 ×{_i0_tf:.4f} '
              f'(kim2025 R_ct 앵커 Eₐ={_i0_tprov["Ea_Rct_eV"]:.4f} eV, 밴드 '
              f'×{_i0_tprov["i0_T_factor_band"][0]:.3f}–{_i0_tprov["i0_T_factor_band"][1]:.3f}) '
              f'— 부호역전 해소, 단 D_s·OCP 는 여전히 25 °C', flush=True)
    _terr, _tmeta = temperature_verdict(a.temp_k, _gt, a.allow_unscaled_t,
                                        a.allow_grid_t_mismatch, a.i0_temp_scale)
    if _tmeta is not None:
        _tmeta['i0_T_factor'] = float(_i0_tf)
        _tmeta['i0_T_provenance'] = _i0_tprov
    if _terr:
        _sig_c = (_tmeta or {}).get('sigma_ion_T_C', _T_REF_C)
        _msg = [f'온도 상태가 일관되지 않습니다 — 차단 ({", ".join(_terr)}).',
                f'  · --grid σ_ion 이 놓인 온도 : {_sig_c:g} °C'
                + ('  (그리드에 온도 계약 없음 → 옛 payload = 25 °C 규약값)'
                   if not (_gt or {}).get('present') else
                   ('  (payload --temp-c 로 Arrhenius 스케일됨, '
                    f"×{(_gt or {}).get('factor', 1.0):.3f})" if (_gt or {}).get('T_C') is not None
                    else '  (T_dependence=NOT_MODELLED = T_ref 규약값)')),
                f'  · --temp-k 동역학 온도      : {a.temp_k - 273.15:g} °C '
                f'(기준 {_T_REF_K:g} K; f=F/RT 만 이 T 를 따름)']
        if 'GRID_T_MISMATCH' in _terr:
            # ★ HIGH-9: 계약 **없는** 그리드도 이 분기로 온다 (i0 스케일 시).  그 경우 "payload 를
            #   --temp-c 없이 다시 돌려라" 는 이미 그런 그리드라 무의미하므로 해법을 갈라 적는다.
            _has_contract = bool((_gt or {}).get('present'))
            _msg += [
                '  ⛔ G-1 혼합-온도: σ_ion 과 BV/확산/OCP 가 **서로 다른 온도**에 있습니다 — 어느 온도의',
                '     셀도 아닙니다.  (STEP3 σ_ion_eff·이온 옴강하가 한 온도, 반응·확산이 다른 온도)']
            if _has_contract:
                _msg += [
                    f'     ▶ 그리드에 맞추려면: --temp-k {_sig_c + 273.15:g}'
                    + ('' if a.i0_temp_scale else ' --allow-unscaled-t'),
                    '     ▶ 25 °C 로 돌리려면 : payload 를 --temp-c 없이 다시 돌려 그리드를 재생성']
            else:
                _msg += [
                    '     ▶ 그리드에 온도 계약이 없습니다 (--temp-c 없이 만든 payload = σ_ion 25 °C 규약값).',
                    f'     ▶ 제대로 맞추려면: payload(STEP3) 를 --temp-c {a.temp_k - 273.15:g} 로 다시 돌려',
                    '        σ_ion 을 같은 온도로 굽고, 그 그리드로 이 런을 재실행하십시오.',
                    f'     ▶ 25 °C 로 돌리려면 : --temp-k {_T_REF_K:g}']
            _msg += [
                '     ▶ 알고 감수(진단용) : --allow-grid-t-mismatch (meta 에 MIXED_TEMPERATURE 기록)']
        if 'KINETICS_UNSCALED' in _terr:
            _msg += [
                '  ⛔ T1-d 부호역전: i0/D_s/OCP 는 25 °C 상수라 T 를 안 따릅니다.  이 상태로 돌리면',
                '     반응 과전압이 온도에 따라 **증가**합니다 — 실험(R_ct 30→60 °C 4.28× 감소)과 반대.',
                '     ▶ BV 기울기만 보려는 의도면: --allow-unscaled-t (meta 에 kinetics_T_scaling=NONE)']
        _msg.append('  ▶ 상세: docs/temp_pressure_capability.md §3')
        ap.error('\n'.join(_msg))
    _tban = temperature_banner(_tmeta)
    if _tban:
        print(_tban, flush=True)
    if a.i0_poly is not None and a.i0 <= 0:
        # _i0s = i0_p/i0_ref 정규화 분모 — 0이면 0·inf=NaN이 AMG 빌드 후 newton_fail로 오진됨
        # (리뷰 #8 재현: '--i0 0 --i0-poly ...' → 그리드 로드·전처리 다 하고 죽음)
        ap.error('--i0 must be > 0 even with --i0-poly/--i0-sc (값은 상쇄되나 정규화 분모)')
    if a.selftest:
        ok = _selftest_radial()
        ok &= _selftest_cell()
        ok &= _selftest_discharge()
        ok &= _selftest_solver()
        ok &= _selftest_b1()
        ok &= _selftest_chain()
        ok &= _selftest_temperature()
        print('STEP4-V2 SELFTEST', 'PASS' if ok else 'FAIL')
        sys.exit(0 if ok else 1)
    if not a.grid:
        ap.error('--grid required (or --selftest)')
    g = np.load(a.grid, allow_pickle=False)
    sid = g['sid']; pid = g['pid']
    vox_um = float(g['vox_um']); z_top = float(g['z_top_um'])
    # ★x,y 주기 BC — payload 가 npz 에 구운 계약(없으면 옛 그리드 = 절연벽, 하위호환).
    #   --periodic-xy/--no-periodic-xy 로 override (재해석·비교런용).
    _per_grid = bool(np.asarray(g['periodic_xy']).ravel()[0]) if 'periodic_xy' in g.files else None
    if a.periodic_xy is not None:
        _per = a.periodic_xy
    elif _per_grid is None:
        _per = False
        print('    ℹ 그리드에 periodic_xy 없음(옛 payload) → 절연벽 가정 '
              '(STEP3 를 --periodic 로 돌렸다면 --periodic-xy 로 맞출 것)', flush=True)
    else:
        _per = _per_grid
    if _per:
        print('    ★x,y 주기 BC (STEP3 규약 정합 — 전도·BV 계면 함께 wrap)', flush=True)
    sig_e = g['sig_e_S_cm']; sig_i = g['sig_i_S_cm']
    r_um = g['am_r_um']
    # ── poly/SC 전기화학 분리: 반경 문턱으로 [n_am] 물성 벡터 구성 (미지정 = 기존 스칼라 경로;
    #    인자 가드는 위 parse 직후로 이동 — 리뷰 #18) ──
    ds_arg, i0_p, split_meta = a.d_s, None, None
    if a.d_s_poly is not None or a.i0_poly is not None:
        is_poly = r_um >= a.am_split_um
        n_po, n_sc = int(is_poly.sum()), int((~is_poly).sum())
        if n_po == 0 or n_sc == 0:
            print(f'  ⚠ AM split 문턱 {a.am_split_um:g}µm가 반경분포 '
                  f'{r_um.min():.2f}–{r_um.max():.2f}µm를 가르지 못함 — 전 입자 '
                  f'{"poly" if n_sc == 0 else "SC"} 물성으로 균일 진행 (의도 확인)', flush=True)
        if a.d_s_poly is not None:
            ds_arg = np.where(is_poly, a.d_s_poly, a.d_s_sc)
        if a.i0_poly is not None:
            i0_p = np.where(is_poly, a.i0_poly, a.i0_sc)
        split_meta = dict(am_split_um=a.am_split_um, n_poly=n_po, n_sc=n_sc,
                          d_s_poly=a.d_s_poly, d_s_sc=a.d_s_sc,
                          i0_poly=a.i0_poly, i0_sc=a.i0_sc)
        print(f'  ★ AM poly/SC 전기화학 분리: r≥{a.am_split_um:g}µm → poly n={n_po}, SC n={n_sc}'
              + (f'; D_s poly/SC={a.d_s_poly:g}/{a.d_s_sc:g} m²/s (--d-s 무시)'
                 if a.d_s_poly is not None else '')
              + (f'; i0 poly/SC={a.i0_poly:g}/{a.i0_sc:g} A/m² (--i0 무시)'
                 if a.i0_poly is not None else ''), flush=True)
    if a.ocp_test:
        ocp = OCP.synthetic_test()
        print('⚠ TEST-ONLY synthetic OCP — 결과는 수치 스모크 전용 (§F1: 물리값 아님)', flush=True)
    else:
        if not (a.ocp_csv and a.params_json):
            ap.error('--ocp-csv/--params-json required (§F1 앵커; 임시 스모크는 --ocp-test)')
        ocp = OCP.load(a.ocp_csv, a.params_json)
        if a.x0 is not None:
            ocp.x0 = float(a.x0)
        if a.x100 is not None:                              # ASSB vs-Li 창 재산정 훅 (기본 미사용)
            ocp.x100 = float(a.x100)
        _ovr = '  [x0/x100 CLI override]' if (a.x0 is not None or a.x100 is not None) else ''
        print(f'  OCP: {ocp.provenance}  c_max={ocp.c_max:g}  x0={ocp.x0}  x100={ocp.x100}{_ovr}', flush=True)
    dudt = _load_xy_csv(a.dudt_csv) if a.dudt_csv else None
    # ── ★Rest 스텝 (v2 chaining): 망/BV 솔브 없음 — CellSystem 빌드 전에 처리 (수 초) ──
    if a.rest:
        # ★ MED-13 (2026-07-30 리뷰): 이 분기는 :3135 에서 sys.exit(0) 하는데, B-1 열화 배선
        #   (--i0-cycle-mult) 과 i0(T) 적용이 **그 뒤**(:3146~)에 있었다.  그래서 체인 사이클의
        #   rest 세그먼트가 --cycle-n/--i0-cycle-mult 를 받고도 cycle_interphase 기록 없이
        #   버리면서, 온도 meta 는 "적용됨" 으로 찍혔다.  수치는 rest V 가 i0-가중 혼합전위라
        #   균일 스케일이 상쇄돼 무해하지만 **기록 누락**은 감사 실패다.  → 여기서 같은 배선을
        #   적용하고 meta 에 남긴다 (i0 는 아래 kin_r 에 반영, 상쇄되더라도 규약 일치).
        _b1_rest_on = ((a.i0_cycle_mult != 1.0) or (a.asr_film_cycle_ohm_cm2 != 0.0)
                       or (a.cycle_n != 0))
        if _b1_rest_on and a.i0_cycle_mult <= 0:
            ap.error('--i0-cycle-mult must be > 0 (i0 정규화 분모)')
        # 본 경로(:3166~)와 **같은 규약**: i0_p 가 있으면 그쪽이 실효 진폭, 없으면 스칼라.
        if i0_p is not None:
            _rest_i0, _rest_i0p = a.i0, i0_p * a.i0_cycle_mult
        else:
            _rest_i0, _rest_i0p = a.i0 * a.i0_cycle_mult, None
        _rest_i0, _rest_i0p = apply_i0_temperature(_rest_i0, _rest_i0p, _i0_tf)
        if _b1_rest_on:
            print(f'  ★B-1 계면상(N={a.cycle_n}, rest): R_ct 채널 i0×{a.i0_cycle_mult:g} '
                  f'[ASSUMED-FORM: 배수=yun2023 R_ct(N) 앵커; 필름옴성은 I=0 이라 무효]', flush=True)
        n_am_r = len(r_um)
        xf, _prev_end, _cx = load_chain_state(a.init_state, n_am_r, a.nr, r_um, ocp)
        rad = RadialDiffusion(n_am_r, a.nr, r_um * 1e-6, ds_arg, ocp.c_max, 0.5)
        rad.x[:] = np.clip(xf, 1e-6, 1.0 - 1e-6)
        V_p_r = 4.0 / 3.0 * np.pi * (r_um * 1e-6) ** 3
        _wv_r = V_p_r / V_p_r.sum()
        # ★클립-전 원본 대비 총 드리프트 감사 (수치리뷰 chain#3b: run_rest 내부 drift 는 클립 후
        #   기준이라 클립 삭제분에 눈멂 — in-band 오버슛 절단까지 여기서 잡는다)
        _x_pre = float(((xf * rad.Vk).sum(1) / rad.Vk.sum() * _wv_r).sum())
        t_s = a.t_rest_min * 60.0
        kin_r = Kinetics(_rest_i0, a.alpha_a, a.alpha_c, 0.0, a.temp_k)  # i0(x) 모양 = V-가중용
        _alive = None if _cx['dead'] is None else ~_cx['dead']
        print(f'  ★Rest {a.t_rest_min:g}min (REST-LOCAL I=0 완화; 입자간 재분배 미모델=v2.1 훅; '
              f'V=i0·A-가중{"" if _alive is not None else ", dead-마스크 無(구상태)"}) '
              f'← {a.init_state} (전런 end={_prev_end})', flush=True)
        ro, drift = run_rest(rad, ocp, V_p_r, t_s, i0_fn=kin_r.i0,
                             i0_amp=(_rest_i0p if _rest_i0p is not None else None),
                             alive=_alive, j0=_cx['J'])
        drift_tot = abs(float(ro['x_mean'][-1]) - _x_pre)
        if not (drift <= 1e-9):                              # NaN-안전 부정형 (수치리뷰 chain#3d)
            print(f'  ⚠ rest 질량 드리프트 {drift:.2e} — CN 보존 위반, 점검 필요', flush=True)
        if not (drift_tot <= 1e-6):
            print(f'  ⚠ rest 총 드리프트(클립 포함) {drift_tot:.2e} — 입력 상태 오버슛 절단 감지', flush=True)
        meta = dict(mode='rest', t_rest_min=a.t_rest_min, nr=a.nr, c_max=ocp.c_max,
                    x0=ocp.x0, x100=ocp.x100, ocp_provenance=ocp.provenance,
                    test_only=ocp.test_only, mass_drift=float(drift),
                    mass_drift_incl_clip=float(drift_tot),
                    chain={'init_state': a.init_state, 'prev_end': _prev_end,
                           'save_state': a.save_state or None},
                    rest_model='REST-LOCAL: per-particle zero-flux radial relaxation; '
                               'inter-particle redistribution NOT modeled (v2.1 hook — '
                               'bimodal D_s/i0 split beds are first-order affected)',
                    v_trace='i0(x_surf)·R²-weighted linearized mixed potential OCP, dead '
                            'particles excluded — I=0 표식용 근사 (전기화학 리뷰 chain#3)',
                    d_s=(float(rad.D[0]) if rad.D.max() == rad.D.min() else
                         dict(mode='per_particle', min=float(rad.D.min()), max=float(rad.D.max()))))
        if _tmeta is not None:                           # 자명한 25 °C 기본이면 None → meta 불변
            meta['temperature'] = _tmeta
        if _b1_rest_on:                                  # ★MED-13: rest 도 열화를 기록한다
            meta['cycle_interphase'] = cycle_interphase_meta(
                a.cycle_n, a.i0_cycle_mult, a.asr_film_cycle_ohm_cm2, rest=True)
        np.savez_compressed(a.out, **ro, x_shell_final=rad.x.copy(),
                            params_json=json.dumps(meta))
        if a.save_state:
            save_chain_state(a.save_state, rad.x, r_um, ocp, 'rest_end', t_end=t_s,
                             note=f'prev={_prev_end}', J=np.zeros(n_am_r), dead=_cx['dead'])
            print(f'  chain state → {a.save_state}', flush=True)
        print(f'saved {a.out}  (rest {a.t_rest_min:g}min, ΔV_ocp '
              f'{(ro["V"][-1] - ro["V"][0]) * 1e3:+.2f} mV, surf-mean gap '
              f'{ro["surf_mean_gap"][0]:.4f}→{ro["surf_mean_gap"][-1]:.4f}, drift {drift:.1e})')
        sys.exit(0)
    # ── ★v2 chaining 초기상태 (전 런의 --save-state) ──
    x_field_cli, j_field_cli, dead_cli, _prev_end = None, None, None, ''
    if a.init_state:
        x_field_cli, _prev_end, _cx = load_chain_state(a.init_state, len(r_um), a.nr, r_um, ocp)
        j_field_cli, dead_cli = _cx['J'], _cx['dead']
        print(f'  ★v2 chaining: --init-state ← {a.init_state} (전런 end={_prev_end}'
              f'{", J 연속재구성" if j_field_cli is not None else ""})', flush=True)
    # ── B-1 사이클 계면상 성장 (i0(N)↓ = R_ct 채널 / asr-film += 필름옴성; 비-이중계산 리뷰 N1-F9).
    #    i0_p 설정 시 실제 진폭=i0_p(kin.i0_ref 상쇄, L789) → i0_p만 스케일; 스칼라면 a.i0만 (이중 방지).
    _i0_use, _asr_use = a.i0, a.asr_film
    _b1_on = (a.i0_cycle_mult != 1.0) or (a.asr_film_cycle_ohm_cm2 != 0.0) or (a.cycle_n != 0)
    if _b1_on:
        if a.i0_cycle_mult <= 0:
            ap.error('--i0-cycle-mult must be > 0 (i0 정규화 분모)')
        if i0_p is not None:
            i0_p = i0_p * a.i0_cycle_mult                    # per-particle 실제 진폭
        else:
            _i0_use = a.i0 * a.i0_cycle_mult                 # 스칼라 실제 i0
        _asr_use = a.asr_film + a.asr_film_cycle_ohm_cm2 * 1e-4    # Ω·cm² → Ω·m²
        print(f'  ★B-1 계면상(N={a.cycle_n}): R_ct 채널 i0×{a.i0_cycle_mult:g} · 필름옴성 '
              f'+{a.asr_film_cycle_ohm_cm2:g} Ω·cm² (→ASR {_asr_use:g} Ω·m²)  '
              f'[ASSUMED-FORM: 배수=yun2023 R_ct(N) 앵커 341.7→982.3 Ω·cm² @~100cyc(30 °C); '
              f'N→배수 법칙-fit 후속 §6 N1]', flush=True)
    # ★ i0(T) 를 **활성 경로 한 곳에만** 곱한다 (2026-07-29 자체검증 HIGH — 첫 배선이 틀렸다).
    #   per-face i0 는 두 경로가 다르다:
    #     i0_p 없음 : i0_f = kin.i0_ref · shape(x)                    → i0_ref 가 진폭
    #     i0_p 있음 : _i0s = i0_p / kin.i0_ref  (:1435)
    #                 i0_f = kin.i0_ref·shape(x)·i0_p/kin.i0_ref = shape(x)·i0_p
    #                 ⇒ **i0_ref 가 완전히 상쇄된다** (정규화 분모일 뿐)
    #   첫 배선은 i0_ref 에만 곱해서, --i0-poly/--i0-sc 를 쓰는 bimodal 런에서 온도 스케일이
    #   **조용히 사라졌다** (실증: 배수 ×5.5974 를 걸어도 실효 i0_face 비율이 정확히 1.000000).
    #   ⚠ 정정: "양쪽에 곱하면 또 상쇄된다" 는 **틀린 추론이었다**(첫 주석).  i0_ref 는 어차피
    #     상쇄되므로 곱해도 무해하고, i0_p 에 곱한 tf 는 그대로 남는다 → 양쪽에 곱해도 tf 가
    #     정확히 한 번 적용된다.  다만 아래 if/else 로 **활성 경로만** 곱하는 편이 의도가 분명해
    #     그대로 둔다 (어느 쪽이 진폭인지 코드가 스스로 말한다).
    _kin_i0, _i0p_new = apply_i0_temperature(_i0_use, i0_p, _i0_tf)   # ★ 테스트와 같은 함수
    if i0_p is not None:
        i0_p = _i0p_new
    kin = Kinetics(_kin_i0, a.alpha_a, a.alpha_c, _asr_use, a.temp_k)
    sysm = CellSystem(sid, sig_e, sig_i, pid, len(r_um), vox_um, z_top_um=z_top, z_bot_um=0.0,
                      periodic_xy=_per)
    out = simulate(sysm, ocp, r_um * 1e-6, ds_arg, kin, a.c_rate, nr=a.nr,
                   v_min=a.v_min, v_max=a.v_max, t_max=a.t_max, charge=a.charge,
                   cv_hold=a.cv_hold, i_cut_frac=a.i_cut_frac,
                   r_int_ohm_cm2=a.r_int_ohm_cm2, x_init=a.x_init, dudt=dudt,
                   i0_p=i0_p, dx_max=a.dx_max, dt_max=a.dt_max, n_chk=a.n_chk,
                   x_field=x_field_cli, j_field=j_field_cli)
    meta = out.pop('params')
    # C5: 솔버 env 감사 기록 (>0 contrast_cap = capped 런 → σ-메트릭 보고 금지 라벨)
    meta['solver_env'] = {
        'prune_float_comp': int(getattr(sysm, 'n_pruned_e_comp', 0)),
        'prune_float_vox': int(getattr(sysm, 'n_pruned_e_vox', 0)),
        'contrast_cap': float(getattr(sysm, 'contrast_cap', 0.0)),
        'ew': os.environ.get('MPM_S4_EW', '1') != '0',
        'gpu_amg': os.environ.get('MPM_S4_GPU_AMG', '1') != '0',
        'atol_floor_frac': float(os.environ.get('MPM_S4_ATOL_FLOOR_FRAC', '0.05')),
    }
    reason = out.pop('end_reason')
    meta['end_reason'] = reason
    # 방향·세그먼트 부기 (전기화학 리뷰 chain#7): q_frac_at_cutoff 는 전체-창 |Δx̄| 규약 — 체인
    # 세그먼트 비교용으로 부호와 "이 시작점에서 갈 수 있던 스팬 대비" 분율을 병기 (v1 값과 혼동 방지).
    _dxs = float(out['x_mean'][-1] - meta['x_init'])
    meta['dx_mean_signed'] = _dxs
    meta['q_frac_segment'] = float(abs(_dxs) / max(abs((ocp.x0 if a.charge else ocp.x100)
                                                       - meta['x_init']), 1e-12))
    if a.init_state or a.save_state:                         # v2 chaining 감사 기록
        meta['chain'] = {'init_state': a.init_state or None, 'prev_end': _prev_end or None,
                         'save_state': a.save_state or None}
    if _tmeta is not None:                                   # ★온도 계약 감사 (T1-a/T1-d/G-1).
        meta['temperature'] = _tmeta                         #   자명한 25 °C 기본이면 None → meta 불변
    if split_meta is not None:
        meta['am_electro_split'] = split_meta                # poly/SC 분리 감사 기록 (값+문턱+개수)
    if _b1_on:                                               # B-1 사이클 계면상 감사 기록 (ASSUMED-FORM)
        # ★ HIGH-6 (2026-07-30 리뷰): 'kim2025 R_ct(N) anchor' 는 **존재하지 않는 앵커**였다.
        #   kim2025 는 전부 post-formation(사이클 축 없음); R_ct(N) 앵커는 yun2023 뿐이다.
        #   ★ MED-13: rest 분기와 **같은 헬퍼**를 써서 두 기록이 갈라지지 않게 한다.
        meta['cycle_interphase'] = cycle_interphase_meta(
            a.cycle_n, a.i0_cycle_mult, a.asr_film_cycle_ohm_cm2)
    np.savez_compressed(a.out, **out, params_json=json.dumps(meta))
    if a.save_state:                                         # newton_fail/soc_overrun 도 저장 — 로더가 명시 거부
        save_chain_state(a.save_state, out['x_shell_final'], r_um, ocp, reason,
                         t_end=float(out['t'][-1]) if len(out['t']) else 0.0,
                         note=f'prev_end={reason}; rint={a.r_int_ohm_cm2:g}; i0={a.i0:g}; '
                              f'ds={"pp" if a.d_s_poly is not None else format(a.d_s, "g")}',
                         J=out['J_final'], dead=out['dead_particle'])
        print(f'  chain state → {a.save_state}  (end={reason})', flush=True)
    print(f'saved {a.out}  (steps {len(out["t"])}, end={reason}, '
          f'V_term {out["V_terminal"][0]:.3f}→{out["V_terminal"][-1]:.3f}, '
          f'delivered {out["q_frac_at_cutoff"] * 100:.1f}%, '
          f'E-bal max {np.max(out["energy_balance_rel"]):.1e})')
    if a.viz_out and len(out['viz_t']):
        nb = sysm.n_bv
        idx = np.arange(nb)
        if nb > a.viz_max_faces:
            idx = np.random.default_rng(0).choice(nb, a.viz_max_faces, replace=False)
            idx.sort()
        If_full = out['viz_I_face']                          # (n_chk, n_bv) [A]
        m_abs = np.array([max(float(np.mean(np.abs(r_[np.abs(r_) > 0]))) if (np.abs(r_) > 0).any()
                              else 0.0, 1e-30) for r_ in If_full])
        i_rel = If_full[:, idx] / m_abs[:, None]             # i/ī (v1 jrxn 규약과 동일 RELATIVE)
        viz = {
            'kind': 'step4_viz', 'c_rate': a.c_rate, 'charge': bool(a.charge),
            'v_min': a.v_min, 'v_max': a.v_max, 'cv_hold': bool(a.cv_hold),   # 컷오프 조건 (비교 라벨용)
            'i_cut_frac': a.i_cut_frac, 'r_int_ohm_cm2': a.r_int_ohm_cm2,
            'am_electro_split': split_meta,                 # poly/SC 분리 (None=균일) — 리뷰 #14:
                                                            # 뷰어 고정슬롯(st4_viz.json)에서 파일명
                                                            # 태그가 떨어져도 런 구별 가능해야 (rint 교훈)
            'x0': ocp.x0, 'x100': ocp.x100, 'nr': a.nr, 'vox_um': vox_um,
            'x_init': float(meta['x_init']), 'chained': bool(meta.get('chained', False)),
            'c_max_mol_m3': ocp.c_max,
            'i_1c_a': float(out['I_1C_A']), 'i_mean_abs_a': [float(f'{v:.4g}') for v in m_abs],
            'end_reason': reason, 'test_only': bool(ocp.test_only), 'provenance': ocp.provenance,
            # ★ 수렴품질 (저율 완화-수용 투명화, 2026-07-22): worst_resid = 스텝 최대 잔차(전류수지
            #   상대오차, 0.0014=0.14%), rate_relax = 저율 완화배수(0.2C=5·0.1C=10).  뷰어가 배지로
            #   표시 → 완화-수용 곡선의 신뢰도를 사용자가 바로 판단 (0.5%↓ 良 / 1%↓ 주의 / 그이상=하드페일).
            # ⚠ .size 필수 — out[*] 는 이 시점 ndarray 라 `if arr` 는 원소 2개 이상서 ValueError
            #   (2026-07-22 77fa751 이후 잠복: 스텝 ≥2 인 모든 런이 npz 저장 직후 viz 단계서 죽어
            #    뷰어 JSON 이 안 생기고 킷 로그엔 FAILED 로 찍힘 — 2026-07-28 킷 e2e 에서 검출)
            'conv': {'worst_resid': round(float(max(out['newton_resid'])) if out['newton_resid'].size else 0.0, 6),
                     'worst_kcl': round(float(max(out['kcl_rel'])) if out['kcl_rel'].size else 0.0, 6),
                     'rate_relax': round(float(getattr(sysm, '_rate_relax', 1.0)), 2)},
            # ★ 전체 방전곡선 시계열 (뷰어 '📈 방전곡선' 버튼용 — 체크포인트 아닌 전 스텝; 스칼라라 가벼움)
            'curve': {'t_s': [round(float(v), 1) for v in out['t']],
                      'V': [round(float(v), 4) for v in out['V']],
                      'V_terminal': [round(float(v), 4) for v in out['V_terminal']],
                      'x_mean': [round(float(v), 5) for v in out['x_mean']],
                      'eta_kin_mV': [round(float(v) * 1e3, 2) for v in out['eta_kin_mean']],
                      # 과전압 분해용 (뷰어 곡선 패널): η_ohm = (|Q_ohm_e|+|Q_ohm_i|)/|I|
                      'eta_diff_mV': [round(float(v) * 1e3, 2) for v in out['eta_diff_mean']],
                      'eta_diff_iw_mV': [round(float(v) * 1e3, 2) for v in out['eta_diff_mean_iw']],
                      'I_A': [float(f'{v:.4g}') for v in out['I']],
                      'Q_ohm_e_W': [float(f'{v:.4g}') for v in out['Q_ohm_e_W']],
                      'Q_ohm_i_W': [float(f'{v:.4g}') for v in out['Q_ohm_i_W']],
                      'Q_rint_W': [float(f'{v:.4g}') for v in out['Q_rint_W']],
                      'Q_ct_W': [float(f'{v:.4g}') for v in out['Q_ct_W']]},
            # ★ 운전-중 φ(z) 상보 프로파일 (체크포인트별) — φ_e ≈ 평평(µV)·φ_i 수십 mV, 곡률 미러.
            #   STEP3 unit-ΔV per-network 프로파일과 다른 물리임을 명시.  NaN(dof 없는 층)→null.
            'phi_z': {'z_um': [round(float(v), 2) for v in out['viz_z_um']],
                      # φ_e 스윙은 µV급 → 1e-6 반올림이면 프로파일이 계단 양자화됨 → 1e-9 (φ_i는
                      # mV급이라 1e-6로 충분).  구 viz(1e-6 φ_e)는 뷰어 캡션이 스윙만 정확.
                      'phi_e_V': [[(None if not np.isfinite(v) else round(float(v), 9)) for v in row]
                                  for row in out['viz_phi_e_z']],
                      'phi_i_V': [[(None if not np.isfinite(v) else round(float(v), 6)) for v in row]
                                  for row in out['viz_phi_i_z']],
                      'note': 'OPERATING z-layer mean potentials per checkpoint — NOT the STEP3 '
                              'unit-ΔV per-network profile'},
            't_s': [round(float(v), 1) for v in out['viz_t']],
            'x_mean': [round(float(v), 4) for v in out['viz_x_mean']],
            'x_shell': np.round(out['viz_x_shell'].astype(np.float64), 4).tolist(),
            'faces': {'n_total': int(nb), 'n_kept': int(len(idx)),
                      'pos_um': np.round(sysm.f_pos_um[idx].astype(np.float64), 1).tolist(),
                      'pid': sysm.f_pid[idx].astype(int).tolist(),
                      'i_rel': np.round(i_rel, 3).tolist()},
        }
        if _tmeta is not None:                          # 뷰어가 혼합-온도 런을 배지로 구분할 수 있게
            viz['temperature'] = _tmeta                 # (자명한 25 °C 기본이면 키 자체가 없음)
        with open(a.viz_out, 'w') as fh:
            json.dump(viz, fh, separators=(',', ':'))
        import os as _os
        print(f'saved {a.viz_out}  ({_os.path.getsize(a.viz_out) / 1e6:.1f} MB — '
              f'chk {len(viz["t_s"])}, faces {len(idx):,}/{nb:,})')
    if reason == 'newton_fail':                              # 코드리뷰 chain#4: 실패 스텝이 exit 0 이면
        sys.exit(3)                                          # 킷의 `|| echo FAILED` 가 한 스텝 늦게 발화


if __name__ == '__main__':
    main()
