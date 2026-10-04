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
    return base


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
    chk('A6 상태 값은 다섯 중 하나 · 사유는 넷 중 하나 — SOLVER_ANOMALY 를 쓰지 않는다 (v2 §5-1 · 물리 f3)',
        tuple(tf.STATUSES) == ('OK', 'NOT_PERCOLATING', 'BAND_FALLBACK', 'MODEL_BELOW_CONTINUUM_BOUND', 'NOT_COMPUTED')
        and tuple(tf.REASONS) == ('solver_guard', 'missing_input', 'temperature_mismatch', 'percolation_disagree')
        and 'SOLVER_ANOMALY' not in tf.STATUSES)

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
    c2 = tf.ion_columns(dual(h={'percolating_fraction': 0.0, 'sigma_full': None, 'sigma_full_status': 'not_computed'}), LEDGER, 12.0)
    chk('C2 G2 반대 (솔버 0 · calc_percolation 12 %) → NOT_COMPUTED (percolation_disagree)',
        c2['ion_net_status_hertz'] == 'NOT_COMPUTED' and c2['ion_net_status_reason_hertz'] == 'percolation_disagree')
    chk('C3 G2 는 `sigma_full_status` 로 판정하지 않는다 — 관통 · 비관통 모두 상태 문자열과 무관 (TAU-22)',
        tf.ion_columns(dual(h={'sigma_full_status': 'not_computed'}), LEDGER, 92.0)['ion_net_status_hertz'] == 'OK')

    # ── D. G3 비관통 ──
    np_kw = {'percolating_fraction': 0.0, 'sigma_full': None, 'sigma_full_status': 'not_computed'}
    d1 = tf.ion_columns(dual(h=np_kw, p=np_kw), LEDGER, 0.0)
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
    g2 = [tf.ion_columns(dual(h={'sigma_full': v}), LEDGER, 92.0)['ion_net_status_reason_hertz'] for v in (0.0, -0.1, float('nan'), float('inf'))]
    chk('G2 σ 가 0 · 음수 · NaN · inf → NOT_COMPUTED (solver_guard)', g2 == ['solver_guard'] * 4)

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

    # ── K3. G3 의 생산자 경로 (TAU-22 처방 그대로) — 위 띠에만 닿는 합성 침대: 바닥 L0 띠에 외톨이 SE 셋 (띠 규칙 L0 유지) +
    #       위쪽 사슬 z 10..20 (바닥과 끊김).  솔버는 관통 0 · σ None · 상태 'not_computed' (= valid_zero 가 아니다 — 상태로는 비관통을
    #       판별할 수 없다) · calc_percolation 도 0 % ⇒ 도우미는 NOT_PERCOLATING · f = 0.
    import dem_analysis_core as dac
    B = {i: {'type': 1, 'x': 3.0 * i, 'y': 0.0, 'z': float(z), 'radius': 1.0} for i, z in ((1, 0.0), (2, 1.0), (3, 2.0))}
    B.update({10 + k: {'type': 1, 'x': 0.0, 'y': 5.0, 'z': float(z), 'radius': 1.0} for k, z in enumerate(range(10, 21))})
    BC = [{'id1': 10 + k, 'id2': 11 + k, 'contact_area': 0.1, 'delta': 0.05} for k in range(10)]
    with contextlib.redirect_stdout(io.StringIO()):
        db = {cm: nc._run_all_networks(B, BC, [1], [], {1: 'SE'}, 1.0, 20.0, 10.0, 10.0, None, contact_mode=cm)
              for cm in ('hertzian', 'physics')}
        cp = dac.calc_percolation(B, BC, [1], 20.0, box_x=10.0, box_y=10.0)
    k3 = tf.ion_columns(db, led, cp['percolation_pct'])
    chk('K3 위 띠에만 닿는 합성 → 솔버 관통 0 · 상태 not_computed (valid_zero 아님 · TAU-22) · calc_percolation 0 % · 띠 L0 → '
        'NOT_PERCOLATING · f = 0 · tau2 빈칸 (두 모드)',
        db['hertzian']['percolating_fraction'] == 0 and db['hertzian']['sigma_full_status'] == 'not_computed'
        and db['hertzian']['boundary_rule'] == 'L0' and cp['percolation_pct'] == 0
        and k3['ion_net_status_hertz'] == k3['ion_net_status_physics'] == 'NOT_PERCOLATING'
        and k3['f_ion_hertz'] == 0.0 and k3['tau2_ion_physics'] is None)

    print(f'\ntest_tau_flux: {_ok}/{_ok + len(_fail)} PASS' + (f'   FAILED: {_fail}' if _fail else ''))
    return 0 if not _fail else 1


if __name__ == '__main__':
    sys.exit(main())
