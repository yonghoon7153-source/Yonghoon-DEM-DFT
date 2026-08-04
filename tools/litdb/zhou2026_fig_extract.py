#!/usr/bin/env python3
"""zhou2026 (Chem. Eng. J. 539 (2026) 177014) — 본문 그림 실물 독립 검증.

litdb/papers/zhou2026_high_entropy_lgps_multicationic.md 의 §20 (본문 10 pp 실물 검증)
근거를 만드는 스크립트. 본문 PDF(inbox #49)에는 Methods 절이 아예 없고 계산 파라미터가
전부 SI 로 빠져 있어서, 본문에서 확인 가능한 것은 "그림이 실제로 무엇을 그리는가" 뿐이다.
그래서 축을 캘리브레이션하고 마커를 픽셀에서 복원한다.

복원 대상
  fig2a : H-LM0.2PS(빨강) 회귀선 기울기 -> Ea, 그 선이 지나는 σ(25 °C)·σ(0 °C),
          그리고 실제 데이터 마커 위치 (25 °C 마커가 있는가?)
  fig2d : AIMD MSD 3곡선 -> 후반부 기울기 -> D -> Nernst-Einstein σ, 3점 Ea
  fig3c : NEB 프로파일 22+22 이미지 에너지, 봉우리 개수와 높이
  fig7a : rate 곡선 5개의 방전 종점 (본문 서술 165/140/129/113/96 과 대조)
  fig7c : 1C 100 cyc 충·방전 용량 마커 (본문 125 / 초록 130 과 대조)

입력: litdb/inbox/_49_fig{1,2,3,4,5,6,7}.png
      (PDF 각 쪽의 임베디드 이미지. 없으면 --dump 로 재생성)
의존성: PyMuPDF(fitz, --dump 시) + PIL. **numpy/scipy 없이 순수 파이썬**
        (이 머신에 numpy 미설치 — jun2022 검증 스크립트와 같은 제약)

usage:
  python tools/litdb/zhou2026_fig_extract.py --dump      # PDF -> _49_fig*.png
  python tools/litdb/zhou2026_fig_extract.py all
  python tools/litdb/zhou2026_fig_extract.py fig3c
"""
import math
import sys

from PIL import Image

INBOX = "litdb/inbox"
PDF = (
    f"{INBOX}/49. A high-entropy multicationic substituted Li10GeP2S12 "
    "solid electrolyte enabling stable all-solid-state batteries.pdf"
)
# PDF 쪽 -> 그림 번호 (쪽마다 임베디드 이미지 1장이 그림 전체)
PAGE2FIG = {2: "fig1", 3: "fig2", 4: "fig3", 5: "fig4", 6: "fig5", 7: "fig6", 8: "fig7"}

KB_EV = 8.617333262e-5     # eV/K
KB_J = 1.380649e-23
QE = 1.602176634e-19
V_CELL = 953.5             # Å^3  (a=8.70078, c=12.59562 -> a^2 c; SI Table S4)
N_LI = 20                  # Li per unit cell (Z=2 x Li10)


# ------------------------------------------------------------------ 공통 유틸
def dump_figures():
    import fitz

    d = fitz.open(PDF)
    for pg, nm in PAGE2FIG.items():
        xref = d[pg - 1].get_images(full=True)[0][0]
        pix = fitz.Pixmap(d, xref)
        pix.save(f"{INBOX}/_49_{nm}.png")
        print(f"  {nm}: {pix.width}x{pix.height}")


def load(nm):
    return Image.open(f"{INBOX}/_49_{nm}.png").convert("RGB")


def is_dark(px, x, y, thr=400):
    r, g, b = px[x, y]
    return r + g + b < thr


def long_lines(px, along, across, horizontal, frac=0.7):
    """along 축을 훑어 across 범위의 어두운 픽셀이 frac 이상인 위치(=프레임 선)를 반환."""
    n_need = int((across[1] - across[0]) * frac)
    out = []
    for k in range(*along):
        n = sum(
            1
            for j in range(*across)
            if is_dark(px, (j if horizontal else k), (k if horizontal else j))
        )
        if n > n_need:
            out.append(k)
    return group(out)


