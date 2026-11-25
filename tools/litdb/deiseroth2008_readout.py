#!/usr/bin/env python3
"""deiseroth2008_readout.py — Deiseroth et al., Angew. Chem. Int. Ed. 47, 755 (2008) · `Fig. 2` 픽셀 판독.

카드: litdb/papers/deiseroth2008_li6ps5x_argyrodite_high_li_mobility.md  (§3 · §5 · §10)
원본: 본문 PDF 4 쪽 (SI 없음 — 결정 자료는 CSD 418488–418490 기탁).  ⚠ PDF 는 리포에 없다.
      `Fig. 2` (정적 ⁷Li NMR 선폭 FWHH vs T, 세 조성 세 판) 는 **1-bit CCITT 스텐실 래스터**
      (page 2 · 1322×1128 px · ImageMask) 다 — 벡터 좌표가 없어서 픽셀에서 읽는다.

⛔ 이 스크립트가 내는 값은 전부 **판독 (figure-read)** 이다.  카드에 옮길 때 `figure-read ≈` 표지를 떼지 말 것.
   논문이 숫자로 적은 것은 본문 문장뿐이다: "around 6000 Hz for the iodide and chloride" (140–160 K) ·
   Br 은 "rigid linewidth is not reached at 140 K, which is the lowest accessible temperature" ·
   "line-narrowing process is completed at 200 K" · I 는 "two-step … restricted motion … (170–250 K)".

무엇을 하나
  (1) PDF 에서 `Fig. 2` 래스터를 꺼낸다 (크기 · ImageMask 가 기대와 다르면 **읽지 않고 멈춘다**).
      극성은 '잉크가 소수' 규칙으로 정한다 (PyMuPDF 가 스텐실 마스크를 반전된 극성으로 줄 수 있다).
  (2) 축: y 축 = 가장 긴 세로 잉크 열 (세 판이 같은 열 · 세 토막) · x 축 = 가장 아래의 긴 가로 잉크 행.
      눈금: x 는 축 아래로 뻗은 짧은 세로선 18 개 (긴 것 9 = 140…300 K · 짧은 것 9 = 130…290 K) ·
      y 는 판마다 축 왼쪽으로 뻗은 가로선 6 개 (위→아래 6000…1000 Hz, 글자 라벨은 6000·4000·2000 에만).
      값 배정은 순서로 하고, 선형 최소제곱 잔차가 1 px 를 넘으면 멈춘다.
  (3) 마커: y 축 두 열을 지운 뒤 8-연결 성분 → 크기 거름 (가로·세로 15–21 px; 범례 글자는 27–30 px 라 빠진다).
      y 축 위에 걸친 마커 (Cl · Br 의 맨 왼쪽 점) 는 오른쪽 반쪽만 남는다 → 같은 판 마커 너비의 중앙값으로 중심을 복원한다.
  (4) 본문 문장과 대조 (`checks`) + 유도량 (반폭 온도 T½ — **우리 산수**).
검증 (출력 · 개수 불일치는 종료 코드 1)
  · 판마다 마커 17 개 (Cl · Br 130–280 K + 295 K · I 140–300 K) — 다르면 실패.
  · 본문 문장 네 개를 판독값으로 대조 (판정이 아니라 보고 — 어긋나면 그대로 적는다).
이 도구가 못 하는 것
  · 다른 판본의 PDF (그림 해상도 · 배치가 다르면) — 래스터 크기가 1322×1128 이 아니면 멈춘다.
  · 마커 중심 = 상자 중심으로 읽는다. 삼각형 (I 판) 은 무게중심과 상자 중심이 h/6 ≈ 3 px (≈ 60 Hz) 어긋난다 —
    Origin 이 어느 쪽에 찍는지 모르므로 I 값에는 ±60 Hz 의 계통 모호성이 있다 (□ ○ 는 ±20 Hz 안).
  · 선폭의 원 스펙트럼은 없다 — FWHH 를 어떻게 쟀는지 (적합 · 직독) 논문이 적지 않았다.
  · 유도량 T½ (첫 점과 끝 점 선폭의 중간값을 지나는 온도, 선형 보간) 은 우리 정의다. 논문 값이 아니다.
    '경직 선폭' 기준점이 Br 은 측정창 밖이라 (논문 문장) Br 의 T½ 는 **상한**으로만 읽는다.
usage
  ~/.venvs/litdb/bin/python3 tools/litdb/deiseroth2008_readout.py --pdf "<본문>.pdf"
  python3 tools/litdb/deiseroth2008_readout.py --selftest     # 합성 그림으로 양성 + 음성 경로
출력
  litdb/figures/deiseroth2008_li6ps5x_argyrodite_high_li_mobility/digitized.csv
  (열: figure, compound, marker, T_K, FWHH_Hz, x_px, y_px, note)
"""
import argparse
import csv
import io
import sys
from collections import deque
from pathlib import Path

