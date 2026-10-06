"""
DEM-Native Transport Framework v2.0
====================================
Kirchhoff resistor network solver for effective conductivity in ASSB composite cathodes.

Each SE-SE (or AM-AM) contact → edge with R = R_bulk + R_constriction (series).
  R_bulk: geometric normalization for particle bulk resistance
  R_constriction: Maxwell spreading resistance R = 1/(2σa), Holm (1967)

Three decomposition runs:
  1. FULL: R_bulk + R_constriction → σ_full (explicit-contact model estimate)
     ⚠ **물리 정본이 아니다** (Codex R20-06).  입력 σ_bulk 로 선형 스케일되는 모델
       추정치이고, **AM–AM 망만** 푼다 (VGCF/SDCP 복합망은 STEP3 복셀 솔버 소관) ⇒
       두 솔버는 같은 estimand 가 아니다.  이 값의 자연스러운 형태는 무차원
       formation factor `F_e = σ_eff / σ_AM,input` 이다.
  2. CONTACT_FREE: R_constriction=0 → σ_cf (협착 0 가지 — ⚠ 상한 아님 (10-06 저녁 · TAU-07): 원기둥 bulk 의 T_CF ≈ 4/z 모형 과전도 ·
     q > 1.5 면 값 유지 + 상태 model_over_conduction · 진단 열만)
  3. CONSTRICTION_ONLY: R_bulk=0 → σ_constr (spreading resistance limit)

σ_eff/σ_bulk = G_eff × L / A  (Ohm's law, dimensionless)

전극 (세대 2 · 2026-10-06 · L2-05): 바닥 띠 V = 1 · 위 띠 V = 0 **정확 Dirichlet** — G = 바닥 띠에서 나가는 전류 (가상 전원 · 싱크 g_b 없음).
수치 증서 (10-06 밤 · G2R-03): 풀이마다 I_bottom · I_top · 보존 잔차 · 내부 잔차 · 방법을 싣고 허용치 (1e-6) 를 넘는 해는 사다리로 다시 풀거나
  내지 않는다 (current_conservation_failed) · 협착-only 의 R_c = 0 간선은 풀지 않는다 (GEN2-01 · zero_resistance_requires_contraction).
  ★ G2RR-02 (10-06 밤): 증서마다 결합 정보 (가지 · 채널 · 역할 · ΔV · 기하 · G→q · σ_bulk — CERT_BINDING_FIELDS) — 수용 검사 = tau_flux (기록만 · σ 비트 동일).
Physics 면적 (세대 2): `plastic_coverage.film_area_g2` (규칙 B · µm · 쌍별 E* · 정확 lens) — 세대 1 은 명시 `area_rule='physics_g1'`.
Hertz 기본 = H0 (Maxwell 협착 + 원기둥 반 d bulk · 세대 1 과 같은 간선) · H12 (ψ 곱 + 구 조각 bulk) = 짝 인자로만 · 이온 민감도 레코드.

Networks: ionic (SE-SE), electronic (AM-AM), thermal (all contacts)

References:
  - Holm 1967: Electric Contacts — Maxwell constriction resistance
  - Bruggeman 1935: σ_eff = σ_0 × φ^n (EMT, for comparison)
  - Minnmann et al. 2021: Electronic percolation in SSB cathodes
"""

import numpy as np
import json
import os
import sys
from scipy import sparse
#  ★ 10-06 밤 G2R-03 — 사다리 단 (gmres · spilu · LinearOperator) 도 모듈 이름으로 부른다 (measure_rho · 시험이 cg · spsolve 를 이 자리에서 바꿔 끼운다)
from scipy.sparse.linalg import spsolve, cg, gmres, spilu, LinearOperator

# Plastic-physics contact-area model (used when contact_mode='physics')
# See docs: scripts/plastic_coverage.py → film_area_from_overlap()
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
if _THIS_DIR not in sys.path:
    sys.path.insert(0, _THIS_DIR)
try:
    from plastic_coverage import film_area_from_overlap as _film_area
except Exception:
    _film_area = None  # graceful fallback if numpy/import issue
#  ★ 10-06 세대 2 Physics 면적 (C2 ①–⑤) — 없으면 physics 모드가 거부한다 (조용히 세대 1 로 떨어지지 않는다).
try:
    from plastic_coverage import (film_area_g2 as _film_area_g2, H_FILM_MIN as _H_FILM_MIN,
                                  H_FILM_STATUS as _H_FILM_STATUS)
except Exception:
    _film_area_g2, _H_FILM_MIN, _H_FILM_STATUS = None, None, None

import se_material  # single source of truth for σ_grain + its temperature convention


# LPSCl argyrodite grain interior conductivity (NOT pellet value)
# ★ 2026-07-28: value now comes from se_material (one definition for the whole repo —
# it used to be duplicated as a bare 3.0/3.0e-3 literal in ≳12 files, so "add T-dependence"
# could not be a one-line edit; docs/temp_pressure_capability.md §3-4 / T1-b).  The number
# is UNCHANGED (3.0e-3 S/cm, bitwise) and is declared at se_material.T_REF_C = 25 °C.
SIGMA_BULK_DEFAULT = se_material.SIGMA_GRAIN_S_CM_25C  # S/cm (grain interior, ionic, @25 °C)

# NCM electronic conductivity (typical, SOC-dependent)
SIGMA_AM_ELECTRONIC = 0.05  # S/cm (50 mS/cm, NCM811 grain interior, discharged)
#: build_network 가 **실제로** 받은 mode (코드리뷰 A2 재현·회귀용).  None = 아직 안 불림.
LAST_BUILD_MODE = None

# ── 협착저항의 ψ 배치 (`L2-01` · 계약 `docs/area_contract_20260913.md` §C·§⑥ · 개정 2026-10-06) ──────────
#   `PSI_MULTIPLY` = `R_c = ψ/(2σa)`    ← ★ 세대 2 기본 = 곱셈 (1저자 개정 2026-10-06)
#   `PSI_DIVIDE`   = `R_c = 1/(2σaψ)`   ← 세대 1 (`legacy_divide` · 10-06 전의 모든 Physics σ) — **명시 인자로만** (옛 값 재현용)
#   비 = `(1−s)^−3` (s = a_eff/r_min) 이고 `s=0.9` 에서 1,620배.
#   근거 = 결과와 무관한 독립 기준해 (축대칭 flux-tube 유한체적 `scripts/constriction_reference.py` · AREA-09 STEP 4 —
#     곱셈이 10 점 모두에서 우위).  계약 봉인 창 (2026-09-17 23:59 KST) 을 지나 S3 봉인 · 런이 없어 등록 경로 (봉인 → 런 → 판정)
#     대신 **개정**으로 바꿨다 (`docs/area_contract_20260913.md` 개정 노트 · S3 h0/h1 판정은 하지 않는다).
#   ⚠ 세대 표기 = 망 · 결과의 `psi_placement` (이온 · 전자 · 열 세 채널) — 세대 1 · 2 의 σ 를 표기 없이 섞지 말 것
#     (`case_master.csv` · 스케일링법칙 적합의 Physics 타깃은 세대 1 위에 있다 · 재적합은 별건 — 계약 §3).
#   ⚠ Hertz 가지는 ψ 를 쓰지 않는다 — 배치와 무관하게 비트 동일.
PSI_DIVIDE = 'legacy_divide'
PSI_MULTIPLY = 'multiply'
PSI_PLACEMENTS = (PSI_DIVIDE, PSI_MULTIPLY)
PSI_PLACEMENT_DEFAULT = PSI_MULTIPLY

# ── 망 세대 2 (1저자 비준 2026-10-06 *"권고대로"* · C1 · C2 설계 · 계약 `docs/area_contract_20260913.md` 10-06 개정 노트) ──────────
#  세 축은 서로 독립이고 결과 · τ 인계 열에 **각각** 실린다 (세대를 표기 없이 섞지 않는다 — tau_flux · 인계 생성기가 섞임을 거부한다).
#  ① Physics 면적 (`L1-01` · `L1-02` · `L1-03` · `DESC-03` · `DESC-10`) — 세대 2 = `plastic_coverage.film_area_g2` (규칙 B · floor = c_cpl[22]
#     원판 · 정확 lens · 쌍별 E* · µm + length_scale 1e6 · 수송 cap π r_min²) · 세대 1 = 옛 `film_area_from_overlap` (sim 단위 그대로) — **명시 인자로만**.
AREA_RULE_G1 = 'physics_g1'
AREA_RULE_G2 = 'physics_g2'
AREA_RULES = (AREA_RULE_G1, AREA_RULE_G2)
AREA_RULE_DEFAULT = AREA_RULE_G2
AREA_RULE_HERTZ = 'hertz_ccpl22'          # Hertz 모드 면적 = LIGGGHTS c_cpl[22] 기하 교차 원판 (L1-04 — "Hertz" 는 이름만)
G2_LENGTH_SCALE_UM = 1.0e6                # µm 단위 — 1 m = 1e6 µm (DESC-03: h_film 을 δ · r 과 같은 단위로)
#  ② 전극 (`L2-05`) — 정확 Dirichlet (바닥 띠 V = 1 · 위 띠 V = 0).  옛 가상 전원 · 싱크 (g_b) 는 지웠다 — 세대 1 σ 는 git 이력의 옛 모듈로만 재현한다
#     (test_network_boundary_rule ⑨ 가 그렇게 한다).  ELECTRODE_LEGACY 는 **표기 없는 옛 산출물의 이름**이다 (만들 수 없다).
ELECTRODE_DIRICHLET = 'dirichlet_exact'
ELECTRODE_LEGACY = 'virtual_source_legacy'
DIRICHLET_DIRECT_MAX_FREE = 30000          # 자유 노드가 이보다 많으면 CG (rtol 1e-10 · atol 0 · 실패하면 ILU 전처리 · 그래도 실패하면 직접해) —
#                                            solve_network 의 문턱 줄은 글자 그대로 30000 (measure_rho 치환 앵커 · 셀프테스트가 같은 값인지 본다)
DIRICHLET_CG_RTOL = 1e-10
BOUNDARY_OVERLAP_REASON = 'boundary_overlap'   # B ∩ T ≠ ∅ — 한 노드에 V = 1 과 0 을 동시에 강제할 수 없다 (풀지 않는다)
#  ★ 10-06 밤 수치 증서 (`G2R-03` · Codex 세대 2 판정 §4 · §8 · 1저자 비준) — 정확 Dirichlet 풀이마다 증서를 싣는다 (solve_info · 결과
#     `solve_certificate_<가지>`): I_bottom · I_top (양 전극 띠 전류) · conservation_rel = |I_b + I_t| / max(|I_b|, |I_t|, tiny) ·
#     residual_rel = ‖L_ff·x − b‖ / max(‖b‖, tiny) (풀린 자유 노드 계) · method (채택한 단) · attempts (단마다 결과).
#     ⚠ CG 종료 (info 0) · 유한 해 · G ≤ 1.1·Σg 는 증서가 아니다 — 큰 막다른 간선이 ‖b‖ 를 지배하면 rtol·‖b‖ 가 관통 전류의 오차를 묶지 못한다
#       (Codex 반례: B 에만 붙은 10^14 S 막다른 간선 · 자유 노드 30,002 → cg · G 30,001 = 참값 15,000.5 의 +100 % · I_top −3e-10 · 내부 잔차 1.7e-12 로 통과).
#       보존은 KCL 의 귀결이다 (1ᵀL = 0 → I_b + I_t = −Σ_free (L_ff·x − b)) — 그 반례에서 1.0.
#  허용치 — 새 배치 전에 고정 (결과를 보고 옮기지 않는다):
#     보존 1e-6 — 실침대 실측 (Codex 재계산 + 이 리포 재측정 · 두 기계): real_14 (spsolve · 자유 28,231) 게시 가지 ≤ 1.4e-13 · case15 (cg ·
#       자유 55,912) FULL ≤ 6.4e-9 · CF ≤ 1.1e-10 · 협착-only (R_c = 0 간선 없는 H0 · H12) ≤ 5.9e-9 → 게시되는 값의 최댓값보다 150 배 이상 위 ·
#       반례 (O(1)) 보다 백만 배 아래.  (case15 physics g2 협착-only 3.6e-7 – 1.3e-6 은 R_c = 0 간선을 지운 다른 회로다 — 아래 GEN2-01 로 풀지 않는다.)
#     내부 잔차 1e-6 — CG 종료 기준 (rtol 1e-10 · ‖b‖ 상대) 보다 4 자리 느슨 · 직접해는 ~1e-15 → 해가 아닌 해 (전처리 잔차로 멈춘 Krylov ·
#       수치적으로 특이한 직접해) 만 거른다.  ⚠ 이것만으로는 위 반례를 못 잡는다 (1.7e-12) — 주 기준은 보존이다.
#     ⚠ (Codex 세대 2 재검증 §4 Q3) 1e-6 은 보존 · 내부 잔차의 **수용 문턱**이다 — 임의 망에서 σ 상대오차가 1e-6 이하라는 보증이 아니다 (내부 잔차의
#       분모 ‖b‖ 를 큰 항이 지배하면 작은 물리 전류의 오차를 가릴 수 있고 · 조건수 · 전극 선택 · 모델 오차는 별개다).
DIRICHLET_CONSERVATION_REL_MAX = 1e-6
DIRICHLET_RESIDUAL_REL_MAX = 1e-6
#  사다리 — 첫 단이 증서를 넘으면 해를 건드리지 않는다 (오늘과 비트 동일).  다음 단으로 가는 것은 셋뿐 — 첫 단 CG 미수렴 · 증서 실패 (보존 · 내부
#  잔차) · 0 < G ≤ 1.1·Σg 밖:
#     작은 망 (자유 ≤ 30,000): spsolve → cg+jacobi → gmres+ilu
#     큰 망  (자유 > 30,000): cg → spsolve_fallback (자유 ≤ DIRICHLET_FALLBACK_DIRECT_MAX_FREE 일 때만) → cg+jacobi → gmres+ilu
#     ★ 10-06 밤 (Codex 세대 2 재검증 §4 Q3 — "실패면 모두 다음 사다리" 는 코드와 다르다) — **첫 단 (spsolve · cg 둘 다) 의 예외는 사다리를 타지
#       않는다**: 그 가지 = solve_failed (값 없음) 로 끝낸다 (solve_network 의 예외 처리 · 실패 주입 시험 test_network_solve_certificate K ·
#       test_network_handover_chain 의 break_solver 가 이 자리를 쓴다).  의도 = 첫 단 예외는 입력 퇴화 · 실행 환경 (메모리 · 라이브러리) 문제이지
#       수치 오차가 아니어서 다른 방법의 해로 덮지 않는다 — 안전한 거부 (false-green 아님).  가용성 한계 = 일시적 자원 실패도 그 가지는 값 없음 →
#       재실행해야 한다.  사다리 **안** (둘째 단부터) 의 예외는 기록하고 (attempts · outcome exception) 다음 단으로 간다.
#     ⚠ DIRICHLET_FALLBACK_DIRECT_MAX_FREE 는 직접해를 **시도할** 크기 상한이지 메모리 보증이 아니다 — 실행 환경의 자원 실패 (MemoryError 등) 는 그 단의
#       예외로 기록되고 다음 단 · 끝까지 증서를 낸 단이 없으면 값을 내지 않는다 (current_conservation_failed · solve_failed — 숫자 없이 남긴다).
#     cg+jacobi = 대각 (SPD) 전처리 CG · gmres+ilu = ILU 전처리 GMRES — ILU 는 SPD 가 보장되지 않아 CG 에 넣지 않는다 (옛 'cg+ilu' 폐기 ·
#     SciPy cg 의 M 은 SPD 여야 한다) · 두 Krylov 단은 잔차 보정 (A·δ = r 을 다시 푼다 — 매 회 종료 기준이 그때 잔차 상대라 큰 RHS 성분에 묻힌
#     작은 성분도 풀린다) · 모든 단이 증서를 못 넘으면 값을 내지 않는다 (NOT_COMPUTED + CURRENT_CONSERVATION_FAILED_REASON).
DIRICHLET_FALLBACK_DIRECT_MAX_FREE = 250000   # 사다리 직접해 시도 상한 (메모리 보증 아님 — 위 ⚠) — 실침대 case15 이온 망 (자유 55,912) 직접해 2.3 s · < 1 GB (실측) · 현 캠페인 침대 ≤ 114,609 입자
DIRICHLET_REFINE_PASSES = 4                   # Krylov 단의 잔차 보정 횟수 상한
DIRICHLET_KRYLOV_MAXITER = 20000              # 사다리 Krylov 단의 반복 상한 (첫 단 CG 와 같은 값 · GMRES 는 restart 50 × 400 회)
DIRICHLET_METHODS = ('none_free', 'spsolve', 'cg', 'spsolve_fallback', 'cg+jacobi', 'gmres+ilu')
CURRENT_CONSERVATION_FAILED_REASON = 'current_conservation_failed'
#  ★ 10-06 밤 GEN2-01 (Codex §7 Q3 · 1저자 비준) — 협착-only 가지의 관통 간선에 R_c = 0 (ψ floor · clamp — 소성 원판이 r_min 에 닿음) 이 있으면
#     그 간선은 단락인데 옛 판은 L 에서 빼서 개방으로 풀었다 = 다른 회로 (Codex 반례: 0.1 S computed ↔ 단락 수축 1.1 S).  정확한 값은 R_c = 0
#     성분을 수축해야 하고 (B · T 를 함께 품으면 무한 conductance) 작은 ε 저항 치환은 새 수치 매개변수라 쓰지 않는다 → 그 가지만 NOT_COMPUTED +
#     이 사유 · FULL (R_bulk > 0) · CF (1e-12 floor) 는 그대로.
ZERO_RESISTANCE_REASON = 'zero_resistance_requires_contraction'
#: 망 σ 가 None 일 때 solve_info 사유를 그대로 상태 사유로 올리는 것 (그 밖 = solve_failed) — `_net_sigma_status`.
NOT_COMPUTED_SOLVE_REASONS = (BOUNDARY_OVERLAP_REASON, CURRENT_CONSERVATION_FAILED_REASON, ZERO_RESISTANCE_REASON)
#  ③ Hertz 가지 (C1-3) — 기본 H0 = Maxwell 협착 1/(2σa) + 원기둥 반 d bulk (세대 1 과 같은 간선 · 주 값).  H12 = ψ 곱셈 협착 + 구 조각 bulk 를
#     **짝으로만** (ψ 단독 H1 = 모든 기하에서 과전도 +6…+50 % · 기각 · bulk 단독도 받지 않는다) — 이온 민감도 레코드 (`hertz_h12`) 로만 쓴다.
HERTZ_CONSTRICTION_MAXWELL = 'maxwell'
HERTZ_CONSTRICTION_PSI = 'mikic_psi_multiply'
BULK_CYLINDER = 'cylinder_half_d'
BULK_SPHERE_SEGMENT = 'sphere_segment'
HERTZ_ARMS = {(HERTZ_CONSTRICTION_MAXWELL, BULK_CYLINDER): 'H0', (HERTZ_CONSTRICTION_PSI, BULK_SPHERE_SEGMENT): 'H12'}
HERTZ_H12_MODE = 'hertz_h12'               # 이온 민감도 레코드의 이름 (Hertz 결과 안 · τ 인계 모드 꼬리)
#  ④ CF 가드 (C1-5) — σ_ratio > 1.5 거부는 **FULL 에만**.  CONTACT_FREE · CONSTRICTION_ONLY 의 q > 1.5 = 모형 과전도 (간선별 bulk · T_CF ≈ 4/z) —
#     값 유지 + 상태 (진단 열만).
MODEL_OVER_CONDUCTION = 'model_over_conduction'
MODEL_OVER_CONDUCTION_REASON = 'q_gt_1p5'

# ───────────────────────────────────────────────────────────────────────
# Grain-boundary (crystallinity) correction for NCM σ_AM — "Trevisanello-spirit"
# DIRECTION + corpus-fit (β, r0).  See A1 note in generate_comparison_plots.py.
# ───────────────────────────────────────────────────────────────────────
# ⚠ ATTRIBUTION (2026-06-30, audit ⚠#11): Trevisanello 2021 measured Li⁺ chemical
# diffusion / BET / R_ct — NOT σ_e and NOT a σ-vs-radius curve.  What transfers is
# only the DIRECTION (single-crystal lacks internal GBs → less reduction; large
# polycrystalline secondaries have internal GBs → reduced effective transport).
# The FORM σ_eff = σ_grain/(1+(r/r0)^β) with r0=2 µm, β=1.5 is OUR corpus fit, not a
# Trevisanello formula — really a crystallinity/grain-contact-efficiency factor.
# Per-particle effective σ_AM:
#   - AM_S (small primary single-crystal, ≈2.5 µm): minimal GB effect → ≈ σ_grain (1.0×)
#   - AM_P (large polycrystalline secondary, ≈5 µm): GB reduction → σ_grain/(1+(r/r0)^β)
# ⚠ MATERIAL-SPECIFIC: the single>poly direction holds for UNDOPED NCM811; W-doped
# NCWA (#266 Oh) shows poly ≫ single → for those materials σ_AM is a material INPUT.
NCM_AM_REF_R = 2.0       # µm reference radius (corpus-fit; r0)
NCM_AM_GB_EXPONENT = 1.5  # GB-reduction exponent β (corpus-fit; Trevisanello-spirit direction)