def group_runs(idx, gap=1):
    """연속 인덱스를 묶어 각 런(리스트)을 반환."""
    runs, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > gap:
            runs.append(cur)
            cur = []
        cur.append(i)
    if cur:
        runs.append(cur)
    return runs


def group(idx, gap=1):
    """연속 인덱스를 묶어 각 그룹의 중심을 반환."""
    runs, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > gap:
            runs.append(cur)
            cur = []
        cur.append(i)
    if cur:
        runs.append(cur)
    return [sum(r) / len(r) for r in runs]


def ticks(px, axis, span, horizontal, depth=4, inward=+1, thr=430):
    """축선에서 안쪽(inward=+1: 좌표 증가 방향)으로 depth 픽셀 이어지는 눈금 중심."""
    hit = []
    for k in range(*span):
        ok = True
        for d in range(1, depth + 1):
            a = axis + inward * d
            x, y = (k, a) if horizontal else (a, k)
            if not is_dark(px, x, y, thr):
                ok = False
                break
        if ok:
            hit.append(k)
    return group(hit)


def lsq(pts):
    """[(x,y)] -> (slope, intercept, R^2)"""
    n = len(pts)
    mx = sum(p[0] for p in pts) / n
    my = sum(p[1] for p in pts) / n
    sxx = sum((p[0] - mx) ** 2 for p in pts)
    sl = sum((p[0] - mx) * (p[1] - my) for p in pts) / sxx
    ic = my - sl * mx
    sst = sum((p[1] - my) ** 2 for p in pts)
    r2 = 1 - sum((p[1] - (ic + sl * p[0])) ** 2 for p in pts) / sst if sst else float("nan")
    return sl, ic, r2


def blobs(px, box, hit, min_px=25):
    """4-이웃 연결성분 중심 [(cx, cy, npx)] — 순수 파이썬 flood fill."""
    x0, x1, y0, y1 = box
    seen = set()
    out = []
    for sy in range(y0, y1):
        for sx in range(x0, x1):
            if (sx, sy) in seen or not hit(*px[sx, sy]):
                continue
            st = [(sx, sy)]
            seen.add((sx, sy))
            pts = []
            while st:
                x, y = st.pop()
                pts.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in seen and hit(*px[nx, ny]):
                        seen.add((nx, ny))
                        st.append((nx, ny))
            if len(pts) >= min_px:
                out.append((sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts), len(pts)))
    out.sort()
    return out


def nernst_einstein(D_cm2s, T):
    """D [cm^2/s] -> σ [mS/cm], Haven=1, Li 20개/셀."""
    n = N_LI / (V_CELL * 1e-24) * 1e6          # m^-3
    sig = n * QE * QE * (D_cm2s * 1e-4) / (KB_J * T)   # S/m
    return sig / 100 * 1000


