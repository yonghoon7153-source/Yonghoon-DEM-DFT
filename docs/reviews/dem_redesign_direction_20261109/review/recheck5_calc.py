#!/usr/bin/env python3
"""5 회차 짧은 확인 (메모 3.2 의 4 회차 고침만) 의 산술 · 독립.

규칙은 메모 본문 (§4 단계 3 · 4 · 부록 D-1 · D-2 · D-3) 의 문장에서 따로 옮겼다.
fix/arith5.py · review/calc_r4_recheck.py 는 import 하지 않는다 (출력은 대조에만 씀).
잡음 모형은 메모와 같은 가정: 단마다 독립 정규 · ln σ 팔 잡음 σ · Φ 팔 잡음 σ/10.
계산 · 시뮬레이션 런 0 건 (DEM · MPM 없음).  numpy 난수 표본 셈뿐이다.
"""
import math
import sys
import numpy as np

TAU = 0.02          # ln σ 격자 둔감 문턱 (τ = δ)
DELTA = 0.02        # ln σ 허용폭
TAU_P = 0.002       # Φ 팔
DELTA_P = 0.002
LN13, LN115 = math.log(1.3), math.log(1.15)
BAND3A = (math.log(0.7), math.log(1.4))
BAND3B = {'k1': (0.94, 1.00), 'k02': (0.83, 0.91)}
SIG_RANGE = (1.46, 4.23)   # 치우침 신호의 한 항 기대 범위 (메모의 등록 반올림값)


def hdr(t):
    print('\n== ' + t)


# ---------------------------------------------------------------- 팔 규칙
def arm_rule(X, delta, tau, rlo, rhi, mult=3.0):
    """X[..., 0..3] = (증인, 판정1, 판정2, 판정3).  증인은 nan 이면 없음.
    A: d1·d2 > 0 · rlo|d1| ≤ |d2| ≤ rhi|d1| → [min(xl, xl+3d2) − δ, max(...) + δ]
    B: A 아님 · |d1|,|d2| ≤ τ · U = {d1, d2} ∪ ({d0} · |d0| ≤ τ 일 때) 가
       '0 아닌 같은 부호' 가 아님 → xl ± (δ + 3 max_U |d|)   (본문 442 · D-1 997–1000)
    """
    d0 = X[..., 1] - X[..., 0]
    d1 = X[..., 2] - X[..., 1]
    d2 = X[..., 3] - X[..., 2]
    xl = X[..., 3]
    a = (d1 * d2 > 0) & (np.abs(d2) >= rlo * np.abs(d1)) & (np.abs(d2) <= rhi * np.abs(d1))
    use0 = np.isfinite(d0) & (np.abs(d0) <= tau)
    pos = (d1 > 0) & (d2 > 0) & (~use0 | (d0 > 0))
    neg = (d1 < 0) & (d2 < 0) & (~use0 | (d0 < 0))
    drift = pos | neg
    b = (~a) & (np.abs(d1) <= tau) & (np.abs(d2) <= tau) & (~drift)
    mU = np.maximum(np.abs(d1), np.abs(d2))
    mU = np.where(use0, np.maximum(mU, np.abs(np.nan_to_num(d0))), mU)
    lo = np.where(a, np.minimum(xl, xl + mult * d2) - delta, xl - (delta + mult * mU))
    hi = np.where(a, np.maximum(xl, xl + mult * d2) + delta, xl + (delta + mult * mU))
    conv = a | b
    lo = np.where(conv, lo, np.nan)
    hi = np.where(conv, hi, np.nan)
    return conv, a, b, lo, hi, d0, d1, d2


def rule_cur(X, delta=DELTA, tau=TAU):
    return arm_rule(X, delta, tau, 0.5, 1.1)


def rule_up(X, delta=DELTA, tau=TAU):
    return arm_rule(X, delta, tau, 0.29, 0.75)


def one(tup, rule=rule_cur, delta=DELTA, tau=TAU):
    X = np.array([tup], dtype=float)
    c, a, b, lo, hi, d0, d1, d2 = rule(X, delta, tau)
    kind = 'A' if a[0] else ('B' if b[0] else '미수렴')
    return kind, lo[0], hi[0], (d0[0], d1[0], d2[0])


