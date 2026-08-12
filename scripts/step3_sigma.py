#!/usr/bin/env python3
"""STEP3 v1 — electronic-conductivity voxel resistor network for MPM additive structures.

Solves ∇·(σ∇φ)=0 on a voxelized conductive skeleton (AM + VGCF/SuperP/SDCP; SE·PTFE = e-insulators)
between the collector plane (bottom, φ=1) and the top plane (φ=0), finite-volume with HARMONIC-mean
face conductances (phase boundaries handled naturally), and reports:
  · sigma_e_eff  — effective through-plane electronic conductivity (S/cm)
  · per-AM-particle current density (slide-20 colouring: which AM carry the current)
  · per-phase current shares (how much flows through carbon vs AM–AM necks)

DESIGN / TRUST (docs/step3_sigma_network.md):
  · FULL-resolution inputs (se_dump + phase + AM scaffold) — the payload's subsampled clouds would
    fragment bridges (unphysical).  Runs on kgy inside the payload step (mpm_webapp_payload --step3).
  · v1 trust unit = RELATIVE comparison at identical settings (voxel res + σ hooks fixed).  Absolute
    σ_e needs the DEM Stage-E contact-area cross-calibration (sub-voxel constriction NOT modelled —
    a 1-voxel neck's area is quantized to the face area; documented limit).
  · Boundary: lateral walls insulating (Neumann).  The MPM RVE is x,y-periodic; v1 keeps Neumann for
    solver simplicity — identical for all compared runs, so the relative Δσ is unaffected to first
    order (documented).
  · σ table (S/cm), every value overridable:
      AM_S 0.010 / AM_P 0.005   ⚠ **corpus-fit endpoints**, NOT a Trevisanello measurement.
                                  A1 close-out (2026-06-30, docs/a1_sigma_e_direction_closeout.md)
                                  RETRACTED that attribution: Trevisanello 2021 measured Li⁺ chemical
                                  diffusion / BET / R_ct and supports the NCM(r) GB **direction** only.
                                  10/5 = our σ_e scaling-law fit endpoints (live 9.13/4.14) rounded.
                                  ⚠ scale transplant: those endpoints are coefficients of a MACROSCOPIC
                                  effective form; using them as a voxel **phase** σ has an unknown
                                  multiplier (§F1 → null).  Treat as an order-of-magnitude hook.
      VGCF 100 · SuperP 10      ⚠ literature order-of-magnitude hooks (graphitic fibre / CB compact)
                                  ⚠ voxel_conductivity.py(레거시·미사용)는 500/100 — 생산 정본은 이 100/10
      SDCP 250                  USER anchor (2026-07-16; 진성호계 S-PEDOT, interim 150 대체 — code L43).
                                  ⚠ the pellet ×5.1 anchor is COMPOSITE-level — do NOT paste onto a phase σ;
                                  the +52% σ_e is EMERGENT from the network solve.  --sigma-sdcp overrides.
      SE · PTFE 0               (electronic insulators)

Analytic self-tests (python3 scripts/step3_sigma.py --selftest):
  uniform block → σ exactly; series laminate → harmonic mean; parallel laminate → arithmetic mean;
  disconnected slab → σ ≈ 0.  These pin the assembly/BC signs.
"""
import argparse
import sys

import os as _os
import numpy as np
from scipy import ndimage, sparse
from scipy.sparse.linalg import cg

_THIS_DIR = _os.path.dirname(_os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)
import se_material  # single source of truth for σ_ion(SE) + its temperature convention

# ── SE ionic σ (S/cm) — the ONE definition, declared at se_material.T_REF_C = 25 °C ──
# STEP3 itself never hard-coded an SE ionic σ: the sig_i table is built by the caller
# (mpm_webapp_payload --sigma-ion-se).  Re-export it here so every STEP3 consumer reads the
# same number/convention instead of a fresh 0.003 literal, and so the temperature helpers are
# importable from the module that owns the solve.  docs/temp_pressure_capability.md T1-b.
SIGMA_ION_SE_S_CM_25C = se_material.SIGMA_GRAIN_S_CM_25C   # 3.0e-3 S/cm = 3.0 mS/cm (Cronau)


def sigma_ion_se_S_cm(T_C=None, ea_ev=None):
    """SE ionic σ in S/cm.  T_C None (default) → the bare 3.0e-3 literal, bitwise."""
    return se_material.sigma_grain_S_cm(T_C, ea_ev)


def temperature_provenance(T_C=None, ea_ev=None):
    """Provenance block for STEP3 σ outputs (T_C / T_ref_C / Ea_ion_eV / T_dependence)."""
    return se_material.provenance(T_C, ea_ev)


# σ defaults (S/cm) — see module docstring for anchor status
# SDCP 250 = USER-provided anchor UPDATE (2026-07-16; supersedes interim 150 of 2026-07-10,
# 진성호계 S-PEDOT 자릿수).  Still overridable per run.  ⚠ pre-2026-07-16 production outputs
# (DBE +45.4% 등) were solved at 150 — re-run needed for the 250-anchored numbers.
SIGMA_DEFAULT = {'AM_S': 0.010, 'AM_P': 0.005, 'VGCF': 100.0, 'SuperP': 10.0, 'SDCP': 250.0,
                 'SWCNT': 100.0}
SID_NAME = {1: 'AM_S', 2: 'AM_P', 3: 'VGCF', 4: 'SuperP', 5: 'SDCP', 6: 'SE', 7: 'PTFE',
            8: 'SWCNT'}                                    # voxel σ-id → name
#   sid 7 (PTFE) = SENSITIVITY-ONLY: production은 PTFE를 전도 격자에 아예 안 넣음(절연 = void와
#   동일 취급, bulk PTFE σ~1e-16 S/cm).  --sigma-ptfe > 0 민감도 런에서만 payload가 phase-4 점을
#   _apts에 포함시켜 여기로 스탬프됨.
#   sid 8 (SWCNT, A14 sheath) = 전자망 도체 (σ_e VGCF급 ⚠hook — koo2026 0.20 S/cm은 분말-복합체
#   값이지 상(phase) σ가 아님, 이식 금지) + 이온망 기본 = SE-투명(σ_i=σ_ion_se): 실제 skin은
#   2-10nm sub-voxel이라 1-voxel(≈0.4µm) 스탬프가 이온접촉을 끊으면 차단을 40-200× 과대표현
#   (trade-off 상한의 이중계상).  --swcnt-ion-block = 상한 시나리오 opt-in(σ_i=0 → BV면 소멸).

# Set True (mpm_webapp_payload --step3-gpu) to run the Kirchhoff CG on GPU (CuPy cuSPARSE) — a
# multi-M-dof fine-vox solve drops from ~1 h (CPU) to minutes.  Auto-falls back to scipy CPU if
# CuPy/CUDA is unavailable, so it is always safe to leave on.
GPU_SOLVE = False

# ── SR-03: CPU CG 전처리 (기본 OFF = 현행 Jacobi 경로와 **bitwise 동일**) ─────────────────
#   합성 침대 실측 (전자 채널 σ 대비 1e5, rtol 1e-8, scripts/sr03_precond_bench.py — STEP3 의
#   **실제** solve_sigma_z 를 돌리며 전처리만 교체해 σ_eff 까지 비교):
#       dof      61,592 │ 144,888 │ 486,963      Jacobi 시간  3.9 │ 15.6 │ 74.9 s
#       Jacobi it 3,374 │   5,074 │   7,088      AMG 시간(빌드+) 4.5 │ 11.3 │ 51.0 s
#       AMG    it   218 │     222 │     261      속도            0.87× │ 1.38× │ 1.47×
#   ★ 채택 사유 ①은 속도가 아니라 **반복수 절벽**이다.  AMG 는 dof 를 7.9배 늘려도 218→261
#     (평평)인데 Jacobi 는 3,374→7,088 로 자란다 (겉보기 dof^0.36; 구간지수는 0.48→0.28 로
#     일정하지 않아 외삽은 어림값).  production 2.7 M dof 로 어림하면 Jacobi ≈1.3 만 회 =
#     maxiter 30,000 의 절반 — 더 미세한 vox 나 더 높은 대비면 **미수렴("σ UNRELIABLE")**
#     으로 떨어질 여지가 있고, 그때 잃는 것은 시간이 아니라 런 전체다.
#   ⚠ 사유 ②(속도)는 **작다** — 실측 1.4–1.5×, 2.7 M 외삽 ≈2.4×.  벽시계의 진짜 치료는
#     GPU(cupy)다.  AMG 를 "58 분 → 몇 분" 으로 팔지 말 것.  (실제 arm A 2.7 M dof 3,485 s
#     는 위 합성 스케일링의 4.4배 — 실침대가 그만큼 더 어렵다는 뜻이고, 그렇다면 AMG 이득도
#     2.4배보다 클 **것으로 보이나** 그것은 추론이지 측정이 아니다.)
#   ★ 해-불변 확인 (채택의 조건): 같은 계를 두 전처리로 풀고 **σ_eff** 비교 — rtol 1e-8 에서
#     0.0007–0.014 %, rtol 1e-10 에서 0.0001 %.  (‖Δφ‖_rel 은 1e-3 까지 벌어지지만 그 차이는
#     전류를 안 나르는 약결합 영역에 살아 σ 로 넘어오지 않는다.)
#   ⚠ 그래도 **A/B 두 팔은 같은 전처리여야 한다** — 0.01 % 는 작지만 Δσ_e 가 그보다 작을
#     수 있다.  그래서 `LAST_BACKEND['precond']` 를 manifest 에 남기고 비교기가 검사한다.
#   ⚠ v1 은 **CPU 경로 전용**.  GPU 경로는 이미 빠르고, GPU V-cycle 미러는 STEP4 에 선례가
#     있으나(step4_dyn._gpu_vcycle_wrap) 여기 필요가 아직 측정되지 않았다.
#   ⚠ 위는 **합성 침대**다 — 실침대(fibre/AM 분포)에서의 재확인은 SR-01 종료 후.
AMG_SOLVE = False


#: ★ RC6-08 (Codex 6회차): 마지막 solve 의 **실제 backend**.  요청(GPU_SOLVE)과 실제가
#:   다를 수 있는데(CuPy 부재 → CPU fallback) 옛 코드는 print 만 하고 반환 dict 에
#:   backend/gpu_used/fallback_reason 이 전부 없었다 — 결과만 보면 GPU 로 푼 것인지
#:   CPU 로 떨어진 것인지 **구분 불가**였다.  로그는 보존되지 않으므로 산출물에 남긴다.
#:   SR-03 로 `precond` 추가 — 전처리도 요청과 실제가 갈릴 수 있다(pyamg 부재 → Jacobi).
LAST_BACKEND = {'requested': None, 'used': None, 'fallback_reason': None, 'precond': None}


def _amg_M(L):
    """pyamg smoothed-aggregation 전처리 (그래프-라플라시안 특화).  실패하면 None → Jacobi.

    ★ 같은 패턴이 이미 리포에 있다 (`step4_dyn._amg_M`).  그 **코드**를 부르지 않은 이유는
    의존 방향이다 — STEP4 가 STEP3 격자를 소비하므로 STEP3 → STEP4 import 는 역방향이고,
    그 헬퍼는 step4 모듈 전역(GPU, MPM_S4_GPU_AMG)에 묶여 있어 STEP3 에서 부르면 STEP4 의
    GPU 스위치가 STEP3 거동을 조용히 바꾼다.  패턴만 따르고 결합은 만들지 않는다."""
    try:
        import pyamg
    except ImportError:
        LAST_BACKEND['fallback_reason'] = 'pyamg 미설치 → Jacobi'
        print('    ⚠ STEP3 AMG 요청됐으나 pyamg 미설치 → Jacobi-CG 로 진행 '
              '(`python3 -m pip install pyamg`)', flush=True)
        return None
    try:
        import time as _t
        t0 = _t.time()
        print(f'    STEP3 AMG 전처리 구축 중 (dof {L.shape[0]:,})…', flush=True)
        ml = pyamg.smoothed_aggregation_solver(sparse.csr_matrix(L), max_coarse=500)
        print(f'    STEP3 AMG 구축 완료 (levels {len(ml.levels)}, {_t.time() - t0:.0f}s) → CG',
              flush=True)
        return ml.aspreconditioner(cycle='V')
    except Exception as _e:                                # noqa: BLE001 — 전처리 실패는 치명적이지 않다
        LAST_BACKEND['fallback_reason'] = f'AMG build 실패 {type(_e).__name__}: {_e}'
        print(f'    ⚠ STEP3 AMG 구축 실패 ({type(_e).__name__}: {_e}) → Jacobi-CG', flush=True)
        return None


def _solve_cg(L, b):
    """Preconditioned CG for the SPD Kirchhoff system L·φ = b.  GPU (CuPy) when GPU_SOLVE and
    the import succeeds, else scipy CPU — SAME matrix + tol (1e-8) → SAME φ (backend swap only).
    CPU preconditioner = Jacobi (default) or AMG when AMG_SOLVE (SR-03, 해-불변 측정 완료).
    Returns (phi: np.ndarray, info: int).

    ★ 실제로 쓴 backend·전처리를 모듈 전역 `LAST_BACKEND` 에 남긴다 (RC6-08 / SR-03)."""
    diag = L.diagonal()
    LAST_BACKEND.update(requested=('gpu' if GPU_SOLVE else 'cpu'),
                        used=None, fallback_reason=None, precond=None)
    if GPU_SOLVE:
        try:
            import cupy as cp
            import cupyx.scipy.sparse as cxs
            from cupyx.scipy.sparse.linalg import cg as cg_gpu
            Lg = cxs.csr_matrix(L.astype(np.float64))
            bg = cp.asarray(b, dtype=np.float64)
            Mg = cxs.diags(1.0 / cp.asarray(diag))
            try:
                xg, info = cg_gpu(Lg, bg, tol=1e-8, maxiter=30000, M=Mg)
            except TypeError:                              # newer CuPy renamed tol → rtol/atol
                xg, info = cg_gpu(Lg, bg, rtol=1e-8, atol=0.0, maxiter=30000, M=Mg)
            LAST_BACKEND.update(used='gpu', precond='jacobi')   # v1: GPU 경로는 Jacobi 유지
            return cp.asnumpy(xg), int(info)
        except Exception as _e:
            LAST_BACKEND['fallback_reason'] = f'{type(_e).__name__}: {_e}'
            print(f'    STEP3 GPU solve unavailable ({type(_e).__name__}: {_e}) → CPU fallback', flush=True)
    LAST_BACKEND['used'] = 'cpu'
    Minv = _amg_M(L) if AMG_SOLVE else None                # SR-03 opt-in; None → 현행 Jacobi
    LAST_BACKEND['precond'] = 'amg' if Minv is not None else 'jacobi'
    if Minv is None:
        Minv = sparse.diags(1.0 / diag)
    try:
        return cg(L, b, rtol=1e-8, maxiter=30000, M=Minv)
    except TypeError:                                      # scipy < 1.12 has no rtol kwarg
        return cg(L, b, tol=1e-8, maxiter=30000, M=Minv)


