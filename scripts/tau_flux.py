#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이온 망 인계 열 f · tau2 · tau — τ 결정 16 ② (봉인 밖 도우미 · 1저자 비준 2026-10-04 *"권고대로"*).

  python3 scripts/tau_flux.py <케이스 폴더>… [--tsv OUT] [--json OUT]     # 폴더 = network_conductivity_dual.json + full_metrics.json
  python3 scripts/test_tau_flux.py                                          # 시험 (게이트에 등록)

정본 = `docs/reviews/tau_conventions_judgment_v2_20261003.md` §5-1 (열 · 식) · §5-2 (게이트 G1–G6) · 결정 1 · 2 · 15 · 16.
모드 = `hertz` · `physics` (같은 정의 · 면적과 협착식만 다름).  상태 · 메타 키는 **모드 꼬리**를 단다 (10-04 비준 —
`ion_net_status_hertz` …).  σ₀ · 온도 · φ · L 기준은 두 모드 공통이라 꼬리가 없다.
★ 10-06 저녁 세대 2 (1저자 비준) — 셋째 모드 `hertz_h12` = Hertz 이온 **민감도** (ψ 곱 협착 + 구 조각 bulk · 같은 망 · 같은 전극 ·
Hertz 레코드 안 `hertz_h12` 에서 읽는다 · **기본 학습 열 아님** = 배포 부록).  모드마다 세대 표기 셋 (`ion_net_area_rule_<m>` ·
`ion_net_electrode_<m>` · `ion_net_bulk_<m>`) + 공통 세대 칸 `ion_net_generation` → 한 행 50 열 (모드 셋 × 15 + 공통 5) · ★ 10-16 L214R-02 부터 끝에
FULL 모형 한계 독립 표지 두 칸 (`full_model_limit_hertz` · `full_model_limit_physics`) → 52 열 (옛 50 열의 이름 · 자리는 그대로).
★ 10-06 밤 세대 계약 (Codex 세대 2 적대 리뷰 G2R-01 · G2R-02 · 1저자 비준) — 모드마다 허용 모델 조합을 **닫힌 표**로 본다 (`network_generation_contract` ·
`G2_MODE_CONTRACT` · `LEGACY_MODE_CONTRACT`): 세대 2 = 표기 전부 필수 (부분 결손 · 모르는 값 · H12 를 주 Hertz 자리에 = 거부) · 옛 세대 추론 =
세대 2 표지 (`G2_MARKER_KEYS`) 가 **하나도 없는** 레코드에만 (`inferred_legacy` 로 표지 — 이력 사실 physics_g1 · virtual_source_legacy · cylinder_half_d) ·
그 밖 = `invalid` (레코드 있는 모드 전부 NOT_COMPUTED invalid_input).  여러 폴더를 한 표로 낼 때 행마다 계약 먼저 (`row_generation_problems`) ·
그다음 세대 섞임 (`generation_mixing_problem` · CLI rc 2) — 같은 결함만 모인 코호트도 거부한다.  웹앱 망 정지 계약 ⑨ · 공용 기록 검사 · 인계 생성기 ·
배포 빌더가 같은 함수를 부른다.
★ 10-06 밤 G2RR-02 (Codex 세대 2 재검증 §3 · §7-2 · 1저자 비준) — 세대 2 계약이 수치 증서의 **결합**까지 본다 (`certificate_binding_problems` · 종류 'cert'):
가지 · 채널 · 역할 · 전극 · ΔV · 봉인된 기하 (G→q) 대조 + 발행 σ_ratio · σ_dim 을 증서의 I_bottom/ΔV × T/A 로 저장 반올림 반폭 안에 재구성 · 숫자를 싣는
CF · 협착-only 진단도 같은 검사 · 해 없는 가지는 증서를 요구하지 않는다 (상태 ↔ 증서가 해를 주장하지 않는가만) — 정책 표 `CERT_BRANCH_POLICY`.
★ 10-07 Codex 세대 2 재검증 2 (§5 G2RR2-04 · §6 G2RR2-05 · 1저자 "해결해놔") — 같은 계약이 σ₀ 결합 (`sigma0_binding_problems` — 이온 세 가지 증서 σ₀ =
부모 σ₀ · 부모 σ₀ = 그 레코드의 온도 규약 · 전자 · 열 증서 = 그 채널 기준 전도도 · 정지 계약 ⑧ 도 같은 함수) 과 가지 표 (`branch_table_problems` — 정직한
실패 = 숫자 없음 + 상태 + 사유 ↔ 상태 기록 통째 결손 = 거부 · 다시 읽기 K7 이 이 결과를 그대로 쓴다) 를 본다.  CF · 협착-only 차원값은 부모 σ₀ 로 재구성한다.

| 열 | 식 |
|---|---|
| `f_ion_<m>` | f_mc = σ_ratio × (L_gap / L_mc) — σ_ratio = 솔버 무차원 `sigma_full` (8 자리 · `TAU-25`) · **판 간격 해의 질량보존 두께 재척도 (해 아님)** |
| `f_ion_<m>_gap` | σ_ratio 그대로 — φ_mc 와 짝짓지 말 것 (T 를 L_gap/L_mc 배 낮춘다) |
| `tau2_ion_<m>` | T = φ_SE,mc / f_mc (= φ_구합 / σ_ratio — 현행 웹앱 T 와 정의상 같은 수 · 자기상사 가정) · tortuosity factor |
| `tau_ion_<m>` | √T — **COMSOL 입력 아님** |

게이트 (먼저 걸린 것 하나만 — 순서 = 아래 표):
| 순서 | 게이트 | 실패 시 |
|---|---|---|
| (폴더) | ★ 세대 (10-05 RGLR2-02) — 케이스 폴더 (`case_row` · 웹앱 `_ion_handover`) 의 망 활성 세대가 확정되지 않음 (`network_generation_problem`: full_metrics ↔ 도장 불일치 · 되돌림 실패 기록 · 중단된 게시 흔적 · 도장 손상) — 아래 게이트 결과를 덮는다 | `NOT_COMPUTED` (`generation_invalid: 세부` · 두 모드 · 값 빈칸) |
| 0 | 그 모드의 망 결과 · 장부 (L_gap · L_mc · φ_mc) · calc_percolation 값이 있다 · 띠 규칙 기록이 있다 (안 A · 기록 없는 옛 산출물은 짐작하지 않는다) | `NOT_COMPUTED` (`missing_input`) |
| 0b | ★ 공용 기술 검사 `ion_record_problem` (10-05 RGLR-01 · 02) — 상태 ↔ 값 (computed = σ 두 표현 유한 양수 · 관통 분율 (0, 1] · 두 표현 항등식 · valid_zero = RGL-02 의 증명된 비관통 조합만 · 그 밖 = 생산자 계약 밖) | `NOT_COMPUTED` (`invalid_input: 세부` · 생산자 not_computed 신고면 `solver_guard`) |
| 0c | ★ 세대 계약 `network_generation_contract` (10-06 밤 G2R-01 · 02) — 케이스 전체: 모드마다 허용 모델 조합 (닫힌 표) · 세대 2 표기 전부 필수 · 옛 세대 추론은 표지가 하나도 없을 때만 | `NOT_COMPUTED` (`invalid_input: 세대 계약 (G2R-01 · 02): 세부` · 레코드 있는 모드 전부 · 세대 칸 invalid) |
| 1 | G1 띠 = 솔버 기록 `boundary_rule` 이 L0 | `BAND_FALLBACK` |
| 2 | G2 솔버 관통 (`percolating_fraction > 0`) == calc_percolation (`percolation_pct > 0`) — 판정은 관통 분율로 한다 (`TAU-22` · 상태 ↔ 값 정합은 0b 가 먼저 본다) | `NOT_COMPUTED` (`percolation_disagree`) |
| 3 | G4 온도 짝 — 그 모드의 σ₀ · T 기록이 있다 (없으면 `missing_input`) · 두 모드의 (σ₀, T) 가 같다 · 호출자가 σ₀ 의 T 를 주장하면 망 T 와 같다 | `NOT_COMPUTED` (`temperature_mismatch`) |
| 4 | G3 비관통 (G1 · G2 통과 + 관통 성분 없음) | `NOT_PERCOLATING` — f = 0 · tau2 · tau 빈칸 (= ∞) |
| 5 | 관통인데 σ 가 없거나 0 · 음수 · 비유한 (0b 뒤에는 도달하지 않는 방어) | `NOT_COMPUTED` (`solver_guard`) — ★ 10-15 L214: 0b 의 공용 판정이 확인한 FULL 모형 한계면 `NOT_COMPUTED` (`full_over_conduction`) |
| 5b | ★ 10-16 L214R-09 — 게시할 f · tau2 · tau 가 셋 다 유한 양수 (값 상태 OK · MBCB 를 주기 전 · 넘침 · 밑넘침 · 0 나누기 — 밑정규 σ_ratio · 장부 극값) | `NOT_COMPUTED` (`invalid_input: non_finite — 세부` · 기술적 실패 · 값 빈칸 · 유한한 극값은 그대로) |
| 6 | G5 f > φ (T < 1) | `MODEL_BELOW_CONTINUUM_BOUND` — **값 유지** + 표지 (빈칸으로 거르면 코퍼스를 T ≥ 1 쪽으로 선별한다) |
G6 (협착 세대) = 메타 `ion_net_constriction_<m>` · 두 모드 모두 **물리 타깃 (실험 절대 대조) HOLD** — 값은 싣는다.
상태 부류 (10-05 RGLR-01): `NOT_COMPUTED` = **기술적 실패** (입력 결손 · 무효 · 솔버 관문 · 온도 짝 · 관통 불일치 · 세대 무효 (RGLR2-02) — 값 없음) ↔ `BAND_FALLBACK` ·
`NOT_PERCOLATING` · `MODEL_BELOW_CONTINUUM_BOUND` = **등록된 과학적 HOLD** (입력은 0b 를 통과한 유효값 · 규칙대로 빈칸 또는 표지).
★ 10-15 L214 (Codex LHS214 판정 §2 · 1저자 10-14 비준 Q1–Q5) — 셋째 부류 **FULL 모형 한계** = `NOT_COMPUTED` + 사유 정확히 `full_over_conduction`
(`is_model_limit_status`) · 기술 실패 아님 · 값 빈칸 (거부된 q · 수치 증서 = 레코드의 증서) · 공용 판정 `full_model_limit_problem` (생산자 · 게시 · 정지 계약 ·
다시 읽기 · 인계 · 배포가 같은 함수) 을 통과한 레코드만 (사유만 위조 · 증서 결손 · 남의 증서 · 틀린 q 재구성 = invalid_input).  앞 게이트 (띠 · 관통 불일치 · 온도 짝) 우선.
★ 10-16 L214R-02 (Codex LHS214 재검증 §3 · 수정 계획 Q2 · 1저자 10-16 비준 "권고대로") — 위 표시 우선순위는 그대로 두고 FULL 모형 한계 **사실**을 상태와 따로
독립 표지 두 칸 (`MODEL_LIMIT_FLAG_COL` · `full_model_limit_flag`) 으로 싣는다: 표지 = 그 모드 레코드가 공용 판정 `full_model_limit_problem` 을 통과한 모형 한계인가 —
띠 규칙 · 앞 게이트와 무관.  옛 판은 L1 · L2 띠에서 상태가 BAND_FALLBACK (사유 공란) 이 되며 그 사실이 사라져, 상태만 읽는 배포 관문 (주 타깃 H0 HOLD) 이
L1 · L2 + H0 모형 한계 행을 배포했다 (Codex 반례 · 27 파일 · check 문제 0).  배포 build · check 는 이 칸으로 HOLD 한다 (`lhs_release_build`).  H12 표지 칸은 없다 (1저자 Q2 = 두 칸).
⚠ 옛 판은 0b 가 없어 L1/L2 레코드가 G1 에서 바로 BAND_FALLBACK 로 돌아갔다 — computed 인데 σ_ratio None · NaN · −1 · 관통 분율 2 가 '과학적 HOLD'
로 통과했고 (RGLR-01), σ_ratio 만 ×4 인 레코드는 tau2 ÷4 로 OK 였다 (RGLR-02).

⚠ `ion_net_basis_check_<m>` 는 **메타**다 (게이트 아님): 망 φ (`phi_se`, 4 자리 · 판 간격 상자 · 구 부피 합) 가 장부의
φ_mc·L_mc/L_gap (= φ_구합) 와 같은지 본다 — 어긋나면 망과 장부가 다른 판 높이 · 상자 · SE 집합을 썼다는 뜻이다.
게이트로 쓰려면 새 규칙으로 등록한다 (v2 §5-2 G5 의 "새 규칙" 규약 · 1저자).
⚠ 한정어는 열 사전 (v2 §5-3) 이 정본이다 — 협착 세대 (hertz = 1세대 반공간 Maxwell · physics = 10-06 부터 세대 2 ψ 곱셈 ·
그 전 산출물은 세대 1 ψ 분모 — 행마다 `ion_net_constriction_<m>` · `ion_net_psi_<m>`) · ML 기술자 전용 · 실험 절대 대조 금지 ·
τ_e (Nguyen Eq 2) 아님 · 'COMSOL 입력' 은 GUI Equation 확인 전 쓰지 않는다.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys

#: ★ 10-06 세대 2 (C1-3 · 1저자 비준) — 세 번째 모드 `hertz_h12` = Hertz 이온 **민감도** 레코드 (ψ 곱 협착 + 구 조각 bulk · 같은 망 · 같은 전극).
#:   생산자 (`network_conductivity._run_all_networks` hertzian) 가 Hertz 레코드 **안** `hertz_h12` 로 싣는다 (모드 파일 · legacy · dual 이 같은 사본) →
#:   `mode_record` 가 거기서 읽는다.  **기본 학습 열이 아니다** (배포 = 민감도 부록 · 행마다 H0 와 짝인 두 규약의 시나리오 — 구간 · 괄호 아님 · Codex G2R-04) — 주 값은 hertz (H0) 그대로.
MODES = ('hertz', 'physics', 'hertz_h12')
DUAL_KEY = {'hertz': 'hertzian', 'physics': 'physics'}
H12_MODE = 'hertz_h12'
#: 세대 표기 (값 = network_conductivity 상수와 같은 문자열 — 무거운 생산자를 임포트하지 않으려고 둔다 · test_network_generation2 E1 · E2 ·
#:   test_gen2_role_contract T1 이 대조).  표기 없는 옛 레코드 = 이력 사실: 10-06 전 솔버는 늘 가상 전원 전극 · 원기둥 bulk · physics 면적 세대 1
#:   이었다 (짐작이 아니다 — ψ 기록 없는 mikic = 세대 1 과 같은 규약).  ★ 10-06 밤 (G2R-02) — 그 추론은 세대 2 표지가 **하나도 없는** 레코드에만
#:   (`network_generation_contract` = inferred_legacy) — 옛 판은 빈 칸이면 늘 채워 세대 2 physics 의 면적 · ψ 삭제를 세대 1 로 읽었다.
ELECTRODE_LEGACY = 'virtual_source_legacy'
ELECTRODE_G2 = 'dirichlet_exact'
AREA_RULE_HERTZ = 'hertz_ccpl22'
AREA_RULE_PHYSICS_G1 = 'physics_g1'
AREA_RULE_PHYSICS_G2 = 'physics_g2'
BULK_CYLINDER = 'cylinder_half_d'
BULK_SPHERE_SEGMENT = 'sphere_segment'
PSI_LEGACY = 'legacy_divide'
PSI_G2 = 'multiply'


def mode_record(dual, m):
    """dual (`network_conductivity_dual.json`) 에서 모드 하나의 망 레코드 — hertz · physics = 그 키 · hertz_h12 = Hertz 레코드 안 `hertz_h12`.
    없거나 객체가 아니면 None."""
    if not isinstance(dual, dict):
        return None
    if m == H12_MODE:
        rh = dual.get(DUAL_KEY['hertz'])
        rec = rh.get(H12_MODE) if isinstance(rh, dict) else None
    else:
        rec = dual.get(DUAL_KEY.get(m, m))
    return rec if isinstance(rec, dict) else None
STATUSES = ('OK', 'NOT_PERCOLATING', 'BAND_FALLBACK', 'MODEL_BELOW_CONTINUUM_BOUND', 'NOT_COMPUTED')
#: 사유 **코드** — 사유 칸은 코드 그대로이거나 '코드: 세부' (세부를 다는 코드 = invalid_input · generation_invalid · 코드는 `reason_code`).
#:   ★ 10-05 RGLR-01: invalid_input = 공용 기술 검사 (`ion_record_problem`) 가 생산자 계약 위반으로 본 레코드.
#:   ★ 10-05 RGLR2-02 (Codex 3차 재검증): generation_invalid = 케이스 폴더의 망 활성 세대가 **확정되지 않았다** (`network_generation_problem` —
#:     full_metrics ↔ 도장 불일치 · 되돌림 실패 기록 · 중단된 게시 흔적 · 도장 손상) — 읽는 쪽 fail-closed (기술적 실패 부류 · 재실행 필요).
REASONS = ('solver_guard', 'missing_input', 'temperature_mismatch', 'percolation_disagree', 'invalid_input', 'generation_invalid')
INVALID_INPUT = 'invalid_input'
GENERATION_INVALID = 'generation_invalid'
#: ★ 10-15 L214-01 · 02 (Codex LHS214 판정 §2 · §4 A1 · 1저자 10-14 비준 Q1–Q5 권고대로) — **FULL 모형 한계** (수치 인증 성공 / 출력 채택 거부) 의 사유.
#:   기술 실패 사유 (REASONS) 가 **아니다** — 상태 NOT_COMPUTED · 사유 정확히 이 값 (세부 꼬리 없음 · `is_model_limit_status`) 이면 그 모드의 단상 FULL q 가
#:   사전 고정 출력 상한 1.5 를 넘어 값 (f · tau2 · tau · f_gap) 을 내지 않은 것이고, 그 레코드는 공용 판정 `full_model_limit_problem` 을 통과했다 (0b 가
#:   확인 — 사유만 위조 · 증서 결손 · 남의 증서 · 틀린 q 재구성 = invalid_input).  값 = 생산자 상수와 같은 문자열 (무거운 생산자를 임포트하지 않으려고 둔다 ·
#:   test_lhs214_model_limit T6 이 대조).
MODEL_LIMIT_REASON = 'full_over_conduction'           # = network_conductivity.FULL_OVER_CONDUCTION_REASON
CHANNEL_MODEL_LIMIT = 'model_limit'                   # = network_conductivity.CHANNEL_MODEL_LIMIT (채널 상태)
#: ★ 10-16 L214R-02 (Codex LHS214 재검증 §3 · 수정 계획 Q2 · 1저자 10-16 비준) — FULL 모형 한계 **독립 표지** 인계 칸 (모드 → 열 이름 · 값 = `full_model_limit_flag` ·
#:   직렬화 `_cell` = 'True' · 'False' · 레코드 없음 · 세대 무효 = 빈칸).  상태 칸은 앞 게이트 우선 (띠 L1 · L2 = BAND_FALLBACK · 사유 공란) 이라 모형 한계 사실을
#:   덮는다 — 이 칸이 띠 규칙과 무관하게 그 사실을 보존하고, 배포 build · check (`lhs_release_build.V13_MODEL_LIMIT_FLAG` — 같은 이름 · test_l214r02 D8 이 대조) 가
#:   주 타깃 (hertz = H0) 표지로 HOLD 한다.  H12 는 칸이 없다 (1저자 Q2 = 두 칸 · H12 = 민감도 부록 정책 그대로).
MODEL_LIMIT_FLAG_COL = {'hertz': 'full_model_limit_hertz', 'physics': 'full_model_limit_physics'}