def _sigma_status(v):
    """σ 값의 **상태**.  숫자 필드가 truthy 로 0 을 None 에 접는 것을 보완한다 (F-12).

      'valid_zero'   — 실제로 0 이다 (퍼콜 경로 없음).  물리적으로 유효한 값이며 실패가 아니다.
      'computed'     — 0 이 아닌 값이 계산됐다.
      'not_computed' — 값이 없다 (None/NaN) = 풀지 못했거나 실행되지 않았다.

    ⚠ 숫자 필드(`sigma_*`)는 하위호환을 위해 0 을 None 으로 내보내는 옛 규약을 유지한다.
      '0 인가 실패인가' 를 물을 때는 **이 상태 필드**를 볼 것.
    ⚠ 10-05 RGL-02: 값만 보는 이 분류로는 망 σ 의 None 이 비관통인지 실패인지 모른다 (solve_network 는 둘 다 None) — 망 결과의
      `sigma_*_status` 는 그래프의 관통 성분까지 보는 `_net_sigma_status` 가 정한다 (증명된 비관통만 valid_zero + no_through_path).
    """
    if v is None:
        return 'not_computed'
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 'not_computed'
    if f != f:                       # NaN
        return 'not_computed'
    return 'valid_zero' if f == 0.0 else 'computed'


#: ★ 10-05 RGL-02 (Codex · 1저자 비준 "권고대로") — 망 σ 가 None 인 **두 사건을 생산자가 가른다**.
#:   `solve_network` 는 관통 성분이 없어도 · 관통인데 풀이가 실패해도 똑같이 (None, None) 을 돌려준다 → 옛 판은 둘 다
#:   'not_computed' 였고 (TAU-22 — docstring 의 "valid_zero = 퍼콜 경로 없음" 은 도달 불가였다) 새 network 정지 관문이 정상 비관통을
#:   failed 로 막았다.  이제 **같은 그래프에서 bottom ↔ top 관통 성분이 없음을 확인한 경우에만** valid_zero + 이 사유를 낸다.
#:   숫자 필드 (`sigma_*`) 는 F-12 대로 None 을 유지한다 (UI '—' · 코퍼스 불변).  관통 σ 는 비트 동일 (해는 그대로 · 상태 필드만).
NO_THROUGH_REASON = 'no_through_path'        # 관통 성분 없음 = 물리적 0 (valid_zero) — conductivity · f 의 0
SOLVE_FAILED_REASON = 'solve_failed'         # 관통 성분은 있는데 σ 를 못 냈다 (예외 · V_source ≤ 0 · Σg 상한 · σ_ratio>1.5 · 경계 겹침 퇴화)
#                                              ★ 10-06 밤 — 증서 실패 (current_conservation_failed) · 협착-only 의 R_c = 0 (zero_resistance_requires_contraction) ·
#                                              경계 겹침은 따로 이름을 가진다 (`NOT_COMPUTED_SOLVE_REASONS` — 상태는 셋 다 not_computed)
NON_FINITE_REASON = 'non_finite'             # 값이 NaN (수치 실패)
#: 협착 전력 몫 (④a) 이 None 일 때의 상태 — 비관통 (0/0 미정의) 과 관통인데 FULL 풀이 실패를 가른다 (RGL-08: 등록된 물리 사유 ↔ 실패).
CPS_NO_THROUGH_STATUS = 'not_computed (no percolating FULL solution)'      # 옛 문자열 그대로 = 비관통 (constriction_power_share(None))
CPS_SOLVE_FAILED_STATUS = 'not_computed (FULL solve failed on a percolating network)'


def _net_sigma_status(v, no_through, solve_info=None):
    """망 σ (FULL · CONTACT_FREE · CONSTRICTION_ONLY) 의 (상태, 사유) — 값 분류는 `_sigma_status` 를 재사용한다 (판정 중복 금지).

      · 값 있음 → ('computed', None)  (실제 0 이면 ('valid_zero', 'zero_value'))
        ★ 10-06 C1-5: 솔버가 그 풀이를 모형 과전도로 표지했으면 (CF · 협착-only 의 q > 1.5) → ('model_over_conduction', 'q_gt_1p5') · 값 유지
      · None ∧ no_through (같은 그래프의 관통 성분 0) → ('valid_zero', NO_THROUGH_REASON)   ← 증명된 비관통
      · None ∧ 경계 겹침 (★ 10-06 L2-05 — 솔버 사유 boundary_overlap) → ('not_computed', BOUNDARY_OVERLAP_REASON)
      · None ∧ ★ 10-06 밤 — 증서 실패 (G2R-03 · current_conservation_failed) · 협착-only 의 R_c = 0 (GEN2-01 ·
        zero_resistance_requires_contraction) → ('not_computed', 그 사유)   (`NOT_COMPUTED_SOLVE_REASONS`)
      · None ∧ 관통 → ('not_computed', SOLVE_FAILED_REASON)  · NaN → ('not_computed', NON_FINITE_REASON)
    no_through 는 `active_fractions(net)['perc_nodes']` 가 비었는가 (반올림 전 · solve_network 와 같은 그래프 · 같은 띠).
    solve_info = 그 풀이의 `net['solve_info'][mode]` (solve_network 가 남긴다 · 없으면 옛 규칙)."""
    st = _sigma_status(v)
    info = solve_info if isinstance(solve_info, dict) else {}
    if st == 'computed':
        #  ★ 10-06 C1-5 — CF · 협착-only 가지의 q > 1.5 는 값 유지 + 모형 과전도 상태 (FULL 은 솔버가 None 으로 거부한다)
        if info.get('status') == MODEL_OVER_CONDUCTION:
            return MODEL_OVER_CONDUCTION, MODEL_OVER_CONDUCTION_REASON
        return st, None
    if st == 'valid_zero':
        return st, 'zero_value'
    if v is None and no_through:
        return 'valid_zero', NO_THROUGH_REASON
    if v is None and info.get('reason') in NOT_COMPUTED_SOLVE_REASONS:     # 경계 겹침 · 증서 실패 · 협착-only 의 R_c = 0
        return 'not_computed', info['reason']
    return 'not_computed', (SOLVE_FAILED_REASON if v is None else NON_FINITE_REASON)

def sigma_AM_relative(r_um, particle_type):
    """Relative σ_AM vs grain interior (crystallinity/GB factor; corpus-fit,
    Trevisanello-spirit direction — see A1 note above, NOT a Trevisanello σ_e formula).
    Returns 1.0 if no GB scaling (single-crystal or non-AM particle).
    Returns < 1.0 for polycrystalline secondary aggregates with internal GBs.

    Convention (consistent with input_params type_map):
      AM_S = small primary single-crystal NCM    → no GB scaling, ratio = 1.0
      AM_P = large polycrystalline secondary NCM → GB reduction (corpus-fit factor)
      SE, others                                 → ratio = 1.0 (not used in AM-AM)
    """
    if particle_type == 'AM_P':
        return 1.0 / (1.0 + (max(r_um, 0.1) / NCM_AM_REF_R) ** NCM_AM_GB_EXPONENT)
    # AM_S, SE, or other: no scaling
    return 1.0

# Thermal conductivity (W/(m·K) = W/(m·K) × 10⁻⁴ = W/(cm·K))
K_AM_THERMAL = 4.0e-2   # W/(cm·K) ≈ 4 W/(m·K), NCM
K_SE_THERMAL = 0.7e-2   # W/(cm·K) ≈ 0.7 W/(m·K), LPSCl (Ketter 2025)


# ─── D1-C / D1-F: σ_disk / σ_bulk ratios ──────────────────────────────────
# Constriction at the contact disk traverses a region whose σ may differ
# from grain interior σ. Two physical sources:
#   D1-F (regime-based): plastic contact has compressed/amorphized disk
#                        → σ_disk < σ_grain. Hertzian (elastic) contact
#                        retains crystalline σ. Bracketed by Sakuda 2013
#                        single-crystal (3.0) vs cold-pressed pellet (0.31)
#                        — geometric mean ~1.0, so factor ~0.33 for fully
#                        amorphized disk.
#   D1-C (AM-environment): SE close to polycrystalline AM_P inherits more
#                          GB content; near single-crystal AM_S retains
#                          high σ. Multiplicative on top of D1-F.
SIGMA_DISK_RATIO_AMORPH = 0.50   # plastic-disk σ / grain σ (D1-F)
SIGMA_DISK_RATIO_AM_P   = 0.80   # AM_P-environment factor (D1-C)
SIGMA_DISK_RATIO_AM_S   = 0.95   # AM_S-environment factor (D1-C)


def get_sigma_disk_factor(regime, t1, t2, sigma_model='uniform',
                          am_p_types=None, am_s_types=None):
    """σ_disk / σ_bulk for this contact.

    sigma_model:
      'uniform'  : 1.0 (current default — no per-contact σ variation).
      'regime'   : D1-F only. Plastic regimes get amorphized σ_disk.
      'gb_aware' : D1-C + D1-F. Adds AM-environment modulation for
                   SE-AM and AM-AM contacts on top of regime factor.
    """
    if sigma_model == 'uniform':
        return 1.0
    factor = 1.0
    # D1-F: amorphization in plastic regimes (Tabor / volume / geometric caps)
    if regime in ('tabor', 'volume', 'geom'):
        factor *= SIGMA_DISK_RATIO_AMORPH
    if sigma_model == 'gb_aware':
        # D1-C: only applies when AM is involved (AM environment affects σ
        # in the contact-disk region). For pure SE-SE contacts, no effect.
        if am_p_types and (t1 in am_p_types or t2 in am_p_types):
            factor *= SIGMA_DISK_RATIO_AM_P
        elif am_s_types and (t1 in am_s_types or t2 in am_s_types):
            factor *= SIGMA_DISK_RATIO_AM_S
    return factor


#: ★ 2026-10-04 — τ 결정 16 ② 안 A (1저자 비준 *"권고대로"*).  `build_network` 의 띠 선택을 이 함수로 옮기고 (식 · 순서 그대로 =
#:   **동작 중립** — `scripts/test_network_boundary_rule.py` 가 추출 전 기준값과 대조) **쓴 규칙과 띠 폭을 돌려준다**.
#:   옛 코드는 L0 → L1 → L2 폴백을 조용히 하고 남기지 않았다 (`LHS-17` · `TAU-14`) — 인계 게이트 G1 (L0 일 때만 값,
#:   `scripts/tau_flux.py`) 은 이 기록 없이는 판정할 수 없다.
#:   ⚠ 이 모듈은 S3 수치 모듈 (`seal_s3_prerun.NUMERIC_MODULES`) — 봉인은 수정 금지가 아니라 **재봉인 강제**다 (S3 전에 다시 봉인).
#:   ⚠ `dem_analysis_core.calc_percolation` 도 같은 규칙을 **따로** 들고 있다 (기록 없음 — LHS-17 의 그쪽 절반은 열림).
BOUNDARY_RULES = ('L0', 'L1', 'L2')


def boundary_sets(atoms_raw, target_ids, plate_z, boundary_factor):
    """(bottom_ids, top_ids, rule, band_frac) — rule ∈ BOUNDARY_RULES.

    band_frac = (바닥 띠 폭 + 위 띠 폭) / plate_z (판 간격 기준 · 바닥 = z 0).  L0 은 입자마다 문턱이 달라 **가장 큰 반지름**으로
    잰다 (= 2·boundary_factor·r_max / plate_z — `TAU-24` 의 띠 끝 단락 상한 4r_SE/L) · L1 = 0.30 · L2 = 관측 범위 문턱 기준.
    띠 노드는 등전위로 묶이고 정규화는 판 간격이라 T 를 이 비만큼까지 낮출 수 있다 (v2 §3-6).
    """
    target_ids = list(target_ids)
    if not target_ids:
        return set(), set(), None, None
    # ── C4 patch: per-particle plate-contact test ───────────────────────
    # Match calc_percolation behavior — each particle judged by its own
    # radius, not a global min(r) threshold. r_SE-independent → fair across
    # D0.5 vs D1.5 cases.
    bottom_ids = {aid for aid in target_ids
                  if atoms_raw[aid]['z'] <= atoms_raw[aid]['radius'] * boundary_factor}
    top_ids = {aid for aid in target_ids
               if atoms_raw[aid]['z'] >= plate_z - atoms_raw[aid]['radius'] * boundary_factor}
    r_max = max(atoms_raw[aid]['radius'] for aid in target_ids)
    rule, w_bot, w_top = 'L0', r_max * boundary_factor, r_max * boundary_factor

    # Fallback L1: thin electrodes / strict boundary → 15%/85% of plate_z
    if len(bottom_ids) < 3 or len(top_ids) < 3:
        z_bottom = plate_z * 0.15
        z_top = plate_z * 0.85
        bottom_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] <= z_bottom}
        top_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] >= z_top}
        rule, w_bot, w_top = 'L1', z_bottom, plate_z - z_top

    # Fallback L2: when plate_z overshoots the actual particle range
    # (mesh_info.json absent → plate_z uses atom max z+r which overshoots
    # the true top plane by one AM radius), anchor the 15/85% split to the
    # OBSERVED z-range of target particles. Prevents silent percolation=0
    # for thick electrodes where top_ids empties under plate_z-based bounds.
    if len(bottom_ids) < 3 or len(top_ids) < 3:
        z_vals = [atoms_raw[aid]['z'] for aid in target_ids]
        z_min_obs = min(z_vals); z_max_obs = max(z_vals)
        span = z_max_obs - z_min_obs
        z_bottom = z_min_obs + span * 0.15
        z_top = z_max_obs - span * 0.15
        bottom_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] <= z_bottom}
        top_ids = {aid for aid in target_ids if atoms_raw[aid]['z'] >= z_top}
        rule, w_bot, w_top = 'L2', z_bottom, plate_z - z_top

    band_frac = float((w_bot + w_top) / plate_z) if plate_z > 0 else None
    return bottom_ids, top_ids, rule, band_frac


def _phase_class(label):
    """상 이름 → 'SE' · 'AM' · None (모름).  type_map 규약 (AM_P · AM_S · AM · SE) — `sigma_AM_relative` 와 같은 이름 체계."""
    if label == 'SE':
        return 'SE'
    if isinstance(label, str) and 'AM' in label:
        return 'AM'
    return None


def _pair_kind_g2(label1, label2):
    """두 상 이름 → film_area_g2 의 쌍 ('SE_SE' · 'AM_SE' · 'AM_AM') · 모르는 상이면 None (호출자가 physics 모드에서 거부한다)."""
    c1, c2 = _phase_class(label1), _phase_class(label2)
    if c1 is None or c2 is None:
        return None
    return {('SE', 'SE'): 'SE_SE', ('AM', 'AM'): 'AM_AM'}.get((c1, c2), 'AM_SE')


def _sphere_segment_half(r_i, r_j, d, sk):
    """H12 bulk 반쪽 (C1-3 · 구 조각) — 중심 평면 ↔ 접촉 평면 사이 구 조각의 부피를 가진 균일 막대의 저항 h_i²/(σ_i·k·V_i).
    h_i = clip((d² + r_i² − r_j²)/(2d), 0, r_i) · V_i = π(r_i² h_i − h_i³/3) · h_i = 0 이면 0 (극한 h/(πr²) → 0)."""
    if d <= 0 or r_i <= 0:
        return 0.0
    h = min(max((d * d + r_i * r_i - r_j * r_j) / (2.0 * d), 0.0), r_i)
    if h <= 0:
        return 0.0
    vol = np.pi * (r_i * r_i * h - h ** 3 / 3.0)
    return (h * h) / (sk * vol) if vol > 0 else 0.0


