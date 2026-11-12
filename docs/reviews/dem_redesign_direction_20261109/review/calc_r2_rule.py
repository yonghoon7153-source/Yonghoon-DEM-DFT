# 내부 반박 리뷰 2 회차 · 손 산술 확인용 (계산 · 시뮬레이션 아님)
# 고친 수렴 규칙 (memo_v3_2.md D-1): d1*d2 > 0 and 0.5|d1| <= |d2| <= 1.1|d1|
# 구간: [min(q24, q24+3 d2) - delta, max(q24, q24+3 d2) + delta]
import math
L13, L115 = math.log(1.3), math.log(1.15)
N = (12, 16, 24)

def conv(x):
    d1, d2 = x[1] - x[0], x[2] - x[1]
    return d1 * d2 > 0 and 0.5 * abs(d1) <= abs(d2) <= 1.1 * abs(d1), d1, d2

def interval(q, delta=0.02):
    d2 = q[2] - q[1]
    lo = min(q[2], q[2] + 3 * d2) - delta
    hi = max(q[2], q[2] + 3 * d2) + delta
    return lo, hi

def grade1(lo, hi):  # 충전 하나만 볼 때의 등급 (세 충전이 같다고 둔 경우)
    if lo >= L13: return '다름'
    if lo >= -L115 and hi <= L115: return '같음'
    if hi <= -L13: return '반대'
    return '중간'

def show(tag, s, f, rinf):
    q = [a - b for a, b in zip(s, f)]
    cs, cf, cq = conv(s), conv(f), conv(q)
    ok = cs[0] and cf[0] and cq[0]
    lo, hi = interval(q)
    g = grade1(lo, hi) if ok else '중간(미수렴)'
    print(f'{tag}: conv S {cs[0]} (비 {cs[2]/cs[1]:.3f}) · F {cf[0]} (비 {cf[2]/cf[1]:.3f}) · R {cq[0]} (비 {cq[2]/cq[1]:.3f})'
          f' | q {[round(v,4) for v in q]} | 구간 [{lo:.4f}, {hi:.4f}] | 참 ln R {rinf:.4f} (R {math.exp(rinf):.3f}) 구간 안? {lo <= rinf <= hi} | 등급 {g}')
    return lo, hi, ok

print('== A. S 와 F 의 차수가 다를 때 (S 오차 a/n · F 오차 b/n² · 같은 부호) — R 은 두 항이 서로 지우는 꼴')
for a, b, rinf in ((4, 72, math.log(1.284)), (11, 180, 0.139)):
    s = [rinf + a / n for n in N]  # S 쪽 ln σ (s∞ = rinf 로 두고 F∞ = 0)
    f = [0 + b / n**2 for n in N]
    lo, hi, ok = show(f'a {a} · b {b}', s, f, rinf)
    # 구간 뺄셈 (각 팔의 한 항 구간에서 R 구간을 낸다)
    los, his = interval(s); lof, hif = interval(f)
    print(f'   구간 뺄셈: [{los-hif:.4f}, {his-lof:.4f}] 참 {rinf:.4f} 안? {los-hif <= rinf <= his-lof} → 등급 {grade1(los-hif, his-lof)}')

print('\n== B. 느린 항 + 빠른 항 (같은 부호 · 서로 지우지 않음) — R 하나에 오차 A n^-0.1 + B n^-2')
for A, BA, qinf in ((0.1, 10, math.log(1.3) - 0.03), (0.25, 5.2, math.log(1.15)), (0.1, 10, math.log(1.15) + 0.008)):
    B = BA * A
    for sign in (+1,):
        q = [qinf + sign * (A * n**-0.1 + B / n**2) for n in N]
        c, d1, d2 = conv(q)
        lo, hi = interval(q)
        e24 = A * 24**-0.1 + B / 576
        print(f'A {A} B/A {BA} q∞ {qinf:.4f}: q {[round(v,4) for v in q]} 비 {d2/d1:.3f} 수렴 {c} | 구간 [{lo:.4f},{hi:.4f}] 참 안? {lo <= qinf <= hi} | 남은 오차/|d2| {e24/abs(d2):.1f} | 등급 {grade1(lo,hi) if c else "중간"} (참 R {math.exp(qinf):.3f})')
# 아래에서 다가오는 경우 (참 = 중간 → 같음 으로)
qinf = 0.148  # R 1.160 (같음 문턱 1.15 바로 위)
A, B = 0.1, 1.0
q = [qinf - (A * n**-0.1 + B / n**2) for n in N]
c, d1, d2 = conv(q); lo, hi = interval(q)
print(f'아래에서 · q∞ {qinf} (R {math.exp(qinf):.3f}): q {[round(v,4) for v in q]} 비 {d2/d1:.3f} 수렴 {c} 구간 [{lo:.4f},{hi:.4f}] 등급 {grade1(lo,hi) if c else "중간"}')
# 8 셀 넷째 점으로 보이는가
A, B = 0.1, 1.0
q4 = [A * n**-0.1 + B / n**2 for n in (8, 12, 16, 24)]
d0, d1, d2 = q4[1]-q4[0], q4[2]-q4[1], q4[3]-q4[2]
print(f'8 셀 점: d0 {d0:.4f} d1 {d1:.4f} d2 {d2:.4f} (부호 같음 → "점근 영역 의심" 표지 안 뜸) · d1/d0 {d1/d0:.3f}')