import numpy as np

SLUG = "deiseroth2008_li6ps5x_argyrodite_high_li_mobility"
ROOT = Path(__file__).resolve().parents[2]
RASTER_SHAPE = (1128, 1322)              # (h, w) of the Fig. 2 ImageMask on page 2
PANELS = ("Li6PS5Cl", "Li6PS5Br", "Li6PS5I")
MARKERS = ("square", "circle", "triangle")
X_MAJOR = [140 + 20 * i for i in range(9)]     # long ticks, labelled
X_MINOR = [130 + 20 * i for i in range(9)]     # short ticks
Y_TICKS = [6000, 5000, 4000, 3000, 2000, 1000]  # top → bottom, same length
N_EXPECT = 17
MK_MIN, MK_MAX = 15, 21                  # marker bbox (px)
TICK_MIN = 15                            # tick length (px); split-marker edges are ~8


class ReadoutError(RuntimeError):
    pass


# ---------------------------------------------------------------- raster in
def check_raster_shape(shape):
    if tuple(shape) != RASTER_SHAPE:
        raise ReadoutError(f"Fig. 2 raster is {shape}, expected {RASTER_SHAPE} — different PDF edition? refusing")


def raster_from_pdf(pdf):
    import pymupdf
    from PIL import Image
    doc = pymupdf.open(str(pdf))
    page = doc[1]
    cand = [im for im in page.get_images(full=True) if (im[3], im[2]) == RASTER_SHAPE]
    if len(cand) != 1:
        raise ReadoutError(f"page 2: {len(cand)} image(s) of size {RASTER_SHAPE[::-1]} (expected 1) — refusing")
    xref = cand[0][0]
    if "/ImageMask true" not in doc.xref_object(xref, compressed=True):
        raise ReadoutError("Fig. 2 image is not an ImageMask — different PDF edition? refusing")
    a = np.array(Image.open(io.BytesIO(doc.extract_image(xref)["image"])).convert("L"))
    check_raster_shape(a.shape)
    return ink_from_gray(a)


def ink_from_gray(a):
    ink = a < 128
    if ink.mean() > 0.5:                 # stencil mask came back inverted
        ink = ~ink
    return ink


# ---------------------------------------------------------------- geometry
def runs(v):
    out, s = [], None
    for i, x in enumerate(v):
        if x and s is None:
            s = i
        elif not x and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(v) - 1))
    return out


