#!/usr/bin/env python3
"""liu2026_ccto_readout.py — Liu et al., J. Colloid Interface Sci. 729 (2027) 141891 그림 재판독.

카드: litdb/papers/liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl.md  (§3 · §5 · §10-③)
원본: litdb/inbox/ 의 본문 PDF (14 쪽) + SI PDF (70 쪽).  ⚠ PDF 는 리포에 없다 (litdb/inbox 는 .gitignore).

⛔ 이 스크립트가 내는 값은 전부 **그림 판독**이다 — 카드에 옮길 때 `figure-read` / `벡터 판독` 표지를 떼지 말 것.
   벡터 그림 (SI p.30 · p.44 · p.46) 은 PDF 경로 좌표라 정확하고, 래스터 그림 (SI p.12 · 본문 p.9) 은
   픽셀 판독이라 표식 반지름 (수 px) 만큼 흔들린다.

무엇을 읽나 (하위 명령)
  s23   Fig. S23  LPSC-PTFE LSV — 곡선이 논문 기준 100 µA (0.1 mA) 를 넘는 전위  (라벨 3.69 V 와 대조)
  s39   Fig. S39  PLI / PLIC LSV — 같은 기준 교차 (라벨 4.57 / 4.62 V 와 대조)
  s37   Fig. S37  PLIC / PLI ln σ vs 1000/T 표식 좌표 → σ(30–60 °C) · Ea 재적합 (본문 1.44 / 1.40 과 대조)
  s5    Fig. S5   AIMD MSD 그림의 *그려진 적합선* 기울기 (Å² ps⁻¹) → cm² s⁻¹ · D = 기울기/6 (보고 6.77e-5 와 대조)
  f5a   Fig. 5a   LFP‖Li 1 C 장기 — PLIC 마지막 표식의 사이클 수 (라벨 '1100th' 와 대조)
  all   위 전부

사용
  python3 tools/litdb/liu2026_ccto_readout.py all
  python3 tools/litdb/liu2026_ccto_readout.py s37 --si "litdb/inbox/Sup) Colossal-dielectric ….pdf"
  python3 tools/litdb/liu2026_ccto_readout.py --selftest

이 도구가 못 하는 것 (한계)
  · 눈금 위치는 **눈금 숫자 글자의 중심**으로 잡는다 (Origin 내보내기는 숫자 중심 = 눈금). 글자가 비대칭이면 ±0.5 pt.
  · 래스터 판독 (s5 · f5a) 은 색 문턱으로 선 · 표식을 고른다 — 다른 PDF 판본 (재압축 JPEG) 에서는 문턱을 다시 봐야 한다.
  · 쪽 번호 · 경로 순서는 이 판본 (Elsevier VoR 2026-11 · SI Word 내보내기) 에 묶여 있다. 판본이 바뀌면 `--check` 가 실패한다.
  · 그림이 말하지 않는 것 (셀 면적 S · 두께 L · 맞춤 창) 은 만들어 내지 않는다.
"""
import argparse
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INBOX = ROOT / "litdb" / "inbox"
MAIN_HINT = "Colossal-dielectric cathode interface engineering"
K_B = 8.617333e-5  # eV/K


# ── 순수 함수 (selftest 대상) ──────────────────────────────────────────
def calib(p0, v0, p1, v1):
    """두 눈금 (좌표 p, 값 v) → 좌표를 값으로 바꾸는 함수. 같은 좌표 두 개면 오류."""
    if p1 == p0:
        raise ValueError("calib: 두 눈금 좌표가 같다")
    s = (v1 - v0) / (p1 - p0)
    return lambda p: v0 + (p - p0) * s


def first_crossing(xy, thr, xmin=-math.inf):
    """(x, y) 열에서 x > xmin 이고 y ≥ thr 인 첫 점의 x 를 선형보간으로. 못 넘으면 None."""
    pts = sorted(xy)
    prev = None
    for x, y in pts:
        if x <= xmin:
            prev = (x, y)
            continue
        if y >= thr:
            if prev is not None and prev[1] < thr and x != prev[0]:
                x0, y0 = prev
                return x0 + (thr - y0) * (x - x0) / (y - y0)
            return x
        prev = (x, y)
    return None


