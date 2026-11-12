# 내부 반박 리뷰 3 회차 고침용 손 산술 (계산 · 시뮬레이션 아님 · 결정 규칙의 산술과 그 규칙의 수렴 · 갈림 비율 셈뿐)
# 대상 규칙 = memo_v3_2.md 3 회차 고침 (§4 단계 3 · 부록 D-1 · D-2)
#   팔규칙 3 회차 (MR3-03):
#     A  d1*d2 > 0 and 0.5|d1| <= |d2| <= 1.1|d1|  -> [min(x24, x24+3 d2) - δ, max(...) + δ]
#     B  A 가 아니고 |d1| <= τ, |d2| <= τ, 그리고 "쓰는 변화" 가 0 아닌 같은 부호가 아님
#        쓰는 변화 = d1, d2 (+ x8 이 있고 |d0| <= τ 면 d0)  -> x24 ± (δ + 3 max|쓰는 변화|)
#   팔 구간 (MR3-01): 값 = 팔규칙 · 잡음 = (-inf, ln θ] · 못닿음 = Φ_cap 팔규칙의 hi <= Φ_m 일 때만 [ln cap, +inf)
#   ln R_k = [lo(분자) - hi(분모), hi(분자) - lo(분모)]
#   띠 (MR3-02): 안 · 밖 · 미정 셋 · 미정 -> (마) (2 회차는 밖 -> (라))
import math
import numpy as np

L13, L115 = math.log(1.3), math.log(1.15)
DEL = TAU = 0.02
DPHI = TPHI = 0.002
INF = float('inf')
N4 = (8, 12, 16, 24)


def arm2(x, delta=DEL, tau=TAU):
    """2 회차 규칙 · x = [x8 (None 가능), x12, x16, x24]"""
    d1, d2 = x[2] - x[1], x[3] - x[2]
    if d1 * d2 > 0 and 0.5 * abs(d1) <= abs(d2) <= 1.1 * abs(d1):
        a, b = x[3], x[3] + 3 * d2
        return 'A', min(a, b) - delta, max(a, b) + delta
    if x[0] is not None:
        d0 = x[1] - x[0]
        ds = (d0, d1, d2)
        mono = all(d > 0 for d in ds) or all(d < 0 for d in ds)
        m = max(abs(d) for d in ds)
        if not mono and m <= tau:
            return 'B', x[3] - delta - 3 * m, x[3] + delta + 3 * m
    return None, None, None


def arm3(x, delta=DEL, tau=TAU):
    """3 회차 규칙 (MR3-03) · x = [x8 (None 가능), x12, x16, x24]"""
    d1, d2 = x[2] - x[1], x[3] - x[2]
    if d1 * d2 > 0 and 0.5 * abs(d1) <= abs(d2) <= 1.1 * abs(d1):
        a, b = x[3], x[3] + 3 * d2
        return 'A', min(a, b) - delta, max(a, b) + delta
    if abs(d1) <= tau and abs(d2) <= tau:
        used = [d1, d2]
        if x[0] is not None and abs(x[1] - x[0]) <= tau:
            used.append(x[1] - x[0])
        mono = all(d > 0 for d in used) or all(d < 0 for d in used)
        if not mono:
            m = max(abs(d) for d in used)
            return 'B', x[3] - delta - 3 * m, x[3] + delta + 3 * m
    return None, None, None


def grade(ivs):
    """ivs = [(lo, hi)] 충전마다 ln R 구간 (±inf 가능) · 충전 조건 먼저 · 평균은 뒤"""
    los = [a for a, b in ivs]; his = [b for a, b in ivs]; n = len(ivs)
    if all(l >= L115 for l in los) and sum(los) / n >= L13:
        return '다름'
    if all(l >= -L13 and h <= L13 for l, h in ivs) and sum(los) / n >= -L115 and sum(his) / n <= L115:
        return '같음'
    if all(h <= -L115 for h in his) and sum(his) / n <= -L13:
        return '반대'
    return '중간'


def lad(fn):
    return [fn(n) for n in N4]


def iv_diff(s, f):
    return (s[0] - f[1], s[1] - f[0])


