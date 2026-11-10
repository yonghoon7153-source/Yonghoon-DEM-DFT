#!/usr/bin/env python3
"""wang2022_two_parameter_readout.py — Wang, Ye, Chen & Li, JACS Au 2, 886 (2022) 그림 재판독.

카드: litdb/papers/wang2022_two_parameter_space_dendrite_constriction.md  (§5.3 · §6.2 · §6.3)
원본: litdb/inbox/ 의 본문 PDF (12 쪽) + SI PDF (13 쪽).  ⚠ PDF 는 리포에 없다 (litdb/inbox 는 .gitignore).

⛔ 이 스크립트가 내는 값은 전부 **그림 판독**이다 — 카드에 옮길 때 `figure-read ≈` 표지를 떼지 말 것.
   이 논문의 그림은 전부 PDF 에 박힌 **래스터**다 (벡터 경로 없음). 축 눈금 픽셀과 막대 윗변 · 표식 중심 픽셀을
   찾아 값으로 바꾼다. 막대는 ±1 px (K* ≈ ±0.07 GPa · E_hull ≈ ±1.5 %), 표식은 ±1–2 px 만큼 흔들린다.

무엇을 읽나 (하위 명령)
  f1c   Fig. 1C   Br 계열 — 원조성 + y = 0…1.25 의 K* (청록 막대) · E_hull (빗금 막대 · 로그축) · 조성 표식
  s2    Fig. S2   I 계열 (a) · F 계열 (b) — 같은 꼴
  f2    Fig. 2    (K*, E_hull) 평면의 원 네 개 중심
  s1    Fig. S1a  P2S7|Li 의 Hull(x, K_eff) 표식 → V*eps 역산 · K*(x) 프로파일 (우리 산술)
  all   위 전부 (+ --write 면 litdb/figures/<slug>/digitized.csv)

검산 (판독할 때마다 건다 — 하나라도 어긋나면 종료 코드 2)
  · 원조성 표식 = Li 5.5 / P 1.0 / S 4.5 / Cl 1.5 (±0.08)        ← 왼쪽 축 눈금
  · 원조성 K* 막대 = 본문 25.1 GPa (±0.4) · y = 0 막대 = 본문 8.4 GPa (±0.3)   ← K* 축 눈금
  · Br 계열 E_hull 최소 · 최대 = 본문 "30−75 meV/atom" (±4)               ← E_hull 로그축 눈금
  · Fig. 2 파란 원 = 본문 25.1 GPa (±0.6) · 237 meV/atom (±15) · 초록 원 K* = 8.4 (±0.3)
  · Fig. S1a: 20 / 30 / 36 GPa 곡선이 x = 0.4 에서 같은 V*eps (±0.05 Å^3) · max_x K*(x) = 범례의 39.7 GPa (±0.5)

사용
  ~/.venvs/litdb/bin/python3 tools/litdb/wang2022_two_parameter_readout.py all
  ~/.venvs/litdb/bin/python3 tools/litdb/wang2022_two_parameter_readout.py all --write
  ~/.venvs/litdb/bin/python3 tools/litdb/wang2022_two_parameter_readout.py s1 --si "<SI PDF 경로>"
  python3 tools/litdb/wang2022_two_parameter_readout.py --selftest        # PDF · PyMuPDF 없이 돈다

이 도구가 못 하는 것 (한계)
  · 축 눈금 픽셀은 **이 판본의 래스터에서 한 번 재서 상수로 박았다** (ACS VoR · 본문 그림 1458x1260 등).
    다른 판본 (재압축 · 다른 해상도) 이면 그림을 크기로 못 찾거나 위 검산이 실패한다 — 그때는 눈금을 다시 잰다.
  · E_hull 막대가 축 바닥 (≈ 2 meV/atom) 아래면 값을 못 읽는다 → None ('막대 없음') 으로 낸다. 0 으로 채우지 않는다.
  · 표식이 다른 표식 · 선과 겹치면 못 찾는다 → None. 지어내지 않는다 (Fig. S1a 에서 0 선 위의 표식은 K* 계열에 가려진다).
  · V*eps · K*(x) 는 그림에서 읽은 두 값의 차를 K_eff 로 나눈 **우리 산술**이다 — 논문 값이 아니다.
  · 그림이 말하지 않는 것 (V(x) 와 eps(x) 각각 · 어느 조성의 반응 변형률) 은 만들어 내지 않는다.
  · Fig. 3 · 4 · 5 · 6 · S3 · S6 · S7 의 판독 (카드 §6.4–§6.8) 은 여기 없다 — 그 값들은 카드에 '눈으로 읽음' 수준으로만 썼다.
"""
import argparse
import csv
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INBOX = ROOT / "litdb" / "inbox"
SLUG = "wang2022_two_parameter_space_dendrite_constriction"
HINT = "two-parameter space to tune solid electrolytes"
EV_A3_TO_GPA = 160.21766          # 1 eV/Å^3 = 160.218 GPa