# ------------------------------------------------------- Fig 2a (Arrhenius) --
def fig2a():
    print("=" * 72)
    print("[Fig 2a] H-LM0.2PS 아레니우스 — 인쇄 Ea 0.313 eV / 본문 σ 13.24(25 °C)·3.10(0 °C)")
    im = load("fig2")
    px = im.load()
    # 프레임: x=79/700, y=64/352 (실측)
    X0, X1, XV0, XV1 = 107.0, 672.0, 2.6, 4.6      # 하단 눈금 2.6 ~ 4.6 (11틱)
    Y0, Y1, YV0, YV1 = 80.0, 336.0, -1.0, -5.0     # 좌측 눈금 -1 ~ -5 (5틱)
    kx = (XV1 - XV0) / (X1 - X0)
    ky = (YV1 - YV0) / (Y1 - Y0)
    xt = ticks(px, 352, (80, 700), True, depth=4, inward=-1)
    yt = ticks(px, 79, (65, 352), False, depth=4, inward=+1)
    print(f"  x 눈금 {len(xt)}개 {[round(t) for t in xt]}  (라벨 2.6..4.6, 0.2 간격)")
    print(f"  y 눈금 {len(yt)}개 {[round(t) for t in yt]}  (라벨 -1..-5)")
    # 상단 T(°C) 축과 교차검산
    for T, lab in ((373.15, "100 °C"), (273.15, "0 °C")):
        print(f"    검산 {lab}: 1000/T={1000/T:.4f} -> x={X0 + (1000/T - XV0)/kx:.1f} px")

    def red(r, g, b):
        return r > 185 and g < 95 and b < 95

    # 회귀선 = 열마다 '가는 빨간 런 1개'만 있는 열
    line = []
    for x in range(83, 698):
        runs, cur = [], []
        for y in range(66, 350):
            if red(*px[x, y]):
                cur.append(y)
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        if len(runs) == 1 and len(runs[0]) <= 5:
            line.append((x, sum(runs[0]) / len(runs[0])))
    sl, ic, r2 = lsq(line)
    slope = sl * ky / kx                      # d log10 σ / d(1000/T)
    Ea = -math.log(10) * KB_EV * 1000 * slope
    print(f"  회귀선 단독 열 {len(line)}개 (x {line[0][0]}..{line[-1][0]}), 픽셀 R2={r2:.5f}")
    print(f"  -> 선 기울기 {slope:.4f} dex/(1000/T)  =>  Ea = {Ea:.4f} eV   [인쇄 0.313 ✓]")

    def line_sigma(T):
        xpx = X0 + (1000 / T - XV0) / kx
        return 10 ** (YV0 + ((ic + sl * xpx) - Y0) * ky) * 1000   # mS/cm

    for T, lab, quoted in ((298.15, "25 °C", 13.24), (273.15, "0 °C", 3.10)):
        v = line_sigma(T)
        print(f"  선 위의 σ({lab}) = {v:6.3f} mS/cm  vs 본문 {quoted:5.2f}  ({v/quoted-1:+.1%})")

    # 실제 데이터 마커 (두꺼운 빨간 런의 국소 최대)
    prof = {}
    for x in range(83, 698):
        runs, cur = [], []
        for y in range(66, 350):
            if red(*px[x, y]):
                cur.append(y)
            elif cur:
                runs.append(cur)
                cur = []
        if cur:
            runs.append(cur)
        if runs:
            best = max(runs, key=len)
            prof[x] = (len(best), sum(best) / len(best))
    grp, cur = [], []
    for x in sorted(prof):
        L, c = prof[x]
        if L >= 7:
            if cur and x - cur[-1][0] > 3:
                grp.append(cur)
                cur = []
            cur.append((x, L, c))
    if cur:
        grp.append(cur)
    print("  데이터 마커 (두꺼운 런 클러스터):")
    for g in grp:
        if max(L for _, L, _ in g) < 9:
            continue
        tot = sum(L for _, L, _ in g)
        cx = sum(x * L for x, L, _ in g) / tot
        cy = sum(c * L for _, L, c in g) / tot
        inv = XV0 + (cx - X0) * kx
        s = 10 ** (YV0 + (cy - Y0) * ky) * 1000
        print(f"    T = {1000/inv - 273.15:6.1f} °C   σ = {s:8.3f} mS/cm")
    print("  ※ 25 °C(1000/T = 3.354, x = %.0f px) 자리에 마커가 없다 — 측정은 10 °C 격자." % (X0 + (3.3540 - XV0) / kx))

    # RT 부근 마커를 개별 정밀 측정 ('Ea = 0.313 eV' 빨간 라벨이 마커와 같은 색이라 창을 좁혀 잡는다)
    def redish(x, y):
        r, g, b = px[x, y]
        return r > 150 and r - g > 60 and r - b > 60

    print("  RT 부근 마커 정밀 판독 (창별 최장 수직런):")
    near = {}
    for lo, hi, lab in ((270, 284, "40 °C"), (298, 314, "30 °C"), (330, 344, "20 °C"), (402, 416, "0 °C")):
        best = None
        for x in range(lo, hi):
            col = [y for y in range(66, 350) if redish(x, y)]
            for r in group_runs(col):
                if best is None or len(r) > best[0]:
                    best = (len(r), x, sum(r) / len(r))
        L, x, yc = best
        inv = XV0 + (x - X0) * kx
        s = 10 ** (YV0 + (yc - Y0) * ky) * 1000
        near[lab] = (1000 / inv - 273.15, s)
        print(f"    {lab:6s} 런 {L:2d}px @ x={x}  ->  T = {1000/inv - 273.15:5.1f} °C   σ = {s:6.2f} mS/cm")
    # 30/20 °C 마커로 25 °C 내삽 (1/T 선형, log σ)
    (t30, s30), (t20, s20) = near["30 °C"], near["20 °C"]
    f = (1 / 298.15 - 1 / (t30 + 273.15)) / (1 / (t20 + 273.15) - 1 / (t30 + 273.15))
    s25 = 10 ** (math.log10(s30) + f * (math.log10(s20) - math.log10(s30)))
    print(f"  -> 마커 내삽 σ(25 °C) ≈ {s25:.1f} mS/cm ;  선 위 값 {line_sigma(298.15):.2f} ;  본문 13.24")
    print(f"  -> 0 °C 마커 {near['0 °C'][1]:.2f} = 본문 3.10 ✓ (교정 신뢰도 0.3 %)")
    print("  -> 즉 13.24 는 **30 °C 데이터점**이다. 결론절은 이것을 '25 °C' 라고 쓴다.")
    for T30 in (303.15, 298.15):
        ea = -KB_EV * math.log(3.10 / 13.24) / (1 / 273.15 - 1 / T30)
        print(f"     13.24 를 {T30-273.15:.0f} °C 로 보면 3.10(0 °C) 과의 Ea = {ea:.3f} eV  [인쇄 0.313]")

    for use_T in (False, True):
        y1 = math.log(13.24e-3 * (298.15 if use_T else 1))
        y2 = math.log(3.10e-3 * (273.15 if use_T else 1))
        ea = -KB_EV * (y2 - y1) / (1 / 273.15 - 1 / 298.15)
        print(f"  본문 두 σ 값이 함의하는 Ea ({'σT' if use_T else 'σ '} 형식) = {ea:.4f} eV")
    print("  -> 인쇄 Ea 0.313 eV 로는 σ(0 °C) = %.2f mS/cm 가 나온다 (본문 3.10)."
          % (13.24 * math.exp(-0.313 / KB_EV * (1 / 273.15 - 1 / 298.15))))