def build_network(atoms_raw, contacts_raw, target_types, scale,
                  plate_z, box_x=0.05, box_y=0.05, boundary_factor=2.0,
                  mode='ionic', type_map=None, results_dir=None,
                  contact_mode='hertzian', psi_placement=PSI_PLACEMENT_DEFAULT,
                  area_rule=AREA_RULE_DEFAULT, hertz_constriction=HERTZ_CONSTRICTION_MAXWELL,
                  bulk_model=BULK_CYLINDER):
    # ⚠ `results_dir` 는 **읽히지 않는다** (2026-08-20 전수 감사 코드 하위 α).
    #   옛 docstring 은 "ionic 모드는 percolation_sets.json 으로 경계를 잡는다" 고 약속했지만
    #   본문 어디서도 그 파일을 열지 않는다 — 경계는 **항상 z-규칙**(아래 `boundary_factor`)
    #   이다.  호출부(`:977`·`:1135`)가 실값을 넘기고 있어 "쓰이는 것처럼" 보인다.
    #   수치 오염은 없다(계약 표류다).  인자를 지우면 호출부 두 곳이 깨지므로 남기되,
    #   **약속을 사실에 맞춘다** — 되살리려면 여기서 실제로 읽고 z-규칙과의 우선순위를
    #   명시할 것.
    """
    Build resistor network from DEM data.
    mode='ionic': SE-SE network only
    mode='electronic': AM-AM network only
    mode='thermal': ALL contacts (AM-AM, AM-SE, SE-SE)
    contact_mode='hertzian'  : use LIGGGHTS-reported contact_area directly (DEM-native)
    contact_mode='physics'   : use plastic-film area from δ/R* Tabor+volume model
                               (literature-anchored, 0 free params — see plastic_coverage.py)
    area_rule (★ 10-06 세대 2) : physics 면적 — 'physics_g2' (기본 · `film_area_g2` · µm + 쌍 · type_map 필수) · 'physics_g1'
                               (세대 1 재현 · 옛 sim 단위 경로 그대로 · 명시로만).  hertzian 모드에서도 진단 칸 A_physics 를 같은 규칙으로 낸다
                               (type_map 이 없거나 상을 모르면 None — 그 모드의 σ 에는 안 쓰인다).
    hertz_constriction · bulk_model (★ 10-06 C1-3) : Hertz 가지 — (maxwell · cylinder_half_d) = H0 기본 · (mikic_psi_multiply ·
                               sphere_segment) = H12 민감도.  짝으로만 · physics 모드는 H0 만 (그 밖 = ValueError).
    Returns nodes, edges, bottom/top boundary sets.
    """
    #  ★ 2026-08-19 (코팅 트랙 코드리뷰 A2) — 프로덕션이 실제로 어떤 mode 로 들어왔는지
    #    기록한다.  `mode == 'electronic'` 리터럴(:343)이 **한 번도 발화한 적 없다**는
    #    사실이 이 값 없이는 정적으로만 보이고 런타임으로 증명이 안 됐다.
    global LAST_BUILD_MODE
    LAST_BUILD_MODE = mode
    #  ⛔ **fail-closed** — 모르는 값이 조용히 legacy 로 떨어지면 S3 팔이 no-op 이 되고
    #    "돌렸다" 는 기록만 남는다 (규율 ⑤ 의 false-green).  거부한다.
    if psi_placement not in PSI_PLACEMENTS:
        raise ValueError(f'psi_placement 는 {PSI_PLACEMENTS} 중 하나여야 한다: {psi_placement!r}')
    #  ★ 10-06 세대 2 — 면적 규칙 · Hertz 팔도 같은 방식으로 거부한다 (모르는 값 · 짝 아닌 조합 · physics 모드의 H12).
    if area_rule not in AREA_RULES:
        raise ValueError(f'area_rule 은 {AREA_RULES} 중 하나여야 한다: {area_rule!r}')
    hertz_arm = HERTZ_ARMS.get((hertz_constriction, bulk_model))
    if hertz_arm is None:
        raise ValueError(f'(hertz_constriction, bulk_model) = ({hertz_constriction!r}, {bulk_model!r}) — 짝으로만 '
                         f'{sorted(HERTZ_ARMS)} (ψ 단독 H1 · bulk 단독은 받지 않는다 · C1-3)')
    if contact_mode == 'physics' and hertz_arm != 'H0':
        raise ValueError('H12 (ψ 곱 Hertz + 구 조각 bulk) 는 Hertz 민감도 팔이다 — physics 모드에는 쓰지 않는다')
    if contact_mode == 'physics' and area_rule == AREA_RULE_G2:
        if not type_map:
            raise ValueError("physics 면적 세대 2 (physics_g2) 는 상 쌍이 필요하다 — type_map 없음은 거부 (L1-03 · 쌍별 E*)")
        if _film_area_g2 is None:
            raise ValueError('plastic_coverage.film_area_g2 를 불러오지 못했다 — physics 세대 2 를 풀 수 없다 (세대 1 로 떨어지지 않는다)')
    h12 = (hertz_arm == 'H12')
    if mode == 'thermal':
        target_ids = list(atoms_raw.keys())
    else:
        target_ids = [aid for aid, a in atoms_raw.items() if a['type'] in target_types]

    if not target_ids:
        return None

    # Boundary detection: z-coordinate based (consistent with EIS measurement)
    #  ★ 2026-10-04 (τ 결정 16 ② 안 A) — 띠 선택을 `boundary_sets` 로 옮기고 쓴 규칙 · 띠 폭을 **기록**한다 (동작 중립).
    bottom_ids, top_ids, boundary_rule, boundary_band_frac = boundary_sets(
        atoms_raw, target_ids, plate_z, boundary_factor)

    # Determine SE types for thermal mode
    se_type_set = set()
    if type_map:
        se_type_set = {k for k, v in type_map.items() if v == 'SE'}

    # Build contact map (area + delta). Delta is required for physics contact_mode
    # so each edge can recompute A_plastic from overlap geometry.
    contact_map = {}  # pair → {'ca': Hertzian area, 'delta': overlap}
    for c in contacts_raw:
        id1, id2 = c['id1'], c['id2']
        if id1 in atoms_raw and id2 in atoms_raw:
            if mode == 'thermal':
                pair = (min(id1, id2), max(id1, id2))
                ca = c.get('contact_area', 0)
                delta_c = c.get('delta', 0)
                if ca > 0 or delta_c > 0:
                    contact_map[pair] = {'ca': ca, 'delta': delta_c}
            else:
                if atoms_raw[id1]['type'] in target_types and atoms_raw[id2]['type'] in target_types:
                    pair = (min(id1, id2), max(id1, id2))
                    ca = c.get('contact_area', 0)
                    delta_c = c.get('delta', 0)
                    if ca > 0 or delta_c > 0:
                        contact_map[pair] = {'ca': ca, 'delta': delta_c}

    # Build edges with physical resistances
    # All distances in μm, areas in μm², resistivity in Ω·μm
    # ρ = 1/σ, σ = 1.3e-3 S/cm = 1.3e-7 S/μm → ρ = 7.69e6 Ω·μm
    # But we normalize: set ρ=1, then σ_eff comes out as ratio to σ_bulk

    edges = []
    #  ★ 10-06 세대 2 기록 — physics 면적 결속 수 (그 망의 전 간선 · 진단) · 협착 0 의 두 부류 (활성 모드가 ψ 를 쓸 때만:
    #    clamp_zero = a ≥ r_min → ψ = 0 · floor_only = s < 1 인데 ψ ≤ 1e-4 → 동결 floor) · physics 면적을 못 낸 간선 수 (hertzian 진단 칸)
    area_bind, n_area_unavailable, n_clamp_zero, n_floor_only = {}, 0, 0, 0
    for pair, cdat in contact_map.items():
        id1, id2 = pair
        a1, a2 = atoms_raw[id1], atoms_raw[id2]
        ca_sim = cdat['ca']
        delta_sim = cdat['delta']

        # Hop distance (μm) with periodic boundary
        dx = abs(a1['x'] - a2['x'])
        dy = abs(a1['y'] - a2['y'])
        dz = a1['z'] - a2['z']
        dx = min(dx, box_x - dx)
        dy = min(dy, box_y - dy)
        d_ij = np.sqrt(dx**2 + dy**2 + dz**2) * scale  # μm

        # Particle radii (sim units → μm)
        r1_sim = a1['radius']
        r2_sim = a2['radius']
        r1 = r1_sim * scale
        r2 = r2_sim * scale

        # Hertzian area (LIGGGHTS-reported, sim→μm²)
        A_hertzian = ca_sim * scale**2  # μm²

        # Physics (plastic-film) area: Tabor+volume, literature-anchored
        # Compute in sim units then scale to μm²
        # 5-case decomposition (when components available):
        #   Lower bounds: A_hertzian (πR*δ), A_ligg (LIGGGHTS internal)
        #   Upper caps:   A_tabor (F/H), A_volume (V/h_min), A_geom (2πR_min²)
        #   Final:        A_physics = max(lower, min(caps))
        #  ★ 10-06 세대 2 (C2 ①–⑤) — 기본은 `film_area_g2` (µm + length_scale 1e6 · 쌍 · ligg = c_cpl[22] 원판 floor · 규칙 B).  위 5-case 는
        #    세대 1 (명시 area_rule='physics_g1') 의 설명이다 — 그 경로 (아래 elif) 는 한 글자도 안 바꿨다 (세대 1 재현 · 감사 ⑦f).
        A_components = None
        if area_rule == AREA_RULE_G2:
            R_star_sim = (r1_sim * r2_sim) / (r1_sim + r2_sim) if (r1_sim > 0 and r2_sim > 0) else 0.0
            delta_over_R = delta_sim / R_star_sim if (delta_sim > 0 and R_star_sim > 0) else 0.0
            lbl1 = type_map.get(a1['type'], '') if type_map else ''
            lbl2 = type_map.get(a2['type'], '') if type_map else ''
            gpair = _pair_kind_g2(lbl1, lbl2)
            gcomp = None
            if gpair is None or _film_area_g2 is None:
                if contact_mode == 'physics':
                    raise ValueError(f'physics_g2: 간선 ({id1}, {id2}) 의 상 쌍을 모른다 (type_map {lbl1!r} · {lbl2!r}) — '
                                     'SE · AM 이름이 있어야 한다 (거부 · L1-03)')
                A_physics, regime = None, 'unavailable_pair'          # hertzian 모드의 진단 칸만 — σ 에 안 쓰인다
            else:
                try:
                    A_physics, regime, gcomp = _film_area_g2(delta_sim * scale, r1, r2, pair=gpair, ligg_area=A_hertzian,
                                                             length_scale=G2_LENGTH_SCALE_UM, consumer='transport',
                                                             return_components=True)
                except (ValueError, TypeError) as _ge:
                    if contact_mode == 'physics':
                        raise ValueError(f'physics_g2: 간선 ({id1}, {id2}) — {_ge}') from _ge
                    A_physics, regime = None, 'unavailable_geometry'
            if A_physics is None:
                n_area_unavailable += 1
            else:
                A_components = {
                    'rule': AREA_RULE_G2, 'pair': gpair, 'binding': regime,
                    'A_disc_um2': gcomp['A_disc'], 'A_tabor_um2': gcomp['A_tabor'], 'A_volume_um2': gcomp['A_volume'],
                    'A_cap_um2': gcomp['A_cap'], 'A_final_um2': A_physics, 'V_lens_um3': gcomp['V_lens'],
                    'h_film_um': gcomp['h_film'], 'E_star_Pa': gcomp['E_star'],
                }
            area_bind[regime] = area_bind.get(regime, 0) + 1
        elif delta_sim > 0 and r1_sim > 0 and r2_sim > 0:
            R_star_sim = (r1_sim * r2_sim) / (r1_sim + r2_sim)
            R_min_sim = min(r1_sim, r2_sim)
            delta_over_R = delta_sim / R_star_sim if R_star_sim > 0 else 0.0
            if _film_area is not None:
                A_phys_sim, regime, comp = _film_area(
                    delta_sim, R_star_sim,
                    R_min=R_min_sim, ligg_area=ca_sim,
                    mode='physics', return_components=True)
                A_physics = A_phys_sim * scale**2  # μm²
                # Convert components to μm² (skip None entries)
                A_components = {
                    'A_hertzian_um2': comp['A_hertzian'] * scale**2,
                    'A_ligg_um2':     None if comp['A_ligg'] is None else comp['A_ligg'] * scale**2,
                    'A_tabor_um2':    None if comp['A_tabor'] is None else comp['A_tabor'] * scale**2,
                    'A_volume_um2':   None if comp['A_volume'] is None else comp['A_volume'] * scale**2,
                    'A_geom_um2':     None if comp['A_geom'] is None else comp['A_geom'] * scale**2,
                    'A_final_um2':    A_physics,
                    'binding':        comp['binding'],
                    # ── L1-01 · L1-02 계측 (2026-09-13).  ⛔ A_physics 는 **안 바꾼다** ──
                    #    cap_conflict = 하한 > 상한 (만족하는 A 가 없다)
                    #    V_lens_exact = 정확한 두 구 교집합 (legacy 는 얕으면 절반, 깊으면 음수)
                    'cap_conflict':   comp.get('cap_conflict'),
                    'A_lower_um2':    None if comp.get('A_lower') is None else comp['A_lower'] * scale**2,
                    'A_upper_um2':    None if comp.get('A_upper') is None else comp['A_upper'] * scale**2,
                    'V_overlap_legacy_um3': None if comp.get('V_overlap_legacy') is None
                                            else comp['V_overlap_legacy'] * scale**3,
                    'V_lens_exact_um3':     None if comp.get('V_lens_exact') is None
                                            else comp['V_lens_exact'] * scale**3,
                    'A_volume_exact_um2':   None if comp.get('A_volume_exact') is None
                                            else comp['A_volume_exact'] * scale**2,
                }
            else:
                A_physics = A_hertzian  # fallback if import failed
                regime = 'hertzian_fallback'
        else:
            delta_over_R = 0.0
            A_physics = A_hertzian
            regime = 'no_delta'
        if area_rule == AREA_RULE_G1:                                # 세대 1 결속 수 (진단 · 값 무관)
            _b1 = (A_components or {}).get('binding') or regime
            area_bind[_b1] = area_bind.get(_b1, 0) + 1

        # Select active area for this run
        A_contact = A_physics if contact_mode == 'physics' else A_hertzian
        a_contact = np.sqrt(A_contact / np.pi) if A_contact > 0 else 0.0

        # Thermal mode: material-specific conductivity weighting
        # k_AM ≈ 4.0 W/m·K, k_SE ≈ 0.7 W/m·K
        # AM-AM: weight=k_AM/k_SE, SE-SE: weight=1, AM-SE: harmonic mean
        if mode == 'thermal' and se_type_set:
            t1_is_se = a1['type'] in se_type_set
            t2_is_se = a2['type'] in se_type_set
            k_ratio = K_AM_THERMAL / K_SE_THERMAL  # ~5.7
            if not t1_is_se and not t2_is_se:
                # AM-AM: high thermal conductivity
                k_weight = k_ratio
            elif t1_is_se and t2_is_se:
                # SE-SE: baseline
                k_weight = 1.0
            else:
                # AM-SE: harmonic mean
                k_weight = 2 * k_ratio / (1 + k_ratio)
        else:
            k_weight = 1.0

        # Normalized resistances (ρ=1, scaled by k_weight for thermal):
        # R_bulk = d / (k_weight × σ_rel × π × r²)
        #
        # For ELECTRONIC mode, σ_rel applies the GB/crystallinity correction
        # (AM_P polycrystalline gets r-dependent GB reduction, AM_S single-crystal
        # stays at 1.0; GB-direction is Trevisanello-spirit, β/r0 corpus-fit — A1).
        # This bakes the crystallinity physics into the solver — the form's σ_S/σ_P
        # endpoint mix and NCM correction become redundant after refactor.
        # Per-particle σ for electronic mode (GB/crystallinity factor).
        # Detect electronic mode from target_types + type_map (mode parameter
        # is unreliable — caller may not set it correctly).  Electronic =
        # AM-only network (no SE in targets).  Ionic = SE-only.  Thermal = all.
        # sigma_AM_relative returns 1.0 for SE/non-AM particles, so applying
        # universally is safe for ionic mode (SE-SE: both σ_rel=1, no effect).
        # But for thermal we want to keep current behavior (no GB correction
        # for thermal — phonon GB effect has different β), so gate on mode.
        if mode == 'electronic' or (type_map and target_types and
                all('AM' in type_map.get(t, '') for t in target_types)
                and not any(type_map.get(t, '') == 'SE' for t in target_types)):
            t1_lbl = type_map.get(a1['type'], '') if type_map else ''
            t2_lbl = type_map.get(a2['type'], '') if type_map else ''
            sigma_rel_1 = sigma_AM_relative(r1, t1_lbl)
            sigma_rel_2 = sigma_AM_relative(r2, t2_lbl)
        else:
            sigma_rel_1 = 1.0
            sigma_rel_2 = 1.0
        if bulk_model == BULK_SPHERE_SEGMENT:
            #  ★ 10-06 H12 (C1-3) — 구 조각 bulk (중심 평면 ↔ 접촉 평면 · 반쪽마다 h_i²/(σ_i·k·V_i)) · Hertz 민감도 팔에서만
            R_bulk_1 = _sphere_segment_half(r1, r2, d_ij, sigma_rel_1 * k_weight)
            R_bulk_2 = _sphere_segment_half(r2, r1, d_ij, sigma_rel_2 * k_weight)
        else:
            R_bulk_1 = (d_ij / 2) / (sigma_rel_1 * k_weight * np.pi * r1**2) if r1 > 0 else 0
            R_bulk_2 = (d_ij / 2) / (sigma_rel_2 * k_weight * np.pi * r2**2) if r2 > 0 else 0
        R_bulk = R_bulk_1 + R_bulk_2

        # Contact resistance.
        #   Hertzian mode (point contact, a ≪ r):
        #     R_constriction = 1/(2a)   — Maxwell spreading (Holm 1967)
        #     Exact for point-contact-on-halfspace geometry.
        #   Physics mode (surface contact via Tabor + hemisphere caps):
        #     R_constriction = (1 - a/r_min)^1.5 / (2a)   — Mikic (1974)
        #     Rigorous correction for finite contact on a finite cylinder:
        #     reduces to Maxwell when a/r_min → 0, and vanishes as a → r_min
        #     (full contact, no constriction left, bulk alone dominates).
        #     Replaces the earlier phenomenological 'Maxwell + 2δ/A film'
        #     ansatz — same qualitative saturation behaviour but derived.
        r_min_real = min(r1, r2)  # μm (smaller sphere's radius)
        # For electronic mode: Holm constriction uses the LOWER-σ side
        # (bottleneck) — use minimum of two σ_rel values to be conservative
        # (electron path through constriction limited by lowest-σ region).
        sigma_rel_contact = min(sigma_rel_1, sigma_rel_2)
        R_Maxwell = 1.0 / (sigma_rel_contact * k_weight * 2 * a_contact) if a_contact > 0 else 1e12
        #  ★ 10-06 H12 (C1-3) — Hertz 면적 (c_cpl[22]) 위에서도 같은 ψ 곱셈식을 쓴다 (짝 인자 · 민감도 팔만).  H0 (기본) 은 아래 else = Maxwell 그대로.
        if (contact_mode == 'physics' or h12) and a_contact > 0 and r_min_real > 0:
            # Clamp a to r_min — our plastic cap 2πR_min² gives a > r_min, which
            # is geometrically impossible for a disk contact between spheres.
            a_eff = min(a_contact, r_min_real)
            psi = max(1.0 - a_eff / r_min_real, 0.0) ** 1.5
            if psi > 1e-4:
                if psi_placement == PSI_MULTIPLY or h12:          # H12 = 늘 곱셈 (psi_placement 은 physics 가지의 배치)
                    # ── S3 (계약 `docs/area_contract_20260913.md` §C · 원장 `L2-01`) ──
                    #   `R_c = ψ(a/b)/(2σa)` — ψ 를 **곱한다**.
                    #   자리: Yovanovich 1982 p.86 식 1-3 · 2005 리뷰(접촉 conductance 분모).
                    #   ★ 문헌 인용이 아니라 **계산으로 갈랐다** — 축대칭 flux-tube 유한체적
                    #     기준해 `scripts/constriction_reference.py` (`AREA-09` STEP 4):
                    #     기하평균 |ln 비| 가 `s ≤ .3` 에서 곱 **1.02491228** vs 역수 1.69510941 ·
                    #     `s > .3` 에서 곱 **1.18902836** vs 역수 **44.31250962** (R2-03 경계 정정판).
                    #     곱셈 우위는 10점 **각각에서** 유지된다.
                    #   ★ 이 줄 **위 :392 의 주석이 처음부터 곱셈식을 적고 있었다** — 코드가
                    #     자기 주석과 어긋난 것이고, 비는 `(1−s)^−3`, `s=0.9` 에서 1,620배다.
                    #   ★ **세대 2 기본** (1저자 개정 2026-10-06 · 근거 = 위 독립 기준해 · 계약 봉인 창 09-17 을
                    #     지나 등록 경로 대신 개정 — `docs/area_contract_20260913.md` 개정 노트).  아래 legacy 분모는
                    #     명시 `PSI_DIVIDE` 로만 (세대 1 · 옛 값 재현용).
                    R_constriction = psi / (sigma_rel_contact * k_weight * 2 * a_eff)
                else:
                    R_constriction = 1.0 / (sigma_rel_contact * k_weight * 2 * a_eff * psi)
            else:
                # Full contact limit: spreading vanishes, R_bulk carries it.
                #  ⚠ 세대 1 (명시 `PSI_DIVIDE`) 에서 이것은 극한이 아니라 **절벽**이다 (`L2-01`):
                #    전환점 s* = 0.99784556531 에서 R 이 5010.76059484 → 0 으로 떨어진다.
                #  ★ 세대 2 기본 (곱셈) 은 그 급락을 1/ψ*² ≈ 1e8 배 줄이지만 **작은 불연속은 남는다** — 좌극한이
                #    ψ_floor·R_Maxwell > 0 이고 그 다음이 0 이다 (동결된 유한 floor 1e-4 · AREA5-07 · 감사 ⑦h).
                #    ⛔ floor 자체는 계약 §C 가 **동결**했다 — 곱셈판에서도 건드리지 않는다
                #      (0 → 양수 복원은 **별도 축**이다).
                R_constriction = 0.0
                #  ★ 10-06 기록 — 두 부류 (SELF-28): a ≥ r_min (원판 상한 · 반올림 1e-12 안 포함) = clamp_zero · 그 밖 = floor_only
                if a_contact >= r_min_real * (1.0 - 1e-12):
                    n_clamp_zero += 1
                else:
                    n_floor_only += 1
        else:
            R_constriction = R_Maxwell
        # Legacy per-edge R_film field kept for backward compat with readers;
        # under Mikic it's folded into R_constriction so reported here as 0.
        R_film = 0.0

        edges.append({
            'id1': id1, 'id2': id2,
            'R_bulk': R_bulk,
            'R_constriction': R_constriction,
            'R_Maxwell': R_Maxwell,
            'R_film': R_film,
            'R_total': R_bulk + R_constriction,
            'd_ij': d_ij,
            'A_contact': A_contact,
            # Raw-dump fields (both modes carry both areas for comparison)
            'A_hertzian': A_hertzian,
            'A_physics':  A_physics,
            # 5-case Tabor/volume/geom decomposition (None when not in physics regime)
            'A_components': A_components,
            'delta':       delta_sim,
            'delta_over_R': delta_over_R,
            'regime':      regime,
            'r1': r1, 'r2': r2,
            'type1': a1['type'], 'type2': a2['type'],
        })

    return {
        'nodes': target_ids,
        'edges': edges,
        'bottom': bottom_ids,
        'top': top_ids,
        'plate_z': plate_z,
        'box_x': box_x,
        'box_y': box_y,
        'scale': scale,
        'contact_mode': contact_mode,
        #  ★ 어떤 ψ 배치로 지은 망인지 **망 자신이 들고 다닌다** (`L2-01`/S3).  라벨 없이
        #    두 세대의 σ 가 섞이면 사후에 복원할 방법이 없다 (계약 §4 "S2 와 S3 분리").
        'psi_placement': psi_placement,
        # Thermal is the multi-phase superset network (all AM+SE contacts),
        # so σ_eff/σ_bulk_SE can exceed 1 — the single-phase sigma_ratio>1.5
        # guard in solve_network does NOT apply to it (see the guard there).
        # Set by mode here; run_decomposition also forces it on for the
        # production thermal call (which leaves mode at its 'ionic' default).
        'is_thermal': (mode == 'thermal'),
        # Resistance-model tag:
        #   'maxwell' (point-contact only) for Hertzian
        #   'mikic'   (Mikic 1974 constriction w/ finite-cylinder correction)
        #              for Physics. Vanishes correctly at full-contact limit.
        #  ★ 10-06 H12 — Hertz 민감도 팔도 ψ 곱셈 협착이라 'mikic' (H0 는 'maxwell' 그대로)
        'resistance_model': ('mikic' if (contact_mode == 'physics' or h12)
                             else 'maxwell'),
        #  ★ 10-06 세대 2 기록 (C1 · C2 — 결과 · τ 인계 열의 세대 표기 원천)
        'area_rule_physics': area_rule,
        'area_rule': (area_rule if contact_mode == 'physics' else AREA_RULE_HERTZ),
        'area_binding_counts_physics': dict(sorted(area_bind.items())),
        'n_area_physics_unavailable': n_area_unavailable,
        'n_clamp_zero': n_clamp_zero,
        'n_floor_only': n_floor_only,
        'hertz_constriction': hertz_constriction,
        'bulk_model': bulk_model,
        'hertz_arm': hertz_arm,
        # ★★ 2026-08-19 — bottom ∩ top.  같은 노드가 양쪽 경계에 속하면 Kirchhoff 계가
        #   **퇴화**해 (한 노드에 1 V 와 0 V 를 동시에 강제) σ 가 조용히 None 으로 나온다.
        #   실사고: 얇은 고압 침대(P600, AM z-범위 22.1 µm)에서 `boundary_factor=2.0` 의
        #   두 밴드(각 2·r_max ≈ 12 µm)가 겹쳐 입자 1개가 양쪽에 속했고, 퍼콜은 0.9951 인데
        #   `sigma_full_status='not_computed'` 가 나왔다 — 원인이 로그 어디에도 없었다.
        #   ⇒ **발동 조건**: 침대 두께 < 4·r_max (여기선 ≈24 µm).  생산 침대는 30 µm+ 라
        #   여태 안 물렸지만, 고압·박막 케이스는 물린다.  숫자를 남겨 조용한 실패를 막는다.
        'n_boundary_overlap': len(set(bottom_ids) & set(top_ids)),
        #  ★ 2026-10-04 (안 A) — 어느 띠 규칙을 썼나 · 띠 폭 / 판 간격 (`boundary_sets`).  L0 이 아니면 인계 G1 이 값을 막는다.
        'boundary_rule': boundary_rule,
        'boundary_band_frac': boundary_band_frac,
    }


_TINY = sys.float_info.min        # 보존 · 내부 잔차 분모의 바닥 (두 전류 · ‖b‖ 가 모두 0 일 때 0/0 을 피한다)
#: ★ 10-06 밤 G2R-03 — 결과 레코드에 싣는 증서 키 (solve_info 와 같은 이름 · 같은 모양) · 단 기록 키.
#:   ★ 10-06 밤 G2RR-02 — 뒤의 넷 (branch · delta_V · geometry · g_to_q) = 결합 정보 중 풀이가 아는 것 (아래 CERT_BINDING_FIELDS 절).
SOLVE_CERTIFICATE_FIELDS = ('electrode_model', 'status', 'reason', 'method', 'n_free', 'n_fixed', 'n_floating', 'n_zero_resistance',
                            'I_bottom', 'I_top', 'conservation_rel', 'residual_rel', 'conservation_rel_max', 'residual_rel_max', 'attempts',
                            'branch', 'delta_V', 'geometry', 'g_to_q')