print('== 0. 3 회차 B 는 |d0| ≤ τ 이면 2 회차 B 와 같다 (옛 반례 숫자 그대로) · 다르면 d0 를 크기 · 부호 · 구간 어디에도 쓰지 않는다')
cases = {
    'P1-2 ① 위에서 (0.664 n^-0.1)': lad(lambda n: 0.664 * n ** -0.1),
    'MR2-06 B 구멍 · 24 셀 잡음 (0.5 n^-0.1, 24 +0.016)': [0.5 * n ** -0.1 + (0.016 if n == 24 else 0) for n in N4],
    '8 셀 구멍 c 0.30 (x8 = x12 − 0.010)': None,
    '8 셀 구멍 c 0.50': None,
    '8 셀 구멍 c 0.60': None,
}
for c in (0.30, 0.50, 0.60):
    s = lad(lambda n: c * n ** -0.1); s[0] = s[1] - 0.010
    cases[f'8 셀 구멍 c {c:.2f}' if c != 0.30 else '8 셀 구멍 c 0.30 (x8 = x12 − 0.010)'] = s
const0 = [0.0] * 4
for tag, s in cases.items():
    r2, r3 = arm2(s), arm3(s)
    f = arm3(const0)
    iv2 = iv_diff(r2[1:], arm2(const0)[1:]) if r2[0] else None
    iv3 = iv_diff(r3[1:], f[1:]) if r3[0] else None
    fmt = lambda iv: f'[{iv[0]:.4f}, {iv[1]:.4f}] {grade([iv] * 3)}' if iv else '미수렴 · 중간'
    print(f'  {tag}: 2 회차 {r2[0]} {fmt(iv2)} · 3 회차 {r3[0]} {fmt(iv3)}')
s = lad(lambda n: 0.30 * n ** -0.1)
print(f'  8 셀 문구: 자연 x8 {s[0]:.4f} · x12 {s[1]:.4f} · 자연 d0 {s[1] - s[0]:+.4f} · 예는 x8 = x12 − 0.010 (자연값보다 {s[0] - (s[1] - 0.010):.4f} 낮춤)')

print('\n== 1. MR3-01 · 못 닿음의 정직한 한쪽 경계 (3a 판독 상한 2.4 MPa)')
cap = math.log(2.4)
fF = [math.log(v) for v in (1.85, 2.0, 2.15, 2.3)]
cF, loF, hiF = arm3(fF)
print(f'  ① F 팔 {cF} σ 구간 [{math.exp(loF):.3f}, {math.exp(hiF):.3f}] MPa · 분자 (S) 못닿음 인증되면 ln R_k ∈ [{cap - hiF:+.4f}, +∞) (R ≥ {math.exp(cap - hiF):.3f})')
iv_unr = (cap - hiF, INF)
print(f'     충전 셋이 모두 그 꼴: 2 회차 (+∞ 한 점) → 다름 · 3 회차 → {grade([iv_unr] * 3)}')
print(f'  ② 두 충전 [0.15, 0.25] + 셋째 +∞ (2 회차) → {grade([(0.15, 0.25), (0.15, 0.25), (INF, INF)])} · 셋째 정직한 경계 → {grade([(0.15, 0.25), (0.15, 0.25), iv_unr])}')
# 정보가 있는 못 닿음: F 가 상한보다 한참 아래
fF2 = [math.log(v) for v in (0.50, 0.53, 0.55, 0.57)]
c2, lo2, hi2 = arm3(fF2)
print(f'     F 가 낮은 경우 (0.53 · 0.55 · 0.57 MPa · {c2}) → ln R_k ≥ {cap - hi2:.3f} (R ≥ {math.exp(cap - hi2):.2f}) → 셋 다 그러면 {grade([(cap - hi2, INF)] * 3)}')
# ③ F 미수렴이면 중간
fN = [math.log(v) for v in (1.6, 2.2, 1.9, 2.35)]
print(f'  ③ F 미수렴 ({arm3(fN)[0]}) → 3 회차는 분자 못닿음 충전도 분모 팔규칙을 부른다 → 점 중간')
# ④ 상한에서의 Φ 추세
sphi = [0.934, 0.940, 0.944, 0.947]
cp, lp, hp = arm3(sphi, DPHI, TPHI)
print(f'  ④ S 상한 Φ_cap 팔 {cp} 구간 [{lp:.4f}, {hp:.4f}] · Φ_m 0.95 → 인증? {hp <= 0.95} → 아니면 그 충전 중간')
sphi2 = [0.930, 0.934, 0.936, 0.937]
cp2, lp2, hp2 = arm3(sphi2, DPHI, TPHI)
print(f'     인증되는 예 (0.930 · 0.934 · 0.936 · 0.937) {cp2} [{lp2:.4f}, {hp2:.4f}] → 인증? {hp2 <= 0.95}')
# 순서 1 (분모만 못 닿음 → 반대) 를 등급표로
sS = [math.log(v) for v in (0.95, 1.0, 1.03, 1.05)]
cs, los_, his_ = arm3(sS)
iv_d = (-INF, his_ - cap)
print(f'  분모 (F) 못닿음 · S {cs} σ 구간 [{math.exp(los_):.3f}, {math.exp(his_):.3f}] → ln R_k ≤ {his_ - cap:.3f}')
print(f'     충전 하나만 그 꼴 · 나머지 둘 [−0.05, 0.05] → 2 회차 순서 1 = 반대 · 3 회차 → {grade([iv_d, (-0.05, 0.05), (-0.05, 0.05)])} · 셋 다 그 꼴 → {grade([iv_d] * 3)}')

