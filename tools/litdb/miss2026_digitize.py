#!/usr/bin/env python3
"""miss2026_digitize.py — Miß, Lange, Staubitz, Roling, ACS Appl. Mater. Interfaces 18, 32830 (2026) **그림 판독 + 표 재계산**.

카드: litdb/papers/miss2026_insitu_conductivity_porosity_pressure_compaction.md  (§3 · §7 · §10)
원본: 본문 PDF (7 쪽, ACS) + SI PDF (7 쪽).  ⚠ PDF 는 리포에 없다.  그림 3 · 4 · S4 는 전부 **내장 래스터**다 — 벡터 좌표가 없다.

⛔ 이 스크립트가 내는 그림 값은 전부 **판독 (digitized)** 이다.  카드·표에 옮길 때 `판독` 표지를 떼지 말 것.
   논문이 숫자로 적은 것은 SI 표 S1 · S2 (질량 · 지름 · ρ0 · E · 압력별 두께) 와 본문 문장 몇 개뿐이다.

무엇을 하나
  (1) 표 S2 재계산 (`--check`): 압력별 회복률 d_min/d_load − 1 · 식 4 의 Δd_elastic · 공극 세 규약
      (인쇄된 식 2 = d + Δd (Δd<0) · 보정 없음 · d + |Δd|) — 표 S1 의 "지름 0.5 cm" 를 반지름으로 읽어야 (r = 0.5 cm)
      본문 공극 (10 MPa ≈0.30) 이 나온다 (지름이면 ε = −1.8).
  (2) 판독: Fig. 3a 밀어낸 SE 펠릿 두께 (파랑 ◆) · Fig. 3b σ_ion · Fig. 4a 공극 (닫힌 ● 가압 중 / 열린 □ 제거 뒤) ·
      Fig. 4b σ vs ε · Fig. S4a 밀어낸 NMC622 펠릿 두께 · Fig. S4b σ_e.
방법
  · 축: 축선에 붙은 눈금 (Fig. 3b · 4 · S4) 의 픽셀 중심 → 선형 최소제곱 (Fig. 4b y 는 log10).  Fig. 3a · S4a 두께 축은
    **인쇄된 표 S2 두께** (가압 중 + 제거 뒤 마커) 로 보정 — 잔차를 출력한다 (기대: < 1 µm).
  · 마커: 색 마스크의 연결성분.  Fig. 4a 의 열린 □ 는 닫힌 ● 위에 불투명 흰 속으로 덧그려져 겹친다 →
    □ = 막힌 구멍 (binary_fill_holes − 마스크) 의 중심, ● = 5×5 침식 뒤 아래 가장자리 − 반지름 (가려진 원에 견고).
검증 (`--check` 가 출력)
  · Fig. 3a 보정: 인쇄 두께 23 점 최대 잔차 ≈0.5 µm · Fig. S4a: 15 점 ≈0.2 µm.
  · Fig. 3b: σ_파랑/σ_검정 = d_밖/d_가압(p) 항등식 (본문 정의) 이 판독에서 ≲1 % 로 성립.
  · Fig. 4a 열린 □ 판독 = 표 S2 d_min 재계산 (r = 0.5 cm) 과 ≲0.0015 (p ≥ 150 MPa).
usage
  python3 tools/litdb/miss2026_digitize.py --pdf "<본문>.pdf" --si "<SI>.pdf" [--out litdb/figures/<slug>/digitized.csv] [--check]
  python3 tools/litdb/miss2026_digitize.py --check-only     # PDF 없이 표 S2 재계산만
"""
import argparse
import csv
import math
import sys
from pathlib import Path

SLUG = "miss2026_insitu_conductivity_porosity_pressure_compaction"
ROOT = Path(__file__).resolve().parents[2]

