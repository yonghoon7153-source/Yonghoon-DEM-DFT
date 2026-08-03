#!/usr/bin/env python3
"""cam_kinetics — CAM 계면 반응동역학의 **온도 의존** 단일 출처 (i0(T)).

왜 이 모듈이 있나
────────────────
`step4_dyn.py` 의 `--temp-k` 는 지금까지 **쓸 수 없는 노브**였다.  `Kinetics.T` 가 바꾸는 것은
Butler-Volmer 지수의 `f = F/(RT)` **하나뿐**이고 `i0` 는 25 °C 상수로 남았기 때문에, T 를 올리면
같은 전류에 필요한 η_ct 가 **커진다**.  실측은 반대다 — R_ct 는 30→60 °C 에 4.28× **감소**한다.
그래서 `docs/temp_pressure_capability.md` §3-3① 이 이걸 "온도를 반영했다는 인상을 주면서 반대
답을 내는 것 = 가장 나쁜 실패" 로 규정하고, 킷은 `--temp-k` 를 **의도적으로 굽지 않았다**.

이 모듈이 그 구멍을 닫는다.  i0 의 온도 의존을 **우리 소재계 자체 측정**에 앵커한다.

★ 앵커 (kim2025 — 우리와 같은 NCM811 + LPSCl) ★
──────────────────────────────────────────────
Kim, Kang, Park, Lee — Electrochim. Acta 542 (2025) 147413, Table S6.
같은 셀(NCM811:LPSCl:SuperP = 72:27:1, uncoated)을 **세 온도에서** 측정:

    R_ct = 289.9 / 139.6 / 67.8 Ω·cm²   @ 30 / 45 / 60 °C     (전부 stated = pdf_verified)

세 점 Arrhenius 적합 → **Eₐ(R_ct) = 0.4212 eV, R² = 0.99943**
(구간별 0.4049 / 0.4398 eV = 8 % 스프레드 — 완벽한 직선은 아니지만 3점으로 충분히 견고)

★★ 정정 (2026-07-30 적대리뷰 HIGH-1) — `R_ct ∝ 1/i0` 은 **틀렸다** ★★
선형화 BV (step4_dyn `Kinetics._ct`: `g = i0·A·f·(αa e⁺ + αc e⁻)`, `f = F/RT`) 에서

    R_ct = 1/(dI/dη)|_{η=0} = **RT / (F · i0 · A)**      ← T 가 **RT 에도** 있다

따라서 `i0 ∝ T / R_ct` 이지 `1/R_ct` 가 아니다.  첫 배선은 `ln R_ct` 를 그대로 적합해 Eₐ
전량을 i0 에 실었고 → i0 배수가 **10.5 % 과소**(60 °C: 5.5974 vs 정합 6.2545).
리포 자체 규약과도 어긋났다 — `se_material.py` 의 σ·T (Kraft) 규약은 이미 `(T_ref/T)`
전인자를 포함한다.  올바른 형태:

    i0(T)/i0(T_ref) = (T/T_ref) · R_ct(T_ref)/R_ct(T)
                    = (T/T_ref) · exp[ −(Eₐ_Rct/k_B)·(1/T − 1/T_ref) ]

    25 °C ×1.0000 · 30 °C ×1.3325 · 45 °C ×2.9907 · 60 °C ×6.2545
    (★ 이 네 숫자는 아래 selftest 가 `i0_temperature_factor` 로 재계산해 대조한다 — LOW-1 에서
     45 °C 자리에 2.947 이라는 손계산 오탈자가 **코드 소유 모듈에만** 남아 docs 와 갈렸다.
     이제 이 표에 손으로 쓴 값이 함수와 어긋나면 selftest 가 FAIL 한다.)

★ 전이 가정 (라벨 필수) ★
─────────────────────────
- 앵커는 **72 wt% NCM, uncoated, post-formation** 한 조성이다.  Eₐ 가 조성·코팅·사이클 상태에
  무관하다고 **가정**한다.
  ★★ 정정 (2026-07-30 리뷰 HIGH-7) — 이 자리에 "코팅계 T-스윕은 논문에 없다" 고 적었던 것은
  **거짓**이었다.  `docs/data/kim2025_tlm_kinetics_anchors.csv` (Table S4, LNO 62 wt%) 에
  세 온도가 stated 로 있다:  **30 °C 22.4 · 45 °C 8.7 · 60 °C 7.6 Ω·cm²**.
  그리고 그 데이터는 위 전이가정을 **반증**한다 — 구간별 Eₐ 가 0.524 / 0.082 eV 로 **6.4×**
  갈라져 Arrhenius 가 아니고(3점 R² ≈ 0.86), 코팅계 i0(60) 배수는 uncoated 와 크게 다르다.
  ⇒ **코팅 케이스에 이 모듈을 쓰면 uncoated Eₐ 를 조용히 상속한다.**  `--i0-temp-scale` 을
  코팅 프리셋(coating_presets.py)과 함께 쓸 때는 그 사실을 결과에 적어야 한다.
  (누락이 우리에게 유리한 방향으로 작동했다는 점이 이 정정의 요지다.)
- Eₐ 자체는 우리가 세 점에서 적합한 값이다.  논문이 "0.42 eV" 를 인쇄한 것이 아니라
  `docs/data/rint_eis_anchors.csv` 의 stated R 값들에서 **우리가 유도**했다 → provenance는
  `derived_from_stated_anchors`.  아래 selftest 가 CSV 를 다시 읽어 이 상수를 재유도해 검증한다.
- **분해율 Eₐ 와 혼동 금지.**  이건 R_ct 라는 **상태량**의 온도 의존이지, 열화 **속도**의 가속이
  아니다.  LPSCl 분해율 Eₐ 는 문헌에 존재하지 않는다(`docs/joule_hotspot.md` §TARGET 1) —
  이 모듈로 열화 가속을 만들면 안 된다.

★ 여전히 앵커가 없는 것 (그래서 T 를 켜도 부분 반영) ★
──────────────────────────────────────────────────
D_s(T) · OCP dU/dT · σ_e(T) · κ(T) · SE 경도 H(T)/σ_y(T) · 분해율.
⇒ `--temp-k` + 이 모듈 = **σ_ion + i0 만** 온도를 따르는 PARTIAL 상태.  전-물리 온도 스윕 아님.
   다만 **부호는 맞는다** — 그게 이 모듈의 요점이다.

Selftest:  python3 scripts/cam_kinetics.py --selftest
"""

