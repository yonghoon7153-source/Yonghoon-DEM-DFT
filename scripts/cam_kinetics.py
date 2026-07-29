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

`R_ct ∝ 1/i0` 이므로 이것이 곧 i0 의 온도 앵커다:

    i0(T) / i0(T_ref) = R_ct(T_ref) / R_ct(T) = exp[ −(Eₐ/k_B)·(1/T − 1/T_ref) ]

    25 °C ×1.000 · 30 °C ×1.311 · 45 °C ×2.803 · 60 °C ×5.598

★ 전이 가정 (라벨 필수) ★
─────────────────────────
- 앵커는 **72 wt% NCM, uncoated, post-formation** 한 조성이다.  Eₐ 가 조성·코팅·사이클 상태에
  무관하다고 **가정**한다.  같은 논문의 LNO 코팅 셀은 R_ct 가 ~20× 낮지만(22.4 vs 453.4 @62 wt%)
  T-스윕은 uncoated 만 있어서 코팅계 Eₐ 는 미지다.
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
    t, tr = float(T_C) + 273.15, float(t_ref_c) + 273.15
    if t <= 0.0:
        raise ValueError(f'i0_temperature_factor: T_C={T_C} 는 절대영도 이하')
    return math.exp(-(ea / KB_EV) * (1.0 / t - 1.0 / tr))


def rct_temperature_factor(T_C=None, ea_ev=None, t_ref_c=T_REF_C):
    """R_ct(T)/R_ct(T_ref) = 1 / i0 배수 (같은 앵커, 역수 — 보고용 편의)."""
    return 1.0 / i0_temperature_factor(T_C, ea_ev, t_ref_c)


def provenance(T_C=None, ea_ev=None):
    """감사 기록 dict.  T_C=None 이면 None (기본 런의 산출물은 이 키를 갖지 않는다)."""
    if T_C is None:
        return None
    ea = EA_RCT_EV if ea_ev is None else float(ea_ev)
    lo = i0_temperature_factor(T_C, EA_RCT_EV_INTERVALS[0])
    hi = i0_temperature_factor(T_C, EA_RCT_EV_INTERVALS[1])
    return {
        'T_C': float(T_C),
        'T_ref_C': float(T_REF_C),
        'Ea_Rct_eV': ea,
        'Ea_provenance': EA_RCT_PROVENANCE,
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
        'transfer_assumption': (
            '앵커는 72 wt% uncoated 한 조성 · post-formation.  Eₐ 가 조성/코팅/사이클 상태에 '
            '무관하다고 가정.  LNO 코팅계 T-스윕은 논문에 없음.'),
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
    chk('★ R_ct 는 그만큼 작아진다 (kim2025 30→60 에 4.28× 감소와 정합)',
        abs(rct_temperature_factor(60.0) * i0_temperature_factor(60.0) - 1.0) < 1e-12
        and abs((rct_temperature_factor(60.0) / rct_temperature_factor(30.0)) - (67.8 / 289.9))
        < 0.02, f'R_ct(60)/R_ct(30) 모델 '
                f'{rct_temperature_factor(60.0) / rct_temperature_factor(30.0):.4f} vs 앵커 '
                f'{67.8 / 289.9:.4f}')
    chk('저온에서는 i0 가 작아진다', i0_temperature_factor(0.0) < 1.0,
        f'0 °C: ×{i0_temperature_factor(0.0):.4f}')

    # 5) 앵커 3점을 실제로 재현하는가 (모델 ↔ 앵커 왕복)
    r30 = 289.9
    for t_c, r_meas in RCT_T_ANCHOR:
        r_pred = r30 * rct_temperature_factor(t_c) / rct_temperature_factor(30.0)
        chk(f'앵커 재현 {t_c:.0f} °C: R_ct {r_pred:.1f} vs 측정 {r_meas:.1f}',
            abs(r_pred / r_meas - 1.0) < 0.03, f'{100 * (r_pred / r_meas - 1):+.1f}%')

    # 6) 밴드 (구간 Eₐ 스프레드) — 단일값 보고 방지
    p = provenance(60.0)
    chk('provenance 가 Eₐ 밴드를 병기 (단일값 보고 방지)',
        p['i0_T_factor_band'][0] < p['i0_T_factor'] < p['i0_T_factor_band'][1],
        f"×{p['i0_T_factor_band'][0]:.3f}–{p['i0_T_factor_band'][1]:.3f}")
    chk('provenance 가 "열화율 아님" 을 명시', 'NOT_a_degradation_rate' in p
        and '날조' in p['NOT_a_degradation_rate'])
    chk('provenance 가 미앵커 목록을 병기', 'degradation rate' in p['still_unanchored'])
    chk('T 미지정이면 provenance 는 None (기본 산출물 불변)', provenance() is None)

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