print('\n== C. 경계 칼날 (한 항 · 비 1.1 · 0.5 바로 안팎)')
def p_for_ratio(target):
    lo, hi = 0.01, 10.0
    r = lambda p: (1 - (2/3)**p) / ((4/3)**p - 1)
    for _ in range(200):
        m = (lo + hi) / 2
        if (r(m) - target) * (r(lo) - target) <= 0: hi = m
        else: lo = m
    return (lo + hi) / 2
for tgt in (1.099, 1.101, 0.501, 0.499):
    p = p_for_ratio(tgt)
    c = 1.0
    q = [c * n**-p for n in N]
    ok, d1, d2 = conv(q)
    resid = q[2] / abs(d2)
    print(f'비 {tgt}: p {p:.3f} 수렴 {ok} 남은 오차 {resid:.2f}·|d2| (구간이 덮는 것 3·|d2| + δ)')

print('\n== D. "한 팔만 잡음 → 잡음 문턱 값" 과 새 수렴 조건')
s = [math.log(0.02) + 0.3 / n for n in N]   # S 는 잡음 위 · 한 항 수렴
f = [math.log(0.005)] * 3                   # F 는 세 단 모두 잡음 문턱으로 올림 (상수)
print('F 상수 →', conv(f), '→ 그 점은 늘 중간 (옛 규칙: (a) |d|≤δ 통과 · (b) d1·d2 ≥ 0 · 0 ≤ 1.1·0 통과)')

print('\n== E. U5 (c) ②′ (접촉 전 미끄럼 기준) 과 세 물체 노드')
# A–B 접촉: 법선 x · B–C 접촉: 법선 y · 질량 1 · µ 0.5 (A–B) · B–C 마찰 없음 · 완전 비탄성 법선
vA = (0.0, 0.0); vB = (-1.0, 0.1); vC = (0.0, -2.0)
mu = 0.5
Jn = 0.5            # A–B 법선: vBx' = -1 + Jn = vAx' = -Jn
def solve(Jt):      # Jt = B 가 A 에서 받는 접선 (y) 충격량
    Jc = (2.1 + Jt) / 2          # B–C 법선 (y): vBy' = vCy'
    vB2 = (-1 + Jn, 0.1 + Jt - Jc); vA2 = (-Jn, -Jt); vC2 = (0.0, -2 + Jc)
    return vA2, vB2, vC2, Jc
def ke(*vs): return 0.5 * sum(x*x + y*y for x, y in vs)
for tag, Jt in (('맞는 풀이 (사후 미끄럼에 맞섬 · 미끄러짐)', +mu * Jn), ('첫 절을 지키는 풀이 (사전 미끄럼에 맞섬)', -mu * Jn)):
    vA2, vB2, vC2, Jc = solve(Jt)
    slip_pre = vB[1] - vA[1]; slip_post = vB2[1] - vA2[1]
    P0 = (vA[0]+vB[0]+vC[0], vA[1]+vB[1]+vC[1]); P1 = (vA2[0]+vB2[0]+vC2[0], vA2[1]+vB2[1]+vC2[1])
    c1 = Jt * slip_pre <= 0                     # ②′ 첫 절: 접촉 전 미끄럼과 반대 또는 0
    c2 = slip_pre * slip_post >= 0              # ②′ 둘째 절: 미끄럼을 0 너머로 뒤집지 않음 (최종 미끄럼으로 읽음)
    print(f'{tag}: Jt {Jt:+.2f} · 미끄럼 {slip_pre:+.3f} → {slip_post:+.3f} · Jt·사후미끄럼 {Jt*slip_post:+.3f} (≤ 0 이면 소산)'
          f' · ②′ 첫 절 {"통과" if c1 else "불합격"} · 둘째 절 {"통과" if c2 else "불합격"}'
          f' · ② {"통과" if abs(Jt) <= mu*Jn + 1e-12 else "불합격"} · KE {ke(vA,vB,vC):.3f} → {ke(vA2,vB2,vC2):.3f} · 운동량 {P0} → {tuple(round(v,6) for v in P1)}')
# 맞는 풀이가 붙음이 아님을 확인: 붙음이면 Jt = 0.95/1.5 = 0.633 > µ·Jn
print('붙음에 필요한 Jt =', round(0.95 / 1.5, 3), '> µ·Jn =', mu * Jn, '→ 미끄러짐이 맞다')
# 둘째 절을 지킬 수 있는 Coulomb 허용 Jt 가 있는가: 사후 미끄럼 = -0.95 + 1.5 Jt ≥ 0 이려면 Jt ≥ 0.633
print('|Jt| ≤ µ·Jn 에서 사후 미끄럼 범위:', round(-0.95 + 1.5 * (-mu * Jn), 3), '…', round(-0.95 + 1.5 * (mu * Jn), 3), '→ 어떤 허용 Jt 도 미끄럼을 뒤집지 않을 수 없다')
# 1 회차 두 물체 반례 (마찰 방향이 틀린 구현) 를 사후 미끄럼 기준으로 보면
v1 = (1.0, 0.5); w = (-1.0, -0.5); J1 = (-1.0, +0.5)
a = (v1[0] + J1[0], v1[1] + J1[1]); b = (w[0] - J1[0], w[1] - J1[1])
print('1 회차 두 물체 반례: 사후 미끄럼', a[1] - b[1], '· 물체 1 의 접선 충격량', J1[1], '→ 사후 미끄럼과 같은 쪽 → 사후 기준으로도 불합격')
