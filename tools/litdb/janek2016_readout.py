#!/usr/bin/env python3
"""janek2016_readout.py — Janek & Zeier 2016 *Nat. Energy* 1, 16141 (Comment) `Fig. 1` 의 **벡터 경로 판독** + 본문 · 캡션 산수 검산.

digest: litdb/papers/janek2016_solid_future_battery_development.md
출력:   litdb/figures/janek2016_solid_future_battery_development/digitized.csv

무엇을 읽나 (전부 PDF 안의 벡터 좌표 — 픽셀 판독이 아니다)
  Fig. 1a  18650 셀 에너지 밀도: 파란 채움 사각 (w_vol · 2 개) · 빨간 채움 원 (w_grav · 2 개) · 실선 / 점선 곡선 4 개의 꼭짓점 ·
           'Physicochemical limit' 띠 (그라데이션 래스터 이미지 — bbox 만) → 연도 · Wh l⁻¹ · Wh kg⁻¹
  Fig. 1b  Arrhenius 선 10 개 — 색 + 점선 여부로 가르고, **라벨 글자색**과 **라벨–선 거리** 로 짝을 검사한다
           (LLZO 와 EC:DEC:LiPF6 는 같은 초록이라 점선 여부로만 갈린다) · 상온 회색 띠 →
           끝점 (1000/T · log σ · K) · 회색 띠 · 298.15 K · 353.15 K 에서의 log σ (선 안에서만 보간 · 외삽 안 함) ·
           x 로 고르게 다시 뽑은 점의 최소제곱 Ea (σ 형식 · log σ vs 1000/T) + 직선에서 벗어난 최대 폭 (휘어짐) ·
           본문 'higher than typical liquid electrolytes' 대조 — 같은 그림 안 LGPS · Li7P3S11 − EC:DEC · EC:PC (둘 다 그려진 온도만) ·
           LGPS 선 ↔ kamaya2011 digest 의 벡터 판독 CSV (Kamaya `Fig. 3` LGPS 꼭짓점 · 같은 1000/T 에서 차)
  본문 · 캡션 산수 (PDF 와 무관한 상수 계산): 3.5 Ah × 3.65 V → Wh · 48 g 로 Wh kg⁻¹ · 18650 원기둥 부피로 Wh l⁻¹ ·
           Li 금속 이론 용량 · Li 20 µm / 1 µm 의 면적 용량 · 4.2 → 5 V 전압만의 증가율 · US$100 kWh⁻¹ ↔ US$30 kg⁻¹ 가 깔고 있는 Wh kg⁻¹

축 보정은 눈금선 좌표에 대한 **최소제곱 1 차식**이고, 눈금 개수가 값 개수와 다르거나 잔차가 문턱을 넘으면 멈춘다.
`Fig. 1b` 는 위쪽 K 축 눈금을 아래 1000/T 축으로 되돌려 **같은 자리인지** 따로 검사한다.

⛔ 이 도구가 못 하는 것
  · `Fig. 2` · `Fig. 3` 은 모식도 (작은 래스터 타일 수백 장) 라 읽지 않는다 — 읽을 값이 없다 (`Fig. 2` 의 +70 % 등은 글자다).
  · 'Physicochemical limit' 띠는 그라데이션이라 **한계가 어디서 시작하는지** 그림에 정의가 없다 — 이미지 bbox 만 낸다.
  · `Fig. 1b` 의 선은 원 논문 (refs 5 · 22–29) 의 측정점이 아니라 **이 Comment 가 다시 그린 선**이다 — 원전 값이 아니다.
    선의 끝점 · 휘어짐은 다시 그린 사람의 선택이다 (예: LGPS 선은 Kamaya 2011 측정 범위보다 짧다 — digest §5).
  · y 눈금 간격이 고르지 않다 (20.6–21.2 pt · 손으로 그린 축) — 보정 잔차를 기록하고 판독 불확도를 ±0.03 dex 로 본다.
  · 선이 베지어 ('c') 로 그려져 있으면 읽지 않고 멈춘다 (이 그림은 전부 직선 조각이다).
  · 판독값은 **그림이 그린 값**이다 — digest 에서는 `figure-read ≈` 로만 쓴다.
  · 산수의 18 mm × 65 mm 원기둥 · Li 밀도 0.534 g cm⁻³ · M(Li) 6.941 g mol⁻¹ · F 는 **우리 가정 · 상수**다 — 논문 값이 아니다.

usage
  python3 tools/litdb/janek2016_readout.py --pdf "litdb/inbox/128._A_solid_future_for_battery_development.pdf"
  python3 tools/litdb/janek2016_readout.py --selftest     # 합성 PDF 로 양성 + 음성 경로
"""
import argparse
import copy
import csv
import math
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "janek2016_solid_future_battery_development"
OUT_CSV = ROOT / "litdb" / "figures" / SLUG / "digitized.csv"
DEFAULT_PDF = ROOT / "litdb" / "inbox" / "128._A_solid_future_for_battery_development.pdf"

KB_EV = 8.617333262e-5        # eV/K
LN10 = math.log(10.0)
F_C = 96485.33212             # C/mol
M_LI = 6.941                  # g/mol   (우리 상수)
RHO_LI = 0.534                # g/cm³  (우리 상수)

BLACK = (0.14, 0.12, 0.13)
BLUE = (0.24, 0.37, 0.67)
RED = (0.71, 0.07, 0.26)
GREY = (0.29, 0.30, 0.31)
GREEN = (0.07, 0.53, 0.26)

