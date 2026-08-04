"""wang2025 (Angew 2025, 64, e202501411) — 본문 그림 픽셀 독립 검증.

2차 패스용. 1차 digest(2026-08-04, 본문+SI 텍스트 정독)와 다른 통로:
PDF 그림을 600-900 dpi 렌더 → 축 프레임/눈금을 픽셀로 잡고 → 막대·곡선을 실측.

의존: PyMuPDF + PIL 만 (numpy 없음 — zhou2026_si_verify.py / ren2026_fig_verify.py 선례 준용).

대상
  Fig 2c  : sigma / Ea 막대 (LPSC 값은 본문에 없고 그림에만 있다)
  Fig 5e  : PDOS — P-p 가 정말 VBM 에 있나 + band gap + O 2p 깊이

실행: python tools/litdb/wang2025_fig_verify.py [pdf경로]
"""
import sys
import fitz
from PIL import Image

try:                      # Windows 콘솔이 cp949 라 한글/em-dash 가 깨진다
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

PDF = sys.argv[1] if len(sys.argv) > 1 else (
    "litdb/inbox/52. Electronic Localization Enables Long-Cycling "
    "Sulfides-Based All-Solid-State Lithium Batteries.pdf")

# ---------------------------------------------------------------- helpers
def render(page, clip, dpi, out):
    pix = page.get_pixmap(dpi=dpi, clip=fitz.Rect(*clip))
    pix.save(out)
    return Image.open(out).convert("RGB")


def frame(im, min_h, min_v):
    """축 프레임(굵은 검은 선)의 행/열 인덱스."""
    W, H = im.size
    px = im.load()
    dark = lambda c: c[0] < 100 and c[1] < 100 and c[2] < 100
    rows = [y for y in range(H) if sum(1 for x in range(W) if dark(px[x, y])) > min_h]
    cols = [x for x in range(W) if sum(1 for y in range(H) if dark(px[x, y])) > min_v]
    return rows, cols


def top_of(px, x, y0, y1, test):
    """열 x 에서 test 를 만족하는 가장 위쪽 픽셀의 y."""
    for y in range(int(y0), int(y1)):
        if test(px[x, y]):
            return y
    return None


def height(px, x, y0, y1, test):
    """열 x 에서 test 색의 최대 높이(바닥 y1 기준, px)."""
    best = 0
    for y in range(int(y0), int(y1)):
        if test(px[x, y]):
            best = max(best, y1 - y)
    return best


