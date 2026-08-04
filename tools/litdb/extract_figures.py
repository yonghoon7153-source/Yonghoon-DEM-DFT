#!/usr/bin/env python3
"""extract_figures.py — 논문 PDF 에서 **그림/표를 캡션 기준으로 잘라** litdb 에 등록.

1저자 요청(2026-08-06): "논문 에이전트도 figure 크로핑해서 저장해두면 보기 좋지 않나."
digest(`litdb/papers/<slug>.md`) 본문에 `Fig. 5e` 같은 언급이 나오면 webapp 이 그 그림을
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
  python3 tools/litdb/extract_figures.py --inbox           # 어느 PDF ↔ 어느 논문인지 표만
  python3 tools/litdb/extract_figures.py --inbox --run     # 실제로 자르기

한 편만 콕 집을 때 (⚠ <slug> 는 자리표시자다 — litdb/papers/ 의 실제 파일 이름을 넣는다)
  python3 tools/litdb/extract_figures.py --slug kraft2017_lattice_polarizability_argyrodite_Li6PS5X \\
      --pdf "litdb/inbox/31. ….pdf" --pdf "litdb/inbox/31. Sup) ….pdf" --clean

출력
  litdb/figures/<slug>/fig_<label>.png ...
  litdb/figures/<slug>/figures.json     ← webapp 이 읽는 색인
"""
import argparse
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
        "     ~/.venvs/litdb/bin/python3 tools/litdb/extract_figures.py --inbox\n"
        "   (자주 쓸 거면 ~/.bashrc 에)  alias litfig='~/.venvs/litdb/bin/python3 "
        "~/Yonghoon-DEM-DFT/tools/litdb/extract_figures.py'")

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "litdb" / "figures"

# ① 캡션 후보. 번호 뒤에 소문자가 바로 붙으면(2a) 본문 참조이므로 (?![a-z]) 로 막는다.
#   ⚠ "Supplementary Fig. 1." 처럼 접두어가 붙는 저널이 있다(실측: Zhou 2026 SI 는 이것 때문에
#     27쪽에서 0개가 나왔다). 접두어가 붙으면 번호에 S 가 없어도 SI 번호로 취급한다.
SI_PRE = r"(?:Supplementary|Supplemental|Supporting|Extended\s+Data|Extended|Online)\s+"
CAP_RE = re.compile(
    r"^\s*(?P<si>" + SI_PRE + r")?"
    r"(?P<kind>Fig(?:ure|\.)?|FIG(?:URE|\.)?|Table|TABLE|Scheme|SCHEME)\s*"
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
    kind = "table" if kw.startswith("table") else \
           ("scheme" if kw.startswith("scheme") else "figure")
    rest, sep = m.group("rest"), m.group("sep")
    if sep in ".|:,–—":              # "Figure 1." / "Figure 5 |" → 캡션 확정
        pass
    elif rest[:1].islower() or VERBS.match(rest):
        return None                            # "Figure 3 shows ..." → 본문
    if len(t) < 12:                            # "Figure 1" 만 있는 상호참조 조각
        return None
    return kind, m.group("label"), bool(m.group("si"))


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
    """이 쪽의 그래픽 bbox 들 — 배치 이미지 + 벡터 경로. (쪽당 1회만: get_drawings 가 느리다)"""
    ck = (id(page.parent), page.number)
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


def _side_rect(page, cap, blocks, up, margin=6.0):
    """캡션 기준 위(up=True)/아래 영역 → (rect, 이미지수, 벡터수).

    세로 경계는 "같은 단(column)에서 가장 가까운 다른 텍스트 블록" — 위에 다른 그림의
    캡션이 있으면 거기서 끊긴다. 그다음 그래픽 bbox 로 실제 범위까지 넓힌다
    (캡션보다 넓은 그림 / 삐져나온 축 라벨).
    """
    x0, y0, x1, y1 = cap[:4]
    band, pr = (x0, x1), page.rect
    if up:
        lim = pr.y0 + 24
        for b in blocks:
            if b[3] <= y0 + 1 and band_overlap(band, (b[0], b[2])) > 0.45:
                lim = max(lim, b[3])
        rect = fitz.Rect(x0, lim + 2, x1, y0 - 2)
    else:
        lim = pr.y1 - 24
        for b in blocks:
            if b[1] >= y1 - 1 and band_overlap(band, (b[0], b[2])) > 0.45:
                lim = min(lim, b[1])
        rect = fitz.Rect(x0, y1 + 2, x1, lim - 2)
    if rect.height < 36:
        return None, 0, 0
    hit = [(k, r) for k, r in graphics(page) if r.intersects(rect) and
           (r & rect).get_area() > 0.12 * r.get_area()]
    if hit:
        u = hit[0][1]
        for _k, r in hit[1:]:
            u |= r
        y_lo = max(min(rect.y0, u.y0) - margin, (lim + 2) if up else (y1 + 2))
        y_hi = min(max(rect.y1, u.y1) + margin, (y0 - 2) if up else (lim - 2))
        rect = fitz.Rect(min(rect.x0, u.x0) - margin, y_lo,
                         max(rect.x1, u.x1) + margin, y_hi) & pr
    ks = [k for k, _r in hit]
    return (rect if rect.height >= 36 else None), ks.count("img"), ks.count("draw")


def region_for(page, cap, kind, blocks, tables=(), min_draw=6, stop_y=1e9):
    """캡션 블록 → (잘라낼 사각형, 이미지수, 벡터수).

    figure/scheme 는 캡션 **위**가 기본. ⚠ SI 는 캡션을 그림 **위**에 두는 쪽이 많다
    (실측: Zhou 2026 SI 의 Fig S1/S2/S12 는 캡션이 쪽 맨 위 y=76 이고 그림이 그 아래).
    위가 비면 아래로 한 번 더 본다 — 표는 처음부터 아래.
    """
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


def _shrink(path):
    """PNG 재압축 — 선화(line art)는 팔레트로 줄이면 60~80% 작아진다. PIL 없으면 그냥 둔다."""
    try:
        from PIL import Image
    except Exception:
        return
    try:
        im = Image.open(path).convert("RGB")
        q = im.quantize(colors=256, method=Image.MEDIANCUT)
        # 팔레트로 바꿔 오차가 큰 사진류는 원본 유지 (구조 그림·그래프만 이득)
        if len(im.getcolors(maxcolors=4096) or []) > 3500:
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
        doc = fitz.open(pdf_path)
        si = bool(re.search(r"\bsup|\bsi\b|supporting|supplement", Path(pdf_path).name, re.I))
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
                fn = f"{'tab' if kind == 'table' else 'fig'}_{label.upper()}.png"
                rec = {"key": key, "kind": kind, "label": label.upper(), "page": pno + 1,
                       "file": fn, "caption": caption[:900],
                       "bbox": [round(v, 1) for v in rect],
                       "w": pix.width, "h": pix.height, "px": pix.width * pix.height, "dpi": d_eff,
                       "src": Path(pdf_path).name, "blank": round(br, 3)}
                seen[key] = rec
                found.append(rec)
                if not dry:
                    out_dir.mkdir(parents=True, exist_ok=True)
                    pix.save(out_dir / fn)
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
            # ⚠ 원본 PDF 는 repo 에 없다(litdb/inbox 는 .gitignore). 그래서 **어느 하위 폴더의
            #   어느 파일**이었는지를 남긴다 — 다른 머신에서도 --inbox_dir 만 맞추면 다시 찾는다.
            "sources": [_relto(p, relto) for p in pdf_paths],
            "figures": found}
    if not dry:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "figures.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta, skipped


