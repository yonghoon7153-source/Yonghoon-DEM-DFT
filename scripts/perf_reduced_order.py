#!/usr/bin/env python3
"""perf_reduced_order — 구조(STEP3 σ 삼중항 + 기하) → **성능**(η 분해·율특성) 0-D 축소차수.

왜 이게 필요한가
────────────────
사용자 목표는 "P:S 별 성능변화 및 열화" 인데, 성능(용량·율특성)은 STEP4 시간전개에서만 나오고
그건 **0.2C 한 판에 6일**이다.  게다가 실측: 코퍼스 190 케이스 중 STEP4 산출물은 **0건**
(full_metrics 187 · mpm_metrics 187 은 있음).  ⇒ 성능을 **회귀할 데이터가 없다**.

그래서 이 모듈은 성능을 **적합하지 않는다**.  STEP4 와 **같은 물리**를 0-D 로 줄여서
구조에서 직접 계산한다.  적합 파라미터 **0개** — 모든 입력이 측정(STEP3/MPM)이거나 앵커다.

    설계 → [ML, 187 샘플] → 구조(σ_ion·σ_e·L·coverage·CN) → [이 모듈, 적합 없음] → 성능

ML 은 **구조**만 배우면 된다(샘플 187개로 충분).  구조→성능은 물리라 학습이 필요 없다.

★ 다공전극 옴강하 — L/3 인 이유 (적합 아님, 유도)
──────────────────────────────────────────────
전해질(이온) 전류는 세퍼레이터에서 I, 집전체에서 0 이다.  반응이 두께에 균일하면
`i_ion(z) = I·(1 − z/L)` 이므로

    Δφ(z) = (I/κ)·∫₀^z (1 − s/L) ds = (I/κ)·(z − z²/2L)

셀 전압 벌점은 z=L 에서의 **끝점 강하**가 아니라 **반응-가중 평균**이다 (반응이 일어나는
모든 z 가 그 지점의 φ 를 느낀다).  균일 반응 가중:

    η_ohm = (1/L)∫₀^L Δφ(z) dz = (I/κ)·(L/2 − L/6) = **I·L/(3κ)**

⇒ `ASR_eff = L/(3·σ)` — 끝점 강하(L/2κ)도, 판상 근사(L/κ)도 아니다.
   (Newman 다공전극 이론의 표준 결과.  고율에서 반응이 세퍼레이터 쪽으로 몰리면 실효 경로가
    더 짧아져 이보다 **작아진다** → L/3 은 보수적 상한 쪽.)

★ 검증 (2026-08-03) — 리포의 실측 2C STEP4 런과 대조
────────────────────────────────────────────────
`docs/sdcp_318_base_sbe_dbe_comparison.md:95` 중간충전 2C η [mV]:
    SBE  옴 93.3 / kin 36.2 / 확산 5.9      delivered CC 81.5% → CCCV 88.9%
    DBE  옴 87.3 / kin 31.7 / 확산 5.8      delivered CC 83.0% → CCCV 89.6%
`--validate` 가 이 앵커로 잔차를 인쇄한다.  ⚠ 이 앵커는 **σ_ion 이 런 로그에 기록된 값이
아니라** 우리가 아는 침대 파라미터로 재구성한 것이라, 잔차에는 입력 불일치가 섞여 있다 —
"모델 오차" 로 단정하지 말 것 (§F1).

Selftest:  python3 scripts/perf_reduced_order.py --selftest
사용:      python3 scripts/perf_reduced_order.py --sigma-ion 2.03e-4 --sigma-e 1.98e-3 \
               --thickness-um 72.48 --loading 3.18 --c-rate 2
"""

import argparse
import math

F_CONST = 96485.33212      # C/mol
R_GAS = 8.31446261815324   # J/(mol·K)
T_REF_K = 298.15

