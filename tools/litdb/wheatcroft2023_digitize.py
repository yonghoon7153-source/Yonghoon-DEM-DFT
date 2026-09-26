#!/usr/bin/env python3
"""wheatcroft2023_digitize.py — Wheatcroft et al., Batteries & Supercaps 6, e202300032 (2023) **그림 판독**.

카드: litdb/papers/wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md  (§3.4 · §3.5 · §13)
원본: 본문 PDF (10 쪽, Wiley) + SI `batt202300032-sup-0001-misc_information.pdf` (11 쪽).
⚠ PDF 는 리포에 없다 (litdb/inbox 는 .gitignore).  그림은 전부 **래스터**(임베디드 이미지)다 — 벡터 좌표가 없다.

⛔ 이 스크립트가 내는 값은 전부 **digitized (그림 판독)** 이다.  표에 옮길 때 `digitized` 라벨을 떼지 말 것.
   논문 본문이 **숫자로 적은 것**은 평균 ± 값뿐이고 (p. 4–6, p. 8), 개별 입자 값 · 개수 n (군별) 은 그림에만 있다.

무엇을 읽나 (쪽 = PDF 쪽, 1-based)
  · Fig. 2f (본문 p.3)  P_f vs D — 평판(속 빈 적색 □) 15 · 원뿔-구형 팁(청색 ●) 15
  · Fig. 3e (본문 p.4)  P_f/D² vs D — 실험 두 계열 + FE 절점(K_IC 0.05/0.10/0.15/0.20, D 5/10/15/20 µm)
  · Fig. 3c (본문 p.4)  탄성 σθθ/(P/D²) 중심선 — 최대값·중심값
  · Fig. 5  (본문 p.6)  상자그림 7 군 — Q1 · 중앙값 · Q3 · 수염 끝
  · Fig. 6  (본문 p.6)  P_f/D² vs D — 7 군 (P · E · Ex · 3.0 · 3.4 · 3.9 · 4.3 V)
  · Fig. 1d · 2e        하중–변위 최대점

방법
  1. 축: 바깥쪽 눈금(Origin 그림) 또는 격자선(MATLAB 그림, Fig. 3c·3e)의 픽셀 중심 → 선형 최소제곱.
  2. 마커: 채도 ≥ 0.45 인 픽셀의 연결성분 (반투명 영역 음영은 채도가 낮아 빠진다).  두 마커가 붙은 성분은
     위치+색상 4차원 k-means(k=2, 시드 고정) 로 가른다.  Fig. 6 은 음영이 마커 **위에** 그려져 색이 변하므로
     (적색 □ → 갈색) 군 판정은 **모양·색을 눈으로** 정한 앵커 목록(ANCHOR6)에 최근접 대응시키고,
     재검출 좌표가 앵커에서 벗어나면 flag 를 단다.
  3. Fig. 2f 속 빈 □ 는 윤곽이 1–2 px 라 성분검출이 불안정 → 눈으로 찍은 근사점 주위 ±6 px 의 적색 픽셀 중심으로 보정.
  판독 분해능: Fig. 6 1 px = 0.021 µm · 0.154 MPa / Fig. 2f 1 px = 0.032 µm · 0.108 mN / Fig. 3e 1 px = 0.037 µm · 0.44 MPa.

검증 (이 스크립트가 --check 로 출력한다)
  · Fig. 2f 평판 15점 → P_f/D² 평균 207.0, 모집단 SD 48.7  ⇔  본문 p.5 "207 ± 49 MPa"
  · Fig. 2f 원뿔 15점 → 67.0 ± 20.5  ⇔  본문 p.6 "67 ± 21 MPa" (Pristine)
  · Fig. 6 각 군 평균이 본문 평균을 ≤ 0.4 MPa 로 재현, Fig. 5 상자 사분위와도 대응 (카드 §3.5)

알려진 원본 불일치 (판독이 드러낸 것 — 카드 §10)
  · Fig. 3e 의 평판 점은 Fig. 2f 와 **같은 하중 P_f 를 다른 D 로** 찍었다 (P_f = σ·D² 로 역산하면 14/15 짝이 맞는다).
    그 D 로 계산한 평균은 ≈184 MPa — 본문 "207 ± 49 MPa (Figure 3)" 는 Fig. 2f 의 (D, P_f) 에서 나온다.
  · 본문 p.6 "cycled … six secondary particles" ↔ Fig. 6 에 보이는 점 3.0 V 8 · 3.4 V 8 · 3.9 V 15 · 4.3 V 8, Ex 6 (+1, y축 120 밖).

usage
  python3 tools/litdb/wheatcroft2023_digitize.py --pdf "<…>/Wheatcroft…Fracture_Testing….pdf" \\
        [--si "<…>/batt202300032-sup-0001-misc_information.pdf"] \\
        [--csv litdb/figures/wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem/digitized.csv] [--check]
"""
import argparse
import colorsys
import csv
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage
from scipy.cluster.vq import kmeans2