# ── 이 판본의 래스터에서 잰 눈금 (픽셀) ────────────────────────────────
#   K0 = K* 0 GPa 의 행 · KPX = px/GPa · E10 = E_hull 10 meV/atom 의 행 · EDEC = px/decade
#   Y0 = 조성 0.0 의 행 · YPX = px/(조성 1) · rows = 패널 본문 행 범위
PANELS = {
    "f1c": dict(src="main", page=4, wh=(1458, 1260), label="Fig. 1C (LPSCl-Br)", X="Br",
                rows=(660, 1161), K0=1160.5, KPX=15.70, E10=1038.0, EDEC=174.25, Y0=1131.0, YPX=44.25),
    "s2a": dict(src="si", page=2, wh=(1249, 1120), label="Fig. S2a (LPSCl-I)", X="I",
                rows=(100, 505), K0=504.5, KPX=13.267, E10=400.5, EDEC=147.25, Y0=479.0, YPX=37.30),
    "s2b": dict(src="si", page=2, wh=(1249, 1120), label="Fig. S2b (LPSCl-F)", X="F",
                rows=(625, 1028), K0=1027.5, KPX=13.267, E10=923.5, EDEC=147.0, Y0=1002.0, YPX=37.25),
}
Y_LABELS = ["orig", "0.00", "0.25", "0.50", "0.75", "1.00", "1.25"]
FIG2 = dict(src="main", page=6, wh=(706, 471), X0=98.0, XPX=78.667 / 5.0, E1000=18.0, EDEC=103.5)
FIGS1 = dict(src="si", page=1, wh=(1710, 685), X0=239.5, XPX=503.0, Y0=102.5, YPX=234.0)


# ── 순수 함수 (selftest 대상) ──────────────────────────────────────────
def lin_value(px, p0, px_per_unit, sign=-1.0):
    """픽셀 → 선형축 값. p0 = 값 0 의 픽셀. sign = −1 이면 위로 갈수록 (행이 작을수록) 값이 커진다."""
    if px_per_unit == 0:
        raise ValueError("lin_value: px_per_unit 가 0 이다")
    return sign * (px - p0) / px_per_unit


def log_value(px, p_ref, v_ref, px_per_decade):
    """픽셀 → 로그축 값 (위로 갈수록 커진다). p_ref = 값 v_ref 의 행."""
    if px_per_decade == 0 or v_ref <= 0:
        raise ValueError("log_value: px_per_decade 가 0 이거나 기준값이 0 이하다")
    return v_ref * 10 ** ((p_ref - px) / px_per_decade)


def runs(vals):
    """정렬된 정수열 → 연속 구간 [(시작, 끝)]."""
    out = []
    for v in vals:
        v = int(v)
        if out and v - out[-1][1] <= 1:
            out[-1][1] = v
        else:
            out.append([v, v])
    return [(a, b) for a, b in out]