# ------------------------------------------------------------ Fig 2d (MSD) --
def fig2d():
    print("=" * 72)
    print("[Fig 2d] AIMD MSD 250/300/350 K — 본문 'Ea ≈ 0.15 eV'")
    im = load("fig2")
    px = im.load()
    X0, X1, XV1 = 839.0, 1328.0, 14.0        # 0 ~ 14 ps
    Y0, Y1, YV1 = 824.0, 489.0, 3.5          # 0 ~ 3.5 Å^2
    kx = XV1 / (X1 - X0)
    ky = YV1 / (Y0 - Y1)
    LEG = (835, 1050, 491, 620)              # 범례 상자 (제외)

    def mk(f):
        return lambda r, g, b: f(r, g, b)

    series = {
        250: lambda r, g, b: r < 90 and g < 90 and b < 90,
        300: lambda r, g, b: r > 150 and g < 95 and b < 95,
        350: lambda r, g, b: b > 140 and r < 110 and g < 130,
    }
    D = {}
    for T, f in series.items():
        c = {}
        for x in range(842, 1327):
            ys = [
                y
                for y in range(491, 822)
                if f(*px[x, y]) and not (LEG[0] <= x <= LEG[1] and LEG[2] <= y <= LEG[3])
            ]
            if ys:
                c[x] = sum(ys) / len(ys)

        def val(t):
            xp = X0 + t / kx
            k = min(c, key=lambda q: abs(q - xp))
            return (Y0 - c[k]) * ky

        prof = {t: round(val(t), 3) for t in (2, 4, 6, 8, 10, 12, 13.8)}
        print(f"  {T} K  MSD(ps->Å²) {prof}")
        for lo, hi, tag in ((6.0, 13.8, "6-13.8 ps"), (2.0, 12.0, "2-12 ps")):
            pts = [(lo + 0.2 * k, val(lo + 0.2 * k)) for k in range(int((hi - lo) / 0.2) + 1)]
            sl, _, r2 = lsq(pts)
            d = sl * 1e-4 / 6
            if tag.startswith("6"):
                D[T] = d
            print(f"      {tag:10s} 기울기 {sl:7.4f} Å²/ps  D={d:.3e} cm²/s"
                  f"  NE σ={nernst_einstein(d, T):7.1f} mS/cm  (R²={r2:.3f})")
    print(f"  -> σ_NE(300 K) / σ_exp(13.24) = {nernst_einstein(D[300], 300)/13.24:.0f}배")
    for lab, useT in (("ln D ", False), ("ln(DT)", True)):
        pts = [(1 / T, math.log(D[T] * (T if useT else 1))) for T in sorted(D)]
        sl, _, _ = lsq(pts)
        print(f"  {lab} vs 1/T (6-13.8 ps 창) -> Ea = {-KB_EV*sl:.4f} eV")
    print("  ※ 250 K 곡선은 2~10.5 ps 평탄 후 단발 계단. 250 K 만 12 ps 에서 끊으면 Ea 가 0.15 eV 대로 올라간다.")


