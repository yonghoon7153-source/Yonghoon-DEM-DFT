#!/usr/bin/env python3
"""메모 3.2 · 5 회차 좁은 고침 (MR5-01 · 03 · 05 · 07) 의 산술 · 독립.

규칙은 메모 본문 (§4 단계 3 "해상도와 수치 오차" A · B · "F 정합" · 단계 2 U6 (b) · 단계 4 "F 대조" ⓪)
과 부록 D-1 · D-2 · D-3 의 문장에서 따로 옮겼다.
review5/recheck5_calc.py · fix/arith5.py 는 import 하지 않는다 (출력은 대조에만 쓴다).
잡음 모형은 메모와 같은 가정이다: 단마다 독립 정규 · ln σ 팔 잡음 σ · Φ 팔 잡음 σ/10.
계산 · 시뮬레이션 런 0 건 (DEM · MPM 없음).  numpy 난수 표본 셈뿐이다.
"""
import math
import numpy as np

TAU = DELTA = 0.02            # ln σ 팔 (τ = δ)
TAUP = DELTAP = 0.002         # Φ 팔
LN115, LN13 = math.log(1.15), math.log(1.3)
B3A = (math.log(0.7), math.log(1.4))              # 3a 띠 (F/NZ22 0.7–1.4 · ln)
W3A = (B3A[1] - B3A[0]) / 4                       # 큰 변화 문턱 = 띠 폭/4
B3B = [(0.94, 1.00), (0.83, 0.91)]                # 3b κ 1 · κ 0.2 (Φ_d)
W3B = [0.06 / 4, 0.08 / 4]
SIGLO, SIGHI = 1.46, 4.23                         # 치우침 신호의 한 항 기대 범위 (메모 등록 값)


def hdr(t):
    print('\n== ' + t)


# ------------------------------------------------------------ 팔 규칙 (본문 441 · 442 · D-1)
def arm(x, delta, tau, rlo, rhi):
    """x[..., 0:4] = (증인 · 판정 셋).  증인이 nan 이면 8 셀 (또는 증인) 런 없음."""
    w, a1, a2, a3 = x[..., 0], x[..., 1], x[..., 2], x[..., 3]
    with np.errstate(invalid='ignore'):
        d0 = a1 - w
        d1 = a2 - a1
        d2 = a3 - a2
        isA = (d1 * d2 > 0) & (np.abs(d2) >= rlo * np.abs(d1)) & (np.abs(d2) <= rhi * np.abs(d1))
        use0 = np.isfinite(d0) & (np.abs(d0) <= tau)
    allpos = (d1 > 0) & (d2 > 0) & (~use0 | (np.nan_to_num(d0) > 0))
    allneg = (d1 < 0) & (d2 < 0) & (~use0 | (np.nan_to_num(d0) < 0))
    isB = (~isA) & (np.abs(d1) <= tau) & (np.abs(d2) <= tau) & ~(allpos | allneg)
    mU = np.maximum(np.abs(d1), np.abs(d2))
    mU = np.where(use0, np.maximum(mU, np.abs(np.nan_to_num(d0))), mU)
    lo = np.where(isA, np.minimum(a3, a3 + 3 * d2) - delta, a3 - (delta + 3 * mU))
    hi = np.where(isA, np.maximum(a3, a3 + 3 * d2) + delta, a3 + (delta + 3 * mU))
    conv = isA | isB
    return dict(conv=conv, A=isA, B=isB, lo=np.where(conv, lo, np.nan), hi=np.where(conv, hi, np.nan),
                d0=d0, d1=d1, d2=d2)


def cur(x, delta=DELTA, tau=TAU):        # 지금 사다리 8 · 12 · 16 · 24
    return arm(x, delta, tau, 0.5, 1.1)


def up(x, delta=DELTA, tau=TAU):         # 올린 사다리 12 · 16 · 24 · 36 (등비)
    return arm(x, delta, tau, 0.29, 0.75)


def one(t, rule=cur):
    r = rule(np.array([t], dtype=float))
    k = 'A' if r['A'][0] else ('B' if r['B'][0] else '미수렴')
    return k, r['lo'][0], r['hi'][0], (r['d0'][0], r['d1'][0], r['d2'][0])


def grade_one(lo, hi):
    """충전 셋이 같은 구간일 때의 점 등급 (D-1 3)."""
    if lo >= LN115 and lo >= LN13:
        return '다름'
    if lo >= -LN13 and hi <= LN13 and lo >= -LN115 and hi <= LN115:
        return '같음'
    if hi <= -LN115 and hi <= -LN13:
        return '반대'
    return '중간'


