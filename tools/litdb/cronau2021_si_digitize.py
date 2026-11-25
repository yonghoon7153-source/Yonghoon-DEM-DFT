#!/usr/bin/env python3
"""cronau2021_si_digitize.py — Cronau 2021 (ACS Energy Lett. 6, 3072−3077) **SI 그림 디지타이즈**.

카드: litdb/papers/cronau2021_stack_pressure_ionic_conductivity.md  (§SI)
원본: ACS SI `nz1c01299_si_001.pdf` (10 쪽).  ⚠ PDF 는 리포에 없다 (litdb/inbox 는 .gitignore).

⛔ 이 스크립트가 내는 값은 전부 **digitized (그림 판독)** 이다.  SI 본문에는 σ 숫자가 **하나도 없다**
   (텍스트 전수 확인).  표에 옮길 때 `digitized` 라벨을 떼지 말 것.

무엇을 읽나
  · Fig. S1 (a–f)  AM/GC 6종 σ vs stack pressure, 제작압 5단 (97.34 … 486.73 MPa)
  · Fig. S2 (a–d)  µC 4종 σ vs stack pressure — ★ S2c = µC-Li6PS5Cl
  · Fig. S3        펠릿 밀도 vs 제작압 (보조, 겹친 마커는 분리 못 함 → flag)
  · Fig. S4 (a,b)  Au 스퍼터 · stack ~10 MPa 의 σ(로그축)·Ea vs 제작압 — 본문 Fig. 4 표기값의 원 데이터
  · Fig. S5        GC-Li6PS5Br EIS −80 °C 의 반원 끝(최저 −Z″ 군집) 위치 (보조)

방법 (S1/S2)
  1. SI 에 박힌 래스터(~200 dpi)를 **SMask(알파) 합성**해 흰 바탕으로 복원 — 알파를 버리면 축 글자가
     검은 바탕에 묻힌다 (첫 시도에서 실제로 그랬다).  S1 = JPEG(DCT), S2 = Flate(무손실).
  2. 축: 왼쪽/아래 축선 중심을 명암가중 서브픽셀로 잡고, **바깥쪽 눈금**(주눈금 = 길이 ≥ 6 px)의
     명암가중 중심으로 선형 최소제곱 — 잔차 y ≤ 3e-6 S/cm · x ≤ 0.19 MPa (전 패널).
  3. 계열 색 = 범례 마커(채도 > 60) 평균 — Origin 기본색 (0,0,128)·(255,128,0)·(0,128,0)·(0,128,192)·(128,0,0).
  4. 배경 = **열(column)별 중앙값** — 영역 띠(빨강→노랑→초록)가 x 방향으로만 변하므로.
  5. 마커 중심 = **가림(occlusion) 인지 고정반경 원 맞춤**: 제 색 픽셀 = 1, 배경 = 0 로 두고
     다른 계열 색·반투명 가장자리는 **무시** → 원 안/밖 불일치 수 최소 (0.1 px 격자, 동률 최적의 중심).
     그리는 순서 = 범례 순서 (486.73 이 맨 위) — 겹침에서 확인.
     반경 R = 반투명 가중 면적 √(Σα/π) 로 고립 마커에서 측정: S1 4.87 px · S2 4.85 px.
  6. 판독 불확실도 (그림 판독만; 측정 산포는 SI 에 없다 = n/a):
       S2c 1 px = 0.0101 mS/cm → ±0.01 mS/cm · S1e 1 px = 0.0030 mS/cm → ±0.003 mS/cm ·
       가려진 점(own_px < 25) ±0.02 mS/cm.
  검증: S4a 판독이 본문 Fig. 4 패널 표기값 0.15 / 0.65 / 2.40 mS/cm 를 0.145 / 0.654 / 2.45 로 재현
        (≤ 3 %, 로그축 1 px ≈ 1.7 %).  단 Fig. 4c 표기 0.59 ↔ S4a ≈0.53 은 6 px 차 — 판독 오차가 아니다.

알려진 원본 표기 오류 (판독에 반영)
  · Fig. S1c (와 본문 Fig. 2c · Fig. 3a,b) y축 단위 "mS·cm⁻¹" — 눈금값(×10⁻³/×10⁻⁴)과 대조하면 **S·cm⁻¹** 이어야 한다.
  · Fig. S1 캡션 b) "AM-80 Li2O – 20 P2S5" — 패널 제목은 Li2S.  SI 합성절 제목 "80 Li2 – 20 P2S5".

usage
  python3 tools/litdb/cronau2021_si_digitize.py --pdf "<…>/nz1c01299_si_001.pdf"
        [--csv litdb/figures/cronau2021_stack_pressure_ionic_conductivity/si_digitized.csv]
        [--overlay-dir <dir>]      # 맞춘 원을 그린 검증용 PNG
"""
import argparse
import csv
import os
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