print('\n== 2. MR3-08 · 한 팔 잡음의 한쪽 경계 (δ 를 붙임 · 버림은 구간으로)')
th = 0.008
for num in (0.0090, 0.0095, 0.020):
    x = lad(lambda n: math.log(num))
    c_, lo, hi = arm3(x)
    b = lo - math.log(th)
    print(f'  분자 {num} MPa ({c_}) · lo(분자) − ln θ = {b:.4f} (R ≥ {math.exp(b):.3f}) · ln 1.15 이상? {b >= L115} → {"분모 잡음 (한쪽 경계)" if b >= L115 else "둘 다 잡음 쪽 (버림)"}')
print(f'  2 회차 규칙의 사각 띠 (값 > 1.15 θ 인데 경계 < ln 1.15) = ({1.15 * th:.5f}, {1.15 * th * math.exp(DEL):.5f}] MPa → 3 회차는 버림')

print('\n== 3. MR3-05 · 실제 문턱 (팔 구간의 차) · 공통 표류 c/n')
for c in (0.0, 1.0, 1.6):
    hw = 2 * DEL + 3 * c / 48
    dif = math.exp(L13 + hw)
    same = math.exp(L115 - hw) if L115 - hw > 0 else None
    print(f'  c {c}: 반폭 {hw:.4f} → 다름에 R ≥ {dif:.3f} · 같음에 R ≤ {same:.3f}' if same else f'  c {c}: 반폭 {hw:.4f} → 다름에 R ≥ {dif:.3f} · 같음 불가 (반폭 > ln 1.15)')
print(f'  같음이 불가능해지는 공통 표류 c > {(L115 - 2 * DEL) * 16:.3f}')
for c in (1.0, 1.6):
    for r in (1.0, 1.35):
        s = lad(lambda n: math.log(r) + c / n); f = lad(lambda n: c / n)
        a, b = arm3(s), arm3(f)
        iv = iv_diff(a[1:], b[1:])
        print(f'    c {c} 참 R {r}: S {a[0]} F {b[0]} → [{iv[0]:.4f}, {iv[1]:.4f}] {grade([iv] * 3)}')

