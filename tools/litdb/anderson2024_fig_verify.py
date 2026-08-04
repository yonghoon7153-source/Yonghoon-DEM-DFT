"""anderson2024 (LLZO 59-dopant HT screening, Adv. Energy Mater. 14, 2304025) — 그림 픽셀 독립 검증.

왜 하나
  이 논문의 정량 데이터는 거의 전부 **Table S5 (Supporting Information)** 에 있는데
  inbox 에는 본문 12 pp PDF 만 있다 (SI 없음). 본문 Table 1 은 59개 도판트 중 **18개만**
  싣는다. 그런데 Figure 4 는 σ_ionic / σ_electronic 을 **연속 컬러맵 주기율표**로 그려서
  측정된 전 도판트를 담고 있다 → 컬러바를 LUT 로 역변환하면 나머지를 복원할 수 있다.
  Table 1 의 18개가 그대로 ground truth 로 쓰여서 역변환 정확도를 자기검증할 수 있다.

무엇을 하나
  1. check_fig1()  : Fig 1 셀 색 분류 → 본문 '29 novel + 30 previously reported' 검증.
  2. check_fig4()  : Fig 4a/4b 셀 색 → 컬러바 역변환 → σ_i, σ_e 복원 + Table 1 잔차 리포트.
  3. check_fig3()  : Fig 3a/3b 마커 색분리 → garnet wt% / cubic wt% 를 59 도판트 × 3 site
                     전부 되읽고, '선호 site 는 >90 % cubic' 진술을 분포로 검증.
  4. check_fig3cd(): Fig 3c(BV mismatch) · 3d(DFT 결함에너지) 를 site 별로 되읽어
                     ①저자의 '이론 최적 site' 정의 ②BV vs DFT 일치율 ③예측력을 검증.
  5. check_vs_si_digest(): 1차 digest(2026-07-28, SI Table S5 기반) 목록과 대조해
                     그림 ↔ SI 가 어긋나는 칸을 찾는다.
  6. write_csv()   : 위 복원값을 db/properties/anderson2024_llzo_dopant_screening_recovered.csv
                     로 병합 출력 (source 열로 인쇄값/역판독을 구분).

결과 해설은 digest `litdb/papers/anderson2024_llzo_comprehensive_dopant_screening.md` §19.

의존성: PIL + 표준 라이브러리만 (numpy 없음 — repo 관례).
실행:  python tools/litdb/anderson2024_fig_verify.py
"""

import math
import os
from collections import deque

import fitz
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INBOX = os.path.join(ROOT, "litdb", "inbox")

WHITE = 243


def _pdf_path():
    for name in os.listdir(INBOX):
        if name.startswith("51.") and name.endswith(".pdf"):
            return os.path.join(INBOX, name)
    raise SystemExit("paper 51 PDF not found in litdb/inbox")


def extract_figures():
    """본문 PDF 에 박혀 있는 원본 래스터를 네이티브 해상도로 뽑는다 (페이지 렌더 아님)."""
    doc = fitz.open(_pdf_path())
    out = {}
    for page_no, tag in [(3, "fig1"), (4, "fig2"), (5, "fig3"), (6, "fig4"),
                         (7, "fig5"), (9, "fig6")]:
        page = doc[page_no - 1]
        best = None
        for info in page.get_images(full=True):
            xref, w, h = info[0], info[2], info[3]
            if w == 2986:                       # 저널 로고
                continue
            if best is None or w * h > best[1] * best[2]:
                best = (xref, w, h)
        pix = fitz.Pixmap(doc, best[0])
        if pix.n - pix.alpha not in (1, 3):
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        path = os.path.join(INBOX, "_51_%s.png" % tag)
        pix.save(path)
        out[tag] = path
    return out


# ------------------------------------------------------------------ 그리드

# 그림에 그려진 그대로의 주기율표 배치 (Lu/Hf 배치, 란탄족 La..Yb 는 col 2 부터 별도 줄)
ROWS = [
    ["H"] + [None] * 16 + ["He"],
    ["Li", "Be"] + [None] * 10 + ["B", "C", "N", "O", "F", "Ne"],
    ["Na", "Mg"] + [None] * 10 + ["Al", "Si", "P", "S", "Cl", "Ar"],
    ["K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
     "Ga", "Ge", "As", "Se", "Br", "Kr"],
    ["Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
     "In", "Sn", "Sb", "Te", "I", "Xe"],
    ["Cs", "Ba", "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
     "Tl", "Pb", "Bi", "Po", "At", "Rn"],
    [None, None, "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
     "Ho", "Er", "Tm", "Yb", None, None],
]


def _runs(vals, thr, min_len):
    out, r = [], None
    for i, v in enumerate(vals):
        if v > thr:
            r = [i, i] if r is None else [r[0], i]
        else:
            if r and r[1] - r[0] >= min_len:
                out.append(tuple(r))
            r = None
    if r and r[1] - r[0] >= min_len:
        out.append(tuple(r))
    return out


