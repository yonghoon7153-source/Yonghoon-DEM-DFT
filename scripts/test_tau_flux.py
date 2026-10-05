#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""이온 망 인계 열 f · tau2 · tau 도우미 (`scripts/tau_flux.py`) — τ 결정 16 ② (1저자 비준 2026-10-04 *"권고대로"*).

  python3 scripts/test_tau_flux.py

★ 정본 = `docs/reviews/tau_conventions_judgment_v2_20261003.md` §5-1 (열 · 식) · §5-2 (게이트 G1–G6) · 결정 1 · 15 · 16.
★ 비준 (10-04): 상태 · 메타 키에 **모드 꼬리** (`ion_net_status_hertz` …) · 띠 규칙은 솔버가 결과에 남긴 `boundary_rule` (안 A).
★ 반례 먼저 — 각 게이트가 막아야 할 입력을 픽스처로 먼저 적었다 (옛 코드 = 도우미 없음 → 전부 실패).
"""
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
_ok, _fail = 0, []


def chk(name, cond):
    global _ok
    if cond:
        _ok += 1
        print(f'  PASS  {name}')
    else:
        _fail.append(name)
        print(f'  FAIL  {name}')


L_GAP, L_MC, PHI_MC = 30.0, 28.5, 0.21            # 판 간격 · 질량 보존 두께 (µm) · 질량 보존 φ_SE
PHI_SPHERE = PHI_MC * L_MC / L_GAP                 # = 0.1995 (구 부피 합 · 판 간격 상자) — φ_mc·L_mc = φ_구합·L_gap


def res(mode, **kw):
    base = {'sigma_full': 0.05 if mode == 'hertzian' else 0.08, 'percolating_fraction': 0.9, 'boundary_rule': 'L0',
            'boundary_band_frac': 0.06, 'boundary_factor': 2.0, 'phi_se': round(PHI_SPHERE, 4),
            'resistance_model': 'maxwell' if mode == 'hertzian' else 'mikic', 'psi_placement': 'legacy_divide',
            'contact_mode': mode, 'n_boundary_overlap': 0, 'sigma_full_status': 'computed', 'sigma_grain_S_cm': 0.003,
            'temperature_provenance': {'T_C': None, 'T_ref_C': 25.0, 'sigma_ion_T_factor': 1.0, 'T_dependence': 'NOT_MODELLED'}}
    base.update(kw)
    #  ★ 10-05 RGLR-02 — 생산자 레코드는 σ 를 **두 표현**으로 싣는다 (σ_ratio 8 자리 · σ_dim = round(σ_ratio × σ₀[S/cm] × 1000, 6) mS/cm ·
    #    network_conductivity.run_decomposition).  손 레코드도 그 짝을 갖춘다 (공용 기술 검사가 항등식을 본다) — 따로 주면 그 값을 쓴다.
    if 'sigma_full_mScm' not in kw:
        q, s0 = base.get('sigma_full'), base.get('sigma_grain_S_cm')
        ok_ = all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) and v > 0 for v in (q, s0))
        base['sigma_full_mScm'] = round(q * s0 * 1000, 6) if ok_ else None
    return base


def npz(**kw):
    """생산자 정상 비관통 레코드 모양 (RGL-02 — valid_zero + no_through_path · σ 숫자 None (F-12) · 관통 분율 0 · CF · constr · 이온 채널 valid_zero)."""
    d = dict(percolating_fraction=0.0, sigma_full=None, sigma_full_mScm=None, sigma_full_status='valid_zero',
             sigma_full_reason='no_through_path', sigma_bulk_net_status='valid_zero', sigma_constr_net_status='valid_zero',
             ionic_status='valid_zero')
    d.update(kw)
    return d


def _rc(reason):
    """사유 칸 → 사유 코드 ('invalid_input: 세부' → 'invalid_input')."""
    return str(reason or '').split(':', 1)[0].strip()


def dual(h=None, p=None, drop=()):
    d = {'hertzian': res('hertzian', **(h or {})), 'physics': res('physics', **(p or {}))}
    for k in drop:
        d.pop(k)
    return d


LEDGER = {'thickness_um': L_GAP, 'thickness_mass_conserving_um': L_MC, 'phi_se_mass_conserving': PHI_MC}


def blank3(o, m):
    return o[f'f_ion_{m}'] is None and o[f'tau2_ion_{m}'] is None and o[f'tau_ion_{m}'] is None


def main():
    import tau_flux as tf

    o = tf.ion_columns(dual(), LEDGER, 92.0)
    f_h = 0.05 * L_GAP / L_MC
    # ── A. 값 · 키 ──
    chk('A1 OK (hertz): f = σ_ratio·L_gap/L_mc · tau2 = φ_mc/f · tau = √tau2 · f_gap = σ_ratio · 상태 OK',
        o['ion_net_status_hertz'] == 'OK' and o['ion_net_status_reason_hertz'] == ''
        and o['f_ion_hertz'] == f_h and o['f_ion_hertz_gap'] == 0.05
        and o['tau2_ion_hertz'] == PHI_MC / f_h and o['tau_ion_hertz'] == math.sqrt(PHI_MC / f_h))
    chk('A2 tau2 = φ_구합 / σ_ratio (현행 웹앱 T 와 정의상 같은 수 — 결정 1 · v2 §3-7) · 상대 1e-12',
        abs(o['tau2_ion_hertz'] / (PHI_SPHERE / 0.05) - 1) < 1e-12 and abs(o['tau2_ion_physics'] / (PHI_SPHERE / 0.08) - 1) < 1e-12)
    want = set()
    for m in ('hertz', 'physics'):
        want |= {f'f_ion_{m}', f'f_ion_{m}_gap', f'tau2_ion_{m}', f'tau_ion_{m}', f'ion_net_status_{m}',
                 f'ion_net_status_reason_{m}', f'ion_net_area_mode_{m}', f'ion_net_constriction_{m}', f'ion_net_psi_{m}',
                 f'ion_net_band_rule_{m}', f'ion_net_band_frac_{m}', f'ion_net_basis_check_{m}'}
    want |= {'ion_sigma0_mScm', 'ion_sigma0_T_C', 'phi_basis', 'L_basis'}
    chk('A3 키 = v2 §5-1 (상태 · 메타는 모드 꼬리 — 10-04 비준) · 꼬리 없는 상태 키 (`ion_net_status`) 없음',
        set(o) == want and 'ion_net_status' not in o)
    chk('A4 메타: 면적 모드 hertz/physics · 협착 maxwell_halfspace / mikic_psi_divide · ψ = physics 만 legacy_divide · '
        'σ₀ 3.0 mS/cm @ 25 °C · phi_basis mass_conserving · L_basis L_mc',
        o['ion_net_area_mode_hertz'] == 'hertz' and o['ion_net_area_mode_physics'] == 'physics'
        and o['ion_net_constriction_hertz'] == 'maxwell_halfspace' and o['ion_net_constriction_physics'] == 'mikic_psi_divide'
        and o['ion_net_psi_physics'] == 'legacy_divide' and o['ion_net_psi_hertz'] == ''
        and o['ion_sigma0_mScm'] == 3.0 and o['ion_sigma0_T_C'] == 25.0
        and o['phi_basis'] == 'mass_conserving' and o['L_basis'] == 'L_mc')
    chk('A5 띠 메타 = 솔버 기록 그대로 (규칙 L0 · 폭 0.06)',
        o['ion_net_band_rule_hertz'] == 'L0' and o['ion_net_band_frac_hertz'] == 0.06)
    #  ★ 10-05 RGLR-01 — 사유 코드에 invalid_input (공용 기술 검사 · 생산자 계약 위반 레코드) 이 더해졌다 → 다섯.  사유 칸은 코드 그대로이거나
    #    'invalid_input: 세부' — 코드는 `reason_code` 로 읽는다.
    #  ★ 10-05 RGLR2-02 (Codex 3차 재검증) — generation_invalid (케이스 폴더의 망 활성 세대가 확정되지 않음 · 읽는 쪽 fail-closed) → 여섯.
    #    세부를 다는 코드 = invalid_input · generation_invalid.
    chk('A6 상태 값은 다섯 중 하나 · 사유 코드는 여섯 중 하나 (RGLR-01 invalid_input · RGLR2-02 generation_invalid 추가) — SOLVER_ANOMALY 를 '
        '쓰지 않는다 (v2 §5-1 · 물리 f3)',
        tuple(tf.STATUSES) == ('OK', 'NOT_PERCOLATING', 'BAND_FALLBACK', 'MODEL_BELOW_CONTINUUM_BOUND', 'NOT_COMPUTED')
        and tuple(tf.REASONS) == ('solver_guard', 'missing_input', 'temperature_mismatch', 'percolation_disagree', 'invalid_input',
                                  'generation_invalid')
        and 'SOLVER_ANOMALY' not in tf.STATUSES
        and getattr(tf, 'reason_code', lambda r: None)('invalid_input: σ_ratio None') == 'invalid_input'
        and getattr(tf, 'reason_code', lambda r: None)('generation_invalid: 도장 ≠ full_metrics') == 'generation_invalid')

    # ── B. G1 띠 ──
    b1 = tf.ion_columns(dual(h={'boundary_rule': 'L1'}), LEDGER, 92.0)
    chk('B1 G1 띠 L1 → BAND_FALLBACK · f · tau2 · tau · f_gap 빈칸 (physics 는 L0 그대로 OK)',
        b1['ion_net_status_hertz'] == 'BAND_FALLBACK' and blank3(b1, 'hertz') and b1['f_ion_hertz_gap'] is None
        and b1['ion_net_band_rule_hertz'] == 'L1' and b1['ion_net_status_physics'] == 'OK')
    b2 = tf.ion_columns(dual(h={'boundary_rule': 'L2'}, p={'boundary_rule': 'L2'}), LEDGER, 92.0)
    chk('B2 G1 띠 L2 → BAND_FALLBACK (두 모드)', b2['ion_net_status_hertz'] == b2['ion_net_status_physics'] == 'BAND_FALLBACK')
    d3 = dual()
    for k in ('hertzian', 'physics'):
        d3[k].pop('boundary_rule')
    b3 = tf.ion_columns(d3, LEDGER, 92.0)
    chk('B3 띠 규칙 기록 없음 (안 A 전의 옛 산출물) → NOT_COMPUTED (missing_input) · 짐작하지 않는다',
        b3['ion_net_status_hertz'] == 'NOT_COMPUTED' and b3['ion_net_status_reason_hertz'] == 'missing_input'
        and blank3(b3, 'hertz') and b3['ion_net_band_rule_hertz'] == '')

    # ── C. G2 관통 일치 ──
    c1 = tf.ion_columns(dual(), LEDGER, 0.0)
    chk('C1 G2 솔버 관통 > 0 인데 calc_percolation 0 → NOT_COMPUTED (percolation_disagree) · 빈칸',
        c1['ion_net_status_hertz'] == 'NOT_COMPUTED' and c1['ion_net_status_reason_hertz'] == 'percolation_disagree' and blank3(c1, 'hertz'))
    #  ★ 10-05 RGL-02 · RGLR-01 — 비관통 픽스처는 생산자 어휘 (valid_zero + no_through_path) 로 쓴다.  옛 픽스처 (not_computed · 관통 분율 0) 는
    #    RGL-02 전 생산자 모양이라 이제 공용 기술 검사가 기술적 실패로 본다 (C3 · L7).
    c2 = tf.ion_columns(dual(h=npz()), LEDGER, 12.0)
    chk('C2 G2 반대 (솔버 0 · calc_percolation 12 %) → NOT_COMPUTED (percolation_disagree)',
        c2['ion_net_status_hertz'] == 'NOT_COMPUTED' and c2['ion_net_status_reason_hertz'] == 'percolation_disagree')
    #  ★ 10-05 RGLR-01 — 옛 C3 ("G2 는 상태 문자열을 무시한다 · TAU-22 → 상태 not_computed 인데 σ 있음 = OK") 는 RGL-02 생산자 수정 전 규약이다
    #    (그때는 상태가 비관통 · 실패를 못 갈랐다).  지금은 상태 ↔ 값이 생산자 계약이고, 모순 레코드 (not_computed 인데 σ 있음) 는 공용 기술
    #    검사가 G1–G5 **앞**에서 기술적 실패로 막는다 (생산자가 not_computed 를 신고 = solver_guard).  G2 판정 자체는 여전히 관통 분율로 한다 (C1 · C2).
    c3 = tf.ion_columns(dual(h={'sigma_full_status': 'not_computed'}), LEDGER, 92.0)
    chk('C3 상태 ↔ 값 모순 (not_computed 인데 σ 있음 · 관통) → NOT_COMPUTED (solver_guard) — 옛 TAU-22 의 "상태 무시" 는 RGL-02 · RGLR-01 로 대체',
        c3['ion_net_status_hertz'] == 'NOT_COMPUTED' and c3['ion_net_status_reason_hertz'] == 'solver_guard' and blank3(c3, 'hertz')
        and c3['ion_net_status_physics'] == 'OK')

    # ── D. G3 비관통 ──
    d1 = tf.ion_columns(dual(h=npz(), p=npz()), LEDGER, 0.0)
    chk('D1 G3 비관통 (두 판정 모두 0) → NOT_PERCOLATING · f = 0 · f_gap = 0 · tau2 · tau 빈칸 (= ∞)',
        d1['ion_net_status_hertz'] == 'NOT_PERCOLATING' and d1['f_ion_hertz'] == 0.0 and d1['f_ion_hertz_gap'] == 0.0
        and d1['tau2_ion_hertz'] is None and d1['tau_ion_hertz'] is None and d1['ion_net_status_physics'] == 'NOT_PERCOLATING')

    # ── E. G4 온도 짝 ──
    e_a = tf.ion_columns(dual(h={'sigma_grain_S_cm': 0.003}, p={'sigma_grain_S_cm': 0.003}), LEDGER, 92.0)
    e_b = tf.ion_columns(dual(h={'sigma_grain_S_cm': 0.0016}, p={'sigma_grain_S_cm': 0.0016}), LEDGER, 92.0)
    chk('E1 G4 σ_grain 두 값 (3.0 · 1.6 mS/cm) → tau2 · f 비트 동일 · σ₀ 메타만 다르다 (무차원 sigma_full · TAU-25)',
        e_a['tau2_ion_hertz'] == e_b['tau2_ion_hertz'] and e_a['f_ion_physics'] == e_b['f_ion_physics']
        and e_a['ion_sigma0_mScm'] == 3.0 and e_b['ion_sigma0_mScm'] == 1.6)
    hot = {'T_C': 60.0, 'T_ref_C': 25.0, 'sigma_ion_T_factor': 4.79, 'T_dependence': 'ARRHENIUS'}
    e2 = tf.ion_columns(dual(h={'temperature_provenance': hot, 'sigma_grain_S_cm': 0.01437},
                             p={'temperature_provenance': hot, 'sigma_grain_S_cm': 0.01437}), LEDGER, 92.0, sigma0_T_claim=25.0)
    chk('E2 G4 호출자가 25 °C 의 σ₀ 를 쓰려는데 망은 60 °C → NOT_COMPUTED (temperature_mismatch) · 빈칸',
        e2['ion_net_status_hertz'] == 'NOT_COMPUTED' and e2['ion_net_status_reason_hertz'] == 'temperature_mismatch' and blank3(e2, 'physics'))
    e3 = tf.ion_columns(dual(h={'temperature_provenance': hot, 'sigma_grain_S_cm': 0.01437},
                             p={'temperature_provenance': hot, 'sigma_grain_S_cm': 0.01437}), LEDGER, 92.0)
    chk('E3 주장 없음 → σ₀ 메타 = 망 자신의 값 (14.37 mS/cm @ 60 °C) · 짝이 정의상 맞으므로 OK',
        e3['ion_net_status_hertz'] == 'OK' and abs(e3['ion_sigma0_mScm'] - 14.37) < 1e-9 and e3['ion_sigma0_T_C'] == 60.0)
    e4 = tf.ion_columns(dual(p={'temperature_provenance': hot, 'sigma_grain_S_cm': 0.01437}), LEDGER, 92.0)
    chk('E4 두 모드의 σ₀ · T 가 다르면 두 모드 다 NOT_COMPUTED (temperature_mismatch) · σ₀ 메타 빈칸',
        e4['ion_net_status_hertz'] == e4['ion_net_status_physics'] == 'NOT_COMPUTED'
        and e4['ion_net_status_reason_physics'] == 'temperature_mismatch' and e4['ion_sigma0_mScm'] is None)

    # ── F. G5 연속체 하한 ──
    f1 = tf.ion_columns(dual(p={'sigma_full': 0.3}), LEDGER, 92.0)
    chk('F1 G5 f > φ (T < 1) → MODEL_BELOW_CONTINUUM_BOUND · 값 유지 (빈칸으로 거르지 않는다)',
        f1['ion_net_status_physics'] == 'MODEL_BELOW_CONTINUUM_BOUND' and f1['tau2_ion_physics'] is not None
        and f1['tau2_ion_physics'] < 1 and f1['f_ion_physics'] is not None)
    f2 = tf.ion_columns(dual(h={'sigma_full': PHI_SPHERE}), LEDGER, 92.0)
    chk('F2 경계 T = 1 은 OK (엄격한 T < 1 만 표지)',
        abs(f2['tau2_ion_hertz'] - 1.0) < 1e-12 and f2['ion_net_status_hertz'] == ('OK' if f2['tau2_ion_hertz'] >= 1 else 'MODEL_BELOW_CONTINUUM_BOUND'))

    # ── G. 솔버 관문 ──
    g1 = tf.ion_columns(dual(h={'sigma_full': None, 'sigma_full_status': 'not_computed'}), LEDGER, 92.0)
    chk('G1 관통인데 σ 없음 (솔버 관문 · 경계 겹침 퇴화) → NOT_COMPUTED (solver_guard)',
        g1['ion_net_status_hertz'] == 'NOT_COMPUTED' and g1['ion_net_status_reason_hertz'] == 'solver_guard' and blank3(g1, 'hertz'))
    #  ★ 10-05 RGLR-01 — 상태 computed 인데 σ_ratio 가 0 · 음수 · NaN · inf = 생산자 계약 위반 (생산자는 그런 값을 computed 로 내지 않는다) →
    #    공용 기술 검사 invalid_input (옛: L0 에서만 solver_guard 로 걸렸고 L1/L2 는 BAND_FALLBACK 로 가려졌다 — 띠와 무관하게 같은 판정).
    g2 = [_rc(tf.ion_columns(dual(h={'sigma_full': v}), LEDGER, 92.0)['ion_net_status_reason_hertz']) for v in (0.0, -0.1, float('nan'), float('inf'))]
    chk('G2 computed 인데 σ_ratio 가 0 · 음수 · NaN · inf → NOT_COMPUTED (invalid_input — RGLR-01 · 옛 solver_guard)', g2 == ['invalid_input'] * 4)

    # ── H. 입력 누락 ──
    h1 = tf.ion_columns(dual(), {'thickness_um': L_GAP, 'thickness_mass_conserving_um': None, 'phi_se_mass_conserving': PHI_MC}, 92.0)
    chk('H1 질량 보존 두께 없음 → 두 모드 NOT_COMPUTED (missing_input) (판 간격 f 를 φ_mc 와 섞지 않는다)',
        h1['ion_net_status_hertz'] == h1['ion_net_status_physics'] == 'NOT_COMPUTED'
        and h1['ion_net_status_reason_hertz'] == 'missing_input' and blank3(h1, 'hertz'))
    h2 = tf.ion_columns(dual(drop=('physics',)), LEDGER, 92.0)
    chk('H2 physics 결과 없음 → physics NOT_COMPUTED (missing_input) · hertz OK',
        h2['ion_net_status_physics'] == 'NOT_COMPUTED' and h2['ion_net_status_reason_physics'] == 'missing_input'
        and h2['ion_net_status_hertz'] == 'OK')
    h3 = tf.ion_columns(dual(), LEDGER, None)
    chk('H3 calc_percolation 값 없음 → NOT_COMPUTED (missing_input)', h3['ion_net_status_hertz'] == 'NOT_COMPUTED'
        and h3['ion_net_status_reason_hertz'] == 'missing_input')
    h4 = [tf.ion_columns(dual(), dict(LEDGER, **{k: v}), 92.0)['ion_net_status_reason_hertz']
          for k, v in (('thickness_um', 0.0), ('thickness_mass_conserving_um', float('nan')), ('phi_se_mass_conserving', -0.2), ('thickness_um', True))]
    chk('H4 장부 값이 0 · NaN · 음수 · bool → missing_input', h4 == ['missing_input'] * 4)

    h5 = tf.ion_columns(dual(p={'temperature_provenance': None}), LEDGER, 92.0)
    chk('H5 G4 — 그 모드의 온도 기록 (temperature_provenance) 이 없으면 짝을 볼 수 없다 → physics NOT_COMPUTED (missing_input) · hertz OK',
        h5['ion_net_status_physics'] == 'NOT_COMPUTED' and h5['ion_net_status_reason_physics'] == 'missing_input'
        and h5['ion_net_status_hertz'] == 'OK' and h5['ion_sigma0_mScm'] == 3.0)

    # ── I. 기준 대조 (메타 · 게이트 아님) ──
    chk('I1 망 φ (4 자리) = φ_mc·L_mc/L_gap → basis_check ok', o['ion_net_basis_check_hertz'] == 'ok')
    i2 = tf.ion_columns(dual(h={'phi_se': round(PHI_SPHERE, 4) + 0.01}), LEDGER, 92.0)
    chk('I2 망 φ 가 장부와 0.01 어긋남 → basis_check "mismatch:…" (상태는 그대로 — 새 게이트로 쓰려면 등록 · 1저자)',
        i2['ion_net_basis_check_hertz'].startswith('mismatch:') and i2['ion_net_status_hertz'] == 'OK')
    i3 = tf.ion_columns(dual(h={'phi_se': None}), LEDGER, 92.0)
    chk('I3 망 φ 없음 → basis_check "unchecked"', i3['ion_net_basis_check_hertz'] == 'unchecked')

    # ── J. 케이스 폴더 · CLI ──
    tmp = tempfile.mkdtemp(prefix='tauflux_')
    c_ok = os.path.join(tmp, 'case_ok'); os.makedirs(c_ok)
    json.dump(dual(), open(os.path.join(c_ok, 'network_conductivity_dual.json'), 'w'))
    json.dump(dict(LEDGER, percolation_pct=92.0), open(os.path.join(c_ok, 'full_metrics.json'), 'w'))
    c_no = os.path.join(tmp, 'case_nodual'); os.makedirs(c_no)
    json.dump(dict(LEDGER, percolation_pct=92.0), open(os.path.join(c_no, 'full_metrics.json'), 'w'))
    row_ok = tf.case_row(c_ok)
    row_no = tf.case_row(c_no)
    chk('J1 case_row: 폴더 (dual + full_metrics) → 같은 열 · 이름 = 폴더 이름',
        row_ok['case'] == 'case_ok' and row_ok['tau2_ion_hertz'] == o['tau2_ion_hertz'] and row_ok['ion_net_status_physics'] == 'OK')
    chk('J2 dual 파일 없음 → 두 모드 NOT_COMPUTED (missing_input) — 행은 남긴다 (조용히 빠지지 않는다)',
        row_no['ion_net_status_hertz'] == row_no['ion_net_status_physics'] == 'NOT_COMPUTED'
        and row_no['ion_net_status_reason_hertz'] == 'missing_input')
    out_tsv = os.path.join(tmp, 'out.tsv')
    r = subprocess.run([sys.executable, os.path.join(HERE, 'tau_flux.py'), c_ok, c_no, '--tsv', out_tsv],
                       capture_output=True, text=True, timeout=120)
    lines = open(out_tsv, encoding='utf-8').read().splitlines() if os.path.exists(out_tsv) else []
    hdr = lines[0].split('\t') if lines else []
    chk('J3 CLI → TSV (머리 = case + 열 · 두 행 · 수는 repr 로 되읽어 같은 값) · rc 0',
        r.returncode == 0 and len(lines) == 3 and hdr[0] == 'case' and set(hdr[1:]) == want
        and float(lines[1].split('\t')[hdr.index('tau2_ion_hertz')]) == o['tau2_ion_hertz'])

    # ── K. 생산자 ↔ 소비자 계약 — 실제 망 솔버 결과 (안 A 키 포함) 를 그대로 먹인다 (키 이름이 갈라지면 여기서 빨개진다) ──
    import contextlib
    import io
    import network_conductivity as nc
    A = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
    C = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1, 'delta': 0.05} for i in range(1, 21)]
    with contextlib.redirect_stdout(io.StringIO()):
        dk = {cm: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
              for cm in ('hertzian', 'physics')}
    v_se = 21 * 4.0 / 3.0 * math.pi                 # SE 만 → se_of_solid_vol = 1
    eps_s = 1.0 - v_se / (10.0 * 10.0 * 20.0)       # 구 부피 합 기공 (판 간격 상자)
    eps_u = 0.97                                    # 정확 union 기공 (임의 — k 는 tau2 에서 약분된다)
    led = {'thickness_um': 20.0, 'thickness_mass_conserving_um': 20.0 * (1 - eps_s) / (1 - eps_u),
           'phi_se_mass_conserving': (1 - eps_u) * 1.0}
    k1 = tf.ion_columns(dk, led, 100.0)
    chk('K1 솔버 결과 그대로 → 두 모드 OK · 띠 L0 · 폭 0.2 · 협착 · ψ · σ₀ 3.0 @ 25 °C · basis ok · tau2 = φ_망/σ_ratio (4 자리 φ 반올림 안)',
        k1['ion_net_status_hertz'] == k1['ion_net_status_physics'] == 'OK'
        and k1['ion_net_band_rule_hertz'] == 'L0' and abs(k1['ion_net_band_frac_physics'] - 0.2) < 1e-12
        and k1['ion_net_constriction_hertz'] == 'maxwell_halfspace' and k1['ion_net_constriction_physics'] == 'mikic_psi_divide'
        and k1['ion_net_psi_physics'] == 'legacy_divide' and k1['ion_sigma0_mScm'] == 3.0 and k1['ion_sigma0_T_C'] == 25.0
        and k1['ion_net_basis_check_hertz'] == k1['ion_net_basis_check_physics'] == 'ok'
        and abs(k1['tau2_ion_hertz'] - dk['hertzian']['phi_se'] / dk['hertzian']['sigma_full']) <= 5e-5 / dk['hertzian']['sigma_full'] + 1e-12
        and k1['f_ion_hertz_gap'] == dk['hertzian']['sigma_full'])
    with contextlib.redirect_stdout(io.StringIO()):
        dk_old = {cm: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
                  for cm in ('hertzian', 'physics')}
    for r_ in dk_old.values():
        r_.pop('boundary_rule')
    chk('K2 같은 결과에서 띠 규칙만 지우면 (안 A 전 산출물) → NOT_COMPUTED (missing_input) — 옛 코퍼스를 짐작으로 채우지 않는다',
        tf.ion_columns(dk_old, led, 100.0)['ion_net_status_reason_hertz'] == 'missing_input')

    # ── K3. G3 의 생산자 경로 — 위 띠에만 닿는 합성 침대: 바닥 L0 띠에 외톨이 SE 셋 (띠 규칙 L0 유지) + 위쪽 사슬 z 10..20 (바닥과 끊김).
    #       솔버는 관통 0 · σ None · calc_percolation 도 0 % ⇒ 도우미는 NOT_PERCOLATING · f = 0.
    #  ★ 10-05 RGL-02 (Codex · 1저자 비준 "권고대로") — 생산자 계약이 바뀌었다: 옛 판은 비관통에도 상태 'not_computed' 를 내서
    #    (TAU-22 · 상태로는 비관통을 판별할 수 없었다) 새 network 정지 관문이 정상 비관통을 failed 로 막았다.  이제 생산자가 **같은
    #    그래프에서 bottom ↔ top 관통 성분이 없음을 확인한 경우에만** 'valid_zero' + 사유 `no_through_path` 를 낸다 (숫자 필드는 F-12 대로
    #    None · CF · constr 도 같은 상태).  도우미 G2/G3 은 여전히 상태가 아니라 percolating_fraction 으로 판정한다 (TAU-22 · C3).
    import dem_analysis_core as dac
    B = {i: {'type': 1, 'x': 3.0 * i, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in ((1, 0.0), (2, 1.0), (3, 2.0))}
    B.update({10 + k: {'type': 1, 'x': 0.0, 'y': 5.0, 'z': float(z), 'radius': 1.0} for k, z in enumerate(range(10, 21))})
    BC = [{'id1': 10 + k, 'id2': 11 + k, 'contact_area': 0.1, 'delta': 0.05} for k in range(10)]
    with contextlib.redirect_stdout(io.StringIO()):
        db = {cm: nc._run_all_networks(B, BC, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
              for cm in ('hertzian', 'physics')}
        cp = dac.calc_percolation(B, BC, [1], 20.0, box_x=10.0, box_y=10.0)
    k3 = tf.ion_columns(db, led, cp['percolation_pct'])
    chk('K3 위 띠에만 닿는 합성 → 솔버 관통 0 · 상태 valid_zero + 사유 no_through_path (RGL-02 — 옛 판 not_computed) · CF · constr 같은 상태 · '
        'σ None (F-12) · calc_percolation 0 % · 띠 L0 → NOT_PERCOLATING · f = 0 · tau2 빈칸 (두 모드)',
        all(db[m]['percolating_fraction'] == 0 and db[m]['sigma_full_status'] == 'valid_zero'
            and db[m].get('sigma_full_reason') == 'no_through_path'
            and db[m].get('sigma_bulk_net_status') == db[m].get('sigma_constr_net_status') == 'valid_zero'
            and db[m]['sigma_full'] is None and db[m]['sigma_full_mScm'] is None for m in ('hertzian', 'physics'))
        and db['hertzian']['boundary_rule'] == 'L0' and cp['percolation_pct'] == 0
        and k3['ion_net_status_hertz'] == k3['ion_net_status_physics'] == 'NOT_PERCOLATING'
        and k3['f_ion_hertz'] == 0.0 and k3['tau2_ion_physics'] is None)

    # ── K4. RGL-02 — 관통인데 풀지 못한 침대는 비관통이 아니다 (같은 관통 사슬 · 선형 풀이 예외 주입).  생산자는 'not_computed' + 사유
    #       `solve_failed` (관통 분율 > 0) 를 내고, 협착 전력 몫의 사유도 '비관통' 문자열이 아니다 · 도우미는 NOT_COMPUTED (solver_guard).
    _orig_spsolve = nc.spsolve

    def _boom(*_a, **_k):
        raise RuntimeError('주입: spsolve 실패 (수치 실패 시험)')
    nc.spsolve = _boom
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            dfail = {cm: nc._run_all_networks(A, C, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
                     for cm in ('hertzian', 'physics')}
    finally:
        nc.spsolve = _orig_spsolve
    k4 = tf.ion_columns(dfail, led, 100.0)
    chk('K4 관통인데 풀이 실패 (spsolve 예외) → 상태 not_computed + 사유 solve_failed · 관통 분율 > 0 · 전력 몫 사유 ≠ "비관통" · '
        'NOT_COMPUTED (solver_guard) (두 모드)',
        all(dfail[m]['sigma_full_status'] == 'not_computed' and dfail[m].get('sigma_full_reason') == 'solve_failed'
            and dfail[m]['percolating_fraction'] > 0
            and dfail[m].get(f'constriction_power_share_ion_{t}_status') != 'not_computed (no percolating FULL solution)'
            and str(dfail[m].get(f'constriction_power_share_ion_{t}_status', '')).startswith('not_computed')
            for m, t in (('hertzian', 'hertz'), ('physics', 'physics')))
        and k4['ion_net_status_hertz'] == k4['ion_net_status_physics'] == 'NOT_COMPUTED'
        and k4['ion_net_status_reason_hertz'] == 'solver_guard')
    chk('K5 관통 침대의 σ 는 상태 · 사유 필드를 더해도 그대로 (computed · 사유 None)',
        all(dk[m]['sigma_full_status'] == 'computed' and dk[m].get('sigma_full_reason') is None for m in ('hertzian', 'physics')))

    # ── K6 · K7 (10-05 WEB-03 Q1 · Codex 재검증 §5 Q1 · 1저자 비준) — 관통인데 풀지 못한 채널은 **생산자가** 채널 상태 failed 로 신고한다 ──
    #    옛 판: 이온은 valid_null (= 미퍼콜의 정답과 같은 이름 · 사유 문구만 "미퍼콜이 아니다") · 전자 · 열은 아무 표지 없이 valid_null → 게시 게이트
    #    (`pipeline_service.network_content_verdict`) 가 ok 로 읽어 일반 경로가 Stage E 까지 갔다.  비관통 · 상 부재는 그대로 유효 null.
    MODES2 = (('hertzian', 'hertz'), ('physics', 'physics'))
    chk('K6 ★ WEB-03 Q1 — 관통인데 풀지 못함 (spsolve 예외 · 전 채널) → 이온 · 열 채널 상태 failed + 사유 solve_failed (옛: valid_null) (두 모드)',
        all(dfail[m].get('ionic_status') == 'failed' and 'solve_failed' in str(dfail[m].get('ionic_status_reason', ''))
            and dfail[m].get('thermal_status') == 'failed' for m, _t in MODES2))

    def _break_only(channel):
        """`spsolve` 를 그 채널의 FULL 풀이에서만 실패시킨다 (호출 사슬의 run_decomposition `_mode` · solve_network `mode` 로 가린다)."""
        orig = nc.spsolve

        def _f(*a, **k):
            fr, smode, rmode = sys._getframe(1), None, None
            while fr is not None:
                if fr.f_code.co_name == 'solve_network' and smode is None:
                    smode = fr.f_locals.get('mode')
                if fr.f_code.co_name == 'run_decomposition':
                    rmode = fr.f_locals.get('_mode')
                    break
                fr = fr.f_back
            if rmode == channel and smode == 'full':
                raise RuntimeError(f'주입: {channel} FULL spsolve 실패 (채널 하나만)')
            return orig(*a, **k)
        return orig, _f

    #  SE 사슬 (type 2 · x 0) + AM 사슬 (type 1 · x 5) — 둘 다 관통 · 전자망 = AM 사슬 (요청된 채널 셋 다 있다)
    AM_A = {i: {'type': 2, 'x': 0.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in enumerate(range(21), 1)}
    AM_A.update({100 + k: {'type': 1, 'x': 5.0, 'y': 0.0, 'z': float(z), 'radius': 1.0} for k, z in enumerate(range(21))})
    AM_C = C + [{'id1': 100 + k, 'id2': 101 + k, 'contact_area': 0.1, 'delta': 0.05} for k in range(20)]
    AM_TM = {1: 'AM_P', 2: 'SE'}

    def _run_tm(A_, C_, tm, plate_=20.0, channel=None, temp_c=None):
        orig = None
        if channel:
            orig, nc.spsolve = _break_only(channel)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                r_ = {cm: nc._run_all_networks(A_, C_, [k for k, v in tm.items() if v == 'SE'], [k for k, v in tm.items() if 'AM' in v],
                                               tm, 1.0, plate_, 10.0, 10.0, None, contact_mode=cm, temp_c=temp_c)
                      for cm in ('hertzian', 'physics')}
        finally:
            if orig is not None:
                nc.spsolve = orig
        return json.loads(json.dumps(r_))                  # 디스크 모양 (JSON 왕복)
    k7 = {'전자만 실패 (SE · AM 관통)': (_run_tm(AM_A, AM_C, AM_TM, channel='electronic'), ('computed', 'failed', 'computed')),
          '열만 실패 (SE 관통)': (_run_tm(A, C, {1: 'SE'}, channel='thermal'), ('computed', 'not_applicable', 'failed')),
          '이온만 실패 (SE 관통)': (_run_tm(A, C, {1: 'SE'}, channel='ionic'), ('failed', 'not_applicable', 'computed')),
          '정상 (SE · AM 관통)': (_run_tm(AM_A, AM_C, AM_TM), ('computed', 'computed', 'computed')),
          'AM 비관통 (사슬 끊김) — 유효 null': (_run_tm(AM_A, [c_ for c_ in AM_C if c_['id1'] != 110], AM_TM),
                                         ('computed', 'valid_null', 'computed')),
          'SE 정상 비관통 — 유효 null': (db, ('valid_zero', 'not_applicable', 'valid_null'))}
    k7got = {lbl: tuple((r_[m].get('ionic_status'), r_[m].get('electronic_status'), r_[m].get('thermal_status')) for m, _t in MODES2)
             for lbl, (r_, _w) in k7.items()}
    k7bad = {lbl: k7got[lbl] for lbl, (_r, w) in k7.items() if k7got[lbl] != (w, w)}
    chk(f'K7 ★ WEB-03 Q1 — 채널마다: 요청된 채널 (이온 · 전자 · 열) 의 관통 풀이 실패만 failed · 비관통 (valid_zero · valid_null) · 상 부재 '
        f'(not_applicable) 는 유효 null 그대로 (두 모드) {k7bad or ""}', not k7bad)

    # ── L. RGLR-01 · 02 (Codex 10-05 재검증 §2 · §3 · 1저자 비준) — 공용 기술 검사 `ion_record_problem` ──────────────────────────────
    #    network 정지 계약 (`webapp/pipeline_service.network_stop_verdict` ③) 과 τ 인계 소비자 (`ion_columns`) 가 **같은 함수**를 쓴다 · 과학적
    #    게이트 (G1 띠 폴백 · G3 비관통 · G5 연속체 하한) **앞**에서 돈다.  반례는 실 생산자 출력 위에 같은 필드를 두 모드 (또는 한 모드) 함께
    #    바꾼다 — 파일 간 불일치가 아니라 같은 잘못된 레코드가 소비자에게 가는 경우 (Codex 와 같은 모양).
    import copy
    import random
    import se_material as sem
    prob_fn = getattr(tf, 'ion_record_problem', None)
    tol_fn = getattr(tf, 'sigma_identity_tol', None)

    def _prob(rec):
        return prob_fn(rec) if prob_fn else ('NO_HELPER', '도우미 없음 (옛 코드)')

    def _mut(d_, fn, modes=('hertzian', 'physics')):
        d2 = copy.deepcopy(d_)
        for m_ in modes:
            fn(d2[m_])
        return d2

    def _led(A_, plate_):
        phi_ = sum(4.0 / 3.0 * math.pi * a['radius'] ** 3 for a in A_.values()) / (10.0 * 10.0 * plate_)
        return {'thickness_um': plate_, 'thickness_mass_conserving_um': plate_, 'phi_se_mass_conserving': phi_}

    #  띠 폴백 L1 (test_pipeline_provenance band_l1 과 같은 침대) · L2 (관측 z 범위 0..10 · 판 40) · 약한 접촉 (작은 σ) · 60 °C (온도 변환 σ₀)
    AB1 = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 0.5 * k, 'radius': 0.4} for i, k in enumerate(range(81), 1)}
    CB1 = [{'id1': i, 'id2': i + 1, 'contact_area': 0.1 * 0.16, 'delta': 0.05 * 0.4} for i in range(1, 81)]
    AB2 = {i: {'type': 1, 'x': 0.0, 'y': 0.0, 'z': 0.5 * k, 'radius': 0.4} for i, k in enumerate(range(21), 1)}
    CB2 = CB1[:20]
    CW = [{'id1': i, 'id2': i + 1, 'contact_area': 1e-5, 'delta': 0.05} for i in range(1, 21)]
    dB1, dB2 = _run_tm(AB1, CB1, {1: 'SE'}, plate_=40.0), _run_tm(AB2, CB2, {1: 'SE'}, plate_=40.0)
    dW, dT = _run_tm(A, CW, {1: 'SE'}), _run_tm(A, C, {1: 'SE'}, temp_c=60.0)
    lB1, lB2 = _led(AB1, 40.0), _led(AB2, 40.0)
    ok_recs = {'관통 L0': dk, '정상 비관통': db, '띠 L1': dB1, '띠 L2': dB2, '작은 σ': dW, '온도 60 °C σ₀': dT}
    l1 = {lbl: tuple(_prob(d_[m_]) for m_ in ('hertzian', 'physics')) for lbl, d_ in ok_recs.items()}
    chk(f'L1 공용 기술 검사 `ion_record_problem` — 실 생산자 출력 (관통 · 비관통 · 띠 L1 · L2 · 작은 σ · 60 °C σ₀) 두 모드 전부 유효 (None) '
        f'{ {k: v for k, v in l1.items() if v != (None, None)} or ""}',
        prob_fn is not None and all(v == (None, None) for v in l1.values()))
    chk('L1b 픽스처 조건이 섰다 — 띠 규칙 L1 · L2 · 작은 σ (Hertz σ_dim < 1e-3 mS/cm) · 60 °C σ₀ (Arrhenius · σ_grain_S_cm ≠ 0.003)',
        all(dB1[m_]['boundary_rule'] == 'L1' and dB2[m_]['boundary_rule'] == 'L2' for m_ in ('hertzian', 'physics'))
        and 0 < dW['hertzian']['sigma_full_mScm'] < 1e-3
        and abs(dT['hertzian']['sigma_grain_S_cm'] - sem.sigma_grain_S_cm(60.0)) == 0 and dT['hertzian']['sigma_grain_S_cm'] != 0.003)

    codex = {'σ_ratio None': lambda r: r.update(sigma_full=None), 'σ_ratio NaN': lambda r: r.update(sigma_full=float('nan')),
             'σ_ratio −1': lambda r: r.update(sigma_full=-1), '관통 분율 2': lambda r: r.update(percolating_fraction=2)}
    l2 = {}
    for lbl, fn in codex.items():
        ob = tf.ion_columns(_mut(dB1, fn), lB1, 100.0)
        op = tf.ion_columns(_mut(dB1, fn, ('physics',)), lB1, 100.0)
        l2[lbl] = (ob['ion_net_status_hertz'], _rc(ob['ion_net_status_reason_hertz']), ob['ion_net_status_physics'],
                   _rc(ob['ion_net_status_reason_physics']), op['ion_net_status_hertz'], op['ion_net_status_physics'],
                   _rc(op['ion_net_status_reason_physics']))
    want2 = ('NOT_COMPUTED', 'invalid_input', 'NOT_COMPUTED', 'invalid_input', 'BAND_FALLBACK', 'NOT_COMPUTED', 'invalid_input')
    chk(f'L2 ★ RGLR-01 Codex 반례 (실 띠 L1 침대 · 같은 필드를 두 모드 함께) σ_ratio None · NaN · −1 · 관통 분율 2 → NOT_COMPUTED (invalid_input) · '
        f'physics 만 바꾸면 physics 만 (Hertz 는 BAND_FALLBACK 그대로) — 옛: 넷 다 BAND_FALLBACK {l2}',
        all(v == want2 for v in l2.values()) and len(l2) == 4)
    l2b = {lbl: (lambda o_: (o_['ion_net_status_hertz'], _rc(o_['ion_net_status_reason_hertz'])))(tf.ion_columns(_mut(dk, fn), led, 100.0))
           for lbl, fn in codex.items()}
    chk(f'L2b 같은 반례를 L0 침대에서도 → NOT_COMPUTED (invalid_input) — 띠와 무관한 한 판정 (옛: σ 반례 solver_guard · 관통 분율 2 = OK) {l2b}',
        all(v == ('NOT_COMPUTED', 'invalid_input') for v in l2b.values()))

    o1, o2 = tf.ion_columns(dB1, lB1, 100.0), tf.ion_columns(dB2, lB2, 100.0)
    o3 = tf.ion_columns(dk, dict(led, phi_se_mass_conserving=1e-4), 100.0)
    chk('L3 양성 대조 — 입력이 유효한 등록된 과학적 HOLD 는 그대로: 띠 L1 · L2 → BAND_FALLBACK · 연속체 하한 → MODEL_BELOW_CONTINUUM_BOUND (값 유지) · '
        '정상 비관통 → NOT_PERCOLATING (K3) — 기술 검사가 과잉차단하지 않는다',
        o1['ion_net_status_hertz'] == o1['ion_net_status_physics'] == 'BAND_FALLBACK' and o1['ion_net_band_rule_hertz'] == 'L1'
        and o2['ion_net_status_hertz'] == o2['ion_net_status_physics'] == 'BAND_FALLBACK' and o2['ion_net_band_rule_physics'] == 'L2'
        and o3['ion_net_status_hertz'] == o3['ion_net_status_physics'] == 'MODEL_BELOW_CONTINUUM_BOUND' and o3['tau2_ion_hertz'] is not None
        and k3['ion_net_status_hertz'] == 'NOT_PERCOLATING')

    t4 = {'σ_ratio ×4 · 두 모드 (Codex ratio_times4)': (lambda r: r.update(sigma_full=r['sigma_full'] * 4), ('hertzian', 'physics')),
          'σ_ratio ×4 · physics 만': (lambda r: r.update(sigma_full=r['sigma_full'] * 4), ('physics',)),
          'σ_dim ×4 · 두 모드': (lambda r: r.update(sigma_full_mScm=r['sigma_full_mScm'] * 4), ('hertzian', 'physics')),
          'σ_dim ×4 · Hertz 만': (lambda r: r.update(sigma_full_mScm=r['sigma_full_mScm'] * 4), ('hertzian',))}
    l4 = {}
    for lbl, (fn, modes) in t4.items():
        o_ = tf.ion_columns(_mut(dk, fn, modes), led, 100.0)
        l4[lbl] = all((o_[f'ion_net_status_{t}'] == 'NOT_COMPUTED' and _rc(o_[f'ion_net_status_reason_{t}']) == 'invalid_input'
                       and o_[f'tau2_ion_{t}'] is None) if m in modes else
                      (o_[f'ion_net_status_{t}'] == 'OK' and o_[f'tau2_ion_{t}'] == k1[f'tau2_ion_{t}']) for m, t in MODES2)
    chk(f'L4 ★ RGLR-02 두 σ 표현 항등식 (실 L0 침대) — σ_ratio 만 · σ_dim 만 ×4 (두 모드 · 한 모드) → 바뀐 모드만 NOT_COMPUTED (invalid_input) · '
        f'tau2 빈칸 (옛: σ_ratio ×4 → tau2 ÷4 로 OK) · 안 바꾼 모드는 OK 그대로 {l4}', all(l4.values()) and len(l4) == 4)
    ow, ot = tf.ion_columns(dW, led, 100.0), tf.ion_columns(dT, led, 100.0)
    chk('L4b 양성 대조 — 작은 σ (Hertz σ_dim ~1e-4 · 6 자리 반올림이 상대 0.4 %) · 60 °C σ₀ (Arrhenius) 는 생산자 그대로 OK (σ₀ 메타 = 그 온도의 값)',
        ow['ion_net_status_hertz'] == ow['ion_net_status_physics'] == 'OK'
        and ot['ion_net_status_hertz'] == ot['ion_net_status_physics'] == 'OK' and ot['ion_sigma0_T_C'] == 60.0
        and abs(ot['ion_sigma0_mScm'] - sem.sigma_grain_S_cm(60.0) * 1000) < 1e-9)
    if tol_fn is not None:
        rH = dk['hertzian']
        cen = 1000.0 * rH['sigma_grain_S_cm'] * rH['sigma_full']
        tol = tol_fn(rH['sigma_grain_S_cm'], rH['sigma_full'], rH['sigma_full_mScm'])
        in_, out_ = dict(rH, sigma_full_mScm=cen + 0.999 * tol), dict(rH, sigma_full_mScm=cen + 1.001 * tol)
        chk(f'L4c 경계 — 허용 = 5e-7 + 1000·σ₀·5e-9 + 부동소수 여유 (= {tol:.6g} mS/cm) · 0.999×허용 안 → 유효 · 1.001×허용 밖 → invalid_input',
            abs(tol - (5e-7 + 1000.0 * rH['sigma_grain_S_cm'] * 5e-9)) < 1e-12 and _prob(in_) is None and _rc(_prob(out_)[0]) == 'invalid_input')
    else:
        chk('L4c 경계 — sigma_identity_tol 도우미 없음 (옛 코드)', False)

    #  L5 성질 시험 — 생산자 반올림 그대로 (σ_ratio = round(·, 8) · σ_dim = round(σ_ratio_raw × σ₀ × 1000, 6) · numpy float64 · 파이썬 float 둘 다)
    #     로 만든 레코드는 σ₀ 가 25 °C 상수든 Arrhenius 변환이든 전부 통과해야 한다 (경계가 생산자 정밀도보다 빡빡하면 정상 출력을 막는다).
    import numpy as _np
    rng = random.Random(20261005)
    l5_bad, l5_n, l5_skip, l5_tamper_miss = [], 0, 0, 0
    for i_ in range(20000):
        q_true = 10 ** rng.uniform(-6.0, math.log10(1.5))
        t_c = rng.choice([None, rng.uniform(-30.0, 120.0)])
        ea = rng.choice([None, 0.29, 0.41, 0.46])
        s0 = sem.sigma_grain_S_cm(t_c, ea)
        q_raw = _np.float64(q_true) if i_ % 2 else q_true
        q_st, sd_st = float(round(q_raw, 8)), float(round(q_raw * s0 * 1000, 6))
        rec = {'sigma_full_status': 'computed', 'sigma_full': q_st, 'sigma_full_mScm': sd_st, 'percolating_fraction': 1.0,
               'sigma_grain_S_cm': s0}
        if q_st <= 0 or sd_st <= 0:                     # 반올림으로 0 이 된 σ — computed 인데 0 = 양수 규칙이 막는다 (항등식 시험 밖)
            l5_skip += 1
            if _prob(rec) is None:
                l5_bad.append(('zero-pass', q_true, s0))
            continue
        l5_n += 1
        p_ = _prob(rec)
        if p_ is not None:
            l5_bad.append((q_true, s0, q_st, sd_st, p_))
        if sd_st > 1e-4 and _prob(dict(rec, sigma_full=q_st * 4)) is None:   # Codex 모양 ×4 는 σ_dim 이 반올림 바닥보다 클 때 늘 잡힌다
            l5_tamper_miss += 1
    chk(f'L5 성질 시험 (2 만 표본 · σ_ratio 1e-6–1.5 · σ₀ 25 °C · −30–120 °C × Ea 띠) — 생산자 반올림 출력 {l5_n} 건 전부 통과 · '
        f'반올림 0 ({l5_skip} 건) 은 양수 규칙이 막음 · σ_ratio ×4 놓침 {l5_tamper_miss} {l5_bad[:2] or ""}',
        prob_fn is not None and not l5_bad and l5_n > 19000 and l5_tamper_miss == 0)

    vz = {'사유 solve_failed': {'sigma_full_reason': 'solve_failed'}, '사유 zero_value': {'sigma_full_reason': 'zero_value'},
          'σ_ratio 0.0': {'sigma_full': 0.0}, 'σ_dim 0.0': {'sigma_full_mScm': 0.0}, '관통 분율 0.3': {'percolating_fraction': 0.3},
          'CF 상태 not_computed': {'sigma_bulk_net_status': 'not_computed'}, 'constr 상태 없음': {'sigma_constr_net_status': None},
          '이온 채널 valid_null': {'ionic_status': 'valid_null'}}
    l6 = {}
    for lbl, kv in vz.items():
        rec = dict(db['hertzian'], **kv)
        o_ = tf.ion_columns({'hertzian': rec, 'physics': db['physics']}, led, 0.0)
        l6[lbl] = (_rc((_prob(rec) or ('',))[0]), o_['ion_net_status_hertz'], _rc(o_['ion_net_status_reason_hertz']))
    chk(f'L6 ★ 증명된 비관통 = RGL-02 조합만 (사유 no_through_path · σ 숫자 None · 관통 분율 0 · CF · constr · 이온 채널 valid_zero) — 한 키씩 어긋나면 '
        f'invalid_input · τ 인계 NOT_COMPUTED (NOT_PERCOLATING 아님) { {k: v for k, v in l6.items() if v != ("invalid_input", "NOT_COMPUTED", "invalid_input")} or ""}',
        all(v == ('invalid_input', 'NOT_COMPUTED', 'invalid_input') for v in l6.values()) and len(l6) == len(vz))
    st7 = {repr(s_): _rc((_prob(dict(dk['hertzian'], sigma_full_status=s_)) or ('',))[0]) for s_ in (None, 'garbage', 'valid_null', 'COMPUTED')}
    st7['키 없음'] = _rc((_prob({k: v for k, v in dk['hertzian'].items() if k != 'sigma_full_status'}) or ('',))[0])
    st7['not_computed'] = _rc((_prob(dfail['hertzian']) or ('',))[0])
    chk(f'L7 상태 어휘 — 생산자 계약 밖 (None · 키 없음 · 모르는 문자열 · 채널 어휘 valid_null) → invalid_input · 생산자 신고 not_computed → solver_guard {st7}',
        all(v == 'invalid_input' for k, v in st7.items() if k != 'not_computed') and st7['not_computed'] == 'solver_guard')
    chk('L8 어휘 짝 — 공용 기술 검사의 비관통 사유 = 생산자 (network_conductivity.NO_THROUGH_REASON) · 사유 코드 invalid_input 은 REASONS 안',
        getattr(tf, 'NO_THROUGH_REASON', None) == nc.NO_THROUGH_REASON and 'invalid_input' in tf.REASONS)

    # ── M. 세대 일관성 (10-05 RGLR2-02 · Codex 3차 재검증 §2 · Q2) — 케이스 폴더의 망 활성 세대가 **확정되지 않았으면** τ 인계를 싣지 않는다 ──
    #    (읽는 쪽 fail-closed · 최근 시도 기록을 못 썼어도 디스크만 보고 가른다).  확정 안 됨 = full_metrics 가 주장하는 망 세대 ≠ 도장 (도장 없음 포함) ·
    #    full_metrics 의 두 id 가 서로 다름 · 도장 손상 · 최근 시도가 활성을 무효로 남김 (되돌림 실패) · 중단된 게시 흔적 (.publish_backup_* ·
    #    .stage_stash_net_*).  full_metrics 가 망 세대를 주장하지 않으면 (접촉 분석만 · 도장 이전 옛 세대) 대조할 것이 없다 — 막지 않는다.
    gen_fn = getattr(tf, 'network_generation_problem', None)
    tmpm = tempfile.mkdtemp(prefix='tauflux_gen_')

    def _mk(name, fm_over=None, prov=None, attempt=None, extra=()):
        c_ = os.path.join(tmpm, name)
        os.makedirs(c_)
        json.dump(dual(), open(os.path.join(c_, 'network_conductivity_dual.json'), 'w'))
        json.dump(dict(LEDGER, percolation_pct=92.0, **(fm_over or {})), open(os.path.join(c_, 'full_metrics.json'), 'w'))
        if prov is not None:
            with open(os.path.join(c_, 'network_provenance.json'), 'w') as f_:
                f_.write(prov if isinstance(prov, str) else json.dumps(prov))
        if attempt is not None:
            json.dump(attempt, open(os.path.join(c_, 'network_attempt.json'), 'w'))
        for n_ in extra:
            if n_.endswith('/'):
                os.makedirs(os.path.join(c_, n_.rstrip('/')))
            else:
                open(os.path.join(c_, n_), 'w').write('{}')
        return c_
    P1 = {'network_run_id': 'R1', 'solver_status': 'success'}
    FM1 = {'network_run_id': 'R1', 'active_network_run_id': 'R1'}
    A_OK = {'latest_attempt_status': 'success', 'solver_status': 'success', 'network_attempt_run_id': 'R1', 'active_status': 'success'}
    good = {'세대 일치 (full_metrics R1 = 도장 R1 · 최근 시도 success)': _mk('g_ok', FM1, P1, A_OK),
            '접촉 분석만 다시 쓴 full_metrics (망 id 없음) + 도장 R1': _mk('g_contact', None, P1),
            '도장 이전 옛 세대 (도장 · id 없음)': _mk('g_legacy'),
            '최근 재계산 실패 · 되돌림 성공 (publish_exception · 활성 유지)': _mk('g_pubexc', FM1, P1, dict(
                A_OK, latest_attempt_status='failed', solver_status='failed', network_attempt_run_id='R2',
                failure_kind='publish_exception', previous_generation_kept=True)),
            '다른 단계의 stash (접촉 분석 · 망 아님)': _mk('g_cstash', FM1, P1, A_OK, extra=('.stage_stash_ContactAnalysis_x/',))}
    bad = {'full_metrics R2 ≠ 도장 R1 (Codex rollback_destination_failure 의 디스크)': _mk(
               'b_mismatch', {'network_run_id': 'R2', 'active_network_run_id': 'R2'}, P1, A_OK),
           'full_metrics 의 두 id 가 다르다 (R1 · R2)': _mk('b_twoids', {'network_run_id': 'R1', 'active_network_run_id': 'R2'}, P1),
           'full_metrics 가 R1 을 주장하는데 도장 없음 (첫 실행 되돌림 실패)': _mk('b_noprov', FM1),
           '도장 손상 (읽을 수 없음)': _mk('b_provbad', None, '{망가진 JSON'),
           '최근 시도 = 되돌림 실패 (rollback_failed · 활성 무효)': _mk('b_rbfail', FM1, P1, dict(
               A_OK, latest_attempt_status='failed', failure_kind='rollback_failed', active_status='invalid',
               previous_generation_kept=False, active_problem='full_metrics 되돌림 실패')),
           '중단된 게시의 사본 (.publish_backup_*)': _mk('b_backup', FM1, P1, A_OK, extra=('.publish_backup_R2_full_metrics.json',)),
           '중단된 망 풀이의 stash (.stage_stash_net_*)': _mk('b_stash', FM1, P1, A_OK, extra=('.stage_stash_net__x/',))}
    rg = {k: tf.case_row(v) for k, v in good.items()}
    rb = {k: tf.case_row(v) for k, v in bad.items()}
    gbad = {k: (r['ion_net_status_hertz'], r['ion_net_status_physics'], (gen_fn(good[k]) if gen_fn else '?'))
            for k, r in rg.items() if not (r['ion_net_status_hertz'] == r['ion_net_status_physics'] == 'OK'
                                           and r['tau2_ion_hertz'] == o['tau2_ion_hertz'] and gen_fn and gen_fn(good[k]) == '')}
    chk(f'M1 양성 대조 — 세대 일치 · 접촉 분석만 · 도장 이전 · 되돌림 성공한 재계산 실패 · 다른 단계 stash → τ 인계 그대로 (OK · 같은 tau2) · '
        f'세대 문제 없음 {gbad or ""}', not gbad and len(rg) == 5)
    bbad = {k: (r['ion_net_status_hertz'], r['ion_net_status_reason_hertz'][:40])
            for k, r in rb.items() if not (r['ion_net_status_hertz'] == r['ion_net_status_physics'] == 'NOT_COMPUTED'
                                           and tf.reason_code(r['ion_net_status_reason_hertz']) == 'generation_invalid'
                                           and tf.reason_code(r['ion_net_status_reason_physics']) == 'generation_invalid'
                                           and all(r[f'{c}_ion_{m}'] is None for c in ('f', 'tau2', 'tau') for m in ('hertz', 'physics'))
                                           and gen_fn and gen_fn(bad[k]))}
    chk(f'M2 ★ RGLR2-02 세대가 확정되지 않은 폴더 {len(bad)} 종 → 두 모드 NOT_COMPUTED (generation_invalid: 세부) · f · tau2 · tau 빈칸 '
        f'(옛: OK — dual 만 읽어 옛 세대 τ 를 실었다) {bbad or ""}', not bbad and len(rb) == 7)
    _gb = gen_fn(bad['full_metrics R2 ≠ 도장 R1 (Codex rollback_destination_failure 의 디스크)']) if gen_fn else ''
    chk(f'M3 세대 문제 사유 = 무엇이 어긋났는지 (두 id) — {_gb[:90]!r}', 'R2' in _gb and 'R1' in _gb)
    M_ = {'phi_se': 0.30, 'sigma_full_mScm': 0.12, 'sigma_bulk_net_mScm': 0.5}
    chk('M4 ★ 등급 τ getter (tau2_from_metrics) — 읽는 쪽이 세대 무효 표지를 단 metrics → tau2 None (hertz · bulk) · 표지 없으면 값 그대로',
        tf.tau2_from_metrics(dict(M_, network_generation_problem='full_metrics ↔ 도장 불일치'))[0] is None
        and tf.tau2_from_metrics(dict(M_, network_generation_problem='x'), 'bulk')[0] is None
        and tf.tau2_from_metrics(M_)[0] is not None and tf.tau2_from_metrics(M_, 'bulk')[0] is not None
        and getattr(tf, 'GENERATION_PROBLEM_KEY', None) == 'network_generation_problem')
    import shutil
    shutil.rmtree(tmpm, ignore_errors=True)

    print(f'\ntest_tau_flux: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
