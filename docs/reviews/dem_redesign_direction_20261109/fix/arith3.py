# 내부 반박 리뷰 2 회차 고침용 손 산술 (계산 · 시뮬레이션 아님 · 결정적 산술과 격자 적분뿐)
# 고친 규칙 (메모 3.2 · 2 회차 고침):
#   팔 x (ln σ 또는 Φ_m) 마다 A (한 항) 또는 B (격자 둔감) 로 수렴을 보고 팔 구간을 낸다.
#   A: d1*d2 > 0 and 0.5|d1| <= |d2| <= 1.1|d1|  -> [min(x24, x24+3 d2) - δ, max(...) + δ]
#   B: A 가 아니고, d0 d1 d2 가 0 아닌 같은 부호 (한결같은 표류) 가 아니고, max|d| <= τ
#        -> [x24 - δ - 3 max|d|, x24 + δ + 3 max|d|]
#   ln R 구간 = [lo_분자 - hi_분모, hi_분자 - lo_분모]  (R 자신의 세 값은 쓰지 않는다)
import math
L13, L115 = math.log(1.3), math.log(1.15)
DELTA, TAU = 0.02, 0.02
N4 = (8, 12, 16, 24)

def arm(x, delta=DELTA, tau=TAU):
    """x = [x8, x12, x16, x24] -> (경로, lo, hi, d0, d1, d2)"""
    d0, d1, d2 = x[1] - x[0], x[2] - x[1], x[3] - x[2]
    if d1 * d2 > 0 and 0.5 * abs(d1) <= abs(d2) <= 1.1 * abs(d1):
        a, b = x[3], x[3] + 3 * d2
        return 'A', min(a, b) - delta, max(a, b) + delta, d0, d1, d2
    ds = (d0, d1, d2)
    mono = all(d > 0 for d in ds) or all(d < 0 for d in ds)
    m = max(abs(d) for d in ds)
    if not mono and m <= tau:
        return 'B', x[3] - delta - 3 * m, x[3] + delta + 3 * m, d0, d1, d2
    return '미수렴', None, None, d0, d1, d2

def grade1(lo, hi):  # 충전 셋이 같다고 둔 점 등급
    if lo >= L13: return '다름'
    if lo >= -L115 and hi <= L115 and lo >= -L13 and hi <= L13: return '같음'
    if hi <= -L13: return '반대'
    return '중간'

def point(s, f, rinf, tag):
    a_s, a_f = arm(s), arm(f)
    if a_s[0] == '미수렴' or a_f[0] == '미수렴':
        print(f'{tag}: S {a_s[0]} (비 {a_s[5]/a_s[4] if a_s[4] else float("nan"):.3f}) · F {a_f[0]} → 중간 (미수렴) · 참 ln R {rinf:.4f} (R {math.exp(rinf):.3f})')
        return
    lo, hi = a_s[1] - a_f[2], a_s[2] - a_f[1]
    print(f'{tag}: S {a_s[0]} [{a_s[1]:.4f},{a_s[2]:.4f}] · F {a_f[0]} [{a_f[1]:.4f},{a_f[2]:.4f}] → ln R [{lo:.4f},{hi:.4f}] '
          f'(R {math.exp(lo):.3f}–{math.exp(hi):.3f}) · 참 {rinf:.4f} (R {math.exp(rinf):.3f}) 안? {lo <= rinf <= hi} · 등급 {grade1(lo, hi)} (참 등급 {grade1(rinf, rinf)})')

print('== MR2-01: 차수가 다른 두 팔 (리뷰 calc_r2_rule.py A 의 두 경우) · 팔 구간의 차')
for a, b, rinf in ((4, 72, math.log(1.284)), (11, 180, 0.139)):
    s = [rinf + a / n for n in N4]; f = [b / n**2 for n in N4]
    point(s, f, rinf, f'a {a} · b {b}')

print('\n== 판정문 DRD-01 반례를 팔로: S = ln(1.10 + 3.36/n) · F = 0 (상수 → B 길) / F = -0.05·12/n (A 길)')
s = [math.log(1.10 + 3.36 / n) for n in N4]
point(s, [0.0] * 4, math.log(1.10), 'F 상수')
f = [-0.05 * 12 / n for n in N4]; s2 = [si + fi for si, fi in zip(s, f)]
point(s2, f, math.log(1.10), 'F 한 항 1 차')

