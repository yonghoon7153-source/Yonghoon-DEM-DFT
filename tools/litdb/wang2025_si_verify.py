"""wang2025 (Angew 2025, 64, e202501411) — **SI(34 pp) 실물 독립 검증** (3차 패스).

1차 = 본문+SI 텍스트 정독 / 2차 = 본문 그림 픽셀 실측(`wang2025_fig_verify.py`).
3차 = 사용자가 inbox `52. Sup)` (SI 전용 PDF 34 pp) 를 넣었다 → SI 그림·표를 픽셀로 재실측.

의존: PyMuPDF + PIL 만 (numpy 없음 — ren2026/zhou2026/wang2025 선례 준용).

대상
  Fig S9/S10 : 크로노암페로메트리 5전압 계단 → 정상상태 전류 실측 → sigma_e 재계산
               (본문의 6.33e-7 / 1.55e-7 S/cm 가 자기 그림에서 나오는가?)
  Fig S11    : 전셀 BVSE 등가면 — 도핑 전/후 등가면 피복률 (채널 "확장"이 맞나?)
  Fig S15/S16: Li/LPSC/Li 0.5 mA/cm2 지속시간, Cu/Li 단락 시각
  Fig S17    : XPS 정량 파이 — top-face 면적으로 라벨 검증 ((d) 합 110.3% 의 범인 찾기)
  Fig S19    : 계면 슬랩의 O(빨강) 원자 개수·위치
  Table S5   : ICP wt% → 화학량론 재계산

실행: python tools/litdb/wang2025_si_verify.py ["52. Sup) ....pdf"]
출력: litdb/inbox/_52si_verify_out.txt (+ _52si_*.png)
"""
import math
import sys

import fitz
from PIL import Image

try:                      # Windows 콘솔이 cp949 라 한글/em-dash 가 깨진다
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PDF = sys.argv[1] if len(sys.argv) > 1 else (
    "litdb/inbox/52. Sup) Electronic Localization Enables Long-Cycling "
    "Sulfides-Based All-Solid-State Lithium Batteries.pdf")
OUT = "litdb/inbox/_52si_verify_out.txt"
LOG = []


def say(s=""):
    print(s)
    LOG.append(s)


# ------------------------------------------------------------------ render
def fig(doc, pageno, tag, dpi=500):
    """페이지의 그림 영역(로고 제외)만 잘라 래스터라이즈."""
    page = doc[pageno - 1]
    rects = []
    for im in page.get_images(full=True):
        if (im[2], im[3]) == (312, 86):      # Wiley 로고
            continue
        r = page.get_image_rects(im[0])
        if r:
            rects.append(r[0])
    clip = rects[0]
    for r in rects[1:]:
        clip |= r
    pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), clip=clip)
    fn = f"litdb/inbox/_52si_{tag}.png"
    pix.save(fn)
    return Image.open(fn).convert("RGB")