try:
    import pymupdf as fitz
except ImportError:                                   # 옛 이름
    import fitz

SLUG = "wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem"
ROOT = Path(__file__).resolve().parents[2]

# ── Fig. 6 앵커: (군, D µm, P_f/D² MPa) — 2× 확대 오버레이에서 모양·색으로 군을 정한 것 (2026-09-26) ──
ANCHOR6 = {
    "P":    [(6.21, 98.0), (6.59, 100.6), (7.01, 95.5), (7.98, 61.6), (8.76, 93.5), (8.82, 66.1), (9.76, 72.0),
             (10.04, 46.9), (10.43, 75.7), (10.60, 70.4), (11.35, 52.5), (15.82, 41.8), (15.98, 52.4),
             (17.20, 41.1), (17.37, 43.5)],
    "E":    [(8.40, 103.6), (8.62, 115.1), (9.19, 69.0), (9.24, 89.7), (10.44, 49.3), (10.46, 72.4), (10.99, 65.5),
             (11.35, 70.6), (11.40, 66.4), (11.96, 59.5), (12.55, 46.3), (13.81, 49.5), (13.87, 41.1),
             (14.04, 40.4), (15.23, 50.8), (18.27, 41.4)],
    "Ex":   [(7.32, 101.2), (9.08, 92.1), (11.06, 76.4), (11.99, 63.4), (13.96, 59.7), (14.99, 59.7)],
    "3.0V": [(6.04, 48.8), (7.32, 55.6), (8.35, 46.5), (9.88, 41.7), (13.94, 5.8), (13.97, 27.8), (14.19, 30.5),
             (15.29, 29.8)],
    "3.4V": [(6.43, 92.3), (7.56, 57.5), (7.67, 40.1), (8.39, 33.5), (8.62, 37.0), (8.86, 35.8), (10.11, 43.1),
             (11.43, 29.0)],
    "3.9V": [(8.01, 20.6), (8.38, 20.0), (8.42, 31.4), (8.53, 23.8), (8.63, 25.6), (9.87, 19.1), (10.42, 12.0),
             (10.48, 58.4), (11.05, 17.3), (11.94, 18.8), (11.97, 21.0), (12.22, 9.5), (12.35, 7.3), (12.90, 15.2),
             (16.25, 8.8)],
    "4.3V": [(6.32, 10.6), (6.42, 7.4), (7.55, 13.5), (7.57, 17.7), (8.16, 16.2), (8.24, 6.5), (9.40, 6.2),
             (10.94, 10.0)],
}
STATED = {  # 본문 (쪽) — 평균 ± (정의 미기재)
    "P": (67, 21, "p.6"), "E": (64, 22, "p.6"), "3.0V": (36, 15, "p.6"), "3.4V": (46, 15, "p.6 (결론 p.8: 46 ± 19)"),
    "3.9V": (21, 12, "p.6 (결론 p.8: 20 ± 11)"), "4.3V": (11, 4, "p.6"), "Ex": (None, None, "숫자 없음"),
}
# Fig. 2f 근사점 (눈으로 찍음 → 스크립트가 ±6 px 로 보정)
APPROX_2F_FLAT = [(7.15, 11.3), (7.15, 10.0), (7.35, 11.0), (8.35, 13.1), (8.8, 18.0), (9.55, 24.9), (10.0, 29.7),
                  (10.25, 26.6), (10.3, 19.5), (10.6, 21.1), (10.6, 17.8), (13.7, 44.0), (14.5, 37.5), (15.5, 49.2),
                  (18.35, 28.8)]
APPROX_2F_CONO = [(6.22, 3.75), (6.61, 4.37), (7.03, 4.68), (7.99, 3.9), (8.78, 7.17), (8.84, 5.12), (9.77, 6.85),
                  (10.06, 4.7), (10.45, 8.2), (10.6, 7.9), (11.36, 6.74), (15.84, 10.43), (15.99, 13.37),
                  (17.22, 12.15), (17.38, 13.12)]