# ---------------------------------------------------------------- §1 사다리 산술
def sec1():
    hdr('1. 사다리 산술 (MR4-02 · 08 · 본문 351 · 447 · 316)')
    f = lambda p: (1.5 ** p - 1) / (1 - 0.75 ** p)
    for p in (0.05, 0.1, 0.5, 0.72, 1.0, 2.0, 3.0, 3.08, 4.0):
        print(f'  p {p:4}: d0/d1 = (1.5^p − 1)/(1 − 0.75^p) = {f(p):.4f}')
    # 판정 간격 같음 (12·16·24) 의 d2/d1 와 남은 오차
    r_cur = lambda p: (24 ** -p - 16 ** -p) / (16 ** -p - 12 ** -p)
    rem = lambda p: 1 / (1.5 ** p - 1)
    lo = hi = None
    for p10 in range(1, 500):
        p = p10 / 100
        if hi is None and r_cur(p) <= 1.1:
            hi = p
        if lo is None and r_cur(p) <= 0.5:
            lo = p
    print(f'  지금 사다리 A 범위 0.5–1.1 ↔ p ≈ {hi:.2f}–{lo:.2f} (r(p) 단조 감소) · p {hi:.2f} 에서 남은 오차/|d2| = {rem(hi):.3f} (≤ 3)')
    # 등비 (16·24·36 · 24·36·54): d2/d1 = 1.5^-p
    pa = math.log(1 / 0.75) / math.log(1.5)
    pb = math.log(1 / 0.29) / math.log(1.5)
    print(f'  올린 사다리 (등비 1.5) 0.29–0.75 ↔ p {pa:.3f}–{pb:.3f} · 남은 오차/|d2| = r/(1−r) · r 0.75 → {0.75/0.25:.2f}')
    # 메모의 숫자에서 꺼지는가 (잡음 없음)
    def signal(d0, d1):
        a, b = sorted((SIG_RANGE[0] * d1, SIG_RANGE[1] * d1))
        dist = 0.0 if a <= d0 <= b else min(abs(d0 - a), abs(d0 - b))
        return (abs(d0) > TAU) and (dist > TAU), dist
    c = -0.04 * 16                              # BH01 16 셀 4 % 를 1 차 c/n 로
    ex = {
        'BH01 1 차 (c/16 = −0.04)': (c * (1 / 12 - 1 / 8), c * (1 / 16 - 1 / 12)),
        'U6 (a) 옮김 (d1 0.049 · 1 차)': (0.098, 0.049),
    }
    R = lambda n: math.log(1.10 + 3.36 / n)
    ex['판정문 반례 ln(1.10 + 3.36/n)'] = (R(12) - R(8), R(16) - R(12))
    for p in (0.5, 1.0, 2.0, 3.0):
        for dd in (0.01, 0.05):
            ex[f'한 항 p {p} · d1 {dd}'] = (f(p) * dd, dd)
    ex['p 0.1 표류 (P1-2: 0.664·n^-0.1)'] = (0.664 * (12 ** -0.1 - 8 ** -0.1), 0.664 * (16 ** -0.1 - 12 ** -0.1))
    for k, (d0, d1) in ex.items():
        on, dist = signal(d0, d1)
        print(f'  {k}: d0 {d0:+.4f} · d1 {d1:+.4f} · 비 {d0/d1:.3f} · 기대 범위까지 거리 {dist:.4f} → {"켜짐" if on else "꺼짐"}')
    # 반례: p 4 (빠른 수렴 · A 범위 밖) 는 켜진다
    d1 = 0.012
    on, dist = signal(f(4.0) * d1, d1)
    print(f'  [반례] 한 항 p 4.0 · d1 0.012 → d0 {f(4.0)*d1:+.4f} · 거리 {dist:.4f} → {"켜짐" if on else "꺼짐"} (메모 "한 항 p 0.5–3" 밖 · 참고)')


# ---------------------------------------------------------------- §2 계산량
def sec2():
    hdr('2. 계산량 (MR4-08 · 본문 316 · 591 · 506 · 부록 A 892)')
    cur = sum(n ** 3 for n in (8, 12, 16, 24))
    up = sum(n ** 3 for n in (12, 16, 24, 36))
    old = sum(n ** 3 for n in (8, 12, 16))
    print(f'  지금 {cur} · 올림 {up} · 3.1 {old} → 올림/지금 {up/cur:.4f} · 올림/3.1 {up/old:.3f} · 지금/3.1 {cur/old:.3f}')
    k3b = (60 * 6) / (48 * 2.3)
    lev = sum((n / 16) ** 3 for n in (8, 12, 16, 24))
    # 단계 3 판정 팔: 3a (S · F0.5 · F0) · 3b κ1 (S · F0.5 · F0) · 3b κ0.2 (A0.5 · F0.5 · F0) · 충전 셋 · 네 단
    judge = 9 * lev * (1 + 2 * k3b)
    r36 = (36 / 16) ** 3
    re3a = 3 * r36
    re3b = 3 * r36 * k3b
    print(f'  3b/3a 런 비 {k3b:.4f} · 단계 3 판정 계산량 (3a 16 셀 런 단위) {judge:.1f}')
    print(f'  다시 보기 (36 셀 · F(µ0) · 충전 셋): 3a 두 점 (한 런) {re3a/judge:.3f} · 3b 점 하나 {re3b/judge:.3f} · 넷 {(re3a+2*re3b)/judge:.3f}')
    # κ 0.2 의 무른 점이 κ 1 의 0.2 배라면 (가정 · 참고)
    judge2 = 9 * lev * (1 + k3b) + 9 * lev * k3b * 0.2
    print(f'  [참고 · κ 0.2 런이 κ 1 의 0.2 배라면] 3a {re3a/judge2:.3f} · 3b κ1 {re3b/judge2:.3f} · 넷 {(re3a+re3b+0.2*re3b)/judge2:.3f}')
    print(f'  54 셀 / 36 셀 = {(54/36)**3:.3f}')


# ---------------------------------------------------------------- §3 띠 문턱 · 한쪽 충전 (MR4-05)
def sec3():
    hdr('3. 띠 문턱 · 한쪽 충전 (MR4-01 · 05 · 본문 383 · 396 · 416 · 454)')
    w3a = BAND3A[1] - BAND3A[0]
    print(f'  3a 띠 폭 (ln) {w3a:.4f} → /4 {w3a/4:.4f} ({w3a/4/TAU:.2f} τ) · 3b κ1 폭 {1.00-0.94:.2f} → /4 {0.015} ({0.015/TAU_P:.1f} τ) · κ0.2 폭 {0.91-0.83:.2f} → /4 {0.08/4:.3f} ({0.02/TAU_P:.1f} τ)')
    nz = {0.90: 0.68, 0.95: 1.11}
    cap, theta = 2.4, 0.008
    for phi, s in nz.items():
        print(f'  Φ_d {phi}: NZ22 {s} MPa → 못 닿음 F/NZ22 ≥ {cap/s:.3f} · 잡음 F/NZ22 ≤ {theta/s:.4f}')
    # 3 회차 평균: 한 충전 [ln 2.162, ∞) · 둘 [ln .95, ln 1.05]
    lo = (math.log(cap / 1.11) + 2 * math.log(0.95)) / 3
    print(f'  3 회차 판 평균 아래 끝 = {lo:.4f} (띠 위 끝 ln 1.4 = {BAND3A[1]:.4f}) → {"걸침 → 미정" if lo < BAND3A[1] else "밖"}')
    # 잡음 충전을 3 회차 평균에 넣으면: 위 끝 평균
    hi = (math.log(theta / 0.68) + 2 * math.log(1.05)) / 3
    print(f'  [참고] 잡음 충전 하나 (0.90) + 둘 1.05: 3 회차 식의 평균 위 끝 {hi:.3f} < ln 0.7 {BAND3A[0]:.3f} → 3 회차 식으로도 이미 밖')