# ── inbox 자동 매칭 ─────────────────────────────────────────────────────
#   1저자가 `--slug <slug>` 를 그대로 붙여넣어 bash 오류를 냈다(2026-08-06).
#   자리표시자를 직접 채우게 하지 말고, inbox 를 훑어 digest 와 자동으로 짝지어 준다.
INBOX = ROOT / "litdb" / "inbox"
PAPERS = ROOT / "litdb" / "papers"


def pdf_roots(inbox_dir=""):
    """PDF 를 찾을 곳들 (순서대로).

    ⚠ 왜 업로드 폴더까지 (2026-08-06 1저자 요청 "논문 에이전트 먹이면 자동으로"):
      채팅에 올린 PDF 는 litdb/inbox/ 가 아니라 Claude Code 업로드 폴더에 떨어진다.
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
    for p in sorted(inbox.rglob("*.pdf")):
        if any(d.startswith((".", "~$")) or d in ("$RECYCLE.BIN", "node_modules")
               for d in p.relative_to(inbox).parts[:-1]):
            continue
        name = p.stem
        num = int(m.group(1)) if (m := re.match(r"\s*(\d+)\s*[.)]", name)) else None
        si = bool(SI_TAG.search(name))
        slug, why = None, ""
        if num is not None and num in bynum:
            slug, why = bynum[num], f"inbox #{num}"
        else:
            ft = _toks(re.sub(r"^\s*\d+\s*[.)]\s*", "", name))
            need = min(min_hits, len(ft))
            best, bs = None, 0.0
            for s, (tt, _n) in papers.items():
                sc, hit = score(ft, tt)
                if len(hit) < need or sc <= bs:
                    continue
                # 토큰이 min_hits 에 못 미치면(ECERD2600097 처럼 짧은 파일명) **희소한**
                # 토큰이 맞았을 때만 인정한다 — 흔한 `batteries` 하나로는 안 된다.
                if len(hit) < min_hits and not any(df.get(t, 0) <= rare for t in hit):
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
        print(f"│  Read litdb/figures/{slug}/{r['file']}   ({cap}…)")
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
        print(f"→ litdb/figures/{slug}/  (figures.json 포함)")
        _read_plan(slug, meta)


def _write_sources_index():
    """slug → 원본 PDF (inbox 상대경로) 한눈 색인.

    PDF 본체는 repo 에 없으므로(저작권·용량), **어디서 왔는지**만이라도 추적 가능하게 둔다.
    figures.json 마다 들어 있는 sources 를 모아 litdb/figures/_sources.json 로 쓴다.
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
        print(f"→ litdb/figures/_sources.json  ({len(idx)}편: 어느 PDF 에서 왔는지 색인)")


