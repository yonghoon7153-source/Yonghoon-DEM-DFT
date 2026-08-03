"""jun2022 (JMCA 10, 7888) ESI 실물 독립 검증 — Table S1/S2/S3 재계산.

litdb/inbox 의 ESI PDF(20 pp)에서 뽑은 인쇄값만 입력으로 쓴다.
목적은 세 가지:

  (A) Table S1 의 Boltzmann 가중식(Eq 6-8)이 인쇄된 P_i 를 재현하는지, 그리고
      digest §8.2(d) 가 지목한 0.0028 셀이 실제로 식과 어긋나는지.
  (B) Table S2 의 chi_c^7.14 결정화도 보정 사슬(sigma_calc -> 0.8/0.7)이 닫히는지,
      그리고 Table S3 배열별 sigma 를 Eq 6-8 로 접으면 Table S2 의 chi_c=1.0 열이
      나오는지 (= 혼합을 보정 전에 하는지 후에 하는지 판정).
  (C) Table 2 의 STD 열이 Table S3 배열 STD 의 산술평균인지 (9개 조성 전수),
      그리고 기술자(STD)와 sigma 의 순위상관을 Table S3 27행에서 재계산.

scipy 없이 돌도록 Spearman/Pearson 을 직접 구현했다.
"""

import math
from itertools import groupby

KT = 25.85          # meV, T = 300 K
CHI_08 = 0.8 ** 7.14
CHI_07 = 0.7 ** 7.14