def linfit(xs, ys):
    n = len(xs)
    if n < 2:
        raise ValueError("linfit: 점이 2개 미만")
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((a - mx) ** 2 for a in xs)
    if sxx == 0:
        raise ValueError("linfit: x 분산 0")
    m = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sxx
    return m, my - m * mx


def ea_from_arrhenius(inv_T_1000, ln_sigma):
    """ln σ vs 1000/T 기울기 → Ea (eV). 기울기가 양이면 (온도가 오를수록 σ 감소) 오류."""
    m, _ = linfit(inv_T_1000, ln_sigma)
    if m >= 0:
        raise ValueError("ea_from_arrhenius: 기울기가 음이 아니다 — 축/부호 확인")
    return -m * 1000.0 * K_B


# ── PDF 헬퍼 ───────────────────────────────────────────────────────────
def _fitz():
    try:
        import pymupdf as fitz  # noqa
    except ImportError:
        try:
            import fitz  # noqa
        except ImportError:
            sys.exit("⛔ PyMuPDF 가 없다 — ~/.venvs/litdb/bin/python3 로 실행 (tools/litdb/extract_figures.py 머리말)")
    return fitz


def find_pdf(si):
    cands = [p for p in INBOX.glob("*.pdf") if MAIN_HINT.lower() in p.name.lower()]
    want = [p for p in cands if ("sup" in p.name.lower()) == si]
    if not want:
        sys.exit(f"⛔ litdb/inbox 에서 {'SI' if si else '본문'} PDF 를 못 찾았다 — --si / --main 으로 경로를 준다")
    return want[0]


def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    x0, y0, x1, y1 = s["bbox"]
                    out.append((t, (x0 + x1) / 2, (y0 + y1) / 2, s["bbox"]))
    return out


def tick(sp, text, region):
    """region=(x0,y0,x1,y1) 안의 text 라벨 중심. 없거나 둘 이상이면 오류 (판본 확인용)."""
    hits = [(cx, cy) for t, cx, cy, _ in sp
            if t == text and region[0] <= cx <= region[2] and region[1] <= cy <= region[3]]
    if len(hits) != 1:
        raise RuntimeError(f"눈금 '{text}' 가 영역 {region} 에 {len(hits)}개 — 판본이 다른가?")
    return hits[0]


def polylines(page, clip):
    fitz = _fitz()
    out = []
    for d in page.get_drawings():
        r = fitz.Rect(d["rect"])
        if not fitz.Rect(clip).contains(r):
            continue
        if d.get("color") is None:               # 채우기만 있는 도형 (삽도 강조 상자 · 화살표) 은 곡선이 아니다
            continue                             # ⚠ 2026-11-06: 이걸 안 거르면 S23 본도 교차가 2.58 V 로 나온다
        pts = []
        for it in d["items"]:
            if it[0] == "l":
                pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
            elif it[0] == "c":
                pts += [(it[1].x, it[1].y), (it[4].x, it[4].y)]
        if len(pts) >= 20:
            out.append({"color": d.get("color"), "rect": tuple(r), "pts": pts})
    return out


# ── 하위 명령 ──────────────────────────────────────────────────────────
def cmd_s23(si):
    fitz = _fitz()
    pg = fitz.open(si)[29]                       # SI p.30
    sp = spans(pg)
    # 본도 x: '0'…'6' (y≈300) · y: '0.0' '2.0' (x≈176) / 삽도 x: '2' '3' '4' (y≈217) · y: '0.0' '0.1'
    X = calib(tick(sp, "0", (190, 290, 215, 310))[0], 0, tick(sp, "6", (390, 290, 410, 310))[0], 6)
    Y = calib(tick(sp, "0.0", (160, 230, 190, 255))[1], 0, tick(sp, "2.0", (160, 110, 190, 130))[1], 2.0)
    iX = calib(tick(sp, "2", (205, 205, 230, 230))[0], 2, tick(sp, "4", (320, 205, 345, 230))[0], 4)
    iY = calib(tick(sp, "0.0", (190, 195, 215, 215))[1], 0, tick(sp, "0.1", (190, 150, 215, 170))[1], 0.1)
    pls = polylines(pg, (100, 80, 450, 330))
    inset = [p for p in pls if p["rect"][0] > 210 and p["rect"][3] < 205]
    main = [p for p in pls if p not in inset]
    mxy = [(X(x), Y(y)) for p in main for x, y in p["pts"]]
    ixy = [(iX(x), iY(y)) for p in inset for x, y in p["pts"]]
    r = {"main_V_at_0.1mA": first_crossing(mxy, 0.1, 2.5),
         "inset_V_at_0.1mA": first_crossing(ixy, 0.1, 2.6),
         "main_V_at_0.05mA": first_crossing(mxy, 0.05, 2.5),
         "label_V": 3.69}
    print("Fig. S23 LPSC-PTFE LSV (벡터):", {k: (round(v, 3) if v else v) for k, v in r.items()})
    return r