print('\n== 1 회차 P1-2 반례 (한 항 · 느린 수렴) 를 팔로: S = q∞ ± 0.664 n^-0.1 · F = 0')
for qinf, sg, tag in ((0.0, +1, '위에서 · 참 같음'), (math.log(1.5), -1, '아래에서 · 참 다름')):
    s = [qinf + sg * 0.664 * n**-0.1 for n in N4]
    point(s, [0.0] * 4, qinf, tag)
    print('   S 세 단', [round(v, 4) for v in s[1:]], ' d0', round(s[1] - s[0], 4))

print('\n== 한 팔 안의 두 항 (고친 규칙의 한계 · S = q∞ + a/n - b/n² · F = 0)')
for a, b, rinf in ((4, 72, math.log(1.284)), (8, 144, math.log(1.25)), (12, 216, math.log(1.20))):
    s = [rinf + a / n - b / n**2 for n in N4]
    point(s, [0.0] * 4, rinf, f'a {a} b {b}')

print('\n== MR2-02: 느린 항 + 빠른 항 (같은 부호) 를 한 팔에 · F = 0')
for A, B, qinf in ((0.1, 1.0, math.log(1.262)), (0.25, 1.3, math.log(1.15)), (0.5, 2.6, math.log(1.10)), (0.5, 2.6, math.log(1.20))):
    s = [qinf + A * n**-0.1 + B / n**2 for n in N4]
    point(s, [0.0] * 4, qinf, f'A {A} B {B}')
    e24 = A * 24**-0.1 + B / 576
    print(f'   24 셀에 남는 오차 {e24:.4f} · d2 {s[3]-s[2]:.4f} · 남은 오차/|d2| {e24/abs(s[3]-s[2]):.1f}')
# 넷째 단 (16 · 24 · 36 등비) 로도 가르지 못한다
A, B = 0.1, 1.0
q = {n: A * n**-0.1 + B / n**2 for n in (16, 24, 36)}
dd2, dd3 = q[24] - q[16], q[36] - q[24]
print(f'16·24·36: 변화 비 {dd3/dd2:.4f} (등비 사다리의 수렴 범위 0.29–0.75 안?) {0.2867 <= dd3/dd2 <= 0.7468} · '
      f'구간 [{min(q[36], q[36]+3*dd3)-DELTA:.4f}, {max(q[36], q[36]+3*dd3)+DELTA:.4f}] 극한 0 안? {min(q[36], q[36]+3*dd3)-DELTA <= 0}')

print('\n== MR2-06 의 B 길 구멍: 잡음 아래 숨은 느린 표류')
# L1: 표류 + 잡음 (부호를 잡음이 엇갈리게) · F = 0
c = 0.3; noise = (0.0, +0.006, -0.006, +0.006)
s = [c * n**-0.1 + e for n, e in zip(N4, noise)]
print('L1 S', [round(v, 4) for v in s], arm(s)[0], ' 24 셀에 남는 오차', round(c * 24**-0.1, 4))
point(s, [0.0] * 4, 0.0, 'L1 (참 R 1.00)')
# L2: 순수 느린 표류 + 8 셀만 반대쪽 (점근 영역 밖)
s = [0.30 * n**-0.1 for n in N4]; s[0] = s[1] - 0.010
print('L2 S', [round(v, 4) for v in s], arm(s)[0])
point(s, [0.0] * 4, 0.0, 'L2 (참 R 1.00)')
# 남는 오차 / 판정 단 순변화 (p 0.1)
p = 0.1
print('p 0.1: 24 셀 남는 오차 ÷ |x24 − x12| =', round(24**-p / (12**-p - 24**-p), 1), ' ÷ |x24 − x8| =', round(24**-p / (8**-p - 24**-p), 1))