print('\n== 4. MR3-04 · 최악 예 (팔 규칙이 반대쪽 등급을 인증하는 경우)')
for A_, B_, rinf in ((0.1, 1.0, 0.148), (0.3, 1.5, L13)):
    s = lad(lambda n: rinf - A_ * n ** -0.1 - B_ / n ** 2)
    r = arm3(s); iv = iv_diff(r[1:], arm3(const0)[1:])
    print(f'  숨은 느린 항 (아래에서) A {A_} B {B_} 참 R {math.exp(rinf):.3f}: 비 {(s[3] - s[2]) / (s[2] - s[1]):.3f} {r[0]} → [{iv[0]:.4f}, {iv[1]:.4f}] {grade([iv] * 3)} · 24 셀 남은 오차 {rinf - s[3]:.3f}')
for c in (0.30, 0.50, 0.60):
    s = lad(lambda n: c * n ** -0.1); s[0] = s[1] - 0.010
    r = arm3(s); iv = iv_diff(r[1:], arm3(const0)[1:])
    print(f'  8 셀 구멍 c {c} (참 R 1.00): d {s[1]-s[0]:+.4f} {s[2]-s[1]:+.4f} {s[3]-s[2]:+.4f} {r[0]} → [{iv[0]:.4f}, {iv[1]:.4f}] {grade([iv] * 3)}')

print('\n== 5. MR3-06 · 세 물체 노드 · ②′ 의 사후 미끄럼 = 그 노드의 모든 쌍 충격량 뒤 (최종)')
mu, Jn = 0.5, 0.5
def seq_AB_then_BC(b, c):
    vA = [0.0, 0.0]; vB = [-1.0, b]; vC = [0.0, c]
    vA[0] -= Jn; vB[0] += Jn
    slip_mid = vB[1] - vA[1]
    Jt = max(-mu * Jn, min(mu * Jn, -slip_mid / 2))
    vB[1] += Jt; vA[1] -= Jt
    after_AB = vB[1] - vA[1]
    Jc = (vB[1] - vC[1]) / 2; vB[1] -= Jc; vC[1] += Jc
    return Jt, slip_mid, after_AB, vB[1] - vA[1], vB[1] - vC[1]
def check2p(Jt, slip, eps=1e-12):
    if abs(slip) <= eps:
        return abs(Jt) <= mu * Jn + eps
    return Jt * slip < 0 and abs(abs(Jt) - mu * Jn) <= eps
Jt, sm, sab, sf, bc = seq_AB_then_BC(0.1, -2.0)
print(f'  순차 (A–B → B–C): J_t {Jt:+.3f} · 그 쌍을 풀 때 미끄럼 {sm:+.3f} → {sab:+.3f} · 최종 {sf:+.3f} · ②′ (그 쌍 시점) {check2p(Jt, sab)} · ②′ (최종) {check2p(Jt, sf)} · J_t × 최종 {Jt * sf:+.3f}')
# 동시 풀이 (맞는 풀이) 는 최종 시점에서도 통과
Jt = 0.25; Jc = (2.1 + Jt) / 2; vA = (-Jn, -Jt); vB = (-1 + Jn, 0.1 + Jt - Jc)
print(f'  맞는 풀이 (동시 · J_t +0.25): 최종 미끄럼 {vB[1] - vA[1]:+.3f} · ②′ (최종) {check2p(Jt, vB[1] - vA[1])}')
# 칼날 (붙음에 J_t = µJn 정확히)
b, c = 0.1, -0.85; Jt = -(b + c) / 3; Jc = (b - c + Jt) / 2
vA = (-Jn, -Jt); vB = (-1 + Jn, b + Jt - Jc)
print(f'  칼날 (b 0.1 · c −0.85): J_t {Jt:.6f} · 최종 미끄럼 {vB[1] - vA[1]:+.2e} · ②′ (허용폭 1e-12) {check2p(Jt, vB[1] - vA[1])}')

print('\n== 6. MR3-03 · 팔 하나가 잡음만일 때 수렴으로 받히는 비율 (단마다 독립 정규 · 2 회차 ↔ 3 회차 B)')
rng = np.random.default_rng(20261112)


