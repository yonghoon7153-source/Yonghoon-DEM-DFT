#!/usr/bin/env python3
"""sharma2023_verify.py — `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` 카드의 수치 재현.

무엇을 하나 (카드 §3·§6 의 derived(ours) · digitized 값이 전부 여기서 나온다):
  (A) derived(ours) — 논문이 **인쇄한** C_ij 6개(Fig 5 캡션, p. 5)만 입력으로
      · 논문 자신의 Eq. (10) 육방 VRH 를 다시 풀어 E 140.16 · ν 0.253 재현 확인
      · C14 를 넣은 전체 삼방정(−3m) 6×6 VRH 와 비교 (논문 식은 C14 를 안 쓴다)
      · 방향별 영률 E(l) = 1/S'_3333 (c축 · 기저면 · 전 방향 최소/최대)
      · Delafargue–Ulm 기저면 압입탄성률 ↔ Fig 5b 색막대 172.2 GPa 대조
      · 등방 집합체 압입탄성률 Y/(1−ν²) ↔ 측정 평균 M_exp 대조
      · G_c = K²/M, 우리 fracture_model.py (Auerbach P_c ∝ K²R/E*, δ_c ∝ K^{4/3}E*^{-4/3}) 감도
  (B) digitized — **커밋된 크롭**(litdb/figures/<slug>/*.png)에서 픽셀로
      · Fig 6a/b/d 상자그림: 사분위 · 중앙값 · 수염 · 평균 점
        검증 = 평균 점 판독이 캡션의 평균(stated)을 재현하는지
      · Fig 5a C_ij 상자그림 (같은 방식, 검증 = 캡션 평균)
      · Fig 2c 소결로 온도 프로파일 마디 (검증 = 본문 3 °C/min)
      · Fig S1 h_min 50/100/150 nm 정규곡선 봉우리 (scipy 있으면)
    → litdb/figures/<slug>/digitized.csv

⛔ 못 하는 것
  · 크롭을 다시 자르면(해상도·여백이 바뀌면) 축 보정 상수(아래 FRAMES)가 틀어진다.
    이 스크립트는 2026-09-26 수동 재크롭판(figures.json 의 recrop) 전용이다.
  · 상자그림 **수염의 정의**(1 SD? 백분위?)는 논문에 없다 — 이 도구는 위치만 읽는다.
  · 겹친 삼각형 표지(Fig S1)의 개수는 세지 않는다 (N = 174 는 SI 캡션 값).

usage
  python3 tools/litdb/sharma2023_verify.py            # 표 출력 + digitized.csv 쓰기
  python3 tools/litdb/sharma2023_verify.py --no-write # 출력만
"""
import argparse
import csv
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SLUG = "sharma2023_nmc_single_crystal_anisotropic_nanoindentation"
FD = ROOT / "litdb" / "figures" / SLUG

# ── stated inputs (p. 5 Fig 5 caption · p. 6 Fig 6 caption) ────────────────────────────
C11, C12, C13, C14, C44, C33 = 194.89, 133.74, 11.85, 8.61, 74.14, 177.24
M_STATED = {"NMC111": 192.78, "NMC532": 200.81, "NMC622": 150.88, "NMC811": 229.9}
H_STATED = {"NMC111": 9.37, "NMC532": 14.29, "NMC622": 9.92, "NMC811": 14.17}
K_STATED = {"NMC111": 0.162, "NMC532": 0.296, "NMC622": 0.258, "NMC811": 0.271}
PM_M = {"NMC111": 39.59, "NMC532": 33.61, "NMC622": 58.35, "NMC811": 40.55}
PM_H = {"NMC111": 2.94, "NMC532": 2.53, "NMC622": 3.11, "NMC811": 3.32}
COMPS = ["NMC111", "NMC532", "NMC622", "NMC811"]

ROWS = []   # → digitized.csv


def rec(fig, item, value, unit, grade, note=""):
    ROWS.append({"figure": fig, "item": item, "value": value, "unit": unit, "grade": grade, "note": note})


