#!/usr/bin/env python3
"""zhou2026 (Chem. Eng. J. 539 (2026) 177014) — **SI 27 pp** 실물 독립 검증.

litdb/papers/zhou2026_high_entropy_lgps_multicationic.md §21 의 근거 스크립트.
본문 검증(§20)은 tools/litdb/zhou2026_fig_extract.py 가 만들었고, 이 파일은 그때
"inbox 에 SI PDF 가 없다"며 미룬 §20.13 Q1–Q5 를 SI 실물로 닫기 위한 것이다.

핵심 대상
  fig311 : SI Fig 3-11 = H-LM0.2PS(열간가압) Nyquist 16패널(-50~100 °C, 10 °C 격자).
           패널마다 축을 캘리브레이션하고 커브 최저점(cusp) Z' 를 픽셀에서 복원 ->
           sigma(T) = d/(R*A), d=1.362 mm, A=0.785 cm^2 -> 독립 아레니우스.
           * 25 °C 패널이 존재하는가? (본문 Fig 2a 판독 = "없다" 의 SI 교차확인)
  tabS3  : SI Table S3 전자전도도 3점 -> 옴 법칙 선형성 주장 재검산
  tabS4  : SI Table S4 Rietveld -> 셀부피, Li 총수, 4d 자리 점유 합
  cell   : 5원소 등몰(0.2)을 LGPS 단위셀(50원자)로 표현 가능한가 -> 최소 슈퍼셀

의존성: PyMuPDF(fitz, --dump 시) + PIL. **numpy/scipy 없이 순수 파이썬**
        (이 머신에 numpy 미설치 — zhou2026_fig_extract.py 와 같은 제약)

usage:
  python tools/litdb/zhou2026_si_verify.py --dump    # SI PDF -> _49si_fig311.png
  python tools/litdb/zhou2026_si_verify.py all
"""
import math
import sys

from PIL import Image

INBOX = "litdb/inbox"
PDF = (
    f"{INBOX}/49. Sup) A high-entropy multicationic substituted Li10GeP2S12 "
    "solid electrolyte enabling stable all-solid-state batteries.pdf"
)
FIG311 = f"{INBOX}/_49si_fig311.png"

KB_EV = 8.617333262e-5      # eV/K
D_HOT = 0.1362              # cm  (SI Table S2, H-LM0.2PS 두께 1.362 mm)
AREA = 0.785                # cm^2 (SI Table S3 각주, Φ10 mm)

# SI Fig 3-11 패널 격자 (784x666 원본 임베디드 이미지 좌표)
BOT = [135, 309, 476, 639]                                  # 각 행 x축(박스 아래변) y
COL = [(18, 192), (226, 388), (422, 584), (618, 780)]       # 각 열 박스 x 범위
TOP = [7, 181, 355, 521]
# (행, 열) -> (온도 °C, x축 major tick 값 리스트)
PANELS = {
    (0, 0): (100, [0, 2, 4, 6, 8, 10, 12]),
    (0, 1): (90, [0, 2, 4, 6, 8, 10, 12]),
    (0, 2): (80, [0, 3, 6, 9, 12, 15]),
    (0, 3): (70, [0, 3, 6, 9, 12, 15]),
    (1, 0): (60, [0, 5, 10, 15, 20]),
    (1, 1): (50, [0, 5, 10, 15, 20, 25, 30]),
    (1, 2): (40, [0, 5, 10, 15, 20, 25, 30, 35]),
    (1, 3): (30, [0, 10, 20, 30, 40, 50, 60, 70, 80]),
    (2, 0): (20, [0, 20, 40, 60, 80, 100]),
    (2, 1): (10, [0, 30, 60, 90, 120, 150]),
    (2, 2): (0, [0, 50, 100, 150, 200, 250, 300]),
    (2, 3): (-10, [0, 100, 200, 300, 400, 500, 600]),
    (3, 0): (-20, [0, 150, 300, 450, 600, 750]),
    (3, 1): (-30, [0, 300, 600, 900, 1200, 1500]),
    (3, 2): (-40, [0, 300, 600, 900, 1200, 1500, 1800]),
    (3, 3): (-50, [0, 600, 1200, 1800, 2400, 3000]),
}