def first_sustained(count, thr, window, need):
    """위에서부터 훑어 count[i] ≥ thr 이고 그 뒤 window 행 중 need 행 이상이 ≥ thr 인 첫 i. 없으면 None.

    막대 윗변을 찾는 데 쓴다 — 막대를 가로지르는 선 · 표식 (몇 행의 끊김) 에 속지 않고,
    막대 위에 떠 있는 얇은 것 (격자선 한두 행) 을 윗변으로 잡지도 않는다.
    """
    n = len(count)
    for i in range(n):
        if count[i] >= thr and sum(1 for c in count[i:i + window] if c >= thr) >= need:
            return i
    return None


def components(mask, minsize=25):
    """bool 2D (리스트 또는 ndarray) → 4-연결 성분 [{n, cy, cx, y0, y1, x0, x1}]."""
    h = len(mask)
    w = len(mask[0]) if h else 0
    seen = [[False] * w for _ in range(h)]
    out = []
    for y0 in range(h):
        row = mask[y0]
        for x0 in range(w):
            if not row[x0] or seen[y0][x0]:
                continue
            q = deque([(y0, x0)])
            seen[y0][x0] = True
            pts = []
            while q:
                y, x = q.popleft()
                pts.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < h and 0 <= xx < w and mask[yy][xx] and not seen[yy][xx]:
                        seen[yy][xx] = True
                        q.append((yy, xx))
            if len(pts) >= minsize:
                ys = [p[0] for p in pts]
                xs = [p[1] for p in pts]
                out.append({"n": len(pts), "cy": sum(ys) / len(ys), "cx": sum(xs) / len(xs),
                            "y0": min(ys), "y1": max(ys), "x0": min(xs), "x1": max(xs)})
    return out


def band_marker(mask, xc, half, y_lo, y_hi, min_w=4, min_h=5, max_h=24):
    """세로 띠 (xc ± half) 안에서 표식 하나의 중심 행을 찾는다. 없으면 None.

    행마다 띠 안의 참 픽셀 수를 세고, 그 수가 min_w 이상인 행이 min_h…max_h 만큼 이어진 구간을 표식으로 본다
    (가는 연결선은 한 행에 1–2 px 라 걸리지 않는다). 구간이 여럿이면 None — 어느 것인지 고르지 않는다.
    """
    x0, x1 = max(0, xc - half), xc + half + 1
    rows_ok = []
    for y in range(y_lo, y_hi):
        if sum(1 for v in mask[y][x0:x1] if v) >= min_w:
            rows_ok.append(y)
    segs = [(a, b) for a, b in runs(rows_ok) if min_h <= b - a + 1 <= max_h]
    if len(segs) != 1:
        return None
    a, b = segs[0]
    num = den = 0
    for y in range(a, b + 1):
        c = sum(1 for v in mask[y][x0:x1] if v)
        num += y * c
        den += c
    return num / den


def v_eps(h0, hk, k_eff):
    """Hull(x, 0) · Hull(x, K_eff) [eV/atom] → V·ε [Å^3/atom]  (식 1 을 뒤집은 우리 산술)."""
    if k_eff <= 0:
        raise ValueError("v_eps: K_eff 가 0 이하면 나눌 수 없다")
    return (hk - h0) / k_eff * EV_A3_TO_GPA


def kstar_of(h0, veps):
    """K*(x) = |Hull(x, 0)| / (V·ε) [GPa]. 팽창이 0 이하면 None (논문 규칙으로는 무한대)."""
    if veps is None or veps <= 0:
        return None
    return abs(h0) / veps * EV_A3_TO_GPA


def check_anchors(pairs):
    """[(이름, 읽은 값, 기대값, 허용 오차)] → 어긋난 것의 목록. 읽은 값이 None 이면 어긋난 것으로 센다."""
    bad = []
    for name, got, want, tol in pairs:
        if got is None or abs(got - want) > tol:
            bad.append((name, got, want, tol))
    return bad


# ── PDF · 래스터 ──────────────────────────────────────────────────────
def find_pdfs(main=None, si=None):
    def pick(want_si):
        if not INBOX.is_dir():
            return None
        for p in sorted(INBOX.glob("*.pdf")):
            low = p.name.lower().replace("_", " ")
            if HINT in low and (("sup" in low.split(HINT)[0]) == want_si):
                return p
        return None
    m = Path(main) if main else pick(False)
    s = Path(si) if si else pick(True)
    return m, s