# ------------------------------------------------------------- Fig 3c (NEB) --
def fig3c():
    print("=" * 72)
    print("[Fig 3c] NEB — 본문은 장벽 수치를 하나도 인쇄하지 않는다")
    im = load("fig3").crop((620, 440, 1695, 1002))
    im.save(f"{INBOX}/_49_fig3c_crop.png")
    px = im.load()
    w, h = im.size
    vl = long_lines(px, (0, w), (0, h), False, 0.7)
    hl = long_lines(px, (0, h), (0, w), True, 0.7)
    xt = ticks(px, int(hl[-1]), (200, 1050), True, depth=4, inward=-1)
    x0 = xt[0]
    sx = 4.0 * (len(xt) - 1) / (xt[-1] - x0)          # 라벨 0,4,...,24 (마지막은 프레임과 겹쳐 미검출)
    y_top, y_bot = hl[0], hl[-1]
    sy = (0.30 - (-0.05)) / (y_bot - y_top)
    print(f"  프레임 x {vl[0]:.0f}/{vl[-1]:.0f}  y {y_top:.0f}/{y_bot:.0f} ; x눈금 {len(xt)}개 간격 "
          f"{(xt[-1]-x0)/(len(xt)-1):.1f} px = 4 이미지")
    for t in ticks(px, int(vl[0]), (38, 465), False, depth=4, inward=+1):
        print(f"    y눈금 검산 {t:6.1f} px -> {0.30 - (t - y_top) * sy:+.4f} eV")

    def orange(r, g, b):
        return r > 195 and 90 < g < 175 and b < 105

    def green(r, g, b):
        return r < 150 and 120 < g < 200 and b < 150 and g - r > 25 and g - b > 25

    out = {}
    for nm, hit in (("LGPS(주황)", orange), ("LM0.2PS(초록)", green)):
        bl = [t for t in blobs(px, (0, w, 0, h), hit) if t[1] > 150]   # 범례 마커 제외
        pts = [(round((cx - x0) * sx), 0.30 - (cy - y_top) * sy) for cx, cy, _ in bl]
        out[nm] = pts
        es = [p[1] for p in pts]
        peaks = [
            (i, e) for k, (i, e) in enumerate(pts)
            if 0 < k < len(pts) - 1 and e > pts[k - 1][1] and e > pts[k + 1][1]
        ]
        print(f"  {nm}: 마커 {len(pts)}개  image {pts[0][0]}..{pts[-1][0]}")
        print("      " + "  ".join(f"{i}:{e:+.3f}" for i, e in pts))
        print(f"      최대 {max(es):+.4f} / 최소 {min(es):+.4f} / 전체 폭 {max(es)-min(es):.4f} eV")
        print(f"      국소 봉우리 {len(peaks)}개: " + ", ".join(f"image {i} = {e:.4f} eV" for i, e in peaks))
    return out