# ── 래스터 · 축 ───────────────────────────────────────────────────────────────
def page_images(doc, page_no):
    """page_no(1-based) 의 임베디드 이미지 → [RGB float] (get_image_info 순서)."""
    page = doc[page_no - 1]
    out = []
    for info in page.get_image_info(xrefs=True):
        x = info["xref"]
        if not x:
            continue
        pix = fitz.Pixmap(doc, x)
        if pix.n - pix.alpha >= 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
        out.append(a.astype(float))
    return out


def ticks(im, frame, axis):
    """바깥쪽 눈금 중심 (px) 목록 — axis 'x' = 아래 축, 'y' = 왼쪽 축."""
    x0, y0, x1, y1 = frame
    dark = im.sum(axis=2) < 300
    if axis == "x":
        prof = dark[y1 + 2:y1 + 16, x0 - 3:x1 + 4].sum(axis=0); off = x0 - 3
    else:
        prof = dark[y0 - 3:y1 + 4, x0 - 16:x0 - 2].sum(axis=1); off = y0 - 3
    pos = [off + i for i in range(len(prof)) if prof[i] >= 4]
    g = []
    for p in pos:
        if g and p - g[-1][-1] <= 1:
            g[-1].append(p)
        else:
            g.append([p])
    return [float(np.mean(q)) for q in g]


def calib(pix, val):
    a, b = np.polyfit(np.asarray(pix, float), np.asarray(val, float), 1)
    return lambda p: a * p + b, lambda v: (v - b) / a


def sat_mask(sub, smin=0.45, vmin=0.2):
    s = sub / 255.0
    mx, mn = s.max(axis=2), s.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-9), 0)
    return (sat >= smin) & (mx >= vmin)


def refine(im, px, test, win):
    x, y = int(round(px[0])), int(round(px[1]))
    sub = im[y - win:y + win + 1, x - win:x + win + 1]
    m = test(sub)
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    return x - win + xs.mean(), y - win + ys.mean()


# ── 그림별 ──────────────────────────────────────────────────────────────────
def fig2f(im):
    fx, _ = calib([1489.5, 1551.5, 1614.5, 1676.5, 1738.5, 1800.5, 1863.5, 1925.5], [6, 8, 10, 12, 14, 16, 18, 20])
    fy, _ = calib([861.5, 907.5, 953.5, 1000.5, 1046.5, 1092.5, 1138.5, 1185.5, 1231.5, 1277.5],
                  [50, 45, 40, 35, 30, 25, 20, 15, 10, 5])
    gx = np.poly1d(np.polyfit([6, 20], [1489.5, 1925.5], 1)); gy = np.poly1d(np.polyfit([50, 5], [861.5, 1277.5], 1))
    red = lambda s: (s[..., 0] > 120) & (s[..., 0] - s[..., 1] > 30) & (s[..., 0] - s[..., 2] > 30)
    blue = lambda s: (s[..., 2] > 150) & (s[..., 0] < 100) & (s[..., 1] < 100)
    rows = []
    for series, lst, test, win in (("flat platen", APPROX_2F_FLAT, red, 6), ("cono-spherical", APPROX_2F_CONO, blue, 4)):
        for D, P in lst:
            r = refine(im, (gx(D), gy(P)), test, win)
            Dn, Pn = fx(r[0]), fy(r[1])
            rows.append(dict(figure="2f", series=series, D=Dn, y=Pn, y_name="P_f", y_unit="mN",
                             sigma=Pn / Dn ** 2 * 1e3))       # mN/µm² → MPa (×1000)
    return rows


