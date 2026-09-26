#!/usr/bin/env python3
"""shi2019_fig_digitize.py — Shi et al. (Adv. Energy Mater. 2020, 10, 1902881) 본문·SI 그림 **판독**.

카드: litdb/papers/shi2019_high_am_loading_particle_size_assb.md  (§S SI 보강 · §3 ⛔ 정정)
원본: 본문 9 pp (Wiley 인쇄본) + SI `aenm201902881-sup-0001-suppmat.pdf` 8 pp.
⚠ PDF 는 리포에 없다 (litdb/inbox 는 .gitignore).  --main / --si 로 경로를 준다.

⛔ 이 스크립트가 내는 값은 전부 **digitized (그림 판독)** 이다.  본문·SI 에 **숫자로 적힌 값**
   (≈75 · 125 · >150 · 155 mAh/g, θ 98 → 52 %, 52 % vs 25 %, λ_min 2.1, 0.39 mS/cm, Table S3 …)
   은 여기서 만들지 않는다 — 카드가 그것들을 `stated` / `SI-stated` 로 따로 적는다.
   아래 `check` 행은 판독값을 그 stated 값에 대 보는 **검증**이지 새 값이 아니다.

방법
  1. 본문 그림은 쪽마다 래스터 1장 (JPEG, CMYK, ≈300 dpi 원판) → 원판 해상도 그대로 RGB 변환.
     SI Fig. S1 은 RGBA+SMask 라 원판을 떼면 글자가 검은 바탕에 묻힌다 → **쪽 렌더(400 dpi)** 로 판독.
     SI Fig. S2 는 RGB 원판.
  2. 축 보정: 축 안쪽(또는 바깥쪽) 눈금의 픽셀 위치를 검출해 **눈금 라벨 값**에 선형 대응.
     아래 CAL 상수는 그 검출값이다 — 실행할 때 다시 검출해 **2 px 이상 어긋나면 멈춘다** (원판이 바뀐 것).
  3. 마커: 계열 색 마스크 → (속빈 마커는 구멍 채우기) → 형태학적 열림(선 제거) → 연결성분 중심.
     겹쳐 가려진 마커는 `occluded` 로 표시하고 값은 **보이는 부분 추정** (육안 ±3 mAh/g).
  4. 곡선(Fig 3d · 7a): 계열 색 픽셀의 해당 열 중앙값.  색은 범례 선에서 표본 추출
     (Fig 3d: 빨강 ≈(250,0,0) · 주황 ≈(255,90,0) · 초록 ≈(19,170,0) — 주황의 G≈90 이 빨강 문턱과 겹쳐서
     G/R 비로 가른다; 첫 시도에서 빨강 계열이 주황에 오염됐다).
  판독 불확실도 (그림 판독만 — 원문에 오차막대 없음 = n/a):
     Fig 3a/3b θ ±0.005 (1 px) · Fig 3d λ ±0.02 (1 px) — 단 f_CAM ≳ 79 wt% 수직 구간은 λ 가 무의미하게
     민감해 **±0.3 wt%** 로 읽을 것 · Fig 5/6 용량 ±0.5 mAh/g (1 px) + 마커 중심 ±1 · Fig 7a ±0.2 vol% ·
     Fig S1b ±0.2 %p · Fig S2 θ ±0.003.

알려진 원문 표기 이상 (판독에 반영)
  · Fig 5b 위쪽 λ 축 눈금 "2.5 · 1.3 · 0.8 · 0.6" 은 **아래 축 눈금 2 · 4 · 6 · 8 µm 에 대응**하는 값이지
    데이터 점의 λ 가 아니다.  데이터 점은 SE 1.5 / 3 / 5 / 8 µm (λ = 3.33 / 1.67 / 1.00 / 0.625).
  · Fig 5e 가로축은 4–12 µm 로 그려졌지만 점은 CAM **5 µm · 12 µm 두 개뿐**이다 (스윕 아님).
  · Fig 7b 세로축 제목은 "CAM loading (vol%)" 인데 눈금이 60 · 70 · 80 · **80** (맨 위 중복) —
    Fig 3c 의 wt% 눈금(60 · 70 · 80 · 90)과 같은 자리.  Fig 7a 로는 80 wt% ≈ 47.6–59.3 vol% 이므로
    vol% 로 읽으면 앞뒤가 안 맞는다 ⇒ **Fig 7b 세로축은 정량 판독 금지** (여기서도 안 읽는다).
  · SI Fig S1b 세로축 제목은 "f_CAM (%)" 인데 캡션·SI 본문은 "active cathode ratio" (= θ_CAM) 이다.
    값이 38–70 % 로 움직이고 조성은 80:15 고정이므로 θ_CAM 으로 읽는다 (라벨 오기).

usage
  python3 tools/litdb/shi2019_fig_digitize.py --main "<본문.pdf>" --si "<SI.pdf>" \
      [--csv litdb/figures/shi2019_high_am_loading_particle_size_assb/digitized.csv]
"""
import argparse
import csv
import io
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

