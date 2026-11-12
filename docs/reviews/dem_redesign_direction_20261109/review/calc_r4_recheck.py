# 내부 반박 리뷰 4 회차 재확인 (Codex 아님) · 손 산술 확인용 (계산 · 시뮬레이션 아님 · 결정 규칙의 산술과 확률 셈뿐)
# 대상 규칙 = memo_v3_2.md (3aae76fc2e89) §4 단계 3 · 부록 D-1 · D-2 · §7 Q13 · U6 (b)
# 이 파일은 고친 쪽 fix/arith4.py 를 import 하지 않고 D-1 문장에서 규칙을 따로 옮겼다.
import math
import numpy as np

L13, L115 = math.log(1.3), math.log(1.15)
DEL = TAU = 0.02
DPHI = TPHI = 0.002
INF = float('inf')
CAP = math.log(2.4)          # 3a 판독 응력 상한 6 σ_y
TH = math.log(0.008)         # 3a 잡음 문턱 θ


def arm(x, delta=DEL, tau=TAU, lo_hi=(0.5, 1.1), fac=3.0):
    """D-1 팔규칙 (3 회차) · x = (x8 | None, x12, x16, x24) → ('A'|'B'|None, lo, hi)"""
    x8, x12, x16, x24 = x
    d1, d2 = x16 - x12, x24 - x16
    if d1 * d2 > 0 and lo_hi[0] * abs(d1) <= abs(d2) <= lo_hi[1] * abs(d1):
        a, b = sorted((x24, x24 + fac * d2))
        return 'A', a - delta, b + delta
    if abs(d1) <= tau and abs(d2) <= tau:
        U = [d1, d2]
        if x8 is not None and abs(x12 - x8) <= tau:
            U.append(x12 - x8)
        same = all(d > 0 for d in U) or all(d < 0 for d in U)       # "0 아닌 같은 부호"
        if not same:
            m = max(abs(d) for d in U)
            return 'B', x24 - (delta + 3 * m), x24 + (delta + 3 * m)
    return None, None, None


def grade(ivs):
    """D-1 의 3. (충전 조건 먼저 · 평균은 뒤)"""
    los = [a for a, b in ivs]; his = [b for a, b in ivs]; n = len(ivs)
    if all(l >= L115 for l in los) and sum(los) / n >= L13: return '다름'
    if all(l >= -L13 and h <= L13 for l, h in ivs) and sum(los) / n >= -L115 and sum(his) / n <= L115: return '같음'
    if all(h <= -L115 for h in his) and sum(his) / n <= -L13: return '반대'
    return '중간'


def lnlad(vals):  # MPa 네 단 → ln
    return tuple(None if v is None else math.log(v) for v in vals)


print('== 1. MR3-01 · 리뷰 손 반례를 새 규칙 (D-1 · 한 식 · Φ_cap 확인) 에 다시 넣음')
F = arm(lnlad((1.85, 2.0, 2.15, 2.3)))
iv1 = (CAP - F[2], INF)                     # 분자 (S) 못닿음 · Φ_cap 확인됨 · ln R ∈ [ln cap − hi(F), +∞)
print(f'  ① F {F[0]} σ [{math.exp(F[1]):.3f}, {math.exp(F[2]):.3f}] MPa → ln R ≥ {iv1[0]:+.4f} (R ≥ {math.exp(iv1[0]):.3f}) · 충전 셋 → {grade([iv1]*3)} (2 회차 +∞ → 다름)')
print(f'  ② 두 충전 [0.15, 0.25] + 셋째 ① → {grade([(0.15, 0.25), (0.15, 0.25), iv1])} (2 회차 → 다름)')
Fn = arm(lnlad((1.6, 2.2, 1.9, 2.35)))
print(f'  ③ 분자 못닿음 · F 1.6 · 2.2 · 1.9 · 2.35 MPa → F 팔 {Fn[0]} → D-1 의 2 → 점 중간')
c4 = arm((0.934, 0.940, 0.944, 0.947), DPHI, TPHI)
print(f'  ④ Φ_cap 0.934 · 0.940 · 0.944 · 0.947 → {c4[0]} [{c4[1]:.4f}, {c4[2]:.4f}] · hi ≤ Φ_m 0.95? {c4[2] <= 0.95} → 확인 안 됨 → 점 중간')
S = arm(lnlad((0.95, 1.0, 1.03, 1.05)))
ivd = (-INF, S[2] - CAP)
print(f'  분모 못닿음 · S {S[0]} [{math.exp(S[1]):.3f}, {math.exp(S[2]):.3f}] → ln R ≤ {ivd[1]:.3f} · 한 충전 + ±0.05 둘 → {grade([ivd, (-0.05, 0.05), (-0.05, 0.05)])} · 셋 → {grade([ivd]*3)}')
F2 = arm(lnlad((0.50, 0.53, 0.55, 0.57)))
print(f'  크기 있는 못닿음 · F {F2[0]} → ln R ≥ {CAP - F2[2]:.3f} (R ≥ {math.exp(CAP - F2[2]):.2f}) · 셋 → {grade([(CAP - F2[2], INF)]*3)}')