def audit():
    """이미 잘라둔 것 전체 점검 — 53편을 눈으로 다 볼 수는 없으니 **의심스러운 것만** 띄운다.

    잡아내는 것
      · 그림 0개                     → 캡션 형식이 특이하거나 스캔 PDF
      · 번호 구멍 (Fig 1,2,4 …)      → 그 번호를 놓쳤다 (전면 그림·캡션 아래 배치 등)
      · 본문 없이 SI 만              → SI 오분류(원소기호 Si 등) 또는 본문 PDF 누락
      · 거의 백지 (그림만, blank ≥ 0.965) → 영역을 잘못 잡았다 (표는 원래 흰 바탕이라 제외)
      · 극단 세로비 (h/w ≥ 4.5)      → 두 그림을 한 장에 물었을 수 있다
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
            flags.append("그림 0개")
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
        # ⚠ 표는 흰 바탕에 글자라 원래 blank 가 높다 — 그림만 본다
        blank = [r["key"] for r in figs
                 if r["kind"] != "table" and r.get("blank", 0) >= 0.965]
        if blank:
            flags.append("거의 백지 " + ",".join(blank[:4]))
        tall = [r["key"] for r in figs if r["kind"] != "table"
                and r.get("w") and r["h"] / r["w"] >= 4.5]
        if tall:
            flags.append("극단 세로비 " + ",".join(tall[:4]))
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


def main():
    ap = argparse.ArgumentParser(
        description="논문 PDF 에서 그림·표를 캡션 기준으로 잘라 litdb/figures/<slug>/ 에 넣는다.")
    ap.add_argument("--pdf", action="append",
                    help="본문 PDF. SI 도 있으면 --pdf 를 한 번 더 (파일명에 sup/SI 가 있으면 S 번호로)")
    ap.add_argument("--slug", help="litdb/papers/<slug>.md 의 slug")
    ap.add_argument("--inbox", action="store_true",
                    help="litdb/inbox/ 를 훑어 digest 와 자동 매칭 (기본은 매칭표만, --run 이면 실행)")
    ap.add_argument("--run", action="store_true", help="--inbox 에서 실제로 추출까지")
    ap.add_argument("--inbox_dir", default="", help="inbox 위치를 바꿔서 (기본 litdb/inbox)")
    ap.add_argument("--only", default="", help="--inbox 에서 slug 에 이 문자열이 든 것만")
    ap.add_argument("--skip-done", action="store_true",
                    help="--inbox 에서 이미 figures.json 이 있는 논문은 건너뛴다")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--maxpx", type=int, default=3000,
                    help="긴 변 픽셀 상한. 0 이면 --dpi 그대로")
    ap.add_argument("--dry", action="store_true", help="파일 안 쓰고 표만 출력")
    ap.add_argument("--clean", action="store_true", help="기존 <slug> 폴더를 지우고 새로")
    ap.add_argument("--audit", action="store_true",
                    help="이미 잘라둔 것 전체 점검 (구멍·백지·SI만 등 의심스러운 것만)")
    a = ap.parse_args()

    if a.audit:
        return audit()

    if a.inbox:
        box = Path(a.inbox_dir).expanduser() if a.inbox_dir else INBOX
        if not box.is_dir():
            # litdb/inbox/ 는 .gitignore 대상이라 clone 한 머신에는 없다 (2026-08-06 실측).
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
                   "   litdb/inbox/ 는 .gitignore 대상이라 clone 한 머신에는 안 따라온다.",
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
            print("     python3 tools/litdb/extract_figures.py --inbox --run")
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
        #   litdb/inbox/ → 채팅 업로드 폴더 순으로, 먼저 걸리는 곳에서 쓴다.
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
            "   ⚠ <slug> 는 자리표시자다 — litdb/papers/ 의 실제 파일 이름을 넣는다. 예:\n"
            "     python3 tools/litdb/extract_figures.py --inbox            # 뭐가 뭔지 먼저 보기\n"
            "     python3 tools/litdb/extract_figures.py --inbox --run      # 전부 자르기\n"
            "     python3 tools/litdb/extract_figures.py --clean \\\n"
            "         --slug kraft2017_lattice_polarizability_argyrodite_Li6PS5X \\\n"
            "         --pdf 'litdb/inbox/31. Influence of Lattice Polarizability….pdf'")
    for p in a.pdf:
        if not Path(p).exists():
            raise SystemExit(f"⛔ PDF 없음: {p}")
    if a.clean and not a.dry:
        shutil.rmtree(OUT_ROOT / a.slug, ignore_errors=True)

    meta, skipped = extract(a.pdf, a.slug, dpi=a.dpi, dry=a.dry, maxpx=a.maxpx)
    _report(a.slug, meta, skipped, a.dry)
    return 0


if __name__ == "__main__":
    sys.exit(main())