try:
    import pymupdf as fitz
except ImportError:                                   # 옛 이름
    import fitz

SLUG = "shi2019_high_am_loading_particle_size_assb"
ROOT = Path(__file__).resolve().parents[2]


# ── 원판 꺼내기 ──────────────────────────────────────────────────────────────
def page_raster(doc, pno):
    """쪽의 (유일한) 래스터를 원판 해상도 RGB float 배열로."""
    imgs = doc[pno].get_images(full=True)
    if len(imgs) != 1:
        raise SystemExit(f"p{pno + 1}: 래스터가 1장이 아니다 ({len(imgs)}) — 다른 판본?")
    info = doc.extract_image(imgs[0][0])
    return np.asarray(Image.open(io.BytesIO(info["image"])).convert("RGB"), float)


def page_render(doc, pno, rect, dpi):
    pix = doc[pno].get_pixmap(clip=fitz.Rect(*rect), dpi=dpi)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return np.asarray(im, float)


# ── 눈금 검출 (보정 상수 재확인용) ──────────────────────────────────────────
def group(a):
    out, cur = [], []
    for v in a:
        if cur and v - cur[-1] > 2:
            out.append(float(np.mean(cur)))
            cur = []
        cur.append(v)
    if cur:
        out.append(float(np.mean(cur)))
    return out


def ticks_bottom_in(im, frame, thr=4, span=(3, 12)):
    x0, y0, x1, y1 = frame
    dark = im.max(2) < 120
    band = dark[y1 - span[1]:y1 - span[0], x0 - 3:x1 + 3]
    return group(list(np.where(band.sum(0) >= thr)[0] + x0 - 3))


def ticks_left_in(im, frame, thr=4, span=(3, 12)):
    x0, y0, x1, y1 = frame
    dark = im.max(2) < 120
    band = dark[y0 - 3:y1 + 3, x0 + span[0]:x0 + span[1]]
    return group(list(np.where(band.sum(1) >= thr)[0] + y0 - 3))


def near(found, want, tol=2.0):
    return all(any(abs(f - w) <= tol for f in found) for w in want)


# ── 마커 ────────────────────────────────────────────────────────────────────
def blobs(mask, k=7, amin=12, amax=5000, fill=False):
    m = ndimage.binary_fill_holes(mask) if fill else mask
    m = ndimage.binary_opening(m, structure=np.ones((k, k), bool))
    lab, n = ndimage.label(m)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        a = int((lab[sl] == i).sum())
        if amin <= a <= amax:
            cy, cx = ndimage.center_of_mass(lab == i)
            out.append((cx, cy, a))
    return sorted(out)


def colour(im, kind):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    sat = im.max(2) - im.min(2)
    ratio = G / np.maximum(R, 1)
    return {
        "red": (R > 170) & (G < 120) & (B < 120) & (R - G > 90),
        "red_pure": (sat > 150) & (R > 180) & (ratio < 0.18) & (B < 80),
        "orange": (sat > 150) & (R > 200) & (ratio > 0.28) & (ratio < 0.52) & (B < 60),
        "orange_marker": (R > 200) & (G > 80) & (G < 200) & (B < 120) & (R - B > 100),
        "green": (sat > 100) & (G > R + 60) & (G > B + 60),
        "blue": (B > 120) & (B - R > 60),
        "dark": im.max(2) < 110,
        "black": im.max(2) < 60,
        "gray": (np.abs(R - G) < 12) & (np.abs(G - B) < 12) & (R > 150) & (R < 200),
    }[kind]