# 페이지 번호는 0 부터 · 사각형은 pt (PDF 좌표, y 아래로 증가)
CFG = {
    "fig1a": {
        "page": 1, "clip": (40, 90, 300, 262),
        "xticks": {"rgb": BLACK, "band": (234.8, 235.2), "min_len": 2.0, "vals": [1990, 1995, 2000, 2005, 2010, 2015], "tol": 0.15},
        "yL": {"rgb": BLUE, "band": (85.1, 85.5), "vals": [1000, 800, 600, 400, 200, 0], "tol": 5.0},     # 왼쪽 눈금 x0 ≈ 85.3
        "yR": {"rgb": RED, "band": (270.7, 271.1), "vals": [500, 400, 300, 200, 100, 0], "tol": 2.5},      # 오른쪽 눈금 x0 ≈ 270.9
        "squares": {"rgb": BLUE, "n": 2},
        "circles": {"rgb": RED, "n": 2},
        "curves": {"w_vol_solid": (BLUE, False), "w_vol_dashed": (BLUE, True),
                   "w_grav_solid": (RED, False), "w_grav_dashed": (RED, True)},
        "bar_min_w": 50.0,
    },
    "fig1b": {
        "page": 1, "clip": (340, 90, 560, 262),
        "xticks": {"rgb": BLACK, "band": (235.5, 235.9), "min_len": 2.0, "vals": [2, 3, 4, 5], "tol": 0.01},   # 아래 큰 눈금 y0 ≈ 235.7
        "top": {"rgb": BLACK, "band": (95.0, 95.4), "min_len": 1.2, "K": [600, 500, 400, 300, 200], "tol": 0.02},  # 위 K 눈금 y0 ≈ 95.2
        "yticks": {"rgb": BLACK, "band": (360.8, 361.2), "vals": [-1, -2, -3, -4, -5, -6], "tol": 0.05},       # 왼쪽 눈금 x0 ≈ 361.0
        "rt_bar": {"rgb": GREY, "min_h": 100.0},
        "min_len": 20.0,
        # 이름 · 참고문헌 번호 · 선 색 · 점선 · 라벨 글자 (공백 지운 줄 텍스트의 앞부분)
        "series": [
            ("Li10GeP2S12", 5, (0.15, 0.20, 0.44), True, "Li10GeP2S12"),
            ("P(EO)12-LiTFSI", 22, (0.14, 0.19, 0.41), False, "P(EO)12-"),
            ("Li3.25Ge0.25P0.75S4", 23, (0.96, 0.51, 0.17), True, "Li3.25Ge0.25P0.75S4"),
            ("Li7P3S11 glass ceramic", 24, (0.60, 0.17, 0.32), True, "Li7P3S11"),
            ("EC:DEC:LiPF6", 25, GREEN, False, "EC:DEC:LiPF6"),
            ("EC:PC:LiPF6", 25, (0.25, 0.32, 0.64), False, "EC:PC:LiPF6"),
            ("LiPON", 26, (0.48, 0.07, 0.08), True, "LiPON"),
            ("Li3.5Zn0.25GeO4", 27, BLACK, True, "Li3.5Zn0.25GeO4"),
            ("Li7La3Zr2O12", 28, GREEN, True, "Li7La3Zr2O12"),
            ("Li1.5Al0.5Ge1.5(PO4)3", 29, (0.46, 0.49, 0.19), True, "Li1.5Al0.5Ge1.5(PO4)3"),
        ],
        # 본문 주장 대조용 온도 (K): 80 °C (고분자 EV 운전 · 본문) · 25 °C · 액체 선이 시작하는 297 K 바로 아래 · 0 · −20 · −33 °C
        "extra_T": [353.15, 298.15, 297.0, 273.15, 253.15, 240.0],
    },
}


class ReadoutError(RuntimeError):
    pass


def _fitz():
    try:
        import pymupdf as fz
    except ImportError:  # 옛 판
        import fitz as fz
    return fz


def _close(c, ref, tol=0.02):
    return c is not None and len(c) == 3 and all(abs(a - b) <= tol for a, b in zip(c, ref))


def _dashed(d):
    """'[ 2 2 ] 0' → True · '[] 0' → False · 채움 경로 (None) → False."""
    ds = d.get("dashes")
    if not ds:
        return False
    inner = ds[ds.find("[") + 1:ds.find("]")] if "[" in ds and "]" in ds else ""
    return inner.strip() != ""


def _overlap(r, clip):
    """폭 0 인 선분 (세로 눈금) 은 Rect.intersects 가 False 를 준다 — 좌표로 직접 본다."""
    return not (r.x1 < clip[0] or r.x0 > clip[2] or r.y1 < clip[1] or r.y0 > clip[3])


def drawings_in(page, clip):
    return [d for d in page.get_drawings() if _overlap(d["rect"], clip)]


def ticks(draws, rgb, band, axis, min_len=1.0, max_len=6.0, thin=0.6):
    """색이 맞는 짧은 축정렬 선분 = 눈금. axis='y' → x0 가 band 안 → y 위치들 · axis='x' → y0 가 band 안 → x 위치들."""
    out = []
    for d in draws:
        if not _close(d.get("color"), rgb) or d.get("fill") is not None:
            continue
        r = d["rect"]
        w, h = r.width, r.height
        if axis == "y" and h <= thin and min_len <= w <= max_len and band[0] <= r.x0 <= band[1]:
            out.append((r.y0 + r.y1) / 2.0)
        elif axis == "x" and w <= thin and min_len <= h <= max_len and band[0] <= r.y0 <= band[1]:
            out.append((r.x0 + r.x1) / 2.0)
    out.sort()
    ded = []
    for v in out:
        if not ded or abs(v - ded[-1]) > 0.05:
            ded.append(v)
    return ded


def fit_linear(pix, vals, tol, name):
    """최소제곱 val = m·pix + b. 개수가 다르거나 잔차 최대가 tol (값 단위) 을 넘으면 멈춘다."""
    if len(pix) != len(vals) or len(pix) < 3:
        raise ReadoutError(f"{name}: 눈금 {len(pix)} 개 ↔ 값 {len(vals)} 개 (3 개 이상 · 같은 수여야 한다)")
    n = len(pix)
    mx, my = sum(pix) / n, sum(vals) / n
    sxx = sum((x - mx) ** 2 for x in pix)
    if sxx == 0:
        raise ReadoutError(f"{name}: 눈금이 한 점에 모였다")
    m = sum((x - mx) * (y - my) for x, y in zip(pix, vals)) / sxx
    b = my - m * mx
    res = max(abs(m * x + b - y) for x, y in zip(pix, vals))
    if res > tol:
        raise ReadoutError(f"{name}: 축 보정 잔차 {res:.4g} > {tol} — 눈금 분류가 틀렸거나 축이 선형이 아니다")
    return m, b, res


def calib(tick_pix, vals, tol, name):
    """눈금 좌표는 오름차순 · 값은 CFG 순서 그대로 (y 축은 위 → 아래 = 큰 값 → 작은 값)."""
    return fit_linear(sorted(tick_pix), vals, tol, name)