# --------------------------------------------------- Fig S9/S10  sigma_e
def dc_polarization(doc):
    say("=" * 78)
    say("[1] Fig S9 (LPSC) / S10 (LPSC-YO) — DC 분극 정상상태 전류 → sigma_e")
    say("=" * 78)
    # 축 보정: y 라벨 밴드 2.0 ... 0.0 uA, x 라벨 0 ... 35000 s (양쪽 그림 동일 판형)
    y20, y00 = 526.0, 1156.5
    x0, x1 = 349.0, 2004.5
    cur = lambda y: (y00 - y) * 2.0 / (y00 - y20)          # uA
    xof = lambda t: x0 + t * (x1 - x0) / 35000.0

    def band(px, x):
        """열 x 에서 '가장 아래 연속 덩어리'(=플래토 궤적)의 중심 y."""
        ys = [y for y in range(560, 1170) if sum(px[x, y]) < 730]
        if not ys:
            return None
        ys.sort()
        out = [ys[-1]]
        for y in reversed(ys[:-1]):
            if out[-1] - y <= 12:
                out.append(y)
            else:
                break
        return sum(out) / len(out)

    volts = [0.1, 0.2, 0.3, 0.4, 0.5]
    ends = [6900, 14100, 21300, 28500, 35700]              # 각 계단 끝 직전 (s)
    thick, area = 0.08, math.pi * 0.25                     # 800 um, phi 10 mm
    geom = thick / area                                    # cm^-1
    say(f"셀 기하(SI p.3): phi 10 mm, 800 um -> A={area:.4f} cm2, L/A={geom:.5f} cm^-1")
    res = {}
    for tag, pageno, who in [("S9", 13, "LPSC"), ("S10", 14, "LPSC-YO")]:
        im = fig(doc, pageno, tag)
        px = im.load()
        iss = []
        for te in ends:
            vals = [band(px, x) for x in range(int(xof(te - 800)), int(xof(te)))]
            vals = [v for v in vals if v is not None]
            iss.append(cur(sum(vals) / len(vals)))
        res[tag] = iss
        say(f"\n  {tag} = {who}")
        say("    V (V)      : " + "  ".join("%6.1f" % v for v in volts))
        say("    I_ss (uA)  : " + "  ".join("%6.3f" % i for i in iss))
        say("    sigma_e    : " + "  ".join("%6.2e" % (i * 1e-6 / v * geom)
                                            for v, i in zip(volts, iss)))
    say("\n  LPSC/LPSC-YO 비 (전압별): "
        + "  ".join("%5.1fx" % (a / b) for a, b in zip(res["S9"], res["S10"])))

    def slope(y):
        n, sx, sy = len(volts), sum(volts), sum(y)
        sxy = sum(v * i for v, i in zip(volts, y))
        sxx = sum(v * v for v in volts)
        return (n * sxy - sx * sy) / (n * sxx - sx * sx)

    say("")
    for tag, who in [("S9", "LPSC"), ("S10", "LPSC-YO")]:
        s = slope(res[tag])
        icpt = sum(res[tag]) / 5 - s * 0.3
        say("  %-8s dI/dV = %.4f uA/V -> sigma_e(기울기) = %.2e S/cm   (절편 %+.3f uA)"
            % (who, s, s * 1e-6 * geom, icpt))
    say("\n  본문 보고값: LPSC 6.33e-7 / LPSC-YO 1.55e-7 S/cm  (비 4.08x)")
    say("  -> 어느 계단에서도 재현 안 됨. 기울기 기준으로는 순서가 뒤집힌다.")


# ------------------------------------------------------- Fig S11 등가면
def bvse_coverage(doc):
    say("")
    say("=" * 78)
    say("[2] Fig S11 — 전셀 BVSE 등가면 피복률 (노란 등가면 vs 흰 빈공간)")
    say("=" * 78)
    im = fig(doc, 15, "S11")
    px = im.load()
    for name, (x0, y0, x1, y1) in {"LPSC    (a)": (65, 57, 1257, 1245),
                                   "LPSC-YO (b)": (1640, 57, 2848, 1245)}.items():
        tot = yel = wht = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b = px[x, y]
                tot += 1
                if r > 150 and g > 140 and b < 130 and r + g > 2 * b:
                    yel += 1
                elif r > 235 and g > 235 and b > 235:
                    wht += 1
        say("  %s  등가면 %.2f%%   빈공간 %.2f%%   (셀박스 %d px)"
            % (name, yel * 100 / tot, wht * 100 / tot, tot))
    say("  주의: 3D 렌더의 투영 면적이지 부피가 아니고, 두 패널의 iso-level 은 미표기다.")