try:
    import pymupdf as fitz
except ImportError:                                   # 옛 이름
    import fitz

SLUG = "cronau2021_stack_pressure_ionic_conductivity"
ROOT = Path(__file__).resolve().parents[2]
FAB = [97.34, 194.69, 292.03, 389.30, 486.73]         # 범례 순서 = 그리는 순서 (마지막이 맨 위)

# ── 패널 정의 (frame = 대략의 축틀 L,T,R,B; 축선은 ±4 px 안에서 다시 잡는다) ─────────────
PANELS = {
    "S1": dict(page=4, R=4.87, panels=[
        ("S1a", "AM-Li7P3S11",            "AM", (133, 63, 623.5, 457),      5e-5, 7),
        ("S1b", "AM-80Li2S-20P2S5",       "AM", (750, 65.5, 1241, 459),     1e-4, 8),
        ("S1c", "GC-Li7P3S11",            "GC", (133.5, 532, 624, 925.5),   5e-4, 7),
        ("S1d", "GC-Li6PS5Br",            "GC", (749.5, 535.5, 1240, 929),  2e-4, 7),
        ("S1e", "GC-Li6PS5Cl",            "GC", (128, 993.5, 619, 1387),    2e-4, 7),
        ("S1f", "GC-Li5.5PS4.5Cl1.5",     "GC", (752.5, 997, 1243, 1390.5), 5e-4, 6)]),
    "S2": dict(page=5, R=4.85, panels=[
        ("S2a", "uC-Li6PS5Br",            "uC", (128, 63, 618, 457.5),      5e-4, 6),
        ("S2b", "uC-Li10GeP2S12",         "uC", (745, 65.5, 1235, 460),     1e-3, 8),
        ("S2c", "uC-Li6PS5Cl",            "uC", (128, 528, 618, 922),       5e-4, 9),
        ("S2d", "uC-Li5.5PS4.5Cl1.5",     "uC", (751, 530, 1241, 924.5),    5e-4, 11)]),
}
T_OWN, T_BG, MIN_OWN = 55.0, 28.0, 5


# ── 래스터 추출 ──────────────────────────────────────────────────────────────
def page_images(doc, page_no):
    """page_no(1-based) 의 임베디드 이미지들을 **SMask 합성·흰 바탕**으로 → [(bbox, RGB uint8)] (위→아래)."""
    page = doc[page_no - 1]
    out = []
    for im in page.get_images(full=True):
        xref, smask = im[0], im[1]
        base = fitz.Pixmap(doc, xref)
        rgb = np.frombuffer(base.samples, np.uint8).reshape(base.height, base.width, base.n)[:, :, :3]
        rgb = rgb.astype(float)
        if smask:
            m = fitz.Pixmap(doc, smask)
            a = np.frombuffer(m.samples, np.uint8).reshape(m.height, m.width, m.n)[:, :, 0].astype(float) / 255.
            if a.shape != rgb.shape[:2]:
                a = np.array(Image.fromarray((a * 255).astype(np.uint8)).resize(
                    (rgb.shape[1], rgb.shape[0]), Image.BILINEAR)).astype(float) / 255.
            rgb = rgb * a[..., None] + 255 * (1 - a[..., None])
        info = [i for i in page.get_image_info(xrefs=True) if i["xref"] == xref]
        bbox = info[0]["bbox"] if info else (0, 0, 0, 0)
        out.append((bbox, np.clip(rgb, 0, 255).astype(np.uint8)))
    out.sort(key=lambda t: t[0][1])
    return out