def fig3e(im):
    xv = lambda x: (x - 1103) / 27.28; yv = lambda y: (2305.5 - y) / 2.275     # 격자선 0/5/…/25 µm · 0/50/…/300 MPa
    X0, X1, Y0, Y1 = 1105, 1783, 1626, 2303
    sub = im[Y0:Y1, X0:X1]
    r, g, b = sub[..., 0], sub[..., 1], sub[..., 2]
    out = []
    for series, m, fill in (("flat platen", (r > 170) & (g < 110) & (b < 110), True),
                            ("cono-spherical", (b > 150) & (r < 90) & (g < 90), False)):
        if fill:
            m = ndimage.binary_fill_holes(ndimage.binary_closing(m, np.ones((3, 3))))
        lab, n = ndimage.label(m)
        pts = []
        for i in range(1, n + 1):
            ys, xs = np.nonzero(lab == i)
            if len(xs) < 15:
                continue
            pts.append([xv(xs.mean() + X0), yv(ys.mean() + Y0), len(xs), np.ptp(xs) + 1])
        pts = [p for p in pts if not (11.0 < p[0] < 11.8 and p[1] > 265)]        # 범례 마커
        merged = []
        for p in sorted(pts, key=lambda q: q[0]):                              # 윤곽이 둘로 쪼개진 □ 재결합
            if merged and abs(merged[-1][0] - p[0]) < 0.35 and abs(merged[-1][1] - p[1]) < 7:
                a, c = merged[-1], p
                w = a[2] + c[2]
                merged[-1] = [(a[0] * a[2] + c[0] * c[2]) / w, (a[1] * a[2] + c[1] * c[2]) / w, w, max(a[3], c[3])]
            else:
                merged.append(p)
        for p in merged:
            if series == "flat platen" and p[3] > 24:                          # 나란히 붙은 □ 두 개
                out += [dict(figure="3e", series=series, D=p[0] - 0.22, y=p[1], flag="split-pair"),
                        dict(figure="3e", series=series, D=p[0] + 0.22, y=p[1], flag="split-pair")]
            else:
                out.append(dict(figure="3e", series=series, D=p[0], y=p[1], flag="ok"))
    for d in out:
        d.update(y_name="P_f/D2", y_unit="MPa", sigma=d["y"], P_implied=d["y"] * d["D"] ** 2 / 1e3)
    # FE 절점 (검은 점) — 얇은 선·글자는 4×4 침식으로 지운다
    dark = sub.sum(axis=2) < 200
    er = ndimage.binary_erosion(dark, np.ones((4, 4)))
    lab, n = ndimage.label(er)
    nodes = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        D = xv(xs.mean() + X0)
        if len(xs) >= 10 and min(abs(D - k) for k in (5, 10, 15, 20)) < 0.08:   # <10 px = 실험 ● 윤곽 조각
            nodes.append(dict(figure="3e", series="FE node", D=round(D), y=yv(ys.mean() + Y0), y_name="P_f/D2",
                              y_unit="MPa", flag=f"px={len(xs)}" + (" (merged nodes)" if len(xs) > 30 else "")))
    return out, nodes


def fig3c(im):
    X0, X1, Y0, Y1 = 1227, 1787, 180, 1044
    xv = lambda x: (x - 1507) / 56.0; zv = lambda y: 0.5 - (y - Y0) / (Y1 - Y0)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    red = (r > 150) & (g < 100) & (b < 100); blue = (b > 150) & (r < 90) & (g < 90)
    rows = []
    for name, m in (("cono-spherical", red), ("flat platen", blue)):
        ys, xs = np.nonzero(m[Y0 + 2:Y1 - 1, X0 + 2:X1 - 1]); ys = ys + Y0 + 2; xs = xs + X0 + 2
        sel = zv(ys) < 0.45 if name == "flat platen" else np.ones_like(ys, bool)
        i = np.argmax(np.where(sel, xs, -1))
        rows.append(dict(figure="3c", series=name + " max", D=zv(ys[i]), y=xv(xs[i]), y_name="sigma_tt/(P/D2)",
                         y_unit="-", flag="x=z/D"))
    y = int(round(Y0 + 0.5 * (Y1 - Y0)))
    xr = np.nonzero(red[y - 2:y + 3, X0:X1].any(axis=0))[0] + X0
    rows.append(dict(figure="3c", series="centre z/D=0 (both)", D=0.0, y=xv(xr.mean()), y_name="sigma_tt/(P/D2)",
                     y_unit="-", flag="red over blue"))
    return rows


def fig5(im):
    fy, _ = calib([22.5, 110.5, 199.5, 288.5, 377.5, 466, 555, 644.5, 732.5], [160, 140, 120, 100, 80, 60, 40, 20, 0])
    dark = im.sum(axis=2) < 250
    rows = []
    for gname, c in zip(["P", "E", "Ex", "3.0V", "3.4V", "3.9V", "4.3V"],
                        [237.5, 364, 490.5, 617.5, 744.5, 870, 996.5]):
        col = int(round(c)) - 25
        runs, cur = [], None
        for yy in range(26, 730):
            if dark[yy, col]:
                cur = [yy, yy] if cur is None else [cur[0], yy]
            elif cur:
                runs.append(cur); cur = None
        # 상자 가장자리·중앙값만: 틀(0 · 160) 과 위쪽 글자("Uncycled"/"Cycled", ≈150–156 MPa) 를 뺀다
        v = sorted((fy((a + b) / 2) for a, b in runs if 1.0 < fy((a + b) / 2) < 130.0), reverse=True)
        if len(v) >= 3:
            for name, val in zip(("Q3", "median", "Q1"), v[:3]):
                rows.append(dict(figure="5", series=gname, D=float("nan"), y=val, y_name=name, y_unit="MPa", flag="box"))
    return rows