def load_raster(pdf, page_no, want_wh):
    """쪽에 박힌 래스터 가운데 크기가 want_wh 인 것을 RGB 리스트 (H x W x 3 · numpy) 로. 투명 마스크는 흰 바탕에 합성."""
    import fitz
    import numpy as np
    if pdf is None or not Path(pdf).exists():
        raise SystemExit(f"⛔ PDF 없음: {pdf} — --main / --si 로 경로를 준다 (litdb/inbox 는 리포에 없다)")
    doc = fitz.open(str(pdf))
    page = doc[page_no - 1]
    xref = None
    for info in page.get_image_info(xrefs=True):
        if (info["width"], info["height"]) == tuple(want_wh):
            xref = info["xref"]
            break
    if xref is None:
        raise SystemExit(f"⛔ {Path(pdf).name} p.{page_no} 에 {want_wh} 래스터가 없다 — 판본이 다르다 (눈금을 다시 재야 한다)")
    pix = fitz.Pixmap(doc, xref)
    if pix.n - pix.alpha >= 4 or pix.n == 1:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    rgb = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].astype(float)
    sm = doc.extract_image(xref).get("smask", 0)
    if sm:
        mk = fitz.Pixmap(doc, sm)
        a = np.frombuffer(mk.samples, dtype=np.uint8).reshape(mk.height, mk.width, mk.n)[..., 0].astype(float) / 255.0
        if a.shape == rgb.shape[:2]:
            rgb = rgb * a[..., None] + 255.0 * (1 - a[..., None])
    return rgb.round().astype(int)


# ── Fig. 1C · S2 ─────────────────────────────────────────────────────
def read_bar_panel(im, P):
    """막대 패널 하나 → [{y, Kstar, Ehull, comp{Li,P,S,Cl,X}}]. 못 읽은 값은 None."""
    import numpy as np
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    ya, yb = P["rows"]
    cyan = (R >= 170) & (R <= 238) & (G >= 240) & (B >= 240)
    hatch = (R >= 170) & (R <= 240) & (G >= 100) & (G <= 215) & (B >= 225) & (R - G > 20) & (B - G > 30)
    cols = cyan[ya:yb].sum(axis=0)
    segs = [(a, b) for a, b in runs(np.where(cols > 12)[0]) if 8 <= b - a <= 30]
    if len(segs) != len(Y_LABELS):
        raise SystemExit(f"⛔ {P['label']}: 청록 막대 {len(segs)} 개 (기대 {len(Y_LABELS)}) — 판본 · 색 문턱을 본다")
    marks = {"Li": (R < 70) & (G < 70) & (B < 70),
             "P": (R > 200) & (G < 110) & (B > 200),
             "S": (R > 200) & (G < 90) & (B < 90),
             "Cl": (R < 90) & (G < 90) & (B > 180),
             "X": (R < 90) & (G > 90) & (G < 190) & (B < 90)}
    out = []
    for lab, (a, b) in zip(Y_LABELS, segs):
        w = b - a + 1
        i = first_sustained(list(cyan[ya:yb, a + 1:b].sum(axis=1)), 0.5 * (w - 2), 12, 8)
        kstar = None if i is None else lin_value(ya + i, P["K0"], P["KPX"])
        j = first_sustained(list(hatch[ya:yb, b + 1:b + 25].sum(axis=1)), 3, 14, 9)
        ehull = None if j is None else log_value(ya + j, P["E10"], 10.0, P["EDEC"])
        comp = {}
        xc = b + 1
        for el, mk in marks.items():
            sub = mk[ya:yb, xc - 13:xc + 14]
            cs = [c for c in components(sub.tolist(), 25)
                  if c["x1"] - c["x0"] >= 6 and 6 <= c["y1"] - c["y0"] <= 30]
            comp[el] = None if not cs else lin_value(ya + max(cs, key=lambda c: c["n"])["cy"], P["Y0"], P["YPX"])
        out.append({"y": lab, "Kstar": kstar, "Ehull": ehull, "comp": comp})
    return out