# ------------------------------------------------------------ 띠 점 상태 (D-2 · 본문 454)
def band_point(r, band, width):
    """r = 팔 규칙 결과 (N, P, K) · 점 상태 0 안 · 1 미정 · 2 밖 · 3 큰 변화."""
    conv = r['conv']
    big = (~conv) & (np.maximum(np.abs(r['d1']), np.abs(r['d2'])) > np.asarray(width)[None, :, None])
    anybig = big.any(-1)
    anync = (~conv).any(-1)
    lo = np.where(conv, r['lo'], 0.0).mean(-1)
    hi = np.where(conv, r['hi'], 0.0).mean(-1)
    blo = np.array([b[0] for b in band])[None, :]
    bhi = np.array([b[1] for b in band])[None, :]
    st = np.ones(anync.shape, dtype=np.int8)
    st[(~anync) & (lo >= blo) & (hi <= bhi)] = 0
    st[(~anync) & ((hi < blo) | (lo > bhi))] = 2
    st[anybig] = 3
    return st


def band_verdict(st):
    v = np.zeros(st.shape[0], dtype=np.int8)
    v[(st == 1).any(-1)] = 1
    v[((st == 2) | (st == 3)).any(-1)] = 2
    return v


def band_sim(N, sig, seed, corr=False, bias8=0.0):
    """띠 점 넷 (3a 0.90 · 0.95 = ln σ 비 · 3b κ 1 · κ 0.2 = Φ_d) · 충전 셋 · 단 다섯 (8 · 12 · 16 · 24 · 36).
    참값 = 띠 가운데.  corr = 3a 두 점이 같은 런 (잡음 완전 상관)."""
    rng = np.random.default_rng(seed)
    if corr:
        e3a = np.repeat(rng.normal(0, sig, size=(N, 1, 3, 5)), 2, axis=1)
    else:
        e3a = rng.normal(0, sig, size=(N, 2, 3, 5))
    e3b = rng.normal(0, sig / 10, size=(N, 2, 3, 5))
    e3a[..., 0] += bias8
    e3b[..., 0] += bias8 / 10
    x3a = e3a + 0.5 * (B3A[0] + B3A[1])
    x3b = e3b + np.array([0.97, 0.87])[None, :, None, None]

    def status(rule, sl):
        sa = band_point(rule(x3a[..., sl]), [B3A, B3A], [W3A, W3A])
        sb = band_point(rule(x3b[..., sl], DELTAP, TAUP), B3B, W3B)
        return np.concatenate([sa, sb], axis=1)

    st0 = status(cur, slice(0, 4))
    st1 = status(up, slice(1, 5))
    v0 = band_verdict(st0)
    v1 = band_verdict(np.where(st0 == 1, st1, st0))    # 미정이던 점만 다시 본 값
    return st0, v0, v1


# ------------------------------------------------------------ §1 MR5-01
def sec1():
    hdr('1. MR5-01 · ⓪ 다시 미정 (4 회차 판 = 열되 "채택 금지") 의 다음 걸음과 빈도')
    # (a) 다음 걸음 대조: 4 회차 판 (열되 채택 금지) 대 (가) (열지 않음)
    nxt_hold = {'(4-ii)': 'S-연화', '(4-iii)': '1저자'}
    r4 = {
        'F-보류': {'(4-ii)': 'S-연화', '(4-iii)': '1저자'},
        'F-상자': {'(4-ii)': 'S-연화', '(4-iii)': '1저자'},
        'F-(i) · 채택 금지': {'(4-ii)': 'S-연화', '(4-iii)': '1저자'},
        'F-(ii) · 채택 금지': {'(4-ii)': 'S-연화', '(4-iii)': '1저자'},
        'F-(iii) · 채택 금지': {'(4-ii)': 'S-연화', '(4-iii)': '1저자'},
    }
    same = all(v == nxt_hold for v in r4.values())
    print('  4 회차 판 (메모 513–515 · D-3 1099–1103 을 그대로 옮김): 다섯 결과의 다음 걸음')
    for k, v in r4.items():
        print(f'    {k}: (4-ii) → {v["(4-ii)"]} · (4-iii) → {v["(4-iii)"]}')
    print(f'  "열지 않을 때" (507 · D-3 1091): (4-ii) → {nxt_hold["(4-ii)"]} · (4-iii) → {nxt_hold["(4-iii)"]}')
    print(f'  다섯 결과 모두 열지 않을 때와 같은가: {same} → (가) = 열지 않음 (다음 걸음 같음 · A′ · 3D 문 F 몫 · F 팔 둘 · 줄인 상자 S 짝 비용 0)')
    print('  옛 1110 행 "F-(i) · F-(ii) 의 다음 걸음만" = 틀린 전칭 (F-(iii) 의 (4-iii) 맥락도 (다) → 1저자로 바뀌었다 · MR5-02)')
    # (b) 빈도 (참 띠 가운데)
    for sig in (0.001, 0.005, 0.01):
        for corr in (False, True):
            st0, v0, v1 = band_sim(100000, sig, seed=6100 + int(sig * 1e4) + 7 * corr, corr=corr)
            und = v0 == 1
            p_und = und.mean()
            p_re_in = (v1[und] == 0).mean()
            p_re_und = (v1[und] == 1).mean()
            p_re_out = (v1[und] == 2).mean()
            print(f'  σ {sig} · {"런마다 상관" if corr else "점마다 독립"}: 2D 띠 미정 {p_und:.3f} → 다시 안 {p_re_in:.3f} · 다시 미정 {p_re_und:.3f} · 불합격 {p_re_out:.4f} '
                  f'→ ⓪ 다시 미정의 빈도 {p_und * p_re_und:.3f} (2D 안 {(v0 == 0).mean():.3f} · 생산 재료 가능 {(v0 == 0).mean() + p_und * p_re_in:.3f})')