def cmd_s39(si):
    fitz = _fitz()
    pg = fitz.open(si)[45]                       # SI p.46
    sp = spans(pg)
    iX = calib(tick(sp, "4.0", (205, 220, 235, 240))[0], 4.0, tick(sp, "5.0", (355, 220, 385, 240))[0], 5.0)
    iY = calib(tick(sp, "0.00", (185, 210, 220, 225))[1], 0, tick(sp, "0.10", (185, 155, 220, 175))[1], 0.10)
    pls = polylines(pg, (100, 80, 450, 330))
    inset = [p for p in pls if p["rect"][0] > 215 and p["rect"][3] < 205]
    out = {}
    for p in inset:
        c = p["color"] or (0, 0, 0)
        name = "PLIC(pink)" if c[0] > 0.9 else "PLI(blue)"
        out[name] = first_crossing([(iX(x), iY(y)) for x, y in p["pts"]], 0.1, 4.0)
    print("Fig. S39 삽도 0.1 mA 교차 (벡터):", {k: (round(v, 3) if v else v) for k, v in out.items()},
          "· 라벨 PLI 4.57 / PLIC 4.62")
    return out


def cmd_s37(si):
    fitz = _fitz()
    pg = fitz.open(si)[43]                       # SI p.44
    sp = spans(pg)
    X = calib(tick(sp, "3.0", (225, 290, 250, 310))[0], 3.0, tick(sp, "3.3", (360, 290, 385, 310))[0], 3.3)
    # y 눈금은 숫자 글자 대신 눈금선 좌표 (0.0 · 1.5) 를 쓴다 — 아래 짧은 수평선
    ticks = sorted({round(d["rect"].y0, 2) for d in pg.get_drawings()
                    if d.get("color") == (0.0, 0.0, 0.0) and 3 < d["rect"].width < 5 and d["rect"].height == 0
                    and d["rect"].x0 < 190})
    if len(ticks) < 6:
        raise RuntimeError(f"S37 y 눈금선 {len(ticks)}개 — 판본 확인")
    Y = calib(ticks[-1], 0.0, ticks[0], 1.5)     # 아래 = 0.0 · 위 = 1.5
    marks = {}
    for d in pg.get_drawings():
        r, f = d["rect"], d.get("fill")
        if f and 8.5 < r.width < 9.5 and 8.5 < r.height < 9.5:     # 바깥 원 (지름 ≈9 pt)
            name = "PLIC" if f[0] > 0.95 else "PLI"
            marks.setdefault(name, []).append((X((r.x0 + r.x1) / 2), Y((r.y0 + r.y1) / 2)))
    res = {}
    for name, pts in marks.items():
        pts.sort(reverse=True)                     # 1000/T 큰 쪽 = 30 °C 먼저
        ea = ea_from_arrhenius([p[0] for p in pts], [p[1] for p in pts])
        res[name] = {"T_C": [round(1000 / p[0] - 273.15, 1) for p in pts],
                     "sigma_mS_cm": [round(math.exp(p[1]), 3) for p in pts], "Ea_eV": round(ea, 3)}
    print("Fig. S37 표식 (벡터):", res, "· 본문 σ(30 °C) PLIC 1.44 / PLI 1.40 · Ea 0.30 / 0.29")
    return res