# ---- 인쇄값 (SI p.6, 표 S1 · S2) ------------------------------------------------------------
M_L, M_N = 0.0802, 0.0800                 # g   (표 S1: 80.2 · 80.0 mg)
RHO_L, RHO_N = 1.87, 4.48                 # g/cm3 (표 S1, ref 1 Adeli 2019 · ref 5 Hua 2020)
E_L, E_N = 67e3, 180e3                    # MPa (표 S1, ref 6 · ref 7)
R_CM = 0.5                                # cm — 표 S1 "Diameter 0.5 cm" 를 반지름으로 읽는다 (재현 근거 = --check)
P_L = [10, 20, 30, 40, 50, 70, 100, 150, 200, 250, 300, 350, 400]
D_L = [0.77875, 0.736875, 0.71625, 0.701875, 0.680625, 0.66375, 0.6475, 0.620625, 0.604375, 0.5925, 0.588,
       0.575625, 0.566875]
DM_L = [0.778125, 0.744375, 0.718125, 0.7, 0.6875, 0.669375, 0.66, 0.634375, 0.6175, 0.603125, 0.5975, 0.588125,
        0.5825]
DS_L = [0.000116, 0.000222, 0.000322, 0.000418, 0.000513, 0.000700, 0.000985, 0.001421, 0.001844, 0.002251,
        0.002671, 0.003072, 0.003478]
P_N = [50, 100, 150, 200, 250, 300, 350, 400]
D_N = [0.343125, 0.32625, 0.311875, 0.29625, 0.285625, 0.276875, 0.26875, 0.264375]
DM_N = [0.345625, 0.33375, 0.321875, 0.31125, 0.304375, 0.29875, 0.291875, 0.283125]
DS_N = [0.000096, 0.000185, 0.000268, 0.000346, 0.000423, 0.000497, 0.000567, 0.000629]


def eps(m, rho, d_mm, r_cm=R_CM):
    return 1.0 - m / (math.pi * r_cm ** 2 * (d_mm / 10.0) * rho)


def check_table():
    print("== 표 S1 '지름 0.5 cm' 판별 (SE, 10 MPa, d 0.77875 mm)")
    for r in (0.25, 0.5):
        print(f"   r = {r} cm → ε = {eps(M_L, RHO_L, D_L[0], r):+.3f}")
    for name, P, D, DM, DS, m, rho, E in (("µc-Li5.5PS4.5Cl1.5", P_L, D_L, DM_L, DS_L, M_L, RHO_L, E_L),
                                          ("pc-NMC622", P_N, D_N, DM_N, DS_N, M_N, RHO_N, E_N)):
        print(f"== {name}: p · 회복 d_min/d_load−1 · Δd 식4 재계산 vs 인쇄 · ε 가압중 [식2 인쇄 | 보정없음 | d+|Δd|] · ε 제거뒤")
        for p, d, dm, ds in zip(P, D, DM, DS):
            print(f"   {p:3d}  {dm / d - 1:+7.3%}  {dm * p / E:.6f} vs {ds:.6f}  "
                  f"[{eps(m, rho, d - ds):.4f} | {eps(m, rho, d):.4f} | {eps(m, rho, d + ds):.4f}]  {eps(m, rho, dm):.4f}")


# ---- 판독 ----------------------------------------------------------------------------------
def _np():
    import numpy as np
    from PIL import Image
    from scipy import ndimage as ndi
    return np, Image, ndi


def page_rasters(pdf, pno):
    """쪽 pno (1-based) 의 내장 이미지들 → [(bbox, RGB ndarray)] (위→아래, 왼→오른 순)."""
    import fitz
    np, Image, _ = _np()
    doc = fitz.open(pdf)
    page = doc[pno - 1]
    out = []
    for info in page.get_image_info(xrefs=True):
        pix = fitz.Pixmap(doc, info["xref"])
        if pix.n - pix.alpha >= 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].astype(int)
        out.append((tuple(info["bbox"]), arr))
    out.sort(key=lambda t: (round(t[0][1]), t[0][0]))
    return out


def lin(pos, val):
    np, _, _ = _np()
    pos, val = np.asarray(pos, float), np.asarray(val, float)
    A = np.vstack([np.ones(len(pos)), pos]).T
    c, *_ = np.linalg.lstsq(A, val, rcond=None)
    return c, float(np.max(np.abs(val - A @ c)))


