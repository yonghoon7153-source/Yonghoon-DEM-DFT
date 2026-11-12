# 내부 반박 리뷰 3 회차 · 손 산술 확인용 (계산 · 시뮬레이션 아님 · 결정 규칙의 산술과 확률 셈뿐)
# 대상 규칙 = memo_v3_2.md (c72f09ef3245) §4 단계 3 "해상도와 수치 오차" · 부록 D-1
#   팔규칙: d0=x12-x8, d1=x16-x12, d2=x24-x16
#   A: d1*d2>0 and 0.5|d1|<=|d2|<=1.1|d1| -> [min(x24,x24+3d2)-δ, max(...)+δ]
#   B: not A, x8 있음, (d0,d1,d2) 가 0 아닌 같은 부호가 아님, max|d|<=τ -> x24 ± (δ+3max|d|)
#   ln R_k 구간 = [lo(분자)-hi(분모), hi(분자)-lo(분모)]
import math, random
L13, L115 = math.log(1.3), math.log(1.15)
DELTA = TAU = 0.02

def arm(x, delta=DELTA, tau=TAU, has8=True):
    """x = {8: , 12: , 16: , 24: } -> ('A'|'B'|None, lo, hi)"""
    d1, d2 = x[16] - x[12], x[24] - x[16]
    if d1 * d2 > 0 and 0.5 * abs(d1) <= abs(d2) <= 1.1 * abs(d1):
        a, b = sorted((x[24], x[24] + 3 * d2))
        return 'A', a - delta, b + delta
    if has8 and 8 in x:
        d0 = x[12] - x[8]
        ds = (d0, d1, d2)
        same = all(d > 0 for d in ds) or all(d < 0 for d in ds)
        m = max(abs(d) for d in ds)
        if not same and m <= tau:
            return 'B', x[24] - (delta + 3 * m), x[24] + (delta + 3 * m)
    return None, None, None

def grade(intervals):
    """intervals = [(lo,hi)] per charge (ln R) -> 등급 (D-1 5.)"""
    los = [a for a, b in intervals]; his = [b for a, b in intervals]
    n = len(intervals)
    if all(l >= L115 for l in los) and sum(los) / n >= L13: return '다름'
    if all(l >= -L13 and h <= L13 for l, h in intervals) and sum(los) / n >= -L115 and sum(his) / n <= L115: return '같음'
    if all(h <= -L115 for h in his) and sum(his) / n <= -L13: return '반대'
    return '중간'

def lnR(s, f):
    rs, rf = arm(s), arm(f)
    if rs[0] is None or rf[0] is None: return None
    return (rs[1] - rf[2], rs[2] - rf[1]), rs[0], rf[0]

def ladder(fn): return {n: fn(n) for n in (8, 12, 16, 24)}
const0 = ladder(lambda n: 0.0)

print('== 1. MR2-01 손 반례 다시 (팔 구간의 차)')
for tag, s, f, rinf in (('S=ln1.284+4/n · F=72/n²', ladder(lambda n: math.log(1.284) + 4 / n), ladder(lambda n: 72 / n**2), math.log(1.284)),
                        ('S=0.139+11/n · F=180/n²', ladder(lambda n: 0.139 + 11 / n), ladder(lambda n: 180 / n**2), 0.139)):
    iv, cs, cf = lnR(s, f)
    print(f'{tag}: S {cs} F {cf} · ln R [{iv[0]:.4f}, {iv[1]:.4f}] · 참 {rinf:.4f} 안? {iv[0] <= rinf <= iv[1]} · 등급 {grade([iv]*3)}')

print('\n== 2. 새 반례 · 두 팔이 다른 규칙 (S = B 네 단 · F = A 세 단) · 한 팔 안 두 항')
# S: 잡음뿐 (B 로 정당하게 받힘) · F: 두 항 (서로 지움) → F 팔 구간이 극한을 못 담음
s = {8: 0.010, 12: -0.004, 16: 0.006, 24: 0.000}           # 참 0
f = ladder(lambda n: -(8 / n - 144 / n**2))                # 참 0 · 두 항
iv, cs, cf = lnR(s, f)
print(f'S {cs} · F {cf} (F 값 {[round(f[n],4) for n in (8,12,16,24)]}) · ln R [{iv[0]:.4f}, {iv[1]:.4f}] · 참 0 안? {iv[0] <= 0 <= iv[1]} · 등급 {grade([iv]*3)}')

