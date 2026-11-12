# 내부 반박 리뷰 4 회차 재확인 지적의 고침용 손 산술 (계산 · 시뮬레이션 아님 · 결정 규칙의 산술과 그 규칙의 갈림 비율 셈뿐)
# 대상 규칙 = memo_v3_2.md 4 회차 고침 (§4 단계 2 U6 (b) · 단계 3 · 단계 4 F 대조 ⓪ · 부록 D-1 · D-2 · D-3)
# 규칙은 메모 문장 (D-1 · D-2) 에서 다시 옮겼다.  fix/arith4.py 를 import 하지 않는다 (그 출력과 대조만 한다).
#   팔규칙 (D-1 · 3 회차 = 4 회차 · 4 회차 MR4-07 은 문장만 맞춤):
#     A  d1*d2 > 0 and lo|d1| <= |d2| <= hi|d1|  -> [min(x3, x3+3 d2) - δ, max(...) + δ]   (지금 사다리 lo 0.5 hi 1.1 · 올린 사다리 0.29 0.75)
#     B  A 가 아니고 |d1| <= τ, |d2| <= τ, 쓰는 변화 (d1, d2 + |d0| <= τ 면 d0) 가 "모두 0 아닌 같은 부호" 가 아님
#        -> x3 ± (δ + 3 max|쓰는 변화|)
#   띠 (4 회차 MR4-01 · 05): 띠 팔 미수렴 가운데 "큰 변화" (판정 두 변화 가운데 하나가 그 띠 폭의 1/4 넘음 · 또는 단마다 상태가 다름) → (라)
#                           확인된 못닿음 · 잡음 충전 → 그 띠 점 밖 · 그 밖 미수렴 · 걸침 → 미정 → (마)
#   단계 4 F 대조 ⓪ (4 회차 MR4-01): 2D 띠 미정 이력이면 미정이던 띠 점만 한 단 올려 (16 · 24 · 36 · 증인 12) 한 번 다시 본다
#   U6 (b) (4 회차 MR4-02 · 03): 치우침 신호 = |d0| > τ 이고 d0 가 d1 × [r0(0.1) , r0(3.08)] 에서도 τ 넘게 떨어짐 · 잡음 신호는 3 회차 그대로
import math
import numpy as np

L13, L115 = math.log(1.3), math.log(1.15)
DEL = TAU = 0.02
DPHI = TPHI = 0.002
INF = float('inf')
RUNG = (8, 12, 16, 24, 36)
CAP3A = math.log(2.4)          # 3a 판독 응력 상한 6 σ_y (MPa)
TH3A = math.log(0.008)         # 3a 잡음 문턱 θ (MPa)
NZ095, NZ090 = 1.11, 0.68      # NZ22 경화 0 곡선 (MPa · 카드 §3.3)
BAND3A = (math.log(0.7), math.log(1.4))
BK1 = (0.94, 1.00)
BK02 = (0.83, 0.91)
W4 = {'3a': (BAND3A[1] - BAND3A[0]) / 4, 'k1': (BK1[1] - BK1[0]) / 4, 'k02': (BK02[1] - BK02[0]) / 4}


def ratio_p(p):
    return (1 - (2 / 3) ** p) / ((4 / 3) ** p - 1)


def r0_p(p):
    """한 항 c·n^(−p) 의 d0/d1 (8 → 12 간격 1/24 · 12 → 16 간격 1/48)"""
    return (1.5 ** p - 1) / (1 - 0.75 ** p)


def solve(f, target, a, b):
    for _ in range(200):
        m = (a + b) / 2
        if (f(m) - target) * (f(a) - target) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2


P_LO = solve(ratio_p, 1.1, 0.05, 2.0)      # A 의 위 끝 (변화 비 1.1)
P_HI = solve(ratio_p, 0.5, 1.0, 6.0)       # A 의 아래 끝 (변화 비 0.5)
R0_LO, R0_HI = r0_p(0.1), r0_p(P_HI)       # 8 셀 기대 범위 (겉보기 차수 0.1 – 3.08)


def arm(x, delta=DEL, tau=TAU, lo_r=0.5, hi_r=1.1, use_w=True):
    """한 팔 · x = (증인, 판정 셋) · 증인은 None 가능 → ('A'|'B'|None, lo, hi, d0, d1, d2)"""
    w, a, b, c = x
    d1, d2 = b - a, c - b
    d0 = None if w is None else a - w
    if d1 * d2 > 0 and lo_r * abs(d1) <= abs(d2) <= hi_r * abs(d1):
        e1, e2 = c, c + 3 * d2
        return 'A', min(e1, e2) - delta, max(e1, e2) + delta, d0, d1, d2
    if abs(d1) <= tau and abs(d2) <= tau:
        used = [d1, d2]
        if use_w and d0 is not None and abs(d0) <= tau:
            used.append(d0)
        same = all(d > 0 for d in used) or all(d < 0 for d in used)       # "모두 0 아닌 같은 부호"
        if not same:
            m = max(abs(d) for d in used)
            return 'B', c - delta - 3 * m, c + delta + 3 * m, d0, d1, d2
    return None, None, None, d0, d1, d2