def arm_vec(x, delta, tau, rule):
    d0 = x[..., 1] - x[..., 0]; d1 = x[..., 2] - x[..., 1]; d2 = x[..., 3] - x[..., 2]
    A = (d1 * d2 > 0) & (np.abs(d2) >= 0.5 * np.abs(d1)) & (np.abs(d2) <= 1.1 * np.abs(d1))
    a, b = x[..., 3], x[..., 3] + 3 * d2
    loA, hiA = np.minimum(a, b) - delta, np.maximum(a, b) + delta
    with np.errstate(invalid='ignore'):
        if rule == 2:
            has8 = ~np.isnan(d0)
            mono = ((d0 > 0) & (d1 > 0) & (d2 > 0)) | ((d0 < 0) & (d1 < 0) & (d2 < 0))
            m = np.maximum(np.abs(d0), np.maximum(np.abs(d1), np.abs(d2)))
            B = ~A & has8 & ~mono & (m <= tau)
        else:
            use0 = ~np.isnan(d0) & (np.abs(d0) <= tau)
            small = (np.abs(d1) <= tau) & (np.abs(d2) <= tau)
            mono12 = ((d1 > 0) & (d2 > 0)) | ((d1 < 0) & (d2 < 0))
            mono3 = mono12 & (((d0 > 0) & (d1 > 0)) | ((d0 < 0) & (d1 < 0)))
            mono = np.where(use0, mono3, mono12)
            m12 = np.maximum(np.abs(d1), np.abs(d2))
            m = np.where(use0, np.maximum(np.abs(d0), m12), m12)
            B = ~A & small & ~mono
    lo = np.where(A, loA, x[..., 3] - delta - 3 * m)
    hi = np.where(A, hiA, x[..., 3] + delta + 3 * m)
    return A | B, lo, hi


NA = 400000
for sig, b8 in ((0.001, 0.0), (0.001, 0.05), (0.005, 0.0), (0.005, 0.05), (0.01, 0.0), (0.01, 0.05)):
    x = rng.normal(0, sig, (NA, 4)); x[:, 0] += b8
    p2 = arm_vec(x, DEL, TAU, 2)[0].mean(); p3 = arm_vec(x, DEL, TAU, 3)[0].mean()
    print(f'  잡음 σ {sig} · 8 셀 치우침 {b8}: 팔 2 회차 {p2:.3f} · 3 회차 {p3:.3f} → 3 회차 점 (팔 6) {p3 ** 6:.3f} · 시험 같음 (점 3) {p3 ** 18:.3g} · G 같음 (점 6) {p3 ** 36:.3g} · 띠 (팔 12) {p3 ** 12:.3f}')
x = rng.normal(0, 0.001, (NA, 4)); x[:, 0] = np.nan
print(f'  8 셀 없음 (σ 0.001): 3 회차 팔 {arm_vec(x, DEL, TAU, 3)[0].mean():.3f} (2 회차 = A 만 {arm_vec(x, DEL, TAU, 2)[0].mean():.3f})')
for sp in (0.0001, 0.0005, 0.001):
    x = rng.normal(0, sp, (NA, 4))
    p3 = arm_vec(x, DPHI, TPHI, 3)[0].mean()
    print(f'  Φ 팔 (δ = τ = 0.002) 잡음 {sp}: 팔 {p3:.3f} · A 등급 팔 6 {p3 ** 6:.3f}')

print('\n== 7. MR3-03 · B 가 받는 숨은 느린 표류 (p 0.1) 의 크기 · 남은 오차 ÷ |d2|')
p = 0.1
r24 = 24 ** -p; dd2 = 24 ** -p - 16 ** -p
print(f'  남은 오차 ÷ |d2| = {r24 / abs(dd2):.1f} (τ 0.02 의 표류를 받으면 24 셀에 남는 오차 약 {r24 / abs(dd2) * 0.02:.2f})')
for sig in (0.001, 0.005):
    out = []
    for step in (1, 2, 4):
        c = step * sig / abs(dd2)
        base = np.array([c * n ** -p for n in N4])
        x = base + rng.normal(0, sig, (NA, 4))
        conv, lo, hi = arm_vec(x, DEL, TAU, 3)
        A = None
        miss = conv & ((lo > 0) | (hi < 0))
        out.append(f'단 변화 {step}σ (c {c:.3f} · 24 셀 남은 오차 {c * r24:.3f}): 받힘 {conv.mean():.3f} · 받혀서 극한 0 을 놓침 {miss.mean():.3f}')
    print(f'  잡음 σ {sig}: ' + ' / '.join(out))