print('\n== 3. 새 반례 · 분자만 못 닿음 = +∞ 가 다른 팔의 수렴 · 크기 · 추세를 건너뜀 (D-1 4)')
cap = math.log(2.4)       # 3a 판독 상한 6 σ_y = 2.4 MPa
# F 는 Φ_m 에 2.0 · 2.15 · 2.3 MPa 로 닿음 (해상도마다 오름) · S 는 세 단 모두 상한 안에서 못 닿음
fF = {8: math.log(1.85), 12: math.log(2.0), 16: math.log(2.15), 24: math.log(2.3)}
cf, flo, fhi = arm(fF)
print(f'F 팔 {cf} 구간 σ [{math.exp(flo):.3f}, {math.exp(fhi):.3f}] MPa · 정직한 아래 경계 ln R ≥ ln 2.4 − hi(F) = {cap - fhi:+.4f} (R ≥ {math.exp(cap - fhi):.3f})')
print('  메모 규칙: lo = hi = +∞ → 충전 셋 모두 그러면 점 = 다름 (실제로는 R 이 1 아래일 수도 있음)')
# F 미수렴 (잡음 크고 부호 흔들림 · τ 초과) 이어도 +∞ 길은 F 를 보지 않는다
fN = {8: math.log(1.6), 12: math.log(2.2), 16: math.log(1.9), 24: math.log(2.35)}
print(f'  F 가 미수렴 ({arm(fN)[0]}) 이어도 +∞ 길은 F 팔규칙을 부르지 않는다 → 다름')
# S 쪽: 상한에서 Φ 가 0.940 · 0.944 · 0.947 (Φ_m 0.95) · 한 항 외삽은 0.95 를 넘는다
sphi = {8: 0.934, 12: 0.940, 16: 0.944, 24: 0.947}
print(f'  S 의 상한 Φ 팔 {arm(sphi, delta=0.002, tau=0.002)[:1]} 외삽 x24+3d2 = {0.947 + 3*(0.947-0.944):.3f} > Φ_m 0.95 → 극한에서는 닿을 수 있다')

print('\n== 4. 잡음만 있는 팔의 수렴 비율 (단마다 독립 정규 · 규칙만 셈) · B 의 |d0| ≤ τ 와 8 셀 치우침')
random.seed(1)
def p_arm(sig, off8=0.0, N=400000):
    ok = 0
    for _ in range(N):
        e = {n: random.gauss(0, sig) for n in (8, 12, 16, 24)}
        e[8] += off8
        if arm(e)[0] is not None: ok += 1
    return ok / N
for sig, off8 in ((0.001, 0.0), (0.001, 0.05), (0.005, 0.0), (0.005, 0.05), (0.01, 0.0)):
    p = p_arm(sig, off8)
    print(f'잡음 σ {sig} · 8 셀 치우침 {off8}: 팔 {p:.3f} · 점 (팔 6) {p**6:.3f} · 시험 같음 (점 3) {p**18:.3g} · G 같음 (점 6) {p**36:.3g} · F 띠 (팔 12) {p**12:.3f}')

print('\n== 5. F 띠 미수렴 → 밖 → (라) 의 무게 (메모의 잡음 모형 · τ ≫ 잡음 · 팔 0.933)')
pa = 0.933
print(f'띠 팔 12 모두 수렴 {pa**12:.3f} → 띠 미정 (라) {1-pa**12:.3f} · (가) 에 닿는 비율 ≤ G 같음 {pa**36:.3f} × 띠 {pa**12:.3f} = {pa**36*pa**12:.3f}')
pp = pa**6; pt = 3*pp**2*(1-pp) + pp**3; pg = 1-(1-pt)**2
print(f'참 차이가 커도 (나) ≤ G 다름의 수렴 몫 {pg:.3f} × 띠 {pa**12:.3f} = {pg*pa**12:.3f}')