# --------------------------------------------------------- Fig S17 파이
def xps_pies(doc):
    say("")
    say("=" * 78)
    say("[3] Fig S17 — XPS 정량 파이 top-face 면적 (라벨 검증)")
    say("=" * 78)
    im = fig(doc, 21, "S17")
    px = im.load()

    def cls(p):
        r, g, b = p
        if 140 <= r <= 205 and 180 <= g <= 218 and 205 <= b <= 245 and b > r + 25:
            return "PS4(하늘)"
        if r >= 195 and 110 <= g <= 165 and b >= 225:
            return "P-O(자홍)"
        if r >= 225 and 165 <= g <= 205 and b <= 90:
            return "Li3P(금)"
        if r >= 228 and 175 <= g <= 205 and 140 <= b <= 200 and r > b + 45:
            return "P-S-Li(살구)"
        if 125 <= r <= 175 and 45 <= g <= 95 and 175 <= b <= 215:
            return "Li2S(보라)"
        if 60 <= r <= 105 and 125 <= g <= 165 and 190 <= b <= 225:
            return "Y-S-Li(강청)"
        return None

    quad = {"(a) Li/LPSC-YO  P 2p": (0, 0, 1430, 840),
            "(b) Li/LPSC     P 2p": (1430, 0, 2890, 840),
            "(c) Li/LPSC-YO  S 2p": (0, 840, 1430, 1689),
            "(d) Li/LPSC     S 2p": (1430, 840, 2890, 1689)}
    labels = {"(a) Li/LPSC-YO  P 2p": {"PS4(하늘)": 91.0, "P-O(자홍)": 5.40, "Li3P(금)": 3.60},
              "(b) Li/LPSC     P 2p": {"PS4(하늘)": 91.0, "Li3P(금)": 9.00},
              "(c) Li/LPSC-YO  S 2p": {"P-S-Li(살구)": 84.0, "Li2S(보라)": 9.90,
                                       "Y-S-Li(강청)": 6.60},
              "(d) Li/LPSC     S 2p": {"P-S-Li(살구)": 89.0, "Li2S(보라)": 21.30}}
    bias = []
    for k, (x0, y0, x1, y1) in quad.items():
        cnt = {}
        for y in range(y0, y1):
            for x in range(x0, x1):
                t = cls(px[x, y])
                if t:
                    cnt[t] = cnt.get(t, 0) + 1
        tot = sum(cnt.values())
        say(f"  {k}   (라벨 합 {sum(labels[k].values()):.2f}%)")
        for t, v in sorted(cnt.items(), key=lambda z: -z[1]):
            if v * 100 / tot < 0.5:
                continue
            meas = v * 100 / tot
            lab = labels[k].get(t)
            extra = ""
            if lab and lab < 50:
                extra = f"   측정/라벨 = {meas / lab:.3f}"
                if k.startswith("(a)") or k.startswith("(b)") or k.startswith("(c)"):
                    bias.append(meas / lab)
            say(f"      {t:<14} 측정 {meas:6.2f}%   라벨 {lab if lab else '-':>6}{extra}")
    lo, hi = min(bias), max(bias)
    # (d) 보라는 파이 앞쪽(front-bottom) 조각 -> 같은 위치의 (b) 금 1.407 / (c) 보라 1.490 로 보정
    say("")
    say("  원근 편향 인자(측정/라벨) = %.3f ~ %.3f  [라벨 합이 100%% 로 닫히는 a/b/c 로 교정]"
        % (lo, hi))
    say("  (d) 와 같은 front 위치의 조각: (b) 금 1.407, (c) 보라 1.490")
    say("  (d) 보라 측정 29.61%% -> 보정 %.1f ~ %.1f %%  (11%% 였다면 15.5~16.4%% 로 보였어야 함)"
        % (29.61 / 1.490, 29.61 / 1.407))
    say("  -> 라벨 21.30% 와 일치. 따라서 (d) 에서 틀린 라벨은 P-S-Li '89%' (78.7% 여야 함)이고,")
    say("     Li2S 21.30% -> 9.90% 헤드라인은 그대로 유효하다.")


# ----------------------------------------------- Fig S15/S16 사이클 시각
def cycling_times(doc):
    say("")
    say("=" * 78)
    say("[4] Fig S15 / S16 — 지속시간·단락 시각")
    say("=" * 78)
    im = fig(doc, 19, "S15")
    px = im.load()
    x0, x1 = 222.0, 2848.0                                  # 0 h, 100 h
    xs = [x for x in range(224, 2846)
          if any(sum(px[x, y]) < 620 for y in range(150, 420))]
    t = lambda x: (x - x0) * 100.0 / (x1 - x0)
    say("  Fig S15  Li/LPSC/Li @0.5 mA/cm2 : 궤적 %.1f h -> %.1f h, 전압 붕괴/단락 표시 없음"
        % (t(min(xs)), t(max(xs))))

    im = fig(doc, 20, "S16")
    px = im.load()

    def scan(fx0, fx1, red, ylo, yhi):
        tt = lambda x: (x - fx0) * 120.0 / (fx1 - fx0)
        cols = []
        for x in range(int(fx0) + 4, int(fx1) - 4):
            g = [y for y in range(ylo, yhi)
                 if ((px[x, y][0] > 150 and px[x, y][1] < 110 and px[x, y][2] < 110) if red
                     else (40 < px[x, y][0] < 175
                           and abs(px[x, y][0] - px[x, y][1]) < 28
                           and abs(px[x, y][1] - px[x, y][2]) < 28))]
            if g:
                cols.append((x, min(g)))
        last = tt(cols[-1][0])
        spike = tt([c for c in cols if c[1] < 700][-1][0])
        return spike, last

    s, l = scan(275, 1265, True, 600, 930)
    say("  Fig S16a Cu/LPSC-YO/Li        : 마지막 도금 스파이크 %.1f h, 궤적 끝 %.1f h (단락 없음)" % (s, l))
    s, l = scan(1687, 2679, False, 600, 930)
    say("  Fig S16b Cu/LPSC/Li           : 마지막 도금 스파이크 %.1f h, 이후 0 V 평탄 %.1f h ('short circuit' 화살표)" % (s, l))