# ── 검증 앵커 (docs/sdcp_318_base_sbe_dbe_comparison.md:92-95, 2C 중간충전) ─────────────
SDCP_2C_ANCHOR = {
    'SBE': {'eta_ohm_mV': 93.3, 'eta_kin_mV': 36.2, 'eta_diff_mV': 5.9,
            'delivered_cc_pct': 81.5, 'delivered_cccv_pct': 88.9, 'sigma_e_mScm': 1.979},
    'DBE': {'eta_ohm_mV': 87.3, 'eta_kin_mV': 31.7, 'eta_diff_mV': 5.8,
            'delivered_cc_pct': 83.0, 'delivered_cccv_pct': 89.6, 'sigma_e_mScm': 3.002},
}
SDCP_BED = {'thickness_um': 72.48, 'loading_mAh_cm2': 3.18, 'sigma_ion_mScm': 0.203,
            'r_p_um': 3.0, 'i0_A_m2': 2.0, 'd_s_m2_s': 3e-14, 'coverage': 0.5,
            'src': 'docs/sdcp_318_base_sbe_dbe_comparison.md + webapp /eis 기본값 '
                   '(⚠ 런 로그에서 읽은 것이 아니라 재구성 — 입력 불일치가 잔차에 섞임)'}

TLM_FACTOR = 3.0           # ASR_eff = L/(TLM_FACTOR·σ) — 위 유도, 적합 아님


def asr_ohm_cm2(thickness_um, sigma_mScm, tlm=TLM_FACTOR):
    """다공전극 실효 옴 ASR [Ω·cm²] = L/(3σ).  σ [mS/cm] · L [µm]."""
    if not (sigma_mScm > 0):
        return float('inf')
    return (thickness_um * 1e-4) / (sigma_mScm * 1e-3) / float(tlm)


def current_density_A_cm2(loading_mAh_cm2, c_rate):
    """운전 전류밀도 [A/cm²] = loading[mAh/cm²]·C-rate / 1h."""
    return loading_mAh_cm2 * c_rate * 1e-3


def specific_area_cm2_cm3(r_p_um, phi_am, coverage=1.0):
    """반응 비표면적 [cm²/cm³] = 3φ_AM/r_p × coverage (구형 AM).

    coverage = SE 와 실제로 접한 몫 (STEP3 Tabor/Hertz) — 나머지 표면은 반응 못 한다.
    """
    if not (r_p_um > 0):
        return 0.0
    return 3.0 * phi_am / (r_p_um * 1e-4) * max(0.0, min(1.0, coverage))


def eta_kin_V(j_A_cm2, i0_A_m2, a_spec_cm2_cm3, thickness_um, temp_k=T_REF_K,
              alpha_sum=1.0):
    """BV 반응 과전압 [V].  i0 [A/m²] → 면적당; a_spec·L 로 체적→면적 환산.

    η = (2RT/(αF))·asinh( j / (2·i0_areal) ) — 대칭 BV 의 정확형 (선형화 아님).
    """
    i0_areal = i0_A_m2 * 1e-4 * a_spec_cm2_cm3 * (thickness_um * 1e-4)   # A/cm²(geo)
    if i0_areal <= 0:
        return float('inf')
    f = alpha_sum * F_CONST / (R_GAS * temp_k)
    return (2.0 / f) * math.asinh(j_A_cm2 / (2.0 * i0_areal))


def ocp_slope_from_csv(path, x0=None, x100=None):
    """OCP 표(step4_pybamm_anchor --export-params 산출 CSV: x,U) → 창-평균 |dU/dx| [V].

    ★ 이 값은 **읽는 것**이지 가정하는 것이 아니다 (아래 eta_diff_V 참조).
    """
    xs, us = [], []
    for i, ln in enumerate(open(path)):
        parts = ln.replace(',', ' ').split()
        if i == 0 and parts and not parts[0].replace('.', '', 1).replace('-', '', 1).isdigit():
            continue                                          # 헤더
        if len(parts) >= 2:
            try:
                xs.append(float(parts[0])); us.append(float(parts[1]))
            except ValueError:
                continue
    if len(xs) < 3:
        raise ValueError(f'{path}: (x,U) 점이 부족 ({len(xs)})')
    o = sorted(range(len(xs)), key=lambda k: xs[k])
    xs = [xs[k] for k in o]; us = [us[k] for k in o]
    lo = min(x for x in (x0, x100) if x is not None) if (x0 or x100) else xs[0]
    hi = max(x for x in (x0, x100) if x is not None) if (x0 or x100) else xs[-1]
    seg = [(x, u) for x, u in zip(xs, us) if lo - 1e-9 <= x <= hi + 1e-9]
    if len(seg) < 2:
        raise ValueError(f'{path}: 창 [{lo},{hi}] 안에 점이 부족')
    # 창 평균 |dU/dx| = 총 전압변화 / 총 stoich 변화 (구간 절대값 가중)
    num = sum(abs(seg[i + 1][1] - seg[i][1]) for i in range(len(seg) - 1))
    den = abs(seg[-1][0] - seg[0][0])
    return num / den if den > 0 else float('nan')