import math
import os

# ── kim2025 Table S6 앵커 (rint_eis_anchors.csv 와 동일 값 — selftest 가 대조) ──────────────
#    (T_C, R_ct Ω·cm²) — NCM811:LPSCl:SuperP 72:27:1, uncoated, post-formation
RCT_T_ANCHOR = ((30.0, 289.9), (45.0, 139.6), (60.0, 67.8))
RCT_ANCHOR_SOURCE = ('kim2025 Electrochim.Acta 542 (2025) 147413 Table S6 — '
                     'NCM811+LPSCl 72wt% uncoated, R values STATED (pdf_verified)')

# ★ LNO 코팅계 T-스윕 (Table S4, 62 wt%) — **비-Arrhenius**.  전이가정의 반증 증거로 보관한다
#   (구간별 Eₐ 0.524 / 0.082 eV = 6.4× 스프레드).  기본 배선은 uncoated 를 쓰므로 코팅 케이스는
#   이 값과 다르다 — selftest 가 그 차이를 못박는다.
RCT_T_ANCHOR_LNO = ((30.0, 22.4), (45.0, 8.7), (60.0, 7.6))

T_REF_C = 25.0                  # se_material.T_REF_C 와 같은 규약 (selftest 가 일치 확인)
KB_EV = 8.617333262e-5          # eV/K

