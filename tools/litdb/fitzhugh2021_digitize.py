#!/usr/bin/env python3
"""fitzhugh2021_digitize.py — Fitzhugh, Chen, Wang, Ye, Li, Energy Environ. Sci. 14, 4574 (2021) **그림 판독 + SI 표 검산**.

카드: litdb/papers/fitzhugh2021_sei_design_constrained_ensemble.md  (§5 · §6 · §12)
원본: 본문 PDF (10 쪽, RSC) + ESI PDF (8 쪽).  ⚠ PDF 는 리포에 없다 (litdb/inbox 는 gitignore).
      그림은 전부 **내장 JPEG 래스터**다 — 벡터 좌표가 없다.  그래서 픽셀에서 읽는다.

⛔ 이 스크립트가 내는 그림 값은 전부 **판독 (figure-read)** 이다.  카드·표에 옮길 때 `figure-read ≈` 표지를 떼지 말 것.
   논문이 숫자로 적은 것은 본문 문장 몇 개 (LPS 분포 18.5 / 14.8 / 13.0 GPa · RMSE 2.59 GPa · 16.07 → 12.07 → 6.89 → 2.05 GPa 등) 와
   ESI Table 1 · 2 (K_crit · 조성) 뿐이다.

무엇을 하나
  (1) ESI Table 1 · 2 검산 (`--check-only` · PDF 불필요): 조성 합 = 1 · 명목 산화수 전하합 Σ x·z · 원소별 최대 변화 · K_crit 평균.
  (2) 판독 (`--pdf --si`):
      Fig. 5a · 5b · 5d · S4a–d · S6 (마커)  ·  Fig. 3a · S1a–c (히스토그램 40 칸) · S1d (막대)  ·
      Fig. 3b (원소 칸 색 → 색 막대 값)  ·  Fig. 5c · S5 (CV 봉우리 위치 · 높이)  ·  Fig. S2 (곡선 값).
  (3) 판독값끼리의 검산과 유도량 (`--check`): 아래 '검증'.
방법
  · 축: 축 테두리 밖 눈금의 픽셀 중심 → 선형 최소제곱 (잔차 출력).  히스토그램은 격자선 (흰 선) 과 막대 밑변으로 보정.
  · 마커: 색 마스크 → 열림 (침식 + 팽창) 으로 선을 지우고 → 연결성분 중심.  범례 마커는 x 가 수정 수준 (0 · 1.25 · 2.5 · 4 · 5 · 6 %) 에서
    벗어난 것으로 걸러 낸다.
  · Fig. 3b: 칸 안의 글자 (검정) 를 뺀 중앙값 색 → 같은 그림의 색 막대 (−1 … +1) 에서 가장 가까운 색의 값.
검증 (`--check` 가 출력 · 문턱을 넘으면 종료 코드 1)
  · Fig. 5b 의 K_crit(0 %) · K_crit(5 %) 판독 = ESI Table 2 첫 행 13.31 · 7.60 GPa (문턱 0.06).
  · Fig. S1d 의 LPS 막대 = 본문 18.5 / 14.8 / 13.0 GPa (문턱 0.15).
  · K_eff 곡선 8 묶음이 전부 G(K_eff) = G0·(1 − K_eff/K_crit) (식 3 의 선형 꼴) 을 따른다 (문턱 0.002 eV/atom).
  · Fig. 5c 의 넓은 봉우리 픽셀 높이 ÷ Fig. 5d 의 H_R = 상수 (곡선 여섯이 같은 전류 눈금 · 문턱 ±6 %).
  · Fig. S1b (LSPS) 를 25 GPa 에서 자른 평균 · 분산 ↔ Fig. S3 뿌리 노드에 인쇄된 value 14.416 · mse 27.974 (보고만 한다 — 판정 아님).
이 도구가 못 하는 것
  · 다른 판본의 PDF (그림 해상도 · 배치가 다르면) — 내장 이미지 크기가 기대와 다르면 **읽지 않고 멈춘다**.
  · 가려진 마커 (Fig. 5b 0 % 의 주황 ● 는 파랑 ■ 밑 · K_eff = 10 · 4 · 6 GPa 의 0 값은 빨강 밑) 는 못 읽는다 — 행이 없다.
  · Fig. 3b 의 값은 '색 → 색 막대' 환산이라 0 근처 (거의 흰색) 에서 ±0.03 정도 흔들린다.  어떤 상관계수인지는 논문이 적지 않았다.
  · 히스토그램은 0–80 GPa 만 그려져 있다 — 그 위 꼬리는 못 본다 (그래서 평균 · 표준편차가 본문값보다 조금 낮게 나온다).
  · 유도량 (ε_RXN·V⁰ = G0/K_crit · 기여 분해 · 순위 상관 · 선형 보간 개시 전압) 은 **우리 산술**이지 논문 값이 아니다.
usage
  ~/.venvs/litdb/bin/python3 tools/litdb/fitzhugh2021_digitize.py --pdf "<본문>.pdf" --si "<ESI>.pdf" --check
  python3 tools/litdb/fitzhugh2021_digitize.py --check-only      # PDF 없이 표 검산만 (표준 라이브러리 + numpy)
  python3 tools/litdb/fitzhugh2021_digitize.py --selftest        # 합성 그림으로 양성 + 음성 경로
"""
import argparse
import csv
import io
import re
import sys
from pathlib import Path

import numpy as np

SLUG = "fitzhugh2021_sei_design_constrained_ensemble"
ROOT = Path(__file__).resolve().parents[2]
EV_PER_GPA_A3 = 160.21766            # 1 eV/GPa = 160.2 Å^3
MOD = [0.0, 1.25, 2.5, 4.0, 5.0, 6.0]  # composition modification levels (%), Fig. 5 · S4 · S6
ROWS = []
FAIL = []

# ---- 인쇄값 (본문 · ESI) ----------------------------------------------------------------------
TXT_LPS = (18.5, 14.8, 13.0)         # 본문 p.4578: LPS(Li7P3S11) 분포 평균 · 중앙 · 표준편차 (GPa)
ROOT_NODE = (14.416, 27.974, 10000)  # Fig. S3 뿌리 노드에 인쇄: value · mse · samples
RMSE = 2.59                          # 본문 p.4578 · Fig. 4 캡션 (GPa)
# 명목 산화수 (전하합 검산용 — 우리 가정이다: Pb 2+ · Sb 3+ · Bi 3+ · Ni 2+ · Ti 4+ · N 3− · C 4+)
Z = dict(H=1, Li=1, B=3, C=4, N=-3, O=-2, F=-1, Si=4, P=5, S=-2, Cl=-1, K=1, Ti=4, Ni=2, Zn=2, Ge=4, Br=-1, Sb=3,
         I=-1, Pb=2, Bi=3)
