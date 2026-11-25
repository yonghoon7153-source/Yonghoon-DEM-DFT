#!/usr/bin/env python3
"""kato2016_readout.py — Kato 2016 *Nat. Energy* 1, 16030 (LSiPSCl · Li9.6P3S12) 그림의 **벡터 경로 판독** + SI 표 산수 검산.

digest: litdb/papers/kato2016_high_power_assb_lsipscl_superionic.md
출력:   litdb/figures/kato2016_high_power_assb_lsipscl_superionic/digitized.csv

무엇을 읽나 (전부 PDF 안의 벡터 좌표 — 픽셀 판독이 아니다)
  Fig. 2a  Arrhenius 표지: LSiPSCl (짙은 초록 별표) · Li9.6P3S12 (올리브 삼각) · LGPS (자홍 사각) ·
           Li10.35Si1.35P1.65S12 (빨간 원) → 1000/T · log σ · 온도 범위 · Ea 재적합 (σ 형식)
  Fig. 3   LiCoO2/SE/Li 첫 충방전 표지 3 계 → 충전 끝 · 방전 끝 용량 (mAh) · CE
  Fig. 4e,f 100 °C 18 C 사이클 표지 (방전 사각 · 충전 삼각 · 효율 원) → 1 · 100 · 500 · 1000 번째 근처 값 · 유지율
  Fig. 5b  5 s 뒤 과도 전류 (전고체 원 · Li 이온 사각) vs 전압 계단 → Li 이온 셀 평탄 전류 · 2.5 V 계단 값
  SI Table S1 · S2 (PDF 텍스트를 손으로 옮긴 상수) → 단위셀 Li 수 · 전하 균형 · Cl 분포 · V = a²c · 자리대칭 검사
  SI Table S4 · S5 · Fig. S11 캡션 → C 율 정의 · 셀 질량 · R0 로 낸 분리막 유효 σ · 두 점 Arrhenius Ea

축 보정은 눈금선(tick) 좌표에 대한 **최소제곱 1 차식** 이고, 잔차가 문턱을 넘거나 눈금 개수가 값 개수와 다르면 멈춘다.
Fig. 2a 는 위쪽 °C 축 눈금을 아래 1000/T 축으로 되돌려 **같은 자리인지** 따로 검사한다.
범례 표지는 CFG 의 'legend' 사각형으로 뺀다 — 빼지 못하면 개수 검사에서 멈춘다.

⛔ 이 도구가 못 하는 것
  · 래스터 그림 (Fig. 2b,c · Fig. 5 삽입 분자 그림 · SI 그림) 은 안 읽는다 — SI 는 Fig. S4 (벡터 157 경로 · 이 도구 범위 밖) 를 빼면 래스터다.
  · Fig. 4a–d 충방전 곡선은 짧은 선분 1.5 천 개로 쪼개져 있어 곡선별로 가르지 않는다 (digest 에서 눈대중).
  · Fig. 6 Ragone 표지는 온도 (25 / 100 °C) 표시가 표지에 없어 판독하지 않는다.
  · 판독값은 **그림이 그린 값**이다 — 저자 원자료가 아니다. digest 에서는 `figure-read ≈` 로만 쓴다.
  · Fig. 3 CE 는 '표지 사이 거리' 다 — 양극 질량이 논문에 없어 mAh 를 mAh g⁻¹ 로 못 바꾼다.
  · 표 산수의 밀도 가정 (LCO 5.05 · LGPS 2.05 · AB 2.0 g cm⁻³) 은 **우리 가정**이다 — 논문 값이 아니다.
  · 겹친 표지 (≤ 1 pt) 는 한 점으로 합친다 — 반복 측정인지 중복 그리기인지 가르지 못한다 (합친 수는 기록).

usage
  ~/.venvs/litdb/bin/python3 tools/litdb/kato2016_readout.py --pdf "litdb/inbox/126._High-power_all-solid-state_batteries_using_sulfide_superionic_conductors.pdf"
  ~/.venvs/litdb/bin/python3 tools/litdb/kato2016_readout.py --selftest     # 합성 PDF 로 양성 + 음성 경로
"""
import argparse
import csv
import importlib.util
import math
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SLUG = "kato2016_high_power_assb_lsipscl_superionic"
OUT_CSV = ROOT / "litdb" / "figures" / SLUG / "digitized.csv"

KB_EV = 8.617333262e-5        # eV/K
EV_TO_KJMOL = 96.485332       # kJ/mol per eV
R_GAS = 8.314462618e-3        # kJ/(mol K)
LN10 = math.log(10.0)
NA = 6.02214076e23

BLACK = (0.14, 0.12, 0.13)

# 페이지 번호는 0 부터 · 사각형은 pt (PDF 좌표, y 아래로 증가)
CFG = {
    "fig2a": {
        "page": 1, "clip": (80, 85, 265, 250),
        "yticks": {"band": (83.5, 84.6), "vals": [0, -1, -2, -3, -4, -5]},          # 왼쪽 눈금 x0 ≈ 84.04
        "xticks": {"band": (239.4, 240.5), "vals": [1, 2, 3, 4, 5]},               # 아래 눈금 y0 ≈ 239.95
        "top": {"band": (91.0, 92.0), "C": [400, 200, 100, 0, -50]},              # 위 °C 눈금 y0 ≈ 91.5
        "legend": [(86, 165, 100, 245), (179, 94, 192, 147)],
        "series": {
            "LSiPSCl": {"kind": "asterisk", "rgb": (0.17, 0.40, 0.22), "n": (6, 6)},
            "Li9.6P3S12": {"kind": "fill", "rgb": (0.58, 0.58, 0.23), "items": 3, "n": (8, 8)},
            "LGPS": {"kind": "stroke_re", "rgb": (0.75, 0.32, 0.62), "n": (11, 11)},
            "Li10.35Si1.35P1.65S12": {"kind": "stroke_c", "rgb": (0.93, 0.17, 0.16), "n": (12, 12)},
        },
    },
    "fig3": {
        "page": 2, "clip": (70, 50, 272, 286),
        "xticks": {"band": (279.9, 281.0), "vals": [0.0, 0.2, 0.4, 0.6, 0.8]},
        "panels": {                                   # 왼쪽 눈금 x0 ≈ 77.2 · 패널마다 4.5 → 2.5 V
            "Li9.6P3S12": {"ybox": (50, 128), "kind": "fill", "rgb": (0.58, 0.58, 0.23), "items": 3, "n": (40, 60)},
            "LGPS": {"ybox": (128, 206), "kind": "stroke_re", "rgb": (0.75, 0.32, 0.62), "n": (35, 50)},
            "LSiPSCl": {"ybox": (206, 286), "kind": "asterisk", "rgb": (0.17, 0.40, 0.22), "n": (40, 60)},
        },
        "ytick_band": (76.7, 77.7), "yvals": [4.5, 4.0, 3.5, 3.0, 2.5],
        "legend": [(188, 160, 210, 200)],
        "paper_CE": {"Li9.6P3S12": 90, "LGPS": 61, "LSiPSCl": 39},
    },
    "fig4a": {
        "page": 3, "clip": (95, 55, 300, 192),
        "ytick_band": (109.0, 110.0), "yvals": [4, 3, 2],
        "xticks": {"bands": [(128.5, 129.5), (184.1, 185.1)], "vals": [30, 60, 90, 120]},
        "panels": {"100C": (60, 132.6), "25C": (132.6, 188.2)},
        "navy": (0.18, 0.19, 0.57), "magenta": (0.93, 0.0, 0.55), "cut_navy": 1.06, "cut_mag": (2.40, 2.62),
        "n_ends": {"100C": (3, 3), "25C": (2, 2)},
    },
    "fig4e": {
        "page": 3, "clip": (105, 350, 260, 450), "type": "Normal (LTO+LGPS / LGPS / LCO+LGPS)",
        "yticks": {"band": (109.0, 110.0), "vals": [250, 200, 150, 100, 50]},
        "xticks": {"band": (444.2, 445.2), "vals": [200, 400, 600, 800]},
        "ce_axis": {"vals": [125, 100, 75, 50, 25]},                      # 오른쪽 축 = 같은 눈금 자리
        "n": (45, 55), "cycles": [1, 100, 500, 1000],
    },
    "fig4f": {
        "page": 3, "clip": (342, 350, 497, 450), "type": "Large-current (LTO+LSiPSCl / LSiPSCl / LCO+LSiPSCl)",
        "yticks": {"band": (346.0, 347.0), "vals": [250, 200, 150, 100, 50]},
        "xticks": {"band": (444.3, 445.3), "vals": [100, 200, 300, 400]},
        "ce_axis": {"vals": [125, 100, 75, 50, 25]},
        "n": (45, 55), "cycles": [1, 100, 500],
    },
    "fig5b": {
        "page": 4, "clip": (334, 50, 505, 127),
        "yticks": {"band": (335.7, 336.7), "vals": [-1.0, -1.5, -2.0, -2.5, -3.0]},
        "xticks": {"band": (123.6, 124.6), "vals": [0.5, 1.0, 1.5, 2.0]},
        "assb_rgb": (0.08, 0.46, 0.74), "lib_rgb": (0.66, 0.66, 0.67), "n": (25, 30),
    },
}