# ── 축 · 눈금 ────────────────────────────────────────────────────────────────
def refine_axis(g, L, T, R, B):
    rows = slice(int(T) + 15, int(B) - 15)
    xs = np.arange(int(L) - 4, int(L) + 5)
    prof = np.array([np.median(g[rows, x]) for x in xs])
    k = int(np.argmax(prof)); lo, hi = max(0, k - 1), min(len(xs), k + 2)
    xc = float((xs[lo:hi] * prof[lo:hi]).sum() / prof[lo:hi].sum())
    cols = slice(int(L) + 15, int(R) - 15)
    ys = np.arange(int(B) - 4, int(B) + 5)
    prof = np.array([np.median(g[y, cols]) for y in ys])
    k = int(np.argmax(prof)); lo, hi = max(0, k - 1), min(len(ys), k + 2)
    yc = float((ys[lo:hi] * prof[lo:hi]).sum() / prof[lo:hi].sum())
    return xc, yc


def ticks_y(g, xc, T, B, thr=60):
    x0 = int(np.floor(xc)) - 1
    det = x0 - 2
    out, y = [], int(T) - 4
    while y <= int(B) + 4:
        if g[y, det] > thr:
            ys = []
            while y <= int(B) + 6 and g[y, det] > thr * 0.5:
                ys.append(y); y += 1
            ys = np.array(ys); w = g[ys, det].astype(float)
            yc = float((ys * w).sum() / w.sum()); yr = int(round(yc))
            n = 0
            while g[yr, x0 - n] > thr and n <= 20:
                n += 1
            out.append((yc, n))
        else:
            y += 1
    return out


def ticks_x(g, yc, L, R, thr=60):
    y0 = int(np.ceil(yc)) + 1
    det = y0 + 1
    W = g.shape[1]
    out, x = [], int(L) - 4
    while x <= min(int(R) + 4, W - 1):
        if g[det, x] > thr:
            xs = []
            while x <= min(int(R) + 6, W - 1) and g[det, x] > thr * 0.5:
                xs.append(x); x += 1
            xs = np.array(xs); w = g[det, xs].astype(float)
            xc = float((xs * w).sum() / w.sum()); xr = int(round(xc))
            n = 0
            while g[y0 + n, xr] > thr and n <= 20:
                n += 1
            out.append((xc, n))
        else:
            x += 1
    return out


def fit_axis(ticks, values, desc=False, major_len=6):
    maj = sorted([t for t in ticks if t[1] >= major_len], key=lambda t: t[0], reverse=desc)
    if len(maj) != len(values):
        raise RuntimeError(f"주눈금 {len(maj)}개 ≠ 라벨 {len(values)}개: {maj}")
    p = np.array([t[0] for t in maj]); v = np.array(values, float)
    A = np.vstack([np.ones_like(p), p]).T
    coef, *_ = np.linalg.lstsq(A, v, rcond=None)
    return coef, float(np.abs(v - A @ coef).max())


# ── 범례 · 배경 ──────────────────────────────────────────────────────────────
def find_legend(rgb, L, T, R, B):
    """가장 큰 순백 연결영역 = 범례 상자 (테두리가 옅은 회색이라 선 검출은 못 믿는다 — S2b 실측)."""
    y0, y1, x0, x1 = int(T) + 3, int(B) - 3, int(L) + 3, int(R) - 3
    white = rgb[y0:y1, x0:x1].min(axis=2) >= 250
    lab, _ = ndimage.label(white)
    best, barea = None, 0
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        if sl is None:
            continue
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        area = int((lab[sl] == i).sum())
        if w > 100 and h > 80 and area > barea:
            best, barea = (sl[1].start + x0 - 1, sl[0].start + y0 - 1, sl[1].stop + x0, sl[0].stop + y0), area
    return best


def legend_colors(rgb, box):
    x0, y0, x1, y1 = box
    reg = rgb[y0 + 2:y1 - 1, x0 + 2:x1 - 1].astype(int)
    lab, n = ndimage.label((reg.max(axis=2) - reg.min(axis=2)) > 60)
    blobs = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < 15:
            continue
        cy, cx = ys.mean(), xs.mean()
        d = np.hypot(ys - cy, xs - cx)
        blobs.append((cy, reg[ys[d < 2.5], xs[d < 2.5]].mean(axis=0)))
    blobs.sort(key=lambda b: b[0])
    return [b[1] for b in blobs]


def background_model(rgb, L, T, R, B, legend):
    bg = np.zeros((rgb.shape[1], 3))
    ys = np.arange(int(T) + 2, int(B) - 1)
    for x in range(int(L) + 2, int(R) - 1):
        keep = np.ones_like(ys, bool)
        if legend and legend[0] - 2 <= x <= legend[2] + 2:
            keep &= ~((ys >= legend[1] - 2) & (ys <= legend[3] + 2))
        bg[x] = np.median(rgb[ys[keep], x].astype(float), axis=0)
    return bg