def grade(ivs):
    los = [a for a, b in ivs]; his = [b for a, b in ivs]; n = len(ivs)
    if all(l >= L115 for l in los) and sum(los) / n >= L13:
        return '다름'
    if all(l >= -L13 and h <= L13 for l, h in ivs) and sum(los) / n >= -L115 and sum(his) / n <= L115:
        return '같음'
    if all(h <= -L115 for h in his) and sum(his) / n <= -L13:
        return '반대'
    return '중간'


def bias_new(d0, d1, tau=TAU):
    """4 회차 치우침 신호 · d0 가 잡음 꼴 기대 (0) 와 한 항 꼴 기대 d1 × [R0_LO, R0_HI] 어느 쪽에서도 τ 넘게 떨어짐"""
    if d0 is None:
        return False
    a, b = sorted((d1 * R0_LO, d1 * R0_HI))
    dist = 0.0 if a <= d0 <= b else min(abs(d0 - a), abs(d0 - b))
    return abs(d0) > tau and dist > tau


def bias_old(d0, tau=TAU):
    return d0 is not None and abs(d0) > tau


def lad(fn, rungs=(8, 12, 16, 24)):
    return tuple(fn(n) for n in rungs)


print(f'== 0. 8 셀 기대 범위 · 한 항 c·n^(−p) 이면 d0/d1 = (1.5^p − 1)/(1 − 0.75^p)')
print(f'  A 의 겉보기 차수 범위: 변화 비 1.1 ↔ p {P_LO:.3f} · 변화 비 0.5 ↔ p {P_HI:.3f}')
for p in (1e-4, 0.1, 0.5, P_LO, 1.0, 2.0, P_HI, 4.0):
    print(f'  p {p:.3f}: d2/d1 {ratio_p(p):.4f} · d0/d1 {r0_p(p):.4f}')
print(f'  4 회차 기대 범위 d0 ∈ d1 × [{R0_LO:.3f} , {R0_HI:.3f}] (p 0.1 – {P_HI:.2f} · 0.1 = 리포의 다른 양에서 본 가장 느린 겉보기 차수)')

print('\n== 1. MR4-02 · U6 (b) 치우침 신호 · 옛 (|d0| > τ) ↔ 4 회차 (두 기대 어느 쪽에서도 τ 넘게 떨어짐) · 메모 자신의 숫자')
cases = []
e16 = math.log(1.04); c1 = e16 * 16
cases.append(('BH01 3D 구 16 셀 약 4 % · 1 차 (U2 · 응력 오차로 옮긴 어림)', lad(lambda n: c1 / n)))
c2 = 0.049 / (1 / 12 - 1 / 16)
cases.append(('U6 (a) 허용 ΔΦ_m 0.005 → Δln σ 약 0.049 · 1 차', lad(lambda n: -c2 / n)))
cases.append(('판정문 반례 S = ln(1.10 + 3.36/n)', lad(lambda n: math.log(1.10 + 3.36 / n))))
for p in (0.5, 1.0, 2.0, 3.0):
    for d1t in (0.01, 0.02, 0.05):
        c = d1t / abs(16 ** -p - 12 ** -p)
        cases.append((f'한 항 p {p} · |d1| {d1t}', lad(lambda n, c=c, p=p: c * n ** -p)))
cases.append(('1 회차 P1-2 ① 0.664·n^(−0.1)', lad(lambda n: 0.664 * n ** -0.1)))
cases.append(('p 0.1 표류 · |d1| 0.05', lad(lambda n: (0.05 / abs(16 ** -0.1 - 12 ** -0.1)) * n ** -0.1)))
s = list(lad(lambda n: 0.30 * n ** -0.1)); s[0] = s[1] - 0.010
cases.append(('8 셀 구멍 예 (0.30·n^(−0.1) · x8 = x12 − 0.010)', tuple(s)))
s = [0.0, 0.0, 0.0, 0.0]; s[0] = 0.05
cases.append(('잡음 없는 팔에 8 셀 치우침 +0.05', tuple(s)))
s = [0.0, 0.0, 0.0, 0.0]; s[0] = 0.025
cases.append(('잡음 없는 팔에 8 셀 치우침 +0.025', tuple(s)))
for tag, x in cases:
    r = arm(x)
    d0, d1, d2 = r[3], r[4], r[5]
    print(f'  {tag}: d0 {d0:+.4f} · d1 {d1:+.4f} · d2 {d2:+.4f} · 팔 {r[0]} · d0/d1 {d0 / d1 if d1 else float("nan"):.3f} → 옛 {"켜짐" if bias_old(d0) else "꺼짐"} · 4 회차 {"켜짐" if bias_new(d0, d1) else "꺼짐"}')

rng = np.random.default_rng(5041112)


