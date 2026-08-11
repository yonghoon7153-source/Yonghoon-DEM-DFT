#!/usr/bin/env python3
"""접촉면적 지수 −½ (Holm 협착) 를 **우리 자신의 STEP3 σ_e 필드**에서 뽑는다.

왜 (litdb `nam2026_primer_layer_dry_electrode_collector` §13 P-7):
  우리 σ_ionic 폼의 `cov^½` 와 σ_e 의 `√A_AM-AM` 은 **Holm 1967 협착저항
  R = ρ/(2a) ∝ A^(−½)** 에서 온 **가정**이다.  Nam 2026 은 완전히 독립적인 경로
  (AFM 실측 지형 위 연속체 Ohm 해) 로 **j_peak ∝ A^(−0.54)** 를 냈다 — 우리 지수의
  2 번째 독립 지지.  이 스크립트는 **3 번째**를 만든다: 우리 STEP3 복셀 필드에서
  입자별 전류밀도와 접촉면적을 뽑아 같은 지수를 재는 것.  새 실험도 GPU 도 필요 없다
  (기존 payload 만 있으면 된다).

물리 (지수가 −½ 인 이유):
  반지름 a 인 원형 접촉의 협착저항 R = ρ/(2a) ∝ A^(−½)  (A = πa²)
  고정 ΔV 에서 전류      I = ΔV/R ∝ A^(+½)
  접촉의 전류밀도        j = I/A  ∝ A^(−½)          ← 이것이 −0.5

★★ 이 도구의 정직 조항 (읽지 않고 결과를 인용하지 말 것) ★★
 (1) payload 의 `je` 는 입자 복셀에 대한 **평균** |J_z| proxy 이지 **peak** 이 아니다
     (step3_sigma.per_particle_current docstring).  Nam 2026 은 peak 을 썼다.
     평균은 협착 특이점에 덜 민감하므로 **|기울기| 가 작게 나오는 쪽으로 편향** →
     여기서 나온 값은 **하한**으로 읽어야 한다.  peak 판은 복셀 필드가 필요하다(킷 쪽).
 (2) 네트워크 해에서 **접촉마다 ΔV 가 다르다** — 회귀는 협착 지수와 전위 분포를 섞는다.
     Nam 2026 의 3-전극 집계판도 같은 성격의 혼입을 갖는다 (층이 다를 뿐).
 (3) `coverage` 는 DEM/MPM 기하 접촉면적(%)이고 **전기적** 접촉면적이 아니다.
     STEP3 는 sub-voxel 협착을 풀지 않는다 (mpm_webapp_payload 자신의 주석).
 (4) ★ **크기 교란이 실재한다**: A = (cov/100)·4πr² 이므로 log A = log cov + 2 log r.
     j 가 다른 이유로 r 에 의존하면 **순진한 회귀는 크기효과를 지수로 착각한다**.
     → 이 스크립트는 log r 을 **통제한 편회귀**를 정본으로 보고하고, 순진한 기울기는
       (문헌 3-점 집계와 같은 형태라는 이유로) 참고로만 병기한다.
       selftest 가 통제 없이는 실제로 편향되는 것을 **재현**한다.

사용:
    python3 scripts/holm_exponent_from_field.py --payload <mpm_payload.json> [--out out.json]
    python3 scripts/holm_exponent_from_field.py --selftest
"""
from __future__ import annotations

import argparse
import json
import math
import sys

import numpy as np

#: 비교 대상 — 둘 다 **다른 경로**에서 온 같은 지수.
HOLM_EXPONENT = -0.5          # Holm 1967 협착 (해석)
NAM2026_EXPONENT = -0.54      # Nam 2026 SI Fig S10 + 본문 j_peak (AFM 지형 + 연속체 Ohm)


def _ols(X, y):
    """최소제곱 → (beta, r2).  X 는 절편을 **포함하지 않은** 설계행렬."""
    A = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float('nan')
    return beta, r2


def _bootstrap_ci(X, y, idx_of_interest, n_boot=2000, seed=0, alpha=0.05):
    """계수의 부트스트랩 백분위 CI → (lo, hi).  n 이 작을 때 정규근사보다 정직하다."""
    rng = np.random.default_rng(seed)
    n = len(y)
    if n < 8:
        return float('nan'), float('nan')
    out = np.empty(n_boot)
    for b in range(n_boot):
        s = rng.integers(0, n, n)
        try:
            beta, _ = _ols(X[s], y[s])
            out[b] = beta[idx_of_interest]
        except np.linalg.LinAlgError:
            out[b] = np.nan
    out = out[np.isfinite(out)]
    if out.size < n_boot // 4:
        return float('nan'), float('nan')
    return float(np.quantile(out, alpha / 2)), float(np.quantile(out, 1 - alpha / 2))