# ---------------------------------------------------------------- §4 숨은 느린 항 (MR4-04)
def lnR_interval(S_vals, F_vals=(0, 0, 0, 0)):
    kS, loS, hiS, dS = one(S_vals)
    kF, loF, hiF, dF = one(F_vals)
    return kS, kF, loS - hiF, hiS - loF, dS


def grade_same_fills(lo, hi):
    if lo >= LN115 and lo >= LN13:
        return '다름'
    if lo >= -LN13 and hi <= LN13 and lo >= -LN115 and hi <= LN115:
        return '같음'
    if hi <= -LN115 and hi <= -LN13:
        return '반대'
    return '중간'


def sec4():
    hdr('4. 숨은 느린 항의 크기 (MR4-04 · 본문 448 · 부록 A 888)')
    def S_of(L, A, B, p, sgn=-1):
        return [L + sgn * (A * n ** -p + B / n ** 2) for n in (8, 12, 16, 24)]
    cases = [
        ('A 0.3 B 1.5 · 참 R 1.30', S_of(math.log(1.3), 0.3, 1.5, 0.1)),
        ('A 1.0 B 5.0 · 참 R 2.00', S_of(math.log(2.0), 1.0, 5.0, 0.1)),
        ('A 1.6 B 8.0 · 참 R 2.94', S_of(math.log(2.94), 1.6, 8.0, 0.1)),
        ('위에서 A .95 B 4.75 · 참 R 0.769', S_of(-math.log(1.3), 0.95, 4.75, 0.1, sgn=+1)),
    ]
    for name, S in cases:
        kS, kF, lo, hi, d = lnR_interval(S)
        print(f'  {name}: S 팔 {kS} (비 {d[2]/d[1]:.3f}) · d1 {d[1]:+.4f} d2 {d[2]:+.4f} · ln R [{lo:.3f}, {hi:.3f}] → {grade_same_fills(lo, hi)}')
    # 해석 상한: 비 = 1.1 (A 의 위 끝) · 폭 3·d2 + 4δ = 2 ln 1.15 (같음의 한계) 에서
    for p in (0.1, 0.05, 0.02):
        a1 = 12 ** -p - 16 ** -p; a2 = 16 ** -p - 24 ** -p
        b1 = 1 / 144 - 1 / 256; b2 = 1 / 256 - 1 / 576
        k = (a2 - 1.1 * a1) / (1.1 * b1 - b2)          # B = k·A 이면 비 1.1
        d2u = a2 + k * b2                               # A 하나당 d2
        A = (2 * LN115 - 4 * DELTA) / 3 / d2u
        gap = A * 24 ** -p + k * A / 576                # 극한 − x(24)
        Lmax = LN115 + gap - 3 * A * d2u - 2 * DELTA
        print(f'  [해석 상한] p {p}: B = {k:.3f}·A · A ≤ {A:.3f} → 같음으로 인증되는 참 R 의 위 끝 = {math.exp(Lmax):.2f}')
    # 같음의 위 끝: S = L − A n^-p − B n^-2 (A, B > 0) 를 격자로 뒤져 같음이 되는 최대 L
    for p in (0.1, 0.05):
        best = (0, None)
        for A in np.linspace(0.05, 12.0, 240):
            for B in np.linspace(0.0, 60.0, 241):
                # L 을 이분: 같음 조건 hi ≤ ln 1.15 · lo ≥ −ln 1.15
                Sx = [-(A * n ** -p + B / n ** 2) for n in (8, 12, 16, 24)]
                kS, kF, lo0, hi0, d = lnR_interval(Sx)
                if kS != 'A':
                    continue
                # ln R 구간 = L + [lo0, hi0] → 같음이려면 L + hi0 ≤ ln1.15 그리고 L + lo0 ≥ −ln1.15
                Lmax = LN115 - hi0
                if Lmax + lo0 >= -LN115 and Lmax > best[0]:
                    best = (Lmax, (A, B, d[1], d[2]))
        L, (A, B, d1, d2) = best
        print(f'  p {p}: 같음으로 인증되는 참 R 의 위 끝 ≈ {math.exp(L):.2f} (A {A:.2f} · B {B:.1f} · d1 {d1:+.4f} · d2 {d2:+.4f} · 변화 {abs(d1)*100:.1f}–{abs(d2)*100:.1f} %) [격자 탐색 · 하한]')