print('\n== 8. MR3-02 · 갈림의 비율 (단마다 독립 정규 잡음 · 2 회차 규칙 ↔ 3 회차 규칙 · 같은 표본)')
# 판정 팔: 시험 2 (3a · 3b κ1) × 점 3 × 충전 3 × 팔 2 (S · F(µ 0.5)) · ln σ
# 띠 팔: 3a F(µ0) 점 2 (ln σ − ln σ_NZ22) · 3b κ1 F(µ0) Φ_d · 3b κ0.2 F(µ0) Φ_d · 충전 3
# A 등급 팔: κ0.2 Φ_m(F(µ0.5)) · Φ_m(A(µ0.5)) · 충전 3
BAND3A = (math.log(0.7), math.log(1.4)); BK1 = (0.94, 1.00); BK02 = (0.83, 0.91)


def lad_noise(N, shape, sig, b8):
    e = rng.normal(0, sig, (N,) + shape + (4,))
    e[..., 0] += b8
    return e


def sim(N, sig, b8, corr, lnR, band3a_truth=(0.0, 0.0), rule=3):
    sigp, b8p = sig / 10, b8 / 10
    # 판정 팔: (N, 시험 2, 점 3, 충전 3, 팔 2, 단 4)
    if corr:
        e = lad_noise(N, (2, 1, 3, 2), sig, b8); e = np.broadcast_to(e, (N, 2, 3, 3, 2, 4))
    else:
        e = lad_noise(N, (2, 3, 3, 2), sig, b8)
    x = e.copy(); x[:, :, :, :, 0, :] += lnR
    conv, lo, hi = arm_vec(x, DEL, TAU, rule)
    cS, cF = conv[..., 0], conv[..., 1]
    loR = lo[..., 0] - hi[..., 1]; hiR = hi[..., 0] - lo[..., 1]
    pc = (cS & cF).all(axis=3)                              # (N, 2, 3)
    dif = (loR >= L115).all(axis=3) & (loR.mean(axis=3) >= L13)
    same = ((loR >= -L13) & (hiR <= L13)).all(axis=3) & (loR.mean(axis=3) >= -L115) & (hiR.mean(axis=3) <= L115)
    opp = (hiR <= -L115).all(axis=3) & (hiR.mean(axis=3) <= -L13)
    g = np.where(~pc, 0, np.where(dif, 1, np.where(same, 2, np.where(opp, 3, 0))))   # 0 중간 1 다름 2 같음 3 반대
    t_opp = (g == 3).any(axis=2); t_dif = (g == 1).sum(axis=2) >= 2; t_same = (g == 2).all(axis=2)
    t = np.where(t_opp, 3, np.where(t_dif, 1, np.where(t_same, 2, 0)))               # (N, 2)
    G = np.where((t == 3).any(axis=1), 3, np.where((t == 1).any(axis=1), 1, np.where((t == 2).all(axis=1), 2, 0)))
    # 띠
    if corr:
        e3a = np.broadcast_to(lad_noise(N, (1, 3), sig, b8), (N, 2, 3, 4))
    else:
        e3a = lad_noise(N, (2, 3), sig, b8)
    x3a = e3a + np.array(band3a_truth)[None, :, None, None]
    c3a, l3a, h3a = arm_vec(x3a, DEL, TAU, rule)
    xk1 = lad_noise(N, (3,), sigp, b8p) + 0.97
    xk02 = lad_noise(N, (3,), sigp, b8p) + 0.87
    ck1, lk1, hk1 = arm_vec(xk1, DPHI, TPHI, rule)
    ck02, lk02, hk02 = arm_vec(xk02, DPHI, TPHI, rule)
    def bandstate(c, l, h, band):
        allc = c.all(axis=-1); ml, mh = l.mean(axis=-1), h.mean(axis=-1)
        inn = allc & (ml >= band[0]) & (mh <= band[1])
        out = allc & ((ml > band[1]) | (mh < band[0]))
        return np.where(inn, 0, np.where(out, 2, 1))                                  # 0 안 1 미정 2 밖
    b3a = bandstate(c3a, l3a, h3a, BAND3A)                                           # (N, 2)
    bk1 = bandstate(ck1, lk1, hk1, BK1); bk02 = bandstate(ck02, lk02, hk02, BK02)
    allb = np.concatenate([b3a, bk1[:, None], bk02[:, None]], axis=1)
    band = np.where((allb == 2).any(axis=1), 2, np.where((allb == 1).any(axis=1), 1, 0))
    # A 등급
    xF = lad_noise(N, (3,), sigp, b8p) + 0.88; xA = lad_noise(N, (3,), sigp, b8p) + 0.88
    cFa, lFa, hFa = arm_vec(xF, DPHI, TPHI, rule); cAa, lAa, hAa = arm_vec(xA, DPHI, TPHI, rule)
    ac = (cFa & cAa).all(axis=1)
    dlo = lFa - hAa; dhi = hFa - lAa
    lack = ac & (dlo >= 0.01).all(axis=1) & (dlo.mean(axis=1) >= 0.02)
    enough = ac & ((dlo >= -0.02) & (dhi <= 0.02)).all(axis=1) & (dlo.mean(axis=1) >= -0.01) & (dhi.mean(axis=1) <= 0.01)
    aopp = ac & (dhi <= -0.01).all(axis=1) & (dhi.mean(axis=1) <= -0.02)
    Ag = np.where(aopp, 3, np.where(lack, 1, np.where(enough, 2, 0)))                 # 0 중간 1 부족 2 충분 3 반대
    # 갈림 (기술 실패 · 마찰 경보는 없다고 둠)
    out = np.full(N, '마', dtype='<U1')
    if rule == 3:
        base = np.where(G == 1, '나', np.where(G == 2, '가', '마'))
        base = np.where(band == 1, '마', base)                                        # 띠 미정 → (마)
        up = (band == 0) & (Ag == 1) & ((base == '가') | (base == '마'))            # 덧규칙 A 부족 → (나) (띠 안에서만)
        base = np.where(up, '나', base)
        base = np.where((band == 0) & (base == '가') & (Ag == 0), '마', base)
        out = np.where((Ag == 3) | (band == 2) | (G == 3), '라', base)
    else:
        base = np.where(G == 1, '나', np.where(G == 2, '가', '마'))
        up = (Ag == 1) & ((base == '가') | (base == '마'))
        base = np.where(up, '나', base)
        base = np.where((base == '가') & (Ag == 0), '마', base)
        out = np.where((Ag == 3) | (band != 0) | (G == 3), '라', base)
    res = {k: float((out == k).mean()) for k in ('가', '나', '마', '라')}
    res['G같음'] = float((G == 2).mean()); res['G다름'] = float((G == 1).mean())
    res['띠안'] = float((band == 0).mean()); res['띠미정'] = float((band == 1).mean()); res['띠밖'] = float((band == 2).mean())
    return res