# (parent, sigma mS/cm [ref no. as printed], Kcrit parent, child A, K, child B, K, child C, K) — ESI p.6 Table 1 (LSPS · 4 V)
T1 = [
    ("Li0.364P0.110S0.388I0.138", "1.7 [1]", 16.07, "Li0.324O0.04F0.042P0.098S0.346Cl0.026I0.123", 12.07,
     "Li0.306O0.014F0.090P0.093S0.324Cl0.002Br0.03Sb0.024I0.115", 6.89, "Li0.141O0.375F0.282P0.01S0.14I0.053", 2.05),
    ("Li0.338B0.169S0.351I0.143", "0.2 [2]", 15.7, "Li0.335B0.135O0.019F0.047S0.322Cl0.002I0.142", 11.23,
     "Li0.322B0.069F0.102P0.015S0.275Br0.042Sb0.038I0.136", 5.46,
     "Li0.113B0.010O0.323F0.282S0.138Cl0.010I0.048Bi0.076", 1.90),
    ("Li0.431Si0.092S0.323I0.154", "0.04 [3]", 17.74, "Li0.369O0.033F0.041Si0.067P0.039S0.274Cl0.044I0.132", 12.45,
     "Li0.406F0.103Si0.004P0.015S0.273Cl0.001Sb0.053I0.145", 5.49, "Li0.149O0.336F0.321S0.140I0.053", 2.19),
    ("Li0.423O0.013Si0.118P0.003S0.443", "0.12 [4]", 17.4,
     "Li0.362O0.033F0.043Si0.068P0.003S0.394Cl0.046Br0.045Pb0.006", 11.78,
     "Li0.376O0.093F0.082Si0.019P0.003S0.355Cl0.059K0.001Sb0.012", 7.51,
     "Li0.123O0.288F0.281P0.001S0.149Cl0.008Ti0.150", 2.11),
    ("Li0.333S0.500Ge0.167", "0.15-0.5 [5,6]", 15.57, "Li0.300O0.033F0.043S0.449Cl0.025Ge0.150", 10.75,
     "Li0.312O0.002F0.090S0.398Cl0.008Ge0.111Br0.040Sb0.013I0.022Pb0.004", 5.93,
     "Li0.078O0.348F0.285P0.017S0.117Ge0.009Bi0.145", 1.56),
    ("Li0.333Si0.167S0.500", "0.27 [4]", 15.2, "Li0.275O0.035F0.041Si0.140S0.413Cl0.042Br0.012Pb0.041", 11.22,
     "Li0.266O0.065F0.068Si0.125S0.399Cl0.064Br0.005Sb0.009", 8.66, "Li0.083O0.367F0.375P0.018S0.124Cl0.033", 1.86),
    ("Li0.400Si0.133S0.467", "1.0 [7]", 16.51, "Li0.341O0.049F0.043Si0.133S0.398Cl0.025Br0.004Pb0.004", 11.66,
     "Li0.338O0.065F0.072Si0.063S0.394Cl0.068", 9.49, "Li0.147O0.365F0.301S0.177Cl0.010", 2.21),
    ("Li0.370Si0.130S0.389Cl0.111", "0.05 [8]", 13.57, "Li0.334O0.048F0.021Si0.081S0.415Cl0.100", 10.47,
     "Li0.287O0.096F0.083Si0.132P0.011S0.305Cl0.086", 8.98, "Li0.070O0.188F0.317Si0.025S0.074Cl0.021Br0.306", 2.27),
    ("Li0.406O0.061Si0.130S0.403", "0.1 [1]", 15.24, "Li0.297O0.092F0.039Si0.125S0.349Cl0.037Br0.025Pb0.036", 10.68,
     "Li0.332O0.093F0.069Si0.030S0.330Cl0.061K0.001Zn0.044Br0.040", 8.86, "Li0.223O0.040F0.445Si0.070S0.222", 1.90),
    ("Li0.425O0.013Si0.121S0.441", "0.3 [9]", 16.62, "Li0.355O0.055F0.040Si0.127S0.399Cl0.025", 11.82,
     "Li0.364O0.078F0.077Si0.023S0.378Cl0.080", 9.00, "Li0.129N0.156O0.257F0.291Si0.006P0.010S0.131Cl0.020", 1.81),
]
# ESI p.7 Table 2 (LGPS · 4 V) — 같은 부모 10 개
T2 = [
    ("Li0.364P0.110S0.388I0.138", "1.7 [1]", 13.31, "Li0.280O0.021F0.042P0.085S0.417Cl0.048I0.106", 7.60,
     "Li0.319O0.021F0.105P0.010S0.387Cl0.099K0.018I0.040", 3.88, "Li0.128C0.011N0.115F0.508P0.022S0.137K0.030I0.049", 1.36),
    ("Li0.338B0.169S0.351I0.143", "0.2 [2]", 12.62, "Li0.345B0.119O0.008F0.037P0.037S0.308I0.146", 9.23,
     "Li0.316B0.177N0.008F0.092S0.274I0.133", 6.89, "Li0.100B0.050O0.199F0.466S0.104Ni0.038I0.042", 2.83),
    ("Li0.431Si0.092S0.323I0.154", "0.04 [3]", 12.77, "Li0.417O0.013F0.029Si0.120S0.272I0.149", 7.75,
     "Li0.337N0.035O0.080F0.079P0.080S0.252I0.138", 5.50, "Li0.137N0.010O0.220F0.461P0.020S0.103I0.049", 2.13),
    ("Li0.423O0.013Si0.118P0.003S0.443", "0.12 [4]", 13.35, "Li0.451O0.010F0.054Si0.078S0.408", 8.58,
     "Li0.348N0.065F0.094S0.394Cl0.075K0.006", 4.71, "Li0.117O0.247F0.453Si0.040P0.019S0.123", 2.10),
    ("Li0.333S0.500Ge0.167", "0.15-0.5 [5,6]", 14.54, "Li0.272Ni0.034O0.030F0.042P0.021S0.444Cl0.042Ge0.115", 9.25,
     "Li0.294O0.052F0.091P0.040S0.406Ge0.117", 6.77, "Li0.051N0.267O0.520F0.054P0.098Ge0.010", 2.05),
    ("Li0.333Si0.167S0.500", "0.27 [4]", 13.56, "Li0.314O0.031F0.048Si0.148S0.459", 8.90,
     "Li0.299O0.001F0.091Si0.206S0.403", 6.02, "Li0.088O0.257F0.453Si0.050S0.132", 2.09),
    ("Li0.400Si0.133S0.467", "1.0 [7]", 13.68, "Li0.387O0.010F0.049Si0.083P0.035S0.435", 8.68,
     "Li0.416O0.009F0.105Si0.103S0.367", 5.74, "Li0.106O0.257F0.454Si0.040P0.020S0.124", 2.10),
    ("Li0.370Si0.130S0.389Cl0.111", "0.05 [8]", 9.61, "Li0.359O0.013F0.050Si0.089P0.033S0.349Cl0.108", 6.26,
     "Li0.330O0.017F0.096Si0.115P0.016S0.327Cl0.099", 4.18,
     "H0.011Li0.125N0.012O0.011F0.579P0.026S0.131Cl0.037Ni0.025Br0.043", 1.80),
    ("Li0.406O0.061Si0.130S0.403", "0.1 [1]", 13.45, "Li0.376O0.068F0.051Si0.081P0.035S0.355Cl0.034", 7.63,
     "H0.003Li0.288O0.068F0.067Si0.180P0.078S0.219Cl0.096", 4.62, "Li0.329F0.516Si0.070P0.021S0.065", 1.04),
    ("Li0.425O0.013Si0.121S0.441", "0.3 [9]", 13.35, "Li0.458O0.010F0.054Si0.071S0.407", 8.59,
     "Li0.390F0.103Si0.023S0.376Cl0.105Ge0.003", 4.15, "Li0.118O0.247F0.453Si0.040P0.019S0.122", 2.10),
]


def put(fig, panel, series, x, xu, y, yu, note=""):
    ROWS.append(dict(figure=fig, panel=panel, series=series, x=x, x_unit=xu, y=y, y_unit=yu, note=note))


def flag(msg):
    FAIL.append(msg)
    print("   ⛔ " + msg)


# ---- 표 검산 (PDF 불필요) -----------------------------------------------------------------------
def parse_formula(f):
    d = {}
    for el, v in re.findall(r"([A-Z][a-z]?)([0-9.]+)", f):
        if el not in Z:
            raise ValueError(f"unknown element {el!r} in {f!r}")
        d[el] = d.get(el, 0.0) + float(v)
    return d


def charge(d):
    return sum(v * Z[k] for k, v in d.items())