# ---------------------------------------------------------------- §5 B 의 0 (MR4-07)
def sec5():
    hdr('5. B 의 0 (MR4-07 · 본문 82 · 442 · 458 · D-1 1005)')
    for t in [(0, 0, 0, 0), (0.010, 0.010, 0.012, 0.018), (0.010, 0.013, 0.013, 0.019), (0.0, 0.010, 0.010, 0.020)]:
        k, lo, hi, d = one(t)
        print(f'  {t}: d {tuple(round(v, 4) for v in d)} → {k} · 구간 [{lo:.3f}, {hi:.3f}]')
    # 1 회차 P1-2 반례에 8 셀 = 12 셀 (계단 · 포화) 을 넣음
    S = [0.664 * n ** -0.1 for n in (8, 12, 16, 24)]
    kS, kF, lo, hi, d = lnR_interval(S)
    print(f'  P1-2 원래 (q∞ 0 · 위에서): S {[round(v, 4) for v in S]} → S 팔 {kS} → ln R [{lo}, {hi}] → 중간 (막힘)')
    S2 = [S[1], S[1], S[2], S[3]]
    kS, kF, lo, hi, d = lnR_interval(S2)
    print(f'  [반례] 같은 표류 · x(8) = x(12) 만 바꿈: d {tuple(round(v, 4) for v in d)} → S 팔 {kS} → ln R [{lo:.4f}, {hi:.4f}] → {grade_same_fills(lo, hi)} (참 R 1.00 = 같음)')
    S3 = [S[1] + 0.0001, S[1], S[2], S[3]]
    kS, kF, lo, hi, d = lnR_interval(S3)
    g = grade_same_fills(lo, hi) if kS != '미수렴' else '중간 (미수렴)'
    print(f'  [대조] x(8) = x(12) + 0.0001 → d0 {d[0]:+.4f} (d1 · d2 와 같은 부호): S 팔 {kS} → {g}')
    S4 = [S[1] - 0.0001, S[1], S[2], S[3]]
    kS, kF, lo, hi, d = lnR_interval(S4)
    g = grade_same_fills(lo, hi) if kS != '미수렴' else '중간 (미수렴)'
    print(f'  [대조] x(8) = x(12) − 0.0001 → d0 {d[0]:+.4f} (반대 부호 · 3 회차 본문 풀이로도 B · ③ 의 알려진 한계): S 팔 {kS} → {g}')


# ---------------------------------------------------------------- §6 팔마다 표본 (U6 (b) 두 신호 · 수렴)
def arms(N, sig, rng, bias8=0.0, levels5=False):
    e = rng.normal(0.0, sig, size=(N, 5))     # 8 · 12 · 16 · 24 · 36
    e[:, 0] += bias8
    return e


def sec6(N=400000, seed=11):
    hdr(f'6. 팔마다 표본 (단마다 독립 정규 · {N} 표본) · U6 (b) 두 신호 · 수렴 비율')
    rng = np.random.default_rng(seed)

    def bias_sig(d0, d1):
        a = np.minimum(SIG_RANGE[0] * d1, SIG_RANGE[1] * d1)
        b = np.maximum(SIG_RANGE[0] * d1, SIG_RANGE[1] * d1)
        dist = np.where((d0 >= a) & (d0 <= b), 0.0, np.minimum(np.abs(d0 - a), np.abs(d0 - b)))
        return (np.abs(d0) > TAU) & (dist > TAU)

    for sig in (0.001, TAU / 8, TAU / 4, TAU / 2):
        e = arms(N, sig, rng)
        c, a, b, lo, hi, d0, d1, d2 = rule_cur(e[:, :4])
        cu, au, bu, *_ = rule_up(e[:, 1:5])
        nz = (~a) & (d1 * d2 < 0) & (np.maximum(np.abs(d1), np.abs(d2)) > TAU / 2)
        bs = bias_sig(d0, d1)
        old = np.abs(d0) > TAU
        # 증인 없음 (8 셀 없음 · 또는 τ 넘게 치우침)
        X = e[:, :4].copy(); X[:, 0] = np.nan
        cn, *_ = rule_cur(X)
        p_nz = nz.mean(); p_bs = bs.mean()
        print(f'  σ {sig:.4f}: 수렴 지금 {c.mean():.4f} · 올림 {cu.mean():.4f} · 증인 없음 {cn.mean():.4f} | 잡음 신호 팔마다 {p_nz:.4f} (팔 둘 {1-(1-p_nz)**2:.4f} · 점 둘 독립 {1-(1-p_nz)**4:.4f}) | 치우침 신호 팔마다 {p_bs:.4f} (팔 둘 {1-(1-p_bs)**2:.4f}) · 옛 |d0|>τ {old.mean():.4f}')
        if sig == TAU / 2:
            both = (nz & bs).mean()
            print(f'      τ/2 에서 두 신호가 한 팔에서 함께 켜짐 {both:.4f} · 치우침 켜진 팔 가운데 잡음 신호도 켜짐 {both/max(p_bs,1e-12):.3f}')
            # 팔 둘: 치우침 켜짐 ∧ 잡음 신호 꺼짐 (둘 다)
            e2 = arms(N, sig, rng)
            c2, a2, b2, lo2, hi2, d02, d12, d22 = rule_cur(e2[:, :4])
            nz2 = (~a2) & (d12 * d22 < 0) & (np.maximum(np.abs(d12), np.abs(d22)) > TAU / 2)
            bs2 = bias_sig(d02, d12)
            anyb = bs | bs2; anyn = nz | nz2
            print(f'      팔 둘 · 점 하나: 치우침만 {(anyb & ~anyn).mean():.4f} · 둘 다 {(anyb & anyn).mean():.4f} · 잡음만 {(~anyb & anyn).mean():.4f}')
    for b8 in (0.025, 0.05):
        e = arms(N, 0.001, rng, bias8=b8)
        c, a, b, lo, hi, d0, d1, d2 = rule_cur(e[:, :4])
        print(f'  σ 0.001 · x(8) + {b8}: 치우침 신호 팔마다 {bias_sig(d0, d1).mean():.4f} · 수렴 지금 {c.mean():.4f} · 옛 |d0|>τ {(np.abs(d0)>TAU).mean():.4f}')
    for b8 in (0.05,):
        for sig in (0.005, 0.01):
            e = arms(N, sig, rng, bias8=b8)
            c, a, b, lo, hi, d0, d1, d2 = rule_cur(e[:, :4])
            cu, *_ = rule_up(e[:, 1:5])
            print(f'  σ {sig} · x(8) + {b8}: 수렴 지금 {c.mean():.4f} · 올림 {cu.mean():.4f} · 치우침 신호 {bias_sig(d0, d1).mean():.4f}')