def is_model_limit_status(status, reason):
    """τ 인계 상태 · 사유 칸 → FULL 모형 한계인가 (NOT_COMPUTED · 사유 정확히 full_over_conduction — 세부 꼬리 · 다른 상태 = 아니다)."""
    return status == 'NOT_COMPUTED' and reason == MODEL_LIMIT_REASON
#: 협착식 라벨 (G6 세대 메타 `ion_net_constriction_<m>`) — 저항 모델 **과 결과의 ψ 배치**로 정한다 (`constriction_label`).
#:   ★ 10-06 (`L2-01` 세대 2 · 1저자 개정) — physics 기본이 ψ 곱셈이 됐다.  resistance_model 만 보면 세대 1 · 2 가 같은 'mikic' 이라
#:   라벨이 세대를 거짓으로 말한다 ⇒ physics (mikic) 는 결과의 `psi_placement` 를 따른다 (값 = network_conductivity.PSI_* 와 같은 문자열 ·
#:   무거운 생산자를 이 도우미에서 임포트하지 않으려고 값을 둔다 — test_psi_default_switch ⑤ 가 대조한다).
#:   ψ 기록이 없는 mikic = 2026-09-15 깃발 도입 전 산출물 = 세대 1 — 그 전 코드는 처음 반입 (04-24) 부터 늘 분모였고 깃발 도입은 비트 동일이었다
#:   (감사 audit_transport_cap_equivalence ⑦f) ⇒ 짐작이 아니라 이력 사실이다.  모르는 ψ 값 = 'unknown:mikic/<값>'.
CONSTRICTION = {'maxwell': 'maxwell_halfspace', 'mikic': 'mikic_psi_divide'}      # mikic = ψ 기록 없는 결과 (세대 1) 의 라벨
PSI_CONSTRICTION = {'legacy_divide': 'mikic_psi_divide', 'multiply': 'mikic_psi_multiply'}
BAND_RULES = ('L0', 'L1', 'L2')
PHI_TOL = 5e-5 + 1e-9          # 망 φ 는 4 자리 반올림 (network_conductivity `round(phi_se, 4)`) — 반폭 + 부동소수 여유
#: 행의 망 세대 칸 (세 모드 공통 · 10-06 밤 G2R-02) — g2 · inferred_legacy (옛 세대 **추론**) · invalid (세대 계약 위반) · '' (레코드 없음)
ROW_GENERATION_COL = 'ion_net_generation'
SHARED = ('ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis', ROW_GENERATION_COL)
#: 생산자 (`network_conductivity.NO_THROUGH_REASON`) 의 증명된 비관통 사유 — 같은 값이어야 한다 (test_tau_flux L8 이 대조한다 · 무거운 생산자를
#:   이 도우미에서 임포트하지 않으려고 값을 둔다 — `pipeline_service.NETWORK_NO_THROUGH_REASON` 과 같은 방식).
NO_THROUGH_REASON = 'no_through_path'


def reason_code(reason):
    """사유 칸 → 사유 코드 ('invalid_input: σ_ratio None' → 'invalid_input' · '' → '')."""
    return str(reason or '').split(':', 1)[0].strip()


def constriction_label(res, legacy=False):
    """망 결과 한 모드 → 협착식 라벨 (G6 세대 메타).  hertz (maxwell) = maxwell_halfspace · physics (mikic) = 결과의 ψ 배치
    (multiply → mikic_psi_multiply · legacy_divide → mikic_psi_divide · 모르는 값 → unknown:mikic/<값>) · 모르는 저항 모델 → unknown:<이름> ·
    결과 없음 → ''.  ψ 기록 없음 → legacy=True (케이스가 옛 세대로 추론됨 — 09-15 깃발 전 = 세대 1) 면 mikic_psi_divide · 아니면 unknown:mikic/None
    (★ 10-06 밤 G2R-02 — 세대 2 표지가 남은 레코드의 빈 ψ 를 세대 1 로 읽지 않는다)."""
    rm = (res or {}).get('resistance_model')
    if rm is None:
        return ''
    if rm == 'mikic':
        psi = (res or {}).get('psi_placement')
        if psi is None and legacy:
            return CONSTRICTION['mikic']
        return PSI_CONSTRICTION.get(psi, f'unknown:mikic/{psi}')
    return CONSTRICTION.get(rm, f'unknown:{rm}')