def check_tables(tables=(("ESI Table 1 (LSPS · 4 V)", T1), ("ESI Table 2 (LGPS · 4 V)", T2)), verbose=True):
    """조성 합 · 전하합 · 최대 변화 · 평균.  반환: 합이 1 에서 0.005 넘게 벗어난 칸의 목록."""
    bad = []
    for name, tab in tables:
        k = np.array([[r[2], r[4], r[6], r[8]] for r in tab])
        if verbose:
            print(f"== {name}")
            print(f"   K_crit 평균  parent / A / B / C = {np.round(k.mean(axis=0), 2)}   범위 "
                  + " · ".join(f"{a:.2f}–{b:.2f}" for a, b in zip(k.min(axis=0), k.max(axis=0))))
            print(f"   child ÷ parent 평균비  A / B / C = {np.round((k[:, 1:] / k[:, :1]).mean(axis=0), 3)}")
        new = {"A": {}, "B": {}, "C": {}}
        for i, r in enumerate(tab):
            p = parse_formula(r[0])
            line = f"   행 {i + 1:2d} parent 합 {sum(p.values()):.3f} Σxz {charge(p):+.3f} |"
            if abs(sum(p.values()) - 1) > 0.005:
                bad.append((name, i + 1, "parent", round(sum(p.values()), 3)))
            for tag, f in (("A", r[3]), ("B", r[5]), ("C", r[7])):
                c = parse_formula(f)
                els = set(p) | set(c)
                dl = {e: c.get(e, 0) - p.get(e, 0) for e in els}
                em = max(dl, key=lambda e: abs(dl[e]))
                for e in c:
                    if e not in p:
                        new[tag][e] = new[tag].get(e, 0) + 1
                if abs(sum(c.values()) - 1) > 0.005:
                    bad.append((name, i + 1, tag, round(sum(c.values()), 3)))
                line += (f" {tag}: 합 {sum(c.values()):.3f} Σxz {charge(c):+.3f} Li {c.get('Li', 0):.3f}"
                         f" O+F {c.get('O', 0) + c.get('F', 0):.3f} max {em}{dl[em]:+.3f} |")
                put(name.split(" (")[0], f"row {i + 1}", f"child {tag} nominal charge sum", i + 1, "row",
                    round(charge(c), 3), "e per atom", f"Kcrit {r[4 + 2 * 'ABC'.index(tag)]} GPa · {f}")
            put(name.split(" (")[0], f"row {i + 1}", "parent nominal charge sum", i + 1, "row", round(charge(p), 3),
                "e per atom", f"Kcrit {r[2]} GPa · sigma {r[1]} · {r[0]}")
            if verbose:
                print(line)
        if verbose:
            for tag in "ABC":
                print(f"   child {tag} 에 새로 들어온 원소 (행 수): "
                      + ", ".join(f"{e} {n}" for e, n in sorted(new[tag].items(), key=lambda t: -t[1])))
    if verbose:
        print("   합 ≠ 1 (±0.005) 인 칸:", bad if bad else "없음")
        print("   ※ 전구체 Li2S · P2S5 · LiI · LiF · Li2O 는 전부 Σxz = 0 이라 그 혼합도 Σxz = 0 이다 (선형 제약).")
    return bad


# ---- 픽셀 도우미 (numpy 만) --------------------------------------------------------------------
def dark(img, thr=120):
    return img.max(axis=2) < thr


def group(vals, tol=1):
    out = []
    for v in sorted(vals):
        if out and v - out[-1][-1] <= tol:
            out[-1].append(v)
        else:
            out.append([v])
    return [float(np.mean(g)) for g in out]


def ticks_along(mask, frame, side, depth=14, minlen=4):
    x0, y0, x1, y1 = frame
    if side == "bottom":
        strip = mask[y1 + 3:y1 + 3 + depth, x0 - 5:x1 + 6]
        return group(list(np.where(strip.sum(axis=0) >= minlen)[0] + x0 - 5))
    if side == "left":
        strip = mask[y0 - 5:y1 + 6, x0 - 3 - depth:x0 - 3]
    else:
        strip = mask[y0 - 5:y1 + 6, x1 + 3:x1 + 3 + depth]
    return group(list(np.where(strip.sum(axis=1) >= minlen)[0] + y0 - 5))


def fit_axis(pix, vals):
    """픽셀 → 값 선형 최소제곱.  눈금 수가 안 맞으면 조용히 맞추지 않고 ValueError."""
    if len(pix) != len(vals) or len(pix) < 2:
        raise ValueError(f"tick count mismatch: found {len(pix)} px positions for {len(vals)} labels")
    a = np.vstack([np.asarray(pix, float), np.ones(len(pix))]).T
    sol = np.linalg.lstsq(a, np.asarray(vals, float), rcond=None)[0]
    return float(sol[0]), float(sol[1]), float(np.abs(a @ sol - np.asarray(vals, float)).max())


def color_mask(img, rgb, tol=90):
    return np.abs(img - np.array(rgb)[None, None, :]).sum(axis=2) < tol


def erode(m, r):
    """(2r+1)² 정사각 침식.  그림 밖은 False 로 본다 (테두리에 닿은 덩어리는 깎인다)."""
    h, w = m.shape
    pad = np.pad(m, r, constant_values=False)
    out = np.ones_like(m)
    for dy in range(2 * r + 1):
        for dx in range(2 * r + 1):
            out &= pad[dy:dy + h, dx:dx + w]
    return out


def dilate(m, r):
    h, w = m.shape
    pad = np.pad(m, r, constant_values=False)
    out = np.zeros_like(m)
    for dy in range(2 * r + 1):
        for dx in range(2 * r + 1):
            out |= pad[dy:dy + h, dx:dx + w]
    return out


def opening(m, r):
    return dilate(erode(m, r), r)


def label(m):
    """4-연결 성분.  반환: [(x 평균, y 평균, 넓이, y 최소, y 최대)]"""
    h, w = m.shape
    seen = np.zeros(m.shape, bool)
    out = []
    ys, xs = np.nonzero(m)
    for y, x in zip(ys.tolist(), xs.tolist()):
        if seen[y, x]:
            continue
        stack = [(y, x)]
        seen[y, x] = True
        py, px = [], []
        while stack:
            cy, cx = stack.pop()
            py.append(cy)
            px.append(cx)
            for ny, nx in ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)):
                if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        out.append((float(np.mean(px)), float(np.mean(py)), len(py), min(py), max(py)))
    return sorted(out)


def blobs(mask, open_r, min_area):
    return [b for b in label(opening(mask, open_r)) if b[2] >= min_area]


COL = {"blue": (31, 119, 180), "orange": (255, 127, 14), "green": (44, 160, 44), "red": (214, 39, 40),
       "purple": (148, 103, 189), "brown": (140, 86, 75)}


def read_markers(img, frame, xt, yt, yr=None, open_r=3, min_area=25, depth=14, yp_manual=None):
    """마커 판독.  반환 {색: [(x, y[, y_right])...]} — x 가 MOD 수준에서 0.06 넘게 벗어난 것 (범례) 은 버린다."""
    m = dark(img)
    sx, ix, rx = fit_axis(ticks_along(m, frame, "bottom", depth), xt)
    if yp_manual:
        sy, iy, ry = fit_axis(yp_manual[0], yp_manual[1])
    else:
        sy, iy, ry = fit_axis(ticks_along(m, frame, "left", depth), yt)
    cal = dict(rx=rx, ry=ry)
    if yr:
        sr, ir, rr = fit_axis(ticks_along(m, frame, "right", depth), yr)
        cal["rr"] = rr
    x0, y0, x1, y1 = frame
    sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
    out = {}
    for cn in ("blue", "orange", "green", "red"):
        pts = []
        for bx, by, area, _a, _b in blobs(color_mask(sub, COL[cn]), open_r, min_area):
            xv = sx * (bx + x0 + 3) + ix
            lv = min(MOD, key=lambda t: abs(t - xv))
            if abs(lv - xv) > 0.06:
                continue                                        # 범례 마커
            rec = [lv, sy * (by + y0 + 3) + iy]
            if yr:
                rec.append(sr * (by + y0 + 3) + ir)
            pts.append(tuple(rec))
        if pts:
            out[cn] = pts
    return out, cal