# ---------------------------------------------------------------- §7 갈림 표본 (가) · (나)
def grade_points(lo, hi):
    """lo, hi: (N, P, K) 충전 구간 (nan = 미수렴).  점 등급 코드: 0 중간 · 1 다름 · 2 같음 · 3 반대"""
    conv = np.all(np.isfinite(lo), axis=-1)
    lo_ = np.where(np.isfinite(lo), lo, 0.0); hi_ = np.where(np.isfinite(hi), hi, 0.0)
    d = conv & np.all(lo_ >= LN115, -1) & (lo_.mean(-1) >= LN13)
    s = conv & np.all(lo_ >= -LN13, -1) & np.all(hi_ <= LN13, -1) & (lo_.mean(-1) >= -LN115) & (hi_.mean(-1) <= LN115)
    o = conv & np.all(hi_ <= -LN115, -1) & (hi_.mean(-1) <= -LN13)
    g = np.zeros(conv.shape, dtype=np.int8)
    g[d] = 1; g[s] = 2; g[o] = 3
    return g


def test_grade(g):
    """g: (N, 3 점) → 0 중간 · 1 다름 · 2 같음 · 3 반대"""
    anyo = np.any(g == 3, -1)
    nd = np.sum(g == 1, -1)
    alls = np.all(g == 2, -1)
    t = np.zeros(g.shape[0], dtype=np.int8)
    t[alls] = 2
    t[nd >= 2] = 1
    t[anyo] = 3
    return t


def band_points(lo, hi, band, width, d1, d2, conv):
    """lo, hi, d1, d2, conv: (N, P, K).  band = (lo, hi) per P (list).
    점 상태: 0 안 · 1 미정 · 2 밖 · 3 큰 변화"""
    big = (~conv) & (np.maximum(np.abs(d1), np.abs(d2)) > width[None, :, None])
    anybig = np.any(big, -1)
    anync = np.any(~conv, -1)
    lo_ = np.where(conv, lo, 0.0).mean(-1); hi_ = np.where(conv, hi, 0.0).mean(-1)
    blo = np.array([b[0] for b in band])[None, :]; bhi = np.array([b[1] for b in band])[None, :]
    inside = (lo_ >= blo) & (hi_ <= bhi)
    outside = (hi_ < blo) | (lo_ > bhi)
    st = np.ones(anync.shape, dtype=np.int8)      # 미정
    st[(~anync) & inside] = 0
    st[(~anync) & outside] = 2
    st[anybig] = 3
    return st


def band_verdict(st):
    v = np.zeros(st.shape[0], dtype=np.int8)           # 0 안
    v[np.any(st == 1, -1)] = 1                          # 미정
    v[np.any((st == 2) | (st == 3), -1)] = 2            # 밖
    return v


def simulate(N, sig, Rtrue, nfill=3, ladder='cur', bias8=0.0, seed=1, corr=False):
    rng = np.random.default_rng(seed)
    rule = rule_cur if ladder == 'cur' else rule_up
    sl = slice(0, 4) if ladder == 'cur' else slice(1, 5)
    # 판정 팔: 시험 2 · 점 3 · 충전 nfill · 팔 2 (S · F) · 단 5
    shape = (N, 2, 3, nfill, 2, 5)
    if corr:   # 같은 런의 점끼리 완전 상관
        e = rng.normal(0, sig, size=(N, 2, 1, nfill, 2, 5)).repeat(3, axis=2)
    else:
        e = rng.normal(0, sig, size=shape)
    e[..., 0] += bias8
    X = e.copy()
    X[..., 0, :] += math.log(Rtrue)          # S 팔
    c, a, b, lo, hi, d0, d1, d2 = rule(X[..., sl])
    loR = lo[..., 0] - hi[..., 1]
    hiR = hi[..., 0] - lo[..., 1]
    loR = np.where(c[..., 0] & c[..., 1], loR, np.nan)
    hiR = np.where(c[..., 0] & c[..., 1], hiR, np.nan)
    G = np.zeros(N, dtype=np.int8)
    tg = []
    for t in range(2):
        g = grade_points(loR[:, t], hiR[:, t])
        tg.append(test_grade(g))
    t0, t1 = tg
    G[:] = 0
    G[(t0 == 2) & (t1 == 2)] = 2
    G[(t0 == 1) | (t1 == 1)] = 1
    G[(t0 == 3) | (t1 == 3)] = 3
    # 띠 팔: 점 4 (3a .90 · .95 (ln) · 3b κ1 · κ0.2 (Φ)) · 충전 nfill · 단 5
    centers_ln = math.log(math.sqrt(0.7 * 1.4))
    if corr:
        e3a = rng.normal(0, sig, size=(N, 1, nfill, 5)).repeat(2, axis=1)
    else:
        e3a = rng.normal(0, sig, size=(N, 2, nfill, 5))
    e3b = rng.normal(0, sig / 10, size=(N, 2, nfill, 5))
    e3a[..., 0] += bias8; e3b[..., 0] += bias8 / 10
    X3a = e3a + centers_ln
    X3b = e3b + np.array([0.97, 0.87])[None, :, None, None]
    ca, aa, ba, loa, hia, d0a, d1a, d2a = rule(X3a[..., sl])
    cb, ab, bb, lob, hib, d0b, d1b, d2b = rule(X3b[..., sl], DELTA_P, TAU_P)
    sta = band_points(loa, hia, [BAND3A, BAND3A], np.array([(BAND3A[1]-BAND3A[0])/4]*2), d1a, d2a, ca)
    stb = band_points(lob, hib, [BAND3B['k1'], BAND3B['k02']], np.array([0.015, 0.02]), d1b, d2b, cb)
    band = band_verdict(np.concatenate([sta, stb], axis=1))
    # A 등급: F · A 팔 (Φ) · 참 Δφ 0
    eA = rng.normal(0, sig / 10, size=(N, nfill, 2, 5))
    eA[..., 0] += bias8 / 10
    cA, aA, bA, loA, hiA, *_ = rule(eA[..., sl], DELTA_P, TAU_P)
    convA = np.all(cA, axis=(-1, -2))
    lD = loA[..., 0] - hiA[..., 1]; hD = hiA[..., 0] - loA[..., 1]
    lD = np.where(np.isfinite(lD), lD, 0); hD = np.where(np.isfinite(hD), hD, 0)
    Aok = convA & (lD.mean(-1) >= -0.01) & (hD.mean(-1) <= 0.01) & np.all(lD >= -0.02, -1) & np.all(hD <= 0.02, -1)
    Ashort = convA & (lD.mean(-1) >= 0.02) & np.all(lD >= 0.01, -1)
    Aopp = convA & (hD.mean(-1) <= -0.02) & np.all(hD <= -0.01, -1)
    # 갈림
    out = np.full(N, 'ma', dtype=object)
    la = Aopp | (band == 2) | (G == 3)
    na = (~la) & (band == 0) & ((G == 1) | Ashort)
    ga = (~la) & (band == 0) & (G == 2) & Aok & ~Ashort
    return {
        '(가)': ga.mean(), '(나)': na.mean(), '(라)': la.mean(),
        'G 다름': (G == 1).mean(), '띠 안': (band == 0).mean(), '띠 미정': (band == 1).mean(),
    }