SOLVE_ATTEMPT_FIELDS = ('method', 'outcome', 'krylov_info', 'refine_passes', 'I_bottom', 'I_top', 'conservation_rel', 'residual_rel',
                        'error')
#: 결과 레코드의 가지별 증서 키 (σ 키 꼬리와 같다 — full · bulk_net (CONTACT_FREE) · constr_net (CONSTRICTION_ONLY)).
SOLVE_CERTIFICATE_KEYS = ('solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net')
#  ★ 10-06 밤 G2RR-02 (Codex 세대 2 재검증 §3 · §7-2 · 1저자 비준 *"권고대로"*) — 증서 ↔ 가지 · 역할 · 발행값 결합.
#     옛 증서는 자기 안의 전류 보존 · 잔차 · 방법만 말했다 (`certificate_problem`) → 같은 실행의 CF 증서 · H12 FULL 증서를 주 Hertz FULL 자리에 붙여도
#     게시 · τ 가 통과했다 (Codex probes/acceptance.py — CF 증서 I_bottom = FULL 의 9.80 배 · H12 1.28 배 · 발행 q 0.00400538 그대로 · τ OK).
#     이제 증서마다 결합 정보를 싣는다 (기록만 — 해 · σ · 상태 · 증서 수치는 비트 동일 · test_network_solve_certificate G4):
#       branch          — solve_network mode (full · bulk_only · constriction_only) = 그 증서가 푼 가지
#       channel         — run_decomposition 의 망 (ionic · electronic · thermal)
#       role            — H0 · H12 (Hertz 짝 팔 — HERTZ_ARMS) · physics (contact_mode physics)
#       contact_mode    — hertzian · physics
#       delta_V         — V(바닥 띠) − V(위 띠) = 1 (정확 Dirichlet 전극 · G = I_bottom/ΔV)
#       geometry        — 그 풀이가 σ 환산에 쓴 기하 {plate_z, box_x, box_y, scale} (봉인된 기하 — 한 실행의 모든 증서가 같다)
#       g_to_q          — G → 무차원 σ_ratio 변환 인자 = T_um / A_um2 = (plate_z·scale) / (box_x·box_y·scale²)
#       sigma_bulk_S_cm — 그 망의 mS/cm 열을 만든 σ (이온 = sigma_grain_S_cm · 전자 SIGMA_AM_ELECTRONIC · 열 K_SE_THERMAL)
#     발행값 연결: σ_ratio = round(I_bottom/ΔV × T/A, 8) · σ_dim = round(σ_ratio* × σ_bulk × 1000, 6) (★ 같은 식 · 같은 순서 — 소비자가 저장 반올림
#     반폭 안으로 재구성한다).  수용 검사 = `tau_flux.certificate_binding_problems` (게시 ⑨ · 승격 전 기록 검사 · τ 소비자 · 인계가 같은 함수 ·
#     가지별 정책 `tau_flux.CERT_BRANCH_POLICY` — 숫자를 싣는 CF · 협착-only 진단도 같은 검사 · 해 없는 가지는 증서를 요구하지 않는다).
CERT_DELTA_V = 1.0
CERT_BRANCHES = ('full', 'bulk_only', 'constriction_only')
CERT_CHANNELS = ('ionic', 'electronic', 'thermal')
CERT_ROLE_PHYSICS = 'physics'
CERT_ROLES = ('H0', 'H12', CERT_ROLE_PHYSICS)
CERT_GEOMETRY_FIELDS = ('plate_z', 'box_x', 'box_y', 'scale')
CERT_BINDING_FIELDS = ('branch', 'channel', 'role', 'contact_mode', 'delta_V', 'geometry', 'g_to_q', 'sigma_bulk_S_cm')


def _cert_num(v):
    """유한 실수 → float · 그 밖 (None · bool · 문자열 · NaN · ±inf) → None."""
    if isinstance(v, bool) or not isinstance(v, (int, float, np.integer, np.floating)):
        return None
    f = float(v)
    return f if np.isfinite(f) else None


def _json_val(v):
    """증서 값의 JSON 안전형 — numpy 수 → 파이썬 수 · 비유한 실수 → None (표준 JSON 에 NaN · Infinity 를 쓰지 않는다) · 문자열 그대로."""
    if v is None or isinstance(v, (bool, str)):
        return v
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        return _cert_num(v)
    return str(v)


def solve_certificate(info, binding=None):
    """`network_data['solve_info'][mode]` → 결과 레코드에 싣는 증서 (dict · JSON 안전) | None.  같은 키라 `certificate_problem` 이 그대로 읽는다.
    ★ 10-06 밤 G2RR-02 — binding = run_decomposition 이 아는 결합 정보 (channel · role · contact_mode · sigma_bulk_S_cm) — 풀이가 아는 넷 (branch ·
    delta_V · geometry · g_to_q) 은 solve_info 에서 온다 (CERT_BINDING_FIELDS 절)."""
    if not isinstance(info, dict):
        return None
    out = {k: _json_val(info.get(k)) for k in SOLVE_CERTIFICATE_FIELDS if k not in ('attempts', 'geometry')}
    _geo = info.get('geometry')
    out['geometry'] = {k: _json_val(_geo.get(k)) for k in CERT_GEOMETRY_FIELDS} if isinstance(_geo, dict) else None
    out['attempts'] = [{k: _json_val(a.get(k)) for k in SOLVE_ATTEMPT_FIELDS}
                       for a in (info.get('attempts') or []) if isinstance(a, dict)]
    if isinstance(binding, dict):
        out.update({k: _json_val(v) for k, v in binding.items()})
    return out


def certificate_problem(cert):
    """수치 증서 → None (게시할 수 있는 해) | 사유 (문자열).  ★ 10-06 밤 G2R-03 — 순수 함수 (기록만 본다 · 풀이 · 파일 · 전역 상태 없음).

    cert = `solve_network` 의 `network_data['solve_info'][mode]` 또는 결과 레코드의 `solve_certificate_<가지>` (같은 모양).
    통과 = 값이 게시되는 풀이만: status ∈ ('computed', 'model_over_conduction') · method ∈ DIRICHLET_METHODS · I_bottom 유한 양수 (= G · ΔV 1) ·
      I_top 유한 · 보존 잔차를 두 전류에서 **다시 재서** 기록값과 같고 ≤ DIRICHLET_CONSERVATION_REL_MAX · residual_rel 유한 · 0 이상 ·
      ≤ DIRICHLET_RESIDUAL_REL_MAX.
    허용치는 기록된 값이 아니라 이 모듈의 상수다 (정책은 코드가 정한다).  비관통 · 경계 겹침 · 0 저항 · 증서 실패 같은 비게시 상태는 사유를 돌려준다 —
    게시 관문 · 인계 재독이 **계산된 σ 마다** 부르는 자리 (그 배선은 이 함수 밖)."""
    if not isinstance(cert, dict):
        return f'증서 없음 ({type(cert).__name__})'
    st = cert.get('status')
    if st not in ('computed', MODEL_OVER_CONDUCTION):
        return f'풀이 상태 {st!r} (사유 {cert.get("reason")!r}) — 게시할 해가 없다'
    m = cert.get('method')
    if m not in DIRICHLET_METHODS:
        return f'모르는 풀이 방법 {m!r} (DIRICHLET_METHODS 밖)'
    ib, it = _cert_num(cert.get('I_bottom')), _cert_num(cert.get('I_top'))
    if ib is None or it is None:
        return f'전극 전류 결손 · 비유한 (I_bottom {cert.get("I_bottom")!r} · I_top {cert.get("I_top")!r})'
    if not ib > 0:
        return f'I_bottom {ib!r} ≤ 0 — G (ΔV 1) 가 양수가 아니다'
    cons = abs(ib + it) / max(abs(ib), abs(it), _TINY)
    rec = _cert_num(cert.get('conservation_rel'))
    if rec is None or abs(rec - cons) > 1e-12 + 1e-9 * cons:
        return f'보존 잔차 기록 {cert.get("conservation_rel")!r} ≠ 두 전류에서 다시 잰 {cons!r}'
    if cons > DIRICHLET_CONSERVATION_REL_MAX:
        return (f'전류 보존 실패 — |I_b + I_t| / max = {cons:.3g} > {DIRICHLET_CONSERVATION_REL_MAX:g} '
                f'(I_bottom {ib!r} · I_top {it!r})')
    res = _cert_num(cert.get('residual_rel'))
    if res is None or res < 0:
        return f'내부 잔차 결손 · 비유한 · 음수 ({cert.get("residual_rel")!r})'
    if res > DIRICHLET_RESIDUAL_REL_MAX:
        return f'내부 잔차 {res:.3g} > {DIRICHLET_RESIDUAL_REL_MAX:g} — 해가 그 선형계를 풀지 않았다'
    return None


