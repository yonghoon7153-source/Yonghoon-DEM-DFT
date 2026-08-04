"""ren2026 (Li2ZrCl6 + Er/Nd, Authorea preprint) — Figure 3 픽셀 독립 검증.

목적
  1. Fig 3d/3e 의 y축 라벨이 "ln(D)" 인데 실제로 그려진 양이 log10(D) 임을 보인다.
  2. Methods 는 AIMD 온도를 600/700/800/900 K 로 적었는데 그림에는 1000/T = 2.0 (500 K)
     점이 하나 더 있고, 그 점이 600 K 점보다 위에 있다(= D(500K) > D(600K), 비아레니우스).
  3. 그 500 K 점을 빼고 600-900 K 만으로 재적합하면 Ea 가 약 2배로 커지고, 같은 논문의
     NEB 장벽(Er 0.5 = 0.370 eV)과 오히려 일치한다.
  4. 부수 검증: EIS 펠릿 기하(check_eis) · XRD 피크 위치 vs fcc LiCl(check_xrd) ·
     서술자 막대(check_descriptor) · 100 사이클 유지율(check_cycling).

결과 해설은 digest `litdb/papers/ren2026_li2zrcl6_low_ion_potential_doping.md` §20.

의존성: PIL 만 (numpy 없음). 원본 PDF 는 litdb/inbox/ 에 있다.
실행:  python tools/litdb/ren2026_fig_verify.py
"""
import os
from collections import deque

import fitz
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PDF = os.path.join(
    ROOT, "litdb", "inbox",
    "50. Regulation of the Lattice dynamics of Li2ZrCl6 solid electrolytes via "
    "low-ion-potential element doping for all-solid-state batteries.pdf",
)
PNG = os.path.join(ROOT, "litdb", "inbox", "_50_p15_600.png")
DPI = 600
KB = 8.617333262e-5  # eV/K

# 계열 대표색 (Origin 파스텔). Fig 3d = Er 계열, Fig 3e = Nd 계열, 색 순서 동일.
REF = {
    "c1": (140, 236, 205),   # 1번 legend = Li2ZrCl6
    "c2": (246, 175, 124),   # 2번 = x 0.125
    "c3": (178, 178, 222),   # 3번 = x 0.25
    "c4": (240, 158, 200),   # 4번 = x 0.375
    "c5": (194, 235, 143),   # 5번 = x 0.5
    "c6": (248, 223, 132),   # 6번 = x 0.625
}
SER = ["x=0", "x=0.125", "x=0.25", "x=0.375", "x=0.5", "x=0.625"]

# 인쇄된 Ea (그림 우상단 주석에서 육안 판독)
PRINTED = {
    "d": [0.2392, 0.3842, 0.3140, 0.2624, 0.1625, 0.1859],  # Er
    "e": [0.2392, 0.2070, 0.2046, 0.1893, 0.2818, 0.3069],  # Nd
}

# 패널 기하 (600 dpi 페이지 픽셀). 프레임/눈금은 아래 assert 로 실측 재확인한다.
PANEL = {
    # x0,x1,y0,y1(플롯 프레임) / x축: 1000/T=1.0 픽셀, 1단위당 픽셀 / y축: -4.6 픽셀, 0.2당 픽셀
    "d": dict(box=(815, 1832, 1972, 2850), x0px=815.0, xppu=924.5,
              y0px=2008.5, yppu=70.1818,
              mask_legend=(818, 1200, 2555, 2846), mask_text=(1620, 1832, 1972, 2325)),
    "e": dict(box=(2070, 3090, 1970, 2848), x0px=2070.5, xppu=928.0,
              y0px=2008.5, yppu=73.0,
              mask_legend=(2073, 2460, 2555, 2846), mask_text=(2875, 3090, 1970, 2325)),
}


def render():
    if os.path.exists(PNG):
        return
    doc = fitz.open(PDF)
    doc[14].get_pixmap(dpi=DPI).save(PNG)   # PDF 15쪽 = Figure 3


def blobs(px, name, P, tol=32, amin=150):
    """한 색 계열의 마커(데이터점) 중심을 연결성분으로 추출."""
    R, G, B = REF[name]
    x0, x1, y0, y1 = P["box"]
    lx0, lx1, ly0, ly1 = P["mask_legend"]
    tx0, tx1, ty0, ty1 = P["mask_text"]

    def ok(x, y):
        if lx0 <= x <= lx1 and ly0 <= y <= ly1:      # 범례 상자
            return False
        if tx0 <= x <= tx1 and ty0 <= y <= ty1:      # Ea 주석 텍스트
            return False
        r, g, b = px[x, y]
        return abs(r - R) <= tol and abs(g - G) <= tol and abs(b - B) <= tol

    seen, out = set(), []
    for y in range(y0 + 3, y1 - 3):
        for x in range(x0 + 3, x1 - 3):
            if (x, y) in seen or not ok(x, y):
                continue
            q, pts = deque([(x, y)]), []
            seen.add((x, y))
            while q:
                cx, cy = q.popleft()
                pts.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if x0 < nx < x1 and y0 < ny < y1 and (nx, ny) not in seen and ok(nx, ny):
                            seen.add((nx, ny))
                            q.append((nx, ny))
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            # 마커: 조밀하고 작다. 적합선은 가늘고 길어서 걸러진다.
            if len(pts) >= amin and 12 <= w <= 50 and 12 <= h <= 50 and len(pts) / (w * h) > 0.33:
                out.append((sum(xs) / len(xs), sum(ys) / len(ys)))
    return sorted(out)