def fig6(im):
    fx, _ = calib([172.5, 267.5, 362.5, 457.5, 552.5, 647.5, 742.5, 837.5, 932.5], [4, 6, 8, 10, 12, 14, 16, 18, 20])
    fy, _ = calib([18.5, 148.5, 278.5, 408.5, 539.5, 669.5, 799.5], [120, 100, 80, 60, 40, 20, 0])
    X0, Y0, X1, Y1 = 175, 21, 930, 797
    sub = im[Y0:Y1, X0:X1]
    lab, n = ndimage.label(sat_mask(sub))
    det = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 20:
            continue
        if len(xs) > 300:                                   # 붙은 두 마커 → 위치+색상 k-means
            cols = sub[ys, xs] / 255.0
            hue = np.array([colorsys.rgb_to_hsv(*c)[0] * 360 for c in cols])
            feat = np.c_[xs, ys, np.cos(np.radians(hue)) * 15, np.sin(np.radians(hue)) * 15]
            best = None
            for seed in range(10):
                cen, lb = kmeans2(feat, 2, minit="++", seed=seed)
                sse = sum(((feat[lb == k] - cen[k]) ** 2).sum() for k in range(2))
                if best is None or sse < best[0]:
                    best = (sse, lb)
            for k in range(2):
                s = best[1] == k
                det.append((fx(xs[s].mean() + X0), fy(ys[s].mean() + Y0), "kmeans-split"))
        elif len(xs) > 290:
            det.append((fx(xs.mean() + X0), fy(ys.mean() + Y0), "possible-overlap"))
        else:
            det.append((fx(xs.mean() + X0), fy(ys.mean() + Y0), "ok"))
    # 앵커 대응 (정규화 거리: D 0.15 µm · σ 1.5 MPa)
    rows, used = [], set()
    for gname, lst in ANCHOR6.items():
        for D, S in lst:
            dist = [((d[0] - D) / 0.15) ** 2 + ((d[1] - S) / 1.5) ** 2 for d in det]
            order = np.argsort(dist)
            j = next((int(k) for k in order if int(k) not in used), None)
            ok = j is not None and dist[j] <= 1.0
            if ok:
                used.add(j)
                rows.append(dict(figure="6", series=gname, D=det[j][0], y=det[j][1], y_name="P_f/D2", y_unit="MPa",
                                 flag=det[j][2]))
            else:
                rows.append(dict(figure="6", series=gname, D=D, y=S, y_name="P_f/D2", y_unit="MPa",
                                 flag="anchor-only (not re-detected)"))
    return rows


def peak(im, xt, yt, test, box, label):
    fx, _ = calib(*xt); fy, _ = calib(*yt)
    x0, y0, x1, y1 = box
    m = test(im[y0:y1, x0:x1]); ys, xs = np.nonzero(m); ys = ys + y0; xs = xs + x0
    i = ys.argmin()
    return dict(figure=label, series="peak", D=fx(xs[i]), y=fy(ys[i]), y_name="P", y_unit="mN", flag="x=displacement µm")


# ── 통계 ────────────────────────────────────────────────────────────────────
def stats_line(vals):
    v = np.asarray(vals, float)
    return f"n={len(v):2d} mean {v.mean():6.1f}  SD(N) {v.std():5.1f}  SD(N-1) {v.std(ddof=1):5.1f}"