# ------------------------------------------------------------------ 공통 유틸
def dump_figure():
    import fitz

    d = fitz.open(PDF)
    pix = fitz.Pixmap(d, 106)          # SI p10 하단 = Fig 3-11 16패널 그리드
    pix.save(FIG311)
    print(f"  fig311: {pix.width}x{pix.height} -> {FIG311}")


def load():
    return Image.open(FIG311).convert("RGB")


def is_dark(px, x, y, thr=680):
    r, g, b = px[x, y]
    return r + g + b < thr


def is_teal(px, x, y):
    """데이터 마커/선 = 청록. 회색 축·검은 텍스트와 분리."""
    r, g, b = px[x, y]
    return g > r + 18 and b > r + 10 and g < 235 and r + g + b < 700


def runs_of(xs, gap=2):
    out, cur = [], []
    for i in xs:
        if cur and i - cur[-1] > gap:
            out.append(cur)
            cur = []
        cur.append(i)
    if cur:
        out.append(cur)
    return [sum(c) / len(c) for c in out]


def best_ap(cands, n_need):
    """후보 위치에서 등차수열(major tick) n_need 개를 가장 잘 설명하는 (x0, step)."""
    best = None
    for i in range(len(cands)):
        for j in range(i + 1, len(cands)):
            for k in range(1, n_need):
                step = (cands[j] - cands[i]) / k
                if step < 15:       # 15 px 미만 = minor tick (100 °C 패널 오인 방지)
                    continue
                x0 = cands[i]
                err, hit = 0.0, 0
                for m in range(n_need):
                    tgt = x0 + m * step
                    near = min(cands, key=lambda c: abs(c - tgt))
                    dd = abs(near - tgt)
                    if dd < 3.5:
                        hit += 1
                        err += dd
                    else:
                        err += 3.5
                score = (hit, -err)
                if best is None or score > best[0]:
                    best = (score, x0, step)
    return best[1], best[2]