print('\n== 2. MR3-08 · 한 팔 잡음의 경계에 δ · 버림 띠')
for v in (0.0090, 0.0093, 0.0095, 0.020):
    a = arm(lnlad((v, v, v, v)))
    b = a[1] - TH
    print(f'  분자 {v} ({a[0]}) → lo(분자) − ln θ = {b:.4f} (R ≥ {math.exp(b):.3f}) → {"버림" if b < L115 else "한쪽 경계"}')
print(f'  2 회차 판의 사각 띠 (1.15 θ , 1.15 θ e^δ] = ({1.15*0.008:.5f}, {1.15*0.008*math.exp(DEL):.5f}] MPa')

print('\n== 3. MR3-02 · 검정력 · 독립 정규 가정의 곱 (해석) 으로 메모 숫자를 따로 다시 냄')
# 잡음만 있는 팔의 수렴 비율 p (MC 아님 · Cauchy 꼴 P(A) + 반대 부호 2/3 · σ ≪ τ)
pA = (math.atan((1.1 + 0.5) / (math.sqrt(3) / 2)) - math.atan((0.5 + 0.5) / (math.sqrt(3) / 2))) / math.pi
print(f'  P(A | 잡음) = {pA:.4f} (d₂/d₁ = 위치 −½ · 척도 √3/2 Cauchy) · P(d₁d₂ < 0) = 2/3')
# 8 셀 τ 안 (σ ≪ τ): 수렴 = A ∨ B · B = not A ∧ not (d0, d1, d2 같은 부호)
#   P = P(A) + 1 − P(넷 단조) − P(A) + P(A ∧ 넷 단조) = 1 − 1/12 + P(A ∧ 넷 단조)
#   P(A ∧ 넷 단조) ≈ 0.0164 은 리뷰 3 회차 · fix/arith3 의 격자 적분값 (여기서 다시 셈하지 않음 · 아래 §4 MC 로 대조)
pmono = 1 / 12
p_arm = 1 - pmono + 0.0164
print(f'  팔 (A 또는 B · 8 셀 정상) ≈ {p_arm:.4f} · 8 셀 쓸 수 없음 ≈ {pA + 2/3:.4f}')
for p, tag in ((p_arm, '8 셀 정상'), (pA + 2/3, '8 셀 치우침')):
    G_same = p ** 36; band = p ** 12; Aok = 0.934 ** 6 if tag == '8 셀 정상' else (pA + 2/3) ** 6
    q = p ** 6; t_dif = 3 * q * q * (1 - q) + q ** 3; G_dif = 1 - (1 - t_dif) ** 2
    print(f'  [{tag}] G 같음 {G_same:.4f} · 띠 안 {band:.3f} · A 충분 {Aok:.3f} → (가) ≈ {G_same*band*Aok:.4f} · G 다름 {G_dif:.3f} → (나) ≈ {G_dif*band:.4f}')
print('  (나) 는 A 등급 팔 6 과 G 의 팔 36 전부를 요구하지 않는다 → "팔 54 개가 모두 수렴" 은 (가) 에만 맞는 말')
# 같은 런의 점끼리 완전 상관 (한 시험의 점 셋이 같은 잡음): 시험 = 점 하나 꼴
p = p_arm; q = p ** 6
G_same_c = q ** 2; band_c = p ** 3 * 0.934 ** 6; G_dif_c = 1 - (1 - q) ** 2
print(f'  [완전 상관 · 8 셀 정상] G 같음 {G_same_c:.3f} · 띠 안 {band_c:.3f} → (가) ≈ {G_same_c*band_c*0.934**6:.3f} · G 다름 {G_dif_c:.3f} → (나) ≈ {G_dif_c*band_c:.3f}')
print('  거짓 비율: 참 같음 → (나) 는 B 구간 반폭 ≈ 0.05 라 아래 끝이 ln 1.3 에 못 닿아 0 · 참 다름 (R 1.5) → (가) 는 위 끝이 ln 1.15 를 넘어 0 · 잡음만으로 (라) 0')

