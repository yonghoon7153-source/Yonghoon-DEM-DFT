#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이온 망 인계 열 f · tau2 · tau — τ 결정 16 ② (봉인 밖 도우미 · 1저자 비준 2026-10-04 *"권고대로"*).

  python3 scripts/tau_flux.py <케이스 폴더>… [--tsv OUT] [--json OUT]     # 폴더 = network_conductivity_dual.json + full_metrics.json
  python3 scripts/test_tau_flux.py                                          # 시험 (게이트에 등록)

정본 = `docs/reviews/tau_conventions_judgment_v2_20261003.md` §5-1 (열 · 식) · §5-2 (게이트 G1–G6) · 결정 1 · 2 · 15 · 16.
모드 = `hertz` · `physics` (같은 정의 · 면적과 협착식만 다름).  상태 · 메타 키는 **모드 꼬리**를 단다 (10-04 비준 —
`ion_net_status_hertz` …).  σ₀ · 온도 · φ · L 기준은 두 모드 공통이라 꼬리가 없다.

| 열 | 식 |
|---|---|
| `f_ion_<m>` | f_mc = σ_ratio × (L_gap / L_mc) — σ_ratio = 솔버 무차원 `sigma_full` (8 자리 · `TAU-25`) · **판 간격 해의 질량보존 두께 재척도 (해 아님)** |
| `f_ion_<m>_gap` | σ_ratio 그대로 — φ_mc 와 짝짓지 말 것 (T 를 L_gap/L_mc 배 낮춘다) |
| `tau2_ion_<m>` | T = φ_SE,mc / f_mc (= φ_구합 / σ_ratio — 현행 웹앱 T 와 정의상 같은 수 · 자기상사 가정) · tortuosity factor |
| `tau_ion_<m>` | √T — **COMSOL 입력 아님** |

게이트 (먼저 걸린 것 하나만 — 순서 = 아래 표):
| 순서 | 게이트 | 실패 시 |
|---|---|---|
| 0 | 그 모드의 망 결과 · 장부 (L_gap · L_mc · φ_mc) · calc_percolation 값이 있다 · 띠 규칙 기록이 있다 (안 A · 기록 없는 옛 산출물은 짐작하지 않는다) | `NOT_COMPUTED` (`missing_input`) |
| 0b | ★ 공용 기술 검사 `ion_record_problem` (10-05 RGLR-01 · 02) — 상태 ↔ 값 (computed = σ 두 표현 유한 양수 · 관통 분율 (0, 1] · 두 표현 항등식 · valid_zero = RGL-02 의 증명된 비관통 조합만 · 그 밖 = 생산자 계약 밖) | `NOT_COMPUTED` (`invalid_input: 세부` · 생산자 not_computed 신고면 `solver_guard`) |
| 1 | G1 띠 = 솔버 기록 `boundary_rule` 이 L0 | `BAND_FALLBACK` |
| 2 | G2 솔버 관통 (`percolating_fraction > 0`) == calc_percolation (`percolation_pct > 0`) — 판정은 관통 분율로 한다 (`TAU-22` · 상태 ↔ 값 정합은 0b 가 먼저 본다) | `NOT_COMPUTED` (`percolation_disagree`) |
| 3 | G4 온도 짝 — 그 모드의 σ₀ · T 기록이 있다 (없으면 `missing_input`) · 두 모드의 (σ₀, T) 가 같다 · 호출자가 σ₀ 의 T 를 주장하면 망 T 와 같다 | `NOT_COMPUTED` (`temperature_mismatch`) |
| 4 | G3 비관통 (G1 · G2 통과 + 관통 성분 없음) | `NOT_PERCOLATING` — f = 0 · tau2 · tau 빈칸 (= ∞) |
| 5 | 관통인데 σ 가 없거나 0 · 음수 · 비유한 (0b 뒤에는 도달하지 않는 방어) | `NOT_COMPUTED` (`solver_guard`) |
| 6 | G5 f > φ (T < 1) | `MODEL_BELOW_CONTINUUM_BOUND` — **값 유지** + 표지 (빈칸으로 거르면 코퍼스를 T ≥ 1 쪽으로 선별한다) |
G6 (협착 세대) = 메타 `ion_net_constriction_<m>` · 두 모드 모두 **물리 타깃 (실험 절대 대조) HOLD** — 값은 싣는다.
상태 부류 (10-05 RGLR-01): `NOT_COMPUTED` = **기술적 실패** (입력 결손 · 무효 · 솔버 관문 · 온도 짝 · 관통 불일치 — 값 없음) ↔ `BAND_FALLBACK` ·
`NOT_PERCOLATING` · `MODEL_BELOW_CONTINUUM_BOUND` = **등록된 과학적 HOLD** (입력은 0b 를 통과한 유효값 · 규칙대로 빈칸 또는 표지).
⚠ 옛 판은 0b 가 없어 L1/L2 레코드가 G1 에서 바로 BAND_FALLBACK 로 돌아갔다 — computed 인데 σ_ratio None · NaN · −1 · 관통 분율 2 가 '과학적 HOLD'
로 통과했고 (RGLR-01), σ_ratio 만 ×4 인 레코드는 tau2 ÷4 로 OK 였다 (RGLR-02).