def analyze(area, current, radius, *, n_boot=2000, seed=0, n_bins=5):
    """접촉면적 A · 전류밀도 j · 반지름 r → 지수 판정 dict.

    반환 키:
      naive_slope        log j ~ log A            (문헌 3-점 집계와 같은 형태; 크기 교란 있음)
      partial_slope      log j ~ log A + log r    ← **정본** (크기 통제)
      binned_slope       r-분위 안에서만 회귀한 뒤 가중평균 (비모수 통제)
    """
    area = np.asarray(area, float)
    current = np.asarray(current, float)
    radius = np.asarray(radius, float)
    ok = (np.isfinite(area) & np.isfinite(current) & np.isfinite(radius)
          & (area > 0) & (current > 0) & (radius > 0))
    n_drop = int((~ok).sum())
    area, current, radius = area[ok], current[ok], radius[ok]
    n = len(area)
    if n < 10:
        return {'status': 'insufficient', 'n': n, 'n_dropped': n_drop,
                'reason': f'유효 입자 {n}개 — 회귀에 부족하다 (최소 10)'}

    la, lj, lr = np.log(area), np.log(current / current.mean()), np.log(radius)

    beta_n, r2_n = _ols(la[:, None], lj)
    lo_n, hi_n = _bootstrap_ci(la[:, None], lj, 1, n_boot, seed)

    # ★ 정본: 크기를 통제한 편회귀.  A 와 r 이 (log 상) 완전공선이면 (cov 가 상수면)
    #   분리 불가 → 그 사실을 숨기지 말고 보고한다.
    X2 = np.column_stack([la, lr])
    cond = float(np.linalg.cond(np.column_stack([np.ones(n), X2])))
    beta_p, r2_p = _ols(X2, lj)
    lo_p, hi_p = _bootstrap_ci(X2, lj, 1, n_boot, seed)

    # 비모수 통제: r 분위 안에서만 회귀 (분위 안에서는 r 변동이 작다)
    edges = np.quantile(radius, np.linspace(0, 1, n_bins + 1))
    slopes, weights = [], []
    for i in range(n_bins):
        m = (radius >= edges[i]) & (radius <= edges[i + 1] if i == n_bins - 1
                                    else radius < edges[i + 1])
        if m.sum() < 8 or np.ptp(la[m]) < 1e-9:
            continue
        b, _ = _ols(la[m][:, None], lj[m])
        slopes.append(b[1]); weights.append(int(m.sum()))
    binned = (float(np.average(slopes, weights=weights)) if slopes else float('nan'))

    return {
        'status': 'ok', 'n': n, 'n_dropped': n_drop,
        'naive_slope': float(beta_n[1]), 'naive_r2': float(r2_n),
        'naive_ci95': [lo_n, hi_n],
        'partial_slope': float(beta_p[1]), 'partial_r2': float(r2_p),
        'partial_ci95': [lo_p, hi_p],
        'partial_logr_coef': float(beta_p[2]),
        'design_condition_number': cond,
        'collinearity_warning': bool(cond > 1e3),
        'binned_slope': binned, 'binned_n_bins_used': len(slopes),
        'vs_holm': float(beta_p[1] - HOLM_EXPONENT),
        'vs_nam2026': float(beta_p[1] - NAM2026_EXPONENT),
        'consistent_with_holm': bool(np.isfinite(lo_p) and lo_p <= HOLM_EXPONENT <= hi_p),
    }


def from_payload(payload, current_key='je'):
    """MPM webapp payload → (area_um2, current, radius_um, meta).

    coverage 는 **퍼센트**(deformed_coverage per_particle docstring) → A = (cov/100)·4πr².
    """
    parts = payload.get('particles') or []
    A, J, R, skipped = [], [], [], 0
    for p in parts:
        if not str(p.get('type', '')).upper().startswith('AM'):
            continue                                   # 전자망은 AM 상이다
        cov, r, j = p.get('coverage'), p.get('r'), p.get(current_key)
        if cov is None or r is None or j is None:
            skipped += 1
            continue
        A.append(float(cov) / 100.0 * 4.0 * math.pi * float(r) ** 2)
        J.append(float(j)); R.append(float(r))
    return (np.array(A), np.array(J), np.array(R),
            {'n_particles_total': len(parts), 'n_am_used': len(A),
             'n_am_missing_field': skipped, 'current_key': current_key})