rng = np.random.default_rng(4041112)


def arm_v(x, delta, tau, lo=0.5, hi=1.1, use8=True):
    d0 = x[:, 1] - x[:, 0]; d1 = x[:, 2] - x[:, 1]; d2 = x[:, 3] - x[:, 2]
    A = (d1 * d2 > 0) & (np.abs(d2) >= lo * np.abs(d1)) & (np.abs(d2) <= hi * np.abs(d1))
    small = (np.abs(d1) <= tau) & (np.abs(d2) <= tau)
    u0 = use8 & (np.abs(d0) <= tau)
    same12 = ((d1 > 0) & (d2 > 0)) | ((d1 < 0) & (d2 < 0))
    same3 = same12 & (((d0 > 0) & (d1 > 0)) | ((d0 < 0) & (d1 < 0)))
    same = np.where(u0, same3, same12)
    B = ~A & small & ~same
    return A, B


def arm_v_r2(x, delta, tau):
    d0 = x[:, 1] - x[:, 0]; d1 = x[:, 2] - x[:, 1]; d2 = x[:, 3] - x[:, 2]
    A = (d1 * d2 > 0) & (np.abs(d2) >= 0.5 * np.abs(d1)) & (np.abs(d2) <= 1.1 * np.abs(d1))
    same3 = ((d0 > 0) & (d1 > 0) & (d2 > 0)) | ((d0 < 0) & (d1 < 0) & (d2 < 0))
    m = np.maximum(np.abs(d0), np.maximum(np.abs(d1), np.abs(d2)))
    return A, (~A & ~same3 & (m <= tau))


N = 400000
print('\n== 4. MR3-03 · 잡음만 있는 팔 (MC · 단마다 독립 정규)')
for sig, b8 in ((0.001, 0), (0.005, 0), (0.01, 0), (0.001, 0.05)):
    x = rng.normal(0, sig, (N, 4)); x[:, 0] += b8
    A, B = arm_v(x, DEL, TAU)
    print(f'  σ {sig} · 8 셀 치우침 {b8}: 팔 {(A | B).mean():.3f}')

print('\n== 5. U6 (b) 촉발 · (i) 잡음 촉발 팔마다 비율 · 팔 둘 (S · F) 이면 · (ii) 잘 수렴하는 A 팔이 |d₀| > τ 로 촉발하는 조건')
for sig in (0.0025, 0.005, 0.01):
    x = rng.normal(0, sig, (N, 4))
    d1 = x[:, 2] - x[:, 1]; d2 = x[:, 3] - x[:, 2]
    A = (d1 * d2 > 0) & (np.abs(d2) >= 0.5 * np.abs(d1)) & (np.abs(d2) <= 1.1 * np.abs(d1))
    t = (~A & (d1 * d2 < 0) & (np.maximum(np.abs(d1), np.abs(d2)) > TAU / 2)).mean()
    print(f'  잡음 σ {sig} (τ/{TAU/sig:.0f}): 팔마다 {t:.3f} · 팔 둘에서 하나라도 {1-(1-t)**2:.3f} (놓침 {(1-t)**2:.3f})')
for p in (0.5, 1.0, 2.0):
    r0 = (12 ** -p - 8 ** -p) / (16 ** -p - 12 ** -p)      # d0/d1
    r2 = (24 ** -p - 16 ** -p) / (16 ** -p - 12 ** -p)     # d2/d1
    print(f'  한 항 c·n^(−{p}) (잡음 없음): d₂/d₁ {r2:.3f} → A · d₀/d₁ {r0:.2f} → |d₁| > τ/{r0:.2f} = {TAU/r0:.4f} 이면 |d₀| > τ → "8 셀 치우침" 촉발 (A 팔인데)')
xs = [math.log(1.10 + 3.36 / n) for n in (8, 12, 16, 24)]
print(f'  판정문 반례 S = ln(1.10 + 3.36/n): d₀ {xs[1]-xs[0]:+.4f} (|d₀| > τ) · 팔 {arm(tuple(xs))[0]} → U6 (b) 에서 이 꼴이면 촉발')
print(f'  U6 (a) 문턱 ΔΦ_m 0.005 · NZ22 경화 0 곡선 기울기 d ln σ/dΦ ≈ ln(1.11/0.68)/0.05 = {math.log(1.11/0.68)/0.05:.1f} → Δln σ ≈ {math.log(1.11/0.68)/0.05*0.005:.3f} (> τ) [어림]')