# ---- PDF 래스터 ---------------------------------------------------------------------------------
def rasters(pdf, tag):
    """쪽 → [RGB 배열].  내장 이미지 크기가 기대와 다르면 멈춘다 (다른 판본을 조용히 읽지 않는다)."""
    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf
    from PIL import Image
    doc = pymupdf.open(pdf)
    out = {}
    for i, pg in enumerate(doc):
        for im in pg.get_images(full=True):
            if im[2] < 400:
                continue
            arr = np.asarray(Image.open(io.BytesIO(doc.extract_image(im[0])["image"])).convert("RGB")).astype(int)
            out.setdefault(i + 1, []).append(arr)
    want = {5: [(1653, 529)], 7: [(1653, 1113)]} if tag == "main" else \
        {1: [(1275, 1650)], 2: [(1275, 1650)], 4: [(1430, 1023)], 5: [(1427, 564), (1443, 514)]}
    for pgno, sizes in want.items():
        got = sorted((a.shape[1], a.shape[0]) for a in out.get(pgno, []))
        if got != sorted(sizes):
            raise SystemExit(f"⛔ {tag} PDF p.{pgno}: 내장 이미지 크기 {got} ≠ 기대 {sorted(sizes)} — 다른 판본이다. 읽지 않는다.")
    return out


# ---- 판독: 마커 그림 ---------------------------------------------------------------------------
def read_line_figs(main, si):
    f5 = main[7][0]
    s4 = si[4][0]
    s6 = [a for a in si[5] if a.shape[1] == 1443][0]
    xt = [0, 1, 2, 3, 4, 5, 6]
    res = {}
    jobs = [
        ("5a", f5, (142, 66, 749, 493), [0.5, 0.4, 0.3, 0.2, 0.1, 0.0], None, 2, 12, None),
        ("5b", f5, (966, 65, 1574, 492), [0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.32], [14, 13, 12, 11, 10, 9, 8, 7], 3, 25, None),
        ("5d", f5, (966, 614, 1571, 1039), [30, 20, 10], None, 3, 25, None),
        ("S4a", s4, (149, 17, 690, 397), [4.6, 4.4, 4.2, 4.0, 3.8, 3.6], None, 3, 25, None),
        ("S4b", s4, (875, 17, 1416, 397), [7.5, 7.0, 6.5, 6.0, 5.5, 5.0], None, 3, 25, None),
        # S4c: 0.01 눈금이 라벨에 가려 자동 검출이 7/9 → 검출된 7 개를 값에 손으로 맞춘다
        ("S4c", s4, (145, 560, 690, 943), None, None, 2, 12,
         ([608.5, 656.5, 704.0, 751.5, 799.0, 894.5, 942.0], [0.06, 0.05, 0.04, 0.03, 0.02, 0.0, -0.01])),
        ("S4d", s4, (871, 561, 1416, 944), [0.20, 0.15, 0.10, 0.05, 0.0], None, 2, 12, None),
        ("S6L", s6, (107, 23, 688, 429), [5.5, 5.25, 5.0, 4.75, 4.5, 4.25, 4.0], None, 3, 25, None),
        ("S6R", s6, (845, 24, 1426, 430), [0.4, 0.3, 0.2, 0.1, 0.0], None, 2, 12, None),
    ]
    for name, img, fr, yt, yr, orad, amin, ypm in jobs:
        pts, cal = read_markers(img, fr, xt, yt, yr, orad, amin, yp_manual=ypm)
        res[name] = pts
        print(f"   {name}: 보정 잔차 " + " ".join(f"{k} {v:.4f}" for k, v in cal.items()) + " | "
              + " ; ".join(f"{c} " + " ".join(f"{p[0]:g}:{p[1]:.4f}" for p in v) for c, v in pts.items()))
    return res


SERIES = {
    "5a": {"blue": "K_eff = 0 GPa", "orange": "K_eff = 5 GPa", "green": "K_eff = 10 GPa", "red": "K_eff = 15 GPa"},
    "S4c": {"blue": "K_eff = 0 GPa", "orange": "K_eff = 2 GPa", "green": "K_eff = 4 GPa", "red": "K_eff = 6 GPa"},
    "S4d": {"blue": "K_eff = 0 GPa", "orange": "K_eff = 3 GPa", "green": "K_eff = 6 GPa", "red": "K_eff = 8 GPa"},
    "S6R": {"blue": "K_eff = 0 GPa", "orange": "K_eff = 3 GPa", "green": "K_eff = 5 GPa", "red": "K_eff = 6 GPa"},
}
YLAB = {"5a": ("interface decomposition energy at 4 V (LGPS | glass)", "eV/atom"),
        "S4c": ("interface decomposition energy at 2 V (LGPS | glass)", "eV/atom"),
        "S4d": ("interface decomposition energy at 3 V (LGPS | glass)", "eV/atom"),
        "S6R": ("self-decomposition energy of the glass at 3.5 V", "eV/atom")}


def series_of(res, name, color):
    d = dict((p[0], p[1]) for p in res[name].get(color, []))
    return np.array([d.get(m, np.nan) for m in MOD])


def emit_line_rows(res):
    for name in ("5a", "S4c", "S4d", "S6R"):
        for cn, lab in SERIES[name].items():
            for p in res[name].get(cn, []):
                put(name[:-1] if name[0] != "S" else name[:2], name[-1].lower() if name != "S6R" else "right",
                    f"{YLAB[name][0]} · {lab}", p[0], "modification %", round(p[1], 4), YLAB[name][1],
                    "figure-read (marker centroid)")
    for p in res["5b"].get("blue", []):
        put("5", "b", "predicted interface K_crit at 4 V (LGPS | glass)", p[0], "modification %", round(p[2], 3), "GPa",
            "figure-read · right axis")
    for p in res["5b"].get("orange", []):
        put("5", "b", "predicted self-decomposition energy at 3.5 V (K_eff = 0)", p[0], "modification %", round(p[1], 4),
            "eV/atom", "figure-read · left axis · 0 % marker hidden under the blue square (see S6 right)")
    for cn, lab in (("blue", "H_L pre-peak current (about 3 V)"), ("orange", "H_R broad-peak current (about 3.5 V)")):
        for p in res["5d"].get(cn, []):
            put("5", "d", lab, p[0], "modification %", round(p[1], 2), "uA", "figure-read")
    for name, lab in (("S4a", "predicted interface K_crit at 2 V (LGPS | glass)"),
                      ("S4b", "predicted interface K_crit at 3 V (LGPS | glass)"),
                      ("S6L", "predicted K_crit for self-decomposition at 3.5 V")):
        for p in res[name].get("blue", []):
            put(name[:2], name[2:].lower() if name != "S6L" else "left", lab, p[0], "modification %", round(p[1], 3),
                "GPa", "figure-read")


# ---- 판독: 히스토그램 · 막대 -------------------------------------------------------------------
def read_hist(img, box, xz, p10, yz, p500):
    """2 GPa 칸 40 개의 높이.  xz · p10 = K_crit 0 의 x 픽셀 · 10 GPa 당 픽셀 / yz · p500 = 0 의 y 픽셀 · 500 개당 픽셀."""
    red = (img[:, :, 0] > 150) & (img[:, :, 1] < 150) & (img[:, :, 2] < 130) & (img[:, :, 0] - img[:, :, 2] > 60)
    bm = red | (img.max(axis=2) < 100)
    x0, y0, x1, y1 = box
    out = []
    for b in range(40):
        c0 = int(round(xz + (2 * b + 1) * p10 / 10.0))
        col = bm[y0:int(round(yz)) + 1, c0 - 1:c0 + 2].sum(axis=1) >= 2
        ys = np.where(col)[0]
        if len(ys) == 0:
            out.append(0.0)
            continue
        top = ys[-1]
        for t in ys[::-1]:
            if top - t <= 1:
                top = t
            else:
                break
        out.append(max(0.0, (yz - (top + y0)) / p500 * 500.0))
    return np.array(out)