print('\n== 6. 공통 표류 (S · F 같은 c/n) · ln R 은 정확히 상수인데 구간이 넓어진다')
for c in (0.0, 1.0, 1.6, 2.0):
    for rinf in (0.0, math.log(1.35)):
        s = ladder(lambda n: rinf + c / n); f = ladder(lambda n: c / n)
        iv, cs, cf = lnR(s, f)
        print(f'c {c} · 참 R {math.exp(rinf):.2f}: S {cs} F {cf} · ln R [{iv[0]:.4f}, {iv[1]:.4f}] · 등급 {grade([iv]*3)}')

print('\n== 7. B 의 8 셀 구멍 · 진폭을 키우면 거짓 다름 (메모는 중간 예만 든다)')
for c in (0.30, 0.50, 0.60):
    s = ladder(lambda n: c * n**-0.1)
    s[8] = s[12] - 0.010                                    # 8 셀만 반대쪽 (d0 = +0.010)
    iv, cs, cf = lnR(s, const0)
    d = (s[12]-s[8], s[16]-s[12], s[24]-s[16])
    print(f'c {c}: d {tuple(round(v,4) for v in d)} · S {cs} · ln R [{iv[0]:.4f}, {iv[1]:.4f}] · 참 0 · 등급 {grade([iv]*3)}')
# 메모 문구 "8 셀만 0.010 낮으면": 자연값에서 0.010 낮추면 d0 는?
c = 0.30; nat8 = c * 8**-0.1; x12 = c * 12**-0.1
print(f'메모 문구 확인: 자연 8 셀 {nat8:.4f} · 12 셀 {x12:.4f} · 자연 d0 {x12-nat8:+.4f} · 8 셀을 0.010 낮추면 d0 {x12-(nat8-0.010):+.4f} (메모는 +0.010)')

print('\n== 8. 아래에서 다가오는 숨은 느린 항 · 진폭을 키우면 거짓 같음의 참값이 1.30 까지')
for A, B, rinf in ((0.1, 1.0, 0.148), (0.3, 1.5, L13)):
    s = ladder(lambda n: rinf - A * n**-0.1 - B / n**2)
    iv, cs, cf = lnR(s, const0)
    d1, d2 = s[16]-s[12], s[24]-s[16]
    print(f'A {A} B {B} 참 R {math.exp(rinf):.3f}: 비 {d2/d1:.3f} S {cs} · ln R [{iv[0]:.4f}, {iv[1]:.4f}] · 등급 {grade([iv]*3)} · 24 셀 남은 오차 {rinf - s[24]:.3f}')

print('\n== 9. MR2-04 예의 한쪽 경계 (δ 를 붙이면)')
th = 0.008
for num in (0.0095, 0.020):
    x = ladder(lambda n: math.log(num))
    c_, lo, hi = arm(x)
    print(f'분자 {num} (세 단 같음 → {c_}) · 메모 ln R ≥ {math.log(num/th):.3f} · 규칙대로 lo(분자) − ln θ = {lo - math.log(th):.3f} (R ≥ {math.exp(lo - math.log(th)):.3f}) · ln 1.15 넘나? {lo - math.log(th) >= L115}')
print(f'버림 문턱: 값 > 1.15 θ 인데 lo(분자) − ln θ < ln 1.15 인 띠 = ({1.15*th:.5f}, {1.15*th*math.exp(DELTA):.5f}] MPa (분자 상수일 때)')

print('\n== 10. MR2-03 · 세 물체 노드 칼날 · 순차 한 번 풀이와 사후 미끄럼의 시점')
# A–B 법선 x (µ 0.5) · B–C 법선 y (무마찰) · 질량 1 · 완전 비탄성 · Jn = 0.5
mu, Jn = 0.5, 0.5
def simul(b, c, Jt):
    Jc = (b - c + Jt) / 2
    vA = (-Jn, -Jt); vB = (-1 + Jn, b + Jt - Jc); vC = (0.0, c + Jc)
    return vA, vB, vC