# ── SI 표 (PDF 텍스트에서 옮긴 상수) ─────────────────────────────────────────
TABLE_S1 = {   # Li9.54Si1.74P1.44S11.7Cl0.3 · 25 °C · 중성자 Rietveld
    "Li": {"Li(1) 16h": (16, 0.5), "Li(2) 4d": (4, 1.0), "Li(3) 8f": (8, 0.972), "Li(4) 4c": (4, 0.765)},
    "g_P1_4d": 0.108, "g_P2_2b": 1.0,
    "g_S": {"S(1)": 0.9590, "S(2)": 0.9827, "S(3)": 0.9817},
    "Li3_xyz": (0.24384, 0.24384, 0.0),           # '= x(Li(3))' · z = 0
    "a": 8.709652, "c": 12.56907, "Rwp": 4.45, "Re": 1.98, "S_printed": 2.25,
    "nominal": {"Li": 9.54, "Si": 1.74, "P": 1.44, "S": 11.7, "Cl": 0.3},
}
TABLE_S2 = {   # Li9.6P3S12 · 25 °C
    "Li": {"Li(1) 16h": (16, 0.51), "Li(2) 4d": (4, 0.55), "Li(3) 8f": (8, 0.35), "Li(4) 4c": (4, 0.79)},
    "Li3_xyz": (0.276, 0.269, 0.128),
    "a": 8.7144, "c": 12.4677, "Rwp": 2.88, "S_printed": 2.42,
    "nominal": {"Li": 9.6, "P": 3.0, "S": 12.0},
}
CELL = {"m_LCO_mg": 4.867, "Q_LCO_mAh_g": None, "Q_theor_mAh": 0.667, "area_cm2": 1.0,
        "E_LCO": {"large": 319.6, "high_voltage": 430.9, "normal": 297.7, "LIB": 302.4},
        "E_cell": {"large": 17.6, "high_voltage": 32.8, "normal": 16.4, "LIB": 73.2},
        "sep_um": 240, "R0_ASSB_25C": 3.68, "R0_LIB_25C": 3.37}
R_TEMPS = {"R0": {"ASSB": (3.68, 41.0), "LIB": (3.37, 44.4)},    # (25 °C Table S5 · −30 °C Fig. S11 캡션) Ω
           "R1": {"ASSB": (1.94, 14.2), "LIB": (0.62, 42.4)},
           "R2": {"ASSB": (2.43, 157.4), "LIB": (4.16, 708.4)}}
R_EA_PRINTED = {("R1", "ASSB"): 21.9, ("R2", "ASSB"): 45.6, ("R1", "LIB"): 46.4, ("R2", "LIB"): 56.4}
DENS = {"LCO": 5.05, "LGPS": 2.05, "AB": 2.0}   # ⚠ 우리 가정 (g cm^-3)
TABLE_S6 = {"a": {"t_um": 25, "wt": {"LCO": 70, "LGPS": 27, "AB": 3}, "oneC_mA": 0.93},
            "b": {"t_um": 308, "wt": {"LCO": 61, "LGPS": 36, "AB": 3}, "oneC_mA": 8.0},
            "main": {"t_um": 28, "wt": {"LCO": 60, "LGPS": 34, "AB": 6}, "m_LCO_mg": 4.867}}


class ReadoutError(RuntimeError):
    pass


# ───────────────────────── 기본 연산 ─────────────────────────
def _close(c, ref, tol=0.02):
    return c is not None and len(c) == 3 and all(abs(a - b) <= tol for a, b in zip(c, ref))


def _center(r):
    return ((r.x0 + r.x1) / 2.0, (r.y0 + r.y1) / 2.0)


def _items_bbox(d):
    """경로 항목 좌표의 경계상자 (x0, y0, x1, y1).
    ⚠ PyMuPDF 1.2x 의 d['rect'] 는 하위경로가 둘 이상인 경로 ('m … l m … l S') 에서 **두 번째 하위경로의 시작점을
    빼먹는다** (2026-11-10 실측: '+' 별표 (97.8–102.2) 의 rect 가 x0 = 100 으로 나왔다). 그래서 표지 중심은
    rect 가 아니라 항목 좌표로 낸다. 'c' 의 조절점은 원 근사에서 외접 정사각형 안이라 중심이 안 틀어진다."""
    xs, ys = [], []
    for it in d["items"]:
        if it[0] == "re":
            r = it[1]
            xs += [r.x0, r.x1]
            ys += [r.y0, r.y1]
        elif it[0] == "qu":
            q = it[1]
            for p in (q.ul, q.ur, q.ll, q.lr):
                xs.append(p.x)
                ys.append(p.y)
        else:
            for p in it[1:]:
                if hasattr(p, "x"):
                    xs.append(p.x)
                    ys.append(p.y)
    if not xs:
        r = d["rect"]
        return (r.x0, r.y0, r.x1, r.y1)
    return (min(xs), min(ys), max(xs), max(ys))


def _in_rects(p, rects):
    return any(x0 <= p[0] <= x1 and y0 <= p[1] <= y1 for x0, y0, x1, y1 in rects)


def drawings_in(page, clip):
    import fitz
    R = fitz.Rect(clip)
    return [d for d in page.get_drawings() if R.contains(d["rect"]) or R.intersects(d["rect"])]


def ticks(draws, band, axis, max_len=6.0, thin=0.6):
    """검은 짧은 축정렬 선분 / 얇은 채움 사각형 = 눈금. axis='y' → 왼쪽 눈금 (x0 가 band 안) → y 위치들,
    axis='x' → 아래 눈금 (y0 가 band 안) → x 위치들. 0.05 pt 안의 중복은 하나로."""
    out = []
    for d in draws:
        if not (_close(d.get("color"), BLACK) or _close(d.get("fill"), BLACK)):
            continue
        r = d["rect"]
        w, h = r.width, r.height
        if axis == "y" and h <= thin and 1.0 <= w <= max_len and band[0] <= r.x0 <= band[1]:
            out.append((r.y0 + r.y1) / 2.0)
        elif axis == "x" and w <= thin and 1.0 <= h <= max_len and band[0] <= r.y0 <= band[1]:
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
    """눈금 픽셀은 오름차순 · 값은 CFG 순서 그대로 (y 축은 위 → 아래 = 큰 값 → 작은 값)."""
    return fit_linear(sorted(tick_pix), vals, tol, name)