def find_axes(ink):
    h, w = ink.shape
    colbest = [max([b - a + 1 for a, b in runs(ink[:, c])] or [0]) for c in range(w // 3)]
    ycols = [c for c, n in enumerate(colbest) if n >= 0.9 * max(colbest)]
    if not ycols or max(ycols) - min(ycols) > 3:
        raise ReadoutError(f"y-axis columns not found / not contiguous: {ycols}")
    segs = [r for r in runs(ink[:, ycols[0]]) if r[1] - r[0] > 0.15 * h]
    if len(segs) != 3:
        raise ReadoutError(f"expected 3 y-axis segments (3 panels), got {len(segs)}")
    rowbest = [max([b - a + 1 for a, b in runs(ink[r, :])] or [0]) for r in range(h)]
    xrows = [r for r in range(h // 2, h) if rowbest[r] >= 0.6 * w]
    if not xrows or max(xrows) - min(xrows) > 4:
        raise ReadoutError(f"x-axis rows not found / not contiguous: {xrows}")
    return ycols, segs, xrows


def group(idx):
    out, cur = [], []
    for i in idx:
        if cur and i != cur[-1] + 1:
            out.append(cur)
            cur = []
        cur.append(i)
    if cur:
        out.append(cur)
    return out


def x_ticks(ink, ycols, xrows):
    r0 = max(xrows) + 1
    lens = []
    for c in range(ink.shape[1]):
        n, r = 0, r0
        while r < ink.shape[0] and ink[r, c]:
            n += 1
            r += 1
        lens.append(n)
    ticks = []
    for g in group([c for c, n in enumerate(lens) if n >= 3]):
        ticks.append((float(np.mean(g)), max(lens[c] for c in g)))
    long_ = [t for t in ticks if t[1] >= TICK_MIN]
    short = [t for t in ticks if t[1] < TICK_MIN]
    if len(long_) != len(X_MAJOR) or len(short) != len(X_MINOR):
        raise ReadoutError(f"x ticks: {len(long_)} long / {len(short)} short (expected 9 / 9) — refusing")
    px = [t[0] for t in long_] + [t[0] for t in short]
    val = X_MAJOR + X_MINOR
    return fit(px, val, "x")


def y_ticks(ink, ycols, seg):
    c0 = min(ycols) - 1
    rows = []
    for r in range(seg[0], seg[1] + 1):
        n, c = 0, c0
        while c >= 0 and ink[r, c]:
            n += 1
            c -= 1
        if n >= TICK_MIN:
            rows.append(r)
    centers = [float(np.mean(g)) for g in group(rows)]
    if len(centers) != len(Y_TICKS):
        raise ReadoutError(f"y ticks in panel rows {seg}: {len(centers)} (expected 6) — refusing")
    return fit(sorted(centers), Y_TICKS, "y")


def fit(px, val, name):
    px, val = np.asarray(px, float), np.asarray(val, float)
    A = np.vstack([px, np.ones_like(px)]).T
    (m, b), *_ = np.linalg.lstsq(A, val, rcond=None)
    res_px = np.abs(px - (val - b) / m)
    if res_px.max() > 1.0:
        raise ReadoutError(f"{name} calibration residual {res_px.max():.2f} px > 1 px — refusing")
    return float(m), float(b), float(res_px.max())


# ---------------------------------------------------------------- markers
def components(mask):
    h, w = mask.shape
    seen = np.zeros(mask.shape, bool)
    out = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        q = deque([(y0, x0)])
        seen[y0, x0] = True
        pts = []
        while q:
            y, x = q.popleft()
            pts.append((y, x))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
        py = [p[0] for p in pts]
        px = [p[1] for p in pts]
        out.append((min(px), min(py), max(px), max(py), len(pts)))
    return out


def panel_bounds(segs, xrows, h):
    """Row band of each panel = midpoints of the gaps between y-axis segments.

    ⚠ Not the segment itself: in the real figure the Br markers at 280 · 295 K hang **below** the end
      of the Br y-axis segment (rows 659–665 vs segment end 656) — clipping at the segment cut them
      in half and the size filter dropped them (first run: 15/17).
    """
    out = []
    for i, s in enumerate(segs):
        lo = 0 if i == 0 else (segs[i - 1][1] + s[0]) // 2
        hi = (min(xrows) - 1) if i == len(segs) - 1 else (s[1] + segs[i + 1][0]) // 2
        out.append((lo, min(hi, h - 1)))
    return out


def read_markers(ink, ycols, band, xrows):
    m = ink.copy()
    m[:, min(ycols):max(ycols) + 1] = False
    m[min(xrows):max(xrows) + 1, :] = False
    sub = np.zeros_like(m)
    lo, hi = band
    sub[lo:hi + 1, max(ycols) + 1:] = m[lo:hi + 1, max(ycols) + 1:]
    seg = band
    full, split, rejected = [], [], 0
    for x0, y0, x1, y1, n in components(sub):
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if MK_MIN <= w <= MK_MAX and MK_MIN <= h <= MK_MAX:
            full.append(((x0 + x1) / 2.0, (y0 + y1) / 2.0, w, ""))
        elif x0 <= max(ycols) + 2 and 5 <= w < MK_MIN and MK_MIN <= h <= MK_MAX:
            split.append((x1, (y0 + y1) / 2.0))
        else:
            rejected += 1
    if not full:
        raise ReadoutError(f"no markers in panel rows {seg}")
    wmed = float(np.median([f[2] for f in full]))
    for x1, yc in split:
        full.append((x1 - (wmed - 1) / 2.0, yc, wmed, "on y-axis line: centre rebuilt from right half + median width"))
    full.sort(key=lambda t: t[0])
    return full, rejected


def readout(ink):
    ycols, segs, xrows = find_axes(ink)
    mx, bx, rx = x_ticks(ink, ycols, xrows)
    rows, info = [], {"x_res_px": rx, "panels": []}
    bands = panel_bounds(segs, xrows, ink.shape[0])
    for name, mk, seg, band in zip(PANELS, MARKERS, segs, bands):
        my, by, ry = y_ticks(ink, ycols, seg)
        pts, rej = read_markers(ink, ycols, band, xrows)
        info["panels"].append({"compound": name, "n": len(pts), "rejected": rej, "y_res_px": ry})
        for xc, yc, _w, note in pts:
            rows.append({"figure": "Fig. 2", "compound": name, "marker": mk,
                         "T_K": round(mx * xc + bx, 1), "FWHH_Hz": round(my * yc + by),
                         "x_px": round(xc, 1), "y_px": round(yc, 1), "note": note})
    return rows, info


# ---------------------------------------------------------------- text checks
def series(rows, name):
    s = sorted((r["T_K"], r["FWHH_Hz"]) for r in rows if r["compound"] == name)
    return [t for t, _ in s], [f for _, f in s]


def at(T, F, t0, tol=2.0):
    for t, f in zip(T, F):
        if abs(t - t0) <= tol:
            return f
    return None


def t_half(T, F):
    mid = (F[0] + F[-1]) / 2.0
    for i in range(1, len(T)):
        if F[i - 1] >= mid >= F[i]:
            return T[i - 1] + (T[i] - T[i - 1]) * (F[i - 1] - mid) / max(F[i - 1] - F[i], 1e-9), mid
    return None, mid


def checks(rows, info):
    ok = True
    out = []
    for p in info["panels"]:
        good = p["n"] == N_EXPECT
        ok &= good
        out.append(f"[{'ok' if good else 'FAIL'}] {p['compound']}: {p['n']} markers (expected {N_EXPECT}) · "
                   f"rejected comps {p['rejected']} · y-cal residual {p['y_res_px']:.2f} px")
    out.append(f"[info] x-cal residual {info['x_res_px']:.2f} px · 1 px = "
               f"{10.0 / 66.2:.2f} K (x) · ≈ 20 Hz (y)")
    sc = {n: series(rows, n) for n in PANELS}
    tmin = {n: sc[n][0][0] for n in PANELS}
    out.append("[report] lowest T per series: " + " · ".join(f"{n} {tmin[n]:.1f} K" for n in PANELS)
               + "  ← text: '140 K, which is the lowest accessible temperature' / Exp. '140–300 K'")
    cl140, br140, i140 = (at(*sc[n], 140) for n in PANELS)
    out.append(f"[report] 140 K: Cl {cl140} · Br {br140} · I {i140} Hz  ← text: 'around 6000 Hz for the iodide and chloride'")
    Tb, Fb = sc["Li6PS5Br"]
    drop = Fb[0] - Fb[-1]
    f200 = at(Tb, Fb, 200)
    out.append(f"[report] Br: {Fb[0]} Hz @ {Tb[0]:.0f} K → {f200} Hz @ 200 K → {Fb[-1]} Hz @ {Tb[-1]:.0f} K · "
               f"share of total drop done by 200 K = {(Fb[0] - f200) / drop:.0%}  ← text: 'completed at 200 K'")
    Ti, Fi = sc["Li6PS5I"]
    s1 = (at(Ti, Fi, 140) - at(Ti, Fi, 160)) / 20.0
    s2 = (at(Ti, Fi, 170) - at(Ti, Fi, 250)) / 80.0
    s3 = (at(Ti, Fi, 260) - at(Ti, Fi, 300)) / 40.0
    out.append(f"[report] I slopes (Hz/K): 140→160 {s1:.0f} · 170→250 {s2:.1f} · 260→300 {s3:.1f}  "
               "← text: 'two-step narrowing … restricted motion at intermediate temperatures (170–250 K)'")
    for n in PANELS:
        th, mid = t_half(*sc[n])
        tag = " (upper bound: rigid limit not reached in window)" if n == "Li6PS5Br" else ""
        out.append(f"[ours] T½ {n}: {th:.0f} K (midpoint {mid:.0f} Hz between first and last point){tag}")
    return ok, out


# ---------------------------------------------------------------- selftest
def synth(values, h=RASTER_SHAPE[0], w=RASTER_SHAPE[1], drop_major_x=None, letter=False):
    """Draw a 3-panel figure with the real layout; values = {panel: [(T, F), ...]}."""
    ink = np.zeros((h, w), bool)
    ycol = (172, 173)
    segs = [(12, 308), (359, 655), (706, 1004)]
    xrow = (1002, 1004)
    ink[xrow[0]:xrow[1] + 1, 172:1299] = True
    for s in segs:
        ink[s[0]:s[1] + 1, ycol[0]:ycol[1] + 1] = True
    X = lambda T: 172.5 + (T - 130) * 6.62
    for i, T in enumerate(X_MAJOR):
        if i == drop_major_x:
            continue
        c = int(round(X(T)))
        ink[1005:1025, c - 1:c + 2] = True
    for T in X_MINOR:
        c = int(round(X(T)))
        ink[1005:1014, c - 1:c + 2] = True
    tick0 = [31.5, 379.0, 725.5]
    for k, s in enumerate(segs):
        for j in range(6):
            r = int(round(tick0[k] + 50.4 * j))
            ink[r - 1:r + 2, 151:172] = True
    for k, name in enumerate(PANELS):
        Y = lambda F, k=k: tick0[k] + (6000 - F) / 1000.0 * 50.4
        for T, F in values[name]:
            cx, cy = int(round(X(T))), int(round(Y(F)))
            ink[cy - 9:cy + 10, cx - 9] = ink[cy - 9:cy + 10, cx + 9] = True
            ink[cy - 9, cx - 9:cx + 10] = ink[cy + 9, cx - 9:cx + 10] = True
        if letter:                       # a 28-px tall 'L' inside the panel must be rejected
            r0 = int(tick0[k]) + 80
            ink[r0:r0 + 28, 1040:1043] = True
            ink[r0 + 25:r0 + 28, 1040:1056] = True
    return ink


def selftest():
    ok = True

    def expect(cond, msg):
        nonlocal ok
        print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
        ok &= bool(cond)

    # last two Cl/Br points at 700/600 Hz hang below the end of their y-axis segment (real-figure case)
    truth = {n: [(130 + 10 * i, 6000 - 300 * i) for i in range(15)] + [(280, 700), (295, 600)]
             for n in PANELS[:2]}
    truth[PANELS[2]] = [(140 + 10 * i, 6100 - 280 * i) for i in range(17)]
    try:
        rows, info = readout(synth(truth))
    except ReadoutError as e:          # a refusal on the clean synthetic figure is itself a failure
        expect(False, f"positive: clean synthetic figure is read ({e})")
        print("selftest: FAIL")
        return 1
    got = {n: series(rows, n) for n in PANELS}
    err_t = max(abs(a - b[0]) for n in PANELS for a, b in zip(got[n][0], truth[n]))
    err_f = max(abs(a - b[1]) for n in PANELS for a, b in zip(got[n][1], truth[n]))
    expect(all(p["n"] == N_EXPECT for p in info["panels"]), "positive: 17 markers per panel (incl. 2 on the y-axis line)")
    expect(err_t <= 0.5 and err_f <= 40, f"positive: max |ΔT| {err_t:.2f} K ≤ 0.5 · max |ΔF| {err_f:.0f} Hz ≤ 40")
    # negative 1: wrong raster size → refuse
    try:
        check_raster_shape((1000, 1000))
        expect(False, "negative: wrong raster size is refused")
    except ReadoutError:
        expect(True, "negative: wrong raster size is refused")
    # negative 2: a missing labelled x tick → calibration refuses (not silently re-assigned)
    try:
        readout(synth(truth, drop_major_x=3))
        expect(False, "negative: missing x tick is refused")
    except ReadoutError:
        expect(True, "negative: missing x tick is refused")
    # negative 3: move one marker by +10 K → the reader reports the moved value (comparison is live)
    moved = {n: list(v) for n, v in truth.items()}
    moved[PANELS[0]][5] = (moved[PANELS[0]][5][0] + 10 + 5, moved[PANELS[0]][5][1])
    rows_m, _ = readout(synth(moved))
    tm = series(rows_m, PANELS[0])[0]
    expect(any(abs(t - 195) <= 0.5 for t in tm) and not any(abs(t - 180) <= 0.5 for t in tm),
           "negative: a moved marker is read at its new T (180 → 195 K), not snapped back")
    # negative 4: a letter-sized component inside each panel is rejected by the size filter
    rows_l, info_l = readout(synth(truth, letter=True))
    base_rej = [p["rejected"] for p in info["panels"]]
    expect(all(p["n"] == N_EXPECT and p["rejected"] == b + 1 for p, b in zip(info_l["panels"], base_rej)),
           "negative: a 28-px letter is rejected (one more rejected component per panel), marker count stays 17")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", help="main-text PDF (Angew. Chem. Int. Ed. 2008, 47, 755)")
    ap.add_argument("--out", default=str(ROOT / "litdb" / "figures" / SLUG / "digitized.csv"))
    ap.add_argument("--selftest", action="store_true", help="synthetic figure, positive + negative paths")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.pdf:
        ap.error("--pdf is required (or --selftest)")
    try:
        rows, info = readout(raster_from_pdf(a.pdf))
    except ReadoutError as e:
        print(f"⛔ {e}")
        return 2
    ok, lines = checks(rows, info)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print("\n".join(lines))
    print(f"→ {a.out}  ({len(rows)} rows · figure-read)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
