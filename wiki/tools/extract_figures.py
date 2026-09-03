#!/usr/bin/env python3
"""extract_figures.py — 논문 PDF 에서 **그림/표를 캡션 기준으로 잘라** 위키 raw 층에 등록.

(이식: `claude/friendly-meitner-lldvar` 브랜치의 `tools/litdb/extract_figures.py`
 e80dd480 판을 이 브랜치의 wiki 구조에 맞춰 경로만 바꾼 것. 캡션 앵커·기하
 검증·OCR 관용 로직은 그대로다 — 재구현하지 않는다.)

1저자 요청(2026-08-06): "논문 에이전트도 figure 크로핑해서 저장해두면 보기 좋지 않나."
digest(`wiki/raw/papers/<slug>.md`) 본문에 `Fig. 5e` 같은 언급이 나오면 webapp 이 그 그림을
오른쪽 여백에 띄운다 — 그 그림들을 만드는 도구다.

왜 "임베디드 이미지 추출"이 아니라 **캡션 앵커 + 영역 렌더**인가
  ACS/RSC/Elsevier 논문의 상당수가 그림을 **벡터**로 넣는다. `page.get_images()` 는
  이 경우 아무것도(또는 조각난 래스터만) 돌려준다. 반대로 캡션은 어떤 저널이든 텍스트라
  안정적으로 잡힌다 → 캡션 위(그림) / 아래(표) 영역을 통째로 **렌더**하면 벡터·래스터·
  혼합 어느 쪽이든 똑같이 나온다.

오탐 방지 (이게 핵심)
  본문에도 "Figure 2a shows a representative..." 처럼 Figure 로 시작하는 문단이 많다.
  실측(Kraft 2017 p4)에서 캡션 4개 중 2개가 이런 본문 문단이었다. 두 겹으로 막는다:
    ① 구두점 규칙 — 번호 뒤가 `.`/`|`/`:` 이거나 대문자로 시작해야 캡션
       ("Figure 3 shows" 는 소문자 동사라 탈락, "Figure 2a" 는 번호에 소문자가 붙어 탈락)
    ② **기하 검증** — 잘라낼 영역에 실제 그래픽(배치 이미지 or 벡터 경로)이 있어야 한다.
       본문 문단 위에는 본문 문단밖에 없으므로 여기서 확실히 걸린다.

usage — 보통은 이 두 줄이면 끝난다 (inbox 를 훑어 digest 와 자동으로 짝지어 준다)
  python3 wiki/tools/extract_figures.py --inbox           # 어느 PDF ↔ 어느 논문인지 표만
  python3 wiki/tools/extract_figures.py --inbox --run     # 실제로 자르기

한 편만 콕 집을 때 (⚠ <slug> 는 자리표시자다 — wiki/raw/papers/ 의 실제 파일 이름을 넣는다)
  python3 wiki/tools/extract_figures.py --slug kraft2017_lattice_polarizability_argyrodite_Li6PS5X \\
      --pdf "wiki/inbox/31. ….pdf" --pdf "wiki/inbox/31. Sup) ….pdf" --clean

출력
  wiki/raw/figures/<slug>/fig_<label>.png ...
  wiki/raw/figures/<slug>/figures.json     ← webapp 이 읽는 색인
"""
import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
from pathlib import Path

try:
    import fitz                                # PyMuPDF
except ImportError:                            # ⚠ Ubuntu 24.04+ 는 PEP 668 로 시스템 pip 이 막힌다
    sys.exit(
        "⛔ PyMuPDF 가 없다. Ubuntu 24.04(WSL)는 시스템 pip 이 막혀 있어(PEP 668) venv 를 쓴다:\n"
        "     python3 -m venv ~/.venvs/litdb\n"
        "     ~/.venvs/litdb/bin/pip install -q pymupdf pillow\n"
        "   그 다음부터는 python3 대신 이걸로 실행:\n"
        "     ~/.venvs/litdb/bin/python3 wiki/tools/extract_figures.py --inbox\n"
        "   (자주 쓸 거면 ~/.bashrc 에)  alias litfig='~/.venvs/litdb/bin/python3 "
        "~/Yonghoon-DEM-DFT/wiki/tools/extract_figures.py'")

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "wiki" / "raw" / "figures"

# ① 캡션 후보. 번호 뒤에 소문자가 바로 붙으면(2a) 본문 참조이므로 (?![a-z]) 로 막는다.
#   ⚠ "Supplementary Fig. 1." 처럼 접두어가 붙는 저널이 있다(실측: Zhou 2026 SI 는 이것 때문에
#     27쪽에서 0개가 나왔다). 접두어가 붙으면 번호에 S 가 없어도 SI 번호로 취급한다.
#   ⚠ 옛 스캔 저널의 OCR 은 글자를 숫자로 읽는다 — 실측(Thornton & Ning 1998, Powder Tech.):
#     "Fig. 3." → **"F19. 3."** (i→1, g→9, o→0, s→5, l→1). 캡션은 멀쩡한데 키워드만 깨져
#     9쪽짜리 논문에서 캡션 인정 0건이었다. 키워드 철자만 관대하게 받는다 (번호는 진짜 숫자).
SI_PRE = r"(?:Supplementary|Supplemental|Supporting|Extended\s+Data|Extended|Online)\s+"
CAP_RE = re.compile(
    r"^\s*(?P<si>" + SI_PRE + r")?"
    r"(?P<kind>F[i1l][gq9](?:ure|s)?\.?|Tab[l1]e|Sche[mn]e)\s*"
    r"(?P<label>S?\d+)(?![a-z0-9])\s*(?P<sep>[.|:,–—]|\s)\s*(?P<rest>.*)",
    re.S | re.I)
# 본문 문단이 흔히 쓰는 동사 — 구두점이 없을 때 최종 판별
VERBS = re.compile(
    r"^(shows?|displays?|presents?|illustrates?|summari[sz]es?|gives?|depicts?|compares?|"
    r"plots?|reports?|indicates?|reveals?|lists?|contains?|provides?|demonstrates?|"
    r"and|in|of|for|to|is|are|was|were|we|it|this|which|shown|show|see|from|the)\b", re.I)


def is_caption(text):
    """캡션이면 (kind, label, si) 아니면 None. si=True 면 SI 번호(S를 붙인다)."""
    t = " ".join(text.split())
    m = CAP_RE.match(t)
    if not m:
        return None
    kw = m.group("kind").lower()
    kind = "table" if kw.startswith("tab") else \
           ("scheme" if kw.startswith("sch") else "figure")
    rest, sep = m.group("rest"), m.group("sep")
    if sep in ".|:,–—":              # "Figure 1." / "Figure 5 |" → 캡션 확정
        pass
    elif rest[:1].islower() or VERBS.match(rest):
        return None                            # "Figure 3 shows ..." → 본문
    if len(t) < 12:                            # "Figure 1" 만 있는 상호참조 조각
        return None
    return kind, m.group("label"), bool(m.group("si"))


def caption_rotation(page, cap_bbox):
    """캡션 줄의 **쓰기 방향**으로 회전을 판정. 0 이면 정상, 90 이면 옆으로 누운 표.

    왜 (2026-08-19, de Klerk 2016 SI 에서 잡음): Wiley/ACS SI 는 넓은 표를
    `sidewaystable` 로 **90° 눕혀** 싣는 일이 잦다. 그러면 캡션 줄의 dir 이
    (0,−1) 이 되고 bbox 가 **세로로 긴 띠**가 된다(실측 x 113–125 · y 72–720).
    "캡션 아래가 표" 라는 기하 논리가 통째로 깨져서 표가 **한 장도 안 잘린다**
    (de Klerk Tables S1–S3 가 정확히 그렇게 누락돼 있었다).
    """
    x0, y0, x1, y1 = cap_bbox
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            bx0, by0, bx1, by1 = l["bbox"]
            if bx1 < x0 - 2 or bx0 > x1 + 2 or by1 < y0 - 2 or by0 > y1 + 2:
                continue
            d = l.get("dir", (1, 0))
            if abs(d[0]) < 0.5 and abs(d[1]) > 0.5:
                return 90
    return 0


def text_blocks(page):
    return [b for b in page.get_text("blocks") if b[6] == 0 and b[4].strip()]


def merge_caption(blocks, cap, gap=14.0):
    """캡션이 여러 블록으로 쪼개진 경우 아래로 이어붙인다 → (합친 bbox, 합친 글).

    ⚠ 왜 (2026-08-06 실측, Zhou 2026 SI): 캡션이 그림 **위**에 오는 SI 에서 캡션 본문이
      2~3 블록으로 쪼개져 있었다. 첫 블록만 캡션으로 보면 "그 아래 영역"이 두 번째 캡션
      줄까지밖에 안 돼(높이 3 pt) 그림을 통째로 놓친다.
    """
    order = sorted(blocks, key=lambda b: (b[1], b[0]))
    try:
        i = order.index(cap)
    except ValueError:
        return fitz.Rect(cap[:4]), " ".join(cap[4].split())
    r = fitz.Rect(cap[:4])
    txt = [cap[4]]
    for b in order[i + 1:]:
        if b[1] - r.y1 > gap or b[1] < r.y0:
            break
        if band_overlap((r.x0, r.x1), (b[0], b[2])) < 0.5:
            break
        if is_caption(b[4]):                   # 다음 그림 캡션이면 멈춘다
            break
        r |= fitz.Rect(b[:4])
        txt.append(b[4])
    return r, " ".join(" ".join(txt).split())


_GCACHE = {}


def graphics(page):
    """이 쪽의 그래픽 bbox 들 — 배치 이미지 + 벡터 경로. (쪽당 1회만: get_drawings 가 느리다)

    ⚠ 캐시 키에 **id(page.parent) 를 쓰면 안 된다** (2026-08-06, 53편 배치에서 발각):
      문서를 닫고 다음 걸 열면 CPython 이 같은 주소를 재사용해서 키가 충돌한다
      (실측 2편 6회 반복 → 27건 충돌). 그러면 뒤 논문의 쪽이 **앞 논문의 그래픽**을
      물려받아 기하 검증이 엉뚱하게 통과/탈락한다.
      증상: 한 편만 돌리면 4장인데 배치로 돌리면 1장(huang2022), sendek2017 fig_2·3 소실.
      파일 경로로 키를 잡고, 문서마다 캐시를 비운다.
    """
    ck = (page.parent.name, page.number)
    if ck in _GCACHE:
        return _GCACHE[ck]
    out = []
    for it in page.get_image_info():
        out.append(("img", fitz.Rect(it["bbox"])))
    for d in page.get_drawings():
        r = fitz.Rect(d["rect"])
        if r.width > 1.5 and r.height > 1.5:   # 밑줄·괘선 같은 1픽셀 요소 제외
            out.append(("draw", r))
    _GCACHE[ck] = out
    return out


def band_overlap(a, b):
    """가로 구간 겹침 비율 (좁은 쪽 기준)."""
    lo, hi = max(a[0], b[0]), min(a[1], b[1])
    w = min(a[1] - a[0], b[1] - b[0])
    return max(0.0, hi - lo) / w if w > 0 else 0.0


def table_rect(page, cap, tables, stop_y=1e9, margin=5.0):
    """표는 **본문과 같은 텍스트**라 '그래픽 검증'이 안 통한다 → PyMuPDF 표 검출을 쓴다.

    ⚠ 캡션 블록이 표 앞부분을 통째로 삼키는 쪽이 있다(실측: Hargreaves SI p21 에서
      캡션 bbox 가 첫 표를 덮었다). 그래서 "캡션 **아래**"가 아니라 "캡션 시작선 이후"에
      걸리는 표를 전부 합집합한다 — 한 캡션이 이어진 두 조각을 거느리는 경우까지 잡힌다.
      단 stop_y(= 같은 쪽의 다음 캡션 y0)에서 끊는다 — 안 그러면 Table S6 크롭에 S7 까지
      딸려 들어간다(실측: Kraft 2017 SI p8).
    """
    x0, y0, x1, y1 = cap[:4]
    hit = [fitz.Rect(t) for t in tables]
    hit = [t for t in hit if t.y1 > y0 + 2 and band_overlap((x0, x1), (t.x0, t.x1)) > 0.30
           and t.y0 < stop_y]                   # ⚠ 다음 캡션 앞에서 끊는다
    if not hit:
        return None
    u = fitz.Rect(hit[0])
    for t in hit[1:]:
        u |= t
    u |= fitz.Rect(x0, y0, x1, y1)              # 표는 캡션까지 넣어야 스스로 설명된다
    return (fitz.Rect(u.x0 - margin, u.y0 - margin,
                      u.x1 + margin, u.y1 + margin) & page.rect)