def linefit_pixels(px, name, P, tol=26):
    """적합선 자체의 기울기 (마커가 아니라 그려진 직선)."""
    R, G, B = REF[name]
    x0, x1, y0, y1 = P["box"]
    lx0, lx1, ly0, ly1 = P["mask_legend"]
    tx0, tx1, ty0, ty1 = P["mask_text"]
    data = []
    for xc in range(x0 + 130, x1 - 40, 25):
        runs, cur = [], []
        for y in range(y0 + 3, y1 - 3):
            if (lx0 <= xc <= lx1 and ly0 <= y <= ly1) or (tx0 <= xc <= tx1 and ty0 <= y <= ty1):
                continue
            r, g, b = px[xc, y]
            if abs(r - R) <= tol and abs(g - G) <= tol and abs(b - B) <= tol:
                cur.append(y)
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        runs = [r for r in runs if len(r) <= 13]     # 두꺼우면 마커
        if len(runs) == 1:
            data.append((xc, sum(runs[0]) / len(runs[0])))
    return data


def ols(pts):
    n = len(pts)
    sx = sum(p[0] for p in pts)
    sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts)
    sxy = sum(p[0] * p[1] for p in pts)
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


def ea_from_slope(m, base10=True):
    """y = log10 D 이면 Ea = -m*kB*1000*ln10 ; y = ln D 이면 ln10 을 뺀다."""
    return -m * KB * 1000.0 * (2.302585 if base10 else 1.0)


# ============================================================================
# 나머지 그림 검증 (Fig 2b XRD / Fig 3g EIS / Fig 4b 서술자 / Fig 5g 사이클)
# 축 보정 상수는 전부 프레임·눈금 실측에서 얻었다 (본문 digest §18 참조).
# ============================================================================

PNG11 = os.path.join(ROOT, "litdb", "inbox", "_50_p11_600.png")   # Figure 2
PNG19 = os.path.join(ROOT, "litdb", "inbox", "_50_p19_600.png")   # Figure 4
PNG21 = os.path.join(ROOT, "litdb", "inbox", "_50_p21_600.png")   # Figure 5


def render_page(idx, path):
    if not os.path.exists(path):
        fitz.open(PDF)[idx].get_pixmap(dpi=DPI).save(path)


def _cc(px, ref, box, tol, amin, wmax=50, hmax=50, dens=0.33):
    """색 ref 에 맞는 연결성분 중심 목록."""
    R, G, B = ref
    x0, x1, y0, y1 = box
    ok = lambda x, y: (abs(px[x, y][0] - R) <= tol and abs(px[x, y][1] - G) <= tol
                       and abs(px[x, y][2] - B) <= tol)
    seen, out = set(), []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not ok(x, y):
                continue
            q, pts = deque([(x, y)]), []
            seen.add((x, y))
            while q:
                cx, cy = q.popleft()
                pts.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in seen and ok(nx, ny):
                            seen.add((nx, ny))
                            q.append((nx, ny))
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            if len(pts) >= amin and w <= wmax and h <= hmax and len(pts) / (w * h) > dens:
                out.append((sum(xs) / len(xs), sum(ys) / len(ys)))
    return sorted(out)