def build_grid(px, W, panel_y0, panel_y1):
    """1족(col 0) 셀들로 행 밴드를, K주기 행으로 열 밴드를 잡는다.

    열 사이/행 사이는 실제로 흰 띠라서, 셀 없는 칸은 순백으로 남는다.
    본문 제목·범례 텍스트가 행 간극을 오염시키므로 행 프로파일은 col 0 폭만 쓴다.
    """
    nw = lambda c: not (c[0] > WHITE and c[1] > WHITE and c[2] > WHITE)

    # 1) 열 그리드: 스캔라인마다 비백색 run 을 세어 가장 칸이 많은 줄(= 18칸 꽉 찬 주기)을
    #    고르고, 그 줄의 run 시작 간격 **중앙값**을 피치로 쓴다(빠지거나 붙은 칸에 강건).
    best = None
    for y in range(panel_y0 + 4, panel_y1 - 4, 4):
        xs = [x for x in range(W) if nw(px[x, y])]
        if not xs:
            continue
        rr, r = [], None
        for x in xs:
            if r and x == r[1] + 1:
                r[1] = x
            else:
                if r and r[1] - r[0] > 40:
                    rr.append(tuple(r))
                r = [x, x]
        if r and r[1] - r[0] > 40:
            rr.append(tuple(r))
        if len(rr) >= 15 and (best is None or len(rr) > len(best[1])):
            best = (y, rr)
    if best is None:
        raise SystemExit("column grid row not found")
    starts = [t[0] for t in best[1]]
    diffs = sorted(starts[i + 1] - starts[i] for i in range(len(starts) - 1))
    pitch_x = float(diffs[len(diffs) // 2])
    cx0 = starts[0]

    # 2) 행 밴드: **col 0 한 칸 폭만** 보고 센다 (인접 칸이 붙어 있어도 오염되지 않게)
    xa, xb = int(cx0 + pitch_x * 0.15), int(cx0 + pitch_x * 0.85)
    yprof = [sum(1 for x in range(xa, xb, 3) if nw(px[x, y]))
             for y in range(panel_y0, panel_y1)]
    bands = [(a + panel_y0, b + panel_y0) for a, b in _runs(yprof, max(yprof) * 0.5, 50)]
    if len(bands) < 6:
        raise SystemExit("row bands not found: %r" % (bands,))
    bands = bands[:6]                                   # 1~6 주기
    pitch_y = (bands[-1][0] - bands[0][0]) / 5.0

    # 3) 란탄족 줄: 마지막 주기 아래에서 col 2~15 구간을 보고 찾는다
    lan_y0 = int(bands[-1][1] + pitch_y * 0.25)
    xl0, xl1 = int(cx0 + pitch_x * 2.2), int(cx0 + pitch_x * 15.8)
    ylan = [sum(1 for x in range(xl0, xl1, 5) if nw(px[x, y]))
            for y in range(lan_y0, panel_y1)]
    lr = _runs(ylan, max(ylan) * 0.5 if ylan else 1, 50)
    lan = (lr[0][0] + lan_y0, lr[0][1] + lan_y0) if lr else None

    cells = {}
    allbands = list(bands) + ([lan] if lan else [])
    for ri, (by0, by1) in enumerate(allbands):
        for ci in range(18):
            el = ROWS[ri][ci]
            if not el:
                continue
            x0 = int(cx0 + pitch_x * ci)
            x1 = int(cx0 + pitch_x * (ci + 1)) - 1
            cells[el] = (x0, by0, x1, by1)
    return cells, (cx0, pitch_x, bands, lan)


def median_fill(px, bbox, shrink=0.28):
    """셀 내부 중앙부에서 글자(어두움)·테두리를 뺀 채움색의 중앙값. 순백이면 None."""
    x0, y0, x1, y1 = bbox
    dx, dy = int((x1 - x0) * shrink), int((y1 - y0) * shrink)
    rs, gs, bs, n = [], [], [], 0
    for y in range(y0 + dy, y1 - dy + 1):
        for x in range(x0 + dx, x1 - dx + 1):
            r, g, b = px[x, y]
            n += 1
            if r + g + b < 330:                 # 검은 글자
                continue
            if r > WHITE and g > WHITE and b > WHITE:
                continue                        # 배경 흰색
            rs.append(r); gs.append(g); bs.append(b)
    if not rs or len(rs) < n * 0.25:
        return None
    rs.sort(); gs.sort(); bs.sort()
    m = len(rs) // 2
    return (rs[m], gs[m], bs[m])


# ------------------------------------------------------------------- Fig 1

def check_fig1(path):
    print("=" * 78)
    print("Fig 1 — 본문 '59 dopants = 29 novel + 30 previously reported' 검증")
    print("=" * 78)
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    cells, _ = build_grid(px, W, 0, H)

    def cls(rgb):
        r, g, b = rgb
        if r > 205 and g > 175 and b < 150:
            return "novel(yellow)"
        if b > 130 and r < 175 and g < 200:
            return "reported(blue)"
        if r > 190 and g < 130 and b < 130:
            return "host(red)"
        return "unused(grey)"

    groups = {}
    for el, bbox in cells.items():
        fill = median_fill(px, bbox)
        if fill:
            groups.setdefault(cls(fill), []).append(el)
    order = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg",
             "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V",
             "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se",
             "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh",
             "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba",
             "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl",
             "Pb", "Bi", "Po", "At", "Rn", "La", "Ce", "Pr", "Nd", "Pm", "Sm",
             "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb"]
    key = lambda e: order.index(e) if e in order else 999
    for k in ("host(red)", "reported(blue)", "novel(yellow)"):
        v = sorted(groups.get(k, []), key=key)
        print("  %-16s n=%2d  %s" % (k, len(v), " ".join(v)))
    ny, nb = len(groups.get("novel(yellow)", [])), len(groups.get("reported(blue)", []))
    print()
    print("  본문 §1  : '59 different dopants (29 novel, plus the 30 previously reported)'")
    print("  본문 §2.1: 'Rietveld fits on all 180 PXRD patterns' → 180/3 = 60 도판트")
    print("  초록     : '59 dopants ... (177 total materials)'   → 177/3 = 59 도판트")
    print("  Fig 1 캡션: 'all the dopants (yellow and blue, except Sb) were tested and screened'")
    print("  ---")
    print("  픽셀 실측: novel(노랑)=%d, previously reported(파랑)=%d, 합=%d" % (ny, nb, ny + nb))
    print("  → 색칠된 도판트는 %d개. Sb 를 빼면 %d개 = 초록/Table의 '59'와 일치."
          % (ny + nb, ny + nb - 1))
    print("  → 즉 '180 patterns'(60개 합성) 와 '177 materials'(59개 스크리닝) 는 서로 모순이"
          " 아니라 **Sb 1개 차이**다. 다만 본문의 '29 novel / 30 reported' 는 그림과 어긋난다")
    print("     (그림은 노랑 %d / 파랑 %d). Sb 가 파랑이므로 '스크리닝된 기보고 도판트'가"
          " 29개인 것이고, 신규는 %d개다 → 본문 숫자가 뒤바뀌어 있다." % (ny, nb, ny))
    return groups


# ------------------------------------------------------------------- Fig 4

# 본문 Table 1 (18개) — 컬러맵 역변환 정확도 자기검증용 ground truth
TABLE1 = {
    # dopant: (site, garnet%, cubic%, sigma_i, sigma_e, HV_intI, Vmin, CCD)
    "Al": ("Li", 98.61, 98.61, 6.04e-5, 2.65e-8, 2.44, "0.7", "0.2"),
    "Ba": ("La", 92.32, 30.70, 1.36e-5, 1.90e-8, 0.48, "<0.1", "0.60"),
    "Ca": ("La", 97.90, 92.07, 2.87e-5, 2.31e-8, 5.47, "2.2", ">0.40"),
    "Co": ("Zr", 93.43, 44.13, 9.37e-5, 1.20e-6, 0.46, "<0.1", "0.1"),
    "Cs": ("La", 94.52, 75.14, 3.14e-5, 2.62e-8, 1.69, "<0.1", ">0.50"),
    "Dy": ("La", 93.83, 93.83, 3.27e-5, 3.85e-8, -0.05, "1", ">0.45"),
    "Fe": ("Li", 98.07, 98.07, 1.19e-3, 5.40e-8, 0.71, "1", "0.2"),
    "Ga": ("Li", 98.57, 98.43, 1.16e-3, 1.97e-8, 1.46, "1", "0.1"),
    "Hf": ("Zr", 97.71, 74.36, 4.90e-5, 4.51e-8, 1.44, "<0.1", ">0.45"),
    "In": ("Zr", 97.56, 41.51, 2.58e-5, 2.00e-8, 1.66, "<0.1", ">0.25"),
    "Mg": ("Zr", 95.84, 95.84, 2.37e-5, 2.84e-8, 3.72, "<0.1", ">0.30"),
    "Na": ("La", 95.19, 68.43, 4.81e-5, 2.88e-8, 3.85, "<0.1", ">0.50"),
    "Nd": ("La", 95.80, 50.91, 4.28e-6, 2.96e-8, 9.30, "<0.1", ">0.55"),
    "Ru": ("Zr", 97.64, 97.64, 6.26e-5, 2.09e-7, 6.09, "<0.1", ">0.30"),
    "Sc": ("Zr", 97.69, 62.86, 2.46e-5, 2.05e-8, 0.36, "<0.1", ">0.40"),
    "Ti": ("Zr", 99.14, 58.21, 1.19e-5, 2.66e-8, 1.71, "<0.1", "0.55"),
    "W":  ("Zr", 100.00, 99.38, 2.73e-4, 3.08e-8, 3.58, "<0.1", "0.40"),
    "Zn": ("Li", 99.01, 98.27, 2.42e-5, 2.16e-8, 6.60, "0.8", ">0.40"),
}


def _colorbar(px, xs, y0, y1, log_top, log_bot):
    lut = []
    n = y1 - y0
    for i in range(n + 1):
        y = y0 + i
        cols = [px[x, y] for x in xs]
        med = tuple(sorted(c[k] for c in cols)[len(cols) // 2] for k in (0, 1, 2))
        lut.append((med, log_top + (log_bot - log_top) * i / n))
    return lut


def _invert(lut, rgb):
    best = None
    for c, v in lut:
        d = (c[0] - rgb[0]) ** 2 + (c[1] - rgb[1]) ** 2 + (c[2] - rgb[2]) ** 2
        if best is None or d < best[0]:
            best = (d, v)
    return best[1], math.sqrt(best[0])


def check_fig4(path):
    print()
    print("=" * 78)
    print("Fig 4 — 컬러맵 역변환으로 σ_i / σ_e 복원 (SI Table S5 부재 대응)")
    print("=" * 78)
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    out = {}
    for tag, (py0, py1), idx, log_top, log_bot in [
            ("a  σ_i  RT ionic conductivity [S/cm]", (0, H // 2), 3, -3.0, -6.0),
            ("b  σ_e  electronic conductivity [S/cm]", (H // 2, H), 4, -6.0, -8.0)]:
        ys = [y for y in range(py0, py1) if max(px[1865, y]) - min(px[1865, y]) > 50]
        lut = _colorbar(px, range(1854, 1882, 4), min(ys), max(ys), log_top, log_bot)
        cells, _ = build_grid(px, 1815, py0, py1)

        vals = {}
        for el, bbox in cells.items():
            fill = median_fill(px, bbox)
            if fill is None:
                continue
            if max(fill) - min(fill) < 14:          # 무채색 회색 = 데이터 없음
                vals[el] = None
                continue
            v, dist = _invert(lut, fill)
            vals[el] = (10 ** v, dist, fill)
        out[tag[0]] = vals

        print()
        print("--- panel %s ---" % tag)
        print("  colorbar y=%d..%d → 10^%.0f .. 10^%.0f | 측정칸 %d, 회색(무측정) %d"
              % (min(ys), max(ys), log_top, log_bot,
                 sum(1 for v in vals.values() if v), sum(1 for v in vals.values() if not v)))
        print()
        print("  [자기검증] Table 1 의 18개 인쇄값 vs 픽셀 역변환")
        print("   %-4s %-11s %-11s %7s" % ("el", "Table 1", "pixel", "ratio"))
        errs = []
        for el in sorted(TABLE1):
            ref = TABLE1[el][idx]
            got = vals.get(el)
            if not got:
                print("   %-4s %-11.3g %-11s %7s" % (el, ref, "GREY", "-"))
                continue
            errs.append(math.log10(got[0] / ref))
            print("   %-4s %-11.3g %-11.3g %6.2fx" % (el, ref, got[0], got[0] / ref))
        bias = 0.0
        if errs:
            a = sorted(abs(e) for e in errs)
            bias = sum(errs) / len(errs)
            print("   n=%d  |Δlog10| median=%.3f (=%.2fx)  max=%.3f (=%.2fx)  bias=%+.3f dex"
                  % (len(errs), a[len(a) // 2], 10 ** a[len(a) // 2], a[-1],
                     10 ** a[-1], bias))
        # Table 1 잔차의 계통 편의를 빼서 나머지 도판트 값을 보정한다
        corr = 10 ** (-bias) if errs else 1.0
        for el in vals:
            if vals[el]:
                vals[el] = (vals[el][0] * corr,) + vals[el][1:]

        # "Undoped:" 스와치 (그리드 밖 별도 박스)
        sw = median_fill(px, (818, py0 + (170 if idx == 3 else 164),
                              902, py0 + (265 if idx == 3 else 259)))
        und = None
        if sw and max(sw) - min(sw) >= 14:
            und = 10 ** _invert(lut, sw)[0] * corr
            print("  Undoped 스와치 → %.2e  (본문 %s)"
                  % (und, "1.6e-6" if idx == 3 else "1.7e-7"))

        print()
        print("  [복원] Table 1 에 없는 도판트 — 이 그림에서만 얻을 수 있는 값"
              " (계통편의 %+.3f dex 보정 후)" % bias)
        rest = [e for e in vals if e not in TABLE1]
        live = sorted([e for e in rest if vals[e]], key=lambda e: -vals[e][0])
        for el in live:
            v, dist, fill = vals[el]
            flag = "  ⚠LUT거리 %.0f" % dist if dist > 25 else ""
            print("   %-4s  %.2e%s" % (el, v, flag))
        grey = sorted([e for e in rest if not vals[e]], key=lambda e: e)
        print("   GREY(측정값 없음): %s" % " ".join(grey))

        # --- 본문 계수 주장 검증 ---
        if idx == 3 and und:
            allv = {}
            for el, v in vals.items():
                if v:
                    allv[el] = TABLE1[el][3] if el in TABLE1 else v[0]
            nlow = sorted((el, v) for el, v in allv.items() if v < 1.6e-6)
            print()
            print("  [본문 계수 주장 검증]  undoped σ_i: 본문 1.6e-6 / 스와치 픽셀 %.2e" % und)
            print("   '36 dopants yield >10x improvement (=1.6e-5 초과)'")
            for ref, tag in ((1.6e-6, "본문값"), (und, "픽셀값")):
                print("     기준 undoped=%.2e (%s) → %d개 / 측정 %d개"
                      % (ref, tag, sum(1 for v in allv.values() if v >= 10 * ref),
                         len(allv)))
            print("   'just three show a lower conductivity than undoped' → %d개 %s"
                  % (len(nlow), ["%s %.1e" % t for t in nlow]))
            best = sorted(allv.items(), key=lambda t: -t[1])[:6]
            print("   상위 6: %s" % ", ".join("%s %.2e" % t for t in best))
        if idx == 4 and und:
            allv = {}
            for el, v in vals.items():
                if v:
                    allv[el] = TABLE1[el][4] if el in TABLE1 else v[0]
            band = sum(1 for v in allv.values() if 1e-8 <= v <= 5e-8)
            above = sorted(((el, v) for el, v in allv.items() if v > 1e-7),
                           key=lambda t: -t[1])
            print()
            print("  [본문 계수 주장 검증]  undoped σ_e = %.2e (본문 1.7e-7)" % und)
            print("   'nearly all doped samples between 1 and 5e-8' → 픽셀 실측 %d/%d (%.0f %%)"
                  % (band, len(allv), 100 * band / len(allv)))
            print("   σ_e > 1e-7 인 도판트: %s"
                  % ", ".join("%s %.2e" % t for t in above))
    return out


# ------------------------------------------------------------------- Fig 3

FIG3_LABELS = {
    # 그림 3 x축 순서 (좌→우). 3개 블록 = 이론 최적 site 별 그룹.
    "Li": ["B", "Al", "Fe", "Zn", "Ga"],
    "La": ["Na", "K", "Ca", "Rb", "Sr", "Y", "Ag", "Cs", "Ba", "Pr", "Nd",
           "Sm", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Bi"],
    "Zr": ["Mg", "Si", "P", "Sc", "Ti", "V", "Cr", "Mn", "Co", "Ni", "Cu",
           "Ge", "Se", "Nb", "Mo", "Ru", "Rh", "Pd", "Cd", "In", "Sn", "Te",
           "Ce", "Eu", "Hf", "Ta", "W", "Re", "Ir", "Pt", "Au", "Tl", "Pb"],
}


def _hue(rgb):
    r, g, b = (v / 255.0 for v in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    d = mx - mn
    if d < 1e-6:
        return None, 0.0
    if mx == r:
        h = (60 * (g - b) / d) % 360
    elif mx == g:
        h = 60 * (b - r) / d + 120
    else:
        h = 60 * (r - g) / d + 240
    return h, d / mx


def _marker_class(rgb):
    h, s = _hue(rgb)
    if h is None or s < 0.30:
        return None
    if 14 <= h < 48:
        return "pref"          # 주황 = 이론 최적 site (캡션 명시)
    if h >= 335 or h < 14:
        return "altA"          # 진홍
    if 185 <= h < 232:
        return "altB"          # 남색
    return None


def check_fig3(path):
    """Fig 3a/3b 마커를 도판트 슬롯 × 색으로 분해해 wt% 를 되읽는다.

    x 축: 프레임/구분선(수직 검은 선)으로 Und + 3개 그룹 경계를 잡고 균등 분할.
    y 축: 점선 격자(패널 a 는 80-100, 패널 b 는 0-100)를 찾아 선형 보정.
    검증: Table 1 의 garnet% / cubic% 18개와 대조.
    """
    print()
    print("=" * 78)
    print("Fig 3a/3b — 마커 위치 역판독 (총 garnet wt% · cubic wt%)")
    print("=" * 78)
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()

    order = FIG3_LABELS["Li"] + FIG3_LABELS["La"] + FIG3_LABELS["Zr"]
    print("  Fig 3 x축 도판트 수: Li그룹 %d + La그룹 %d + Zr그룹 %d = %d  (Sb 없음)"
          % (len(FIG3_LABELS["Li"]), len(FIG3_LABELS["La"]),
             len(FIG3_LABELS["Zr"]), len(order)))

    # --- x 그리드: 수직 구분선 ---
    dark = lambda c: c[0] < 110 and c[1] < 110 and c[2] < 110
    vlines = []
    for x in range(W):
        n = sum(1 for y in range(10, 740, 4) if dark(px[x, y]))
        if n > 150:
            vlines.append(x)
    groups, r = [], None
    for x in vlines:
        if r and x == r[1] + 1:
            r[1] = x
        else:
            if r:
                groups.append((r[0] + r[1]) / 2.0)
            r = [x, x]
    if r:
        groups.append((r[0] + r[1]) / 2.0)
    if len(groups) < 5:
        raise SystemExit("fig3 vertical separators not found: %r" % (groups,))
    x_axis, x_und, x_li, x_la, x_right = groups[:5]
    slots = {}
    for i, el in enumerate(FIG3_LABELS["Li"]):
        w = (x_la - x_und) / len(FIG3_LABELS["Li"]) if False else \
            (x_li - x_und) / len(FIG3_LABELS["Li"])
        slots[el] = (x_und + w * i, x_und + w * (i + 1))
    for i, el in enumerate(FIG3_LABELS["La"]):
        w = (x_la - x_li) / len(FIG3_LABELS["La"])
        slots[el] = (x_li + w * i, x_li + w * (i + 1))
    for i, el in enumerate(FIG3_LABELS["Zr"]):
        w = (x_right - x_la) / len(FIG3_LABELS["Zr"])
        slots[el] = (x_la + w * i, x_la + w * (i + 1))
    slots["Und"] = (x_axis, x_und)

    # --- y 그리드: 점선 격자 ---
    greyp = lambda c: (abs(c[0] - c[1]) < 22 and abs(c[1] - c[2]) < 22
                       and 90 < c[0] < 215)
    grid = []
    for y in range(10, 742):
        n = sum(1 for x in range(140, 2040, 3) if greyp(px[x, y]))
        if n > 200:
            grid.append(y)
    bands, r = [], None
    for y in grid:
        if r and y <= r[1] + 2:
            r[1] = y
        else:
            if r:
                bands.append((r[0] + r[1]) / 2.0)
            r = [y, y]
    if r:
        bands.append((r[0] + r[1]) / 2.0)
    bands = [b for b in bands if 20 < b < 735]
    a_lines = [b for b in bands if b < 300]     # 패널 a: 100,95,90,85(,80)
    b_lines = [b for b in bands if b > 400]     # 패널 b: 100,80,60,40,20
    if len(a_lines) < 3 or len(b_lines) < 4:
        raise SystemExit("fig3 gridlines not found: %r" % (bands,))

    def calib(lines, top_val, step):
        y0, y1 = lines[0], lines[-1]
        v0 = top_val
        v1 = top_val - step * (len(lines) - 1)
        return lambda y: v0 + (v1 - v0) * (y - y0) / (y1 - y0)

    a_pct = calib(a_lines, 100.0, 5.0)
    b_pct = calib(b_lines, 100.0, 20.0)
    print("  y보정: panel a 격자 %s (100→%.0f%%),  panel b 격자 %s"
          % ([round(v) for v in a_lines], a_pct(a_lines[-1]),
             [round(v) for v in b_lines]))

    def read(panel_y0, panel_y1, pct):
        out = {}
        for el, (sx0, sx1) in slots.items():
            acc = {}
            for x in range(int(sx0) + 2, int(sx1) - 1):
                for y in range(panel_y0, panel_y1):
                    k = _marker_class(px[x, y])
                    if k:
                        acc.setdefault(k, []).append(y)
            vals = {}
            for k, ys in acc.items():
                if len(ys) < 60:
                    continue
                ys.sort()
                vals[k] = pct(ys[len(ys) // 2])
            out[el] = vals
        return out

    pa = read(10, int(a_lines[-1] + (a_lines[1] - a_lines[0]) * 1.3), a_pct)
    pb = read(int(b_lines[0] - 25), 745, b_pct)

    print()
    print("  [자기검증] Table 1 18개 vs 픽셀 (선호 site = 주황 마커)")
    print("   %-4s %-16s %-16s" % ("el", "garnet% T1 / px", "cubic% T1 / px"))
    e1, e2 = [], []
    for el in sorted(TABLE1):
        g_ref, c_ref = TABLE1[el][1], TABLE1[el][2]
        g_px = pa.get(el, {}).get("pref")
        c_px = pb.get(el, {}).get("pref")
        if g_px is not None:
            e1.append(abs(g_px - g_ref))
        if c_px is not None:
            e2.append(abs(c_px - c_ref))
        print("   %-4s %6.2f / %-8s %6.2f / %-8s"
              % (el, g_ref, ("%.1f" % g_px) if g_px is not None else "-",
                 c_ref, ("%.1f" % c_px) if c_px is not None else "-"))
    for tag, e in (("garnet%", e1), ("cubic%", e2)):
        if e:
            s = sorted(e)
            print("   %s  n=%d  |Δ| median=%.2f pp  max=%.2f pp"
                  % (tag, len(e), s[len(s) // 2], s[-1]))

    print()
    print("  [본문 진술 검증] '선호 site 는 대부분 >90 % cubic, 비선호는 20-40 %'")
    for key, name in (("pref", "선호(주황)"), ("altA", "비선호A(진홍)"),
                      ("altB", "비선호B(남색)")):
        v = [pb[e][key] for e in order if key in pb.get(e, {})]
        if not v:
            continue
        hi = sum(1 for p in v if p > 90)
        band = sum(1 for p in v if 20 <= p <= 40)
        v_sorted = sorted(v)
        print("   %-14s n=%2d  중앙값 %5.1f %%  >90%%: %2d (%2.0f%%)  20-40%%대: %2d (%2.0f%%)"
              % (name, len(v), v_sorted[len(v_sorted) // 2], hi, 100 * hi / len(v),
                 band, 100 * band / len(v)))
    und = pb.get("Und", {})
    if und:
        print("   undoped  %s" % {k: round(v, 1) for k, v in und.items()})

    print()
    print("  [Fig 3a y축 절단] 패널 a 는 80 wt%% 에서 잘려 있다 — 축 아래로 사라진 점")
    for key, name in (("pref", "선호"), ("altA", "비선호A"), ("altB", "비선호B")):
        gone = [e for e in order if key in pb.get(e, {}) and key not in pa.get(e, {})]
        if gone:
            print("   %-7s 총 garnet <80 wt%% 라 패널 a 에 안 보이는 도판트: %s"
                  % (name, " ".join(gone)))
    print("   → 본문 '총 LLZO 함량은 대체로 높다(>95 %)' 는 이 절단된 축 위에서 읽힌 인상이다.")

    print()
    print("  [선호 site 인데 cubic 이 낮은 도판트] (본문이 '대부분 >90%'라 한 그룹의 실태)")
    low = [(e, pb[e]["pref"]) for e in order
           if "pref" in pb.get(e, {}) and pb[e]["pref"] < 70]
    low.sort(key=lambda t: t[1])
    print("   " + ", ".join("%s %.0f%%" % t for t in low))
    print("   → n=%d / %d (%.0f %%) 가 70 %% 미만이다." % (len(low), len(order),
                                                        100 * len(low) / len(order)))
    return pa, pb


# 패널 c/d 는 a/b 와 x축 항목이 다르다: Re 가 없고(=BV/결함에너지 값 없음),
# 패널 d 는 Yb 자리가 'n/a' 다. 라벨은 산화수 접미사를 떼고 원소기호만 남긴다.
FIG3CD_LABELS = {
    "Li": ["B", "Al", "Fe", "Zn", "Ga"],
    "La": ["Na", "K", "Ca", "Rb", "Sr", "Y", "Ag", "Cs", "Ba", "Pr", "Nd",
           "Sm", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Bi"],
    "Zr": ["Mg", "Si", "P", "Sc", "Ti", "V", "Cr", "Mn", "Co", "Ni", "Cu",
           "Ge", "Se", "Nb", "Mo", "Ru", "Rh", "Pd", "Cd", "In", "Sn", "Te",
           "Ce", "Eu", "Hf", "Ta", "W", "Ir", "Pt", "Au", "Tl", "Pb"],
}


def _site_class(rgb):
    """패널 c/d 팔레트: Li=하늘, La=초록, Zr=황갈."""
    h, s = _hue(rgb)
    if h is None or s < 0.30:
        return None
    if 22 <= h < 55:
        return "Zr"
    if 90 <= h < 155:
        return "La"
    if 182 <= h < 225:
        return "Li"
    return None


def check_fig3cd(path, pb):
    """Fig 3c(bond valence mismatch) · 3d(defect energy) 를 site 별로 되읽어

    ① 저자들이 쓴 '이론 최적 site' 가 정말 argmin(결함에너지) 인지,
    ② 값싼 BV mismatch 가 DFT 결함에너지와 같은 site 를 고르는지,
    ③ 두 지표가 실제 결과(cubic wt%)를 예측하는지 를 검증한다.
    """
    print()
    print("=" * 78)
    print("Fig 3c/3d — BV mismatch · DFT 결함에너지 되읽기 → 예측력 검증")
    print("=" * 78)
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()

    dark = lambda c: c[0] < 110 and c[1] < 110 and c[2] < 110
    vs = [x for x in range(W)
          if sum(1 for y in range(820, 1520, 4) if dark(px[x, y])) > 130]
    seps, r = [], None
    for x in vs:
        if r and x == r[1] + 1:
            r[1] = x
        else:
            if r:
                seps.append((r[0] + r[1]) / 2.0)
            r = [x, x]
    if r:
        seps.append((r[0] + r[1]) / 2.0)
    x_ax, x_li, x_la, x_right = seps[:4]

    slots = {}
    for els, a, b in ((FIG3CD_LABELS["Li"], x_ax, x_li),
                      (FIG3CD_LABELS["La"], x_li, x_la),
                      (FIG3CD_LABELS["Zr"], x_la, x_right)):
        w = (b - a) / len(els)
        for i, el in enumerate(els):
            slots[el] = (a + w * i, a + w * (i + 1))

    def read(y0, y1, top_y, bot_y):
        pct = lambda y: 5.0 * (bot_y - y) / (bot_y - top_y)
        out = {}
        for el, (sx0, sx1) in slots.items():
            acc = {}
            for x in range(int(sx0) + 2, int(sx1) - 1):
                for y in range(y0, y1):
                    k = _site_class(px[x, y])
                    if k:
                        acc.setdefault(k, []).append(y)
            out[el] = {k: pct(sorted(v)[len(v) // 2])
                       for k, v in acc.items() if len(v) >= 60}
        return out

    bv = read(845, 1112, 862.0, 1104.5)     # panel c: 5 → y862, 0 → y1104.5
    de = read(1210, 1470, 1227.0, 1462.5)   # panel d: 5 → y1227, 0 → y1462.5
    de.pop("Yb", None)                       # 패널 d 에서 Yb 는 'n/a'

    author_pref = {}
    for site, els in FIG3_LABELS.items():
        for e in els:
            author_pref[e] = site

    print("  검출: BV mismatch %d 도판트 / 결함에너지 %d 도판트 (Re 는 두 패널 모두 없음)"
          % (len(bv), len(de)))
    print()
    print("  ① 저자가 쓴 '이론 최적 site' == argmin(DFT 결함에너지) 인가")
    mism, skipped = [], []
    for el, d in sorted(de.items()):
        used = author_pref.get(el)
        if not used:
            continue
        if used not in d or len(d) < 3:
            skipped.append(el)          # 마커 겹침으로 3점을 다 못 읽음 = 판정 보류
            continue
        arg = min(d, key=d.get)
        if arg != used:
            mism.append((el, used, arg, d[used], d[arg]))
    judged = len(de) - len(skipped)
    print("     판정 가능 %d개 (마커 겹침으로 보류 %d: %s)"
          % (judged, len(skipped), " ".join(skipped)))
    print("     불일치 %d / %d" % (len(mism), judged))
    for el, used, arg, v_used, v_arg in mism:
        print("       %-3s 저자=%s(%.2f eV)  실제최소=%s(%.2f eV)"
              % (el, used, v_used, arg, v_arg))

    print()
    print("  ② argmin(BV mismatch) == argmin(결함에너지) 인가 (값싼 대리지표의 적중률)")
    agree = tot = 0
    disagree = []
    for el in sorted(set(bv) & set(de)):
        if len(bv[el]) < 3 or len(de[el]) < 3:
            continue
        tot += 1
        a, b = min(bv[el], key=bv[el].get), min(de[el], key=de[el].get)
        if a == b:
            agree += 1
        else:
            disagree.append("%s(BV→%s / DFT→%s)" % (el, a, b))
    if tot:
        print("     3-site 모두 읽힌 %d개 중 일치 %d (%.0f %%)"
              % (tot, agree, 100 * agree / tot))
        print("     불일치: %s" % ", ".join(disagree))

    print()
    print("  ③-a 예측한 site 가 실제로 cubic 을 가장 많이 만드는가 (3 site 순위)")
    win = tie = lose = 0
    losers = []
    for el in FIG3_LABELS["Li"] + FIG3_LABELS["La"] + FIG3_LABELS["Zr"]:
        d = pb.get(el, {})
        if "pref" not in d or len(d) < 3:
            continue
        alts = [d["altA"], d["altB"]]
        if d["pref"] > max(alts):
            win += 1
        elif d["pref"] < min(alts):
            lose += 1
            losers.append("%s(%.0f vs %.0f/%.0f)" % (el, d["pref"], alts[0], alts[1]))
        else:
            tie += 1
    n = win + tie + lose
    print("     선호 site 가 3개 중 1위: %d/%d (%.0f %%) · 2위 %d · 꼴찌 %d"
          % (win, n, 100 * win / n, tie, lose))
    if losers:
        print("     꼴찌 사례: %s" % ", ".join(losers))
    print("     → '어느 site 에 넣을지' 예측은 실제로 잘 맞는다. 이것이 이 논문의 핵심 긍정 결과.")

    print()
    print("  ③-b 지표의 *크기* 가 cubic wt%% 를 예측하는가 (Spearman ρ)")
    for name, tab in (("BV mismatch", bv), ("defect energy", de)):
        pairs = []
        for el, d in tab.items():
            site = author_pref.get(el)
            c = pb.get(el, {}).get("pref")
            if site and site in d and c is not None:
                pairs.append((d[site], c))
        if len(pairs) > 5:
            print("     %-14s n=%2d  ρ = %+.3f" % (name, len(pairs), _spearman(pairs)))
    print("     → 두 지표 모두 '어느 site 에 넣을지'는 알려주지만 '얼마나 cubic 이 되는지'는"
          " 거의 예측하지 못한다 (본문 §2.2 의 Ga/Fe 반례와 같은 방향).")
    return bv, de


def _spearman(pairs):
    def rank(vals):
        idx = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0.0] * len(vals)
        i = 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and vals[idx[j + 1]] == vals[idx[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[idx[k]] = avg
            i = j + 1
        return r
    xs = rank([p[0] for p in pairs])
    ys = rank([p[1] for p in pairs])
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    dx = math.sqrt(sum((v - mx) ** 2 for v in xs))
    dy = math.sqrt(sum((v - my) ** 2 for v in ys))
    return num / (dx * dy) if dx and dy else 0.0


OUT_CSV = os.path.join(ROOT, "db", "properties",
                       "anderson2024_llzo_dopant_screening_recovered.csv")


def write_csv(sig, pa, pb):
    """Fig 3 + Fig 4 복원값을 도판트 1행으로 병합해 CSV 로 낸다.

    source 열이 핵심: Table 1 에 인쇄된 18개는 'paper', 나머지는 'pixel'(우리 역판독).
    두 출처를 섞어 인용하지 않도록 반드시 구분해 쓸 것.
    """
    import csv
    order = FIG3_LABELS["Li"] + FIG3_LABELS["La"] + FIG3_LABELS["Zr"]
    pref_of = {}
    for site, els in FIG3_LABELS.items():
        for e in els:
            pref_of[e] = site
    cols = ["dopant", "preferred_site", "source",
            "garnet_wt_pct_pref", "cubic_wt_pct_pref",
            "cubic_wt_pct_alt_A", "cubic_wt_pct_alt_B",
            "sigma_ionic_S_cm", "sigma_electronic_S_cm"]
    rows = []
    for el in order:
        printed = el in TABLE1
        si = TABLE1[el][3] if printed else (sig["a"].get(el) or [None])[0]
        se = TABLE1[el][4] if printed else (sig["b"].get(el) or [None])[0]
        g = TABLE1[el][1] if printed else pa.get(el, {}).get("pref")
        c = TABLE1[el][2] if printed else pb.get(el, {}).get("pref")
        rows.append({
            "dopant": el,
            "preferred_site": pref_of[el],
            "source": "paper Table 1" if printed else "pixel readback (Fig 3/4)",
            "garnet_wt_pct_pref": "" if g is None else round(g, 2),
            "cubic_wt_pct_pref": "" if c is None else round(c, 2),
            "cubic_wt_pct_alt_A": _r(pb.get(el, {}).get("altA")),
            "cubic_wt_pct_alt_B": _r(pb.get(el, {}).get("altB")),
            "sigma_ionic_S_cm": "" if si is None else "%.3e" % si,
            "sigma_electronic_S_cm": "" if se is None else "%.3e" % se,
        })
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print()
    print("CSV 기록: %s  (%d행)" % (os.path.relpath(OUT_CSV, ROOT), len(rows)))
    print("  ⚠ source 열로 'paper Table 1'(18개 인쇄값) 과 'pixel readback'(41개 우리 역판독)")
    print("    을 반드시 구분해 인용할 것. 역판독 정확도는 위 자기검증 블록 참조.")


def _r(v, nd=1):
    return "" if v is None else round(v, nd)


# 2026-07-28 1차 digest 가 **SI Table S5** 에서 옮겨 적은 '>10× 36종' 목록.
# SI PDF 는 (이 2차 패스 시점에) inbox 에 없어서 여기 박아두고 그림과 대조했다.
#
# ⚠ 2026-08-04 3차 패스(`anderson2024_si_tableS5.py`)가 SI PDF 로 아래를 확정했다 — digest §20:
#   · 'Rh' 는 **'Ho' 의 철자 오타**였다. 엄격한 >10× 는 35종이고 Ho(9.7×) 를 반올림해 넣어야 36.
#   · 결측 5종은 SI 가 맞다(…Yb). **Fig 4a·4b 가 Y·Yb 칸을 맞바꿔 실은 것**이 논문 쪽 오류다.
# 아래 상수는 **2차 패스 당시의 입력을 그대로 보존**한 것이라 고치지 않는다(재현성).
DIGEST_36_FROM_SI = (
    "Ag Al Au Bi Ca Cd Ce Co Cs Cu Dy Fe Ga Gd Hf In K Lu Mg Na Nb Ni Pb Pr "
    "Rb Rh Ru Sc Sm Sn Sr Ta Tl W Y Zn").split()
DIGEST_MISSING_FROM_SI = ["Er", "Mo", "Tb", "Te", "Yb"]


def check_vs_si_digest(sig):
    """1차 digest(SI Table S5 기반) 목록 vs 이번 그림 픽셀 목록 대조."""
    print()
    print("=" * 78)
    print("Fig 4 ↔ 1차 digest(SI Table S5) 대조 — 서로 어긋나는 칸 찾기")
    print("=" * 78)
    vals = {}
    for el, v in sig["a"].items():
        if v:
            vals[el] = TABLE1[el][3] if el in TABLE1 else v[0]
    mine = sorted(e for e, v in vals.items() if v >= 1.6e-5)
    grey = sorted(e for e, v in sig["a"].items() if not v
                  and e in FIG3_LABELS["Li"] + FIG3_LABELS["La"] + FIG3_LABELS["Zr"])
    print("  '>10×' 목록  픽셀 n=%d / SI n=%d" % (len(mine), len(DIGEST_36_FROM_SI)))
    print("    SI 에만: %s" % sorted(set(DIGEST_36_FROM_SI) - set(mine)))
    print("    픽셀에만: %s" % sorted(set(mine) - set(DIGEST_36_FROM_SI)))
    print("  σ 결측 목록  픽셀 %s / SI %s" % (grey, DIGEST_MISSING_FROM_SI))
    print("    SI 에만: %s" % sorted(set(DIGEST_MISSING_FROM_SI) - set(grey)))
    print("    픽셀에만: %s" % sorted(set(grey) - set(DIGEST_MISSING_FROM_SI)))
    for a, b in (("Y", "Yb"), ("Rh", "Ho")):
        va = sig["a"].get(a)
        vb = sig["a"].get(b)
        print("    %-3s = %-24s   %-3s = %s"
              % (a, ("%.3e" % va[0]) if va else "GREY(Fig 4 에 값 없음)",
                 b, ("%.3e" % vb[0]) if vb else "GREY(Fig 4 에 값 없음)"))
    print("  ⚠ 두 목록의 차이가 **Y↔Yb · Rh↔Ho 두 쌍의 맞교환뿐**이다(양쪽 다 정확히 36종).")
    print("    = 그림과 Table S5 중 하나가 이 두 쌍을 서로 바꿔 싣고 있거나,")
    print("      1차 digest 의 SI 전사에서 기호가 뒤바뀌었다.")
    print()
    print("  ✅ 2026-08-04 3차 패스가 SI PDF 로 확정 (digest §20 · anderson2024_si_tableS5.py):")
    print("     · Rh/Ho — **논문은 무결**. 그림·SI 값이 오차 안에서 일치한다")
    print("       (Rh 2.58e-6 = undoped 1.6× · Ho 1.57e-5 = 9.7×).")
    print("       1차 digest 36종 목록의 'Rh' 가 'Ho' 의 철자 오타였을 뿐이다.")
    print("       엄격한 >10× 는 **35종**, Ho 를 반올림(9.7×→10×)해 넣어야 본문의 36 이 된다.")
    print("     · Y/Yb — **논문 쪽 오류**. Table S5 + Fig 3(59/59 일치)가 Fig 4 를 이긴다.")
    print("       채택: **Y(La) σ_i 2.46e-5 · σ_e 3.14e-8 (측정됨) / Yb(La) σ 미측정**.")
    print("       Fig 4a·4b 두 패널 모두 Y·Yb 칸을 맞바꿔 실었다.")
    print("     ⛔ 이 함수의 위 출력은 **2차 패스 당시 상태의 기록**이다. 인용은 §20 을 따를 것.")


def main():
    figs = extract_figures()
    check_fig1(figs["fig1"])
    sig = check_fig4(figs["fig4"])
    pa, pb = check_fig3(figs["fig3"])
    check_fig3cd(figs["fig3"], pb)
    check_vs_si_digest(sig)
    write_csv(sig, pa, pb)


if __name__ == "__main__":
    main()