ROWS = []


def put(fig, panel, series, xname, x, xunit, yname, y, yunit, flag="ok", note=""):
    ROWS.append(dict(figure=fig, panel=panel, series=series, x_name=xname,
                     x_value=(round(x, 4) if isinstance(x, float) else x), x_unit=xunit,
                     y_name=yname, y_value=(round(y, 4) if isinstance(y, float) else y),
                     y_unit=yunit, flag=flag, note=note, provenance="digitized"))


# ── 판독 ────────────────────────────────────────────────────────────────────
def fig3(doc):
    im = page_raster(doc, 3)                                  # 본문 p.4 (0-based 3), 1500x1426
    # (a) θ vs f_CAM @ λ=1.67 — frame (121,60,714,539)
    fa = (121, 60, 714, 539)
    bx = ticks_bottom_in(im, fa)
    if not near(bx, [150.0, 240.5, 330.5, 421.5, 512.5, 603.0, 693.5]):
        raise SystemExit(f"Fig 3a x 눈금 어긋남: {bx}")
    wt = lambda x: 60 + (x - 150.0) / 18.125                  # 60…90 wt% (7 눈금, 5 wt% 간격)
    th = lambda y: (528.0 - y) / 425.0                        # 안쪽 눈금 1.0 ↔ 103, 0.0 ↔ 528
    blue = colour(im, "blue")
    sub = im[fa[1] + 4:fa[3] - 4, fa[0] + 4:fa[2] - 4]
    fallback = [(wt(cx + fa[0] + 4), th(cy + fa[1] + 4))
                for cx, cy, a in blobs(colour(sub, "blue"), k=6, amin=12, amax=500, fill=True)]
    for w in range(60, 91):                                    # 마커는 1 wt% 간격 31 개
        x = int(round(150.0 + (w - 60) * 18.125))
        win = ndimage.binary_fill_holes(blue[fa[1] + 4:fa[3] - 4, x - 9:x + 10])
        lab, n = ndimage.label(win)
        got = None
        for i, sl in enumerate(ndimage.find_objects(lab), 1):
            h, wd = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
            if 9 <= h <= 20 and wd >= 9:
                cy, cx = ndimage.center_of_mass(lab == i)
                got = th(cy + fa[1] + 4)
        if got is None:
            near_fb = [v for u, v in fallback if abs(u - w) < 0.4]
            got = near_fb[0] if near_fb else None
        if got is None:
            put("3", "3a", "lambda=1.67 (D_CAM 5 um)", "f_CAM", float(w), "wt%", "theta_CAM", "n/a",
                "fraction", flag="not_found", note="연결선과 겹쳐 마커 분리 실패")
        else:
            put("3", "3a", "lambda=1.67 (D_CAM 5 um)", "f_CAM", float(w), "wt%", "theta_CAM", float(got),
                "fraction")
    # (b) θ vs λ @ 70 wt% — native 1500 px; frame 는 오른쪽 위
    fb = (907, 62, 1497, 540)
    bx = ticks_bottom_in(im, fb)
    if not near(bx, [916.5, 1051.5, 1185.5, 1320.5, 1455.5]):
        raise SystemExit(f"Fig 3b x 눈금 어긋남: {bx}")
    sub = im[fb[1] + 4:fb[3] - 4, fb[0] + 4:fb[2] - 4]
    # 눈금: x 0 ↔ 916.5 … 4 ↔ 1455.5 (0.5 간격 안쪽 눈금) · y 안쪽 눈금 1.0 ↔ 106.0 … 0.0 ↔ 530.5
    #   (라벨 글자 중심은 눈금보다 ≈3.5 px 위 — 눈금을 쓴다; 3a 도 같은 규약)
    lam_b = lambda x: (x - 916.5) / 134.75
    th_b = lambda y: (530.5 - y) / 424.5
    # 자주색 속빈 사각 — 범례 선 표본 평균 ≈(155,73,241)
    mk = (sub[..., 0] > 110) & (sub[..., 2] > 200) & (sub[..., 1] < 130)
    for cx, cy, a in blobs(mk, k=5, amin=10, amax=600, fill=True):
        put("3", "3b", "f_CAM=70 wt% (D_CAM 5 um)", "lambda", lam_b(cx + fb[0] + 4), "-",
            "theta_CAM", th_b(cy + fb[1] + 4), "fraction",
            note="λ 점 7개(0.33/0.42/0.625/1/1.67/3.33/4) — 본문 SE 목록은 6개(1.5–15 µm); λ=4 점은 목록 밖")
    # (d) 임계 λ vs f_CAM — 오른쪽 아래 사분면 원판 좌표
    oy, ox = int(im.shape[0] * 0.5), int(im.shape[1] * 0.6)
    sub = im[oy:, ox:]
    x2w = lambda x: 65 + (x - 20) / ((522.5 - 20) / 15)       # 65 ↔ 20 px, 80 ↔ 522.5 px
    w2x = lambda w: 20 + (w - 65) * ((522.5 - 20) / 15)
    y2l = lambda y: (599.5 - y) / ((599.5 - 63) / 8)          # 0 ↔ 599.5, 8 ↔ 63
    for name, key in (("theta=80%", "red_pure"), ("theta=90%", "orange"), ("theta=98%", "green")):
        m = colour(sub, key).copy()
        m[:300, :400] = False                                  # 범례 상자 제외
        for w in (65, 70, 72.5, 75, 76, 77, 78, 79, 79.5, 80):
            x = int(round(w2x(w)))
            ys = np.where(m[63:600, x - 1:x + 2].any(1))[0] + 63
            if len(ys):
                steep = w >= 79
                put("3", "3d", name, "f_CAM", float(w), "wt%", "lambda_min", float(y2l(np.median(ys))), "-",
                    flag=("steep" if steep else "ok"),
                    note=("수직 구간 — λ 대신 f_CAM ±0.3 wt% 로 읽을 것" if steep else ""))
            else:
                put("3", "3d", name, "f_CAM", float(w), "wt%", "lambda_min", ">8", "-", flag="off_scale",
                    note="곡선이 λ=8 (축 상한) 위로 나감")
        mm = colour(sub, key).copy()
        mm[:, :400] = False
        xs = np.where(mm[60:72, :].any(0))[0]
        if len(xs):
            put("3", "3d", name, "lambda", 8.0, "-", "f_CAM_at_axis_top", float(x2w(xs.min())), "wt%",
                note="이 f_CAM 이상에서는 해당 θ 를 λ≤8 로 못 얻는다 (그림 범위 안)")