def hist_stats(c, cut=None):
    w = 2.0
    lo = np.arange(40) * w
    frac = np.ones(40) if cut is None else np.clip((cut - lo) / w, 0, 1)
    cc, ww = c * frac, w * frac
    mid = lo + ww / 2
    n = cc.sum()
    mean = (cc * mid).sum() / n
    var = (cc * ((mid - mean) ** 2 + ww ** 2 / 12.0)).sum() / n
    cum = np.cumsum(cc)
    k = int(np.searchsorted(cum, n / 2))
    med = lo[k] + (n / 2 - (cum[k - 1] if k else 0)) / cc[k] * ww[k]
    return n, mean, med, var


def read_hists(main, si):
    f3, s1 = main[5][0], si[1][0]
    jobs = [("3a", "LPS (Li7P3S11)", f3, (133, 56, 738, 430), 169.5, (711.5 - 169.5) / 8, 422.6, (359.5 - 107.0) / 4),
            ("S1a", "LGPS", s1, (177, 110, 581, 366), 201.0, (563.5 - 201.0) / 8, 361.2, (332.5 - 131.5) / 7),
            ("S1b", "LSPS", s1, (735, 110, 1139, 361), 759.5, (1122.0 - 759.5) / 8, 361.0, (317.5 - 143.5) / 4),
            ("S1c", "NPS (Na7P3S11)", s1, (177, 454, 579, 711), 200.0, (563.0 - 200.0) / 8, 704.5, (675.5 - 470.5) / 7)]
    res = {}
    for fig, sse, img, box, xz, p10, yz, p500 in jobs:
        c = read_hist(img, box, xz, p10, yz, p500)
        res[fig] = c
        n, mean, med, var = hist_stats(c)
        print(f"   {fig} {sse}: N(0–80 GPa) ≈ {n:.0f} · 평균 {mean:.2f} · 중앙 {med:.2f} · 표준편차 {np.sqrt(var):.2f} · "
              f"최빈 칸 {2 * int(np.argmax(c))}–{2 * int(np.argmax(c)) + 2} GPa ≈ {c.max():.0f}")
        for b in range(40):
            put(fig[:-1] if fig[0] != "S" else "S1", fig[-1], f"K_crit histogram at 4 V · {sse}", 2 * b + 1, "GPa (bin centre, 2 GPa bins)",
                int(round(c[b])), "count", "figure-read (bar top)")
    return res


def read_bars(si):
    img = si[1][0]
    x0, y0, x1, y1 = 738, 465, 1141, 703
    sub = img[y0:y1 + 1, x0:x1 + 1]
    rows = group([i + y0 for i, f in enumerate((sub.min(axis=2) > 240).mean(axis=1)) if f > 0.25])[:5]
    s, i0, r = fit_axis(rows, [20.0, 17.5, 15.0, 12.5, 10.0])
    out = {}
    for stat, rgb in (("mean", (226, 74, 51)), ("median", (52, 138, 189)), ("std", (152, 142, 213))):
        bl = [b for b in label(color_mask(sub, rgb, 50)) if b[2] > 400 and b[4] - b[3] > 30]
        if len(bl) != 4:
            raise ValueError(f"S1d: expected 4 {stat} bars, found {len(bl)}")
        out[stat] = [s * (b[3] + y0) + i0 for b in bl]
    print(f"   S1d (눈금 잔차 {r:.3f}): " + " | ".join(
        f"{sse} {out['mean'][k]:.2f}/{out['median'][k]:.2f}/{out['std'][k]:.2f}" for k, sse in enumerate(("LGPS", "LSPS", "LPS", "NPS"))))
    for k, sse in enumerate(("LGPS", "LSPS", "LPS (Li7P3S11)", "NPS (Na7P3S11)")):
        for stat in ("mean", "median", "std"):
            put("S1", "d", f"K_crit distribution {stat} at 4 V", sse, "SSE", round(out[stat][k], 2), "GPa",
                "figure-read (bar top)" + (" · text 18.5/14.8/13.0" if k == 2 else ""))
    return out