def polyline(d, name):
    """선분 ('l') 만으로 된 경로 → 꼭짓점 목록. 베지어가 있으면 멈춘다 · 끊긴 곳은 그대로 이어 붙이고 수를 센다."""
    pts, breaks = [], 0
    for it in d["items"]:
        if it[0] != "l":
            raise ReadoutError(f"{name}: '{it[0]}' 항목 — 직선 조각만 읽는다")
        p, q = it[1], it[2]
        if not pts:
            pts.append((p.x, p.y))
        elif math.hypot(p.x - pts[-1][0], p.y - pts[-1][1]) > 0.05:
            breaks += 1
            pts.append((p.x, p.y))
        pts.append((q.x, q.y))
    return pts, breaks


def _dist_seg(p, a, b):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))


def dist_poly(p, pts):
    if len(pts) == 1:
        return math.hypot(p[0] - pts[0][0], p[1] - pts[0][1])
    return min(_dist_seg(p, pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def interp(pts_xy, x):
    """(x, y) 꺾은선에서 x 의 y. 선의 x 범위 밖이면 None (외삽 안 함) — 0.0 은 유효한 값이다."""
    for (x0, y0), (x1, y1) in zip(pts_xy, pts_xy[1:]):
        lo, hi = min(x0, x1), max(x0, x1)
        if lo <= x <= hi:
            if x1 == x0:
                return 0.5 * (y0 + y1)
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None


def lin_fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    m = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    b = my - m * mx
    dev = max(abs(m * x + b - y) for x, y in zip(xs, ys))
    return m, b, dev


def ea_from_slope(m_per_1000K):
    """log10 σ vs 1000/T 의 기울기 → Ea (eV) · σ 형식 (σT 아님)."""
    return -m_per_1000K * LN10 * KB_EV * 1000.0


def text_lines(page, clip):
    """줄 단위 (span 이어 붙이고 공백 제거) 텍스트 · 줄 bbox · 첫 span 색."""
    fz = _fitz()
    out = []
    for b in page.get_text("dict", clip=fz.Rect(clip))["blocks"]:
        for ln in b.get("lines", []):
            sp = ln["spans"]
            if not sp:
                continue
            txt = "".join(s["text"] for s in sp).replace(" ", "")
            c = sp[0]["color"]
            rgb = (((c >> 16) & 255) / 255.0, ((c >> 8) & 255) / 255.0, (c & 255) / 255.0)
            x0, y0, x1, y1 = ln["bbox"]
            out.append({"text": txt, "rgb": rgb, "c": ((x0 + x1) / 2.0, (y0 + y1) / 2.0)})
    return out


def read_fig1a(page, cfg):
    dr = drawings_in(page, cfg["clip"])
    xt = cfg["xticks"]
    mx_, bx_, rx = calib(ticks(dr, xt["rgb"], xt["band"], "x", xt["min_len"]), xt["vals"], xt["tol"], "Fig.1a 연도 축")
    yl, yr = cfg["yL"], cfg["yR"]
    mL, bL, rL = calib(ticks(dr, yl["rgb"], yl["band"], "y"), yl["vals"], yl["tol"], "Fig.1a w_vol 축")
    mR, bR, rR = calib(ticks(dr, yr["rgb"], yr["band"], "y"), yr["vals"], yr["tol"], "Fig.1a w_grav 축")
    year = lambda x: mx_ * x + bx_
    wv = lambda y: mL * y + bL
    wg = lambda y: mR * y + bR

    def centers(pred):
        out = []
        for d in dr:
            r = d["rect"]
            if r.width <= 8 and r.height <= 8 and pred(d):
                c = ((r.x0 + r.x1) / 2.0, (r.y0 + r.y1) / 2.0)
                if not any(math.hypot(c[0] - o[0], c[1] - o[1]) < 0.5 for o in out):
                    out.append(c)
        return sorted(out)

    sq = centers(lambda d: _close(d.get("fill"), cfg["squares"]["rgb"]) and [it[0] for it in d["items"]] == ["re"])
    ci = centers(lambda d: _close(d.get("fill"), cfg["circles"]["rgb"]) and [it[0] for it in d["items"]] == ["c"] * 4)
    if len(sq) != cfg["squares"]["n"] or len(ci) != cfg["circles"]["n"]:
        raise ReadoutError(f"Fig.1a 표지: 사각 {len(sq)} · 원 {len(ci)} — 기대 {cfg['squares']['n']} · {cfg['circles']['n']}")
    curves = {}
    for name, (rgb, dashed) in cfg["curves"].items():
        cand = [d for d in dr if d.get("fill") is None and _close(d.get("color"), rgb) and _dashed(d) == dashed
                and len(d["items"]) >= 2 and d["rect"].width > 20]      # 범례 선 (1 조각 · 14.7 pt) 은 빠진다
        if len(cand) != 1:
            raise ReadoutError(f"Fig.1a 곡선 {name}: 후보 {len(cand)} 개 (1 개여야 한다)")
        pts, brk = polyline(cand[0], name)
        f = wv if name.startswith("w_vol") else wg
        curves[name] = {"pts": [(year(x), f(y)) for x, y in pts], "breaks": brk}
    bars = [i for i in page.get_image_info() if _overlap(_fitz().Rect(i["bbox"]), cfg["clip"])
            and (i["bbox"][2] - i["bbox"][0]) >= cfg["bar_min_w"]]
    if len(bars) != 1:
        raise ReadoutError(f"Fig.1a 'Physicochemical limit' 띠 이미지 {len(bars)} 개 (1 개여야 한다)")
    bb = bars[0]["bbox"]
    return {
        "calib_res": {"year": rx, "w_vol": rL, "w_grav": rR},
        "squares": [(year(x), wv(y)) for x, y in sq],
        "circles": [(year(x), wg(y)) for x, y in ci],
        "curves": curves,
        "bar": {"year0": year(bb[0]), "year1": year(bb[2]), "w_vol_top": wv(bb[1]), "w_vol_bottom": wv(bb[3])},
    }


def read_fig1b(page, cfg):
    dr = drawings_in(page, cfg["clip"])
    xt, yt, tp = cfg["xticks"], cfg["yticks"], cfg["top"]
    mX, bX, rX = calib(ticks(dr, xt["rgb"], xt["band"], "x", xt["min_len"]), xt["vals"], xt["tol"], "Fig.1b 1000/T 축")
    mY, bY, rY = calib(ticks(dr, yt["rgb"], yt["band"], "y"), yt["vals"], yt["tol"], "Fig.1b log σ 축")
    inv = lambda x: mX * x + bX
    lg = lambda y: mY * y + bY
    top = sorted(ticks(dr, tp["rgb"], tp["band"], "x", tp["min_len"]))
    if len(top) != len(tp["K"]):
        raise ReadoutError(f"Fig.1b 위 K 축: 눈금 {len(top)} 개 ↔ 값 {len(tp['K'])} 개")
    top_dev = max(abs(inv(x) - 1000.0 / K) for x, K in zip(top, tp["K"]))
    if top_dev > tp["tol"]:
        raise ReadoutError(f"Fig.1b 위 K 축이 아래 1000/T 축과 {top_dev:.3f} 어긋난다 (> {tp['tol']})")
    bars = [d for d in dr if _close(d.get("fill"), cfg["rt_bar"]["rgb"]) and d["rect"].height >= cfg["rt_bar"]["min_h"]]
    if len(bars) != 1:
        raise ReadoutError(f"Fig.1b 상온 회색 띠 {len(bars)} 개 (1 개여야 한다)")
    rt_x = inv((bars[0]["rect"].x0 + bars[0]["rect"].x1) / 2.0)
    lines = text_lines(page, cfg["clip"])
    strokes = [d for d in dr if d.get("fill") is None and d["rect"].width + d["rect"].height > cfg["min_len"]
               and d.get("width") and d["width"] >= 0.4]
    out = {}
    for name, ref, rgb, dashed, label in cfg["series"]:
        cand = [d for d in strokes if _close(d.get("color"), rgb) and _dashed(d) == dashed]
        if len(cand) != 1:
            raise ReadoutError(f"Fig.1b {name}: 선 후보 {len(cand)} 개 (색 · 점선 조건으로 1 개여야 한다)")
        pts, brk = polyline(cand[0], name)
        lab = [ln for ln in lines if ln["text"].startswith(label)]
        if len(lab) != 1:
            raise ReadoutError(f"Fig.1b {name}: 라벨 '{label}' {len(lab)} 줄")
        if not _close(lab[0]["rgb"], rgb, tol=0.03):
            raise ReadoutError(f"Fig.1b {name}: 라벨 글자색 {tuple(round(v, 2) for v in lab[0]['rgb'])} ≠ 선 색 {rgb}")
        same = [d for d in strokes if _close(d.get("color"), rgb)]
        if len(same) > 1:     # 같은 색 선이 둘 이상 — 라벨이 자기 선에 제일 가까워야 한다
            dd = sorted((dist_poly(lab[0]["c"], polyline(d, name)[0]), id(d) == id(cand[0])) for d in same)
            if not dd[0][1]:
                raise ReadoutError(f"Fig.1b {name}: 라벨이 같은 색의 다른 선에 더 가깝다 (짝이 뒤바뀐다)")
        xy = [(inv(x), lg(y)) for x, y in pts]
        xy_sorted = sorted(xy)
        xs = [p[0] for p in xy_sorted]
        n_s = 60
        grid = [xs[0] + (xs[-1] - xs[0]) * k / (n_s - 1) for k in range(n_s)]
        gy = [interp(xy_sorted, g) for g in grid]
        m, b, dev = lin_fit(grid, gy)
        lo, hi = xy_sorted[0], xy_sorted[-1]
        extra = {T: interp(xy_sorted, 1000.0 / T) for T in cfg["extra_T"]}
        out[name] = {
            "ref": ref, "n_vertices": len(pts), "breaks": brk,
            "x_lo": lo[0], "y_at_x_lo": lo[1], "x_hi": hi[0], "y_at_x_hi": hi[1],
            "T_hi_K": 1000.0 / lo[0], "T_lo_K": 1000.0 / hi[0],
            "rt": interp(xy_sorted, rt_x), "extra": extra,
            "slope": m, "Ea_eV": ea_from_slope(m), "max_dev_dex": dev,
            "xy": xy_sorted,
        }
    return {"calib_res": {"inv_T": rX, "log_sigma": rY, "top_vs_bottom": top_dev},
            "rt_x": rt_x, "rt_K": 1000.0 / rt_x, "series": out}


def text_checks():
    """본문 · 캡션의 수를 상수로 되짚는다 (PDF 와 무관) — (항목, 값, 단위, 메모)."""
    wh = 3.5 * 3.65
    vol_18650 = math.pi * 0.9 ** 2 * 6.5           # cm³ · 18 mm × 65 mm 원기둥 (우리 가정)
    cap_li = F_C / (3.6 * M_LI)                     # mAh/g
    li20 = 20e-4 * RHO_LI * cap_li                  # mAh/cm²
    li1 = 1e-4 * RHO_LI * cap_li
    return [
        ("cell_energy_Wh", wh, "Wh", "3.5 Ah × 3.65 V (caption)"),
        ("w_grav_from_48g", wh / 0.048, "Wh kg-1", "caption mass 48 g · text says 260 · caption says 270"),
        ("vol_18650_cylinder", vol_18650, "cm3", "우리 가정 18 mm × 65 mm · caption 'approximately 16 cm3'"),
        ("w_vol_from_cylinder", wh / (vol_18650 / 1000.0), "Wh l-1", "text · caption 770"),
        ("w_vol_from_16cm3", wh / 0.016, "Wh l-1", "caption '16 cm3' taken literally"),
        ("Li_theoretical_capacity", cap_li, "mAh g-1", "F/(3.6·M_Li) · caption says '3,700 mA g-1' as 'energy density'"),
        ("Li_20um_areal_capacity", li20, "mAh cm-2", "text 20 µm Li · ρ 0.534 (우리 상수)"),
        ("Li_1um_areal_capacity", li1, "mAh cm-2", "text thin-film ~1 µm Li cycled"),
        ("voltage_only_gain_4p2_to_5V", (5.0 / 4.2 - 1.0) * 100.0, "%", "text '>20% … depending on additional cathode capacity'"),
        ("Wh_per_kg_implied_by_cost", 30.0 / 100.0 * 1000.0, "Wh kg-1", "US$30 kg-1 ÷ US$100 kWh-1 (text)"),
    ]


def _fmt(v):
    """CSV 값 칸 — 없는 값만 '—' 다. 0.0 은 값이다 (`v or …` 로 쓰면 0 이 '—' 로 둔갑한다)."""
    return "—" if v is None else f"{v:.6g}"


def run(pdf, out_csv, kamaya_csv=None):
    kamaya_csv = KAMAYA_CSV if kamaya_csv is None else kamaya_csv
    fz = _fitz()
    doc = fz.open(str(pdf))
    pg = doc[CFG["fig1a"]["page"]]
    a = read_fig1a(pg, CFG["fig1a"])
    b = read_fig1b(doc[CFG["fig1b"]["page"]], CFG["fig1b"])
    rows = []

    def put(fig, series, q, v, unit, note=""):
        rows.append({"figure": fig, "series": series, "quantity": q,
                     "value": _fmt(v), "unit": unit, "note": note})

    for k, v in a["calib_res"].items():
        put("Fig. 1a", "axis", f"calib_max_residual_{k}", v, {"year": "yr", "w_vol": "Wh l-1", "w_grav": "Wh kg-1"}[k])
    for (yr, v) in a["squares"]:
        put("Fig. 1a", "w_vol marker (filled square)", f"value@{yr:.2f}", v, "Wh l-1", "solid symbol (cell producers)")
    for (yr, v) in a["circles"]:
        put("Fig. 1a", "w_grav marker (filled circle)", f"value@{yr:.2f}", v, "Wh kg-1", "solid symbol (cell producers)")
    for name, c in a["curves"].items():
        p0, p1 = c["pts"][0], c["pts"][-1]
        unit = "Wh l-1" if name.startswith("w_vol") else "Wh kg-1"
        put("Fig. 1a", name, f"start@{p0[0]:.2f}", p0[1], unit, f"vertices {len(c['pts'])} · breaks {c['breaks']}")
        put("Fig. 1a", name, f"end@{p1[0]:.2f}", p1[1], unit)
    sq = sorted(a["squares"])
    ci = sorted(a["circles"])
    v0 = a["curves"]["w_vol_solid"]["pts"][0][1]
    g0 = a["curves"]["w_grav_solid"]["pts"][0][1]
    put("Fig. 1a", "derived", "ratio_w_vol_2016_over_1991", sq[-1][1] / v0, "-", "caption 'almost a factor of four'")
    put("Fig. 1a", "derived", "ratio_w_grav_2016_over_1991", ci[-1][1] / g0, "-", "caption 'almost a factor of four'")
    for (ys, vs), (yc, vc) in zip(sq, ci):
        put("Fig. 1a", "derived", f"implied_density@{ys:.0f}", vs / vc, "g cm-3", "w_vol / w_grav = cell mass / cell volume")
        put("Fig. 1a", "derived", f"implied_volume_for_48g@{ys:.0f}", 48.0 / (vs / vc), "cm3", "48 g ÷ implied density")
    bar = a["bar"]
    put("Fig. 1a", "Physicochemical limit bar", "year_range", None, "yr", f"{bar['year0']:.2f}–{bar['year1']:.2f}")
    put("Fig. 1a", "Physicochemical limit bar", "w_vol_bottom_edge", bar["w_vol_bottom"], "Wh l-1", "gradient image bbox (no defined limit line)")
    put("Fig. 1a", "Physicochemical limit bar", "w_vol_top_edge", bar["w_vol_top"], "Wh l-1", "gradient image bbox")
    put("Fig. 1a", "derived", "gap_2016_to_bar_bottom", bar["w_vol_bottom"] - sq[-1][1], "Wh l-1")

    for k, v in b["calib_res"].items():
        put("Fig. 1b", "axis", f"calib_max_residual_{k}", v, {"inv_T": "1000/T", "log_sigma": "dex", "top_vs_bottom": "1000/T"}[k])
    put("Fig. 1b", "room-temperature grey bar", "center_1000_over_T", b["rt_x"], "1000 K-1", f"= {b['rt_K']:.1f} K")
    for name, s in b["series"].items():
        note = f"ref {s['ref']} · vertices {s['n_vertices']} · breaks {s['breaks']}"
        put("Fig. 1b", name, "x_hot_end", s["x_lo"], "1000 K-1", f"T {s['T_hi_K']:.1f} K · {note}")
        put("Fig. 1b", name, "logsigma_hot_end", s["y_at_x_lo"], "log S cm-1")
        put("Fig. 1b", name, "x_cold_end", s["x_hi"], "1000 K-1", f"T {s['T_lo_K']:.1f} K")
        put("Fig. 1b", name, "logsigma_cold_end", s["y_at_x_hi"], "log S cm-1")
        miss = "line not drawn there (no extrapolation)"
        put("Fig. 1b", name, "logsigma_at_grey_bar", s["rt"], "log S cm-1", miss if s["rt"] is None else "")
        put("Fig. 1b", name, "sigma_at_grey_bar", None if s["rt"] is None else 10 ** s["rt"] * 1e3, "mS cm-1")
        for T, v in s["extra"].items():
            put("Fig. 1b", name, f"logsigma_at_{T:.2f}K", v, "log S cm-1", miss if v is None else "")
        put("Fig. 1b", name, "Ea_lsq_sigma_form", s["Ea_eV"], "eV", f"slope {s['slope']:.4f} dex per 1000/T · σ form (not σT)")
        put("Fig. 1b", name, "max_dev_from_line", s["max_dev_dex"], "dex", "curvature of the drawn line")
    # 본문 'higher than typical liquid electrolytes' 대조 — 같은 그림 안에서 고체 − 액체 (dex) · 둘 다 그려진 온도만
    ser = b["series"]
    for sol in ("Li10GeP2S12", "Li7P3S11 glass ceramic"):
        for liq in ("EC:DEC:LiPF6", "EC:PC:LiPF6"):
            for T in PAIR_T:
                va, vb = interp(ser[sol]["xy"], 1000.0 / T), interp(ser[liq]["xy"], 1000.0 / T)
                d = None if (va is None or vb is None) else va - vb
                put("Fig. 1b", f"{sol} minus {liq}", f"delta_logsigma_at_{T:.2f}K", d, "dex",
                    "one of the two lines not drawn at this T" if d is None else "positive = solid above liquid")
    xk = kamaya_crosscheck(ser["Li10GeP2S12"]["xy"], kamaya_csv)
    if xk is None:
        put("Fig. 1b", "Li10GeP2S12 vs kamaya2011", "crosscheck", None, "dex", f"kamaya2011 digitized.csv not found: {kamaya_csv}")
    for x, yk, yc in xk or []:
        put("Fig. 1b", "Li10GeP2S12 vs kamaya2011", f"delta_at_{1000.0 / x:.1f}K", None if yc is None else yc - yk, "dex",
            f"Kamaya Fig.3 LGPS vertex {yk:.3f} · this Comment line {'—' if yc is None else f'{yc:.3f}'} · + = Comment above")
    for q, v, unit, note in text_checks():
        put("text/caption", "arithmetic", q, v, unit, note)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        fh.write("# Janek & Zeier 2016 Nat. Energy 1 16141 (Comment) - vector-path readout of Fig. 1. FIGURE VALUES ARE DIGITIZED "
                 "(not printed); 'derived' and 'arithmetic' rows are OUR ARITHMETIC. tools/litdb/janek2016_readout.py\n")
        w = csv.DictWriter(fh, fieldnames=["figure", "series", "quantity", "value", "unit", "note"])
        w.writeheader()
        w.writerows(rows)
    return a, b, rows


PAIR_T = (297.0, 290.0, 280.0, 273.15, 263.15, 253.15, 243.15, 236.5)
KAMAYA_CSV = ROOT / "litdb" / "figures" / "kamaya2011_lgps_lithium_superionic_conductor" / "digitized.csv"


def kamaya_crosscheck(lgps_xy, path):
    """kamaya2011 digest 의 벡터 판독 CSV ('fig3,lgps polyline vertex') 와 같은 1000/T 에서 이 Comment 의 LGPS 선을 대조.
    파일이 없으면 None (sparse checkout 등) — 대조를 건너뛰었다는 행을 남긴다 (조용히 빼지 않는다)."""
    p = Path(path)
    if not p.exists():
        return None
    out = []
    with open(p, encoding="utf-8") as fh:
        for r in csv.reader(fh):
            if len(r) >= 5 and r[0] == "fig3" and r[1] == "lgps polyline vertex":
                x, yk = float(r[2]), float(r[4])
                out.append((x, yk, interp(lgps_xy, x)))
    if not out:
        raise ReadoutError(f"{p}: 'fig3,lgps polyline vertex' 행이 없다 — kamaya2011 CSV 형식이 바뀌었나")
    return sorted(out)


def _summary(a, b):
    print("== Fig. 1a (벡터)")
    print("   보정 잔차:", {k: round(v, 4) for k, v in a["calib_res"].items()})
    for yr, v in sorted(a["squares"]):
        print(f"   w_vol 사각  {yr:8.2f}  {v:7.1f} Wh/l")
    for yr, v in sorted(a["circles"]):
        print(f"   w_grav 원   {yr:8.2f}  {v:7.1f} Wh/kg")
    for name, c in a["curves"].items():
        print(f"   {name:14s} {c['pts'][0][0]:8.2f} → {c['pts'][-1][0]:8.2f}  값 {c['pts'][0][1]:6.1f} → {c['pts'][-1][1]:6.1f}  (꼭짓점 {len(c['pts'])})")
    bar = a["bar"]
    print(f"   한계 띠  {bar['year0']:.2f}–{bar['year1']:.2f} 년 · w_vol {bar['w_vol_bottom']:.1f}–{bar['w_vol_top']:.1f} Wh/l")
    print("== Fig. 1b (벡터)")
    print("   보정 잔차:", {k: round(v, 4) for k, v in b["calib_res"].items()}, f"· 회색 띠 {b['rt_x']:.3f} = {b['rt_K']:.1f} K")
    Ts = sorted(next(iter(b["series"].values()))["extra"], reverse=True) if b["series"] else []
    print("   " + " " * 24 + " 그린 범위 (K)      띠    " + "".join(f"{T:7.1f}" for T in Ts) + "   Ea(eV)  휨(dex)")
    for name, s in b["series"].items():
        rt = "   —  " if s["rt"] is None else f"{s['rt']:6.2f}"
        cells = "".join("     — " if s["extra"][T] is None else f"{s['extra'][T]:7.2f}" for T in Ts)
        print(f"   {name:24s} {s['T_hi_K']:6.1f}–{s['T_lo_K']:6.1f}  {rt}{cells}   {s['Ea_eV']:.3f}   {s['max_dev_dex']:.3f}")
    print("== 본문 · 캡션 산수")
    for q, v, unit, note in text_checks():
        print(f"   {q:32s} {v:9.4g} {unit:9s} {note}")


# ───────────────────────────── selftest ─────────────────────────────

def _build_synthetic(path, mutate=None):
    """실제 CFG 의 띠 · 범위에 맞춘 합성 쪽. mutate: 음성 경로용 변형 이름."""
    fz = _fitz()
    doc = fz.open()
    doc.new_page(width=595, height=782)
    pg = doc.new_page(width=595, height=782)     # 쪽 번호 1
    sh = pg.new_shape()

    def line(p, q, rgb, w=0.25, dashes=None):
        sh.draw_line(p, q)
        sh.finish(color=rgb, width=w, dashes=dashes)

    # Fig. 1a 축: 연도 1990 → x 93.5 · 6.12 pt/년 · w_vol 0 → y 234.9 · 0.13740 pt/(Wh/l) · w_grav 0 → 234.9 · 0.2748 pt/(Wh/kg)
    X = lambda yr: 93.5 + (yr - 1990) * 6.12
    YV = lambda v: 234.9 - v * 0.13740
    YG = lambda v: 234.9 - v * 0.27480
    xt = [1990, 1995, 2000, 2005, 2010, 2015]
    if mutate == "drop_xtick":
        xt = xt[:-1]
    for yr in xt:
        line((X(yr), 235.0), (X(yr), 237.3), BLACK)
    for v in [0, 200, 400, 600, 800, 1000]:
        y = YV(v) + (3.0 if (mutate == "shift_ytick" and v == 600) else 0.0)
        line((85.3, y), (87.5, y), BLUE)
    for v in [0, 100, 200, 300, 400, 500]:
        line((270.9, YG(v)), (273.1, YG(v)), RED)
    squares = [(2012, 650.0), (2016, 770.0)] + ([(2014, 700.0)] if mutate == "extra_square" else [])
    for yr, v in squares:
        sh.draw_rect(fz.Rect(X(yr) - 2, YV(v) - 2, X(yr) + 2, YV(v) + 2))
        sh.finish(fill=BLUE, color=None)
    for yr, v in [(2012, 225.0), (2016, 265.0)]:
        sh.draw_circle((X(yr), YG(v)), 1.8)
        sh.finish(fill=RED, color=None)
    for rgb, f, dash, seq in [(BLUE, YV, None, [(1991, 200), (1995, 270), (2003, 470)]),
                              (BLUE, YV, "[2 2] 0", [(2003, 470), (2008, 590), (2012, 650)]),
                              (RED, YG, None, [(1991, 70), (1995, 92), (2003, 160)]),
                              (RED, YG, "[2 2] 0", [(2003, 160), (2008, 205), (2012, 225)])]:
        sh.draw_polyline([(X(yr), f(v)) for yr, v in seq])
        sh.finish(color=rgb, width=0.5, dashes=dash, closePath=False)
    # Fig. 1b 축: 1000/T 2 → x 383.1 · 46.4 pt · log σ −1 → y 115.5 · 20.76 pt/dex
    IX = lambda s: 383.1 + (s - 2.0) * 46.4
    LY = lambda v: 115.5 + (-1.0 - v) * 20.76
    for s in [2, 3, 4, 5]:
        line((IX(s), 235.7), (IX(s), 238.1), BLACK)
    for K in [600, 500, 400, 300, 200]:
        x = IX(1000.0 / K) + (2.0 if (mutate == "shift_top" and K == 300) else 0.0)
        line((x, 95.2), (x, 96.6), BLACK)
    for v in [-1, -2, -3, -4, -5, -6]:
        line((361.0, LY(v)), (362.4, LY(v)), BLACK)
    sh.draw_rect(fz.Rect(IX(1000 / 300.0) - 1.1, 96.8, IX(1000 / 300.0) + 1.1, 234.0))
    sh.finish(fill=GREY, color=None)
    # 선 3 개: A (초록 실선 · 상온 걸침) · B (초록 점선 · 상온 안 걸침) · C (검정 점선 · log σ 0.0 꼭짓점 포함)
    A = [(3.3, -1.8), (3.8, -2.2), (4.2, -2.9)]          # 기울기 −0.8 → −1.75 로 꺾인다 (휨 검사용)
    B = [(2.6, -2.36), (3.2, -3.4)]
    C = [(1.6, 0.0), (2.6, -3.0)]
    if mutate != "drop_series":
        sh.draw_polyline([(IX(s), LY(v)) for s, v in A])
        sh.finish(color=GREEN, width=0.5, dashes=None, closePath=False)
    sh.draw_polyline([(IX(s), LY(v)) for s, v in B])
    sh.finish(color=GREEN, width=0.5, dashes="[2 2] 0", closePath=False)
    sh.draw_polyline([(IX(s), LY(v)) for s, v in C])
    sh.finish(color=BLACK, width=0.5, dashes="[2 2] 0", closePath=False)
    sh.commit()
    # 라벨 (글자색 = 선 색) · swap_label: A 라벨을 B 선 끝 옆에 둔다 · bad_color: A 라벨 글자색을 빨강으로
    a_pos = (IX(3.0), LY(-3.3)) if mutate == "swap_label" else (IX(4.25), LY(-2.7))
    pg.insert_text(a_pos, "SERA", fontsize=7, color=RED if mutate == "bad_color" else GREEN)
    pg.insert_text((IX(3.25), LY(-3.5)), "SERB", fontsize=7, color=GREEN)
    pg.insert_text((IX(1.7), LY(-1.0)), "SERC", fontsize=7, color=BLACK)
    # 한계 띠 이미지
    if mutate != "drop_bar":
        pix = fz.Pixmap(fz.csRGB, fz.IRect(0, 0, 20, 4), False)
        pix.set_rect(pix.irect, (90, 90, 90))
        pg.insert_image(fz.Rect(X(2001.2), YV(865.0), 271.0, YV(800.0)), pixmap=pix, keep_proportion=False)
    doc.save(str(path))
    return {"X": X, "IX": IX}


def _synthetic_cfg():
    cfg = copy.deepcopy(CFG)
    cfg["fig1b"]["series"] = [("SER_A", 0, GREEN, False, "SERA"), ("SER_B", 0, GREEN, True, "SERB"),
                              ("SER_C", 0, BLACK, True, "SERC")]
    return cfg


def selftest():
    fz = _fitz()
    fails = []

    def expect(cond, msg):
        print(("   ✅ " if cond else "   ❌ ") + msg)
        if not cond:
            fails.append(msg)

    def raises(mutate, which, msg):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "neg.pdf"
            _build_synthetic(p, mutate)
            cfg = _synthetic_cfg()
            pg = fz.open(str(p))[1]
            try:
                (read_fig1a if which == "a" else read_fig1b)(pg, cfg["fig1a" if which == "a" else "fig1b"])
            except ReadoutError as e:
                expect(True, f"{msg} → 멈춤 ({str(e)[:60]})")
                return
            expect(False, f"{msg} → 멈추지 않았다 (조용히 틀린 경로)")

    print("[양성] 합성 쪽에서 아는 값을 되읽는다")
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "pos.pdf"
        _build_synthetic(p)
        cfg = _synthetic_cfg()
        doc = fz.open(str(p))
        a = read_fig1a(doc[1], cfg["fig1a"])
        b = read_fig1b(doc[1], cfg["fig1b"])
        sq = sorted(a["squares"])
        ci = sorted(a["circles"])
        expect(abs(sq[0][0] - 2012) < 0.01 and abs(sq[0][1] - 650) < 0.5, f"w_vol 2012 = {sq[0][1]:.2f} (650)")
        expect(abs(sq[1][0] - 2016) < 0.01 and abs(sq[1][1] - 770) < 0.5, f"w_vol 2016 = {sq[1][1]:.2f} (770)")
        expect(abs(ci[1][1] - 265) < 0.5, f"w_grav 2016 = {ci[1][1]:.2f} (265)")
        expect(abs(a["curves"]["w_vol_solid"]["pts"][0][1] - 200) < 0.5, "w_vol 곡선 시작 200")
        expect(abs(a["curves"]["w_vol_dashed"]["pts"][0][0] - 2003) < 0.01, "점선 시작 2003")
        expect(abs(a["bar"]["w_vol_bottom"] - 800) < 0.5 and abs(a["bar"]["w_vol_top"] - 865) < 0.5, "한계 띠 800–865")
        s = b["series"]
        expect(abs(b["rt_K"] - 300.0) < 0.2, f"회색 띠 {b['rt_K']:.2f} K (300)")
        expect(s["SER_A"]["rt"] is not None and abs(s["SER_A"]["rt"] - (-1.8 - 0.4 / 0.5 * (1000 / 300 - 3.3))) < 0.005,
               f"A 상온 보간 {s['SER_A']['rt']}")
        expect(s["SER_B"]["rt"] is None, "B 는 띠에 안 닿는다 → None (외삽 안 함)")
        expect(s["SER_C"]["y_at_x_lo"] is not None and abs(s["SER_C"]["y_at_x_lo"] - 0.0) < 0.005,
               f"C 의 log σ 0.0 꼭짓점이 0 으로 남는다 ({s['SER_C']['y_at_x_lo']:.4f})")
        expect(abs(s["SER_C"]["Ea_eV"] - ea_from_slope(-3.0)) < 0.002, f"C 기울기 −3 → Ea {s['SER_C']['Ea_eV']:.4f} eV")
        expect(s["SER_C"]["max_dev_dex"] < 0.005 and s["SER_A"]["max_dev_dex"] > 0.01, "휨: 직선 C ≈ 0 · 꺾인 A > 0")
    print("[음성] 틀린 입력은 멈춰야 한다")
    raises("drop_xtick", "a", "Fig.1a 연도 눈금 하나 빠짐")
    raises("shift_ytick", "a", "Fig.1a w_vol 눈금 3 pt 어긋남")
    raises("extra_square", "a", "Fig.1a 사각 표지 3 개")
    raises("drop_bar", "a", "Fig.1a 한계 띠 없음")
    raises("shift_top", "b", "Fig.1b 위 K 축 300 K 눈금 2 pt 어긋남")
    raises("drop_series", "b", "Fig.1b 선 하나 없음")
    raises("bad_color", "b", "Fig.1b 라벨 글자색 ≠ 선 색")
    raises("swap_label", "b", "Fig.1b 같은 색 두 선의 라벨이 남의 선에 더 가깝다")
    print("[대조] kamaya2011 CSV")
    with tempfile.TemporaryDirectory() as td:
        line_xy = [(3.0, -1.5), (4.0, -2.8)]
        expect(kamaya_crosscheck(line_xy, Path(td) / "none.csv") is None, "파일 없음 → None (건너뜀 행을 남긴다)")
        good = Path(td) / "k.csv"
        good.write_text("# c\nfigure,series,x,x_unit,y,y_unit,note\nfig3,lgps polyline vertex,3.5,1000/T,-2.20,log,\n"
                        "fig3,lgps polyline vertex,4.5,1000/T,-3.4,log,\n", encoding="utf-8")
        xk = kamaya_crosscheck(line_xy, good)
        expect(len(xk) == 2 and abs((xk[0][2] - xk[0][1]) - 0.05) < 1e-9 and xk[1][2] is None,
               "같은 1000/T 차 +0.05 · 선 밖 꼭짓점은 None")
        bad = Path(td) / "b.csv"
        bad.write_text("figure,series,x\nfig1a,other,3.0\n", encoding="utf-8")
        try:
            kamaya_crosscheck(line_xy, bad)
            expect(False, "형식이 바뀐 CSV → 멈추지 않았다")
        except ReadoutError:
            expect(True, "형식이 바뀐 CSV (행 없음) → 멈춤")
    print("[CSV] 없는 값과 0 을 가른다")
    expect(_fmt(0.0) == "0" and _fmt(None) == "—" and _fmt(-0.0) in ("-0", "0"), f"_fmt(0.0) = {_fmt(0.0)!r} · _fmt(None) = {_fmt(None)!r}")
    print("[산수] 상수 계산")
    tc = {q: v for q, v, _u, _n in text_checks()}
    expect(abs(tc["w_grav_from_48g"] - 266.15) < 0.05, f"12.775 Wh / 48 g = {tc['w_grav_from_48g']:.2f}")
    expect(abs(tc["Li_theoretical_capacity"] - 3861) < 2, f"Li 이론 용량 {tc['Li_theoretical_capacity']:.0f} mAh/g")
    expect(abs(tc["voltage_only_gain_4p2_to_5V"] - 19.05) < 0.01, "4.2 → 5 V 전압만 +19.05 %")
    print(f"=== selftest {'통과' if not fails else '실패 ' + str(len(fails))}")
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", default=str(DEFAULT_PDF))
    ap.add_argument("--csv", default=str(OUT_CSV))
    ap.add_argument("--kamaya_csv", default=str(KAMAYA_CSV),
                    help="kamaya2011 digest 의 벡터 판독 CSV (LGPS 선 대조용 · 없으면 대조를 건너뛰고 그 사실을 CSV 에 남긴다)")
    ap.add_argument("--selftest", action="store_true")
    ar = ap.parse_args()
    if ar.selftest:
        return selftest()
    pdf = Path(ar.pdf)
    if not pdf.exists():
        print(f"⛔ PDF 없음: {pdf}", file=sys.stderr)
        return 2
    try:
        a, b, rows = run(pdf, Path(ar.csv), Path(ar.kamaya_csv))
    except ReadoutError as e:
        print(f"⛔ 판독 중단: {e}", file=sys.stderr)
        return 3
    _summary(a, b)
    print(f"→ {ar.csv}  ({len(rows)} 행)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
