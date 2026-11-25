#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""huang2022 ESI Table S1/S2 결정구조 독립 재구성·검증.

Table S1(n-Li2SiS3, P4_2 2_1 2 #94) 원자좌표 + Table S2(간극자리)를
대칭연산으로 펼쳐 결합거리·조성·밀도를 다시 계산한다. 외부 패키지 없음.

    py -3.14 tools/litdb/huang2022_si_struct.py
"""
import math
import sys

# Windows 기본 콘솔이 cp949 라 em-dash 에서 죽는다 (digest §11 재현 시 확인).
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

A = 6.44743
C = 11.50292

# P4_2 2_1 2 (No. 94) 일반위치 8개
OPS = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (0.5 - y, 0.5 + x, 0.5 + z),
    lambda x, y, z: (0.5 + y, 0.5 - x, 0.5 + z),
    lambda x, y, z: (0.5 - x, 0.5 + y, 0.5 - z),
    lambda x, y, z: (0.5 + x, 0.5 - y, 0.5 - z),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (-y, -x, -z),
]

# Table S1 (Uiso, U11..U23 포함)
TS1 = {
    "Li1": ("4d", 0.866, (0.5, 0.0, 0.2682), 0.0923,
            (0.071, 0.151, 0.121, -0.054, 0.0, 0.0)),
    "Li2": ("8g", 0.552, (0.6089, 0.6777, 0.8520), 0.0923,
            (0.070, 0.021, 0.203, -0.019, 0.086, 0.013)),
    "M1":  ("4f", 1.0, (0.3438, 0.3438, 0.5), 0.0877,
            (0.1448, 0.1448, 0.1099, 0.0437, 0.0385, -0.0385)),
    "S1":  ("8g", 1.0, (0.22875, 0.2229, 0.34828), 0.0583,
            (0.0499, 0.162, 0.0460, 0.0208, 0.0001, -0.0247)),
    "S2":  ("4e", 1.0, (0.17030, 0.17030, 0.0), 0.0915,
            (0.1091, 0.1091, 0.154, -0.061, -0.090, 0.090)),
}
# Table S2 간극자리 (n-Li2SiS3)
TS2 = {
    "i1": (0.583, 0.097, 0.675),
    "i2": (0.403, 0.083, 0.825),
    "i3": (0.972, 0.028, 0.5),
}
MASS = {"Li": 6.941, "Si": 28.0855, "P": 30.9738, "S": 32.06}


def wrap(v):
    return v - math.floor(v)


def orbit(pos, tol=1e-4):
    out = []
    for op in OPS:
        p = tuple(wrap(v) for v in op(*pos))
        if not any(all(abs(a - b) < tol or abs(abs(a - b) - 1) < tol
                       for a, b in zip(p, q)) for q in out):
            out.append(p)
    return out


def cart(p):
    return (p[0] * A, p[1] * A, p[2] * C)


def dmin(p, q):
    """최소상 거리."""
    best = 1e9
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                v = (q[0] + dx - p[0], q[1] + dy - p[1], q[2] + dz - p[2])
                cx, cy, cz = v[0] * A, v[1] * A, v[2] * C
                d = math.sqrt(cx * cx + cy * cy + cz * cz)
                best = min(best, d)
    return best


def build():
    sites = []
    for nm, (wy, g, pos, _, _) in TS1.items():
        orb = orbit(pos)
        for p in orb:
            sites.append((nm, wy, g, p))
    return sites


def main():
    V = A * A * C
    print("=" * 74)
    print("1. 셀 / 조성 / 밀도")
    print(f"  a={A} c={C} -> V = {V:.4f} A^3")
    sites = build()
    cnt = {}
    for nm, wy, g, _ in sites:
        cnt[nm] = cnt.get(nm, 0) + 1
    for nm, (wy, g, pos, _, _) in TS1.items():
        m = cnt[nm]
        print(f"  {nm:4s} 표기 {wy}  대칭전개 다중도 {m}"
              f"  {'OK' if str(m) == wy[0] + (wy[1] if wy[0] == '8' else '') or m == int(wy[:-1]) else 'X'}"
              f"   점유 {g}  -> {m * g:.3f} /cell")
    nLi = sum(cnt[n] * TS1[n][1] for n in ("Li1", "Li2"))
    nM = cnt["M1"] * TS1["M1"][1]
    nS = sum(cnt[n] * TS1[n][1] for n in ("S1", "S2"))
    print(f"  셀당 Li {nLi:.3f} / M {nM:.1f} / S {nS:.1f}")
    print(f"  M 기준 화학식 : Li{nLi / nM:.3f}(Si0.97P0.03)S{nS / nM:.2f}")
    print(f"  Si=1 정규화   : Li{nLi / nM / 0.97:.3f}SiP{0.03 / 0.97:.4f}S{nS / nM / 0.97:.3f}")
    print("  Table S1 표기 : Li1.97Si0.97P0.03S3   / 본문 표기 : Li1.82SiP0.036S3")
    fw = (nLi / nM) * MASS["Li"] + 0.97 * MASS["Si"] + 0.03 * MASS["P"] + 3 * MASS["S"]
    rho = 4 * fw / (V * 0.6022140)
    print(f"  Table S1 조성 밀도 = {rho:.4f} g/cm3 (85 % -> {0.85 * rho:.4f})")
    fw2 = 1.82 * MASS["Li"] + MASS["Si"] + 0.036 * MASS["P"] + 3 * MASS["S"]
    print(f"  본문 조성 밀도    = {4 * 0.97 * fw2 / (V * 0.6022140):.4f} g/cm3")
    # 전하중성 (S 는 2- )
    for nm, li, si, p, s in (("Table S1", nLi / nM, 0.97, 0.03, nS / nM),
                             ("본문", 1.82, 1.0, 0.036, 3.0)):
        pos = li + 4 * si + 5 * p
        print(f"  전하수지 {nm:9s} : 양 {pos:.4f} / 음 {2 * s:.4f} -> 차 {pos - 2 * s:+.4f}")

    print("=" * 74)
    print("2. 변위인자 Uiso vs 이방성 Ueq=(U11+U22+U33)/3  [정방정: 교차항 0]")
    for nm, (wy, g, pos, uiso, u) in TS1.items():
        ueq = (u[0] + u[1] + u[2]) / 3
        rms = math.sqrt(max(u[:3]))
        print(f"  {nm:4s} Uiso={uiso:.4f}  Ueq={ueq:.4f}  Uiso/Ueq={uiso / ueq:.3f}"
              f"   max RMS 변위 = {rms:.3f} A")

    print("=" * 74)
    print("3. (Si/P)S4 사면체 — 이량체 확인")
    M = [p for nm, _, _, p in sites if nm == "M1"]
    S = [(nm, p) for nm, _, _, p in sites if nm.startswith("S")]
    for i, p in enumerate(M):
        ds = sorted((dmin(p, q), nm) for nm, q in S)[:5]
        mm = sorted(dmin(p, q) for q in M if q != p)[:2]
        print(f"  M{i + 1} {tuple(round(v, 4) for v in p)}")
        print("      M-S : " + "  ".join(f"{d:.4f}({nm})" for d, nm in ds[:4])
              + f"   5번째 {ds[4][0]:.4f}")
        print(f"      최근접 M-M : {mm[0]:.4f}, {mm[1]:.4f} A")
    # 공유 S 개수 = 이량체 판정
    p0, p1 = M[0], min((q for q in M[1:]), key=lambda q: dmin(M[0], q))
    sh = [nm for nm, q in S if dmin(p0, q) < 2.5 and dmin(p1, q) < 2.5]
    print(f"  최근접 M 쌍이 공유하는 S 개수 = {len(sh)} ({sh}) -> "
          f"{'edge-sharing' if len(sh) == 2 else 'corner' if len(sh) == 1 else '?'}")

    print("=" * 74)
    print("4. Li 자리·간극자리 배위 (Li-S)")
    allsites = {nm: [p for n2, _, _, p in sites if n2 == nm]
                for nm in ("Li1", "Li2", "M1", "S1", "S2")}
    for nm in ("Li1", "Li2"):
        p = allsites[nm][0]
        ds = sorted((dmin(p, q), n2) for n2, q in S)
        print(f"  {nm} {tuple(round(v, 4) for v in p)}  Li-S: "
              + "  ".join(f"{d:.3f}({n2})" for d, n2 in ds[:5]))
    for nm, pos in TS2.items():
        orb = orbit(pos)
        p = orb[0]
        ds = sorted((dmin(p, q), n2) for n2, q in S)
        dm = sorted(dmin(p, q) for q in allsites["M1"])[0]
        print(f"  {nm} {pos} (다중도 {len(orb)})  Li-S: "
              + "  ".join(f"{d:.3f}({n2})" for d, n2 in ds[:5])
              + f"   최근접 M {dm:.3f}")

    print("=" * 74)
    print("5. 본문이 말한 이동경로의 실제 도약거리")
    def near(p, cand):
        return sorted((dmin(p, q), q) for q in cand)[0]
    i1 = orbit(TS2["i1"])
    i2 = orbit(TS2["i2"])
    i3 = orbit(TS2["i3"])
    Li1, Li2 = allsites["Li1"], allsites["Li2"]
    print(f"  간극자리 다중도 : i1 {len(i1)}  i2 {len(i2)}  i3 {len(i3)}")
    for nm, a, b in (("Li2-i1", Li2, i1), ("i1-Li1", i1, Li1),
                     ("Li1-i2", Li1, i2), ("i2-Li2", i2, Li2),
                     ("Li2-i3", Li2, i3), ("Li1-Li2", Li1, Li2),
                     ("Li1-Li1", Li1, Li1), ("Li2-Li2", Li2, Li2)):
        best = min(dmin(p, q) for p in a for q in b
                   if not (a is b and p is q))
        print(f"  {nm:9s} 최단 {best:.4f} A")
    # i3 가 z=1/2 면(=M 이량체 면)에 있는가
    print(f"  i3 z 좌표 = {TS2['i3'][2]}  (M1 이량체 평면 z = 0.5)")
    print("  i3 = (x, -x, 1/2) 형 특수자리 : x=%.3f, -x mod1=%.3f"
          % (TS2["i3"][0], wrap(-TS2["i3"][0])))

    print("=" * 74)
    print("6. LiS4 연결방식 / Li-Li 배제 / i3 궤도 갈라짐  [E9 . E10 . E12]")

    # S 를 3x3x3 로 펼쳐 놓고 (직교좌표 키) LiS4 다면체를 이미지까지 구분해 잡는다.
    Ssuper = []
    for nm, q in S:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    Ssuper.append((nm, cart((q[0] + dx, q[1] + dy, q[2] + dz))))

    def s4(c):
        """직교좌표 c 를 중심으로 한 LiS4 (S 4개, 이미지 구분)."""
        ds = sorted((math.dist(c, sc), nm, sc) for nm, sc in Ssuper)
        return [(nm, tuple(round(v, 4) for v in sc)) for _, nm, sc in ds[:4]]

    # Li 를 -1..1 이미지까지 펼친다 (짝의 상대는 이웃 셀에 있을 수 있다).
    Lisuper = []
    for nm in ("Li1", "Li2"):
        for q in allsites[nm]:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        Lisuper.append((nm, cart((q[0] + dx, q[1] + dy, q[2] + dz))))

    print("  Li 층 z 좌표 (대칭전개):")
    for nm in ("Li1", "Li2"):
        zs = sorted({round(p[2], 3) for p in allsites[nm]})
        print(f"    {nm} z = " + " / ".join(f"{z:.3f}" for z in zs))

    # 짝 유형별로 (거리, 공유 S 개수, 셀당 짝수) 를 센다.
    print("  Li-Li 짝 : 거리 / 공유 S / 셀당 짝수 / 연결방식")
    seen = {}
    for nm_a in ("Li1", "Li2"):
        for pa in allsites[nm_a]:          # 홈셀 Li 만 중심으로
            ca = cart(pa)
            sa = set(s4(ca))
            for nm_b, cb in Lisuper:
                d = math.dist(ca, cb)
                if d < 0.1 or d > 3.6:
                    continue
                shared = len(sa & set(s4(cb)))
                key = (tuple(sorted((nm_a, nm_b))), round(d, 3), shared)
                seen[key] = seen.get(key, 0) + 1
    for (pair, d, shared), n in sorted(seen.items(), key=lambda kv: kv[0][1]):
        mode = {2: "edge", 1: "corner", 3: "face"}.get(shared, "isolated")
        # 홈셀 Li 를 양쪽 다 세었으므로 짝수는 절반
        print(f"    {pair[0]}-{pair[1]:4s} {d:.3f} A   공유 S {shared}"
              f"   셀당 {n // 2:2d} 쌍   -> {mode}")

    # 평균장 동시점유 기댓값 (BVSE 가 못 보는 것)
    g1, g2 = TS1["Li1"][1], TS1["Li2"][1]
    CUT = 2.75          # E10 이 쓰는 근접 접촉 컷오프
    gof = {"Li1": g1, "Li2": g2}
    exp, terms = 0.0, []
    for (pair, d, _shared), n in sorted(seen.items(), key=lambda kv: kv[0][1]):
        if d >= CUT:
            continue
        npair = n // 2
        t = npair * gof[pair[0]] * gof[pair[1]]
        exp += t
        terms.append(f"{npair}x{gof[pair[0]]}x{gof[pair[1]]}")
    print(f"  g(Li1)+g(Li2) = {g1} + {g2} = {g1 + g2:.3f}"
          f"  {'> 1 -> 2.4 A 짝이 배타적일 수 없다' if g1 + g2 > 1 else ''}")
    print(f"  평균장 기댓값 = {' + '.join(terms)} = "
          f"{exp:.2f} 접촉/cell (< {CUT} A),  셀 안 Li 는 {nLi:.2f} 개")

    # i3 궤도 4개와 짝 간격 (E12)
    print("  i3 궤도 4개 :")
    i3o = orbit(TS2["i3"])
    for p in i3o:
        print("    " + str(tuple(round(v, 3) for v in p)))
    pairs = sorted({round(dmin(p, q), 4) for p in i3o for q in i3o
                    if p is not q})
    print(f"    궤도 내 최단 간격 = {pairs[0]:.4f} A"
          f"  (특수자리에서 {pairs[0] / 2:.4f} A 씩 벗어난 형태)")


if __name__ == "__main__":
    main()