# ---- 판독: Fig. 3b 원소 칸 색 -------------------------------------------------------------------
PT = {1: {1: "H", 18: "He"},
      2: {1: "Li", 2: "Be", 13: "B", 14: "C", 15: "N", 16: "O", 17: "F", 18: "Ne"},
      3: {1: "Na", 2: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar"},
      4: dict(zip(range(1, 19), "K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split())),
      5: dict(zip(range(1, 19), "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe".split())),
      6: {**{1: "Cs", 2: "Ba"}, **dict(zip(range(4, 19), "Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn".split()))},
      7: {1: "Fr", 2: "Ra"},
      8: dict(zip(range(3, 18), "La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu".split())),
      9: dict(zip(range(3, 18), "Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr".split()))}


def lut_value(rgb, lut_c, lut_v):
    """색 → (값, 색 거리).  거리가 크면 색 막대에 없는 색이다 (회색 = 자료 없음 · 다른 그림)."""
    d = ((lut_c - np.asarray(rgb, float)[None, :]) ** 2).sum(axis=1)
    k = int(np.argmin(d))
    return float(lut_v[k]), float(np.sqrt(d[k]))


def read_ptable(main, x1=868.0, px=36.31, y1=80.0, py=41.0):
    img = main[5][0]
    h, w, _ = img.shape
    xs = [x for x in range(1300, w)
          if int(((img[:, x, :].max(axis=1) - img[:, x, :].min(axis=1)) > 60).sum()) > 150]
    if not xs:
        raise ValueError("Fig. 3b: colour bar not found")
    xc = int(np.median(xs))
    col = img[:, xc - 2:xc + 3, :].mean(axis=1)
    ys = np.where((col.max(axis=1) - col.min(axis=1)) > 25)[0]
    yt, yb = int(ys.min()), int(ys.max())
    tk = group(list(np.where(dark(img)[:, max(xs) + 2:max(xs) + 9].sum(axis=1) >= 3)[0]))
    s, i0, r = fit_axis(tk, [1.0, 0.75, 0.5, 0.25, 0.0, -0.25, -0.5, -0.75, -1.0])
    lut_y = np.arange(yt, yb + 1)
    lut_c, lut_v = col[lut_y], s * lut_y + i0
    out, nodata = {}, []
    for rr, cols in PT.items():
        for cc, el in cols.items():
            cx, cy = x1 + (cc - 1) * px, y1 + (rr - 1) * py
            win = img[int(cy - 14):int(cy + 15), int(cx - 13):int(cx + 14), :].reshape(-1, 3)
            keep = win[win.max(axis=1) > 95]                     # 검정 글자 제외
            med = np.median(keep, axis=0)
            if med.max() - med.min() < 12 and med.mean() < 170:  # 회색 칸 = 자료 없음
                nodata.append(el)
                continue
            v, dist = lut_value(med, lut_c, lut_v)
            if dist > 12:
                raise ValueError(f"Fig. 3b: cell {el} colour {med} is {dist:.1f} away from the colour bar")
            out[el] = (v, dist)
            put("3", "b", "element fraction vs K_crit correlation (all four SSEs · 4 V)", el, "element", round(v, 2),
                "colour-bar value (-1..1)", f"figure-read (cell colour -> colour bar LUT · distance {dist:.1f})")
    srt = sorted(out.items(), key=lambda t: t[1][0])
    print(f"   3b: 색 막대 눈금 잔차 {r:.4f} · 값 있는 원소 {len(out)} · 자료 없음 (회색) {len(nodata)}")
    print("   3b 가장 음 (K_crit 낮춤): " + " ".join(f"{e} {v[0]:+.2f}" for e, v in srt[:9]))
    print("   3b 가장 양 (K_crit 높임): " + " ".join(f"{e} {v[0]:+.2f}" for e, v in srt[-10:]))
    return out, nodata


# ---- 판독: CV (Fig. 5c · S5) · Fig. S2 ----------------------------------------------------------
def envelope(sub, rgb, tol=60):
    cm = color_mask(sub, rgb, tol)
    top = np.full(cm.shape[1], np.nan)
    for x in range(cm.shape[1]):
        ys = np.where(cm[:, x])[0]
        if len(ys):
            top[x] = ys.min()
    return top


def peak_in(v, y, lo, hi, need_prom=0.0):
    """창 [lo, hi] 안의 봉우리 (지형학적 돌출 ≥ need_prom) 중 가장 높은 것의 인덱스.  없으면 ValueError.

    돌출 = 봉우리 값 − max(왼쪽 안장, 오른쪽 안장) · 안장 = 더 높은 점을 만나기 전까지의 최솟값 (끝까지 없으면 끝까지).
    """
    ok = np.where(~np.isnan(y))[0]
    yy = y[ok]
    best = None
    for k in range(2, len(ok) - 2):
        i = ok[k]
        if not (lo <= v[i] <= hi) or yy[k] < yy[k - 2:k + 3].max():
            continue
        higher_l = np.where(yy[:k] > yy[k])[0]
        higher_r = np.where(yy[k + 1:] > yy[k])[0]
        lmin = yy[(higher_l[-1] if len(higher_l) else 0):k + 1].min()
        rmin = yy[k:(k + 1 + higher_r[0] if len(higher_r) else len(yy))].min()
        if yy[k] - max(lmin, rmin) >= need_prom and (best is None or yy[k] > y[best]):
            best = i
    if best is None:
        raise ValueError(f"no peak with prominence >= {need_prom} in [{lo}, {hi}]")
    return best


def read_cv(main, si):
    out = {}
    # Fig. S5 — 절대 축 (전류 1e-5 A).  'Charge' 화살표 (비슷한 파랑) 는 V < 3.0 · I > 1.7 상자로 뺀다.
    s5 = [a for a in si[5] if a.shape[1] == 1427][0]
    m = dark(s5)
    for name, fr in (("Parent", (84, 62, 659, 488)), ("C6", (838, 64, 1412, 488))):
        sx, ix, rx = fit_axis(ticks_along(m, fr, "bottom", 6, 3), [2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
        sy, iy, ry = fit_axis(ticks_along(m, fr, "left", 6, 3), [2.0, 1.5, 1.0, 0.5, 0.0])
        x0, y0, x1, y1 = fr
        sub = s5[y0 + 3:y1 - 2, x0 + 3:x1 - 2].copy()
        v = sx * (np.arange(sub.shape[1]) + x0 + 3) + ix
        ytop_excl = int(round((1.7 - iy) / sy)) - (y0 + 3)       # I = 1.7 의 행
        sub[:max(ytop_excl, 0), v < 3.0] = 255                   # 화살표 상자 지움
        top = envelope(sub, COL["blue"], 70)
        cur = sy * (top + y0 + 3) + iy
        cur[v > 4.2] = np.nan                                    # 범례 · 방전 가지 쪽은 쓰지 않는다
        ip, ib = peak_in(v, cur, 2.55, 3.0, 0.15), peak_in(v, cur, 3.0, 4.0, 0.3)
        out[f"S5 {name}"] = ((v[ip], cur[ip]), (v[ib], cur[ib]))
        print(f"   S5 {name} (잔차 {rx:.4f} V · {ry:.4f}): 프리피크 {v[ip]:.3f} V · {cur[ip] * 10:.2f} µA | "
              f"넓은 봉우리 {v[ib]:.3f} V · {cur[ib] * 10:.2f} µA")
        put("S5", name, "cycle 1 pre-peak", round(float(v[ip]), 3), "V", round(float(cur[ip] * 10), 2), "uA",
            "figure-read (absolute current, not baseline-subtracted)")
        put("S5", name, "cycle 1 broad peak", round(float(v[ib]), 3), "V", round(float(cur[ib] * 10), 2), "uA",
            "figure-read")
    # Fig. 5c — 전류 눈금 없음 (쌓아 그린 곡선).  위치 (V) 와 시작 수준 대비 픽셀 높이만.
    f5 = main[7][0]
    fr = (138, 613, 746, 1040)
    sx, ix, rx = fit_axis(ticks_along(dark(f5), fr, "bottom"), [2, 3, 4, 5, 6, 7, 8, 9])
    x0, y0, x1, y1 = fr
    sub = f5[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
    v = sx * (np.arange(sub.shape[1]) + x0 + 3) + ix
    for lab, cn in (("Parent", "blue"), ("C1.25", "orange"), ("C2.5", "green"), ("C4", "red"), ("C5", "purple"),
                    ("C6", "brown")):
        y = -envelope(sub, COL[cn], 60)
        y[v > 5.5] = np.nan
        ok = np.where(~np.isnan(y))[0]
        base = float(np.median(y[ok[:6]]))
        ip, ib = peak_in(v, y, 2.5, 3.05, 2.0), peak_in(v, y, 3.05, 4.0, 5.0)
        out[f"5c {lab}"] = ((v[ip], y[ip] - base), (v[ib], y[ib] - base), v[ok[0]])
        print(f"   5c {lab:6s}: 시작 {v[ok[0]]:.2f} V | 프리피크 {v[ip]:.2f} V (+{y[ip] - base:.0f} px) | "
              f"넓은 봉우리 {v[ib]:.2f} V (+{y[ib] - base:.0f} px)")
        put("5", "c", f"{lab} pre-peak position", lab, "sample", round(float(v[ip]), 2), "V",
            f"figure-read · height above start {y[ip] - base:.0f} px (no current scale in this panel)")
        put("5", "c", f"{lab} broad-peak position", lab, "sample", round(float(v[ib]), 2), "V",
            f"figure-read · height above start {y[ib] - base:.0f} px")
    return out


def read_s2(si):
    img = si[2][0]
    fr = (168, 142, 738, 566)
    sx, ix, rx = fit_axis(ticks_along(dark(img), fr, "bottom", 6, 3), [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    sy, iy, ry = fit_axis([205.0, 304.0, 549.0], [17.5, 12.5, 0.0])     # 검출되는 y 눈금 셋 (나머지는 가늘어 놓친다)
    x0, y0, x1, y1 = fr
    sub = img[y0 + 3:y1 - 2, x0 + 3:x1 - 2]
    xv = sx * (np.arange(sub.shape[1]) + x0 + 3) + ix
    for lab, cn in (("LCO", "blue"), ("LNO", "orange"), ("LTO", "green"), ("LFPO", "red")):
        cm = color_mask(sub, COL[cn], 70)
        yv = np.full(sub.shape[1], np.nan)
        for j in range(sub.shape[1]):
            ys = np.where(cm[:, j])[0]
            if len(ys):
                kv = sy * (ys + y0 + 3) + iy
                if xv[j] > 0.78:
                    kv = kv[kv < 14.2]                               # 범례 상자
                if len(kv):
                    yv[j] = kv.mean()
        jmax, jmin = int(np.nanargmax(yv)), int(np.nanargmin(yv))
        print(f"   S2 {lab:4s}: 최대 {yv[jmax]:.1f} GPa (x {xv[jmax]:.2f}) · 최소 {yv[jmin]:.1f} GPa (x {xv[jmin]:.2f})")
        put("S2", "-", f"K_crit vs x, (1-x) LPS + x {lab}: maximum", round(float(xv[jmax]), 2), "x", round(float(yv[jmax]), 1),
            "GPa", "figure-read (curve centre)")
        put("S2", "-", f"K_crit vs x, (1-x) LPS + x {lab}: minimum", round(float(xv[jmin]), 2), "x", round(float(yv[jmin]), 1),
            "GPa", "figure-read")
    red = color_mask(sub, COL["red"], 70)
    j0 = int(np.argmin(np.abs(xv - 0.01)))
    k0 = sy * (np.where(red[:, j0])[0].mean() + y0 + 3) + iy
    print(f"   S2 x → 0 (순수 LPS · 네 곡선이 겹친다): {k0:.1f} GPa")
    put("S2", "-", "K_crit at x -> 0 (pure LPS = Li7P3S11; four curves coincide)", 0.01, "x", round(float(k0), 1), "GPa",
        "figure-read · text median of the LPS distribution is 14.8 GPa")
    return k0


# ---- 검산 · 유도량 ------------------------------------------------------------------------------
def spearman(a, b):
    ra, rb = np.argsort(np.argsort(a)), np.argsort(np.argsort(b))
    n = len(a)
    return 1 - 6 * float(((ra - rb) ** 2).sum()) / (n * (n * n - 1))


def checks(res, hists, bars, cv):
    print("== 검산")
    k4 = np.array([p[2] for p in sorted(res["5b"]["blue"])])
    g4 = series_of(res, "5a", "blue")
    k3, g3 = series_of(res, "S4b", "blue"), series_of(res, "S4d", "blue")
    k2, g2 = series_of(res, "S4a", "blue"), series_of(res, "S4c", "blue")
    ks, gs = series_of(res, "S6L", "blue"), series_of(res, "S6R", "blue")
    hl, hr = series_of(res, "5d", "blue"), series_of(res, "5d", "orange")
    for arr, nm in ((k4, "5b K_crit"), (g4, "5a K=0"), (k3, "S4b"), (g3, "S4d K=0"), (k2, "S4a"), (g2, "S4c K=0"),
                    (ks, "S6L"), (gs, "S6R K=0"), (hl, "5d H_L"), (hr, "5d H_R")):
        if np.isnan(arr).any() or len(arr) != 6:
            flag(f"{nm}: 여섯 점이 다 읽히지 않았다 ({arr})")
    # (1) 인쇄값 대조
    d0, d5 = abs(k4[0] - 13.31), abs(k4[4] - 7.60)
    print(f"   (1) Fig. 5b K_crit: 0 % {k4[0]:.2f} ↔ Table 2 13.31 · 5 % {k4[4]:.2f} ↔ 7.60  (차 {d0:.3f} · {d5:.3f})")
    if max(d0, d5) > 0.06:
        flag("Fig. 5b ↔ Table 2 가 0.06 GPa 넘게 어긋난다")
    lps = [bars[s][2] for s in ("mean", "median", "std")]
    dl = max(abs(a - b) for a, b in zip(lps, TXT_LPS))
    print(f"   (2) Fig. S1d LPS {lps[0]:.2f}/{lps[1]:.2f}/{lps[2]:.2f} ↔ 본문 18.5/14.8/13.0  (최대 차 {dl:.2f})")
    if dl > 0.15:
        flag("Fig. S1d ↔ 본문 LPS 통계가 0.15 GPa 넘게 어긋난다")
    # (3) 선형 꼴
    worst = 0.0
    for nm, g, k, ke, key, cn in (("4 V K=5", g4, k4, 5, "5a", "orange"), ("4 V K=10", g4, k4, 10, "5a", "green"),
                                  ("3 V K=3", g3, k3, 3, "S4d", "orange"), ("3 V K=6", g3, k3, 6, "S4d", "green"),
                                  ("2 V K=2", g2, k2, 2, "S4c", "orange"), ("2 V K=4", g2, k2, 4, "S4c", "green"),
                                  ("self 3.5 V K=3", gs, ks, 3, "S6R", "orange"), ("self 3.5 V K=5", gs, ks, 5, "S6R", "green")):
        pred = np.clip(g * (1 - ke / k), 0, None)
        rd = series_of(res, key, cn)
        dd = np.nanmax(np.abs(pred - rd))
        worst = max(worst, dd)
        print(f"   (3) {nm:15s} G0·(1−K/K_crit) = {np.round(pred, 4)}  판독 {np.round(rd, 4)}  최대 차 {dd:.4f}")
    if worst > 0.002:
        flag(f"선형 꼴 최대 차 {worst:.4f} eV/atom > 0.002")
    # (4) Fig. 5c ↔ 5d 눈금
    ratio = np.array([cv[f"5c {s}"][1][1] for s in ("Parent", "C1.25", "C2.5", "C4", "C5", "C6")]) / hr
    print(f"   (4) Fig. 5c 넓은 봉우리 px ÷ Fig. 5d H_R = {np.round(ratio, 2)} px/µA (평균 {ratio.mean():.2f})")
    if (np.abs(ratio / ratio.mean() - 1) > 0.06).any():
        flag("Fig. 5c 곡선들이 같은 전류 눈금이 아니다 (±6 % 초과)")
    # (5) 잘린 분포 ↔ 뿌리 노드 (보고만)
    print(f"   (5) Fig. S3 뿌리 노드 인쇄값: value {ROOT_NODE[0]} · mse {ROOT_NODE[1]} · samples {ROOT_NODE[2]}")
    for fig, sse in (("S1b", "LSPS"), ("S1a", "LGPS"), ("3a", "LPS"), ("S1c", "NPS")):
        n, mean, med, var = hist_stats(hists[fig], 25.0)
        nall = hists[fig].sum()
        print(f"       {sse:4s} ≤ 25 GPa: N ≈ {n:.0f} ({n / nall * 100:.0f} %) · 평균 {mean:.2f} · 분산 {var:.2f}")
        put("S1/3a", "derived", f"{sse} histogram truncated at 25 GPa: mean", 25, "GPa cut", round(mean, 2), "GPa",
            f"OUR ARITHMETIC · N {n:.0f} of {nall:.0f} · variance {var:.2f} · Fig. S3 root node prints value 14.416, mse 27.974")
    print(f"       RMSE {RMSE} GPa ↔ 뿌리 분산 {ROOT_NODE[1]} ⇒ R² ≈ {1 - RMSE ** 2 / ROOT_NODE[1]:.2f} (시험 분산이 뿌리와 같다면)")
    # 유도량 (우리 산술)
    print("== 유도량 (우리 산술 — 논문 값 아님)")
    for nm, g, k in (("계면 2 V", g2, k2), ("계면 3 V", g3, k3), ("계면 4 V", g4, k4), ("자기분해 3.5 V", gs, ks)):
        dv = g / k * EV_PER_GPA_A3
        print(f"   ε_RXN·V⁰ = G0/K_crit  {nm:11s}: {np.round(dv, 2)} Å³/atom")
        for m, x in zip(MOD, dv):
            put("derived", nm, "implied reaction volume eps_RXN*V0 = G0/K_crit", m, "modification %", round(float(x), 2),
                "A^3 per atom", "OUR ARITHMETIC from two figure-read values (not a value of the paper)")
    for i in range(1, 6):
        rk, rg = k4[i] / k4[0], g4[i] / g4[0]
        print(f"   4 V {MOD[i]:>4} %: K_crit ×{rk:.3f} = G0 ×{rg:.3f} ÷ ΔV ×{rg / rk:.3f} → G0 몫 {np.log(rg) / np.log(rk) * 100:.0f} %")
    for nm, a, b in (("H_L ↔ K_crit(4 V)", hl, k4), ("H_L ↔ K_crit(3 V)", hl, k3), ("H_L ↔ 계면 E(3 V, K=0)", hl, g3),
                     ("H_R ↔ 자기분해 E(3.5 V, K=0)", hr, gs), ("H_R ↔ 자기분해 E · child 다섯만", hr[1:], gs[1:])):
        print(f"   Spearman {nm:32s} = {spearman(a, b):+.2f} (n = {len(a)})")
    for ke in (4.6, 4.75, 4.9):
        on = []
        for i in range(6):
            if ke <= k2[i]:
                on.append("≤2.00")
            elif ke <= k3[i]:
                on.append(f"{2 + (ke - k2[i]) / (k3[i] - k2[i]):.2f}")
            else:
                on.append(f"{3 + (ke - k3[i]) / (k4[i] - k3[i]):.2f}")
        print(f"   K_crit(φ) = K_eff 가 되는 전압 (2 · 3 · 4 V 선형 보간 — 우리 가정) K_eff {ke}: {on}")


# ---- 자체 점검 (합성 그림) ---------------------------------------------------------------------
def selftest():
    ok = True

    def expect(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + msg)
        ok = ok and cond
    # (가) 표 검산 — 양성: 인쇄된 두 표는 부모 열이 전부 전하 균형 · 음성: 합이 깨진 조성을 잡는다
    global ROWS
    keep = ROWS
    ROWS = []
    bad = check_tables(verbose=False)
    expect(all(abs(charge(parse_formula(r[0]))) < 0.005 for r in T1 + T2), "부모 유리 20 칸 전부 Σxz ≈ 0")
    expect(sorted((b[1], b[2]) for b in bad) == [(4, "B"), (6, "C")], f"인쇄 그대로 합 ≠ 1 인 칸은 Table 2 의 둘뿐 ({bad})")
    broken = [("Li0.364P0.110S0.388I0.238", "x", 1.0, "Li0.5F0.5", 1.0, "Li0.5F0.5", 1.0, "Li0.5F0.5", 1.0)]
    expect(check_tables((("broken", broken),), verbose=False) == [("broken", 1, "parent", 1.1)], "[음성] 합 1.1 인 조성을 잡는다")
    try:
        parse_formula("Li0.5Xx0.5")
        expect(False, "[음성] 모르는 원소 기호를 조용히 넘기지 않는다")
    except ValueError:
        expect(True, "[음성] 모르는 원소 기호 → ValueError")
    ROWS = keep
    # (나) 마커 판독 — 합성 그림 (테두리 · 눈금 · 선 · 마커) 에서 알려진 값을 되찾는다
    img = np.full((300, 420, 3), 255, int)
    fr = (60, 20, 380, 240)
    img[20:22, 60:381] = 0
    img[239:241, 60:381] = 0
    img[20:241, 60:62] = 0
    img[20:241, 379:381] = 0
    xpix = [80 + 46 * k for k in range(7)]                      # x = 0 … 6
    for xp in xpix:
        img[243:250, xp:xp + 2] = 0
    ypix = [40, 90, 140, 190, 230]                              # y = 4, 3, 2, 1, 0.2
    for yp in ypix:
        img[yp:yp + 2, 50:57] = 0
    truth = {0.0: 3.5, 1.25: 2.0, 2.5: 2.75, 4.0: 1.0, 5.0: 3.0, 6.0: 0.5}
    sx_, ix_, _r = fit_axis([p + 0.5 for p in xpix], [0, 1, 2, 3, 4, 5, 6])
    sy_, iy_, _r = fit_axis([p + 0.5 for p in ypix], [4, 3, 2, 1, 0.2])
    centres = []
    for xv, yv in truth.items():
        cx, cy = int(round((xv - ix_) / sx_)), int(round((yv - iy_) / sy_))
        centres.append((cx, cy))
    for (ax, ay), (bx, by) in zip(centres[:-1], centres[1:]):   # 마커를 잇는 2 px 꺾은선 — 열림이 없으면 전부 한 덩어리가 된다
        for tt in np.linspace(0, 1, 400):
            px_, py_ = int(round(ax + (bx - ax) * tt)), int(round(ay + (by - ay) * tt))
            img[py_:py_ + 2, px_:px_ + 2] = COL["blue"]
    for cx, cy in centres:
        img[cy - 5:cy + 6, cx - 5:cx + 6] = COL["blue"]
    img[30:32, 280:330] = COL["blue"]                           # 범례의 가는 선 (열림으로 지워져야 한다)
    img[26:37, 300:311] = COL["blue"]                           # 범례 마커 (x ≈ 4.9 → 5 % 수준과 0.06 넘게 다르다)
    pts, cal = read_markers(img, fr, [0, 1, 2, 3, 4, 5, 6], [4, 3, 2, 1, 0.2])
    got = dict((p[0], p[1]) for p in pts.get("blue", []))
    expect(len(pts.get("blue", [])) == 6 and set(got) == set(truth) and all(abs(got[k] - truth[k]) < 0.03 for k in truth),
           f"합성 마커 여섯 개를 ±0.03 안으로 되찾고 범례 · 선은 버린다 ({ {k: round(v, 2) for k, v in got.items()} })")
    try:
        read_markers(img, fr, [0, 1, 2, 3, 4, 5], [4, 3, 2, 1, 0.2])
        expect(False, "[음성] 눈금 수가 안 맞으면 멈춘다")
    except ValueError as e:
        expect("tick count mismatch" in str(e), f"[음성] 눈금 7 개에 라벨 6 개 → 우리 가드가 멈춘다 ({str(e)[:60]})")
    # (다) 색 → 값 — 합성 색 막대 (파랑 +1 → 흰 0 → 빨강 −1) · 음성: 막대에 없는 색은 거리가 크다
    t = np.linspace(1, -1, 201)
    lut_c = np.array([[255 * (1 - max(v, 0)), 255 * (1 - abs(v)), 255 * (1 - max(-v, 0))] for v in t])
    v, dist = lut_value([255, 127.5, 127.5], lut_c, t)
    expect(abs(v - (-0.5)) < 0.02 and dist < 3, f"합성 색 막대에서 (255,128,128) → {v:+.2f}")
    v, dist = lut_value([40, 200, 40], lut_c, t)
    expect(dist > 60, f"[음성] 색 막대에 없는 초록은 거리 {dist:.0f} 로 드러난다 (판독기는 12 넘으면 멈춘다)")
    # (라) 순위 상관 · 히스토그램 통계
    expect(abs(spearman(np.array([1, 2, 3, 4.0]), np.array([10, 20, 30, 40.0])) - 1) < 1e-9
           and abs(spearman(np.array([1, 2, 3, 4.0]), np.array([4, 3, 2, 1.0])) + 1) < 1e-9, "Spearman ±1")
    c = np.zeros(40)
    c[5] = 100                                                  # 10–12 GPa 한 칸
    n, mean, med, var = hist_stats(c)
    expect(abs(mean - 11) < 1e-9 and abs(var - 4 / 12) < 1e-9 and abs(med - 11) < 1e-9, "히스토그램 한 칸: 평균 11 · 분산 w²/12")
    n, mean, med, var = hist_stats(c, cut=11.0)
    expect(abs(n - 50) < 1e-9 and abs(mean - 10.5) < 1e-9, "[자르기] 칸 중간에서 자르면 개수 절반 · 평균 10.5")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pdf", help="본문 PDF")
    ap.add_argument("--si", help="ESI PDF")
    ap.add_argument("--out", default=str(ROOT / "litdb" / "figures" / SLUG / "digitized.csv"))
    ap.add_argument("--check", action="store_true", help="판독값 검산 · 유도량도 출력")
    ap.add_argument("--check-only", action="store_true", help="PDF 없이 ESI Table 1 · 2 검산만")
    ap.add_argument("--selftest", action="store_true", help="합성 그림으로 양성 + 음성 경로")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    check_tables()
    if a.check_only:
        return 0
    if not (a.pdf and a.si):
        ap.error("--pdf 와 --si 가 필요하다 (또는 --check-only · --selftest)")
    main_r, si_r = rasters(a.pdf, "main"), rasters(a.si, "si")
    print("== 판독 (전부 figure-read)")
    res = read_line_figs(main_r, si_r)
    emit_line_rows(res)
    hists = read_hists(main_r, si_r)
    bars = read_bars(si_r)
    read_ptable(main_r)
    cv = read_cv(main_r, si_r)
    read_s2(si_r)
    if a.check:
        checks(res, hists, bars, cv)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        f.write("# Fitzhugh 2021 Energy Environ. Sci. 14 4574 - figure readout + ESI table checks. "
                "FIGURE VALUES ARE DIGITIZED (not printed); rows marked OUR ARITHMETIC are derived by us. "
                "tools/litdb/fitzhugh2021_digitize.py\n")
        w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys()))
        w.writeheader()
        w.writerows(ROWS)
    print(f"→ {out}  ({len(ROWS)} 행)")
    if FAIL:
        print(f"⛔ 검산 실패 {len(FAIL)} 건")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