# ── 마커 검출 (1차: 원판 정합 필터) ─────────────────────────────────────────
def detect(rgb, bg, colors, L, T, R, B, legend, r_disk=4.5, min_frac=0.35):
    x0, x1, y0, y1 = int(L) + 2, int(R) - 1, int(T) + 2, int(B) - 1
    sub = rgb[y0:y1, x0:x1].astype(float)
    dbg = np.linalg.norm(sub - bg[x0:x1][None, :, :], axis=2)
    C = np.array(colors, float)
    dcol = np.stack([np.linalg.norm(sub - c[None, None, :], axis=2) for c in C])
    nearest, dmin = dcol.argmin(axis=0), dcol.min(axis=0)
    is_marker = (dmin < 55.0) & (dbg > 45.0)
    is_bg = dbg < 25.0
    excl = np.zeros(sub.shape[:2], bool)
    if legend:
        ex0, ey0, ex1, ey1 = legend
        excl[max(0, ey0 - 3 - y0):max(0, ey1 + 4 - y0), max(0, ex0 - 3 - x0):max(0, ex1 + 4 - x0)] = True
    rr = int(np.ceil(r_disk))
    yy, xx = np.mgrid[-rr:rr + 1, -rr:rr + 1]
    disk = (np.hypot(yy, xx) <= r_disk).astype(float)
    found = []
    for si in range(len(C)):
        w = np.zeros(sub.shape[:2])
        w[is_marker & (nearest == si)] = 1.0
        w[is_bg] = -1.0
        w[excl] = 0.0
        score = ndimage.correlate(w, disk, mode="constant", cval=0.0)
        mx = ndimage.maximum_filter(score, size=int(1.6 * r_disk))
        for (py, px) in np.argwhere((score == mx) & (score > min_frac * disk.sum())):
            ys, xs = slice(max(0, py - 1), py + 2), slice(max(0, px - 1), px + 2)
            s = score[ys, xs] - score[ys, xs].min()
            gy, gx = np.mgrid[ys, xs]
            cy = (gy * s).sum() / s.sum() if s.sum() > 0 else py
            cx = (gx * s).sum() / s.sum() if s.sum() > 0 else px
            found.append((si, cx + x0, cy + y0))
    return found


# ── 마커 중심 (2차: 가림 인지 고정반경 원 맞춤) ─────────────────────────────
def fit_center(O, G, cx0, cy0, R, rad=3.0, step=0.1, win=9):
    H, W = O.shape
    ix0, iy0 = int(round(cx0)), int(round(cy0))
    ys = np.arange(max(0, iy0 - win), min(H, iy0 + win + 1))
    xs = np.arange(max(0, ix0 - win), min(W, ix0 + win + 1))
    YY, XX = np.meshgrid(ys, xs, indexing="ij")
    o = O[np.ix_(ys, xs)].ravel(); g = G[np.ix_(ys, xs)].ravel()
    valid = o | g
    px, py, ov = XX.ravel()[valid], YY.ravel()[valid], o[valid]
    offs = np.arange(-rad, rad + 1e-9, step)
    DX, DY = np.meshgrid(offs, offs)
    CX, CY = cx0 + DX.ravel(), cy0 + DY.ravel()
    ind = np.hypot(px[None, :] - CX[:, None], py[None, :] - CY[:, None]) <= R
    costs = (ind != ov[None, :]).sum(axis=1)
    cost = int(costs.min()); sel = costs == cost
    cx, cy = CX[sel].mean(), CY[sel].mean()
    n_own = int((o & (np.hypot(XX - cx, YY - cy) <= R).ravel()).sum())
    return cx, cy, cost, n_own