def arm_vec(x, delta, tau, lo_r=0.5, hi_r=1.1):
    """x[..., 4] = (증인, 판정 셋) · NaN 증인 허용 → conv, lo, hi, isA, d0, d1, d2"""
    d0 = x[..., 1] - x[..., 0]; d1 = x[..., 2] - x[..., 1]; d2 = x[..., 3] - x[..., 2]
    isA = (d1 * d2 > 0) & (np.abs(d2) >= lo_r * np.abs(d1)) & (np.abs(d2) <= hi_r * np.abs(d1))
    a, b = x[..., 3], x[..., 3] + 3 * d2
    loA, hiA = np.minimum(a, b) - delta, np.maximum(a, b) + delta
    with np.errstate(invalid='ignore'):
        use0 = ~np.isnan(d0) & (np.abs(d0) <= tau)
        small = (np.abs(d1) <= tau) & (np.abs(d2) <= tau)
        same12 = ((d1 > 0) & (d2 > 0)) | ((d1 < 0) & (d2 < 0))
        same3 = same12 & (((d0 > 0) & (d1 > 0)) | ((d0 < 0) & (d1 < 0)))
        same = np.where(use0, same3, same12)
        m12 = np.maximum(np.abs(d1), np.abs(d2))
        m = np.where(use0, np.maximum(np.abs(d0), m12), m12)
    B = ~isA & small & ~same
    lo = np.where(isA, loA, x[..., 3] - delta - 3 * m)
    hi = np.where(isA, hiA, x[..., 3] + delta + 3 * m)
    return isA | B, lo, hi, isA, d0, d1, d2


def bias_vec(d0, d1, tau=TAU):
    a = np.minimum(d1 * R0_LO, d1 * R0_HI); b = np.maximum(d1 * R0_LO, d1 * R0_HI)
    dist = np.where((d0 >= a) & (d0 <= b), 0.0, np.minimum(np.abs(d0 - a), np.abs(d0 - b)))
    return (np.abs(d0) > tau) & (dist > tau)


def noise_vec(isA, d1, d2, tau=TAU):
    return ~isA & (d1 * d2 < 0) & (np.maximum(np.abs(d1), np.abs(d2)) > tau / 2)


NA = 400000
print('\n== 2. MR4-02 · 03 · U6 (b) 두 신호의 팔마다 켜짐 비율 (단마다 독립 정규 · 4 × 10⁵ 표본)')
print('  (팔 둘 = S · F(µ 0.5) · 점 하나면 "하나라도" = 1 − (1 − t)² · 점 둘 (0.84 · 0.90) 이 서로 독립이면 1 − (1 − t)⁴ · 같은 런이라 완전 상관이면 점 하나와 같다)')
for sig, b8 in ((0.001, 0.0), (0.0025, 0.0), (0.005, 0.0), (0.01, 0.0), (0.001, 0.025), (0.001, 0.05), (0.005, 0.05), (0.01, 0.05)):
    x = rng.normal(0, sig, (NA, 4)); x[:, 0] += b8
    conv, lo, hi, isA, d0, d1, d2 = arm_vec(x, DEL, TAU)
    tb_old = (np.abs(d0) > TAU).mean(); tb = bias_vec(d0, d1).mean(); tn = noise_vec(isA, d1, d2).mean()
    tbn = (bias_vec(d0, d1) & ~noise_vec(isA, d1, d2)).mean()
    f2 = lambda t: 1 - (1 - t) ** 2
    f4 = lambda t: 1 - (1 - t) ** 4
    print(f'  잡음 σ {sig} (τ/{TAU / sig:.0f}) · 8 셀 치우침 {b8}: 치우침 옛 {tb_old:.4f} · 4 회차 {tb:.4f} (잡음 신호 없이 {tbn:.4f}) · 잡음 신호 {tn:.4f} '
          f'→ 팔 둘 · 점 하나: 치우침 {f2(tb):.3f} · 잡음 {f2(tn):.3f} / 점 둘 독립: 치우침 {f4(tb):.3f} · 잡음 {f4(tn):.3f}')
# 잘 수렴하는 A 팔 + 잡음 : 옛 촉발은 켜지고 4 회차는 꺼진다
for p, d1t in ((1.0, 0.0131), (1.0, 0.03), (2.0, 0.02)):
    c = d1t / abs(16 ** -p - 12 ** -p)
    base = np.array([c * n ** -p for n in (8, 12, 16, 24)])
    x = base + rng.normal(0, 0.001, (NA, 4))
    conv, lo, hi, isA, d0, d1, d2 = arm_vec(x, DEL, TAU)
    print(f'  한 항 p {p} · |d1| {d1t} + 잡음 0.001: 팔 A {isA.mean():.3f} · 옛 치우침 {(np.abs(d0) > TAU).mean():.3f} · 4 회차 치우침 {bias_vec(d0, d1).mean():.4f}')


# ---------------------------------------------------------------------------------------------------------------
# 단계 3 갈림 모의 (3 회차 fix/arith4.py §8 과 같은 잡음 모형 · 판정 팔 36 · 띠 팔 12 · A 등급 팔 6 · Φ 팔 잡음 = σ/10)
# 다섯 단 (8 · 12 · 16 · 24 · 36) 을 뽑아 둔다: 지금 사다리 = 앞 넷 · 올린 사다리 = 뒤 넷 (증인 12 · 판정 16 · 24 · 36)
# ---------------------------------------------------------------------------------------------------------------
def noise5(N, shape, sig, b8):
    e = rng.normal(0, sig, (N,) + shape + (5,))
    e[..., 0] += b8
    return e


def read(x5, delta, tau, ladder):
    if ladder == 'cur':
        return arm_vec(x5[..., 0:4], delta, tau, 0.5, 1.1)
    return arm_vec(x5[..., 1:5], delta, tau, 0.29, 0.75)