# ------------------------------------------------------------ §2 MR5-03
def sec2():
    hdr('2. MR5-03 · B 의 0 이 x(8) = x(12) 에서 올 때 (본문 442 · 448 ① ③ · D-1 1005)')
    S = [0.664 * n ** -0.1 for n in (8, 12, 16, 24)]
    F = (0.0, 0.0, 0.0, 0.0)
    kF, loF, hiF, _ = one(F)

    def lnR(s):
        k, lo, hi, d = one(s)
        if k == '미수렴':
            return k, d, None
        return k, d, (lo - hiF, hi - loF)

    k, d, iv = lnR(S)
    print(f'  P1-2 원래 S = 0.664·n^(−0.1) (참 R 1.00): 단 {[round(v, 4) for v in S]} · d {tuple(round(float(v), 4) for v in d)} → S 팔 {k} → 중간 (미수렴)')
    for tag, s8 in (('x(8) = x(12)', S[1]), ('x(8) = x(12) + 0.0001', S[1] + 0.0001), ('x(8) = x(12) − 0.0001', S[1] - 0.0001)):
        s = [s8, S[1], S[2], S[3]]
        k, d, iv = lnR(s)
        g = '중간 (미수렴)' if iv is None else f'ln R [{iv[0]:.4f}, {iv[1]:.4f}] → {grade_one(*iv)}'
        print(f'  {tag}: d {tuple(round(float(v), 4) for v in d)} → S 팔 {k} · {g}')
    for t in [(0.010, 0.010, 0.012, 0.018), (0.0, 0.0, 0.0, 0.0)]:
        k, lo, hi, d = one(t)
        print(f'  {t}: d {tuple(round(float(v), 4) for v in d)} → {k} · 팔 구간 [{lo:.3f}, {hi:.3f}]')


# ------------------------------------------------------------ §3 MR5-05
def signals(x):
    r = cur(x[..., :4])
    d0, d1 = r['d0'], r['d1']
    a = np.minimum(SIGLO * d1, SIGHI * d1)
    b = np.maximum(SIGLO * d1, SIGHI * d1)
    dist = np.where((d0 >= a) & (d0 <= b), 0.0, np.minimum(np.abs(d0 - a), np.abs(d0 - b)))
    bias = (np.abs(d0) > TAU) & (dist > TAU)
    noise = (~r['A']) & (r['d1'] * r['d2'] < 0) & (np.maximum(np.abs(r['d1']), np.abs(r['d2'])) > TAU / 2)
    return bias, noise