def is_prose(b, pr=None):
    """이 블록이 **경계로 쓸 수 있는가** (본문 문단 · 다른 캡션 · 머리글/꼬리글).

    ⚠ 왜 (2026-08-06 실측, son2025·rao2011): 그림 **안**의 축 라벨·범례·눈금도 텍스트
      블록으로 추출된다. 그걸 경계로 삼으면 캡션 바로 위 2~11 pt 만 남아 그림이 통째로
      버려진다("영역 없음"). son2025 는 본문 5장 전부, rao2011 은 Fig 1 이 이렇게 날아갔다.
        son2025 p3: 캡션 (40,532,…) 바로 위 = "Energy (eV)" (162,517,197,526) → 높이 2 pt
        rao2011 p2: 캡션 (306,726,…) 바로 위 = "20 40 60 80 100 -2000" → 높이 11 pt
      산문은 낱말이 많다 — 축 라벨·범례는 짧다. 다른 그림의 캡션은 낱말 수와 무관하게
      진짜 경계이므로 그대로 인정한다.
    """
    t = " ".join((b[4] or "").split())
    if bool(is_caption(t)) or (len(t.split()) >= 8 and len(t) >= 45):
        return True
    # 학술지 머리글("Journal of the American Chemical Society")·쪽번호는 짧지만 진짜 경계다.
    #   안 넣으면 크롭 맨 위에 러닝헤드가 딸려 들어온다 (2026-08-06 kraft2017 실측).
    if pr is not None:
        z = 0.09 * pr.height
        if b[3] <= pr.y0 + z or b[1] >= pr.y1 - z:
            return True
    return False


def _side_rect(page, cap, blocks, up, margin=6.0):
    """캡션 기준 위(up=True)/아래 영역 → (rect, 이미지수, 벡터수).

    세로 경계는 "같은 단(column)에서 가장 가까운 **본문 문단**" — 위에 다른 그림의
    캡션이 있으면 거기서 끊긴다. 그다음 그래픽 + 그림 안 텍스트로 실제 범위를 잡는다.
    """
    x0, y0, x1, y1 = cap[:4]
    band, pr = (x0, x1), page.rect
    if up:
        lim = pr.y0 + 24
        for b in blocks:
            if b[3] <= y0 + 1 and band_overlap(band, (b[0], b[2])) > 0.45 and is_prose(b, pr):
                lim = max(lim, b[3])
        rect = fitz.Rect(x0, lim + 2, x1, y0 - 2)
    else:
        lim = pr.y1 - 24
        for b in blocks:
            if b[1] >= y1 - 1 and band_overlap(band, (b[0], b[2])) > 0.45 and is_prose(b, pr):
                lim = min(lim, b[1])
        rect = fitz.Rect(x0, y1 + 2, x1, lim - 2)
    if rect.height < 36:
        return None, 0, 0
    # ⚠ 분모를 그래픽 넓이로만 잡으면 **스캔본**에서 무너진다 (2026-08-06 실측, Thornton 1998):
    #   스캔 PDF 는 쪽 전체가 이미지 1장이라, 그림 영역이 아무리 맞아도 "쪽 넓이의 12%"를
    #   못 넘으면 '그래픽 없음' 으로 버려진다 — 10장 중 7장이 그렇게 날아갔다.
    #   둘 중 **작은 쪽** 기준으로 본다: 큰 그래픽이 영역을 덮는 경우도 통과한다.
    hit = [(k, r) for k, r in graphics(page) if r.intersects(rect) and
           (r & rect).get_area() > 0.12 * min(r.get_area(), rect.get_area())]
    if hit:
        u = hit[0][1]
        for _k, r in hit[1:]:
            u |= r
        # 그림 안의 짧은 텍스트(축 라벨·범례)도 그림의 일부다 — 안 넣으면 잘려 나간다
        for b in blocks:
            if is_prose(b, pr):
                continue
            br = fitz.Rect(b[:4])
            if br.intersects(rect) and (br & rect).get_area() > 0.5 * max(br.get_area(), 1e-6):
                u |= br
        # 그래픽(+그림 안 라벨)에 **딱 맞춘다**. 예전엔 min/max 로 느슨한 후보 사각형과
        # 합쳤는데, 그러면 그림 위 빈 칸이 통째로 딸려 와 크롭이 반쯤 백지가 된다
        # (2026-08-06 kraft2017 fig_S1 실측: 위쪽 절반이 여백).
        y_lo = max(u.y0 - margin, (lim + 2) if up else (y1 + 2))
        y_hi = min(u.y1 + margin, (y0 - 2) if up else (lim - 2))
        rect = fitz.Rect(min(rect.x0, u.x0) - margin, y_lo,
                         max(rect.x1, u.x1) + margin, y_hi) & pr
    ks = [k for k, _r in hit]
    return (rect if rect.height >= 36 else None), ks.count("img"), ks.count("draw")


def _fname_prefix(kind):
    """kind → 파일이름 접두사. **scheme 은 fig 와 갈라야 한다.**

    🐛 2026-08-29 (han2025 실측): `Scheme 1` 과 `Figure 1` 이 둘 다 `fig_1.png` 로 저장돼
    **먼저 쓴 Scheme 1 이 통째로 사라졌다.** figures.json 에는 `s1`·`f1` 두 행이 남아 있어
    "7장 추출" 로 보이는데 실제 PNG 는 6장이고, webapp `_fig_keys()` 는 파일이름을 키로 쓰므로
    한쪽 주석이 통째로 다른 그림에 붙는다. dedupe 는 `key` 로 묶어서 이걸 못 잡는다.
    ⚠ 이미 만들어 둔 폴더는 소급되지 않는다 — `--clean` 으로 다시 돌려야 고쳐진다.
    """
    return {"table": "tab", "scheme": "sch"}.get(kind, "fig")


def region_for(page, cap, kind, blocks, tables=(), min_draw=6, stop_y=1e9):
    """캡션 블록 → (잘라낼 사각형, 이미지수, 벡터수).

    figure/scheme 는 캡션 **위**가 기본. ⚠ SI 는 캡션을 그림 **위**에 두는 쪽이 많다
    (실측: Zhou 2026 SI 의 Fig S1/S2/S12 는 캡션이 쪽 맨 위 y=76 이고 그림이 그 아래).
    위가 비면 아래로 한 번 더 본다 — 표는 처음부터 아래.
    """
    if kind == "table" and caption_rotation(page, cap) == 90:
        # 누운 표는 쪽 전체를 잡는다. 표가 쪽을 거의 다 채우므로 잘라내다 잘릴 위험이
        # 옆띠를 계산하는 것보다 크다. 방향은 렌더 뒤 PIL 로 세운다.
        pr = page.rect
        return (fitz.Rect(pr.x0 + 6, pr.y0 + 6, pr.x1 - 6, pr.y1 - 6), 1, 0)
    if kind == "table":
        r = table_rect(page, cap, tables, stop_y)
        if r is not None and r.height >= 36:
            return r, 1, 0
        return _side_rect(page, cap, blocks, up=False)

    r, ni, nd = _side_rect(page, cap, blocks, up=True)
    if r is not None and (ni or nd >= min_draw):
        return r, ni, nd
    r2, ni2, nd2 = _side_rect(page, cap, blocks, up=False)
    if r2 is not None and (ni2 or nd2 >= min_draw):
        return r2, ni2, nd2
    return (r, ni, nd) if r is not None else (r2, ni2, nd2)


def _upright(path, deg):
    """누운 표 PNG 를 세운다. PIL 없으면 **조용히 넘어가지 않고** 알린다."""
    try:
        from PIL import Image
    except Exception:
        print(f"    ⚠ PIL 없음 — {Path(path).name} 이 {deg}° 누운 채 저장됐다")
        return
    im = Image.open(path)
    im.rotate(-deg, expand=True).save(path, "PNG", optimize=True)


def _shrink(path):
    """PNG 재압축 — 선화(line art)는 팔레트로 줄이면 60~80% 작아진다. PIL 없으면 그냥 둔다."""
    try:
        from PIL import Image
    except Exception:
        return
    try:
        im = Image.open(path).convert("RGB")
        # ⛔⛔ 2026-08-25 (codex D 리뷰) — 여기가 **정확히 반대로** 동작했다.
        #   `getcolors(maxcolors=4096)` 은 4096 색을 넘으면 **None** 을 돌려준다.
        #   `or []` 가 그걸 빈 목록으로 바꿔 len=0 → `0 > 3500` 거짓 → else 로 가서
        #   **256 색으로 양자화**했다. 즉 **색이 가장 풍부한 이미지가 가장 심하게 뭉개졌다.**
        #   스캔 자료집의 글자·미세 범례·열지도 판독을 해친다. talks 뿐 아니라
        #   **모든 그림 추출**에 걸려 있었다. None = "너무 많다" 로 읽는다.
        cols = im.getcolors(maxcolors=4096)
        if cols is None or len(cols) > 3500:
            im.save(path, "PNG", optimize=True)
        else:
            q.save(path, "PNG", optimize=True)
    except Exception:
        pass