def band_point(x5, delta, tau, band, w4, ladder, rule):
    """띠 점 하나 · x5 (N, 충전 3, 5) → 상태 0 안 · 1 미정 · 2 밖 · 3 큰 변화 (4 회차만) · 그리고 미정의 까닭 (걸침 | 미수렴)"""
    conv, lo, hi, isA, d0, d1, d2 = read(x5, delta, tau, ladder)
    allc = conv.all(axis=-1)
    ml, mh = lo.mean(axis=-1), hi.mean(axis=-1)
    inn = allc & (ml >= band[0]) & (mh <= band[1])
    out = allc & ((ml > band[1]) | (mh < band[0]))
    st = np.where(inn, 0, np.where(out, 2, 1))
    if rule == 4:
        big = (~conv & (np.maximum(np.abs(d1), np.abs(d2)) > w4)).any(axis=-1)
        st = np.where(big, 3, st)
    why = np.where(st == 1, np.where(allc, 1, 2), 0)          # 1 걸침 · 2 미수렴
    return st, why


def combine_band(states):
    s = np.stack(states, axis=1)
    return np.where((s == 3).any(axis=1), 3, np.where((s == 2).any(axis=1), 2, np.where((s == 1).any(axis=1), 1, 0)))


def sim(N, sig, b8, corr, lnR, b3a=(0.0, 0.0), nfill=3, ladder='cur', rule=4, recheck=True):
    sigp, b8p = sig / 10, b8 / 10
    if corr:
        e = noise5(N, (2, 1, nfill, 2), sig, b8); e = np.broadcast_to(e, (N, 2, 3, nfill, 2, 5))
    else:
        e = noise5(N, (2, 3, nfill, 2), sig, b8)
    x = e.copy(); x[:, :, :, :, 0, :] += lnR
    conv, lo, hi = read(x, DEL, TAU, ladder)[:3]
    cS, cF = conv[..., 0], conv[..., 1]
    loR = lo[..., 0] - hi[..., 1]; hiR = hi[..., 0] - lo[..., 1]
    pc = (cS & cF).all(axis=3)
    dif = (loR >= L115).all(axis=3) & (loR.mean(axis=3) >= L13)
    same = ((loR >= -L13) & (hiR <= L13)).all(axis=3) & (loR.mean(axis=3) >= -L115) & (hiR.mean(axis=3) <= L115)
    opp = (hiR <= -L115).all(axis=3) & (hiR.mean(axis=3) <= -L13)
    g = np.where(~pc, 0, np.where(dif, 1, np.where(same, 2, np.where(opp, 3, 0))))
    t_opp = (g == 3).any(axis=2); t_dif = (g == 1).sum(axis=2) >= 2; t_same = (g == 2).all(axis=2)
    t = np.where(t_opp, 3, np.where(t_dif, 1, np.where(t_same, 2, 0)))
    G = np.where((t == 3).any(axis=1), 3, np.where((t == 1).any(axis=1), 1, np.where((t == 2).all(axis=1), 2, 0)))
    # 띠 (3a 점 둘 · 3b κ 1 · 3b κ 0.2 · 충전 셋)
    if corr:
        e3a = np.broadcast_to(noise5(N, (1, nfill), sig, b8), (N, 2, nfill, 5))
    else:
        e3a = noise5(N, (2, nfill), sig, b8)
    x3a = e3a + np.array(b3a)[None, :, None, None]
    xk1 = noise5(N, (nfill,), sigp, b8p) + 0.97
    xk02 = noise5(N, (nfill,), sigp, b8p) + 0.87
    s3a0, w3a0 = band_point(x3a[:, 0], DEL, TAU, BAND3A, W4['3a'], ladder, rule)
    s3a1, w3a1 = band_point(x3a[:, 1], DEL, TAU, BAND3A, W4['3a'], ladder, rule)
    sk1, wk1 = band_point(xk1, DPHI, TPHI, BK1, W4['k1'], ladder, rule)
    sk02, wk02 = band_point(xk02, DPHI, TPHI, BK02, W4['k02'], ladder, rule)
    pts = [s3a0, s3a1, sk1, sk02]
    whys = np.stack([w3a0, w3a1, wk1, wk02], axis=1)
    band = combine_band(pts)
    if rule == 3:
        band = np.where(band == 3, 1, band)
    # A 등급
    xF = noise5(N, (nfill,), sigp, b8p) + 0.88; xA = noise5(N, (nfill,), sigp, b8p) + 0.88
    cFa, lFa, hFa = read(xF, DPHI, TPHI, ladder)[:3]; cAa, lAa, hAa = read(xA, DPHI, TPHI, ladder)[:3]
    ac = (cFa & cAa).all(axis=1)
    dlo = lFa - hAa; dhi = hFa - lAa
    lack = ac & (dlo >= 0.01).all(axis=1) & (dlo.mean(axis=1) >= 0.02)
    enough = ac & ((dlo >= -0.02) & (dhi <= 0.02)).all(axis=1) & (dlo.mean(axis=1) >= -0.01) & (dhi.mean(axis=1) <= 0.01)
    aopp = ac & (dhi <= -0.01).all(axis=1) & (dhi.mean(axis=1) <= -0.02)
    Ag = np.where(aopp, 3, np.where(lack, 1, np.where(enough, 2, 0)))
    base = np.where(G == 1, '나', np.where(G == 2, '가', '마'))
    base = np.where(band == 1, '마', base)
    up = (band == 0) & (Ag == 1) & ((base == '가') | (base == '마'))
    base = np.where(up, '나', base)
    base = np.where((band == 0) & (base == '가') & (Ag == 0), '마', base)
    out = np.where((Ag == 3) | (band == 2) | (band == 3) | (G == 3), '라', base)
    res = {k: float((out == k).mean()) for k in ('가', '나', '마', '라')}
    res['G같음'] = float((G == 2).mean()); res['G다름'] = float((G == 1).mean())
    for k, v in (('띠안', 0), ('띠미정', 1), ('띠밖', 2), ('띠큰변화', 3)):
        res[k] = float((band == v).mean())
    mj = band == 1
    res['미정걸침'] = float((mj & ((whys == 1).any(axis=1)) & ~((whys == 2).any(axis=1))).mean())
    res['미정미수렴'] = float((mj & (whys == 2).any(axis=1)).mean())
    res['(라)띠큰변화'] = float(((out == '라') & (band == 3) & ~((Ag == 3) | (G == 3))).mean())
    # 단계 4 F 대조 ⓪ · 띠 다시 보기 (미정이던 점만 한 단 올려 다시 읽음 · 한 번)
    if recheck and rule == 4 and ladder == 'cur':
        r3a0 = band_point(x3a[:, 0], DEL, TAU, BAND3A, W4['3a'], 'up', 4)[0]
        r3a1 = band_point(x3a[:, 1], DEL, TAU, BAND3A, W4['3a'], 'up', 4)[0]
        rk1 = band_point(xk1, DPHI, TPHI, BK1, W4['k1'], 'up', 4)[0]
        rk02 = band_point(xk02, DPHI, TPHI, BK02, W4['k02'], 'up', 4)[0]
        newpts = [np.where(o == 1, r, o) for o, r in zip(pts, (r3a0, r3a1, rk1, rk02))]
        nb = combine_band(newpts)
        m = band == 1
        nm = max(int(m.sum()), 1)
        res['재안'] = float((m & (nb == 0)).sum() / nm)
        res['재미정'] = float((m & (nb == 1)).sum() / nm)
        res['재불합격'] = float((m & ((nb == 2) | (nb == 3))).sum() / nm)
        res['재안_전체'] = float((m & (nb == 0)).mean())
    return res


