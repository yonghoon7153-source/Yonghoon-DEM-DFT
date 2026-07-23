#!/usr/bin/env python3
"""R_int(N) 실측 곡선 shape 적합·검증 — STEP5 fade(N)의 ASSUMED shape(√N) 검증 게이트.

디지타이즈한 (N, R_int) 점(≥4 권장)을 받아 후보 shape을 적합하고 어느 모양이 맞는지 판정한다.
= b1_chem_fade.py 가 **가정**하는 √N(Park2023 확산제한 Wagner)을 실험 곡선으로 **확증/기각**하는 도구.

후보 shape:
  • sqrt   : R = R0 + k·√N            확산제한 Wagner CEI (b1_chem_fade 기본 = Park2023 코팅-앵커)
  • linear : R = R0 + k·N              일정속도 CEI 또는 접촉손실 누적
  • power  : R = R0 + k·N^p            p 적합 — 0.5≈√N / p>0.65=초선형(가속: 접촉손실이 화학 위에 얹힘
                                       = Park2023 bare 파라볼릭) / p<0.35=포화 기미
  • sat    : R = R0 + A·(1−e^(−N/τ))   포화 (접촉 안정화 / CEI self-limiting)

판정: 최소 AIC = best.  √N이 best와 ΔAIC≤2 이내면 "√N 지지(b1_chem_fade 기본 유효)".  power 적합 p가
√N(0.5)에서 크게 벗어나면 그 방향(가속/포화)이 실제 기전.  ⚠ n<4면 shape 구별 통계적 불가 — 경고만.

numpy-only (WSL 이식성): 선형항은 lstsq, 비선형(p,τ)은 그리드 서치 + lstsq 진폭.  ★적합은 magnitude가
아니라 **모양**을 본다(끝점 하나론 √N/선형 구별 불가 = b1_chem_fade 정직 경고를 데이터로 닫는 도구).

사용:
  python3 scripts/fit_rint_curve.py --csv rint_measured.csv          # 컬럼: N,R_int (헤더)
  python3 scripts/fit_rint_curve.py --points "0:18,100:47,250:64,500:83,1000:110"
  python3 scripts/fit_rint_curve.py --csv m.csv --out overlay.png --rint0 18 --label SBE  # b1 √N 오버레이
  python3 scripts/fit_rint_curve.py --selftest
"""
import argparse
import csv as _csv
import sys

import numpy as np


def _r2(R, sse):
    ss_tot = float(np.sum((R - R.mean()) ** 2))
    return 1.0 - sse / ss_tot if ss_tot > 1e-30 else 0.0


def _aic(sse, n, k):
    """작은 표본 보정 AICc = n·ln(SSE/n) + 2k + 2k(k+1)/(n−k−1).  n−k−1≤0이면 AIC로 폴백."""
    sse = max(sse, 1e-12)
    aic = n * np.log(sse / n) + 2 * k
    denom = n - k - 1
    if denom > 0:
        aic += 2.0 * k * (k + 1) / denom
    return float(aic)


def _lstsq_sse(basis, R):
    coef, *_ = np.linalg.lstsq(basis, R, rcond=None)
    sse = float(np.sum((R - basis @ coef) ** 2))
    return coef, sse


def fit_shapes(N, R):
    """4 후보 shape 적합 → {name: {params, sse, r2, aic, k_params}}, n."""
    N = np.asarray(N, float)
    R = np.asarray(R, float)
    n = len(N)
    out = {}
    ones = np.ones(n)

    c, sse = _lstsq_sse(np.column_stack([ones, np.sqrt(np.clip(N, 0, None))]), R)
    out['sqrt'] = {'params': {'R0': c[0], 'k': c[1]}, 'sse': sse, 'r2': _r2(R, sse),
                   'k_params': 2, 'aic': _aic(sse, n, 2)}

    c, sse = _lstsq_sse(np.column_stack([ones, N]), R)
    out['linear'] = {'params': {'R0': c[0], 'k': c[1]}, 'sse': sse, 'r2': _r2(R, sse),
                     'k_params': 2, 'aic': _aic(sse, n, 2)}

    Nsafe = np.clip(N, 0, None)
    best = None
    for p in np.linspace(0.2, 1.6, 141):
        c, sse = _lstsq_sse(np.column_stack([ones, np.power(Nsafe, p)]), R)
        if best is None or sse < best[1]:
            best = (c, sse, float(p))
    c, sse, p = best
    out['power'] = {'params': {'R0': c[0], 'k': c[1], 'p': p}, 'sse': sse, 'r2': _r2(R, sse),
                    'k_params': 3, 'aic': _aic(sse, n, 3)}

    span = max(float(N.max()), 1.0)
    best = None
    for tau in np.linspace(0.05 * span, 3.0 * span, 120):
        c, sse = _lstsq_sse(np.column_stack([ones, 1.0 - np.exp(-N / tau)]), R)
        if best is None or sse < best[1]:
            best = (c, sse, float(tau))
    c, sse, tau = best
    out['sat'] = {'params': {'R0': c[0], 'A': c[1], 'tau': tau}, 'sse': sse, 'r2': _r2(R, sse),
                  'k_params': 3, 'aic': _aic(sse, n, 3)}
    return out, n