def blank_ratio(pix):
    """거의 흰 픽셀 비율 — 빈 영역(=오탐) 걸러내기."""
    s = pix.samples
    n = pix.width * pix.height
    if n == 0:
        return 1.0
    stride, white = pix.n, 0
    step = max(1, n // 20000)                  # 성능: 최대 2만 점만 표본
    cnt = 0
    for i in range(0, n, step):
        j = i * stride
        if s[j] > 244 and s[j + 1] > 244 and s[j + 2] > 244:
            white += 1
        cnt += 1
    return white / max(cnt, 1)


def extract(pdf_paths, slug, dpi=200, dry=False, min_draw=6, keep_blank=0.985,
            maxpx=1500, relto=None):
    out_dir = OUT_ROOT / slug
    found, seen, skipped = [], {}, []
    for pdf_path in pdf_paths:
        _GCACHE.clear()                        # 문서마다 비운다 (위 주석 참고)
        doc = fitz.open(pdf_path)
        # ⚠ 여기 예전에 `\bsup|\bsi\b|…` 라는 **별도 정규식**이 있었다 (2026-08-06 실측 사고):
        #   `\bsup` 이 "**Sup**erionic"·"**sup**erconductor" 를 잡아, 제목에 그 낱말이 든
        #   논문 11편의 **본문 그림이 통째로 S 번호**로 붙었다(kraft2017 본문 8장 → SI 8장).
        #   SI_TAG 하나만 쓴다 — 매칭 쪽과 판정이 갈리면 이런 사고가 또 난다.
        si = bool(SI_TAG.search(Path(pdf_path).stem))
        for pno in range(doc.page_count):
            page = doc[pno]
            blocks = text_blocks(page)
            caps = [(b, is_caption(b[4])) for b in blocks]
            tabs = ()
            if any(h and h[0] == "table" for _b, h in caps):
                # 표가 있는 쪽에서만 (검출이 느리다). 괘선 없는 표는 lines 전략이 못 잡아서
                # text 전략으로 한 번 더 본다 (실측: SI 의 정렬-텍스트 표들이 전부 여기서 나왔다).
                for strat in ("lines", "text"):
                    try:
                        tabs = [t.bbox for t in page.find_tables(strategy=strat).tables]
                    except Exception:
                        tabs = ()
                    if tabs:
                        break
            for cap, hit in caps:
                if not hit:
                    continue
                kind, label, cap_si = hit
                if (si or cap_si) and not label.upper().startswith("S"):
                    label = "S" + label        # SI 의 "Figure 3" 은 곧 Fig S3
                key = f"{kind[0]}{label.upper()}"
                cr, caption = merge_caption(blocks, cap)
                # 같은 쪽에서 이 캡션 다음에 오는 캡션의 시작선 — 표 크롭의 아래 한계
                stop_y = min([b[1] for b, h in caps
                              if h and b[1] > cr.y1 + 1
                              and band_overlap((cr.x0, cr.x1), (b[0], b[2])) > 0.30] or [1e9])
                rect, n_img, n_draw = region_for(page, tuple(cr), kind, blocks, tabs,
                                                 min_draw=min_draw, stop_y=stop_y)
                if rect is None:
                    skipped.append((key, pno + 1, "영역 없음"))
                    continue
                # ② 기하 검증 — 그래픽이 없으면 본문 문단 오탐
                if kind != "table" and n_img == 0 and n_draw < min_draw:
                    skipped.append((key, pno + 1, f"그래픽 없음(img{n_img}/draw{n_draw})"))
                    continue
                # 긴 변이 maxpx 를 넘지 않도록 이 그림만 dpi 를 낮춘다.
                #   ⚠ repo 에 커밋하는 파일이라 크기가 중요하다: 200 dpi 고정이면 논문 1편에
                #     11 MB 까지 갔다(Zhou 2026, 25장). 화면 판독에는 긴 변 1500 px 면 충분.
                d_eff = dpi
                if maxpx:
                    long_pt = max(rect.width, rect.height)
                    if long_pt > 0:
                        d_eff = min(dpi, max(72, int(maxpx * 72.0 / long_pt)))
                rot = caption_rotation(page, tuple(cr)) if kind == "table" else 0
                pix = page.get_pixmap(clip=rect, dpi=d_eff)
                br = blank_ratio(pix)
                if br > keep_blank:
                    skipped.append((key, pno + 1, f"거의 백지({br:.3f})"))
                    continue
                if key in seen:                # 같은 번호가 또 나오면 큰 쪽만 (2단 재조판 등)
                    if pix.width * pix.height <= seen[key]["px"]:
                        skipped.append((key, pno + 1, "중복(작은 쪽)"))
                        continue
                    found = [f for f in found if f["key"] != key]
                fn = f"{_fname_prefix(kind)}_{label.upper()}.png"
                rec = {"key": key, "kind": kind, "label": label.upper(), "page": pno + 1,
                       "file": fn, "caption": caption[:900], "rotated_deg": rot,
                       "bbox": [round(v, 1) for v in rect],
                       "w": pix.width, "h": pix.height, "px": pix.width * pix.height, "dpi": d_eff,
                       "src": Path(pdf_path).name, "blank": round(br, 3)}
                seen[key] = rec
                found.append(rec)
                if not dry:
                    out_dir.mkdir(parents=True, exist_ok=True)
                    pix.save(out_dir / fn)
                    if rot:
                        _upright(out_dir / fn, rot)
                    _shrink(out_dir / fn)
        doc.close()

    def sortkey(r):
        L = r["label"]
        return (r["kind"] != "figure", L.startswith("S"),
                int(re.sub(r"\D", "", L) or 0))
    found.sort(key=sortkey)
    for r in found:
        r.pop("px", None)
    meta = {"slug": slug, "dpi": dpi, "maxpx": maxpx,
            "generated": time.strftime("%Y-%m-%d"),
            # ⚠ 원본 PDF 는 repo 에 없다(wiki/inbox 는 .gitignore). 그래서 **어느 하위 폴더의
            #   어느 파일**이었는지를 남긴다 — 다른 머신에서도 --inbox_dir 만 맞추면 다시 찾는다.
            "sources": [_relto(p, relto) for p in pdf_paths],
            "figures": found}
    if not dry:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "figures.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta, skipped



def extract_slides(pdf_path, slug, dpi=150, dry=False, maxpx=1600,
                   keep_blank=0.995, relto=None, nup=1):
    """발표 덱(PPT→PDF)을 **슬라이드 1장 = 그림 1장**으로 자른다 (`--slides`).

    왜 별도 모드인가 — 본체 extract() 는 "Fig. 1." 같은 **저널 캡션을 앵커**로 쓴다.
    PPT 덱에는 그런 캡션이 아예 없어서 본체를 돌리면 **0장**이 나온다(wiki/raw/talks 4편 실측).
    덱은 슬라이드 자체가 그림이므로 쪽을 통째로 렌더하는 게 맞다.

    캡션 = 그 슬라이드의 상단 텍스트(제목·불릿 앞부분). digest 에서 `Fig. 7` 로 쓰면
    **슬라이드 7**을 가리키게 라벨을 쪽번호로 맞춘다 (덱 자체 인쇄 번호와 다를 수 있으니
    digest 에 "PDF 쪽 = 슬라이드" 를 명시할 것).

    ⭐ `nup=2` (2026-08-25) — **2-up 인쇄 자료집**(한 쪽에 슬라이드 2장)을 위·아래로
      나눈다. 심포지엄 자료집이 대개 이 꼴이라 쪽 렌더만 하면 슬라이드 두 장이 한 그림에
      뭉쳐 digest 가 "Fig. 3" 으로 무엇을 가리키는지 모호해진다.
      라벨은 `<쪽>a` / `<쪽>b` 로 준다 — 덱 자체 인쇄 번호와 다를 수 있으므로
      digest 에 **"PDF 쪽-위치 ↔ 덱 인쇄번호"** 대응을 반드시 적을 것.
      ⚠ 반쪽이 거의 백지면(간지·마지막 홀수 슬라이드) 그 반쪽만 버린다.

    이 모드가 못 하는 것: 한 슬라이드 안의 여러 패널을 나누지 않는다(a/b/c 분해 없음).
      nup 은 **균등 분할**이라 위아래 여백이 다른 레이아웃에서는 경계가 어긋날 수 있다 —
      결과를 눈으로 확인할 것.
    """
    out_dir = OUT_ROOT / slug
    doc = fitz.open(pdf_path)
    found, skipped = [], []
    for pno in range(doc.page_count):
        page = doc[pno]
        d_eff = dpi
        if maxpx:
            long_pt = max(page.rect.width, page.rect.height)
            if long_pt > 0:
                d_eff = min(dpi, max(72, int(maxpx * 72.0 / long_pt)))
        # ── nup 분할 (2-up 자료집) ─────────────────────────────────────
        if nup > 1:
            # ⚠ 2026-08-25 — 여백 자동탐지를 붙였다가 **되돌렸다.** digest 작성 쪽에서
            #   "크롭이 반 슬라이드 어긋난다" 는 보고가 왔지만, fig_3a·fig_15b 를 직접
            #   열어 보니 슬라이드가 온전하고 하단 소번호("1", "26")도 들어 있었다 —
            #   **보고가 틀렸다.** 그리고 흰 띠 신호 자체가 못 믿을 것이었다
            #   (중앙영역 최장 띠 중심이 쪽마다 362/568/316/431 로 제각각).
            #   없는 버그를 고치려 불안정한 탐지기를 넣는 것이 더 나쁘다 → 균등 분할 유지.
            #   레이아웃이 실제로 어긋나는 덱을 만나면 --nup-offset 을 여는 것이 맞다.
            h = page.rect.height / nup
            for k in range(nup):
                clip = fitz.Rect(page.rect.x0, page.rect.y0 + k * h,
                                 page.rect.x1, page.rect.y0 + (k + 1) * h)
                sub = page.get_pixmap(dpi=d_eff, clip=clip)
                sbr = blank_ratio(sub)
                # ⛔ 2026-08-25 (codex D) — `'ab cdef'[2]` 가 **공백**이라 nup=3 에서
                #   라벨이 `1a, 1b, "1 "` 이 됐다. 문자열 슬라이싱 대신 목록으로.
                _SUF = "abcdefgh"
                sublab = f"{pno + 1}{_SUF[k]}" if k < len(_SUF) else f"{pno + 1}_{k}"
                # ⛔ 2026-08-25 (codex D·E) — 여기서 `continue` 로 **슬롯을 버렸다.**
                #   26쪽×2 = 52 슬롯인데 manifest 엔 50개뿐이었고(2a·2b 소멸) 이유가
                #   어디에도 안 남았다. skipped 는 콘솔로만 나가 기록이 아니다.
                #   판정: blank_score 는 **삭제 기준이 아니라 검토 우선순위 점수**다.
                #   전 슬롯·전 PNG 를 남기고, 사람이 확인해야 blank_confirmed 가 된다.
                blank_cand = sbr > keep_blank
                cap = " / ".join(
                    " ".join(b[4].split()) for b in sorted(text_blocks(page), key=lambda b: b[1])
                    if b[4].strip() and clip.y0 <= b[1] < clip.y1)[:900]
                fn = f"fig_{sublab}.png"
                found.append({"key": f"F{sublab}", "kind": "figure", "label": sublab,
                              "slot_id": sublab,
                              "page": pno + 1, "file": fn, "caption": cap,
                              "rotated_deg": 0,
                              "bbox": [round(v, 1) for v in clip],
                              "w": sub.width, "h": sub.height, "dpi": d_eff,
                              "src": Path(pdf_path).name, "blank": round(sbr, 3),
                              "blank_score": round(sbr, 3),
                              # 자동 분류일 뿐 확정 아님 — 확정은 사람만 한다
                              "content_status": "blank_candidate" if blank_cand else "content",
                              "artifact_retained": True,
                              "digest_included": not blank_cand,
                              "reviewed": False,
                              "slide": True, "nup": nup, "nup_index": k})
                if blank_cand:
                    skipped.append((f"F{sublab}", pno + 1,
                                    f"백지 후보({sbr:.3f}) — 보존됨, 검토 대기"))
                if not dry:
                    out_dir.mkdir(parents=True, exist_ok=True)
                    sub.save(out_dir / fn)
                    _shrink(out_dir / fn)
            continue

        pix = page.get_pixmap(dpi=d_eff)
        br = blank_ratio(pix)
        blank_cand = br > keep_blank             # 표지 뒤 백지·간지 — **버리지 않는다**
        # 캡션 = 위에서부터 텍스트 블록을 이어붙인다 (제목 + 첫 불릿이면 충분)
        cap = " / ".join(
            " ".join(b[4].split()) for b in sorted(text_blocks(page), key=lambda b: b[1])
            if b[4].strip())[:900]
        label = str(pno + 1)
        fn = f"fig_{label}.png"
        found.append({"key": f"F{label}", "kind": "figure", "label": label,
                      "slot_id": label,
                      "page": pno + 1, "file": fn, "caption": cap, "rotated_deg": 0,
                      "bbox": [round(v, 1) for v in page.rect],
                      "w": pix.width, "h": pix.height, "dpi": d_eff,
                      "src": Path(pdf_path).name, "blank": round(br, 3),
                      "blank_score": round(br, 3),
                      "content_status": "blank_candidate" if blank_cand else "content",
                      "artifact_retained": True,
                      "digest_included": not blank_cand,
                      "reviewed": False,
                      "slide": True})
        if blank_cand:
            skipped.append((f"F{label}", pno + 1,
                            f"백지 후보({br:.3f}) — 보존됨, 검토 대기"))
        if not dry:
            out_dir.mkdir(parents=True, exist_ok=True)
            pix.save(out_dir / fn)
            _shrink(out_dir / fn)
    doc.close()
    meta = {"slug": slug, "dpi": dpi, "maxpx": maxpx, "mode": "slides", "nup": nup,
            "generated": time.strftime("%Y-%m-%d"),
            "sources": [_relto(Path(pdf_path), relto)], "figures": found}
    if not dry:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "figures.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta, skipped


# ── inbox 자동 매칭 ─────────────────────────────────────────────────────
#   1저자가 `--slug <slug>` 를 그대로 붙여넣어 bash 오류를 냈다(2026-08-06).
#   자리표시자를 직접 채우게 하지 말고, inbox 를 훑어 digest 와 자동으로 짝지어 준다.
INBOX = ROOT / "wiki" / "inbox"
PAPERS = ROOT / "wiki" / "raw" / "papers"
PDF_MAP = ROOT / "wiki" / "raw" / "pdf_map.tsv"


def load_map():
    """손으로 지정한 slug ↔ PDF 짝 (wiki/raw/pdf_map.tsv). 자동 매칭보다 **우선**한다.

    ⚠ 왜 필요한가 (2026-08-06): digest 제목이 원제를 의역한 경우가 많아 파일명과 토큰이
      안 겹친다. 문턱을 낮추면 다른 데서 오탐이 터진다(실측: 본문 색인을 넓히면 6건 중
      3건은 붙고 다른 1건은 오히려 밀렸다). 자동으로 안 되는 것만 여기 적는다.
      형식: `<slug>\t<PDF 파일명 일부>`  (# 은 주석). 파일명은 **부분 일치**면 된다.
    """
    if not PDF_MAP.exists():
        return []
    out = []
    for ln in PDF_MAP.read_text(encoding="utf-8").splitlines():
        ln = ln.split("#")[0].strip()
        if not ln or "\t" not in ln:
            continue
        slug, pat = (x.strip() for x in ln.split("\t", 1))
        if slug and pat:
            out.append((slug, pat.lower()))
    return out


def pdf_roots(inbox_dir=""):
    """PDF 를 찾을 곳들 (순서대로).

    ⚠ 왜 업로드 폴더까지 (2026-08-06 1저자 요청 "논문 에이전트 먹이면 자동으로"):
      채팅에 올린 PDF 는 wiki/inbox/ 가 아니라 Claude Code 업로드 폴더에 떨어진다.
      inbox 에만 의존하면 "방금 올린 논문"을 못 찾아 매번 --pdf 로 경로를 줘야 한다.
    """
    out = []
    if inbox_dir:
        out.append(Path(inbox_dir).expanduser())
    else:
        out.append(INBOX)
    env = os.environ.get("CLAUDE_UPLOAD_DIR", "")
    if env:
        out.append(Path(env).expanduser())
    up = Path.home() / ".claude" / "uploads"
    if up.is_dir():                             # 세션별 폴더 — 최근 것부터
        try:
            out += sorted((d for d in up.iterdir() if d.is_dir()),
                          key=lambda d: -d.stat().st_mtime)
        except OSError:
            pass
    seen, uniq = set(), []
    for d in out:
        if d.is_dir() and d not in seen:
            seen.add(d); uniq.append(d)
    return uniq
# SI 판별. ⚠ `si` 를 느슨하게 잡으면 **원소 기호 Si** 를 SI 로 오인한다 — 실측(2026-08-06):
#   "43. Phase stability … of the Li10±1MP2X12 (M = Ge, Si, Sn …)" 이 SI 로 분류돼
#   본문이 사라지고 그림 번호가 전부 S1,S2… 로 잘못 붙었다.
#   그래서 sup/mmc 계열은 느슨하게, **si·esi 는 파일명 구분자(_ - .)로 둘러싸인 때만** 본다
#   (tz4c02029_si_001.pdf ○ / ", Si," ×).
SI_TAG = re.compile(
    r"(?:(?:^|[^a-z])sup(?:p|pl|porting|plementary|plement|pmat)?(?:[^a-z]|$)"
    r"|(?:^|[^a-z])mmc(?:[^a-z]|$)"
    r"|(?:^|[_\-.])e?si(?:[_\-.0-9]|$))", re.I)
STOP = set("""the a an of on in for and or to with by from as at is are was were be been its
their this that these those we our using via toward towards into over under between among
new novel high low high- ultra super study investigation effect effects influence role
based enabling enables enabled behavior behaviour properties property analysis review
paper article letter communication sup supporting information supplementary supplement
""".split())


# ⚠ \b 를 쓰면 안 된다: `_` 가 단어문자라 'Minnmann_2021_J' 에서 연도를 못 잡는다(실측).
#   앞뒤에 **숫자만** 없으면 되고(긴 숫자열 속 우연한 20xx 는 제외), _ - . 공백은 경계로 본다.
YEAR_RE = re.compile(r"(?<![0-9])(?:19|20)\d{2}(?![0-9])")


def _years(t):
    return set(YEAR_RE.findall(t or ""))


def _toks(s):
    """제목/파일명 → 비교용 토큰 집합.

    ⚠ 인접 토큰을 이어붙인 것도 넣는다: 파일명은 구두점이 지워져 `solidstate` 인데
      제목은 `solid-state` 라 그냥 토큰만 쓰면 안 겹친다(실측: inbox #39, #4, #50 미배정).
    """
    s = re.sub(r"[^0-9a-zA-Z]+", " ", s.lower())
    seq = [t for t in s.split() if len(t) > 2 and t not in STOP and not t.isdigit()]
    out = set(seq)
    out |= {a + b for a, b in zip(seq, seq[1:])}
    return out


def _paper_index():
    """slug → (제목 토큰, inbox 번호 or None)."""
    out = {}
    for f in sorted(PAPERS.glob("*.md")):
        if f.name.startswith("_"):
            continue
        head = f.read_text(encoding="utf-8", errors="ignore")[:4000]
        title = next((ln.lstrip("# ").strip() for ln in head.splitlines()
                      if ln.startswith("# ")), f.stem)
        m = re.search(r"inbox\s*#\s*(\d+)", head)
        out[f.stem] = (_toks(title) | _toks(f.stem), int(m.group(1)) if m else None)
    return out


def _idf(papers):
    """토큰 희소도. `batteries`·`lithium` 처럼 어느 논문에나 있는 말은 증거가 못 된다.

    ⚠ 왜 (2026-08-06 실측): `batteries-12-00060-v2.pdf`(MDPI 파일명, 제목 정보 0)가
      살아남은 토큰 `batteries` 하나로 엉뚱한 논문에 "제목 100%" 로 붙었다.
      단순 개수 대신 **희소한 토큰이 맞았는가**로 점수를 매긴다.
    """
    df = {}
    for tt, _n in papers.values():
        for t in tt:
            df[t] = df.get(t, 0) + 1
    n = max(len(papers), 1)
    return df, (lambda t: math.log(1.0 + n / df.get(t, 0.5)))


def match_inbox(inbox=INBOX, min_score=0.45, min_hits=4, rare=3):
    """inbox PDF → slug 매칭. (배정, 미배정) 반환.

    앵커 세 가지: ① digest 메타의 `inbox #NN` ↔ 파일명 맨 앞 번호 (정확), 흔치 않다(160편 중 20).
                 ② 제목 토큰 겹침 — **IDF 가중**(흔한 말은 거의 0점)
                 ③ 그래도 못 찾으면 PDF 1쪽 본문
    """
    papers = _paper_index()
    df, idf = _idf(papers)

    def score(ft, tt):
        """맞은 토큰의 희소도 합 / 파일명 토큰 전체의 희소도 합."""
        den = sum(idf(t) for t in ft)
        if den <= 0:
            return 0.0, set()
        hit = ft & tt
        return sum(idf(t) for t in hit) / den, hit
    bynum = {n: s for s, (_t, n) in papers.items() if n}
    assign, orphan = {}, []
    # ⚠ rglob: 논문은 보통 주제·교수님별 하위 폴더로 나뉘어 있다(2026-08-06 1저자 폴더 실측).
    #   최상위만 보면 한 편도 못 찾는다. 숨김/휴지통성 폴더는 건너뛴다.
    manual = load_map()
    # 지도의 오타가 조용히 묻히지 않게 — 없는 slug / 아무 파일도 못 맞춘 패턴을 보고한다
    bad_slug = [s for s, _pat in manual if not (PAPERS / f"{s}.md").exists()]
    used = set()

    # ⚠ **번호가 유일할 때만 번호를 쓴다** (2026-08-06 1저자 발견).
    #   폴더가 주제별로 나뉘어 있고(DEM 논문/·DFT 먹인 논문/·이상욱 교수님/…) **폴더마다 01 부터
    #   다시 매겨진다**. 그래서 `#33` 이 서로 다른 논문 두 편을 가리켰고, 둘 다 같은 slug 로 붙어
    #   argyrodite 논문 그림 목록에 DEM 그림 20장이 섞였다(adeli2019: 37장 중 20장이 남의 것,
    #   같은 라벨끼리 덮어써서 원래 Fig 1 은 사라졌다). 전체 112편 중 19편이 이 상태였다.
    #   → 번호가 여러 폴더에서 겹치면 번호는 열쇠가 아니다. 제목 토큰으로만 판정한다.
    _num_cores = {}
    for _p in inbox.rglob("*.pdf"):
        if any(d.startswith((".", "~$")) or d in ("$RECYCLE.BIN", "node_modules")
               for d in _p.relative_to(inbox).parts[:-1]):
            continue
        if (mm := re.match(r"\s*(\d+)\s*[.)]", _p.stem)):
            core = re.sub(r"^\s*\d+\s*[.)]\s*", "", _p.stem)
            core = SI_TAG.sub(" ", core).strip().lower()[:45]   # 같은 논문의 SI 판본은 한 편으로
            _num_cores.setdefault(int(mm.group(1)), set()).add(core)
    dup_nums = {n for n, cores in _num_cores.items() if len(cores) > 1}
    for p in sorted(inbox.rglob("*.pdf")):
        if any(d.startswith((".", "~$")) or d in ("$RECYCLE.BIN", "node_modules")
               for d in p.relative_to(inbox).parts[:-1]):
            continue
        name = p.stem
        num = int(m.group(1)) if (m := re.match(r"\s*(\d+)\s*[.)]", name)) else None
        si = bool(SI_TAG.search(name))
        slug, why = None, ""
        low = str(p.relative_to(inbox)).lower()
        for m_slug, pat in manual:            # ① 손으로 지정한 것이 최우선
            if pat in low:
                slug, why = m_slug, "수동 지정"
                used.add(pat)
                break
        if slug:
            pass
        elif num is not None and num in bynum and num not in dup_nums:
            slug, why = bynum[num], f"inbox #{num}"
        else:
            core = re.sub(r"^\s*\d+\s*[.)]\s*", "", name)
            ft = _toks(core)
            fyears = _years(core)
            need = min(min_hits, len(ft))
            best, bs = None, 0.0
            for s, (tt, _n) in papers.items():
                # ⚠ 연도가 어긋나면 같은 저자의 **다른 논문**이다 (2026-08-06 실측:
                #   'Minnmann_2021_J.Electrochem.Soc' 이 minnmann2024 digest 에 100% 로 붙었다
                #   — 파일명에 남은 토큰이 'minnmann' 하나뿐이라 만점이 나왔다).
                sy = _years(s)
                if sy and fyears and not (sy & fyears):
                    continue
                sc, hit = score(ft, tt)
                if len(hit) < need or sc <= bs:
                    continue
                # 토큰이 min_hits 에 못 미치면(ECERD2600097 처럼 짧은 파일명) **희소한**
                # 토큰이 맞았을 때만, 그것도 **거의 다 맞았을 때만** 인정한다.
                #   ⚠ 느슨하면 'Minnmann_2021_J.Electrochem.Soc'(digest 없는 논문)가
                #     electrochem/soc 몇 개로 엉뚱한 digest 에 56% 로 붙는다 (2026-08-06 실측).
                if len(hit) < min_hits and not (
                        sc >= 0.75 and any(df.get(t, 0) <= rare for t in hit)):
                    continue
                best, bs = s, sc
            if best and bs >= min_score:
                slug, why = best, f"제목 {bs:.0%}"
        if slug:
            assign.setdefault(slug, {"main": [], "si": [], "why": why})
            assign[slug]["si" if si else "main"].append(p)
        else:
            orphan.append((p, si))

    # 파일명이 출판사 해시인 것들(admi202200011sup0001suppmat.pdf, 1s2.0S…mmc1.pdf)은
    # 이름으로는 못 잡는다 → **1쪽 본문**을 읽어 한 번 더 시도한다.
    still = []
    for p, si in orphan:
        try:
            with fitz.open(p) as d:
                head = d[0].get_text()[:600] if d.page_count else ""
        except Exception:
            head = ""
        ft = _toks(head)
        best, bs = None, 0.0
        for s, (tt, _n) in papers.items():
            # 여긴 **제목 쪽** 기준으로 본다 (1쪽 본문이 제목보다 훨씬 길다)
            sc, hit = score(tt, ft)
            if len(hit) >= 5 and sc > bs:
                best, bs = s, sc
        if best and bs >= 0.45:
            assign.setdefault(best, {"main": [], "si": [], "why": f"1쪽 본문 {bs:.0%}"})
            assign[best]["si" if si else "main"].append(p)
        else:
            still.append((p, si))
    dead = [(s, pat) for s, pat in manual if pat not in used]
    if bad_slug or dead:
        print("⚠ wiki/raw/pdf_map.tsv 점검")
        for s in bad_slug:
            print(f"   없는 slug: {s}")
        # 일부 폴더만 훑을 땐 대부분 안 맞는 게 정상이라 목록을 줄여 낸다
        for s, pat in dead[:10]:
            print(f"   아무 PDF 도 못 맞춘 패턴: {s}  ←  '{pat[:52]}'")
        if len(dead) > 10:
            print(f"   … 외 {len(dead)-10}개 (이 폴더에 그 PDF 가 없으면 정상)")
        print()
    return assign, still


def _relto(p, base):
    """inbox 기준 상대경로 (없으면 파일명만)."""
    p = Path(p)
    if base:
        try:
            return str(p.relative_to(base))
        except ValueError:
            pass
    return p.name


def _show(p, box, width=76):
    """inbox 기준 상대경로. 길면 **파일명 쪽을** 줄인다 — 어느 하위 폴더였는지가 더 중요하다."""
    t = _relto(p, box)
    if len(t) <= width:
        return t
    head, _, tail = t.rpartition("/")
    keep = width - len(head) - 2
    return (head + "/" + tail[:max(keep, 12)] + "…") if head and keep > 12 else t[:width - 1] + "…"


def _read_plan(slug, meta, top=8):
    """**에이전트가 다음에 할 일**을 출력에 박아 넣는다.

    ⚠ 왜 (2026-08-06 1저자 요청): "논문 먹이면 저절로 되게". 규칙을 에이전트 프롬프트에만
      적어두면 잊는다. 자른 직후 화면에 '이 파일들을 Read 하라'가 경로째로 찍혀 있으면
      그게 다음 행동이 된다. 사람이 볼 때도 어느 그림부터 볼지 안내가 된다.
    표(tab_*)는 뺀다 — 글자라서 이미지로 읽는 것보다 PDF 텍스트가 정확하다.
    """
    figs = [r for r in meta["figures"] if r["kind"] != "table"]
    if not figs:
        return
    main = [r for r in figs if not r["label"].startswith("S")]
    si = [r for r in figs if r["label"].startswith("S")]
    pick = (main + si)[:top]
    ntab = len(meta["figures"]) - len(figs)
    print()
    print("┌─ 다음 단계 (필수) — 잘라낸 그림을 **Read 로 실제로 본다** ─────────────")
    print("│  캡션만 읽고 쓰면 축·단위·마커 위치를 지어내게 된다. 보고 나서 digest 를 쓴다.")
    for r in pick:
        cap = r["caption"][:58].replace("\n", " ")
        print(f"│  Read wiki/raw/figures/{slug}/{r['file']}   ({cap}…)")
    if len(figs) > top:
        print(f"│  … 본문 그림 {len(main)} + SI {len(si)} 중 위 {len(pick)}장이 우선. "
              f"나머지는 필요할 때만.")
    if ntab:
        print(f"│  표 {ntab}장(tab_*.png)은 이미지로 안 읽는다 — PDF 텍스트가 정확하다.")
    print("│  본 그림에서만 읽은 값은 digest 에 `figure-read ≈` 로 표시하고,")
    print("│  무엇을 보고 무엇을 안 봤는지 사용자에게 밝힌다.")
    print("└──────────────────────────────────────────────────────────────────")


def _report(slug, meta, skipped, dry):
    print(f"=== {slug} — {len(meta['figures'])}개 추출"
          f"{' (dry-run, 안 씀)' if dry else ''}")
    print("key    p   크기         공백  캡션")
    for r in meta["figures"]:
        print(f"{r['key']:<6} {r['page']:<3} {r['w']}x{r['h']:<7} "
              f"{r['blank']:.2f}  {r['caption'][:64]}")
    if skipped:
        print(f"--- 제외 {len(skipped)}건 (오탐 방지)")
        for k, p, why in skipped[:18]:
            print(f"  {k:<6} p{p:<3} {why}")
    if not dry:
        print(f"→ wiki/raw/figures/{slug}/  (figures.json 포함)")
        _read_plan(slug, meta)


def suggest(inbox):
    """그림이 없는 digest × 짝 못 찾은 PDF → **후보 표**를 만들어 준다.

    자동 매칭이 못 붙인 것을 손으로 채우기 쉽게, pdf_map.tsv 에 그대로 붙일 수 있는
    형태로 낸다. 사람이 보고 틀린 줄만 지우면 된다.
    """
    papers = _paper_index()
    df, idf = _idf(papers)
    have = {d.name for d in OUT_ROOT.iterdir()
            if d.is_dir() and (d / "figures.json").exists()} if OUT_ROOT.is_dir() else set()
    assign, orphan = match_inbox(inbox)
    pool = [p for p, _si in orphan]
    todo = [s for s in papers if s not in have and s not in assign]
    print(f"=== 후보 제안: 그림 없는 digest {len(todo)}편 × 짝 못 찾은 PDF {len(pool)}개\n")
    print("# 아래를 wiki/raw/pdf_map.tsv 에 붙이고 **틀린 줄은 지운다** (slug<TAB>파일명 일부)")
    n = 0
    for s in sorted(todo):
        tt = papers[s][0]
        best = []
        for p in pool:
            ft = _toks(re.sub(r"^\s*\d+\s*[.)]\s*", "", p.stem))
            den = sum(idf(t) for t in ft)
            hit = ft & tt
            sc = (sum(idf(t) for t in hit) / den) if den else 0
            if sc > 0.12:
                best.append((sc, p))
        best.sort(key=lambda x: -x[0])
        if not best:
            continue
        n += 1
        for sc, p in best[:3]:
            mark = "" if sc >= 0.3 else "#  ⚠낮음 "
            print(f"{mark}{s}\t{p.stem[:74]}   # {sc:.0%}")
        print()
    print(f"# 후보가 있는 digest {n}편 — 나머지는 PDF 가 이 폴더에 없다")
    return 0


def refresh(box, apply_it=False, dpi=300, maxpx=3000):
    """추출기를 고친 뒤 **결과가 달라지는 논문만** 골라 다시 뽑는다.

    ⚠ 왜 (2026-08-06): 전체 재생성은 PNG 가 통째로 새 blob 이 되어 .git 이 한 번에
      수백 MB 늘어난다(실측: 재생성 4회에 .git 972 MB). 고친 규칙이 실제로 영향을 준
      논문만 다시 뽑으면 히스토리가 그만큼만 는다.
    먼저 dry-run 으로 장수를 비교해 표를 내고, --apply 를 줘야 실제로 덮어쓴다.
    """
    assign, _o = match_inbox(box)
    todo = [d for d in sorted(OUT_ROOT.glob("*/figures.json")) if d.parent.name in assign]
    print(f"훑는 중… PDF 가 있는 {len(todo)}편을 dry-run 으로 비교한다 "
          f"(렌더링은 안 하지만 쪽 분석은 실제와 같아 몇 분 걸린다)")
    rows = []
    for k, d in enumerate(todo, 1):
        slug = d.parent.name
        v = assign[slug]
        # 진행이 보이게 — 안 그러면 몇 분 동안 화면이 멈춘 것처럼 보인다
        print(f"\r  [{k}/{len(todo)}] {slug[:52]:<52}", end="", flush=True)
        try:
            old = len(json.loads(d.read_text(encoding="utf-8")).get("figures", []))
        except (OSError, ValueError):
            old = -1
        pdfs = [str(q) for q in v["main"] + v["si"]]
        try:
            meta, _sk = extract(pdfs, slug, dry=True, dpi=dpi, maxpx=maxpx)
            new = len(meta["figures"])
        except Exception as e:
            print(f"   ⛔ {slug}: {type(e).__name__}: {e}")
            continue
        if new != old:
            rows.append((slug, old, new, pdfs))
    print(f"\r{' ' * 68}\r", end="")
    print(f"=== 재추출 대상: {len(rows)}편 (PDF 가 있는 {len(todo)}편 중)")
    for slug, old, new, _p in rows:
        print(f"   {slug[:56]:<56} {old:>3} → {new:>3}  ({new-old:+d})")
    if not rows:
        print("   바뀌는 게 없다 — 다시 뽑을 필요 없음")
        return 0
    if not apply_it:
        print("\n※ 표만 냈다. 실제로 덮어쓰려면 --apply 를 붙인다.")
        return 0
    print()
    for i, (slug, _o, _n, pdfs) in enumerate(rows, 1):
        print(f"[{i}/{len(rows)}] {slug}")
        shutil.rmtree(OUT_ROOT / slug, ignore_errors=True)
        meta, skipped = extract(pdfs, slug, dpi=dpi, maxpx=maxpx, relto=box)
        _report(slug, meta, skipped, dry=False)
        print()
    _write_sources_index()
    return 0


def _write_sources_index():
    """slug → 원본 PDF (inbox 상대경로) 한눈 색인.

    PDF 본체는 repo 에 없으므로(저작권·용량), **어디서 왔는지**만이라도 추적 가능하게 둔다.
    figures.json 마다 들어 있는 sources 를 모아 wiki/raw/figures/_sources.json 로 쓴다.
    """
    idx = {}
    for j in sorted(OUT_ROOT.glob("*/figures.json")):
        try:
            m = json.loads(j.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        idx[m.get("slug", j.parent.name)] = {"pdfs": m.get("sources", []),
                                             "figures": len(m.get("figures", [])),
                                             "generated": m.get("generated")}
    if idx:
        (OUT_ROOT / "_sources.json").write_text(
            json.dumps(idx, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")
        print(f"→ wiki/raw/figures/_sources.json  ({len(idx)}편: 어느 PDF 에서 왔는지 색인)")


def why(slug, pdfs):
    """왜 그 그림이 버려졌는지 좌표째로 — '영역 없음' 의 원인을 눈으로 본다.

    캡션은 찾았는데 위/아래 어느 쪽도 36 pt 를 못 넘으면 버린다. 그 판단에 쓰인
    병합 캡션 bbox·경계선·후보 사각형·주변 그래픽을 전부 찍는다.
    """
    for pdf_path in pdfs:
        doc = fitz.open(pdf_path)
        si_file = bool(SI_TAG.search(Path(pdf_path).stem))
        print(f"\n##### {Path(pdf_path).name[:78]}  (SI 파일? {si_file})")
        for pno in range(doc.page_count):
            page = doc[pno]
            blocks = text_blocks(page)
            caps = [(b, is_caption(b[4])) for b in blocks]
            for cap, hit in caps:
                if not hit:
                    continue
                kind, label, cap_si = hit
                cr, captxt = merge_caption(blocks, cap)
                up, ui, ud = _side_rect(page, tuple(cr), blocks, up=True)
                dn, di, dd = _side_rect(page, tuple(cr), blocks, up=False)
                ok = (up is not None and (ui or ud >= 6)) or (dn is not None and (di or dd >= 6))
                print(f"  p{pno+1} {kind[0]}{label}{' (SI캡션)' if cap_si else ''} "
                      f"{'OK' if ok else '⛔'}")
                print(f"      쪽 {tuple(round(v) for v in page.rect)} · "
                      f"캡션블록 {tuple(round(v) for v in cap[:4])} → 병합 "
                      f"{tuple(round(v) for v in cr)}")
                for nm, r, ni, nd in (("위", up, ui, ud), ("아래", dn, di, dd)):
                    if r is None:
                        print(f"      {nm}: 없음 (높이 36 pt 미만)")
                    else:
                        print(f"      {nm}: {tuple(round(v) for v in r)} "
                              f"h={r.height:.0f} 이미지{ni} 벡터{nd}")
                if not ok:
                    g = graphics(page)
                    print(f"      쪽 전체 그래픽 {len(g)}개: "
                          + ", ".join(f"{k}{tuple(round(v) for v in r)}" for k, r in g[:4]))
                    print(f"      캡션 앞뒤 블록:")
                    for b in sorted(blocks, key=lambda b: b[1]):
                        if abs(b[1] - cr.y0) < 260:
                            print(f"        {tuple(round(v) for v in b[:4])} "
                                  f"{' '.join(b[4].split())[:56]}")
        doc.close()
    return 0


def audit_src():
    """**남의 논문 그림이 섞였는지** 점검 (2026-08-06 1저자 발견 뒤 신설).

    폴더마다 번호가 01 부터 다시 매겨져 `#33` 이 두 편을 가리키면 둘 다 같은 slug 로 붙었다
    (매칭은 고쳤다 — 아래는 **이미 만들어 둔 데이터** 점검용).
    그림마다 어느 PDF 에서 왔는지 `src` 가 남아 있으므로, 그 파일명이 그 논문 제목과
    얼마나 겹치는지(IDF 가중)로 가른다. 재크로핑 뒤 0 이 나와야 정상.

    ⚠ 출판사 해시 이름 SI(`anie…-sup-0001-misc_information.pdf`)는 제목 토큰이 없어
      낮게 나온다 — 그런 건 `(?)` 로 따로 표시하고 오염으로 세지 않는다.
    """
    papers = _paper_index()
    _df, idf = _idf(papers)

    def sc(ft, tt):
        den = sum(idf(t) for t in ft)
        return (sum(idf(t) for t in (ft & tt)) / den) if den > 0 else 0.0

    bad_tot = n_slug = 0
    for j in sorted(OUT_ROOT.glob("*/figures.json")):
        slug = j.parent.name
        if slug not in papers:
            continue
        try:
            figs = json.loads(j.read_text(encoding="utf-8")).get("figures", [])
        except (OSError, ValueError):
            continue
        per = {}
        for f in figs:
            per.setdefault(f.get("src", ""), []).append(f.get("key", "?"))
        if len(per) < 2:
            continue
        tt = papers[slug][0]
        score = {}
        for s in per:
            core = re.sub(r"^\s*\d+\s*[.)]\s*", "", Path(s).name)
            score[s] = sc(_toks(SI_TAG.sub(" ", core)), tt)
        best = max(score.values())
        # 제목과 거의 안 겹치는데 **다른 출처는 잘 겹치는** 경우만 남의 것으로 본다
        bad = {s: v for s, v in per.items() if score[s] < 0.20 < best}
        if not bad:
            continue
        # 파일명이 출판사 해시(anie202007621-sup-0001-misc…)면 그 논문 SI 일 수 있다 → 판정 보류.
        # 가름: **다른 논문 제목에도 쓰이는 낱말**(df ≥ 1)이 3개 이상이어야 '알아볼 수 있는 제목'.
        def known(s):
            return sum(1 for t in _toks(Path(s).name) if _df.get(t, 0) >= 1)
        sure = {s: v for s, v in bad.items() if known(s) >= 3}
        n_bad = sum(len(v) for v in sure.values())
        if n_bad:
            n_slug += 1
            bad_tot += n_bad
        print(f"{'⛔' if n_bad else '？'} {slug}: {len(figs)}장 중 {n_bad}장 남의 것")
        for s, keys in sorted(per.items(), key=lambda kv: -score[kv[0]]):
            mark = "✓" if s not in bad else ("✗" if s in sure else "？")
            print(f"     {mark} [{score[s]:4.0%}] {Path(s).name[:66]}  ({len(keys)}장)")
    print(f"\n== 남의 그림이 섞인 논문 {n_slug}편 · 총 {bad_tot}장"
          + ("  ✅ 깨끗함" if not bad_tot else "  → 재크로핑 필요"))
    return 1 if bad_tot else 0


def dup_groups(slug_dir):
    """한 slug 폴더 안에서 **바이트가 똑같은** PNG 묶음을 찾는다.

    같은 크롭이 서로 다른 번호로 두 번 나오면 그 번호 중 하나(이상)는
    **실제로 잘린 적이 없다** — 여러 쪽에 걸친 표, 회전된 표, 캡션이 두 번 나오는 배치에서 생긴다.
    돌려주는 값: [[keep_path, dup_path, ...], ...]
    첫 번째 = 남길 것 = **자연순(숫자 인식) 최소** — `fig_9` 가 `fig_10` 보다 앞이다
    (사전순이면 fig_10 이 앞이라 번호가 큰 쪽을 남기는 오류가 난다).

    이 함수가 못 하는 것:
      · **내용이 같지만 바이트가 다른** 크롭(다시 자른 것, 1픽셀 차이)은 못 잡는다.
        픽셀 비교나 근사해시(dHash)는 하지 않는다 — 오탐이 진짜를 가린다.
      · **어느 쪽이 진짜인지는 못 고른다.** 자연순 최소를 남기는 건 결정론적 타이브레이크일 뿐이고,
        묶음에 그림과 표가 섞이면(예: `fig_11` ≡ `tab_1`) 사람이 봐야 한다 — 그래서 `dedupe` 가
        지운 쪽에 `dup_of` 를 남긴다.
    """
    def natkey(p):
        return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", p.name)]
    by_hash = {}
    for p in sorted(Path(slug_dir).glob("*.png"), key=natkey):
        h = hashlib.sha1(p.read_bytes()).hexdigest()
        by_hash.setdefault(h, []).append(p)
    return [v for v in by_hash.values() if len(v) > 1]


def dedupe(apply_it=False):
    """바이트 동일 크롭을 지우고 figures.json 에 `dup_of` 표식을 남긴다.

    표식을 남기는 이유: 파일만 지우면 "그 표는 애초에 없었다"로 읽히는데,
    사실은 **캡션은 찾았고 크롭이 틀린 것**이다. 다시 자를 대상 목록이 사라지면 안 된다.
    """
    hit = tot = 0
    for j in sorted(OUT_ROOT.glob("*/figures.json")):
        groups = dup_groups(j.parent)
        if not groups:
            continue
        try:
            m = json.loads(j.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            print(f"⛔ {j.parent.name}: figures.json 을 못 읽는다")
            continue
        idx = {r.get("file"): r for r in m.get("figures", [])}
        hit += 1
        for grp in groups:
            keep, dups = grp[0].name, [p.name for p in grp[1:]]
            tot += len(dups)
            kl = (idx.get(keep) or {}).get("label", "?")
            dl = ",".join((idx.get(d) or {}).get("label", "?") for d in dups)
            print(f"{'삭제' if apply_it else '삭제예정'} {j.parent.name}: "
                  f"{keep}(label {kl}) 유지 ← {', '.join(dups)} (label {dl})")
            if not apply_it:
                continue
            for d in dups:
                (j.parent / d).unlink(missing_ok=True)
                r = idx.get(d)
                if r is not None:
                    r["file"] = None
                    r["dup_of"] = keep
                    r["note"] = ((r.get("note") or "") + " | "
                                 f"크롭이 {keep} 와 바이트 동일 → 이 번호는 실제로 잘린 적이 "
                                 f"없다. 삭제하고 재추출 대상으로 남김.").strip(" |")
        if apply_it:
            j.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{'지웠다' if apply_it else '지울 것'}: 중복 {tot}장 / {hit}편"
          + ("" if apply_it else "  (실제 삭제는 --apply)"))
    return 0


def selftest():
    """dup_groups/dedupe 자체 점검 — **음성 경로 포함**.

    dup_groups 는 바이트만 보므로 진짜 PNG 가 필요 없다.  임시 폴더에 바이트를 써서 검사한다.
    이 selftest 가 못 하는 것: 추출 본체(캡션 탐지·영역 산정)는 PDF 가 있어야 하므로 여기서 안 본다.
    """
    import tempfile
    global OUT_ROOT
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        print(("  ⭕ " if cond else "  ⛔ ") + name)
        ok, fail = ok + bool(cond), fail + (not cond)

    # --- 파일이름 접두사 (2026-08-29 han2025 회귀: Scheme 1 이 Figure 1 을 덮어썼다)
    chk("양성: figure → fig_", _fname_prefix("figure") == "fig")
    chk("양성: table → tab_", _fname_prefix("table") == "tab")
    chk("양성: scheme → sch_", _fname_prefix("scheme") == "sch")
    chk("음성⑩: scheme 과 figure 의 접두사가 **다르다** (같으면 같은 번호끼리 덮어쓴다)",
        _fname_prefix("scheme") != _fname_prefix("figure"))
    chk("음성⑪: 모르는 kind 는 fig 로 떨어진다 (예외로 죽지 않는다)",
        _fname_prefix("plate") == "fig")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        # --- 양성: 같은 바이트 3장 → 한 묶음, 이름순 첫 장을 남긴다
        d1 = root / "paper_a"; d1.mkdir()
        for n in ("tab_S1.png", "tab_S2.png", "tab_S3.png"):
            (d1 / n).write_bytes(b"\x89PNG-same")
        g = dup_groups(d1)
        chk("양성: 동일 3장 → 묶음 1개", len(g) == 1)
        chk("양성: 묶음 크기 3", len(g[0]) == 3)
        chk("양성: 남길 것은 이름순 첫 장(tab_S1)", g[0][0].name == "tab_S1.png")

        # --- 양성: 자연순 — fig_9 가 fig_10 보다 앞 (사전순이면 뒤집힌다)
        d0 = root / "paper_nat"; d0.mkdir()
        for n in ("fig_9.png", "fig_10.png"):
            (d0 / n).write_bytes(b"\x89PNG-nat")
        chk("양성: 자연순 — fig_9 를 남긴다 (사전순이면 fig_10)",
            dup_groups(d0)[0][0].name == "fig_9.png")

        # --- 음성 ①: 서로 다른 바이트는 절대 묶이면 안 된다
        d2 = root / "paper_b"; d2.mkdir()
        (d2 / "fig_1.png").write_bytes(b"\x89PNG-aaa")
        (d2 / "fig_2.png").write_bytes(b"\x89PNG-bbb")
        chk("음성①: 다른 2장 → 묶음 0개", dup_groups(d2) == [])

        # --- 음성 ②: 1바이트만 달라도 안 묶인다 (문서화된 한계 — 근사해시 안 씀)
        d3 = root / "paper_c"; d3.mkdir()
        (d3 / "fig_1.png").write_bytes(b"\x89PNG-same")
        (d3 / "fig_2.png").write_bytes(b"\x89PNG-samf")
        chk("음성②: 1바이트 차 → 안 묶인다 (한계를 고정)", dup_groups(d3) == [])

        # --- 음성 ③: 1장뿐 / 빈 폴더
        d4 = root / "paper_d"; d4.mkdir()
        (d4 / "fig_1.png").write_bytes(b"\x89PNG-solo")
        chk("음성③: 1장뿐 → 묶음 0개", dup_groups(d4) == [])
        d5 = root / "paper_e"; d5.mkdir()
        chk("음성③: 빈 폴더 → 묶음 0개", dup_groups(d5) == [])

        # --- dedupe: --apply 없이는 아무것도 지우면 안 된다 (음성 ④)
        for d in (d1, d2, d3, d4):
            (d / "figures.json").write_text(json.dumps({
                "slug": d.name,
                "figures": [{"key": p.stem, "kind": "table", "label": p.stem.split("_")[-1],
                             "file": p.name} for p in sorted(d.glob("*.png"))]},
                ensure_ascii=False), encoding="utf-8")
        keep_root, OUT_ROOT = OUT_ROOT, root
        try:
            dedupe(apply_it=False)
            chk("음성④: --apply 없으면 파일이 그대로", len(list(d1.glob("*.png"))) == 3)
            dedupe(apply_it=True)
            chk("양성: --apply 로 2장 삭제", sorted(p.name for p in d1.glob("*.png")) == ["tab_S1.png"])
            chk("음성⑤: 중복 없던 폴더는 안 건드림", len(list(d2.glob("*.png"))) == 2)
            m = json.loads((d1 / "figures.json").read_text(encoding="utf-8"))
            marks = [r for r in m["figures"] if r.get("dup_of") == "tab_S1.png"]
            chk("양성: figures.json 에 dup_of 표식 2개", len(marks) == 2)
            chk("양성: 지운 항목의 file 은 None (기록은 남는다)",
                all(r["file"] is None for r in marks))
            chk("양성: 남긴 항목은 표식이 없다",
                [r for r in m["figures"] if r["file"] == "tab_S1.png"][0].get("dup_of") is None)
        finally:
            OUT_ROOT = keep_root

        # --- --slides 모드 (덱): 백지 슬라이드도 **버리지 않는다** (2026-08-25 codex E)
        #     옛 판은 여기서 "1장만 남는다" 를 검사했다 — 그건 **버리던 시절의 계약**이다.
        #     계약이 바뀌면 그 계약을 주장하던 테스트도 같이 고쳐야 한다.
        deck = root / "deck.pdf"
        d = fitz.open()
        p1 = d.new_page(width=720, height=540)          # 내용 있는 슬라이드
        p1.insert_text((60, 90), "Design variables D50 Dseed", fontsize=28)
        p1.draw_rect(fitz.Rect(60, 140, 660, 480), fill=(0.2, 0.4, 0.9))
        d.new_page(width=720, height=540)               # 백지 간지 (음성 경로)
        d.save(deck); d.close()
        keep_root, OUT_ROOT = OUT_ROOT, root
        try:
            m, sk = extract_slides(str(deck), "deck_test", dpi=72, maxpx=900, relto=root)
            chk("양성(--slides): 슬롯 2개가 **전부** 남는다 (백지도 버리지 않는다)",
                len(m["figures"]) == 2)
            _blank = [f for f in m["figures"]
                      if f.get("content_status") == "blank_candidate"]
            chk("양성(--slides): 백지는 blank_candidate 로 **표시**된다 (삭제 아님)",
                len(_blank) == 1 and _blank[0]["artifact_retained"] is True)
            chk("음성⑧(--slides): 백지 후보는 digest 에서만 빠진다 (행·PNG 는 남는다)",
                _blank[0]["digest_included"] is False)
            chk("음성⑨(--slides): 자동 분류는 **확정이 아니다** (reviewed=False)",
                _blank[0]["reviewed"] is False
                and _blank[0]["content_status"] != "blank_confirmed")
            chk("양성(--slides): 라벨=쪽번호, 파일명 fig_1.png",
                m["figures"][0]["label"] == "1" and m["figures"][0]["file"] == "fig_1.png")
            chk("양성(--slides): 캡션에 슬라이드 텍스트가 들어간다",
                "D50" in m["figures"][0]["caption"])
            chk("양성(--slides): mode 표시가 남는다", m.get("mode") == "slides")
            chk("음성⑥(--slides): 백지는 '보존됨, 검토 대기' 로 사유가 남는다",
                len(sk) == 1 and "검토 대기" in sk[0][2])
            chk("음성⑦(--slides): PNG 는 **2장 다** 쓰인다 (사람이 열어봐야 하므로)",
                len(list((root / "deck_test").glob("*.png"))) == 2)
        finally:
            OUT_ROOT = keep_root

    print(f"\nselftest: {ok} 통과 / {fail} 실패")
    return 1 if fail else 0


def audit():
    """이미 잘라둔 것 전체 점검 — 53편을 눈으로 다 볼 수는 없으니 **의심스러운 것만** 띄운다.

    잡아내는 것
      · 그림 0개                     → 캡션 형식이 특이하거나 스캔 PDF
      · 번호 구멍 (Fig 1,2,4 …)      → 그 번호를 놓쳤다 (전면 그림·캡션 아래 배치 등)
      · 본문 없이 SI 만              → SI 오분류(원소기호 Si 등) 또는 본문 PDF 누락
      · 거의 백지 (그림만, blank ≥ 0.965) → 영역을 잘못 잡았다 (표는 원래 흰 바탕이라 제외)
      · 극단 세로비 (h/w ≥ 4.5)      → 두 그림을 한 장에 물었을 수 있다
      · 중복 크롭 (바이트 동일)      → 그 번호 중 하나는 안 잘렸다 (`--dedupe` 로 정리)
    """
    rows, warn = [], 0
    for j in sorted(OUT_ROOT.glob("*/figures.json")):
        try:
            m = json.loads(j.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            print(f"⛔ {j.parent.name}: figures.json 을 못 읽는다")
            warn += 1
            continue
        figs = m.get("figures", [])
        slug = m.get("slug", j.parent.name)
        main = [r for r in figs if r["kind"] != "table" and not r["label"].startswith("S")]
        si = [r for r in figs if r["kind"] != "table" and r["label"].startswith("S")]
        tab = [r for r in figs if r["kind"] == "table"]
        flags = []
        if not figs:
            flags.append("그림 0개 — 캡션을 못 찾음 (원고형 PDF: 캡션이 뒤쪽 "
                         "'Figure captions' 절에 몰려 있거나 / OCR 이 심하게 깨졌거나)")
        if not main and si:
            flags.append(f"본문 없이 SI {len(si)}장뿐")

        def gaps(lst, pre=""):
            ns = sorted(int(re.sub(r"\D", "", r["label"]) or 0) for r in lst)
            if not ns:
                return []
            return [f"{pre}{k}" for k in range(1, max(ns)) if k not in ns]
        g = gaps(main) + gaps(si, "S")
        if g:
            flags.append("번호 구멍 " + ",".join(g[:6]) + ("…" if len(g) > 6 else ""))
        # ⚠ '거의 백지' 검사는 뺐다 (2026-08-06 실물 확인): 추출 단계가 이미 blank > 0.985 를
        #   버리므로, audit 이 0.965 로 잡던 건 **성긴 선그래프뿐**이었다 — 실제로 열어 보니
        #   liu2013 f4(3점 직선)·fujimura2013 f2(아레니우스 산점도) 전부 정상 크롭.
        #   경보가 다 거짓이면 진짜를 가린다.
        tall = [r["key"] for r in figs if r["kind"] != "table"
                and r.get("w") and r["h"] / r["w"] >= 4.5]
        if tall:
            flags.append("극단 세로비 " + ",".join(tall[:4]))
        dg = dup_groups(j.parent)
        if dg:
            flags.append(f"중복 크롭 {sum(len(g) - 1 for g in dg)}장 "
                         + ",".join(g[0].name for g in dg[:3]) + " (--dedupe)")
        # 항목 둘이 **같은 파일**을 가리키는 경우 — 파일은 하나뿐이라 --dedupe 가 못 잡는다.
        # (webapp 은 그림을 두 번 그리고 파일명→키 사전에서는 하나가 지워진다)
        seen_f = {}
        for r in figs:
            if r.get("file"):
                seen_f.setdefault(r["file"], []).append(r.get("key"))
        shared = {f: ks for f, ks in seen_f.items() if len(ks) > 1}
        if shared:
            flags.append("한 파일을 여러 항목이 가리킴 "
                         + ",".join(f"{f}({'/'.join(map(str, ks))})"
                                    for f, ks in list(shared.items())[:2]))
        rows.append((slug, len(main), len(si), len(tab), flags))
        warn += bool(flags)

    print(f"=== 점검: {len(rows)}편 · 그림 "
          f"{sum(r[1] for r in rows)}(본문) + {sum(r[2] for r in rows)}(SI) + "
          f"{sum(r[3] for r in rows)}(표)\n")
    print(f"{'slug':<48} 본문  SI  표   확인할 것")
    for slug, nm, ns, nt, flags in rows:
        mark = "⚠" if flags else " "
        print(f"{mark} {slug[:46]:<46} {nm:>4} {ns:>3} {nt:>3}   {'; '.join(flags)}")
    ok = sum(1 for r in rows if not r[4])
    print(f"\n깨끗 {ok}편 / 확인 필요 {len(rows)-ok}편")
    print("※ '번호 구멍'은 대개 정상이다 — 전면 그림, 캡션이 그림 아래인 배치, PDF 에 그림이")
    print("  아예 안 들어간 쪽. 해당 논문만 --slug <slug> --clean 으로 다시 돌려 보고 판단한다.")
    return 0


def drop_blank(slug, apply_it=False):
    """사람이 **확정한** 백지 슬롯의 PNG 만 지운다 (2026-08-25 codex E 판정).

    규칙 — 이 셋이 이 함수의 존재 이유다:
      · 대상은 `content_status == "blank_confirmed"` 뿐이다. 자동 분류인
        `blank_candidate` 는 **절대 지우지 않는다** (unreviewed 삭제 금지).
      · manifest 행은 남긴다. 파일이 사라져도 슬롯이 있었다는 사실은 남아야 한다.
      · `--apply` 없이는 지우지 않는다 (이중 의도).

    ⛔ 이 함수가 못 하는 것: 백지인지 아닌지 **판단하지 않는다.** 사람이
      figures.json 에서 `blank_confirmed` + `reviewed:true` 로 바꿔 둔 것만 따른다.
    """
    if not slug:
        raise SystemExit("⛔ --drop-blank 는 slug 가 필요하다")
    d = OUT_ROOT / slug
    fj = d / "figures.json"
    if not fj.is_file():
        raise SystemExit(f"⛔ {fj} 가 없다")
    meta = json.loads(fj.read_text(encoding="utf-8"))
    figs = meta.get("figures", [])
    cand = [f for f in figs if f.get("content_status") == "blank_candidate"]
    conf = [f for f in figs if f.get("content_status") == "blank_confirmed"]
    unrev = [f for f in conf if not f.get("reviewed")]
    if unrev:
        raise SystemExit(
            f"⛔ blank_confirmed 인데 reviewed 가 아닌 슬롯 {len(unrev)}건 "
            f"({', '.join(f.get('slot_id', f.get('label', '?')) for f in unrev[:6])}) — "
            "사람이 열어본 표시 없이 확정만 바뀌었다. 삭제하지 않는다.")
    print(f"{slug}: 슬롯 {len(figs)} · 백지후보 {len(cand)}(검토대기, 대상 아님) "
          f"· 확정 {len(conf)}(삭제 대상)")
    if not conf:
        print("  삭제할 것 없음 — 확정은 사람만 한다 (figures.json 의 "
              "content_status 를 blank_confirmed 로, reviewed 를 true 로).")
        return 0
    n = 0
    for f in conf:
        p = d / f.get("file", "")
        if apply_it and p.is_file():
            p.unlink()
            n += 1
        f["artifact_retained"] = bool(not apply_it)
        f["digest_included"] = False
    if apply_it:
        fj.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  PNG {n}건 삭제 · manifest 행 {len(conf)}건은 그대로 남겼다")
    else:
        print(f"  (dry) --apply 를 붙이면 PNG {len(conf)}건을 지운다. 행은 남는다.")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="논문 PDF 에서 그림·표를 캡션 기준으로 잘라 wiki/raw/figures/<slug>/ 에 넣는다.")
    # nargs="+" 와 append 를 같이 — `--pdf a.pdf b.pdf` (글로브 `01.*.pdf`) 와
    # `--pdf a.pdf --pdf b.pdf` 둘 다 되게. 글로브가 2개를 잡으면 두 번째가
    # 위치인수로 새서 usage 오류가 났다 (2026-08-06 1저자 신고).
    ap.add_argument("--pdf", action="append", nargs="+", metavar="PDF",
                    help="본문 PDF. 여러 개면 그냥 이어 쓰거나 글로브 (SI 는 파일명에 sup/SI 가 있으면 S 번호로)")
    ap.add_argument("--slug", help="wiki/raw/papers/<slug>.md 의 slug")
    ap.add_argument("--inbox", action="store_true",
                    help="wiki/inbox/ 를 훑어 digest 와 자동 매칭 (기본은 매칭표만, --run 이면 실행)")
    ap.add_argument("--run", action="store_true", help="--inbox 에서 실제로 추출까지")
    ap.add_argument("--inbox_dir", default="", help="inbox 위치를 바꿔서 (기본 wiki/inbox)")
    ap.add_argument("--only", default="", help="--inbox 에서 slug 에 이 문자열이 든 것만")
    ap.add_argument("--skip-done", action="store_true",
                    help="--inbox 에서 이미 figures.json 이 있는 논문은 건너뛴다")
    # ⚠ 기본값을 None 으로 두고 아래에서 모드별로 푼다 — 덱(--slides)은 **쪽 통째로** 렌더라
    #   같은 3000 px 를 쓰면 21장에 11 MB 가 된다(2026-08-25 실측). repo 에 커밋하는 파일이므로
    #   덱 기본은 1600 px. 사용자가 명시하면 그 값이 이긴다.
    ap.add_argument("--dpi", type=int, default=None, help="기본: 논문 300 · 덱(--slides) 150")
    ap.add_argument("--maxpx", type=int, default=None,
                    help="긴 변 픽셀 상한. 0 이면 --dpi 그대로. 기본: 논문 3000 · 덱(--slides) 1600")
    ap.add_argument("--dry", action="store_true", help="파일 안 쓰고 표만 출력")
    ap.add_argument("--clean", action="store_true", help="기존 <slug> 폴더를 지우고 새로")
    ap.add_argument("--audit-src", dest="audit_src", action="store_true",
                    help="남의 논문 그림이 섞였는지 점검 (그림의 src ↔ 논문 제목 대조)")
    ap.add_argument("--audit", action="store_true",
                    help="이미 잘라둔 것 전체 점검 (구멍·백지·SI만 등 의심스러운 것만)")
    ap.add_argument("--dedupe", action="store_true",
                    help="바이트 동일 중복 크롭을 정리 (기본 미리보기, --apply 로 실제 삭제)")
    ap.add_argument("--selftest", action="store_true",
                    help="자체 점검 (양성 + 음성 경로)")
    ap.add_argument("--refresh", action="store_true",
                    help="추출기를 고친 뒤 **장수가 달라지는 논문만** 골라 재추출 (--apply 로 실행)")
    ap.add_argument("--apply", action="store_true", help="--refresh 에서 실제로 덮어쓴다")
    ap.add_argument("--suggest", action="store_true",
                    help="그림 없는 digest × 미매칭 PDF 후보표 (pdf_map.tsv 채우기용)")
    ap.add_argument("--why", action="store_true",
                    help="--slug 과 함께: 각 캡션이 왜 살았는지/버려졌는지 좌표째로")
    ap.add_argument("--slides", action="store_true",
                    help="발표 덱(PPT→PDF): 캡션이 없으므로 **슬라이드 1장 = 그림 1장**으로 렌더 "
                         "(wiki/raw/talks 용. --slug --pdf 와 함께)")
    ap.add_argument("--drop-blank", dest="drop_blank", action="store_true",
                    help="사람이 blank_confirmed 로 확정한 슬롯의 PNG 만 지운다. "
                         "manifest 행은 남는다. 실제 삭제에는 --apply 도 필요.")
    ap.add_argument("--nup", type=int, default=1,
                    help="한 쪽에 슬라이드 N 장인 인쇄 자료집을 나눈다 (심포지엄 자료집은 "
                         "대개 2). 라벨이 <쪽>a/<쪽>b 가 된다. --slides 와 함께.")
    a = ap.parse_args()
    if a.pdf:                       # [[a,b],[c]] → [a,b,c]
        a.pdf = [x for grp in a.pdf for x in grp]
    if a.dpi is None:               # 모드별 기본값 (위 주석 참고)
        a.dpi = 150 if a.slides else 300
    if a.maxpx is None:
        a.maxpx = 1600 if a.slides else 3000

    if a.selftest:
        return selftest()

    if a.audit_src:
        return audit_src()

    if a.audit:
        return audit()

    if a.dedupe:
        return dedupe(apply_it=a.apply)

    if a.drop_blank:
        return drop_blank(a.slug, apply_it=a.apply)

    if a.refresh:
        box = Path(a.inbox_dir).expanduser() if a.inbox_dir else INBOX
        if not box.is_dir():
            raise SystemExit(f"⛔ {box} 가 없다 — --inbox_dir 로 지정")
        return refresh(box, apply_it=a.apply, dpi=a.dpi, maxpx=a.maxpx)

    if a.suggest:
        box = Path(a.inbox_dir).expanduser() if a.inbox_dir else INBOX
        if not box.is_dir():
            raise SystemExit(f"⛔ {box} 가 없다 — --inbox_dir 로 지정")
        return suggest(box)

    if a.inbox:
        box = Path(a.inbox_dir).expanduser() if a.inbox_dir else INBOX
        if not box.is_dir():
            # wiki/inbox/ 는 .gitignore 대상이라 clone 한 머신에는 없다 (2026-08-06 실측).
            # PDF 가 있을 만한 곳을 뒤져 후보를 알려준다 — WSL 이면 보통 윈도 Downloads.
            cands, seen = [], set()
            for base in [Path.home(), Path("/mnt/c/Users"), Path("/mnt/d")]:
                if not base.is_dir():
                    continue
                try:
                    for f in base.glob("*/[Dd]ownload*/*.pdf"):
                        if f.parent not in seen:
                            seen.add(f.parent); cands.append(f.parent)
                    for f in base.glob("*/*.pdf"):
                        if f.parent not in seen:
                            seen.add(f.parent); cands.append(f.parent)
                except (PermissionError, OSError):
                    pass
            msg = [f"⛔ {box} 가 없다.",
                   "   wiki/inbox/ 는 .gitignore 대상이라 clone 한 머신에는 안 따라온다.",
                   "   ① PDF 를 거기에 모으거나  ② --inbox_dir 로 있는 곳을 가리킨다:",
                   "        litfig --inbox --inbox_dir '/mnt/c/Users/<계정>/Downloads'"]
            if cands:
                msg.append("\n   PDF 가 보이는 폴더 (개수순):")
                for d in sorted(cands, key=lambda p: -len(list(p.glob('*.pdf'))))[:8]:
                    msg.append(f"      {len(list(d.glob('*.pdf'))):>4}개  {d}")
            raise SystemExit("\n".join(msg))
        assign, orphan = match_inbox(box)
        if a.only:
            assign = {k: v for k, v in assign.items() if a.only.lower() in k.lower()}
        if a.skip_done:
            assign = {k: v for k, v in assign.items()
                      if not (OUT_ROOT / k / "figures.json").exists()}
        print(f"=== inbox 매칭: 논문 {len(assign)}편 / 짝 못 찾은 PDF {len(orphan)}개\n")
        for slug, v in sorted(assign.items()):
            warn = "  ⚠ 본문 후보 2개 이상 — 표를 보고 아닌 건 --pdf 로 따로 돌린다" \
                   if len(v["main"]) > 1 else ""
            print(f"  {slug}  [{v['why']}]{warn}")
            for p in v["main"]:
                print(f"      본문 {_show(p, box)}")
            for p in v["si"]:
                print(f"      SI   {_show(p, box)}")
        if orphan:
            print("\n--- 짝 못 찾음 (digest 가 없거나 제목이 많이 다른 것)")
            for p, si in orphan[:30]:
                print(f"  {'SI ' if si else '본문'} {_show(p, box)}")
            if len(orphan) > 30:
                print(f"  … 외 {len(orphan)-30}개")
        if not a.run:
            print("\n※ 매칭표만 냈다. 실제로 자르려면 뒤에 --run 을 붙인다:")
            print("     python3 wiki/tools/extract_figures.py --inbox --run")
            return 0
        print()
        for i, (slug, v) in enumerate(sorted(assign.items()), 1):
            pdfs = [str(p) for p in v["main"] + v["si"]]
            print(f"[{i}/{len(assign)}] {slug}")
            shutil.rmtree(OUT_ROOT / slug, ignore_errors=True)
            try:
                meta, skipped = extract(pdfs, slug, dpi=a.dpi, maxpx=a.maxpx, relto=box)
            except Exception as e:                 # 한 편이 깨져도 나머지는 계속
                print(f"   ⛔ 실패: {type(e).__name__}: {e}\n")
                continue
            _report(slug, meta, skipped, dry=False)
            print()
        _write_sources_index()
        return 0

    if a.slug and not a.pdf:
        # 에이전트가 경로를 안 찾아도 되게: slug 만 주면 스스로 찾는다.
        #   wiki/inbox/ → 채팅 업로드 폴더 순으로, 먼저 걸리는 곳에서 쓴다.
        roots = pdf_roots(a.inbox_dir)
        near = []
        for box in roots:
            found, _o = match_inbox(box)
            v = found.get(a.slug)
            if v:
                a.pdf = [str(q) for q in v["main"] + v["si"]]
                print(f"※ PDF 자동 탐색 성공 [{v['why']}] — {box}")
                for q in v["main"] + v["si"]:
                    print(f"   {_show(q, box)}")
                break
            near += [k for k in found if a.slug.split("_")[0] in k]
        if not a.pdf:
            raise SystemExit(
                f"⛔ '{a.slug}' 의 PDF 를 못 찾았다. 뒤진 곳:\n"
                + "".join(f"     {d}\n" for d in roots)
                + "   --pdf 로 직접 주거나, 어디에 있는지 --inbox --inbox_dir <폴더> 로 확인한다.\n"
                + (f"   비슷한 slug: {', '.join(sorted(set(near))[:3])}\n" if near else ""))

    if not a.pdf or not a.slug:
        raise SystemExit(
            "⛔ --pdf 와 --slug 가 둘 다 필요하다 (또는 --inbox 로 자동 매칭).\n"
            "   ⚠ <slug> 는 자리표시자다 — wiki/raw/papers/ 의 실제 파일 이름을 넣는다. 예:\n"
            "     python3 wiki/tools/extract_figures.py --inbox            # 뭐가 뭔지 먼저 보기\n"
            "     python3 wiki/tools/extract_figures.py --inbox --run      # 전부 자르기\n"
            "     python3 wiki/tools/extract_figures.py --clean \\\n"
            "         --slug kraft2017_lattice_polarizability_argyrodite_Li6PS5X \\\n"
            "         --pdf 'wiki/inbox/31. Influence of Lattice Polarizability….pdf'")
    for p in a.pdf:
        if not Path(p).exists():
            raise SystemExit(f"⛔ PDF 없음: {p}")
    if a.clean and not a.dry:
        shutil.rmtree(OUT_ROOT / a.slug, ignore_errors=True)

    if a.why:
        return why(a.slug, a.pdf)

    if a.slides:
        if len(a.pdf) > 1:
            raise SystemExit("⛔ --slides 는 덱 1개만 받는다 (덱마다 슬라이드 번호가 다르다).")
        meta, skipped = extract_slides(a.pdf[0], a.slug, dpi=a.dpi,
                                       dry=a.dry, maxpx=a.maxpx, nup=a.nup)
        _report(a.slug, meta, skipped, a.dry)
        if not a.dry:
            _write_sources_index()
        return 0

    meta, skipped = extract(a.pdf, a.slug, dpi=a.dpi, dry=a.dry, maxpx=a.maxpx)
    _report(a.slug, meta, skipped, a.dry)
    if not a.dry:
        # ⚠ --inbox --run 경로만 이걸 부르고 있었다 — 논문 하나를 --slug/--pdf 로 자르면
        #   wiki/raw/figures/_sources.json 이 그 논문만 빠진 채 낡는다 (2026-08-05 발견).
        #   웹앱 배지는 figures.json 을 직접 읽어 영향 없지만, 출처 색인은 어긋난다.
        _write_sources_index()
    return 0


if __name__ == "__main__":
    sys.exit(main())