⚠ `ion_net_basis_check_<m>` 는 **메타**다 (게이트 아님): 망 φ (`phi_se`, 4 자리 · 판 간격 상자 · 구 부피 합) 가 장부의
φ_mc·L_mc/L_gap (= φ_구합) 와 같은지 본다 — 어긋나면 망과 장부가 다른 판 높이 · 상자 · SE 집합을 썼다는 뜻이다.
게이트로 쓰려면 새 규칙으로 등록한다 (v2 §5-2 G5 의 "새 규칙" 규약 · 1저자).
⚠ 한정어는 열 사전 (v2 §5-3) 이 정본이다 — 1세대 협착식 · ML 기술자 전용 · 실험 절대 대조 금지 · τ_e (Nguyen Eq 2) 아님 ·
'COMSOL 입력' 은 GUI Equation 확인 전 쓰지 않는다.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys

MODES = ('hertz', 'physics')
DUAL_KEY = {'hertz': 'hertzian', 'physics': 'physics'}
STATUSES = ('OK', 'NOT_PERCOLATING', 'BAND_FALLBACK', 'MODEL_BELOW_CONTINUUM_BOUND', 'NOT_COMPUTED')
#: 사유 **코드** — 사유 칸은 코드 그대로이거나 'invalid_input: 세부' (세부를 다는 것은 invalid_input 하나 · 코드는 `reason_code`).
#:   ★ 10-05 RGLR-01: invalid_input = 공용 기술 검사 (`ion_record_problem`) 가 생산자 계약 위반으로 본 레코드.
REASONS = ('solver_guard', 'missing_input', 'temperature_mismatch', 'percolation_disagree', 'invalid_input')
INVALID_INPUT = 'invalid_input'
CONSTRICTION = {'maxwell': 'maxwell_halfspace', 'mikic': 'mikic_psi_divide'}
BAND_RULES = ('L0', 'L1', 'L2')
PHI_TOL = 5e-5 + 1e-9          # 망 φ 는 4 자리 반올림 (network_conductivity `round(phi_se, 4)`) — 반폭 + 부동소수 여유
SHARED = ('ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis')
#: 생산자 (`network_conductivity.NO_THROUGH_REASON`) 의 증명된 비관통 사유 — 같은 값이어야 한다 (test_tau_flux L8 이 대조한다 · 무거운 생산자를
#:   이 도우미에서 임포트하지 않으려고 값을 둔다 — `pipeline_service.NETWORK_NO_THROUGH_REASON` 과 같은 방식).
NO_THROUGH_REASON = 'no_through_path'


def reason_code(reason):
    """사유 칸 → 사유 코드 ('invalid_input: σ_ratio None' → 'invalid_input' · '' → '')."""
    return str(reason or '').split(':', 1)[0].strip()