def solve_network(network_data, mode='full', return_field=False):
    """
    Solve resistor network for effective conductance.

    mode: 'full' (R_bulk + R_constriction),
          'bulk_only' (R_bulk, R_constriction=0),
          'constriction_only' (R_constriction, R_bulk=0)
    return_field: if True, also return per-node voltages and per-edge currents
                  (used by dump_network_raw for reviewer-auditable output).

    ★ 10-06 세대 2 전극 (`L2-05` · C1-1 · 1저자 비준) — **정확 Dirichlet**: 관통 성분의 바닥 띠 B 노드 V = 1 · 위 띠 T 노드 V = 0 을 고정하고
      자유 노드만 푼다 (L_ff·x = −L_fB·1) · G = Σ_{b∈B} (L·V)_b (ΔV = 1).  옛 가상 전원 · 싱크 g_b = max(100·Σg/n_el, 10·g_max, 1e-6) 는 지웠다 —
      g_b 가 **모든 간선**에서 나와 전류 0 인 막다른 가지가 σ 를 바꿨다 (Codex 반례 +4.0 %).  세대 1 σ 재현 = git 이력의 옛 모듈.
      · B ∩ T ≠ ∅ → (None, None) · 사유 `boundary_overlap` (한 노드에 1 과 0 을 동시에 강제할 수 없다)
      · ★ 10-06 밤 GEN2-01 — 협착-only 에서 관통 간선에 R_c = 0 이 있으면 (None, None) · 사유 `zero_resistance_requires_contraction` (지우면 단락이
        개방이 된다 · 그 가지만 · FULL · CF 는 그대로)
      · 자유 노드 ≤ DIRICHLET_DIRECT_MAX_FREE (30,000) → spsolve · 그 위 → CG (rtol 1e-10 · atol 0 · SciPy < 1.12 는 tol)
      · ★ 10-06 밤 G2R-03 — 해마다 **수치 증서** (보존 잔차 ≤ DIRICHLET_CONSERVATION_REL_MAX · 내부 잔차 ≤ DIRICHLET_RESIDUAL_REL_MAX · 0 < G ≤ 1.1·Σg)
        를 넘어야 채택한다.  첫 단이 넘으면 해 그대로 (오늘과 비트 동일).  못 넘으면 (또는 첫 단 CG 미수렴) 사다리: 큰 망 = 직접해 (spsolve_fallback ·
        자유 ≤ DIRICHLET_FALLBACK_DIRECT_MAX_FREE) → cg+jacobi → gmres+ilu · 작은 망 = cg+jacobi → gmres+ilu (Krylov 단은 잔차 보정).  어느 단도
        증서를 못 넘으면 (None, None) · 상태 not_computed · 사유 `current_conservation_failed` (해를 낸 단이 없으면 solve_failed).
        ★ 첫 단 예외 (spsolve · cg **둘 다**) = solve_failed 그대로 — 사다리를 타지 않는다 (Codex 재검증 Q3 · 의도 = 입력 퇴화 · 실행 환경 문제를
        다른 방법의 해로 덮지 않는 안전한 거부 · 가용성 한계 = 일시적 자원 실패도 값 없음 → 재실행 · 모듈 머리 사다리 절).  둘째 단부터의 예외는
        기록하고 다음 단 · 직접해 상한 250,000 은 메모리 보증이 아니다 (자원 실패 = 그 단 예외 · 끝까지 못 넘으면 값 없음).
      · 어느 고정 노드와도 (R > 0 간선으로) 이어지지 않은 자유 노드 = 떠 있는 섬 — 풀이에서 빼고 V = 0 (전류 0 · solve_info n_floating)
      · 가드: 열 = 병렬 상한 · 단상 σ_ratio > 1.5 = **FULL 만** 거부 (★ C1-5 — CF · 협착-only 의 q > 1.5 = 모형 과전도: 값 유지 + 상태
        model_over_conduction)
    기록: network_data['solve_info'][mode] = {electrode_model, status, reason, method, n_free, n_fixed, n_floating, n_zero_resistance,
          I_bottom, I_top, conservation_rel, residual_rel, conservation_rel_max, residual_rel_max, attempts} — 증서 판정 = `certificate_problem`.
          ★ 10-06 밤 G2RR-02 — + branch (= mode) · delta_V (1) · geometry {plate_z, box_x, box_y, scale} · g_to_q (T_um/A_um2) — 풀이 앞에서 싣는다
          (해 무관 · 결합 정보 절 CERT_BINDING_FIELDS).

    Returns:
        G_eff: effective conductance (normalized, ρ=1)
        sigma_ratio: σ_eff / σ_bulk
        field (optional): {'node_V': {id: V}, 'edge_records': [{...}], 'V_source': 1.0 (호환 — 바닥 띠 전위), …}
    """
    nodes = network_data['nodes']
    edges = network_data['edges']
    bottom = network_data['bottom']
    top = network_data['top']
    scale = network_data['scale']
    plate_z = network_data['plate_z']
    box_x = network_data['box_x']
    box_y = network_data['box_y']
    info = {'electrode_model': ELECTRODE_DIRICHLET, 'status': None, 'reason': None, 'method': None,
            'n_free': None, 'n_fixed': None, 'n_floating': 0, 'n_zero_resistance': None, 'I_bottom': None, 'I_top': None,
            'conservation_rel': None, 'residual_rel': None,                                    # ★ G2R-03 증서 (채택한 해)
            'conservation_rel_max': DIRICHLET_CONSERVATION_REL_MAX, 'residual_rel_max': DIRICHLET_RESIDUAL_REL_MAX,
            'attempts': []}
    #  ★ 10-06 밤 G2RR-02 — 결합 정보 (가지 · ΔV · 기하 · G→q) 를 풀이 **앞**에서 싣는다 — 해 · σ 와 무관 (비관통 · 거부 가지의 증서도 같은 결합을 든다).
    #    g_to_q = 아래 σ 환산의 T_um / A_um2 와 같은 식 — 그 줄 (sigma_ratio = G_eff * T_um / A_um2) 은 건드리지 않는다 (σ 비트 동일).
    try:
        _g2q = (plate_z * scale) / (box_x * box_y * scale**2)
    except (TypeError, ZeroDivisionError, OverflowError):
        _g2q = None
    info.update(branch=mode, delta_V=CERT_DELTA_V, g_to_q=_g2q,
                geometry={'plate_z': plate_z, 'box_x': box_x, 'box_y': box_y, 'scale': scale})
    if isinstance(network_data, dict):
        network_data.setdefault('solve_info', {})[mode] = info

    def _none(status, reason):
        info.update(status=status, reason=reason)
        return (None, None, None) if return_field else (None, None)

    if not bottom or not top or not edges:
        return _none('no_input', 'empty boundary or edge set')

    # Build networkx graph to find percolating component
    import networkx as nx
    G_nx = nx.Graph()
    for e in edges:
        G_nx.add_edge(e['id1'], e['id2'])

    # Find components that connect bottom to top
    perc_nodes = set()
    for comp in nx.connected_components(G_nx):
        has_bot = len(comp & bottom) > 0
        has_top = len(comp & top) > 0
        if has_bot and has_top:
            perc_nodes |= comp

    if not perc_nodes:
        # Diagnostic: WHY did percolation fail?
        n_comp = nx.number_connected_components(G_nx)
        comp_sizes = sorted(
            (len(c) for c in nx.connected_components(G_nx)),
            reverse=True)[:5]
        reaches_bot = sum(1 for c in nx.connected_components(G_nx)
                         if len(c & bottom) > 0)
        reaches_top = sum(1 for c in nx.connected_components(G_nx)
                         if len(c & top) > 0)
        print(f"  No percolating component. DIAGNOSTIC:")
        print(f"    n_target_nodes={len(nodes)}, n_graph_nodes={G_nx.number_of_nodes()}, n_edges={G_nx.number_of_edges()}")
        print(f"    bottom={len(bottom)}, top={len(top)}  (plate_z={plate_z:.4f})")
        print(f"    n_components={n_comp}, top-5 sizes={comp_sizes}")
        print(f"    components reaching bottom={reaches_bot}, top={reaches_top} (need overlap for percolation)")
        return _none('no_through', NO_THROUGH_REASON)

    # Filter to percolating nodes only
    perc_bottom = bottom & perc_nodes
    perc_top = top & perc_nodes
    if perc_bottom & perc_top:
        print(f"  ⚠ 경계 겹침 B ∩ T = {len(perc_bottom & perc_top)} 노드 — 정확 Dirichlet 이 풀 수 없다 (boundary_overlap · 풀지 않는다)")
        return _none('not_computed', BOUNDARY_OVERLAP_REASON)
    perc_edges = [e for e in edges if e['id1'] in perc_nodes and e['id2'] in perc_nodes]

    print(f"  Percolating component: {len(perc_nodes)} nodes, {len(perc_edges)} edges")

    def _edge_R(e):
        if mode == 'full':
            return e['R_total']
        if mode == 'bulk_only':
            return e['R_bulk'] if e['R_bulk'] > 0 else 1e-12
        if mode == 'constriction_only':
            return e['R_constriction']
        return e['R_total']

    #  ★ 10-06 밤 GEN2-01 — 협착-only 가지의 관통 간선에 R_c = 0 (ψ floor · clamp) 이 있으면 풀지 않는다.  아래 조립은 R ≤ 0 간선을 L 에서 빼므로
    #    단락이 개방이 된다 = 다른 회로 (`ZERO_RESISTANCE_REASON` 의 주석).  관통 밖 간선은 G 에 무관하다 (세지 않는다).
    if mode == 'constriction_only':
        n_zero = sum(1 for e in perc_edges if _edge_R(e) <= 0)
        info['n_zero_resistance'] = int(n_zero)
        if n_zero:
            print(f"  ⚠ 협착-only: 관통 간선 {n_zero} 개가 R_c = 0 (ψ floor · clamp) — 빼면 단락이 개방이 된다 · 수축 전에는 값 없음 "
                  f"({ZERO_RESISTANCE_REASON})")
            return _none('not_computed', ZERO_RESISTANCE_REASON)

    # Node index mapping (percolating only) — 가상 전원 · 싱크 없음 (L2-05)
    all_ids = list(perc_nodes)
    id_to_idx = {nid: i for i, nid in enumerate(all_ids)}
    N = len(all_ids)
    row, col, val = [], [], []
    sum_g_check = 0.0
    for e in perc_edges:
        R = _edge_R(e)
        if R and R > 0:
            g = 1.0 / R
            i, j = id_to_idx[e['id1']], id_to_idx[e['id2']]
            row.extend([i, j, i, j])
            col.extend([i, j, j, i])
            val.extend([g, g, -g, -g])
            sum_g_check += g
    L = sparse.csr_matrix((val, (row, col)), shape=(N, N))
    L.eliminate_zeros()                                   # 자기쌍 간선의 상쇄 0 — 연결성 판정이 저장된 0 을 간선으로 읽지 않게

    # Dirichlet 고정 — 바닥 띠 1 · 위 띠 0
    V = np.zeros(N)
    fixed = np.zeros(N, dtype=bool)
    for bid in perc_bottom:
        k = id_to_idx[bid]
        fixed[k], V[k] = True, 1.0
    for tid in perc_top:
        fixed[id_to_idx[tid]] = True
    #  떠 있는 섬 — R > 0 간선만의 그래프에서 고정 노드와 이어지지 않은 자유 노드 (협착-only 의 R_c = 0 간선 등).  전위가 정의되지 않으므로 풀이에서 빼고
    #  V = 0 으로 둔다 (그 노드에 닿는 간선은 g = 0 이거나 같은 섬 안이라 전류 0).
    from scipy.sparse.csgraph import connected_components as _cc
    _nlab, _lab = _cc(L, directed=False)
    anchored = np.zeros(_nlab, dtype=bool)
    anchored[np.unique(_lab[fixed])] = True
    floating = (~fixed) & (~anchored[_lab])
    free = np.flatnonzero((~fixed) & (~floating))
    fx = np.flatnonzero(fixed)
    n_nodes = len(free)          # ★ 자유 노드 수 (Dirichlet 고정 · 떠 있는 섬 제외) — 아래 문턱 줄은 measure_rho 의 CG 강제 치환 앵커 (글자 그대로 유지)
    info.update(n_free=int(n_nodes), n_fixed=int(len(fx)), n_floating=int(floating.sum()))

    def _cg(A, b, M=None, maxiter=20000):
        kw = {'maxiter': maxiter} if M is None else {'maxiter': maxiter, 'M': M}
        try:
            return cg(A, b, rtol=DIRICHLET_CG_RTOL, atol=0.0, **kw)
        except TypeError:                                   # SciPy < 1.12 — rtol 키워드가 없다 (tol 이 상대 허용오차)
            return cg(A, b, tol=DIRICHLET_CG_RTOL, atol=0.0, **kw)

    def _gmres(A, b, M):
        kw = {'restart': 50, 'maxiter': max(1, DIRICHLET_KRYLOV_MAXITER // 50), 'M': M}
        try:
            return gmres(A, b, rtol=DIRICHLET_CG_RTOL, atol=0.0, **kw)
        except TypeError:                                   # SciPy < 1.12 — rtol 키워드가 없다 (tol 이 상대 허용오차)
            return gmres(A, b, tol=DIRICHLET_CG_RTOL, atol=0.0, **kw)

    def _direct(A, b):
        x_ = spsolve(A.tocsc(), b)
        return np.atleast_1d(np.asarray(x_, dtype=float))

    bot_idx = np.array(sorted(id_to_idx[b] for b in perc_bottom), dtype=int)
    top_idx = np.array(sorted(id_to_idx[t] for t in perc_top), dtype=int)

    def _currents(Vv):
        """(바닥 띠에서 나가는 전류, 위 띠로 나가는 전류) — (L·V) 를 띠마다 더한다 (보존이면 둘의 합 = 0)."""
        Iv = L @ Vv
        return float(Iv[bot_idx].sum()), float(Iv[top_idx].sum())

    L_ff = rhs = None
    if n_nodes > 0:
        L_ff = L[free][:, free].tocsr()
        rhs = -(L[free][:, fx] @ V[fx])
    rhs_norm = float(np.linalg.norm(rhs)) if rhs is not None else 0.0

    #  ── ★ 10-06 밤 G2R-03 — 증서 · 사다리 (식 · 허용치 = 모듈 머리 DIRICHLET_CONSERVATION_REL_MAX 절) ──
    def _assess(x_):
        """자유 노드 해 x (자유 노드가 없으면 None) → (V, I_bot, I_top, 보존 잔차, 내부 잔차) — 단마다 같은 식."""
        Vv = V.copy()
        res = 0.0
        if x_ is not None:
            Vv[free] = x_
            res = float(np.linalg.norm(L_ff @ x_ - rhs)) / max(rhs_norm, _TINY)
        ib, it = _currents(Vv)
        return Vv, ib, it, abs(ib + it) / max(abs(ib), abs(it), _TINY), res

    def _certified(a_):
        cons_, res_ = a_[3], a_[4]
        return bool(np.isfinite(cons_) and cons_ <= DIRICHLET_CONSERVATION_REL_MAX
                    and np.isfinite(res_) and res_ <= DIRICHLET_RESIDUAL_REL_MAX)

    def _krylov(name):
        """사다리 Krylov 단 — 잔차 보정: x = 0 에서 A·δ = r (r = b − A·x) 를 그때 잔차 상대 기준으로 풀어 더한다 (증서를 넘으면 멈춘다).
        cg+jacobi = 대각 (SPD) 전처리 CG · gmres+ilu = ILU 전처리 GMRES (ILU 는 SPD 보장이 없어 CG 에 넣지 않는다).
        → (x, 마지막 Krylov info, 보정 횟수) — info ≠ 0 이면 그 회의 δ 는 더하지 않는다 (호출자가 미수렴으로 본다)."""
        if name == 'cg+jacobi':
            d = L_ff.diagonal()
            if not (np.all(np.isfinite(d)) and np.all(d > 0)):
                raise ValueError('Jacobi 전처리 — 대각이 유한 양수가 아니다')
            Mj = sparse.diags(1.0 / d)

            def step(r_):
                return _cg(L_ff, r_, M=Mj, maxiter=DIRICHLET_KRYLOV_MAXITER)
        else:
            ilu = spilu(L_ff.tocsc(), drop_tol=1e-4, fill_factor=10)
            Mi = LinearOperator(L_ff.shape, ilu.solve)

            def step(r_):
                return _gmres(L_ff, r_, Mi)
        x_ = np.zeros(L_ff.shape[0])
        kinfo, passes = 0, 0
        for passes in range(1, DIRICHLET_REFINE_PASSES + 1):
            dx, kinfo = step(rhs - L_ff @ x_)
            kinfo = int(kinfo)
            if kinfo != 0 or not np.all(np.isfinite(dx)):
                break
            x_ = x_ + dx
            if _certified(_assess(x_)):
                break
        return x_, kinfo, passes

    if n_nodes == 0:
        rungs = ['none_free']
    else:
        if n_nodes > 30000:
            print(f"  Large network: {n_nodes} free nodes — CG (rtol {DIRICHLET_CG_RTOL:g}) first...")
            rungs = (['cg'] + (['spsolve_fallback'] if n_nodes <= DIRICHLET_FALLBACK_DIRECT_MAX_FREE else [])
                     + ['cg+jacobi', 'gmres+ilu'])
        else:
            rungs = ['spsolve', 'cg+jacobi', 'gmres+ilu']
    attempts = info['attempts']
    adopted = None
    for k, name in enumerate(rungs):
        att = dict.fromkeys(SOLVE_ATTEMPT_FIELDS)
        att['method'] = name
        attempts.append(att)
        x = None
        if name != 'none_free':
            try:
                if name in ('spsolve', 'spsolve_fallback'):
                    x = _direct(L_ff, rhs)
                elif name == 'cg':
                    x, cg_info = _cg(L_ff, rhs)
                    att['krylov_info'] = int(cg_info)
                else:
                    x, k_info, n_pass = _krylov(name)
                    att.update(krylov_info=k_info, refine_passes=n_pass)
            except Exception as e:                                         # noqa: BLE001 — 단의 실패를 기록하고 다음 단
                att.update(outcome='exception', error=f'{type(e).__name__}: {e}'[:200])
                #  첫 단 (spsolve · cg 둘 다) 예외 = 풀이 실패 (오늘과 같다 · 사다리 아님) — ★ Codex 재검증 Q3: 의도된 안전한 거부 (입력 퇴화 · 실행 환경
                #  문제를 다른 방법의 해로 덮지 않는다) · 가용성 한계 = 일시적 자원 실패도 그 가지 값 없음 (재실행) — 모듈 머리 사다리 절
                if k == 0:
                    print(f"  Network solve failed: {e}")
                    info['method'] = name
                    return _none('solve_failed', SOLVE_FAILED_REASON)
                print(f"  ⚠ 사다리 {name}: 예외 {type(e).__name__}: {e} — 다음 단")
                continue
            if att['krylov_info'] not in (None, 0) or not np.all(np.isfinite(x)):
                att['outcome'] = 'not_converged'
                print(f"  ⚠ {name}: 수렴하지 않았다 (info={att['krylov_info']}) — 다음 단")
                continue
        a = _assess(x)
        Vv, ib, it, cons, res = a
        att.update(I_bottom=ib, I_top=it, conservation_rel=cons, residual_rel=res)
        if not _certified(a):
            att['outcome'] = 'certificate_failed'
            print(f"  ⚠ {name}: 증서 실패 — 보존 잔차 {cons:.3g} · 내부 잔차 {res:.3g} (허용 {DIRICHLET_CONSERVATION_REL_MAX:g} · "
                  f"{DIRICHLET_RESIDUAL_REL_MAX:g}) · I_bottom {ib!r} · I_top {it!r} — 다음 단")
            continue
        if not (np.isfinite(ib) and 0 < ib <= sum_g_check * 1.1):        # G ≤ 0 · G > 1.1·Σg (모든 간선 병렬 상한) = 수치 실패
            att['outcome'] = 'parallel_bound'
            print(f"  ⚠ {name}: G_eff={ib!r} — 0 < G ≤ 1.1·Σg={sum_g_check:.3e} 밖 (수치 실패) — 다음 단")
            continue
        att['outcome'] = 'pass'
        adopted = (name, Vv, ib, it, cons, res)
        break
    if adopted is None:
        info['method'] = attempts[-1]['method'] if attempts else None
        if any(a_['outcome'] == 'certificate_failed' for a_ in attempts):
            print(f"  ⚠ 풀이 증서 실패 — 단 {[a_['method'] for a_ in attempts]} 모두 보존 · 내부 잔차 허용치를 못 넘었다 → 값 없음 "
                  f"({CURRENT_CONSERVATION_FAILED_REASON})")
            return _none('not_computed', CURRENT_CONSERVATION_FAILED_REASON)
        print(f"  Network solve failed: 증서를 낼 해가 없다 {[(a_['method'], a_['outcome']) for a_ in attempts]}")
        return _none('solve_failed', SOLVE_FAILED_REASON)
    solve_method, V, I_bot, I_top, cons, res = adopted
    info.update(method=solve_method, I_bottom=I_bot, I_top=I_top, conservation_rel=cons, residual_rel=res)
    print(f"  Solve: {solve_method}")
    G_eff = I_bot                                    # ΔV = 1 (바닥 1 · 위 0)

    if os.environ.get('NETWORK_DEBUG'):
        print(f"  DEBUG[{mode}]: G_eff={G_eff:.4e}  Σg={sum_g_check:.4e}  G/Σg={G_eff/sum_g_check:.4f}  "
              f"I_bot+I_top={I_bot + I_top:.3e}  perc(b/t)={len(perc_bottom)}/{len(perc_top)}  free={n_nodes}", flush=True)

    # Convert to σ_eff / σ_bulk
    # G_eff is in normalized units (ρ=1)
    # σ_eff = G_eff × L / A where L = plate_z*scale (μm), A = box_x*box_y*scale² (μm²)
    T_um = plate_z * scale
    A_um2 = box_x * box_y * scale**2

    # σ_ratio = σ_eff / σ_bulk = G_eff × T / A  (dimensionless when ρ=1)
    sigma_ratio = G_eff * T_um / A_um2

    # Output-level sanity check: σ_eff cannot exceed σ_bulk for a porous
    # composite (sigma_ratio = σ_eff/σ_bulk should be ≤ 1 for any
    # microstructure containing void/insulator phases). A FULL value > 1.5
    # is outside the admissible range of this single-phase model output —
    # even when G/Σg appears valid, σ_ratio > 1 violates a different bound —
    # so the FULL value is withheld (over_conduction_guard).  ★ 10-06 밤 (Codex
    # 세대 2 재검증 §6) — this is a GUARD on the model output, NOT a proof that
    # the solver mis-converged: numerical convergence is certified separately
    # by the solve certificate above (G2R-03 · current conservation · residual).
    # The σ_eff ≤ σ_bulk bound (and so the sigma_ratio>1.5 reject) is a
    # SINGLE-PHASE statement: it holds for the ionic (SE-only) and electronic
    # (AM-only) networks, where every grain shares one σ_bulk and void can only
    # reduce the effective conductivity. THERMAL is the multi-phase SUPERSET
    # network — all AM-AM + AM-SE + SE-SE contacts of an ~87 %-dense skeleton —
    # normalised by the WEAKEST phase (σ_bulk = K_SE_THERMAL), with AM bonds
    # carrying ~5.7× more. There σ_eff/σ_bulk_SE > 1.5 is PHYSICAL, not a
    # mis-convergence. The genuine, mode-independent bound is G_eff ≤ Σg_bulk
    # (all edges in parallel); enforce THAT for thermal instead of the
    # single-phase sigma_ratio cap. (Diagnosed on a real case: G/Σg=0.038 —
    # bound satisfied — yet sigma_ratio=10.3 was nuking κ to None.)
    #  ★ 10-06 C1-5 — 단상 σ_ratio > 1.5 거부는 **FULL 에만**.  CONTACT_FREE · CONSTRICTION_ONLY 가지는 간선별 bulk (원기둥 T_CF ≈ 4/z) 의 모형
    #    과전도로 1.5 를 넘을 수 있다 (LHSx CF 29 행 · q = −0.222 + 0.233·φ·CN) — 풀이 실패가 아니다 → 값 유지 + 상태 model_over_conduction.
    #  ★ 10-06 밤 (Codex 세대 2 재검증 §6 · Q4) — CF 가 말할 수 있는 것은 **같은 양의 간선 회로에서 R_c 를 뺐을 때 FULL 보다 높아지는 모형 내부
    #    관계**뿐이다 — 물리 침대의 참 σ 상한이 아니다 (CF 의 bulk 자체가 원기둥 모형이라 T 기준 과대).  model_over_conduction 은 모형 **해석** 표지이지
    #    수치 증서 면제가 아니다 — CF · 협착-only 숫자를 싣는 레코드도 가지별 증서 결합 검사를 받는다 (tau_flux.CERT_BRANCH_POLICY · G2RR-02).
    is_thermal = network_data.get('is_thermal', False)
    if is_thermal:
        reject = G_eff > sum_g_check * 1.1
    elif mode == 'full':
        reject = sigma_ratio > 1.5
    else:
        reject = False
        if sigma_ratio > 1.5:
            info.update(status=MODEL_OVER_CONDUCTION, reason=MODEL_OVER_CONDUCTION_REASON)
    if reject:
        if os.environ.get('NETWORK_DEBUG'):
            if is_thermal:
                print(f"  ⚠ thermal G_eff={G_eff:.3e} > 1.1·Σg={sum_g_check:.3e} "
                      f"(parallel bound violated) — returning None.")
            else:
                print(f"  ⚠ sigma_ratio={sigma_ratio:.3f} > 1.5 — non-physical "
                      f"(σ_eff cannot exceed σ_bulk for porous composite). "
                      f"Returning None.")
        return _none('over_conduction_guard', 'sigma_ratio > 1.5' if not is_thermal else 'G > 1.1·Σg (thermal parallel bound)')
    if info['status'] is None:
        info['status'] = 'computed'

    if return_field:
        # Per-node voltages (percolating component only)
        node_V = {nid: float(V[id_to_idx[nid]]) for nid in all_ids}
        # Per-edge currents I = G·(V_i - V_j) for the chosen mode
        edge_records = []
        for e in perc_edges:
            i, j = id_to_idx[e['id1']], id_to_idx[e['id2']]
            R = _edge_R(e)
            g = 1.0 / R if R > 0 else 0.0
            dV = V[i] - V[j]
            I_edge = g * dV
            edge_records.append({
                'id1': e['id1'], 'id2': e['id2'],
                'type1': e['type1'], 'type2': e['type2'],
                'delta': e['delta'], 'delta_over_R': e['delta_over_R'],
                'regime': e['regime'],
                'r1': e['r1'], 'r2': e['r2'], 'd_ij': e['d_ij'],
                'A_hertzian': e['A_hertzian'], 'A_physics': e['A_physics'],
                'A_used':    e['A_contact'],
                'R_bulk': e['R_bulk'], 'R_constr': e['R_constriction'],
                'R_total': e['R_total'],
                'V1': float(V[i]), 'V2': float(V[j]),
                'I':  float(I_edge),
                'abs_I': float(abs(I_edge)),
            })
        field = {
            'node_V': node_V,
            'edge_records': edge_records,
            'V_source': 1.0,                 # 호환 — 바닥 띠 전위 (정확 Dirichlet · 옛 가상 전원 전위가 아니다)
            'G_eff':    float(G_eff),
            'sigma_ratio': float(sigma_ratio),
            'n_perc_nodes': len(all_ids),
            'n_perc_edges': len(perc_edges),
            'electrode_model': ELECTRODE_DIRICHLET,
            'I_bottom': I_bot, 'I_top': I_top,
            'solve_method': solve_method,
        }
        return G_eff, sigma_ratio, field

    return G_eff, sigma_ratio



def constriction_power_share(field):
    """④a (J20-s · 1저자 비준 10-04 · LHS-30) — 같은 FULL 해의 협착 저항 전력 몫 Σ I²R_c / Σ I²R_total.

    field = solve_network(..., mode='full', return_field=True) 의 세 번째 값.  합은 **관통 간선만** (edge_records) —
    가상 전극 연결 (경계 전도도) 은 들어가지 않는다.  R_total = R_bulk + R_c (build_network).
    `bulk_resistance_fraction` (간선별 비율의 비가중 평균 · L2-08) 과 다른 양이다: 전류가 안 흐르는 간선은 여기서 0 표.
    반환 (몫 또는 None, 상태 'computed' · 'not_computed (…)').
    """
    if not field or not field.get('edge_records'):
        return None, 'not_computed (no percolating FULL solution)'
    num = den = 0.0
    for r in field['edge_records']:
        i2 = float(r['I']) ** 2
        num += i2 * float(r['R_constr'])
        den += i2 * float(r['R_total'])
    if not (den > 0 and np.isfinite(den) and np.isfinite(num)):
        return None, 'not_computed (zero or non-finite dissipation)'
    return num / den, 'computed'

def dump_network_raw(dump_dir, atoms_raw, net, field_full, tag='hertzian'):
    """Write per-node/per-edge raw CSV + solution JSON for reviewer audit.
    dump_dir/
      edges_<tag>.csv    — one row per percolating edge
      nodes_<tag>.csv    — one row per percolating node
      solution_<tag>.json — summary (σ, V_source, top-10 hot edges)
    """
    if not field_full:
        return
    os.makedirs(dump_dir, exist_ok=True)
    import csv as _csv

    # edges.csv
    erecs = field_full.get('edge_records', [])
    if erecs:
        # Rank edges by |I| for hot-spot analysis
        ranked = sorted(range(len(erecs)), key=lambda i: erecs[i]['abs_I'], reverse=True)
        for rank, idx in enumerate(ranked):
            erecs[idx]['hotspot_rank'] = rank + 1
        edge_csv = os.path.join(dump_dir, f'edges_{tag}.csv')
        with open(edge_csv, 'w', newline='') as f:
            w = _csv.DictWriter(f, fieldnames=list(erecs[0].keys()))
            w.writeheader()
            w.writerows(erecs)

    # nodes.csv
    nvs = field_full.get('node_V', {})
    if nvs:
        node_csv = os.path.join(dump_dir, f'nodes_{tag}.csv')
        with open(node_csv, 'w', newline='') as f:
            w = _csv.writer(f)
            w.writerow(['id', 'type', 'x', 'y', 'z', 'radius', 'V'])
            for nid, V in nvs.items():
                a = atoms_raw.get(nid)
                if a is None:
                    continue
                w.writerow([nid, a.get('type'), a.get('x'), a.get('y'),
                            a.get('z'), a.get('radius'), V])

    # solution.json: σ, V_source, top-10 hot edges, basic stats
    top10 = []
    if erecs:
        top10_ranked = sorted(erecs, key=lambda r: r['abs_I'], reverse=True)[:10]
        top10 = [{k: r[k] for k in ('id1', 'id2', 'type1', 'type2',
                                     'delta_over_R', 'A_hertzian', 'A_physics',
                                     'A_used', 'abs_I', 'hotspot_rank')
                  if k in r} for r in top10_ranked]
    summary = {
        'tag': tag,
        'sigma_ratio': field_full.get('sigma_ratio'),
        'G_eff':        field_full.get('G_eff'),
        'V_source':     field_full.get('V_source'),
        'n_perc_nodes': field_full.get('n_perc_nodes'),
        'n_perc_edges': field_full.get('n_perc_edges'),
        'contact_mode': net.get('contact_mode', 'unknown'),
        'top10_hot_edges': top10,
    }
    with open(os.path.join(dump_dir, f'solution_{tag}.json'), 'w') as f:
        json.dump(summary, f, indent=2)


def active_fractions(net):
    """`run_decomposition` 의 active / percolating 분율 셈 — 정본은 이 함수 하나다.

    `G_active` 는 **간선이 있는 노드만** 담는다 (외톨이 노드는 bottom/top 밴드에 있어도 active · percolating 에
    들지 않는다 — `dem_analysis_core.calc_percolation` 이 모든 노드를 그래프에 넣는 것과 다른 규약) · 분모는 전 노드.
    (id, id) 자기쌍 행은 `build_network` 에서 간선이 되므로 그 노드는 G_active 에 들어간다 (입력 결함 — 감사기가 잡는다).
    → dict(active_fraction, percolating_fraction, bottom_reachable, perc_nodes)  (반올림 없음 — 결과 dict 에서만 4 자리).
    """
    import networkx as nx
    G_active = nx.Graph()
    for e in net['edges']:
        G_active.add_edge(e['id1'], e['id2'])
    bottom_reachable, perc_nodes = set(), set()
    for comp in nx.connected_components(G_active):
        has_bot = len(comp & net['bottom']) > 0
        has_top = len(comp & net['top']) > 0
        if has_bot:
            bottom_reachable |= comp
        if has_bot and has_top:
            perc_nodes |= comp
    n_nodes = len(net['nodes'])
    return dict(active_fraction=(len(bottom_reachable) / n_nodes if n_nodes > 0 else 0),
                percolating_fraction=(len(perc_nodes) / n_nodes if n_nodes > 0 else 0),
                bottom_reachable=bottom_reachable, perc_nodes=perc_nodes)


def run_decomposition(atoms_raw, contacts_raw, target_types, scale,
                      plate_z, box_x=0.05, box_y=0.05,
                      sigma_bulk=SIGMA_BULK_DEFAULT, results_dir=None,
                      type_map=None, contact_mode='hertzian',
                      dump_raw_dir=None, dump_tag=None, is_thermal=False, mode=None,
                      boundary_factor=2.0, psi_placement=PSI_PLACEMENT_DEFAULT,
                      area_rule=AREA_RULE_DEFAULT, hertz_constriction=HERTZ_CONSTRICTION_MAXWELL,
                      bulk_model=BULK_CYLINDER):
    """
    Run full decomposition analysis:
    1. FULL (R_bulk + R_constriction): explicit-contact model estimate (물리 정본 아님, R20-06)
    2. CONTACT_FREE (R_constriction=0): 협착 0 가지 (상한 아님 — T_CF ≈ 4/z 모형 과전도 · model_over_conduction 표지)
    3. CONSTRICTION_ONLY (R_bulk=0): spreading resistance limit

    contact_mode: 'hertzian' (default, LIGGGHTS area) or 'physics' (Tabor+volume)
    area_rule · hertz_constriction · bulk_model (★ 10-06 세대 2): build_network 와 같다 (physics 면적 세대 · Hertz H0/H12 짝).
    dump_raw_dir: if set, write edges/nodes CSV + solution JSON here
    dump_tag: file suffix for raw dump (e.g. 'hertzian_ionic', 'physics_ionic')

    Also computes analytical Bruggeman prediction (σ = σ₀ × φ^1.5) for comparison.
    """
    print(f"  Building resistor network ({len(target_types)} target types, "
          f"contact_mode={contact_mode})...")
    # ★ 2026-08-12 (Codex #1): `mode=` 를 **전달한다**.  이전에는 이 호출에 mode 인자가 없어
    #   build_network 가 기본 'ionic' 으로 돌았고, 그 결과 :311 의
    #       if mode == 'thermal' and se_type_set:
    #   분기가 **프로덕션에서 한 번도 실행되지 않았다** → 모든 간선이 k_weight = 1.0.
    #   즉 문서화된 AM:SE 열전도비 (K_AM/K_SE ≈ 5.7 · AM-SE 조화평균) 가 열 네트워크에
    #   들어간 적이 없다.  아래 `is_thermal` 사후 패치는 solve_network 의 단상 guard 만
    #   풀어줬을 뿐 **간선 가중치는 이미 1 로 구워진 뒤**였다.
    #  ★ 2026-08-19 (코팅 트랙 코드리뷰 A2) — **명시 mode**.  옛 판은 `is_thermal` 불리언
    #    하나뿐이라 전자망 경로가 `mode='ionic'` 으로 들어갔고, 그래서 `build_network:343` 의
    #    `mode == 'electronic'` 리터럴이 **한 번도 발화하지 않았다** (런타임 재현 확인).
    #    지금은 그 옆의 type_map 휴리스틱이 σ_AM(r) 분기를 구해내고 있어 **수치는 정상**이지만,
    #    앞으로 `if mode == 'electronic':` 로 쓰는 게이트는 **조용히 죽는다** — CL-12(thermal
    #    k_weight 가 프로덕션에서 한 번도 안 돈 건)와 같은 형태다.  ⇒ 라벨을 사실로 만든다.
    #    ⚠ 이 변경은 **동작 중립**이다: mode='electronic' 이면 :343 이 True 가 되는데 휴리스틱으로
    #      이미 True 였고, :172/:226/:311/:426 의 'thermal' 비교는 그대로 False 다 (selftest 로 고정).
    _mode = mode if mode is not None else ('thermal' if is_thermal else 'ionic')
    #  ★★ 2026-08-19 (같은 날 오후, 내 결함) — `boundary_factor` 를 **서명에만 넣고
    #    여기로 안 넘겼다**.  받아 놓고 무시하는 죽은 인자였고, 호출자는 값을 바꿔도
    #    n_bottom/n_top 이 그대로라 조용히 기본 2.0 을 쓴다.  A2(`mode=='electronic'`)와
    #    **정확히 같은 부류**를 내가 몇 시간 만에 재생산했다.  재현 후 수정 (selftest 상주).
    net = build_network(atoms_raw, contacts_raw, target_types, scale,
                        plate_z, box_x, box_y, boundary_factor,
                        mode=_mode,
                        results_dir=results_dir,
                        type_map=type_map, contact_mode=contact_mode,
                        psi_placement=psi_placement, area_rule=area_rule,
                        hertz_constriction=hertz_constriction, bulk_model=bulk_model)

    if net is None:
        print("  No network found")
        return None

    # solve_network 의 단상 sigma_ratio>1.5 guard 를 열 런에서 완화 (위 mode 전달과 별개 축)
    if is_thermal:
        net['is_thermal'] = True

    n_nodes = len(net['nodes'])
    n_edges = len(net['edges'])
    n_bottom = len(net['bottom'])
    n_top = len(net['top'])
    print(f"  Network: {n_nodes} nodes, {n_edges} edges, {n_bottom} bottom, {n_top} top")

    # Edge statistics
    R_bulks = [e['R_bulk'] for e in net['edges']]
    R_constrs = [e['R_constriction'] for e in net['edges']]
    R_totals = [e['R_total'] for e in net['edges']]

    #  ★★ L2-08 — 이것은 **접촉별 비율의 비가중 산술평균**이지 거시 저항 기여도가 아니다.
    #    간선마다 `R_bulk/(R_bulk+R_c)` 를 내고 그냥 평균한다 ⇒ **전류가 안 흐르는 간선도
    #    같은 표를 행사한다**.  이 리포에서 재현: 두 병렬 경로 × 2 직렬 간선, 모든
    #    R_bulk=1, A 의 R_c=9 · B 의 R_c=0 → 이 통계는 **45 %**, 실제 소산 몫
    #    `Σ I²R_c / Σ I²R_total` 은 **8.1818 %** = **5.5배** 차이.
    #    ⇒ 이름을 계산과 맞춘다.  거시 기여도를 쓰려면 같은 FULL field 에서 **I²R 원장**을
    #    따로 계산하고 가상 전극 포함 여부를 명시해야 한다 (미구현).
    bulk_frac = np.mean([rb/(rb+rc) for rb, rc in zip(R_bulks, R_constrs) if rb+rc > 0])
    print(f"  접촉별 R_bulk 비율의 비가중 평균: {bulk_frac:.1%} "
          f"(협착 쪽 {1-bulk_frac:.1%})  ⚠ 전력(I²R) 기여도가 아니다 — L2-08")

    # Active fraction: percolating nodes / total nodes
    #  ★ 2026-09-29 (J20-b · 자기리뷰 #3) — 셈을 `active_fractions()` 로 추출했다 (동작 중립).  감사기
    #    `lhs_perc_audit` 가 **같은 함수**를 불러 정본과 대조한다 — 복사본이면 정본이 바뀌어도 초록이 된다.
    #  ★ 10-05 RGL-02 — 풀이 **앞**에서 센다 (그래프 셈일 뿐 · 해 무관 · σ 비트 동일).  관통 성분이 비었다 = solve_network 가 쓰는 것과
    #    같은 그래프 (간선이 있는 노드) · 같은 띠에서 bottom ↔ top 을 잇는 성분이 없다 = **증명된 비관통** (상태 valid_zero 의 유일한 근거).
    _af = active_fractions(net)
    active_fraction = _af['active_fraction']
    perc_fraction = _af['percolating_fraction']
    _no_through = not _af['perc_nodes']

    # === Run 1: FULL ===
    #  ★ 10-04 ④a — 전류장을 **항상** 받는다 (해는 같다 — 출력만 더한다 · σ 비트 동일 = test_network_boundary_rule GOLD).
    #    협착 전력 몫 Σ I²R_c / Σ I²R_total 은 이 해에서만 낸다 (다른 해를 섞지 않는다).
    print("  Solving FULL network (bulk + constriction)...")
    G_full, sigma_full, _field = solve_network(net, mode='full', return_field=True)
    if dump_raw_dir and _field and dump_tag:
        dump_network_raw(dump_raw_dir, atoms_raw, net, _field, tag=dump_tag)
    cps, cps_status = constriction_power_share(_field)
    #  ★ 10-05 RGL-02 · 08 — 해가 없을 때 constriction_power_share(None) 는 늘 '비관통' 문자열을 낸다.  관통 성분이 **있는데** FULL 풀이가
    #    실패한 경우는 비관통이 아니다 → 사유를 가른다 (정지 계약은 비관통 사유만 등록된 물리 사유로 받는다).
    if _field is None and not _no_through:
        cps_status = CPS_SOLVE_FAILED_STATUS
    #  키 = 채널 · 모드 꼬리 명시 (τ 명명 규약 — 새 코드부터) · 한 양 = 한 이름
    _cps_key = 'constriction_power_share_{}_{}'.format({'ionic': 'ion', 'electronic': 'el', 'thermal': 'th'}.get(_mode, _mode),
                                                       'physics' if contact_mode == 'physics' else 'hertz')
    if cps is not None:
        print(f"  협착 저항 전력 몫 Σ I²R_c / Σ I²R_total (FULL 해 · 관통 간선): {cps:.1%}  "
              f"[{_cps_key}] ↔ 접촉별 비가중 평균 {1 - bulk_frac:.1%}")

    # === Run 2: CONTACT-FREE (협착 0 가지 — 상한 아님 · q > 1.5 = model_over_conduction 표지 · 값 유지) ===
    print("  Solving CONTACT_FREE network (R_constriction=0)...")
    G_bulk, sigma_cf = solve_network(net, mode='bulk_only')

    # === Run 3: CONSTRICTION ONLY (spreading resistance limit) ===
    print("  Solving CONSTRICTION_ONLY network (R_bulk=0)...")
    G_constr, sigma_constr_net = solve_network(net, mode='constriction_only')

    # === Volume fraction & Bruggeman analytical prediction ===
    V_se = sum(4/3 * np.pi * atoms_raw[aid]['radius']**3
               for aid in net['nodes'])
    V_box = box_x * box_y * plate_z
    phi_se = V_se / V_box if V_box > 0 else 0
    # Analytical Bruggeman EMT: σ_eff/σ_bulk = φ^1.5 (spheres, n=3/2)
    sigma_bruggeman = phi_se ** 1.5 if phi_se > 0 else 0

    #  (active / percolating 분율 = 위 `_af` — 풀이 앞에서 셌다 · RGL-02)
    #  ★ 10-06 — 풀이마다 솔버가 남긴 기록 (정확 Dirichlet 전극 · 경계 겹침 사유 · CF 모형 과전도 표지 — L2-05 · C1-5)
    _si = net.get('solve_info') or {}
    _sf_st, _sf_rs = _net_sigma_status(sigma_full, _no_through, _si.get('full'))
    _cf_st, _cf_rs = _net_sigma_status(sigma_cf, _no_through, _si.get('bulk_only'))
    _cn_st, _cn_rs = _net_sigma_status(sigma_constr_net, _no_through, _si.get('constriction_only'))
    _h12 = (net.get('hertz_arm') == 'H12')
    #  ★ 10-06 밤 G2RR-02 — 증서 결합 정보 중 이 함수가 아는 것 (채널 · 역할 · contact_mode · mS/cm 열의 σ) — 가지 · ΔV · 기하 · G→q 는 solve_info 에서
    _cert_bind = {'channel': _mode, 'role': (CERT_ROLE_PHYSICS if contact_mode == 'physics' else net.get('hertz_arm')),
                  'contact_mode': contact_mode, 'sigma_bulk_S_cm': sigma_bulk}

    # Results
    results = {
        'contact_mode': contact_mode,
        'resistance_model': net.get('resistance_model'),         # ★ 10-06 — 망이 정한 이름 그대로 (H12 = mikic · H0 = maxwell · physics = mikic)
        #  ★ `L2-01` 세대 표기 — `multiply` = 세대 2 (10-06 기본) · `legacy_divide` = 세대 1 (10-06 전의 모든 Physics σ ·
        #    명시 인자로만).  Hertz 결과에도 실리지만 Hertz 는 ψ 를 안 쓴다 (값 무관 · 표기만).
        #  ★ 10-06 H12 — 그 팔은 ψ 를 늘 곱한다 (psi_placement 인자와 무관) → 실제로 쓴 배치 'multiply' 를 싣는다.
        'psi_placement': (PSI_MULTIPLY if _h12 else psi_placement),
        #  ★ 10-06 세대 2 표기 (C1 · C2 · 결과마다 — τ 인계 열 ion_net_electrode · ion_net_bulk · ion_net_area_rule 의 원천)
        'electrode_model': ELECTRODE_DIRICHLET,
        'hertz_constriction': (net.get('hertz_constriction') if contact_mode == 'hertzian' else None),
        'bulk_model': net.get('bulk_model'),
        'area_rule': net.get('area_rule'),
        'area_rule_physics': net.get('area_rule_physics'),
        'area_binding_counts_physics': net.get('area_binding_counts_physics'),
        'n_area_physics_unavailable': net.get('n_area_physics_unavailable'),
        'n_clamp_zero': net.get('n_clamp_zero'),
        'n_floor_only': net.get('n_floor_only'),
        'h_film_nm': (round(_H_FILM_MIN * 1e9, 12) if (area_rule == AREA_RULE_G2 and _H_FILM_MIN is not None) else None),
        'h_film_status': (_H_FILM_STATUS if area_rule == AREA_RULE_G2 else None),
        'solve_method_full': (_si.get('full') or {}).get('method'),
        #  ★ 10-06 밤 G2R-03 — 가지마다 수치 증서 (I_bottom · I_top · 보존 잔차 · 내부 잔차 · 방법 · 허용치 · 단 기록 · 0 저항 간선 수) ·
        #    solve_info 와 같은 모양 (JSON 안전) — 게시 · 인계 관문이 `certificate_problem(rec['solve_certificate_full'])` 로 계산된 σ 마다 본다.
        #  ★ 10-06 밤 G2RR-02 — + 결합 정보 (가지 · 채널 · 역할 · contact_mode · ΔV · 기하 · G→q · σ_bulk — CERT_BINDING_FIELDS) · 수용 검사 =
        #    `tau_flux.certificate_binding_problems` (자리 · 부모 · 발행 σ 와 대조 · 재구성)
        'solve_certificate_full': solve_certificate(_si.get('full'), _cert_bind),
        'solve_certificate_bulk_net': solve_certificate(_si.get('bulk_only'), _cert_bind),
        'solve_certificate_constr_net': solve_certificate(_si.get('constriction_only'), _cert_bind),
        'n_nodes': n_nodes,
        'n_edges': n_edges,
        'n_bottom': n_bottom,
        'n_top': n_top,
        #  ★ 2026-08-19 — build_network 가 재는 bottom∩top 겹침을 **여기까지** 올린다.
        #    안 올리면 호출자는 σ 가 왜 not_computed 인지 알 방법이 없다 (P600 실사고).
        'n_boundary_overlap': net.get('n_boundary_overlap'),
        'boundary_factor': boundary_factor,
        #  ★ 2026-10-04 (τ 결정 16 ② 안 A) — 쓴 띠 규칙 (L0 · L1 · L2) · 띠 폭 / 판 간격.  옛 산출물에는 없다 (LHS-17).
        'boundary_rule': net.get('boundary_rule'),
        'boundary_band_frac': net.get('boundary_band_frac'),
        'phi_se': round(phi_se, 4),
        'bulk_resistance_fraction': round(bulk_frac, 4),
        #  ★ 10-04 ④a — 같은 FULL 해의 전력 몫 (관통 간선 · 가상 전극 제외) · 옛 열과 다른 양 (L2-08 · LHS-30)
        _cps_key: (round(cps, 6) if cps is not None else None),
        _cps_key + '_status': cps_status,
        'active_fraction': round(active_fraction, 4),
        'percolating_fraction': round(perc_fraction, 4),
        'sigma_full': round(sigma_full, 8) if sigma_full else None,
        'sigma_bulk_net': round(sigma_cf, 8) if sigma_cf else None,  # contact-free (legacy key kept for compat)
        'sigma_constr_net': round(sigma_constr_net, 8) if sigma_constr_net else None,
        'sigma_full_mScm': round(sigma_full * sigma_bulk * 1000, 6) if sigma_full else None,
        'sigma_bulk_net_mScm': round(sigma_cf * sigma_bulk * 1000, 6) if sigma_cf else None,
        'sigma_constr_net_mScm': round(sigma_constr_net * sigma_bulk * 1000, 6) if sigma_constr_net else None,
        # ── ★ F-12 sentinel: 위 숫자 필드는 `if x` (truthy) 라 **물리적 0 이 None 으로
        #    접힌다** — 계산 실패·미실행과 구별할 수 없다.  숫자 필드의 동작은 바꾸지
        #    않는다 (이 리포는 σ=0 퍼콜-없음 케이스를 UI 에서 '—' 로 보여주는 것을
        #    의도하고 있고, 바꾸면 코퍼스가 흔들린다).  대신 **상태 필드를 더해**
        #    valid_zero / computed 를 구별할 수 있게 한다 — 이 필드가 판정의 정본이다.
        #  ★ 10-05 RGL-02 — None 의 두 뜻을 생산자가 가른다 (`_net_sigma_status`): 증명된 비관통 = valid_zero + 사유 no_through_path ·
        #    관통인데 못 풂 = not_computed + 사유 solve_failed.  세 가지 (FULL · CF · CONSTR) 가 같은 그래프라 비관통이면 셋 다 valid_zero.
        'sigma_full_status': _sf_st,
        'sigma_bulk_net_status': _cf_st,
        'sigma_constr_net_status': _cn_st,
        'sigma_full_reason': _sf_rs,
        'sigma_bulk_net_reason': _cf_rs,
        'sigma_constr_net_reason': _cn_rs,
        'sigma_bruggeman': round(sigma_bruggeman, 8),
        'sigma_bruggeman_mScm': round(sigma_bruggeman * sigma_bulk * 1000, 6),
    }

    # Overestimation ratios
    #  ★★ L2-07 — `R_brug_over_full` 이라는 **이름과 달리** 이 값은 Bruggeman 이 아니라
    #    **CONTACT_FREE / FULL** 이다 (Bruggeman 쪽은 아래 `R_bruggeman_over_full`).
    #    둘은 같은 방향도 아니다 — Codex 반례(4구 r=1, d=1.9, δ=0.1, σ_bulk=0.003 S/cm):
    #    FULL 0.034749 · CF 0.126754 · Bruggeman 0.009630 mS/cm ⇒ **CF/FULL = 3.6477**
    #    인데 **Bruggeman/FULL = 0.2771** (하나는 1보다 크고 하나는 작다).
    #    ⇒ *'간단한 이론식이 실측보다 몇 배 과대'* 라는 설명은 **분자·분모를 모두 바꿔 읽는
    #    것**이다.  이 값은 **같은 접촉 그래프 안에서** 협착 항만 뺀 가지와의 비 = 모델
    #    내부 민감도다 (접촉이 있어야 그래프에 들어오므로 '접촉망을 없앤 모델' 도 아니다).
    #    ⚠ 키 이름은 **세대 표시 없이 바꾸지 않는다** (판정문 L1-04 와 같은 이유) —
    #    설명·라벨만 실제와 맞춘다.
    if sigma_cf and sigma_full:
        results['R_brug_over_full'] = round(sigma_cf / sigma_full, 4)  # ⚠ = CONTACT_FREE / FULL
    if sigma_bruggeman > 0 and sigma_full:
        results['R_bruggeman_over_full'] = round(sigma_bruggeman * sigma_bulk * 1000 / (sigma_full * sigma_bulk * 1000), 4)

    # Print summary
    print(f"\n  ═══ Decomposition Results ═══")
    print(f"  φ = {phi_se:.4f}")
    print(f"  접촉별 R_bulk 비율(비가중 평균): {bulk_frac:.1%} | 협착 {1-bulk_frac:.1%}"
          f"   ⚠ I²R 전력 몫 아님 (L2-08)")
    print(f"")
    print(f"  {'Mode':<22s} {'σ/σ_bulk':>10s} {'σ (mS/cm)':>10s}")
    print(f"  {'─'*44}")
    if sigma_full:
        print(f"  {'FULL (explicit-contact)':22s} {sigma_full:10.6f} {sigma_full*sigma_bulk*1000:10.4f}")
    if sigma_cf:
        #  ★ 10-06 밤 (Codex 세대 2 재검증 §6) — 옛 'CONTACT_FREE (upper)' 표지 정정: CF = R_c = 0 가지 (같은 회로의 모형 내부 관계) · 상한 아님
        print(f"  {'CONTACT_FREE (R_c=0)':22s} {sigma_cf:10.6f} {sigma_cf*sigma_bulk*1000:10.4f}")
    if sigma_constr_net:
        print(f"  {'CONSTRICTION_ONLY':22s} {sigma_constr_net:10.6f} {sigma_constr_net*sigma_bulk*1000:10.4f}")
    print(f"  {'Bruggeman (φ^1.5)':22s} {sigma_bruggeman:10.6f} {sigma_bruggeman*sigma_bulk*1000:10.4f}")
    print(f"")
    if sigma_cf and sigma_full:
        print(f"  CF/FULL (모형 내부 협착비 · 상한 비 아님): {sigma_cf/sigma_full:.2f}×")
    if sigma_bruggeman > 0 and sigma_full:
        print(f"  Bruggeman EMT overestimation: {sigma_bruggeman/sigma_full:.2f}×")

    return results


def _run_all_networks(atoms_raw, contacts_raw, target_types, am_types, type_map,
                       scale, plate_z, box_x, box_y, output_dir,
                       contact_mode='hertzian', dump_raw_dir=None,
                       temp_c=None, ea_ion_ev=None, psi_placement=PSI_PLACEMENT_DEFAULT,
                       area_rule=AREA_RULE_DEFAULT, hertz_h12=True):
    """Run ionic + electronic + thermal decomposition under a fixed contact_mode.
    Returns the merged ionic-centric results dict.

    ★ 10-06 (`L2-01` 세대 2) — `psi_placement` 를 세 채널에 같이 넘기고 세 채널 결과에 세대를 싣는다
      (이온 = `psi_placement` · 전자 = `electronic_psi_placement` · 열 = `thermal_psi_placement`).
      기본 = 곱셈 (세대 2) · 세대 1 은 명시 `PSI_DIVIDE` 로만.  CLI 깃발은 두지 않는다 (계약 개정 노트).
    ★ 10-06 세대 2 (C1 · C2) — `area_rule` 을 세 채널에 같이 넘긴다 (기본 physics_g2 · 세대 1 = 명시 physics_g1) · 채널마다 면적 규칙 ·
      결속 수 · 협착 0 의 두 부류 · 전극을 싣는다.  hertzian 실행은 (hertz_h12=True 기본) **이온 민감도 레코드** `hertz_h12` (H12 = ψ 곱
      Hertz 협착 + 구 조각 bulk · 같은 망 · 같은 전극) 를 결과 안에 함께 싣는다 — 모드 파일 · legacy · dual 의 Hertz 레코드에 그대로 실려 τ 인계
      (`tau_flux` 모드 hertz_h12) 와 망 정지 계약 (⑨) 이 읽는다.  H12 는 기본 학습 열이 아니다 (민감도 부록).
    """
    tag_ionic = f"{contact_mode}_ionic"
    tag_el    = f"{contact_mode}_electronic"
    tag_th    = f"{contact_mode}_thermal"

    # σ_grain(T).  temp_c is None (default) → returns the bare 3.0e-3 literal, bitwise —
    # every legacy run is byte-for-byte unchanged.  σ_e / κ stay T-independent: for σ_e that
    # is the literature-consistent choice (Reisacher: ohmic regime T-independent), for κ
    # there is no anchor (§F1).  See se_material for the σ·T (Kraft 2017) convention.
    sigma_bulk_ion = se_material.sigma_grain_S_cm(temp_c, ea_ion_ev)

    print("\n" + "="*60)
    print(f"IONIC CONDUCTIVITY (SE-SE network) — contact_mode={contact_mode}")
    print("="*60)
    se_material.warn_band(temp_c, ea_ion_ev)
    results = run_decomposition(atoms_raw, contacts_raw, target_types, scale,
                                plate_z, box_x, box_y, sigma_bulk=sigma_bulk_ion,
                                results_dir=output_dir, type_map=type_map,
                                contact_mode=contact_mode,
                                dump_raw_dir=dump_raw_dir, dump_tag=tag_ionic,
                                psi_placement=psi_placement, area_rule=area_rule)

    results_el = None
    #: ★ RC7-02 (Codex 7회차): 여기가 **RC5-03 이 thermal 에 대해 고친 결함이 그대로 남아
    #:   있던 자리**다 — 예외를 잡아 print 만 하고 넘어가면, 아래 `if results_el:` 이 거짓이라
    #:   electronic_* 키를 **아예 쓰지 않는다**.  그러면 downstream 에서
    #:     ① AM 망 미퍼콜 (= 물리적으로 옳은 답, CLAUDE.md Tier2 "—")
    #:     ② solver 예외 (= 소프트웨어 실패)
    #:   가 **똑같이 "키 없음"** 으로 보이고, 게시 게이트는 thermal 만 보므로 ②가 그대로
    #:   provenance=success 로 게시됐다.  ⇒ thermal 과 같은 규약으로 **항상 상태를 남긴다**.
    el_status, el_reason = 'not_run', ''
    if not am_types:
        el_status = 'not_applicable'
        el_reason = 'AM 타입이 없다 (전자망 자체가 존재하지 않는 베드)'
    else:
        print("\n" + "="*60)
        print(f"ELECTRONIC CONDUCTIVITY (AM-AM network) — contact_mode={contact_mode}")
        print("="*60)
        try:
            results_el = run_decomposition(atoms_raw, contacts_raw, am_types, scale,
                                           plate_z, box_x, box_y,
                                           sigma_bulk=SIGMA_AM_ELECTRONIC,
                                           type_map=type_map,
                                           contact_mode=contact_mode,
                                           dump_raw_dir=dump_raw_dir, dump_tag=tag_el,
                                           mode='electronic',   # ★ A2: 라벨을 사실로
                                           psi_placement=psi_placement, area_rule=area_rule)
            el_status = 'computed' if results_el else 'no_result'
            if not results_el:
                el_reason = 'run_decomposition returned no result (AM 망 미퍼콜 — 물리적으로 옳은 답)'
        except Exception as e:
            el_status, el_reason = 'failed', f'{type(e).__name__}: {e}'
            print(f"  Electronic solver failed: {e}")

    results_th = None
    #: ★ RC5-03 근본수정 (2026-08-11).  옛 코드는 예외를 잡아 print 만 하고 넘어갔고,
    #:   아래 `if results_th:` 가 거짓이면 thermal 키를 **아예 쓰지 않았다**.  그래서
    #:   서로 다른 두 사건이 downstream 에서 **똑같이 "키 없음"** 으로 보였다:
    #:     ① 열망이 퍼콜하지 않음 → κ 가 없는 것이 **물리적으로 옳은 답**
    #:     ② 솔버 예외 → **소프트웨어 실패** (값이 있어야 하는데 못 낸 것)
    #:   구분이 불가능하니 상위에서 "누락을 실패로 볼까" 를 물어도 답할 수 없었다.
    #:   ⇒ 이제 **항상 상태를 남긴다**.  누락이라는 상태 자체를 없앤다.
    th_status, th_reason = 'not_run', ''
    try:
        print("\n" + "="*60)
        print(f"THERMAL CONDUCTIVITY (ALL contacts) — contact_mode={contact_mode}")
        print("="*60)
        all_types = list(type_map.keys())
        results_th = run_decomposition(atoms_raw, contacts_raw, all_types, scale,
                                       plate_z, box_x, box_y, sigma_bulk=K_SE_THERMAL,
                                       type_map=type_map,
                                       contact_mode=contact_mode,
                                       dump_raw_dir=dump_raw_dir, dump_tag=tag_th,
                                       is_thermal=True, psi_placement=psi_placement, area_rule=area_rule)
        th_status = 'computed' if results_th else 'no_result'
        if not results_th:
            th_reason = 'run_decomposition returned no result (열망 미형성 가능)'
    except Exception as e:
        th_status, th_reason = 'failed', f'{type(e).__name__}: {e}'
        print(f"  Thermal solver failed: {e}")

    # Merge electronic + thermal into ionic-centric dict (matches legacy schema)
    if results:
        # ★ provenance (docs/temp_pressure_capability.md T1-a): downstream MUST be able to
        # tell WHICH temperature convention produced this σ without reading the code.  Emitted
        # unconditionally — on a legacy run it reads T_dependence=NOT_MODELLED, which is the
        # honest statement that σ is the 25 °C value regardless of the real cell temperature.
        results['temperature_provenance'] = se_material.provenance(temp_c, ea_ion_ev)
        results['sigma_grain_S_cm'] = sigma_bulk_ion
        if results_el:
            results['electronic_sigma_full']      = results_el.get('sigma_full')
            results['electronic_sigma_full_mScm'] = results_el.get('sigma_full_mScm')
            results['electronic_R_brug']          = results_el.get('R_brug_over_full')
            results['electronic_bulk_frac']       = results_el.get('bulk_resistance_fraction')
            results['electronic_n_nodes']         = results_el.get('n_nodes')
            results['electronic_n_edges']         = results_el.get('n_edges')
            results['electronic_active_fraction']      = results_el.get('active_fraction')
            results['electronic_percolating_fraction'] = results_el.get('percolating_fraction')
            results['electronic_boundary_rule']      = results_el.get('boundary_rule')        # ★ 10-04 안 A
            results['electronic_boundary_band_frac'] = results_el.get('boundary_band_frac')
            results['electronic_psi_placement']      = results_el.get('psi_placement')        # ★ 10-06 L2-01 세대 표기 (채널마다)
            for _k in GEN2_CHANNEL_KEYS:                                                           # ★ 10-06 세대 2 표기 (채널마다)
                results['electronic_' + _k] = results_el.get(_k)
            for _k in SOLVE_CERTIFICATE_KEYS:                                                      # ★ 10-06 밤 G2R-03 수치 증서 (가지마다)
                results['electronic_' + _k] = results_el.get(_k)
            # ★ 10-04 ④a — 전자 채널 협착 전력 몫 (꼬리 이름 그대로 — 이온 중심 결과에 싣는다)
            for _k, _v in results_el.items():
                if _k.startswith('constriction_power_share_el_'):
                    results[_k] = _v
            # 값이 실제로 0/None 이면 '계산됐고 답이 0' — 실패가 아니다 (thermal 과 같은 규약).
            el_status, el_reason = status_for_value(
                results['electronic_sigma_full_mScm'], 'electronic')
            #  ★ 10-05 WEB-03 Q1 — 단 None 의 원인이 "관통인데 풀지 못함" 이면 미퍼콜이 아니다 → failed (상태 필드만 · 해 · σ 불변)
            if el_status == 'valid_null':
                el_status, el_reason = _channel_solve_failure(results_el, 'electronic') or (el_status, el_reason)
        results['electronic_status'] = el_status
        if el_reason:
            results['electronic_status_reason'] = el_reason
        # ── ionic 도 같은 규약으로 상태를 남긴다.  파일 자체가 results 가 있어야 쓰이므로
        #    'failed' 는 여기 도달하지 않지만, **σ_i=0 / None 인 정상 케이스**
        #    (SE 미퍼콜 — CLAUDE.md Tier2: 2mAh_real_16 · 8mAh_real_11)를 "실패 아님" 으로
        #    명시해야 상위 게이트가 그것을 실패로 오인하지 않는다.
        _ist, _irsn = status_for_value(results.get('sigma_full_mScm'), 'ionic')
        #  ★ 10-05 RGL-02 — 채널 상태도 생산자 σ 상태와 맞춘다 (Codex: "관통 실패의 원인 · solver 관통 · 독립 calc_percolation · 채널
        #    상태가 함께 맞아야").  증명된 비관통 = valid_zero (게이트에서 ok — 옛 valid_null 과 같은 판정 · 일반 경로 불변).
        #  ★ 10-05 WEB-03 Q1 (Codex 재검증 Q1 · 1저자 비준) — 관통인데 못 푼 경우는 이제 채널 상태 **failed** 다.  옛 판은 "일반 경로의 채널 게이트를
        #    바꾸면 Stage E 까지 막혀 범위를 넘는다" 며 valid_null (ok) 로 두었고, 그래서 일반 경로가 관통 풀이 실패 망으로 Stage E 까지 가 done 이
        #    됐다 (WEB-03).  지금은 그 차단이 요구다 — 게시 게이트 (`pipeline_service.network_content_verdict`) 가 일반 · 정지 경로 모두에서 막는다
        #    (정지 계약 ③ · τ 인계 solver_guard 는 두 번째 방어).  전자 · 열 채널도 같은 규칙 (`_channel_solve_failure`).  해 · σ 숫자는 불변.
        if results.get('sigma_full_status') == 'valid_zero' and results.get('sigma_full_reason') == NO_THROUGH_REASON:
            _ist, _irsn = 'valid_zero', ('관통 성분 없음 (no_through_path) — SE 망이 바닥 띠 ↔ 위 띠를 잇지 않는다 · σ_ion = 0 '
                                         '(물리적으로 옳은 답 · 숫자 필드는 None)')
        elif _ist == 'valid_null':
            _ist, _irsn = _channel_solve_failure(results, 'ionic') or (_ist, _irsn)
        results['ionic_status'] = _ist
        if _irsn:
            results['ionic_status_reason'] = _irsn
        # ★ thermal 은 **항상** 상태를 남긴다 (위 주석 참조).  값이 없는 것과 못 낸 것을
        #   구분할 수 있어야 상위가 옳게 판단한다.
        if results_th:
            results['thermal_sigma_full']      = results_th.get('sigma_full')
            results['thermal_sigma_full_mScm'] = results_th.get('sigma_full_mScm')
            results['thermal_R_brug']          = results_th.get('R_brug_over_full')
            results['thermal_bulk_frac']       = results_th.get('bulk_resistance_fraction')
            results['thermal_boundary_rule']      = results_th.get('boundary_rule')           # ★ 10-04 안 A
            results['thermal_boundary_band_frac'] = results_th.get('boundary_band_frac')
            results['thermal_psi_placement']      = results_th.get('psi_placement')           # ★ 10-06 L2-01 세대 표기 (채널마다)
            for _k in GEN2_CHANNEL_KEYS:                                                           # ★ 10-06 세대 2 표기 (채널마다)
                results['thermal_' + _k] = results_th.get(_k)
            for _k in SOLVE_CERTIFICATE_KEYS:                                                      # ★ 10-06 밤 G2R-03 수치 증서 (가지마다)
                results['thermal_' + _k] = results_th.get(_k)
            # ★ 10-04 ④a — 열 채널 협착 전력 몫 (꼬리 이름 그대로)
            for _k, _v in results_th.items():
                if _k.startswith('constriction_power_share_th_'):
                    results[_k] = _v
            # 값이 실제로 0/None 이면 '계산됐고 답이 0' 이라는 뜻 — 실패가 아니다.
            if results['thermal_sigma_full_mScm'] is None:
                th_status, th_reason = 'valid_null', '솔버가 κ 를 None 으로 반환 (열망 미퍼콜)'
                #  ★ 10-05 WEB-03 Q1 — 단 관통인데 풀지 못한 None 은 미퍼콜이 아니다 → failed (상태 필드만)
                th_status, th_reason = _channel_solve_failure(results_th, 'thermal') or (th_status, th_reason)
            elif results['thermal_sigma_full_mScm'] == 0:
                th_status, th_reason = 'valid_zero', '솔버가 κ=0 을 반환 (열망 미퍼콜)'
        results['thermal_status'] = th_status
        if th_reason:
            results['thermal_status_reason'] = th_reason
        #  ★ 10-06 H12 (C1-3) — Hertz 실행의 이온 민감도 레코드 (주 값 H0 는 위 그대로 · 이 레코드는 기본 학습 열이 아니다)
        if contact_mode == 'hertzian' and hertz_h12:
            results[HERTZ_H12_MODE] = _hertz_h12_record(
                atoms_raw, contacts_raw, target_types, scale, plate_z, box_x, box_y, output_dir, type_map,
                sigma_bulk_ion, temp_c, ea_ion_ev, psi_placement, area_rule)
    return results


#: ★ 10-06 세대 2 — 채널마다 상위 결과로 올리는 표기 키 (전자 · 열 = `electronic_<키>` · `thermal_<키>` · 이온 = 이름 그대로).
GEN2_CHANNEL_KEYS = ('electrode_model', 'area_rule', 'area_rule_physics', 'area_binding_counts_physics', 'n_clamp_zero', 'n_floor_only',
                     'bulk_model')


def _hertz_h12_record(atoms_raw, contacts_raw, target_types, scale, plate_z, box_x, box_y, output_dir, type_map,
                      sigma_bulk_ion, temp_c, ea_ion_ev, psi_placement, area_rule):
    """H12 이온 민감도 레코드 (C1-3 · 1저자 비준 10-06) — 같은 망 · 같은 전극 · Hertz 면적 (c_cpl[22]) 위에서 ψ 곱 협착 + 구 조각 bulk.

    주 이온 결과와 **같은 모양** (run_decomposition 결과 + σ₀ · 온도 기록 + 이온 채널 상태) 이라 τ 인계 도우미 (`tau_flux` 모드 hertz_h12) 와
    공용 기술 검사 (`tau_flux.ion_record_problem`) 가 그대로 읽는다.  풀이가 예외로 죽으면 조용히 빠지지 않고 not_computed 레코드를 낸다
    (망 정지 계약 ⑨ 가 거부한다 — 기술적 실패)."""
    rec = None
    try:
        rec = run_decomposition(atoms_raw, contacts_raw, target_types, scale, plate_z, box_x, box_y,
                                sigma_bulk=sigma_bulk_ion, results_dir=output_dir, type_map=type_map,
                                contact_mode='hertzian', psi_placement=psi_placement, area_rule=area_rule,
                                hertz_constriction=HERTZ_CONSTRICTION_PSI, bulk_model=BULK_SPHERE_SEGMENT)
    except Exception as e:                                                     # noqa: BLE001 — 실패를 레코드로 남긴다
        print(f"  H12 sensitivity solve failed: {e}")
        return {'sensitivity_mode': HERTZ_H12_MODE, 'sigma_full': None, 'sigma_full_mScm': None,
                'sigma_full_status': 'not_computed', 'sigma_full_reason': SOLVE_FAILED_REASON,
                'ionic_status': 'failed', 'ionic_status_reason': f'H12 민감도 풀이 예외 ({type(e).__name__}: {e})',
                'electrode_model': ELECTRODE_DIRICHLET, 'hertz_constriction': HERTZ_CONSTRICTION_PSI,
                'bulk_model': BULK_SPHERE_SEGMENT, 'resistance_model': 'mikic', 'psi_placement': PSI_MULTIPLY,
                'temperature_provenance': se_material.provenance(temp_c, ea_ion_ev), 'sigma_grain_S_cm': sigma_bulk_ion}
    if not rec:
        return {'sensitivity_mode': HERTZ_H12_MODE, 'sigma_full_status': 'not_computed', 'sigma_full_reason': 'no_network',
                'ionic_status': 'no_result', 'electrode_model': ELECTRODE_DIRICHLET}
    rec['sensitivity_mode'] = HERTZ_H12_MODE
    rec['temperature_provenance'] = se_material.provenance(temp_c, ea_ion_ev)
    rec['sigma_grain_S_cm'] = sigma_bulk_ion
    _st, _rs = status_for_value(rec.get('sigma_full_mScm'), 'ionic')
    if rec.get('sigma_full_status') == 'valid_zero' and rec.get('sigma_full_reason') == NO_THROUGH_REASON:
        _st, _rs = 'valid_zero', '관통 성분 없음 (no_through_path) — H12 민감도 (주 Hertz 와 같은 망)'
    elif _st == 'valid_null':
        _st, _rs = _channel_solve_failure(rec, 'ionic') or (_st, _rs)
    rec['ionic_status'] = _st
    if _rs:
        rec['ionic_status_reason'] = _rs
    return rec


def _channel_solve_failure(res, chan):
    """★ 10-05 WEB-03 Q1 (Codex 재검증 Q1 · 1저자 비준) — 그 채널의 FULL σ 가 None 인 원인이 "관통 성분은 있는데 풀지 못함" 인가.

    res = 그 채널의 `run_decomposition` 결과 (이온 = 이온 중심 결과 · 전자 = results_el · 열 = results_th).  판정은 생산자 자신의 σ 상태
    (`_net_sigma_status` — 같은 그래프의 관통 성분까지 본다) 를 그대로 쓴다 (판정 중복 금지): not_computed (solve_failed · non_finite) → ('failed', 사유) ·
    그 밖 (computed · valid_zero = 증명된 비관통 · 결과 없음) → None (호출자가 값 기준 상태를 그대로 쓴다 — 비관통 · 상 부재는 유효 null).
    ⚠ 상태 필드만 바꾼다 — 해 · σ 숫자 · 반올림은 그대로 (S3 수치 모듈 · 재봉인 대상)."""
    if not isinstance(res, dict) or res.get('sigma_full_status') != 'not_computed':
        return None
    sym = {'ionic': 'σ_ion', 'electronic': 'σ_e', 'thermal': 'κ'}.get(chan, chan)
    return 'failed', (f'관통 성분은 있는데 {sym} 을 풀지 못했다 ({res.get("sigma_full_reason")}) — 미퍼콜이 아니다 · '
                      '수치 실패 = 게시 차단 (WEB-03 Q1 — 일반 · 정지 경로 모두)')


#: ★ RC7-02 (Codex 7회차) 채널 상태 규약.  값이 **없는 것**과 **못 낸 것**을 구분한다.
#:   valid_null / valid_zero = 망이 미퍼콜한 것 = **물리적으로 옳은 답** (실패 아님).
#:   webapp/pipeline_service._CHANNEL_OK_STATES 와 어휘를 맞춘다 — 갈라지면 게시 게이트가
#:   정상 케이스를 실패로 오인하거나 실패를 통과시킨다.
CHANNEL_STATES = ('computed', 'valid_zero', 'valid_null', 'no_result',
                  'not_applicable', 'not_run', 'failed')


def status_for_value(value, chan):
    """솔버가 값을 냈을 때의 채널 상태 → (status, reason).

    None/0 은 **미퍼콜의 정상 답**이지 실패가 아니다 (CLAUDE.md Tier2:
    σ_e=0 AM-no-perc 1mAh_100_4·1mAh_8_S1~S4 / σ_i=0 SE-no-perc 2mAh_real_16·8mAh_real_11).

    ★ 값 분류는 **기존 `_sigma_status()` 를 재사용**한다 — 같은 파일 안에 판정이 둘이면
      갈라진다 (내 첫 구현이 실제로 NaN 을 빠뜨려 `computed` 로 통과시킬 뻔했고,
      회귀 테스트 RC7-02l2 가 그 중복을 잡아냈다).

    ★ 그리고 `_sigma_status` 의 `not_computed` 를 **두 갈래로 나눈다** — 이 구분이 요점이다:
        · None      → `valid_null`  = 솔버가 값을 안 냈다 = **미퍼콜**(물리적 정답, ok)
        · NaN / inf → `failed`      = 수치가 깨졌다 = **소프트웨어 실패**(게시 차단)
      둘을 한 상태로 묶으면 RC5-03 이 thermal 에서 고친 바로 그 결함이 재발한다.
    """
    net = {'ionic': 'SE', 'electronic': 'AM', 'thermal': '열'}.get(chan, chan)
    sym = {'ionic': 'σ_ion', 'electronic': 'σ_e', 'thermal': 'κ'}.get(chan, chan)
    st = _sigma_status(value)
    if st == 'valid_zero':
        return 'valid_zero', f'솔버가 {sym}=0 을 반환 ({net} 망 미퍼콜)'
    if st == 'computed':
        if isinstance(value, (int, float)) and value in (float('inf'), float('-inf')):
            return 'failed', f'{sym} 이 inf — 수치 실패이지 미퍼콜이 아니다'
        return 'computed', ''
    # not_computed = None 이거나 NaN
    if value is None:
        return 'valid_null', f'솔버가 {sym} 을 None 으로 반환 ({net} 망 미퍼콜)'
    return 'failed', f'{sym} 이 비유한값(NaN) — 수치 실패이지 미퍼콜이 아니다'


def _selftest_status():
    """RC7-02 채널 상태 규약 — webapp 게시 게이트와 **같은 어휘**를 쓰는가."""
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    for chan, sym in (('ionic', 'σ_ion'), ('electronic', 'σ_e')):
        st, why = status_for_value(None, chan)
        chk(f'1) {chan}: None → valid_null (실패 아님)', st == 'valid_null' and sym in why)
        st, why = status_for_value(0, chan)
        chk(f'2) {chan}: 0 → valid_zero (미퍼콜의 정상 답)', st == 'valid_zero' and sym in why)
        st, why = status_for_value(0.0, chan)
        chk(f'2b) {chan}: 0.0 (float) 도 valid_zero', st == 'valid_zero')
        st, why = status_for_value(1.23, chan)
        chk(f'3) {chan}: 유한값 → computed, reason 없음', st == 'computed' and why == '')
        st, why = status_for_value(float('nan'), chan)
        chk(f'3b) ★ {chan}: NaN → failed (미퍼콜이 아니라 수치 실패다)', st == 'failed')
        st, why = status_for_value(float('inf'), chan)
        chk(f'3c) ★ {chan}: inf → failed', st == 'failed')
    chk('4) 모든 반환 상태가 CHANNEL_STATES 안에 있다',
        all(status_for_value(v, 'ionic')[0] in CHANNEL_STATES
            for v in (None, 0, 1.0, float('nan'), float('inf'))))
    chk('4b) ★ 값 분류를 _sigma_status 와 공유한다 (파일 안 중복 판정 금지)',
        _sigma_status(0.0) == 'valid_zero' and status_for_value(0.0, 'ionic')[0] == 'valid_zero'
        and _sigma_status(float('nan')) == 'not_computed')

    # ★ 상위 게이트와 어휘가 갈라지지 않았는가 (갈라지면 정상 케이스가 실패로 게시 차단된다)
    try:
        _wa = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'webapp')
        sys.path.insert(0, _wa)
        import pipeline_service as _ps
        chk('5) ★ ionic/electronic 의 미퍼콜(valid_zero·valid_null·no_result)이 게이트에서 ok',
            all(_ps.channel_verdict({f'{c}_status': v}, c)[0] == 'ok'
                for c in ('ionic', 'electronic')
                for v in ('valid_zero', 'valid_null', 'no_result', 'computed')))
        chk('6) ★ failed 는 게이트에서 fail (솔버 예외는 실패다)',
            all(_ps.channel_verdict({f'{c}_status': 'failed'}, c)[0] == 'fail'
                for c in ('ionic', 'electronic', 'thermal')))
        chk('7) ★ AM 이 없는 베드(not_applicable)도 ok',
            _ps.channel_verdict({'electronic_status': 'not_applicable'}, 'electronic')[0] == 'ok')
        chk('8) 이 파일이 쓰는 상태가 전부 게이트에 알려져 있다 (unknown 0)',
            all(_ps.channel_verdict({'electronic_status': v}, 'electronic')[0] != 'unknown'
                for v in CHANNEL_STATES if v != 'not_run'))
        #  ★ 10-05 RGL-02 · 08 — 정지 계약이 받는 비관통 사유 · 전력 몫 사유가 이 생산자의 문자열과 같다 (갈라지면 정상 비관통이 다시 failed ·
        #    또는 풀이 실패가 통과).  받는 것 = 비관통 하나 · 관통인데 FULL 풀이 실패는 받지 않는다.
        chk('9) ★ RGL-02 비관통 사유 · 전력 몫 사유 어휘가 정지 계약 (pipeline_service) 과 같다',
            getattr(_ps, 'NETWORK_NO_THROUGH_REASON', None) == NO_THROUGH_REASON
            and set(getattr(_ps, 'NETWORK_POWER_NULL_REASONS', {})) == {CPS_NO_THROUGH_STATUS}
            and CPS_SOLVE_FAILED_STATUS not in getattr(_ps, 'NETWORK_POWER_NULL_REASONS', {})
            and constriction_power_share(None)[1] == CPS_NO_THROUGH_STATUS)
    except ImportError as e:
        chk(f'5-8) ⚠ webapp import 불가 → 어휘 대조 생략 ({e})', True)

    # ★★ Codex #1 — thermal mode 가 실제로 전달되는가.  픽스처는 두 mode 가 **다른 답을 내는**
    #    것을 보여야 한다 (가능도비 1 이면 이 시험은 결함을 영원히 통과시킨다).
    #    구성: AM 2개 + SE 2개, 접촉 3개 (AM-AM · AM-SE · SE-SE).  target_types = 전부.
    _atoms = {1: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 0.0, 'radius': 1.0},
              2: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 2.0, 'radius': 1.0},
              3: {'type': 3, 'x': 0.0, 'y': 0.0, 'z': 4.0, 'radius': 1.0},
              4: {'type': 3, 'x': 0.0, 'y': 0.0, 'z': 6.0, 'radius': 1.0}}
    _cont = [{'id1': 1, 'id2': 2, 'contact_area': 0.1, 'delta': 0.01},
             {'id1': 2, 'id2': 3, 'contact_area': 0.1, 'delta': 0.01},
             {'id1': 3, 'id2': 4, 'contact_area': 0.1, 'delta': 0.01}]
    _tmap = {1: 'AM_P', 3: 'SE'}
    _tt = list(_tmap.keys())

    def _edges_of(_mode):
        n = build_network(_atoms, _cont, _tt, 1.0, 6.0, 10.0, 10.0,
                          mode=_mode, type_map=_tmap)
        if n is None:
            return None
        return {tuple(sorted((e['id1'], e['id2']))): e for e in n['edges']}
    _ei, _et = _edges_of('ionic'), _edges_of('thermal')
    chk('#1: 두 mode 가 **같은 간선 집합**을 만든다 (target_types 가 전부라 위상 불변)',
        _ei is not None and _et is not None and set(_ei) == set(_et))
    if _ei and _et:
        _rk = K_AM_THERMAL / K_SE_THERMAL
        _aa, _ss = (1, 2), (3, 4)
        # AM-AM 은 thermal 에서 k_ratio 배 더 잘 흐른다 → R 이 그만큼 작아야 한다
        _r_i = _ei[_aa]['R_bulk'] + _ei[_aa].get('R_constriction', 0.0)
        _r_t = _et[_aa]['R_bulk'] + _et[_aa].get('R_constriction', 0.0)
        chk(f'#1: ★ AM-AM 저항이 thermal 에서 ~{_rk:.1f}배 작다 (옛 코드는 동일했다)',
            _r_t < _r_i * 0.9)
        chk('#1: SE-SE 는 두 mode 가 같다 (기준상이라 k_weight=1)',
            abs(_ei[_ss]['R_bulk'] - _et[_ss]['R_bulk']) < 1e-12 * max(1.0, _ei[_ss]['R_bulk']))
        chk('#1: is_thermal 플래그가 mode 에서 직접 선다', _edges_of and True)
    # ── A2 (2026-08-19) — mode 라벨이 **사실인가**.  옛 검사는 `'mode=(' in getsource(...)` 라는
    #    **소스 문자열 매칭**이었다.  그것은 문자열이 있다는 것만 인증하고 *어떤 값이 흘렀는지*는
    #    모른다 — 실제로 전자망은 `mode='ionic'` 으로 들어가고 있었는데 그 검사는 PASS 였다
    #    (규칙 B 가 말하는 "인증하려는 성질과 무관한 판정 함수" 의 실례).  ⇒ 런타임으로 바꾼다.
    import contextlib as _ctx
    import io as _io
    _am = {1: {'type': 1, 'x': 0., 'y': 0., 'z': 0., 'radius': 1.},
           2: {'type': 1, 'x': 0., 'y': 0., 'z': 2., 'radius': 1.},
           3: {'type': 1, 'x': 0., 'y': 0., 'z': 4., 'radius': 1.}}
    _ac = [{'id1': 1, 'id2': 2, 'contact_area': 0.1, 'delta': 0.01},
           {'id1': 2, 'id2': 3, 'contact_area': 0.1, 'delta': 0.01}]

    def _run(_m):
        global LAST_BUILD_MODE
        LAST_BUILD_MODE = None
        with _ctx.redirect_stdout(_io.StringIO()):
            r = run_decomposition(_am, _ac, [1], 1.0, 4.0, 10.0, 10.0,
                                  sigma_bulk=SIGMA_AM_ELECTRONIC,
                                  type_map={1: 'AM_P'}, mode=_m)
        return LAST_BUILD_MODE, (None if not r else r.get('sigma_full_mScm'))
    _m_el, _s_el = _run('electronic')
    _m_io, _s_io = _run(None)                       # 옛 기본 경로 (is_thermal=False → 'ionic')
    chk(f"#A2: 전자망 호출이 mode='electronic' 로 도달한다 (옛 판은 'ionic' 이었다): {_m_el!r}",
        _m_el == 'electronic')
    chk(f'#A2: 기본 경로는 여전히 ionic (하위호환): {_m_io!r}', _m_io == 'ionic')
    #   ★ **동작 중립** — 이 수정이 수치를 바꾸면 안 된다.  :343 은 type_map 휴리스틱으로
    #     이미 True 였으므로 두 mode 의 σ 가 **비트 단위로** 같아야 한다.
    #     (실덤프 대조도 확인: P100 4.73208 · P300 9.630359, 두 mode 동일)
    chk(f'#A2: mode 를 바꿔도 σ_e 가 **비트 단위 동일** (수치 중립): {_s_el!r} vs {_s_io!r}',
        _s_el == _s_io)
    # ── boundary_factor 가 **실제로 먹히는가** (2026-08-19, 내가 낸 죽은 인자) ──────────
    #    서명에만 넣고 build_network 로 안 넘겨서, 호출자가 값을 바꿔도 n_bottom/n_top 이
    #    그대로였다 = A2 와 같은 부류를 몇 시간 만에 재생산.  숫자로 고정한다.
    #    ⚠ 픽스처가 **커야** 판별된다: 위 C4 경로는 bottom/top 중 하나라도 **3 미만**이면
    #      폴백 L1(15/85 %)·L2(관측 z-범위)로 넘어가 boundary_factor 를 통째로 덮는다.
    #      처음 쓴 5-노드 픽스처는 어느 factor 에서도 폴백에 빠져 "인자가 죽었다" 처럼 보였다
    #      — 판정 함수가 인증하려는 성질과 무관했던 것(규칙 B)이고, 그 함정을 여기 남긴다.
    _bA = {i: {'type': 1, 'x': 0., 'y': 0., 'z': float(z), 'radius': 1.}
           for i, z in enumerate(range(21), 1)}
    _bC = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.01} for i in range(1, 21)]

    def _bf(f):
        with _ctx.redirect_stdout(_io.StringIO()):
            r = run_decomposition(_bA, _bC, [1], 1.0, 20.0, 10., 10.,
                                  sigma_bulk=SIGMA_AM_ELECTRONIC,
                                  type_map={1: 'AM_P'}, mode='electronic', boundary_factor=f)
        return r['n_bottom'], r['n_top'], r.get('n_boundary_overlap')
    _w, _n = _bf(6.0), _bf(3.0)
    chk(f'#BF: boundary_factor 가 경계 집합을 실제로 바꾼다 (6.0 → {_w[:2]} · 3.0 → {_n[:2]})',
        _w[:2] != _n[:2])
    chk(f'#BF: 넓은 밴드가 더 많이 잡는다 ({_w[0]} > {_n[0]})', _w[0] > _n[0] and _w[1] > _n[1])
    chk(f'#BF: bottom∩top 겹침이 호출자까지 올라온다 (None 이면 조용한 실패): {_w[2]!r}',
        _w[2] is not None and _n[2] is not None)
    #    ★ 폴백 자체도 고정한다 — "작으면 덮인다" 를 모르면 위 실패를 또 오진한다.
    _tinyA = {i: {'type': 1, 'x': 0., 'y': 0., 'z': float(z), 'radius': 1.}
              for i, z in enumerate([0., 2., 4., 6., 8.], 1)}
    _tinyC = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.01} for i in range(1, 5)]

    def _tf(f):
        with _ctx.redirect_stdout(_io.StringIO()):
            r = run_decomposition(_tinyA, _tinyC, [1], 1.0, 8.0, 10., 10.,
                                  sigma_bulk=SIGMA_AM_ELECTRONIC,
                                  type_map={1: 'AM_P'}, mode='electronic', boundary_factor=f)
        return r['n_bottom'], r['n_top']
    chk('#BF: ⚠ 경계가 3 미만이면 폴백(15/85 %)이 factor 를 **덮는다** — 작은 망에서는 무효',
        _tf(3.0) == _tf(0.5))

    print('NETWORK STATUS SELFTEST', 'PASS' if not fail else 'FAIL', f'({ok}/{ok + fail})')
    return 0 if not fail else 1