def cluster(points, radius=1.0):
    """반경 안의 점들을 하나로 (평균). (중심, 합친 수) 목록 — 별표처럼 여러 경로로 그린 표지를 한 점으로."""
    groups = []
    for p in points:
        for g in groups:
            if math.hypot(p[0] - g[0][0], p[1] - g[0][1]) <= radius:
                g[1].append(p)
                break
        else:
            groups.append([p, [p]])
    return [((sum(q[0] for q in g[1]) / len(g[1]), sum(q[1] for q in g[1]) / len(g[1])), len(g[1])) for g in groups]


def markers(draws, kind, rgb, items=None, max_w=8.0, legend=(), box=None):
    """표지 중심들 (그려진 순서). kind: asterisk · fill · stroke_re · stroke_c · stroke_tri · fill_c · fill_re"""
    raw = []
    for idx, d in enumerate(draws):
        bx = _items_bbox(d)
        bw, bh = bx[2] - bx[0], bx[3] - bx[1]
        if bw > max_w or bh > max_w:
            continue
        its = d["items"]
        ops = [it[0] for it in its]
        ok = False
        if kind == "asterisk":          # 별표 = 선 1–2 개짜리 경로 여러 개 (+ · ×) — 중심으로 합친다 (merged)
            ok = (_close(d.get("color"), rgb) and d.get("fill") is None and 1 <= len(ops) <= 2
                  and all(o == "l" for o in ops) and max(bw, bh) > 2.0)
        elif kind == "fill":
            ok = _close(d.get("fill"), rgb) and len(ops) == items
        elif kind == "stroke_re":
            ok = _close(d.get("color"), rgb) and d.get("fill") is None and ops == ["re"]
        elif kind == "stroke_c":
            ok = _close(d.get("color"), rgb) and d.get("fill") is None and len(ops) == 4 and all(o == "c" for o in ops)
        elif kind == "stroke_tri":
            ok = _close(d.get("color"), rgb) and d.get("fill") is None and len(ops) == 3 and all(o == "l" for o in ops)
        elif kind == "fill_c":
            ok = _close(d.get("fill"), rgb) and len(ops) == 4 and all(o == "c" for o in ops)
        elif kind == "fill_re":
            ok = _close(d.get("fill"), rgb) and ops == ["re"]
        if not ok:
            continue
        c = ((bx[0] + bx[2]) / 2.0, (bx[1] + bx[3]) / 2.0)
        if legend and _in_rects(c, legend):
            continue
        if box and not (box[0] <= c[1] <= box[1]):
            continue
        raw.append((idx, c))
    return raw


def merged(raw, radius=1.0):
    """(그린 순서, 중심) → 겹친 것을 합친 (중심, 합친 수, 첫 순서) — 순서를 보존한다."""
    out = []
    for idx, c in raw:
        for g in out:
            if math.hypot(c[0] - g["c"][0], c[1] - g["c"][1]) <= radius:
                g["pts"].append(c)
                g["c"] = (sum(p[0] for p in g["pts"]) / len(g["pts"]), sum(p[1] for p in g["pts"]) / len(g["pts"]))
                break
        else:
            out.append({"c": c, "pts": [c], "first": idx})
    out.sort(key=lambda g: g["first"])
    return out


def need(n, rng, name):
    if not (rng[0] <= n <= rng[1]):
        raise ReadoutError(f"{name}: 표지 {n} 개 — 기대 {rng[0]}–{rng[1]} (색 · 범례 제외 · 모양 조건을 다시 본다)")