def check_eis():
    """Fig 3g: Nyquist 저항 실측 → 인쇄 σ 를 재현하는 펠릿 기하 역산.
    본문 Experimental: '직경 16 mm, 두께 약 1-2 mm'."""
    px = Image.open(PNG).convert("RGB").load()
    ohm = lambda x: (x - 3275.75) / (195.75 / 200.0)     # Z' = 0 픽셀, 200 ohm 당 195.75 px
    imag = lambda y: (2793.5 - y) / (219.7 / 200.0)
    SER = {"Li2.25Zr0.75Er0.25Cl6": ((246, 175, 124), 0.81),
           "Li2.25Zr0.75Nd0.25Cl6": ((178, 178, 222), 0.76),
           "Li2.5Zr0.5Er0.5Cl6":    ((240, 158, 200), 1.32),
           "Li2.375Zr0.625Nd0.375Cl6": ((194, 235, 143), 1.13)}
    print("\n" + "=" * 78)
    print("Fig 3g — EIS: 인쇄 sigma 를 재현하려면 펠릿 기하가 무엇이어야 하나")
    print("=" * 78)
    rows = [("Li2ZrCl6 (인셋)", 820.0, 0.227)]     # 인셋(Z' 700-1100) 최저점 육안+눈금 판독
    for nm, (ref, sig) in SER.items():
        ms = _cc(px, ref, (3327, 4045, 1974, 2846), 34, 60, dens=0.30)
        if not ms:
            continue
        pts = [(ohm(a), imag(b)) for a, b in ms]
        rows.append((nm, min(p[0] for p in pts), sig))
    import math
    for nm, R, sig in rows:
        out = []
        for d_mm in (16.0, 10.0):
            S = math.pi * (d_mm / 20.0) ** 2          # cm^2
            L = sig * 1e-3 * R * S * 10.0             # mm
            out.append(f"d={d_mm:.0f}mm -> 두께 {L:.2f} mm")
        print(f"  {nm:26s} R={R:6.1f} ohm, 인쇄 sigma={sig:.3f} mS/cm : " + " | ".join(out))
    print("  * 본문 명시 두께 = 1-2 mm. d=16 mm 로는 전부 범위 밖, d=10 mm 로는 전부 범위 안.")


def check_xrd():
    """Fig 2b: 도핑 시료의 날카로운 피크 위치 vs fcc LiCl."""
    render_page(10, PNG11)
    px = Image.open(PNG11).convert("RGB").load()
    X0, X1, YT, YB = 1980, 3179, 2450, 3348
    t2 = lambda x: 20 + (x - 2149.5) / 17.167          # 눈금 20/40/60/80도 실측
    SER = {"Li2ZrCl6": (40, 160, 95), "Li2.25Zr0.75Nd0.25Cl6": (225, 165, 40),
           "Li2.25Zr0.75Er0.25Cl6": (70, 190, 245),
           "Li2.375Zr0.625Nd0.375Cl6": (130, 160, 245), "Li2.5Zr0.5Er0.5Cl6": (190, 100, 245)}

    def trace(ref, tol=58):
        R, G, B = ref
        out = {}
        for x in range(X0, X1):
            ys = [y for y in range(YT, YB)
                  if abs(px[x, y][0] - R) <= tol and abs(px[x, y][1] - G) <= tol
                  and abs(px[x, y][2] - B) <= tol]
            if ys:
                out[x] = min(ys)
        xs = sorted(out)
        keep = {}
        for i, x in enumerate(xs):     # 텍스트 라벨(불연속)을 버린다
            nb = [out[xs[j]] for j in range(max(0, i - 2), min(len(xs), i + 3)) if xs[j] != x]
            if nb and min(abs(out[x] - v) for v in nb) <= 40:
                keep[x] = out[x]
        return keep

    def peaks(tr, win=13, minprom=8):
        xs = sorted(tr)
        res = []
        for i, x in enumerate(xs):
            if i < win or i > len(xs) - win - 1 or xs[i + win] - xs[i - win] > 3 * win:
                continue
            y = tr[x]
            seg = [tr[xs[j]] for j in range(i - win, i + win + 1)]
            if y != min(seg):
                continue
            prom = min(max(seg[:win]), max(seg[win + 1:])) - y
            if prom >= minprom:
                res.append([x, prom])
        out = []
        for x, p in res:
            if out and x - out[-1][0] <= 20:
                if p > out[-1][1]:
                    out[-1] = [x, p]
            else:
                out.append([x, p])
        return out

    print("\n" + "=" * 78)
    print("Fig 2b — XRD 날카로운 피크 위치 (2theta, 12-62도)")
    print("=" * 78)
    for nm, ref in SER.items():
        pk = sorted(t2(x) for x, p in peaks(trace(ref)) if 12 <= t2(x) <= 62)
        print(f"  {nm:26s}: " + ", ".join(f"{v:.1f}" for v in pk))
    print("  fcc LiCl (a=5.1396 A, Cu Ka) 예상 : 30.10(111), 34.89(200), 50.15(220), 59.62(311)")