def fmt(r, keys=('가', '나', '마', '라')):
    return ' '.join(f'({k}) {r[k]:.3f}' for k in keys)


NS = 100000
print('\n== 3. MR4-01 · 같은 표본에서 3 회차 띠 규칙 ↔ 4 회차 띠 규칙 (큰 변화 미수렴 → (라)) · 띠 미정의 까닭 · 단계 4 F 대조 ⓪ 의 띠 다시 보기')
print(f'  큰 변화 문턱 = 띠 폭의 1/4: 3a ln σ {W4["3a"]:.4f} (= {W4["3a"] / TAU:.1f} τ) · 3b κ 1 Φ_d {W4["k1"]:.4f} (= {W4["k1"] / TPHI:.1f} τ) · 3b κ 0.2 {W4["k02"]:.4f} (= {W4["k02"] / TPHI:.1f} τ)')
for sig, b8 in ((0.001, 0.0), (0.005, 0.0), (0.01, 0.0), (0.001, 0.05)):
    for corr in (False, True):
        for tag, lnR, b3 in (('참 같음 (R 1 · 띠 가운데)', 0.0, (0.0, 0.0)),
                             ('참 다름 (R 1.5 · 띠 가운데)', math.log(1.5), (0.0, 0.0)),
                             ('참 같음 · 띠 끝 안 (3a 0.95 의 F/NZ22 1.38)', 0.0, (0.0, math.log(1.38)))):
            st = rng.bit_generator.state
            r3 = sim(NS, sig, b8, corr, lnR, b3, rule=3, recheck=False)
            rng.bit_generator.state = st
            r4 = sim(NS, sig, b8, corr, lnR, b3, rule=4)
            print(f'  σ {sig} · 8 셀 {b8} · {"런마다 상관" if corr else "독립"} · {tag}')
            print(f'     3 회차 {fmt(r3)} | 4 회차 {fmt(r4)} | 띠 안 {r4["띠안"]:.3f} · 미정 {r4["띠미정"]:.3f} (걸침 {r4["미정걸침"]:.3f} · 미수렴 {r4["미정미수렴"]:.3f}) · 밖 {r4["띠밖"]:.3f} · 큰 변화 {r4["띠큰변화"]:.4f}')
            print(f'     띠 다시 보기 (띠 미정일 때 · 단계 4 F 대조 ⓪): 안 {r4["재안"]:.3f} · 다시 미정 {r4["재미정"]:.3f} · 불합격 {r4["재불합격"]:.4f} (전체 표본에서 미정 → 안 {r4["재안_전체"]:.3f})')

