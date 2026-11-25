#!/usr/bin/env python3
"""kamaya2011_readout.py — Kamaya 2011 *Nat. Mater.* 10, 682 (LGPS) 그림의 **벡터 경로 판독** + SI 표 산수 검산.

digest: litdb/papers/kamaya2011_lgps_lithium_superionic_conductor.md
출력:   litdb/figures/kamaya2011_lgps_lithium_superionic_conductor/digitized.csv

무엇을 읽나 (전부 PDF 안의 벡터 좌표 — 픽셀 판독이 아니다)
  Fig. 1a  Arrhenius 측정점 28 개 (빨간 채움 원) → 1000/T · log σ · Ea 재적합 · 본문 수치 대조
  Fig. 1b  CV 경로 (빨간 선 921 점) → 정방향 / 역방향 전류 · 1 mV/s 로 적분한 전하
  Fig. 3   LGPS 선과 유기 전해질 (1 M LiPF6 EC–PC) 선 → 교차점 온도 · 27 °C 값
  Fig. 4   효율 삽입도 8 점 + 1·8 번째 사이클 충방전 끝 용량
  SI Table S1 (PDF 텍스트를 손으로 옮긴 상수) → 단위셀 Li 수 · Ge/P 합 · V = a²c · S = Rwp/Re · U_eq

축 보정은 눈금선(tick) 좌표에 대한 **최소제곱 1 차식** 이고, 잔차가 문턱을 넘으면 멈춘다.
Fig. 1a · 3 은 위쪽 °C 축 눈금을 아래 1000/T 축으로 되돌려 **같은 자리인지** 따로 검사한다 (눈금 분류가
틀리면 여기서 걸린다).

⛔ 이 도구가 못 하는 것
  · 래스터 그림 (Fig. 2 결정구조) · 삽입 Nyquist 곡선 (Fig. 1a 안 작은 그림) 은 안 읽는다.
  · 판독값은 **그림이 그린 값**이다 — 저자 원자료가 아니다. digest 에서는 `figure-read ≈` 로만 쓴다.
  · CV 적분 전하는 '그림 경로 × 논문의 주사 속도 1 mV/s' 일 뿐, 그 전류의 **기원(SE 산화인지 아닌지)을 가르지 않는다**.
  · Fig. 4 빨간 경로 (2–7 번째 사이클) 는 사이클별로 나누지 않고 끝점의 범위만 낸다.
  · SI 표 값은 PDF 텍스트에서 옮긴 상수다 — PDF 가 바뀌면 이 상수도 손으로 다시 본다.

usage
  ~/.venvs/litdb/bin/python3 tools/litdb/kamaya2011_readout.py --pdf "litdb/inbox/125._A_lithium_superionic_conductor.pdf"
  ~/.venvs/litdb/bin/python3 tools/litdb/kamaya2011_readout.py --selftest     # 합성 PDF 로 양성 + 음성 경로
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
SLUG = "kamaya2011_lgps_lithium_superionic_conductor"
OUT_CSV = ROOT / "litdb" / "figures" / SLUG / "digitized.csv"

KB_EV = 8.617333262e-5        # eV/K
EV_TO_KJMOL = 96.485332       # kJ/mol per eV
LN10 = math.log(10.0)

RED = (0.93, 0.12, 0.14)
BLACK = (0.14, 0.12, 0.13)
BLUE = (0.2, 0.27, 0.61)
GREEN = (0.08, 0.6, 0.28)

# 페이지 번호는 0 부터 · clip 은 pt (PDF 좌표, y 아래로 증가)
CFG = {
    "fig1a": {"page": 1, "clip": (100, 75, 365, 262), "tick_items": 20,
              "y_vals": [-6, -5, -4, -3, -2, -1], "x_vals": [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0],
              "top_C": [100, 30, 0, -30, -70, -100], "marker_rgb": RED, "n_markers": (20, 40)},
    "fig1b": {"page": 1, "clip": (375, 55, 560, 275), "tick_items": 10,
              "y_vals": [0, -1, -2, -3], "x_vals": [0, 1, 2, 3, 4, 5], "scan_V_s": 1e-3},
    "fig3": {"page": 2, "clip": (41, 48, 563, 317), "tick_items": 21,
             "y_vals": [0, -1, -2, -3, -4, -5, -6, -7], "x_vals": [1, 2, 3, 4, 5, 6],
             "top_C": [800, 500, 200, 100, 27, -30, -100]},
    "fig4": {"page": 3, "clip": (33, 46, 555, 300), "main_items": 12, "inset_items": 7, "tick_max": 12.0,
             "x_vals": [0, 20, 40, 60, 80, 100, 120, 140], "y_vals": [2.0, 2.5, 3.0, 3.5],
             "ix_vals": [2, 4, 6, 8], "iy_vals": [90, 95, 100]},
}

# SI Table S1 (SI p.3, 27 °C 중성자 Rietveld) — PDF 텍스트에서 옮긴 값
TABLE_S1 = {
    "occ": {"Li(1) 16h": (16, 0.691), "Li(2) 4d": (4, 1.000), "Li(3) 8f": (8, 0.643),
            "Ge(1) 4d": (4, 0.515), "P(1) 4d": (4, 0.485), "Ge(2) 2b": (2, 0.00), "P(2) 2b": (2, 1.00)},
    "U": {"Li(1)": (0.289, 0.093, 0.327), "Li(2)": (0.061, 0.072, 0.008),
          "Li(3)": (0.110, 0.110, 0.313),   # ⚠ 표는 U22 = U11(Li(2)) 라고 적었다 — 8f (x,x,0) 자리대칭이면 자기 U11 (우리 판단)
          "Ge/P(1)": (0.0542, 0.0336, 0.0331), "Ge/P(2)": (0.0373, 0.0373, 0.045),
          "S(1)": (0.079, 0.037, 0.048), "S(2)": (0.071, 0.060, 0.027), "S(3)": (0.057, 0.028, 0.043)},
    "a": 8.69407, "c": 12.5994, "V_printed": 952.349, "Rwp": 4.25, "Re": 1.41, "chi2": 9.08,
}
SYNC = {"a": 8.71771, "c": 12.63452, "T_C": -173}   # 본문 p.682 · Methods: Debye–Scherrer −173 °C


class ReadoutError(RuntimeError):
    pass


# ───────────────────────── 기하 도우미 ─────────────────────────
def _close(c, ref, tol=0.02):
    return c is not None and len(c) == 3 and all(abs(a - b) <= tol for a, b in zip(c, ref))


def _pts(d):
    out = []
    for it in d["items"]:
        for q in it[1:]:
            if hasattr(q, "x"):
                out.append((q.x, q.y))
    ded = [out[0]] if out else []
    for p in out[1:]:
        if p != ded[-1]:
            ded.append(p)
    return ded


def _in_clip(page, clip):
    import fitz
    r = fitz.Rect(clip)
    return [d for d in page.get_drawings() if d["rect"].intersects(r)]


def tick_path(draws, n_items):
    """눈금선 경로 = 검은 선 · 'l' 항목만 정확히 n 개. 없거나 둘 이상이면 멈춘다."""
    c = [d for d in draws if _close(d.get("color"), BLACK) and len(d["items"]) == n_items
         and all(it[0] == "l" for it in d["items"])]
    if len(c) != 1:
        raise ReadoutError(f"눈금선 경로 ({n_items} 선) 를 하나로 못 골랐다: {len(c)} 개")
    return c[0]


def split_ticks(path, max_len=8.0):
    """짧은 수평선 → y 눈금 (y 좌표) · 짧은 수직선 → x 눈금 ((x, y) 중점)."""
    ys, xs = [], []
    for it in path["items"]:
        p, q = it[1], it[2]
        dx, dy = abs(p.x - q.x), abs(p.y - q.y)
        if dy < 0.05 and dx <= max_len:
            ys.append((p.y + q.y) / 2)
        elif dx < 0.05 and dy <= max_len:
            xs.append(((p.x + q.x) / 2, (p.y + q.y) / 2))
    return ys, xs


def fit_linear(pix, vals, tol, name):
    """최소제곱 val = m·pix + b. 잔차 최대가 tol (값 단위) 을 넘거나 개수가 안 맞으면 멈춘다."""
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


def axis(ticks, vals, tol, name, ascending_pix=True):
    t = sorted(ticks) if ascending_pix else sorted(ticks, reverse=True)
    return fit_linear(t, vals, tol, name)


def top_axis_check(top_x, top_C, mx, name, tol=0.03):
    """위쪽 °C 눈금을 아래 1000/T 축으로 옮겼을 때 1000/(T+273.15) 와 같은 자리인가 → 최대 편차."""
    if len(top_x) != len(top_C):
        raise ReadoutError(f"{name}: 위 눈금 {len(top_x)} 개 ↔ °C 값 {len(top_C)} 개")
    dev = max(abs((mx[0] * x + mx[1]) - 1000.0 / (c + 273.15)) for x, c in zip(sorted(top_x), top_C))
    return dev, dev <= tol


def markers(draws, rgb, n_range, fill_only=False, max_w=9.0):
    out = []
    for d in draws:
        if len(d["items"]) != 4 or d["rect"].width > max_w:
            continue
        if not _close(d.get("fill"), rgb):
            continue
        if not fill_only and not _close(d.get("color"), rgb):
            continue
        r = d["rect"]
        out.append(((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2))
    lo, hi = n_range
    if not (lo <= len(out) <= hi):
        raise ReadoutError(f"표지 {len(out)} 개 — 기대 {lo}–{hi} (색 {rgb})")
    return out


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
    """log10 σ vs 1000/T 기울기 → Ea (eV). σ 형식 (σT 아님) — 논문 Fig. 1a 와 같은 형식."""
    return -m_per_1000K * 1000.0 * LN10 * KB_EV


def interp_branch(branch, v):
    """V 가 단조가 아닐 수 있는 가지에서 v 를 처음 가로지르는 선분으로 선형보간. 없으면 None."""
    for (v1, i1), (v2, i2) in zip(branch, branch[1:]):
        if (v1 - v) * (v2 - v) <= 0 and v1 != v2:
            return i1 + (i2 - i1) * (v - v1) / (v2 - v1)
    return None


def integrate(branch, v_lo, v_hi, scan):
    """∫ I dV / 주사속도 → 전하 (C). I 는 A."""
    q = 0.0
    for (v1, i1), (v2, i2) in zip(branch, branch[1:]):
        a, b = max(min(v1, v2), v_lo), min(max(v1, v2), v_hi)
        if b <= a:
            continue
        frac = (b - a) / abs(v2 - v1)
        q += 0.5 * (i1 + i2) * frac * abs(v2 - v1) / scan
    return q


def charge_by_sign(pts, scan):
    """경로 전체 (주사 순서) 를 시간으로 적분해 양극 · 음극 전하 (C) 를 따로 낸다 — 0 을 지나는 선분은 교점에서 쪼갠다.
    삼각파 주사라 dt = |ΔV| / 주사속도."""
    qa = qc = 0.0
    for (v1, i1), (v2, i2) in zip(pts, pts[1:]):
        dt = abs(v2 - v1) / scan
        if dt == 0:
            continue
        if i1 * i2 < 0:                       # 부호가 바뀌는 선분 — 교점에서 두 삼각형으로
            f = i1 / (i1 - i2)
            parts = [(0.5 * i1, f * dt), (0.5 * i2, (1 - f) * dt)]
        else:
            parts = [(0.5 * (i1 + i2), dt)]
        for i_avg, t in parts:
            if i_avg >= 0:
                qa += i_avg * t
            else:
                qc += -i_avg * t
    return qa, qc


def crossings(p, q):
    """두 꺾은선 (데이터 좌표) 의 교점들."""
    out = []
    for (x1, y1), (x2, y2) in zip(p, p[1:]):
        for (x3, y3), (x4, y4) in zip(q, q[1:]):
            den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if den == 0:
                continue
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
            u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den
            if 0 <= t <= 1 and 0 <= u <= 1:
                out.append((x1 + t * (x2 - x1), y1 + t * (y2 - y1)))
    return out


# ───────────────────────── 그림별 판독 ─────────────────────────
def read_arrhenius(page, cfg):
    dr = _in_clip(page, cfg["clip"])
    ys, xs = split_ticks(tick_path(dr, cfg["tick_items"]))
    mid = sum(y for _, y in xs) / len(xs)
    bottom = [x for x, y in xs if y > mid]
    top = [x for x, y in xs if y <= mid]
    my = axis(ys, cfg["y_vals"], 0.02, "log σ 축", ascending_pix=False)   # y 큰 쪽 = 작은 값
    mx = axis(bottom, cfg["x_vals"], 0.02, "1000/T 축")
    dev, ok = top_axis_check(top, cfg["top_C"], mx, "°C 축")
    if not ok:
        raise ReadoutError(f"위 °C 축이 아래 1000/T 축과 안 맞는다 (최대 편차 {dev:.3f})")
    pts = [((mx[0] * x + mx[1]), (my[0] * y + my[1])) for x, y in markers(dr, cfg["marker_rgb"], cfg["n_markers"])]
    pts.sort()
    return {"points": pts, "top_dev": dev, "x_res": mx[2], "y_res": my[2]}


def read_cv(page, cfg):
    dr = _in_clip(page, cfg["clip"])
    ys, xs = split_ticks(tick_path(dr, cfg["tick_items"]))
    my = axis(ys, cfg["y_vals"], 0.01, "전류 축", ascending_pix=True)    # y 작은 쪽 = 0 mA
    mx = axis([x for x, _ in xs], cfg["x_vals"], 0.01, "전압 축")
    red = [d for d in dr if _close(d.get("color"), RED) and len(d["items"]) > 100]
    if len(red) != 1:
        raise ReadoutError(f"CV 경로를 하나로 못 골랐다: {len(red)} 개")
    pts = [(mx[0] * x + mx[1], (my[0] * y + my[1]) * 1e-3) for x, y in _pts(red[0])]   # (V, A)
    i_lo = min(range(len(pts)), key=lambda k: pts[k][0])
    i_hi = max(range(len(pts)), key=lambda k: pts[k][0])
    if not i_lo < i_hi:
        raise ReadoutError("CV 경로 순서가 예상과 다르다 (최저 전위 → 최고 전위)")
    fwd, rev = pts[i_lo:i_hi + 1], pts[i_hi:]
    pk = max(fwd, key=lambda r: r[1])
    s = cfg["scan_V_s"]
    qa, qc = charge_by_sign(pts, s)
    return {"points": pts, "fwd": fwd, "rev": rev, "strip_peak": pk, "Q_anodic_total": qa, "Q_cathodic_total": qc,
            "Q_fwd_0p6_5": integrate(fwd, 0.6, 5.0, s), "Q_fwd_2p14_5": integrate(fwd, 2.14, 5.0, s),
            "Q_strip_to_0p6": integrate([r for r in fwd if r[1] > 0 and r[0] <= 0.6], -1, 0.6, s),
            "full_scale_A": min(r[1] for r in pts), "x_res": mx[2], "y_res": my[2]}


def read_fig3(page, cfg):
    dr = _in_clip(page, cfg["clip"])
    ys, xs = split_ticks(tick_path(dr, cfg["tick_items"]))
    mid = sum(y for _, y in xs) / len(xs)
    my = axis(ys, cfg["y_vals"], 0.02, "log σ 축", ascending_pix=True)    # y 작은 쪽 = 0
    mx = axis([x for x, y in xs if y > mid], cfg["x_vals"], 0.02, "1000/T 축")
    dev, ok = top_axis_check([x for x, y in xs if y <= mid], cfg["top_C"], mx, "°C 축")
    if not ok:
        raise ReadoutError(f"Fig. 3 위 °C 축이 아래 축과 안 맞는다 (최대 편차 {dev:.3f})")

    def line(rgb, n):
        c = [d for d in dr if _close(d.get("color"), rgb) and len(d["items"]) == n]
        if not c:
            raise ReadoutError(f"Fig. 3 선 (색 {rgb}, {n} 선분) 없음")
        return [(mx[0] * x + mx[1], my[0] * y + my[1]) for x, y in _pts(c[0])]

    lgps, org = line(RED, 12), line(GREEN, 11)
    x27 = 1000.0 / 300.15
    return {"lgps": lgps, "organic": org, "cross": crossings(lgps, org), "top_dev": dev,
            "lgps_27C": interp_branch(sorted(lgps), x27)}


def read_fig4(page, cfg):
    dr = _in_clip(page, cfg["clip"])
    tm = cfg.get("tick_max", 8.0)
    ys, xs = split_ticks(tick_path(dr, cfg["main_items"]), max_len=tm)
    mx = axis([x for x, _ in xs], cfg["x_vals"], 0.5, "용량 축")
    my = axis(ys, cfg["y_vals"], 0.01, "전압 축", ascending_pix=False)
    iys, ixs = split_ticks(tick_path(dr, cfg["inset_items"]), max_len=tm)
    imx = axis([x for x, _ in ixs], cfg["ix_vals"], 0.05, "사이클 축")
    imy = axis(iys, cfg["iy_vals"], 0.05, "효율 축", ascending_pix=False)
    ce = sorted((imx[0] * x + imx[1], imy[0] * y + imy[1]) for x, y in markers(dr, BLACK, (8, 8), fill_only=True))

    def curve(rgb, n_min):
        c = [d for d in dr if _close(d.get("color"), rgb) and len(d["items"]) >= n_min]
        if not c:
            raise ReadoutError(f"Fig. 4 곡선 (색 {rgb}) 없음")
        big = max(c, key=lambda d: len(d["items"]))
        return [(mx[0] * x + mx[1], my[0] * y + my[1]) for x, y in _pts(big)]

    out = {"ce": ce}
    for name, rgb in (("first", BLACK), ("eighth", BLUE), ("cycles2to7", RED)):
        pts = curve(rgb, 300)
        ch = [q for q, v in pts if v >= 3.55]
        dis = [q for q, v in pts if v <= 2.0]
        out[name] = {"Q_ch_max": max(ch), "Q_dis_max": max(dis),
                     "Q_dis_min_end": min(q for q, v in pts if v <= 1.95) if any(v <= 1.95 for _, v in pts) else None}
    return out


def table_checks():
    occ, rows = TABLE_S1["occ"], []
    li = sum(m * g for k, (m, g) in occ.items() if k.startswith("Li"))
    ge = sum(m * g for k, (m, g) in occ.items() if k.startswith("Ge"))
    p = sum(m * g for k, (m, g) in occ.items() if k.startswith("P"))
    v = TABLE_S1["a"] ** 2 * TABLE_S1["c"]
    s = TABLE_S1["Rwp"] / TABLE_S1["Re"]
    vs = SYNC["a"] ** 2 * SYNC["c"]
    rows += [("Li per cell", li, "printed 20.200"), ("Ge per cell", ge, "stoichiometric 2"),
             ("P per cell", p, "stoichiometric 4"), ("P/Ge from Table S1", p / ge, "stoichiometric 2"),
             ("V = a^2 c (neutron 27 C)", v, f"printed {TABLE_S1['V_printed']}"),
             ("S = Rwp/Re", s, "-"), ("S^2", s * s, f"printed chi2 {TABLE_S1['chi2']}"),
             ("V = a^2 c (synchrotron -173 C)", vs, "main text a, c"),
             ("V_sync / V_neutron - 1 (%)", (vs / v - 1) * 100, "colder cell is larger: opposite to thermal expansion")]
    for k, u in TABLE_S1["U"].items():
        rows.append((f"U_eq {k} (A^2)", sum(u) / 3, "mean of U11 U22 U33"))
    return rows, {"li": li, "ge": ge, "p": p}


def ratio_claim_ok(claim_a, claim_b, ge, p, tol=0.05):
    """본문 'Ge/P ratio is then a:b' 를 표에서 재현하나 → (Ge, P) 순서로 대조."""
    return abs(claim_a - ge) <= tol and abs(claim_b - p) <= tol


def _hop_line(ea_ev, T):
    src = ROOT / "tools" / "sei" / "collect_neb.py"
    spec = importlib.util.spec_from_file_location("_collect_neb_hop", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    h = mod.hop_check(ea_ev, T)
    return h["line"] if h else None


# ───────────────────────── 실행 ─────────────────────────
def run(pdf):
    import fitz
    doc = fitz.open(pdf)
    a = read_arrhenius(doc[CFG["fig1a"]["page"]], CFG["fig1a"])
    cv = read_cv(doc[CFG["fig1b"]["page"]], CFG["fig1b"])
    f3 = read_fig3(doc[CFG["fig3"]["page"]], CFG["fig3"])
    f4 = read_fig4(doc[CFG["fig4"]["page"]], CFG["fig4"])
    doc.close()
    rows = []

    def put(fig, series, x, xu, y, yu, note=""):
        rows.append((fig, series, round(x, 5), xu, round(y, 6), yu, note))

    xs, ys = [p[0] for p in a["points"]], [p[1] for p in a["points"]]
    m, b, r2 = lin_fit(xs, ys)
    ea = ea_from_slope(m)
    print(f"Fig. 1a  측정점 {len(xs)} 개 · 축 잔차 x {a['x_res']:.4f} / y {a['y_res']:.4f} · °C 축 편차 {a['top_dev']:.4f}")
    print(f"   재적합 기울기 {m:.4f} /(1000/T) · R² {r2:.5f} → Ea ≈ {ea:.4f} eV = {ea * EV_TO_KJMOL:.2f} kJ/mol (논문 24 kJ/mol)")
    for x, y in a["points"]:
        put("fig1a", "LGPS total sigma (red markers)", x, "1000/T K^-1", y, "log10 S/cm",
            f"T = {1000 / x - 273.15:.1f} C · vector marker centre")
    for tC in (27, -30, -45):
        x = 1000.0 / (tC + 273.15)
        near = [p for p in a["points"] if abs(p[0] - x) < 0.03]
        fit_s = 10 ** (m * x + b) * 1e3
        msg = f"   {tC:>4} °C: 직선 {fit_s:.2f} mS/cm"
        if near:
            msg += f" · 그 온도 측정점 {', '.join(f'{10 ** y * 1e3:.2f}' for _, y in near)} mS/cm"
        print(msg)
    print(f"   최저 온도 측정점 ≈ {1000 / max(xs) - 273.15:.1f} °C · 최고 ≈ {1000 / min(xs) - 273.15:.1f} °C (본문 −110 ~ 110 °C)")
    print("   " + str(_hop_line(24.0 / EV_TO_KJMOL, 300.0)))

    print(f"Fig. 1b  CV {len(cv['points'])} 점 · 축 잔차 {cv['x_res']:.4f} V / {cv['y_res']:.4f} mA · 화면 최대 전류 {cv['full_scale_A'] * 1e3:.2f} mA")
    print(f"   Li 탈리 봉우리 {cv['strip_peak'][1] * 1e6:.0f} µA @ {cv['strip_peak'][0]:.2f} V")
    for v in (1.0, 2.0, 2.14, 2.5, 3.0, 4.0, 4.25, 4.5):
        f, r = interp_branch(cv["fwd"], v), interp_branch(cv["rev"], v)
        print(f"   {v:4.2f} V: 정방향 {f * 1e6:6.1f} µA · 역방향 {r * 1e6:6.1f} µA")
        put("fig1b", "CV forward (anodic) branch", v, "V vs Li/Li+", f * 1e6, "uA", "linear interp on vector path")
        put("fig1b", "CV reverse branch", v, "V vs Li/Li+", r * 1e6, "uA", "linear interp on vector path")
    print(f"   정방향 전하 (1 mV/s): 0.6→5 V {cv['Q_fwd_0p6_5']:.3f} C · 2.14→5 V {cv['Q_fwd_2p14_5']:.3f} C · "
          f"Li 탈리 (I>0, ≤0.6 V) {cv['Q_strip_to_0p6']:.3f} C")
    put("fig1b", "OUR ARITHMETIC charge fwd 0.6-5 V", 5.0, "V", cv["Q_fwd_0p6_5"], "C", "int I dV / (1 mV/s)")
    put("fig1b", "OUR ARITHMETIC charge fwd 2.14-5 V", 5.0, "V", cv["Q_fwd_2p14_5"], "C", "int I dV / (1 mV/s)")
    put("fig1b", "OUR ARITHMETIC Li stripping charge", 0.6, "V", cv["Q_strip_to_0p6"], "C", "I>0 part up to 0.6 V")
    print(f"   경로 전체 (0 → −0.5 → 5 → 0 V) 전하: 음극 {cv['Q_cathodic_total']:.3f} C · 양극 {cv['Q_anodic_total']:.3f} C · "
          f"Li 탈리 / 음극 = {cv['Q_strip_to_0p6'] / cv['Q_cathodic_total'] * 100:.1f} %")
    put("fig1b", "OUR ARITHMETIC cathodic charge (whole plotted loop)", 0, "-", cv["Q_cathodic_total"], "C",
        "sign-split time integral; plotted loop starts and ends at 0 V")
    put("fig1b", "OUR ARITHMETIC anodic charge (whole plotted loop)", 0, "-", cv["Q_anodic_total"], "C",
        "sign-split time integral")
    for v, i in cv["points"]:
        put("fig1b", "CV full vector path (A)", v, "V vs Li/Li+", i, "A", "path order = scan order")

    print(f"Fig. 3   °C 축 편차 {f3['top_dev']:.4f} · LGPS 27 °C ≈ log σ {f3['lgps_27C']:.3f}")
    for x, y in f3["cross"]:
        print(f"   LGPS × 유기 전해질 교차: 1000/T {x:.3f} → {1000 / x - 273.15:.1f} °C · log σ {y:.3f}")
        put("fig3", "OUR ARITHMETIC LGPS x organic crossing", x, "1000/T K^-1", y, "log10 S/cm",
            f"T = {1000 / x - 273.15:.1f} C")
    for name in ("lgps", "organic"):
        for x, y in f3[name]:
            put("fig3", f"{name} polyline vertex", x, "1000/T K^-1", y, "log10 S/cm", "")

    print("Fig. 4   효율 삽입도: " + " · ".join(f"{c:.2f}:{e:.1f} %" for c, e in f4["ce"]))
    for c, e in f4["ce"]:
        put("fig4", "coulombic efficiency (inset markers)", c, "cycle", e, "%", "vector marker centre")
    for name in ("first", "eighth", "cycles2to7"):
        d = f4[name]
        print(f"   {name}: 충전 끝 ≈ {d['Q_ch_max']:.1f} · 방전 끝 ≈ {d['Q_dis_max']:.1f} mAh/g"
              + (f" (≤1.95 V 최소 {d['Q_dis_min_end']:.1f})" if d['Q_dis_min_end'] else ""))
        put("fig4", f"{name} charge end (V>=3.55)", d["Q_ch_max"], "mAh/g", 3.6, "V", "max capacity on the path")
        put("fig4", f"{name} discharge end (V<=2.0)", d["Q_dis_max"], "mAh/g", 1.9, "V", "max capacity on the path")

    trows, t = table_checks()
    print("SI Table S1 산수:")
    for k, v, note in trows:
        print(f"   {k}: {v:.4f}  ({note})")
        put("tableS1", "OUR ARITHMETIC " + k, 0, "-", v, "-", note)
    ok = ratio_claim_ok(4.06, 1.94, t["ge"], t["p"])
    print(f"   본문 'Ge/P ratio is then 4.06:1.94' 재현? {ok} (표 합: Ge {t['ge']:.2f} · P {t['p']:.2f})")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        fh.write("# Kamaya 2011 Nat. Mater. 10 682 - vector-path readout. FIGURE VALUES ARE DIGITIZED (not printed); "
                 "rows marked OUR ARITHMETIC are derived by us. tools/litdb/kamaya2011_readout.py\n")
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

    def append_ticks(pg, segs):
        """끊긴 선분 여러 개 = **한 경로** (실물 눈금 경로와 같은 꼴). Shape 는 선분을 이어 버려서 원시 연산자로 쓴다."""
        h = pg.rect.height
        ops = [f"q {BLACK[0]} {BLACK[1]} {BLACK[2]} RG 0.5 w"]
        ops += [f"{x1:.3f} {h - y1:.3f} m {x2:.3f} {h - y2:.3f} l" for (x1, y1), (x2, y2) in segs]
        ops.append("S Q")
        xref = pg.get_contents()[0]
        doc.update_stream(xref, doc.xref_stream(xref) + b"\n" + "\n".join(ops).encode())

    # 합성 Arrhenius: x = 50 + 40·(1000/T − 2.5) pt · y = 250 − 30·(log σ + 6) pt
    page = doc.new_page(width=400, height=300)
    X = lambda v: 50 + 40 * (v - 2.5)
    Y = lambda v: 250 - 30 * (v + 6)
    sh = page.new_shape()
    ea_true = 0.30                                    # eV
    m_true = -ea_true / (1000 * LN10 * KB_EV)
    for k in range(14):
        xv = 2.6 + 0.22 * k
        yv = -1.0 + m_true * (xv - 2.6)
        sh.draw_circle((X(xv), Y(yv)), 2.0)
        sh.finish(color=RED, fill=RED, width=0.3)
    sh.commit()
    segs = [((50, Y(v)), (54, Y(v))) for v in [-6, -5, -4, -3, -2, -1]]
    segs += [((X(v), 250), (X(v), 246)) for v in [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]]
    segs += [((X(1000 / (c + 273.15)), 40), (X(1000 / (c + 273.15)), 44)) for c in [100, 30, 0, -30, -70, -100]]
    append_ticks(page, segs)
    # 합성 CV (두 번째 쪽): 0 V → −0.5 → 0.3 V → 0.6–5 V 일정 +30 µA → 역방향 +10 µA
    pg2 = doc.new_page(width=400, height=300)
    VX = lambda v: 100 + 20 * v
    IY = lambda i_mA: 50 - 40 * i_mA
    path = [(0, -0.5), (-0.5, -2.0), (0.3, 0.2)] + [(0.6 + 0.0044 * k, 0.03) for k in range(1001)] + \
           [(4.9 - 0.049 * k, 0.01) for k in range(101)]
    s2 = pg2.new_shape()
    s2.draw_polyline([(VX(v), IY(i)) for v, i in path])
    s2.finish(color=RED, width=0.6, closePath=False)
    s2.commit()
    append_ticks(pg2, [((90, IY(v)), (95, IY(v))) for v in [0, -1, -2, -3]] +
                 [((VX(v), 200), (VX(v), 196)) for v in [0, 1, 2, 3, 4, 5]])
    doc.save(pdf)
    doc.close()

    d = fitz.open(pdf)
    cfg_a = {"clip": (0, 0, 400, 300), "tick_items": 20, "y_vals": [-6, -5, -4, -3, -2, -1],
             "x_vals": [2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0], "top_C": [100, 30, 0, -30, -70, -100],
             "marker_rgb": RED, "n_markers": (14, 14)}
    a = read_arrhenius(d[0], cfg_a)
    m, b, r2 = lin_fit([p[0] for p in a["points"]], [p[1] for p in a["points"]])
    expect(abs(ea_from_slope(m) - ea_true) < 2e-3, f"(a) 합성 Arrhenius Ea 복원 {ea_from_slope(m):.4f} ≈ {ea_true}")
    expect(a["top_dev"] < 0.01, f"(b) °C 축 자기정합 편차 {a['top_dev']:.4f}")
    # 음성 ① 눈금 값 개수가 틀리면 멈춘다
    raises(lambda: read_arrhenius(d[0], dict(cfg_a, y_vals=[-6, -5, -4, -3, -2])), "(c) 눈금 값 개수 불일치 → 멈춤")
    # 음성 ② 위 °C 축 라벨을 한 칸 밀면 자기정합 검사가 잡는다
    raises(lambda: read_arrhenius(d[0], dict(cfg_a, top_C=[90, 30, 0, -30, -70, -100])), "(d) °C 축 라벨 어긋남 → 멈춤")
    # 음성 ③ 색이 안 맞는 표지만 찾으면 조용히 0 개로 넘어가지 않는다
    raises(lambda: read_arrhenius(d[0], dict(cfg_a, marker_rgb=GREEN)), "(e) 표지 색 불일치 → 0 개로 안 넘어감")
    # 음성 ④ 비선형 눈금 (한 눈금 3 pt 밀림) 은 축 보정에서 멈춘다
    raises(lambda: fit_linear([0, 10, 23, 30], [0, 1, 2, 3], 0.02, "비선형"), "(f) 비선형 눈금 → 멈춤")
    cv = read_cv(d[1], {"clip": (0, 0, 400, 300), "tick_items": 10, "y_vals": [0, -1, -2, -3],
                        "x_vals": [0, 1, 2, 3, 4, 5], "scan_V_s": 1e-3})
    q_true = 30e-6 * (5.0 - 0.6) / 1e-3
    expect(abs(cv["Q_fwd_0p6_5"] - q_true) / q_true < 0.01, f"(g) 합성 CV 정방향 전하 {cv['Q_fwd_0p6_5']:.4f} ≈ {q_true:.4f} C")
    expect(abs(interp_branch(cv["rev"], 3.0) - 10e-6) < 0.5e-6, "(h) 역방향 가지 전류 10 µA 복원")
    # 음극 전하 정답: (0,−0.5)→(−0.5,−2.0) 사다리꼴 0.625 C + 0 을 지나는 선분의 음극 삼각형 0.5·2.0 mA·(0.8·2.0/2.2 V)/1 mV/s
    qc_true = 0.625 + 0.5 * 2.0e-3 * (0.8 * 2.0 / 2.2) / 1e-3
    expect(abs(cv["Q_cathodic_total"] - qc_true) / qc_true < 0.002,
           f"(m) 부호 분리 음극 전하 {cv['Q_cathodic_total']:.4f} ≈ {qc_true:.4f} C (0 교차 선분을 쪼갠다)")
    d.close()
    # 표 산수: 맞는 주장은 통과 · 틀린 주장 (본문 4.06:1.94) 은 잡힌다
    _, t = table_checks()
    expect(abs(t["li"] - 20.200) < 1e-9, f"(i) 단위셀 Li 20.200 재현 ({t['li']:.3f})")
    expect(ratio_claim_ok(2.06, 3.94, t["ge"], t["p"]), "(j) 'Ge 2.06 : P 3.94' 는 통과")
    expect(not ratio_claim_ok(4.06, 1.94, t["ge"], t["p"]), "(k) 본문 'Ge/P 4.06:1.94' 는 재현 안 됨으로 잡힌다")
    expect(abs(ea_from_slope(-1.2534) * EV_TO_KJMOL - 24.0) < 0.05, "(l) 기울기 −1.2534 ↔ 24 kJ/mol 환산")
    print("selftest:", "PASS" if not fails else f"FAIL {len(fails)}")
    return 0 if not fails else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", help="본문 PDF (litdb/inbox/125._A_lithium_superionic_conductor.pdf)")
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