def sec3(N=400000):
    hdr(f'3. MR5-05 · U6 (b) 의 두 신호가 함께 켜짐 (팔 둘 = S · F(µ 0.5) · 점마다 독립 · {N} 표본)')
    rng = np.random.default_rng(6300)
    for sig, b8, tag in ((TAU / 2, 0.0, '잡음만 τ/2'), (TAU / 4, 0.05, '8 셀 치우침 0.05 · 잡음 τ/4'),
                         (TAU / 4, 0.0, '잡음만 τ/4')):
        B, Z = [], []
        for _ in range(6):                                   # 팔 둘 × 점 셋
            e = rng.normal(0, sig, size=(N, 5))
            e[:, 0] += b8
            bs, nz = signals(e)
            B.append(bs); Z.append(nz)
        B = np.array(B); Z = np.array(Z)
        b1, z1 = B[:2].any(0), Z[:2].any(0)                  # 점 하나
        b3, z3 = B.any(0), Z.any(0)                          # 점 셋 (독립)
        print(f'  {tag}: 점 하나 → 치우침만 {(b1 & ~z1).mean():.3f} · 둘 다 {(b1 & z1).mean():.3f} · 잡음만 {(~b1 & z1).mean():.3f} '
              f'· 치우침 켜짐 {b1.mean():.3f} (그 가운데 잡음 신호도 {(b1 & z1).mean() / max(b1.mean(), 1e-12):.2f}) '
              f'| 점 셋 → 치우침 켜짐 {b3.mean():.3f} · 잡음 켜짐 {z3.mean():.3f} · 둘 다 {(b3 & z3).mean():.3f}')


# ------------------------------------------------------------ §4 MR5-07 (f)
def sec4():
    hdr('4. MR5-07 (f) · 부록 A 888 (A 1.6 B 8.0) · D-4⁗ 1191 (미정인 띠 점이 하나뿐)')
    p, A_, B_ = 0.1, 1.6, 8.0
    kF, loF, hiF, _ = one((0.0, 0.0, 0.0, 0.0))

    def iv(L):
        s = [L - (A_ * n ** -p + B_ / n ** 2) for n in (8, 12, 16, 24)]
        k, lo, hi, d = one(s)
        return k, (lo - hiF, hi - loF), d

    for L, tag in ((1.08, 'ln R 1.08 (fix/arith5.py 의 입력)'), (math.log(2.94), 'R 2.94 정확히'),
                   (math.log(2.947), 'R 2.947 (5 회차 리뷰가 적은 값)')):
        k, (lo, hi), d = iv(L)
        print(f'  {tag}: 참 R {math.exp(L):.5f} · S 팔 {k} (비 {d[2] / d[1]:.3f}) · ln R [{lo:.4f}, {hi:.4f}] → {grade_one(lo, hi)}')
    # 같음이 되는 참 R 의 범위 (이 A · B 에서)
    k, (lo0, hi0), d = iv(0.0)
    Lmax = LN115 - hi0
    Lmin = -LN115 - lo0
    print(f'  이 A · B 에서 같음이 되는 참 R: {math.exp(Lmin):.4f} ≤ R ≤ {math.exp(Lmax):.4f} (구간 폭 {hi0 - lo0:.4f} · 2 ln 1.15 = {2 * LN115:.4f})')
    # D-4⁗ 1191: 미정인 띠 점이 하나뿐일 때 다시 보기
    st0, v0, v1 = band_sim(200000, 0.001, seed=6400)
    und = v0 == 1
    one_und = und & ((st0 == 1).sum(-1) == 1)
    print(f'  σ 0.001 · 점마다 독립: 2D 띠 미정 {und.mean():.3f} (그 가운데 미정인 점이 하나뿐 {one_und.sum() / und.sum():.3f} · 전체의 {one_und.mean():.3f})')
    print(f'    미정 전체: 다시 안 {(v1[und] == 0).mean():.3f} · 다시 미정 {(v1[und] == 1).mean():.3f} · 불합격 {(v1[und] == 2).mean():.4f}')
    print(f'    미정인 점이 하나뿐: 다시 안 {(v1[one_und] == 0).mean():.3f} · 다시 미정 {(v1[one_und] == 1).mean():.3f} · 불합격 {(v1[one_und] == 2).mean():.4f}')


# ------------------------------------------------------------ §5 MR5-07 (b)
def sec5(N=400000):
    hdr(f'5. MR5-07 (b) · R 의 팔 (ln σ) 의 큰 변화 표지 문턱 ln σ 0.173 (3a 띠 팔과 같은 값) 이 잡음만으로 켜지는 비율 ({N} 표본)')
    rng = np.random.default_rng(6500)
    for sig in (TAU / 20, TAU / 4, TAU / 2, TAU):
        e = rng.normal(0, sig, size=(N, 4))
        r = cur(e)
        big = (~r['conv']) & (np.maximum(np.abs(r['d1']), np.abs(r['d2'])) > W3A)
        print(f'  잡음 σ {sig:.4f} ({sig / TAU:.2f} τ): 미수렴 {(~r["conv"]).mean():.4f} · 큰 변화 표지 {big.mean():.6f}')
    print(f'  문턱 {W3A:.4f} = {W3A / TAU:.2f} τ')


if __name__ == '__main__':
    sec1(); sec2(); sec3(); sec4(); sec5()