CAVEATS = [
    "je 는 입자 복셀 **평균** |J_z| proxy 이지 peak 이 아니다 → |기울기| 가 작게 나오는 "
    "쪽으로 편향 = 여기 값은 **하한**.  peak 판은 복셀 필드(킷 쪽)가 필요하다.",
    "네트워크 해에서 접촉마다 ΔV 가 다르다 — 회귀는 협착 지수와 전위 분포를 섞는다.",
    "coverage 는 기하 접촉면적(%)이지 전기적 접촉면적이 아니다 (STEP3 는 sub-voxel "
    "협착을 풀지 않는다).",
    "log A = log cov + 2 log r 이므로 크기 교란이 실재한다 → **partial_slope 가 정본**, "
    "naive_slope 는 문헌 3-점 집계와 같은 형태라는 이유로만 병기한다.",
    "이것은 증명이 아니라 정합 신호다.  인용은 'consistent with the ½-power' 수준까지.",
]


def _report(res, meta):
    print('══ Holm 협착 지수 — 우리 STEP3 σ_e 필드 (litdb P-7) ══')
    print(f"  입자: 전체 {meta['n_particles_total']} · AM 사용 {meta['n_am_used']}"
          f" · 필드 결손 {meta['n_am_missing_field']}")
    if res['status'] != 'ok':
        print(f"  ⛔ {res['reason']}")
        return
    print(f"  유효 n = {res['n']} (버림 {res['n_dropped']})")
    print(f"  naive   log j ~ log A            기울기 {res['naive_slope']:+.3f}"
          f"  R² {res['naive_r2']:.3f}  CI95 [{res['naive_ci95'][0]:+.3f},"
          f" {res['naive_ci95'][1]:+.3f}]   ← 크기 교란 있음")
    print(f"  ★ partial log j ~ log A + log r  기울기 {res['partial_slope']:+.3f}"
          f"  R² {res['partial_r2']:.3f}  CI95 [{res['partial_ci95'][0]:+.3f},"
          f" {res['partial_ci95'][1]:+.3f}]   ← 정본")
    print(f"     (log r 계수 {res['partial_logr_coef']:+.3f}"
          f" · 설계 조건수 {res['design_condition_number']:.1f}"
          + ('  ⚠ 공선 — 분리 신뢰 낮음' if res['collinearity_warning'] else '') + ')')
    print(f"  binned  r-분위 통제 가중평균      기울기 {res['binned_slope']:+.3f}"
          f"  ({res['binned_n_bins_used']} 분위)")
    print(f"  vs Holm(−0.50) {res['vs_holm']:+.3f}   vs Nam2026(−0.54) {res['vs_nam2026']:+.3f}"
          f"   → Holm 이 CI 안: {'예' if res['consistent_with_holm'] else '아니오'}")
    print('  ⚠ 정직 조항:')
    for c in CAVEATS:
        print(f'    · {c}')