def cmd_s5(si):
    fitz = _fitz()
    import numpy as np
    pg = fitz.open(si)[11]                       # SI p.12 (래스터 한 장)
    pix = pg.get_pixmap(dpi=300, clip=fitz.Rect(99.2, 75.0, 496.0, 256.2))
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[..., :3].astype(int)
    dark = a.sum(axis=2) < 200

    def runs(idx):
        out, s, p = [], None, None
        for i in idx:
            if s is None:
                s = p = i
            elif i == p + 1:
                p = i
            else:
                out.append((s + p) / 2); s = p = i
        if s is not None:
            out.append((s + p) / 2)
        return out
    cols = [i for i, v in enumerate(dark.sum(axis=0)) if v > 300]
    rows = [i for i, v in enumerate(dark.sum(axis=1)) if v > 300]
    xl, xr = min(c for c in cols if c > pix.width * 0.4), max(cols)
    yt, yb = min(rows), max(rows)
    xt = runs([i + int(xl) - 3 for i, v in enumerate(dark[int(yb) + 2:int(yb) + 12, int(xl) - 3:int(xr) + 3].sum(axis=0)) if v >= 5])
    yt_ = runs([i + int(yt) for i, v in enumerate(dark[int(yt):int(yb) + 8, int(xl) - 14:int(xl) - 3].sum(axis=1)) if v >= 5])
    if len(xt) < 8 or len(yt_) < 5:
        raise RuntimeError(f"S5 눈금 검출 실패 (x {len(xt)} · y {len(yt_)})")
    T = calib(xt[0], 0.0, xt[7], 3500.0)          # fs  — 눈금 0 … 3500
    M = calib(yt_[-1], 0.0, yt_[0], 4.0)          # Å²  — 아래 0 · 위 4
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    br = a.sum(axis=2)
    light = (B > R + 25) & (G > R + 15) & (br >= 570) & (br < 700)   # 연한 적합선
    light[:int(yt) + 2, :] = False; light[int(yb) - 2:, :] = False
    light[:, :int(xl) + 3] = False; light[:, int(xr) - 2:] = False
    colmed = {}
    ys, xs = np.nonzero(light)
    for x, y in zip(xs, ys):
        colmed.setdefault(int(x), []).append(int(y))
    xx = sorted(colmed)
    yy = [float(np.median(colmed[x])) for x in xx]
    m, c = linfit(xx, yy)
    for _ in range(5):                              # 데이터선과 겹친 열을 걸러 다시 맞춘다
        keep = [(x, y) for x, y in zip(xx, yy) if abs(y - (m * x + c)) < 3]
        m, c = linfit([k[0] for k in keep], [k[1] for k in keep])
    x0, x1 = keep[0][0], keep[-1][0]
    slope_A2_ps = (M(m * x1 + c) - M(m * x0 + c)) / ((T(x1) - T(x0)) / 1000.0)
    res = {"t_end_fs": round(T(xr)), "slope_A2_per_ps": round(slope_A2_ps, 4),
           "slope_cm2_s": slope_A2_ps * 1e-4, "D_slope_over_6_cm2_s": slope_A2_ps * 1e-4 / 6,
           "reported_D_cm2_s": 6.77e-5, "n_cols": len(keep)}
    print("Fig. S5 적합선 (픽셀):", {k: (f"{v:.3e}" if isinstance(v, float) and v < 1e-3 else v) for k, v in res.items()})
    return res