NS = 100000
for sig, b8 in ((0.001, 0.0), (0.005, 0.0), (0.001, 0.05)):
    for corr in (False, True):
        for tag, lnR, b3 in (('참 같음 (R 1 · 띠 가운데)', 0.0, (0.0, 0.0)),
                             ('참 다름 (R 1.5 · 띠 가운데)', math.log(1.5), (0.0, 0.0)),
                             ('참 같음 · 띠 끝 (3a 0.95 의 F/NZ22 1.38)', 0.0, (0.0, math.log(1.38)))):
            r2 = sim(NS, sig, b8, corr, lnR, b3, rule=2)
            r3 = sim(NS, sig, b8, corr, lnR, b3, rule=3)
            f = lambda r: ' '.join(f'({k}) {r[k]:.3f}' for k in ('가', '나', '마', '라'))
            print(f'  σ {sig} · 8 셀 {b8} · {"런마다 상관" if corr else "독립"} · {tag}')
            print(f'     2 회차 {f(r2)} | 3 회차 {f(r3)} | G 같음 {r3["G같음"]:.3f} · G 다름 {r3["G다름"]:.3f} · 띠 안 {r3["띠안"]:.3f} · 미정 {r3["띠미정"]:.3f} · 밖 {r3["띠밖"]:.3f}')