def anchors_bar_panel(rows, P):
    o, z = rows[0], rows[1]
    pairs = [(f"{P['label']} 원조성 Li", o["comp"]["Li"], 5.5, 0.08), (f"{P['label']} 원조성 P", o["comp"]["P"], 1.0, 0.08),
             (f"{P['label']} 원조성 S", o["comp"]["S"], 4.5, 0.08), (f"{P['label']} 원조성 Cl", o["comp"]["Cl"], 1.5, 0.08),
             (f"{P['label']} 원조성 K* (본문 25.1)", o["Kstar"], 25.1, 0.4),
             (f"{P['label']} y=0 K* (본문 8.4)", z["Kstar"], 8.4, 0.3)]
    if P["X"] == "Br":
        e = [r["Ehull"] for r in rows[2:] if r["Ehull"] is not None]
        pairs += [("Br 계열 E_hull 최소 (본문 30)", min(e) if e else None, 30.0, 4.0),
                  ("Br 계열 E_hull 최대 (본문 75)", max(e) if e else None, 75.0, 4.0)]
    return pairs


# ── Fig. 2 ───────────────────────────────────────────────────────────
def read_fig2(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    masks = {"core (blue)": (B > 120) & (R < 60) & (G < 110),
             "LGPS-min (orange)": (R > 230) & (G > 170) & (G < 215) & (B < 60),
             "LPSCl-X-min (red)": (R > 230) & (G > 60) & (G < 120) & (B > 60) & (B < 130),
             "LPSCl-min (green)": (G > 140) & (R < 110) & (B < 110) & (R > 30)}
    out = {}
    for name, m in masks.items():
        cs = [c for c in components(m.tolist(), 800) if 35 <= c["x1"] - c["x0"] <= 60 and 35 <= c["y1"] - c["y0"] <= 60]
        if len(cs) != 1:
            out[name] = (None, None)
            continue
        c = cs[0]
        out[name] = (lin_value(c["cx"], FIG2["X0"], FIG2["XPX"], sign=1.0),
                     log_value(c["cy"], FIG2["E1000"], 1000.0, FIG2["EDEC"]))
    return out


# ── Fig. S1a ─────────────────────────────────────────────────────────
def read_figs1(im):
    """{K_eff: {x: Hull}} — 0 선 아래에서 표식을 못 찾으면 0.0 (K* 계열 표식에 가려진 것) 이 아니라 None 으로 둔다.
    단 그 K_eff 에서 이미 Hull 이 0 이 된 구간은 논문 그림이 0 선 위에 그리므로 '0 선' 으로 따로 표시한다."""
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    series = {0.0: (R < 60) & (G < 60) & (B < 60),
              20.0: (R < 60) & (G < 60) & (B > 200),
              30.0: (R > 100) & (R < 160) & (G < 50) & (B > 100) & (B < 170),
              36.0: (R > 110) & (R < 190) & (G < 80) & (B > 200)}
    y_top = int(FIGS1["Y0"] + 0.03 * FIGS1["YPX"])        # 0 선 바로 아래부터 (0 선 위 표식은 겹친다)
    out = {}
    for k, m in series.items():
        ml = m.tolist()
        d = {}
        for i in range(1, 10):
            x = i / 10.0
            xc = int(round(FIGS1["X0"] + x * FIGS1["XPX"]))
            # 범례 (x ≤ 0.5 · −1.19 eV 아래에서 글자가 시작한다) 를 피한다. 그 구간의 자료는 −1.03 eV 위에 있다.
            y_bot = int(FIGS1["Y0"] + (1.10 if x <= 0.5 else 1.30) * FIGS1["YPX"])
            cy = band_marker(ml, xc, 8, y_top, y_bot)
            d[x] = None if cy is None else lin_value(cy, FIGS1["Y0"], FIGS1["YPX"])
        out[k] = d
    return out


def derive_s1(h):
    """Fig. S1a 판독 → [{x, hull0, hull20, hull30, hull36, veps, kstar}] (veps = 가장 낮은 K_eff 에서 읽힌 값으로)."""
    rows = []
    for i in range(1, 10):
        x = i / 10.0
        h0 = h[0.0][x]
        ve = None
        if h0 is not None:
            for k in (20.0, 30.0, 36.0):
                if h[k][x] is not None:
                    ve = v_eps(h0, h[k][x], k)
                    break
        rows.append({"x": x, "hull0": h0, "hull20": h[20.0][x], "hull30": h[30.0][x], "hull36": h[36.0][x],
                     "veps": ve, "kstar": None if h0 is None else kstar_of(h0, ve)})
    return rows


# ── 출력 ─────────────────────────────────────────────────────────────
def fmt(v, nd=2):
    return "—" if v is None else f"{v:.{nd}f}"


def run(which, main, si, write):
    need_main = which in ("f1c", "f2", "all")
    need_si = which in ("s2", "s1", "all")
    rows_csv, pairs = [], []
    rast = {}

    def raster(spec):
        key = (spec["src"], spec["page"], spec["wh"])
        if key not in rast:
            rast[key] = load_raster(main if spec["src"] == "main" else si, spec["page"], spec["wh"])
        return rast[key]

    for key in (["f1c"] if need_main else []) + (["s2a", "s2b"] if need_si and which != "s1" else []):
        P = PANELS[key]
        rows = read_bar_panel(raster(P), P)
        pairs += anchors_bar_panel(rows, P)
        print(f"== {P['label']} — K*-minimised compositions (ML) · figure-read")
        print(f"   {'y':>5}  {'K* GPa':>7}  {'E_hull meV/atom':>15}   Li     P     S     Cl    {P['X']}")
        for r in rows:
            c = r["comp"]
            e = "막대 없음" if r["Ehull"] is None else f"{r['Ehull']:.1f}"
            print(f"   {r['y']:>5}  {fmt(r['Kstar']):>7}  {e:>15}   {fmt(c['Li'])}  {fmt(c['P'])}  {fmt(c['S'])}  "
                  f"{fmt(c['Cl'])}  {fmt(c['X'])}")
            for q, v, u in (("Kstar", r["Kstar"], "GPa"), ("Ehull_shifted_ML", r["Ehull"], "meV/atom")):
                rows_csv.append([P["label"], r["y"], q, "" if v is None else f"{v:.3f}", u, "bar top (raster px)"])
            for el, v in c.items():
                nm = P["X"] if el == "X" else el
                rows_csv.append([P["label"], r["y"], f"x({nm})", "" if v is None else f"{v:.3f}",
                                 "atoms per 12.5-atom formula", "marker centroid (raster px)"])
    if need_main and which != "f1c":
        pts = read_fig2(raster(FIG2))
        print("== Fig. 2 — disc centres · figure-read")
        for name, (k, e) in pts.items():
            print(f"   {name:<20} K* {fmt(k)} GPa   E_hull {fmt(e, 2 if (e or 0) < 1 else 0)} meV/atom")
            rows_csv.append(["Fig. 2", name, "Kstar", "" if k is None else f"{k:.3f}", "GPa", "disc centroid (raster px)"])
            rows_csv.append(["Fig. 2", name, "Ehull_shifted_ML", "" if e is None else f"{e:.3f}", "meV/atom",
                             "disc centroid (raster px)"])
        b, g = pts["core (blue)"], pts["LPSCl-min (green)"]
        pairs += [("Fig. 2 파란 원 K* (본문 25.1)", b[0], 25.1, 0.6), ("Fig. 2 파란 원 E_hull (본문 237)", b[1], 237.0, 15.0),
                  ("Fig. 2 초록 원 K* (본문 8.4)", g[0], 8.4, 0.3)]
    if need_si and which in ("s1", "all"):
        h = read_figs1(raster(FIGS1))
        d = derive_s1(h)
        print("== Fig. S1a — P2S7|Li · Hull(x, K_eff) [eV/atom] figure-read · V*eps / K*(x) = our arithmetic")
        print("     x    0 GPa   20 GPa   30 GPa   36 GPa   V*eps Å^3/atom   |Hull|/(V*eps) GPa")
        for r in d:
            print(f"   {r['x']:.1f}  {fmt(r['hull0'], 3):>7}  {fmt(r['hull20'], 3):>7}  {fmt(r['hull30'], 3):>7}  "
                  f"{fmt(r['hull36'], 3):>7}  {fmt(r['veps']):>14}  {fmt(r['kstar'], 1):>18}")
            for q, v, u, how in (("Hull_0GPa", r["hull0"], "eV/atom", "marker centroid (raster px)"),
                                 ("Hull_20GPa", r["hull20"], "eV/atom", "marker centroid (raster px)"),
                                 ("Hull_30GPa", r["hull30"], "eV/atom", "marker centroid (raster px)"),
                                 ("Hull_36GPa", r["hull36"], "eV/atom", "marker centroid (raster px)"),
                                 ("V_eps", r["veps"], "A^3/atom", "our arithmetic: (Hull_K - Hull_0)/K_eff"),
                                 ("Kstar_of_x", r["kstar"], "GPa", "our arithmetic: |Hull_0|/(V_eps)")):
                rows_csv.append(["Fig. S1a", f"x={r['x']:.1f}", q, "" if v is None else f"{v:.4f}", u, how])
        x4 = h[0.0][0.4]
        ve = [v_eps(x4, h[k][0.4], k) for k in (20.0, 30.0, 36.0) if x4 is not None and h[k][0.4] is not None]
        ks = [r["kstar"] for r in d if r["kstar"] is not None]
        pairs += [("Fig. S1a x=0.4 의 V*eps 세 곡선 일치 (최대 − 최소)", (max(ve) - min(ve)) if len(ve) == 3 else None, 0.0, 0.05),
                  ("Fig. S1a max_x K*(x) (범례 39.7)", max(ks) if ks else None, 39.7, 0.5)]
    bad = check_anchors(pairs)
    print(f"-- 검산 {len(pairs) - len(bad)}/{len(pairs)} 통과")
    for name, got, want, tol in bad:
        print(f"   ⚠ 어긋남: {name} — 읽은 값 {fmt(got, 3)} · 기대 {want} ± {tol}")
    if write and not bad:
        out = ROOT / "litdb" / "figures" / SLUG / "digitized.csv"
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["figure", "series_or_x", "quantity", "value", "unit", "how_read"])
            w.writerows(rows_csv)
        print(f"→ {out.relative_to(ROOT)}  ({len(rows_csv)} 행 · 빈 값 = 그림에서 못 읽음)")
    elif write:
        print("⛔ 검산이 어긋나 CSV 를 쓰지 않았다")
    return 2 if bad else 0