print('\n== MR2-06: 잡음만 있는 팔이 수렴으로 받히는 비율 (단마다 i.i.d. 정규 잡음 · τ 가 잡음보다 충분히 크다고 둠)')
# A (세 단): d2/d1 ~ Cauchy(ρ = -1/2, 척도 √(1-ρ²))
rho = -0.5; sc = math.sqrt(1 - rho**2)
pA = (math.atan((1.1 - rho) / sc) - math.atan((0.5 - rho) / sc)) / math.pi
print('P(A) =', round(pA, 4), ' P(d1·d2 ≤ 0) =', round(0.5 + math.asin(0.5) / math.pi, 4), ' P(한결같은 넷 · 단조) = 1/12 =', round(1 / 12, 4))
# P(A 그리고 단조) 를 격자 적분으로 (x12, x16, x24 · x8 은 Φ 로)
import numpy as np
from math import erf, sqrt
g = np.linspace(-6, 6, 241); h = g[1] - g[0]
phi = np.exp(-g**2 / 2) / math.sqrt(2 * math.pi)
Phi = 0.5 * (1 + np.vectorize(lambda v: erf(v / sqrt(2)))(g))
X12, X16, X24 = np.meshgrid(g, g, g, indexing='ij')
W = (phi[:, None, None] * phi[None, :, None] * phi[None, None, :]) * Phi[:, None, None] * h**3
d1 = X16 - X12; d2 = X24 - X16
mask = (d1 > 0) & (d2 >= 0.5 * d1) & (d2 <= 1.1 * d1)
pAmono = 2 * float((W * mask).sum())  # 위로 단조 + 아래로 단조
pAB = 11 / 12 + pAmono
print('P(A 그리고 단조) ≈', round(pAmono, 4), ' → 팔 하나 P(A 또는 B) ≈', round(pAB, 4))
for k, name in ((6, '점 (충전 셋 × 팔 둘)'), (18, '시험 같음 (점 셋 모두)'), (36, 'G 같음 (점 여섯 모두)')):
    print(f'   {name}: {pAB**k:.3f}')
print('고치기 전 (세 q × 충전 셋 = 9 열 · 열마다 A 만):', f'{pA**9:.1e}', '(리뷰의 독립 d 가정 0.1176 이면', f'{0.1176**9:.1e})')

print('\n== MR2-03: 세 물체 노드 (A 정지 · B (-1, 0.1) · C (0, -2) · 질량 1 · A–B 법선 x µ 0.5 · B–C 법선 y 무마찰 · 완전 비탄성)')
mu, Jn = 0.5, 0.5
def solve(Jt):
    Jc = (2.1 + Jt) / 2
    vA, vB, vC = (-Jn, -Jt), (-1 + Jn, 0.1 + Jt - Jc), (0.0, -2 + Jc)
    return vA, vB, vC, Jc
ke = lambda *vs: 0.5 * sum(x * x + y * y for x, y in vs)
for Jt, tag in ((+0.25, '맞는 풀이'), (-0.25, '사전 미끄럼에 맞선 풀이')):
    vA, vB, vC, Jc = solve(Jt)
    pre, post = 0.1 - 0.0, vB[1] - vA[1]
    stick = abs(post) < 1e-12
    newok = (stick and abs(Jt) <= mu * Jn + 1e-12) or (not stick and Jt * post < 0 and abs(abs(Jt) - mu * Jn) < 1e-12)
    oldok = Jt * pre <= 0 and pre * post >= 0
    print(f'{tag}: Jt {Jt:+.2f} · Jc {Jc:.3f} · 미끄럼 {pre:+.3f} → {post:+.3f} · Jt·사후 {Jt*post:+.3f} · KE {ke((0,0),(-1,0.1),(0,-2)):.3f} → {ke(vA,vB,vC):.3f} '
          f'· 옛 ②′ {"통과" if oldok else "불합격"} · 새 ②′ {"통과" if newok else "불합격"}')
print('붙음에 필요한 Jt', round(0.95 / 1.5, 3), '> µJn', mu * Jn)
# 1 회차 두 물체 반례 (마찰 방향 틀림) 와 맞는 두 물체 풀이
for J1t, tag in ((+0.5, '마찰 방향 틀림'), (-0.5, '맞는 풀이 (붙음)')):
    a = (1.0 - 1.0, 0.5 + J1t); b = (-1.0 + 1.0, -0.5 - J1t)
    post = a[1] - b[1]; stick = abs(post) < 1e-12
    newok = (stick and abs(J1t) <= 0.5 + 1e-12) or (not stick and J1t * post < 0 and abs(abs(J1t) - 0.5) < 1e-12)
    print(f'두 물체 {tag}: J_t {J1t:+.1f} · 사후 미끄럼 {post:+.1f} · KE 1.25 → {ke(a, b):.2f} · 새 ②′ {"통과" if newok else "불합격"}')