def sec7(N=100000):
    hdr(f'7. 갈림 표본 (판정 팔 36 · 띠 팔 12 · A 등급 팔 6 · 점마다 독립 · {N} 표본 · 참 같음 R 1 / 참 다름 R 1.5)')
    rows = [
        ('σ .001 지금', dict(sig=0.001)),
        ('σ .001 지금 · 런마다 상관', dict(sig=0.001, corr=True)),
        ('σ .005 지금', dict(sig=0.005)),
        ('σ .005 올림', dict(sig=0.005, ladder='up')),
        ('σ .005 충전 여섯', dict(sig=0.005, nfill=6)),
        ('σ .005 원점 m2 (σ/√2)', dict(sig=0.005 / math.sqrt(2))),
        ('σ .005 원점 m4 (σ/2)', dict(sig=0.0025)),
        ('σ .01 지금', dict(sig=0.01)),
        ('σ .01 올림', dict(sig=0.01, ladder='up')),
        ('σ .01 원점 m2', dict(sig=0.01 / math.sqrt(2))),
        ('σ .01 원점 m4', dict(sig=0.005)),
        ('σ .001 · 8 셀 +0.05 · 지금', dict(sig=0.001, bias8=0.05)),
        ('σ .001 · 8 셀 +0.05 · 올림', dict(sig=0.001, bias8=0.05, ladder='up')),
        ('σ .005 · 8 셀 +0.05 · 지금', dict(sig=0.005, bias8=0.05)),
        ('σ .005 · 8 셀 +0.05 · 올림', dict(sig=0.005, bias8=0.05, ladder='up')),
    ]
    for i, (name, kw) in enumerate(rows):
        r1 = simulate(N, Rtrue=1.0, seed=100 + i, **kw)
        r5 = simulate(N, Rtrue=1.5, seed=200 + i, **kw)
        print(f'  {name}: 참 같음 (가) {r1["(가)"]:.4f} · 거짓 (나) {r1["(나)"]:.4f} | 참 다름 (나) {r5["(나)"]:.4f} · 거짓 (가) {r5["(가)"]:.4f} · G 다름 {r5["G 다름"]:.3f} · 띠 안 {r5["띠 안"]:.3f} · 띠 미정 {r5["띠 미정"]:.3f} · (라) {r5["(라)"]:.4f}')


# ---------------------------------------------------------------- §8 띠 다시 보기 (MR4-01 · 단계 4 ⓪)
def relook(N, sig, true3a=(None, None), bias8=0.0, seed=7, corr=False, big_tau=False):
    """true3a = (F/NZ22 at .90, at .95) · None = 띠 가운데.  3b 는 띠 가운데.
    2D 띠 (지금 사다리) → 미정이면 미정이던 점만 36 셀을 더해 올린 규칙 (16 · 24 · 36 · 증인 12) 으로 다시 본다."""
    rng = np.random.default_rng(seed)
    cen = math.log(math.sqrt(0.7 * 1.4))
    t = np.array([cen if v is None else math.log(v) for v in true3a])
    if corr:
        e3a = rng.normal(0, sig, size=(N, 1, 3, 5)).repeat(2, axis=1)
    else:
        e3a = rng.normal(0, sig, size=(N, 2, 3, 5))
    e3a[..., 0] += bias8
    X3a = e3a + t[None, :, None, None]
    e3b = rng.normal(0, sig / 10, size=(N, 2, 3, 5)); e3b[..., 0] += bias8 / 10
    X3b = e3b + np.array([0.97, 0.87])[None, :, None, None]
    w3a = np.array([(BAND3A[1] - BAND3A[0]) / 4] * 2)
    w3b = np.array([0.015, 0.02])
    if big_tau:
        w3a = np.array([TAU] * 2); w3b = np.array([TAU_P] * 2)
    def status(rule, s4, s4b):
        ca, aa, ba, loa, hia, d0a, d1a, d2a = rule(X3a[..., s4])
        cb, ab, bb, lob, hib, d0b, d1b, d2b = rule(X3b[..., s4b], DELTA_P, TAU_P)
        sta = band_points(loa, hia, [BAND3A, BAND3A], w3a, d1a, d2a, ca)
        stb = band_points(lob, hib, [BAND3B['k1'], BAND3B['k02']], w3b, d1b, d2b, cb)
        return np.concatenate([sta, stb], axis=1)
    st0 = status(rule_cur, slice(0, 4), slice(0, 4))
    v0 = band_verdict(st0)
    st1 = status(rule_up, slice(1, 5), slice(1, 5))
    st_new = np.where(st0 == 1, st1, st0)        # 미정이던 점만 다시 본 값
    v1 = band_verdict(st_new)
    und = v0 == 1
    res = dict(
        안2D=(v0 == 0).mean(), 미정2D=und.mean(), 밖2D=(v0 == 2).mean(),
        다시안=((v1 == 0) & und).sum() / max(und.sum(), 1),
        다시미정=((v1 == 1) & und).sum() / max(und.sum(), 1),
        불합격=((v1 == 2) & und).sum() / max(und.sum(), 1),
        큰변화2D=np.any(st0 == 3, -1).mean(),
        다시점수=(st0 == 1).sum(-1)[und].mean() if und.any() else 0.0,
    )
    return res