def fig5(doc):
    im = page_raster(doc, 5)                                  # 본문 p.6, 1750x1096
    # (b) 용량 vs SE size — frame (978,68,1481,483)
    fb = (978, 68, 1481, 483)
    bx = ticks_bottom_in(im, fb)
    if not near(bx, [1073.5, 1189.5, 1304.5, 1421.5]):
        raise SystemExit(f"Fig 5b x 눈금 어긋남: {bx}")
    se = lambda x: 2 + (x - 1073.5) / 58.0
    cap = lambda y: 160 - (y - 90.5) / 2.955
    sub = im[fb[1]:fb[3], fb[0]:fb[2]]
    for cx, cy, a in blobs(colour(sub, "red"), k=7, amin=10, amax=800):
        X, Y = cx + fb[0], cy + fb[1]
        if cap(Y) < 60:
            continue                                           # 범례 마커
        put("5", "5b", "Exp (5 um NMC, 60 wt%)", "D_SE", se(X), "um", "capacity", cap(Y), "mAh/g")
    sub = im[fb[1] + 3:fb[3] - 3, fb[0] + 3:fb[2] - 3]
    for cx, cy, a in blobs(colour(sub, "dark"), k=7, amin=15, amax=600, fill=True):
        X, Y = cx + fb[0] + 3, cy + fb[1] + 3
        if cap(Y) < 60 or min(abs(se(X) - d) for d in (1.5, 3.0, 5.0, 8.0)) > 0.2:
            continue                                           # 범례 · "5 µm CAM" 라벨 상자
        put("5", "5b", "Model (5 um NMC, 60 wt%)", "D_SE", se(X), "um", "capacity", cap(Y), "mAh/g")
    for d in (1.5, 3.0):
        put("5", "5b", "Model (5 um NMC, 60 wt%)", "D_SE", d, "um", "capacity", "~155", "mAh/g",
            flag="occluded", note="실험 원 뒤에 가려짐 — 육안 ≈155 (θ≈1 × 155)")
    # (e) 용량 vs CAM size — 축: 왼쪽 축 x≈1265, y 눈금 바깥쪽
    cap_e = lambda y: 160 - (y - 623.5) / 2.9375
    cam_e = lambda x: 4 + (x - 1268) / 52.75
    x0, y0, x1, y1 = 1270, 585, 1745, 1040
    sub = im[y0:y1, x0:x1]
    # 빨강(3 µm 실험)과 주황(1.5 µm 실험)은 G 가 겹친다 → G/R 비로 가른 red_pure · orange_marker, 작은 열림(k=5)
    series = (("Exp (3 um SE)", "red_pure", False, 5), ("Exp (1.5 um SE)", "orange_marker", False, 5),
              ("Model (1.5 um SE)", "blue", True, 7), ("Model (3 um SE)", "dark", True, 7))
    for name, key, fill, k in series:
        for cx, cy, a in blobs(colour(sub, key), k=k, amin=10, amax=600, fill=fill):
            X, Y = cx + x0, cy + y0
            c = cam_e(X)
            if min(abs(c - 5), abs(c - 12)) > 0.3:
                continue                                       # 범례
            put("5", "5e", name + ", 80 wt%", "D_CAM", c, "um", "capacity", cap_e(Y), "mAh/g")
    put("5", "5e", "Model (1.5 um SE), 80 wt%", "D_CAM", 12.0, "um", "capacity", "~140", "mAh/g",
        flag="occluded", note="실험 원 뒤 — 파란 픽셀 139–140")