def verdict(fits):
    best = min(fits, key=lambda k: fits[k]['aic'])
    daic_sqrt = fits['sqrt']['aic'] - fits[best]['aic']
    sqrt_ok = daic_sqrt <= 2.0
    p = fits['power']['params']['p']
    if abs(p - 0.5) < 0.15:
        pdesc = '≈√N (확산제한 Wagner)'
    elif p > 0.65:
        pdesc = '초선형 (가속 — 접촉손실이 화학 위에 얹힘 = Park2023 bare 파라볼릭)'
    elif p < 0.35:
        pdesc = '준-포화 (self-limiting 기미)'
    else:
        pdesc = '√N~선형 사이 (모호)'
    return best, sqrt_ok, daic_sqrt, p, pdesc


def _report(fits, n):
    best, sqrt_ok, daic_sqrt, p, pdesc = verdict(fits)
    print('=' * 84)
    print('R_int(N) shape 적합 — √N(b1_chem_fade 기본) 검증')
    print('-' * 84)
    print(f"  {'shape':>8} {'R²':>8} {'AICc':>10} {'params':>34}")
    for name in ('sqrt', 'linear', 'power', 'sat'):
        f = fits[name]
        pr = '  '.join(f'{k}={v:.4g}' for k, v in f['params'].items())
        star = ' ★best' if name == best else ''
        print(f"  {name:>8} {f['r2']:>8.4f} {f['aic']:>10.2f}   {pr:<32}{star}")
    print('-' * 84)
    if n < 4:
        print(f"  ⚠ n={n} < 4 — shape 구별 통계적으로 불가 (끝점 몇 개론 √N/선형 구별 못 함).  ≥4 N점 필요.")
    print(f"  best shape (min AICc): {best}")
    print(f"  √N ΔAICc vs best = {daic_sqrt:+.2f}  →  "
          f"{'√N 지지 (b1_chem_fade 기본 유효)' if sqrt_ok else '√N 기각 — shape 재검토 필요'}")
    print(f"  power 적합 지수 p = {p:.3f}  →  {pdesc}")
    print('=' * 84)


def _overlay_plot(N, R, fits, out_png, rint0=None, label='case'):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('  (matplotlib 없음 — 그림 생략)')
        return
    N = np.asarray(N, float)
    R = np.asarray(R, float)
    xs = np.linspace(0, max(N.max(), 1), 200)
    best, sqrt_ok, _, p, _ = verdict(fits)
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(N, R, 'ko', ms=6, label='measured (digitized)', zorder=5)
    sq = fits['sqrt']['params']
    ax.plot(xs, sq['R0'] + sq['k'] * np.sqrt(xs), '-', color='#e67e22', lw=1.8,
            label="sqrt-N fit (Park2023 Wagner)%s" % (' [best]' if best == 'sqrt' else ''))
    pw = fits['power']['params']
    ax.plot(xs, pw['R0'] + pw['k'] * np.power(xs, pw['p']), '--', color='#2980b9', lw=1.5,
            label='power fit p=%.2f%s' % (pw['p'], ' [best]' if best == 'power' else ''))
    li = fits['linear']['params']
    ax.plot(xs, li['R0'] + li['k'] * xs, ':', color='#7f8c9b', lw=1.4,
            label='linear fit%s' % (' [best]' if best == 'linear' else ''))
    ax.set_xlabel('cycle N')
    ax.set_ylabel('R_int (Ohm.cm2)')
    ax.set_title('R_int(N) shape validation [%s] — sqrt-N %s' %
                 (label, 'SUPPORTED' if sqrt_ok else 'REJECTED'),
                 fontsize=11, fontweight='bold')
    ax.legend(fontsize=8)
    ax.text(0.5, -0.16, 'best=%s . sqrt-N is the b1_chem_fade assumed shape (this closes it with data)' % best,
            transform=ax.transAxes, ha='center', fontsize=7.5, color='#888')
    fig.tight_layout()
    fig.savefig(out_png, dpi=130, bbox_inches='tight')
    print(f'  saved -> {out_png}')