def sec8(N=100000):
    hdr(f'8. 띠 다시 보기 (MR4-01 · 단계 4 ⓪ · 띠 점 넷 · 충전 셋 · {N} 표본)')
    for sig in (0.001, 0.005, 0.01):
        for corr in (False, True):
            r = relook(N, sig, corr=corr, seed=int(sig * 1e5) + corr)
            print(f'  참 띠 가운데 · σ {sig} · {"런마다 상관" if corr else "점마다 독립"}: 2D 안 {r["안2D"]:.3f} · 미정 {r["미정2D"]:.3f} · 밖 {r["밖2D"]:.4f} (큰 변화 {r["큰변화2D"]:.4f}) | 미정 가운데 다시 안 {r["다시안"]:.3f} · 다시 미정 {r["다시미정"]:.3f} · 불합격 {r["불합격"]:.4f} · 다시 본 점 평균 {r["다시점수"]:.2f} → 생산 재료 가능 {r["안2D"] + r["미정2D"]*r["다시안"]:.3f}')
    for corr in (False, True):
        r = relook(N, 0.001, bias8=0.05, corr=corr, seed=31 + corr)
        print(f'  참 띠 가운데 · σ 0.001 · 8 셀 +0.05 · {"런마다 상관" if corr else "점마다 독립"}: 2D 미정 {r["미정2D"]:.3f} | 다시 안 {r["다시안"]:.3f} · 다시 미정 {r["다시미정"]:.3f} · 불합격 {r["불합격"]:.4f}')
    for sig in (0.001, 0.005, 0.01):
        r = relook(N, sig, big_tau=True, seed=41 + int(sig * 1e4))
        print(f'  [대조] 큰 변화 문턱을 τ 로 두면 · σ {sig}: (라) 쪽 큰 변화 {r["큰변화2D"]:.4f}')
    cases = [((None, 1.45), 0.001), ((None, 1.60), 0.001), ((0.60, None), 0.001), ((None, 1.45), 0.005), ((None, 1.60), 0.005), ((0.60, None), 0.005), ((None, 1.38), 0.001), ((None, 1.41), 0.01)]
    for (t, sig) in cases:
        r = relook(N, sig, true3a=t, seed=51 + int(sig * 1e4) + int((t[1] or t[0]) * 100))
        print(f'  3a 참 F/NZ22 (.90, .95) = {t} · σ {sig}: 2D 밖 (라) {r["밖2D"]:.3f} · 미정 (마) {r["미정2D"]:.3f} · 안 {r["안2D"]:.4f} | 미정 가운데 불합격 {r["불합격"]:.3f} · 다시 미정 {r["다시미정"]:.3f} · 다시 안 (거짓 채택) {r["다시안"]:.4f}')


# ---------------------------------------------------------------- §9 (나) 의 위 끝 · 해석 곱
def sec9():
    hdr('9. (나) 의 위 끝 · 해석 곱 (MR4-09 · 본문 450)')
    for name, p in (('σ .001', 0.933), ('σ .005', 0.922), ('8 셀 치우침 · 증인 없음', 0.735)):
        pt = p ** 6
        tst = 3 * pt ** 2 * (1 - pt) + pt ** 3
        G = 1 - (1 - tst) ** 2
        band = p ** 12
        print(f'  {name}: 팔 {p} → 점 {pt:.3f} · 시험 다름 {tst:.3f} · G 다름 {G:.3f} · 띠 안 {band:.3f} · (나) ≈ {G*band:.4f} · (가) ≈ 팔 54 모두 {p**54:.4f}')
    print(f'  0.927 × 0.433 = {0.927*0.433:.4f} · 0.93 × 0.43 = {0.93*0.43:.4f}')
    print(f'  생산 재료 가능 σ .001: 0.43 + 0.57 × 0.67 = {0.43 + 0.57*0.67:.3f}')