# ★ 위 3점 Arrhenius 적합 결과 (아래 selftest 가 재유도해 검증 — 매직넘버 아님)
EA_RCT_EV = 0.4212              # eV, R² = 0.99943
EA_RCT_EV_INTERVALS = (0.4049, 0.4398)      # 30→45 / 45→60 구간별 (스프레드 = 불확실성 척도)
EA_RCT_PROVENANCE = 'derived_from_stated_anchors (3-point Arrhenius fit of kim2025 R_ct(T))'


def _fit_ea(points):
    """(T_C, R) 점들 → (Ea_eV, R²).  ln R = (Ea/k_B)·(1/T) + c 최소자승."""
    xs = [1.0 / (t + 273.15) for t, _ in points]
    ys = [math.log(r) for _, r in points]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    inter = my - slope * mx
    ss_res = sum((y - (slope * x + inter)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return slope * KB_EV, r2


def i0_temperature_factor(T_C=None, ea_ev=None, t_ref_c=T_REF_C):
    """i0(T)/i0(T_ref) — kim2025 R_ct(T) 앵커 기반.

    T_C=None ⇒ **정확히 1.0** (기본 OFF; 기존 런 bitwise 불변).
    ea_ev 로 Eₐ 를 바꿀 수 있다 — 구간별 스프레드(0.4049/0.4398)를 쓸어 밴드로 보고할 때 사용.
    """
    if T_C is None:
        return 1.0
    ea = EA_RCT_EV if ea_ev is None else float(ea_ev)
    # ⚠ HIGH-6: ea=0 이면 배수 1.0 인데 step4 가드는 해제돼 "스케일했다"고 주장하게 되고,
    #   ea<0 이면 **부호역전이 완전히 복원**된다 (실측 60 °C: 93.44 → 201.82 mV).  둘 다 거부.
    if not (ea > 0.0):
        raise ValueError(f'i0_temperature_factor: Eₐ 는 양수여야 한다 (got {ea!r}) — '
                         'ea=0 은 "스케일 안 함"을 "스케일함"으로 라벨하고, ea<0 은 부호역전을 '
                         '복원한다 (2026-07-30 리뷰 HIGH-6)')
    t, tr = float(T_C) + 273.15, float(t_ref_c) + 273.15
    if t <= 0.0 or tr <= 0.0:
        raise ValueError(f'i0_temperature_factor: T_C={T_C} 는 절대영도 이하')
    # ★ (T/T_ref) 전인자 = R_ct = RT/(F i0 A) 의 RT (HIGH-1).  빠뜨리면 60 °C 에서 10.5% 과소.
    return (t / tr) * math.exp(-(ea / KB_EV) * (1.0 / t - 1.0 / tr))


def rct_temperature_factor(T_C=None, ea_ev=None, t_ref_c=T_REF_C):
    """R_ct(T)/R_ct(T_ref) — **측정된 양** 이므로 순수 Arrhenius (전인자 없음).

    ★★ 이것은 `1/i0_temperature_factor` 가 **아니다** (2026-07-30 리뷰 HIGH-1 의 핵심).
       R_ct = RT/(F·i0·A) 이므로
           R_ct(T)/R_ct(T_ref) = (T/T_ref) · i0(T_ref)/i0(T)
       이고, i0 배수에 이미 (T/T_ref) 가 들어 있어 역수를 취하면 전인자가 **한 번 더** 들어가
       측정값과 어긋난다(60 °C 에서 0.2130 vs 실측 0.2339 = 9% 오차).  옛 코드가 역수로
       정의해 두는 바람에, 그걸로 앵커를 대조하던 테스트가 자기순환이 됐다.
       ⇒ 여기서는 적합된 Eₐ 로 **직접** 계산한다.
    """
    if T_C is None:
        return 1.0
    ea = EA_RCT_EV if ea_ev is None else float(ea_ev)
    if not (ea > 0.0):
        raise ValueError(f'rct_temperature_factor: Eₐ 는 양수여야 한다 (got {ea!r})')
    t, tr = float(T_C) + 273.15, float(t_ref_c) + 273.15
    if t <= 0.0 or tr <= 0.0:
        raise ValueError(f'rct_temperature_factor: T_C={T_C} 는 절대영도 이하')
    return math.exp((ea / KB_EV) * (1.0 / t - 1.0 / tr))


def provenance(T_C=None, ea_ev=None):
    """감사 기록 dict.  T_C=None 이면 None (기본 런의 산출물은 이 키를 갖지 않는다)."""
    if T_C is None:
        return None
    ea = EA_RCT_EV if ea_ev is None else float(ea_ev)
    # ★ HIGH-6: override 를 주면 밴드도 그 값 기준으로 재계산하고 provenance 를 USER_OVERRIDE 로
    #   바꾼다.  옛 코드는 항상 정본 구간쌍으로 밴드를 계산해, override 값이 밴드 **밖**에 있는데도
    #   kim2025 라벨이 붙었다.
    if ea_ev is None:
        lo = i0_temperature_factor(T_C, EA_RCT_EV_INTERVALS[0])
        hi = i0_temperature_factor(T_C, EA_RCT_EV_INTERVALS[1])
        _prov_lbl = EA_RCT_PROVENANCE
    else:
        _sp = 0.5 * (EA_RCT_EV_INTERVALS[1] - EA_RCT_EV_INTERVALS[0])   # 정본 스프레드 폭 유지
        lo = i0_temperature_factor(T_C, max(1e-6, ea - _sp))
        hi = i0_temperature_factor(T_C, ea + _sp)
        _prov_lbl = (f'USER_OVERRIDE (Eₐ={ea:g} eV, 정본 kim2025 유도값 {EA_RCT_EV:g} 아님 — '
                     f'이 런의 i0(T) 는 앵커가 아니라 사용자 지정이다)')
    return {
        'T_C': float(T_C),
        'T_ref_C': float(T_REF_C),
        'Ea_Rct_eV': ea,
        'Ea_provenance': _prov_lbl,
        'Ea_is_user_override': ea_ev is not None,
        'i0_T_factor': i0_temperature_factor(T_C, ea),
        'i0_T_factor_band': [min(lo, hi), max(lo, hi)],
        'Ea_interval_spread_eV': list(EA_RCT_EV_INTERVALS),
        'anchor': RCT_ANCHOR_SOURCE,
        'anchor_points_T_C_Rct': [list(p) for p in RCT_T_ANCHOR],
        'scope': 'i0 (charge-transfer exchange current) ONLY',
        'NOT_a_degradation_rate': (
            'R_ct 는 상태량이다 — 이 인수는 "온도가 높으면 반응이 빠르다"이지 '
            '"온도가 높으면 더 빨리 열화한다"가 아니다.  LPSCl 분해율 Eₐ 는 문헌에 '
            '존재하지 않는다 (docs/joule_hotspot.md TARGET 1) → 열화 가속에 쓰면 날조(§F1).'),
        # ★ HIGH-3 (2026-07-30 리뷰): 옛 문자열은 "LNO 코팅계 T-스윕은 논문에 없음" 이라고
        #   적었으나 **거짓**이다 — Table S4 (LNO 62 wt%) 에 30/45/60 °C 가 stated 로 있고,
        #   그 데이터가 이 전이가정을 **반증**한다.  기계가 읽는 dict 가 문서(docstring §전이가정)
        #   와 반대 사실을 말하고 있었고, 누락이 우리에게 유리한 방향이었다.
        'transfer_assumption': (
            '앵커는 72 wt% uncoated 한 조성 · post-formation.  Eₐ 가 조성/코팅/사이클 상태에 '
            '무관하다고 **가정**한다 — 그러나 이 가정은 코팅계에서 **반증**되어 있다: '
            'kim2025 Table S4 (LNO 62 wt%) 의 R_ct = 22.4/8.7/7.6 Ω·cm² @30/45/60 °C 는 '
            '비-Arrhenius (구간별 Eₐ 0.524 / 0.082 eV = 6.4× 스프레드, 3점 R²≈0.86).  '
            '⇒ 코팅 프리셋과 함께 쓰면 uncoated Eₐ 를 조용히 상속한다 — 결과에 명기할 것.'),
        'transfer_assumption_refuted_for_coated': True,
        'coated_counter_anchor_T_C_Rct': [list(p) for p in RCT_T_ANCHOR_LNO],
        'coated_counter_anchor_source': ('kim2025 Table S4 — NCM811+LPSCl 62wt%, LNO-coated; '
                                         'non-Arrhenius (see transfer_assumption)'),
        'still_unanchored': ['D_s(T)', 'OCP dU/dT', 'sigma_e(T)', 'kappa(T)',
                             'SE hardness H(T)/sigma_y(T)', 'degradation rate'],
    }


def _selftest():
    ok = True

    def chk(name, cond, extra=''):
        nonlocal ok
        print(f"  {'OK  ' if cond else 'FAIL'} {name}" + (f' — {extra}' if extra else ''))
        ok &= bool(cond)

    # 1) 상수가 앵커에서 실제로 유도되는가 (매직넘버 금지)
    ea, r2 = _fit_ea(RCT_T_ANCHOR)
    chk('Eₐ 상수가 3점 적합값과 일치 (매직넘버 아님)',
        abs(ea - EA_RCT_EV) < 5e-4 and r2 > 0.999, f'적합 {ea:.4f} eV, R²={r2:.5f}')
    ea_lo, _ = _fit_ea(RCT_T_ANCHOR[:2])
    ea_hi, _ = _fit_ea(RCT_T_ANCHOR[1:])
    chk('구간별 Eₐ 상수도 일치',
        abs(ea_lo - EA_RCT_EV_INTERVALS[0]) < 5e-4
        and abs(ea_hi - EA_RCT_EV_INTERVALS[1]) < 5e-4, f'{ea_lo:.4f} / {ea_hi:.4f} eV')

    # 2) ★ 정본 CSV 와 앵커 값이 어긋나지 않는가 (두 곳에 적힌 숫자가 갈라지는 것 방지)
    csv_p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         '..', 'docs', 'data', 'rint_eis_anchors.csv')
    try:
        import csv as _csv
        want = {30.0: 289.9, 45.0: 139.6, 60.0: 67.8}
        got = {}
        for r in _csv.DictReader(open(csv_p)):
            if r['anchor_id'].startswith('kim2025_bare_rct') and r['quantity'] == 'R_ct':
                t = float(r['T_meas_C']) if r['T_meas_C'].strip() else None
                if t in want and abs(float(r['value']) - want[t]) < 1e-9:
                    got[t] = float(r['value'])
        chk('정본 rint_eis_anchors.csv 의 R_ct(30/45/60) 와 일치',
            got == want, f'CSV에서 찾은 점 {sorted(got)}')
    except Exception as e:
        chk('정본 CSV 대조', False, f'{type(e).__name__}: {e}')

    # 3) 기본 OFF = 정확히 1.0 (bitwise)
    chk('T_C=None → 정확히 1.0 (기본 런 불변)',
        i0_temperature_factor().hex() == (1.0).hex())
    chk('T_C=T_ref → 1.0 (반올림 오차 없이 ~1)',
        abs(i0_temperature_factor(T_REF_C) - 1.0) < 1e-12)

    # 4) 방향 — 이 모듈의 존재 이유
    f60 = i0_temperature_factor(60.0)
    chk('★ 60 °C 에서 i0 가 커진다 (η_ct 감소 = 실측 방향)', f60 > 1.0, f'i0 ×{f60:.3f}')
    # ★ R_ct 배수는 **순수 Arrhenius** = 측정 그대로.  i0 배수의 역수가 아니다(HIGH-1).
    chk('★ R_ct(60)/R_ct(30) 이 앵커와 일치 (측정값 = 순수 Arrhenius)',
        abs((rct_temperature_factor(60.0) / rct_temperature_factor(30.0)) - (67.8 / 289.9))
        < 0.02, f'모델 {rct_temperature_factor(60.0) / rct_temperature_factor(30.0):.4f} vs '
                f'앵커 {67.8 / 289.9:.4f}')
    chk('★ R_ct 배수 ≠ 1/i0 배수 — 차이가 정확히 (T/T_ref) 전인자',
        abs(rct_temperature_factor(60.0) * i0_temperature_factor(60.0)
            - 333.15 / 298.15) < 1e-12,
        f'곱 {rct_temperature_factor(60.0) * i0_temperature_factor(60.0):.5f} '
        f'= T/T_ref {333.15 / 298.15:.5f}')
    chk('저온에서는 i0 가 작아진다', i0_temperature_factor(0.0) < 1.0,
        f'0 °C: ×{i0_temperature_factor(0.0):.4f}')

    # 5) ★ 비순환 앵커 재현 (2026-07-30 리뷰 HIGH-1) — 옛 테스트는 rct_factor = 1/i0_factor 의
    #    비를 앵커 비와 대조하는 **자기순환**이라 RT 전인자 누락을 구조적으로 못 잡았다.
    #    이제 **모델의 실제 R_ct = 1/(dI/dη)|₀** 를 step4_dyn.Kinetics 로 계산해 앵커와 대조한다.
    try:
        import sys as _s2
        _s2.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from step4_dyn import Kinetics as _K
        _A = 1.0                                   # 면적은 비에서 상쇄 — 절대값이 아니라 비를 본다
        _r30 = None
        _errs = []
        for t_c, r_meas in RCT_T_ANCHOR:
            _k = _K(2.0 * i0_temperature_factor(t_c), temp_k=t_c + 273.15)
            _, _g = _k._ct(0.0, _k.i0(0.5) * _A)   # dI/dη|₀
            _rct = 1.0 / _g                        # = RT/(F i0 A)
            if _r30 is None:
                _r30, _rm30 = _rct, r_meas
            _errs.append((t_c, _rct / _r30, r_meas / _rm30))
        # ★ MED-11 (2026-07-30 리뷰): tol 을 전 점 3% 로 두면 판별력이 **60 °C 한 점의 0.10 pp**
        #   여유에 걸린다 — 현행 45 °C 는 −2.90%, 버그판(전인자 X)은 +1.90% 라 45 °C 만 보면
        #   **버그판이 더 가깝다**.  2.90% 는 3점 적합의 고유 잔차(구간 Eₐ 0.4049/0.4398)이므로
        #   물리 오류가 아니지만, EA 나 앵커를 조금만 건드려도 정상 코드가 위양성 FAIL 로 뒤집힌다.
        #   ⇒ tol 을 점별로 분리: 45 °C 는 적합잔차 허용(5%), 60 °C 는 **판별점**이라 타이트(1%).
        #   이 테스트가 실제로 판별하는 것은 "RT 전인자 유무" 뿐이다 (아래 5b 가 직접 핀).
        _TOL = {30.0: 0.005, 45.0: 0.05, 60.0: 0.01}
        _ok5 = all(abs(m / a - 1.0) < _TOL[t] for t, m, a in _errs)
        chk('★ 비순환: 모델의 1/(dI/dη)|₀ 비가 앵커 R_ct 비와 일치 (점별 tol)',
            _ok5, ' · '.join(f'{t:.0f}°C 모델 {m:.4f} vs 앵커 {a:.4f} '
                             f'({(m/a-1)*100:+.2f}%, tol {_TOL[t]*100:g}%)'
                             for t, m, a in _errs))
        # ★ 판별력 증명: 전인자를 뺀 버그판은 60 °C 에서 tol 을 **반드시** 넘어야 한다
        _bug60 = math.exp(-(EA_RCT_EV / KB_EV) * (1.0 / 333.15 - 1.0 / 298.15))
        _k_bug = _K(2.0 * _bug60, temp_k=333.15)
        _, _g_bug = _k_bug._ct(0.0, _k_bug.i0(0.5) * _A)
        _m_bug = (1.0 / _g_bug) / _r30
        _a60 = RCT_T_ANCHOR[2][1] / _rm30
        chk('★[M11] 버그판(전인자 X)은 60 °C tol 을 넘어 FAIL 한다 (테스트가 실제로 판별)',
            abs(_m_bug / _a60 - 1.0) > _TOL[60.0],
            f'버그판 {(_m_bug/_a60-1)*100:+.2f}% vs tol {_TOL[60.0]*100:g}%')
    except Exception as e:
        chk('★ 비순환 앵커 재현', False, f'{type(e).__name__}: {e}')

    # 5b) ★ RT 전인자가 실제로 들어있는가 (HIGH-1 회귀 핀)
    _f60 = i0_temperature_factor(60.0)
    _f60_no_rt = math.exp(-(EA_RCT_EV / KB_EV) * (1.0 / 333.15 - 1.0 / 298.15))
    chk('★ (T/T_ref) 전인자가 들어있다 (없으면 10.5% 과소 — 옛 결함)',
        abs(_f60 / _f60_no_rt - 333.15 / 298.15) < 1e-12,
        f'{_f60:.4f} (전인자 없으면 {_f60_no_rt:.4f})')

    # 5c) ★ Eₐ 무결성 (HIGH-6)
    for _bad in (0.0, -EA_RCT_EV, -1.0):
        try:
            i0_temperature_factor(60.0, _bad)
            chk(f'Eₐ={_bad} 거부', False, '통과해버림')
        except ValueError:
            chk(f'Eₐ={_bad:g} 거부 (ea=0 은 거짓라벨, ea<0 은 부호역전 복원)', True)
    _po = provenance(60.0, 0.9)
    chk('override 는 USER_OVERRIDE 로 낙인 + 밴드도 그 값 기준',
        _po['Ea_is_user_override'] and 'USER_OVERRIDE' in _po['Ea_provenance']
        and _po['i0_T_factor_band'][0] < _po['i0_T_factor'] < _po['i0_T_factor_band'][1])

    # 5d) ★ LNO 코팅계는 비-Arrhenius = 전이가정의 반증 (HIGH-7)
    _ea_lno, _r2_lno = _fit_ea(RCT_T_ANCHOR_LNO)
    _i1, _ = _fit_ea(RCT_T_ANCHOR_LNO[:2])
    _i2, _ = _fit_ea(RCT_T_ANCHOR_LNO[1:])
    chk('★ LNO 코팅 T-스윕이 존재하고 **비-Arrhenius** (전이가정 반증)',
        _r2_lno < 0.95 and abs(_i1 / max(_i2, 1e-9)) > 3.0,
        f'Eₐ={_ea_lno:.4f} R²={_r2_lno:.4f}, 구간 {_i1:.4f}/{_i2:.4f} eV = {_i1/_i2:.1f}×')
    chk('★ 코팅계 i0(60) 배수가 uncoated 와 유의하게 다르다 (조용한 상속 위험)',
        abs(i0_temperature_factor(60.0, _ea_lno) / i0_temperature_factor(60.0) - 1.0) > 0.2,
        f'코팅 ×{i0_temperature_factor(60.0, _ea_lno):.3f} vs uncoated '
        f'×{i0_temperature_factor(60.0):.3f}')

    # 6) 밴드 (구간 Eₐ 스프레드) — 단일값 보고 방지
    p = provenance(60.0)
    chk('provenance 가 Eₐ 밴드를 병기 (단일값 보고 방지)',
        p['i0_T_factor_band'][0] < p['i0_T_factor'] < p['i0_T_factor_band'][1],
        f"×{p['i0_T_factor_band'][0]:.3f}–{p['i0_T_factor_band'][1]:.3f}")
    chk('provenance 가 "열화율 아님" 을 명시', 'NOT_a_degradation_rate' in p
        and '날조' in p['NOT_a_degradation_rate'])
    chk('provenance 가 미앵커 목록을 병기', 'degradation rate' in p['still_unanchored'])
    chk('T 미지정이면 provenance 는 None (기본 산출물 불변)', provenance() is None)
    # ★[H3] (2026-07-30 재검증): docstring 은 고쳤는데 **기계가 읽는 dict** 는 여전히
    #   "LNO 코팅계 T-스윕은 논문에 없음" 을 npz 로 내보냈다 — 같은 dict 의 anchor_points 옆에서.
    #   문자열을 읽는 테스트가 하나도 없어서 못 잡았다.  이제 전 문자열을 훑는다.
    _all_str = ' '.join(str(v) for v in p.values())
    chk('★[H3] provenance 어디에도 "논문에 없음" 류 거짓 진술이 없다',
        '논문에 없음' not in _all_str and '스윕은 논문에' not in _all_str)
    chk('★[H3] provenance 가 코팅계 반증 사실을 **기계판독 가능**하게 싣는다',
        p.get('transfer_assumption_refuted_for_coated') is True
        and p.get('coated_counter_anchor_T_C_Rct') == [list(x) for x in RCT_T_ANCHOR_LNO]
        and '비-Arrhenius' in p['transfer_assumption'])
    chk('★[H3] provenance 와 step4 trust 문자열이 서로 모순되지 않는다 (같은 사실)',
        ('비-Arrhenius' in p['transfer_assumption']) and ('반증' in p['transfer_assumption']))

    # ★[L1] 독스트링의 헤드라인 배수가 함수와 일치하는가 (손계산 오탈자가 세 군데서 갈렸다)
    import re as _re
    _doc = __doc__ or ''
    _pairs = _re.findall(r'(\d+(?:\.\d+)?)\s*°C\s*×(\d+\.\d+)', _doc)
    _bad = [(t, v) for t, v in _pairs
            if abs(i0_temperature_factor(float(t)) - float(v)) > 5e-4]
    chk('★[L1] 독스트링 i0 배수표가 함수 계산과 일치 (손계산 오탈자 차단)',
        len(_pairs) >= 4 and not _bad,
        f'{len(_pairs)}점 검사' + (f', 불일치 {_bad}' if _bad else ''))
    chk('★[L1] 정정 전 값 5.5974 도 실제 (전인자 뺀) 계산과 일치',
        abs(math.exp(-(EA_RCT_EV / KB_EV) * (1.0 / 333.15 - 1.0 / 298.15)) - 5.5974) < 5e-4)

    # 7) T_REF 규약이 se_material 과 같은가
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import se_material
        chk('T_ref 규약이 se_material 과 동일 (25 °C)',
            abs(se_material.T_REF_C - T_REF_C) < 1e-12)
    except Exception as e:
        chk('se_material T_ref 대조', False, f'{type(e).__name__}: {e}')

    print('CAM-KINETICS SELFTEST', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--temp-c', type=float, default=None, help='i0 배수를 계산할 온도 [°C]')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    if a.temp_c is None:
        ea, r2 = _fit_ea(RCT_T_ANCHOR)
        print(f'kim2025 R_ct(T) 앵커 3점 → Eₐ = {ea:.4f} eV (R² = {r2:.5f})')
        print(f'  구간별: {EA_RCT_EV_INTERVALS[0]:.4f} / {EA_RCT_EV_INTERVALS[1]:.4f} eV')
        for t in (0, 25, 30, 45, 60, 80):
            print(f'  {t:3d} °C : i0 ×{i0_temperature_factor(t):6.3f}  '
                  f'R_ct ×{rct_temperature_factor(t):6.3f}')
    else:
        import json
        print(json.dumps(provenance(a.temp_c), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