print('  [대조] 큰 변화 문턱을 띠 폭의 1/4 대신 τ (ln σ 0.02 · Φ_d 0.002) 로 두면 · 잡음만 있는 띠 팔 12 (ln σ 6 · Φ_d 6) 가운데 하나라도 "τ 넘는 변화로 미수렴" 일 비율:')
for sig in (0.001, 0.005, 0.01):
    xl = rng.normal(0, sig, (NA, 6, 4)); xp = rng.normal(0, sig / 10, (NA, 6, 4))
    cl, _, _, _, _, d1l, d2l = arm_vec(xl, DEL, TAU); cp, _, _, _, _, d1p, d2p = arm_vec(xp, DPHI, TPHI)
    bl = (~cl & (np.maximum(np.abs(d1l), np.abs(d2l)) > TAU)).any(axis=1)
    bp = (~cp & (np.maximum(np.abs(d1p), np.abs(d2p)) > TPHI)).any(axis=1)
    wl = (~cl & (np.maximum(np.abs(d1l), np.abs(d2l)) > W4['3a'])).any(axis=1)
    print(f'    σ {sig}: 문턱 τ → {(bl | bp).mean():.4f} · 문턱 띠 폭의 1/4 → {wl.mean():.4f} (ln σ 팔만 · Φ_d 팔은 위 모의에서 0)')

print('\n== 4. MR4-01 · 참 띠 밖인 F (구현이나 물리가 띠를 벗어남) 의 잡힘 · 거짓 채택')
for sig in (0.001, 0.005):
    for corr in (False, True):
        for tag, b3 in (('3a 0.95 의 F/NZ22 1.60 (뻣뻣 · 띠 위 끝 1.4 밖)', (0.0, math.log(1.60))),
                        ('3a 0.95 의 F/NZ22 1.45 (띠 위 끝 바로 밖)', (0.0, math.log(1.45))),
                        ('3a 0.90 의 F/NZ22 0.60 (무름)', (math.log(0.60), 0.0))):
            r4 = sim(NS, sig, 0.0, corr, 0.0, b3, rule=4)
            caught = r4['라']
            print(f'  σ {sig} · {"런마다 상관" if corr else "독립"} · {tag}: 2D (라) {caught:.3f} (띠 밖 {r4["띠밖"]:.3f}) · 2D 띠 미정 → (마) {r4["띠미정"]:.3f} '
                  f'→ 다시 보기 안 (거짓 채택) {r4["재안"]:.4f} · 다시 미정 {r4["재미정"]:.3f} · 불합격 {r4["재불합격"]:.3f}')

print('\n== 5. MR4-01 · 결함 꼴 (띠 팔이 큰 변화로 미수렴) 의 손 예 · 3a ln σ 띠 팔 · 큰 변화 문턱 0.173')
for tag, x in (('번갈아 ±0.1 (단마다 뒤집힘)', (0.0, 0.1, -0.1, 0.1)),
               ('한 항 p 0.5 · |d1| 0.2 (느린 큰 표류)', lad(lambda n: (0.2 / abs(16 ** -0.5 - 12 ** -0.5)) * n ** -0.5)),
               ('한 항 p 0.1 · |d1| 0.05 (작은 표류)', lad(lambda n: (0.05 / abs(16 ** -0.1 - 12 ** -0.1)) * n ** -0.1)),
               ('같은 부호 작은 변화 0.004 · 0.006 · 0.005 (잡음 꼴 단조)', (0.0, 0.004, 0.010, 0.015))):
    r = arm(x)
    big = r[0] is None and max(abs(r[4]), abs(r[5])) > W4['3a']
    print(f'  {tag}: 팔 {r[0]} · d1 {r[4]:+.4f} · d2 {r[5]:+.4f} → {"큰 변화 → (라)" if big else ("수렴" if r[0] else "작은 변화 미수렴 → 띠 미정 → (마)")}')

print('\n== 6. MR4-03 · 잡음 갈래의 처방 견주기 (판정 팔 · 갈림 비율 · 독립 · 10⁵ 표본 · 참 같음 R 1 / 참 다름 R 1.5)')
for sig in (0.005, 0.01):
    for tag, kw in (('지금 사다리 (등록된 (마) 처리 · 비용 1)', dict(ladder='cur')),
                    ('사다리 올림 (16 · 24 · 36 · 비용 3.29 배)', dict(ladder='up')),
                    ('원점 앙상블 m 2 (σ/√2 가정 · 비용 2 배)', dict(sig_scale=1 / math.sqrt(2))),
                    ('원점 앙상블 m 4 (σ/2 가정 · 비용 4 배)', dict(sig_scale=0.5)),
                    ('충전 여섯 (N 6 · 비용 2 배)', dict(nfill=6))):
        s = sig * kw.get('sig_scale', 1.0)
        lad_ = kw.get('ladder', 'cur'); nf = kw.get('nfill', 3)
        r_same = sim(NS, s, 0.0, False, 0.0, (0.0, 0.0), nfill=nf, ladder=lad_, rule=4, recheck=False)
        r_dif = sim(NS, s, 0.0, False, math.log(1.5), (0.0, 0.0), nfill=nf, ladder=lad_, rule=4, recheck=False)
        print(f'  σ {sig} · {tag}: 참 같음 {fmt(r_same)} · 참 다름 {fmt(r_dif)}')
x = rng.normal(0, 0.01, (NA, 5))
c_cur = arm_vec(x[:, 0:4], DEL, TAU, 0.5, 1.1)[0].mean(); c_up = arm_vec(x[:, 1:5], DEL, TAU, 0.29, 0.75)[0].mean()
x2 = rng.normal(0, 0.005, (NA, 5))
c_cur2 = arm_vec(x2[:, 0:4], DEL, TAU, 0.5, 1.1)[0].mean(); c_up2 = arm_vec(x2[:, 1:5], DEL, TAU, 0.29, 0.75)[0].mean()
print(f'  팔 수렴 비율 (잡음만): σ 0.005 지금 {c_cur2:.3f} · 올림 {c_up2:.3f} / σ 0.01 지금 {c_cur:.3f} · 올림 {c_up:.3f}')