# ════════════════════════════════════════════════════════════════════════════════════
# (A) derived(ours)
# ════════════════════════════════════════════════════════════════════════════════════
def derived():
    C66 = (C11 - C12) / 2
    Q = C11 + C12 + 2 * C33 - 4 * C13
    C2 = (C11 + C12) * C33 - 2 * C13 ** 2
    BV = (2 * (C11 + C12) + 4 * C13 + C33) / 9
    BR = C2 / Q
    GV = (Q + 12 * C44 + 12 * C66) / 30
    GR = 2.5 * C2 * C44 * C66 / (3 * BV * C44 * C66 + C2 * (C44 + C66))
    B, G = (BV + BR) / 2, (GV + GR) / 2
    Y = 9 * B * G / (3 * B + G)
    nu = (3 * B - 2 * G) / (2 * (3 * B + G))
    print("(A1) paper Eq.10 VRH : C66 %.2f | BV %.2f BR %.2f B %.2f | GV %.2f GR %.2f G %.2f | Y %.2f (paper 140.16) nu %.4f (paper 0.253)"
          % (C66, BV, BR, B, GV, GR, G, Y, nu))
    print("      Voigt-bound E %.1f · Reuss-bound E %.1f" % (9 * BV * GV / (3 * BV + GV), 9 * BR * GR / (3 * BR + GR)))
    C = np.array([[C11, C12, C13, C14, 0, 0], [C12, C11, C13, -C14, 0, 0], [C13, C13, C33, 0, 0, 0],
                  [C14, -C14, 0, C44, 0, 0], [0, 0, 0, 0, C44, C14], [0, 0, 0, 0, C14, C66]])
    S = np.linalg.inv(C)
    ev = np.linalg.eigvalsh(C)
    BVf = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[1, 2] + C[0, 2])) / 9
    GVf = ((C[0, 0] + C[1, 1] + C[2, 2]) - (C[0, 1] + C[1, 2] + C[0, 2]) + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    BRf = 1 / ((S[0, 0] + S[1, 1] + S[2, 2]) + 2 * (S[0, 1] + S[1, 2] + S[0, 2]))
    GRf = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[1, 2] + S[0, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    Bf, Gf = (BVf + BRf) / 2, (GVf + GRf) / 2
    Yf, nuf = 9 * Bf * Gf / (3 * Bf + Gf), (3 * Bf - 2 * Gf) / (2 * (3 * Bf + Gf))
    print("(A2) full trigonal VRH (C14 incl.): min eig(C) %.1f GPa | B %.2f G %.2f | Y %.2f (%+.2f %% vs Eq.10) nu %.4f"
          % (ev.min(), Bf, Gf, Yf, 100 * (Yf / Y - 1), nuf))

    vo = {(0, 0): 0, (1, 1): 1, (2, 2): 2, (1, 2): 3, (2, 1): 3, (0, 2): 4, (2, 0): 4, (0, 1): 5, (1, 0): 5}
    s4 = np.zeros((3, 3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for m in range(3):
                    I, J = vo[(i, j)], vo[(k, m)]
                    s4[i, j, k, m] = (0.5 if I > 2 else 1.0) * (0.5 if J > 2 else 1.0) * S[I, J]

    def E_dir(l):
        l = np.asarray(l, float) / np.linalg.norm(l)
        return 1.0 / np.einsum('i,j,k,l,ijkl->', l, l, l, l, s4)

    th = np.radians(np.linspace(0, 90, 181))
    ph = np.radians(np.linspace(0, 360, 361))
    best_min, best_max = (1e9, None), (-1e9, None)
    for t in th:
        for p in ph:
            e = E_dir([math.sin(t) * math.cos(p), math.sin(t) * math.sin(p), math.cos(t)])
            if e < best_min[0]:
                best_min = (e, math.degrees(t))
            if e > best_max[0]:
                best_max = (e, math.degrees(t))
    Ec, Ea = E_dir([0, 0, 1]), E_dir([1, 0, 0])
    print("(A3) directional E: [0001] %.1f · basal-plane %.1f · min %.1f at %.0f deg from c · max %.1f at %.0f deg"
          % (Ec, Ea, best_min[0], best_min[1], best_max[0], best_max[1]))
    M3 = 2 * math.sqrt((C11 * C33 - C13 ** 2) / C11 / (1 / C44 + 2 / (math.sqrt(C11 * C33) + C13)))
    M1 = math.sqrt(math.sqrt(C11 / C33) * (C11 ** 2 - C12 ** 2) / C11 * M3)
    print("(A4) Delafargue-Ulm: M(0001) %.1f (Fig 5b colour bar 172.2) · M(prismatic, approx.) %.1f (colour bar 127)" % (M3, M1))
    Miso = Y / (1 - nu ** 2)
    print("(A5) Y/(1-nu^2) %.1f vs M_exp NMC622 151.81 (108 EBSD sites) %+.1f %% · 150.88 (N=80) %+.1f %%"
          % (Miso, 100 * (Miso / 151.81 - 1), 100 * (Miso / 150.88 - 1)))
    for c in COMPS:
        M = M_STATED[c]
        print("(A6) %s M %.2f -> E = M(1-nu^2): nu 0.25 %.1f · 0.253 %.1f · 0.30 %.1f · 0.32 %.1f | G_c = K^2/M %.3f J/m^2"
              % (c, M, M * (1 - .25 ** 2), M * (1 - .253 ** 2), M * (1 - .3 ** 2), M * (1 - .32 ** 2),
                 (K_STATED[c] * 1e6) ** 2 / (M * 1e9)))
    print("(A7) ours E 140 / nu 0.25: E %+.2f %% · nu %+.2f %% · E/(1-nu^2) %.1f vs %.1f (%+.2f %%)"
          % (100 * (140 / Y - 1), 100 * (0.25 / nu - 1), 140 / (1 - .0625), Miso, 100 * ((140 / (1 - .0625)) / Miso - 1)))
    for lab, k0, k1 in (("K_IC_AM_S 1.0 -> 0.258", 1.0, .258), ("K_IC_AM_S 1.0 -> 0.271", 1.0, .271),
                        ("K_IC_AM_P 0.3 -> 0.271", .3, .271)):
        print("(A8) %s : P_c x %.3f · delta_c x %.3f" % (lab, (k1 / k0) ** 2, (k1 / k0) ** (4 / 3)))
    for E1 in (212.0, 215.2, 229.9):
        r = (E1 / (1 - .253 ** 2)) / (140 / (1 - .0625))
        print("(A9) E_AM_S 140 -> %.1f : E* x %.3f · P_c x %.3f · delta_c x %.3f" % (E1, r, 1 / r, r ** (-4 / 3)))
    for k_sc in (.258, .271):
        print("(A10) SC/PC K ratio %.3f/0.102 = %.2f -> P_c ratio %.1f (ours 1.0/0.3 = 3.33 -> 11.1)"
              % (k_sc, k_sc / .102, (k_sc / .102) ** 2))


# ════════════════════════════════════════════════════════════════════════════════════
# (B) digitized
# ════════════════════════════════════════════════════════════════════════════════════
def _img(name):
    return np.asarray(Image.open(FD / name).convert("RGB")).astype(int)


def _core(mask, k):
    """k×k 창이 전부 True 인 화소 (정사각 침식, 적분영상)."""
    m = mask.astype(np.int32)
    ii = np.pad(m.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
    h, w = m.shape
    out = np.zeros_like(mask)
    r = k // 2
    ys, xs = np.mgrid[r:h - r, r:w - r]
    s = ii[ys + r + 1, xs + r + 1] - ii[ys - r, xs + r + 1] - ii[ys + r + 1, xs - r] + ii[ys - r, xs - r]
    out[r:h - r, r:w - r] = (s == k * k)
    return out


def _hlines(dark, xc, y0, y1, half=45, minw=28):
    band = dark[:, xc - half:xc + half + 1]
    rows = [y for y in range(y0, y1) if band[y].sum() >= minw]
    groups, g = [], []
    for y in rows:
        if g and y - g[-1] <= 1:
            g.append(y)
        else:
            if g:
                groups.append(g)
            g = [y]
    if g:
        groups.append(g)
    return [(float(np.mean(gg)), int(max(band[y].sum() for y in gg))) for gg in groups]


def fig6():
    a = _img("fig_6.png")
    dark = a.max(axis=2) < 100
    # frame (px, this crop): y_top ↔ axis max, y_bottom ↔ 0 ; category whisker x
    P = {"a": (103.5, 729.5, 300.0, [255, 433, 610, 787], "M_exp", "GPa"),
         "b": (102.5, 729.5, 20.0, [1197, 1374, 1551, 1728], "H", "GPa"),
         "d": (911.0, 1488.0, 0.8, [1198, 1375, 1552, 1729], "K_c", "MPa m^1/2")}
    core = _core(a.max(axis=2) < 80, 9)
    for pn, (yt, yb, vmax, xcs, q, unit) in P.items():
        cal = lambda y: (yb - y) / (yb - yt) * vmax
        for comp, xc in zip(COMPS, xcs):
            ls = _hlines(dark, xc, int(yt) + 2, int(yb) - 1)
            wide = [y for y, w in ls if w >= 80]           # box edges + median (full box width)
            caps = [y for y, w in ls if 40 <= w < 80]       # whisker caps
            dy, dx = np.where(core[int(yt) + 3:int(yb) - 2, xc - 30:xc + 31])
            ym = dy.mean() + int(yt) + 3 if len(dy) else float("nan")
            vals = {"mean_dot": cal(ym)}
            if len(wide) >= 3:
                vals["Q3"], vals["median"], vals["Q1"] = cal(wide[0]), cal(wide[1]), cal(wide[-1])
            elif len(wide) == 2:
                vals["Q3"], vals["Q1"] = cal(wide[0]), cal(wide[-1])
            if len(caps) >= 2:
                vals["whisker_hi"], vals["whisker_lo"] = cal(caps[0]), cal(caps[-1])
            st = {"M_exp": M_STATED, "H": H_STATED, "K_c": K_STATED}[q][comp]
            print("  Fig 6%s %-6s %-5s " % (pn, comp, q) + " ".join("%s=%.4g" % kv for kv in vals.items())
                  + "   (stated mean %.4g, dot error %+.3g)" % (st, vals["mean_dot"] - st))
            for k, v in vals.items():
                rec("Fig 6" + pn, f"{comp} {q} {k}", round(v, 4), unit, "digitized",
                    f"stated mean {st}; dot-vs-stated {vals['mean_dot'] - st:+.4f}" if k == "mean_dot" else "")
            if q in ("M_exp", "H") and "whisker_hi" in vals:
                pm = (PM_M if q == "M_exp" else PM_H)[comp]
                half = (vals["whisker_hi"] - vals["whisker_lo"]) / 2
                ctr = (vals["whisker_hi"] + vals["whisker_lo"]) / 2
                print("        whisker half-width %.3g vs stated ± %.3g · whisker centre %.4g vs mean %.4g" % (half, pm, ctr, st))
                rec("Fig 6" + pn, f"{comp} {q} whisker half-width", round(half, 4), unit, "digitized",
                    f"stated ± {pm}; whisker centre {ctr:.3f}")


def fig5():
    a = _img("fig_5.png")
    dark = a.max(axis=2) < 110
    cal = lambda y: (762.5 - y) / (118.8 / 50)      # y ticks: 0 → 762.5 px, 50 GPa per 118.8 px
    core = _core(a.max(axis=2) < 110, 9)
    for nm, xc, st in (("C11", 167, C11), ("C12", 301, C12), ("C13", 437, C13), ("C14", 571, C14),
                       ("C44", 720, C44), ("C33", 837, C33)):
        dy, dx = np.where(core[112:820, xc - 20:xc + 21])
        ym = dy.mean() + 112 if len(dy) else float("nan")
        ls = [(round(cal(y), 1), w) for y, w in _hlines(dark, xc, 112, 820, half=24, minw=20) if cal(y) < 200 or nm in ("C11", "C33")]
        print("  Fig 5a %-4s mean dot %.2f (stated %.2f) · horizontal lines (value, width px): %s" % (nm, cal(ym), st, ls))
        rec("Fig 5a", f"{nm} mean_dot", round(cal(ym), 2), "GPa", "digitized", f"stated {st}")


def fig2c():
    a = _img("fig_2.png")
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (r > 150) & (r - g > 80) & (r - b > 80)
    core = _core(red, 7)
    reg = core[640:1110, 110:750]
    ys, xs = np.where(reg)
    pts = []
    for y, x in zip(ys, xs):
        for p in pts:
            if abs(p[0] - (x + 110)) < 12 and abs(p[1] - (y + 640)) < 12:
                p[2].append((x + 110, y + 640))
                break
        else:
            pts.append([x + 110, y + 640, [(x + 110, y + 640)]])
    nodes = sorted((np.mean([q[0] for q in p[2]]), np.mean([q[1] for q in p[2]])) for p in pts)
    tx = lambda x: (x - 134.0) / ((540.0 - 134.0) / 10)          # x ticks 0,5,10 h
    tT = lambda y: 900 - (y - 671.0) / ((1038.0 - 671.0) / 800)   # y ticks 900 … 100 °C
    prev = None
    for x, y in nodes:
        t, T = tx(x), tT(y)
        rate = "" if prev is None or abs(t - prev[0]) < 1e-6 else " · rate %.2f °C/min" % ((T - prev[1]) / ((t - prev[0]) * 60))
        print("  Fig 2c node t=%.2f h  T=%.0f °C%s" % (t, T, rate))
        rec("Fig 2c", "furnace node", f"{t:.2f} h / {T:.0f} C", "h / degC", "digitized", rate.strip(" ·"))
        prev = (t, T)


def figS1():
    try:
        from scipy import ndimage
    except ImportError:
        print("  (Fig S1 skipped — scipy not available)")
        return
    a = _img("fig_S1.png")
    dark = a.max(axis=2) < 140
    kcal = lambda y: (730.5 - y) / ((730.5 - 95.0) / 0.8)          # y ticks 0.0 → 730.5, 0.8 → 95.0
    for (x0, x1), hm in zip(((176, 696), (705, 1225), (1235, 1755)), (50, 100, 150)):
        lab, n = ndimage.label(dark[20:806, x0:x1], structure=np.ones((3, 3)))
        best = None
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if best is None or ys.max() - ys.min() > best[0]:
                best = (ys.max() - ys.min(), ys, xs)
        _, ys, xs = best
        ypk = ys[xs >= xs.max() - 1].mean() + 20
        print("  Fig S1 h_min=%3d nm : fitted-normal peak K ≈ %.3f MPa m^1/2" % (hm, kcal(ypk)))
        rec("Fig S1", f"h_min {hm} nm normal-curve peak", round(kcal(ypk), 3), "MPa m^1/2", "digitized",
            "NMC622, N = 174 (SI caption)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    print("=== (A) derived(ours) from stated C_ij / means ===")
    derived()
    print("=== (B) digitized from committed crops ===")
    fig6()
    fig5()
    fig2c()
    figS1()
    if not a.no_write:
        out = FD / "digitized.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["figure", "item", "value", "unit", "grade", "note"])
            w.writeheader()
            w.writerows(ROWS)
        print(f"→ {out.relative_to(ROOT)}  ({len(ROWS)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