def main():
    ap = argparse.ArgumentParser(description="Wheatcroft 2023 그림 판독 (값은 전부 digitized)")
    ap.add_argument("--pdf", required=True, help="본문 PDF (10 쪽)")
    ap.add_argument("--si", default="", help="SI PDF (선택; 지금은 판독 대상 없음 — 크기 검사만)")
    ap.add_argument("--csv", default=str(ROOT / "litdb" / "figures" / SLUG / "digitized.csv"))
    ap.add_argument("--check", action="store_true", help="본문 평균 ± 과 대조 출력")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    f1 = page_images(doc, 2)[0]; f2 = page_images(doc, 3)[0]; f3 = page_images(doc, 4)[0]
    p6 = page_images(doc, 6); f5, f6 = p6[0], p6[1]
    need = {"Fig1": (f1, (1281, 1834)), "Fig2": (f2, (1397, 2002)), "Fig3": (f3, (2435, 1805)),
            "Fig5": (f5, (890, 1603)), "Fig6": (f6, (949, 1515))}
    for k, (im, shp) in need.items():
        if im.shape[:2] != shp:
            sys.exit(f"⛔ {k} 래스터 크기 {im.shape[:2]} ≠ {shp} — 다른 판본의 PDF 다. 축 틀을 다시 잡을 것.")
    rows = fig2f(f2)
    e3, nodes = fig3e(f3)
    rows += e3 + nodes + fig3c(f3) + fig5(f5) + fig6(f6)
    rows.append(peak(f1, ([131.5, 216.5, 300.5, 384.5, 468.5, 552.5, 637.5], [0, .4, .8, 1.2, 1.6, 2.0, 2.4]),
                      ([664.5, 736.5, 808.5, 880.5, 952.5, 1024.5, 1097.5, 1169.5], [14, 12, 10, 8, 6, 4, 2, 0]),
                      lambda s: (s[..., 2] > 150) & (s[..., 0] < 80) & (s[..., 1] < 80), (133, 666, 637, 1169), "1d"))
    rows.append(peak(f2, ([1455.5, 1547.5, 1639.5, 1731.5, 1823.5, 1915.5], [0, .4, .8, 1.2, 1.6, 2.0]),
                      ([140.5, 224.5, 307.5, 390.5, 473.5, 557.5], [50, 40, 30, 20, 10, 0]),
                      lambda s: (s[..., 0] > 170) & (s[..., 1] < 120) & (s[..., 2] < 120), (1458, 102, 1913, 556), "2e"))
    Path(a.csv).parent.mkdir(parents=True, exist_ok=True)
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["# Wheatcroft 2023 Batteries & Supercaps 6 e202300032 — figure readout. ALL VALUES DIGITIZED "
                    "(not stated in text). tools/litdb/wheatcroft2023_digitize.py"])
        w.writerow(["figure", "series", "x_name", "x_value", "x_unit", "y_name", "y_value", "y_unit",
                    "sigma_PfD2_MPa", "flag", "provenance"])
        for r in rows:
            xn, xu = ("D", "um")
            if r["figure"] == "3c":
                xn, xu = "z/D", "-"
            elif r["figure"] in ("1d", "2e"):
                xn, xu = "displacement", "um"
            elif r["figure"] == "5":
                xn, xu = "", ""
            sig = r.get("sigma", "")
            w.writerow([r["figure"], r["series"], xn, "" if xn == "" else f"{r['D']:.3f}", xu, r["y_name"],
                        f"{r['y']:.3f}", r["y_unit"], "" if sig == "" else f"{sig:.1f}", r.get("flag", ""),
                        "digitized"])
    print(f"→ {a.csv}  ({len(rows)} rows)")
    if a.check:
        fl = [r["sigma"] for r in rows if r["figure"] == "2f" and r["series"] == "flat platen"]
        co = [r["sigma"] for r in rows if r["figure"] == "2f" and r["series"] == "cono-spherical"]
        print("Fig 2f flat platen P_f/D²   ", stats_line(fl), " | 본문 p.5: 207 ± 49")
        print("Fig 2f cono-spherical P_f/D²", stats_line(co), " | 본문 p.6: 67 ± 21 (Pristine)")
        f3e = [r for r in rows if r["figure"] == "3e" and r["series"] == "flat platen"]
        print("Fig 3e flat platen (같은 P_f, 다른 D)", stats_line([r["y"] for r in f3e]))
        for g in ANCHOR6:
            v = [r["y"] for r in rows if r["figure"] == "6" and r["series"] == g]
            st = STATED[g]
            s = "숫자 없음" if st[0] is None else f"{st[0]} ± {st[1]} ({st[2]})"
            nflag = sum(1 for r in rows if r["figure"] == "6" and r["series"] == g and r["flag"].startswith("anchor"))
            print(f"Fig 6 {g:5s}", stats_line(v), f" | 본문 {s}" + (f"  ⚠ 재검출 안 된 앵커 {nflag}" if nflag else ""))


if __name__ == "__main__":
    main()