def digitize_scatter(rgb, fig, overlay=None):
    spec = PANELS[fig]; R = spec["R"]
    g = 255 - rgb.max(axis=2).astype(int)
    rows = []
    dr = ImageDraw.Draw(overlay) if overlay is not None else None
    for (pid, material, cls, (L, T, Rr, B), ystep, nmaj) in spec["panels"]:
        xc, yc = refine_axis(g, L, T, Rr, B)
        cy, ry = fit_axis(ticks_y(g, xc, T, B), [ystep * i for i in range(nmaj)], desc=True)
        cx, rx = fit_axis(ticks_x(g, yc, L, Rr), [50.0 * i for i in range(11)])
        legend = find_legend(rgb, L, T, Rr, B)
        colors = legend_colors(rgb, legend)
        if len(colors) != 5:
            raise RuntimeError(f"{pid}: 범례 마커 {len(colors)}개 (5개여야 한다)")
        bg = background_model(rgb, L, T, Rr, B, legend)
        box = (int(L) + 2, int(T) + 2, int(Rr) - 1, int(B) - 1)
        cand = {s: [] for s in range(5)}
        for mf in (0.35, 0.10):                       # 1차 후보 + 가려진 점을 위한 낮은 문턱 후보
            for (s, x, y) in detect(rgb, bg, colors, L, T, Rr, B, legend, min_frac=mf):
                cand[s].append((x - box[0], y - box[1]))
        sub = rgb[box[1]:box[3], box[0]:box[2]].astype(float)
        bgs = bg[box[0]:box[2]][None, :, :]
        X = np.zeros(sub.shape[:2], bool)
        ex0, ey0, ex1, ey1 = legend
        X[max(0, ey0 - 3 - box[1]):max(0, ey1 + 4 - box[1]), max(0, ex0 - 3 - box[0]):max(0, ex1 + 4 - box[0])] = True
        Gm = (np.linalg.norm(sub - bgs, axis=2) < T_BG) & ~X
        print(f"  {pid:4s} {material:20s} 축잔차 y {ry:.1e} S/cm · x {rx:.2f} MPa · "
              f"1 px = {abs(cy[1]) * 1e3:.4f} mS/cm", file=sys.stderr)
        for s in range(5):
            O = (np.linalg.norm(sub - np.array(colors[s])[None, None, :], axis=2) < T_OWN) & ~X
            fits = []
            for (x0_, y0_) in cand[s]:
                fx, fy, cost, n_own = fit_center(O, Gm, x0_, y0_, R)
                if n_own >= MIN_OWN:
                    fits.append((fx, fy, cost, n_own))
            merged = []
            for f in sorted(fits, key=lambda f: -f[3]):
                if all(np.hypot(f[0] - m[0], f[1] - m[1]) >= 2.0 for m in merged):
                    merged.append(f)
            for (fx, fy, cost, n_own) in merged:
                Xp, Yp = fx + box[0], fy + box[1]
                flag = "occluded" if n_own < 25 else ("neighbor_overlap" if cost > 40 else "ok")
                rows.append(dict(figure=fig, panel=pid, material=material, cls=cls,
                                 series=f"fab {FAB[s]:.2f} MPa",
                                 x_name="stack_pressure", x=cx[0] + cx[1] * Xp, x_unit="MPa",
                                 y_name="sigma_ion", y=cy[0] + cy[1] * Yp, y_unit="S/cm",
                                 fit_cost=cost, own_px=n_own, flag=flag))
                if dr is not None:
                    dr.ellipse([Xp - R, Yp - R, Xp + R, Yp + R], outline=(255, 255, 255))
                    dr.point((Xp, Yp), fill=(0, 0, 0))
    return rows


# ── 보조 그림 (블롭 중심 판독) ──────────────────────────────────────────────
def blobs(rgb, color, region, excl=(), tol=70, min_area=20):
    x0, y0, x1, y1 = region
    d = np.linalg.norm(rgb.astype(float) - np.array(color, float)[None, None, :], axis=2)
    m = np.zeros(d.shape, bool); m[y0:y1, x0:x1] = d[y0:y1, x0:x1] < tol
    for (a, b, c, e) in excl:
        m[b:e, a:c] = False
    lab, n = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), start=1):
        ys, xs = np.nonzero(lab == i)
        if len(ys) < min_area:
            continue
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        out.append((xs.mean(), ys.mean(), len(ys), len(ys) / float(h * w)))
    return out


def lin(p, v):
    return np.polyfit(np.array(p, float), np.array(v, float), 1)