print('\n== 9. MR3-03 · 숨은 느린 표류 (p 0.1) 의 받힘 비율과 놓침 · 단 변화를 잡음의 배수로 훑음 (A 와 B 둘 다)')
for sig in (0.001, 0.005):
    rows = []
    for step in (1, 2, 4, 6, 8, 12, 16):
        c = step * sig / abs(dd2)
        base = np.array([c * n ** -p for n in N4])
        x = base + rng.normal(0, sig, (NA, 4))
        conv, lo, hi = arm_vec(x, DEL, TAU, 3)
        d1 = x[:, 2] - x[:, 1]; d2 = x[:, 3] - x[:, 2]
        isA = (d1 * d2 > 0) & (np.abs(d2) >= 0.5 * np.abs(d1)) & (np.abs(d2) <= 1.1 * np.abs(d1))
        miss = conv & ((lo > 0) | (hi < 0))
        rows.append(f'{step}σ → 남은 오차 {c * r24:.3f} · 받힘 {conv.mean():.3f} (A {(conv & isA).mean():.3f} · B {(conv & ~isA).mean():.3f}) · 놓침 {miss.mean():.3f}')
    print(f'  잡음 σ {sig}:')
    for r_ in rows:
        print('     ' + r_)

print('\n== 10. 쓰지 않은 대안 · 띠 미정이면 G 의 갈림을 그대로 쓰고 "F 정합 미정" 표지만 (리뷰 MR3-02 의 첫째 길)')
def sim_alt(N, sig, b8, corr, lnR):
    r = sim(N, sig, b8, corr, lnR, (0.0, 0.0), rule=3)
    return r
# 같은 sim 안에서 대안을 셈하려면 G · 띠 · A 를 꺼내야 하므로 (나) 의 상한만 낸다: P(G 다름 그리고 띠 ≠ 밖) ≈ G 다름 (띠 밖 0)
for corr in (False, True):
    r = sim(NS, 0.001, 0.0, corr, math.log(1.5), (0.0, 0.0), rule=3)
    print(f'  σ 0.001 · {"런마다 상관" if corr else "독립"} · 참 다름: 대안이면 (나) ≈ G 다름 {r["G다름"]:.3f} (띠 밖 {r["띠밖"]:.3f}) · 3 회차 규칙 (나) {r["나"]:.3f}')
    r0 = sim(NS, 0.001, 0.0, corr, 0.0, (0.0, 0.0), rule=3)
    print(f'     참 같음: 대안이면 (가) ≤ G 같음 {r0["G같음"]:.3f} · 3 회차 규칙 (가) {r0["가"]:.3f}')

print('\n== 11. 새 한정의 손잡이 (값만 · Q7) · A 의 변화 비 위 끝 1.1 → 1.0 이면 (외삽 배수 2 · p ≥ 1)')
def accA(x, up):
    d1 = x[:, 2] - x[:, 1]; d2 = x[:, 3] - x[:, 2]
    return (d1 * d2 > 0) & (np.abs(d2) >= 0.5 * np.abs(d1)) & (np.abs(d2) <= up * np.abs(d1))
for sig in (0.001,):
    for step in (4, 8, 16):
        c = step * sig / abs(dd2)
        x = np.array([c * n ** -p for n in N4]) + rng.normal(0, sig, (NA, 4))
        print(f'  σ {sig} · 단 변화 {step}σ (남은 오차 {c * r24:.3f}): A 받힘 위 끝 1.1 {accA(x, 1.1).mean():.3f} · 1.0 {accA(x, 1.0).mean():.3f}')
x = rng.normal(0, 0.001, (NA, 4))
print(f'  잡음만 · A 받힘: 1.1 {accA(x, 1.1).mean():.4f} · 1.0 {accA(x, 1.0).mean():.4f}')