print('\n== MR2-04: 한 팔만 잡음 (3a · 응력 잡음 문턱 0.008 MPa)')
thr = 0.008
for sS in (0.0090, 0.0095, 0.020):
    tagstate = '분모만잡음 (한쪽 경계)' if sS > 1.15 * thr else '둘다잡음 쪽 (버림)'
    print(f'S {sS} MPa (24 셀 · 구간 아래 끝을 같은 값으로 둠) · F ≤ 0.008 → 1.15 × 문턱 = {1.15*thr:.4f} → {tagstate} · 경계 ln R ≥ {math.log(sS/thr):.3f} (R ≥ {sS/thr:.2f})')

print('\n== MR2-18: 1 회차 P1-2 ② 의 첫 값')
for c in (0.664, 0.6646):
    print(c, [round(math.log(1.5) - c * n**-0.1, 4) for n in (12, 16, 24)])

print('\n== MR2-12: 선택 수 (k_F = 노드 다물체 풀이 1 + 판독 선택 3 + 틈 보정 · 거리 판정 0–2)')
for extra in (0, 1, 2):
    kF = 1 + 3 + extra
    print(f'k_F {kF}: F-실제 {2 + kF} · F-연화 {3 + kF}')

print('\n== 새 카드 산술 (KE25 · DR21 · JU26)')
print('ketter2025 ρ_geo 1.634: 1.64 기준 공극', round(100 * (1 - 1.634 / 1.64), 2), '% · 1.86 기준', round(100 * (1 - 1.634 / 1.86), 2), '% · 카드 ρ_rel 87.87 % 와', round(100 * 1.634 / 1.86, 2))
print('doerrer2021 순수 LPSCl 적층압 아래 상대밀도 0.86–0.90 → 공극 10–14 % (분모 미기재)')
print('jung2026 H 1.34 GPa vs D1 가장 작은 경도 0.545 GPa:', round(1.34 / 0.545, 2), '배 · YL26 92 MPa / 1.34 GPa =', round(0.092 / 1.34, 3))

print('\n== B 길이 거짓 등급을 내는 예 (느린 표류 + 24 셀 잡음 한 번)')
c, e = 0.5, 0.016
s = [c * n**-0.1 for n in N4]; s[3] += e
r = arm(s); print('S', [round(v, 4) for v in s], r[0], 'd', [round(v, 4) for v in r[3:]], ' 24 셀 남는 오차', round(s[3], 4))
point(s, [0.0] * 4, 0.0, '표류 c 0.5 + 24 셀 +0.016 (참 R 1.00)')

print('\n== B 를 "판정 세 단의 두 변화가 부호 엇갈림 (d1·d2 ≤ 0)" 으로 좁히면 (대안 · 쓰지 않음)')
pA_n = pA; p_alt = 0.5 + math.asin(0.5) / math.pi
arm_n = pA_n + p_alt
pt_n = arm_n ** 6
print(f'팔 {arm_n:.3f} · 점 {pt_n:.3f} · 시험 같음 {pt_n**3:.4f} · G 같음 {pt_n**6:.2e}')
# L2 를 이 좁힌 B 로 보면
s = [0.30 * n**-0.1 for n in N4]; s[0] = s[1] - 0.010
d0, d1, d2 = s[1]-s[0], s[2]-s[1], s[3]-s[2]
print(f'L2 d0 {d0:+.4f} d1 {d1:+.4f} d2 {d2:+.4f} → 좁힌 B? {d1*d2 <= 0} · A? {d1*d2 > 0 and 0.5*abs(d1) <= abs(d2) <= 1.1*abs(d1)} → 미수렴')

print('\n== MR2-02 의 아래에서 다가오는 경우 (리뷰 calc_r2_rule.py B 의 끝 경우) 를 팔로 · F 상수')
qinf = 0.148  # R 1.160 (같음 문턱 1.15 바로 위 · 참 등급 중간)
s = [qinf - (0.1 * n**-0.1 + 1.0 / n**2) for n in N4]
print('S', [round(v, 4) for v in s])
point(s, [0.0] * 4, qinf, '아래에서 A 0.1 B 1.0 (참 R 1.160)')
qinf2 = 0.130  # R 1.139 (참 같음) · 같은 꼴
s2 = [qinf2 - (0.1 * n**-0.1 + 1.0 / n**2) for n in N4]
point(s2, [0.0] * 4, qinf2, '아래에서 A 0.1 B 1.0 (참 R 1.139)')