def digitize_aux(imgs):
    rows = []
    # Fig. S3 — 밀도 (g/cm3) vs 제작압.  y 주눈금 0.4…2.0 (9개) — 명암가중 눈금 중심(판독 원본값).
    s3 = imgs["S3"]
    cy = lin([544.3, 488.9, 433.8, 378.6, 323.5, 268.4, 213.1, 157.9, 102.8], [0.4 + 0.2 * i for i in range(9)])
    fabx = {191: 97.34, 292: 194.69, 394: 292.03, 495: 389.30, 597: 486.73}
    leg3 = (226, 349, 727, 536)
    names = {("green", "square"): "uC-Li6PS5Cl", ("green", "circle"): "GC-Li6PS5Cl",
             ("orange", "square"): "uC-Li6PS5Br", ("orange", "circle"): "AM(=GC/BMO)-Li6PS5Br",
             ("purple", "square"): "uC-Li5.5PS4.5Cl1.5", ("purple", "circle"): "GC-Li5.5PS4.5Cl1.5",
             ("darkred", "square"): "uC-LGPS", ("darkred", "circle"): "AM-80Li2S-20P2S5"}
    for cname, col in (("green", (0, 128, 0)), ("orange", (255, 128, 0)), ("purple", (128, 0, 128)),
                       ("darkred", (128, 0, 0))):
        for (x, y, a, fill) in blobs(s3, col, (154, 77, 734, 542), excl=[leg3], tol=60):
            # 겹친 마커는 모양 판정이 틀린다 (실측: 97 MPa 의 LGPS µC 네모가 윗변이 가려져 fill 0.89 →
            #   '원'으로 오판).  온전한 단독 마커만 이름을 붙이고 나머지는 **미배정**으로 둔다.
            if fill > 0.95 and 75 <= a <= 105:
                shape = "square"
            elif 0.74 <= fill <= 0.84 and 80 <= a <= 100:
                shape = "circle"
            else:
                shape = "unassigned"
            fab = fabx[min(fabx, key=lambda k: abs(k - x))]
            flag = "ok" if shape != "unassigned" else "overlap_not_separable"
            rows.append(dict(figure="S3", panel="S3", material=names.get((cname, shape), cname + " (unassigned)"),
                             cls="", series=f"{cname} {shape}", x_name="fabrication_pressure", x=fab,
                             x_unit="MPa", y_name="density", y=float(np.polyval(cy, y)), y_unit="g/cm3",
                             fit_cost="", own_px=a, flag=flag))
    # Fig. S4a — log10 σ vs 제작압 (Au 스퍼터, stack ~10 MPa);  S4b — Ea vs 제작압
    s4 = imgs["S4"]
    ca = lin([11.2, 150.7, 290.4, 430.3], [-2, -3, -4, -5])
    cxa = lin([93.4, 188.3, 283.0, 377.7, 472.6, 567.5], [0, 100, 200, 300, 400, 500])
    cb = lin([8.6, 78.5, 148.5, 218.4, 288.2, 357.9, 427.7], [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20])
    cxb = lin([737.3, 832.0, 926.7, 1021.6, 1116.5, 1211.4], [0, 100, 200, 300, 400, 500])
    lab4 = {"navy": "GC-Li6PS5Br (legend 'BMO')", "orange": "uC-Li6PS5Br before pellet annealing",
            "green": "uC-Li6PS5Br after pellet annealing (550 C)"}
    cols4 = {"navy": (0, 0, 160), "orange": (255, 128, 0), "green": (0, 128, 0)}
    for cname, col in cols4.items():
        for (x, y, a, _f) in blobs(s4, col, (96, 14, 612, 427), excl=[(195, 316, 605, 425)]):
            rows.append(dict(figure="S4", panel="S4a", material=lab4[cname], cls="", series=cname,
                             x_name="fabrication_pressure", x=float(np.polyval(cxa, x)), x_unit="MPa",
                             y_name="sigma_ion", y=float(10 ** np.polyval(ca, y)), y_unit="S/cm",
                             fit_cost="", own_px=a, flag="ok"))
        for (x, y, a, _f) in blobs(s4, col, (740, 11, 1255, 318)):
            rows.append(dict(figure="S4", panel="S4b", material=lab4[cname], cls="", series=cname,
                             x_name="fabrication_pressure", x=float(np.polyval(cxb, x)), x_unit="MPa",
                             y_name="Ea", y=float(np.polyval(cb, y)), y_unit="eV",
                             fit_cost="", own_px=a, flag="ok"))
    # Fig. S5 — 반원 끝(최저 −Z″ 군집 중심).  군집 중심이라 정확한 최저점이 아니다 (flag).
    s5 = imgs["S5"]
    czy = lin([544.6, 450.8, 357.0, 263.0, 169.4, 75.4], [0, 1e6, 2e6, 3e6, 4e6, 5e6])
    czx = lin([152.4, 269.4, 386.1, 502.6, 619.5, 736.5], [0, 1e6, 2e6, 3e6, 4e6, 5e6])
    for cname, col, fab, win in (("navy", (0, 0, 160), 97.34, (3.3e6, 4.4e6)),
                                 ("orange", (255, 128, 0), 389.30, (0.5e6, 1.3e6))):
        pts = []
        for (x, y, a, _f) in blobs(s5, col, (154, 75, 737, 545), excl=[(150, 75, 420, 180)], tol=80, min_area=6):
            Zr, Zi = float(np.polyval(czx, x)), float(np.polyval(czy, y))
            if win[0] < Zr < win[1]:
                pts.append((Zi, Zr, a))
        if pts:
            Zi, Zr, a = min(pts)
            rows.append(dict(figure="S5", panel="S5", material="GC-Li6PS5Br, -80 C", cls="GC",
                             series=f"fab {fab:.2f} MPa", x_name="Z_real_semicircle_end", x=Zr,
                             x_unit="Ohm cm2", y_name="minus_Z_imag", y=Zi, y_unit="Ohm cm2",
                             fit_cost="", own_px=a, flag="cluster_centroid"))
    return rows