# ---------------------------------------------------------------- §10 손 예 · 표류 받힘 (부록 A 887 · 893)
def sec10(N=400000, seed=5):
    hdr('10. 손 예 (부록 A 887) · p 0.1 표류의 받힘 · 놓침 (부록 A 893 · MR4-09)')
    w = (BAND3A[1] - BAND3A[0]) / 4
    def big(t):
        k, lo, hi, d = one(t)
        state = '수렴 ' + k if k != '미수렴' else ('큰 변화' if max(abs(d[1]), abs(d[2])) > w else '작은 변화 미수렴')
        return state, d
    f = lambda c, p: [c * n ** -p for n in (8, 12, 16, 24)]
    print('  ±0.1 단마다 (0, 0.1, −0.1, 0.1):', big((0.0, 0.1, -0.1, 0.1)))
    c05 = 0.2 / (16 ** -0.5 - 12 ** -0.5)
    print('  한 항 p 0.5 · |d1| 0.2:', big(tuple(f(c05, 0.5))))
    c01 = 0.05 / (16 ** -0.1 - 12 ** -0.1)
    print('  한 항 p 0.1 · |d1| 0.05:', big(tuple(f(c01, 0.1))))
    rng = np.random.default_rng(seed)
    sig = 0.001
    for k in (1, 4, 16):
        c = k * sig / (16 ** -0.1 - 24 ** -0.1)          # |d2| = kσ · 위에서 다가옴 (극한 0)
        base = np.array(f(c, 0.1))
        X = base[None, :] + rng.normal(0, sig, size=(N, 4))
        cv, a, b, lo, hi, *_ = rule_cur(X)
        miss = cv & ~((lo <= 0) & (hi >= 0))
        print(f'  p 0.1 표류 · 단 변화 {k}σ (σ {sig}): 받힘 {cv.mean():.3f} (A {a.mean():.3f} · B {b.mean():.3f}) · 받히고 극한 0 을 놓침 {miss.mean():.3f} (받힘 가운데 {miss.mean()/max(cv.mean(),1e-12):.2f}) · 24 셀 남은 오차 {base[3]:.3f}')



# ---------------------------------------------------------------- §11 채택 금지의 빈도 · 신호의 점 수 · 실제 치우침에서 두 신호
def sec11(N=200000, seed=77):
    hdr('11. "채택 금지" 의 빈도 (단계 4 ⓪) · 치우침 신호의 점 수 · 실제 치우침에서 두 신호가 함께 켜짐')
    for sig in (0.001, 0.005, 0.01):
        for corr in (False, True):
            r = relook(100000, sig, corr=corr, seed=900 + int(sig * 1e4) + corr)
            print(f'  참 띠 가운데 · σ {sig} · {"런마다 상관" if corr else "점마다 독립"}: 2D 띠 미정 {r["미정2D"]:.3f} × 다시 미정 {r["다시미정"]:.3f} = 채택 금지 {r["미정2D"]*r["다시미정"]:.3f} (F 대조를 열어도 다음 걸음이 F-보류와 같음)')
    rng = np.random.default_rng(seed)
    def sigs(e):
        c, a, b, lo, hi, d0, d1, d2 = rule_cur(e[:, :4])
        lo_ = np.minimum(SIG_RANGE[0] * d1, SIG_RANGE[1] * d1); hi_ = np.maximum(SIG_RANGE[0] * d1, SIG_RANGE[1] * d1)
        dist = np.where((d0 >= lo_) & (d0 <= hi_), 0.0, np.minimum(np.abs(d0 - lo_), np.abs(d0 - hi_)))
        bs = (np.abs(d0) > TAU) & (dist > TAU)
        nz = (~a) & (d1 * d2 < 0) & (np.maximum(np.abs(d1), np.abs(d2)) > TAU / 2)
        return bs, nz
    for sig, b8 in ((0.01, 0.0), (0.005, 0.05), (0.0075, 0.05)):
        B = []; Z = []
        for arm in range(6):          # 팔 둘 × 점 셋 (점끼리 독립)
            e = rng.normal(0, sig, size=(N, 5)); e[:, 0] += b8
            bs, nz = sigs(e); B.append(bs); Z.append(nz)
        B = np.array(B); Z = np.array(Z)
        b2 = B[:2].any(0); z2 = Z[:2].any(0); b6 = B.any(0); z6 = Z.any(0)
        print(f'  σ {sig} · 8 셀 +{b8}: 팔 둘 점 하나 → 치우침 {b2.mean():.3f} (그 가운데 잡음 신호도 {((b2 & z2).mean()/max(b2.mean(),1e-12)):.2f}) · 점 셋 (독립) → 치우침 {b6.mean():.3f} · 잡음 {z6.mean():.3f}')
    # 단 하나의 띠 점만 미정일 때 다시 안 (D-4⁗ 1191 의 0.67 대조)
    r_one = []
    rng = np.random.default_rng(3)
    N2 = 100000
    cen = math.log(math.sqrt(0.7 * 1.4))
    e3a = rng.normal(0, 0.001, size=(N2, 2, 3, 5)); X3a = e3a + cen
    e3b = rng.normal(0, 0.0001, size=(N2, 2, 3, 5)); X3b = e3b + np.array([0.97, 0.87])[None, :, None, None]
    def status(rule, s):
        ca, aa, ba, loa, hia, d0a, d1a, d2a = rule(X3a[..., s])
        cb, ab, bb, lob, hib, d0b, d1b, d2b = rule(X3b[..., s], DELTA_P, TAU_P)
        sta = band_points(loa, hia, [BAND3A, BAND3A], np.array([(BAND3A[1]-BAND3A[0])/4]*2), d1a, d2a, ca)
        stb = band_points(lob, hib, [BAND3B['k1'], BAND3B['k02']], np.array([0.015, 0.02]), d1b, d2b, cb)
        return np.concatenate([sta, stb], axis=1)
    st0 = status(rule_cur, slice(0, 4)); st1 = status(rule_up, slice(1, 5))
    one_und = (st0 == 1).sum(-1) == 1
    v1 = band_verdict(np.where(st0 == 1, st1, st0))
    print(f'  σ 0.001 · 미정인 띠 점이 하나뿐일 때 ({one_und.mean():.3f}): 다시 안 {(v1[one_und] == 0).mean():.3f} (D-4⁗ 1191 은 일반 조건부 값 0.67 을 씀)')


if __name__ == '__main__':
    sec1(); sec2(); sec3(); sec4(); sec5(); sec6(); sec9(); sec10(); sec8(); sec11(); sec7()