def _num(v):
    """유한한 수 (bool 제외) 면 float, 아니면 None.
    ★ 10-16 L214R-08 — float 로 못 옮기는 큰 정수 (JSON 정수 10⁴⁰⁰ — json.loads 가 int 로 준다) 도 None (OverflowError 를 내지 않는다 · 생산자
    `network_conductivity._cert_num` 의 L214R-01 A 와 같은 규칙).  부르는 자리는 None 을 거부 사유 (공용 기술 검사 · 증서 결합 · σ₀ 결합 · 온도 규약 · 모형 한계 ·
    τ 게이트 0 · G4) 또는 값 없음 (표시 메타 · 등급 τ getter) 으로 읽는다 — None 을 '숫자 없음 = 받음' 으로 읽는 자리 (숫자 없는 가지 증서의 I_bottom) 는
    `_overflow_int` 로 '숫자가 실렸다' 를 따로 본다 (변환 불가 = 기술 실패 · 없음으로 읽지 않는다)."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    try:
        v = float(v)
    except OverflowError:                          # ★ L214R-08 — 큰 정수의 float 변환 넘침 = 유한 실수가 아니다 (예외 대신 None · 자리마다 사유)
        return None
    return v if math.isfinite(v) else None


def _overflow_int(v):
    """★ 10-16 L214R-08 — float 로 못 옮기는 정수 (bool 제외 — JSON 10⁴⁰⁰) 인가.  `_num` 은 이 값을 None 으로 주므로, None 을 '숫자 없음' 으로 읽는 자리가
    이 함수로 **숫자가 실렸다** 는 사실을 따로 본다 (`_cert_unpublished_problem` — 숫자 없는 가지 증서의 I_bottom = 해 주장)."""
    if isinstance(v, bool) or not isinstance(v, int):
        return False
    try:
        float(v)
    except OverflowError:
        return True
    return False


def _pos(v):
    v = _num(v)
    return v if v is not None and v > 0 else None


#  ── 공용 기술 검사 (10-05 RGLR-01 · 02 · Codex 재검증 §2 · §3 · 1저자 비준) ─────────────────────────────────────────────────────
#  network 정지 계약 (`webapp/pipeline_service.network_stop_verdict` ③) 과 τ 인계 소비자 (`ion_columns`) 가 **이 함수 하나**를 쓴다 (규율 ① —
#  옛 판은 정지 계약이 σ_dim 양수 · 관통 분율 > 0 만, 소비자가 σ_ratio 만 따로 보아 둘이 서로 다른 입력을 받았다).  과학적 게이트 앞에서 돈다.
#
#  ★ RGLR-02 — 두 σ 표현 항등식의 허용 (생산자 `network_conductivity.run_decomposition` 의 저장 정밀도에서 유도 · 새 물리 허용오차가 아니다):
#    생산자는 **같은 반올림 전 값** q* (FULL 해의 σ_eff/σ_bulk) 에서
#        q    = round(q*, 8)                           (`sigma_full`)
#        σ_d  = round(q* × s₀ × 1000, 6)  [mS/cm]       (`sigma_full_mScm` · s₀ = `sigma_grain_S_cm` [S/cm] = 간선 σ 그대로)
#    를 쓴다.  ⇒  |σ_d − 1000·s₀·q| ≤ |σ_d − 1000·s₀·q*| + 1000·s₀·|q* − q| ≤ 5e-7 + 1000·s₀·5e-9  (각 반올림 반폭) + 부동소수 여유.
#    부동소수 여유 = 16·ε·(|σ_d| + 1000·s₀·|q|) — 생산자 곱 (q*·s₀)·1000 의 두 번 반올림 · numpy `round` 의 (×10ⁿ · rint · ÷10ⁿ) 구현 오차
#    (|x| 의 수 ε) · 소비자 쪽 곱 1000·s₀·q 의 반올림을 덮는다 (ε = 2.22e-16 · 16 배는 넉넉한 상한 — 경계 5e-7 의 1e-9 배 수준).
#    s₀ 는 **반올림 없이** 실린다 (`results['sigma_grain_S_cm'] = sigma_bulk_ion` = se_material.sigma_grain_S_cm(T, Ea) 그대로 · JSON 은 float repr
#    왕복이라 비트 동일) — 25 °C 상수 3e-3 이든 Arrhenius 변환값이든 σ_d 를 만든 바로 그 수다 ⇒ s₀ 반올림 항은 없다 (그 키를 낸 유일한 커밋
#    d66fd1448 (07-28 온도 축) 부터 반올림 없음 · 그 전 세대는 키가 없어 검산 불가 = invalid_input · σ_d 의 6 자리 식은 04-24 반입 때부터 그대로 —
#    `git log -S` 로 확인).  ⚠ 소비자의 σ₀ 메타 (`ion_sigma0_mScm` = round(s₀·1000, 10)) 와
#    웹앱 짝 σ₀ (`se_material.sigma_grain_context` = 3.0 × factor) 는 이 검산에 쓰지 않는다 — 생산자가 곱한 s₀ 와 다른 반올림을 가진다.
#    두 τ 를 늘 같게 강제하지 않는다 (8 · 6 자리 반올림 차 · 기준 변환은 오차가 아니다 — Codex §3).
SIGMA_RATIO_ROUND_HALF = 5e-9      # σ_ratio = round(·, 8) 의 반폭
SIGMA_DIM_ROUND_HALF = 5e-7        # σ_dim [mS/cm] = round(·, 6) 의 반폭
_ID_FP = 16 * sys.float_info.epsilon


def sigma_identity_tol(sigma0_S_cm, sigma_ratio, sigma_dim):
    """두 σ 표현 항등식 |σ_dim − 1000·s₀·σ_ratio| 의 허용 [mS/cm] (위 유도 · 생산자 저장 정밀도)."""
    s0, q, sd = abs(float(sigma0_S_cm)), abs(float(sigma_ratio)), abs(float(sigma_dim))
    return SIGMA_DIM_ROUND_HALF + 1000.0 * s0 * SIGMA_RATIO_ROUND_HALF + _ID_FP * (sd + 1000.0 * s0 * q)


def ion_record_problem(rec):
    """망 레코드 (모드 하나 · dual 의 'hertzian' 또는 'physics') 의 **기술적 입력 유효성** → None (유효) | (사유 코드, 세부).

      computed     σ_ratio (`sigma_full`) · σ_dim (`sigma_full_mScm`) 둘 다 유한 양수 · 관통 분율 (0, 1] · s₀ (`sigma_grain_S_cm`) 유한 양수 ·
                   두 표현 항등식 (`sigma_identity_tol` — ★ 10-16 L214R-07 곱 · 차 · 허용을 비교 전에 유한으로 · 넘침 · 밑넘침 = non_finite 사유)
      valid_zero   RGL-02 의 증명된 비관통 조합만 — 사유 no_through_path · σ_ratio · σ_dim None (F-12) · 관통 분율 0 · CF · constr 상태 valid_zero ·
                   이온 채널 valid_zero  (정지 계약 ③ 과 같은 조합 — 'zero_value' 같은 다른 valid_zero 는 받지 않는다)
      not_computed 생산자가 "관통인데 풀지 못함" 을 신고했다 → ('solver_guard', 사유)  — 기술적 실패
                   ★ 10-15 L214 — 단, 사유가 정확히 full_over_conduction (FULL 모형 한계) 이면 공용 판정 `full_model_limit_problem` 을 부른다: 통과 =
                   None (유효 입력 — 값 없음은 그 범주가 정한다 · 소비자는 NOT_COMPUTED full_over_conduction 으로 싣는다) · 실패 = ('invalid_input', …)
                   (사유만 위조 · 증서 결손 · 남의 증서 · 틀린 q · 남은 값 = 기술 실패).  모르는 사유 · 오타 = solver_guard 그대로.
      그 밖        (None · 키 없음 · 모르는 문자열 · 채널 어휘) → ('invalid_input', …)
    띠 규칙 (L0 · L1 · L2) 과 **무관하게** 같은 판정이다 — L1/L2 라는 이유로 무효값 검사를 건너뛰지 않는다 (RGLR-01).  과학적 HOLD (띠 폴백 ·
    비관통 · 연속체 하한) 의 허용은 그대로 — 이 검사를 통과한 유효 입력에서만 그 게이트로 간다."""
    if not isinstance(rec, dict):
        return INVALID_INPUT, f'망 레코드가 객체가 아니다 ({type(rec).__name__})'
    st = rec.get('sigma_full_status')
    q, sd, pf = rec.get('sigma_full'), rec.get('sigma_full_mScm'), rec.get('percolating_fraction')
    if st == 'computed':
        #  ★ 10-16 L214R-08 — float 로 못 옮기는 큰 JSON 정수 (σ 두 표현 · 관통 분율 · σ₀) = `_num` None → 아래 사유 (예외 아님 · 거부)
        why = []
        if _pos(q) is None:
            why.append(f'σ_ratio (sigma_full) {q!r} — 유한 양수여야')
        if _pos(sd) is None:
            why.append(f'σ_dim (sigma_full_mScm) {sd!r} — 유한 양수여야')
        pfn = _num(pf)
        if pfn is None or not (0.0 < pfn <= 1.0):
            why.append(f'관통 분율 {pf!r} — (0, 1] 밖')
        s0 = _pos(rec.get('sigma_grain_S_cm'))
        if s0 is None:
            why.append(f'σ₀ (sigma_grain_S_cm) {rec.get("sigma_grain_S_cm")!r} — 없거나 양수가 아니어서 두 표현 항등식을 검산할 수 없다')
        if why:
            return INVALID_INPUT, 'computed 인데 ' + ' · '.join(why)
        #  ★ 10-16 L214R-07 (Codex 재검증 뒤 같은 부류 Q5 · L214R-01 A · 05 와 같은 규칙) — 1000·σ₀·σ_ratio · |차| · 허용을 비교 **전에** 본다: 곱은 유한 양수 · |차| ·
        #    허용은 유한.  옛 판은 σ_ratio 1e308 · σ_dim 1.0 (σ₀ 3e-3) 에서 곱이 +∞ 로 넘쳐 |차| = 허용 = +∞ 이고 inf ≤ inf 가 참이었다 — 세대 2 는 증서 결합이
        #    따로 막지만 증서 없는 옛 세대 레코드 (inferred_legacy) 는 역사 인계 · τ 행에서 f_ion = ∞ · tau2 = 0 으로 나갔다 · 곱이 0 으로 밑넘치면 절대 반폭 5e-7
        #    뒤에 숨는다.  넘침 · 밑넘침 = 기술 실패 사유 (생산자 NON_FINITE_REASON 꼬리표) — 정상 레코드는 식 · 순서 · 허용 · 판정 그대로
        #    (생산자 값이면 곱 ≥ 1000·σ₀·1e-8 > 0 · 둘 다 작은 유한수)
        prod = 1000.0 * s0 * q
        d, tol = abs(sd - prod), sigma_identity_tol(s0, q, sd)
        if not (math.isfinite(prod) and prod > 0 and math.isfinite(d) and math.isfinite(tol)):
            return INVALID_INPUT, (f'{_nc_mod().NON_FINITE_REASON} — 두 σ 표현 항등식 (RGLR-02) 을 비교할 수 없다: 1000·σ₀·σ_ratio = {prod!r} · |차| {d!r} · 허용 '
                                   f'{tol!r} (곱 = 유한 양수 · 차 · 허용 = 유한이어야 — 넘침 · 밑넘침 · σ_ratio {q!r} · σ_dim {sd!r} · σ₀ {s0!r} · 생산자 저장 범위 밖 · '
                                   'inf ≤ inf 를 같다로 읽지 않는다)')
        if not d <= tol:
            return INVALID_INPUT, (f'두 σ 표현 불일치 (RGLR-02): σ_dim {sd!r} mS/cm ≠ 1000·σ₀·σ_ratio = {prod!r} '
                                   f'(|차| {d:.6g} > 허용 {tol:.6g} — 저장 정밀도 8 · 6 자리 반올림 밖)')
        return None
    if st == 'valid_zero':
        why = []
        if rec.get('sigma_full_reason') != NO_THROUGH_REASON:
            why.append(f'사유 {rec.get("sigma_full_reason")!r} ≠ {NO_THROUGH_REASON!r}')
        if q is not None or sd is not None:
            why.append(f'σ 숫자 필드가 None 이 아니다 (σ_ratio {q!r} · σ_dim {sd!r})')
        if _num(pf) != 0.0:
            why.append(f'관통 분율 {pf!r} (0 이어야)')
        if not (rec.get('sigma_bulk_net_status') == rec.get('sigma_constr_net_status') == 'valid_zero'):
            why.append(f'CF · constr 상태 ({rec.get("sigma_bulk_net_status")!r}, {rec.get("sigma_constr_net_status")!r})')
        if rec.get('ionic_status') != 'valid_zero':
            why.append(f'이온 채널 {rec.get("ionic_status")!r}')
        if why:
            return INVALID_INPUT, 'valid_zero 인데 증명된 비관통 (RGL-02) 조합이 아니다 — ' + ' · '.join(why)
        return None
    if st == 'not_computed':
        if rec.get('sigma_full_reason') == MODEL_LIMIT_REASON:             # ★ 10-15 L214 — 모형 한계 주장은 공용 판정으로만 받는다 (이름만으로 아님)
            mp = full_model_limit_problem(rec, 'ionic')
            if mp is None:
                return None
            return INVALID_INPUT, f'FULL 모형 한계 주장이 공용 판정을 못 넘는다 (L214-01 · 02): {mp}'
        return 'solver_guard', f'생산자 not_computed ({rec.get("sigma_full_reason")!r}) — 관통인데 σ 를 못 냈다'
    return INVALID_INPUT, f'sigma_full_status={st!r} — 생산자 계약 밖 (computed · valid_zero · not_computed 만)'


#  ── ★ 10-15 L214-01 · 02 — FULL 모형 한계의 공용 판정 (Codex LHS214 판정 §2 · §4 A1 최소 처방 · 1저자 10-14 비준 Q1–Q5 권고대로) ──────────────────
#  "수치 인증 성공 / 출력 채택 거부" 를 명시 범주로 — 생산자 (`network_conductivity._net_sigma_status` · `_channel_solve_failure` 가 증서 수준 판정
#  `model_limit_certificate_problem` 으로만 이 범주를 낸다) 와 소비처 전부 (일반 게시 · 정지 계약 — `pipeline_service.channel_verdict` · `network_stop_verdict` ·
#  `network_record_verdict` · τ 0b `ion_record_problem` · 세대 계약 `certificate_binding_problems` · 다시 읽기 K6 · 인계 P4 · 배포) 가 **이 함수 하나**를 쓴다 (규율 ①).
#  옛 판의 구멍 (Codex 반례 · 우리 시험 test_lhs214_model_limit): FULL q > 1.5 가 solve_failed 로 뭉개져 Hertz 포함 레코드 전체 차단 (10-14 실패 14 건) ·
#  plate_z = +∞ 가 같은 가드 사유 · 이름만 허용목록에 넣으면 실패 레코드의 검사 면제 (CF 증서 · 세대 필드 · 숫자 없는 가지 증서) 를 새 범주가 상속.
_ML_CHANNEL_PREFIX = {'ionic': '', 'electronic': 'electronic_'}
_ML_CPS_TAIL = {'ionic': 'ion', 'electronic': 'el'}
#: 채널마다 FULL 에서 유도되는 비 (FULL 값이 없으면 없어야 한다) — 생산자 run_decomposition 의 R_brug_over_full (CF/FULL) · R_bruggeman_over_full ·
#:   전자 = 이온 중심 결과로 올린 electronic_R_brug.
_ML_DERIVED = {'ionic': ('R_brug_over_full', 'R_bruggeman_over_full'), 'electronic': ('electronic_R_brug',)}


def record_mode(rec):
    """망 레코드 한 모드 → 그 레코드가 말하는 역할 ('hertz' = 주 Hertz H0 · 'hertz_h12' = H12 민감도 · 'physics') | None (contact_mode 를 모른다)."""
    if not isinstance(rec, dict):
        return None
    cm = rec.get('contact_mode')
    if cm == 'physics':
        return 'physics'
    if cm == 'hertzian':
        return H12_MODE if rec.get('sensitivity_mode') == H12_MODE else 'hertz'
    return None


def full_model_limit_problem(rec, channel='ionic', mode=None):
    """★ 10-15 L214-01 · 02 — 망 레코드 한 모드의 한 채널 (단상 이온 · 전자) 이 **유효한 FULL 모형 한계** 인가 → None (유효) | 사유 (문자열).

      ① 범위 — channel ∈ {ionic, electronic} (열 = 다상 정규화 · 병렬 상한 — 이 예외 밖) · 레코드 역할 (contact_mode · sensitivity_mode) 을 정할 수 있고 ·
         mode (자리 — hertz · hertz_h12 · physics) 를 주면 그 역할과 같아야 (다른 모드의 레코드 거부)
      ② 상태 · 사유 = (not_computed, full_over_conduction) 정확히 · accepted FULL σ · 차원 σ = null · FULL 유도값 없음 (CF/FULL · Bruggeman/FULL 비 · 그 채널 ·
         모드의 협착 전력 몫 = None + 사유 `network_conductivity.CPS_MODEL_LIMIT_STATUS`)
      ③ 관통 — 그 채널의 percolating_fraction ∈ (0, 1] (모형 한계 = 관통 해가 있었다)
      ④ 채널 상태 = model_limit (failed · 다른 이름이면 그 채널 판정이 우선)
      ⑤ 수치 증서 — `network_conductivity.model_limit_certificate_problem` (FULL 가지 · 가드 상태 · 사유 · 게시 값과 같은 수치 검사 · 채택 단 pass · ΔV · 유한 양수
         기하 · G→q · q_withheld = (I_b/ΔV)·T/A 재구성 · 엄격 > 1.5 · 문턱 · 정책 · 병렬 상한)
      ⑥ 결합 — 증서 채널 = channel · 역할 = 자리의 역할 (H0 · H12 · physics) · contact_mode = 세대 2 표 · 전극 dirichlet_exact · σ₀ = 이온은 부모 sigma_grain_S_cm
         (정확히) · 전자는 `network_conductivity.SIGMA_AM_ELECTRONIC`
    ⚠ 이것은 그 채널 · 그 FULL 가지의 판정이다 — 같은 레코드의 다른 채널 진짜 실패 (게시 채널 판정 · fail 우선) · CF · 협착-only 진단 (가지 표 · 증서 결합 —
      `certificate_binding_problems` 의 기존 정책) · 세대 표기 (`_g2_mode_problems` — 모형 한계 레코드는 실패 면제를 받지 않는다) 는 각자의 자리에서 본다."""
    if not isinstance(rec, dict):
        return f'레코드가 객체가 아니다 ({type(rec).__name__})'
    if channel not in _ML_CHANNEL_PREFIX:
        return f'채널 {channel!r} — FULL 모형 한계 예외는 단상 이온 · 전자 FULL 만 (열은 다상 정규화 · 병렬 상한 — 이 예외 밖)'
    rm = record_mode(rec)
    if rm is None:
        return f'레코드 역할을 정할 수 없다 (contact_mode {rec.get("contact_mode")!r}) — 어느 자리의 증서와 대조할지 모른다'
    if mode is not None and mode != rm:
        return f'자리 {mode!r} ↔ 레코드 역할 {rm!r} — 다른 모드의 레코드 (H12 를 주 Hertz 자리에 · physics 를 Hertz 자리에 …)'
    if channel == 'electronic' and rm == H12_MODE:
        return 'H12 민감도 레코드에는 전자 채널이 없다 (이온 민감도만)'
    nc = _nc_mod()
    p = _ML_CHANNEL_PREFIX[channel]
    why = []
    st, rsn = rec.get(p + 'sigma_full_status'), rec.get(p + 'sigma_full_reason')
    if st != 'not_computed' or rsn != MODEL_LIMIT_REASON:
        why.append(f'{p}sigma_full_status · _reason = ({st!r}, {rsn!r}) ≠ (not_computed, {MODEL_LIMIT_REASON!r})')
    for k in (p + 'sigma_full', p + 'sigma_full_mScm'):
        if rec.get(k) is not None:
            why.append(f'{k} = {rec.get(k)!r} — 모형 한계는 accepted FULL σ · 차원 σ = null (거부된 q 를 값 칸에 싣지 않는다)')
    for k in _ML_DERIVED[channel]:
        if rec.get(k) is not None:
            why.append(f'{k} = {rec.get(k)!r} — FULL 에서 유도되는 비가 남았다 (FULL 값이 없으면 없어야)')
    ck = f'constriction_power_share_{_ML_CPS_TAIL[channel]}_{"physics" if rm == "physics" else "hertz"}'
    if rec.get(ck) is not None or rec.get(ck + '_status') != nc.CPS_MODEL_LIMIT_STATUS:
        why.append(f'{ck} = ({rec.get(ck)!r}, {rec.get(ck + "_status")!r}) — FULL 유도 전력 몫은 None + 모형 한계 사유 {nc.CPS_MODEL_LIMIT_STATUS!r}')
    pf = _num(rec.get(p + 'percolating_fraction'))
    if pf is None or not (0.0 < pf <= 1.0):
        why.append(f'{p}percolating_fraction {rec.get(p + "percolating_fraction")!r} — (0, 1] 밖 (모형 한계 = 관통 해가 있었다 · 비관통은 valid_zero)')
    if rec.get(channel + '_status') != CHANNEL_MODEL_LIMIT:
        why.append(f'채널 상태 {channel}_status = {rec.get(channel + "_status")!r} ≠ {CHANNEL_MODEL_LIMIT!r} (그 채널 판정이 우선 — 모형 한계로 덮지 않는다)')
    cert = rec.get(p + 'solve_certificate_full')
    cp = nc.model_limit_certificate_problem(cert)
    if cp is not None:
        why.append(f'{p}solve_certificate_full: {cp}')
    else:
        want_role, want_cm = CERT_ROLE[rm], dict(G2_MODE_CONTRACT[rm]).get('contact_mode')
        if cert.get('channel') != channel:
            why.append(f'증서 채널 {cert.get("channel")!r} ≠ {channel!r} (다른 물리 채널의 증서)')
        if cert.get('role') != want_role:
            why.append(f'증서 역할 {cert.get("role")!r} ≠ {want_role!r} ({ROLE_NAME.get(rm, rm)} 자리 — 다른 역할의 증서)')
        if cert.get('contact_mode') != want_cm:
            why.append(f'증서 contact_mode {cert.get("contact_mode")!r} ≠ {want_cm!r}')
        if cert.get('electrode_model') != ELECTRODE_G2:
            why.append(f'증서 전극 {cert.get("electrode_model")!r} ≠ {ELECTRODE_G2!r}')
        s_ref = rec.get('sigma_grain_S_cm') if channel == 'ionic' else float(getattr(nc, 'SIGMA_AM_ELECTRONIC'))
        cs = _num(cert.get('sigma_bulk_S_cm'))                  # ★ 10-16 L214R-08 — 증서 · 부모 σ₀ 의 큰 JSON 정수 = None → 아래 사유 (예외 아님 · 거부)
        if cs is None or _num(s_ref) is None or cs != _num(s_ref):
            why.append(f'증서 σ₀ (sigma_bulk_S_cm) {cert.get("sigma_bulk_S_cm")!r} ≠ 그 채널의 σ₀ {s_ref!r} (G2RR2-04 — 정확히 같은 수)')
    return ' · '.join(why) if why else None


def full_model_limit_flag(rec, m):
    """★ 10-16 L214R-02 — 망 레코드 한 모드 (자리 m) → FULL 모형 한계 독립 표지: True | False | None.

      True  — 그 레코드의 이온 FULL 이 공용 판정 `full_model_limit_problem(rec, 'ionic', m)` 을 통과한 모형 한계 (수치 인증 통과 · 사전 고정 출력 상한 q > 1.5 ·
              거부된 q = 증서) — **띠 규칙 · 앞 게이트 (관통 불일치 · 온도 짝 · 세대 계약) 와 무관** (τ 상태 칸이 BAND_FALLBACK 이어도 사실은 남는다)
      False — 그 밖 (값 있는 FULL · 증명된 비관통 · 기술 실패 · 사유만 위조 · 증서 결손 · 남의 증서 · 틀린 q 재구성 = 모형 한계가 아니다)
      None  — 그 모드 레코드 없음 (판정할 사실이 없다)
    새 판정을 만들지 않는다 (규율 ① — 0b `ion_record_problem` · 게시 · 정지 계약 · 다시 읽기 · 인계 · 배포가 쓰는 같은 함수)."""
    if not isinstance(rec, dict):
        return None
    if rec.get('sigma_full_status') != 'not_computed' or rec.get('sigma_full_reason') != MODEL_LIMIT_REASON:
        return False
    return full_model_limit_problem(rec, 'ionic', m) is None


#  ── 망 활성 세대의 확정 여부 (10-05 RGLR2-02 · Codex 3차 재검증 §2 · Q2 ③ · 1저자 비준 범위) ─────────────────────────────────────────
#  케이스 폴더 (웹앱 results) 의 망 값은 여러 파일 (네 망 JSON · network_provenance.json · full_metrics.json) 에 나뉘어 있다.  게시 (승격) 는 동기
#  예외를 되돌리지만 **되돌림 자체가 실패**하거나 프로세스가 중간에 죽으면 파일들이 서로 다른 세대를 가리킬 수 있다 (Codex rollback_destination_failure:
#  망 JSON · 도장 = 옛 세대 · full_metrics = 새 세대).  그런 폴더의 값을 "이전 세대 그대로" 로 읽으면 안 된다 — 읽는 쪽 (케이스 페이지 · τ 인계 ·
#  등급 τ) 이 **디스크만 보고** 가른다 (최근 시도 기록을 못 썼어도).  이 도우미가 정본이고 `webapp/pipeline_service` 가 같은 함수를 부른다.
#  파일 이름 · 접두사는 `webapp/pipeline_service` 와 같은 값이어야 한다 (test_pipeline_provenance T23a 가 대조한다 — 무거운 웹앱 모듈을 여기서
#  임포트하지 않으려고 값을 둔다 · NO_THROUGH_REASON 과 같은 방식).
PROVENANCE_FILE = 'network_provenance.json'       # 활성 세대 도장 (승격했을 때만 갱신)
ATTEMPT_FILE = 'network_attempt.json'             # 최근 시도 (성공 · 실패 모두)
PUBLISH_BACKUP_PREFIX = '.publish_backup_'        # 승격 중 full_metrics 사본 — 되돌림이 끝나면 사라진다 (남으면 = 중단 · 되돌림 실패)
NETWORK_STASH_PREFIX = '.stage_stash_net_'        # 풀이 전 옛 망 산출물을 치워 둔 곳 — 승격 · 폐기로 사라진다 (남으면 = 진행 중 · 중단)
#: 읽는 쪽이 metrics 에 다는 표지 — 값이 있으면 그 metrics 의 망 값은 확정되지 않은 세대의 것 (등급 τ getter `tau2_from_metrics` 가 본다).
GENERATION_PROBLEM_KEY = 'network_generation_problem'


def generation_leftovers(case_dir):
    """중단된 게시 · 풀이의 흔적 (맨 위의 `PUBLISH_BACKUP_PREFIX` 파일 · `NETWORK_STASH_PREFIX` 디렉터리) → 이름 목록 (정렬).
    폴더를 못 읽으면 [] (폴더 자체가 없는 경우 — 다른 검사가 입력 결손으로 답한다)."""
    try:
        names = os.listdir(case_dir)
    except OSError:
        return []
    return sorted(n for n in names if n.startswith(PUBLISH_BACKUP_PREFIX) or n.startswith(NETWORK_STASH_PREFIX))


def network_generation_problem(case_dir, fm=None):
    """케이스 폴더의 망 활성 세대가 **확정되었는가** (읽는 쪽 fail-closed) → '' (확정 · 또는 대조할 것 없음) | 사유 (무효 — 값 인용 금지 · 재실행 필요).

      ① 도장 손상 — `network_provenance.json` 이 있는데 못 읽는다 (RV-06 과 같은 규약: 검증 불가 = 무효)
      ② 중단된 게시 · 풀이의 흔적 (`generation_leftovers`) — 진행 중이거나 중단됐다 (자동으로 유효 세대로 재사용하지 않는다 · Codex Q2 ③)
      ③ full_metrics ↔ 도장 — full_metrics 가 주장하는 망 세대 (`network_run_id` · `active_network_run_id`) 가 서로 다르거나, 도장의 run id 와
         다르다 (도장 없음 포함).  full_metrics 를 못 읽으면 무효.  full_metrics 가 망 세대를 주장하지 않으면 (접촉 분석만 다시 쓴 판 ·
         도장 이전 옛 세대) 대조할 것이 없다 — 막지 않는다 (그 판에는 망 소유 값이 없다).
      ④ 최근 시도 기록이 활성을 무효로 남겼다 (`failure_kind` rollback_failed · interrupted_publish · `active_status` invalid) — 성공한 다음
         승격이 덮을 때까지 유지된다 (재실행 필요).  기록을 못 읽으면 무효.
    fm = 이미 읽은 full_metrics (dict) — None 이면 폴더에서 읽는다."""
    probs = []
    pp = os.path.join(case_dir, PROVENANCE_FILE)
    prov_id, prov_ok = None, True
    if os.path.exists(pp):
        try:
            with open(pp, encoding='utf-8') as fh:
                prov = json.load(fh)
            if not isinstance(prov, dict):
                raise ValueError('객체가 아니다')
            prov_id = prov.get('network_run_id')
        except (OSError, ValueError) as e:
            prov_ok = False
            probs.append(f'도장 ({PROVENANCE_FILE}) 손상 ({type(e).__name__}) — 활성 세대를 확인할 수 없다')
    left = generation_leftovers(case_dir)
    if left:
        probs.append(f'중단된 게시 · 풀이 흔적 {left[:4]}{" …" if len(left) > 4 else ""} — 진행 중이거나 중단됐다 (재실행 필요)')
    if fm is None:
        fp = os.path.join(case_dir, 'full_metrics.json')
        if os.path.exists(fp):
            try:
                with open(fp, encoding='utf-8') as fh:
                    fm = json.load(fh)
            except (OSError, ValueError) as e:
                fm = None
                probs.append(f'full_metrics.json 손상 ({type(e).__name__}) — 망 세대를 대조할 수 없다')
    if isinstance(fm, dict):
        ids = {k: fm.get(k) for k in ('network_run_id', 'active_network_run_id') if fm.get(k) is not None}
        if len(set(ids.values())) > 1:
            probs.append(f'full_metrics 의 두 망 세대 id 가 다르다 {ids}')
        elif ids and prov_ok:
            fid = next(iter(ids.values()))
            if fid != prov_id:
                probs.append(f'full_metrics 의 망 세대 {fid!r} ≠ 도장 {prov_id!r} — 파일들이 서로 다른 세대를 가리킨다 (되돌림 실패 · 중단된 게시)')
    ap = os.path.join(case_dir, ATTEMPT_FILE)
    if os.path.exists(ap):
        try:
            with open(ap, encoding='utf-8') as fh:
                att = json.load(fh)
            if not isinstance(att, dict):
                raise ValueError('객체가 아니다')
        except (OSError, ValueError) as e:
            att = None
            probs.append(f'최근 시도 기록 ({ATTEMPT_FILE}) 손상 ({type(e).__name__}) — 활성 세대가 유효한지 확인할 수 없다')
        if isinstance(att, dict) and (att.get('failure_kind') in ('rollback_failed', 'interrupted_publish')
                                      or att.get('active_status') == 'invalid'):
            probs.append(f'최근 시도 {att.get("network_attempt_run_id")!r} 가 활성 세대를 무효로 남겼다 ({att.get("failure_kind") or "invalid"}: '
                         f'{str(att.get("active_problem") or att.get("reason") or "")[:160]}) — 성공한 재계산 전까지 무효')
    return '; '.join(probs)


def generation_override(row, prob):
    """τ 인계 행 (`ion_columns` · `case_row`) 에 세대 무효를 덮는다 — 두 모드 NOT_COMPUTED (generation_invalid: 사유) · f · tau2 · tau · σ₀ 메타 빈칸 ·
    ★ 10-16 L214R-02 모형 한계 표지 두 칸도 빈칸 (확정되지 않은 세대의 레코드에서 읽은 사실을 싣지 않는다).  prob 가 비면 그대로 돌려준다."""
    if not prob or not isinstance(row, dict):
        return row
    for m in MODES:
        row.update(_blank(m))
        row[f'ion_net_status_{m}'] = 'NOT_COMPUTED'
        row[f'ion_net_status_reason_{m}'] = f'{GENERATION_INVALID}: {prob}'
    row['ion_sigma0_mScm'] = row['ion_sigma0_T_C'] = None
    for col in MODEL_LIMIT_FLAG_COL.values():
        row[col] = None
    return row


#  ── 소비처 공용 tau2 (TAU-03 · 결정 6 · 1저자 비준 10-04 밤 *"권고대로"*) ────────────────────────────────────────────────
#  웹앱 τ 블록 · 등급 τ · overhead 축 · COMSOL 2D 내보내기 · regime DB 가 **이 두 함수**를 쓴다 (옛 다섯 변형 — 등급 · 내보내기는
#  Stage-E physics σ + 3.0 고정이었다).  인계 열 (`ion_columns`) 은 솔버 무차원 σ_ratio (8 자리) 로 따로 계산한다 (`TAU-25`) —
#  여기 값은 full_metrics 의 mS/cm σ (6 자리 반올림) 라 그것과 최대 0.11 % 다를 수 있다 (화면 · 등급용).
METRIC_SIGMA_KEY = {'hertz': 'sigma_full_mScm', 'physics': 'sigma_full_mScm_physics'}   # 원 솔버 σ — Stage-E 키 없음


def tau2_value(phi_se, sigma0, sigma_full):
    """tau2 = φ_SE · σ₀ / σ_full (tortuosity factor).  σ₀ 와 σ_full 은 **같은 런 · 같은 온도의 짝**이어야 한다 —
    짝이면 σ₀ 는 약분되는 수다 (망 σ_full 이 σ₀ 에 정비례).  셋 중 하나라도 양의 유한수가 아니면 None."""
    phi, s0, s = _pos(phi_se), _pos(sigma0), _pos(sigma_full)
    return phi * s0 / s if (phi is not None and s0 is not None and s is not None) else None


def tau2_from_metrics(metrics, mode='hertz'):
    """full_metrics → (tau2 | None, σ₀).  σ = **원 솔버 σ** (`METRIC_SIGMA_KEY` — Stage-E σ 는 Cronau · 파괴 같은 재료 인자를 담아
    τ 가 아니다 · 결정 6) · physics σ 가 없으면 None (Hertz 로 대체하지 않는다 · TAU-21) · σ₀ = `se_material.sigma_grain_context`
    (웹앱과 같은 짝 σ₀ — 온도 런이면 배수 · L4-04).  σ_bulk_net 은 `mode='bulk'` (모드 무관 CF 가지 · 원기둥 bulk)."""
    try:
        import se_material as _sem
    except ImportError:                                  # 같은 폴더 (scripts/) — 호출자 sys.path 에 없을 때
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import se_material as _sem
    if mode not in METRIC_SIGMA_KEY and mode != 'bulk':
        raise ValueError(f'mode={mode!r} — hertz · physics · bulk 만')
    m = metrics if isinstance(metrics, dict) else {}
    sigma0 = _sem.sigma_grain_context(m)[0]
    if m.get(GENERATION_PROBLEM_KEY):                    # ★ 10-05 RGLR2-02 — 읽는 쪽이 세대 무효로 표지한 metrics → τ 없음 (값 인용 금지)
        return None, sigma0
    key = 'sigma_bulk_net_mScm' if mode == 'bulk' else METRIC_SIGMA_KEY[mode]
    return tau2_value(m.get('phi_se'), sigma0, m.get(key)), sigma0


def column_names():
    out = []
    for m in MODES:
        out += [f'f_ion_{m}', f'f_ion_{m}_gap', f'tau2_ion_{m}', f'tau_ion_{m}', f'ion_net_status_{m}',
                f'ion_net_status_reason_{m}', f'ion_net_area_mode_{m}', f'ion_net_constriction_{m}', f'ion_net_psi_{m}',
                f'ion_net_area_rule_{m}', f'ion_net_electrode_{m}', f'ion_net_bulk_{m}',          # ★ 10-06 세대 2 표기
                f'ion_net_band_rule_{m}', f'ion_net_band_frac_{m}', f'ion_net_basis_check_{m}']
    return out + list(SHARED) + list(MODEL_LIMIT_FLAG_COL.values())     # ★ 10-16 L214R-02 — 표지 둘은 끝 (옛 50 열 자리 그대로)


def generation_meta(res, m, legacy=False):
    """망 레코드 한 모드 → (면적 규칙, 전극, bulk) 표기.  레코드 없음 → ('', '', '').
    ★ 10-06 밤 (G2R-02) — 옛 기본값 (hertz 면적 hertz_ccpl22 · physics 면적 physics_g1 · 전극 virtual_source_legacy · bulk cylinder_half_d = 이력 사실)
    은 **옛 세대로 추론된** 케이스 (legacy=True — `network_generation_contract` 가 inferred_legacy) 에만 채운다.  그 밖 (세대 2 · 계약 위반) 은 레코드
    값 그대로 · 없으면 빈칸 (옛 판은 늘 채워 세대 2 숫자를 세대 1 표기로 읽었다)."""
    if not isinstance(res, dict):
        return '', '', ''
    if not legacy:
        return tuple('' if res.get(k) is None else str(res.get(k)) for k in ('area_rule', 'electrode_model', 'bulk_model'))
    area = res.get('area_rule') or (AREA_RULE_PHYSICS_G1 if m == 'physics' else AREA_RULE_HERTZ)
    return str(area), str(res.get('electrode_model') or ELECTRODE_LEGACY), str(res.get('bulk_model') or BULK_CYLINDER)


#  ── 망 세대 계약 (10-06 밤 · Codex 세대 2 적대 리뷰 `docs/reviews/codex_review_gen2_network_20261006.md` G2R-01 · G2R-02 · 1저자 비준) ────────────
#  한 표 · 한 함수 — 웹앱 망 정지 계약 ⑨ (게시 전) · 공용 기록 검사 (일반 · 정지 경로 · `pipeline_service.network_record_verdict`) · τ 인계 소비자
#  (`ion_columns`) · 인계 생성기 (`lhs_design_dataset.load_tau_results` · `build_handover` — `generation_mixing_problem`) · 배포 빌더
#  (`lhs_release_build` — `row_generation_problems`) 가 **이 표**를 부른다 (규율 ① — 사본 금지).
#  옛 판의 구멍 (Codex 실 생산자 반례 · 우리 트리 재현 7a5976602):
#    (가) G2R-01 — 정지 계약 ⑨ 가 중첩 H12 메타만 보고 주 Hertz 가 H0 인지 안 봐, 생산된 H12 레코드를 주 `hertzian` 자리에 넣어도 done · 인계 통과
#         (주 σ +28.2 %) — 세대 축에 모드별 bulk · 협착이 없었다.
#    (나) G2R-02 — 주 Hertz 전극이 dirichlet_exact 가 아니면 무엇이든 "옛 레코드" (⑨ 조기 반환) · 빈 면적 · 전극 · bulk 를 옛 기본값으로 채움 ·
#         모르는 ψ 라벨을 빈 축으로 만들어 비교에서 뺐다 → ψ 오타 · 전극 오타 · 세대 2 physics 의 면적 · ψ 삭제 · 같은 결함 코호트가 통과.
#  규칙 (닫힌 열거): 세대 2 표지 (`G2_MARKER_KEYS` · ψ multiply) 가 레코드 어디에든 하나라도 있으면 세대 2 — 모드마다 `G2_MODE_CONTRACT` 표기 **전부**
#  필수 · 값은 표와 같아야 하고 (주 Hertz = H0 · H12 = ψ 곱 + 구 조각 · physics = ψ 곱 + physics_g2) 세대 2 Hertz 는 H12 레코드도 필수 (생산자가 늘
#  함께 낸다).  표지가 하나도 없으면 옛 세대 **추론** (`inferred_legacy`) — `LEGACY_MODE_CONTRACT` (194 v1.2 배치 원천의 실제 모양) 와 맞아야 한다.
#  그 밖 = `invalid` (레코드 있는 모드 전부 NOT_COMPUTED invalid_input).  ⚠ 표기 계약 + ★ 10-06 밤 G2RR-02 수치 증서 결합 (`certificate_binding_problems`
#  — 숫자를 싣는 가지마다 그 가지 증서의 I_bottom/ΔV × 봉인 기하로 발행 σ 를 재구성) — 숫자만 바꿔 끼운 레코드는 이제 잡힌다 · 증서 · 숫자 · 기하를
#  한 실행의 모든 증서에 걸쳐 일관되게 바꾼 전면 위조는 재계산 없이 못 잡는다 (TAU_SAME_GEN_BASIS 한계와 같은 부류).
NET_GEN_G2 = 'g2'
NET_GEN_LEGACY = 'inferred_legacy'            # 세대 2 표지가 하나도 없는 역사 레코드 — 옛 기본값으로 **추론**했다는 표지
NET_GEN_BAD = 'invalid'                       # 세대 계약 위반 (사유 = 그 행의 상태 칸 · `generation_contract_text`)
#: 세대 2 생산자 (`network_conductivity` a0a24c538 뒤 · CLI `--contact-mode both`) 가 모드마다 쓰는 모델 조합 — (키, 값) · 값 None = 키가 없거나 null
#:   이어야 한다 (physics 의 hertz_constriction = null · 주 Hertz · physics 에 민감도 표지 없음).  값 = 생산자 상수와 같은 문자열 (test_gen2_role_contract
#:   T1 이 생산자 상수 · 실 출력과 대조).  주 Hertz 의 psi_placement = 그 실행의 ψ 배치 표기 (Hertz 는 ψ 를 안 쓴다 — 세대 2 실행은 multiply 뿐 ·
#:   명시 ψ 분모 연구 팔 (세대 2 생산자 + legacy_divide) 은 세대 1 도 2 도 아니다).
G2_MODE_CONTRACT = {
    'hertz': (('contact_mode', 'hertzian'), ('resistance_model', 'maxwell'), ('hertz_constriction', 'maxwell'),
              ('bulk_model', BULK_CYLINDER), ('electrode_model', ELECTRODE_G2), ('area_rule', AREA_RULE_HERTZ),
              ('area_rule_physics', AREA_RULE_PHYSICS_G2), ('psi_placement', PSI_G2), ('sensitivity_mode', None)),
    H12_MODE: (('contact_mode', 'hertzian'), ('resistance_model', 'mikic'), ('hertz_constriction', 'mikic_psi_multiply'),
               ('bulk_model', BULK_SPHERE_SEGMENT), ('electrode_model', ELECTRODE_G2), ('area_rule', AREA_RULE_HERTZ),
               ('area_rule_physics', AREA_RULE_PHYSICS_G2), ('psi_placement', PSI_G2), ('sensitivity_mode', H12_MODE)),
    'physics': (('contact_mode', 'physics'), ('resistance_model', 'mikic'), ('hertz_constriction', None),
                ('bulk_model', BULK_CYLINDER), ('electrode_model', ELECTRODE_G2), ('area_rule', AREA_RULE_PHYSICS_G2),
                ('area_rule_physics', AREA_RULE_PHYSICS_G2), ('psi_placement', PSI_G2), ('sensitivity_mode', None)),
}
#: 채널 (전자 · 열) 결과를 이온 레코드에 올린 표기 (`electronic_<키>` · `thermal_<키>`) — 있으면 그 모드 표와 같아야 한다 (닫힌 열거).
CHANNEL_PREFIXES = ('electronic_', 'thermal_')
G2_CHANNEL_LABELS = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'psi_placement')
#: 세대 2 표지 키 — 하나라도 있으면 옛 세대 추론 자격이 없다.  실 생산자 세대 2 레코드에는 다 있고 194 v1.2 배치 원천 (역사 레코드) 에는 하나도 없다
#:   (test_gen2_role_contract K1 · K2 가 그 차로 대조).  ψ 는 **값** multiply 가 표지다 (legacy_divide 는 09-15 깃발부터 옛 세대에도 있다).
_G2_MARKER_BASE = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'hertz_constriction', 'sensitivity_mode', H12_MODE,
                   'area_binding_counts_physics', 'n_area_physics_unavailable', 'n_clamp_zero', 'n_floor_only', 'h_film_nm', 'h_film_status',
                   'solve_method_full', 'solve_certificate_full', 'solve_certificate_bulk_net', 'solve_certificate_constr_net')
_G2_CHANNEL_MARKERS = ('electrode_model', 'bulk_model', 'area_rule', 'area_rule_physics', 'area_binding_counts_physics', 'n_clamp_zero',
                       'n_floor_only', 'psi_placement')
G2_MARKER_KEYS = _G2_MARKER_BASE + tuple(p + k for p in CHANNEL_PREFIXES for k in _G2_CHANNEL_MARKERS)
#: 옛 세대 (10-06 전 생산자 — 194 v1.2 배치 원천의 실제 모양) — (키, 허용 값) · 허용 값의 None = 키 없음 또는 null.  resistance_model 은 04-24 첫
#:   반입부터 늘 있다 · contact_mode 는 있으면 자리와 같아야 한다 (손 레코드 · 옛 시험 대역에는 없을 수 있다) · ψ = legacy_divide (09-15 깃발 뒤) 또는
#:   기록 없음 (그 전).  H12 는 옛 세대에 없다 (있으면 그 키가 세대 2 표지다).
LEGACY_MODE_CONTRACT = {
    'hertz': (('resistance_model', ('maxwell',)), ('contact_mode', ('hertzian', None)), ('psi_placement', (PSI_LEGACY, None))),
    'physics': (('resistance_model', ('mikic',)), ('contact_mode', ('physics', None)), ('psi_placement', (PSI_LEGACY, None))),
}
ROLE_NAME = {'hertz': 'H0 (Maxwell 협착 + 원기둥 bulk)', H12_MODE: 'H12 (ψ 곱 협착 + 구 조각 bulk)',
             'physics': '세대 2 physics (ψ 곱 + physics_g2 + 원기둥 bulk)'}


def g2_markers(rec):
    """레코드 한 모드 → 그 안의 세대 2 표지 (키 · ψ multiply) 목록 ([] = 표지 없음)."""
    if not isinstance(rec, dict):
        return []
    out = [k for k in G2_MARKER_KEYS if k in rec]
    if rec.get('psi_placement') == PSI_G2:
        out.append('psi_placement=multiply')
    return out


def _nc_mod():
    """생산자 모듈 (network_conductivity) — 무거운 생산자를 τ 모듈 임포트 때 끌어오지 않으려고 부를 때만 임포트한다."""
    import network_conductivity as _nc
    return _nc


def _cert_problem(cert):
    """수치 증서 → None | 사유 (★ 10-06 밤 G2R-03 통합).  판정 = 생산자 모듈의 `certificate_problem` (허용치 = 그 모듈 상수 · 한 곳) —
    무거운 생산자를 τ 모듈 임포트 때 끌어오지 않으려고 부를 때만 임포트한다."""
    return _nc_mod().certificate_problem(cert)


#  ── ★ 10-06 밤 G2RR-02 — 증서 ↔ 가지 · 역할 · 발행값 결합 (Codex 세대 2 재검증 `docs/reviews/codex_review_gen2_network_reverify_20261006.md` §3 · §7-2 ·
#     1저자 비준 "권고대로") ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
#  옛 계약 (G2R-03 통합) 은 `solve_certificate_full` 이라는 **자리**에 있는 증서의 내부 일관성 (보존 · 잔차 · 방법) 만 봤다 → 같은 실행의 CF 증서 ·
#  H12 FULL 증서를 주 Hertz FULL 자리에 복사해도 게시 · τ OK (Codex probes/acceptance.py · 우리 트리 재현 db74ea98 — tau2 10.98080510469845x 그대로).
#  이제 생산자가 증서마다 싣는 결합 정보 (`network_conductivity.CERT_BINDING_FIELDS`) 를 자리 · 부모 레코드 · 발행 σ 와 대조한다 (값 = 생산자 상수와
#  같은 문자열 — 무거운 생산자를 이 도우미에서 임포트하지 않으려고 둔다 · test_network_solve_certificate G1 이 실 출력과 대조):
#    ① 결합 — 가지 = 자리 (full · bulk_only · constriction_only) · 채널 = ionic · 역할 = 모드 (hertz → H0 · hertz_h12 → H12 · physics → physics) ·
#       contact_mode · 전극 = 그 자리의 세대 2 표 값 (부모 표기는 역할 계약이 같은 표로 본다 → 받는 레코드에서 증서 = 부모 · 사유를 겹치지 않는다) ·
#       증서 상태 = 그 가지 상태 · ΔV = 1 (정확 Dirichlet 바닥 1 · 위 0)
#    ② 기하 — geometry {plate_z, box_x, box_y, scale} 유한 양수 · g_to_q = (plate_z·scale)/(box_x·box_y·scale²) (상대 1e-12) · 한 실행의 모든 증서
#       (모드 셋 · 가지 셋 · 채널 사본) 가 같은 기하 = 봉인된 기하 (`_cert_geometry_problems`)
#    ③ 재구성 — q = (I_bottom/ΔV)·T/A (생산자 σ 환산과 같은 식 · 같은 순서) 가 저장 σ_ratio 의 반올림 반폭 (5e-9 + 16ε) 안 · 1000·σ₀·q 가 저장
#       σ_dim 의 저장 정밀도 허용 (`sigma_identity_tol` — 6 자리 반폭 5e-7 + 8 자리 반폭 몫 + 16ε) 안 · σ₀ = **세 가지 모두 부모 sigma_grain_S_cm** ·
#       ★ 10-16 L214R-05 (L214R-01 A 의 규칙 그대로 — 1저자 10-16 Q3 권고대로) — 기하 환산 T · A · T/A · ΔV · 재구성 q · 차원 σ · 그 허용을 비교 **전에** 유한 (양수)
#       로 본다: 넘침 · 밑넘침 (scale² 의 OverflowError · float 로 못 옮기는 큰 JSON 정수 포함) = 기술 실패 사유 (생산자 NON_FINITE_REASON 꼬리표) · 예외 · inf ≤ inf 아님
#       (생산자 판정 `_geometry_TA` · `_cert_num` 을 그대로 부른다 · 식 · 순서 · 허용치 · 정상 레코드 결과 그대로)
#       (★ 10-07 G2RR2-04 — 옛 판은 CF · 협착-only 를 그 증서 자신의 sigma_bulk_S_cm 로 재구성해 증서 내부 자기일관성만 봤고 · 주석은 증서 ↔ 부모 짝을
#       정지 계약 ⑧ 에 맡긴다고 했는데 ⑧ (`pipeline_service.network_sigma0_problem`) 은 증서를 읽지 않았다 → CF 증서 σ₀ ×2 + CF 차원값 재계산이 게시 ·
#       인계 · 다시 읽기를 다 지났다 · Codex 세대 2 재검증 2 §5)
#    ③b ★ 10-07 G2RR2-04 σ₀ 결합 (`sigma0_binding_problems` — 이 계약과 정지 계약 ⑧ 이 같은 함수를 부른다): 이온 세 가지 증서의 sigma_bulk_S_cm = 부모
#       sigma_grain_S_cm (생산자가 같은 float 을 두 자리에 쓴다 — 정확히 같아야 · FULL 도 표기 어긋남을 받지 않는다) · 부모 σ₀ = 그 레코드의 온도 규약
#       (`sigma0_convention_problem` — temperature_provenance 의 T_C · Ea · T_ref 로 se_material 을 다시 부른 값) · 전자 · 열 채널 증서는 그 채널의 기준
#       전도도 (`network_conductivity.SIGMA_AM_ELECTRONIC` · `K_SE_THERMAL`) — 이온 σ₀ 를 강제하지 않는다
#    ④ 수치 증서 — `network_conductivity.certificate_problem` (보존 · 잔차 · 방법 · 허용치 1e-6)
#    ④b ★ 10-16 L214R-06 — 채택 단 (마지막 시도) ↔ 요약 결합 = `network_conductivity.adopted_attempt_binding_problem` (모형 한계 증서 ③ 과 같은 함수 · 마지막 시도 =
#       pass · 같은 방법 · 같은 두 전류 · 예외 없음 · 방법별 수렴 상태 · 수치 · 보존 · 내부 잔차 = 요약 · 앞선 실패 시도 = 정상 fallback 은 허용)
#  정책 (`CERT_BRANCH_POLICY` · 봉인 — 새 194 전 고정 · 결과를 보고 옮기지 않는다):
#    · FULL — 게시 (computed) 면 ①–④ 필수 (τ 의 수치 의존).
#    · CF (bulk_only) · 협착-only (constriction_only) 진단 — **숫자를 싣는** 가지 (값 있음 · 상태 computed · model_over_conduction) 면 ①–④ 필수 ·
#      model_over_conduction 은 모형 해석 표지이지 수치 증서 면제가 아니다 (Codex Q4).
#    · 숫자 없는 가지 (비관통 valid_zero · 0 저항 수축 미구현 · 증서 실패 · 경계 겹침 = not_computed) — **없는 수렴 증서를 요구하지 않는다**: 상태가
#      있으면 이유를 말해야 하고 (valid_zero · not_computed) · 증서가 있으면 해를 주장하지 않아야 (status computed · I_bottom 없음) · 생산자 사유
#      (경계 겹침 · 증서 실패 · 0 저항) 는 증서 사유와 같아야 한다 — 해 없는 가지를 거짓 수렴으로 채우지 않는다.
#    · ★ 10-07 G2RR2-05 (Codex 세대 2 재검증 2 §6) — **정직한 실패 = 숫자 없음 + 상태 + 사유** ↔ **가지 기록 통째 결손** (상태 키가 없거나 null) 을 공용
#      계약이 가른다 (`branch_table_problems`): 생산자는 세 가지의 상태 · 사유를 늘 쓴다 → 상태가 없는 가지는 숫자 · 증서가 함께 없어도 실패 기록이 아니라
#      결손이다 → 레코드 거부 (결손을 임의의 not_computed 로 채우지 않는다).  옛 판은 상태 None 이 첫 검사를 지나고 증서 None 이면 바로 통과해, 주 Hertz
#      CF 다섯 키 삭제가 게시 · 인계를 지났고 다시 읽기 K7 만 따로 거부했다 (K7 = 별도 자격).  이제 K7 은 이 함수의 결과를 그대로 쓴다.
#    · 어긋남 = 레코드 계약 위반 (세대 invalid · 그 실행의 모드 전부 NOT_COMPUTED · 게시 거부 · 인계 거부).  생산자는 증서를 못 넘은 가지에 숫자를
#      싣지 않는다 (그 가지만 NOT_COMPUTED + 사유 · FULL 유지 — 정직한 개별 풀이 실패는 위 "숫자 없는 가지" 로 통과) → 숫자가 실렸는데 결합 증서가
#      없거나 맞지 않으면 개별 풀이 실패가 아니라 레코드 조립 · 편집 모순이다 (Codex §6 의 "모드 정체성 모순" 부류 — 그 레코드의 다른 숫자도 믿을 근거가 없다).
#    · 전자 · 열 채널 증서 — 결합 정보는 기록 · 봉인된 기하 대조에만 쓴다 (이번 τ 인계에 안 쓰는 채널 — 이 수용 검사 밖 · "웹앱 σ 전체 인증" 이 아니다).
#    · 옛 기록 — 결합 키가 없는 세대 2 증서 (G2RR-02 이전 생산자 · 05977e94a – 70a6d91a4) 는 숫자를 싣는 가지에서 거부 (재계산 필요 · 결합 키를 지워
#      옛 증서로 위장할 수 없다 — 지운 것과 옛 것을 구별할 수 없으므로) · 세대 2 표지가 하나도 없는 역사 레코드 (194 v1.2 원천 = inferred_legacy) 는
#      증서가 없어 이 검사 대상이 아니다 (상태 · 값 그대로).
#    · 공용 기술 검사 (`ion_record_problem`) 를 못 넘은 레코드는 결합을 보지 않는다 — 모든 소비처 (정지 계약 ③ · 승격 전 기록 검사 · τ 0b · 인계 P4
#      재검사) 가 그 검사로 먼저 거부한다 (사유를 겹치지 않는다 · 인계 재검사의 "망 정지 계약 재검사" 사유가 그대로 남는다).
#  ⚠ 한계 — 증서 · 숫자 · 기하를 한 실행의 모든 증서에 걸쳐 일관되게 바꾼 전면 위조는 재계산 없이 못 잡는다 (Codex: "일관된 전면 위조를 탐지한다는 보증 아님").
CERT_DELTA_V = 1.0
CERT_ION_CHANNEL = 'ionic'
CERT_ROLE = {'hertz': 'H0', H12_MODE: 'H12', 'physics': 'physics'}
CERT_BINDING_KEYS = ('branch', 'channel', 'role', 'contact_mode', 'delta_V', 'geometry', 'g_to_q', 'sigma_bulk_S_cm')
CERT_GEOMETRY_KEYS = ('plate_z', 'box_x', 'box_y', 'scale')
#: 가지 → (σ_ratio 키, σ_dim 키, 상태 키, 사유 키, 증서 키) — 생산자 run_decomposition 의 결과 키.
CERT_BRANCH_KEYS = (('full', 'sigma_full', 'sigma_full_mScm', 'sigma_full_status', 'sigma_full_reason', 'solve_certificate_full'),
                    ('bulk_only', 'sigma_bulk_net', 'sigma_bulk_net_mScm', 'sigma_bulk_net_status', 'sigma_bulk_net_reason',
                     'solve_certificate_bulk_net'),
                    ('constriction_only', 'sigma_constr_net', 'sigma_constr_net_mScm', 'sigma_constr_net_status', 'sigma_constr_net_reason',
                     'solve_certificate_constr_net'))
CERT_PUBLISHED_STATES = ('computed', 'model_over_conduction')
CERT_UNPUBLISHED_STATES = ('valid_zero', 'not_computed')
#: ★ 10-07 G2RR2-05 — 가지 상태의 닫힌 집합 (생산자 `_net_sigma_status` 가 내는 넷) · 정직한 실패 = 숫자 없음 + 이 중 비게시 상태 + 사유.
CERT_BRANCH_STATES = CERT_PUBLISHED_STATES + CERT_UNPUBLISHED_STATES
CERT_BRANCH_POLICY = {'full': 'required_when_computed', 'bulk_only': 'required_when_published', 'constriction_only': 'required_when_published',
                      'record': 'status_required'}       # ★ G2RR2-05 — 세 가지의 상태 기록 필수 (결손 ≠ 정직한 실패)
CERT_G2Q_REL_TOL = 1e-12
#: ★ 10-07 G2RR2-04 — 부모 σ₀ ↔ 온도 규약 대조의 상대 허용 (se_material 을 같은 인자로 다시 부른 값 — 같은 기계면 비트 같다 · 다른 기계의 libm exp 마지막
#:   자리만 덮는다 · 새 물리 허용오차가 아니다).  증서 σ₀ ↔ 부모 σ₀ 는 정확히 같아야 한다 (생산자가 같은 float 을 두 자리에 쓴다 · JSON 왕복 비트 보존).
SIGMA0_CONVENTION_REL_TOL = 1e-12
#: ★ G2RR2-04 — 전자 · 열 채널 증서의 기준 전도도 = 생산자 상수 (이온 σ₀ 를 강제하지 않는다) · 채널 이름.
CHANNEL_SIGMA_REF = {'electronic_': 'SIGMA_AM_ELECTRONIC', 'thermal_': 'K_SE_THERMAL'}
CHANNEL_CERT_NAME = {'electronic_': 'electronic', 'thermal_': 'thermal'}


def _cert_geometry(cert):
    """증서 → (T, A, '') | (None, None, 사유) — T = plate_z·scale · A = box_x·box_y·scale² (생산자 σ 환산과 같은 식) · g_to_q 대조.
    ★ 10-16 L214R-05 — 기하 네 값 · 환산 T · A 는 생산자 판정 `_geometry_TA` 그대로 (scale² 넘침 · 큰 정수 = 예외가 아니라 사유 · 넘침 · 밑넘침 = NON_FINITE_REASON) ·
    T/A 도 대조 **전에** 유한 양수 (넘친 T/A 와는 어떤 g_to_q 도 inf ≤ inf 로 '같다' — 모형 한계 증서 `model_limit_certificate_problem` 과 같은 규칙)."""
    nc = _nc_mod()
    T, A, why = nc._geometry_TA(cert.get('geometry'))
    if why:
        return None, None, why
    try:
        want = T / A
    except (OverflowError, ZeroDivisionError):                  # 큰 정수끼리의 나눗셈 넘침 (float 나눗셈은 inf)
        want = None
    if nc._cert_num(want) is None or not want > 0:
        return None, None, (f'{nc.NON_FINITE_REASON} — 기하 환산 T/A = {want!r} 가 유한 양수가 아니다 (넘침 · 밑넘침 · T {T!r} · A {A!r} — 생산자는 이 기하를 '
                            f'풀지 않는다 · {nc.INVALID_GEOMETRY_REASON})')
    g2q = nc._cert_num(cert.get('g_to_q'))                      # 큰 정수 = None (사유) · 예외 아님
    if g2q is None or not g2q > 0 or not abs(g2q - want) <= CERT_G2Q_REL_TOL * want:
        return None, None, (f'G→q 인자 g_to_q {cert.get("g_to_q")!r} ≠ 기하에서 다시 잰 (plate_z·scale)/(box_x·box_y·scale²) = {want!r} '
                            '(기하 인자 변이)')
    return T, A, ''


def _cert_published_problem(m, branch, rec, q, sd, st, cert):
    """숫자를 싣는 가지 → None | 사유 (정책 ①–④)."""
    if st not in CERT_PUBLISHED_STATES:
        return f'숫자 (σ_ratio {q!r} · σ_dim {sd!r}) 가 실렸는데 상태 {st!r} — 숫자를 싣는 가지는 computed · model_over_conduction 이어야'
    if not isinstance(cert, dict):
        return f'증서 없음 ({type(cert).__name__}) — 발행 σ 를 뒷받침할 그 가지의 풀이 증서가 없다'
    miss = [k for k in CERT_BINDING_KEYS if k not in cert]
    if len(miss) == len(CERT_BINDING_KEYS):
        return ('결합 정보 없음 — G2RR-02 이전 세대 2 증서 (가지 · 채널 · 역할 · ΔV · 기하 · G→q 없음) · 발행값과 대조할 수 없다 (재계산 필요)')
    if miss:
        return f'결합 정보 부분 결손 {miss}'
    p = _cert_problem(cert)
    if p is not None:
        return p
    #  ★ 10-16 L214R-06 (Codex 재검증 뒤 같은 부류 Q4) — 채택 단 (마지막 시도) ↔ 요약 결합: 모형 한계 증서 ③ 과 **같은 함수** (생산자 수용 상수 그대로 · 앞선 실패
    #    시도 = 정상 fallback 은 허용).  옛 판은 게시 증서의 시도 기록을 읽지 않아 마지막 시도를 실패 · 잔차 1.0 · 예외 · 다른 방법 · 전류 ×2 · 목록 비움 / 뺌 ·
    #    직접해 단 krylov_info 1 로 바꿔도 게시 · τ OK 였다 (생산자는 해를 낸 모든 증서에 시도 목록을 싣고 pass 단에서 멈춘다 — 정직한 증서는 늘 통과)
    ap = _nc_mod().adopted_attempt_binding_problem(cert)
    if ap is not None:
        return ap
    bad = []
    if cert.get('branch') != branch:
        bad.append(f'가지 {cert.get("branch")!r} ≠ 자리 {branch!r} (다른 가지의 증서)')
    if cert.get('channel') != CERT_ION_CHANNEL:
        bad.append(f'채널 {cert.get("channel")!r} ≠ {CERT_ION_CHANNEL!r} (다른 물리 채널의 증서)')
    if cert.get('role') != CERT_ROLE[m]:
        bad.append(f'역할 {cert.get("role")!r} ≠ {CERT_ROLE[m]!r} ({ROLE_NAME.get(m, m)} 자리 — 다른 역할의 증서)')
    #  전극 · contact_mode = 그 자리의 세대 2 표 값 — 부모 표기는 역할 계약 (`_g2_mode_problems`) 이 같은 표로 본다 → 받는 레코드에서는 증서 = 부모 ·
    #  부모만 어긋난 레코드에 사유를 겹치지 않는다 (정지 계약 ⑨ · τ 사유 한 줄)
    want_cm = dict(G2_MODE_CONTRACT[m]).get('contact_mode')
    if cert.get('contact_mode') != want_cm:
        bad.append(f'contact_mode {cert.get("contact_mode")!r} ≠ {want_cm!r} (부모 · 자리)')
    if cert.get('electrode_model') != ELECTRODE_G2:
        bad.append(f'전극 {cert.get("electrode_model")!r} ≠ {ELECTRODE_G2!r} (부모 · 자리)')
    if cert.get('status') != st:
        bad.append(f'증서 상태 {cert.get("status")!r} ≠ 그 가지 상태 {st!r}')
    nc = _nc_mod()
    dv = nc._cert_num(cert.get('delta_V'))                          # ★ 10-16 L214R-05 — 큰 정수 = None (ΔV 사유) · 예외 아님
    if dv != CERT_DELTA_V:
        bad.append(f'ΔV {cert.get("delta_V")!r} ≠ {CERT_DELTA_V!r} (정확 Dirichlet — 바닥 띠 1 · 위 띠 0)')
    T, A, gwhy = _cert_geometry(cert)
    if gwhy:
        bad.append(gwhy)
    if T is not None and dv is not None and dv > 0:                 # 재구성 — 결합 어긋남과 함께 보인다 (무엇이 어긋났는지 한 번에)
        q_rec = (float(cert['I_bottom']) / dv) * T / A
        if nc._cert_num(q_rec) is None or not q_rec > 0:            # ★ L214R-05 — 같은 식 · 같은 순서의 재구성이 유한 입력에서 넘치거나 0 으로 밑넘치면 비교하지 않는다
            bad.append(f'{nc.NON_FINITE_REASON} — 증서 재구성 q = I_bottom/ΔV × T/A = {q_rec!r} 가 유한 양수가 아니다 (넘침 · 밑넘침 — 생산자 solve_network 는 '
                       f'이 해를 {nc.NON_FINITE_REASON} 로 거부한다 · 발행 σ_ratio {q!r} 와 비교하지 않는다)')
            return ' · '.join(bad)
        qn, sdn = _num(q), _num(sd)
        if qn is None or not abs(qn - q_rec) <= SIGMA_RATIO_ROUND_HALF + _ID_FP * abs(q_rec):
            bad.append(f'발행 σ_ratio {q!r} ≠ 증서 재구성 I_bottom/ΔV × T/A = {q_rec!r} (저장 반올림 반폭 {SIGMA_RATIO_ROUND_HALF:g} 밖)')
        #  차원 σ — ★ 10-07 G2RR2-04: 세 가지 모두 **부모 σ₀** (공용 기술 검사의 두 표현 항등식과 같은 σ₀ · 같은 허용).  옛 판은 CF · 협착-only 를 그
        #  증서 자신의 sigma_bulk_S_cm 로 재구성해 증서 σ₀ 와 차원값을 함께 바꾼 레코드 (Codex cf_sigma0_x2) 가 자기일관으로 통과했다.  증서 σ₀ = 부모 σ₀
        #  · 부모 σ₀ = 온도 규약은 `sigma0_binding_problems` (이 계약 · 정지 계약 ⑧ 같은 함수) 가 따로 본다.
        s_ref = _pos(rec.get('sigma_grain_S_cm'))
        if s_ref is None or sdn is None:
            bad.append(f'차원 σ {sd!r} · 부모 σ₀ (sigma_grain_S_cm) {rec.get("sigma_grain_S_cm")!r} 결손 — 증서에서 재구성할 수 없다')
        else:
            d_rec = 1000.0 * s_ref * q_rec
            tol = sigma_identity_tol(s_ref, q_rec, sdn)
            if nc._cert_num(d_rec) is None or not d_rec > 0 or nc._cert_num(tol) is None:   # ★ L214R-05 — 넘친 차원 σ · 허용 (σ_dim + 1000·σ₀·q) 과는 x ≤ inf 가 참
                bad.append(f'{nc.NON_FINITE_REASON} — 증서 재구성 차원 σ 1000·σ₀(부모)·q = {d_rec!r} · 저장 정밀도 허용 {tol!r} 가 유한하지 않다 (넘침 · '
                           f'밑넘침 — 발행 σ_dim {sdn!r} 와 비교하지 않는다)')
            elif not abs(sdn - d_rec) <= tol:
                bad.append(f'발행 σ_dim {sdn!r} mS/cm ≠ 증서 재구성 1000·σ₀(부모)·q = {d_rec!r} (G2RR2-04 · 저장 정밀도 허용 {tol:.3g} 밖 — 증서 σ₀ 로 '
                           '다시 계산한 차원값은 받지 않는다)')
    return ' · '.join(bad) if bad else None


def _cert_unpublished_problem(branch, st, rsn, cert):
    """숫자 없는 가지 → None | 사유 — 없는 수렴 증서를 요구하지 않는다 · 상태 ↔ 증서가 해를 주장하지 않는가만.
    (상태 기록 결손 · 사유 없음 = `_branch_table` · 증서 σ₀ = `sigma0_binding_problems` — 같은 계약의 다른 자리)"""
    if st is not None and st not in CERT_UNPUBLISHED_STATES:
        return f'숫자 없음 ↔ 상태 {st!r} (사유 {rsn!r}) — 해가 없는 가지는 valid_zero · not_computed 로 이유를 말해야 한다'
    if cert is None:
        return None
    if not isinstance(cert, dict):
        return f'증서 자리가 객체가 아니다 ({type(cert).__name__})'
    if cert.get('status') in CERT_PUBLISHED_STATES or _num(cert.get('I_bottom')) is not None:
        return (f'숫자 없는 가지 ({st} · {rsn}) 인데 증서가 해를 주장한다 (status {cert.get("status")!r} · I_bottom {cert.get("I_bottom")!r}) — '
                '해 없는 가지를 거짓 수렴 증서로 채우지 않는다')
    #  ★ 10-16 L214R-08 (같은 부류 Q6) — 여기서 None 은 '해 주장 없음 = 받음' 이다 → float 로 못 옮기는 큰 정수 (JSON 10⁴⁰⁰ · `_num` = None) 를 그 None 으로 읽지 않는다:
    #    숫자가 실렸으므로 해를 주장한 것 = 기술 실패 사유 (옛 판 = OverflowError) · NaN · None (숫자 아님) 의 기존 뜻은 그대로
    if _overflow_int(cert.get('I_bottom')):
        return (f'{_nc_mod().NON_FINITE_REASON} — 숫자 없는 가지 ({st} · {rsn}) 인데 증서 I_bottom 이 float 로 못 옮기는 정수 ({cert["I_bottom"].bit_length()} 비트) — '
                '숫자가 실렸으므로 해를 주장한다 (변환 불가 = 기술 실패 · 없음으로 읽지 않는다 · 해 없는 가지를 거짓 수렴 증서로 채우지 않는다)')
    if 'branch' in cert and cert.get('branch') != branch:
        return f'가지 {cert.get("branch")!r} ≠ 자리 {branch!r} (다른 가지의 증서)'
    if rsn in _nc_mod().NOT_COMPUTED_SOLVE_REASONS and cert.get('reason') != rsn:
        return f'숫자 없음의 사유 {rsn!r} ≠ 증서 사유 {cert.get("reason")!r}'
    return None


def _branch_table(rec):
    """★ 10-07 G2RR2-05 — 가지 표 (FULL · CF · 협착-only) 의 상태 기록 → [(가지, 키, 사유)].  정직한 실패 (숫자 없음 + 비게시 상태 + 사유) ↔ 기록 결손."""
    out = []
    for branch, qk, dk, sk, rk, ck in CERT_BRANCH_KEYS:
        st, rsn = rec.get(sk), rec.get(rk)
        has_num = rec.get(qk) is not None or rec.get(dk) is not None
        if st is None:
            left = [k for k in (qk, dk, sk, rk, ck) if k in rec]
            out.append((branch, sk, f'가지 {branch} 의 상태 기록이 없다 ({"키 없음" if sk not in rec else "null"} · 남은 키 {left}) — 정직한 실패 '
                                    '(숫자 없음 + 상태 + 사유) 가 아니라 기록 결손이다 (생산자는 세 가지의 상태 · 사유를 늘 쓴다 · 결손을 not_computed 로 채우지 '
                                    '않는다 · G2RR2-05)'))
        elif st not in CERT_BRANCH_STATES:
            out.append((branch, sk, f'모르는 가지 상태 {st!r} (닫힌 집합 {list(CERT_BRANCH_STATES)} · G2RR2-05)'))
        elif has_num and st not in CERT_PUBLISHED_STATES:
            out.append((branch, sk, f'숫자 (σ_ratio {rec.get(qk)!r} · σ_dim {rec.get(dk)!r}) 가 실렸는데 상태 {st!r} — 숫자를 싣는 가지는 '
                                    f'{list(CERT_PUBLISHED_STATES)}'))
        elif not has_num and st not in CERT_UNPUBLISHED_STATES:
            out.append((branch, sk, f'숫자 없음 ↔ 상태 {st!r} (사유 {rsn!r}) — 해가 없는 가지는 {list(CERT_UNPUBLISHED_STATES)} 로 이유를 말한다'))
        elif not has_num and not (isinstance(rsn, str) and rsn):
            out.append((branch, rk, f'숫자 없는 가지 ({st}) 의 사유가 없다 ({rsn!r}) — 정직한 실패는 이유를 말한다 (G2RR2-05)'))
    return out


def branch_table_problems(m, rec):
    """★ 10-07 G2RR2-05 (Codex 세대 2 재검증 2 §6) — 세대 2 이온 모드 레코드 한 모드 → 가지 표 어긋남 ['키: 사유'] ([] = 통과).
    공용 계약 (`certificate_binding_problems` — 정지 계약 ⑨ · 공용 기록 검사 · τ 소비자 · 인계 P4) 이 이 결과를 그대로 싣고, 다시 읽기 K7 이 이 결과를
    그대로 쓴다 (별도 자격 없음).  공용 기술 검사 (`ion_record_problem`) 를 못 넘은 레코드는 [] (같은 문 — 그 검사가 먼저 거부한다)."""
    if not isinstance(rec, dict) or m not in CERT_ROLE or ion_record_problem(rec) is not None:
        return []
    return [f'{k}: {w}' for _b, k, w in _branch_table(rec)]


def _se_material():
    """σ₀ 온도 규약의 정본 (se_material — 생산자 `network_conductivity._run_all_networks` 와 같은 함수) — 부를 때만 임포트한다."""
    import se_material as _sm
    return _sm


def sigma0_convention_problem(rec):
    """★ 10-07 G2RR2-04 — 레코드의 σ₀ (sigma_grain_S_cm) = 그 레코드의 온도 규약 (temperature_provenance — T_C · Ea_ion_eV · T_ref_C 로 se_material 을
    다시 부른 값) 인가 → None | 사유.  T_dependence (NOT_MODELLED ⇔ T_C 없음) · sigma_ion_T_factor 도 같은 규약이어야 한다.  허용 = 상대
    SIGMA0_CONVENTION_REL_TOL (같은 함수 · 같은 인자 — 다른 기계의 libm 마지막 자리만).  옛 판은 두 모드의 (σ₀, 온도) 가 서로 같은지만 봐서, 모드 셋 ·
    사본 넷의 T_C 만 60 °C 로 바꾼 레코드가 σ₀ 3.0 mS/cm '@60 °C' 로 게시 · 인계됐다.
    ★ 10-16 L214R-10 — 다시 계산한 σ_grain · 배수가 유한 양수가 아니거나 대조의 차 · 허용이 유한하지 않으면 (넘침 · 밑넘침) 생산자 NON_FINITE_REASON 꼬리표 사유
    (None 아님 · inf ≤ inf 를 같다로 읽지 않는다)."""
    if not isinstance(rec, dict):
        return f'레코드가 객체가 아니다 ({type(rec).__name__})'
    s0, prov = _pos(rec.get('sigma_grain_S_cm')), rec.get('temperature_provenance')
    if s0 is None or not isinstance(prov, dict):
        return (f'σ₀ (sigma_grain_S_cm) {rec.get("sigma_grain_S_cm")!r} · 온도 규약 (temperature_provenance) {type(prov).__name__} — 둘 다 있어야 '
                '그 실행의 온도 규약과 대조할 수 있다')
    t_c, ea, t_ref = prov.get('T_C'), prov.get('Ea_ion_eV'), prov.get('T_ref_C')
    why = [f'{k} {v!r} — 유한 수가 아니다' for k, v in (('T_C', t_c), ('Ea_ion_eV', ea)) if v is not None and _num(v) is None]
    if _num(t_ref) is None:
        why.append(f'T_ref_C {t_ref!r} — 유한 수가 아니다')
    if why:
        return '온도 규약 기록 형식 — ' + ' · '.join(why)
    sm = _se_material()
    try:
        want = sm.sigma_grain_S_cm(_num(t_c), _num(ea), _num(t_ref))
        fac = sm.arrhenius_sigma_factor(_num(t_c), _num(ea), _num(t_ref))
    except (TypeError, ValueError, OverflowError) as e:
        return f'온도 규약을 다시 계산할 수 없다 ({type(e).__name__}: {e})'
    #  ★ 10-16 L214R-10 (같은 부류 N2 · L214R-01 A · 05 · 07 과 같은 규칙) — 다시 계산한 σ_grain · 규약 배수 (want · fac) 와 대조의 차 · 허용을 비교 **전에** 본다:
    #    want · fac = 유한 양수 · 차 · 허용 = 유한.  옛 판은 T_C −272.15 · Ea −0.0613 eV 에서 (T_ref/T)·exp(…) 가 예외 없이 +∞ (exp 는 넘치지 않고 곱이 넘친다) →
    #    |σ₀ − ∞| ≤ 1e−12·∞ (inf ≤ inf) 가 참이라 **어떤 σ₀ 든** None 이었다 (σ₀ 결합 · 증서 결합 · 세대 계약 · τ 행 · 정지 계약 ⑧ ⑨ · 기록 판정 · 다시 읽기가
    #    받았다) · 0 으로 밑넘친 배수는 어긋남으로만 걸렸다.  넘침 · 밑넘침 = 기술 실패 사유 (생산자 NON_FINITE_REASON 꼬리표 · None 아님) — 정상 규약 (25 °C 상수
    #    3e−3 · 생산자의 Arrhenius 값) 은 식 · 허용 · 판정 · 문구 그대로 (같은 식을 미리 계산해 둘 뿐)
    f_rec = _num(prov.get('sigma_ion_T_factor'))
    d_f = None if f_rec is None else abs(f_rec - fac)
    tol_f, d_s, tol_s = SIGMA0_CONVENTION_REL_TOL * abs(fac), abs(s0 - want), SIGMA0_CONVENTION_REL_TOL * abs(want)
    if not (math.isfinite(want) and want > 0 and math.isfinite(fac) and fac > 0
            and all(math.isfinite(v) for v in (tol_f, d_s, tol_s) + (() if d_f is None else (d_f,)))):
        return (f'{_nc_mod().NON_FINITE_REASON} — 온도 규약 (T_C {t_c!r} · Ea {ea!r} · T_ref {t_ref!r}) 을 다시 계산한 σ_grain {want!r} · 규약 배수 {fac!r} 가 '
                f'유한 양수가 아니거나 대조의 차 · 허용 (배수 {d_f!r} / {tol_f!r} · σ₀ {d_s!r} / {tol_s!r}) 이 유한하지 않다 — 넘침 · 밑넘침 ((T_ref/T)·exp(…) 가 '
                '예외 없이 +∞ · 0) · inf ≤ inf 를 같다로 읽지 않는다 (생산자는 이 규약으로 σ₀ 를 내지 않는다)')
    bad = []
    dep = 'NOT_MODELLED' if t_c is None else 'ARRHENIUS'
    if prov.get('T_dependence') != dep:
        bad.append(f'T_dependence {prov.get("T_dependence")!r} ≠ {dep!r} (T_C {t_c!r})')
    if f_rec is None or not d_f <= tol_f:
        bad.append(f'sigma_ion_T_factor {prov.get("sigma_ion_T_factor")!r} ≠ 규약 배수 {fac!r}')
    if not d_s <= tol_s:
        bad.append(f'σ₀ {s0!r} S/cm ≠ 온도 규약 (T_C {t_c!r} · Ea {ea!r} · T_ref {t_ref!r}) 의 σ_grain {want!r}')
    return ('σ₀ ↔ 온도 규약 (G2RR2-04): ' + ' · '.join(bad)) if bad else None


def sigma0_binding_problems(rec):
    """★ 10-07 G2RR2-04 (Codex 세대 2 재검증 2 §5 최소 수정) — 망 레코드 한 모드 (dual 의 hertzian · physics · H12) 의 σ₀ 결합 → ['사유'] ([] = 통과).
      · 부모 σ₀ ↔ 그 레코드의 온도 규약 (`sigma0_convention_problem`)
      · 이온 세 가지 (FULL · CF · 협착-only) 증서의 sigma_bulk_S_cm = 부모 sigma_grain_S_cm — 정확히 (생산자가 같은 float 을 쓴다 · FULL 도 표기 어긋남 거부 ·
        해 없는 가지의 증서도 σ₀ 를 실었으면 같아야)
      · 전자 · 열 채널 증서 (`electronic_` · `thermal_`) = 그 채널의 기준 전도도 (생산자 상수) · 채널 이름 — 이온 σ₀ 를 강제하지 않는다
    정지 계약 ⑧ (`pipeline_service.network_sigma0_problem` — 승격 전 투영 · 게시 · 인계 P4 재검사) 과 세대 2 계약 (`certificate_binding_problems` — ⑨ · 공용
    기록 검사 · τ 소비자 · 다시 읽기 K2) 이 이 한 함수를 부른다 (사본 금지 — 규율 ①)."""
    if not isinstance(rec, dict):
        return [f'레코드가 객체가 아니다 ({type(rec).__name__})']
    out = []
    cv = sigma0_convention_problem(rec)
    if cv:
        out.append(cv)
    p0 = rec.get('sigma_grain_S_cm')
    for _b, *_k, ck in CERT_BRANCH_KEYS:
        c = rec.get(ck)
        if isinstance(c, dict) and 'sigma_bulk_S_cm' in c:
            cs = c.get('sigma_bulk_S_cm')
            csn = _nc_mod()._cert_num(cs)                       # ★ 10-16 L214R-05 — 증서 값의 큰 JSON 정수 = None (아래 사유) · 예외 아님 (생산자 `_cert_num` 그대로)
            if csn is None or _num(p0) is None or csn != _num(p0):
                out.append(f'{ck}: 증서 σ₀ (sigma_bulk_S_cm) {cs!r} ≠ 부모 σ₀ (sigma_grain_S_cm) {p0!r} — 이온 가지 증서는 그 실행의 σ₀ 로 풀린다 '
                           '(G2RR2-04 · 정확히 같은 수)')
    refs = None
    for pre in CHANNEL_PREFIXES:
        for _b, *_k, ck in CERT_BRANCH_KEYS:
            c = rec.get(pre + ck)
            if not isinstance(c, dict):
                continue
            if refs is None:
                nc = _nc_mod()
                refs = {p_: float(getattr(nc, a_)) for p_, a_ in CHANNEL_SIGMA_REF.items()}
            #  ★ 10-16 L214R-08 — 큰 JSON 정수 (`_num` = None) ≠ 기준 전도도 → 아래 사유 (옛 판 = OverflowError · 키가 있으면 값이 맞아야 — 없음으로 읽지 않는다)
            if 'sigma_bulk_S_cm' in c and _num(c.get('sigma_bulk_S_cm')) != refs[pre]:
                out.append(f'{pre}{ck}: 증서 σ_bulk {c.get("sigma_bulk_S_cm")!r} ≠ {CHANNEL_CERT_NAME[pre]} 채널 기준 전도도 {refs[pre]!r} '
                           f'(network_conductivity.{CHANNEL_SIGMA_REF[pre]} · G2RR2-04)')
            if 'channel' in c and c.get('channel') != CHANNEL_CERT_NAME[pre]:
                out.append(f'{pre}{ck}: 증서 채널 {c.get("channel")!r} ≠ 자리 {CHANNEL_CERT_NAME[pre]!r} (G2RR2-04 · 채널마다 그 채널의 기준 전도도)')
    return out


def certificate_binding_problems(m, rec):
    """★ 10-06 밤 G2RR-02 — 세대 2 레코드 한 모드 (hertz · hertz_h12 · physics) → 증서 결합 어긋남 목록 ([] = 통과 · 정책 = 위 절 · CERT_BRANCH_POLICY).
    공용 기술 검사 (`ion_record_problem`) 를 못 넘은 레코드는 [] — 모든 소비처가 그 검사로 먼저 거부한다.
    ★ 10-07 — G2RR2-05 가지 표 (`branch_table_problems` — 상태 기록 결손 · 사유 없음 · 모르는 상태) · G2RR2-04 σ₀ 결합 (`sigma0_binding_problems`) 을 싣는다
    (가지 표에서 이미 어긋난 가지는 증서 검사를 겹치지 않는다)."""
    if not isinstance(rec, dict) or m not in CERT_ROLE or ion_record_problem(rec) is not None:
        return []
    table = _branch_table(rec)
    out = [f'{k}: {w}' for _b, k, w in table]
    bad_b = {b for b, _k, _w in table}
    for branch, qk, dk, sk, rk, ck in CERT_BRANCH_KEYS:
        if branch in bad_b:
            continue
        q, sd, st, cert = rec.get(qk), rec.get(dk), rec.get(sk), rec.get(ck)
        if branch == 'full' and st == 'not_computed' and rec.get(rk) == MODEL_LIMIT_REASON and q is None and sd is None:
            #  ★ 10-15 L214-02 (consumer C1 #3) — FULL 모형 한계 가지: 실제 FULL 수치 증서를 **보존**한 것이 정상이다 ("숫자 없는 가지가 해를 주장" 규칙의 예외 ·
            #    증서를 버리거나 상태만 바꿔 옛 검사를 통과시키지 않는다) — 공용 판정 (자리의 역할 · 증서 결합 · q 재구성) 으로만 받는다
            why = full_model_limit_problem(rec, 'ionic', m)
        elif st in CERT_PUBLISHED_STATES or q is not None or sd is not None:
            why = _cert_published_problem(m, branch, rec, q, sd, st, cert)
        else:
            why = _cert_unpublished_problem(branch, st, rec.get(rk), cert)
        if why:
            out.append(f'{ck}: {why}')
    out += sigma0_binding_problems(rec)
    return out


def _cert_geometry_problems(recs):
    """한 실행 (dual 의 모드 레코드 · 채널 사본 · H12) 의 모든 증서가 같은 기하 (geometry · g_to_q) 를 싣는가 — 봉인된 기하 → [(모드, 사유)]."""
    seen = {}
    for m in MODES:
        rec = recs.get(m)
        if not isinstance(rec, dict):
            continue
        for pre in ('',) + CHANNEL_PREFIXES:
            for *_k, ck in CERT_BRANCH_KEYS:
                c = rec.get(pre + ck)
                if isinstance(c, dict) and ('geometry' in c or 'g_to_q' in c):
                    key = json.dumps([c.get('geometry'), c.get('g_to_q')], sort_keys=True, default=str)
                    seen.setdefault(key, []).append((m, pre + ck))
    if len(seen) <= 1:
        return []
    groups = sorted(seen.items(), key=lambda kv: -len(kv[1]))
    ref_key, ref_where = groups[0]
    return [(where[0][0], f'봉인된 기하 불일치 — {[f"{m_}.{k_}" for m_, k_ in where][:4]} 의 기하 · G→q {key} ≠ 같은 실행의 다른 증서 '
                          f'{len(ref_where)} 개 (예: {ref_where[0][0]}.{ref_where[0][1]}) 의 {ref_key} — 한 실행의 증서는 한 기하로 풀렸다')
            for key, where in groups[1:]]


def _g2_mode_problems(m, rec):
    """세대 2 한 모드 레코드 → 어긋남 목록 (부분 결손 · 모르는 값 · 다른 역할의 값).  생산자 실패 레코드 (sigma_full_status not_computed — H12 풀이
    예외 가지는 표기 일부만 싣는다) 는 **있는** 표기만 대조한다 — 그 모드는 공용 기술 검사가 solver_guard 로 막아 값이 실리지 않는다."""
    bad = []
    #  ★ 10-15 L214-02 (Codex LHS214 판정 §2 · consumer C1 #2) — 표기 결손 면제는 **게시되지 않는 진짜 실패 레코드**에만.  FULL 모형 한계 (사유 full_over_conduction)
    #    레코드는 게시될 수 있으므로 정상 세대 표기를 전부 요구한다 (옛 판: not_computed 면 무엇이든 면제 → bulk_model 삭제가 [] 로 통과).
    failed = rec.get('sigma_full_status') == 'not_computed' and rec.get('sigma_full_reason') != MODEL_LIMIT_REASON
    want = dict(G2_MODE_CONTRACT[m])
    for k, v in G2_MODE_CONTRACT[m]:
        if v is None:
            if rec.get(k) is not None:
                bad.append(f'{k}={rec.get(k)!r} (없어야 한다)')
        elif k not in rec:
            if not failed:
                bad.append(f'{k} 없음 (부분 결손)')
        elif rec.get(k) != v:
            bad.append(f'{k}={rec.get(k)!r} ≠ {v!r}')
    for p in CHANNEL_PREFIXES:
        for k in G2_CHANNEL_LABELS:
            if p + k in rec and rec.get(p + k) != want.get(k):
                bad.append(f'{p}{k}={rec.get(p + k)!r} ≠ {want.get(k)!r}')
    #  (10-06 밤 G2R-03 의 FULL 수치 증서 검사는 ★ G2RR-02 에서 `certificate_binding_problems` 로 옮겼다 — 같은 수치 검사 + 가지 · 역할 · 발행값 결합 ·
    #   숫자를 싣는 CF · 협착-only 진단 · 종류 'cert' 로 따로 보고한다.)
    return bad


def _legacy_mode_problems(m, rec):
    """옛 세대로 추론할 한 모드 레코드 → 옛 세대 표 (`LEGACY_MODE_CONTRACT`) 와의 어긋남 목록."""
    return [f'{k}={rec.get(k)!r} ∉ {allowed}' for k, allowed in LEGACY_MODE_CONTRACT.get(m, ()) if rec.get(k) not in allowed]


def network_generation_contract(dual):
    """망 레코드 묶음 (dual — 'hertzian' · 'physics' · Hertz 안 'hertz_h12') → 세대 계약 판정 (표기만 본다 · 값 무관).

      → {'generation': 'g2' | 'inferred_legacy' | 'invalid' | '' (모드 레코드가 하나도 없음),
         'problems': [(모드, 종류, 세부)] — 종류 = 'role' (세대 2 표와 어긋남 · 부분 결손 · 모르는 값) · 'missing_h12' (세대 2 Hertz 에 H12 없음) ·
                     'not_object' (H12 자리가 객체가 아님) · 'legacy_role' (옛 세대 표와 어긋남) ·
                     ★ 'cert' (10-06 밤 G2RR-02 — 수치 증서 · 결합: `certificate_binding_problems` · 봉인된 기하 `_cert_geometry_problems`),
         'markers': {모드: [세대 2 표지]}}"""
    d = dual if isinstance(dual, dict) else {}
    recs = {m: mode_record(d, m) for m in MODES}
    present = [m for m in MODES if recs[m] is not None]
    rh = d.get(DUAL_KEY['hertz'])
    if not present:
        return {'generation': '', 'problems': [], 'markers': {}}
    markers = {m: g2_markers(recs[m]) for m in present}
    probs = []
    if any(markers.values()):
        for m in present:
            bad = _g2_mode_problems(m, recs[m])
            if bad:
                probs.append((m, 'role', ' · '.join(bad)))
            #  ★ 10-06 밤 G2RR-02 — 수치 증서 · 결합 (가지 · 채널 · 역할 · 전극 · ΔV · 기하 · 발행값 재구성 · 숫자를 싣는 진단 · 해 없는 가지)
            cb = certificate_binding_problems(m, recs[m])
            if cb:
                probs.append((m, 'cert', ' · '.join(cb)))
        for m, det in _cert_geometry_problems(recs):                     # ★ G2RR-02 — 한 실행의 증서 = 한 기하 (봉인된 기하)
            probs.append((m, 'cert', det))
        if recs['hertz'] is not None and recs[H12_MODE] is None:
            if H12_MODE in rh:
                probs.append((H12_MODE, 'not_object', f'H12 자리 (hertzian.{H12_MODE}) 가 객체가 아니다 ({type(rh.get(H12_MODE)).__name__})'))
            else:
                probs.append((H12_MODE, 'missing_h12', f'세대 2 Hertz 레코드에 이온 민감도 레코드 ({H12_MODE}) 가 없다 — 생산자 (hertzian 실행) 는 늘 '
                                                        '함께 낸다 (부분 결손)'))
        gen = NET_GEN_G2
    else:
        for m in present:
            bad = _legacy_mode_problems(m, recs[m])
            if bad:
                probs.append((m, 'legacy_role', ' · '.join(bad)))
        gen = NET_GEN_LEGACY
    return {'generation': NET_GEN_BAD if probs else gen, 'problems': probs, 'markers': markers}


def generation_contract_text(con):
    """세대 계약 판정 → 사유 문장 ('' = 문제 없음) — 모드 · 역할 · 어긋남."""
    out = []
    for m, kind, det in (con or {}).get('problems') or []:
        if kind == 'role':
            out.append(f'{m}: {ROLE_NAME.get(m, m)} 역할 표기가 아니다 — {det}')
        elif kind == 'legacy_role':
            out.append(f'{m}: 세대 2 표기가 없는데 옛 세대 역할 표기도 아니다 — {det}')
        elif kind == 'cert':                                           # ★ 10-06 밤 G2RR-02
            out.append(f'{m}: 수치 증서 · 결합 (G2R-03 · G2RR-02 — 가지 · 역할 · 발행값) — {det}')
        else:
            out.append(f'{m}: {det}')
    return '; '.join(out)


#: 행 표기 칸 (`ion_net_<칸>_<모드>`) — 세대 계약을 행에서 다시 보는 데 쓴다 (`row_generation_problems`).
ROW_META = ('constriction', 'psi', 'area_rule', 'electrode', 'bulk', 'area_mode')


def _row_meta(m, res, legacy):
    """망 레코드 한 모드 → 행 표기 칸 (`ion_columns` 와 같은 표기 함수)."""
    g_area, g_elec, g_bulk = generation_meta(res, m, legacy)
    return {'constriction': constriction_label(res, legacy),
            'psi': ((res or {}).get('psi_placement') or '') if m in ('physics', H12_MODE) else '',
            'area_rule': g_area, 'electrode': g_elec, 'bulk': g_bulk, 'area_mode': ('hertz' if m == H12_MODE else m)}


def _expected_row_meta():
    """세대마다 · 모드마다 행 표기 칸의 허용 값 — 계약 표 (`G2_MODE_CONTRACT` · `LEGACY_MODE_CONTRACT`) 를 `ion_columns` 와 **같은 표기 함수**로 옮긴 것
    (표가 하나라 행 판정이 레코드 판정과 갈라지지 않는다).  None = 그 세대에 없는 모드."""
    exp = {NET_GEN_G2: {}, NET_GEN_LEGACY: {}}
    for m in MODES:
        canon = {k: v for k, v in G2_MODE_CONTRACT[m] if v is not None}
        exp[NET_GEN_G2][m] = {b: {v} for b, v in _row_meta(m, canon, False).items()}
        if m not in LEGACY_MODE_CONTRACT:
            exp[NET_GEN_LEGACY][m] = None
            continue
        keys = [k for k, _a in LEGACY_MODE_CONTRACT[m]]
        sets = {}
        for combo in itertools.product(*(a for _k, a in LEGACY_MODE_CONTRACT[m])):
            canon = {k: v for k, v in zip(keys, combo) if v is not None}
            for b, v in _row_meta(m, canon, True).items():
                sets.setdefault(b, set()).add(v)
        exp[NET_GEN_LEGACY][m] = sets
    return exp


_EXPECTED_ROW_META = _expected_row_meta()


def row_generation_problems(row):
    """τ 인계 행 (`ion_columns` 값 · 인계 원천 직렬화 칸 · 인계표 CSV 행) → (세대, [문제]) — 행 하나의 세대 계약 (코호트 판정 **앞**에 행마다).

      세대 칸 (`ion_net_generation`) 이 있는 행 (새 스키마) — 값은 g2 · inferred_legacy 여야 하고 (invalid · 모르는 값 = 위반) 모드마다 표기 칸
        (`ion_net_<협착 · ψ · 면적 규칙 · 전극 · bulk · 면적 모드>_<모드>`) 이 **전부** 있고 그 세대의 허용 값 (`_expected_row_meta`) 이어야 한다 ·
        세대 2 는 주 Hertz 가 있으면 H12 도 필수 · 옛 세대는 H12 없음.
      세대 칸이 없는 행 (계약 전 스키마 — v1.2 인계표 등) — 있는 표기 칸만 대조 · 세대는 전극 칸으로 (dirichlet_exact = 세대 2 · virtual_source_legacy =
        옛 세대) · 전극 칸도 없으면 옛 세대 (그 스키마는 세대 2 전 tau_flux 의 것 — 세대 2 행에는 늘 전극 칸이 있다).
      레코드 없는 행 (모든 표기 칸 빈칸 — 폴더 · dual 없음) — ('', []) 판정 밖.
    값 · 직렬화 칸 둘 다 문자열로 대조한다."""
    r = row if isinstance(row, dict) else {}

    def cell(k):
        v = r.get(k)
        return '' if v is None else str(v)
    new_schema = ROW_GENERATION_COL in r
    present = [m for m in MODES if any(cell(f'ion_net_{b}_{m}') for b in ('constriction', 'electrode', 'bulk', 'area_rule'))]
    g = cell(ROW_GENERATION_COL) if new_schema else None
    if not present:
        return ('', []) if not g else (g, [f'세대 칸 {g!r} 인데 모드 표기가 하나도 없다'])
    if g is None:
        if any(f'ion_net_electrode_{m}' in r for m in MODES):
            el = {cell(f'ion_net_electrode_{m}') for m in present}
            g = NET_GEN_G2 if el == {ELECTRODE_G2} else NET_GEN_LEGACY if el == {ELECTRODE_LEGACY} else ''
            if not g:
                return '', [f'세대 칸 없는 행의 전극 표기 {sorted(el)} — 한 세대로 읽을 수 없다']
        else:
            g = NET_GEN_LEGACY
    if g == NET_GEN_BAD:
        return g, ['세대 계약 위반 (invalid — 사유는 그 행의 상태 칸 · network_generation_contract)']
    if g not in (NET_GEN_G2, NET_GEN_LEGACY):
        return g, [f'모르는 세대 칸 {g!r} (g2 · inferred_legacy 만)']
    probs = []
    for m in MODES:
        want = _EXPECTED_ROW_META[g].get(m)
        if want is None:
            if m in present:
                probs.append(f'{m}: 세대 {g} 에 없는 모드인데 표기가 있다')
            continue
        if m not in present:
            if g == NET_GEN_G2 and m == H12_MODE and 'hertz' in present:
                probs.append(f'{m}: 세대 2 행인데 H12 표기가 없다 (부분 결손 — 세대 2 Hertz 는 늘 H12 를 함께 낸다)')
            continue
        role = ROLE_NAME.get(m, m) if g == NET_GEN_G2 else '옛 세대'
        for b, allowed in want.items():
            col = f'ion_net_{b}_{m}'
            if col not in r:
                if new_schema:
                    probs.append(f'{col} 칸 없음')
                continue
            if cell(col) not in allowed:
                probs.append(f'{col}={cell(col)!r} ∉ {sorted(allowed)} ({role} 역할)')
    return g, probs


#: 세대 축 (여러 행이 한 표 · 한 학습 집합에 들어갈 때 같아야 하는 것) — 세대 · ψ 배치 (physics 협착 라벨에서) · physics 면적 규칙 · 전극 ·
#:   ★ 10-06 밤 (G2R-01) 모드별 협착 · bulk (옛 축에는 주 Hertz 의 bulk · 협착이 없어 H12 를 주 자리에 둔 행이 축으로는 같았다).
GENERATION_AXES = ('generation', 'psi', 'area_rule_physics', 'electrode') + tuple(f'{b}_{m}' for m in MODES for b in ('constriction', 'bulk'))
_PSI_FROM_LABEL = {'mikic_psi_multiply': 'multiply', 'mikic_psi_divide': 'legacy_divide'}


def generation_axes(row):
    """τ 인계 행 (값 또는 직렬화 칸) → 세대 축 dict (GENERATION_AXES) — 빈칸 = 그 축의 레코드 없음.
    ψ = physics 협착 라벨에서 · 모르는 라벨 (unknown:…) 은 **그대로** 축 값이 된다 (옛 판은 빈 축으로 만들어 비교에서 빠졌다 — G2R-02) ·
    전극 = 레코드 있는 모드의 처음 값 (한 행 안 어긋남은 행 계약이 먼저 본다)."""
    r = row if isinstance(row, dict) else {}
    lab = str(r.get('ion_net_constriction_physics') or '')
    out = {'generation': str(r.get(ROW_GENERATION_COL) or ''), 'psi': _PSI_FROM_LABEL.get(lab, lab),
           'area_rule_physics': str(r.get('ion_net_area_rule_physics') or ''),
           'electrode': next((str(r.get(f'ion_net_electrode_{m}')) for m in MODES if r.get(f'ion_net_electrode_{m}')), '')}
    for m in MODES:
        for b in ('constriction', 'bulk'):
            out[f'{b}_{m}'] = str(r.get(f'ion_net_{b}_{m}') or '')
    return out


def generation_mixing_problem(rows):
    """여러 행 → '' (한 세대 · 또는 판정할 표기 없음) | 사유.
    ★ 10-06 밤 (G2R-02) — **행마다 세대 계약 먼저** (`row_generation_problems` — 같은 결함만 모인 코호트도 걸린다 · 옛 판은 "서로 같다" 를 "유효하다" 로
    썼다) · 그다음 세대 축 섞임 (세대 · ψ · physics 면적 · 전극 · 모드별 협착 · bulk).  빈칸 축 · 레코드 없는 행은 판정 밖."""
    bad_rows = []
    for r in rows or []:
        g, probs = row_generation_problems(r)
        if probs:
            bad_rows.append(f'{(r or {}).get("case") or (r or {}).get("case_id") or "?"} ({g or "?"}): {probs[0]}'
                            + (f' 외 {len(probs) - 1}' if len(probs) > 1 else ''))
    if bad_rows:
        return ('세대 계약 위반 행 (G2R-01 · 02 — 행마다 먼저 · 같은 결함만 모인 코호트도 거부): ' + '; '.join(bad_rows[:5])
                + (f' … 모두 {len(bad_rows)} 행' if len(bad_rows) > 5 else ''))
    seen = {a: {} for a in GENERATION_AXES}
    for r in rows or []:
        ax = generation_axes(r)
        for a in GENERATION_AXES:
            if ax[a]:
                seen[a].setdefault(ax[a], (r or {}).get('case') or (r or {}).get('case_id') or '?')
    bad = [f'{a}: ' + ' · '.join(f'{v} (예: {c})' for v, c in sorted(vals.items())) for a, vals in seen.items() if len(vals) > 1]
    return ('세대 섞임 — 한 표 · 학습 집합에 세대가 다른 행 (세대 · ψ 배치 · physics 면적 규칙 · 전극 · 모드별 협착 · bulk) 을 표기 없이 섞지 않는다: '
            + '; '.join(bad)) if bad else ''


def _sigma0(res):
    """망 결과 → (σ₀ mS/cm, T °C) 또는 None.  σ₀ = 간선 재료 σ (`sigma_grain_S_cm`, 이미 그 T 의 Arrhenius 값) · T = provenance
    T_C (None 이면 규약 기준 T_ref_C = 25 °C · NOT_MODELLED)."""
    s = _pos(res.get('sigma_grain_S_cm'))
    prov = res.get('temperature_provenance')
    if s is None or not isinstance(prov, dict):
        return None
    t = _num(prov.get('T_C'))
    if t is None:
        if prov.get('T_C') is not None:
            return None
        t = _num(prov.get('T_ref_C'))
    if t is None:
        return None
    return (round(s * 1000.0, 10), t)


def _blank(m):
    return {f'f_ion_{m}': None, f'f_ion_{m}_gap': None, f'tau2_ion_{m}': None, f'tau_ion_{m}': None}


def ion_columns(dual, ledger, perc_pct, sigma0_T_claim=None):
    """한 케이스의 이온 인계 열.

    dual          — `network_conductivity_dual.json` ({'hertzian': 결과, 'physics': 결과}) · 한 모드만 있어도 된다
    ledger        — `full_metrics.json` 의 `thickness_um` (L_gap) · `thickness_mass_conserving_um` (L_mc) · `phi_se_mass_conserving` (φ_mc)
    perc_pct      — `calc_percolation` 의 `percolation_pct` (같은 L0 띠 · G2)
    sigma0_T_claim — 호출자가 쓰려는 σ₀ 의 온도 (°C) — 망 T 와 다르면 G4 실패.  None 이면 σ₀ 메타 = 망 자신의 값 (짝이 정의상 맞다).
                     ⚠ tau2 · f 는 무차원 sigma_full 로 계산하므로 σ₀ 수치에 무관하다 (§3-1) — G4 는 σ₀ 메타 · mS/cm 환산의 짝을 지킨다.
    """
    dual = dual if isinstance(dual, dict) else {}
    ledger = ledger if isinstance(ledger, dict) else {}
    out = {}
    L_gap, L_mc, phi_mc = (_pos(ledger.get('thickness_um')), _pos(ledger.get('thickness_mass_conserving_um')),
                           _pos(ledger.get('phi_se_mass_conserving')))
    pp = _num(perc_pct)
    if pp is not None and pp < 0:
        pp = None
    ledger_ok = None not in (L_gap, L_mc, phi_mc)
    phi_sphere = (phi_mc * L_mc / L_gap) if ledger_ok else None
    # G4 — 모드들의 σ₀ · T 짝 (공통 메타 · ★ 10-06: H12 레코드도 같은 실행의 같은 σ₀ 여야 한다)
    recs = {m: mode_record(dual, m) for m in MODES}
    s0 = {m: _sigma0(r) for m, r in recs.items() if isinstance(r, dict)}
    s0_vals = {v for v in s0.values() if v is not None}
    t_bad = len(s0_vals) > 1
    shared_s0 = next(iter(s0_vals)) if len(s0_vals) == 1 else None
    if shared_s0 is not None and sigma0_T_claim is not None:
        ct = _num(sigma0_T_claim)
        if ct is None or ct != shared_s0[1]:
            t_bad = True
    out['ion_sigma0_mScm'] = None if (t_bad or shared_s0 is None) else shared_s0[0]
    out['ion_sigma0_T_C'] = None if (t_bad or shared_s0 is None) else shared_s0[1]
    out['phi_basis'], out['L_basis'] = 'mass_conserving', 'L_mc'
    #  ★ 10-16 L214R-02 — FULL 모형 한계 독립 표지: 아래 게이트 (띠 폴백 먼저 · 관통 불일치 · 온도 짝 · 세대 계약) 의 표시와 **따로** 레코드에서 바로 (공용 판정) —
    #    상태 칸이 BAND_FALLBACK 이어도 그 모드의 모형 한계 사실이 인계 · 배포까지 간다 (표시 우선순위는 그대로)
    for m, col in MODEL_LIMIT_FLAG_COL.items():
        out[col] = full_model_limit_flag(recs[m], m)

    #  ★ 10-06 밤 세대 계약 (G2R-01 · 02) — 케이스의 세대를 닫힌 표로 먼저 정한다 (옛 판: 한 행 안 전극이 서로 같은지만 봤다 = "서로 같다" 를 "유효하다"
    #    로).  위반이면 레코드 있는 모드 전부 기술적 무효 (invalid_input · 값 빈칸) · 옛 기본값은 inferred_legacy 케이스에만 채운다.
    con = network_generation_contract(dual)
    legacy = con['generation'] == NET_GEN_LEGACY
    gen_txt = generation_contract_text(con)
    out[ROW_GENERATION_COL] = con['generation']
    for m in MODES:
        res = recs[m]
        o = _blank(m)
        rule = (res or {}).get('boundary_rule')
        meta = _row_meta(m, res, legacy) if isinstance(res, dict) else {b: '' for b in ROW_META}
        o.update({f'ion_net_area_mode_{m}': ('hertz' if m == H12_MODE else m),       # H12 면적 = Hertz 면적 (c_cpl[22]) 그대로
                  f'ion_net_constriction_{m}': meta['constriction'],             # ★ 10-06 — ψ 배치까지 본다 (세대 2 = mikic_psi_multiply)
                  f'ion_net_psi_{m}': meta['psi'],
                  f'ion_net_area_rule_{m}': meta['area_rule'], f'ion_net_electrode_{m}': meta['electrode'], f'ion_net_bulk_{m}': meta['bulk'],
                  f'ion_net_band_rule_{m}': rule if rule in BAND_RULES else '',
                  f'ion_net_band_frac_{m}': _num((res or {}).get('boundary_band_frac')),
                  f'ion_net_status_reason_{m}': ''})
        phi_net = _num((res or {}).get('phi_se'))
        if phi_net is None or phi_sphere is None:
            o[f'ion_net_basis_check_{m}'] = 'unchecked'
        else:
            d = abs(phi_net - phi_sphere)
            o[f'ion_net_basis_check_{m}'] = 'ok' if d <= PHI_TOL else f'mismatch:{d:.6g}'

        def fail(status, reason=''):
            o[f'ion_net_status_{m}'] = status
            o[f'ion_net_status_reason_{m}'] = reason
            return o

        pf = _num((res or {}).get('percolating_fraction'))
        if res is None or not ledger_ok or pp is None or pf is None or (pf is not None and pf < 0):
            out.update(fail('NOT_COMPUTED', 'missing_input'))
            continue
        if rule not in BAND_RULES:                       # 띠 규칙 기록 없음 (안 A 전) — 짐작하지 않는다
            out.update(fail('NOT_COMPUTED', 'missing_input'))
            continue
        prob = ion_record_problem(res)                   # 0b 공용 기술 검사 (RGLR-01 · 02) — 과학적 게이트 (G1 · G3 · G5) 앞 · 띠와 무관
        if prob is None and gen_txt:                      # ★ 10-06 밤 세대 계약 (G2R-01 · 02) — 케이스 전체 (한 모드가 틀리면 그 실행의 세대가 미확정)
            prob = (INVALID_INPUT, f'세대 계약 (G2R-01 · 02): {gen_txt}')
        if prob is not None:
            code, detail = prob
            out.update(fail('NOT_COMPUTED', code if code != INVALID_INPUT else f'{code}: {detail}'))
            continue
        if rule != 'L0':                                 # G1
            out.update(fail('BAND_FALLBACK'))
            continue
        if (pf > 0) != (pp > 0):                         # G2
            out.update(fail('NOT_COMPUTED', 'percolation_disagree'))
            continue
        if s0.get(m) is None:                            # G4 — 그 모드의 σ₀ · T 기록이 없다 (짝을 볼 수 없다)
            out.update(fail('NOT_COMPUTED', 'missing_input'))
            continue
        if t_bad:                                        # G4
            out.update(fail('NOT_COMPUTED', 'temperature_mismatch'))
            continue
        if pf == 0:                                      # G3
            o[f'f_ion_{m}'], o[f'f_ion_{m}_gap'] = 0.0, 0.0
            out.update(fail('NOT_PERCOLATING'))
            continue
        sf = _pos(res.get('sigma_full'))
        if sf is None:                                   # 솔버 관문 (관통인데 σ 없음 · 0 · 음수 · 비유한)
            #  ★ 10-15 L214 — 0b 가 통과시킨 not_computed 는 공용 판정이 확인한 FULL 모형 한계뿐 (그 밖 not_computed 는 0b 가 solver_guard 로 이미 막았다) →
            #    정확한 사유 그대로 (solver_guard 로 뭉개지 않는다 · 값 넷 빈칸 · 띠 · 관통 불일치 · 온도 짝 같은 앞 게이트의 우선순위는 그대로)
            mlim = res.get('sigma_full_status') == 'not_computed' and res.get('sigma_full_reason') == MODEL_LIMIT_REASON
            out.update(fail('NOT_COMPUTED', MODEL_LIMIT_REASON if mlim else 'solver_guard'))
            continue
        f = sf * L_gap / L_mc
        #  ★ 10-16 L214R-09 (L214R-06–08 수정 중 보고된 같은 부류 N1 · L214R-01 A · 05 · 07 과 같은 규칙) — 값 상태 (OK · MBCB) 를 주기 **전에** 게시할 수 f · tau2 ·
        #    tau 가 셋 다 유한 양수인가 본다 (`_pos`).  옛 판은 0b 를 통과한 밑정규 σ_ratio (옛 세대 lhs00_000 σ_ratio 1e−310 · σ_dim 1e−7 — 두 표현 항등식의 절대
        #    반폭 5e−7 안) 에서 tau2 = +∞ 로 OK · 장부 극값 (L_gap 1e308 + L_mc 1e−10 · L_mc 1e−310) 에서 f = +∞ · tau2 = tau = 0 으로 MBCB (세대 2 도 — 증서는 장부를
        #    묶지 않는다 · 정지 계약 · 다시 읽기 · 인계 관문이 받았다) · φ_mc 1e308 에서 tau2 = +∞ · f 가 0 으로 밑넘치면 (L_gap 5e−324) ZeroDivisionError 였다.
        #    넘침 · 밑넘침 = 기술 실패 (NOT_COMPUTED · invalid_input · 생산자 NON_FINITE_REASON 꼬리표 · 값 넷 빈칸 — 기존 사유 어휘 그대로) · 유한한 극값은 그대로
        #    (새 범위 문턱 없음) · 정상 행은 식 · 순서 · 값 그대로 · 비관통 (f = 0 · tau2 빈칸 = 등록된 물리적 ∞) 은 위 G3 에서 이미 끝났다
        t2 = phi_mc / f if _pos(f) is not None else None
        tau = math.sqrt(t2) if _pos(t2) is not None else None
        if None in (_pos(f), _pos(t2), _pos(tau)):
            out.update(fail('NOT_COMPUTED', f'{INVALID_INPUT}: {_nc_mod().NON_FINITE_REASON} — τ 환산이 유한 양수가 아니다: f = σ_ratio·L_gap/L_mc = {f!r} · '
                                            f'tau2 = φ_mc/f = {t2!r} · tau = √tau2 = {tau!r} (σ_ratio {sf!r} · L_gap {L_gap!r} · L_mc {L_mc!r} · φ_mc {phi_mc!r} — '
                                            '넘침 · 밑넘침 · 생산자 저장 범위 밖 입력 · +∞ · 0 을 값으로 싣지 않는다)'))
            continue
        o[f'f_ion_{m}'], o[f'f_ion_{m}_gap'], o[f'tau2_ion_{m}'], o[f'tau_ion_{m}'] = f, sf, t2, tau
        out.update(fail('MODEL_BELOW_CONTINUUM_BOUND' if t2 < 1.0 else 'OK'))   # G5 — 값 유지
    return {k: out[k] for k in column_names()}


def _load(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def case_row(case_dir, sigma0_T_claim=None):
    """케이스 폴더 → {'case': 이름, …열}.  파일이 없으면 그 사실이 상태로 남는다 (행을 빼지 않는다).
    ★ 10-05 RGLR2-02 — 폴더의 망 활성 세대가 확정되지 않았으면 (`network_generation_problem`) 두 모드 NOT_COMPUTED (generation_invalid) ·
    값 빈칸 — dual 만 읽어 옛 세대 τ 를 싣지 않는다."""
    dual = _load(os.path.join(case_dir, 'network_conductivity_dual.json'))
    fm = _load(os.path.join(case_dir, 'full_metrics.json')) or {}
    row = {'case': os.path.basename(os.path.normpath(case_dir))}
    row.update(ion_columns(dual, fm, fm.get('percolation_pct'), sigma0_T_claim=sigma0_T_claim))
    return generation_override(row, network_generation_problem(case_dir))


def _cell(v):
    if v is None:
        return ''
    if isinstance(v, float):
        return repr(v)
    return str(v)


def main(argv=None):
    ap = argparse.ArgumentParser(description='이온 망 인계 열 f · tau2 · tau (τ 결정 16 ② · v2 §5)')
    ap.add_argument('cases', nargs='+', help='케이스 폴더 (network_conductivity_dual.json + full_metrics.json)')
    ap.add_argument('--tsv', help='TSV 출력 경로 (없으면 표준 출력)')
    ap.add_argument('--json', help='JSON 출력 경로 (선택)')
    ap.add_argument('--sigma0-T-claim', type=float, help='쓰려는 σ₀ 의 온도 °C (예: 25) — 망 T 와 다르면 temperature_mismatch')
    a = ap.parse_args(argv)
    rows = [case_row(c, a.sigma0_T_claim) for c in a.cases]
    #  ★ 10-06 세대 2 — 세대가 다른 케이스 폴더를 한 표로 묶지 않는다 (ψ 배치 · physics 면적 규칙 · 전극).  TSV · JSON 을 쓰지 않고 rc 2.
    mix = generation_mixing_problem(rows)
    if mix:
        sys.stderr.write(f'[tau_flux] ⛔ {mix} — 출력하지 않는다 (같은 세대 폴더끼리 따로 부를 것)\n')
        return 2
    cols = ['case'] + column_names()
    txt = '\t'.join(cols) + '\n' + ''.join('\t'.join(_cell(r[c]) for c in cols) + '\n' for r in rows)
    if a.tsv:
        with open(a.tsv, 'w', encoding='utf-8') as fh:
            fh.write(txt)
    else:
        sys.stdout.write(txt)
    if a.json:
        with open(a.json, 'w', encoding='utf-8') as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
    n = {s: sum(1 for r in rows for m in MODES if r[f'ion_net_status_{m}'] == s) for s in STATUSES}
    sys.stderr.write('[tau_flux] ' + ' · '.join(f'{k} {v}' for k, v in n.items()) + f' (케이스 {len(rows)} × 모드 {len(MODES)})\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