# ---------------------------------------------------------------- 통계 유틸
def _rank(xs):
    """평균 순위 (동점은 평균)."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = sum((a - mx) ** 2 for a in xs)
    syy = sum((b - my) ** 2 for b in ys)
    return sxy / math.sqrt(sxx * syy)


def spearman(xs, ys):
    return pearson(_rank(xs), _rank(ys))


def popstd(xs):
    n = len(xs)
    m = sum(xs) / n
    return math.sqrt(sum((x - m) ** 2 for x in xs) / n)


# ------------------------------------------------- ESI Table S1 (인쇄값 그대로)
# (Cl@4c 점유율, dE meV/atom, P_i(E), P_i(sigma), 곱, 정규화 P_i, sigma_RT mS/cm)
TABLE_S1 = [
    ("0%",   23, 0.4121, 1.0000, 0.4121, 0.6482,   0.02),
    ("25%",   4, 0.8678, 0.1739, 0.1509, 0.2373,  45.0),
    ("50%a",  0, 1.0000, 0.0114, 0.0114, 0.0179, 115.0),
    ("50%b", 11, 0.6450, 0.0028, 0.0018, 0.0029, 183.0),
    ("75%",  13, 0.6107, 0.0970, 0.0592, 0.0932,  60.0),
    ("100%",206, 0.0003, 0.9795, 0.0003, 0.0005,   0.57),
]
S1_BULK_PRINTED = 18.79

# ------------------------------------------------- ESI Table S2 (인쇄값 그대로)
# x: (chi=1.0, chi=0.8, chi=0.7)
TABLE_S2 = {
    0.0:  (18.79,  3.82,  1.47),
    0.25: (27.32,  5.55,  2.14),
    0.5:  (52.11, 10.59,  4.08),
    0.75: (142.89, 29.04, 11.19),
}

# ------------------------------------------------- ESI Table S3 (인쇄값 그대로, 27행)
# (X, x, 4a표기, 4c표기, Erel, r4aX, r4aS, r4cX, r4cS, STD, sigma_0.8)
# 반지름의 None = 인쇄된 "—" (그 자리에 해당 음이온종이 없음)
TS3 = [
    ("Cl", 0.25, "100/0", "25/75",  2.7, 2.68, None, 2.47, 2.42, 0.1174,  3.05),
    ("Cl", 0.25, "75/25", "50/50",  0.0, 2.62, 2.52, 2.50, 2.40, 0.0885, 10.57),
    ("Cl", 0.25, "50/50", "75/25",  8.4, 2.51, 2.54, 2.54, 2.44, 0.0601, 14.03),
    ("Cl", 0.25, "25/75", "100/0", 29.6, 2.40, 2.46, 2.58, None, 0.0817, 14.43),
    ("Cl", 0.5,  "100/0", "50/50",  8.5, 2.65, None, 2.50, 2.42, 0.0997,  8.13),
    ("Cl", 0.5,  "75/25", "75/25",  0.0, 2.57, 2.49, 2.51, 2.38, 0.0814, 13.01),
    ("Cl", 0.5,  "50/50", "100/0",  7.8, 2.48, 2.47, 2.54, None, 0.0517, 14.03),
    ("Cl", 0.75, "100/0", "75/25",  6.7, 2.59, None, 2.51, 2.38, 0.0894, 28.25),
    # 아래 행의 4c-S 칸은 ESI 에 "0.00" 으로 인쇄돼 있다 (D7). 물리적으로는 "—".
    ("Cl", 0.75, "75/25", "100/0",  0.0, 2.52, 2.47, 2.50, 0.00, 0.0335, 29.88),

    ("Br", 0.25, "100/0", "25/75",  0.0, 2.88, None, 2.67, 2.39, 0.2085,  1.04),
    ("Br", 0.25, "75/25", "50/50",  0.5, 2.74, 2.75, 2.63, 2.40, 0.1535,  6.10),
    ("Br", 0.25, "50/50", "75/25", 11.3, 2.70, 2.65, 2.67, 2.38, 0.1391, 13.21),
    ("Br", 0.25, "25/75", "100/0", 18.6, 2.57, 2.68, 2.66, None, 0.0833,  6.91),
    ("Br", 0.5,  "100/0", "50/50",  0.0, 2.78, None, 2.64, 2.40, 0.1617,  4.88),
    ("Br", 0.5,  "75/25", "75/25",  6.3, 2.70, 2.72, 2.62, 2.42, 0.1409, 15.65),
    ("Br", 0.5,  "50/50", "100/0",  8.0, 2.67, 2.75, 2.67, None, 0.0674,  8.74),
    ("Br", 0.75, "100/0", "75/25",  0.9, 2.74, None, 2.62, 2.40, 0.1407, 10.98),
    ("Br", 0.75, "75/25", "100/0",  0.0, 2.68, 2.70, 2.66, None, 0.0646, 19.51),

    ("I",  0.25, "100/0", "25/75",  0.0, 3.05, None, 2.76, 2.39, 0.2703, 0.0041),
    ("I",  0.25, "75/25", "50/50",  9.4, 2.93, 2.71, 2.83, 2.40, 0.2131,  4.47),
    ("I",  0.25, "50/50", "75/25", 20.1, 2.85, 2.63, 2.83, 2.39, 0.1919,  6.10),
    ("I",  0.25, "25/75", "100/0", 36.1, 2.70, 2.66, 2.83, None, 0.0896,  2.03),
    ("I",  0.5,  "100/0", "50/50",  0.0, 2.95, None, 2.79, 2.38, 0.2408,  1.08),
    ("I",  0.5,  "75/25", "75/25",  9.0, 2.90, 2.68, 2.79, 2.38, 0.2182,  5.69),
    ("I",  0.5,  "50/50", "100/0", 13.8, 2.84, 2.65, 2.85, None, 0.1111,  7.32),
    ("I",  0.75, "100/0", "75/25",  0.0, 2.93, None, 2.76, 2.39, 0.2282,  5.89),
    ("I",  0.75, "75/25", "100/0",  8.2, 2.85, 2.59, 2.81, None, 0.1271, 18.50),
]

# Table 2 (본문) 의 STD 열 인쇄값 — x=0 은 Table 1 6배열, x>0 은 Table S3
T2_STD = {
    ("Cl", 0.0): 0.1193, ("Cl", 0.25): 0.0869, ("Cl", 0.5): 0.0776, ("Cl", 0.75): 0.0615,
    ("Br", 0.0): 0.1688, ("Br", 0.25): 0.1461, ("Br", 0.5): 0.1233, ("Br", 0.75): 0.1027,
    ("I",  0.0): 0.2494, ("I",  0.25): 0.1912, ("I",  0.5): 0.1901, ("I",  0.75): 0.1776,
}

# Table 1 (본문, x=0) 의 STD — 4자리종류가 모두 있는 배열만 표시하기 위해 다중도도 기록
T1_STD = {
    "Cl": [("0%", 0.2391, 2), ("25%", 0.1034, 4), ("50%a", 0.0638, 4),
           ("50%b", 0.0931, 4), ("75%", 0.0826, 4), ("100%", 0.1336, 2)],
    "Br": [("0%", 0.2861, 2), ("25%", 0.1356, 4), ("50%a", 0.1166, 4),
           ("50%b", 0.1489, 4), ("75%", 0.1046, 4), ("100%", 0.2089, 2)],
    "I":  [("0%", 0.3479, 2), ("25%", 0.2265, 4), ("50%a", 0.2118, 4),
           ("50%b", 0.1676, 4), ("75%", 0.2142, 4), ("100%", 0.3285, 2)],
}


def boltzmann_mix(erels, sigmas, kt=KT):
    """ESI Eq (6)-(8). Delta sigma 는 최저 sigma 대비 차이를 그대로 kT 로 나눈다."""
    smin = min(sigmas)
    emin = min(erels)
    pe = [math.exp(-(e - emin) / kt) for e in erels]
    ps = [math.exp(-(s - smin) / kt) for s in sigmas]
    prod = [a * b for a, b in zip(pe, ps)]
    tot = sum(prod)
    p = [q / tot for q in prod]
    return sum(pi * si for pi, si in zip(p, sigmas)), p, pe, ps


def hr(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# =========================================================== (A) Table S1
hr("A. Table S1 — Eq (6)/(7) 이 인쇄된 P_i 를 재현하는가 (kT 역산)")
print(f"{'cfg':>6} {'dE':>5} {'P(E)인쇄':>9} {'kT역산':>7} | "
      f"{'dsig':>8} {'P(s)인쇄':>9} {'kT역산':>8} {'P(s)@300K':>10} {'배율':>6}")
smin = min(r[6] for r in TABLE_S1)
for name, de, pe, ps, prod, pn, sig in TABLE_S1:
    kt_e = (de / -math.log(pe)) if 0 < pe < 1 else float("nan")
    dsig = sig - smin
    kt_s = (dsig / -math.log(ps)) if 0 < ps < 1 and dsig > 0 else float("nan")
    ps_pred = math.exp(-dsig / KT)
    ratio = ps / ps_pred if ps_pred > 0 else float("nan")
    print(f"{name:>6} {de:5d} {pe:9.4f} {kt_e:7.2f} | "
          f"{dsig:8.2f} {ps:9.4f} {kt_s:8.2f} {ps_pred:10.6f} {ratio:6.2f}x")

sb = sum(r[5] * r[6] for r in TABLE_S1)
print(f"\n  sum(P_i * sigma_i) with printed P_i = {sb:.3f}  (인쇄 {S1_BULK_PRINTED})")
# 0.0028 대신 식대로 8.4e-4 를 넣으면?
fixed = list(TABLE_S1)
ps_fix = math.exp(-(183.0 - smin) / KT)
prods = []
for name, de, pe, ps, prod, pn, sig in TABLE_S1:
    prods.append(pe * (ps_fix if name == "50%b" else ps))
tot = sum(prods)
sb_fix = sum((q / tot) * r[6] for q, r in zip(prods, TABLE_S1))
print(f"  0.0028 -> {ps_fix:.2e} (식대로) 로 고치면 sigma_bulk = {sb_fix:.3f} mS/cm "
      f"({100*(sb_fix/S1_BULK_PRINTED-1):+.2f}%)")

# =========================================================== (B) chi_c 사슬
hr("B1. Table S2 — chi_c^7.14 보정 사슬이 닫히는가")
print(f"  0.8^7.14 = {CHI_08:.6f}   0.7^7.14 = {CHI_07:.6f}")
print(f"{'x':>5} {'chi=1.0':>9} {'*0.8^7.14':>11} {'인쇄0.8':>9} {'*0.7^7.14':>11} {'인쇄0.7':>9}")
for x, (c10, c08, c07) in TABLE_S2.items():
    print(f"{x:5} {c10:9.2f} {c10*CHI_08:11.3f} {c08:9.2f} {c10*CHI_07:11.3f} {c07:9.2f}")

hr("B2. Table S3 배열 sigma 를 Eq(6-8) 로 접으면 Table S2 의 chi=1.0 열이 나오는가")
print("   (핵심: 혼합을 chi_c 보정 '전' 의 원값에 하는가, '후' 의 값에 하는가)")
print(f"{'X':>3} {'x':>5} {'n':>2} {'mix(보정후)':>12} {'mix(보정전)':>12} "
      f"{'/0.8^7.14':>11} {'S2인쇄(1.0)':>12} {'Table2(0.8)':>12}")
T2_SIG = {("Cl", 0.25): 5.55, ("Cl", 0.5): 10.59, ("Cl", 0.75): 29.04,
          ("Br", 0.25): 3.28, ("Br", 0.5): 6.55, ("Br", 0.75): 12.42,
          ("I", 0.25): 1.58, ("I", 0.5): 2.75, ("I", 0.75): 6.67}
for X in ("Cl", "Br", "I"):
    for x in (0.25, 0.5, 0.75):
        rows = [r for r in TS3 if r[0] == X and r[1] == x]
        er = [r[4] for r in rows]
        s08 = [r[10] for r in rows]
        s10 = [v / CHI_08 for v in s08]
        mix_after, _, _, _ = boltzmann_mix(er, s08)
        mix_before, _, _, _ = boltzmann_mix(er, s10)
        printed10 = TABLE_S2[x][0] if X == "Cl" else None
        p10 = f"{printed10:12.2f}" if printed10 else f"{'—':>12}"
        print(f"{X:>3} {x:5} {len(rows):2d} {mix_after:12.2f} {mix_before:12.2f} "
              f"{mix_before*CHI_08:11.2f} {p10} {T2_SIG[(X,x)]:12.2f}")

# =========================================================== (C) Table 2 STD
hr("C1. Table 2 의 STD 열 = 배열 STD 의 단순 산술평균인가 (12셀 전수)")
print(f"{'X':>3} {'x':>5} {'n':>2} {'산술평균':>10} {'Table2인쇄':>11} {'차':>9}")
for X in ("Cl", "Br", "I"):
    stds0 = [s for _, s, _ in T1_STD[X]]
    m0 = sum(stds0) / len(stds0)
    print(f"{X:>3} {0.0:5} {len(stds0):2d} {m0:10.4f} {T2_STD[(X,0.0)]:11.4f} "
          f"{m0-T2_STD[(X,0.0)]:+9.4f}")
    for x in (0.25, 0.5, 0.75):
        rows = [r for r in TS3 if r[0] == X and r[1] == x]
        m = sum(r[9] for r in rows) / len(rows)
        print(f"{X:>3} {x:5} {len(rows):2d} {m:10.4f} {T2_STD[(X,x)]:11.4f} "
              f"{m-T2_STD[(X,x)]:+9.4f}")

hr("C2. 자리종류 수(=반지름 칸이 채워진 개수)가 배열마다 다르다 — 인구조사 효과")
print("   x=0 은 Table 1: ordered 2배열이 자리종류 2개, 나머지 4개")
print("   x>0 은 Table S3: '—' 가 있는 행은 자리종류 3개\n")
print(f"{'X':>3} {'x':>5} {'배열수':>6} {'자리종류4개':>11} {'<4개':>6} "
      f"{'전체평균STD':>12} {'4종류만평균':>12}")
for X in ("Cl", "Br", "I"):
    full0 = [s for _, s, n in T1_STD[X] if n == 4]
    all0 = [s for _, s, _ in T1_STD[X]]
    print(f"{X:>3} {0.0:5} {len(all0):6d} {len(full0):11d} {len(all0)-len(full0):6d} "
          f"{sum(all0)/len(all0):12.4f} {sum(full0)/len(full0):12.4f}")
    for x in (0.25, 0.5, 0.75):
        rows = [r for r in TS3 if r[0] == X and r[1] == x]
        def ntypes(r):
            # 4c-S 칸의 0.00 은 인쇄오류(D7), 실질 '—'
            vals = [r[5], r[6], r[7], (None if (r[8] in (None, 0.0)) else r[8])]
            return sum(v is not None for v in vals)
        full = [r[9] for r in rows if ntypes(r) == 4]
        allr = [r[9] for r in rows]
        fm = f"{sum(full)/len(full):12.4f}" if full else f"{'없음':>12}"
        print(f"{X:>3} {x:5} {len(allr):6d} {len(full):11d} {len(allr)-len(full):6d} "
              f"{sum(allr)/len(allr):12.4f} {fm}")

hr("C3. 기술자 성능 — Table S3 27행 순위상관 + 조성군 안의 순위 뒤집힘")
xs = [r[9] for r in TS3]
ys = [r[10] for r in TS3]
print(f"  전체 27행: Spearman rho = {spearman(xs, ys):+.3f} | "
      f"Pearson R2(sigma) = {pearson(xs, ys)**2:.3f} | "
      f"R2(log10 sigma) = {pearson(xs, [math.log10(v) for v in ys])**2:.3f}")
for X in ("Cl", "Br", "I"):
    sub = [r for r in TS3 if r[0] == X]
    a = [r[9] for r in sub]
    b = [r[10] for r in sub]
    print(f"  {X:>2} 9행    : Spearman rho = {spearman(a, b):+.3f} | "
          f"R2(log10) = {pearson(a,[math.log10(v) for v in b])**2:.3f}")

print("\n  조성군(X,x) 안에서 '최소 STD 배열'이 '최대 sigma 배열'인가:")
print(f"{'X':>3} {'x':>5} {'n':>2} {'minSTD행 sigma':>14} {'maxSigma':>9} {'일치':>5} {'rho':>7}")
inv = 0
for X in ("Cl", "Br", "I"):
    for x in (0.25, 0.5, 0.75):
        rows = [r for r in TS3 if r[0] == X and r[1] == x]
        lo = min(rows, key=lambda r: r[9])
        hi = max(rows, key=lambda r: r[10])
        ok = lo is hi
        if not ok:
            inv += 1
        rho = spearman([r[9] for r in rows], [r[10] for r in rows])
        print(f"{X:>3} {x:5} {len(rows):2d} {lo[10]:14.2f} {hi[10]:9.2f} "
              f"{'O' if ok else 'X':>5} {rho:+7.3f}")
print(f"\n  -> 9개 조성군 중 {inv}개에서 최소 STD 배열이 최속이 아니다.")

print("\n  뒤집힘이 일어난 군에서 '최소 STD' 를 가진 배열의 자리 점유:")
for X in ("Cl", "Br", "I"):
    for x in (0.25, 0.5, 0.75):
        rows = [r for r in TS3 if r[0] == X and r[1] == x]
        lo = min(rows, key=lambda r: r[9])
        hi = max(rows, key=lambda r: r[10])
        if lo is not hi:
            print(f"    {X} x={x}: minSTD = 4a {lo[2]} / 4c {lo[3]} "
                  f"(STD {lo[9]:.4f}, sigma {lo[10]:.2f})  vs  "
                  f"최속 4a {hi[2]} / 4c {hi[3]} (STD {hi[9]:.4f}, sigma {hi[10]:.2f})")

hr("C4. 최안정 배열(Erel=0)이 x 에 따라 어디로 이동하는가")
print(f"{'X':>3} {'x':>5} {'최안정 4a':>10} {'최안정 4c':>10} {'2위와의 차(meV/atom)':>22}")
for X in ("Cl", "Br", "I"):
    for x in (0.25, 0.5, 0.75):
        rows = sorted([r for r in TS3 if r[0] == X and r[1] == x], key=lambda r: r[4])
        gap = rows[1][4] - rows[0][4]
        print(f"{X:>3} {x:5} {rows[0][2]:>10} {rows[0][3]:>10} {gap:22.1f}")

hr("C5. 4a 를 X 로 꽉 채운 행(100/0)만 골라 x 에 따른 STD 추세 — 통제 비교")
print(f"{'X':>3} {'x=0.25':>8} {'x=0.5':>8} {'x=0.75':>8} {'추세':>18}")
for X in ("Cl", "Br", "I"):
    vals = []
    for x in (0.25, 0.5, 0.75):
        r = [r for r in TS3 if r[0] == X and r[1] == x and r[2] == "100/0"]
        vals.append(r[0][9] if r else float("nan"))
    trend = "감소" if vals[0] > vals[1] > vals[2] else "비단조"
    print(f"{X:>3} {vals[0]:8.4f} {vals[1]:8.4f} {vals[2]:8.4f} "
          f"{trend+f' ({100*(vals[2]/vals[0]-1):+.0f}%)':>18}")

hr("C6. Table S2 실험점에서 chi_c 를 역산하면 정말 70-80% 인가")
EXP = {0.0: [(3.10, "Jung"), (2.30, "Jung"), (2.5, "Adeli")],
       0.25: [(7.00, "Jung"), (5.10, "Jung"), (4.2, "Adeli")],
       0.5: [(10.20, "Jung"), (5.10, "Jung"), (12.0, "Adeli"), (5.9, "Adeli")]}
print(f"{'x':>5} {'sigma_calc':>11} {'sigma_exp':>10} {'출처':>7} {'역산 chi_c':>11}")
allchi = []
for x, pts in EXP.items():
    c10 = TABLE_S2[x][0]
    for s, src in pts:
        chi = (s / c10) ** (1 / 7.14)
        allchi.append(chi)
        print(f"{x:5} {c10:11.2f} {s:10.2f} {src:>7} {chi:11.3f}")
print(f"\n  역산 chi_c 범위 = {min(allchi):.3f} – {max(allchi):.3f} (n={len(allchi)})")
print(f"  70–80% 밖으로 나가는 점: "
      f"{sum(1 for c in allchi if c < 0.70 or c > 0.80)} / {len(allchi)}")
