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


# ---------------------------------------------------------------- CG (warm start)
def _amg_M(L):
    """pyamg AMG preconditioner (그래프-라플라시안 특화) — 설치 시에만.  실패하면 None."""
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
        ml = pyamg.smoothed_aggregation_solver(sparse.csr_matrix(L), max_coarse=500)
        print(f'    AMG 구축 완료 (levels {len(ml.levels)}, {_t.time() - t0:.0f}s) → CG', flush=True)
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
    solve일 때만 발동(_cg 4단)."""
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
        ml = pyamg.smoothed_aggregation_solver(Ls, B=B, max_coarse=800).aspreconditioner('V')
        return LinearOperator(L.shape, matvec=lambda r, _s=s, _m=ml: _s * _m.matvec(_s * r))
    except Exception as e:
        print(f'    near-null-B AMG 구축 실패 ({type(e).__name__}: {e})', flush=True)
        return None


def _cg(L, b, x0=None, rtol=1e-9, atol=0.0, pc_cache=None, deep=False):
    """3단 솔브: GPU Jacobi-CG → (실패시) CPU AMG-CG(pyamg) → CPU Jacobi-CG.
    실전 격자(VGCF 100 S/cm ↔ BV면 1e-11 S, ~9자릿수 대비)에서 Jacobi 단독은 정체할 수
    있어(2026-07-15 V100 스모크: 50k iter 미수렴) AMG 폴백이 프로덕션 안전망.
    deep=True: 심층-수렴권 정밀 솔브(RHS가 거의 노이즈) — GPU 실패 시 CPU로 내려가지 않고
    'deep_weak'만 기억하고 반환 (35분짜리 무용 CPU-CG 방지; newton 게이트가 수렴 취급).
    pc_cache: 'gpu_dead'=실솔브 GPU 무능(sticky) · 'deep_weak'=심층권 무용 · 'amg'=계층 재사용."""
    diag = L.diagonal()
    cache = pc_cache if pc_cache is not None else {}
    if GPU and not cache.get('gpu_dead'):
        try:
            import cupy as cp
            import cupyx.scipy.sparse as cxs
            from cupyx.scipy.sparse.linalg import cg as cg_gpu
            if L.shape[0] >= 50000:
                print(f'      GPU Jacobi-CG 시도 (≤20k it, ~1분 — 실패 시 AMG 폴백)…', flush=True)
            Lg = cxs.csr_matrix(L.astype(np.float64))
            bg = cp.asarray(b, np.float64)
            Mg = cxs.diags(1.0 / cp.asarray(diag))
            x0g = cp.asarray(x0, np.float64) if x0 is not None else None
            try:
                xg, info = cg_gpu(Lg, bg, x0=x0g, tol=rtol, maxiter=20000, M=Mg)
            except TypeError:
                xg, info = cg_gpu(Lg, bg, x0=x0g, rtol=rtol, atol=atol, maxiter=20000, M=Mg)
            if int(info) == 0:
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
    #   속도만 바꿈(CG는 어떤 SPD M에서도 같은 Jx=b로 수렴) → 물리(해) 완전 불변, 안전.
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
    # ★트리거 수정 (2026-07-23 v100 0.2C 실런 진단): 자기-바닥(_CGStop)이 CG를 ~10×목표서 멈춰 잔차가
    #   1000×문턱에 도달 못 → near-null-B AMG 실전 미발동 = 0.2C hard-fail 근본원인.  near-null 오차는
    #   J·v≈0 라 잔차 norm에 작게 실려 '비율'판정이 부적합 → 판정을 '목표 미달(info≠0=자기-바닥 단축)
    #   + 유의미 초과(>3×목표)'로 전환 (기존 1000× 조건은 belt-and-suspenders로 유지).
    _stall_short = (info != 0 and _rr(x) > 3.0 * _tgt) or (_rr(x) > _NN_TRIGGER * _tgt)
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

    def step(self, dt):
        """CN 한 스텝 (J 고정).  벡터화 Thomas (n_p 동시)."""
        lam = self.D * dt / (self.R ** 2)                   # [n_p]
        aL = self.A_lo / (self.Vk * self.d_rho)             # [nr]
        aH = self.A_hi / (self.Vk * self.d_rho)
        lo = np.outer(lam, aL)                              # [n_p, nr] (k=0 열은 0)
        hi = np.outer(lam, aH)
        hi[:, -1] = 0.0                                     # 표면: 확산항 없음(유속은 소스로)
        dg = lo + hi
        s = np.zeros_like(self.x)
        s[:, -1] = self.J / (self.c_max * self.R) / self.Vk[-1]
        rhs = self.x + 0.5 * (lo * np.roll(self.x, 1, 1) - dg * self.x + hi * np.roll(self.x, -1, 1))
        rhs[:, 0] -= 0.5 * lo[:, 0] * self.x[:, -1]         # roll 오염 가드 (lo[:,0]=0이라 실제 0)
        rhs[:, -1] -= 0.5 * hi[:, -1] * self.x[:, 0]
        rhs += dt * s
        a = -0.5 * lo
        c = -0.5 * hi
        d = 1.0 + 0.5 * dg
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

    def __init__(self, sid, sig_e_tab_S_cm, sig_i_tab_S_cm, pid, n_am, vox_um,
                 z_top_um=None, z_bot_um=0.0):
        vox_m = vox_um * 1e-6
        self.vox_m = vox_m
        sig_e = np.asarray(sig_e_tab_S_cm, np.float64)[sid] * 100.0   # S/m
        sig_i = np.asarray(sig_i_tab_S_cm, np.float64)[sid] * 100.0
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

        SL = ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
              (np.s_[:, :, :-1], np.s_[:, :, 1:]))
        for sl_a, sl_b in SL:
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
        self.gB = sig_e[ii[m], jj[m], kk[m]] * vox_m * vox_m / dist
        self.aB = Ae[m]
        np.add.at(diag0, self.aB, self.gB)
        ii, jj = np.where(top_i); kk = k_last[top_i]
        Ai = idx_i[ii, jj, kk]; m = Ai >= 0
        dist = np.maximum(np.abs(z_p - zc[kk[m]]), 0.5 * vox_um) * 1e-6
        self.gT = sig_i[ii[m], jj[m], kk[m]] * vox_m * vox_m / dist
        self.aT = Ai[m] + self.n_e
        np.add.at(diag0, self.aT, self.gT)                  # 접지(φ=0): diag-only
        # BV 면 목록 (+면 중점 µm 좌표 — 뷰어 표면-반응 필드용; 격자 프레임 = payload µm 프레임)
        am_m = (sid == 1) | (sid == 2)
        ion_m = (sid == 5) | (sid == 6)
        fe, fi, fp, fpos = [], [], [], []
        for d, (sl_a, sl_b) in enumerate(SL):
            for am_first in (True, False):
                slA, slB = (sl_a, sl_b) if am_first else (sl_b, sl_a)
                m = am_m[slA] & ion_m[slB]
                Ae2 = idx_e[slA]; Bi2 = idx_i[slB]
                m &= (Ae2 >= 0) & (Bi2 >= 0)
                if not m.any():
                    continue
                fe.append(Ae2[m]); fi.append(Bi2[m] + self.n_e); fp.append(pid[slA][m])
                pos = np.argwhere(m).astype(np.float32) + 0.5     # 하부 셀 중심 (sliced=하부 인덱스)
                pos[:, d] += 0.5                                  # 축 방향 면 중점
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
            if self.N >= 50000:                             # 대형계 Newton 진행 라인 (침묵 방지)
                print(f'    Newton it{it}: 잔차 {r:.2e} (목표 {tol_rel:.0e}) → 보정해 CG…', flush=True)
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
            atol_cg = 0.05 * float(getattr(self, 'agg_floor_abs', 0.0))
            dphi, info = _cg(self.J, -Fv, x0=None, rtol=1e-5, atol=atol_cg,
                             pc_cache=self._pc_cache, deep=deep)
            self.last_cg_info = max(getattr(self, 'last_cg_info', 0), int(info))
            self._cg_failed = bool(info)
            step = 1.0
            accepted = False
            f2_old = float(np.linalg.norm(Fv))              # ℓ2-merit (∞는 단일노드 거부로 정체 유발)
            for k in range(10):                             # 감쇠: merit 감소 보장 (Armijo c=1e-4)
                Fn, I_fn, eta_n = self.residual(phi + step * dphi, U_f, i0_f, kin, V_app,
                                                I_faces_init=I_f)
                if float(np.linalg.norm(Fn)) <= f2_old * (1.0 - 1e-4 * step):
                    accepted = True
                    break
                step *= 0.5
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
             dudt=None, i0_p=None, n_chk=12, verbose=True):
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
    if i0_p is not None:
        i0_p = np.asarray(i0_p, np.float64)
        if i0_p.shape != (n_am,) or not np.all(i0_p > 0):
            raise ValueError(f'i0_p must be [{n_am}] > 0 (got shape {i0_p.shape})')
    _i0s = None if i0_p is None else i0_p / kin.i0_ref      # 입자별 진폭 스케일 (균일=1.0 → ×1.0 bitwise 불변)
    V_p = 4.0 / 3.0 * np.pi * np.asarray(r_p_m) ** 3        # [m³] 물리 구부피 (용량 기준)
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
    _x_s0 = rad.surf_x()
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
    _next_rec = 0.0

    def _rec_chk(t_now, x_bar_now, I_f_now, phi_now):
        chk['t'].append(float(t_now)); chk['x_mean'].append(float(x_bar_now))
        chk['x_shell'].append(rad.x.astype(np.float16).copy())
        chk['I_face'].append(np.asarray(I_f_now, np.float32).copy())
        _pe, _pi = sys_.phi_z_profiles(phi_now)             # 운전-중 φ(z) 상보 프로파일
        chk['phi_e_z'].append(_pe); chk['phi_i_z'].append(_pi)

    t, dt = 0.0, dt_init
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
        _frac = abs(x_bar - x_ini) / max(_win, 1e-12)
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
    else:
        out['q_frac_at_cutoff'] = float(abs(out['x_mean'][-1] - x_ini) / abs(ocp.x100 - ocp.x0))
    out['x_final_per_particle'] = rad.mean_x()
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
                         cv_hold=bool(cv_hold), r_int_ohm_cm2=r_int_ohm_cm2,
                         c_max=ocp.c_max, x0=ocp.x0, x100=ocp.x100, x_init=x_ini,
                         ocp_provenance=ocp.provenance, test_only=ocp.test_only)
    return out


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
    ap.add_argument('--alpha-a', type=float, default=0.5)
    ap.add_argument('--alpha-c', type=float, default=0.5)
    ap.add_argument('--asr-film', type=float, default=0.0,
                    help='계면 필름 ASR [★Ω·m²★] (SEI/CEI 훅).  ⚠ 단위 주의(리뷰 electrochem#5): 표준 EIS 단위는 '
                         'Ω·cm²인데 이 옵션은 Ω·m² (1 Ω·cm² = 1e-4 Ω·m²).  Ω·cm² 로 넣고 싶으면 아래 '
                         '--asr-film-cycle-ohm-cm2 (자동 ×1e-4 변환)를 쓸 것.')
    # ── B-1 사이클 계면상 성장 (R_int(N) 화학몫; 리뷰 N1-F9 비-이중계산: R_ct=i0(N)↓ 한 채널,
    #    필름옴성=asr-film 별개) ──  ⚠ 성장'값'은 kim2025 R_ct(N) 앵커에서 산출한 배수를 주입
    #    (법칙 N→배수 자동화는 Jung/Conforto fit 후 = §6 N1; 지금은 배수 직접 = ASSUMED-FORM 라벨).
    ap.add_argument('--cycle-n', type=int, default=0,
                    help='B-1 사이클 번호 N (메타·산출물 태그; 0=pristine).  전기화학엔 --i0-cycle-mult/'
                         '--asr-film-cycle가 실제 열화를 주입 — N 자체가 물성을 안 바꿈(법칙 미탑재, §6 N1).')
    ap.add_argument('--i0-cycle-mult', type=float, default=1.0,
                    help='★R_ct 화학몫 채널: i0 → i0×배수 (배수=R_ct,0/R_ct(N)<1 열화; kim2025 앵커).  BV 비선형 '
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
    ap.add_argument('--temp-k', type=float, default=298.15)
    ap.add_argument('--x-init', type=float, default=None, help='초기 stoich (기본: 창 끝)')
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
    if a.i0_poly is not None and a.i0 <= 0:
        # _i0s = i0_p/i0_ref 정규화 분모 — 0이면 0·inf=NaN이 AMG 빌드 후 newton_fail로 오진됨
        # (리뷰 #8 재현: '--i0 0 --i0-poly ...' → 그리드 로드·전처리 다 하고 죽음)
        ap.error('--i0 must be > 0 even with --i0-poly/--i0-sc (값은 상쇄되나 정규화 분모)')
    if a.selftest:
        ok = _selftest_radial()
        ok &= _selftest_cell()
        ok &= _selftest_discharge()
        ok &= _selftest_b1()
        print('STEP4-V2 SELFTEST', 'PASS' if ok else 'FAIL')
        sys.exit(0 if ok else 1)
    if not a.grid:
        ap.error('--grid required (or --selftest)')
    g = np.load(a.grid, allow_pickle=False)
    sid = g['sid']; pid = g['pid']
    vox_um = float(g['vox_um']); z_top = float(g['z_top_um'])
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
              f'[ASSUMED-FORM: 배수=kim2025 R_ct(N) 앵커; N→배수 법칙-fit 후속 §6 N1]', flush=True)
    kin = Kinetics(_i0_use, a.alpha_a, a.alpha_c, _asr_use, a.temp_k)
    sysm = CellSystem(sid, sig_e, sig_i, pid, len(r_um), vox_um, z_top_um=z_top, z_bot_um=0.0)
    out = simulate(sysm, ocp, r_um * 1e-6, ds_arg, kin, a.c_rate, nr=a.nr,
                   v_min=a.v_min, v_max=a.v_max, t_max=a.t_max, charge=a.charge,
                   cv_hold=a.cv_hold, i_cut_frac=a.i_cut_frac,
                   r_int_ohm_cm2=a.r_int_ohm_cm2, x_init=a.x_init, dudt=dudt,
                   i0_p=i0_p, dx_max=a.dx_max, dt_max=a.dt_max, n_chk=a.n_chk)
    meta = out.pop('params')
    reason = out.pop('end_reason')
    meta['end_reason'] = reason
    if split_meta is not None:
        meta['am_electro_split'] = split_meta                # poly/SC 분리 감사 기록 (값+문턱+개수)
    if _b1_on:                                               # B-1 사이클 계면상 감사 기록 (ASSUMED-FORM)
        meta['cycle_interphase'] = {'cycle_n': a.cycle_n, 'i0_cycle_mult': a.i0_cycle_mult,
                                    'asr_film_cycle_ohm_cm2': a.asr_film_cycle_ohm_cm2,
                                    'provenance': 'ASSUMED-FORM: mult=kim2025 R_ct(N) anchor; N→mult law pending fit (§6 N1)'}
    np.savez_compressed(a.out, **out, params_json=json.dumps(meta))
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
            'c_max_mol_m3': ocp.c_max,
            'i_1c_a': float(out['I_1C_A']), 'i_mean_abs_a': [float(f'{v:.4g}') for v in m_abs],
            'end_reason': reason, 'test_only': bool(ocp.test_only), 'provenance': ocp.provenance,
            # ★ 수렴품질 (저율 완화-수용 투명화, 2026-07-22): worst_resid = 스텝 최대 잔차(전류수지
            #   상대오차, 0.0014=0.14%), rate_relax = 저율 완화배수(0.2C=5·0.1C=10).  뷰어가 배지로
            #   표시 → 완화-수용 곡선의 신뢰도를 사용자가 바로 판단 (0.5%↓ 良 / 1%↓ 주의 / 그이상=하드페일).
            'conv': {'worst_resid': round(float(max(out['newton_resid'])) if out['newton_resid'] else 0.0, 6),
                     'worst_kcl': round(float(max(out['kcl_rel'])) if out['kcl_rel'] else 0.0, 6),
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
        with open(a.viz_out, 'w') as fh:
            json.dump(viz, fh, separators=(',', ':'))
        import os as _os
        print(f'saved {a.viz_out}  ({_os.path.getsize(a.viz_out) / 1e6:.1f} MB — '
              f'chk {len(viz["t_s"])}, faces {len(idx):,}/{nb:,})')


if __name__ == '__main__':
    main()