# ────────────────────────────────────────────────────────────────────────────
def _selftest():
    ok = fail = 0

    def chk(msg, cond):
        nonlocal ok, fail
        print(('  PASS  ' if cond else '  FAIL  ') + msg)
        ok, fail = ok + (1 if cond else 0), fail + (0 if cond else 1)

    rng = np.random.default_rng(7)
    n = 600
    r = rng.uniform(1.0, 6.0, n)                       # µm
    cov = rng.uniform(5.0, 60.0, n)                    # %
    A = cov / 100.0 * 4 * math.pi * r ** 2

    # ① 순수 −0.5, 크기효과 없음 → 두 회귀 모두 −0.5 를 찾아야 한다
    j = 3.0 * A ** (-0.5) * np.exp(rng.normal(0, 0.02, n))
    res = analyze(A, j, r, n_boot=300)
    chk('1) 합성 j∝A^(−0.5) — partial 이 −0.5 를 복원한다',
        abs(res['partial_slope'] + 0.5) < 0.02)
    chk('2) 크기효과가 없으면 naive 도 −0.5 (교란이 없을 때는 일치)',
        abs(res['naive_slope'] + 0.5) < 0.03)
    chk('3) Holm 이 CI 안에 든다', res['consistent_with_holm'] is True)
    chk('4) binned 통제도 같은 값', abs(res['binned_slope'] + 0.5) < 0.05)

    # ② ★ 크기효과가 섞이면 naive 는 **편향되고** partial 은 버틴다 (통제가 필요한 이유)
    j2 = 3.0 * A ** (-0.5) * r ** 0.8 * np.exp(rng.normal(0, 0.02, n))
    res2 = analyze(A, j2, r, n_boot=300)
    chk('5) ★ 크기효과 r^0.8 을 섞으면 naive 기울기가 실제로 편향된다 (결함 재현)',
        abs(res2['naive_slope'] + 0.5) > 0.10)
    chk('6) ★ partial 은 그 상황에서도 −0.5 를 지킨다 (크기 통제가 작동)',
        abs(res2['partial_slope'] + 0.5) < 0.03)
    chk('7) partial 이 크기 계수도 옳게 회수한다 (+0.8)',
        abs(res2['partial_logr_coef'] - 0.8) < 0.05)

    # ③ 널 — 지수가 없으면 0 근처, Holm 과 정합이라고 말하면 안 된다
    j3 = np.full(n, 2.0) * np.exp(rng.normal(0, 0.02, n))
    res3 = analyze(A, j3, r, n_boot=300)
    chk('8) ★ 널(지수 없음) 에서 −0.5 를 주장하지 않는다',
        abs(res3['partial_slope']) < 0.05 and res3['consistent_with_holm'] is False)

    # ④ 공선 — cov 가 상수면 log A 와 log r 이 완전공선 → 경고해야 한다
    A_col = 0.30 * 4 * math.pi * r ** 2
    res4 = analyze(A_col, 3.0 * A_col ** (-0.5), r, n_boot=200)
    chk('9) ★ cov 가 상수면 공선 경고를 낸다 (조용히 분리했다고 하지 않는다)',
        res4['collinearity_warning'] is True)

    # ⑤ 방어 — 비유한·비양수·부족
    A_bad = A.copy(); A_bad[:5] = np.nan; A_bad[5:10] = 0.0
    res5 = analyze(A_bad, j, r, n_boot=200)
    chk('10) NaN·0 면적을 버리고 개수를 보고한다',
        res5['n'] == n - 10 and res5['n_dropped'] == 10)
    chk('11) 표본이 너무 적으면 회귀를 하지 않고 사유를 남긴다',
        analyze(A[:5], j[:5], r[:5])['status'] == 'insufficient')

    # ⑥ payload 어댑터
    pay = {'particles': (
        [{'type': 'AM_P', 'r': float(r[i]), 'coverage': float(cov[i]), 'je': float(j[i])}
         for i in range(n)]
        + [{'type': 'SE', 'r': 0.5, 'coverage': 10.0, 'je': 1.0}] * 20
        + [{'type': 'AM_S', 'r': 2.0, 'coverage': 10.0}])}          # je 결손 1개
    A6, J6, R6, meta6 = from_payload(pay)
    chk('12) payload 어댑터가 AM 만 고른다 (SE 20개 제외)', meta6['n_am_used'] == n)
    chk('13) je 결손 입자를 세어 보고한다', meta6['n_am_missing_field'] == 1)
    chk('14) coverage 를 **퍼센트**로 해석한다 (A = cov/100·4πr²)',
        abs(A6[0] - cov[0] / 100.0 * 4 * math.pi * r[0] ** 2) < 1e-9)
    chk('15) 어댑터를 거쳐도 −0.5 가 나온다 (배선 확인)',
        abs(analyze(A6, J6, R6, n_boot=200)['partial_slope'] + 0.5) < 0.03)

    # ⑦ 정직 조항이 실제로 출력에 실린다
    chk('16) ★ 정직 조항이 5개 이상 명시돼 있다 (하한·ΔV·기하면적·크기교란·인용수준)',
        len(CAVEATS) >= 5 and any('하한' in c for c in CAVEATS)
        and any('ΔV' in c for c in CAVEATS))
    chk('17) 비교 상수가 문헌값 그대로다',
        HOLM_EXPONENT == -0.5 and NAM2026_EXPONENT == -0.54)

    print(f'\nholm_exponent_from_field selftest: {ok}/{ok + fail} PASS')
    return fail == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--payload', help='mpm webapp payload JSON')
    ap.add_argument('--current-key', default='je',
                    help="입자 전류 키 (je=전자, jb=BV, jrxn=반응).  기본 je")
    ap.add_argument('--out', help='판정 JSON 저장 경로')
    ap.add_argument('--n-boot', type=int, default=2000)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if not a.payload:
        ap.error('--payload 또는 --selftest 가 필요하다')
    with open(a.payload, encoding='utf-8') as f:
        payload = json.load(f)
    A, J, R, meta = from_payload(payload, a.current_key)
    res = analyze(A, J, R, n_boot=a.n_boot)
    _report(res, meta)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as f:
            json.dump({'result': res, 'meta': meta, 'caveats': CAVEATS,
                       'holm_exponent': HOLM_EXPONENT,
                       'nam2026_exponent': NAM2026_EXPONENT,
                       'source_payload': a.payload}, f, ensure_ascii=False, indent=2,
                      allow_nan=False)
        print(f'  → {a.out}')


if __name__ == '__main__':
    main()