def eta_diff_V(j_A_cm2, a_spec_cm2_cm3, thickness_um, r_p_um, d_s_m2_s,
               dudx_V=None, c_max_mol_m3=51765.0):
    """고체확산 과전압 [V] — 준정상 구형 확산의 표면-평균 stoich 격차 × |dU/dx|.

    Δx_surf = (j_local/(F·c_max))·r_p/(5·D_s)   (구형, 준정상 5-계수)
    η_diff  = |dU/dx|·Δx_surf

    ★ dudx_V 는 **필수 입력**이다 (기본 None → η_diff 계산 안 함, None 반환).
      2026-08-03: 처음엔 1.2 V 를 ASSUMED 기본값으로 박았는데, 실측 앵커 대비 η_diff 가
      **+160 %** 로 튀었다.  앵커에 맞게 1.2→0.46 으로 내리면 숫자는 맞지만 그건
      **실측에 맞춘 적합**이고, 이 모듈이 내세운 "적합 파라미터 0" 과 frame[4](모델을
      실험에 각각 독립 보정, 서로에 맞추지 않음)를 동시에 깬다.  ⇒ 튜닝하지 않고,
      OCP 표에서 **읽도록** 만들었다 (ocp_slope_from_csv).  표가 없으면 η_diff 는 **미산출**.
    """
    if dudx_V is None:
        return None                                           # 앵커 없음 → 침묵의 가짜값 금지
    if not (d_s_m2_s > 0 and r_p_um > 0 and a_spec_cm2_cm3 > 0):
        return float('inf')
    j_local = j_A_cm2 / (a_spec_cm2_cm3 * (thickness_um * 1e-4))          # A/cm²(surface)
    j_si = j_local * 1e4                                                  # A/m²
    dx = (j_si / (F_CONST * c_max_mol_m3)) * (r_p_um * 1e-6) / (5.0 * d_s_m2_s)
    return abs(dudx_V) * dx