def check(vA0, vB0, vC0, vA, vB, vC, Jt, eps=1e-12):
    post = vB[1] - vA[1]
    if abs(post) <= eps: c2p = abs(Jt) <= mu * Jn + eps
    else: c2p = (Jt * post < 0) and abs(abs(Jt) - mu * Jn) <= eps
    ke0 = 0.5 * sum(x*x + y*y for x, y in (vA0, vB0, vC0)); ke1 = 0.5 * sum(x*x + y*y for x, y in (vA, vB, vC))
    return post, c2p, ke0, ke1
b, c = 0.1, -0.85                     # 칼날: 붙음에 필요한 J_t = −(b+c)/3 = 0.25 = µJn
Jt_stick = -(b + c) / 3
vA, vB, vC = simul(b, c, Jt_stick)
post, ok, k0, k1 = check((0, 0), (-1, b), (0, c), vA, vB, vC, Jt_stick)
print(f'칼날 b {b} c {c}: 붙음 J_t {Jt_stick!r} (µJn {mu*Jn}) · 사후 미끄럼 {post!r} · ②′ (허용폭 1e-12) {ok} · 허용폭 0 이면 ② |J_t| ≤ µJn: {abs(Jt_stick) <= mu*Jn}')
# 순차 한 번: A–B 먼저 (그 시점 미끄럼으로 마찰) 뒤 B–C
b, c = 0.1, -2.0
vA = [0.0, 0.0]; vB = [-1.0, b]; vC = [0.0, c]
vA[0] -= Jn; vB[0] += Jn                         # A–B 법선
slip_mid = vB[1] - vA[1]
Jt_need = -slip_mid / 2
Jt = max(-mu * Jn, min(mu * Jn, Jt_need))
vB[1] += Jt; vA[1] -= Jt
slip_after_AB = vB[1] - vA[1]
Jc = (vB[1] - vC[1]) / 2                          # B–C 완전 비탄성
vB[1] -= Jc; vC[1] += Jc
slip_final = vB[1] - vA[1]
ke1 = 0.5 * (vA[0]**2 + vA[1]**2 + vB[0]**2 + vB[1]**2 + vC[0]**2 + vC[1]**2)
print(f'순차 한 번 (A–B → B–C): J_t {Jt:+.3f} · 그 쌍을 풀 때 미끄럼 {slip_mid:+.3f} → {slip_after_AB:+.3f} (붙음 · ②′ 통과) · 최종 미끄럼 {slip_final:+.3f} · J_t × 최종 미끄럼 {Jt*slip_final:+.3f} (> 0 = 마찰이 일을 함) · KE 2.505 → {ke1:.3f} (③ 통과)')
# 반대 순서 (B–C → A–B) 와 견줌 (⑤ 순서 바꿈)
vA = [0.0, 0.0]; vB = [-1.0, b]; vC = [0.0, c]
Jc = (vB[1] - vC[1]) / 2; vB[1] -= Jc; vC[1] += Jc
vA[0] -= Jn; vB[0] += Jn
slip_mid = vB[1] - vA[1]; Jt2 = max(-mu * Jn, min(mu * Jn, -slip_mid / 2))
vB[1] += Jt2; vA[1] -= Jt2
print(f'반대 순서 (B–C → A–B): J_t {Jt2:+.3f} · 최종 B–C 상대 법선속도 vB_y − vC_y = {vB[1]-vC[1]:+.3f} (0 아님 → ⑤ 또는 ① 이 잡음)')

print('\n== 11. 검정력 숫자 다시 (메모 0.933 · 0.660 · 0.287 · 0.083)')
p = p_arm(0.001, 0.0, N=800000)
print(f'팔 {p:.4f} · 점 {p**6:.4f} · 시험 같음 {p**18:.4f} · G 같음 {p**36:.4f}')
