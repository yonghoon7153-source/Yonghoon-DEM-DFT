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

usage
  python3 tools/litdb/extract_figures.py --pdf <file.pdf> --slug <litdb slug>
  python3 tools/litdb/extract_figures.py --pdf <file.pdf> --slug <slug> --dry   # 안 쓰고 표만
  python3 tools/litdb/extract_figures.py --pdf a.pdf --pdf b.pdf --slug <slug>  # 본문+SI 합치기

출력
  litdb/figures/<slug>/fig_<label>.png ...
  litdb/figures/<slug>/figures.json     ← webapp 이 읽는 색인
"""
import argparse
import json
import re
import shutil
import sys
import time
from pathlib import Path

import fitz                                    # PyMuPDF

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


def table_rect(page, cap, tables, margin=5.0):
    """표는 **본문과 같은 텍스트**라 '그래픽 검증'이 안 통한다 → PyMuPDF 표 검출을 쓴다.

    ⚠ 캡션 블록이 표 앞부분을 통째로 삼키는 쪽이 있다(실측: Hargreaves SI p21 에서
      캡션 bbox 가 첫 표를 덮었다). 그래서 "캡션 **아래**"가 아니라 "캡션 시작선 이후"에
      걸리는 표를 전부 합집합한다 — 한 캡션이 이어진 두 조각을 거느리는 경우까지 잡힌다.
    """
    x0, y0, x1, y1 = cap[:4]
    hit = [fitz.Rect(t) for t in tables]
    hit = [t for t in hit if t.y1 > y0 + 2 and band_overlap((x0, x1), (t.x0, t.x1)) > 0.30]
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


def region_for(page, cap, kind, blocks, tables=(), min_draw=6):
    """캡션 블록 → (잘라낼 사각형, 이미지수, 벡터수).

    figure/scheme 는 캡션 **위**가 기본. ⚠ SI 는 캡션을 그림 **위**에 두는 쪽이 많다
    (실측: Zhou 2026 SI 의 Fig S1/S2/S12 는 캡션이 쪽 맨 위 y=76 이고 그림이 그 아래).
    위가 비면 아래로 한 번 더 본다 — 표는 처음부터 아래.
    """
    if kind == "table":
        r = table_rect(page, cap, tables)
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
            maxpx=1500):
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
                rect, n_img, n_draw = region_for(page, tuple(cr), kind, blocks, tabs,
                                                 min_draw=min_draw)
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
            "sources": [Path(p).name for p in pdf_paths],
            "figures": found}
    if not dry:
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "figures.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    return meta, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", action="append", required=True,
                    help="본문 PDF. SI 도 있으면 --pdf 를 한 번 더 (파일명에 sup/SI 가 있으면 S 번호로)")
    ap.add_argument("--slug", required=True, help="litdb/papers/<slug>.md 의 slug")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--maxpx", type=int, default=1500,
                    help="긴 변 픽셀 상한 (repo 용량 관리). 0 이면 --dpi 그대로")
    ap.add_argument("--dry", action="store_true", help="파일 안 쓰고 표만 출력")
    ap.add_argument("--clean", action="store_true", help="기존 <slug> 폴더를 지우고 새로")
    a = ap.parse_args()

    for p in a.pdf:
        if not Path(p).exists():
            raise SystemExit(f"⛔ PDF 없음: {p}")
    if a.clean and not a.dry:
        shutil.rmtree(OUT_ROOT / a.slug, ignore_errors=True)

    meta, skipped = extract(a.pdf, a.slug, dpi=a.dpi, dry=a.dry, maxpx=a.maxpx)
    print(f"=== {a.slug} — {len(meta['figures'])}개 추출"
          f"{' (dry-run, 안 씀)' if a.dry else ''}")
    print("key    p   크기         공백  캡션")
    for r in meta["figures"]:
        print(f"{r['key']:<6} {r['page']:<3} {r['w']}x{r['h']:<7} "
              f"{r['blank']:.2f}  {r['caption'][:64]}")
    if skipped:
        print(f"\n--- 제외 {len(skipped)}건 (오탐 방지)")
        for k, p, why in skipped[:18]:
            print(f"  {k:<6} p{p:<3} {why}")
    if not a.dry:
        print(f"\n→ litdb/figures/{a.slug}/  (figures.json 포함)")


if __name__ == "__main__":
    sys.exit(main())