def predict(sigma_ion_mScm, sigma_e_mScm, thickness_um, loading_mAh_cm2, c_rate,
            phi_am=0.55, r_p_um=3.0, coverage=0.5, i0_A_m2=2.0, d_s_m2_s=3e-14,
            temp_k=T_REF_K, r_int_ohm_cm2=0.0, v_window_V=1.5, tlm=TLM_FACTOR,
            dudx_V=None):
    """구조 → 성능.  적합 파라미터 0개.  반환 dict (mV 단위 η + delivered 추정).

    delivered 는 **율특성 지표**다: 총 과전압이 창(v_window_V)을 얼마나 갉아먹는지.
      delivered ≈ 1 − η_total/V_window   (선형 근사, ★ASSUMED — OCP 곡률·CV 미포함)
    ⇒ 절대 용량 예측이 아니라 **상대 비교(P:S 스윕)용** 이다.  절대값은 STEP4 가 심판.
    """
    j = current_density_A_cm2(loading_mAh_cm2, c_rate)
    asr_i = asr_ohm_cm2(thickness_um, sigma_ion_mScm, tlm)
    asr_e = asr_ohm_cm2(thickness_um, sigma_e_mScm, tlm)
    a_spec = specific_area_cm2_cm3(r_p_um, phi_am, coverage)
    e_ohm_i = j * asr_i
    e_ohm_e = j * asr_e
    e_ohm_r = j * r_int_ohm_cm2                       # 집전체 계면 (직렬, TLM 아님)
    e_kin = eta_kin_V(j, i0_A_m2, a_spec, thickness_um, temp_k)
    e_dif = eta_diff_V(j, a_spec, thickness_um, r_p_um, d_s_m2_s, dudx_V)
    # ★ η_diff 는 OCP 기울기가 없으면 **미산출**(None) — 0 으로 치면 총 η 를 과소평가
    #   하면서 그 사실이 숨는다.  총합도 같이 '부분'으로 낙인한다.
    e_tot = e_ohm_i + e_ohm_e + e_ohm_r + e_kin + (e_dif or 0.0)
    return {
        'c_rate': c_rate, 'j_A_cm2': j,
        'ASR_ion_ohm_cm2': asr_i, 'ASR_e_ohm_cm2': asr_e,
        'a_spec_cm2_cm3': a_spec,
        'eta_ohm_ion_mV': e_ohm_i * 1e3, 'eta_ohm_e_mV': e_ohm_e * 1e3,
        'eta_ohm_rint_mV': e_ohm_r * 1e3,
        'eta_ohm_mV': (e_ohm_i + e_ohm_e + e_ohm_r) * 1e3,
        'eta_kin_mV': e_kin * 1e3,
        'eta_diff_mV': (None if e_dif is None else e_dif * 1e3),
        'eta_total_mV': e_tot * 1e3,
        'eta_total_is_partial': e_dif is None,   # True = 확산항 빠진 **하한**
        'dudx_V': dudx_V,
        'delivered_frac_est': max(0.0, 1.0 - e_tot / v_window_V),
        'ionic_limited': e_ohm_i > e_ohm_e,           # σ_ion≪σ_e 시그니처
        'ohm_share_pct': 100.0 * (e_ohm_i + e_ohm_e + e_ohm_r) / e_tot if e_tot > 0 else 0.0,
        'model': 'reduced-order 0-D (STEP4 와 동일 물리, 공간해 없음) — 적합 파라미터 0',
        'assumed': ['delivered 선형근사 (OCP 곡률·CV 미포함)',
                    ('dU/dx 미제공 → η_diff 미산출 (총 η 는 하한)' if dudx_V is None
                     else f'dU/dx = {dudx_V:g} V (OCP 표에서 읽은 값)'),
                    'coverage 를 반응면 몫으로 사용',
                    f'옴 TLM 계수 L/{tlm:g}σ (균일반응 유도; 고율은 이보다 작음)'],
    }