print('\n== 6. Q13 · 사다리를 올려도 잡음만 있는 팔의 수렴 비율은 그대로 (16 · 24 · 36 · 증인 12 · A 범위 0.29–0.75)')
for sig in (0.005, 0.01):
    x = rng.normal(0, sig, (N, 4))
    A, B = arm_v(x, DEL, TAU)
    A2, B2 = arm_v(x, DEL, TAU, lo=0.29, hi=0.75)
    print(f'  σ {sig}: 지금 사다리 팔 {(A|B).mean():.3f} · 올린 사다리 팔 {(A2|B2).mean():.3f} → G 같음 {((A|B).mean())**36:.2e} · {((A2|B2).mean())**36:.2e}')
pA2 = (math.atan((0.75 + 0.5) / (math.sqrt(3) / 2)) - math.atan((0.29 + 0.5) / (math.sqrt(3) / 2))) / math.pi
print(f'  P(A | 잡음) 0.5–1.1 {pA:.4f} · 0.29–0.75 {pA2:.4f}')
print(f'  계산량 (12³+16³+24³+36³)/(8³+12³+16³+24³) = {(12**3+16**3+24**3+36**3)/(8**3+12**3+16**3+24**3):.3f} · 3.1 기본 대비 {(12**3+16**3+24**3+36**3)/(8**3+12**3+16**3):.2f}')

print('\n== 7. MR3-04 · "최악 예" 는 최악이 아님 · 숨은 느린 항 (A 꼴로 받힘) 의 진폭을 키우면')
def slow(lnR, A_, B_, sgn, p=0.1):
    return tuple(lnR + sgn * (A_ * n ** -p + B_ / n ** 2) for n in (8, 12, 16, 24))
c0 = arm((0.0, 0.0, 0.0, 0.0))          # F 상수 → B · ±δ
for lnR, A_, B_, sgn, p, tag in ((math.log(2.0), 1.0, 5.0, -1, 0.1, '참 R 2.00 (다름) · 아래에서 · p 0.1'),
                                 (1.08, 1.6, 8.0, -1, 0.1, f'참 R {math.exp(1.08):.2f} (다름) · 아래에서 · p 0.1'),
                                 (-L13, 0.95, 4.75, +1, 0.1, '참 R 0.769 (반대 · 문턱 포함) · 위에서 · p 0.1')):
    s = slow(lnR, A_, B_, sgn, p); a = arm(s)
    iv = (a[1] - c0[2], a[2] - c0[1]) if a[0] else None
    d1, d2 = s[2] - s[1], s[3] - s[2]
    print(f'  {tag}: A {A_} B {B_} → 비 {d2/d1:.3f} {a[0]} · ln R [{iv[0]:.4f}, {iv[1]:.4f}] → {grade([iv]*3)} · 24 셀 남은 오차 {abs(lnR - s[3]):.3f} · 단 변화 {abs(d1):.3f} · {abs(d2):.3f}')
# p 0.1 · 비 1.1 의 꼴 (B = 4.93 A) 에서 같음으로 숨길 수 있는 참 R 의 위 끝 (F 쪽 δ 포함)
g = lambda n, A_, B_, p: A_ * n ** -p + B_ / n ** 2
for p in (0.1, 0.05):
    best = None
    for A_ in np.linspace(0.05, 6, 1200):
        for kB in np.linspace(2.5, 8, 111):
            B_ = kB * A_
            s0 = slow(0.0, A_, B_, -1, p); a = arm(s0)
            if a[0] != 'A':
                continue
            lo, hi = a[1] - c0[2], a[2] - c0[1]            # lnR = 0 일 때의 구간 → lnR 만큼 평행이동
            # 같음: lnR + lo ≥ −ln1.15 · lnR + hi ≤ ln1.15 (충전 셋 같은 꼴 · 평균 = 각 값)
            lnR_max = L115 - hi
            if lnR_max + lo >= -L115 - 1e-12 and (best is None or lnR_max > best[0]):
                best = (lnR_max, A_, B_)
    print(f'  p {p}: 같음으로 인증되는 참 R 의 위 끝 ≈ {math.exp(best[0]):.2f} (A {best[1]:.2f} · B {best[2]:.2f}) [격자 탐색 · 위 끝은 p → 0 이면 한없이 커진다]')