# ------------------------------------------------------------------ fig 3-11
def fig311():
    im = load()
    px = im.load()
    print("SI Fig 3-11 — H-LM0.2PS 열간가압 Nyquist 16패널 픽셀 복원")
    print(f"  sigma = d/(R*A), d = {D_HOT*10:.3f} mm, A = {AREA} cm^2 (SI Table S2/S3)")
    print()
    print("   T(°C)   x0px   px/unit   cusp Z'(Ω)   sigma(mS/cm)   1000/T   ln(sigmaT)")
    out = []
    for (ri, ci), (temp, ticks) in sorted(PANELS.items(), key=lambda kv: -kv[1][0]):
        y0, ytop = BOT[ri], TOP[ri]
        x1, x2 = COL[ci]
        cands = [c for c in runs_of([x for x in range(x1, x2) if is_dark(px, x, y0 - 2)])
                 if x1 + 6 < c < x2 - 6]
        xt0, step = best_ap(cands, len(ticks))
        unit = step / (ticks[1] - ticks[0])          # px per Ω
        teal = [(x, y) for y in range(ytop + 2, y0 - 1)
                for x in range(x1 + 2, x2 - 2) if is_teal(px, x, y)]
        ymax = max(y for _, y in teal)
        cusp = [x for x, y in teal if y >= ymax - 1]
        xc = sum(cusp) / len(cusp)
        r_ohm = (xc - xt0) / unit
        sigma = D_HOT / (r_ohm * AREA) * 1e3         # mS/cm
        tk = temp + 273.15
        out.append((tk, sigma, r_ohm))
        print(f"  {temp:5d}  {xt0:6.1f}  {unit:8.3f}   {r_ohm:9.2f}   {sigma:10.3f}"
              f"   {1000/tk:7.3f}   {math.log(sigma*tk):9.3f}")

    # 아레니우스 (sigma*T 형식, 논문과 동일하게 sigma=A exp(-Ea/kT) 도 병기)
    for label, yf in (("sigma*T", lambda s, t: math.log(s * t)),
                      ("sigma  ", lambda s, t: math.log(s))):
        for lo, hi in ((-50, 100), (0, 100), (20, 60), (-50, 0), (-50, -10)):
            pts = [(1 / t, yf(s, t)) for t, s, _ in out
                   if lo <= t - 273.15 <= hi]
            n = len(pts)
            sx = sum(p[0] for p in pts) / n
            sy = sum(p[1] for p in pts) / n
            num = sum((p[0] - sx) * (p[1] - sy) for p in pts)
            den = sum((p[0] - sx) ** 2 for p in pts)
            slope = num / den
            ea = -slope * KB_EV
            ss = sum((p[1] - sy) ** 2 for p in pts)
            rr = 1 - sum((p[1] - (sy + slope * (p[0] - sx))) ** 2 for p in pts) / ss
            print(f"  Ea[{label}] {lo:+4d}..{hi:+4d} °C ({n}점) = {ea:.4f} eV   R^2={rr:.5f}")
    print()
    print("  * 인쇄값: Ea = 0.313 eV (본문 Fig 2a) / 0.31 (SI Table S2)")
    print("  * 25 °C 패널: 존재하지 않음 (격자가 -50..100 °C 10 °C 간격)")
    s30 = [s for t, s, _ in out if abs(t - 303.15) < 0.1][0]
    s20 = [s for t, s, _ in out if abs(t - 293.15) < 0.1][0]
    print(f"  * 30 °C 복원 sigma = {s30:.2f} mS/cm (인쇄 13.24), "
          f"20 °C = {s20:.2f} (본문 Fig 2a 마커 9.31)")
    lo, hi = sorted((s20, s30))
    print(f"  * 25 °C 를 굳이 쓰려면 20/30 °C 사이 내삽 = {math.sqrt(lo*hi):.2f} mS/cm")


# ------------------------------------------------------------------ Table S3
def tabS3():
    print("SI Table S3 — DC 분극 전자전도도 재검산 (본문 주장: '완벽한 선형 = 옴 법칙')")
    L, A = 0.1624, 0.785            # cm  (냉간가압 LM0.2PS 두께 1.624 mm)
    data = [(300, 1.554e-6), (400, 2.424e-6), (500, 3.363e-6)]   # mV, mA
    print("   V(mV)   I(nA)   sigma_e(S/cm) 재계산   인쇄값     R_chord(Ω)")
    printed = [1.07e-9, 1.25e-9, 1.39e-9]
    for (v, i_ma), p in zip(data, printed):
        i_a = i_ma * 1e-3
        s = i_a * L / (v * 1e-3 * A)
        print(f"  {v:5d}  {i_ma*1e6:6.3f}   {s:.4e}          {p:.2e}   {v*1e-3/i_a:.3e}")
    n = len(data)
    sx = sum(v for v, _ in data) / n
    sy = sum(i for _, i in data) / n
    slope = sum((v - sx) * (i - sy) for v, i in data) / sum((v - sx) ** 2 for v, _ in data)
    icept = sy - slope * sx
    ss = sum((i - sy) ** 2 for _, i in data)
    rr = 1 - sum((i - (icept + slope * v)) ** 2 for v, i in data) / ss
    print(f"  선형회귀 I(V): 기울기 {slope:.4e} mA/mV, 절편 {icept*1e6:+.3f} nA, R^2={rr:.5f}")
    print(f"  -> 절편이 0 이 아니다: V=0 에서 {icept*1e6:+.3f} nA, x절편 {-icept/slope:.1f} mV")
    print(f"  -> chord 저항이 300->500 mV 에서 {100*(1-(500/3.363e-6)/(300/1.554e-6)):.1f} % 감소")
    print(f"     (= sigma_e 가 {100*(1.39/1.07-1):.0f} % 증가) — '일정한 전자저항' 주장과 불일치")
    s_slope = slope * 1e-3 * L / (1e-3 * A)
    print(f"  기울기(미분) 기준 sigma_e = {s_slope:.3e} S/cm "
          f"(= 인쇄 최저값의 {s_slope/1.07e-9:.2f}배)")