print('\n== 7. MR4-03 · 치우침 갈래의 처방 (사다리 올림) 의 효과 · 8 셀 0.05 치우침 (독립 · 참 같음 / 참 다름)')
for sig in (0.001, 0.005):
    for lad_ in ('cur', 'up'):
        r_same = sim(NS, sig, 0.05, False, 0.0, (0.0, 0.0), ladder=lad_, rule=4, recheck=False)
        r_dif = sim(NS, sig, 0.05, False, math.log(1.5), (0.0, 0.0), ladder=lad_, rule=4, recheck=False)
        print(f'  σ {sig} · 8 셀 0.05 · {"지금 사다리" if lad_ == "cur" else "올린 사다리"}: 참 같음 {fmt(r_same)} · 참 다름 {fmt(r_dif)}')

print('\n== 8. MR4-04 · "최악 예" 는 최악이 아니다 · 숨은 느린 항 (A 로 받힘) 의 진폭을 키우면')
const0 = (0.0, 0.0, 0.0, 0.0)
F0 = arm(const0)


def lnR_iv(s):
    r = arm(s)
    if r[0] is None:
        return None
    return (r[1] - F0[2], r[2] - F0[1]), r


for lnR, A_, B_, sgn, p, tag in ((math.log(1.3), 0.3, 1.5, -1, 0.1, '메모의 예 (참 R 1.30 · 아래에서)'),
                                 (math.log(2.0), 1.0, 5.0, -1, 0.1, '참 R 2.00 · 아래에서'),
                                 (1.08, 1.6, 8.0, -1, 0.1, '참 R 2.94 · 아래에서'),
                                 (-L13, 0.95, 4.75, +1, 0.1, '참 R 0.769 (반대 문턱 · 끝 포함) · 위에서')):
    s = lad(lambda n: lnR + sgn * (A_ * n ** -p + B_ / n ** 2))
    iv, r = lnR_iv(s)
    d1, d2 = s[2] - s[1], s[3] - s[2]
    print(f'  {tag} · A {A_} B {B_} p {p}: 비 {d2 / d1:.3f} {r[0]} · ln R [{iv[0]:.4f}, {iv[1]:.4f}] → {grade([iv] * 3)} · 24 셀 남은 오차 {abs(lnR - s[3]):.3f} · 단 변화 {abs(s[1] - s[0]):.3f} · {abs(d1):.3f} · {abs(d2):.3f} (8 · 12 · 16 셀 변화)')
for p in (0.1, 0.05):
    best = None
    for A_ in np.linspace(0.05, 6, 1200):
        for kB in np.linspace(2.5, 8, 111):
            B_ = kB * A_
            s0 = lad(lambda n: -(A_ * n ** -p + B_ / n ** 2))
            r = arm(s0)
            if r[0] != 'A':
                continue
            lo, hi = r[1] - F0[2], r[2] - F0[1]
            lnR_max = L115 - hi
            if lnR_max + lo >= -L115 - 1e-12 and (best is None or lnR_max > best[0]):
                best = (lnR_max, A_, B_)
    print(f'  p {p}: 같음으로 인증되는 참 R 의 위 끝 ≈ {math.exp(best[0]):.2f} (A {best[1]:.2f} · B {best[2]:.2f}) [격자 탐색 · p → 0 이면 위 끝이 한없이 커진다]')

print('\n== 9. MR4-05 · 3a 띠 점의 한쪽 충전 (못닿음 · 잡음)')
nz = math.log(NZ095)
ivs = [(CAP3A - nz, INF), (math.log(0.95), math.log(1.05)), (math.log(0.95), math.log(1.05))]
ml = sum(a for a, b in ivs) / 3; mh = sum(b for a, b in ivs) / 3
st3 = '안' if (ml >= BAND3A[0] and mh <= BAND3A[1]) else ('밖' if (ml > BAND3A[1] or mh < BAND3A[0]) else '미정')
print(f'  Φ_d 0.95 · 한 충전이 2.4 MPa 안에서 못 닿음 (확인됨 · F/NZ22 ≥ {2.4 / NZ095:.2f} · ln 구간 [{CAP3A - nz:.3f}, +∞)) · 다른 둘 0.95–1.05:')
print(f'     3 회차 (평균에 넣음): 평균 아래 끝 {ml:.3f} · 위 끝 +∞ · 띠 [{BAND3A[0]:.3f}, {BAND3A[1]:.3f}] → {st3} → (마) · 2 회차 = 밖 → (라) · 4 회차 = 그 충전이 띠 위 끝보다 {math.exp(CAP3A - nz) / 1.4:.2f} 배 이상 → 밖 (뻣뻣) → (라)')
print(f'  Φ_d 0.90 · 한 충전이 잡음 (F(µ 0) ≤ θ 0.008 MPa · NZ22 {NZ090} MPa 의 {0.008 / NZ090:.4f} 배 이하 · ln 구간 (−∞, {TH3A - math.log(NZ090):.3f}]) → 4 회차 = 밖 (무름) → (라)')