def fig6(doc):
    im = page_raster(doc, 6)                                  # 본문 p.7, 1500x1357
    cfg = {"6b": ((875, 60, 1496, 575), lambda y: 160 - (y - 79.5) / 3.733,
                  lambda x: 60 + (x - 934.5) / 25.5, "3 um LPS / 5 um NMC (lambda 1.67)"),
           "6d": ((876, 737, 1493, 1249), lambda y: 160 - (y - 756.5) / 3.743,
                  lambda x: 60 + (x - 934.5) / 25.35, "1.5 um LPS / 5 um NMC (lambda 3.33)")}
    for panel, (fr, cap, wt, lab) in cfg.items():
        bx = ticks_bottom_in(im, fr)
        if not near(bx, [934.5, 1061.5, 1188.5 if panel == "6d" else 1189.5], tol=2.5):
            raise SystemExit(f"Fig {panel} x 눈금 어긋남: {bx}")
        x0, y0, x1, y1 = fr
        sub = im[y0 + 3:y1 - 3, x0 + 3:x1 - 3]
        for cx, cy, a in blobs(colour(sub, "red"), k=7, amin=15, amax=800):
            w = wt(cx + x0 + 3)
            if min(abs(w - v) for v in (60, 70, 80)) > 0.5:
                continue                                       # 범례
            put("6", panel, "Exp " + lab, "f_CAM", w, "wt%", "capacity", cap(cy + y0 + 3), "mAh/g")
        for cx, cy, a in blobs(colour(sub, "dark"), k=7, amin=15, amax=600, fill=True):
            w = wt(cx + x0 + 3)
            c = cap(cy + y0 + 3)
            if min(abs(w - v) for v in (60, 70, 80)) > 0.3 or c > 156.5 or c < 45:
                continue                                       # 범례 · 라벨 상자
            put("6", panel, "Model " + lab, "f_CAM", w, "wt%", "capacity", c, "mAh/g")
    for panel, lab, pts in (("6b", "3 um LPS / 5 um NMC (lambda 1.67)", ((60, "~155"), (80, "~75"))),
                            ("6d", "1.5 um LPS / 5 um NMC (lambda 3.33)", ((60, "~155"), (70, "~155")))):
        for w, v in pts:
            put("6", panel, "Model " + lab, "f_CAM", float(w), "wt%", "capacity", v, "mAh/g",
                flag="occluded", note="실험 원과 겹침 — 육안")