# ------------------------------------------------------------------ Table S4
def tabS4():
    print("SI Table S4 — Rietveld 재검산 (P42/nmc, a=b=8.70078 Å, c=12.59562 Å, 298 K)")
    a, c = 8.70078, 12.59562
    v = a * a * c
    print(f"  셀부피 V = a^2 c = {v:.2f} Å^3   (본문 Fig 1c figure-read 951.5 -> 오차 "
          f"{100*(951.5-v)/v:+.2f} %)")
    li = [("Li1", 16, 0.474), ("Li2", 4, 0.89), ("Li3", 8, 0.72), ("Li4", 4, 0.77)]
    tot = sum(m * o for _, m, o in li)
    print("  Li 총수 = " + " + ".join(f"{m}x{o}" for _, m, o in li) +
          f" = {tot:.3f}  (Z=2 x Li10 = 20 -> {100*(tot-20)/20:+.2f} %)")
    site4d = [("Ge", 0.1), ("P1", 0.5), ("W", 0.1), ("Sn", 0.1), ("Si", 0.1), ("Ti", 0.1)]
    print("  4d 점유 합 = " + " + ".join(f"{n} {o}" for n, o in site4d) +
          f" = {sum(o for _, o in site4d):.2f}")
    print("  4d 자리 4개/셀 -> M 원자수 = 4 x (0.1x5) = "
          f"{4*0.5:.1f} 개, 원소당 {4*0.1:.1f} 개")
    print("  Uiso 폭: S3 0.00150 ~ S2 0.03546 (같은 S 자리끼리 "
          f"{0.03546/0.00150:.0f}배), Li3 0.07247 (B = {8*math.pi**2*0.07247:.1f} Å^2)")
    print("  주: '고엔트로피 양이온 점유는 공칭 화학량론으로 구속' — 정련으로 결정한 값이 아님")
    print("  주: Rwp / chi^2 / GOF 미보고 -> 정련 품질 검증 불가")


# ------------------------------------------------------------------ 슈퍼셀
def cell():
    print("5원소 등몰(각 0.2) 을 LGPS 격자에 정수 원자수로 담는 최소 슈퍼셀")
    print("  LGPS 단위셀(P42/nmc, Z=2) = Li 20 + M 2 + P 4 + S 24 = 50 원자")
    print("  M 2개/셀을 5원소로 등몰 분배 -> 원소당 0.4 개/셀 (정수 불가)")
    for n in range(1, 13):
        per = 0.4 * n
        ok = abs(per - round(per)) < 1e-9
        if ok:
            print(f"  셀 {n:2d}개: 원소당 {per:.1f} 개, 총 {50*n} 원자  <= 최소 정수해"
                  if n == 5 else
                  f"  셀 {n:2d}개: 원소당 {per:.1f} 개, 총 {50*n} 원자")
    print("  -> 배수는 5의 배수여야 한다 (1x1x5 / 5x1x1 등 = 250 원자, AIMD 15 ps 기준 무거움)")
    print("  -> SI 는 슈퍼셀 배수도 원자수도 쓰지 않았고, SI Fig 5 는 'unit cell' 이라 명시한다")
    print("     (부분점유 구를 그린 Rietveld CIF 시각화 = MD 입력이 될 수 없는 그림)")


# ------------------------------------------------------------------ 그림 공통
def _near(c, ref, t=60):
    return sum((a - b) ** 2 for a, b in zip(c, ref)) ** 0.5 < t