def lin_fit(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    m = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx
    b = my - m * mx
    ss_res = sum((y - (m * x + b)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return m, b, 1 - ss_res / ss_tot if ss_tot else float("nan")


def ea_from_slope(m_per_1000K):
    """log10 σ vs 1000/T 기울기 → Ea (eV). σ 형식 (σT 아님) — 논문 Fig. 2a 와 같은 형식."""
    return -m_per_1000K * 1000.0 * LN10 * KB_EV


def ce_from_branch(pts, x_eps_frac=0.01):
    """(용량, 전압) 표지 → 충전 끝 (최대 용량) · 방전 끝 (용량 > x_eps 중 최저 전압 표지) · CE.
    충전 시작 표지 (용량 ≈ 0) 는 방전 끝 후보에서 뺀다. 방전 가지가 없으면 멈춘다."""
    if len(pts) < 5:
        raise ReadoutError(f"CE: 표지 {len(pts)} 개 — 너무 적다")
    xmax = max(p[0] for p in pts)
    cand = [p for p in pts if p[0] > x_eps_frac * xmax]
    if not cand:
        raise ReadoutError("CE: 방전 끝 후보가 없다")
    dis_end = min(cand, key=lambda p: p[1])
    vmin_charge = min(p[1] for p in pts if abs(p[0] - xmax) < 1e-9)
    if dis_end[1] >= vmin_charge - 0.3:
        raise ReadoutError(f"CE: 방전 끝 전압 {dis_end[1]:.2f} V 가 충전 끝 {vmin_charge:.2f} V 와 0.3 V 안 — 방전 가지가 안 보인다")
    return {"Q_charge": xmax, "x_dis_end": dis_end[0], "V_dis_end": dis_end[1],
            "Q_discharge": xmax - dis_end[0], "CE": (xmax - dis_end[0]) / xmax * 100.0}


def nearest(series, x):
    return min(series, key=lambda p: abs(p[0] - x))


def hop_line(ea_ev, T):
    src = ROOT / "tools" / "sei" / "collect_neb.py"
    if not src.exists():
        return None
    spec = importlib.util.spec_from_file_location("_collect_neb_hop", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    h = mod.hop_check(ea_ev, T)
    return h["line"] if h else None


# ───────────────────────── 그림별 판독 ─────────────────────────
def read_fig2a(page, cfg):
    dr = drawings_in(page, cfg["clip"])
    my = calib(ticks(dr, cfg["yticks"]["band"], "y"), cfg["yticks"]["vals"], 0.01, "Fig2a y")
    mx = calib(ticks(dr, cfg["xticks"]["band"], "x"), cfg["xticks"]["vals"], 0.01, "Fig2a x")
    top = ticks(dr, cfg["top"]["band"], "x")
    if len(top) != len(cfg["top"]["C"]):
        raise ReadoutError(f"Fig2a 위 °C 눈금 {len(top)} 개 ↔ 값 {len(cfg['top']['C'])} 개")
    tops = sorted(cfg["top"]["C"], reverse=True)            # 왼쪽 (고온) → 오른쪽 (저온)
    dev = max(abs((mx[0] * x + mx[1]) - 1000.0 / (c + 273.15)) for x, c in zip(top, tops))
    if dev > 0.02:
        raise ReadoutError(f"Fig2a 위 °C 축이 1000/T 축과 {dev:.3f} 어긋난다 — 라벨이나 눈금 분류가 틀렸다")
    out = {"x_res": mx[2], "y_res": my[2], "top_dev": dev, "series": {}, "subs": {}}
    for name, s in cfg["series"].items():
        raw = markers(dr, s["kind"], s["rgb"], s.get("items"), legend=cfg["legend"])
        g = merged(raw, radius=1.0)
        need(len(g), s["n"], f"Fig2a {name}")
        pts = [(mx[0] * c["c"][0] + mx[1], my[0] * c["c"][1] + my[1], len(c["pts"])) for c in g]
        out["series"][name] = sorted(pts)
        # 한 점 안에 **서로 다른 자리 (> 0.1 pt)** 가 있으면 겹쳐 그린 표지 (반복 측정 꼴) — 하나씩 기록
        subs = []
        for c in g:
            sc = cluster(c["pts"], radius=0.1)
            if len(sc) > 1:
                subs.append([(mx[0] * p[0] + mx[1], my[0] * p[1] + my[1], k) for p, k in sc])
        out["subs"][name] = sorted(subs)
    return out


def read_fig3(page, cfg):
    dr = drawings_in(page, cfg["clip"])
    mx = calib(ticks(dr, cfg["xticks"]["band"], "x"), cfg["xticks"]["vals"], 0.002, "Fig3 x")
    yt = ticks(dr, cfg["ytick_band"], "y")
    out = {"x_res": mx[2], "series": {}}
    for name, p in cfg["panels"].items():
        pt = [y for y in yt if p["ybox"][0] <= y <= p["ybox"][1]]
        my = calib(pt, cfg["yvals"], 0.005, f"Fig3 y ({name})")
        raw = markers(dr, p["kind"], p["rgb"], p.get("items"), legend=cfg["legend"], box=p["ybox"])
        g = merged(raw, radius=0.9)
        need(len(g), p["n"], f"Fig3 {name}")
        pts = [(mx[0] * c["c"][0] + mx[1], my[0] * c["c"][1] + my[1]) for c in g]
        res = ce_from_branch(pts)
        order_max = max(range(len(pts)), key=lambda i: pts[i][0])
        res["order_split_ok"] = all(pts[i][0] <= pts[i + 1][0] + 1e-6 for i in range(order_max)) and \
            all(pts[i][0] >= pts[i + 1][0] - 1e-6 for i in range(order_max, len(pts) - 1))
        res.update({"y_res": my[2], "n": len(pts), "pts": pts})
        out["series"][name] = res
    return out


def read_fig4a(page, cfg):
    """방전 곡선 끝 용량. 남색 실선 (LTO 셀) = 짧은 선분 수천 개 → 하한 전압 (1 V) 근처 점을 x 로 묶어 곡선마다 끝 x ·
    자홍 점선 (흑연 셀) = 경로 하나하나의 끝점 중 전압이 하한 (2.5 V) 근처인 것. 범례 선 (V > 4.5) 은 저절로 빠진다."""
    dr = drawings_in(page, cfg["clip"])
    xs = []
    for band in cfg["xticks"]["bands"]:
        xs = ticks(dr, band, "x")
        if len(xs) == len(cfg["xticks"]["vals"]):
            break
    mx = calib(xs, cfg["xticks"]["vals"], 0.05, "Fig4a x")
    yt = ticks(dr, cfg["ytick_band"], "y")
    out = {"x_res": mx[2], "ends": {}}
    for pn, (y0, y1) in cfg["panels"].items():
        my = calib([y for y in yt if y0 <= y <= y1], cfg["yvals"], 0.01, f"Fig4a y {pn}")
        V = lambda y: my[0] * y + my[1]
        low = []
        for d in dr:
            if not _close(d.get("color"), cfg["navy"]):
                continue
            for it in d["items"]:
                for p in it[1:]:
                    if hasattr(p, "x") and y0 <= p.y <= y1 and V(p.y) < cfg["cut_navy"]:
                        low.append((p.x, p.y))
        navy = []
        for c, n in cluster(sorted(low), radius=3.0):
            xe = max(q[0] for q in low if abs(q[0] - c[0]) < 3.5)
            if all(abs(xe - e) > 0.5 for e in navy):
                navy.append(xe)
        need(len(navy), cfg["n_ends"][pn], f"Fig4a {pn} 남색 곡선 끝")
        mag = []
        for d in dr:
            if not _close(d.get("color"), cfg["magenta"]):
                continue
            ps = [(p.x, p.y) for it in d["items"] for p in it[1:] if hasattr(p, "x") and y0 <= p.y <= y1]
            if not ps:
                continue
            xm = max(ps, key=lambda p: p[0])
            if cfg["cut_mag"][0] <= V(xm[1]) <= cfg["cut_mag"][1]:
                mag.append((mx[0] * xm[0] + mx[1], V(xm[1])))
        # 점선은 대시 조각마다 경로가 따로다 — 끝 근처 조각 둘 이상이 창에 들면 x 로 묶어 가장 먼 것만 (실물 900 C: 28.3 · 30.6)
        mag.sort()
        dedup = []
        for x, v in mag:
            if dedup and x - dedup[-1][0] < 4.0:
                dedup[-1] = (x, v)
            else:
                dedup.append((x, v))
        mag = dedup
        need(len(mag), (2, 2), f"Fig4a {pn} 자홍 곡선 끝")
        out["ends"][pn] = {"large_current": sorted(mx[0] * x + mx[1] for x in navy), "high_voltage": sorted(mag)}
    return out


def read_cycles(page, cfg):
    dr = drawings_in(page, cfg["clip"])
    my = calib(ticks(dr, cfg["yticks"]["band"], "y"), cfg["yticks"]["vals"], 0.2, "Fig4 y")
    mx = calib(ticks(dr, cfg["xticks"]["band"], "x"), cfg["xticks"]["vals"], 0.5, "Fig4 x")
    mce = calib(ticks(dr, cfg["yticks"]["band"], "y"), cfg["ce_axis"]["vals"], 0.1, "Fig4 CE")
    red, blue = (0.93, 0.11, 0.14), (0.13, 0.25, 0.6)
    dis = merged(markers(dr, "stroke_re", red), 0.5)
    chg = merged(markers(dr, "stroke_tri", blue), 0.5)
    ce = merged(markers(dr, "stroke_c", BLACK), 0.5)
    for nm, g in (("방전", dis), ("충전", chg), ("효율", ce)):
        need(len(g), cfg["n"], f"Fig4 {nm}")
    f = lambda g, m: sorted((mx[0] * c["c"][0] + mx[1], m[0] * c["c"][1] + m[1]) for c in g)
    return {"x_res": mx[2], "y_res": my[2], "dis": f(dis, my), "chg": f(chg, my), "ce": f(ce, mce)}


def read_fig5b(page, cfg):
    dr = drawings_in(page, cfg["clip"])
    my = calib(ticks(dr, cfg["yticks"]["band"], "y"), cfg["yticks"]["vals"], 0.01, "Fig5b y")
    mx = calib(ticks(dr, cfg["xticks"]["band"], "x"), cfg["xticks"]["vals"], 0.01, "Fig5b x")
    a = merged(markers(dr, "fill_c", cfg["assb_rgb"]), 0.5)
    lib = merged(markers(dr, "fill_re", cfg["lib_rgb"]), 0.5)
    need(len(a), cfg["n"], "Fig5b 전고체")
    need(len(lib), cfg["n"], "Fig5b Li 이온")
    f = lambda g: sorted((mx[0] * c["c"][0] + mx[1], my[0] * c["c"][1] + my[1]) for c in g)
    return {"x_res": mx[2], "y_res": my[2], "assb": f(a), "lib": f(lib)}


# ───────────────────────── 표 산수 ─────────────────────────
def site_ok_8f(xyz, tol=1e-6):
    """P4₂/nmc (No. 137, origin 1) 8f = (x, x, 0) — Table S1 · Kamaya 2011 과 같은 원점 관례."""
    x, y, z = xyz
    return abs(x - y) <= tol and abs(z) <= tol


def li_per_cell(table, li3_mult=None):
    tot = 0.0
    for k, (mult, g) in table["Li"].items():
        if k.startswith("Li(3)") and li3_mult is not None:
            mult = li3_mult
        tot += mult * g
    return tot


def table_checks():
    rows = []
    t1 = TABLE_S1
    li1 = li_per_cell(t1)
    si = 4 * (1 - t1["g_P1_4d"]) + 2 * (1 - t1["g_P2_2b"])
    p = 4 * t1["g_P1_4d"] + 2 * t1["g_P2_2b"]
    cl_site = {k: 8 * (1 - g) for k, g in t1["g_S"].items()}
    cl = sum(cl_site.values())
    s = 8 * sum(t1["g_S"].values())
    charge = li1 + 4 * si + 5 * p - 2 * s - cl
    v1 = t1["a"] ** 2 * t1["c"]
    nom = t1["nominal"]
    rows += [("S1 Li per cell (refined)", li1, "16h·0.5 + 4d·1 + 8f·0.972 + 4c·0.765"),
             ("S1 Li per cell (nominal, Z=2)", 2 * nom["Li"], "2 × 9.54"),
             ("S1 Li excess vs nominal (%)", (li1 / (2 * nom["Li"]) - 1) * 100, "refined / nominal − 1"),
             ("S1 Si per f.u. (refined)", si / 2, "4d (1−0.108) · 2b 0"),
             ("S1 P per f.u. (refined)", p / 2, "4d 0.108 + 2b 1"),
             ("S1 tetrahedral cations per f.u. (nominal Si+P)", nom["Si"] + nom["P"], "LGPS-type has 3 M sites per 12 anions"),
             ("S1 Cl per f.u. (refined)", cl / 2, "Σ 8·(1−g(S))"),
             ("S1 Cl share on Cl(1) (%)", cl_site["S(1)"] / cl * 100, "paper: 'mainly located in Cl(1)'"),
             ("S1 Cl share on Cl(2)+Cl(3) (%)", (cl_site["S(2)"] + cl_site["S(3)"]) / cl * 100, "paper: 'insubstantial'"),
             ("S1 charge balance per cell (e)", charge, "Li+ + 4 Si + 5 P − 2 S − Cl (refined occupancies)"),
             ("S1 nominal charge balance per f.u. (e)",
              nom["Li"] + 4 * nom["Si"] + 5 * nom["P"] - 2 * nom["S"] - nom["Cl"], "Li9.54Si1.74P1.44S11.7Cl0.3"),
             ("S1 V = a^2 c (A^3)", v1, "a 8.709652 · c 12.56907"),
             ("S1 c/a", t1["c"] / t1["a"], ""),
             ("S1 S = Rwp/Re", t1["Rwp"] / t1["Re"], f"printed {t1['S_printed']}"),
             ("S1 Li(3) 8f site symmetry ok", 1.0 if site_ok_8f(t1["Li3_xyz"]) else 0.0, "(x, x, 0)")]
    t2 = TABLE_S2
    li2_8f = li_per_cell(t2)
    li2_16 = li_per_cell(t2, li3_mult=16)
    v2 = t2["a"] ** 2 * t2["c"]
    rows += [("S2 Li per cell if Li(3) is 8f", li2_8f, "as printed"),
             ("S2 Li per cell if Li(3) is 16-fold general", li2_16, "coordinates (0.276, 0.269, 0.128) are general"),
             ("S2 Li per cell (nominal, Z=2)", 2 * t2["nominal"]["Li"], "2 × 9.6"),
             ("S2 Li(3) 8f site symmetry ok", 1.0 if site_ok_8f(t2["Li3_xyz"]) else 0.0, "(x, x, 0) required"),
             ("S2 nominal charge balance per f.u. if all P5+ (e)", 9.6 + 5 * 3 - 2 * 12, "Li9.6P3S12"),
             ("S2 mean P valence for neutrality", (2 * 12 - 9.6) / 3, "(24 − 9.6)/3"),
             ("S2 synthesis P (elemental) per f.u.", 3 - 2 * ((12 - 9.6 / 2) / 5), "x Li2S + y P2S5 + z P"),
             ("S2 V = a^2 c (A^3)", v2, "a 8.7144 · c 12.4677"),
             ("S2 Re = Rwp/S", t2["Rwp"] / t2["S_printed"], "")]
    # 셀 산수
    q_th = CELL["m_LCO_mg"] * 1e-3 * 137.0
    rows += [("cell theoretical capacity at 137 mAh/g (mAh)", q_th, f"paper 0.667 mAh · m_LCO {CELL['m_LCO_mg']} mg"),
             ("cell 18C current (mA/cm2)", 18 * CELL["Q_theor_mAh"], "paper 12 mA/cm2"),
             ("cell 1500C current (mA/cm2)", 1500 * CELL["Q_theor_mAh"], "paper 1000 mA/cm2")]
    for k in CELL["E_LCO"]:
        rows.append((f"cell mass implied ({k}) (mg/cm2)", CELL["m_LCO_mg"] * CELL["E_LCO"][k] / CELL["E_cell"][k],
                     "m_LCO × E_LCO / E_cell (Table S4)"))
    sig0 = CELL["sep_um"] * 1e-4 / CELL["R0_ASSB_25C"] * 1e3
    rows.append(("separator effective sigma from R0, normal type 25 C (mS/cm)", sig0,
                 "240 um / R0 3.68 Ohm cm2 — upper bound on separator resistance"))
    inv = 1 / 298.15 - 1 / 243.15
    for (rk, cell), (r25, r_30) in [((rk, c), v) for rk, d in R_TEMPS.items() for c, v in d.items()]:
        ea = R_GAS * math.log(r_30 / r25) / (-inv)
        pr = R_EA_PRINTED.get((rk, cell))
        rows.append((f"two-point Ea {rk} {cell} (kJ/mol)", ea, f"25 C Table S5 · −30 C Fig. S11 caption · printed {pr}"))
    # Li 농도 (본문 ~35 mol/dm3)
    for nm, li, v in (("LGPS Kamaya neutron", 20.0, 952.349), ("LSiPSCl nominal", 2 * 9.54, v1)):
        rows.append((f"Li concentration {nm} (mol/dm3)", li / (v * 1e-24) / NA * 1e3, "total Li, not carrier"))
    # Table S6 · 본문 셀 로딩 (밀도는 우리 가정)
    for k, t in TABLE_S6.items():
        wt = t["wt"]
        rho_th = 100.0 / sum(wt[m] / DENS["LGPS" if m == "LGPS" else m] for m in wt)
        m_lco = t.get("m_LCO_mg") or t["oneC_mA"] / 0.137
        comp_mg = m_lco / (wt["LCO"] / 100.0)
        rho_app = comp_mg * 1e-3 / (t["t_um"] * 1e-4)
        rows.append((f"Table S6/{k} LCO loading (mg/cm2)", m_lco, "1C / 137 mAh/g" if k != "main" else "Methods"))
        rows.append((f"Table S6/{k} composite relative density (%)", rho_app / rho_th * 100,
                     f"apparent {rho_app:.2f} / solid {rho_th:.2f} g/cm3 (assumed densities)"))
    return rows


# ───────────────────────── 실행 ─────────────────────────
def run(pdf):
    import fitz
    doc = fitz.open(pdf)
    f2 = read_fig2a(doc[CFG["fig2a"]["page"]], CFG["fig2a"])
    f3 = read_fig3(doc[CFG["fig3"]["page"]], CFG["fig3"])
    f4a = read_fig4a(doc[CFG["fig4a"]["page"]], CFG["fig4a"])
    f4e = read_cycles(doc[CFG["fig4e"]["page"]], CFG["fig4e"])
    f4f = read_cycles(doc[CFG["fig4f"]["page"]], CFG["fig4f"])
    f5 = read_fig5b(doc[CFG["fig5b"]["page"]], CFG["fig5b"])
    doc.close()
    rows = []

    def put(fig, series, x, xu, y, yu, note=""):
        rows.append((fig, series, round(x, 5), xu, round(y, 6), yu, note))

    print(f"Fig. 2a  축 잔차 x {f2['x_res']:.4f} / y {f2['y_res']:.4f} · °C 축 편차 {f2['top_dev']:.4f}")
    for name, pts in f2["series"].items():
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        m, b, r2 = lin_fit(xs, ys)
        ea = ea_from_slope(m)
        tC = [1000.0 / x - 273.15 for x in xs]
        x25 = 1000.0 / 298.15
        near = [p for p in pts if abs(p[0] - x25) < 0.02]
        subs = f2["subs"].get(name, [])
        msg = (f"   {name}: {len(pts)} 점 · 경로 {min(p[2] for p in pts)}–{max(p[2] for p in pts)} 개/점 · "
               f"{max(tC):.1f} ~ {min(tC):.1f} °C · 재적합 Ea ≈ {ea:.4f} eV = {ea * EV_TO_KJMOL:.1f} kJ/mol (R² {r2:.4f})")
        if near:
            msg += f" · 25 °C 점 σ ≈ {10 ** near[0][1] * 1e3:.2f} mS/cm"
        else:
            msg += f" · 25 °C 직선 σ ≈ {10 ** (m * x25 + b) * 1e3:.2f} mS/cm (25 °C 점 없음)"
        print(msg)
        print("      온도 (°C): " + ", ".join(f"{t:.0f}" for t in sorted(tC, reverse=True)))
        for sb in subs:
            t0 = 1000.0 / sb[0][0] - 273.15
            print(f"      겹쳐 그린 표지 @ {t0:.1f} °C: " + " · ".join(f"{10 ** y * 1e3:.2f} mS/cm ({k} 경로)" for _, y, k in sb))
            for x, y, k in sb:
                put("fig2a", f"{name} (overdrawn sub-marker)", x, "1000/T K^-1", y, "log10 S/cm",
                    f"T = {1000 / x - 273.15:.1f} C · {k} paths at this spot")
        for x, y, k in pts:
            put("fig2a", name, x, "1000/T K^-1", y, "log10 S/cm", f"T = {1000 / x - 273.15:.1f} C · paths {k}")
        put("fig2a", f"OUR ARITHMETIC Ea refit {name}", 0, "-", ea * EV_TO_KJMOL, "kJ/mol",
            f"sigma form · {len(pts)} points · {max(tC):.0f} to {min(tC):.0f} C")
    ea_lsi = ea_from_slope(lin_fit([p[0] for p in f2["series"]["LSiPSCl"]], [p[1] for p in f2["series"]["LSiPSCl"]])[0])
    print("   " + str(hop_line(ea_lsi, 298.15)))

    print(f"Fig. 3   축 잔차 x {f3['x_res']:.5f} mAh")
    for name, r in f3["series"].items():
        print(f"   {name}: 표지 {r['n']} · 충전 끝 {r['Q_charge']:.3f} mAh · 방전 끝 위치 {r['x_dis_end']:.3f} mAh "
              f"({r['V_dis_end']:.2f} V) · 방전 {r['Q_discharge']:.3f} mAh · CE ≈ {r['CE']:.1f} % "
              f"(논문 {CFG['fig3']['paper_CE'][name]} %) · 그린 순서 = 충전→방전 {r['order_split_ok']}")
        for x, y in r["pts"]:
            put("fig3", name, x, "mAh", y, "V", "vector marker centre (drawing order)")
        put("fig3", f"OUR ARITHMETIC CE {name}", r["Q_charge"], "mAh", r["CE"], "%", "(Q_ch − x_dis_end)/Q_ch")

    print(f"Fig. 4a  축 잔차 x {f4a['x_res']:.3f} mAh/g (곡선 끝 = 하한 전압 근처 마지막 점)")
    rates = {"100C": {"large_current": ["1500C", "900C", "150C"], "high_voltage": ["900C", "150C"]},
             "25C": {"large_current": ["60C", "1.8C"], "high_voltage": ["60C", "1.8C"]}}
    for pn, e in f4a["ends"].items():
        lc = " · ".join(f"{r} {x:.1f}" for r, x in zip(rates[pn]["large_current"], e["large_current"]))
        hv = " · ".join(f"{r} {x:.1f} ({v:.2f} V)" for r, (x, v) in zip(rates[pn]["high_voltage"], e["high_voltage"]))
        print(f"   {pn}: 대전류형 (LTO · 1 V 하한) {lc} mAh/g | 고전압형 (흑연 · 2.5 V 하한) {hv}")
        for r, x in zip(rates[pn]["large_current"], e["large_current"]):
            put("fig4a", f"large-current type end capacity {pn} {r}", x, "mAh/g", 1.0, "V", "vector; rate label from figure")
        for r, (x, v) in zip(rates[pn]["high_voltage"], e["high_voltage"]):
            put("fig4a", f"high-voltage type end capacity {pn} {r}", x, "mAh/g", v, "V", "vector; rate label from figure")

    for tag, f in (("fig4e", f4e), ("fig4f", f4f)):
        cfg = CFG[tag]
        print(f"Fig. 4{tag[-1]}  {cfg['type']} · 축 잔차 x {f['x_res']:.3f} cycle / y {f['y_res']:.3f} mAh/g")
        d1 = nearest(f["dis"], 1)
        for cyc in cfg["cycles"]:
            dd, cc, ee = nearest(f["dis"], cyc), nearest(f["chg"], cyc), nearest(f["ce"], cyc)
            print(f"   ~{cyc:>4}: 방전 표지 @{dd[0]:.0f} {dd[1]:.1f} · 충전 @{cc[0]:.0f} {cc[1]:.1f} mAh/g · "
                  f"효율 @{ee[0]:.0f} {ee[1]:.1f} % · 첫 방전 대비 {dd[1] / d1[1] * 100:.1f} %")
            put(tag, "OUR ARITHMETIC retention vs first discharge marker", dd[0], "cycle", dd[1] / d1[1] * 100, "%",
                "nearest marker; markers are every ~20 (e) / ~10 (f) cycles")
        for nm in ("dis", "chg", "ce"):
            for x, y in f[nm]:
                put(tag, {"dis": "discharge capacity", "chg": "charge capacity", "ce": "coulombic efficiency"}[nm],
                    x, "cycle", y, "%" if nm == "ce" else "mAh/g", "vector marker centre")

    lib_hi = [p for p in f5["lib"] if p[0] >= 0.8]
    mean_hi = sum(p[1] for p in lib_hi) / len(lib_hi)
    spread = max(p[1] for p in lib_hi) - min(p[1] for p in lib_hi)
    a25 = nearest(f5["assb"], 2.5)
    print(f"Fig. 5b  축 잔차 x {f5['x_res']:.4f} V / y {f5['y_res']:.4f} · Li 이온 셀 ≥0.8 V 평탄 log i ≈ {mean_hi:.3f} "
          f"(≈ {10 ** mean_hi * 1e3:.1f} mA/cm2 · 폭 {spread:.3f} dec · {len(lib_hi)} 점) · "
          f"전고체 @{a25[0]:.2f} V log i ≈ {a25[1]:.3f} (≈ {10 ** a25[1] * 1e3:.0f} mA/cm2)")
    for nm in ("assb", "lib"):
        for x, y in f5[nm]:
            put("fig5b", {"assb": "all-solid-state cell", "lib": "lithium-ion cell"}[nm], x, "V (step)", y,
                "log10 A/cm2", "vector marker centre")
    put("fig5b", "OUR ARITHMETIC Li-ion plateau (>=0.8 V)", 0.8, "V", 10 ** mean_hi * 1e3, "mA/cm2", f"mean of {len(lib_hi)}")

    print("SI 표 · 셀 산수:")
    for k, v, note in table_checks():
        print(f"   {k}: {v:.4f}  ({note})")
        put("tables", "OUR ARITHMETIC " + k, 0, "-", v, "-", note)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        fh.write("# Kato 2016 Nat. Energy 1 16030 - vector-path readout. FIGURE VALUES ARE DIGITIZED (not printed); "
                 "rows marked OUR ARITHMETIC are derived by us (densities in loading rows are our assumptions). "
                 "tools/litdb/kato2016_readout.py\n")
        w = csv.writer(fh)
        w.writerow(["figure", "series", "x", "x_unit", "y", "y_unit", "note"])
        w.writerows(rows)
    print(f"→ {OUT_CSV.relative_to(ROOT)} ({len(rows)} 행)")
    return 0


# ───────────────────────── 자가시험 ─────────────────────────
def selftest():
    import fitz
    fails = []

    def expect(cond, msg):
        print(("  ok   " if cond else "  FAIL ") + msg)
        if not cond:
            fails.append(msg)

    def raises(fn, msg):
        try:
            fn()
        except ReadoutError:
            expect(True, msg)
            return
        expect(False, msg + " (안 멈췄다)")

    tmp = Path(tempfile.mkdtemp())
    pdf = tmp / "synthetic.pdf"
    doc = fitz.open()
    GREEN, OLIVE = (0.17, 0.40, 0.22), (0.58, 0.58, 0.23)

    def tick(sh, p, q):
        sh.draw_line(p, q)
        sh.finish(color=BLACK, width=0.25)

    ast_ops = {}

    def asterisk(pg_, c, s=2.2):
        """별표 = '+' 경로 (끊긴 선 2) + '×' 경로 (끊긴 선 2) — 실물 Fig. 2a/3 과 같은 꼴.
        ⚠ Shape.draw_line 은 연속 선분을 이어 붙여서 (끝점 → 다음 시작점) '+' 가 찌그러진다 — 원시 연산자로 쓴다."""
        x, y = c
        h = pg_.rect.height
        segs = [[((x, y - s), (x, y + s)), ((x - s, y), (x + s, y))],
                [((x - 1.6, y - 1.6), (x + 1.6, y + 1.6)), ((x - 1.6, y + 1.6), (x + 1.6, y - 1.6))]]
        for path in segs:
            ops = [f"q {GREEN[0]} {GREEN[1]} {GREEN[2]} RG 0.5 w"]
            ops += [f"{x1:.3f} {h - y1:.3f} m {x2:.3f} {h - y2:.3f} l" for (x1, y1), (x2, y2) in path]
            ops.append("S Q")
            ast_ops.setdefault(pg_.number, []).extend(ops)

    def flush_ops(pg_):
        xref = pg_.get_contents()[0]
        doc.update_stream(xref, doc.xref_stream(xref) + b"\n" + "\n".join(ast_ops.get(pg_.number, [])).encode())

    def tri(sh, c, rgb=OLIVE):
        x, y = c
        sh.draw_polyline([(x - 2.6, y + 2.3), (x + 2.6, y + 2.3), (x, y - 2.3), (x - 2.6, y + 2.3)])
        sh.finish(color=rgb, fill=rgb, width=0.5, closePath=True)

    # 쪽 1: 합성 Arrhenius — x = 60 + 30·(1000/T − 1) · y = 60 + 25·(−log σ)
    pg = doc.new_page(width=300, height=250)
    X = lambda v: 60 + 30 * (v - 1)
    Y = lambda v: 60 + 25 * (-v)
    sh = pg.new_shape()
    for v in [0, -1, -2, -3, -4, -5]:
        tick(sh, (50, Y(v)), (53.5, Y(v)))
    for v in [1, 2, 3, 4, 5]:
        tick(sh, (X(v), 200), (X(v), 203.5))
    for c in [400, 200, 100, 0, -50]:
        tick(sh, (X(1000 / (c + 273.15)), 40), (X(1000 / (c + 273.15)), 43.5))
    ea_true = 0.24
    m_true = -ea_true / (1000 * LN10 * KB_EV)
    for k in range(6):
        xv = 3.354 + 0.15 * k
        asterisk(pg, (X(xv), Y(-1.6 + m_true * (xv - 3.354))))
    asterisk(pg, (X(3.354) + 0.3, Y(-1.6) + 0.2))           # 겹친 표지 (반복 측정 꼴) → 합쳐져야
    asterisk(pg, (20, 120))                                   # 범례 표지 → 빠져야
    for k in range(8):
        xv = 2.6 + 0.3 * k
        tri(sh, (X(xv), Y(-2.2 + m_true * 1.1 * (xv - 2.6))))
    sh.commit()
    flush_ops(pg)
    cfg = {"clip": (0, 0, 300, 250), "yticks": {"band": (49.5, 50.5), "vals": [0, -1, -2, -3, -4, -5]},
           "xticks": {"band": (199.5, 200.5), "vals": [1, 2, 3, 4, 5]}, "top": {"band": (39.5, 40.5), "C": [400, 200, 100, 0, -50]},
           "legend": [(10, 110, 30, 130)],
           "series": {"LSiPSCl": {"kind": "asterisk", "rgb": GREEN, "n": (6, 6)},
                      "Li9.6P3S12": {"kind": "fill", "rgb": OLIVE, "items": 3, "n": (8, 8)}}}
    # 쪽 2: 합성 Fig. 3 한 패널 — 충전 0 → 0.6 mAh (4.0→4.25 V) · 방전 0.6 → 0.15 mAh (4.1→2.7 V) · 충전 시작 표지 (0, 3.0)
    pg2 = doc.new_page(width=300, height=250)
    QX = lambda q: 50 + 200 * q
    VY = lambda v: 40 + 30 * (4.5 - v)
    s2 = pg2.new_shape()
    for v in [4.5, 4.0, 3.5, 3.0, 2.5]:
        tick(s2, (45, VY(v)), (48.5, VY(v)))
    for q in [0.0, 0.2, 0.4, 0.6, 0.8]:
        tick(s2, (QX(q), 110), (QX(q), 113.5))
    # 충전 시작 표지를 방전 끝 (2.7 V) 보다 **낮게** (2.6 V) 둔다 — '용량 ≈ 0 표지 배제' 규칙이 없으면 CE 가 틀어진다
    seq = [(0.0, 2.6)] + [(0.04 * k, 4.0 + 0.25 * 0.04 * k / 0.6) for k in range(16)] + \
          [(0.6 - 0.05 * k, 4.1 - (1.4 / 9) * k) for k in range(1, 10)]
    for q, v in seq:
        tri(s2, (QX(q), VY(v)))
    s2.commit()
    cfg3 = {"clip": (0, 0, 300, 250), "xticks": {"band": (109.5, 110.5), "vals": [0.0, 0.2, 0.4, 0.6, 0.8]},
            "panels": {"S": {"ybox": (30, 105), "kind": "fill", "rgb": OLIVE, "items": 3, "n": (20, 30)}},
            "ytick_band": (44.5, 45.5), "yvals": [4.5, 4.0, 3.5, 3.0, 2.5], "legend": []}
    # 쪽 3: 합성 Fig. 4a 한 패널 — 남색 실선 3 개 (끝 40 · 80 · 120 mAh/g @ 1 V, 짧은 선분으로 쪼갬) · 자홍 2 개 (끝 30 · 90 @ 2.5 V)
    pg3 = doc.new_page(width=300, height=250)
    CX = lambda q: 50 + 1.5 * q
    VY3 = lambda v: 200 - 30 * (v - 1)
    NAVY, MAG = (0.18, 0.19, 0.57), (0.93, 0.0, 0.55)
    s3 = pg3.new_shape()
    for v in [4, 3, 2]:
        tick(s3, (45, VY3(v)), (48.5, VY3(v)))
    for q in [30, 60, 90, 120]:
        tick(s3, (CX(q), 197), (CX(q), 200))
    for qend in (40.0, 80.0, 120.0):
        prev = (CX(0), VY3(2.5))
        for kk in range(1, 41):
            q = qend * kk / 40
            v = 2.5 - 1.5 * (kk / 40) ** 6
            cur = (CX(q), VY3(v))
            s3.draw_line(prev, cur)
            s3.finish(color=NAVY, width=0.7)
            prev = cur
    for qend in (30.0, 90.0):
        s3.draw_polyline([(CX(0), VY3(4.0)), (CX(qend * 0.8), VY3(3.6)), (CX(qend), VY3(2.5))])
        s3.finish(color=MAG, width=0.7, closePath=False)
    s3.commit()
    cfg4a = {"clip": (0, 0, 300, 250), "ytick_band": (44.5, 45.5), "yvals": [4, 3, 2],
             "xticks": {"bands": [(196.5, 197.5)], "vals": [30, 60, 90, 120]},
             "panels": {"P": (60, 205)}, "navy": NAVY, "magenta": MAG, "cut_navy": 1.06, "cut_mag": (2.40, 2.62),
             "n_ends": {"P": (3, 3)}}
    doc.save(pdf)
    doc.close()

    d = fitz.open(pdf)
    try:
        a = read_fig2a(d[0], cfg)
    except ReadoutError as e:          # 양성 경로가 멈추면 그 자체가 FAIL 이다 (조용히 죽지 않게)
        expect(False, f"(a) 합성 Arrhenius 양성 경로가 멈췄다: {e}")
        print("selftest: FAIL (양성 경로)")
        return 1
    pts = a["series"]["LSiPSCl"]
    m, b, r2 = lin_fit([p[0] for p in pts], [p[1] for p in pts])
    expect(abs(ea_from_slope(m) - ea_true) < 3e-3, f"(a) 합성 Arrhenius (별표) Ea 복원 {ea_from_slope(m):.4f} ≈ {ea_true}")
    expect(len(pts) == 6 and max(p[2] for p in pts) == 4 and min(p[2] for p in pts) == 2,
           "(b) 별표 '+'·'×' 두 경로가 한 점 · 겹친 표지도 합쳐진다 (6 점 · 경로 2–4)")
    expect(a["top_dev"] < 0.01, f"(c) °C 축 자기정합 편차 {a['top_dev']:.4f}")
    raises(lambda: read_fig2a(d[0], dict(cfg, legend=[])), "(d) 범례를 안 빼면 개수 검사에서 멈춘다")
    raises(lambda: read_fig2a(d[0], dict(cfg, yticks={"band": (49.5, 50.5), "vals": [0, -1, -2, -3, -4]})),
           "(e) 눈금 값 개수 불일치 → 멈춤")
    raises(lambda: read_fig2a(d[0], dict(cfg, top={"band": (39.5, 40.5), "C": [300, 200, 100, 0, -50]})),
           "(f) °C 축 라벨 어긋남 → 멈춤")
    raises(lambda: read_fig2a(d[0], dict(cfg, series={"X": {"kind": "fill", "rgb": (0.1, 0.9, 0.1), "items": 3, "n": (8, 8)}})),
           "(g) 표지 색 불일치 → 0 개로 조용히 안 넘어간다")
    raises(lambda: fit_linear([0, 10, 23, 30], [0, 1, 2, 3], 0.02, "비선형"), "(h) 비선형 눈금 → 멈춤")
    f3 = read_fig3(d[1], cfg3)
    r = f3["series"]["S"]
    expect(abs(r["CE"] - (0.6 - 0.15) / 0.6 * 100) < 0.2, f"(i) 합성 첫 사이클 CE 복원 {r['CE']:.2f} ≈ 75.0 %")
    expect(r["order_split_ok"], "(j) 그린 순서 = 충전 → 방전 (쪼갬 일치)")
    raises(lambda: ce_from_branch([(0.0, 3.0)] + [(0.05 * k, 4.0 + 0.01 * k) for k in range(12)]),
           "(k) 방전 가지가 없으면 CE 를 지어내지 않고 멈춘다")
    e4 = read_fig4a(d[2], cfg4a)["ends"]["P"]
    expect(all(abs(a_ - b_) < 0.3 for a_, b_ in zip(e4["large_current"], [40, 80, 120])) and len(e4["large_current"]) == 3,
           f"(r) 합성 Fig. 4a 실선 끝 용량 {[round(v, 1) for v in e4['large_current']]} ≈ [40, 80, 120]")
    expect([round(x) for x, _ in e4["high_voltage"]] == [30, 90], f"(s) 합성 점선 끝 용량 {e4['high_voltage']}")
    raises(lambda: read_fig4a(d[2], dict(cfg4a, cut_navy=0.5)), "(t) 하한 전압을 틀리게 주면 끝점 0 개 → 멈춤")
    d.close()
    # 표 산수 음성 경로: 8f 자리대칭은 S1 은 통과 · S2 는 걸린다 · S2 를 일반 자리로 세면 명목 Li 와 맞는다
    expect(site_ok_8f(TABLE_S1["Li3_xyz"]), "(l) Table S1 Li(3) (x, x, 0) 은 8f 자리대칭을 지킨다")
    expect(not site_ok_8f(TABLE_S2["Li3_xyz"]), "(m) Table S2 Li(3) (0.276, 0.269, 0.128) 는 8f 가 아니다 — 잡힌다")
    expect(abs(li_per_cell(TABLE_S2, 16) - 19.12) < 1e-6 and abs(li_per_cell(TABLE_S2) - 16.32) < 1e-6,
           "(n) S2 Li 수: 8f 로 16.32 · 16 중 자리로 19.12 (명목 19.2)")
    expect(abs(li_per_cell(TABLE_S1) - 22.836) < 1e-6, "(o) S1 Li 수 22.836 /cell 재현")
    ea2 = R_GAS * math.log(14.2 / 1.94) / (1 / 243.15 - 1 / 298.15)
    expect(abs(ea2 - 21.9) < 0.2, f"(p) 두 점 Arrhenius: R1 ASSB {ea2:.2f} ≈ 논문 21.9 kJ/mol")
    expect(abs(ea_from_slope(-1.2) * EV_TO_KJMOL - 22.98) < 0.05, "(q) 기울기 −1.2 ↔ 22.98 kJ/mol 환산")
    print("selftest:", "PASS" if not fails else f"FAIL {len(fails)}")
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", help="본문 PDF (litdb/inbox/126._High-power_all-solid-state_batteries_using_sulfide_superionic_conductors.pdf)")
    ap.add_argument("--selftest", action="store_true", help="합성 PDF 로 양성 + 음성 경로")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.pdf:
        ap.error("--pdf 가 필요하다 (또는 --selftest)")
    if not os.path.exists(args.pdf):
        ap.error(f"PDF 없음: {args.pdf}")
    try:
        return run(args.pdf)
    except ReadoutError as e:
        print(f"⛔ 판독 중단: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