# ── selftest (PDF · PyMuPDF · numpy 없이) ─────────────────────────────
def selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(("  ✅ " if cond else "  ❌ ") + name)
        ok = ok and bool(cond)

    # 눈금 환산
    chk("양성: 선형축 (0 GPa 행 1160.5 · 15.70 px/GPa) 에서 행 765 → 25.19", abs(lin_value(765, 1160.5, 15.70) - 25.191) < 0.01)
    chk("양성: 로그축 (10 → 행 1038 · 174.25 px/decade) 에서 행 864 → ≈ 99.6", abs(log_value(864, 1038.0, 10.0, 174.25) - 99.67) < 0.5)
    for name, fn in (("선형축 px_per_unit 0", lambda: lin_value(1, 0, 0)), ("로그축 px_per_decade 0", lambda: log_value(1, 0, 10.0, 0)),
                     ("로그축 기준값 0", lambda: log_value(1, 0, 0.0, 100))):
        try:
            fn()
            chk(f"음성: {name} → ValueError", False)
        except ValueError:
            chk(f"음성: {name} → ValueError", True)
    # 막대 윗변: 행 30 부터 막대 · 행 50–53 은 표식이 가로질러 끊김 · 행 10 에 떠 있는 격자선 한 줄
    cnt = [0] * 100
    cnt[10] = 20
    for i in range(30, 100):
        cnt[i] = 0 if 50 <= i <= 53 else 20
    chk("양성: 끊김 · 떠 있는 선이 있어도 윗변 = 30", first_sustained(cnt, 10, 12, 8) == 30)
    chk("음성: 막대가 없으면 None (0 으로 채우지 않는다)", first_sustained([0] * 50, 10, 12, 8) is None)
    chk("음성: 격자선 한 줄만 있으면 None", first_sustained([0] * 10 + [20] + [0] * 40, 10, 12, 8) is None)
    # 표식: 12x12 정사각형 (행 40–51) + 그것을 지나는 2 px 두께 선
    W, H = 40, 100
    m = [[False] * W for _ in range(H)]
    for y in range(40, 52):
        for x in range(14, 26):
            m[y][x] = True
    for y in range(0, H):                      # 대각 연결선 (한 행에 2 px)
        x = min(W - 2, max(0, y // 3))
        m[y][x] = m[y][x + 1] = True
    cy = band_marker(m, 20, 8, 0, H)
    chk("양성: 선이 지나가도 표식 중심 행 ≈ 45.5", cy is not None and abs(cy - 45.5) < 0.6)
    only_line = [[False] * W for _ in range(H)]
    for y in range(H):
        only_line[y][20] = only_line[y][21] = True
    chk("음성: 가는 선만 있으면 표식 없음 (None)", band_marker(only_line, 20, 8, 0, H) is None)
    two = [row[:] for row in m]
    for y in range(70, 82):
        for x in range(14, 26):
            two[y][x] = True
    chk("음성: 띠 안에 표식이 둘이면 고르지 않는다 (None)", band_marker(two, 20, 8, 0, H) is None)
    # 연결 성분
    cs = components(m, 100)
    chk("양성: 정사각형 + 선 = 성분 1 개 (≥ 100 px)", len(cs) == 1 and cs[0]["n"] >= 144)
    chk("음성: 최소 크기보다 작으면 0 개", components(only_line, 10_000) == [])
    # 역산
    ve = v_eps(-0.885, -0.439, 20.0)
    chk("양성: (−0.885 → −0.439 @ 20 GPa) → V·ε ≈ 3.573 Å^3/atom", abs(ve - 3.573) < 0.005)
    chk("양성: K*(x) = 0.885 / 3.573 ≈ 39.7 GPa", abs(kstar_of(-0.885, ve) - 39.68) < 0.1)
    chk("음성: 팽창이 0 이하면 K* = None (유한값을 지어내지 않는다)", kstar_of(-0.5, 0.0) is None and kstar_of(-0.5, -1.0) is None)
    try:
        v_eps(-1.0, -0.5, 0.0)
        chk("음성: K_eff = 0 → ValueError", False)
    except ValueError:
        chk("음성: K_eff = 0 → ValueError", True)
    # 검산기
    chk("양성: 허용 오차 안이면 어긋남 0", check_anchors([("a", 25.19, 25.1, 0.4), ("b", 8.44, 8.4, 0.3)]) == [])
    chk("음성: 값이 벗어나면 잡는다", len(check_anchors([("a", 26.0, 25.1, 0.4)])) == 1)
    chk("음성: 못 읽은 값 (None) 은 통과가 아니다", len(check_anchors([("a", None, 25.1, 0.4)])) == 1)
    chk("양성: runs([1,2,3,7,8]) = [(1,3),(7,8)]", runs([1, 2, 3, 7, 8]) == [(1, 3), (7, 8)])
    print("selftest:", "통과" if ok else "실패")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Wang–Li 2022 (JACS Au 2, 886) 그림 재판독 — figure-read")
    ap.add_argument("which", nargs="?", default="all", choices=["f1c", "s2", "f2", "s1", "all"])
    ap.add_argument("--main", help="본문 PDF 경로 (기본: litdb/inbox 에서 제목으로 찾는다)")
    ap.add_argument("--si", help="SI PDF 경로")
    ap.add_argument("--write", action="store_true", help="검산이 다 통과하면 litdb/figures/<slug>/digitized.csv 를 쓴다")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    m, s = find_pdfs(a.main, a.si)
    return run(a.which, m, s, a.write)


if __name__ == "__main__":
    sys.exit(main())