def check_descriptor():
    """Fig 4b: 이온퍼텐셜 Phi 와 sigma 막대 높이를 재서 상관을 직접 계산."""
    render_page(18, PNG19)
    px = Image.open(PNG19).convert("RGB").load()
    X0, X1, Y0, Y1 = 852, 4153, 2225, 3441
    val = lambda y: (3443.1 - y) / 144.57 * 0.2        # 왼축 0.0-1.6 눈금 실측
    segs = []
    for y in range(Y0, Y1):
        x = X0
        while x < X1:
            if sum(px[x, y]) < 300:
                x2 = x
                while x2 + 1 < X1 and sum(px[x2 + 1, y]) < 330:
                    x2 += 1
                if 55 <= x2 - x <= 130:                 # 막대 상단 가로선
                    segs.append((y, x, x2))
                x = x2 + 1
            else:
                x += 1
    segs.sort(key=lambda s: (s[1], s[0]))
    grp = []
    for y, a, b in segs:
        if grp and abs(grp[-1][1] - a) < 12 and abs(y - grp[-1][3]) <= 3:
            grp[-1][3] = y
        else:
            grp.append([y, a, b, y])
    bars = []
    for y0, a, b, _ in grp:
        r, g, _b = px[(a + b) // 2, y0 + 18]
        bars.append((a, "pink" if r > g + 10 else "green", round(val(y0), 3)))
    print("\n" + "=" * 78)
    print("Fig 4b — 서술자 막대 실측 (pink = ionic potential, green = sigma)")
    print("=" * 78)
    print("  " + ", ".join(f"{c[:1]}{v}" for _, c, v in sorted(bars)))
    print("  * 상관은 digest §20.6 표 참조 (문헌 16계: Pearson -0.204 / Spearman -0.141).")


def check_cycling():
    """Fig 5g: 방전용량 첫점 대비 100 사이클 유지율."""
    render_page(20, PNG21)
    px = Image.open(PNG21).convert("RGB").load()
    R, G, B = (140, 236, 205)
    cap = []
    for x in range(1070, 4022):
        ys = [y for y in range(4697, 5813)
              if abs(px[x, y][0] - R) <= 34 and abs(px[x, y][1] - G) <= 34 and abs(px[x, y][2] - B) <= 34]
        runs = []
        for y in ys:
            if runs and y - runs[-1][-1] <= 3:
                runs[-1].append(y)
            else:
                runs.append([y])
        runs = [r for r in runs if len(r) >= 8]
        if len(runs) != 1:
            continue
        cap.append((5816.5 - sum(runs[0]) / len(runs[0])) / 207.0 * 60)   # 왼축 0-240, 60당 207 px
    print("\n" + "=" * 78)
    print("Fig 5g — 100 사이클 유지율")
    print("=" * 78)
    print(f"  첫 점 {cap[0]:.1f} -> 100 cyc {cap[-1]:.1f} mAh/g  => 유지율 {100*cap[-1]/cap[0]:.1f} %"
          f"   (본문 인쇄값 82.5 %)")


def main():
    render()
    px = Image.open(PNG).convert("RGB").load()
    for pan, tag in (("d", "Fig 3d — Er 계열"), ("e", "Fig 3e — Nd 계열")):
        P = PANEL[pan]
        calx = lambda x: 1.0 + (x - P["x0px"]) / P["xppu"]
        caly = lambda y: -4.6 - (y - P["y0px"]) / P["yppu"] * 0.2
        print("=" * 78)
        print(tag)
        print("=" * 78)
        for i, key in enumerate(REF):
            ms = blobs(px, key, P)
            pts = [(calx(a), caly(b)) for a, b in ms]
            pts.sort()
            lin = [(calx(a), caly(b)) for a, b in linefit_pixels(px, key, P)]
            pr = PRINTED[pan][i]
            print(f"\n  [{SER[i]}]  인쇄 Ea = {pr:.4f} eV")
            print("    마커: " + ", ".join(f"{1000/X:.0f}K→{Y:+.3f}" for X, Y in pts))
            if len(lin) >= 4:
                m = ols(lin)
                print(f"    그려진 적합선 기울기 → Ea(log10)={ea_from_slope(m):.4f} / "
                      f"Ea(ln)={ea_from_slope(m, False):.4f}")
            hi = [p for p in pts if p[0] < 1.75]     # 600-900 K
            if len(pts) >= 2:
                print(f"    마커 재적합 전체({len(pts)}점)      Ea = {ea_from_slope(ols(pts)):.4f}")
            if len(hi) >= 2:
                print(f"    마커 재적합 600-900K({len(hi)}점) Ea = {ea_from_slope(ols(hi)):.4f}")
            lo = [p for p in pts if p[0] >= 1.9]
            if lo and len(hi) >= 2:
                # 500 K 점이 600-900 K 외삽선 위/아래 어디에 있나
                m = ols(hi)
                c = sum(p[1] for p in hi) / len(hi) - m * sum(p[0] for p in hi) / len(hi)
                for X, Y in lo:
                    print(f"    500 K 점: 실측 {Y:+.3f} vs 600-900K 외삽 {m*X+c:+.3f} "
                          f"→ {Y-(m*X+c):+.3f} dex ({'위(비물리)' if Y > m*X+c else '아래'})")
    check_eis()
    check_xrd()
    check_descriptor()
    check_cycling()


if __name__ == "__main__":
    main()