def rasterize(am_c, am_r, am_t, add_pts, add_phase, box_lo, box_hi, vox, tol_am_um=0.10, se_pts=None,
              add_fid=None, fid_gap_tol=2.0, add_kind=None):
    """Voxel σ-id grid: 0 = non-conductive, 1 = AM_S, 2 = AM_P, 3.. = additives (2,3,5 → 3,4,5).
    Also returns per-voxel AM particle index (-1 = not AM) for per-particle currents.
    am_t: 1 = AM_P, 2 = AM_S (LIGGGHTS type convention).  All coords in one frame (µm).

    AM-AM CONTACT BRIDGES: a DEM contact's Hertz neck (a ≈ √(Rδ) ~ 0.3-0.5µm) is at/below the
    voxel size, so plain rasterization randomly DROPS touching contacts (6-neighbour faces need
    shared/adjacent voxels) — the integration test showed a non-percolating AM skeleton from
    quantization alone.  Fix = stamp a 1-voxel-radius bridge at the contact midpoint of every
    AM pair with gap ≤ tol_am_um (the SAME contact rule econn uses), σ-id of the SOFTER particle
    (series-conservative).  Neck AREA is thereby quantized to ~vox² — a documented v1 limit,
    identical across compared runs (relative trust preserved)."""
    lo = np.asarray(box_lo, np.float64)
    n = np.maximum(1, np.ceil((np.asarray(box_hi) - lo) / vox).astype(int))
    sid = np.zeros(tuple(n), np.int8)
    pid = np.full(tuple(n), -1, np.int32)
    # SE (sid 6, optional): stamped FIRST = lowest priority — AM / contact bridges / additives
    # overwrite.  Enables the IONIC solve (SE+SDCP conduct; AM/carbon/PTFE ion-block) on the SAME
    # grid: the electronic table just sets σ(SE)=0.  Chunked (tens of millions of points).
    if se_pts is not None and len(se_pts):
        for c0 in range(0, len(se_pts), 8_000_000):
            ijk = np.floor((np.asarray(se_pts[c0:c0 + 8_000_000], np.float64) - lo) / vox).astype(int)
            ok = ((ijk >= 0) & (ijk < n)).all(1)
            ijk = ijk[ok]
            sid[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = 6

    def _ball(centre_um, rad_um, s, particle):
        c = (centre_um - lo) / vox; rr = rad_um / vox
        i0 = np.maximum(0, np.floor(c - rr).astype(int)); i1 = np.minimum(n - 1, np.ceil(c + rr).astype(int))
        if (i1 < i0).any():
            return
        gx, gy, gz = np.ogrid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
        m = ((gx + 0.5 - c[0]) ** 2 + (gy + 0.5 - c[1]) ** 2 + (gz + 0.5 - c[2]) ** 2) <= rr * rr
        sub = sid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
        sub[m] = s
        if particle >= 0:
            psub = pid[i0[0]:i1[0] + 1, i0[1]:i1[1] + 1, i0[2]:i1[2] + 1]
            psub[m] = particle

    for i in range(len(am_c)):                             # AM spheres (few hundred): ball masks
        _ball(am_c[i], am_r[i], 2 if am_t[i] == 1 else 1, i)   # type 1 = AM_P → sid 2; 2 = AM_S → sid 1
    # AM-AM contact bridges (econn contact rule: gap ≤ tol) — NO blanket except here: silently
    # losing every bridge = the fragmented-skeleton σ-collapse the integration test exists to catch
    if len(am_c) >= 2:
        from scipy.spatial import cKDTree
        tree = cKDTree(am_c)
        for i, j in tree.query_pairs(2.0 * float(am_r.max()) + tol_am_um):
            d = float(np.linalg.norm(am_c[i] - am_c[j]))
            if d <= am_r[i] + am_r[j] + tol_am_um:
                mid = am_c[i] + (am_c[j] - am_c[i]) * (am_r[i] + 0.5 * (d - am_r[i] - am_r[j])) / max(d, 1e-12)
                soft = i if am_t[i] == 1 else j            # the LOWER-σ particle = AM_P (0.005 < AM_S 0.010)
                s = 2 if (am_t[i] == 1 or am_t[j] == 1) else 1   # mixed / P-P → AM_P id (series-conservative);
                _ball(mid, 1.2 * vox, s, soft)             #   S-S stays AM_S.  (Review M2: was inverted.)
    # additive points: cell-stamp (carbon overwrites AM at shared cells — the higher-σ phase wins,
    # which is the physical series-shortcut at an anchored contact)
    if add_pts is not None and len(add_pts):
        # ── ★ SR-01 (2026-08-11): 섬유 첨가제의 **점-스탬프는 6-face 연결을 깬다** ──────────
        #   점 간격이 MPM dx 에 묶여 σ-격자와 무관하게 고정돼 있어, 선이 복셀 경계를 비스듬히
        #   지나면 연속한 두 점이 **face 를 공유하지 않는 대각 셀**에 찍힌다.  솔버는 6-face
        #   conductance 를 쓰므로 그 조각들은 **전기적으로 분리**된다.
        #   실침대 실측 (킷 5침대, VGCF 1 wt%, vox 0.4): 섬유의 **68.5–86.4 % 가 평균 2.6–3.4
        #   조각**으로 끊긴다.  선분 스탬프로 바꾸면 단절이 18.4–72.5 % 로 내려가고, 남는 것은
        #   **AM 이 섬유를 끊은 물리적 단절**과 ±4 %p 안에서 일치한다
        #   (docs/data/sr01_realbed_ab.csv · scripts/sr01_realbed_ab.py).
        #   ⚠ 점 재샘플링으로는 못 고친다 (0.02·vox 로 조여도 31 % 잔존) — Codex CR-01.
        #   ⚠ 아티팩트 크기가 **AM 수에 강하게 의존**(+13.9~+50.1 %p) → 조성이 다른 침대끼리
        #     비교하면 **차등 적용**된다 = 공통모드로 상쇄되지 않는다 (Codex CR-02).
        #   ⇒ `add_fid` (섬유 id) 를 주면 **선분 스탬프**로 굽는다.  **기본은 현행 점 스탬프**
        #     (opt-in) — Δσ_e 크기를 재기 전에 default 를 바꾸지 않는다.
        if add_fid is not None and len(add_fid) == len(add_pts):
            ijk, ph = _fibre_segment_ijk(add_pts, add_phase, add_fid, lo, vox, n, fid_gap_tol,
                                         add_kind=add_kind)
        else:
            ijk = np.floor((add_pts - lo) / vox).astype(int)
            ok = ((ijk >= 0) & (ijk < n)).all(1)
            ijk, ph = ijk[ok], add_phase[ok]
        for code, s in ((2, 3), (3, 4), (5, 5), (4, 7), (6, 8)):   # phase → sid (4=PTFE: sensitivity-
            m = ph == code                                  #   only; 6=SWCNT sheath A14 → sid 8)
            if m.any():
                sid[ijk[m, 0], ijk[m, 1], ijk[m, 2]] = s
    return sid, pid


#: ★ fid 가 **경로(폴리라인)** 를 뜻하는 상(相)만.  phase 2=VGCF · 4=PTFE · 6=SWCNT sheath.
#
#   ⚠⚠ 나머지(3=SuperP · 5=SDCP)의 fid 는 **경로가 아니다** — `additives.seed_coat` 계열이
#   `return_ids=True` 로 돌려주는 값이 **AM 구 index** 라, 한 구 표면에 흩어진 수십 점이 같은
#   fid 를 공유한다.  그것을 폴리라인으로 이어 구우면 **구 표면을 무작위 순서로 헤집는 선분**이
#   되고, 실측(구 R=3 µm·47점·vox 0.4)에서 셀이 **45 → 582 (×12.9)** 로 터지며 그중 **87 % 가
#   AM 구 내부**를 채운다 = 탄소를 활물질 안에 그리는 것.
#   ⚠ `gap_tol` 가드는 여기서 **구조적으로 발화하지 않는다** — 간격이 전부 R 스케일로 균일해
#   중앙값의 2배를 넘는 점프가 생기지 않는다 (실측 파단 0 건).
#   ★ 같은 판별이 이미 리포에 있었다: `mpm_webapp_payload` 의 뷰어 폴리라인 마스크
#   (`fib_mask = np.isin(phase, POLYLINE_PHASES) & (fid >= 0)`, 주석까지 달려 있었다).
#   두 번째로 구현하면서 그 가드를 잃은 것이 이 결함이다 → **여기가 단일 소스**이고 payload 가
#   이것을 import 한다.
#   ⚠ 보수적 선택: SuperP-ballmill 의 랜덤워크 **체인**은 진짜 경로지만, fid 만으로는
#   thinky(coat) 와 구분되지 않아 **점 스탬프로 남긴다** (틀린 연결을 만드는 것보다 덜 잇는
#   쪽이 안전).  구분하려면 시더가 per-fid 경로 플래그를 남겨야 한다 — 미착수.
POLYLINE_PHASES = (2, 4, 6)


def _fibre_segment_ijk(add_pts, add_phase, add_fid, lo, vox, n, gap_tol=2.0,
                       polyline_phases=POLYLINE_PHASES, add_kind=None):
    """섬유 점열 → **선분이 지나는 셀** (6-face 연결 보장).  → (ijk, phase)

    ★ 같은 fid 의 연속 점을 경로로 보고 Amanatides–Woo 로 굽는다.  ⚠ 시더가 **AM 안 점을
      드랍**하므로 간격이 `gap_tol·(중앙값 간격)` 을 넘으면 **끊는다** — 안 그러면 폴리라인이
      AM 을 관통해 탄소를 AM 내부에 넣는다 (실측: 셀 수 1.7배 팽창).  남는 단절은 물리다.
    ★ `polyline_phases` 밖의 상은 **점 스탬프로 남긴다** — 그 fid 는 경로가 아니다
      (위 POLYLINE_PHASES 주석 참조).
    """
    from fibre_segment_raster import segment_cells          # 같은 scripts/ 안
    P = np.asarray(add_pts, np.float64)
    F = np.asarray(add_fid)
    PH = np.asarray(add_phase)
    poly = set(int(p) for p in polyline_phases)
    # ★ 시더가 선언한 fid 의미가 있으면 **그것이 이긴다** (additives.ID_PATH/ID_GROUP).
    #   phase 화이트리스트는 옛 산출물용 폴백일 뿐 — SuperP 는 phase 로 못 가른다.
    K = np.asarray(add_kind) if add_kind is not None and len(add_kind) == len(P) else None
    out_ijk, out_ph = [], []
    for f in np.unique(F):
        m = F == f
        Q = P[m]
        if len(Q) == 0:
            continue
        ph_f = PH[m][0]
        is_path = (int(K[m][0]) == 1) if K is not None else (int(ph_f) in poly)
        if not is_path:                                     # ★ 경로가 아닌 fid → 점 스탬프
            cc = np.floor((Q - lo) / vox).astype(int)
            out_ijk.append(cc); out_ph.append(np.full(len(cc), ph_f)); continue
        if len(Q) == 1:
            out_ijk.append(np.floor((Q - lo) / vox).astype(int)); out_ph.append([ph_f]); continue
        d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
        med = float(np.median(d)) if len(d) else 0.0
        brk = (np.nonzero(d > gap_tol * med)[0] + 1) if med > 0 else np.array([], int)
        for R in (np.split(Q, brk) if len(brk) else [Q]):
            if len(R) == 1:
                cc = np.floor((R - lo) / vox).astype(int)
            else:
                seg = [segment_cells(R[i] - lo, R[i + 1] - lo, vox) for i in range(len(R) - 1)]
                cc = np.vstack(seg)
            out_ijk.append(cc); out_ph.append(np.full(len(cc), ph_f))
    if not out_ijk:
        return np.zeros((0, 3), int), np.zeros(0, PH.dtype)
    ijk = np.vstack(out_ijk).astype(int)
    ph = np.concatenate(out_ph)
    ok = ((ijk >= 0) & (ijk < n)).all(1)
    return ijk[ok], ph[ok]


def solve_sigma_z(sid, sigma_of_sid, vox, return_field=False, z_top_um=None, plate_band_um=None,
                  z_bot_um=None, plate_band_bot_um=None, bot_allowed=None, periodic_xy=False):
    """Effective through-plane (z) σ of the voxel σ-id grid.  Finite volume, harmonic-mean face
    conductance g = (2σaσb/(σa+σb))·vox (cubic voxels: face area vox² / distance vox), collector
    plate φ=1 at the bed bottom, φ=0 plate at the bed top, lateral Neumann.

    PLATES = BAND-COUPLED CONTACT SETS (physics review F1): every conductive voxel whose centre
    lies within `band` of its plate PLANE couples with the distance-aware conductance
    g = σ·vox²/max(dist, vox/2).  A single-quantization-layer plate made σ swing ×7.7 under a
    ±0.2µm sub-voxel bed shift (2-4 AM crowns = the whole exit) — the band (default vox+0.1µm,
    capped 1.4·vox: the 0.1µm is the econn contact tol) makes the plate contact set the PHYSICAL
    crown-contact set, restoring cross-scaffold relative trust.  Top plane = z_top_um (bed
    thickness, production) else the top face of the highest AM layer; bottom plane = floor of the
    lowest occupied layer.  σ_eff uses the true plate gap L = z_plate − z_b.
    Returns dict(sigma_eff, n_dof, plate_z_um, n_plate_vox, cg_info, resid, unconverged
    [, phi, cond])."""
    nx, ny, nz = sid.shape
    sig = sigma_of_sid[sid]                                # per-voxel σ (S/cm)
    cond = sig > 0
    if not cond.any():
        return {'sigma_eff': 0.0, 'n_dof': 0, 'n_floating_dropped': 0, 'cg_info': 0, 'resid': 0.0,
                'unconverged': False, 'reason': 'no_conductive_voxels'}
    occ = np.where(cond.any((0, 1)))[0]
    k_bot = int(occ[0])
    am_occ = np.where((((sid == 1) | (sid == 2)) & cond).any((0, 1)))[0]
    k_top_ref = int(am_occ[-1]) if len(am_occ) else int(occ[-1])
    # plate PLANES in CONTINUOUS µm (not voxel-snapped): production passes z_bot=0 (collector)
    # and z_top=thickness — snapping to occupied layers re-introduced sub-voxel plate luck
    # (probe: ×2.8 residual swing) because the plane then hops with the rasterization phase.
    z_b = float(z_bot_um) if z_bot_um is not None else k_bot * vox
    z_plate = float(z_top_um) if z_top_um is not None else (k_top_ref + 1) * vox
    z_plate = min(z_plate, nz * vox)
    if z_plate - z_b <= 1.5 * vox:                         # degenerate (≈1-layer bed) → no through-path
        return {'sigma_eff': 0.0, 'n_dof': int(cond.sum()), 'n_floating_dropped': 0, 'cg_info': 0,
                'resid': 0.0, 'unconverged': False, 'reason': 'degenerate_thin_bed'}
    band = plate_band_um if plate_band_um is not None else (vox + 0.10)
    # BOTTOM band override (collector GEOMETRY axis): 'wetted/primer' = default band (vox+0.1 —
    # a conformal conductive film reaches ~0.2µm gaps, + quantization half-voxel); 'bare' passes a
    # TIGHTER band (0.5·vox+0.1 = true-contact crowns only) → fewer collector contacts → the exit
    # current funnels through crown contacts and the per-AM je map redistributes near the collector
    # (the primer-paper Fig-4d red-box story).  ±half-voxel quantization blur documented.
    band_bot = plate_band_bot_um if plate_band_bot_um is not None else band
    zc = (np.arange(nz) + 0.5) * vox                       # voxel-centre heights
    # PER-COLUMN SINGLE CONTACT (review F1, final form): each lateral column couples to a plate
    # through ONE voxel — its surface voxel — iff that surface is within `band` of the plane,
    # with distance-aware g.  A layer-band coupled a column through TWO layers whenever the band
    # edge crossed a voxel centre (probe: plate-voxel count 54→278 on a +0.1µm shift, σ ×2) —
    # per-column contact makes the plate set the physical crown patch and σ vary smoothly.
    any_c = cond.any(2)
    k_first = np.argmax(cond, axis=2)                      # column's lowest conductive voxel
    k_last = nz - 1 - np.argmax(cond[:, :, ::-1], axis=2)  # column's highest conductive voxel
    bot_m = any_c & (zc[k_first] - z_b <= band_bot)
    # ANALYTIC contact mask (v3, optional): [nx,ny] bool from EXACT sphere/point z (payload computes
    # it — gap ≤ 0.1µm bare / ≤ 0.3µm film-wetted).  Voxel-centre bands cannot resolve below
    # ~half-voxel; the analytic mask removes that blur — the SELECTION is exact, only the coupling
    # conductance stays voxel-scale.
    if bot_allowed is not None:
        bot_m &= np.asarray(bot_allowed, bool)
    top_m = any_c & (z_plate - zc[k_last] <= band)
    if not bot_m.any() or not top_m.any():
        return {'sigma_eff': 0.0, 'n_dof': int(cond.sum()), 'n_floating_dropped': 0, 'cg_info': 0,
                'resid': 0.0, 'unconverged': False,
                'reason': f'no_plate_contact(bot={int(bot_m.sum())},top={int(top_m.sum())},'
                          f'z_b={z_b:.2f},z_plate={z_plate:.2f},band={band:.2f})'}
    # FLOATING ISLANDS (components touching NEITHER plate contact) = singular blocks, zero current
    # by physics → dropped (their je reads 0).
    # ★ 리뷰 B#1 caveat: 이 label 은 6-connectivity(비주기)라 periodic_xy=True 의 x/y wrap 커플링을
    #   모른다.  σ_z/thermal/pore 는 무해(plate 안 닿는 성분은 어차피 net through-flux 0=dangling).
    #   solve_reaction_current 은 seam으로만 본류에 붙은 경계 patch의 BV 반응전류를 0으로 과소계상할
    #   수 있으나, 프로덕션 조밀 베드는 본류가 bulk로 x=0 에 닿아 실질 영향 미미(경계 몇 입자).
    lab, _nl = ndimage.label(cond)                         # 6-connectivity = the face-coupling graph
    _ii, _jj = np.where(bot_m); _lb = lab[_ii, _jj, k_first[bot_m]]
    _ii, _jj = np.where(top_m); _lt = lab[_ii, _jj, k_last[top_m]]
    plate = np.unique(np.concatenate([_lb, _lt]))
    plate = plate[plate > 0]
    # ★ 2026-08-12 (Codex #2): `plate` 는 **합집합** = "한쪽 플레이트에라도 닿는" 성분이다.
    #   솔브에는 옳다 — 한쪽만 닿는 성분은 Dirichlet 이 걸려 특이하지 않고 net through-flux 가
    #   0 이라 σ_eff 에 기여하지 않는다.  그러나 그 n_dof 로 만든 `eps_connected_pct` 를
    #   "관통 공극률" 로 읽으면 **과대**다.  ⇒ 교집합(양쪽 다 닿음)을 **따로 세어** 병기한다.
    #   솔브 경로는 그대로 (측정만 추가).
    _sb = set(np.unique(_lb[_lb > 0]).tolist())
    _st = set(np.unique(_lt[_lt > 0]).tolist())
    _through = np.array(sorted(_sb & _st), dtype=lab.dtype)
    n_through_dof = int(np.isin(lab, _through).sum()) if len(_through) else 0
    n_float = int(cond.sum())
    cond &= np.isin(lab, plate)
    n_float -= int(cond.sum())
    n_dof = int(cond.sum())
    n_plate_reachable_dof = n_dof                          # = 합집합 (이름을 정직하게)
    if n_dof == 0:
        return {'sigma_eff': 0.0, 'n_dof': 0, 'n_floating_dropped': n_float, 'cg_info': 0,
                'resid': 0.0, 'unconverged': False, 'reason': 'all_floating_dropped'}
    sig = np.where(cond, sig, 0.0)
    idx = -np.ones(sid.shape, np.int64)
    idx[cond] = np.arange(n_dof)

    rows, cols, vals = [], [], []
    diag = np.zeros(n_dof, np.float64)
    b = np.zeros(n_dof, np.float64)

    def couple(sl_a, sl_b):
        A, B = idx[sl_a], idx[sl_b]
        sa, sb = sig[sl_a], sig[sl_b]
        m = (A >= 0) & (B >= 0)
        if not m.any():
            return
        g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox   # σ[S/cm]·vox[µm] — unit cancels in σ_eff
        a2, b2 = A[m], B[m]
        rows.append(a2); cols.append(b2); vals.append(-g)
        rows.append(b2); cols.append(a2); vals.append(-g)
        np.add.at(diag, a2, g); np.add.at(diag, b2, g)

    couple(np.s_[:-1, :, :], np.s_[1:, :, :])
    couple(np.s_[:, :-1, :], np.s_[:, 1:, :])
    couple(np.s_[:, :, :-1], np.s_[:, :, 1:])
    if periodic_xy:                                        # ★x,y 주기 wrap (MPM RVE 'boundary p p f' 정합;
        if nx > 1:                                         #   z=plate 유지).  nx/ny=1이면 자기결합 방지 가드.
            couple(np.s_[-1:, :, :], np.s_[:1, :, :])      # x: nx-1 ↔ 0
        if ny > 1:
            couple(np.s_[:, -1:, :], np.s_[:, :1, :])      # y: ny-1 ↔ 0
    # per-column plate couplings, distance-aware: g = σ·vox²/max(dist, vox/2) (= 2σ·vox at half-cell)
    def _plate_couple(mask, ksurf, plane, phi_p):
        ii, jj = np.where(mask)
        kk2 = ksurf[mask]
        A = idx[ii, jj, kk2]; sa = sig[ii, jj, kk2]
        m = A >= 0
        if not m.any():
            return 0, None, None
        dist = np.maximum(np.abs(zc[kk2[m]] - plane), 0.5 * vox)
        g = sa[m] * vox * vox / dist
        np.add.at(diag, A[m], g)
        if phi_p != 0.0:
            np.add.at(b, A[m], g * phi_p)
        return int(m.sum()), A[m], g
    n_pb, _Ab, _gb = _plate_couple(bot_m, k_first, z_b, 1.0)
    n_pt, _At, _gt = _plate_couple(top_m, k_last, z_plate, 0.0)
    L = sparse.coo_matrix((np.concatenate(vals + [diag]),
                           (np.concatenate(rows + [np.arange(n_dof)]),
                            np.concatenate(cols + [np.arange(n_dof)]))),
                          shape=(n_dof, n_dof)).tocsr()
    print(f'    STEP3 solve: {n_dof:,} dof, plate contacts {n_pb:,}/{n_pt:,} — CG running '
          f'({"GPU" if GPU_SOLVE else "CPU"}, 수 분 소요 가능)…', flush=True)
    phi, info = _solve_cg(L, b)
    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
    unconv = bool(info) or resid > 1e-6                    # review F2: NEVER ship a silent bad σ
    if unconv:
        print(f'  ⚠ STEP3 CG not converged (info={info}, resid={resid:.1e}) — σ UNRELIABLE')
    # total current through the bottom plate: I = Σ g_b·(1 − φ)
    I = float(np.sum(_gb * (1.0 - phi[_Ab]))) if _Ab is not None else 0.0
    # σ_eff = I·L/(A·ΔV): L = plate gap (µm), A = nx·ny·vox² → σ_eff in the σ-table unit (S/cm)
    sigma_eff = max(0.0, I * (z_plate - z_b) / (nx * ny * vox * vox))
    out = {'sigma_eff': float(sigma_eff), 'n_dof': n_dof, 'n_floating_dropped': n_float,
           # ★ n_dof 는 **합집합**(한쪽 플레이트에라도 닿음).  아래 둘을 병기해 이름을 정직하게.
           'n_plate_reachable_dof': n_plate_reachable_dof,      # ≡ n_dof (legacy: either_plate)
           'n_through_dof': n_through_dof,                      # 교집합 = 양 플레이트 관통
           'plate_z_um': (round(z_b, 3), round(z_plate, 3)), 'n_plate_vox': (n_pb, n_pt),
           'k_plates': (k_bot, k_top_ref), 'cg_info': int(info) if info else 0, 'resid': resid,
           'unconverged': unconv}
    if return_field:
        P = np.zeros(sid.shape, np.float64); P[cond] = phi
        out['phi'] = P; out['cond'] = cond
    return out


def per_particle_current(res, sid, pid, sigma_of_sid, n_am):
    """Mean |J_z| PROXY per AM particle (z-face current g·Δφ ∝ J_z·vox² — run-relative, the
    viewer percentile-normalizes; NOT vox-invariant across runs) — the slide-20 axis."""
    if 'phi' not in res:                                   # early-returned solve (see res['reason'])
        return np.zeros(n_am, np.float64)
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    jz = np.zeros(sid.shape, np.float64)
    sa, sb = sig[:, :, :-1], sig[:, :, 1:]
    both = cond[:, :, :-1] & cond[:, :, 1:]
    g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
    dphi = P[:, :, :-1] - P[:, :, 1:]
    f = g * dphi                                           # face current ∝ σ·Δφ (per face area vox²)
    jz[:, :, :-1] += np.abs(f) * 0.5
    jz[:, :, 1:] += np.abs(f) * 0.5
    je = np.zeros(n_am, np.float64); nv = np.zeros(n_am, np.int64)
    m = pid >= 0
    np.add.at(je, pid[m], jz[m]); np.add.at(nv, pid[m], 1)
    return np.where(nv > 0, je / np.maximum(nv, 1), 0.0)


def phase_current_share(res, sid, sigma_of_sid):
    """Fraction of total dissipation per σ-id (where the current actually flows)."""
    if 'phi' not in res:
        return {}
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    diss = np.zeros(sid.shape, np.float64)
    for sl_a, sl_b in ((np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
                       (np.s_[:, :, :-1], np.s_[:, :, 1:])):
        both = cond[sl_a] & cond[sl_b]
        sa, sb = sig[sl_a], sig[sl_b]
        g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
        d = g * (P[sl_a] - P[sl_b]) ** 2                   # per-face dissipation; split ∝ each side's
        wa = np.where(both, sb / np.maximum(sa + sb, 1e-30), 0.0)   # RESISTANCE (review F4 — the old
        diss[sl_a] += wa * d; diss[sl_b] += (1.0 - wa) * d          # half-half gave carbon 50% at a
        #   1e4-contrast face where it truly dissipates ~0.01%)
    tot = diss.sum()
    out = {}
    for s in np.unique(sid[sid > 0]):
        out[int(s)] = float(diss[sid == s].sum() / max(tot, 1e-30))
    return out


# ── STEP3 열전도 (σ_thermal) — 범용 Laplace 솔버(solve_sigma_z) 재사용, 多상 k 맵 ──────────────
# k 값 (W/cm·K; ×100 = W/m·K).  ★SE=문헌앵커(Ketter 2025 = LPSCl/SE 논문); AM=generic NCM 문헌-order
# (전용 인용 없음; network_conductivity.py의 uncited NCM 기본과 同값 — Ketter 아님[Ketter는 SE]),
# carbon/SDCP/PTFE/pore = ASSUMED order-of-mag (라벨 · 소체적분율이라 k_eff 영향 작음 · 스윕용).
K_AM_THERMAL = 4.0e-2    # NCM, ≈4 W/m·K  [generic NCM 문헌-order; 전용 인용 없음, NOT Ketter(=SE)]
K_SE_THERMAL = 0.7e-2    # LPSCl, ≈0.7 W/m·K  [lit: Ketter 2025 (LPSCl thermal)]
K_PTFE_THERMAL = 2.5e-3  # PTFE, ≈0.25 W/m·K  [polymer generic; 전용 인용 없음]
K_PORE_THERMAL = 0.0     # 압밀 ASSB 공극(Ar/진공, ~7% 고립) → 무시 [ASSUMED; 가스면 ~2.6e-4]


def thermal_k_table(k_am=K_AM_THERMAL, k_se=K_SE_THERMAL, k_carbon=None, k_sdcp=None,
                    k_ptfe=K_PTFE_THERMAL, k_pore=K_PORE_THERMAL):
    """sid-indexed 열전도 k 배열 (_sig3 電子표와 동일 레이아웃: 0=pore,1=AM_S,2=AM_P,3=VGCF,
    4=SuperP,5=SDCP,6=SE,7=PTFE,8=SWCNT).  ★열은 多상: σ_e(AM만)/σ_ion(SE만)과 달리 全상이 열
    통과 → SE(6)·PTFE(7)는 0 아님(pore는 기본 0=진공 가정).  carbon(VGCF/SuperP/SWCNT) 기본 =
    k_am(도체≥AM 보수적 ASSUMED, --k-carbon 상향 스윕 권장); SDCP 기본 = k_se.  반환 (k_array, prov)."""
    kc = k_am if k_carbon is None else float(k_carbon)
    ks = k_se if k_sdcp is None else float(k_sdcp)
    prov = {'AM(NCM)': f'{k_am*100:.1f} W/mK [generic NCM 문헌-order; 전용 인용 없음 — NOT Ketter(=LPSCl/SE); '
                       'network_conductivity.py uncited NCM 기본과 同값]',
            'SE(LPSCl)': f'{k_se*100:.2f} W/mK [lit Ketter2025 (LPSCl thermal)]',
            'carbon(VGCF/SuperP/SWCNT)': f'{kc * 100:.1f} W/mK [ASSUMED ~AM 하한; 소분율·--k-carbon 상향 스윕]',
            'SDCP': f'{ks * 100:.2f} W/mK [ASSUMED ~SE; ⚠전자적으론 최강도체 → k_carbon가 더 맞을 수(스윕)]',
            'PTFE': f'{k_ptfe * 100:.2f} W/mK [polymer generic; 전용 인용 없음]',
            'pore': f'{k_pore * 100:.3f} W/mK [ASSUMED 압밀ASSB≈0(진공/고립)]',
            'caveats': 'k_eff = 문헌/ASSUMED k 입력의 복셀-solve 전파값 — 열전도 실험 앵커 없음(Kapitza 계면 '
                       '열저항 무시 → 상한); network_conductivity thermal과 같은 k 앵커 공유 → 표현(복셀-field '
                       'vs 입자-graph)-일치만이지 입력·물리 검증 아님, 스케일도 다름(W/mK vs mScm-eq), 독립 아님'}
    return np.array([k_pore, k_am, k_am, kc, kc, ks, k_se, k_ptfe, kc], float), prov


def solve_thermal(sid, vox, z_top_um, z_bot_um=0.0, k_table=None, field_sids=None, field_max=90000,
                  periodic_xy=False):
    """복셀 through-plane 열전도 k_eff + 상별 ΔT/열저항(병목) 몫.  solve_sigma_z 재사용(∇·(k∇T)=0, 同 격자).
    ★多상이라 압밀 베드선 全상 연결 → 보통 항상 퍼콜(유한).  반환: k_eff_W_mK(=k_eff[W/cm·K]×100, ★Kapitza
    무시 상한), temp_drop_share(상별 through-plane 온도강하/열저항 몫 — 높을수록 열 병목; ★열류 아님 —
    직렬 flux는 상별 동일), n_dof, cg_resid, reason/unconverged.
    field_sids 주면 out['_field_pts']/['_field_j'] = 열류 |k∇T| 점군(電子/이온 필드와 동일 문법, 多상=全상
    solid; payload가 p99.8 정규화·직렬화 — '_' prefix = JSON 前 임시)."""
    if k_table is None:
        k_table, _ = thermal_k_table()
    res = solve_sigma_z(sid, k_table, vox, return_field=True, z_top_um=z_top_um, z_bot_um=z_bot_um,
                        periodic_xy=periodic_xy)
    out = {'k_eff_W_mK': None, 'reason': res.get('reason'), 'n_dof': int(res.get('n_dof', 0)),
           'cg_resid': float(f"{res.get('resid', 0.0):.2g}"), 'unconverged': bool(res.get('unconverged'))}
    if not res.get('reason') and res.get('n_dof'):
        out['k_eff_W_mK'] = float(f"{res['sigma_eff'] * 100.0:.4g}")   # W/cm·K → W/m·K
        # phase_current_share = ∝ k(∇T)² 소산 functional의 상별 분담 = through-plane ΔT/열저항 몫(병목).
        # ★열류(∝ k∇T) 아님 — 정상 전도 ∇·(k∇T)=0 은 소산 0, 직렬 flux 상별 동일.
        share = phase_current_share(res, sid, k_table)
        out['temp_drop_share'] = {SID_NAME[k]: round(v, 4) for k, v in share.items()}
        # ★ T(z) 프로파일 원자료 — 전자/이온이 phi_profile 을 갖는 것과 같은 자격을 열전도에도 준다.
        #   (2026-08-04: 뷰어가 열류·Joule 모드에서 **전자 φ(z)** 를 그리고 있었다 — 열전도는 자기
        #    solve 의 정규화 온도 T(z)@ΔT=1 이 있어야 한다.)  '_' prefix = JSON 前 pop 대상.
        out['_res'] = res
        if field_sids is not None:                             # 열류 |k∇T| 점군 (多상 = 全상 solid conduct)
            fp, fj = field_point_cloud(res, sid, k_table, vox, tuple(field_sids), max_points=field_max)
            if fp is not None:
                out['_field_pts'] = fp
                out['_field_j'] = fj
    return out


def carbon_se_contact_area(sid, vox):
    """탄소(VGCF 3·SuperP 4·SWCNT 8) ↔ SE(6) 복셀-면 접촉 면적 (µm²).
    kim2024 Fig3b: NCM–SE–carbon 3상 계면이 sulfide SE 전기화학 분해를 촉매 → 이 면적이
    STEP5 VGCF-촉매 화학열화(carbon_se_area)의 구조 입력.  phase_current_share 면-순회와 동일 규약."""
    carb = np.isin(sid, (3, 4, 8)); se = (sid == 6)
    faces = 0
    for a, b in ((np.s_[:-1, :, :], np.s_[1:, :, :]),
                 (np.s_[:, :-1, :], np.s_[:, 1:, :]),
                 (np.s_[:, :, :-1], np.s_[:, :, 1:])):
        faces += int((carb[a] & se[b]).sum()) + int((se[a] & carb[b]).sum())
    return float(faces) * vox * vox


def _voxel_jmag(P, cond, sig):
    """Cell-centred |J| proxy (∝ σ·Δφ, run-relative) — per_particle_current 와 동일 규약.
    각 축의 양면 전류 |g·Δφ|(g=조화평균 컨덕턴스)를 셀에 반씩 배분 → |J|=√(ΣJ축²).
    field_point_cloud·joule_hotspot 공유(단일 소스, 중복 제거)."""
    jmag = np.zeros(sig.shape, np.float64)
    for axis in (0, 1, 2):
        sa_sl = [slice(None)] * 3; sb_sl = [slice(None)] * 3
        sa_sl[axis] = slice(0, -1); sb_sl[axis] = slice(1, None)
        sa_sl, sb_sl = tuple(sa_sl), tuple(sb_sl)
        both = cond[sa_sl] & cond[sb_sl]
        sa, sb = sig[sa_sl], sig[sb_sl]
        g = np.where(both, 2.0 * sa * sb / np.maximum(sa + sb, 1e-30), 0.0)
        f = np.abs(g * (P[sa_sl] - P[sb_sl]))               # face current ∝ σ·Δφ (per face area)
        comp = np.zeros(sig.shape, np.float64)
        comp[sa_sl] += f * 0.5
        comp[sb_sl] += f * 0.5
        jmag += comp * comp
    return np.sqrt(jmag)


def joule_hotspot(res, sid, sigma_of_sid, vox, sel_sids, box_lo=(0.0, 0.0, 0.0),
                  max_points=40000, hot_budget_frac=0.35, seed=1):
    """#29 — 복셀 Joule 발열밀도 q ∝ |J|²/σ (run-relative) 점군 = '어디서 발열이 몰리는지' hot-spot MAP.
    전류가 구속(소수 percolating neck)에 몰리고 σ 낮은 곳에서 q 최대 → 발열 hot-spot.  field_point_cloud
    와 동일 |J|(_voxel_jmag) 재사용 = 순수 readout(재솔브 없음, σ 불변).  전자망(sel_sids=AM+carbon)에 적용.
    ★한계 (정직): 절대 ΔT(K) 온도상승은 Poisson 열확산(∇·(k∇ΔT)=−q) + 실전류 스케일 + LPSCl 분해
    Arrhenius Eₐ 앵커가 필요(미보유) → v2.  이 함수는 발열 '생성' 분포(hot-spot 위치)까지만 정직 산출.
    Returns dict(pts_um [N,3], q [N], hot_frac_50, conc_ratio, n) 또는 None.  viewer가 percentile 정규화."""
    if 'phi' not in res:
        return None
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    jmag = _voxel_jmag(P, cond, sig)
    q = np.where(cond, jmag * jmag / np.maximum(sig, 1e-30), 0.0)     # 발열밀도 (run-relative, W/cm³ 스케일 전)
    sel = np.isin(sid, np.asarray(list(sel_sids), np.int64)) & cond & (q > 0)
    ii, jj, kk = np.where(sel)
    if not len(ii):
        return None
    vals = q[ii, jj, kk]
    # hot-spot 집중도: q 총합의 50%를 담는 상위-복셀 분율 (작을수록 집중=hot-spot 뚜렷) + 최대/평균 비
    srt = np.sort(vals)[::-1]; cum = np.cumsum(srt); tot = float(cum[-1])
    hot_frac_50 = float((np.searchsorted(cum, 0.5 * tot) + 1) / len(vals)) if tot > 0 else 0.0
    conc_ratio = float(vals.max() / max(vals.mean(), 1e-30))
    if len(ii) > max_points:                                          # field_point_cloud 규약: 상위 hot 유지 + 균일 배경
        rng = np.random.default_rng(seed)
        order = np.argsort(vals)[::-1]
        n_hot = int(max_points * hot_budget_frac)
        pick = np.concatenate([order[:n_hot], rng.choice(order[n_hot:], size=max_points - n_hot, replace=False)])
        ii, jj, kk, vals = ii[pick], jj[pick], kk[pick], vals[pick]
    pts = np.stack([(ii + 0.5) * vox + box_lo[0], (jj + 0.5) * vox + box_lo[1],
                    (kk + 0.5) * vox + box_lo[2]], axis=1).astype(np.float32)
    return {'pts': pts, 'q': vals.astype(np.float32), 'hot_frac_50': hot_frac_50,
            'conc_ratio': conc_ratio, 'n': int(len(vals))}


def field_point_cloud(res, sid, sigma_of_sid, vox, sel_sids, box_lo=(0.0, 0.0, 0.0),
                      max_points=40000, hot_budget_frac=0.35, seed=1):
    """Per-voxel current-density MAGNITUDE sampled at the selected conducting phase(s), as a
    subsampled point cloud for a paper-style field figure (Fig-2/Fig-4 grammar).

    Reuses the SAME validated (phi, cond) the solve returned (return_field=True) — this is a pure
    READOUT, it does not re-solve or change σ.  The cell-centred |J| proxy mirrors
    per_particle_current EXACTLY: for each of the 3 axes the two bounding face currents |g·Δφ| are
    half-split onto the cell (g = 2σaσb/(σa+σb) = the SAME harmonic-mean conductance the matrix
    used — so a high-σ phase such as SDCP actually lights up), then |J| = √(Jx²+Jy²+Jz²).
    Run-relative (∝ σ·Δφ; the viewer percentile-normalises); NOT vox-invariant across runs.

    sel_sids : iterable of σ-ids to KEEP (electronic field → AM+carbon {1,2,3,4,5};
               ionic field → SE+SDCP {5,6}).  Only voxels that are BOTH sel AND conductive (in the
               plate-connected component `cond`) are emitted — floating islands already dropped.
    Returns (pts_um [N,3] float32, jmag [N] float32) in the payload µm frame (voxel centres +
    box_lo), or (None, None) if the solve early-returned / nothing selected.

    Subsample keeps ALL of the hottest `hot_budget_frac` of the budget (so the conduction
    backbone survives at low point counts) + a uniform-random background for honest density."""
    if 'phi' not in res:
        return None, None
    P, cond = res['phi'], res['cond']
    sig = sigma_of_sid[sid]
    jmag = _voxel_jmag(P, cond, sig)
    sel = np.isin(sid, np.asarray(list(sel_sids), np.int64)) & cond
    ii, jj, kk = np.where(sel)
    if not len(ii):
        return None, None
    vals = jmag[ii, jj, kk]
    if len(ii) > max_points:
        rng = np.random.default_rng(seed)
        order = np.argsort(vals)[::-1]
        n_hot = int(max_points * hot_budget_frac)
        hot = order[:n_hot]
        rest = rng.choice(order[n_hot:], size=max_points - n_hot, replace=False)
        pick = np.concatenate([hot, rest])
        ii, jj, kk, vals = ii[pick], jj[pick], kk[pick], vals[pick]
    pts = np.stack([(ii + 0.5) * vox + box_lo[0],
                    (jj + 0.5) * vox + box_lo[1],
                    (kk + 0.5) * vox + box_lo[2]], axis=1)
    return pts.astype(np.float32), vals.astype(np.float32)


def pore_tau(sid, vox, z_top_um, extra_solid_pts=None, box_lo=(0.0, 0.0, 0.0), periodic_xy=False):
    """A6 — PORE-phase effective-diffusion tortuosity (DiffuDict/TauFactor convention).

    Runs the SAME validated finite-volume machinery (solve_sigma_z, physics unchanged) on the
    VOID phase: σ(void)=1, σ(solid)=0, plates at z=0 / z_top → the returned sigma_eff IS the
    dimensionless D_eff/D0.  τ = ε_total / (D_eff/D0)   [tortuosity FACTOR: D_eff = D0·ε/τ].

    Conventions (honest):
      • PTFE is NOT rasterized into the e/ionic sid grid (insulator on both networks), so sid==0
        alone would read PTFE volume as open pore (ε over-count → τ under-count).  Its material
        points must be passed via extra_solid_pts (µm, grid frame) — stamped solid here, same
        single-voxel stamp convention rasterize() uses for additive points.
      • the grid is CROPPED to z ≤ z_top_um first (REQUIRED arg: without it the top plate would
        sit on the rasterization box's void padding cap and ε/D_rel measure the cap, not the
        bed).  Uncropped, every column's topmost pore voxel floats in that cap and the top
        plate loses/keeps contact by sub-voxel luck.
      • plate band = vox EXACTLY (review M1) — NOT the e-solve default vox+0.1: after the crop a
        true surface pore's centre is provably < vox from its plate plane while a pore ROOFED by
        one solid voxel is ≥ vox away, so band=vox separates open from sealed at both plates.
        The e-solve's +0.1 µm is crown-contact physics (a plate PRESSES onto crowns); for the
        pore there is no press — solid above a pore genuinely seals it.  With the default band,
        D_rel leaked through 1-voxel roofs whenever frac(z_top/vox) ∈ [0.5, 0.75) (τ<1 possible).
      • ε_total counts ALL void voxels of the cropped domain (isolated pores included —
        TauFactor convention: closed porosity RAISES τ); ε_connected (plate-reaching component)
        is reported alongside — None when the solve early-returns before the floating-island
        filter (its n_dof then counts ALL pore voxels, review m2).  D_rel below 1e-12
        (non-percolating pore) → tau=None.
      • known small biases (review m1/m4, documented not fixed): ε is measured over the cropped
        height nzc·vox while D_rel is normalised by L=z_top → one-sided τ over-read ≤ 0.5·vox/
        z_top (+0.67 % worst at 30 µm/vox 0.4, exact when frac(z_top/vox)<0.5); the AM-AM
        contact-bridge balls rasterize() stamps (1.2·vox Hertz-neck proxy) count as solid here
        (~2 % of the pore phase at ε≈15 % — a real neck does occupy that space).
      • STRUCTURAL descriptor (frame[4] cross-check / gas·liquid-infiltration axis).  ASSB Li⁺
        transport lives on the SE contact network (σ_ionic solves) — do NOT substitute this τ
        into the transport forms (CLAUDE.md audit #2 double-count trap).

    Returns dict(eps_total_pct, eps_connected_pct, D_rel, tau, n_dof, resid, unconverged
                 [, reason])."""
    if z_top_um is None or float(z_top_um) <= 0.0:
        raise ValueError('pore_tau requires z_top_um > 0 (bed thickness): without the crop the '
                         'void padding cap above the bed is measured instead of the pore network')
    s = np.asarray(sid)
    nzc = int(np.floor(float(z_top_um) / vox + 0.5))        # top-layer centre stays ≤ plate plane
    nzc = max(2, min(s.shape[2], nzc))
    s = s[:, :, :nzc].copy()
    if extra_solid_pts is not None and len(extra_solid_pts):
        ijk = np.floor((np.asarray(extra_solid_pts, np.float64) - np.asarray(box_lo, np.float64))
                       / vox).astype(int)
        ok = ((ijk >= 0) & (ijk < np.array(s.shape))).all(1)
        ijk = ijk[ok]
        s[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = 7               # any non-zero id = solid to the pore solve
    pore = (s == 0)
    eps = float(pore.mean())
    if eps <= 0.0:
        return {'eps_total_pct': 0.0, 'eps_connected_pct': 0.0, 'D_rel': 0.0, 'tau': None,
                'n_dof': 0, 'resid': 0.0, 'unconverged': False, 'reason': 'no_void'}
    res = solve_sigma_z(pore.astype(np.int8), np.array([0.0, 1.0]), vox,
                        z_top_um=z_top_um, z_bot_um=0.0, plate_band_um=vox, periodic_xy=periodic_xy)
    d_rel = float(res['sigma_eff'])
    out = {'eps_total_pct': round(100.0 * eps, 2),
           # on early-return paths n_dof counts ALL pore voxels (floating filter never ran) —
           # connected fraction is then UNKNOWN, not "everything" (review m2)
           # ⚠ 2026-08-12 (Codex #2): 이 값은 **either-plate**(한쪽에라도 닿음)이다.  "관통
           #   공극률" 이 아니다 — 그 뜻으로 쓰려면 아래 `eps_through_pct` 를 쓸 것.
           #   이름은 하위호환을 위해 유지하고 규약을 `eps_connected_basis` 에 적는다.
           'eps_connected_pct': (None if res.get('reason')
                                 else round(100.0 * res['n_dof'] / s.size, 2)),
           'eps_connected_basis': 'legacy:either_plate',
           'eps_through_pct': (None if res.get('reason') or res.get('n_through_dof') is None
                               else round(100.0 * res['n_through_dof'] / s.size, 2)),
           'D_rel': float(f'{d_rel:.4g}'),
           'tau': (float(f'{eps / d_rel:.4g}') if d_rel > 1e-12 else None),
           'n_dof': res['n_dof'],
           'n_plate_reachable_dof': res.get('n_plate_reachable_dof'),
           'n_through_dof': res.get('n_through_dof'),
           'resid': res['resid'], 'unconverged': res['unconverged']}
    if res.get('reason'):
        out['reason'] = res['reason']
    return out


def pore_pnm(sid, vox, z_top_um, extra_solid_pts=None, box_lo=(0.0, 0.0, 0.0)):
    """A13 — pore-network TOPOLOGY descriptors (nearest-seed pore-body partition; A6 확장).

    Same crop + PTFE-stamp preamble as pore_tau (conventions inherited), then:
      • EDT(pore) → plateau maxima (3³ max-filter, dist>1 voxel) = pore-body seeds →
        `ndimage.watershed_ift` basin partition (solid = background).
      • per-body: volume → equivalent radius r_eq = (3V/4π)^⅓ [µm].
      • throats: face-adjacent voxel pairs with different body labels → pore-CN (degree),
        n_throats, throat equivalent radius √(A_face/π) (voxel-resolution floor = vox).
      • closed_from_top_pct: pore volume in components NOT reaching the top layer
        (separator side = the open exterior; the bottom is the collector plate = sealed).
        This is the gas/liquid-infiltration closure axis (#286 yoo2026) — DIFFERENT from
        A6 eps_connected (both-plate percolation for the D_eff solve).

    Honest limits: EDT-plateau seeding over-segments long ridges (fine-grained bodies —
    distributions are the robust readout, single n_pores is marker-sensitive); throat area
    is a voxel face count (0.4 µm floor, sub-voxel constriction unresolved — same caveat
    as STEP3 σ).  Thin-pore fallback (no seed with dist>1): connected components become the
    bodies (n_throats=0, flagged).  STRUCTURAL descriptor only — NOT a transport input
    (same audit-#2 non-substitution rule as pore_tau)."""
    if z_top_um is None or float(z_top_um) <= 0.0:
        raise ValueError('pore_pnm requires z_top_um > 0 (same crop rule as pore_tau)')
    s = np.asarray(sid)
    nzc = int(np.floor(float(z_top_um) / vox + 0.5))
    nzc = max(2, min(s.shape[2], nzc))
    s = s[:, :, :nzc].copy()
    if extra_solid_pts is not None and len(extra_solid_pts):
        ijk = np.floor((np.asarray(extra_solid_pts, np.float64) - np.asarray(box_lo, np.float64))
                       / vox).astype(int)
        ok = ((ijk >= 0) & (ijk < np.array(s.shape))).all(1)
        ijk = ijk[ok]
        s[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = 7
    pore = (s == 0)
    if not pore.any():
        return {'reason': 'no_void', 'n_pores': 0}

    # closed-from-top (component level — watershed 무관, 먼저 계산)
    lab_c, _n_c = ndimage.label(pore)                       # 6-conn = face graph
    top_ids = np.unique(lab_c[:, :, nzc - 1])
    top_ids = top_ids[top_ids > 0]
    v_all = float(pore.sum())
    v_open = float(np.isin(lab_c, top_ids).sum()) if len(top_ids) else 0.0
    closed_pct = 100.0 * (1.0 - v_open / max(v_all, 1.0))

    dist = ndimage.distance_transform_edt(pore)
    mx = ndimage.maximum_filter(dist, size=3)
    peaks = pore & (dist >= mx) & (dist > 1.0)              # >1 voxel: 1-voxel skin/line은 seed 아님
    mark, n_seed = ndimage.label(peaks)
    fallback = n_seed == 0
    if fallback:                                            # ultra-thin pore망: 성분=바디로
        lab = lab_c
        n_bodies = int(lab.max())
    else:
        # 최근접-seed 파티션 (SNOW-lite): pore 복셀을 유클리드-최근접 seed에 귀속.
        # ⚠ scipy watershed_ift는 이 용도에 부적합 확인(selftest dumbbell 734/7 오분할 —
        # IFT plateau/큐-순서 quirk) → 결정적 nearest-seed로 교체 (371/370, r_eq 2.23µm 정답).
        # 한계(정직): 직선-거리 metric이라 오목 기공에서 seed-Voronoi 경계가 벽을 가로질러
        # 그릴 수 있음 — throat 집계는 pore-내부 면만 세므로 가짜 인접은 제한적, 분포 판독 권장.
        _, idx = ndimage.distance_transform_edt(mark == 0, return_indices=True)
        lab = np.where(pore, mark[idx[0], idx[1], idx[2]], 0)
        n_bodies = int(len(np.unique(lab)) - (1 if (lab == 0).any() else 0))
    cnt = np.bincount(lab.ravel().astype(np.int64))
    if cnt.size:
        cnt[0] = 0
    ids = np.nonzero(cnt)[0]
    vol_um3 = cnt[ids] * (vox ** 3)
    r_eq = (3.0 * vol_um3 / (4.0 * np.pi)) ** (1.0 / 3.0)

    pairs = {}
    if not fallback:
        W = int(lab.max()) + 1
        for ax in range(3):
            sa = [slice(None)] * 3
            sb = [slice(None)] * 3
            sa[ax] = slice(0, -1)
            sb[ax] = slice(1, None)
            la = lab[tuple(sa)].ravel()
            lb = lab[tuple(sb)].ravel()
            m = (la > 0) & (lb > 0) & (la != lb)
            if m.any():
                lo = np.minimum(la[m], lb[m]).astype(np.int64)
                hi = np.maximum(la[m], lb[m]).astype(np.int64)
                key, c = np.unique(lo * W + hi, return_counts=True)
                for k, cc in zip(key, c):
                    pairs[int(k)] = pairs.get(int(k), 0) + int(cc)
        deg = np.zeros(W, np.int32)
        for k in pairs:
            deg[k // W] += 1
            deg[k % W] += 1
        cn = deg[ids]
    else:
        cn = np.zeros(len(ids), np.int32)
    throat_r = (np.sqrt(np.array(list(pairs.values()), float) * vox * vox / np.pi)
                if pairs else np.array([]))

    def _st(v, f=3):
        return {} if not len(v) else {
            'mean': float(f'{np.mean(v):.{f}g}'), 'med': float(f'{np.median(v):.{f}g}'),
            'p90': float(f'{np.percentile(v, 90):.{f}g}'), 'max': float(f'{np.max(v):.{f}g}')}
    out = {'n_pores': int(n_bodies), 'n_throats': int(len(pairs)),
           'r_eq_um': _st(r_eq), 'pore_cn': _st(cn.astype(float), 3),
           'closed_from_top_pct': round(closed_pct, 2),
           'trust': 'STRUCTURAL PNM (nearest-seed partition, EDT-plateau seed) — 분포가 robust 판독; '
                    'n_pores는 marker-민감, throat=face-count(vox 하한).  수송 폼 대입 금지(A6 동일)'}
    if len(throat_r):
        out['throat_r_eq_um'] = _st(throat_r)
    if fallback:
        out['fallback'] = 'components (no EDT>1 seed — ultra-thin pore)'
    return out


def solve_reaction_current(sid, sig_e_of_sid, sig_i_of_sid, pid, n_am, vox, gct_code,
                           z_top_um=None, z_bot_um=None, periodic_xy=False):
    """STEP4-v1 — 저율·균일-SOC 갈바노스타틱 **반응전류 분포** (랩 slide-20 물리, 선형화 BV).

    같은 복셀 격자 위 TWO networks를 반응 계면에서만 결합한 단일 SPD Kirchhoff 시스템:
      · electronic net (σ_e table: AM+carbon+SDCP) ← 집전체 plate (bottom, φ_e=1 소스)
      · ionic net      (σ_i table: SE+SDCP+SWCNT-sheath-if-transparent) ← 분리막 plate (top, φ_i=0 싱크)
      · BV faces: AM(sid 1,2) ↔ ion-conductor(sid 5,6,8-투명시; σ_i>0 게이트) 인접 면마다 선형화 Butler-Volmer
        컨덕턴스 g_ct = (i0·F/RT)·A_face.  Li는 이 면으로만 두 망을 건넌다 — 반응 면적이
        rasterized 접촉(=coverage)에서 자연히 나온다.
    가정(정직): 저율 선형화(과전압≪RT/F), 균일 SOC(OCV 상수 소거 — linear라 총전류로 스케일),
    충·방전은 부호만 반전.  SDCP는 혼성전도라 두 망 모두에 노드를 갖지만 자기-BV는 없음
    (인터칼레이션 전극이 아님) — 기여는 이온/전자 '배달'로만 (STEP3 서사와 연속).
    Returns dict(i_am[n_am] — 입자별 반응전류(code units, RELATIVE: caller가 정규화),
    I_tot, kcl_err, resid, unconverged, n_dof_e/i, n_bv_faces [, reason])."""
    nx, ny, nz = sid.shape
    sig_e = sig_e_of_sid[sid]
    sig_i = sig_i_of_sid[sid]
    cond_e = sig_e > 0
    cond_i = sig_i > 0
    out0 = {'i_am': np.zeros(n_am), 'I_tot': 0.0, 'kcl_err': 0.0, 'resid': 0.0,
            'unconverged': False, 'n_dof_e': int(cond_e.sum()), 'n_dof_i': int(cond_i.sum()),
            'n_bv_faces': 0}
    if not cond_e.any() or not cond_i.any():
        return {**out0, 'reason': 'missing_network'}
    z_b = float(z_bot_um) if z_bot_um is not None else 0.0
    z_plate = min(float(z_top_um) if z_top_um is not None else nz * vox, nz * vox)
    band = vox + 0.10
    zc = (np.arange(nz) + 0.5) * vox
    any_e = cond_e.any(2)
    k_first_e = np.argmax(cond_e, axis=2)
    bot_e = any_e & (zc[k_first_e] - z_b <= band)            # 집전체 접점 (전자망만)
    any_i = cond_i.any(2)
    k_last_i = nz - 1 - np.argmax(cond_i[:, :, ::-1], axis=2)
    top_i = any_i & (z_plate - zc[k_last_i] <= band)         # 분리막 접점 (이온망만)
    if not bot_e.any() or not top_i.any():
        return {**out0, 'reason': f'no_plate_contact(bot_e={int(bot_e.sum())},top_i={int(top_i.sum())})'}
    # anchored-component filter: 결합 그래프(전자·이온·BV 인접 = 모두 6-이웃 face)를 union 마스크
    # 라벨로 근사 — 어느 plate에도 안 닿는 섬은 전류 0이므로 제거 (특이 블록 방지).  union 인접이
    # 실제 엣지가 아닌 희귀 케이스(SE|carbon 면)는 아래 ε-diag 가드가 받친다.
    uni = cond_e | cond_i
    lab, _nl = ndimage.label(uni)
    _ii, _jj = np.where(bot_e)
    anch = set(lab[_ii, _jj, k_first_e[bot_e]].tolist())
    _ii, _jj = np.where(top_i)
    anch |= set(lab[_ii, _jj, k_last_i[top_i]].tolist())
    anch.discard(0)
    keep = np.isin(lab, list(anch))
    cond_e &= keep
    cond_i &= keep
    n_e = int(cond_e.sum())
    n_i = int(cond_i.sum())
    if n_e == 0 or n_i == 0:
        return {**out0, 'reason': 'all_floating_dropped'}
    idx_e = -np.ones(sid.shape, np.int64); idx_e[cond_e] = np.arange(n_e)
    idx_i = -np.ones(sid.shape, np.int64); idx_i[cond_i] = np.arange(n_i)
    sig_e = np.where(cond_e, sig_e, 0.0)
    sig_i = np.where(cond_i, sig_i, 0.0)
    N = n_e + n_i
    rows, cols, vals = [], [], []
    diag = np.zeros(N, np.float64)
    b = np.zeros(N, np.float64)

    def _net_couple(idxN, sigN, off, sl_a, sl_b):
        A, B = idxN[sl_a], idxN[sl_b]
        sa, sb = sigN[sl_a], sigN[sl_b]
        m = (A >= 0) & (B >= 0)
        if not m.any():
            return
        g = (2.0 * sa[m] * sb[m] / (sa[m] + sb[m])) * vox
        a2, b2 = A[m] + off, B[m] + off
        rows.append(a2); cols.append(b2); vals.append(-g)
        rows.append(b2); cols.append(a2); vals.append(-g)
        np.add.at(diag, a2, g); np.add.at(diag, b2, g)

    # 방향 목록 (전도·BV가 공유 → 주기성 일관 보장).  periodic_xy면 x,y wrap 추가 (z=plate 유지).
    _dirs = [(np.s_[:-1, :, :], np.s_[1:, :, :]), (np.s_[:, :-1, :], np.s_[:, 1:, :]),
             (np.s_[:, :, :-1], np.s_[:, :, 1:])]
    if periodic_xy:                                        # ★RVE 'boundary p p f' 정합 (σ-solve와 동일 규약)
        if sid.shape[0] > 1:
            _dirs.append((np.s_[-1:, :, :], np.s_[:1, :, :]))   # x: nx-1 ↔ 0
        if sid.shape[1] > 1:
            _dirs.append((np.s_[:, -1:, :], np.s_[:, :1, :]))   # y: ny-1 ↔ 0
    for sl_a, sl_b in _dirs:
        _net_couple(idx_e, sig_e, 0, sl_a, sl_b)
        _net_couple(idx_i, sig_i, n_e, sl_a, sl_b)
    # BV 계면 결합 + per-face 기록 (입자별 합산용) — 전도와 동일 _dirs(주기 wrap 포함)로 계면도 일관 주기
    am_m = (sid == 1) | (sid == 2)
    # ★MED-2(감사): 반응 계면 = AM↔이온공급상.  이온상 = SDCP(5)·SE(6)·SWCNT-sheath(8, 투명할 때만).
    #   sid 8 누락 시 σ_ion 솔브(sheath 투명=σ_i[8]>0)와 STEP4 반응(8 제외)이 모순 → wrap_frac↑ AM
    #   표면이 반응서 사라져 STEP4가 --swcnt-ion-block인 것처럼 반응전류 과소.  cond_i(σ_i>0)로 게이트
    #   하여 --swcnt-ion-block(σ_i[8]=0)이면 sid 8 자동 제외 = 솔브와 계면 일관.  기본 bimodal 무영향.
    ion_m = ((sid == 5) | (sid == 6) | (sid == 8)) & cond_i
    bv_e, bv_i, bv_pid = [], [], []
    gct = float(gct_code)
    for sl_a, sl_b in _dirs:
        for am_first in (True, False):
            slA, slB = (sl_a, sl_b) if am_first else (sl_b, sl_a)
            m = am_m[slA] & ion_m[slB]
            Ae = idx_e[slA]; Bi = idx_i[slB]
            m &= (Ae >= 0) & (Bi >= 0)
            if not m.any():
                continue
            a2 = Ae[m]; b2 = Bi[m] + n_e
            g = np.full(len(a2), gct)
            rows.append(a2); cols.append(b2); vals.append(-g)
            rows.append(b2); cols.append(a2); vals.append(-g)
            np.add.at(diag, a2, g); np.add.at(diag, b2, g)
            bv_e.append(a2); bv_i.append(b2); bv_pid.append(pid[slA][m])
    n_bv = int(sum(len(x) for x in bv_e))
    if n_bv == 0:
        return {**out0, 'n_dof_e': n_e, 'n_dof_i': n_i, 'reason': 'no_reaction_interface'}
    # plates: 전자망 bottom(φ=1 소스), 이온망 top(φ=0)
    def _plate(idxN, sigN, off, mask, ksurf, plane, phi_p):
        ii, jj = np.where(mask)
        kk2 = ksurf[mask]
        A = idxN[ii, jj, kk2]
        sa = sigN[ii, jj, kk2]
        m = A >= 0
        dist = np.maximum(np.abs(zc[kk2[m]] - plane), 0.5 * vox)
        g = sa[m] * vox * vox / dist
        np.add.at(diag, A[m] + off, g)
        if phi_p != 0.0:
            np.add.at(b, A[m] + off, g * phi_p)
        return A[m] + off, g
    eb_nodes, eb_g = _plate(idx_e, sig_e, 0, bot_e, k_first_e, z_b, 1.0)
    _plate(idx_i, sig_i, n_e, top_i, k_last_i, z_plate, 0.0)
    # degree-0 노드(엣지 전무)만 ε-고정.  union-라벨이 false-adjacency로 남길 수 있는 "고립
    # 서브그래프"(예: SE에 싸인 carbon 섬)는 특이 블록이지만 b=0 + CG(x0=0)에서 φ≡0으로 정확히
    # 유지된다(구조적 블록대각 + Krylov가 0-블록을 못 건드림) — 리뷰 프로브로 ΔI ~1e-15 확인.
    # ⚠ 이 안전성은 CG+x0=0 전제: 직접분해(spsolve)나 블록혼합 preconditioner로 바꾸면
    # 컴포넌트-그래프 anchoring(BV 엣지 기반 union-find)으로 교체할 것.
    diag[diag == 0.0] = 1.0
    L = sparse.coo_matrix((np.concatenate(vals + [diag]),
                           (np.concatenate(rows + [np.arange(N)]),
                            np.concatenate(cols + [np.arange(N)]))), shape=(N, N)).tocsr()
    print(f'    STEP4 rxn solve: e {n_e:,} + i {n_i:,} dof, BV faces {n_bv:,} — CG '
          f'({"GPU" if GPU_SOLVE else "CPU"})…', flush=True)
    phi, info = _solve_cg(L, b)
    resid = float(np.linalg.norm(L @ phi - b) / max(np.linalg.norm(b), 1e-30))
    unconv = bool(info) or resid > 1e-6
    I_tot = float(np.sum(eb_g * (1.0 - phi[eb_nodes])))
    i_am = np.zeros(n_am, np.float64)
    I_bv = 0.0
    for a2, b2, pd in zip(bv_e, bv_i, bv_pid):
        f = gct * (phi[a2] - phi[b2])                        # +: e-net → i-net (한 방향, linear)
        I_bv += float(f.sum())
        mm2 = pd >= 0
        np.add.at(i_am, pd[mm2], f[mm2])
    kcl = abs(I_tot - I_bv) / max(abs(I_tot), 1e-30)         # KCL: plate 유입 = BV 총 통과
    return {'i_am': i_am, 'I_tot': I_tot, 'kcl_err': float(kcl), 'resid': resid,
            'unconverged': unconv, 'n_dof_e': n_e, 'n_dof_i': n_i, 'n_bv_faces': n_bv}


def _selftest_rxn():
    """STEP4 sandwich analytic: 하반 AM slab / 상반 SE slab, 계면 BV — 직렬저항 I와 균일 i_n."""
    vox = 0.5
    nxy, nz = 6, 12
    sid = np.zeros((nxy, nxy, nz), np.int8)
    sid[:, :, :6] = 1                                        # AM (전자망)
    sid[:, :, 6:] = 6                                        # SE (이온망)
    pid = np.full(sid.shape, -1, np.int32)
    pid[:, :, :6] = 0                                        # 입자 1개로 합산
    sig_e = np.array([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    sig_i = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0])
    gct = 0.05                                               # 면당 (code units)
    r = solve_reaction_current(sid, sig_e, sig_i, pid, 1, vox, gct,
                               z_top_um=nz * vox, z_bot_um=0.0)
    # 직렬 해석해 (µm-code 단위 일관, 코드 규약대로 직접 합산):
    #   per-column R = 1/g_plate,e + 5/(σe·vox) + 1/g_ct + 5/(σi·vox) + 1/g_plate,i
    ge_plate = 1.0 * vox * vox / (0.5 * vox)
    gi_plate = 2.0 * vox * vox / (0.5 * vox)
    R_col = 1.0 / ge_plate + 5 * (1.0 / (1.0 * vox)) + 1.0 / gct + 5 * (1.0 / (2.0 * vox)) + 1.0 / gi_plate
    I_exp = nxy * nxy / R_col
    okI = abs(r['I_tot'] - I_exp) / I_exp < 1e-3
    okK = r['kcl_err'] < 1e-6
    okU = abs(r['i_am'][0] - r['I_tot']) / r['I_tot'] < 1e-6   # 입자 1개 = 총전류 (CG rtol 1e-8 여유)
    print(f"rxn sandwich: I={r['I_tot']:.6f} (expect {I_exp:.6f})  {'OK' if okI else 'FAIL'}")
    print(f"rxn KCL: plate vs ΣBV err={r['kcl_err']:.2e}  {'OK' if okK else 'FAIL'}")
    print(f"rxn per-particle sum == I_tot  {'OK' if okU else 'FAIL'}")
    # 방향 대칭 — 좌/우 미러 배치가 같은 I·face 수 (am_first 양쪽 분기 고정; 물리 리뷰 프로브 영구화)
    sidL = np.zeros((6, 6, 12), np.int8); sidL[:3] = 1; sidL[3:] = 6
    sidR = np.zeros((6, 6, 12), np.int8); sidR[3:] = 1; sidR[:3] = 6
    pidL = np.where(sidL == 1, 0, -1).astype(np.int32)
    pidR = np.where(sidR == 1, 0, -1).astype(np.int32)
    rL = solve_reaction_current(sidL, sig_e, sig_i, pidL, 1, vox, gct, z_top_um=nz * vox, z_bot_um=0.0)
    rR = solve_reaction_current(sidR, sig_e, sig_i, pidR, 1, vox, gct, z_top_um=nz * vox, z_bot_um=0.0)
    okM = (rL['n_bv_faces'] == rR['n_bv_faces']
           and abs(rL['I_tot'] - rR['I_tot']) / max(abs(rL['I_tot']), 1e-30) < 1e-6)
    print(f"rxn mirror(lateral BV): I_L={rL['I_tot']:.6f} I_R={rR['I_tot']:.6f} "
          f"faces {rL['n_bv_faces']}/{rR['n_bv_faces']}  {'OK' if okM else 'FAIL'}")
    ok = okI and okK and okU and okM
    print('RXN SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest():
    """Analytic checks that pin assembly + BC signs."""
    ok = True
    sig_tab = np.array([0.0, 1.0, 4.0])
    # 1) uniform block σ=1 → σ_eff = 1
    sid = np.ones((6, 6, 10), np.int8)
    r = solve_sigma_z(sid, sig_tab, 0.5)
    ok &= abs(r['sigma_eff'] - 1.0) < 1e-6
    print(f"uniform:  σ_eff={r['sigma_eff']:.6f}  (expect 1.0)  {'OK' if ok else 'FAIL'}")
    # 2) series laminate (z-stacked σ=1 / σ=4, half-half) → harmonic mean 1.6
    sid = np.ones((6, 6, 10), np.int8); sid[:, :, 5:] = 2
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = abs(r['sigma_eff'] - 1.6) < 1e-3
    ok &= e; print(f"series:   σ_eff={r['sigma_eff']:.6f}  (expect 1.6 harmonic)  {'OK' if e else 'FAIL'}")
    # 3) parallel laminate (x-split) → arithmetic mean 2.5
    sid = np.ones((6, 6, 10), np.int8); sid[3:, :, :] = 2
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = abs(r['sigma_eff'] - 2.5) < 1e-3
    ok &= e; print(f"parallel: σ_eff={r['sigma_eff']:.6f}  (expect 2.5 arithmetic)  {'OK' if e else 'FAIL'}")
    # 4) disconnected (air gap layer) → σ_eff = 0
    sid = np.ones((6, 6, 10), np.int8); sid[:, :, 5] = 0
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = r['sigma_eff'] < 1e-12
    ok &= e; print(f"gap:      σ_eff={r['sigma_eff']:.2e}  (expect 0)  {'OK' if e else 'FAIL'}")
    # 5) thin conductive column (1/36 of area) → σ_eff = 1/36 of column σ
    sid = np.zeros((6, 6, 10), np.int8); sid[0, 0, :] = 1
    r = solve_sigma_z(sid, sig_tab, 0.5)
    e = abs(r['sigma_eff'] - 1.0 / 36.0) < 1e-6
    ok &= e; print(f"column:   σ_eff={r['sigma_eff']:.6f}  (expect {1/36:.6f})  {'OK' if e else 'FAIL'}")
    # 6) SR-03 AMG — 기본 OFF 이고, 켜도 **같은 σ** 를 내며, 실제로 쓴 전처리가 도장된다.
    #    고대비(σ 1 : 1e4) 격자로 — 전처리가 갈릴 여지가 있는 조건에서 봐야 뜻이 있다.
    global AMG_SOLVE
    hi = np.array([0.0, 1.0, 1.0e4])
    sid = np.ones((8, 8, 12), np.int8); sid[2:6, 2:6, :] = 2       # 고대비 관통 채널
    e = (AMG_SOLVE is False)
    ok &= e; print(f"amg-off:  기본 AMG_SOLVE={AMG_SOLVE}  (expect False = 현행 경로)  "
                   f"{'OK' if e else 'FAIL'}")
    sj = solve_sigma_z(sid, hi, 0.5)['sigma_eff']; pj = LAST_BACKEND['precond']
    AMG_SOLVE = True
    try:
        sa = solve_sigma_z(sid, hi, 0.5)['sigma_eff']; pa = LAST_BACKEND['precond']
    finally:
        AMG_SOLVE = False
    d = abs(sa - sj) / max(sj, 1e-30)
    #   pyamg 부재 환경에서는 폴백해 precond='jacobi' 가 되고 σ 는 당연히 같다 — 그때도 통과.
    e = d < 1e-6 and pj == 'jacobi' and pa in ('amg', 'jacobi')
    ok &= e; print(f"amg-inv:  σ_eff {sj:.8g} → {sa:.8g}  Δ={d:.1e}  precond {pj}→{pa}  "
                   f"(expect Δ<1e-6, 해-불변)  {'OK' if e else 'FAIL'}")
    print('SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_pore():
    """A6 pore-τ analytic checks — crop, PTFE stamping, TauFactor convention."""
    ok = True
    # 1) all-void box → ε=100%, D_rel=1, τ=1 exactly
    sid = np.zeros((6, 6, 10), np.int8)
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = abs(r['tau'] - 1.0) < 1e-6 and abs(r['eps_total_pct'] - 100.0) < 1e-9
    ok &= e; print(f"all-void: τ={r['tau']}  ε={r['eps_total_pct']}%  (expect 1, 100)  {'OK' if e else 'FAIL'}")
    # 2) straight 2×2 channel through solid → D_rel = area share EXACT (plate half-cell convention),
    #    τ = 1 exactly (straight pore has no tortuosity)
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = abs(r['tau'] - 1.0) < 1e-6 and abs(r['D_rel'] - 4.0 / 36.0) < 5e-4   # D_rel ships %.4g-rounded
    ok &= e; print(f"channel:  τ={r['tau']}  D_rel={r['D_rel']:.4f}  (expect 1, {4/36:.4f})  {'OK' if e else 'FAIL'}")
    # 3) void padding cap ABOVE the bed (raster box taller than the pressed thickness) — uncropped,
    #    every column's topmost pore voxel floats in the cap and the top plate decouples; the crop
    #    must restore the exact channel answer
    sid = np.ones((6, 6, 14), np.int8); sid[2:4, 2:4, :] = 0; sid[:, :, 10:] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = abs(r['tau'] - 1.0) < 1e-6
    ok &= e; print(f"crop:     τ={r['tau']}  (expect 1 — padding cap cropped)  {'OK' if e else 'FAIL'}")
    # 4) extra_solid_pts stamping (the PTFE path): plug the channel with 4 stamped points → the pore
    #    no longer percolates → D_rel ~ 0, τ = None
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0
    plug = np.array([[1.25, 1.25, 2.25], [1.75, 1.25, 2.25], [1.25, 1.75, 2.25], [1.75, 1.75, 2.25]])
    r = pore_tau(sid, 0.5, z_top_um=5.0, extra_solid_pts=plug)
    e = (r['tau'] is None) and r['D_rel'] < 1e-9
    ok &= e; print(f"stamp:    τ={r['tau']}  D_rel={r['D_rel']:.1e}  (expect None, ~0 — plugged)  {'OK' if e else 'FAIL'}")
    # 5) isolated-pore honesty: a sealed 2-voxel pocket raises ε_total but not ε_connected;
    #    τ uses ε_total (TauFactor) → closed porosity reads as τ > 1
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0; sid[0, 0, 4:6] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = r['eps_total_pct'] > r['eps_connected_pct'] and r['tau'] is not None and r['tau'] > 1.0
    ok &= e; print(f"isolated: ε_tot={r['eps_total_pct']}% > ε_conn={r['eps_connected_pct']}%  τ={r['tau']}"
                   f"  (expect τ>1: closed porosity penalised)  {'OK' if e else 'FAIL'}")
    # 6) review M1 — 1-voxel solid ROOF must SEAL the channel even when frac(z_top/vox) puts the
    #    roofed pore centre inside the e-solve's default band (vox+0.1): vox=0.4, z_top=2.68
    #    (frac 0.7) → roofed pore dist 0.48 < 0.5 leaked with the old band; band=vox seals it
    sid = np.ones((6, 6, 8), np.int8); sid[2:4, 2:4, 0:6] = 0    # channel k=0..5, solid roof k=6
    r = pore_tau(sid, 0.4, z_top_um=2.68)
    e = r['tau'] is None and r['D_rel'] < 1e-9 and bool(r.get('reason'))
    ok &= e; print(f"roof:     τ={r['tau']}  D_rel={r['D_rel']:.1e}  reason={r.get('reason')}"
                   f"  (expect sealed — old band read τ<1 through the roof)  {'OK' if e else 'FAIL'}")
    # 7) ★ Codex #2 — `eps_connected_pct` 는 either-plate 다.  **한쪽 플레이트에만 닿는 막다른
    #    공극**(dead-end)을 넣으면 두 계수가 갈려야 한다.  갈리지 않으면 이 시험은 가능도비 1
    #    이고 결함을 영원히 통과시킨다 → 여기서 **차이를 강제로 요구**한다.
    sid = np.ones((6, 6, 10), np.int8)
    sid[2:4, 2:4, :] = 0                                    # 관통 채널 (양 플레이트)
    sid[0, 0, 0:5] = 0                                      # 바닥에만 닿는 막다른 공극
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = (r['n_through_dof'] is not None
         and r['n_plate_reachable_dof'] == r['n_dof']
         and r['n_through_dof'] < r['n_plate_reachable_dof']      # ★ 판별력: 갈려야 한다
         and r['n_plate_reachable_dof'] - r['n_through_dof'] == 5  # 막다른 5 복셀 정확히
         and r['eps_through_pct'] < r['eps_connected_pct']
         and r['eps_connected_basis'] == 'legacy:either_plate')
    ok &= e; print(f"deadend:  reachable={r['n_plate_reachable_dof']} through={r['n_through_dof']} "
                   f"(expect Δ=5: 바닥만 닿는 공극) ε_conn={r['eps_connected_pct']}% > "
                   f"ε_through={r['eps_through_pct']}%  {'OK' if e else 'FAIL'}")
    # 8) 관통만 있으면 둘이 같아야 한다 (위 시험이 항상 갈리는 것은 아님을 보이는 대조군)
    sid = np.ones((6, 6, 10), np.int8); sid[2:4, 2:4, :] = 0
    r = pore_tau(sid, 0.5, z_top_um=5.0)
    e = r['n_through_dof'] == r['n_plate_reachable_dof'] and \
        r['eps_through_pct'] == r['eps_connected_pct']
    ok &= e; print(f"control:  reachable={r['n_plate_reachable_dof']} == through={r['n_through_dof']}"
                   f"  (막다른 공극 없으면 동일)  {'OK' if e else 'FAIL'}")
    print('PORE SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_segstamp():
    """SR-01 opt-in 선분 스탬프 — 기본 경로 불변 + 연결 보장 + AM 관통 방지."""
    from fibre_segment_raster import n_components_6face
    ok = fail = 0

    def chk(m, c):
        nonlocal ok, fail
        print(('  PASS  ' if c else '  FAIL  ') + m)
        ok, fail = ok + (1 if c else 0), fail + (0 if c else 1)

    vox = 0.4
    lo, hi = np.zeros(3), np.array([20.0, 20.0, 20.0])
    rng = np.random.default_rng(3)
    step = 0.7 * 0.141                       # production 점 간격 규약
    pts, fid, ph = [], [], []
    for k in range(3):
        d = rng.normal(size=3); d /= np.linalg.norm(d)
        P = rng.uniform(4, 14, 3) + np.arange(int(10 / step))[:, None] * step * d
        pts.append(P); fid += [k] * len(P); ph += [2] * len(P)     # phase 2 = VGCF
    pts = np.vstack(pts); fid = np.array(fid); ph = np.array(ph)
    z3 = (np.zeros((0, 3)), np.zeros(0), np.zeros(0, int))

    sid_pt, _ = rasterize(*z3, pts, ph, lo, hi, vox)
    sid_sg, _ = rasterize(*z3, pts, ph, lo, hi, vox, add_fid=fid)
    cpt = np.argwhere(sid_pt == 3); csg = np.argwhere(sid_sg == 3)
    chk(f'1) ★ 결함 재현: 점-스탬프 성분 {n_components_6face(cpt)} > 섬유 3개',
        n_components_6face(cpt) > 3)
    chk(f'2) ★ add_fid → 선분: 성분 {n_components_6face(csg)} = 섬유 3',
        n_components_6face(csg) == 3)
    chk(f'3) 셀 증가 {len(csg) / max(len(cpt), 1):.2f}배 < 1.6', len(csg) / max(len(cpt), 1) < 1.6)
    sid_b, _ = rasterize(*z3, pts, ph, lo, hi, vox, add_fid=None)
    chk('4) ★ add_fid=None 은 기존과 bitwise 동일 (opt-in 이 기본을 안 건드린다)',
        np.array_equal(sid_pt, sid_b))
    # AM 드랍으로 생긴 큰 간격은 **끊어야** 한다 (안 그러면 폴리라인이 AM 을 관통)
    A = np.arange(0, 4, step)[:, None] * np.array([1, 0.3, 0.2])
    P2 = np.vstack([A + np.array([2, 2, 2]), A + np.array([9, 4, 3.4])])
    sid_g, _ = rasterize(*z3, P2, np.full(len(P2), 2), lo, hi, vox,
                         add_fid=np.zeros(len(P2), int))
    chk(f'5) ★ 큰 간격은 끊어 굽는다 (성분 {n_components_6face(np.argwhere(sid_g == 3))} = 2)',
        n_components_6face(np.argwhere(sid_g == 3)) == 2)
    # σ 로 읽었을 때의 크기 — 점 스탬프가 퍼콜을 잃는다
    sg = np.zeros(9); sg[3] = 100.0
    ra = solve_sigma_z(sid_pt, sg, vox); rb = solve_sigma_z(sid_sg, sg, vox)
    chk(f"6) ★ σ_z 점={ra['sigma_eff']:.4g} < 선분={rb['sigma_eff']:.4g} "
        f"(floating 버림 {ra['n_floating_dropped']} → {rb['n_floating_dropped']})",
        rb['sigma_eff'] > ra['sigma_eff'])
    # ★ 배선 확인 — 구현만 하고 payload 가 안 넘기면 무의미하다 (이 리포의 반복 교훈)
    import os as _os
    _pp = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'mpm_webapp_payload.py')
    try:
        _src = open(_pp, encoding='utf-8').read()
        chk('7) ★ payload 가 rasterize 에 add_fid 를 넘긴다 (배선)',
            'add_fid=_afid' in _src)
        chk('8) ★ payload CLI 에 --step3-fibre-stamp 가 있고 기본이 point 다',
            "'--step3-fibre-stamp'" in _src and "default='point'" in _src)
        chk('9) ★ manifest 에 fibre_stamp 가 기록된다 (어느 방식으로 돌았는지 추적)',
            "'fibre_stamp': a.step3_fibre_stamp" in _src
            and "'fibre_stamp_applied'" in _src)
    except OSError as _e:
        chk(f'7-9) ⚠ payload 배선 확인 생략 ({_e})', True)

    # ── ★★ 회귀 10-12: **경로가 아닌 fid** (coat id = AM 구 index) ──────────────────────
    #   적대리뷰(코드 렌즈, 2026-08-12)가 재현: `additives.seed_coat(return_ids=True)` 는
    #   **AM 구 index** 를 fid 로 준다 (SDCP thinky·SuperP thinky).  한 구 표면에 흩어진
    #   수십 점이 같은 fid 를 공유하므로 폴리라인으로 이으면 구 표면을 헤집는 선분이 되고,
    #   실측 셀 45 → 582 (×12.9), 그중 87 % 가 **AM 구 내부**.  gap_tol 은 간격이 균일해
    #   **발화하지 않는다**(파단 0 건).  → POLYLINE_PHASES 화이트리스트로 막는다.
    rng = np.random.default_rng(0)
    u = rng.normal(size=(47, 3)); u /= np.linalg.norm(u, axis=1)[:, None]
    coat = np.array([10.0, 10.0, 10.0]) + 3.0 * u             # 구 표면 산포 47점, 1 fid
    lo3 = np.array([0.0, 0.0, 0.0]); n3 = np.array([64, 64, 64])
    fid1 = np.zeros(len(coat), np.int32)
    for ph_code, name, is_poly in ((5, 'SDCP', False), (3, 'SuperP', False), (2, 'VGCF', True)):
        ijk_s, _ = _fibre_segment_ijk(coat, np.full(len(coat), ph_code, np.int8), fid1,
                                      lo3, 0.4, n3)
        n_pt = len(np.unique(np.floor((coat - lo3) / 0.4).astype(int), axis=0))
        ratio = len(np.unique(ijk_s, axis=0)) / max(n_pt, 1)
        if not is_poly:
            chk(f'10-{ph_code}) ★ {name}(coat id)는 경로가 아니다 → 점 스탬프 유지 '
                f'(셀 비 {ratio:.2f}× ≤ 1.0)', ratio <= 1.0 + 1e-9)
        else:
            chk(f'10-{ph_code}) 대조: {name}는 폴리라인이라 선분이 걸린다 (셀 비 {ratio:.1f}×)',
                ratio > 1.6)
    # 화이트리스트가 뷰어 가드와 **같은 소스**인가 (두 번째 구현이 이 결함의 원인이었다)
    try:
        _src2 = open(_pp, encoding='utf-8').read()
        chk('11) ★ payload 뷰어 폴리라인 마스크가 step3 의 POLYLINE_PHASES 를 쓴다 (단일 소스)',
            'POLYLINE_PHASES' in _src2)
    except OSError:
        pass
    chk('12) POLYLINE_PHASES = (2,4,6) — VGCF·PTFE·SWCNT 만 경로',
        tuple(POLYLINE_PHASES) == (2, 4, 6))

    # ── ② fid 의미 계약: 시더 선언이 phase 추측을 **이긴다** (Codex E-01) ────────────────
    #   SuperP(phase 3) 는 mixing 에 따라 경로(ballmill)도 그룹(thinky)도 된다 — phase 로는
    #   원리적으로 못 가른다.
    import additives as _adt
    chk('13) SuperP ballmill = 경로 (체인)', _adt.id_kind_of('cblack') == _adt.ID_PATH)
    chk('14) ★ SuperP thinky = 그룹 — 같은 phase 인데 반대라 phase 로는 못 가른다',
        _adt.id_kind_of('cblack', 'coat_block') == _adt.ID_GROUP)
    chk('15) 미등록 시더는 안전측(GROUP)', _adt.id_kind_of('nope') == _adt.ID_GROUP)
    #   ★ **대각선**이어야 점 스탬프가 끊긴다 (축정렬 선은 점으로도 face 를 공유한다 —
    #     이것이 리포 selftest 가 4개월간 이 결함을 통과시킨 이유이기도 하다).
    _s0 = np.array([2.0, 2.0, 2.0]); _d1 = np.array([6.0, 6.0, 6.0])
    _ln = _s0 + np.linspace(0, 1, 40)[:, None] * _d1[None, :]
    _f0 = np.zeros(len(_ln), np.int32); _n3 = np.array([64, 64, 64]); _lo3 = np.zeros(3)
    _ph3 = np.full(len(_ln), 3, np.int8)
    _ijp, _ = _fibre_segment_ijk(_ln, _ph3, _f0, _lo3, 0.4, _n3,
                                 add_kind=np.full(len(_ln), _adt.ID_PATH, np.int8))
    _ijg, _ = _fibre_segment_ijk(_ln, _ph3, _f0, _lo3, 0.4, _n3,
                                 add_kind=np.full(len(_ln), _adt.ID_GROUP, np.int8))
    chk('16) ★ 같은 phase·같은 점열이라도 kind=PATH 는 잇고 GROUP 은 안 잇는다',
        n_components_6face(np.unique(_ijp, axis=0)) == 1
        and n_components_6face(np.unique(_ijg, axis=0)) > 1)
    _ijf, _ = _fibre_segment_ijk(_ln, _ph3, _f0, _lo3, 0.4, _n3)
    chk('17) kind 없으면 phase 폴백 (3 ∉ POLYLINE_PHASES → 점) = 옛 산출물 호환',
        np.array_equal(np.unique(_ijf, axis=0), np.unique(_ijg, axis=0)))

    # ── ③ segment_cells 음방향 + **정확한 복셀 경계** 끝점 (Codex E-06) ─────────────────
    #   기존 음방향 사례는 끝점이 경계에 정확히 놓이지 않아 이 경로를 안 탔다.
    from fibre_segment_raster import segment_cells as _sc
    for _nm, _p0, _p1 in (('음방향-경계끝', np.array([2.0, .2, .2]), np.array([0.8, .2, .2])),
                          ('양방향-경계끝', np.array([0.8, .2, .2]), np.array([2.0, .2, .2])),
                          ('음방향-경계시작', np.array([1.6, .2, .2]), np.array([0.5, .2, .2]))):
        _cc = np.unique(_sc(_p0, _p1, 0.4), axis=0)
        _sp = int(abs(np.floor(_p1[0] / 0.4) - np.floor(_p0[0] / 0.4))) + 1
        chk(f'18-{_nm}) 1성분 · 셀 {len(_cc)} = 기대 {_sp} (여분/backtrack 없음)',
            n_components_6face(_cc) == 1 and len(_cc) == _sp)

    # ── ④ point legacy parity — 계약 도입이 점 경로를 안 건드린다 ─────────────────────
    _amc = np.array([[5.0, 5.0, 5.0]]); _amr = np.array([1.5]); _amt = np.array([1])
    _hi3 = _lo3 + 64 * 0.4
    _sa, _ = rasterize(_amc, _amr, _amt, _ln, np.full(len(_ln), 2, np.int8), _lo3, _hi3, 0.4)
    _sb, _ = rasterize(_amc, _amr, _amt, _ln, np.full(len(_ln), 2, np.int8), _lo3, _hi3, 0.4,
                       add_kind=np.full(len(_ln), _adt.ID_PATH, np.int8))
    chk('19) ★ add_fid 없이는 add_kind 를 줘도 점 경로 bitwise 동일 (legacy parity)',
        np.array_equal(_sa, _sb))

    print(f'\nstep3 segment-stamp selftest: {ok}/{ok + fail} PASS')
    return 0 if not fail else 1


def _selftest_swcnt():
    """A14 — phase-6(SWCNT sheath) rasterize 스탬프 + 전자-도체/이온-투명 배선 검증.
    리뷰 CRITICAL 재발 방지: phase→sid 맵 누락 시 점이 무음 drop되어 σ_e 효과가 0이 되는 버그."""
    ok = True
    am_c = np.array([[5.0, 5.0, 5.0]]); am_r = np.array([2.0]); am_t = np.array([1])
    pts = np.array([[5.0, 5.0, 7.3], [1.0, 1.0, 1.0]])       # sheath skin점 + 원거리 VGCF 대조점
    ph = np.array([6, 2], np.int8)
    se = np.array([[8.0, 8.0, 8.0]])
    sid, _ = rasterize(am_c, am_r, am_t, pts, ph, (0, 0, 0), (10.0, 10.0, 10.0), 0.4, se_pts=se)
    v6 = sid[int(5.0 / .4), int(5.0 / .4), int(7.3 / .4)]
    v2 = sid[int(1.0 / .4), int(1.0 / .4), int(1.0 / .4)]
    e = (v6 == 8) and (v2 == 3)
    ok &= e; print(f'stamp:     phase6→sid {v6} (expect 8), phase2→sid {v2} (expect 3)  {"OK" if e else "FAIL"}')
    # 전자 테이블: idx8 도체 / 이온 테이블: 기본 SE-투명(σ>0) vs 차단(0) — payload 테이블 모양 재현
    sig_e = np.array([0, .01, .005, 100, 10, 250, 0, 0, 100.0])
    sig_i_t = np.array([0, 0, 0, 0, 0, .0006, .003, 0, .003])
    sig_i_b = np.array([0, 0, 0, 0, 0, .0006, .003, 0, 0.0])
    e = sig_e[v6] > 0 and sig_i_t[v6] > 0 and sig_i_b[v6] == 0.0
    ok &= e; print(f'tables:    σ_e[8]={sig_e[8]} σ_i_transparent[8]={sig_i_t[8]} σ_i_blockUB[8]={sig_i_b[8]}  '
                   f'{"OK" if e else "FAIL"}')
    # SID_NAME 완결성 (phase_current_share KeyError 방지)
    e = SID_NAME.get(8) == 'SWCNT'
    ok &= e; print(f'sid-name:  SID_NAME[8]={SID_NAME.get(8)}  {"OK" if e else "FAIL"}')
    print('SWCNT-STAMP SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_pnm():
    """A13 pore-PNM analytic checks — dumbbell 2-body/1-throat, sealed closure, thin fallback."""
    ok = True
    # 1) dumbbell: 두 구형 기공(r=4.4vox) + 1-voxel 목(neck) — 밀봉 박스 → n_pores=2, n_throats=1,
    #    CN mean=1, closed_from_top=100%
    n = (40, 20, 20)
    sid = np.ones(n, np.int8)
    zz = np.indices(n).astype(float)
    for cx in (10.0, 30.0):
        m = ((zz[0] - cx) ** 2 + (zz[1] - 10.0) ** 2 + (zz[2] - 10.0) ** 2) <= 4.4 ** 2
        sid[m] = 0
    sid[10:31, 10, 10] = 0                                   # 1-voxel neck (dist=1 → seed 아님)
    r = pore_pnm(sid, 0.5, z_top_um=10.0)
    e = (r['n_pores'] == 2 and r['n_throats'] == 1
         and abs(r['pore_cn']['mean'] - 1.0) < 1e-9 and r['closed_from_top_pct'] == 100.0)
    ok &= e
    print(f"dumbbell: n_pores={r['n_pores']} throats={r['n_throats']} CN={r['pore_cn'].get('mean')} "
          f"closed={r['closed_from_top_pct']}%  (expect 2/1/1.0/100)  {'OK' if e else 'FAIL'}")
    # r_eq sanity: 구 r=4.4vox=2.2µm에 목 절반씩 → 등가반경 ≈2.2µm ±20%
    e = abs(r['r_eq_um']['med'] - 2.2) / 2.2 < 0.2
    ok &= e
    print(f"r_eq:     med={r['r_eq_um']['med']}µm  (expect ≈2.2 ±20%)  {'OK' if e else 'FAIL'}")
    # 2) 위-열린 직선 채널 (2×2, 전체 관통) — ultra-thin → fallback=components, closed 0%
    sid = np.ones((6, 6, 10), np.int8)
    sid[2:4, 2:4, :] = 0
    r = pore_pnm(sid, 0.5, z_top_um=5.0)
    e = r['n_pores'] == 1 and r['closed_from_top_pct'] == 0.0 and 'fallback' in r
    ok &= e
    print(f"channel:  n_pores={r['n_pores']} closed={r['closed_from_top_pct']}% fallback={'Y' if 'fallback' in r else 'N'}"
          f"  (expect 1/0/Y)  {'OK' if e else 'FAIL'}")
    # 3) 열린 채널 + 밀봉 구 공존 → closed% = 구 부피 몫 (0<closed<100)
    sid = np.ones((20, 20, 12), np.int8)
    sid[2:4, 2:4, :] = 0
    m = ((zz[0][:20, :20, :12] - 12.0) ** 2 + (zz[1][:20, :20, :12] - 12.0) ** 2
         + (zz[2][:20, :20, :12] - 5.0) ** 2) <= 3.4 ** 2
    sid[m] = 0
    r = pore_pnm(sid, 0.5, z_top_um=6.0)
    e = 0.0 < r['closed_from_top_pct'] < 100.0
    ok &= e
    print(f"mixed:    closed={r['closed_from_top_pct']}%  (expect 0<x<100)  {'OK' if e else 'FAIL'}")
    # 4) no void → reason
    r = pore_pnm(np.ones((4, 4, 6), np.int8), 0.5, z_top_um=3.0)
    e = r.get('reason') == 'no_void'
    ok &= e
    print(f"no-void:  reason={r.get('reason')}  {'OK' if e else 'FAIL'}")
    print('PNM SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


# ── Track-B (COMSOL 하이브리드) 파라미터 헬퍼 ───────────────────────────────────────────
#    설계: AM 구 = 해상 기하 / SE = 연속체 / VGCF = 1D Edge / AM-AM 넥 = DEM δ (소성 미미).
#    아래 셋은 payload → comsol_pkg 익스포트의 순수 계산 조각이다.

def tau_from_solve(phi_cond, sigma_bulk, sigma_eff):
    """복셀 Laplace 해 → 굴곡도.  **선형 관례** σ_eff = σ_bulk·φ/τ ⇒ τ = φ·σ_bulk/σ_eff.

    ⚠ 관례 지뢰: build_tau_regime_db._tau_from_sigma 는 √(φ·σ/σ_eff) = **τ² 관례**다.
    같은 구조가 선형 τ=4 ↔ √ 관례 2 로 두 배 다르게 읽힌다.  COMSOL 의 tortuosity 입력은
    통상 선형(σ_eff = σ·ε/τ) → Track-B export 는 전부 이 함수로 통일하고 관례를 함께 적는다.
    """
    if not (phi_cond and sigma_bulk and sigma_eff) or min(phi_cond, sigma_bulk, sigma_eff) <= 0:
        return None
    return float(phi_cond) * float(sigma_bulk) / float(sigma_eff)


def kdom_calibration(phi_full, tau_full, phi_geo, tau_geo):
    """Track-B SE 연속체의 국소 전도도 배율 κ_dom/σ_bulk — ★ 이중계상 가드.

    하이브리드 COMSOL 은 AM 구를 **기하로 해상**하므로 AM-장애물 굴곡도는 모델이 스스로
    만든다.  측정 τ_full(전체 미세구조)을 그대로 SE 도메인 σ 에 먹이면 AM 몫이 **두 번**
    걸린다.  모델이 측정 σ_eff 를 재현할 조건:
        κ_dom·(φ_geo/τ_geo) = σ_bulk·(φ_full/τ_full)
        ⇒ κ_dom/σ_bulk = (φ_full/τ_full) / (φ_geo/τ_geo)
    φ_geo/τ_geo = "AM 여집합을 꽉 찬 SE 로 이상화" 한 같은 복셀 Laplace 해(한 번 더 푼 값).
    반환은 대체로 (0,1]: 1 = AM 기하가 굴곡을 전부 설명(SE 내부 몫 0), 작을수록 SE
    내부(넥·공극·입계) 몫이 크다.  >1 이면 규약/입력 불일치 신호이므로 호출부가 경고할 것.
    ⚠ 한계 (심화리뷰 2026-08-05): 이 배율은 z-관통 유효전도 **스칼라 하나**로만 맞춘다 —
    일축 압밀 미세구조의 in-plane↔z 이방성, 구 주변 국소 spreading, graded-z 불균질은
    검증 밖.  B1(총량 σ) 성립 / B2(BV 국소 분포)는 균질화 오차 상속 → B2 전 τ_x/τ_y
    병기 솔브로 이방성 정량 (TODO(trackb)).  복셀 계단 편향(+13~16% @vox0.4)은
    소비자 측 geo-probe 2-런 재규격으로 소거 (comsol_pkg conventions §7).
    """
    if None in (phi_full, tau_full, phi_geo, tau_geo):
        return None
    if min(phi_full, tau_full, phi_geo, tau_geo) <= 0:
        return None
    return (float(phi_full) / float(tau_full)) / (float(phi_geo) / float(tau_geo))


def am_surface_patches(sid, pid, n_am, reaction_sids=(5, 6), carbon_sids=(3, 4, 8),
                       block_sids=(7,)):
    """AM 표면 face walk — 입자별 이웃-상 분류 (Track-B per-particle coverage 벡터).

    표면 face = AM 복셀(sid 1·2)과 비-AM 복셀이 맞닿는 격자면.  face 단위로 이웃 상을 세어
    입자별 f_cov = 반응상 face / 전체 face 를 만든다.  기본 반응상 = SE(6)+SDCP(5) —
    step4 의 BV 접촉면 규약(AM|SE·AM|SDCP)과 동일.  carbon 기본 = VGCF(3)+SuperP(4)+
    SWCNT(8) = 전자 접점.  block 기본 = PTFE(7) — **개재 차단**: PTFE 가 AM|SE 사이에
    끼면 점군 coverage(순수 거리)는 못 보지만 이 walk 는 이웃 sid 로 직접 잡는다.

    ★ 점군 coverage 와 분업: 이 walk 는 위치·개재를 보고, 절대면적은 점군이 정확하다
      (복셀 표면은 계단으로 ~1.5× 과대; **비율** f_cov 에선 분자·분모 상쇄).
    ★ n_am 은 필수 인자 — pid.max()+1 추정은 마지막 입자가 표면에 안 잡히면 벡터가
      짧아진다 (SuperP `_fid.max()+1` 전역 오프셋 버그 회귀 방지).  도메인 밖은 void.

    Returns dict of [n_am] arrays: n_face, f_reaction, f_carbon, f_void, f_block.
    """
    sid = np.asarray(sid); pid = np.asarray(pid)
    am = (sid == 1) | (sid == 2)
    n_face = np.zeros(n_am, np.int64)
    c_rxn = np.zeros(n_am, np.int64); c_carb = np.zeros(n_am, np.int64)
    c_void = np.zeros(n_am, np.int64); c_blk = np.zeros(n_am, np.int64)
    rxn, carb, blk = list(reaction_sids), list(carbon_sids), list(block_sids)
    for ax in range(3):
        for sgn in (+1, -1):
            nb = np.zeros_like(sid)                       # 채우기 0 = 도메인 밖 → void
            dst = [slice(None)] * 3; src = [slice(None)] * 3
            if sgn > 0:
                dst[ax], src[ax] = slice(0, -1), slice(1, None)
            else:
                dst[ax], src[ax] = slice(1, None), slice(0, -1)
            nb[tuple(dst)] = sid[tuple(src)]
            m = am & ~((nb == 1) | (nb == 2))             # AM 복셀의 비-AM 이웃 face
            p, s = pid[m], nb[m]
            ok = (p >= 0) & (p < n_am)
            p, s = p[ok], s[ok]
            np.add.at(n_face, p, 1)
            np.add.at(c_rxn, p, np.isin(s, rxn).astype(np.int64))
            np.add.at(c_carb, p, np.isin(s, carb).astype(np.int64))
            np.add.at(c_void, p, (s == 0).astype(np.int64))
            np.add.at(c_blk, p, np.isin(s, blk).astype(np.int64))
    den = np.maximum(n_face, 1).astype(np.float64)
    return {'n_face': n_face,
            'f_reaction': c_rxn / den, 'f_carbon': c_carb / den,
            'f_void': c_void / den, 'f_block': c_blk / den}


def _selftest_trackb():
    """Track-B 헬퍼 검증 — 관례·이중계상 가드·face walk (개재 차단 포함)."""
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    # 선형 관례: 곧은 도체 φ=0.5, σ_eff=0.5σ → τ=1 정확
    chk('τ 선형 관례: 직선 도체 τ=1', abs(tau_from_solve(0.5, 2.0, 1.0) - 1.0) < 1e-12)
    t_lin = tau_from_solve(0.5, 1.0, 0.125)
    chk('★ 관례 지뢰가 실재: 같은 해가 선형 τ=4 vs √ 관례 2', abs(t_lin - 4.0) < 1e-12
        and abs(np.sqrt(0.5 * 1.0 / 0.125) - 2.0) < 1e-12)
    chk('τ None-가드 (σ_eff=0 → 발산 대신 None)', tau_from_solve(0.5, 1.0, 0.0) is None)

    # 이중계상 가드: AM 기하가 전부 설명하면 κ_dom = σ_bulk (배율 1)
    chk('κ_dom: τ_full=τ_geo·φ 동일 → 배율 1', abs(kdom_calibration(0.4, 2.0, 0.4, 2.0) - 1.0) < 1e-12)
    r = kdom_calibration(0.30, 3.0, 0.45, 1.5)            # SE 내부 몫이 남는 정상 케이스
    chk('κ_dom < 1 (SE 내부 넥/공극 몫)', r is not None and 0 < r < 1, f'{r:.4f}')
    chk('재현 항등식: κ_dom·(φg/τg) == σ·(φf/τf)',
        abs(r * (0.45 / 1.5) - 1.0 * (0.30 / 3.0)) < 1e-15)
    chk('κ_dom None-가드', kdom_calibration(None, 2.0, 0.4, 2.0) is None)

    # face walk: 고립 AM 1복셀 = 6 face 전부 void
    sid = np.zeros((5, 5, 5), np.int8); pid = np.full((5, 5, 5), -1, np.int32)
    sid[2, 2, 2] = 1; pid[2, 2, 2] = 0
    P = am_surface_patches(sid, pid, n_am=3)
    chk('고립 AM 1복셀 → 6 face 전부 void', P['n_face'][0] == 6 and P['f_void'][0] == 1.0)
    chk('★ n_am 명시 → 표면에 없는 입자도 벡터에 (SuperP 오프셋 회귀)',
        len(P['n_face']) == 3 and P['n_face'][1] == 0 and P['n_face'][2] == 0)

    # SE 가 한 면에 붙으면 f_reaction = 1/6;  SDCP(5) 도 반응상 (step4 규약)
    sid2 = sid.copy(); sid2[3, 2, 2] = 6
    chk('SE 인접 face → f_reaction 1/6',
        abs(am_surface_patches(sid2, pid, 3)['f_reaction'][0] - 1 / 6) < 1e-12)
    sid2[1, 2, 2] = 5
    chk('SDCP 도 반응상 (AM|SDCP BV 규약)',
        abs(am_surface_patches(sid2, pid, 3)['f_reaction'][0] - 2 / 6) < 1e-12)

    # ★ PTFE 개재: AM|PTFE|SE 면 그 face 는 block 이지 reaction 이 아니다 (점군은 못 보는 것)
    sid3 = sid.copy(); sid3[3, 2, 2] = 7; sid3[4, 2, 2] = 6
    P3 = am_surface_patches(sid3, pid, 3)
    chk('★ PTFE 개재 → block=1/6, reaction=0', abs(P3['f_block'][0] - 1 / 6) < 1e-12
        and P3['f_reaction'][0] == 0.0)

    # carbon face (VGCF sid3) + 도메인 경계 = void
    sid4 = np.zeros((3, 3, 3), np.int8); pid4 = np.full((3, 3, 3), -1, np.int32)
    sid4[0, 1, 1] = 2; pid4[0, 1, 1] = 1                  # 경계 위 AM_P, 입자 1
    sid4[1, 1, 1] = 3                                      # VGCF 이웃
    P4 = am_surface_patches(sid4, pid4, 3)
    chk('경계 face = void · VGCF face = carbon (입자별 분리)',
        P4['n_face'][1] == 6 and abs(P4['f_carbon'][1] - 1 / 6) < 1e-12
        and abs(P4['f_void'][1] - 5 / 6) < 1e-12 and P4['n_face'][0] == 0)

    # 두 입자 face 가 섞이지 않는다
    sid5 = np.zeros((7, 3, 3), np.int8); pid5 = np.full((7, 3, 3), -1, np.int32)
    sid5[1, 1, 1] = 1; pid5[1, 1, 1] = 0
    sid5[5, 1, 1] = 2; pid5[5, 1, 1] = 2
    sid5[2, 1, 1] = 6                                      # 입자 0 만 SE 접촉
    P5 = am_surface_patches(sid5, pid5, 3)
    chk('입자별 독립 집계', abs(P5['f_reaction'][0] - 1 / 6) < 1e-12
        and P5['f_reaction'][2] == 0.0 and P5['n_face'][2] == 6)

    print('TRACK-B SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def _selftest_temp():
    """σ_ion(T) 규약 — STEP3 표면에서 se_material 위임이 실제로 성립하는지 (bitwise + 배수표)."""
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    chk('SIGMA_ION_SE_S_CM_25C is bitwise 3.0e-3 (= the old bare 0.003 literal)',
        float(SIGMA_ION_SE_S_CM_25C).hex() == (0.003).hex(), float(SIGMA_ION_SE_S_CM_25C).hex())
    chk('sigma_ion_se_S_cm() with no T is bitwise 3.0e-3',
        float(sigma_ion_se_S_cm()).hex() == (0.003).hex())
    chk('sigma_ion_se_S_cm(25) is bitwise 3.0e-3 (T_ref identity)',
        float(sigma_ion_se_S_cm(25.0)).hex() == (0.003).hex())
    for t_c, want in ((30.0, 1.28), (45.0, 2.56), (60.0, 4.79)):   # docs table, T_ref 25, Ea 0.41
        r = sigma_ion_se_S_cm(t_c) / SIGMA_ION_SE_S_CM_25C
        chk(f'{t_c:.0f} °C → x{want} (docs/temp_pressure_capability.md T1-b)',
            abs(round(r, 2) - want) < 5e-3, f'got x{r:.4f}')
    p_off, p_on = temperature_provenance(), temperature_provenance(60.0)
    chk('provenance OFF = NOT_MODELLED', p_off['T_dependence'] == 'NOT_MODELLED'
        and p_off['T_C'] is None and p_off['T_ref_C'] == 25.0)
    chk('provenance ON = ARRHENIUS + Ea 0.41', p_on['T_dependence'] == 'ARRHENIUS'
        and p_on['Ea_ion_eV'] == 0.41)
    chk('σ_e stays T-independent (Reisacher ohmic; solver convention)',
        p_on['sigma_e_T_dependence'] == 'NOT_MODELLED')
    # the electronic/thermal tables must NOT have moved
    chk('SIGMA_DEFAULT electronic table untouched',
        SIGMA_DEFAULT == {'AM_S': 0.010, 'AM_P': 0.005, 'VGCF': 100.0, 'SuperP': 10.0,
                          'SDCP': 250.0, 'SWCNT': 100.0})
    chk('thermal k table untouched', (K_AM_THERMAL, K_SE_THERMAL) == (4.0e-2, 0.7e-2))

    # ── the σ_ion solve is LINEAR in the SE phase σ, so σ_eff(T)/σ_eff(T_ref) == the
    #    Arrhenius factor exactly.  This is what mpm_webapp_payload's --temp-c actually does
    #    (it scales the sig_i table entry for SE before solve_sigma_z).
    sid = np.zeros((4, 4, 6), np.int8); sid[:] = 6          # all-SE block (sid 6 = SE)
    def _sig_i(T=None):
        t = np.zeros(9); t[6] = sigma_ion_se_S_cm(T); return t
    r_ref = solve_sigma_z(sid, _sig_i(), 0.4, z_top_um=6 * 0.4, z_bot_um=0.0)['sigma_eff']
    r_60 = solve_sigma_z(sid, _sig_i(60.0), 0.4, z_top_um=6 * 0.4, z_bot_um=0.0)['sigma_eff']
    chk('σ_eff is exactly linear in σ_SE → σ_eff(60 °C)/σ_eff(25 °C) == x4.785',
        abs(r_60 / r_ref - se_material.arrhenius_sigma_factor(60.0)) < 1e-9,
        f'{r_ref:.6g} → {r_60:.6g}  (x{r_60/r_ref:.4f})')
    chk('σ_eff(no T) == σ_eff(25 °C) bitwise',
        float(r_ref).hex() == float(solve_sigma_z(sid, _sig_i(25.0), 0.4, z_top_um=6 * 0.4,
                                                  z_bot_um=0.0)['sigma_eff']).hex())
    print('TEMP SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true', help='run the analytic laminate/percolation checks')
    ap.add_argument('--selftest-rxn', action='store_true',
                    help='STEP4 sandwich analytic (series-R total current + uniform per-particle i + KCL)')
    ap.add_argument('--selftest-pore', action='store_true',
                    help='A6 pore-τ analytic checks (crop / PTFE stamp / TauFactor convention)')
    ap.add_argument('--selftest-pnm', action='store_true',
                    help='A13 pore-PNM checks (dumbbell 2-body/1-throat / closure / thin fallback)')
    ap.add_argument('--selftest-swcnt', action='store_true',
                    help='A14 SWCNT sheath 스탬프 검증 (phase6→sid8, 전자-도체/이온-투명 테이블)')
    ap.add_argument('--selftest-segstamp', action='store_true',
                    help='SR-01 opt-in 선분 스탬프 (기본 불변 + 연결 보장 + AM 관통 방지)')
    ap.add_argument('--integration', action='store_true',
                    help='run the committed real14 integration probe (AM-only vs +300 synthetic VGCF, '
                         'seed 0, vox 0.4) — reproduces the review-anchored numbers + monotonicity')
    ap.add_argument('--selftest-temp', action='store_true',
                    help='σ_ion(T) 규약 검증 (se_material 위임: T=None bitwise / 25 °C / 문서 배수표)')
    ap.add_argument('--selftest-trackb', action='store_true',
                    help='Track-B 헬퍼 검증 (τ 선형 관례 · κ_dom 이중계상 가드 · AM face walk)')
    se_material.temperature_argparse(ap)   # --temp-c / --ea-ion-ev (both default None)
    a = ap.parse_args()
    if a.selftest_temp:
        sys.exit(_selftest_temp())
    if a.selftest_trackb:
        sys.exit(_selftest_trackb())
    if a.temp_c is not None:               # resolve + report the SE ionic σ this run would use
        _p = temperature_provenance(a.temp_c, a.ea_ion_ev)
        print(f"σ_ion(SE) @ {a.temp_c:.1f} °C = {sigma_ion_se_S_cm(a.temp_c, a.ea_ion_ev):.6g} S/cm "
              f"(T_ref={_p['T_ref_C']:.0f} °C, Ea={_p['Ea_ion_eV']} eV, {_p['convention']})")
        se_material.warn_band(a.temp_c, a.ea_ion_ev)
        print('  ⇒ pass the same --temp-c to mpm_webapp_payload (which builds the sig_i table).')
        sys.exit(0)
    if a.selftest:
        sys.exit(_selftest())
    if a.selftest_rxn:
        sys.exit(_selftest_rxn())
    if a.selftest_pore:
        sys.exit(_selftest_pore())
    if a.selftest_pnm:
        sys.exit(_selftest_pnm())
    if a.selftest_swcnt:
        sys.exit(_selftest_swcnt())
    if a.selftest_segstamp:
        sys.exit(_selftest_segstamp())
    if a.integration:
        import os
        _csv = os.path.join(os.path.dirname(__file__), '..', 'docs/data/real14_am_scaffold.csv')
        am = np.loadtxt(_csv, delimiter=',', comments='#')
        t, c, r = am[:, 0].astype(int), am[:, 1:4] * 1000.0, am[:, 4] * 1000.0
        c[:, 2] -= (c[:, 2] - r).min()
        hi = (50.0, 50.0, float((c[:, 2] + r).max()))
        rng = np.random.default_rng(0)
        pts = []
        for _ in range(300):
            p0 = rng.uniform([0, 0, 0], hi); d = rng.normal(size=3); d /= np.linalg.norm(d)
            pts.append(p0 + np.outer(np.arange(0, 10, 0.2), d))
        pts = np.concatenate(pts); ph = np.full(len(pts), 2)
        inb = ((pts >= 0) & (pts < hi)).all(1); pts, ph = pts[inb], ph[inb]
        sig = np.array([0.0, 0.010, 0.005, 100.0, 10.0, 150.0, 0.0])
        out = {}
        for label, ap_, aph in (('AM-only', None, None), ('AM+VGCF', pts, ph)):
            sid, pid = rasterize(c, r, t, ap_, aph, (0, 0, 0), hi, 0.4)
            res = solve_sigma_z(sid, sig, 0.4, z_top_um=hi[2], z_bot_um=0.0)
            out[label] = res['sigma_eff']
            print(f"[{label:8s}] σ_eff={res['sigma_eff']:.4g} S/cm  dof={res['n_dof']:,} "
                  f"plate_vox={res['n_plate_vox']} resid={res['resid']:.1e}")
        boost = out['AM+VGCF'] / max(out['AM-only'], 1e-30)
        print(f"carbon boost ×{boost:.2f}  → {'PASS (monotone)' if boost > 1.0 else 'FAIL'}")
        sys.exit(0 if boost > 1.0 else 1)
    ap.print_help()