def _parse_points(spec):
    N, R = [], []
    for tok in spec.split(','):
        a, b = tok.split(':')
        N.append(float(a))
        R.append(float(b))
    return N, R


def _read_csv(path):
    N, R = [], []
    with open(path, newline='') as f:
        rd = _csv.DictReader(f)
        cols = {c.lower().strip(): c for c in rd.fieldnames}
        nk = cols.get('n') or cols.get('cycle') or rd.fieldnames[0]
        rk = (cols.get('r_int') or cols.get('rint') or cols.get('r') or
              cols.get('r_int_ohm_cm2') or rd.fieldnames[1])
        for row in rd:
            N.append(float(row[nk]))
            R.append(float(row[rk]))
    return N, R


def _selftest():
    ok = tot = 0

    def chk(name, cond):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}")

    N = np.array([0, 50, 100, 250, 500, 1000], float)
    # 1) 순수 √N 데이터 → best in {sqrt,power}, √N 지지, r2≈1
    R = 18 + 2.9 * np.sqrt(N)
    fits, n = fit_shapes(N, R)
    best, sqrt_ok, daic, p, _ = verdict(fits)
    chk('√N 데이터 → √N 지지', sqrt_ok)
    chk('√N 데이터 → r2(sqrt)≈1', fits['sqrt']['r2'] > 0.999)
    chk('√N 데이터 → power p≈0.5', abs(p - 0.5) < 0.12)
    # 2) 선형 데이터 → best linear (or power p≈1), √N 기각 가능
    R = 18 + 0.09 * N
    fits, n = fit_shapes(N, R)
    best, sqrt_ok, daic, p, _ = verdict(fits)
    chk('선형 데이터 → power p≈1', p > 0.85)
    chk('선형 데이터 → best≠sqrt', best != 'sqrt')
    # 3) 초선형 p=0.8 (가속) 데이터 → power p≈0.8
    R = 18 + 0.5 * np.power(N, 0.8)
    fits, n = fit_shapes(N, R)
    _, _, _, p, pdesc = verdict(fits)
    chk('p=0.8 데이터 → 적합 p≈0.8', abs(p - 0.8) < 0.12)
    chk('p=0.8 → 초선형 라벨', '초선형' in pdesc)
    # 4) AICc가 power/sat의 여분 param을 벌점 (완전 동일적합서 sqrt<power)
    R = 18 + 2.9 * np.sqrt(N)
    fits, _ = fit_shapes(N, R)
    chk('AICc가 sqrt(2p) < power(3p) 벌점 (동일적합)', fits['sqrt']['aic'] <= fits['power']['aic'] + 1e-6)
    # 5) n<4 도 죽지 않음
    fits, n = fit_shapes([0, 100, 1000], [18, 47, 110])
    chk('n=3 실행 OK (경고 대상)', n == 3 and 'sqrt' in fits)
    print(f'  fit_rint_curve selftest: {ok}/{tot} PASS')
    return ok == tot


def main(argv):
    ap = argparse.ArgumentParser(description='R_int(N) shape 적합·√N 검증 (STEP5 게이트)')
    ap.add_argument('--csv', help='(N,R_int) CSV (헤더 N,R_int)')
    ap.add_argument('--points', help='"N:R,N:R,..." 인라인 점')
    ap.add_argument('--out', help='오버레이 PNG 경로')
    ap.add_argument('--rint0', type=float, help='(참고) pristine R_int — 제목/오버레이용')
    ap.add_argument('--label', default='case')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        sys.exit(0 if _selftest() else 1)
    if a.csv:
        N, R = _read_csv(a.csv)
    elif a.points:
        N, R = _parse_points(a.points)
    else:
        ap.error('--csv 또는 --points (또는 --selftest)')
    if len(N) < 2:
        ap.error('점이 2개 미만 — 적합 불가')
    fits, n = fit_shapes(N, R)
    _report(fits, n)
    if a.out:
        _overlay_plot(N, R, fits, a.out, rint0=a.rint0, label=a.label)


if __name__ == '__main__':
    main(sys.argv[1:])