# ---------------------------------------------------------------- Fig 2c
def fig2c(doc):
    """sigma / Ea 막대. 왼축 0-4 mS/cm, 오른축 0.25-0.45 eV."""
    im = render(doc[3], (375, 45, 545, 160), 600, "litdb/inbox/_52_f2c.png")
    px = im.load()
    rows, cols = frame(im, 600, 500)
    TOP, BOT = rows[0] + 2.5, rows[-1] + 2.5          # 값 4 / 값 0 의 y
    val = lambda y: (BOT - y) / (BOT - TOP) * 4.0
    is_blue = lambda c: c[2] > 150 and c[2] > c[0] + 30 and c[1] > 90
    is_red = lambda c: c[0] > 190 and c[0] > c[2] + 30 and c[1] < 170

    hits = {}
    for x in range(cols[-1 - 5] and cols[0] + 4, cols[-6]):
        for k, t in (("B", is_blue), ("R", is_red)):
            y = top_of(px, x, TOP, BOT, t)
            if y:
                hits.setdefault(k, []).append((x, y))

    def group(pts):
        out, cur = [], [pts[0]]
        for p in pts[1:]:
            if p[0] - cur[-1][0] <= 3:
                cur.append(p)
            else:
                if len(cur) > 25:
                    out.append(cur)
                cur = [p]
        if len(cur) > 25:
            out.append(cur)
        return out

    bb, rb = group(hits["B"]), group(hits["R"])
    med = lambda g: sorted(p[1] for p in g)[len(g) // 2]
    rows_out = []
    for i, lab in enumerate(["0", "0.02", "0.05", "0.08", "0.1"]):
        sig = val(med(bb[i]))
        ea = 0.25 + 0.05 * val(med(rb[i]))       # 오른축 0.25-0.45 를 0-4 에 매핑
        rows_out.append((lab, sig, ea))
    return rows_out


# ---------------------------------------------------------------- Fig 5e
def fig5e(doc):
    im = render(doc[7], (295, 150, 430, 285), 900, "litdb/inbox/_52_f5e_big.png")
    px = im.load()
    W, H = im.size
    dark = lambda c: c[0] < 110 and c[1] < 110 and c[2] < 110
    rows, _ = frame(im, 800, 700)
    # 프레임 가로선은 3덩어리(위 테두리 / 두 패널 경계 / 아래 축) — 덩어리로 묶는다
    bands, cur = [], [rows[0]]
    for a in rows[1:]:
        if a - cur[-1] <= 2:
            cur.append(a)
        else:
            bands.append(sum(cur) / len(cur))
            cur = [a]
    bands.append(sum(cur) / len(cur))
    Y_TOP, Y_MID, Y_BOT = int(bands[0]), int(bands[1]), int(bands[-1])

    # 아래축 바깥쪽 눈금 -> E 보정
    ticks = [x for x in range(W)
             if sum(1 for y in range(Y_BOT + 2, Y_BOT + 19) if dark(px[x, y])) > 10]
    cen, cur = [], [ticks[0]]
    for a in ticks[1:]:
        if a - cur[-1] <= 2:
            cur.append(a)
        else:
            cen.append(sum(cur) / len(cur))
            cur = [a]
    cen.append(sum(cur) / len(cur))
    x0, x1 = cen[0], cen[-1]                       # -6 eV, +6 eV
    scale = (x1 - x0) / 12.0
    E = lambda x: (x - x0) / scale - 6.0
    X = lambda e: int(round((e + 6.0) * scale + x0))

    is_S = lambda c: 120 < c[0] < 215 and 110 < c[1] < 200 and c[2] < 90
    is_P = lambda c: c[2] > 190 and c[1] > 140 and c[0] < 120
    is_Y = lambda c: 150 < c[0] < 230 and c[1] < 115 and 150 < c[2] < 240
    is_O = lambda c: c[0] > 200 and c[1] < 90 and 90 < c[2] < 190

    def edge(y0, y1, test, rng, thr=8, need=5):
        run = 0
        for x in rng:
            if height(px, x, y0, y1, test) >= thr:
                run += 1
                if run >= need:
                    return E(x - (need - 1) * (1 if rng.step > 0 else -1))
            else:
                run = 0
        return None

    out = {}
    # 상단 = LPSC
    out["LPSC_VBM"] = edge(Y_TOP, Y_MID, is_S, range(X(1.0), X(-2.0), -1))
    out["LPSC_CBM"] = edge(Y_TOP, Y_MID, is_S, range(X(0.5), X(6.0)))
    out["P_vs_S"] = [(e,
                      height(px, X(e), Y_TOP, Y_MID, is_P),
                      height(px, X(e), Y_TOP, Y_MID, is_S))
                     for e in (-4.4, -3.5, -2.0, -0.8, -0.2)]
    # 하단 = LPSC-YO
    out["YO_VBM"] = edge(Y_MID, Y_BOT, is_S, range(X(1.2), X(-2.0), -1))
    out["YO_CBM"] = edge(Y_MID, Y_BOT, is_S, range(X(0.6), X(6.0)))
    out["YO_at_VBM"] = [(e,
                         height(px, X(e), Y_MID, Y_BOT, is_S),
                         height(px, X(e), Y_MID, Y_BOT, is_Y),
                         height(px, X(e), Y_MID, Y_BOT, is_O))
                        for e in (-5.5, -2.8, -1.0, -0.55, 0.0)]
    # O 2p 가 얼마나 깊은가: 적분 무게의 deep 비율
    for key, test in (("O", is_O), ("S", is_S)):
        lo = sum(height(px, x, Y_MID, Y_BOT, test) for x in range(X(-6.0), X(-2.0)))
        hi = sum(height(px, x, Y_MID, Y_BOT, test) for x in range(X(-2.0), X(0.3)))
        out[key + "_deep_frac"] = 100.0 * lo / (lo + hi)
    return out


# ---------------------------------------------------------------- main
def main():
    doc = fitz.open(PDF)
    print("=" * 68)
    print("wang2025 Fig 2c — sigma / Ea 막대 실측 (x=0.05 행이 인쇄 라벨 3.53 / 0.34)")
    print("=" * 68)
    bars = fig2c(doc)
    print("  x       sigma(mS/cm)   Ea(eV)")
    for lab, s, e in bars:
        print("  %-6s   %6.2f       %.4f" % (lab, s, e))
    s0, e0 = bars[0][1], bars[0][2]
    s5, e5 = bars[2][1], bars[2][2]
    kT = 8.617333e-5 * 298.15
    import math
    pred = math.exp((e0 - e5) / kT)
    print("\n  LPSC  sigma %.2f mS/cm · Ea %.3f eV   (본문에 숫자 없음 — 그림만)" % (s0, e0))
    print("  LPSC-YO sigma %.2f mS/cm · Ea %.3f eV" % (s5, e5))
    print("  실측 sigma 비 = %.2f x" % (s5 / s0))
    print("  Ea 차 %.3f eV 만으로 기대되는 비(298 K) = %.2f x" % (e0 - e5, pred))
    print("  => 전지수인자(prefactor) 는 %.1f x **감소**해야 아귀가 맞는다." % (pred / (s5 / s0)))
    print("     (그들 설명은 'carrier 농도 증가' = prefactor 증가 — 방향이 반대)")
    print("     민감도: prefactor 감소 결론은 dEa > %.4f eV 이면 성립." % (kT * math.log(s5 / s0)))

    print()
    print("=" * 68)
    print("wang2025 Fig 5e — PDOS: 'p-p hybridization at the Fermi level' 검증")
    print("=" * 68)
    r = fig5e(doc)
    print("  [LPSC]  VBM %.2f eV · CBM %.2f eV  -> gap ~ %.2f eV"
          % (r["LPSC_VBM"], r["LPSC_CBM"], r["LPSC_CBM"] - r["LPSC_VBM"]))
    print("   E(eV)    P-p(px)  S-p(px)   P/S")
    for e, p, s in r["P_vs_S"]:
        print("   %+5.1f     %4d     %4d     %s"
              % (e, p, s, ("%.0f%%" % (100.0 * p / s)) if s else "-"))
    pk = max(p for _, p, _ in r["P_vs_S"])
    at_vbm = [p for e, p, _ in r["P_vs_S"] if e == -0.8][0]
    print("   => P-p 봉우리는 -4.4 eV (S-p 와 동급 = 진짜 p-p 결합상태).")
    print("      VBM 봉우리(-0.8 eV) 에서 P-p 는 자기 최대의 %.0f%% · S-p 의 %.0f%% 뿐."
          % (100.0 * at_vbm / pk, 100.0 * at_vbm / 457))
    print()
    print("  [LPSC-YO] VBM %.2f eV · CBM %.2f eV -> gap ~ %.2f eV"
          % (r["YO_VBM"], r["YO_CBM"], r["YO_CBM"] - r["YO_VBM"]))
    print("   E(eV)    S-p   Y-d   O-p  (px)")
    for e, s, y, o in r["YO_at_VBM"]:
        print("   %+5.2f   %4d  %4d  %4d" % (e, s, y, o))
    print("   O 2p 무게 중 E < -2 eV 비율 = %.0f%%   (S 3p 는 %.0f%%)"
          % (r["O_deep_frac"], r["S_deep_frac"]))
    print("   => O 2p 는 S 3p VBM 아래로 매몰. Y-d 는 VBM 에만 소량(S-p 대비 ~19%).")
    print()
    print("  ⚠ 이 gap 은 **그림에서 읽은 DOS-threshold 값**이다. 우리 canonical")
    print("    (fixed-occ nscf VBM/CBM 고유값) 규율상 절대값 인용 금지 — ±0.2-0.3 eV.")


if __name__ == "__main__":
    main()