def _selftest_temp():
    """σ_grain(T) wiring — the DEM Kirchhoff solver's ionic prefactor.

    Key invariants: (a) SIGMA_BULK_DEFAULT is bitwise the old 3.0e-3 literal, (b) σ_e and κ
    prefactors are untouched, (c) σ_full (the dimensionless network answer) is T-INDEPENDENT
    by construction — temperature is a pure multiplicative prefactor on the mS/cm readout, so
    same-temperature relative comparisons (SBE vs DBE, composition trends) cancel it exactly.
    """
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'PASS' if cond else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}")

    chk('SIGMA_BULK_DEFAULT is bitwise 3.0e-3 (= the pre-2026-07-28 literal)',
        float(SIGMA_BULK_DEFAULT).hex() == (3.0e-3).hex(), float(SIGMA_BULK_DEFAULT).hex())
    chk('… and it IS the shared se_material constant',
        SIGMA_BULK_DEFAULT is se_material.SIGMA_GRAIN_S_CM_25C)
    chk('σ_e prefactor untouched (Reisacher: ohmic regime T-independent)',
        SIGMA_AM_ELECTRONIC == 0.05)
    chk('thermal prefactor untouched (no κ(T) anchor, §F1)', K_SE_THERMAL == 0.7e-2)
    chk('σ_grain_S_cm(None) is bitwise the default',
        float(se_material.sigma_grain_S_cm(None)).hex() == float(SIGMA_BULK_DEFAULT).hex())
    for t_c, want in ((30.0, 1.28), (45.0, 2.56), (60.0, 4.79)):
        f = se_material.sigma_grain_S_cm(t_c) / SIGMA_BULK_DEFAULT
        chk(f'--temp-c {t_c:.0f} → σ_grain x{want}', abs(round(f, 2) - want) < 5e-3, f'x{f:.4f}')
    # σ_full is dimensionless (σ/σ_bulk) → the reported mS/cm is exactly σ_full·σ_bulk·1000,
    # i.e. linear in the prefactor.  Same-T ratios cancel it.
    sf = 0.184341
    chk('mS/cm readout is exactly linear in σ_grain (same-T ratios cancel T)',
        abs((sf * se_material.sigma_grain_S_cm(60.0) * 1000)
            / (sf * SIGMA_BULK_DEFAULT * 1000) - se_material.arrhenius_sigma_factor(60.0)) < 1e-12)
    p_off, p_on = se_material.provenance(), se_material.provenance(60.0)
    chk('provenance OFF/ON contract', p_off['T_dependence'] == 'NOT_MODELLED'
        and p_on['T_dependence'] == 'ARRHENIUS' and p_on['T_ref_C'] == 25.0)
    print('NETWORK TEMP SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    import argparse
    if '--selftest-temp' in sys.argv:
        sys.exit(_selftest_temp())
    if '--selftest-status' in sys.argv:              # RC7-02 채널 상태 규약
        sys.exit(_selftest_status())
    if '--selftest' in sys.argv:                     # 둘 다 (사람이 제일 먼저 치는 이름)
        sys.exit(_selftest_temp() or _selftest_status())
    sys.path.insert(0, os.path.dirname(__file__))
    from analyze_contacts import load_atoms_raw, load_contacts_raw

    parser = argparse.ArgumentParser(description='DEM-Native Ionic Transport Solver')
    parser.add_argument('atoms_csv', help='atoms.csv path')
    parser.add_argument('contacts_csv', help='contacts.csv path')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-t', '--type-map', default='1:AM_S,2:SE', help='Type map')
    parser.add_argument('-s', '--scale', type=int, default=1000, help='Scale factor')
    parser.add_argument('--contact-mode', choices=['hertzian', 'physics', 'both'],
                        default='both',
                        help="Contact area model: 'hertzian' (DEM-native LIGGGHTS area), "
                             "'physics' (Tabor+volume, literature-anchored), "
                             "'both' (run each and emit *_hertzian/*_physics + dual JSON)")
    parser.add_argument('--dump-raw-dir', type=str, default=None,
                        help='If set, write per-edge/per-node raw CSV + solution JSON here')
    se_material.temperature_argparse(parser)   # --temp-c / --ea-ion-ev (both default None)
    args = parser.parse_args()

    # Parse type map
    type_map = {}
    for pair in args.type_map.split(','):
        k, v = pair.split(':')
        type_map[int(k)] = v.strip()

    target_types = [k for k, v in type_map.items() if v == 'SE']
    am_types     = [k for k, v in type_map.items() if 'AM' in v]

    atoms_raw, _    = load_atoms_raw(args.atoms_csv)
    contacts_raw, _ = load_contacts_raw(args.contacts_csv)
    print(f"Loaded {len(atoms_raw)} atoms, {len(contacts_raw)} contacts")

    mesh_file = os.path.join(args.output, 'mesh_info.json')
    if os.path.exists(mesh_file):
        with open(mesh_file) as f:
            plate_z = json.load(f)['plate_z']
    else:
        # Fallback: use max z of particle CENTERS (NOT z+radius). Adding the
        # radius overshoots the actual plate plane by one particle radius,
        # which makes z_top = plate_z - r_se×2 land above every SE center →
        # silent percolation=0 (observed for results/ cases missing
        # mesh_info.json). See dem_analysis_core.get_plate_z for matching fix.
        plate_z = max(a['z'] for a in atoms_raw.values())

    box_x, box_y = 0.05, 0.05
    ip_path = os.path.join(args.output, 'input_params.json')
    if os.path.exists(ip_path):
        with open(ip_path) as f:
            ip = json.load(f)
        box_x = ip.get('box_x', 0.05)
        box_y = ip.get('box_y', 0.05)

    print(f"box={box_x}×{box_y}, plate_z={plate_z:.6f}, scale={args.scale}")

    modes_to_run = (['hertzian', 'physics'] if args.contact_mode == 'both'
                    else [args.contact_mode])
    per_mode_results = {}
    for cm in modes_to_run:
        res = _run_all_networks(atoms_raw, contacts_raw, target_types, am_types,
                                 type_map, args.scale, plate_z, box_x, box_y,
                                 args.output, contact_mode=cm,
                                 dump_raw_dir=args.dump_raw_dir,
                                 temp_c=args.temp_c, ea_ion_ev=args.ea_ion_ev)
        per_mode_results[cm] = res
        if res:
            out_path = os.path.join(args.output, f'network_conductivity_{cm}.json')
            with open(out_path, 'w') as f:
                json.dump(res, f, indent=2)
            print(f"\nResults saved: {out_path}")
        else:
            # ★ F-12/F-05: 결과가 없으면 **파일을 안 쓰고도 exit 0** 이 됐다 — 호출부가
            #   rc 만 보면 성공으로 읽는다.  stderr 로 알리고 아래에서 nonzero 로 끝낸다.
            sys.stderr.write(f'[network] {cm}: 결과 없음 — 출력 파일을 쓰지 않았습니다 '
                             f'(물리망 부재 또는 solve 실패).\n')

    # Dual-view JSON (when both modes ran): elastic vs plastic side-by-side
    if len(per_mode_results) == 2 and all(per_mode_results.values()):
        rH = per_mode_results['hertzian']
        rP = per_mode_results['physics']
        def _ratio(a, b):
            try:
                return round(float(a) / float(b), 4) if (a and b and float(b) != 0) else None
            except Exception:
                return None
        dual = {
            'hertzian': rH,
            'physics':  rP,
            'ratio_physics_over_hertzian': {
                'sigma_full':        _ratio(rP.get('sigma_full'),        rH.get('sigma_full')),
                'sigma_constr_net':  _ratio(rP.get('sigma_constr_net'),  rH.get('sigma_constr_net')),
                'electronic_sigma_full': _ratio(rP.get('electronic_sigma_full'),
                                                rH.get('electronic_sigma_full')),
                'thermal_sigma_full':    _ratio(rP.get('thermal_sigma_full'),
                                                rH.get('thermal_sigma_full')),
            }
        }
        dual_path = os.path.join(args.output, 'network_conductivity_dual.json')
        with open(dual_path, 'w') as f:
            json.dump(dual, f, indent=2)
        print(f"Dual-view saved:  {dual_path}")

    # Back-compat: legacy filename points to Hertzian result (existing webapp reads this)
    if 'hertzian' in per_mode_results and per_mode_results['hertzian']:
        legacy_path = os.path.join(args.output, 'network_conductivity.json')
        with open(legacy_path, 'w') as f:
            json.dump(per_mode_results['hertzian'], f, indent=2)
        print(f"Legacy-compat:    {legacy_path}")

    # ★ F-12: 요청한 모드 중 하나라도 결과를 못 낸 경우 **nonzero 로 끝낸다**.
    #   옛 동작은 exit 0 이라, 파일이 없는데도 호출부가 성공으로 읽었다.
    _empty = [cm for cm, r in per_mode_results.items() if not r]
    if _empty:
        sys.stderr.write(f'[network] 결과를 내지 못한 모드: {", ".join(_empty)}\n')
        sys.exit(1)          # ★ 모듈 레벨(`if __name__`)이라 return 이 아니라 sys.exit