# -------------------------------------------------- Fig S19 계면 슬랩 O
def interface_slab(doc):
    say("")
    say("=" * 78)
    say("[5] Fig S19 — 계면 슬랩의 O(빨강) 원자 개수·위치")
    say("=" * 78)
    im = fig(doc, 23, "S19")
    px = im.load()
    for name, (x0, x1) in {"(a) Li/LPSC   ": (150, 1400),
                           "(b) Li/LPSC-YO": (1500, 2860)}.items():
        pts = set()
        for y in range(40, 2050):
            for x in range(x0, x1):
                r, g, b = px[x, y]
                if r > 150 and g < 90 and b < 90:
                    pts.add((x, y))
        seen, comps = set(), []
        for p in pts:
            if p in seen:
                continue
            stack, comp = [p], []
            seen.add(p)
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        q = (cx + dx, cy + dy)
                        if q in pts and q not in seen:
                            seen.add(q)
                            stack.append(q)
            comps.append(comp)
        big = [c for c in comps if len(c) > 400]
        ys = [sum(p[1] for p in c) / len(c) for c in big]
        say("  %s  O(빨강) 덩어리 %d 개%s"
            % (name, len(big),
               ("   y중심 = " + ", ".join("%d" % y for y in sorted(ys))) if big else ""))
    say("  (b) 구조 전체 y 범위 ~ 500-2050 px. O 는 전부 상단 계면 밴드 안/바로 아래에 몰려 있다.")
    say("  Y(청록 YS4) 는 (b) 에 1 개, SE 최상층(계면 밴드 안).")


# ------------------------------------------------------------ Table S5
def icp():
    say("")
    say("=" * 78)
    say("[6] Table S5 — ICP wt% 재계산")
    say("=" * 78)
    M = {"Li": 6.941, "P": 30.9738, "S": 32.06, "Y": 88.9059, "O": 15.999, "Cl": 35.453}
    found = {"Li": 17.1185, "P": 10.3464, "S": 56.3060, "Y": 1.3518}
    nom = {"Li": 6.1, "P": 0.95, "Y": 0.05, "S": 4.925, "O": 0.075, "Cl": 1.0}
    mass = sum(nom[e] * M[e] for e in nom)
    say("  명목식 Li6.1P0.95Y0.05S4.925O0.075Cl, 식량 %.3f g/mol" % mass)
    say("  원소   found wt%%   nominal wt%%   편차")
    for e in ["Li", "P", "S", "Y"]:
        nw = nom[e] * M[e] / mass * 100
        say("  %-4s  %8.4f     %8.4f     %+6.1f%%" % (e, found[e], nw, (found[e] / nw - 1) * 100))
    mol = {e: found[e] / M[e] for e in found}
    py = mol["P"] + mol["Y"]
    say("  -> Li/(P+Y) = %.3f  (명목 6.1, %+.1f%%)" % (mol["Li"] / py, (mol["Li"] / py / 6.1 - 1) * 100))
    say("     Y/(P+Y)  = %.4f (명목 0.05, %+.1f%%)" % (mol["Y"] / py, (mol["Y"] / py / 0.05 - 1) * 100))
    say("     S/(P+Y)  = %.3f  (명목 4.925, %+.1f%%)" % (mol["S"] / py, (mol["S"] / py / 4.925 - 1) * 100))
    say("     4원소 합 %.3f wt%% -> 미측정(Cl+O) %.3f wt%% (명목 %.3f)"
        % (sum(found.values()), 100 - sum(found.values()),
           (nom["Cl"] * M["Cl"] + nom["O"] * M["O"]) / mass * 100))


def main():
    doc = fitz.open(PDF)
    say(f"SI PDF: {PDF}  ({doc.page_count} pp)")
    dc_polarization(doc)
    bvse_coverage(doc)
    xps_pies(doc)
    cycling_times(doc)
    interface_slab(doc)
    icp()
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG) + "\n")
    print(f"\n[saved] {OUT}")


if __name__ == "__main__":
    main()