def main():
    ap = argparse.ArgumentParser(description="Cronau 2021 SI 그림 디지타이즈 (값은 전부 digitized)")
    ap.add_argument("--pdf", required=True, help="ACS SI PDF (nz1c01299_si_001.pdf)")
    ap.add_argument("--csv", default=str(ROOT / "litdb" / "figures" / SLUG / "si_digitized.csv"))
    ap.add_argument("--overlay-dir", default="", help="맞춘 원을 그린 검증용 PNG 를 둘 곳")
    a = ap.parse_args()
    doc = fitz.open(a.pdf)
    imgs = {"S1": page_images(doc, 4)[0][1], "S2": page_images(doc, 5)[0][1]}
    p6 = page_images(doc, 6)
    imgs["S3"], imgs["S4"] = p6[0][1], p6[1][1]
    imgs["S5"] = page_images(doc, 7)[0][1]
    for k, need in (("S1", (1447, 1260)), ("S2", (987, 1258))):
        if imgs[k].shape[:2] != need:
            sys.exit(f"⛔ {k} 래스터 크기 {imgs[k].shape[:2]} ≠ {need} — 다른 판본의 SI 다. 패널 틀을 다시 잡을 것.")
    rows = []
    for fig in ("S1", "S2"):
        ov = Image.fromarray(imgs[fig]) if a.overlay_dir else None
        rows += digitize_scatter(imgs[fig], fig, ov)
        if ov is not None:
            os.makedirs(a.overlay_dir, exist_ok=True)
            ov.save(os.path.join(a.overlay_dir, f"overlay_{fig}.png"))
    rows += digitize_aux(imgs)
    rows.sort(key=lambda r: (r["figure"], r["panel"], str(r["series"]), r["x"]))
    Path(a.csv).parent.mkdir(parents=True, exist_ok=True)
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["# Cronau 2021 ACS Energy Lett. 6, 3072 — SI (nz1c01299_si_001.pdf) figure readout. "
                    "ALL VALUES DIGITIZED (not stated in text). tools/litdb/cronau2021_si_digitize.py"])
        w.writerow(["figure", "panel", "material", "class", "series", "x_name", "x_value", "x_unit",
                    "y_name", "y_value", "y_unit", "fit_cost", "own_px", "flag", "provenance"])
        for r in rows:
            yv = f"{r['y']:.5e}" if r["y_unit"] in ("S/cm", "Ohm cm2") else f"{r['y']:.4f}"
            xv = f"{r['x']:.4e}" if r["x_unit"] == "Ohm cm2" else f"{r['x']:.2f}"
            w.writerow([r["figure"], r["panel"], r["material"], r["cls"], r["series"], r["x_name"], xv,
                        r["x_unit"], r["y_name"], yv, r["y_unit"], r["fit_cost"], r["own_px"], r["flag"],
                        "digitized"])
    print(f"✓ {len(rows)} 행 → {a.csv}", file=sys.stderr)


if __name__ == "__main__":
    main()