print('\n== 10. MR4-06 · ⑤ 의 칼날 = 폭 문턱 2.2 %p (가상 값 · 산술만)')
for tag, srch in (('폭 2.1 %p (표지)', [13.0, 13.3, 13.6, 13.8, 14.1, 14.4, 14.7, 15.1]),
                  ('폭 2.3 %p (표지 없음)', [13.0, 13.3, 13.6, 13.9, 14.2, 14.5, 14.8, 15.3])):
    width = max(srch) - min(srch)
    steps = [srch[i + 1] - srch[i] for i in range(7)]
    print(f'  {tag}: 폭 {width:.1f} · 걸음마다 {min(steps):.1f}–{max(steps):.1f} %p (σ_y 20 배 · 여덟 점) · 판정 상자 0.03 GPa 에서 11.8 % (가상) → {"⑤ 보류" if width < 2.2 else "가로지름 · σ_y* 0.03 범위 끝 값 → (4-i)"}')

print('\n== 11. MR4-07 · d0 = 0 에서 D-1 (모두 0 아닌 같은 부호가 아니면 B) ↔ 3 회차 본문 풀이 ("같은 부호면 d0 가 τ 안이고 반대 부호일 때만 B")')
for x in ((0.010, 0.010, 0.012, 0.018), (0.0, 0.0, 0.0, 0.0), (0.010, 0.013, 0.013, 0.019)):
    r = arm(x)
    d0, d1, d2 = r[3], r[4], r[5]
    old_body = (d1 * d2 < 0) or (d1 * d2 > 0 and d0 is not None and abs(d0) <= TAU and d0 * d1 < 0)
    print(f'  x {x}: d0 {d0:+.3f} · d1 {d1:+.3f} · d2 {d2:+.3f} → D-1 {r[0]} · 3 회차 본문 풀이 {"B" if (old_body and r[0] != "A") else ("A" if r[0] == "A" else "아님")}')

print('\n== 12. MR4-08 · 사다리 전환과 띠 다시 보기의 계산량 (2D · 런 비용 ∝ 점 × 걸음 ∝ n³ · 3b 런은 3a 런의 (60 × 6)/(48 × 2.3) 배 · 부록 A 의 16 셀 규모)')
cur = sum(n ** 3 for n in (8, 12, 16, 24)); up = sum(n ** 3 for n in (12, 16, 24, 36)); base31 = sum(n ** 3 for n in (8, 12, 16))
print(f'  팔 하나의 사다리: 지금 {cur} · 올림 {up} → {up / cur:.3f} 배 (3.1 기본 {base31} 의 {up / base31:.2f} 배) · 런 수는 같다 (단 넷)')
k3b = (60 * 6) / (48 * 2.3)
u = lambda n: (n / 16) ** 3
stage3 = 9 * sum(u(n) for n in (8, 12, 16, 24)) + (9 * sum(u(n) for n in (8, 12, 16, 24)) + 9 * sum(u(n) for n in (8, 12, 16, 24)) + 3 * u(16)) * k3b
re_cur = {'3a (런 셋 · 두 점 같이)': 3 * u(36), '3b κ 1 (런 셋)': 3 * u(36) * k3b, '3b κ 0.2 (런 셋)': 3 * u(36) * k3b}
print(f'  3b 런 / 3a 런 = {k3b:.2f} · 단계 3 판정 · 띠 · A 팔 계산량 = 3a 16 셀 런 {stage3:.1f} 개 몫')
for k, v in re_cur.items():
    print(f'  띠 다시 보기 · {k}: 36 셀 → 3a 16 셀 런 {v:.1f} 개 몫 = 단계 3 의 {v / stage3:.3f} 배 (올린 사다리면 54 셀 · {(54 / 36) ** 3:.3f} 배 더)')
print(f'  띠 점 넷이 모두 미정이면 {sum(re_cur.values()) / stage3:.3f} 배 · 3a 만이면 {re_cur["3a (런 셋 · 두 점 같이)"] / stage3:.3f} 배')

print('\n== 13. MR4-09 · (나) 의 위 끝 = G 다름 × 띠 수렴 · 받힘 가운데 놓침 (p 0.1 표류 + 잡음)')
r = sim(NS, 0.001, 0.0, False, math.log(1.5), (0.0, 0.0), rule=4, recheck=False)
print(f'  σ 0.001 · 독립 · 참 다름: G 다름 {r["G다름"]:.3f} × 띠 안 {r["띠안"]:.3f} = {r["G다름"] * r["띠안"]:.3f} · 모의 (나) {r["나"]:.3f}')
p = 0.1; r24 = 24 ** -p; dd2 = abs(24 ** -p - 16 ** -p)
for sig in (0.001,):
    for step in (1, 4, 16):
        c = step * sig / dd2
        base = np.array([c * n ** -p for n in (8, 12, 16, 24)])
        x = base + rng.normal(0, sig, (NA, 4))
        conv, lo, hi = arm_vec(x, DEL, TAU)[:3]
        miss = conv & ((lo > 0) | (hi < 0))
        print(f'  σ {sig} · 단 변화 {step}σ (24 셀 남은 오차 {c * r24:.3f}): 받힘 {conv.mean():.3f} · 받혀서 극한 0 을 놓침 {miss.mean():.3f} (받힘 가운데 {miss.mean() / conv.mean():.2f})')