print('  → 가정 밖에서는 등급이 참값과 무관할 수 있다 (같음 ← 참 R 2.0–3.0 (p 0.1) · 다름 ← 참 반대).  메모의 "최악 예 (R 1.30 · 1.00)" 는 예일 뿐 최악이 아니다')

print('\n== 8. MR3-03 의 대가 · |d₀| > τ 인 같은 부호 d₀ (표류의 증인) 를 버린다 · p 0.1 표류 + 잡음')
p = 0.1
dd2 = 24 ** -p - 16 ** -p
for sig in (0.003, 0.005):
    for c in (0.62, 0.66):
        base = np.array([c * n ** -p for n in (8, 12, 16, 24)])
        x = base + rng.normal(0, sig, (N, 4))
        A3, B3 = arm_v(x, DEL, TAU); A2_, B2_ = arm_v_r2(x, DEL, TAU)
        d0 = base[1] - base[0]
        print(f'  σ {sig} · c {c} (d₀ {d0:+.4f} · d₂ {c*dd2:+.4f} · 24 셀 남은 오차 {c*24**-p:.3f}): B 받힘 2 회차 {B2_.mean():.4f} · 3 회차 {B3.mean():.4f}')

print('\n== 9. F 띠 (3a) · 못닿음 충전 하나를 평균에 넣으면 (2 회차: 그 띠 점은 밖)')
nz = math.log(1.11)
ivs = [(CAP - nz, INF), (-0.05, 0.05), (-0.05, 0.05)]
ml = sum(a for a, b in ivs) / 3; mh = sum(b for a, b in ivs) / 3
band = (math.log(0.7), math.log(1.4))
state = '안' if (ml >= band[0] and mh <= band[1]) else ('밖' if (ml > band[1] or mh < band[0]) else '미정')
print(f'  Φ_d 0.95 · F(µ 0) 한 충전이 2.4 MPa 안에서 못 닿음 (F/NZ22 ≥ {2.4/1.11:.2f}) · 다른 둘 비 0.95–1.05 → 평균 아래 끝 {ml:.3f} (띠 위 끝 {band[1]:.3f}) → {state} (2 회차 판: 밖 → (라))')

print('\n== 10. MR3-07 고친 ⑤ 의 칼날이 폭 문턱 2.2 %p 로 옮겨 감 (탐색 값 · 가상 값 · 산술만)')
grid = [0.03, 0.05, 0.08, 0.12, 0.18, 0.27, 0.40, 0.60]
for tag, srch in (('폭 2.1 %p (표지)', [13.0, 13.3, 13.6, 13.8, 14.1, 14.4, 14.7, 15.1]),
                  ('폭 2.3 %p (표지 없음)', [13.0, 13.3, 13.6, 13.9, 14.2, 14.5, 14.8, 15.3])):
    width = max(srch) - min(srch)
    flag = width < 2.2
    start = min(range(8), key=lambda i: (abs(srch[i] - 11.5), grid[i]))
    judged0 = srch[start] - 1.2                     # 판정 상자가 탐색보다 1.2 %p 낮다고 둠 (상자 · 충전 차)
    cross = 10.0 <= judged0 <= 13.0
    out = '⑤ 보류' if (flag and cross) else ('가로지름 · σ_y* 0.03 "범위 끝 값" → (4-i) 면 생산 재료' if cross else '상태 그대로')
    print(f'  {tag}: 폭 {width:.1f} · 출발 {grid[start]} GPa · 판정 상자 그 점 {judged0:.1f} % (아래 끝이라 걷기 멈춤) → {out}')

print('\n== 11. U6 (b) "8 셀 치우침" 촉발 · 메모 자신의 해상도 숫자로 (BH01 3D 구 16 셀 약 4 % · 1 차 수렴 가정)')
e16 = math.log(1.04)
c = e16 * 16                       # 오차 c/n · 16 셀에서 ln 1.04
d0, d1, d2 = c / 12 - c / 8, c / 16 - c / 12, c / 24 - c / 16
print(f'  1 차 · 16 셀 오차 ln 1.04: d₀ {d0:+.4f} · d₁ {d1:+.4f} · d₂ {d2:+.4f} → A (비 {d2/d1:.2f}) · |d₀| > τ? {abs(d0) > TAU} → 촉발 (B 와 무관한 팔)')