def _num(v):
    """유한한 수 (bool 제외) 면 float, 아니면 None."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    v = float(v)
    return v if math.isfinite(v) else None


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
                   두 표현 항등식 (`sigma_identity_tol`)
      valid_zero   RGL-02 의 증명된 비관통 조합만 — 사유 no_through_path · σ_ratio · σ_dim None (F-12) · 관통 분율 0 · CF · constr 상태 valid_zero ·
                   이온 채널 valid_zero  (정지 계약 ③ 과 같은 조합 — 'zero_value' 같은 다른 valid_zero 는 받지 않는다)
      not_computed 생산자가 "관통인데 풀지 못함" 을 신고했다 → ('solver_guard', 사유)  — 기술적 실패
      그 밖        (None · 키 없음 · 모르는 문자열 · 채널 어휘) → ('invalid_input', …)
    띠 규칙 (L0 · L1 · L2) 과 **무관하게** 같은 판정이다 — L1/L2 라는 이유로 무효값 검사를 건너뛰지 않는다 (RGLR-01).  과학적 HOLD (띠 폴백 ·
    비관통 · 연속체 하한) 의 허용은 그대로 — 이 검사를 통과한 유효 입력에서만 그 게이트로 간다."""
    if not isinstance(rec, dict):
        return INVALID_INPUT, f'망 레코드가 객체가 아니다 ({type(rec).__name__})'
    st = rec.get('sigma_full_status')
    q, sd, pf = rec.get('sigma_full'), rec.get('sigma_full_mScm'), rec.get('percolating_fraction')
    if st == 'computed':
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
        d, tol = abs(sd - 1000.0 * s0 * q), sigma_identity_tol(s0, q, sd)
        if not d <= tol:
            return INVALID_INPUT, (f'두 σ 표현 불일치 (RGLR-02): σ_dim {sd!r} mS/cm ≠ 1000·σ₀·σ_ratio = {1000.0 * s0 * q!r} '
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
        return 'solver_guard', f'생산자 not_computed ({rec.get("sigma_full_reason")!r}) — 관통인데 σ 를 못 냈다'
    return INVALID_INPUT, f'sigma_full_status={st!r} — 생산자 계약 밖 (computed · valid_zero · not_computed 만)'


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
    key = 'sigma_bulk_net_mScm' if mode == 'bulk' else METRIC_SIGMA_KEY[mode]
    return tau2_value(m.get('phi_se'), sigma0, m.get(key)), sigma0


def column_names():
    out = []
    for m in MODES:
        out += [f'f_ion_{m}', f'f_ion_{m}_gap', f'tau2_ion_{m}', f'tau_ion_{m}', f'ion_net_status_{m}',
                f'ion_net_status_reason_{m}', f'ion_net_area_mode_{m}', f'ion_net_constriction_{m}', f'ion_net_psi_{m}',
                f'ion_net_band_rule_{m}', f'ion_net_band_frac_{m}', f'ion_net_basis_check_{m}']
    return out + list(SHARED)


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
    # G4 — 두 모드의 σ₀ · T 짝 (공통 메타)
    s0 = {m: _sigma0(dual[DUAL_KEY[m]]) for m in MODES if isinstance(dual.get(DUAL_KEY[m]), dict)}
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

    for m in MODES:
        res = dual.get(DUAL_KEY[m])
        res = res if isinstance(res, dict) else None
        o = _blank(m)
        rm = (res or {}).get('resistance_model')
        rule = (res or {}).get('boundary_rule')
        o.update({f'ion_net_area_mode_{m}': m,
                  f'ion_net_constriction_{m}': CONSTRICTION.get(rm, '' if rm is None else f'unknown:{rm}'),
                  f'ion_net_psi_{m}': ((res or {}).get('psi_placement') or '') if m == 'physics' else '',
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
            out.update(fail('NOT_COMPUTED', 'solver_guard'))
            continue
        f = sf * L_gap / L_mc
        t2 = phi_mc / f
        o[f'f_ion_{m}'], o[f'f_ion_{m}_gap'], o[f'tau2_ion_{m}'], o[f'tau_ion_{m}'] = f, sf, t2, math.sqrt(t2)
        out.update(fail('MODEL_BELOW_CONTINUUM_BOUND' if t2 < 1.0 else 'OK'))   # G5 — 값 유지
    return {k: out[k] for k in column_names()}


def _load(path):
    try:
        with open(path, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return None


def case_row(case_dir, sigma0_T_claim=None):
    """케이스 폴더 → {'case': 이름, …열}.  파일이 없으면 그 사실이 상태로 남는다 (행을 빼지 않는다)."""
    dual = _load(os.path.join(case_dir, 'network_conductivity_dual.json'))
    fm = _load(os.path.join(case_dir, 'full_metrics.json')) or {}
    row = {'case': os.path.basename(os.path.normpath(case_dir))}
    row.update(ion_columns(dual, fm, fm.get('percolation_pct'), sigma0_T_claim=sigma0_T_claim))
    return row


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
    sys.stderr.write('[tau_flux] ' + ' · '.join(f'{k} {v}' for k, v in n.items()) + f' (케이스 {len(rows)} × 모드 2)\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