def validate(verbose=True):
    """리포의 실측 2C STEP4 런(SBE/DBE)과 대조 → 잔차 리스트."""
    out = []
    for lab, a in SDCP_2C_ANCHOR.items():
        p = predict(SDCP_BED['sigma_ion_mScm'], a['sigma_e_mScm'],
                    SDCP_BED['thickness_um'], SDCP_BED['loading_mAh_cm2'], 2.0,
                    r_p_um=SDCP_BED['r_p_um'], coverage=SDCP_BED['coverage'],
                    i0_A_m2=SDCP_BED['i0_A_m2'], d_s_m2_s=SDCP_BED['d_s_m2_s'])
        row = {'label': lab}
        for k in ('eta_ohm_mV', 'eta_kin_mV'):
            row[k] = (p[k], a[k], (p[k] - a[k]) / a[k] * 100.0 if a[k] else float('nan'))
        # η_diff 는 dU/dx 없이 미산출 → 대신 **앵커가 함의하는 dU/dx** 를 역산해 진단으로만 보고
        pd_ = predict(SDCP_BED['sigma_ion_mScm'], a['sigma_e_mScm'], SDCP_BED['thickness_um'],
                      SDCP_BED['loading_mAh_cm2'], 2.0, r_p_um=SDCP_BED['r_p_um'],
                      coverage=SDCP_BED['coverage'], i0_A_m2=SDCP_BED['i0_A_m2'],
                      d_s_m2_s=SDCP_BED['d_s_m2_s'], dudx_V=1.0)
        row['implied_dudx_V'] = a['eta_diff_mV'] / pd_['eta_diff_mV'] if pd_['eta_diff_mV'] else None
        out.append(row)
        if verbose:
            print(f"  {lab}:")
            for k in ('eta_ohm_mV', 'eta_kin_mV'):
                m, r, e = row[k]
                print(f"    {k:14s} 모델 {m:7.1f} vs 실측 {r:6.1f}  ({e:+6.1f}%)")
            print(f"    {'eta_diff_mV':14s} 미산출 (dU/dx 입력 없음) — 실측 "
                  f"{a['eta_diff_mV']:.1f} mV 가 함의하는 |dU/dx| = "
                  f"{row['implied_dudx_V']:.3f} V  ★진단일 뿐, 기본값 아님")
    if verbose:
        # ★가장 중요한 검증: 모델이 SBE→DBE 방향(σ_e↑ → η↓)을 맞추는가
        d = out[1]['eta_ohm_mV'][0] - out[0]['eta_ohm_mV'][0]
        r = SDCP_2C_ANCHOR['DBE']['eta_ohm_mV'] - SDCP_2C_ANCHOR['SBE']['eta_ohm_mV']
        print(f"\n  ★방향성 (DBE−SBE η_ohm): 모델 {d:+.2f} mV vs 실측 {r:+.2f} mV "
              f"— 부호 {'일치' if d * r > 0 else '★불일치'}")
        print(f"  ⚠ {SDCP_BED['src']}")
    return out


