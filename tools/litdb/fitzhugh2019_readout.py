#!/usr/bin/env python3
"""fitzhugh2019_readout.py — Fitzhugh, Wu, Ye, Deng, Qi, Li, Adv. Energy Mater. 9, 1900807 (2019) **SI 카탈로그 집계 + 그림 판독**.

카드: litdb/papers/fitzhugh2019_ht_functionally_stable_interfaces_sulfide.md  (§5 · §14 · §16)
원본: 본문 PDF (12 쪽) + SI PDF (36 쪽 · 그림 5 쪽 + 카탈로그 29 쪽).  ⚠ PDF 는 리포에 없다 (litdb/inbox 는 gitignore).
      그림은 전부 **내장 래스터** (본문 JPEG · SI PNG) 다 — 벡터 좌표가 없다.  그래서 픽셀에서 읽는다.

⛔ 이 스크립트가 내는 그림 값은 전부 **판독 (figure-read)** 이고 카탈로그 개수는 **우리 집계 (✎)** 다.
   카드 · 표에 옮길 때 `figure-read ≈` / `✎` 표지를 떼지 말 것.  논문이 숫자로 준 것은 본문 문장 (69,640 · 67,062 · 11,935 ·
   "over 1000 / over 2000" · 200 / 97 / 75 meV/atom) 과 Table 1 (항목 수 · 안정 비율) 뿐이다.

무엇을 하나
  (1) SI 카탈로그 (텍스트 층) 파싱: 목록 넷 (음극 기능적 · 음극 잠재적 · 양극 기능적 · 양극 잠재적) 의 항목 수 · 고유 조성 ·
      `*` / `&` 표시 수 · 원소 포함 수 · 논문의 음이온 분류 규칙 (§2.3) 으로 다시 센 클래스별 개수.
  (2) `--lookup <화학식>…`: 그 조성이 어느 목록에 몇 항목 있는지 (예: --lookup Li3PO4 B2O3 SiO2 LiCl).
  (3) 그림 판독 (`--figs`): Fig. 1B (hull 수 막대) · Fig. 2A (LSPS hull energy 곡선 · 창 가장자리 · 기울기) ·
      Fig. 2D · 3B · 3C (클래스 마커) · Fig. 3A (누적 막대) · Fig. 4 (통과율 막대) · Fig. 1D · S2 (원소 칸 색 → 색 막대 값) ·
      Fig. S1A (LSPS–LCO 곡선의 거친 격자 마커 · 최솟값) · Fig. 5G,H (CV 봉우리 위치).
방법
  · 축: ggplot 양식의 흰 격자선 (깨끗한 열 · 행에서 흰 줄) 의 픽셀 중심 ↔ 눈금값의 선형 최소제곱.  잔차를 같이 찍는다.
  · 막대 · 마커: 색 마스크 → 열마다 맨 위 픽셀 (막대) 또는 눈금 열 주변의 색 무게중심 (마커).
  · 색 지도: 칸 안 글자를 피한 자리의 중앙값 색 → 같은 그림 색 막대 (+1 … −1) 에서 가장 가까운 색의 값.
  · CV: 가로축은 음영 띠의 폭 (0–1.5 V 또는 2–4 V) 으로 보정한다 — 눈금 글자를 읽지 않는다.
검증 (`--check` 가 출력 · 문턱을 넘으면 종료 코드 1)
  · 카탈로그 토큰 (mp- / mvc-) 수 = 파싱된 항목 수 (빠진 항목 0) · 조성 분율 합 = 1 ± 0.06.
  · Table 1 항목 수의 합 = 45,580 (본문).
  · Fig. 4 막대 높이 × Table 1 항목 수 = 카탈로그 클래스별 개수 (칸마다 |차| ≤ max(4, 2 %)).  ← 파서와 판독을 서로 검산한다.
  · Fig. 1B 막대 합 = 67,062 · 11,935 (본문 · ±3 %).
  · Fig. 2A 의 2.35 V 위 기울기 = 10/15 eV/V (Li 10 개 / 비-Li 원자 15 개 · ±0.01).
이 도구가 못 하는 것
  · 다른 판본의 PDF — 내장 이미지 크기가 기대와 다르면 **읽지 않고 멈춘다** (격자선 탐침 자리가 이 판본 전용이다).
  · 카탈로그의 '없음' 이 왜 없는지 (어느 조건에서 떨어졌는지) — 논문이 싣지 않았다.  반응 에너지 · 산물 · x_m 도 없다.
  · 조성 대조는 소수 둘째 자리 분율 (± 0.011) 이다 — 다형은 구분하지만 분율이 같은 서로 다른 화합물은 못 가른다.
  · 겹친 마커 (Fig. 2D · 3B 의 낮은 값 · 고전압) 는 틀리게 읽을 수 있다 — 그런 칸은 None 이거나 ±0.05 로 본다.
  · Fig. 1D · S2 의 값은 '색 → 색 막대' 환산이라 0 근처에서 ±0.03 흔들린다.  어떤 상관계수인지는 논문이 적지 않았다.
  · Fig. 5 의 XRD 는 읽지 않는다 (음영 구간은 카드에 눈 + 픽셀 판독으로 적었다).
  · Fig. 4B 의 0.2 % 미만 막대 (O+P · O+N) 는 바닥선에 묻혀 1 픽셀도 안 보인다 — 막대 검산에서 건너뛴다.  그 두 칸은
    초록 선 (개수) 으로만 읽힌다 (≈ 12 · ≈ 4 ↔ 카탈로그 11 · 2).  초록 선은 굵기 4 픽셀이고 뾰족한 꼭짓점 (양극 N) 에서 치우친다.
  · Fig. 4B 의 P 막대는 파랑 뚜껑 위쪽이 초록 선에 가려 있다 — 읽힌 값 (≈ 2.8 %) 은 하한이다.
  · 정규화 (원자당이 Li 포함인지) 는 그림에 적혀 있지 않다 — 기울기 검산은 'Li 제외 원자당' 과 맞는다는 것까지만 말한다.
usage
  ~/.venvs/litdb/bin/python3 tools/litdb/fitzhugh2019_readout.py                 # 카탈로그 집계 (요약)
  ~/.venvs/litdb/bin/python3 tools/litdb/fitzhugh2019_readout.py --figs --check   # 그림 판독 + 검산
  ~/.venvs/litdb/bin/python3 tools/litdb/fitzhugh2019_readout.py --lookup Li3PO4 B2O3 LiCl
  python3 tools/litdb/fitzhugh2019_readout.py --selftest                          # PDF 없이 (numpy 만) 양성 + 음성 경로
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

import numpy as np

SLUG = "fitzhugh2019_ht_functionally_stable_interfaces_sulfide"
ROOT = Path(__file__).resolve().parents[2]
INBOX = ROOT / "litdb" / "inbox"
STEM = "A high throughput search for functionally stable interfaces in sulfide solid state lithium ion conductors"
MAIN_DEFAULT = INBOX / f"122. {STEM}.pdf"
SI_DEFAULT = INBOX / f"122. Sup) {STEM}.pdf"

# ---- 인쇄값 (본문 · Table 1) -------------------------------------------------------------------
TXT = {"n_eval": 69640, "n_iface": 67062, "n_hulls": 11935, "n_anion": 45580}
TABLE1 = {  # 클래스: (항목 수, 음극 범위 안정 %, 양극 범위 안정 %)
    "F": (2902, 0.6, 17.3), "I": (911, 1.1, 13.4), "N": (1808, 0.3, 12.5), "O": (24241, 0.01, 5.7),
    "O+N": (1171, 4.1, 83.9), "O+P": (7469, 0.5, 64.8), "O+S": (1220, 0.3, 13.3), "P": (982, 9.3, 35.7),
    "S": (3150, 4.0, 73.9), "Se": (1726, 5.7, 55.8)}
ANIONS = {"N", "P", "O", "S", "Se", "F", "I"}          # §2.3 의 분류 집합 (Cl · Br · Te 는 없다)
ORDER_A = ["O+P", "O+N", "O", "F", "Se", "S", "O+S", "N", "P", "I"]      # Fig. 4A 가로축 순서
ORDER_B = ["O+P", "O+N", "O+S", "N", "O", "F", "P", "I", "Se", "S"]      # Fig. 4B 가로축 순서
SECTIONS = ["anode_functional", "anode_potential", "cathode_functional", "cathode_potential"]
EXPECT_IMG = {"fig1": (1856, 2268), "fig2": (1750, 1994), "fig3": (1750, 1844), "fig4": (1750, 774),
              "fig5": (2048, 2101), "figS1": (1431, 699), "figS2": (1431, 1441)}
IMG_AT = {"fig1": ("main", 3), "fig2": ("main", 4), "fig3": ("main", 6), "fig4": ("main", 7),
          "fig5": ("main", 9), "figS1": ("si", 2), "figS2": ("si", 3)}
CLASS_RGB = {"O": (63, 81, 159), "S": (230, 39, 41), "Se": (238, 169, 52), "F": (124, 41, 124),
             "P": (250, 190, 200), "N": (18, 128, 65), "I": (205, 85, 180), "O+P": (129, 129, 57),
             "O+N": (119, 115, 114), "O+S": (117, 202, 214)}
FAIL = []


def fail(msg):
    FAIL.append(msg)
    print(f"   ⛔ {msg}")


# ================================ 1. 카탈로그 =====================================================
HEADER_RE = re.compile(r"^\s*(Potentially\s+)?Functionally Stable Anode Coatings for LSPS\s*$")
ENTRY_RE = re.compile(r"([A-Z][A-Za-z0-9.\s]*?)\s*(\*?)(&?)(\*?)\s*:\s*(mp|mvc)-\s*(\d+)")
EL_RE = re.compile(r"([A-Z][a-z]?)(\d\.\d+)")


def composition(formula):
    """'Li0.67S0.33' → {'Li': 0.67, 'S': 0.33}."""
    return {e: float(x) for e, x in EL_RE.findall(formula)}


def parse_catalog(text):
    """SI 텍스트 → {section: [(formula, star, amp, mp_id), …]} + 진단.

    ⚠ SI 는 양극 목록의 제목도 'Anode' 로 인쇄했다 (오식).  그래서 제목 **순서**로 가른다:
      기능적 → 잠재적 → 기능적 → 잠재적 = 음극 · 음극 · 양극 · 양극.  제목이 넷이 아니면 멈춘다.
    """
    lines = text.split("\n")
    heads = [i for i, ln in enumerate(lines) if HEADER_RE.match(ln)]
    kinds = [bool(HEADER_RE.match(lines[i]).group(1)) for i in heads]
    if len(heads) != 4 or kinds != [False, True, False, True]:
        raise ValueError(f"목록 제목이 [기능적, 잠재적, 기능적, 잠재적] 넷이 아니다: {len(heads)}개 {kinds}")
    out, diag = {}, {}
    for name, a, b in zip(SECTIONS, heads, heads[1:] + [len(lines)]):
        body = [ln for ln in lines[a + 1:b]
                if not ln.startswith("=====PAGE") and not re.fullmatch(r"\s*\d{1,2}\s*", ln)]
        chunk = " ".join(body)
        rows = [(re.sub(r"\s+", "", m.group(1)), bool(m.group(2) or m.group(4)), bool(m.group(3)),
                 f"{m.group(5)}-{m.group(6)}") for m in ENTRY_RE.finditer(chunk)]
        n_tok = len(re.findall(r"\b(?:mp|mvc)-", chunk))
        bad = [r[0] for r in rows if abs(sum(composition(r[0]).values()) - 1.0) > 0.06 or not composition(r[0])]
        out[name] = rows
        diag[name] = {"tokens": n_tok, "rows": len(rows), "bad_fraction_sum": bad}
    return out, diag


def anion_class(elements):
    """§2.3 규칙: {N,P,O,S,Se,F,I} 중 하나만 → 그 원소 · O + {N,S,P} 중 하나 → 'O+X' · 그 밖은 None."""
    a = set(elements) & ANIONS
    if len(a) == 1:
        return next(iter(a))
    if len(a) == 2 and "O" in a and (a - {"O"}) <= {"N", "S", "P"}:
        return "O+" + next(iter(a - {"O"}))
    return None


def tally(cat):
    """목록별 요약 dict."""
    res = {}
    for name, rows in cat.items():
        comps = [composition(r[0]) for r in rows]
        cls = collections.Counter(anion_class(c) for c in comps)
        res[name] = {
            "entries": len(rows), "unique_formulas": len({r[0] for r in rows}),
            "star": sum(r[1] for r in rows), "amp": sum(r[2] for r in rows),
            "amp_unique": len({r[0] for r in rows if r[2]}),
            "contains": {e: sum(e in c for c in comps) for e in ("Li", "S", "Se", "O", "F", "Cl", "Br", "I", "N", "P")},
            "class": {k: cls.get(k, 0) for k in TABLE1}, "unclassified": cls.get(None, 0),
            "top_repeats": collections.Counter(r[0] for r in rows).most_common(3)}
    return res


def parse_formula(s):
    """'Li3PO4' · 'B2O3' → 원자 분율 dict.  괄호는 지원하지 않는다 (못 읽으면 ValueError)."""
    toks = re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", s)
    if not toks or "".join(a + b for a, b in toks) != s:
        raise ValueError(f"화학식을 못 읽었다: {s!r} (괄호 · 공백 없이 예: Li3PO4)")
    amt = collections.Counter()
    for el, n in toks:
        amt[el] += float(n) if n else 1.0
    tot = sum(amt.values())
    return {k: v / tot for k, v in amt.items()}


def lookup(cat, formula, tol=0.011):
    """조성이 같은 항목을 목록마다 센다 → {section: [(formula, star, amp, id), …]}."""
    t = parse_formula(formula)
    out = {}
    for name, rows in cat.items():
        hits = []
        for r in rows:
            c = composition(r[0])
            if set(c) == set(t) and all(abs(c[k] - t[k]) <= tol for k in t):
                hits.append(r)
        if hits:
            out[name] = hits
    return out


# ================================ 2. 그림 판독 ====================================================
def runs(mask, off=0):
    out, s = [], None
    for i, v in enumerate(mask):
        if v and s is None:
            s = i
        if not v and s is not None:
            out.append((s + off, i - 1 + off))
            s = None
    if s is not None:
        out.append((s + off, len(mask) - 1 + off))
    return out


def is_white(px, thr=246):
    return px.min(axis=-1) >= thr


def is_red(px):      # ggplot 빨강 #E24A33
    return (px[..., 0] > 190) & (px[..., 1] < 120) & (px[..., 2] < 100)


def is_blue(px):     # ggplot 파랑 #348ABD
    return (px[..., 0] < 110) & (px[..., 1] > 100) & (px[..., 1] < 175) & (px[..., 2] > 150)


def grid_centers(line_px, lo, hi, n_expect, what):
    """한 줄 (열 또는 행) 의 픽셀에서 흰 격자선 중심을 찾는다.  개수가 기대와 다르면 멈춘다."""
    rs = [r for r in runs(is_white(line_px[lo:hi]), off=lo) if r[1] - r[0] <= 6]
    c = [0.5 * (a + b) for a, b in rs]
    if len(c) != n_expect:
        raise RuntimeError(f"{what}: 격자선 {len(c)}개 (기대 {n_expect}) — 다른 판본이거나 탐침 자리가 어긋났다")
    return np.array(c)


def linfit(px, val, what, tol):
    a, b = np.polyfit(np.asarray(px, float), np.asarray(val, float), 1)
    res = np.abs(a * np.asarray(px, float) + b - np.asarray(val, float)).max()
    if res > tol:
        fail(f"{what}: 축 보정 잔차 {res:.4g} > {tol}")
    return a, b


def bar_top(mask_col):
    idx = np.where(mask_col)[0]
    return idx.min() if len(idx) else None


def colour_to_value(cbar_rgb, rgb):
    """색 막대 (위 = +1 · 아래 = −1 · N×3) 에서 가장 가까운 색의 값과 색 거리."""
    d = ((np.asarray(cbar_rgb, float) - np.asarray(rgb, float)) ** 2).sum(axis=1)
    i = int(d.argmin())
    return float(np.linspace(1, -1, len(cbar_rgb))[i]), float(np.sqrt(d[i]))


def marker_value(im, rows, x, rgb, a, b, tol=38, half=5):
    """눈금 열 x 주변 (±half) 에서 그 색 픽셀의 가장 빽빽한 무리의 행 평균 → 축 값.  못 찾으면 None."""
    r0, r1 = rows
    blk = im[r0:r1, x - half:x + half + 1]
    m = np.abs(blk - np.array(rgb)).max(axis=2) < tol
    if m.sum() < 8:
        return None
    rr = np.where(m)[0]
    sm = np.convolve(np.bincount(rr, minlength=r1 - r0), np.ones(9), "same")
    sel = rr[np.abs(rr - sm.argmax()) <= 10]
    return float(a * (r0 + sel.mean()) + b)


def load_images(main_pdf, si_pdf):
    import pymupdf                                    # 지연 임포트 — selftest 는 PyMuPDF 없이 돈다
    docs = {"main": pymupdf.open(main_pdf), "si": pymupdf.open(si_pdf)}
    out = {}
    for name, (which, page) in IMG_AT.items():
        d = docs[which]
        pix = pymupdf.Pixmap(d, d[page].get_images(full=True)[0][0])
        if pix.n - pix.alpha >= 4:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        if (pix.width, pix.height) != EXPECT_IMG[name]:
            raise RuntimeError(f"{name}: 내장 이미지 {pix.width}x{pix.height} ≠ 기대 {EXPECT_IMG[name]} — 다른 판본, 읽지 않는다")
        arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3]
        out[name] = arr.astype(int)
    return out


def read_fig1b(im):
    col = im[:, 187]
    gy = grid_centers(col, 780, 1300, 6, "Fig. 1B y")
    a, b = linfit(gy, [30000, 25000, 20000, 15000, 10000, 5000], "Fig. 1B", 40)
    zero = int(round(-b / a))
    sub = im[760:zero + 2, 150:950]
    res = {}
    for label, mask in (("material", is_red(sub)), ("element_set", is_blue(sub))):
        z = zero - 760
        cols = [r for r in runs(mask[z - 12:z - 2].sum(axis=0) > 3) if r[1] - r[0] > 15]
        vals = []
        for s, e in cols:
            tops = []
            for x in range(s + 4, e - 3):
                r = z - 1
                while r >= 0 and (mask[r, x] or mask[max(r - 3, 0):r, x].any()):
                    r -= 1
                tops.append(r + 1)
            vals.append(float(a * (np.median(tops) + 760) + b))
        res[label] = vals                      # 8 → 5 차원 순서
    return res


def read_fig2a(im):
    gy = grid_centers(im[:, 170], 76, 500, 5, "Fig. 2A y")
    ay, by = linfit(gy, [2.0, 1.5, 1.0, 0.5, 0.0], "Fig. 2A y", 0.01)
    row = im[110:131].sum(axis=(0, 2)).astype(float)
    gx = []
    for guess in (204, 439, 672, 906, 1140, 1376):       # 음영 아래라 흰 줄이 아니다 — 근방의 밝기 극대로 잡는다
        seg = row[guess - 4:guess + 5]
        gx.append(guess - 4 + float(np.mean(np.where(seg == seg.max())[0])))
    ax, bx = linfit(gx, [0, 1, 2, 3, 4, 5], "Fig. 2A x", 0.01)
    pts = []
    for x in range(206, 1376):
        dark = np.where(im[70:495, x].max(axis=1) < 90)[0]
        if len(dark):
            pts.append((ax * x + bx, ay * (70 + np.median(dark)) + by))
    p = np.array(pts)

    def at(v):
        if v < p[0, 0]:                                   # 곡선은 V ≈ 0.007 에서 시작한다 — 0 V 는 첫 구간 기울기로 외삽
            k, c = np.polyfit(p[:25, 0], p[:25, 1], 1)
            return float(k * v + c)
        return float(np.interp(v, p[:, 0], p[:, 1]))

    def slope(v0, v1):
        m = (p[:, 0] >= v0) & (p[:, 0] <= v1)
        return float(np.polyfit(p[m, 0], p[m, 1], 1)[0])

    band = im[110:131, 560:720].mean(axis=0)             # 음영 경계: 빨강 → 초록 → 파랑
    lab = "".join("R" if (c[0] - c[2] > 8 and c[0] - c[1] > 8) else "G" if (c[1] - c[0] > 3 and c[1] - c[2] > 3)
                  else "B" if c[2] - c[0] > 8 else "?" for c in band)
    g = re.search(r"G+", lab)
    if not g:
        raise RuntimeError("Fig. 2A: 초록 (중립) 음영을 못 찾았다")
    lo = 560 + 0.5 * (lab.rfind("R", 0, g.start()) + g.start())      # 빨강 끝과 초록 시작의 가운데
    hi = 560 + 0.5 * (g.end() - 1 + lab.find("B", g.end() - 1))       # 초록 끝과 파랑 시작의 가운데
    edges = (float(ax * lo + bx), float(ax * hi + bx))
    return {"values": {v: round(at(v), 3) for v in (0.0, 0.5, 1.0, 1.5, 2.25, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)},
            "flat_level": round(at(1.9), 3), "window_from_shading": edges,
            "slopes": {"0.02-0.20": slope(0.02, 0.20), "0.5-0.75": slope(0.5, 0.75), "1.05-1.6": slope(1.05, 1.6),
                       "2.08-2.27": slope(2.08, 2.27), "2.35-5": slope(2.35, 5.0)}}


def read_markers(im, col_probe, row_range, n_y, yvals, x_of_v, rows, what):
    gy = grid_centers(im[:, col_probe], row_range[0], row_range[1], n_y, f"{what} y")
    a, b = linfit(gy, yvals, f"{what} y", 0.01)
    out = {}
    for cls, rgb in CLASS_RGB.items():
        out[cls] = [None if (v := marker_value(im, rows, int(round(x_of_v(V))), rgb, a, b)) is None else round(v, 3)
                    for V in np.arange(0, 5.01, 0.5)]
    return out


def read_fig3a(im):
    gy = list(grid_centers(im[:, 222], 100, 500, 4, "Fig. 3A y"))
    a, b = linfit(gy, [0.4, 0.3, 0.2, 0.1], "Fig. 3A y", 0.002)
    sub = im[93:524]
    blue, red = is_blue(sub), is_red(sub)
    cols = [r for r in runs(blue.sum(axis=0) > 5) if r[1] - r[0] > 40]
    names = ["S", "Se", "I", "P", "N", "O+S", "O+P", "F", "O+N", "O"]
    if len(cols) != 10:
        raise RuntimeError(f"Fig. 3A: 막대 {len(cols)}개 (기대 10)")
    out = {}
    for nm, (s, e) in zip(names, cols):
        s = max(s, e - 102)                               # 첫 막대 (S) 는 왼쪽의 범례 파랑 조각과 붙어 잡힌다 — 막대 폭 (≈ 101) 만 쓴다
        xs = range(s + 12, e - 12)
        tb = np.median([bar_top(blue[:, x]) for x in xs if blue[:, x].any()]) + 93
        tr = np.median([bar_top(red[:, x]) for x in xs if red[:, x].any()]) + 93
        mid = (s + e) // 2
        dark = np.where(sub[:, mid].max(axis=1) < 70)[0] + 93
        top = np.mean([r for r in dark if tr - 12 <= r < tr + 2])   # 빨강 바로 위 검은 테두리의 중심 = 전체 높이 (범례 글자 제외)
        out[nm] = {"total": round(float(a * top + b), 3), "interface": round(float(a * tb + b), 3)}
        out[nm]["intrinsic"] = round(out[nm]["total"] - out[nm]["interface"], 3)
    return out


def read_fig4(im):
    def green(px):
        return (px[..., 1] > 110) & (px[..., 0] < 110) & (px[..., 2] < 130) & (px[..., 1] - px[..., 0] > 50)
    spec = {"anode": (90, 700, 99, (150, 600), [4, 3, 2, 1], [141.5 + 55 * i for i in range(10)], ORDER_A, 4),
            "cathode": (980, 1600, 992, (100, 640), [35, 30, 25, 20, 15, 10, 5],
                        [1034, 1089, 1145, 1199.5, 1254.5, 1309, 1364, 1419, 1474.5, 1529.5], ORDER_B, 7)}
    ticks = {"anode": ([165.5, 286.5, 409, 530.5, 652], [40, 30, 20, 10, 0]),          # 오른쪽 축 눈금 (개수) 의 행
             "cathode": ([99.5, 191.5, 284.5, 376.5, 468.5, 561, 653], [1200, 1000, 800, 600, 400, 200, 0])}
    out = {"count_line": {}, "px_per_pct": {}}
    for side, (xl, xr, probe, rr, yv, cats, names, n) in spec.items():
        gy = grid_centers(im[:, probe], rr[0], rr[1], n, f"Fig. 4 {side} y")
        a, b = linfit(gy, yv, f"Fig. 4 {side} y", 0.06)
        out["px_per_pct"][side] = abs(1.0 / a)
        ca, cb_ = np.polyfit(*ticks[side], 1)
        sub = im[:, xl:xr]
        red = is_red(sub)
        cap = (sub[..., 2] - sub[..., 0] > 40) & (sub[..., 2] > 120)      # JPEG 로 번진 파랑까지 (초록 선은 B < 120 이라 빠진다)
        grn = green(sub)
        out["count_line"][side] = {}
        for cx, nm in zip(cats, names):                  # 초록 선 (기능적 + 잠재적 개수) — 선 굵기 4 픽셀 · 뾰족한 꼭짓점은 치우친다
            rows_ = np.where(grn[:, int(round(cx)) - xl - 1:int(round(cx)) - xl + 2].any(axis=1))[0]
            out["count_line"][side][nm] = None if not len(rows_) else round(float(ca * rows_.mean() + cb_), 1)
        res = {}
        for cx, nm in zip(cats, names):
            x = int(round(cx)) - xl
            xs = range(x - 12, x + 13)
            rt = [bar_top(red[:, q]) for q in xs if red[:, q].any()]
            f = float(a * np.median(rt) + b) if len(rt) >= 8 else 0.0
            bt = []                                          # 파랑 (잠재적) 뚜껑: 빨강 꼭대기 바로 위의 파랑 줄 (1–2 픽셀짜리도 잡는다)
            if len(rt) >= 8:
                top_red = int(np.median(rt))
                for q in xs:                                 # 빨강 꼭대기에서 위로 이어진 파랑만 (3 픽셀 틈까지 허용)
                    r = top_red - 1
                    while r >= 0 and (cap[r, q] or cap[max(r - 3, 0):r, q].any()):
                        r -= 1
                    if top_red - (r + 1) >= 2:
                        bt.append(r + 1)
            p = float(a * np.median(bt) + b) if len(bt) > 12 else None
            res[nm] = (round(f, 3), None if p is None else round(p, 3))
        out[side] = res
    return out


PT = [["H"] + [None] * 16 + ["He"],
      ["Li", "Be"] + [None] * 10 + ["B", "C", "N", "O", "F", "Ne"],
      ["Na", "Mg"] + [None] * 10 + ["Al", "Si", "P", "S", "Cl", "Ar"],
      ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr"],
      ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe"],
      ["Cs", "Ba", None, "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn"],
      ["Fr", "Ra"] + [None] * 16]
LAN = ["La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]
ACT = ["Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"]


def read_ptable(im, bands, fbands, x0, pitch, cbar, dx=(-24, -6), dy=(12, 27)):
    """주기율표 색 지도 한 장 → {원소: 값 또는 None(회색 = 50 구조 미만)}.  bands = 행 띠 7 개 · fbands = La/Ac 띠."""
    (cx0, cx1), (cy0, cy1) = cbar
    cb = im[cy0:cy1 + 1, cx0:cx1 + 1].mean(axis=1)
    out, worst = {}, 0.0

    def put(el, a, b, k):
        nonlocal worst
        yc, xc = (a + b) // 2, int(x0 + pitch * k + pitch * 0.45)
        c = np.median(im[yc + dy[0]:yc + dy[1], xc + dx[0]:xc + dx[1]].reshape(-1, 3), axis=0)
        if abs(c[0] - c[1]) < 8 and abs(c[1] - c[2]) < 8 and c[0] < 150:
            out[el] = None
        else:
            v, err = colour_to_value(cb, c)
            out[el], worst = round(v, 2), max(worst, err)
    for ri, (a, b) in enumerate(bands):
        for ci, el in enumerate(PT[ri]):
            if el:
                put(el, a, b, ci)
    for (a, b), names in zip(fbands, (LAN, ACT)):
        for k, el in enumerate(names):
            put(el, a, b, 2 + k)
    return out, worst


def read_colour_maps(imgs):
    res = {}
    b1 = [(1569, 1637), (1644, 1712), (1720, 1788), (1795, 1863), (1870, 1938), (1946, 2013), (2021, 2088)]
    res["chem"], w = read_ptable(imgs["fig1"], b1, [(2097, 2164), (2172, 2239)], 302, 68.53,
                                 ((1620, 1632), (1561, 2243)))
    worst = w
    for lab, off in (("0V", 60), ("2V", 500), ("4V", 940)):          # Fig. S2 세 장: 같은 배치가 세로로 436/437 픽셀씩
        sub = imgs["figS2"]
        top = {"0V": 83, "2V": 539, "4V": 996}[lab]
        bands = [(top + int(round(43.2 * i)), top + int(round(43.2 * i)) + 40) for i in range(7)]
        fb = [(top + 303, top + 343), (top + 346, top + 386)]
        res[lab], w = read_ptable(sub, bands, fb, 180.8, 49.294, ((1128, 1132), (top + 2, top + 384)),
                                  dx=(-12, -4), dy=(6, 12))
        worst = max(worst, w)
    return res, worst


def read_figs1a(im):
    ay, by = linfit(grid_centers(im[:, 151], 100, 610, 9, "Fig. S1A y"),
                    [0, -0.05, -0.10, -0.15, -0.20, -0.25, -0.30, -0.35, -0.40], "Fig. S1A y", 0.002)
    ax, bx = linfit(grid_centers(im[600, :], 150, 705, 6, "Fig. S1A x"), [0, 0.2, 0.4, 0.6, 0.8, 1.0], "Fig. S1A x", 0.003)
    sub = im[100:615, 149:707]
    dark = sub.max(axis=2) < 60
    seen = np.zeros(dark.shape, bool)
    pts = []
    for y, x in zip(*np.where(dark)):                 # 연결성분 — × 마커 (72–84 픽셀) 만 남긴다 (범례 글자는 더 작다)
        if seen[y, x]:
            continue
        stack, comp = [(y, x)], []
        seen[y, x] = True
        while stack:
            yy, xx = stack.pop()
            comp.append((yy, xx))
            for dy_ in (-1, 0, 1):
                for dx_ in (-1, 0, 1):
                    ny, nx = yy + dy_, xx + dx_
                    if 0 <= ny < dark.shape[0] and 0 <= nx < dark.shape[1] and dark[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        if 66 <= len(comp) <= 90:
            c = np.array(comp)
            pts.append((round(float(ax * (c[:, 1].mean() + 149) + bx), 3), round(float(ay * (c[:, 0].mean() + 100) + by), 3)))
    pts = sorted(p for p in pts if p[1] < -0.005 or p[0] > 0.9)      # 범례의 × 표본 (ΔG ≈ −0.02 근처 · x ≈ 0.18) 제거
    pts = [p for p in pts if not (0.15 < p[0] < 0.2 and p[1] > -0.05)]
    gray = np.abs(sub - 128).max(axis=2) < 25
    ys = np.where(gray)[0]
    return {"coarse_points": pts, "x0_value": pts[0][1] if pts else None,
            "curve_min": round(float(ay * (ys.max() - 2 + 100) + by), 3)}


def read_cv(im):
    sub = im[1300:2050]
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    green = (G > 170) & (G - R > 25) & (G - B > 25)
    gr = [r for r in runs(green.mean(axis=0) > 0.02) if r[1] - r[0] > 15]
    if len(gr) < 2:
        raise RuntimeError("Fig. 5G,H: 초록 음영 띠를 못 찾았다")
    g0, g1 = gr[0]                                     # 패널 G: 0–1.5 V
    px_per_v = (g1 - g0) / 1.5
    mag = (R > 140) & (B > 120) & (G < 130) & (R - G > 45) & (B - G > 30)
    xs = [x for x in np.where(mag.any(axis=0))[0] if 200 <= x < 980]
    top = {x: np.where(mag[:, x])[0].min() for x in xs}
    V = {x: (x - g0) / px_per_v for x in xs}
    base = np.median([top[x] for x in xs if 1.8 < V[x] < 3.0])
    pk = min(xs, key=lambda x: top[x])
    h = base - top[pk]
    out = {"li2s_peak_V": round(float(V[pk]), 2)}
    for frac in (0.05, 0.5):
        out[f"li2s_rise_{int(frac * 100)}pct_V"] = round(float(min(V[x] for x in xs if 2.5 < V[x] < V[pk] and base - top[x] >= frac * h)), 2)
    h0, h1 = gr[1][0], gr[-1][1]                       # 패널 H: 2–4 V 띠 (조각 여럿이면 처음과 끝)
    ppv = (h1 - h0) / 2.0
    v0 = h0 - 2 * ppv
    cur = (B > 120) & (R < 110) & (G < 110) & (B - R > 50)
    cx = [x for x in np.where(cur.any(axis=0))[0] if 0 <= (x - v0) / ppv <= 2.0]
    mid = np.median([(np.where(cur[:, x])[0].min() + np.where(cur[:, x])[0].max()) / 2
                     for x in np.where(cur.any(axis=0))[0] if 2.5 < (x - v0) / ppv < 3.8])
    up = max(cx, key=lambda x: mid - np.where(cur[:, x])[0].min())
    dn = max(cx, key=lambda x: np.where(cur[:, x])[0].max() - mid)
    out.update({"panelH_anodic_peak_V": round(float((up - v0) / ppv), 2), "panelH_cathodic_peak_V": round(float((dn - v0) / ppv), 2),
                "panelH_cathodic_over_anodic": round(float((np.where(cur[:, dn])[0].max() - mid) / (mid - np.where(cur[:, up])[0].min())), 2)})
    return out


# ================================ 3. 검산 =========================================================
def check_fig4_vs_catalog(fig4, summary):
    """Fig. 4 막대 × Table 1 항목 수 ↔ 카탈로그 클래스 개수.  어긋난 칸 목록을 돌려준다."""
    bad = []
    for side, fn, pn in (("anode", "anode_functional", "anode_potential"), ("cathode", "cathode_functional", "cathode_potential")):
        ppp = (fig4.get("px_per_pct") or {}).get(side)           # 축의 픽셀/% — 3 픽셀이 안 되는 막대는 바닥선에 묻혀 못 읽는다
        for cls, (f, p) in fig4[side].items():
            n = TABLE1[cls][0]
            pairs = [(f / 100 * n, summary[fn]["class"][cls], "기능적")]
            if p is not None:
                pairs.append((p / 100 * n, summary[fn]["class"][cls] + summary[pn]["class"][cls], "기능적+잠재적"))
            for est, cnt, what in pairs:
                if ppp and max(est, cnt) / n * 100 * ppp < 3.0:
                    continue                                     # 판독 하한 밑 (양극 패널의 O+P · O+N)
                if abs(est - cnt) > max(4.0, 0.02 * cnt):
                    bad.append(f"{side} {cls} {what}: 막대×항목 {est:.1f} ↔ 카탈로그 {cnt}")
    return bad


def check_all(summary, diag, figs):
    print("\n=== 검산")
    for name in SECTIONS:
        d = diag[name]
        if d["tokens"] != d["rows"]:
            fail(f"{name}: mp/mvc 토큰 {d['tokens']} ≠ 파싱 항목 {d['rows']}")
        if d["bad_fraction_sum"]:
            fail(f"{name}: 분율 합 ≠ 1 인 조성 {d['bad_fraction_sum'][:3]}")
    s1 = sum(v[0] for v in TABLE1.values())
    print(f"   Table 1 항목 합 {s1:,} ↔ 본문 {TXT['n_anion']:,}")
    if s1 != TXT["n_anion"]:
        fail("Table 1 합 불일치")
    if summary["anode_functional"]["entries"] <= 1000 or summary["cathode_functional"]["entries"] <= 2000:
        fail("목록 크기가 본문의 'over 1000 / over 2000' 과 안 맞는다")
    if not figs:
        print("   (그림 검산은 --figs 와 함께)")
        return
    bad = check_fig4_vs_catalog(figs["fig4"], summary)
    print(f"   Fig. 4 막대 × Table 1 ↔ 카탈로그: 어긋난 칸 {len(bad)}")
    for b in bad:
        fail(b)
    for label, target in (("material", TXT["n_iface"]), ("element_set", TXT["n_hulls"])):
        tot = sum(figs["fig1b"][label])
        print(f"   Fig. 1B {label} 막대 합 {tot:,.0f} ↔ 본문 {target:,}  ({100 * (tot / target - 1):+.1f} %)")
        if abs(tot / target - 1) > 0.03:
            fail(f"Fig. 1B {label} 합이 3 % 넘게 어긋난다")
    sl = figs["fig2a"]["slopes"]["2.35-5"]
    print(f"   Fig. 2A 2.35 V 위 기울기 {sl:.3f} eV/V ↔ 10/15 = 0.667")
    if abs(sl - 10 / 15) > 0.01:
        fail("Fig. 2A 산화 구간 기울기가 Li 10 / 비-Li 15 와 안 맞는다")


# ================================ 4. 출력 =========================================================
def print_summary(summary, diag):
    print(f"=== SI 카탈로그 집계 (✎ 우리 집계 — 논문 값 아님) · {SLUG}")
    print("목록                 항목  고유조성    *     &  (&고유)  Li함유  열클래스밖  파싱")
    for name in SECTIONS:
        s, d = summary[name], diag[name]
        print(f"{name:<19} {s['entries']:>5} {s['unique_formulas']:>8} {s['star']:>5} {s['amp']:>5} {s['amp_unique']:>7} "
              f"{s['contains']['Li']:>7} {s['unclassified']:>10}  {d['rows']}/{d['tokens']}")
    for side, fn, pn in (("음극 (0 V)", "anode_functional", "anode_potential"), ("양극 (4 V)", "cathode_functional", "cathode_potential")):
        print(f"--- {side} 클래스별 기능적 + 잠재적:  "
              + "  ".join(f"{k} {summary[fn]['class'][k]}+{summary[pn]['class'][k]}" for k in ORDER_B))


def print_figs(figs):
    print("\n=== 그림 판독 (figure-read ≈)")
    print("Fig. 1B  물질 순회 (8→5D):", [int(round(v, -1)) for v in figs["fig1b"]["material"]],
          "· 원소 집합:", [int(round(v, -1)) for v in figs["fig1b"]["element_set"]])
    f2 = figs["fig2a"]
    print("Fig. 2A  LSPS hull energy:", f2["values"])
    print(f"         평탄 구간 값 {f2['flat_level']} · 음영 창 {f2['window_from_shading'][0]:.3f}–{f2['window_from_shading'][1]:.3f} V"
          f" · 기울기 → Li/15: " + " · ".join(f"{k} V {abs(v) * 15:.1f}" for k, v in f2["slopes"].items()))
    print("Fig. 3A  [전체 / 계면 몫 / 고유 몫] eV/atom:",
          "  ".join(f"{k} {v['total']}/{v['interface']}/{v['intrinsic']}" for k, v in figs["fig3a"].items()))
    print("   (아래 세 줄: 마커가 겹친 칸은 틀릴 수 있다 — 특히 Fig. 3B 의 4–5 V · Fig. 2D 의 2 V 근처. — 는 못 찾음)")
    for name, idx, vs in (("Fig. 3C 계면 몫", (3, 4, 5, 6, 8, 10), "1.5/2/2.5/3/4/5 V"), ("Fig. 3B 전체", (4, 8, 10), "2/4/5 V"),
                          ("Fig. 2D 재료 수준", (0, 4, 8, 10), "0/2/4/5 V")):
        key = {"Fig. 3C 계면 몫": "fig3c", "Fig. 3B 전체": "fig3b", "Fig. 2D 재료 수준": "fig2d"}[name]
        print(f"{name} ({vs}):", "  ".join(f"{k} " + "/".join("—" if figs[key][k][i] is None else f"{figs[key][k][i]:.2f}" for i in idx)
                                           for k in CLASS_RGB))
    for side in ("anode", "cathode"):
        print(f"Fig. 4 {side} 통과율 % (기능적 → +잠재적):",
              "  ".join(f"{k} {f:.2f}" + ("" if p is None else f"→{p:.2f}") for k, (f, p) in figs["fig4"][side].items()))
        print(f"       {side} 초록 선 개수 (선 굵기 ±3 · 꼭짓점이 뾰족한 칸은 더 치우친다):",
              "  ".join(f"{k} {v}" for k, v in figs["fig4"]["count_line"][side].items()))
    print(f"       (막대 판독 하한 = 3 픽셀: 음극 {3 / figs['fig4']['px_per_pct']['anode']:.3f} % · 양극 {3 / figs['fig4']['px_per_pct']['cathode']:.2f} % — "
          "그 밑은 바닥선에 묻힌다)")
    want = ["S", "Se", "Te", "I", "Cl", "Br", "P", "B", "F", "Si", "Li", "N", "O", "Al", "Mg", "Zr", "Nd", "La", "Sc"]
    for lab, name in (("chem", "Fig. 1D 화학"), ("0V", "Fig. S2A 0 V"), ("2V", "Fig. S2B 2 V"), ("4V", "Fig. S2C 4 V")):
        m = figs["maps"][lab]
        print(f"{name}:", "  ".join(f"{e} {'회색' if m[e] is None else format(m[e], '+.2f')}" for e in want))
    s1 = figs["figs1a"]
    print(f"Fig. S1A LSPS–LCO: x = 0 에서 {s1['x0_value']} · 곡선 최솟값 {s1['curve_min']} · 거친 격자 마커 {len(s1['coarse_points'])}개")
    print("Fig. 5G,H CV:", figs["cv"])


# ================================ 5. selftest =====================================================
def selftest():
    ok = []

    def expect(cond, name):
        ok.append(bool(cond))
        print(f"   {'✓' if cond else '✗'} {name}")

    head = ["Functionally Stable Anode Coatings for LSPS", "Potentially Functionally Stable Anode Coatings for LSPS",
            "Functionally Stable Anode Coatings for LSPS", "Potentially Functionally Stable Anode Coatings for LSPS"]
    text = "\n".join([
        "CATALOG CONTENTS", "Functionally Stable Anode Coatings for LSPS ………… 7",       # 목차 줄은 제목이 아니다
        head[0], "Li0.67S0.33*:   mp-1153 ", "Nd0.40S0.20O0.40:   mp-3211", "Al0.50Co0.50:   mp-284", "7",
        head[1], "Li0.50Ga0.25Ir0. 25:   mp-31441",                                        # 화학식 안의 공백
        head[2], "Si0.33O0.67*&:   mp-7000", "Ag0.17As0.17Pb0.17S0.50*:   mp-", "22665",   # 줄바꿈된 id
        "Cs0.02Mg0.07Al0.15Si0.15O0.61*& :   mp-695133", "Li0.14Co0.29S0.57*:   mvc-16740",
        head[3], "Li0.67S0.33*:   mp-1153"])
    cat, diag = parse_catalog(text)
    expect([len(cat[s]) for s in SECTIONS] == [3, 1, 4, 1], "양성: 목록 넷의 항목 수 3 · 1 · 4 · 1")
    expect(all(diag[s]["tokens"] == diag[s]["rows"] for s in SECTIONS), "양성: 토큰 수 = 항목 수 (줄바꿈 id · mvc 포함)")
    expect(cat["cathode_functional"][0] == ("Si0.33O0.67", True, True, "mp-7000")
           and cat["cathode_functional"][1][1:3] == (True, False), "양성: * 와 & 를 따로 읽는다 (*& ↔ * 만)")
    expect(cat["cathode_functional"][1][3] == "mp-22665", "양성: 줄바꿈된 mp- 번호를 잇는다")
    expect(cat["anode_potential"][0][0] == "Li0.50Ga0.25Ir0.25", "양성: 화학식 안의 공백을 지운다")
    s = tally(cat)
    expect(s["anode_functional"]["class"]["O+S"] == 1 and s["anode_functional"]["class"]["S"] == 1
           and s["anode_functional"]["unclassified"] == 1, "양성: 음이온 분류 (O+S · S · 분류 밖)")
    expect(anion_class({"Ba", "Br", "O"}) == "O" and anion_class({"Ca", "P", "I"}) is None
           and anion_class({"Na", "P", "S", "O"}) is None, "양성: Br 은 분류 집합 밖 · 두 음이온 (P+I) 과 세 음이온은 분류 안 함")
    expect(set(lookup(cat, "Li2S")) == {"anode_functional", "cathode_potential"} and not lookup(cat, "Li3PO4"),
           "양성: 조성 조회 (Li2S 는 두 목록 · Li3PO4 는 없음)")
    expect(not lookup(cat, "LiS") and not lookup(cat, "Li3S"), "음성: 원소가 같아도 분율이 다르면 (LiS · Li3S) 안 맞는다")
    try:                                                # 음성 1: 제목이 셋뿐이면 조용히 세지 않고 멈춘다
        parse_catalog("\n".join([head[0], "Li0.67S0.33*: mp-1", head[1], "Li0.50F0.50: mp-2", head[2], "C1.00: mp-3"]))
        expect(False, "음성: 제목 셋 → 멈춤")
    except ValueError:
        expect(True, "음성: 제목 셋 → 멈춤")
    _, d2 = parse_catalog("\n".join([head[0], "Li0.67S0.63: mp-1", "S1.00 mp-9", head[1], head[2], head[3]]))
    expect(d2["anode_functional"]["bad_fraction_sum"] == ["Li0.67S0.63"], "음성: 분율 합 ≠ 1 을 잡는다")
    expect(d2["anode_functional"]["tokens"] == 2 and d2["anode_functional"]["rows"] == 1, "음성: 콜론 빠진 항목은 토큰 ≠ 항목으로 드러난다")
    try:
        parse_formula("Li3(PO4)")
        expect(False, "음성: 괄호 화학식 → 거부")
    except ValueError:
        expect(True, "음성: 괄호 화학식 → 거부")
    # 합성 그림: 회색 바탕 + 흰 격자선 5 줄 + 빨간 막대 (값 0.30)
    img = np.full((220, 120, 3), 229, int)
    rows_ = [20, 60, 100, 140, 180]                     # 0.4 · 0.3 · 0.2 · 0.1 · 0.0
    for r in rows_:
        img[r - 1:r + 2] = 255
    img[60:181, 40:80] = (226, 74, 51)
    gy = grid_centers(img[:, 10], 0, 220, 5, "selftest")
    a, b = linfit(gy, [0.4, 0.3, 0.2, 0.1, 0.0], "selftest", 1e-6)
    expect(abs(a * bar_top(is_red(img)[:, 60]) + b - 0.30) < 0.003, "양성: 격자선 보정 + 막대 꼭대기 = 0.30")
    try:
        grid_centers(img[:, 10], 0, 220, 6, "selftest")
        expect(False, "음성: 격자선 개수가 기대와 다르면 멈춤")
    except RuntimeError:
        expect(True, "음성: 격자선 개수가 기대와 다르면 멈춤")
    cbar = np.stack([np.linspace(0, 255, 201), np.full(201, 100.0), np.linspace(255, 0, 201)], axis=1)
    v, err = colour_to_value(cbar, cbar[50])
    expect(abs(v - 0.5) < 1e-9 and err < 1e-9, "양성: 색 → 색 막대 값 (+0.5)")
    mk = np.full((100, 40, 3), 229, int)
    mk[30:41, 15:26] = CLASS_RGB["S"]
    expect(abs(marker_value(mk, (0, 100), 20, CLASS_RGB["S"], -0.01, 1.0) - 0.65) < 0.01
           and marker_value(mk, (0, 100), 20, CLASS_RGB["N"], -0.01, 1.0) is None, "양성/음성: 마커 색 무게중심 · 없는 색은 None")
    fake = {n: {"class": {k: 0 for k in TABLE1}} for n in SECTIONS}
    fake["cathode_functional"]["class"]["S"] = 1103
    fig4 = {"anode": {k: (0.0, None) for k in ORDER_A}, "cathode": {k: (0.0, None) for k in ORDER_B}}
    fig4["cathode"]["S"] = (34.92, None)
    expect(check_fig4_vs_catalog(fig4, fake) == [], "양성: 34.92 % × 3,150 ≈ 1,103 은 통과")
    fig4["cathode"]["S"] = (30.0, None)
    expect(len(check_fig4_vs_catalog(fig4, fake)) == 1, "음성: 30 % 로 잘못 읽으면 검산이 잡는다")
    print(f"selftest {sum(ok)}/{len(ok)}")
    return 0 if all(ok) else 1


def main():
    ap = argparse.ArgumentParser(description="Fitzhugh 2019 AEM — SI 카탈로그 집계 + 그림 판독 (figure-read · ✎)")
    ap.add_argument("--pdf", default=str(MAIN_DEFAULT), help="본문 PDF (기본: litdb/inbox 의 122 번)")
    ap.add_argument("--si", default=str(SI_DEFAULT), help="SI PDF")
    ap.add_argument("--figs", action="store_true", help="그림 판독까지")
    ap.add_argument("--check", action="store_true", help="검산 (문턱을 넘으면 종료 코드 1)")
    ap.add_argument("--lookup", nargs="+", metavar="FORMULA", help="조성 조회 (예: Li3PO4 B2O3)")
    ap.add_argument("--json", metavar="PATH", help="집계 · 판독을 JSON 으로 저장")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    for p in (a.pdf, a.si):
        if not Path(p).exists():
            print(f"⛔ PDF 없음: {p}\n   litdb/inbox 는 gitignore 다 — --pdf / --si 로 경로를 준다.")
            return 2
    import pymupdf
    text = "".join(f"\n=====PAGE {i + 1}=====\n" + pg.get_text() for i, pg in enumerate(pymupdf.open(a.si)))
    cat, diag = parse_catalog(text)
    summary = tally(cat)
    print_summary(summary, diag)
    if a.lookup:
        print("\n=== 조회 (LSPS 기준 · '없음' 의 이유는 논문에 없다)")
        for f in a.lookup:
            hits = lookup(cat, f)
            print(f"   {f:<10}", " | ".join(f"{k}: {len(v)}항목 [{v[0][0]}{'*' if v[0][1] else ''}{'&' if v[0][2] else ''} {v[0][3]}]"
                                             for k, v in hits.items()) or "— 어느 목록에도 없음")
    figs = None
    if a.figs:
        im = load_images(a.pdf, a.si)
        maps, worst = read_colour_maps(im)
        figs = {"fig1b": read_fig1b(im["fig1"]), "fig2a": read_fig2a(im["fig2"]), "fig3a": read_fig3a(im["fig3"]),
                "fig3c": read_markers(im["fig3"], 240, (1340, 1730), 5, [0.4, 0.3, 0.2, 0.1, 0.0],
                                      lambda V: 278.5 + 232.4 * V, (1320, 1730), "Fig. 3C"),
                "fig3b": read_markers(im["fig3"], 240, (760, 1131), 5, [2.0, 1.5, 1.0, 0.5, 0.0],
                                      lambda V: 278.5 + 232.4 * V, (740, 1140), "Fig. 3B"),
                "fig2d": read_markers(im["fig2"], 170, (1420, 1880), 5, [2.0, 1.5, 1.0, 0.5, 0.0],
                                      lambda V: 211.1 + 231.2 * V, (1380, 1885), "Fig. 2D"),
                "fig4": read_fig4(im["fig4"]), "maps": maps, "figs1a": read_figs1a(im["figS1"]), "cv": read_cv(im["fig5"])}
        print_figs(figs)
        print(f"   (색 지도의 색 대조 최대 거리 {worst:.1f} / 255)")
    if a.check:
        check_all(summary, diag, figs)
    if a.json:
        Path(a.json).write_text(json.dumps({"summary": summary, "diag": diag, "figs": figs}, ensure_ascii=False, indent=1,
                                           default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)), encoding="utf-8")
        print(f"→ {a.json}")
    if FAIL:
        print(f"\n⛔ 검산 실패 {len(FAIL)}건")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