def ticks(g, axis, line, lo, hi, side, start, thr=170, minlen=3, maxlen=20):
    """축선에 붙은 눈금 → [(중심, 길이)].  axis 'v' = 세로 축선(열 line), 'h' = 가로 축선(행 line)."""
    np, _, _ = _np()
    runs = []
    hi = min(hi, g.shape[0] if axis == "v" else g.shape[1])
    lo = max(lo, 0)
    for t in range(lo, hi):
        n = 0
        for k in range(start, start + maxlen):
            if axis == "v":
                x = line + side * k
                if not 0 <= x < g.shape[1]:
                    break
                v = g[t, x]
            else:
                y = line + side * k
                if not 0 <= y < g.shape[0]:
                    break
                v = g[y, t]
            if v < thr:
                n += 1
            else:
                break
        runs.append((t, n))
    grp, cur = [], []
    for t, n in runs + [(None, 0)]:
        if n >= minlen:
            cur.append((t, n))
        elif cur:
            w = np.array([c[1] for c in cur], float)
            grp.append((float(np.average([c[0] for c in cur], weights=w)), max(c[1] for c in cur)))
            cur = []
    return grp


def color_mask(a, color):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return {"black": (R < 95) & (G < 95) & (B < 95), "red": (R > 170) & (G < 100) & (B < 100),
            "blue": (B > 170) & (R < 100) & (G < 120),
            "purple": (R > 90) & (R < 215) & (G < 95) & (B > 90) & (B < 225)}[color]


def blobs(a, color, box, amin, amax, wmin=3, wmax=18, exclude=()):
    np, _, ndi = _np()
    x0, y0, x1, y1 = box
    lab, _ = ndi.label(color_mask(a[y0:y1, x0:x1], color))
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl is None:
            continue
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        ar = int((lab[sl] == i).sum())
        if not (amin <= ar <= amax and wmin <= w <= wmax and wmin <= h <= wmax):
            continue
        cy, cx = ndi.center_of_mass(lab == i)
        cx, cy = cx + x0, cy + y0
        if any(e[0] <= cx <= e[2] and e[1] <= cy <= e[3] for e in exclude):
            continue
        out.append((cx, cy, ar))
    return sorted(out)


def near(v, grid):
    return min(grid, key=lambda q: abs(q - v))


ROWS = []


def put(fig, series, xn, xv, xu, yn, yv, yu, flag="", prov="digitized"):
    ROWS.append({"figure": fig, "series": series, "x_name": xn, "x_value": xv, "x_unit": xu, "y_name": yn,
                 "y_value": yv, "y_unit": yu, "flag": flag, "provenance": prov})