def _selftest():
    ok = tot = 0

    def chk(name, cond, extra=''):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}" + (f' — {extra}' if extra else ''))

    # 1) TLM 계수가 유도값 (끝점 L/2 도, 판상 L 도 아님)
    a3 = asr_ohm_cm2(72.48, 0.203)
    chk('ASR = L/(3σ) — 유도된 반응-가중 평균', abs(a3 - (72.48e-4 / 0.203e-3) / 3.0) < 1e-9,
        f'{a3:.2f} Ω·cm²  (끝점 L/2σ = {a3*1.5:.2f}, 판상 L/σ = {a3*3:.2f})')
    # 2) 스케일링: η_ohm ∝ rate, ∝ L, ∝ 1/σ
    p1 = predict(0.203, 1.979, 72.48, 3.18, 1.0)
    p2 = predict(0.203, 1.979, 72.48, 3.18, 2.0)
    chk('η_ohm ∝ C-rate (2C = 1C 의 2배)',
        abs(p2['eta_ohm_mV'] / p1['eta_ohm_mV'] - 2.0) < 1e-9)
    pL = predict(0.203, 1.979, 144.96, 3.18, 2.0)
    chk('η_ohm ∝ 두께', abs(pL['eta_ohm_mV'] / p2['eta_ohm_mV'] - 2.0) < 1e-9)
    pS = predict(0.406, 1.979, 72.48, 3.18, 2.0)
    chk('η_ohm,ion ∝ 1/σ_ion',
        abs(pS['eta_ohm_ion_mV'] / p2['eta_ohm_ion_mV'] - 0.5) < 1e-9)
    # 3) ★이온-제한 시그니처 (σ_ion ≪ σ_e 이면 이온 옴이 지배)
    chk('σ_ion(0.203) ≪ σ_e(1.979) → 이온 옴이 전자 옴을 지배',
        p2['ionic_limited'] and p2['eta_ohm_ion_mV'] > 8 * p2['eta_ohm_e_mV'],
        f"이온 {p2['eta_ohm_ion_mV']:.1f} vs 전자 {p2['eta_ohm_e_mV']:.2f} mV")
    # 4) BV 는 선형화가 아니라 asinh (고율서 로그 포화)
    hi = predict(0.203, 1.979, 72.48, 3.18, 8.0)
    chk('η_kin 이 rate 에 **선형이 아님** (asinh 포화)',
        hi['eta_kin_mV'] / p2['eta_kin_mV'] < 4.0,
        f"8C/2C = {hi['eta_kin_mV']/p2['eta_kin_mV']:.2f}× (선형이면 4.0)")
    # 5) 실측 앵커 대조 — 방향성 + 자릿수
    v = validate(verbose=False)
    sbe = dict(zip(('m', 'r', 'e'), v[0]['eta_ohm_mV']))
    chk('★앵커가 함의하는 |dU/dx| 를 진단으로 보고 (기본값으로 승격 안 함)',
        v[0].get('implied_dudx_V') is not None and 0.2 < v[0]['implied_dudx_V'] < 1.0,
        f"{v[0]['implied_dudx_V']:.3f} V")
    chk('★실측 2C η_ohm 과 같은 자릿수 (SBE 93.3 mV)', abs(sbe['e']) < 60.0,
        f"모델 {sbe['m']:.1f} vs 실측 {sbe['r']:.1f} ({sbe['e']:+.1f}%)")
    dm = v[1]['eta_ohm_mV'][0] - v[0]['eta_ohm_mV'][0]
    dr = v[1]['eta_ohm_mV'][1] - v[0]['eta_ohm_mV'][1]
    chk('★DBE 가 SBE 보다 η_ohm 낮다 (σ_e↑ 방향 재현)', dm < 0 and dr < 0,
        f'모델 {dm:+.2f} vs 실측 {dr:+.2f} mV')
    # 6) 퇴화 입력 방어
    chk('σ=0 → inf (조용한 0 아님)', math.isinf(asr_ohm_cm2(72.48, 0.0)))
    chk('coverage=0 → 반응면 0 → η_kin inf',
        math.isinf(predict(0.203, 1.979, 72.48, 3.18, 2.0, coverage=0.0)['eta_kin_mV']))
    # ★ 확산 게이트: dU/dx 없으면 **조용한 0 이 아니라 미산출**, 총합은 '하한' 으로 낙인
    pnd = predict(0.203, 1.979, 72.48, 3.18, 2.0)
    chk('dU/dx 없음 → η_diff None (0 으로 위장 안 함)',
        pnd['eta_diff_mV'] is None and pnd['eta_total_is_partial'] is True)
    pwd = predict(0.203, 1.979, 72.48, 3.18, 2.0, dudx_V=0.46)
    chk('dU/dx 주면 산출되고 총합이 그만큼 커진다',
        pwd['eta_diff_mV'] is not None and pwd['eta_total_is_partial'] is False
        and pwd['eta_total_mV'] > pnd['eta_total_mV'],
        f"{pnd['eta_total_mV']:.1f} → {pwd['eta_total_mV']:.1f} mV")
    chk('η_diff ∝ dU/dx (선형)',
        abs(predict(0.203, 1.979, 72.48, 3.18, 2.0, dudx_V=0.92)['eta_diff_mV']
            / pwd['eta_diff_mV'] - 2.0) < 1e-9)
    # OCP 표 리더 — 창-평균 |dU/dx| 를 **읽는다**
    import tempfile as _tf, os as _os
    with _tf.NamedTemporaryFile('w', suffix='.csv', delete=False) as fh:
        fh.write('x,U\n0.2,4.3\n0.5,4.0\n0.9,3.7\n'); _p = fh.name
    _sl = ocp_slope_from_csv(_p)
    chk('OCP CSV → 창-평균 |dU/dx| 를 읽는다 (가정 아님)',
        abs(_sl - 0.6 / 0.7) < 1e-9, f'{_sl:.4f} V  (총 |ΔU| 0.6 / Δx 0.7)')
    _os.unlink(_p)
    # 7) 적합 파라미터가 정말 0개인지 (라벨 정직성)
    chk('산출물이 "적합 0" 을 명시', '적합 파라미터 0' in p2['model'])
    chk('ASSUMED 항목이 열거된다', len(p2['assumed']) >= 4)
    print(f"PERF-REDUCED-ORDER SELFTEST {ok}/{tot} {'PASS' if ok == tot else 'FAIL'}")
    return 0 if ok == tot else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--validate', action='store_true', help='리포 실측 2C 런과 대조')
    ap.add_argument('--sigma-ion', type=float, default=0.203, help='σ_ion [mS/cm]')
    ap.add_argument('--sigma-e', type=float, default=1.979, help='σ_e [mS/cm]')
    ap.add_argument('--thickness-um', type=float, default=72.48)
    ap.add_argument('--loading', type=float, default=3.18, help='[mAh/cm²]')
    ap.add_argument('--c-rate', type=float, default=2.0)
    ap.add_argument('--phi-am', type=float, default=0.55)
    ap.add_argument('--r-p-um', type=float, default=3.0)
    ap.add_argument('--coverage', type=float, default=0.5)
    ap.add_argument('--i0', type=float, default=2.0, help='[A/m²]')
    ap.add_argument('--d-s', type=float, default=3e-14, help='[m²/s]')
    ap.add_argument('--r-int-ohm-cm2', type=float, default=0.0)
    ap.add_argument('--dudx', type=float, default=None,
                    help='창-평균 |dU/dx| [V] — η_diff 에 필수.  미지정이면 η_diff 미산출 '
                         '(0 으로 위장하지 않는다).  --ocp-csv 로 표에서 읽는 쪽을 권장.')
    ap.add_argument('--ocp-csv', default='',
                    help='OCP 표 CSV (x,U) → 창-평균 |dU/dx| 자동 산출 (step4_pybamm_anchor '
                         '--export-params 산출물).  --dudx 보다 우선.')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    if a.validate:
        print('실측 2C STEP4 런 대조 (docs/sdcp_318_base_sbe_dbe_comparison.md:92-95)')
        validate()
        return 0
    _dudx = a.dudx
    if a.ocp_csv:
        _dudx = ocp_slope_from_csv(a.ocp_csv)
        print(f"  OCP 표에서 읽은 창-평균 |dU/dx| = {_dudx:.4f} V  ({a.ocp_csv})")
    p = predict(a.sigma_ion, a.sigma_e, a.thickness_um, a.loading, a.c_rate,
                phi_am=a.phi_am, r_p_um=a.r_p_um, coverage=a.coverage,
                i0_A_m2=a.i0, d_s_m2_s=a.d_s, r_int_ohm_cm2=a.r_int_ohm_cm2,
                dudx_V=_dudx)
    print(f"\n{a.c_rate:g}C · L={a.thickness_um:g}µm · loading={a.loading:g} mAh/cm² "
          f"· σ_ion={a.sigma_ion:g} / σ_e={a.sigma_e:g} mS/cm")
    print(f"  j = {p['j_A_cm2']*1e3:.2f} mA/cm²   ASR: ion {p['ASR_ion_ohm_cm2']:.2f} · "
          f"e {p['ASR_e_ohm_cm2']:.3f} Ω·cm²")
    print(f"  η [mV]  옴 {p['eta_ohm_mV']:7.1f}  (이온 {p['eta_ohm_ion_mV']:.1f} · "
          f"전자 {p['eta_ohm_e_mV']:.3f} · R_int {p['eta_ohm_rint_mV']:.1f})")
    _d = ('   미산출(--dudx 또는 --ocp-csv 필요)' if p['eta_diff_mV'] is None
          else f"{p['eta_diff_mV']:6.1f}")
    print(f"          kin {p['eta_kin_mV']:6.1f}   확산 {_d}")
    print(f"          = 총 {p['eta_total_mV']:.1f} mV"
          + ('  ★확산항 빠진 **하한**' if p['eta_total_is_partial'] else ''))
    print(f"  옴 지배 {p['ohm_share_pct']:.0f}% · "
          f"{'★이온-제한' if p['ionic_limited'] else '전자-제한'}")
    print(f"  delivered(상대비교용) ≈ {p['delivered_frac_est']*100:.1f}%")
    print(f"  ⚠ ASSUMED: {' · '.join(p['assumed'])}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