def fig7(doc):
    im = page_raster(doc, 7)                                  # 본문 p.8, 1500x732
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    masks = {"Phi=0": (R > 200) & (G < 90) & (B < 90),
             "Phi=0.1": (R > 200) & (G > 100) & (G < 200) & (B < 120) & (R - B > 90),
             "Phi=0.2": (B > 150) & (B - R > 50)}
    X = lambda w: 397 + (w - 70) * 14.07                      # 격자선 60/70/80 wt% = 256.5/397/538
    V = lambda y: 80 - (y - 101) / 7.5                         # 격자선 10 vol% 간격 74.5–75 px
    for w in (50, 60, 70, 75, 80, 85, 90):
        for name, m in masks.items():
            vals = []
            for dx in (-2, 0, 2, 4, -4):
                x = int(round(X(w))) + dx
                if not 106 <= x <= 681:
                    continue
                ys = np.where(m[91:634, x])[0] + 91
                if len(ys):
                    vals.append(V(np.median(ys)))
                    break
            if vals:
                put("7", "7a", name, "f_CAM", float(w), "wt%", "CAM_loading", float(vals[0]), "vol%",
                    note="Shi 의 f_CAM 은 5 wt% CNF 포함 분모 (f = 0.95·M_CAM/(M_CAM+M_SE)); 밀도 = SI Table 1 (LPS 1.87 · NMC 4.85)")


def figS1(doc):
    # SMask 합성이 필요 → 쪽 렌더 400 dpi (래스터 자리 (94.5,72.0,517.3,276.4))
    im = page_render(doc, 4, (94.5, 72.0, 517.3, 276.4), 400)
    x0, y0, x1, y1 = 1293, 47, 2288, 845
    val = lambda y: 75 - (y - 59.5) / 15.7                    # 눈금 라벨 75 ↔ 59.5 · 35 ↔ 687.5
    sub = im[y0 + 4:y1 - 4, x0 + 4:x1 - 4]
    series = (("CAM-5/SE-1.5 (lambda 3.33)", "black"), ("CAM-5/SE-3 (lambda 1.67)", "red"),
              ("CAM-12/SE-5 (lambda 2.4)", "blue"), ("CAM-12/SE-8 (lambda 1.5)", "gray"))
    for name, key in series:
        pts = [(cx + x0 + 4, val(cy + y0 + 4)) for cx, cy, a in
               blobs(colour(sub, key), k=13, amin=60, amax=5000)]
        pts = [p for p in pts if abs(p[0] - 1803) > 15]        # 범례 마커 열 제외
        plateau = [v for x, v in pts if x >= 1580]
        for i, (x, v) in enumerate(pts):
            put("S1", "S1b", name + ", CAM:SE=80:15", "box_point_index", i + 1, "-",
                "active_ratio_theta", float(v), "%",
                note="세로축 라벨은 인쇄본 'f_CAM (%)' — 캡션상 active cathode ratio")
        if plateau:
            put("S1", "S1b", name + ", CAM:SE=80:15", "plateau(box ≥ 문턱)", "range", "-",
                "active_ratio_theta", f"{min(plateau):.1f}–{max(plateau):.1f}", "%", flag="summary")