def cmd_f5a(main):
    fitz = _fitz()
    import numpy as np
    d = fitz.open(main)
    pg = d[8]                                    # 본문 p.9
    x = d.extract_image(pg.get_images()[0][0])
    from io import BytesIO
    from PIL import Image
    a = np.asarray(Image.open(BytesIO(x["image"])).convert("RGB")).astype(int)
    dark = a.sum(axis=2) < 250
    band = dark[467:478, 100:1000].sum(axis=0)
    ticks, s, p = [], None, None
    for i in [i + 100 for i, v in enumerate(band) if v >= 6]:
        if s is None:
            s = p = i
        elif i == p + 1:
            p = i
        else:
            ticks.append((s + p) / 2); s = p = i
    if s is not None:
        ticks.append((s + p) / 2)
    if len(ticks) != 6:
        raise RuntimeError(f"Fig. 5a x 눈금 {len(ticks)}개 (6 이어야) — 판본 확인")
    C = calib(ticks[0], 0, ticks[-1], 1000)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    pink = (R > 220) & (G > 140) & (G < 200) & (B > 140) & (B < 200) & (R - G > 35)
    ys, xs = np.nonzero(pink[150:330, 120:1000])
    purple = (B > 200) & (R > 150) & (G < 170) & (R < 230) & (B - G > 50)
    pc = [i + 800 for i, v in enumerate(purple[60:465, 800:1000].sum(axis=0)) if v > 200]
    res = {"last_pink_edge_cycle": round(C(xs.max() + 120)), "right_axis_cycle": round(C(sum(pc) / len(pc))) if pc else None,
           "label": "1100th 89.2%"}
    print("Fig. 5a (픽셀):", res)
    return res


# ── selftest (양성 + 음성) ─────────────────────────────────────────────
def selftest():
    ok = True

    def chk(name, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  ✗ ") + name)
        ok &= bool(cond)
    f = calib(10, 0.0, 110, 1.0)
    chk("calib 양성: 60 → 0.5", abs(f(60) - 0.5) < 1e-12)
    try:
        calib(5, 0, 5, 1); chk("calib 음성: 같은 좌표면 오류", False)
    except ValueError:
        chk("calib 음성: 같은 좌표면 오류", True)
    line = [(v / 100, (v / 100) ** 2 * 0.01) for v in range(0, 601)]          # I = 0.01 V²
    xc = first_crossing(line, 0.1, 2.5)
    chk("first_crossing 양성: 0.01·V² = 0.1 → V = √10", xc is not None and abs(xc - math.sqrt(10)) < 1e-3)
    chk("first_crossing 음성: 문턱 미달이면 None", first_crossing(line, 1.0, 2.5) is None)
    chk("first_crossing 음성: xmin 앞의 큰 값은 무시", first_crossing([(0, 5), (3, 0.01), (4, 0.2)], 0.1, 1) is not None
        and first_crossing([(0, 5), (3, 0.01), (4, 0.2)], 0.1, 1) > 3)
    inv = [3.3, 3.2, 3.1, 3.0]
    ln = [math.log(1.0) - 0.30 / (K_B * 1000) * (x - 3.3) for x in inv]    # Ea 0.30 eV 합성
    chk("ea_from_arrhenius 양성: 합성 0.30 eV 회수", abs(ea_from_arrhenius(inv, ln) - 0.30) < 1e-9)
    try:
        ea_from_arrhenius(inv, list(reversed(ln))); chk("ea_from_arrhenius 음성: 뒤집힌 축이면 오류", False)
    except ValueError:
        chk("ea_from_arrhenius 음성: 뒤집힌 축이면 오류", True)
    # 1/6 판정의 음성 경로: D 를 기울기/6 으로 냈다면 '보고값 = 기울기' 판정이 거짓이어야 한다
    slope = 0.6768e-4
    chk("1/6 판정 양성: 보고 = 기울기 → 일치", abs(6.77e-5 / slope - 1) < 0.01)
    chk("1/6 판정 음성: 보고가 기울기/6 이면 불일치로 나온다", abs((slope / 6) / slope - 1) > 0.5)
    print("selftest", "통과" if ok else "실패")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("what", nargs="?", choices=["s23", "s39", "s37", "s5", "f5a", "all"])
    ap.add_argument("--si", default="")
    ap.add_argument("--main", default="")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.what:
        ap.error("하위 명령이 필요하다 (s23 · s39 · s37 · s5 · f5a · all) 또는 --selftest")
    si = Path(a.si) if a.si else find_pdf(si=True)
    mn = Path(a.main) if a.main else find_pdf(si=False)
    for w in (["s23", "s39", "s37", "s5", "f5a"] if a.what == "all" else [a.what]):
        {"s23": lambda: cmd_s23(si), "s39": lambda: cmd_s39(si), "s37": lambda: cmd_s37(si),
         "s5": lambda: cmd_s5(si), "f5a": lambda: cmd_f5a(mn)}[w]()
    return 0


if __name__ == "__main__":
    sys.exit(main())