def _apex(px, xr, yr, ref, thick=4, t=60):
    """색 ref 인 두께 thick 이상 세로런의 최고점 x (지시선/앤티앨리어싱 배제).

    ref 가 콜백이면 (r,g,b)->bool 판정자로 쓴다 (RGB 거리보다 색상 분리가 정확한 경우).
    """
    hit = ref if callable(ref) else (lambda r, g, b: _near((r, g, b), ref, t))
    best = None
    for x in range(*xr):
        ys = [y for y in range(*yr) if hit(*px[x, y])]
        runs, cur = [], []
        for y in ys:
            if cur and y - cur[-1] > 1:
                runs.append(cur)
                cur = []
            cur.append(y)
        if cur:
            runs.append(cur)
        runs = [r for r in runs if len(r) >= thick]
        if runs:
            top = min(r[0] for r in runs)
            if best is None or top < best[1]:
                best = (x, top)
    return best


# ------------------------------------------------------------------ SI Fig 6
def figS6():
    """AIMD 아레니우스 3점 — y축이 정말 선형 눈금인가."""
    print("SI Fig 6 — AIMD ln(D_T) vs 1/T (원본 1298x798)")
    yt = {-21.886: 112.5, -22.218: 333.0, -22.916: 553.5}
    ks = sorted(yt, reverse=True)
    d1, d2 = yt[ks[1]] - yt[ks[0]], yt[ks[2]] - yt[ks[1]]
    print(f"  y 주눈금 픽셀간격 = {d1:.1f} px / {d2:.1f} px  (동일)")
    print(f"  그 눈금의 값 간격 = {ks[0]-ks[1]:.3f} / {ks[1]-ks[2]:.3f}  "
          f"(비 {(ks[1]-ks[2])/(ks[0]-ks[1]):.2f})")
    print("  -> **y축은 선형 눈금이 아니다.** 세 데이터값을 등간격 커스텀 눈금으로 찍었다.")
    print("     그림 위 빨간 'Linear fit' 의 기울기는 물리량이 아니다.")
    pts = [(1 / 350, -21.886), (1 / 300, -22.218), (1 / 250, -22.916)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        print(f"  구간 기울기 {1/x1:.0f}->{1/x2:.0f} K : Ea = {-(y2-y1)/(x2-x1)*KB_EV:.4f} eV")
    n = len(pts)
    sx = sum(p[0] for p in pts) / n
    sy = sum(p[1] for p in pts) / n
    slope = (sum((p[0]-sx)*(p[1]-sy) for p in pts) / sum((p[0]-sx)**2 for p in pts))
    print(f"  3점 최소제곱 Ea = {-slope*KB_EV:.4f} eV   <-> 그림 인쇄값 0.15 eV "
          f"({0.15/(-slope*KB_EV):.2f}배)")
    print("  마커 실측 = (361.7,113.9)/(718.7,332.7)/(1219.4,552.2) px "
          "= 1/350, 1/300, 1/250 과 눈금값 위에 정확히 일치")


# ------------------------------------------------------------------ SI Fig 8
def figS8():
    """XPS 성분 위치 — Q1."""
    im = Image.open(f"{INBOX}/_49si_figS8.png").convert("RGB")
    px = im.load()
    print("SI Fig 8 — XPS 성분 봉우리 위치 픽셀 복원 (SI 에는 숫자가 하나도 인쇄돼 있지 않다)")
    # (c) Ti 2p : 눈금 908 px = 468 eV, 21.5 px/eV (역방향 축)
    be_c = lambda x: 468 - (x - 908) / 21.5
    RED = lambda r, g, b: r > 150 and g < 110 and b < 110
    YEL = lambda r, g, b: r > 150 and g > 140 and b < 110
    BLU = lambda r, g, b: b > 130 and r < 110 and g < 130
    for lab, ref, th in (("Ti '4+' 성분(빨강)", RED, 4),
                         ("Ti '0' 성분(노랑)", YEL, 3),
                         ("Ti '0' 성분(파랑)", BLU, 1)):
        b = _apex(px, (868, 1249), (20, 309), ref, th)
        if b:
            print(f"  (c) {lab:22s} = {be_c(b[0]):7.2f} eV")
    print("      (c) 검은 포락선 광폭 봉우리 = 464.6 eV")
    print("      -> '4+' 쌍 458.8/464.6 : SO 분리 5.8 eV OK, 그러나 이는 **TiO2** 위치"
          " (TiS2 Ti4+ 는 456.0-457.0)")
    print("      -> '0' 쌍 455.4/460.0 : 분리 4.6 eV — Ti 2p 이중항(5.7-6.1)이 아니다."
          " Ti 금속 2p3/2 는 453.9")
    # (d) Si 2p : 45 px = 106 eV, 36.333 px/eV
    be_d = lambda x: 106 - (x - 45) / 36.333
    for lab, ref in (("주성분(빨강)", RED), ("어깨(파랑)", BLU)):
        b = _apex(px, (14, 404), (430, 779), ref, 4)
        if b:
            print(f"  (d) Si 2p {lab:12s} = {be_d(b[0]):7.2f} eV  (봉우리 높이 {781-b[1]} px)")
    print("      -> 본문이 인쇄한 '~102.5 eV, dominant Si4+' 는 **작은 쪽** 성분이다")
    # (e) Sn 3d : 505 px = 496 eV, 19.8333 px/eV
    be_e = lambda x: 496 - (x - 505) / 19.8333
    b = _apex(px, (428, 821), (420, 781), RED, 4)
    if b:
        print(f"  (e) Sn 3d5/2 = {be_e(b[0]):.2f} eV   <-> 본문 인쇄 485.0 eV "
              f"(차이 {be_e(b[0])-485.0:+.2f} eV)")
    print("      -> SI 그림 위치는 정상 Sn4+ (SnS2 486.3-486.8 / SnO2 486.6). "
          "틀린 것은 데이터가 아니라 본문에 옮겨적은 숫자다")


# ------------------------------------------------------------------ SI Fig 1b
def figS1b():
    """(203) 피크 이동 — 격자 팽창/수축 주장(§9a)의 원자료."""
    import math
    im = Image.open(f"{INBOX}/_49si_figS1.png").convert("RGB")
    px = im.load()
    tt = lambda x: 28 + (x - 802) / ((1095 - 802) / 4)     # 802 px=28°, 1095 px=32°
    REF = [("Li10GeP2S12 (ref)", (90, 90, 90), (360, 448)),
           ("Si", (237, 125, 49), (2, 448)), ("Sn", (50, 90, 200), (2, 448)),
           ("Ti", (60, 160, 110), (2, 448)), ("W (비정질)", (190, 140, 220), (2, 448)),
           ("Si/Ge/Sn", (200, 170, 40), (2, 448)),
           ("Si/Ge/Sn/Ti", (40, 200, 215), (2, 448)),
           ("Si/Ge/Sn/W", (140, 70, 70), (2, 448)),
           ("Si/Sn/W/Ti", (150, 150, 40), (2, 448)),
           ("5원소 LM0.2PS", (240, 60, 60), (2, 448))]
    print("SI Fig 1b — (203) 피크 위치 (안내 점선 = 29.488° = LGPS 자기 피크)")
    print("  조성                2theta(°)   d(203)(Å)   Δ2theta vs LGPS")
    ref0 = None
    for lab, c, yr in REF:
        pts = [(x, y) for x in range(805, 1093) for y in range(*yr)
               if _near(px[x, y], c, 45)]
        if len(pts) < 150:      # 색이 안 잡히면(=비정질로 봉우리가 없으면) 인용 금지
            print(f"  {lab:20s} 검출 실패 (색 픽셀 {len(pts)}개)")
            continue
        ym = min(y for _, y in pts)
        xs = [x for x, y in pts if y <= ym + 2]
        th = tt(sum(xs) / len(xs))
        d = 1.5406 / (2 * math.sin(math.radians(th / 2)))
        if ref0 is None:
            ref0 = th
        elif abs(th - 29.488) < 0.012:
            # 회색 안내 점선과 색 트레이스가 구분되지 않은 경우 = 판독 실패로 처리
            print(f"  {lab:20s}   판독 불가 (안내 점선과 분리 실패)")
            continue
        print(f"  {lab:20s} {th:8.3f}   {d:8.4f}   {th-ref0:+7.3f}")
    print("  ⚠ 색 분리 임계값을 흔들면 Si·Si/Ge/Sn 행이 안내선으로 붕괴한다 -> 두 행은 인용 금지.")
    print("    -0.18(Sn) / -0.14(Si,Ge,Sn,Ti) / +0.03(5원소) 세 값만 임계값에 강건했다")
    print("  ⚠ W 는 비정질이라 봉우리 자체가 없다 — 값 인용 금지")
    print("  ⚠ (203) 은 1/d^2 = 4/a^2 + 9/c^2 이라 a·c 가 반대로 움직이면 이동이 상쇄된다."
          " 단일 반사로 부피를 논증할 수 없다")


# ------------------------------------------------------------------ SI Fig 15
def figS15():
    """풀셀 임피던스 4.2 V 유지 — Q5 주변."""
    im = Image.open(f"{INBOX}/_49si_figS15.png").convert("RGB")
    px = im.load()
    z = lambda x: 60 + (x - 830) / 1.1278       # 830 px = 60 Ω, 67.67 px/60 Ω
    SER = [("3.8 V 1st charge", (35, 35, 35), 3), ("4.2 V 1st charge", (228, 38, 44), 3),
           ("3.6 V 2nd charge", (30, 70, 190), 3), ("4.2 V 0 h", (40, 160, 70), 2),
           ("4.2 V 10 h", (160, 90, 200), 3), ("4.2 V 20 h", (200, 160, 30), 3),
           ("4.2 V 50 h", (30, 190, 190), 3)]
    print("SI Fig 15b — LNO@NCM721|LM0.2PS|LiIn 풀셀 임피던스 (호의 오른쪽 종점)")
    for lab, ref, th in SER:
        best = -1
        for x in range(900, 1245):
            ys = [y for y in range(210, 406) if _near(px[x, y], ref, 60)]
            runs, cur = [], []
            for y in ys:
                if cur and y - cur[-1] > 1:
                    runs.append(cur)
                    cur = []
                cur.append(y)
            if cur:
                runs.append(cur)
            if any(len(r) >= th for r in runs):
                best = x
        print(f"  {lab:20s} Z' 종점 ≈ {z(best):6.0f} Ω" if best > 0 else f"  {lab} 실패")
    print("  * 좌측 절편은 전 계열 ≈70 Ω 로 같다 -> 커진 것은 계면호(SE 벌크 아님)")
    print("  * 3.8 V -> 4.2 V 유지 50 h 에서 단조 증가, 유지 중에도 포화하지 않는다")
    print("  ⚠ 3.8 V 곡선은 다른 곡선에 덮여 종점 검출이 불안정(≈210-250 Ω)")


def main():
    if "--dump" in sys.argv:
        dump_figure()
        return
    todo = [a for a in sys.argv[1:] if not a.startswith("-")] or ["all"]
    tasks = {"fig311": fig311, "figS6": figS6, "figS8": figS8, "figS1b": figS1b,
             "figS15": figS15, "tabS3": tabS3, "tabS4": tabS4, "cell": cell}
    for name, fn in tasks.items():
        if "all" in todo or name in todo:
            fn()
            print("-" * 78)


if __name__ == "__main__":
    main()