def figS2(doc):
    im = page_raster(doc, 5)                                  # SI p.6, 860x747 RGB
    x0, y0, x1, y1 = 175, 37, 838, 609
    bx = ticks_bottom_in(im, (x0, y0, x1, y1))
    if not near(bx, [188.5, 318.5, 448.5, 577.5, 707.0, 836.5]):
        raise SystemExit(f"Fig S2 x 눈금 어긋남: {bx}")
    lam = lambda x: (x - 188.5) / 162.0
    th = lambda y: 1.0 - (y - 99.5) / 617.5
    sub = im[y0 + 3:y1 - 3, x0 + 3:x1 - 3]
    for name, key in (("5 um CAM", "blue"), ("12 um CAM", "orange_marker")):
        for cx, cy, a in blobs(colour(sub, key), k=5, amin=10, amax=800):
            L = lam(cx + x0 + 3)
            if abs(L - 2.07) < 0.1:
                continue                                       # 범례
            put("S2", "S2", name + ", f_CAM=60 wt%", "lambda", L, "-", "theta_CAM", th(cy + y0 + 3), "fraction")
    put("S2", "S2", "5 um CAM, f_CAM=60 wt%", "lambda", 3.333, "-", "theta_CAM", "~1.00", "fraction",
        flag="occluded", note="12 µm 삼각 뒤 — 육안 1.00")


def checks():
    """판독값 ↔ 원문 stated 값 대조 (검증 전용 행)."""
    def get(panel, series_sub, xv, tol):
        for r in ROWS:
            if r["panel"] == panel and series_sub in r["series"] and isinstance(r["x_value"], float) \
                    and abs(r["x_value"] - xv) <= tol and isinstance(r["y_value"], float):
                return r["y_value"]
        return None
    pairs = [
        ("3d", "theta=98%", 75.0, 0.01, 2.1, "본문 p.5 'λmin = 2.1' (75 wt%, 98 %)"),
        ("3a", "lambda=1.67", 80.0, 0.3, 0.52, "본문 p.5 Fig 4b θ=52 % (80 wt%, λ 1.67) — 다른 시뮬 세트"),
        ("5b", "Exp", 8.0, 0.2, 75.0, "본문 p.5 '≈75 mAh/g' (8 µm LPS)"),
        ("5b", "Exp", 5.0, 0.2, 125.0, "본문 p.5 '≈125 mAh/g' (5 µm LPS)"),
    ]
    for panel, s, xv, tol, want, why in pairs:
        got = get(panel, s, xv, tol)
        ROWS.append(dict(figure="check", panel=panel, series=s, x_name="x", x_value=xv, x_unit="",
                         y_name="digitized_vs_stated", y_value=(f"{got:.3g} vs {want}" if got is not None else "n/a"),
                         y_unit="", flag="check", note=why, provenance="check"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--main", required=True, help="본문 PDF (Wiley 9 pp)")
    ap.add_argument("--si", required=True, help="SI PDF (aenm201902881-sup-0001-suppmat.pdf)")
    ap.add_argument("--csv", default=str(ROOT / "litdb" / "figures" / SLUG / "digitized.csv"))
    a = ap.parse_args()
    dm, ds = fitz.open(a.main), fitz.open(a.si)
    if dm.page_count != 9 or ds.page_count != 8:
        raise SystemExit(f"쪽수가 다르다 (본문 {dm.page_count}/9 · SI {ds.page_count}/8) — 다른 판본?")
    fig3(dm); fig5(dm); fig6(dm); fig7(dm); figS1(ds); figS2(ds); checks()
    cols = ["figure", "panel", "series", "x_name", "x_value", "x_unit", "y_name", "y_value", "y_unit",
            "flag", "note", "provenance"]
    with open(a.csv, "w", newline="", encoding="utf-8") as f:
        f.write("# Shi et al. Adv. Energy Mater. 2020, 10, 1902881 (DOI 10.1002/aenm.201902881) — main + SI figure "
                "readout. ALL y_value = DIGITIZED (not stated) except rows flagged 'check' (digitized vs stated). "
                "tools/litdb/shi2019_fig_digitize.py\n")
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in ROWS:
            w.writerow(r)
    print(f"{len(ROWS)} 행 → {a.csv}")
    for r in ROWS:
        if r["flag"] == "check":
            print(f"  check {r['panel']:3s} {r['series']:14s} {r['y_value']:>14s}  {r['note']}")


if __name__ == "__main__":
    sys.exit(main())