def axis_lines(g, xlo, xhi, thr=150):
    np, _, _ = _np()
    col = max(range(xlo, xhi), key=lambda x: int((g[:, x] < thr).sum()))
    row = max(range(g.shape[0] // 2, g.shape[0]), key=lambda y: int((g[y, col + 3:col + 600] < thr).sum()))
    return col, row


def thickness_panel(a, fig, box, P, D, DM, xmaj, excl, label, dl_last, dm_last, amin_k, amin_r):
    cx, ex = lin(xmaj, [50 * i for i in range(len(xmaj))])
    bk = [b for b in blobs(a, "black", box, amin_k, 200, exclude=excl)]
    rd = [b for b in blobs(a, "red", box, amin_r, 220, exclude=excl)]
    bl = blobs(a, "blue", box, 8, 200, exclude=excl)
    pk = [near(cx[0] + cx[1] * b[0], P) for b in bk]
    pr = [near(cx[0] + cx[1] * b[0], P) for b in rd]
    ypx = [b[1] for b in bk] + [b[1] for b in rd]
    yval = [D[P.index(p)] for p in pk] + [DM[P.index(p)] for p in pr]
    cy, ey = lin(ypx, yval)
    print(f"   {fig}: x 눈금 {len(xmaj)} (잔차 {ex:.2f} MPa) · 보정 마커 {len(ypx)} (인쇄 두께) 최대 잔차 {ey * 1000:.2f} µm")
    for b in bl:
        p, d = cx[0] + cx[1] * b[0], cy[0] + cy[1] * b[1]
        print(f"   {fig} 밀어낸 펠릿 (◆): p ≈ {p:.1f} MPa · d ≈ {d:.4f} mm · 가압 중 400 대비 {d / dl_last - 1:+.2%} · "
              f"다이 안 제거 뒤 400 대비 {d / dm_last - 1:+.2%}")
        put(fig, f"{label} pressed-out pellet thickness (after 400 MPa)", "p", round(p, 1), "MPa", "d", round(d, 4),
            "mm", f"y-cal on {len(ypx)} printed Table S2 points, max|res| {ey * 1000:.2f} um")


def fig3(pdf):
    np, _, _ = _np()
    ras = [r for r in page_rasters(pdf, 3) if r[1].shape[1] > 1500]
    a = ras[0][1]
    g = a.max(axis=2)
    # (a) — y 축 열 110 · x 축 행 647 부근 (원본 1750×740)
    ca, ra = axis_lines(g, 90, 140)
    xa = [t[0] for t in ticks(g, "h", ra, ca - 5, 870, 1, 2) if t[1] >= 10][:9]
    thickness_panel(a, "3a", (ca + 5, 150, 870, ra - 2), P_L, D_L, DM_L, xa, [(150, 60, 700, 160)],
                    "LPSCl", D_L[-1], DM_L[-1], 85, 110)
    # (b) — σ vs p
    cb, rb = axis_lines(g, 980, 1040)
    xb = [t[0] for t in ticks(g, "h", rb, cb - 5, 1750, 1, 2) if t[1] >= 10][:9]
    yb = [t[0] for t in ticks(g, "v", cb, 150, rb + 5, -1, 1) if t[1] >= 9]
    cxb, _ = lin(xb, [50 * i for i in range(len(xb))])
    cyb, eyb = lin(yb, [5, 4, 3, 2, 1, 0][:len(yb)])
    print(f"   3b: y 주눈금 {len(yb)} (잔차 {eyb:.3f} mS/cm)")
    for color, nm in (("black", "in situ thickness"), ("blue", "pressed-out thickness")):
        vals = []
        for b in blobs(a, color, (cb + 4, 150, 1750, rb - 2), 50, 200, exclude=[(920, 50, 1750, 150)]):
            p, s = cxb[0] + cxb[1] * b[0], cyb[0] + cyb[1] * b[1]
            pn = near(p, P_L)
            vals.append((pn, s))
            put("3b", f"LPSCl sigma_ion ({nm})", "p", pn, "MPa", "sigma", round(s, 3), "mS/cm", f"x read {p:.1f}")
        print(f"   3b {color}: " + " ".join(f"{p}:{s:.2f}" for p, s in vals))


def fig4(pdf):
    np, _, ndi = _np()
    ras = [r for r in page_rasters(pdf, 4) if r[1].shape[1] > 1500]
    a = ras[0][1]
    g = a.max(axis=2)
    ca, ra = axis_lines(g, 60, 200)
    cb, rb = axis_lines(g, 860, 960)
    ya = ticks(g, "v", ca, 175, ra + 5, -1, 1)
    xa = ticks(g, "h", ra, ca - 2, ca + 740, 1, 2)
    yb = [t for t in ticks(g, "v", cb, 190, rb + 5, -1, 1)]
    xb = ticks(g, "h", rb, cb - 2, cb + 700, 1, 2)
    sp = float(np.median(np.diff(sorted(t[0] for t in ya))))
    cya, eya = lin([t[0] for t in ya], [0.02 * round((ra - t[0]) / sp) for t in ya])
    xam = [t[0] for t in xa if t[1] >= 9][:9]
    cxa, exa = lin(xam, [50 * i for i in range(len(xam))])
    ybd = [t[0] for t in yb if t[1] >= 9]
    dec = float(np.median(np.diff(sorted(ybd))))
    cyb, eyb = lin(ybd, [-1 + round((rb - p) / dec) for p in ybd])
    xbm = [t[0] for t in xb if t[1] >= 9]
    cxb, exb = lin(xbm, [0.1 * i for i in range(len(xbm))])
    print(f"   4a: y 눈금 {len(ya)} (잔차 {eya:.4f}) · x 주눈금 {len(xam)} (잔차 {exa:.2f} MPa) · "
          f"4b: y 10단위 {len(ybd)} (잔차 {eyb:.4f}) · x 주눈금 {len(xbm)} (잔차 {exb:.4f})")
    st = np.array([[0, 1, 1, 1, 0], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 1, 1, 1, 0]], bool)

    def markers(box):
        x0, y0, x1, y1 = box
        res = {}
        for color in ("black", "purple"):
            sub = color_mask(a[y0:y1, x0:x1], color)
            holes = ndi.binary_fill_holes(sub) & ~sub
            lab, _ = ndi.label(holes)
            sq = []
            for i, sl in enumerate(ndi.find_objects(lab), start=1):
                ar = int((lab[sl] == i).sum())
                h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
                if 6 <= ar <= 80 and 2 <= w <= 12 and 2 <= h <= 12:
                    yy, xx = ndi.center_of_mass(lab == i)
                    sq.append((xx + x0, yy + y0))
            er = ndi.binary_erosion(sub & ~ndi.binary_dilation(holes, iterations=3), structure=st)
            lab2, _ = ndi.label(er)
            lab0, _ = ndi.label(sub)
            dk = []
            for i, sl in enumerate(ndi.find_objects(lab2), start=1):
                ar = int((lab2[sl] == i).sum())
                if not 3 <= ar <= 120:
                    continue
                yy, xx = ndi.center_of_mass(lab2 == i)
                # 원래 성분의 크기: 화살 (선과 이어진 큰 성분) 은 버리고, 두 마커가 붙은 쌍은 표지
                j = lab0[int(round(yy)), int(round(xx))]
                cy_, cx_ = np.where(lab0 == j)
                cw, chh = cx_.max() - cx_.min() + 1, cy_.max() - cy_.min() + 1
                if max(cw, chh) > 24:
                    continue                                   # 주석 화살촉 (그림 4b 의 (i) · (ii) 화살)
                flag = "merged pair of two touching markers (centroid between them)" if max(cw, chh) > 13 else ""
                col = int(round(xx))
                ys = np.where(sub[:, col])[0]
                ys = ys[(ys >= sl[0].start - 8) & (ys <= sl[0].stop + 8)]
                dk.append((xx + x0, yy + y0, (ys.max() if len(ys) else yy) + y0, ar, flag))
            res[color] = (sq, dk)
        return res

    pa = markers((ca + 4, 190, ca + 672, ra - 2))
    rads = [d[2] - d[1] for c in pa for d in pa[c][1] if d[3] >= 15]
    rad = float(np.median(rads)) if rads else 4.5
    for color, (sq, dk) in pa.items():
        grid, nm = (P_L, "LPSCl") if color == "black" else (P_N, "NMC622")
        for kind, pts in (("after release to 110 kPa (open square)", [(x, y, "") for x, y in sq]),
                          ("under applied pressure (closed circle)", [(x, yb_ - rad, fl) for x, yc, yb_, ar, fl in dk])):
            vals = []
            for x, y, fl in pts:
                p = cxa[0] + cxa[1] * x
                pn = near(p, grid)
                if abs(pn - p) > 4:
                    continue
                e = cya[0] + cya[1] * y
                vals.append((pn, e))
                put("4a", f"{nm} porosity {kind}", "p", pn, "MPa", "eps_void", round(e, 4), "-", fl or f"x read {p:.1f}")
            print(f"   4a {nm} {kind}: " + " ".join(f"{p}:{e:.4f}" for p, e in sorted(vals)))
    pb = markers((cb + 4, 200, cb + 636, rb - 2))
    for color, (sq, dk) in pb.items():
        nm = "LPSCl" if color == "black" else "NMC622"
        vals = []
        for x, yc, yb_, ar, fl in dk:
            e = cxb[0] + cxb[1] * x
            s = 10 ** (cyb[0] + cyb[1] * (yb_ - rad))
            vals.append((e, s, fl))
            put("4b", f"{nm} sigma vs porosity (under load)", "eps_void", round(e, 4), "-", "sigma", round(s, 3),
                "mS/cm", fl)
        print(f"   4b {nm}: " + " ".join(f"{e:.3f}:{s:.2f}{'(쌍)' if fl else ''}" for e, s, fl in sorted(vals)))


def figS4(si):
    ras = page_rasters(si, 4)
    (ba, a), (bb, b) = sorted(ras, key=lambda r: r[0][0])[:2]
    for arr, fig in ((a, "S4a"), (b, "S4b")):
        g = arr.max(axis=2)
        col = max(range(5, 160), key=lambda x: int((g[:, x] < 150).sum()))
        row = max(range(g.shape[0] // 2, g.shape[0]), key=lambda y: int((g[y, col + 3:g.shape[1] - 3] < 150).sum()))
        xm = [t[0] for t in ticks(g, "h", row, col - 2, g.shape[1] - 2, 1, 1, minlen=2) if t[1] >= 8][:9]
        if fig == "S4a":
            thickness_panel(arr, fig, (col + 3, 150, g.shape[1] - 2, row - 2), P_N, D_N, DM_N, xm,
                            [(col, 0, g.shape[1], 150), (330, 398, 342, 410)], "NMC622", D_N[-1], DM_N[-1], 50, 60)
        else:
            ym = [t[0] for t in ticks(g, "v", col, 70, row + 3, -1, 1, minlen=2) if t[1] >= 8 and t[1] < 15]
            cx, _ = lin(xm, [50 * i for i in range(len(xm))])
            cy, ey = lin(ym[-5:], [20, 15, 10, 5, 0][-len(ym[-5:]):])
            print(f"   S4b: y 주눈금 {len(ym)} (잔차 {ey:.3f} mS/cm)")
            for color, nm in (("black", "in situ thickness"), ("blue", "pressed-out thickness")):
                vals = []
                for bl in blobs(arr, color, (col + 3, 70, g.shape[1] - 2, row - 2), 10, 120, wmax=13):
                    p = cx[0] + cx[1] * bl[0]
                    pn = near(p, P_N)
                    if abs(pn - p) > 6:
                        continue
                    s = cy[0] + cy[1] * bl[1]
                    vals.append((pn, s))
                    put("S4b", f"NMC622 sigma_e ({nm})", "p", pn, "MPa", "sigma", round(s, 3), "mS/cm", f"x read {p:.1f}")
                print(f"   S4b {color}: " + " ".join(f"{p}:{s:.2f}" for p, s in vals))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", help="본문 PDF")
    ap.add_argument("--si", help="SI PDF")
    ap.add_argument("--out", default=str(ROOT / "litdb" / "figures" / SLUG / "digitized.csv"))
    ap.add_argument("--check", action="store_true", help="표 S2 재계산도 출력")
    ap.add_argument("--check-only", action="store_true", help="PDF 없이 표 S2 재계산만")
    a = ap.parse_args()
    if a.check or a.check_only:
        check_table()
    if a.check_only:
        return 0
    if not (a.pdf and a.si):
        ap.error("--pdf 와 --si 가 필요하다 (또는 --check-only)")
    print("== 판독")
    fig3(a.pdf)
    fig4(a.pdf)
    figS4(a.si)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        f.write("# Miss 2026 ACS AMI 18 32830 - figure readout. ALL VALUES DIGITIZED (not printed). "
                "tools/litdb/miss2026_digitize.py\n")
        w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys()))
        w.writeheader()
        w.writerows(ROWS)
    print(f"→ {out}  ({len(ROWS)} 행)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