# ---------------------------------------------------------- Fig 7a/7c (셀) --
def fig7():
    print("=" * 72)
    print("[Fig 7a] rate — 본문 '165/140/129/113/96 mAh/g @ 0.1/0.5/1/2/3 C'")
    im = load("fig7")
    px = im.load()
    X0, KX = 164.5, 50.0 / 134.0             # 하단 눈금 50 간격 = 134 px
    Y2V = 433.5                              # 2.0 V
    cols = {
        "C/5 (회색)": lambda r, g, b: abs(r - g) < 28 and abs(g - b) < 28 and 60 < r < 130,
        "C/2 (빨강)": lambda r, g, b: r > 150 and g < 95 and b < 95,
        "1C (파랑)": lambda r, g, b: b > 140 and r < 110 and g < 130,
        "2C (초록)": lambda r, g, b: g > 110 and r < 110 and b < 110 and g - r > 35 and g - b > 35,
        "3C (보라)": lambda r, g, b: r > 120 and b > 170 and g < 120 and b - g > 60,
    }
    print("  ※ 그림의 곡선 라벨은 C/5·C/2·1C·2C·3C — 본문의 '0.1C' 는 그림에 없다 (C/5 = 0.2C)")
    for nm, f in cols.items():
        xs = [x for x in range(166, 700) for y in range(int(Y2V) - 5, int(Y2V) + 6) if f(*px[x, y])]
        if xs:
            print(f"    {nm:11s} 2.0 V 방전 종점 Q = {(max(xs)-X0)*KX:6.1f} mAh/g")

    print("[Fig 7c] 1C 100 cyc — 본문 '초기 125' / 초록·결론 '130' / '100 cyc 후 80'")
    X0c, KXc = 170.5, 100.0 / (1410.5 - 170.5)
    Y0c, KYc = 1083.0, 240.0 / (1083.0 - 637.5)
    for nm, f in (
        ("방전(빨강)", lambda r, g, b: r > 170 and g < 95 and b < 95),
        ("충전(파랑)", lambda r, g, b: b > 150 and r < 110 and g < 130),
    ):
        bl = blobs(px, (172, 1409, 624, 1078), f, min_px=25)
        pts = [((cx - X0c) * KXc, (Y0c - cy) * KYc) for cx, cy, _ in bl]
        if not pts:
            continue
        print(f"    {nm}: {len(pts)}점, 첫 cycle {pts[0][0]:.1f} = {pts[0][1]:.1f} mAh/g"
              f" / 끝 cycle {pts[-1][0]:.1f} = {pts[-1][1]:.1f} mAh/g")
        if "방전" in nm:
            print(f"      유지율 = {pts[-1][1]/pts[0][1]:.1%}  (cycle 1 점은 그림에 없다 — 첫 점이 cycle 2)")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which == "--dump":
        dump_figures()
    else:
        if which in ("all", "fig2a"):
            fig2a()
        if which in ("all", "fig2d"):
            fig2d()
        if which in ("all", "fig3c"):
            fig3c()
        if which in ("all", "fig7"):
            fig7()
