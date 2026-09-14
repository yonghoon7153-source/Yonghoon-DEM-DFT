"""
app.py — DFT 지식 인프라 Flask 앱.
설계: stoic-knuth webapp 인터페이스(사이드바 + CSS변수 테마 + 폴더모델)를
     흰색+한양네이비로 각색하고, 데이터소스를 db/*.json 으로 교체.
동기화: db 파일을 요청마다 읽으므로 계산 등록 즉시 사이트 반영.
"""
from flask import Flask, render_template, jsonify, send_from_directory, abort, request
import re
from markupsafe import Markup, escape
import json, os
from datetime import datetime as _dt
import data as D
import glossary as G
import artifact_policy as AP   # cascade artifact 노출 정책 (Codex Round-3 P0-3)

app = Flask(__name__)

# ─────────────────────────────────────────────────────────────
# 쓰기 API 잠금 (2026-08-07, Codex 코드리뷰 P1)
#
# 이 앱의 업로드·코멘트·이름변경·journal 기록은 **인증도 CSRF 보호도 없다.** 로컬
# WSL 에서 혼자 쓸 땐 그게 편했지만, render.yaml 은 `type: web` 이라 공개
# onrender.com 주소를 갖는다 — 아무나 POST 할 수 있었다. 실측으로 comment·journal·
# upload 가 토큰 없이 200 으로 성공했다.
#
# ⚠ 게다가 Render 기본 파일시스템은 재배포·재시작 때 사라진다(persistent disk 없음).
#   즉 원격에서 쓴 기록은 보안 문제와 별개로 **어차피 유실된다.** 그래서 기본값은
#   "원격 = 읽기 전용" 이 맞다.
#
#   ⚠ 2026-08-16 — 위 의도는 "**원격**이 읽기 전용" 이었는데 구현이
#     `READ_ONLY = not ALLOW_MUTATIONS` 라 **로컬까지 잠갔다.** 그래서 자기 노트북에서
#     그림에 코멘트를 달려 해도 "읽기 전용" 이라고 막혔다. 로컬 기본 바인딩은
#     127.0.0.1 이라 "아무나 POST" 가 성립하지 않는다 — 위험은 공개 주소를 갖는
#     Render 쪽에만 있다. 기본값을 의도대로 되돌린다:
#
#       Render (RENDER 환경변수 있음)  →  기본 **잠금**.  ALLOW_MUTATIONS=1 로만 해제
#       로컬                            →  기본 **열림**.  ALLOW_MUTATIONS=0 으로 잠글 수 있음
#
#     즉 env 를 **안 주면 환경이 정한다**. 명시하면 그게 이긴다 (양방향).
# ─────────────────────────────────────────────────────────────
_ON_RENDER = bool(os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"))
_MUT_ENV = os.environ.get("ALLOW_MUTATIONS", "").strip().lower()
if _MUT_ENV in ("1", "true", "yes"):
    ALLOW_MUTATIONS = True                 # 명시적 허용 — Render 에서도 이게 이긴다
elif _MUT_ENV in ("0", "false", "no"):
    ALLOW_MUTATIONS = False                # 명시적 잠금 — 로컬에서도 잠근다
else:
    ALLOW_MUTATIONS = not _ON_RENDER       # 미지정: 로컬은 열고 원격은 잠근다
READ_ONLY = not ALLOW_MUTATIONS


def _guard_mutation():
    """쓰기 라우트 앞에 건다. 잠겨 있으면 403 과 **켜는 방법**을 같이 준다."""
    if not READ_ONLY:
        return None
    return jsonify({
        "error": "읽기 전용 모드예요 — 이 서버에서는 저장이 꺼져 있어요.",
        "why": ("공개 배포에는 인증이 없고, Render 기본 파일시스템은 재시작 때 초기화돼서 "
                "어차피 기록이 남지 않아요."),
        "how": ("로컬이면 ALLOW_MUTATIONS 를 지우고(또는 =1) 다시 띄우면 열려요. "
                "원격(Render)은 인증이 없어서 일부러 잠가 둡니다."),
        "on_render": _ON_RENDER,
    }), 403


@app.after_request
def _sec_headers(resp):
    # 저장형 XSS 방어를 파서 하나에만 기대지 않는다 (리뷰 P2).
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    return resp

# ⚠ 입문/설명 본문에 **굵게**·`코드` 를 쓰는데 템플릿이 그대로 찍어서 별표가 노출됐다.
#   전체 마크다운 파서를 붙일 자리가 아니므로 **굵게·코드·이스케이프만** 처리한다.
#   ⚠ escape 를 먼저 해야 XSS 가 안 생긴다 (본문은 우리가 쓰지만 규율은 지킨다).
#   ⚠ `.+?` 는 개행을 안 넘는다 — db JSON 의 긴 문장은 소스에서 줄이 접혀 있어서
#     `**` 가 줄바꿈을 넘는 순간 그대로 노출된다. re.S 를 걸어 블록 전체를 본다
#     (md_to_html 의 문단 병합과 같은 이유. 2026-08-07).
#   ⚠⚠ 그런데 re.S 만 걸면 **데이터로 들어 있는 별표**가 짝을 훔쳐 간다 — 실측:
#     저널 55번 항목의 `globstar(**) 지원` 이 300자 뒤의 진짜 `**` 와 짝지어져
#     문장 한 덩어리가 통째로 굵어졌다. 그래서 두 가지 가드를 건다.
#       ① 코드 스팬을 **먼저** 빼돌린다 — `` `**` `` 안의 별표는 데이터다.
#       ② 굵게 구간은 여는 별표 뒤/닫는 별표 앞이 공백이 아니어야 하고(마크다운 규칙),
#          MAXB 자를 넘으면 짝짓기를 포기한다. 우리 문장의 강조는 한 절을 안 넘는다.
#       ③ 여는 별표 바로 뒤가 **닫는 문장부호**(`) ] , . ;` 등)면 강조가 아니다 —
#          `globstar(**)` 가 정확히 그 꼴이다. 강조는 항상 내용어로 시작한다.
#       ④ ⛔ 2026-09-09 (1저자 실사용 보고) — ②의 "여는 별표 뒤가 공백이면 안 된다" 가
#          **너무 좁았다.** 실측으로 안 먹은 것들:
#            `suggests** low multicollinearity**`   ← 여는 쪽만 띄었다
#            `** Li-S₄ sublattice volume + CSM**`   ← 여는 쪽만 띄었다
#          CommonMark 로는 둘 다 굵게가 아닌 게 맞다(left-flanking 규칙). 그런데 **여기는
#          메모장이지 문서 규격이 아니다** — 규칙보다 의도가 우선이다.
#          ⇒ 규칙을 **"양쪽 다 띄면 안 된다"** 로 바꾼다. 한쪽만 띈 것은 강조로 본다.
#            그러면 `10 ** 3 and 2 ** 4`(양쪽 다 띔)는 **여전히 안 걸린다** — ②의
#            원래 목적(문장 통째 굵어짐)이 지켜진다.
_MDL_MAXB = 300
#: ⚠ body 는 **순수 lazy** 여야 한다. 처음에 `(\S(?:.{0,N}?\S)?)` 로 썼다가
#:   `(?:…)?` 가 greedy 라 body 가 **첫 유효 닫힘에서 안 멈추고 늘어났다** —
#:   실측: `**힘**: 4.64 … **step` 이 첫 `**` 부터 **세 번째** `**` 까지 한 덩어리로
#:   잡혀 `힘**:` 가 화면에 남았다 (2026-09-09 전체시험에서 잡혔다).
#:   ⇒ 정규식은 옛것 그대로 두고 **판정만 콜백으로** 옮긴다.
_MDL_BOLD = re.compile(r"\*\*(?![)\]}>,.;:!?])(.{1,%d}?)\*\*" % _MDL_MAXB, re.S)


def _mdl_bold_sub(m):
    """양쪽이 **다** 띄어져 있으면 강조가 아니다 — 원문 그대로 돌려준다.

    ⚠ 안쪽 공백은 **지우지 않고 태그 밖으로 내보낸다.** 지우면
    `suggests** low x**` 가 `suggests<strong>low x</strong>` = "suggestslow" 로 붙는다
    (2026-09-09 자체시험에서 잡았다). 사용자가 띈 자리는 낱말 사이지 강조 안이 아니다.
    """
    raw = m.group(1)
    body = raw.strip(" \t\r\n")
    if not body or body.startswith("*") or body.endswith("*"):
        return m.group(0)                      # 빈 강조·`***` 꼴은 강조가 아니다
    lead = raw[:len(raw) - len(raw.lstrip(" \t"))]
    tail = raw[len(raw.rstrip(" \t")):]
    if lead and tail:
        return m.group(0)                      # 양쪽 다 띔 → 문장 통째 굵어짐 방지
    return "%s<strong>%s</strong>%s" % (lead, body, tail)
_MDL_CODE = re.compile(r"`([^`]+)`")
#: Obsidian 식 하이라이트 — 1저자 메모가 실제로 쓴다 (2026-09-08). 표준 md 는 아니다.
_MDL_MARK = re.compile(r"==(?!\s)(.{1,%d}?)(?<!\s)==" % _MDL_MAXB, re.S)
#: 취소선 — 철회 표기에 실제로 쓴다(`<s>0.199</s> ⛔ 철회`). 볼드와 **같은 가드**를 쓴다.
_MDL_STRIKE = re.compile(r"~~(?!\s)(.{1,%d}?)(?<!\s)~~" % _MDL_MAXB, re.S)
#: 이탤릭 — **단어경계를 요구한다.** 이게 없으면 실측 충돌이 난다:
#:   `D*(design) / D*(host)` 의 두 별표가 짝지어져 `(design) / D` 가 통째로 기울어진다.
#:   ⇒ 여는 별표 앞은 **단어문자가 아니어야** 하고(`D*` 는 열지 않는다),
#:      닫는 별표 뒤도 단어문자가 아니어야 한다. 볼드 가드 ②③ 는 그대로 물려받는다.
_MDL_ITAL = re.compile(
    r"(?<![\w*])\*(?![\s*)\]}>,.;:!?])(.{1,%d}?)(?<![\s([{<*])\*(?![\w*])" % _MDL_MAXB, re.S)


def _mdlite(text: str) -> Markup:
    # ⚠ `text or ""` 였다 — **실측 0 이 화면에서 사라졌다**(0 은 falsy 라 빈 문자열이 됐고,
    #   읽는 사람에게는 '측정 안 함' 과 구분이 안 됐다). None 만 빈 문자열로 본다.
    s = "" if text is None else str(escape(text))
    spans = []                                   # ① 코드 스팬 격리

    def _stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    s = _MDL_CODE.sub(_stash, s)
    s = _MDL_BOLD.sub(_mdl_bold_sub, s)
    s = _MDL_MARK.sub(r"<mark>\1</mark>", s)
    # ⚠ 취소선·이탤릭은 **코드 스팬 격리 뒤·복원 앞**이다. `` `~~x~~` `` 안의 물결과
    #   `` `a*b` `` 안의 별표는 데이터다. 볼드를 먼저 걸어야 `**` 가 이탤릭에 안 먹힌다.
    s = _MDL_STRIKE.sub(r"<s>\1</s>", s)
    s = _MDL_ITAL.sub(r"<em>\1</em>", s)
    s = re.sub(r"\x00(\d+)\x00",
               lambda m: '<code class="mono">%s</code>' % spans[int(m.group(1))], s)
    # ② 표 (2026-09-08) — 카드 본문이 `| a | b |` 를 쓰는데 mdlite 가 표를 몰라서
    #   **화면에 파이프가 그대로 노출됐다** (1저자 신고). 카드마다 글을 고치는 대신
    #   여기서 그린다 — 한 곳을 고치면 기존 카드도 같이 낫고, 저건 진짜 표 데이터다.
    #   ⛔ 못 하는 것: 정렬행(`|---|`)·헤더 구분·셀 병합·중첩 표. **연속한 파이프 줄을
    #     한 표로 묶을 뿐**이고, 첫 줄을 머리행으로 쓴다. 그 이상이 필요하면 md_html 을 쓸 것.
    out, buf = [], []

    def _flush():
        if not buf:
            return
        rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in buf]
        w = max(len(r) for r in rows)
        h = "".join(f"<th>{c}</th>" for c in rows[0] + [""] * (w - len(rows[0])))
        body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r + [""] * (w - len(r)))
                       + "</tr>" for r in rows[1:])
        out.append(f'<table class="mdl-tbl"><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>')
        buf.clear()

    for ln in s.split("\n"):
        t = ln.strip()
        # 파이프로 시작하고 끝나는 줄만 표로 본다. `|ρ|<0.2` 같은 본문은 걸리지 않는다.
        if len(t) > 2 and t.startswith("|") and t.endswith("|"):
            if not re.fullmatch(r"\|[\s:\-|]+\|", t):      # 정렬행은 버린다
                buf.append(t)
            continue
        _flush()
        out.append(ln)
    _flush()
    # ③ 줄바꿈 (2026-08-20) — 카드가 여러 문장이면 한 덩어리로 뭉개져 안 읽힌다.
    #   escape 를 이미 지났으므로 주입 위험 없음.
    s = "\n".join(out).replace("\n", "<br>").replace("<br><table", "<table").replace("</table><br>", "</table>")
    # ④ 결속 (v3 묶음 F · P0-4, 2026-09-09) — 종전 `_mdlite` 는 **결속을 안 탔다.**
    #   템플릿 8개 73곳이 이 경로인데, 그때 unbound 가 0 이었던 건 그 73곳에 결속 대상
    #   문자열이 **없어서**였다. 즉 검사가 초록인 이유가 "지켜서" 가 아니라 "안 마주쳐서"
    #   였다는 뜻이라 다음 카드 한 장이면 조용히 뚫린다. `md_html` 과 **같은 판정기**를 태운다.
    return Markup(_bind_claims(s))


app.jinja_env.filters['mdlite'] = _mdlite


try:
    import markdown as _md
except Exception:
    _md = None


# ── kb frontmatter (v3 묶음 F · P0-34, 2026-09-09) ───────────────────────────
#   kb_wiki 규약을 지킨 문서일수록 화면이 깨졌다: 선행 YAML 15줄이 본문으로 렌더돼
#   /sdcp·/sdcp/self-doping 첫 화면이 `verifiedBy: …` 로 시작하고 목차 1번 항목이 됐다.
#   ⇒ **떼되 버리지 않는다.** updated·status·confidence 는 헤더 배지로 되살린다.
_FM_RE = re.compile(r"\A﻿?---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.S)
#: 배지로 올릴 키와 그 라벨. 순서가 화면 순서다. 나머지 frontmatter 는 조용히 버린다.
_FM_BADGES = (("updated", "갱신"), ("status", "상태"), ("confidence", "확신도"),
              ("verificationStatus", "검증"), ("verifiedAt", "검증일"))


def split_frontmatter(text: str):
    """선행 YAML frontmatter 를 본문에서 뗀다 → `(meta, body)`.

    ⛔ 이 함수가 **못 하는 것**: YAML 을 파싱하지 않는다. `key: value` 한 줄짜리
      최상위 항목만 읽고 중첩 매핑·여러 줄 값·리스트 원소는 값 문자열 그대로 둔다.
      frontmatter 가 없으면 `({}, 원문)` 을 그대로 돌려준다 — 본문을 절대 안 자른다.
    """
    m = _FM_RE.match(text or "")
    if not m:
        return {}, (text or "")
    meta = {}
    for ln in m.group(1).split("\n"):
        if ln[:1] in (" ", "\t", "-", "#") or ":" not in ln:
            continue                              # 중첩·리스트·주석은 안 읽는다
        k, _, v = ln.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, (text or "")[m.end():]


def doc_badges(meta: dict) -> list:
    """frontmatter → 헤더 배지 [(라벨, 값), …]. **없는 것을 채우지 않는다.**

    갱신일이 없으면 오늘로 메우지 않고 `('갱신', None)` 을 내보내 화면이
    '미기재' 라고 말하게 한다 (0 이나 today 로 채우면 그건 거짓말이다).
    """
    if not meta:
        return []
    out = [(lab, meta.get(k)) for k, lab in _FM_BADGES if meta.get(k)]
    if not meta.get("updated") and not meta.get("date"):
        out.insert(0, ("갱신", None))
    elif not meta.get("updated"):
        out.insert(0, ("갱신", meta.get("date")))
    return out


def _md_slugify(value, separator):
    """제목 → 앵커 id. **한글을 보존한다.**

    python-markdown 기본 slugify 는 비-ASCII 를 통째로 버려서 우리 문서의 한국어
    제목이 전부 빈 id 가 된다(그래서 `/concept/dft#12-활성화-…` 딥링크가 죽었다).
    `slugify_unicode` 와 같은 규칙 — 단어문자만 남기고 공백을 구분자로 바꾼다.

    ⚠ **NFKD 를 쓰지 않는다.** 한글 음절이 자모로 분해되면 화면상 글자는 같은데
      바이트가 달라져, 사람이 손으로 적은 링크(`#12-활성화-…`, 조합형)와 안 맞는다.
      NFC 로 **모아서** 고정한다.
    """
    import unicodedata
    v = unicodedata.normalize("NFC", str(value))
    v = re.sub(r"[^\w\s-]", "", v).strip().lower()
    return re.sub(r"[%s\s]+" % re.escape(separator), separator, v)


def md_html(text: str, extensions=("tables", "fenced_code"), origin="internal") -> str:
    """마크다운 → HTML. **raw HTML 통과는 끈다.**

    렌더 결과가 innerHTML(literature.html·log.html) 과 |safe(doc/concept) 로 들어가는데,
    Python-Markdown 은 기본적으로 raw HTML 을 그대로 흘려보낸다(safe_mode 폐지됨).
    litdb digest 는 논문 에이전트가 외부 PDF 를 요약해 쓰는 파일이라 입력이 100% 신뢰
    대상은 아니므로, 태그를 통째로 이스케이프하는 대신 파서 단계에서 raw HTML 만 끈다
    (표·코드블록 등 정상 마크다운 렌더는 그대로 유지된다).

    ⚠ raw HTML 을 껐다고 끝이 아니다 (2026-08-07 리뷰 P2): 파서는 **URL scheme 을 안 본다**.
      `[click](javascript:alert(1))` 이 그대로 `<a href="javascript:...">` 로 나갔다.
      litdb digest 는 논문 에이전트가 외부 PDF 를 요약해 쓰는 파일이라 입력이 100% 신뢰
      대상이 아니므로, 렌더 결과의 href/src 를 **허용 scheme 만 통과**시킨다.
    """
    _, text = split_frontmatter(text)            # ← P0-34: YAML 15줄이 본문으로 새던 자리
    if _md is None:
        return "<pre>" + (text or "") + "</pre>"
    md = _md.Markdown(extensions=list(extensions),
                      extension_configs={"toc": {"slugify": _md_slugify}}
                      if "toc" in extensions else {})
    for name in ("html_block",):
        try:
            md.preprocessors.deregister(name)
        except (KeyError, ValueError):
            pass
    for name in ("html", "raw_html"):
        try:
            md.inlinePatterns.deregister(name)
        except (KeyError, ValueError):
            pass
    return _bind_claims(_sanitize_urls(md.convert(text or "")), origin=origin)


# ── 개념 문서 서버 렌더 (Codex BI P0-2b · 2026-09-08) ────────────────────────
#   종전에는 `concept.html` 이 브라우저 `marked` 로 **다시 그렸고**, 그 순간
#   `box.innerHTML = …` 이 서버가 붙인 `.claim-flag` 를 통째로 덮었다. 서버 스캔은
#   초록인데 사람이 보는 화면에는 결속이 없는 상태 — 실측 14건(bvse 10 · msd_reading 2
#   · md 1 · beta-gate 1). 파서가 둘이면 판정도 둘이 된다.
#   ⇒ **판정은 서버 한 곳**. 콜아웃·수식 보호를 서버로 옮기고 브라우저 재렌더를 없앤다.
_CALLOUT_HEAD = re.compile(r"^>\s*\[!(\w+)\]\s*(.*)$")
_MATH_TOK = "xxMATHxx%dxx"
_CALL_TOK = "xxCALLOUTxx%dxx"
_MATH_PAT = re.compile(r"\$\$[\s\S]+?\$\$|\$[^$\n]+?\$")


def _protect_math(text: str):
    """`$…$` · `$$…$$` 를 자리표시자로 빼둔다 → (text, store).

    ⚠ 빼두지 않으면 Python-Markdown 이 수식 안의 `_`·`*` 를 강조로 먹는다
      (`$\\sum_{i<j}$` → `<em>` 삽입). KaTeX 는 textContent 를 읽으므로 그 순간 깨진다.
    """
    store = []

    def _put(m):
        store.append(m.group(0))
        return _MATH_TOK % (len(store) - 1)
    return _MATH_PAT.sub(_put, text or ""), store


def _split_callouts(text: str, render):
    """Obsidian 콜아웃(`> [!note] 제목`)을 빼서 렌더해 두고 자리표시자를 남긴다.

    본문은 같은 서버 렌더러(`render`)를 다시 타므로 **결속·URL 정화가 콜아웃 안에도**
    걸린다. 브라우저 판(concept.html 옛 :225)은 marked 를 직접 불러 그 둘을 건너뛰었다.
    """
    lines, out, blocks, i = (text or "").split("\n"), [], [], 0
    while i < len(lines):
        m = _CALLOUT_HEAD.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        kind, title, body = m.group(1).lower(), (m.group(2) or "").strip(), []
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            body.append(re.sub(r"^>\s?", "", lines[i]))
            i += 1
        head = f'<div class="cal-t">{escape(title)}</div>' if title else ""
        blocks.append(f'<div class="callout cal-{escape(kind)}">{head}'
                      f'<div class="cal-b">{render(chr(10).join(body))}</div></div>')
        out += ["", _CALL_TOK % (len(blocks) - 1), ""]
    return "\n".join(out), blocks


def doc_html(text: str) -> str:
    """개념·문서용 마크다운 렌더 — 콜아웃 + 수식 보호 + **결속**까지 서버에서.

    ⛔ 이 함수가 **못 하는 것**
      · 수식 안의 문자열은 결속하지 않는다 (자리표시자로 빠져 있다가 결속 뒤에 돌아온다).
        수식에 철회값을 적으면 표식이 안 붙는다 — 알려진 한계다.
      · mermaid·KaTeX 는 여전히 브라우저가 그린다. 그 둘은 **텍스트 노드를 바꾸지만
        `.claim-flag` span 을 지우지는 않는다**(코드블록 교체 · 수식 자리 교체뿐).
      · 결속 실패를 조용히 넘기지 않는다 — `_bind_claims` 가 원문을 돌려주고 시험이 잡는다.
    """
    _, text = split_frontmatter(text)            # ← P0-34 (concept 경로도 같은 구멍이었다)

    def _inner(t):
        if _md is None:
            return "<pre>" + escape(t or "") + "</pre>"
        # `toc` 는 목차를 그리려고 켜는 게 아니라 **안정적인 heading id** 때문에 켠다.
        #   위치 기반 id(`h0`,`h1`…)는 절이 하나만 늘어도 외부 딥링크가 전부 어긋난다.
        m = _md.Markdown(extensions=["tables", "fenced_code", "toc"],
                         extension_configs={"toc": {"slugify": _md_slugify}})
        for name in ("html_block",):
            try:
                m.preprocessors.deregister(name)
            except (KeyError, ValueError):
                pass
        for name in ("html", "raw_html"):
            try:
                m.inlinePatterns.deregister(name)
            except (KeyError, ValueError):
                pass
        return _sanitize_urls(m.convert(t or ""))

    body, math = _protect_math(text or "")
    body, calls = _split_callouts(body, _inner)
    html = _inner(body)
    for n, blk in enumerate(calls):                       # <p>토큰</p> 과 맨토큰 둘 다
        tok = _CALL_TOK % n
        html = html.replace(f"<p>{tok}</p>", blk).replace(tok, blk)
    html = _bind_claims(html)                             # ★ 결속은 여기 한 번뿐이다
    for n, raw in enumerate(math):                        # 수식은 결속 **뒤에** 돌려놓는다
        html = html.replace(_MATH_TOK % n, escape(raw))
    return html


# ── 회신 BG ② — kb 산문의 결속은 **렌더할 때** 붙인다 ─────────────────────────
#   `/todo`·`/requests`·저널·litdb 는 원문이 마크다운이다. 손으로 data-claim 을 심으면
#   원장이 화면 형식에 오염되고, 다음에 원문을 고치면 결속이 조용히 사라진다.
#   그래서 md_html 한 곳에서 자동으로 붙인다 — 새 문서가 들어와도 자동으로 결속된다.
#   ⚠ 자동이라서 **눈에 보여야** 정직하다: `.claim-flag` 가 밑줄+⛔ 를 그리고 사유를 띄운다.
def _bind_claims(html: str, origin: str = "internal") -> str:
    import canonical as _C
    try:
        return _C.annotate_claims(html, origin=origin)[0]
    except Exception:                                    # noqa: BLE001
        # 결속 실패가 화면을 죽이면 안 된다. 다만 **조용히 통과시키지도 않는다** —
        # 시험(`test_markdown_render_binds_claims_and_can_fail`)이 이 경로를 음성으로 잡는다.
        return html


@app.template_filter("claimbind")
def claimbind(text):
    """평문 한 토막에 결속을 붙인다 — 마크다운이 아닌 **템플릿 문자열**용.

    쓰는 곳: 방법·출처 주석처럼 다른 계의 정본값을 인용하는 자유 문장
    (`/composition` 의 `canonical_meta`·`canonical_provisional`).
    ⚠ 먼저 escape 하고 나서 감싼다 — 순서가 바뀌면 삽입한 span 이 이스케이프된다.
    """
    return Markup(_bind_claims(str(escape(text or ""))))


# 허용 scheme — 나머지(javascript:, data:, vbscript: …)는 링크를 죽인다.
_URL_ATTR = re.compile(r"""(?P<a>\b(?:href|src)\s*=\s*)(?P<q>["'])(?P<v>[^"']*)(?P=q)""", re.I)
_URL_OK = re.compile(r"""^\s*(?:https?:|mailto:|/|\#|\./|\.\./|[\w.\-~%()가-힣][^:]*$)""", re.I)


def _sanitize_urls(html: str) -> str:
    """렌더된 HTML 의 href/src 를 허용 scheme 만 통과시킨다.

    ⚠ 파서에서 raw HTML 을 껐다고 안전해지지 않는다 — 마크다운 링크 문법 자체가
      `[x](javascript:alert(1))` 를 정상 링크로 만든다 (2026-08-07 리뷰 P2, 실측 확인).
      스키마가 아닌 상대경로·앵커·한글 파일명은 그대로 살린다.
    """
    def _fix(m):
        v = (m.group("v") or "").strip()
        # &#106;avascript: 같은 엔티티 우회를 막으려면 먼저 푼다
        import html as _h
        plain = _h.unescape(v).replace("\t", "").replace("\n", "").replace("\r", "")
        if _URL_OK.match(plain):
            return m.group(0)
        return f'{m.group("a")}{m.group("q")}#blocked-url{m.group("q")} data-blocked-url="1"'
    return _URL_ATTR.sub(_fix, html)


_BOLD_RE = re.compile(r"\*\*(.+?)\*\*", re.S)


@app.template_filter("bold")
def _bold(s):
    """db JSON 문자열의 '**강조**' 만 <b> 로 승격. 나머지는 전부 이스케이프.

    깔때기·계보 JSON 은 마크다운 강조를 섞어 쓰는데(정직성 문구가 대부분 거기 걸려 있다)
    그대로 렌더하면 별표가 노출된다. escape() 를 먼저 걸어 raw HTML 주입은 차단하고,
    살아남은 ** 쌍만 태그로 바꾼다 — 내부 텍스트는 이미 이스케이프된 상태.
    """
    if s is None:
        return Markup("")
    return Markup(_BOLD_RE.sub(r"<b>\1</b>", str(escape(str(s)))))


def _css_ver():
    """style.css + static/js/*.js 최신 mtime 기반 캐시버스팅 키 (요청마다 계산 → 수정 즉시 반영)."""
    try:
        paths = [os.path.join(app.static_folder, "css", "style.css")]
        jsd = os.path.join(app.static_folder, "js")
        if os.path.isdir(jsd):
            paths += [os.path.join(jsd, f) for f in os.listdir(jsd) if f.endswith(".js")]
        return str(int(max(os.path.getmtime(p) for p in paths)))
    except Exception:
        return "1"


def _vsrc(name, cdn):
    """static/vendor/<name> 이 있으면 로컬(에어갭 OK), 없으면 CDN.
    tools/vendor_libs.sh 로 vendor/ 채우면 자동으로 로컬 전환."""
    p = os.path.join(app.static_folder, "vendor", name)
    if os.path.exists(p):
        return f"/static/vendor/{name}?v={int(os.path.getmtime(p))}"
    return cdn


@app.context_processor
def _inject():
    # ⚠ v3 묶음 A — 사이드바·⌘K·라벨의 단일 출처는 webapp/nav.py 다.
    #   base.html 이 nav 를 손으로 적으면 ⌘K 목록과 또 갈라진다(6개가 그렇게 빠졌다).
    import nav as NAV
    return {"asset_version": _css_ver(), "vsrc": _vsrc, "COMPS": D.COMPOSITIONS,
            "CATS": D.CATEGORIES, "FAMILY_ORDER": D.FAMILY_ORDER,
            "NAV": NAV.sidebar(), "NAVCOMPS": NAV.composition_groups(),
            "ONBOARD": NAV.onboard_stats(), "NAVMOD": NAV}


# ── 페이지 ──────────────────────────────────────────────
#: 홈 커버리지 매트릭스에서 빼는 열 (v3 묶음 B, 2026-09-09). 스크리닝 캠페인은
#: `/cascade` 가 자기 화면을 갖고 있고, 여기서는 조성 × 물성만 센다.
HOME_MATRIX_DROP = ("cascade",)


@app.route("/")
def index():
    b = D.build_matrix()
    cov = D.build_coverage(b["properties"], b["prop_category"], b["index_metrics"])
    # ⚠ v3 묶음 B — 홈 매트릭스에서 **cascade 열을 뺀다.** cascade 는 조성별 물성이 아니라
    #   47종 스크리닝 캠페인이고, 14칸 중 12칸이 N/A 였다(전체 N/A 18칸 중 12칸이 이 열 하나).
    #   ⛔ NOT_APPLICABLE 사전 자체는 **안 건드린다** — 다른 조합이 거기 걸려 있고, 그 사전의
    #     존재 이유가 "금지된 계산을 TODO 로 광고하지 않기" 다.
    #   여기서 cov 를 걸러 covstat·매트릭스·family 칩이 **같은 열 집합**을 보게 한다
    #   (열은 뺐는데 %는 안 뺀 상태로 두면 화면 안에서 분모가 갈린다).
    cats = [c for c in D.CATEGORIES if c["id"] not in HOME_MATRIX_DROP]
    cov = {cid: {k: v for k, v in row.items() if k not in HOME_MATRIX_DROP}
           for cid, row in cov.items()}
    # N/A(성립 안 함/규율상 금지) 칸은 TODO 와 구분해서 렌더 — 튜플 키는 Jinja 에서 못 쓰니 평탄화
    na = {f"{c}|{k}": r for (c, k), r in D.NOT_APPLICABLE.items()}
    # ⚠ v3 묶음 B — 카드는 **축으로 묶어** 내려보낸다(축마다 최신 1장만 펼침). 같은 목록을
    #   두 번 세지 않게 highlights 를 한 번만 만들어 groups·recent 둘 다에 먹인다.
    hl = D.dashboard_highlights()
    return render_template("index.html", active="home", b=b, cov=cov, NA=na, CATS=cats,
                           oi=D.open_items_summary(),
                           covstat=D.coverage_stats(cov), highlights=hl,
                           groups=D.highlight_groups(hl), recent=D.recent_changes(hl),
                           sei=D.sei_summary(), sei_axes=D.sei_axes())


@app.route("/composition/<cid>")
def composition(cid):
    if cid not in D.COMPOSITIONS:
        abort(404)
    b = D.build_matrix()
    dop = D.CASCADE_DOPANT.get(cid)
    # ── 원장 파생 (v3 묶음 D) — 화면·복사·타일이 **같은 출처**를 쓴다 ──────────
    import decisions_view as V
    vals = D.canonical_values(cid)
    fams = {k: v.get("family") for k, v in D.COMPOSITIONS.items()}
    return render_template(
        "composition.html", active="", cid=cid, cid_active=cid,
        comp=D.COMPOSITIONS[cid], structures=D.structures_for(cid),
        struct_groups=D.structure_groups(cid),
        # 이 조성을 지배하는 판정·마감 카드·인용 위험 (손으로 쓴 요약 아님)
        decisions=V.decisions_for(cid),
        cards=V.closure_cards_for(cid, D._PREFIX.get(cid, [cid])),
        hazards=V.hazards_for(cid),
        # 해석 카드 — 값이 아니라 **서술**이다. 카드가 자기 조성을 선언한 것만 온다 (2026-09-14)
        interps=V.interpretation_cards_for(cid),
        notices=V.metric_notices(cid),
        # 이 계열에 등록된 적 없는 축 — TODO 로 광고하지 않고 접는다 (P0-09)
        other_family=V.other_family_axes(cid, fams, vals, set(
            k for (k, c) in D.CANONICAL_NA if c == cid)),
        index_built=b.get("built"),   # Raw 탭 스냅샷 배너 (전체 b 번들은 템플릿에 불필요)
        datafiles=D.datafiles_for(cid), metrics=b["index_metrics"].get(cid, []),
        rollup=b["comp_data"].get(cid), icohp=D.icohp_for(cid),
        # ⚠ ICOHP JSON 과 COHP 곡선 CSV 는 독립이다 (comp2 는 곡선만 있다) — 따로 넘긴다
        cohp_curves=D.cohp_curves_for(cid), elf_curves=D.elf_curves_for(cid),
        cascade_dopant=dop, cascade_meta=D.CASCADE_META,
        cascade_join=D.CASCADE_JOIN_STATUS.get(cid),
        cascade_rows=D.cascade_rows_for(dop) if dop else None,
        canonical=vals,
        canonical_status=D.canonical_status_for(cid), MM=D.metric_meta(),
        # 값 타일의 결속 이름 (원장 파생) — Codex BI P0 · 2026-09-08
        canonical_claim=D.canonical_claim_for(cid),
        # 잣대 세대 — 어느 시절 규칙으로 만들어진 값인가 (2026-09-07)
        canonical_gen=D.canonical_generation_for(cid),
        canonical_prov={k: v for (k, c), v in D.canonical_provenance_flags().items() if c == cid},
        canonical_meta=D.CANONICAL_META,
        canonical_provisional={k: r for (k, c), r in D.CANONICAL_PROVISIONAL.items() if c == cid},
        canonical_na={k: r for (k, c), r in D.CANONICAL_NA.items() if c == cid})


@app.route("/compare")
def compare():
    b = D.build_matrix()
    bvse = D.bvse_shared()          # 3계 공유 BVSE (조성 prefix 로 안 잡히던 자료)
    # ⚠ CANONICAL_PROVISIONAL 은 (key, cid) 튜플 키라 |tojson 이 TypeError 를 낸다 → 문자열로 평탄화.
    prov = {f"{k}|{c}": r for (k, c), r in D.CANONICAL_PROVISIONAL.items()}
    # ★ 2026-08-07 (리뷰 P1): 부제는 "같은 방법끼리만 유효"인데 구현은 값이 있으면 그냥 그렸다.
    #   비교 묶음(comparison_group)과 상태를 같이 내려보내 **차트·레이더가 강제**하게 한다.
    # ⛔ 2026-08-20 (codex 동결감사) — 게이트 **판정**을 같이 내려보낸다. 이전에는
    #   blocking_gate 자체가 안 실려서 화면에서 상태가 사라졌고, 템플릿 JS 에는
    #   "blocking_gate 있으면 미통과" 라는 옛 의미가 남아 있어 필드를 다시 연결하는
    #   순간 회귀할 상태였다. 문구는 서버(canonical.gate_prefix)가 만든다 — 단일 출처.
    import canonical as _C
    meta = {f"{k}|{c}": {"group": e.get("comparison_group"),
                         "status": e.get("status"),
                         "method": e.get("method_id"),
                         "n_seed": e.get("n_seed"),
                         "u": e.get("uncertainty"),
                         "src": e.get("source_path"),
                         "gate": e.get("blocking_gate"),
                         "gate_outcome": _C.gate_outcome(e),
                         "gate_text": _C.gate_prefix(e),
                         "note": e.get("note")}
            for (k, c), e in D.CANONICAL_ENTRY.items() if k and c}
    # ⛔⛔ v3 P0 (Codex 회신에 우리가 적어 둔 사각) — 이 표의 셀은 `<script>` 안 JSON 에서
    #   **브라우저가 조립**한다. 스캐너는 script 를 건너뛰므로 서버 스캔에 안 잡히고,
    #   만들어진 td 에 `data-claim` 이 없으면 철회값이 이름 없이 화면에 뜬다.
    #   ⇒ 결속 이름을 **서버에서** 판다 (손 목록 없음 — 레지스트리 (metric, system) 쌍).
    #   ⚠ 레지스트리에 없는 쌍에는 붙이지 않는다 — 없는 id 를 대면 유령 결속(dangling)이다.
    bind = {f"{k}|{c}": _C.claim_id(k, c) for (k, c) in D.CANONICAL_ENTRY if k and c}
    # 인용을 **막아야 하는** 칸 (철회·비인용) — explorer 와 같은 출처(D.claim_map()).
    blocked = {f"{k}|{c}": {"state": v.get("state"), "why": (v.get("why") or "")[:400],
                            "instead": _C.instead_text(v.get("instead"))}
               for (k, c), v in D.claim_map().items()}
    # MSD 카드가 손으로 쓴 처방·판번호를 들고 있으면 **반드시 낡는다** (실측: '200 ps
    #   헤드라인' 과 '30런 처방' 이 둘 다 09-04/09-08 결정으로 대체됐는데 화면만 몰랐다).
    #   ⇒ 지위·날짜·문구를 원장에서 읽는다. 못 읽으면 카드가 "말할 수 없다" 고 말한다.
    try:
        _dec = {i: {"state": _C.decision_state(d),
                    "date": d.get("date") or (d.get("ratification") or {}).get("date"),
                    "statement": d.get("statement") or ""}
                for i, d in _C.decisions().items() if "lpsocl-box331" in i}
        _dec = {i: v for i, v in _dec.items() if v["state"] == "active"}
    except Exception:                                     # noqa: BLE001
        _dec = {}
    return render_template("compare.html", bvse=bvse, active="compare", b=b,
                           canonical=D.canonical_table(), canonical_provisional=prov,
                           canonical_meta=meta, metric_meta=D.metric_meta(),
                           claim_bind=bind, claim_blocked=blocked, decisions=_dec,
                           canonical_prov={f'{k}|{c}': v for (k, c), v in
                                           D.canonical_provenance_flags().items()})


#: `?archive=1` 없이는 **DOM 에 싣지 않는** cascade 산출물 (v3 묶음 E · 2026-09-09).
#:  · ranked      — manifest `archive_only` (2026-08-16 Codex P0-5)
#:  · champions   — v1 141행. manifest 미등재 = 미승인. v2 는 `casc.v2.champions`(🔁 탭)
#:  · litransport — v1 47종판. 같은 사유
#:  · synergy     — v1 휴리스틱 pair. explicit pair 라벨 0개
#: ⛔ 이 목록을 **줄이는** 방향으로 고치지 말 것. `/api/file` 이 같은 파일에 403 을
#:   내는 한(원장 미등재), 화면만 내보내면 사이트가 자기 정책을 어긴다.
CASCADE_ARCHIVE_ONLY = ("ranked", "champions", "litransport", "synergy")


@app.route("/cascade")
def cascade_page():
    """감사 화면. **역사 47종 랭킹은 `?archive=1` 없이는 DOM 에 넣지 않는다.**

    ⛔ 2026-08-16 (Codex f9 webapp P0-5) — 경고 배너를 붙여도 47종 rank·score 배열이
      `var RANKED` 로 초기 DOM 에 통째로 실려 나갔다. manifest 상 그 산출물은
      `archive_only` 인데 기본 화면이 정책을 어기고 있었다. 보안 문제가 아니라
      **사이트가 "승인된 ranking 0종" 이라고 쓰면서 순위표를 같이 내보내는** 자기모순이다.
      `/cascade/diagnostic` 이 이미 `?view=diagnostic` 로 닫혀 있는 것과 같은 규칙을 쓴다.

    ⛔ 2026-09-09 (v3 묶음 E · P0-12) — 게이트가 `ranked` **하나만** 비웠다. manifest 에
      한 줄도 등재되지 않은 v1 산출물 셋(champions 141행 · litransport · synergy)이
      기본 DOM 에 전량 실려 나갔다. 같은 파일을 `/api/file` 로 받으면 **403**(미등록 =
      미승인)이라, 다운로드는 막고 화면은 내보내는 상태였다. 게이트를 **넓힌다** —
      완화가 아니다. 데이터는 지우지 않고 `?archive=1` 에서 그대로 나간다.
    """
    casc = dict(D.load_cascade())
    archive = request.args.get("archive") == "1"
    diagnostic = request.args.get("view") == "diagnostic"
    # 값을 지우지 않는다 — 이 응답에서만 뺀다. 쿼리를 주면 그대로 나간다.
    if not archive:
        for _k in CASCADE_ARCHIVE_ONLY:
            if casc.get(_k):
                casc[_k] = {**casc[_k], "data": [], "archive_gated": True}
    if not diagnostic and casc.get("themes"):
        # 90종 조합 랭킹은 diagnostic_only 다 (도펀트명 + norm 점수 + BVS 열까지 실린다).
        casc["themes"] = {**casc["themes"], "dopants": [], "diagnostic_gated": True}
    ranked = casc.get("ranked", {}).get("data", [])
    ver = casc.get("verified") or {}
    comp = ver.get("compounds")
    # ⚠ 2026-08-14 — 이 수치들은 **superseded 47종판**의 것이다. 최상단 타일은
    #    D.CASCADE_TRUTH(273/270/90/0)를 쓰고, 아래는 보관함 탭 안에서만 쓴다.
    # ⚠ 게이트가 걸리면 **숫자를 내지 않는다**(None). 게이트 뒤의 0 은 "없다" 가 아니라
    #   "이 응답에서 뺐다" 이고, 그걸 0 으로 찍으면 화면이 없는 것을 세는 꼴이 된다.
    stats = {
        "archive_gated": not archive,
        "dopants": len(ranked) if archive else None,
        "pareto": (sum(1 for r in ranked
                       if str(r.get("pareto", "")).strip().upper() == "Y") if archive else None),
        "champions": (len(casc.get("champions", {}).get("data", [])) if archive else None),
        "verified": (len(comp) if isinstance(comp, (list, dict)) else None),
    }
    deep_map = {v: k for k, v in D.CASCADE_DOPANT.items()}
    # 계보 패널의 논문 링크는 실제 digest 가 있는 것만 — 없는 slug 는 링크를 죽인다
    have = {p["id"] for p in D.list_papers()}
    return render_template("cascade.html", active="cascade", casc=casc,
                           stats=stats, deep_map=deep_map, archive=archive, diagnostic=diagnostic,
                           g3state=D.CASCADE_G3_STATE, fac=D.load_factorial(),
                           facc=D.CASCADE_FACTORIAL_CONTRACT, enrich=D.CASCADE_ENRICHMENT,
                           stages=D.CASCADE_STAGE_GROUPS, stagemap=D.CASCADE_STAGE_GATE_MAP,
                           lineage=D.METHOD_LINEAGE, lit_have=have,
                           # 캠페인 지위 밴드 — 대시보드와 **같은 원장 파일**에서 읽는다
                           band=D.cascade_campaign_band(),
                           # §4b 재판정 패널 — 숫자는 원장 하나에서만 온다 (2026-09-13)
                           p4b=D.cascade_pilot_4b(),
                           mo_db=D.load_molecular_orbitals())


@app.route("/cascade/diagnostic")
def cascade_diagnostic():
    """acquisition 전용 화면 — **결과 화면이 아니다** (Codex Round-3 P1).

    기본 `/cascade` 에는 status·count 만 둔다. 후보명과 89행 랭킹은 여기서만 나가고,
    `?view=diagnostic` 없이는 서버가 렌더 자체를 하지 않는다. `<details>` 로 접어두면
    후보명이 초기 DOM 에 다 실려 public fail-closed 가 아니었다.
    """
    if request.args.get("view") != "diagnostic":
        return render_template("cascade_diagnostic.html", active="cascade",
                               gate=False, casc=None), 403
    casc = D.load_cascade()
    return render_template("cascade_diagnostic.html", active="cascade",
                           gate=True, casc=casc)


@app.route("/elements")
def elements():
    e2c = D.element_to_comps()
    return render_template("elements.html", active="elements",
                           periodic=D.PERIODIC, e2c=e2c,
                           campaign=sorted(D.campaign_elements()),
                           casc_els=sorted(D._cascade_by_element().keys()),
                           comp_elements=D.COMP_ELEMENTS, mo_db=D.load_molecular_orbitals())


@app.route("/explorer")
def explorer():
    # 세부 분석 열 — canonical 앵커(5개)와 **구분해서** 넘긴다 (빈칸이 TODO 가 아니다)
    extra = {"ELF_PS": D.elf_central_min(), "BADER_P": D.bader_charge("P")}
    # 축 전체가 비인용인 metric — **본 표에서 빼고** 사유와 함께 따로 보인다 (v3 C).
    #   TODO(아직 안 함)와 비인용(했는데 못 씀)을 같은 기호로 쓰면 화면이 거짓말을 한다.
    import canonical as _C
    # 방법 검증 앵커 — 조성 물성 표와 **다른 그룹**이라 따로 넘긴다 (2026-08-20)
    return render_template("explorer.html", active="explorer", anchors=D.method_anchors(),
                           noncite=_C.noncitable_metrics(),
                           canonical=D.canonical_table(), canonical_meta=D.CANONICAL_META,
                           canonical_provisional=D.CANONICAL_PROVISIONAL,
                           canonical_status=D.canonical_status_all(), MM=D.metric_meta(),
                           canonical_prov=D.canonical_provenance_flags(),
                           # 인용을 **막아야 하는** 칸 (Codex BI · 2026-09-08)
                           claims=D.claim_map(), comp_elements=D.COMP_ELEMENTS,
                           categories=D.CATEGORIES,
                           extra=extra, extra_meta=D.EXTRA_META,
                           amatrix=D.analysis_matrix(), awhy=D.ANALYSIS_WHY)


@app.route("/compute")
def compute():
    return render_template("compute.html", active="compute",
                           calcs=D.COMPUTE_CALCS, settings=D.COMPUTE_SETTINGS)


@app.route("/api/search")
def api_search():
    return jsonify({"items": D.search_index()})


@app.route("/api/compute-preview")
def api_compute_preview():
    from flask import request
    cid = request.args.get("cid", "")
    calc = request.args.get("calc", "scf")
    return jsonify(D.compute_preview(cid, calc))


#: `/cascade` 가 `?archive=1` 없이는 DOM 에 안 싣는 필드. **`/api/element` 도 같은
#: 게이트를 쓴다** (v3 P0-02 · 2026-09-09).
#: ⛔ 종전에는 이 경로만 열려 있었다 — `_cascade_by_element` 가 게이트 **앞** 원본을
#:   읽고 `/api/element` 에는 게이트가 아예 없어서, 사이트가 "승인된 랭킹 0종" 이라고
#:   쓰면서 47종 rank·score·ox_V 를 그대로 내보내고 주기율표 33칸을 그 순위로
#:   강조하고 있었다. 자기모순이다.
#: ⚠ 이건 게이트 **확장**이지 완화가 아니다. 값을 지우지 않고 이 응답에서만 뺀다 —
#:   `?archive=1` 을 주면 그대로 나간다(/cascade 와 같은 열쇠).
CASCADE_ARCHIVE_FIELDS = ("rank", "score", "ox_V", "E_GPa", "pugh")


def _gate_cascade_rows(rows, archive):
    """스크리닝 행에서 순위·점수축을 가린다 (`archive=False` 일 때).

    ⛔ 못 하는 것: 도펀트 **이름**은 가리지 않는다. `/cascade` 기본 화면도 이름까지는
      막지 않고(후보명은 `?view=diagnostic` 게이트 소관이다), 이름을 지우면
      "이 원소가 스크리닝에 나왔다" 는 사실 자체가 사라져 주기율표 강조가 근거를 잃는다.
    ⛔ 또 못 하는 것: 가려진 자리를 0 으로 메우지 않는다. `archive_gated: true` 를
      달아 화면이 '가려짐' 이라고 말하게 한다 — 없는 것과 가린 것은 다르다.
    """
    if archive:
        return [dict(r) for r in (rows or [])]
    out = []
    for r in (rows or []):
        row = {k: v for k, v in dict(r).items() if k not in CASCADE_ARCHIVE_FIELDS}
        row["archive_gated"] = True
        out.append(row)
    return out


@app.route("/api/element")
def api_element():
    """원소 브리핑 JSON. **캐스케이드 칸은 `/cascade` 와 같은 archive 게이트를 탄다.**"""
    from flask import request
    syms = [s.strip() for s in request.args.get("syms", "").split(",") if s.strip()]
    archive = request.args.get("archive") == "1"
    d = D.element_briefing(syms)
    for e in d.get("elements", []):
        e["cascade"] = _gate_cascade_rows(e.get("cascade"), archive)
    d["cascade_archive_gated"] = not archive
    return jsonify(d)


@app.route("/methods")
def methods():
    md = D.load_canonical_methods()
    html = md_html(md, ("tables", "fenced_code", "toc"))
    return render_template("doc.html", active="methods",
                           title="계산 방법 Canonical (단일 기준)", content=html,
                           docmeta=doc_badges(split_frontmatter(md)[0]), toc=True,
                           subtitle="kb/methodology/computational_methods_canonical.md · 값 인용 전 단일 기준")


@app.route("/cascade/rebuild")
def cascade_rebuild():
    """cascade 재건 **누적 일지** — 발표·원고 서사가 여기서 나온다 (2026-09-13 신설).

    왜 새 화면인가
      `/cascade` 는 옛 v23 산출물의 **감사 화면**이다(승인 랭킹 0종, 보관함 게이트 3종).
      재건은 그 자료를 판정에 쓰지 않기로 한 **다른 캠페인**이라 같은 화면에 얹으면
      "강등된 자료" 와 "지금 하는 일" 이 한 표에 섞인다.

    왜 마크다운을 서버에서 렌더하나
      `md_html()` 이 끝에서 `_bind_claims()` 를 부른다 — 즉 **결속이 서버 한 곳에서**
      붙는다. 브라우저에서 다시 파싱하면 판정이 둘로 갈린다(Codex BI P0-2b 실측 14건).

    ⛔ 이 화면이 **하지 않는 것**
      · 판정하지 않는다. 숫자·판정의 정본은 `db/properties/` 와 `decisions.json` 이고
        이 문서는 그것을 옮겨 적은 것이다. 충돌하면 **원장이 이긴다**.
      · 게이트를 걸지 않는다 — 강등된 v23 산출물을 싣지 않으므로 가릴 것이 없다.
    """
    md = (D.KB / "projects" / "cascade_rebuild_log_2026_09.md").read_text(encoding="utf-8")
    html = md_html(md, ("tables", "fenced_code", "toc"))
    return render_template("doc.html", active="cascade", title="cascade 재건 일지 (누적)",
                           content=html, docmeta=doc_badges(split_frontmatter(md)[0]), toc=True,
                           subtitle="kb/projects/cascade_rebuild_log_2026_09.md · "
                                    "판정 정본은 db/properties · decisions.json — 충돌하면 원장이 이긴다")


@app.route("/sdcp")
def sdcp_wave1():
    """SDCP wave1 — NCM(104) 표면 위 바인더/SDCP 흡착 (VASP 외주 회신 해석).

    ⚠ 표는 **basin 일치 여부를 값과 같은 줄에** 둔다. 어긋난 잡도 숨기지 않고
      경고와 함께 보인다 — 숨기면 "없는 데이터"로 보여 다시 계산하게 된다.
    ⛔ 이 페이지가 못 하는 것: 실제 셀의 바인더 분포를 예측하지 않는다.
      진공·0 K·단분자 값이다. 절대 E_ads 를 타 코드/논문과 직접 비교하지 않는다.
    """
    md = D.load_sdcp_wave1_md()
    html = md_html(md, ("tables", "fenced_code", "toc"))
    rows = D.sdcp_wave1_rows()
    # ⛔ 2026-09-09 (v3 묶음 E) — 마감 문서(sdcp_neutral_closed_2026_08_28.json)의
    #   허용 서술 5항·금지 서술 7항·재개 조건 4항이 화면에 **한 줄도 없었다** (파일명만
    #   두 번). "그래서 뭐라고 쓸 수 있나" 를 화면에서 알 방법이 없었다. 정본을 읽어
    #   본문 맨 앞에 붙인다 — 화면이 문구를 새로 짓지 않는다.
    #   ⚠ 이 카드는 doc.html 의 `content` 앞에 들어간다. 즉 **원자료 표 아래**다 —
    #     표를 먼저 그리는 규칙(doc.html)이 F 묶음 소유라 순서를 여기서 못 뒤집는다.
    #     `data_first` 스위치가 doc.html 에 생기면 그때 맨 위로 올린다.
    card = render_template("_campaign_band.html", closure=D.sdcp_closure_card())
    html = Markup(card) + html
    return render_template(
        "doc.html", active="sdcp",
        title="🧪 SDCP wave1 — 바인더가 NCM 표면 어디에 붙나",
        content=html, data=rows,
        docmeta=doc_badges(split_frontmatter(md)[0]), toc=True,
        parent={"url": "/log", "label": "Work Log"},
        artifact="https://claude.ai/code/artifact/5b5d48c5-e23c-47a1-8493-b42dedb9a121",
        child={"url": "/sdcp/self-doping",
               "label": "⚗️ 자기도핑이란 무엇인가 (배경지식 0 기준)"},
        # ⚠ "두 자기 시드 교차확인" 이라 쓰지 않는다 — seed 투입·독립재현은 미증명
        #   (회신 P 5번). realized basin 이 일치한 잡끼리만 인용한다.
        # ⚠ 부제의 인용 가능 수는 **게이트가 센 것**을 그대로 쓴다(하드코딩 금지) —
        #   종전 부제는 '일치분만 인용' 이라 약속했는데 정작 인용 가능 행이 0 이었다.
        subtitle=f"VASP 외주 30잡 · realized-basin 일치분만 인용 (지금 "
                 f"{rows['n_citable_dE']}행) · 자리대비 미해결 · 절대 E_ads 보류 · "
                 "db/properties/sdcp_wave1_results.json")


@app.route("/sdcp/self-doping")
def sdcp_self_doping():
    """자기도핑이 무엇인가 — **배경지식 0 기준** 해설.

    왜 별도 페이지인가: 원고의 한 단어("removing the sulfonate proton")가 계산의
      charge/multiplicity 를 바꾼다. 프로톤 제거는 음이온 162 전자 singlet, 수소 원자
      제거는 중성 161 전자 doublet 이고 **분자식은 둘 다 C11H15O6S2 라 구분이 안 된다.**
      우리 설정(charge 0 · tot_magnetization 1.0)과 에너지 검산이 후자를 확정한다.
    ⛔ 이 페이지가 못 하는 것: 실험에서 실제로 무엇이 떨어지는지 말하지 않는다.
      전도도도 말하지 않는다 (캐리어 생성 ≠ 잘 흐른다).
    """
    md = D.load_sdcp_selfdoping_md()
    if not md:
        abort(404)
    return render_template(
        "doc.html", active="sdcp",
        title="⚗️ 자기도핑이란 무엇인가",
        content=md_html(md, ("tables", "fenced_code", "toc")),
        docmeta=doc_badges(split_frontmatter(md)[0]), toc=True,
        parent={"url": "/sdcp", "label": "SDCP wave1"},
        # 공유용 HTML — 랩 밖(공저자·처음 보는 대학원생)에 링크로 던질 수 있는 판.
        #   kb md 가 정본이고 이건 읽기용이다. 내용이 갈리면 md 를 고치고 다시 배포한다.
        artifact="https://claude.ai/code/artifact/"
                 "20cb81c9-9bab-468c-ac30-0752ece28d14",
        subtitle="프로톤이 아니라 수소 원자를 뗀다 — 원고 문장 하나가 "
                 "charge/multiplicity 를 바꾸는 이유")


@app.route("/todo")
def todo():
    md = D.load_open_items_md()
    html = md_html(md, ("tables", "fenced_code", "toc"))
    # ⚠ 날짜를 하드코딩하지 않는다 — 원장 파일이 늘어도 이 문구는 그대로 맞다.
    banner = {"url": "/ledger", "label": "🧾 T·Q 원장",
              "text": "이 리스트의 T 번호가 오늘 어디까지 움직였는지는 하루치 원장에서 본다"}
    # 묶음 H · P0 — 마감된 축의 수에 표식(`records_view.mark_closed_axis`).
    #   `/todo` 는 "대신 쓸 것은 저온 구간 Ea 다" 를 초록인 채로 권하고 있었다.
    return render_template("doc.html", active="todo",
                           title="📋 미결 리스트 (Open Items)",
                           content=RV.mark_closed_axis(html), banner=banner,
                           subtitle="kb/open_items.md · 판정 대기 · PDF 확보 대기 · ML 후속 · 심포지엄 대응")


def _kb_evidence_docs():
    """결정 원장이 **이름 댄** kb 문서 목록 → [{path, ok, decisions:[id…]}].

    ⛔ 못 하는 것: kb 를 색인하지 않는다. 원장(`record`·`card`)이 가리킨 것만 센다 —
      "무슨 kb 문서가 있나" 가 아니라 "판정의 논거가 어디에 있나" 를 답하는 목록이다.
    ⚠ 있는지 없는지를 **확인해서** 적는다. 원장이 가리키는데 파일이 없으면 그 자체가
      발견이라 회색으로 남긴다(조용히 빼면 원장이 멀쩡해 보인다).
    """
    import canonical as _C
    seen = {}
    for did, d in _C.decisions().items():
        for ref in (d.get("record"), d.get("card")):
            head = str(ref or "").partition("#")[0]
            if not head.startswith("kb/"):
                continue
            row = seen.setdefault(head, {"path": head,
                                         "ok": D.safe_kb_doc(head) is not None,
                                         "decisions": []})
            if did not in row["decisions"]:
                row["decisions"].append(did)
    return sorted(seen.values(), key=lambda r: r["path"])


@app.route("/kb")
def kb_doc():
    """kb 마크다운 읽기 (v3 묶음 G · 2026-09-09). `?path=kb/…md`

    왜 생겼나: 결정 원장의 근거 문서 14건이 `kb/…md` 라 화면에서 **회색 문자열**로
    끝났다. 정책 결정 7건은 근거가 전부 kb 카드라, 결정에서 논거로 가는 길이 하나도
    없었다. `/todo` 가 이미 kb md 를 doc.html 로 그리고 있으니 배선만 없었던 것이다.

    ⚠ 왜 `/kb/<path>` 가 아니라 질의인자인가: 동적 라우트는 `test_webapp.py` 의
      `DYNAMIC_FIXTURES` 대표인자 대장에 **등재돼야만** 검사에 든다. 그 파일은 이번
      재편에서 아무도 고치지 않기로 한 파일이라(병행 편집 충돌 방지), 등재 없이 동적
      라우트를 늘리면 그 시험이 "검사 밖 라우트" 로 즉시 실패한다. 예쁜 URL 을 위해
      검사 구멍을 내지 않는다 — 대장을 고칠 수 있게 되면 한 줄로 바꿀 수 있다.

    ⛔ 이 라우트가 **못 하는 것**
      · 다운로드가 아니다. `.md` 본문을 렌더할 뿐이고 `/api/file` 허용 뿌리는 그대로다.
      · 문서가 맞는지·최신인지 판정하지 않는다. frontmatter 의 `updated`·`status` 를
        배지로 올리되(doc_badges), **없으면 메우지 않는다**.
      · kb 밖(tools/·litdb/)은 안 연다 — 없으면 404 다 (빈 화면이 아니라).
      · 아무 kb 문서나 목록에 세우지 않는다. 인자 없이 오면 **결정 원장이 실제로 이름
        댄 근거 문서**만 편다 (383개 kb 전체 색인이 아니다).
    """
    from flask import request
    rel = request.args.get("path", "").strip()
    if not rel:
        return render_template("kb_index.html", active="governance",
                               docs=_kb_evidence_docs())
    # URL 이 `kb/` 를 생략해도 받는다 — 화이트리스트에는 **저장소 상대경로**를 준다.
    full = rel if rel.startswith("kb/") else "kb/" + rel.lstrip("/")
    p = D.safe_kb_doc(full)
    if p is None:
        abort(404)
    text = p.read_text(encoding="utf-8")
    meta, _ = split_frontmatter(text)
    return render_template(
        "doc.html", active="governance",
        title="📄 " + p.name, content=md_html(text, ("tables", "fenced_code", "toc")),
        badges=doc_badges(meta),
        parent={"url": "/governance", "label": "⚖ 판정 원장"},
        subtitle=full + " · 원본은 이 파일이다 — 화면은 읽기용이다")


@app.route("/requests")
def requests_page():
    """1저자 요청 대장 — 이 캠페인에서 가장 자주 되돌아오는 문서.

    ⚠ 본문 전에 **어디가 닫혔고 어디가 안 닫혔나**를 먼저 보여준다. 문서가 1000줄이라
      매번 처음부터 읽으면 상태 파악에만 시간이 간다.
    ⛔ 상태의 옳고 그름을 판정하지 않는다 — 표를 옮길 뿐이다. 이모지와 문장이
      어긋나는 행은 한쪽을 고르지 않고 **어긋났다고 표시**한다 (요청 5 가 그렇다).
    """
    md = D.load_requests_md()
    if not md:
        abort(404)
    return render_template("requests.html", active="requests",
                           ledger=D.requests_ledger(),
                           content=md_html(md, ("tables", "fenced_code", "toc")))


# ── 회신 BG ② — 화면 결속용 claim id 변환 (템플릿에서 쓴다) ─────────────────
#   판정 원장의 `claim_ref` 는 `value:<metric>/<system>` 형식이다. 그대로는 결속에 못 쓰므로
#   레지스트리 id(`<metric>@<system>`)로 바꾼다. **없는 형식이면 빈 문자열** — 유령 결속을
#   만들지 않는다 (빈 값이면 템플릿이 data-claim 자체를 안 붙인다).
@app.template_global()
def claim_ref_to_id(ref):
    m = re.match(r"^value:([^/\s]+)/([^/\s]+)$", str(ref or "").strip())
    return f"{m.group(1)}@{m.group(2)}" if m else ""


# ── 결정끼리의 참조를 화면에서 걷게 한다 (v3 묶음 G · 2026-09-09) ─────────────
#   결정 ID 는 repo 전체가 인용 단위로 쓴다 — statement·reopen_criteria·대시보드
#   카드·citation_hazards·마감 기록. 그런데 이름만 대고 갈 데가 없었다.
@app.template_filter("declink")
def _declink(s, known=(), skip=None):
    """본문 안의 결정 ID 를 같은 페이지 앵커(`#<id>`)로 잇는다.

    `skip` 은 자기 자신 — 자기 행에서 자기 id 로 가는 링크는 안 만든다.

    ⛔ 못 하는 것: **원장에 실제로 있는 id 만** 링크한다. 정규식으로 `D-…` 모양을
      전부 잇으면 오타·옛 id 가 조용히 죽은 링크가 된다 (없는 것을 있는 척하는
      이 repo 의 반복 사고형). 모르는 id 는 글자 그대로 남는다.
    ⛔ 또 못 하는 것: 그 결정이 무엇인지 판정하지 않는다 — 이름이 같으면 이을 뿐이다.
    """
    if s is None:
        return Markup("")
    txt = s if isinstance(s, Markup) else escape(str(s))
    ids = sorted({str(k) for k in (known or ()) if k and k != skip},
                 key=len, reverse=True)
    if not ids:
        return Markup(txt)
    pat = re.compile("|".join(re.escape(i) for i in ids))
    return Markup(pat.sub(
        lambda m: f'<a href="#{m.group(0)}" class="mono">{m.group(0)}</a>', str(txt)))


@app.route("/governance")
def governance_page():
    """판례·평가·산출물·인용위험 네 원장을 한 화면에 — **판정이 어디에 근거하는지**.

    ⛔ 이 페이지는 상태를 저장하지 않는다. release_status 와 같은 파생 판정은
       질의 시각에 계산한다 (D-2026-08-20-source-authority: canonical DB 가 원본).

    ⛔ 이 페이지가 **못 하는 것**
      · 값·판정이 맞는지 판정하지 않는다. 판정의 근거·소재만 보인다.
      · 결정 본문을 다 보여주지 않는다 — statement 까지다. rationale·enforcement·
        applies_to 는 원장 파일이 원본이고 화면은 그리로 보내는 길만 낸다.
      · 근거 문서 링크는 두 갈래다: `/api/file` 허용 뿌리(docs·db·litdb/figures)와
        `/kb/<path>` 마크다운 읽기(v3 G). **그 밖은 경로 문자열만** 나온다.
        조각 참조(`…json#절`)는 파일까지만 열고 절로 점프하지 않는다 — 링크 글자는
        조각까지 그대로 둔다(원장이 이름 댄 문자열을 화면이 줄이지 않는다).
      · 사전등록 여부를 추론하지 않는다 — `results_seen` 이 원장에 없으면 "미기재" 다.
      · 인용위험 행의 '결속' 배지는 **원장이 선언한 binding_scope** 를 옮길 뿐,
        그 선언이 맞는지(정말 그 형태가 다 덮이는지)는 검사하지 않는다.
    """
    import canonical as _C
    # ⚠ 이 세 accessor 는 **id 로 키를 잡은 dict** 를 준다 (리스트가 아니다).
    #   처음에 .get("artifacts", []) 로 읽었더니 화면이 조용히 **빈 표**가 됐다 —
    #   "원장이 비어 있다" 와 "원장을 잘못 읽었다" 가 화면에서 구분이 안 됐다.
    def _rows(d):
        return [{**v, "id": v.get("id", k)} for k, v in d.items()]
    dec = _rows(_C.decisions())
    ass = _rows(_C.assessments())
    art = _rows(_C.artifacts())

    # 산출물은 위험한 것부터 (사본 0 = 유실, 사본 1 = 유일본).
    risk = {"lost": 0, "suspect_banned": 1, "superseded": 2, "reference": 3, "canonical": 4}
    art = sorted(art, key=lambda a: (risk.get(a.get("status"), 9),
                                     a.get("copies", 9), a.get("id", "")))
    single = [a for a in art if a.get("copies") == 1 and a.get("status") != "lost"]
    lost = [a for a in art if a.get("status") == "lost"]

    # ── 결정 원장 파생 (2026-09-08) ───────────────────────────────────────
    #   종전 판례 표는 네 칸(id·decision_state·digest·title)뿐이라 원장에 실제로 든 것을
    #   화면이 못 보여줬다. 세 가지가 특히 빠져 있었다:
    #     ① `kind` — 정책/보고량/마감/게이트/지표가 한 표에 섞여 구분이 안 됐다
    #     ② `record_kind` · `results_seen` — **결과를 보기 전에 정했나**가 이 repo 의
    #        핵심 규율인데 화면 어디에도 없었다 (사전등록의 증거가 원장에만 있었다)
    #     ③ 근거 문서(`record`·`card`) 경로 — 결정을 읽고 원본으로 못 갔다
    #   ⚠ 없는 필드를 기본값으로 채우지 않는다. `results_seen` 이 없는 18건은
    #     "결과 보기 전" 도 "결과 본 뒤" 도 아니라 **미기재**다 (원장 부재 관례).
    for d in dec:
        want = (d.get("ratification") or {}).get("decision_digest")
        rat_state = (d.get("ratification") or {}).get("state")
        # 승인 후 본문이 바뀐 판례는 승인이 무효다 — 화면에서 즉시 드러나게 한다.
        #   ⚠ 종전 판은 `want is None` 을 "일치" 로 세어, 승인이 **아예 없는** 결정에도
        #     🔒 를 붙였다. 세 상태를 가른다: 없음 / 일치 / 불일치.
        d["_digest"] = ("none" if not want
                        else "ok" if want == _C.decision_digest(d) else "bad")
        d["_state"] = _C.decision_state(d)          # decision_state 정본 · status 별칭
        d["_ratified"] = rat_state
        rs = d.get("results_seen")
        d["_prereg"] = ("before" if rs is False else "after" if rs is True else "unstated")
        # 근거 문서 — 열 수 있는 것만 링크한다. 두 갈래(파일 서빙 / kb 마크다운 렌더)를
        #   **각자의 화이트리스트**로 판정한다. 하나로 합치면 /api/file 이 kb 전체를
        #   내려받게 된다 (2026-08-17 교훈과 같은 자리).
        #   ⚠ 링크 **글자**는 원장이 적은 ref 그대로다 — 조각(`…#절`)까지 보인다.
        #     href 만 파일까지 자른다. 화면이 원장 문자열을 줄이면 "무엇을 가리켰나" 가 샌다.
        seen, docs = set(), []
        for role, ref in (("기록", d.get("record")), ("카드", d.get("card"))):
            if not ref or ref in seen:
                continue
            seen.add(ref)
            head, _, frag = str(ref).partition("#")
            url = None
            if D.safe_repo_path(head) is not None:
                url = "/api/file/" + head
            elif D.safe_kb_doc(head) is not None:
                url = "/kb?path=" + head              # kb 마크다운 읽기 화면
            docs.append({"role": role, "path": ref, "url": url, "frag": frag})
        d["_docs"] = docs
    # 최신 결정이 위 — id 가 `D-YYYY-MM-DD-slug` 라 문자열 역순이 곧 날짜 역순이다.
    dec.sort(key=lambda d: str(d.get("id", "")), reverse=True)
    # 요약은 **있는 것만** 센다 (없는 종류를 0 으로 찍으면 원장에 그 칸이 있는 것처럼 보인다).
    from collections import Counter
    dec_kinds = Counter(d.get("kind") or "미기재" for d in dec).most_common()
    dec_states = Counter(d.get("_state") or "미기재" for d in dec).most_common()
    # ── 옛 결정 접기 (v3 묶음 G) ──────────────────────────────────────────
    #   대체·철회된 결정을 active 와 같은 굵기로 인라인에 두면 "지금 규칙" 이 안 읽힌다.
    #   ⚠ **DOM 에서 빼지 않는다** — 전건 렌더 시험이 잡고, 무엇보다 옛 판정을 지우는 것이
    #     이 repo 가 금지한 것이다. 두 표로 나누되 둘 다 그린다(옛 것은 <details> 안).
    _OLD = ("superseded", "retracted")
    dec_now = [d for d in dec if d.get("_state") not in _OLD]
    dec_old = [d for d in dec if d.get("_state") in _OLD]
    dec_ids = [d.get("id") for d in dec if d.get("id")]
    # 실제 위험 카운터 — 초록 배너 옆에 나란히 둔다. 초록이 무엇을 보증했는지
    #   말하지 않으면 페이지 전체 건강 신호로 읽힌다 (조사 gov-green-banner-scope-unstated).
    #   ⚠ '비준 없는 active' 는 원장 _rules 위반이다(ratification 없이 active 가 될 수 없다).
    #     0 이어야 정상이고, 0 이 아니면 그 자체가 발견이다.
    dec_active_unratified = [d.get("id") for d in dec
                             if d.get("_state") == "active" and d.get("_ratified") != "ratified"]

    # 네 번째 원장 (2026-09-01): 인용 위험. 25건이 화면 밖에 있었다 —
    #   "무엇을 알아냈나" 만 보이고 "무엇을 인용하면 안 되나" 가 안 보이는 화면은
    #   이 repo 의 반복 사고 유형(낡은 인용)을 못 막는다. 심각한 것부터 정렬.
    haz = D.citation_hazards()
    _sev = {"BLOCKED": 0, "HOLD": 1, "STALE": 2, "SUPERSEDED": 3,
            "CONDITIONAL": 4, "PREVIEW": 5, "RESOLVED": 6}
    hazards = sorted(haz.get("hazards", []),
                     key=lambda h: (_sev.get(h.get("level"), 9), h.get("file", "")))

    # ── 결속됨 / 산문 (v3 묶음 G) ─────────────────────────────────────────
    #   화면이 29행을 **똑같이** 그리면, 어느 행이 기계 결속(다른 화면에서 그 문구를 쓰면
    #   잡힌다)이고 어느 행이 사람이 읽어야만 하는 산문인지 구분이 안 된다.
    #   두 함수의 **차이**를 그대로 옮긴다:
    #     · `hazard_ids()`   = 어휘. 원장에 있는 id 전부 (해소·폐기 포함).
    #     · `hazard_claims()`= 결속 **요구**. RESOLVED·SUPERSEDED 는 빠진다.
    #   ⛔ 이 화면은 binding_scope 가 **맞는지** 검사하지 않는다 — 원장 선언을 옮긴다.
    _hz_vocab = _C.hazard_ids()
    _hz_req = {c["id"] for c in _C.hazard_claims()}
    for h in hazards:
        hid = h.get("id")
        if not hid:
            h["_bind"] = "none"          # 원장에 id 자체가 없다 = 결속 대상이 아니다
        elif hid not in _hz_req:
            h["_bind"] = "inactive"      # 어휘에는 남지만 살아있는 금지가 아니다
        elif h.get("claim"):
            h["_bind"] = "claim"         # 정본값에 결속 — 숫자를 쓰면 잡힌다
        elif h.get("forbidden_phrases"):
            h["_bind"] = "phrase"        # 금지 문구에 결속 — 그 산문을 쓰면 잡힌다
        else:
            h["_bind"] = "name"          # 이름만 댈 수 있다 (결속 요구는 있으나 매칭 문자열 0)
        h["_n_phrase"] = len(h.get("forbidden_phrases") or [])
        h["_n_pending"] = len(h.get("pending_forbidden_phrases") or [])
    hz_bind_counts = Counter(h["_bind"] for h in hazards)
    hz_blocked = [h for h in hazards if h.get("level") == "BLOCKED"]

    return render_template("governance.html", active="governance",
                           decisions=dec, assessments=ass, artifacts=art,
                           dec_now=dec_now, dec_old=dec_old, dec_ids=dec_ids,
                           dec_kinds=dec_kinds, dec_states=dec_states,
                           dec_active_unratified=dec_active_unratified,
                           single=single, lost=lost,
                           hazards=hazards, hazards_updated=haz.get("updated"),
                           hz_bind_counts=hz_bind_counts, hz_blocked=hz_blocked,
                           hz_vocab_n=len(_hz_vocab), hz_req_n=len(_hz_req),
                           problems=_C.validate_governance() + _C.validate_artifacts())


#: /ledger — T 상태 접두 이모지의 표시색 (해석이 아니라 표시다. 모르는 이모지는 기본색).
_TQ_STATUS_COLOR = {"🔶": "#c05621", "⏳": "#9ca3af", "✅": "#0d9488",
                    "⛔": "#6b7280", "🔴": "#be123c"}


@app.route("/ledger")
def ledger_page():
    """T·Q 원장 — 심포지엄 판독 하루치를 원장 파일 그대로 편다.

    데이터원은 **db/properties/tq_ledger_*.json 하나**다 (D.load_tq_ledger, 날짜 역순).
    코드 체계 원본은 kb/CODES.md — 특히 **Q 번호는 문서마다 로컬**이라 화면의
    Q 네 절 머리마다 경고를 박는다 (T·J·M 은 전역 번호).

    ⚠ "원장 파일이 없다" / "원장을 못 읽었다" / "칸이 비어 있다(값 대기)" 는
      세 다른 문장으로 화면에 나온다 (governance_page 교훈 — 잘못 읽은 원장이
      조용히 빈 표가 되면 안 된다). '오늘' 칸이 "-" 인 항목은 **값 대기** 뱃지다.

    ⛔ 이 페이지가 **못 하는 것**
      · 상태·결과의 옳고 그름을 판정하지 않는다 — 원장 문자열을 옮길 뿐이다.
      · '값 대기' 칸을 채우지 않는다 — 내일 원장 파일이 갱신돼야 채워진다.
      · 도구 경로 중 /api/file 허용 뿌리(docs·db·litdb/figures) 밖(tools/ 등)은
        링크로 열지 못한다 — 경로 문자열만 보인다 (safe_repo_path 가 거절).
      · T 상태 이모지의 의미를 해석하지 않는다 — 접두 이모지 그대로 센다.
    """
    ledgers = D.load_tq_ledger()
    broken = [l for l in ledgers if l.get("_error")]
    good = [l for l in ledgers if not l.get("_error")]
    led = good[0] if good else None
    if led is None:
        # 파일이 아예 없는 것(빈 리스트)과 있는데 못 읽은 것(broken)을 구분해 넘긴다.
        return render_template("ledger.html", active="ledger", led=None, broken=broken)

    # ── T 표: 상태칩 색 · '오늘' 마크다운 · 도구 링크(서빙 가능한 것만) ──
    t_raw = led.get("T")
    t_rows, t_counts, n_pending = [], {}, 0
    for t in (t_raw or []):
        status = str(t.get("상태") or "").strip()
        skey = status[:1] if status[:1] in _TQ_STATUS_COLOR else ""
        t_counts[skey or "기타"] = t_counts.get(skey or "기타", 0) + 1
        today = str(t.get("오늘") or "").strip()
        pending = today in ("", "-")
        # ⚠ 끝난 행에 '내일 채워진다' 를 붙이지 않는다 (v3 G · 2026-09-09).
        #   실측: 상태가 "✅ 완료(2026-07-28)" · "⛔ 폐기(2026-07-28)" 인 행에도 '값 대기'
        #   가 붙어 있었다 — 한 달 반 전에 끝난 항목이 대기 중으로 보인다.
        #   ⛔ 상태를 **해석하지 않는다**: 접두 이모지만 본다(이 화면의 원칙 그대로).
        closed = skey in ("✅", "⛔")
        n_pending += pending and not closed
        tool = str(t.get("도구") or "").strip()
        path = tool.split()[0] if tool else ""
        if "/" not in path:
            path = ""
        t_rows.append({"id": t.get("id", "?"), "what": t.get("무엇", ""),
                       "status": status,
                       "color": _TQ_STATUS_COLOR.get(skey, "var(--text2)"),
                       "pending": pending, "closed": closed,
                       "today_html": "" if pending else md_html(today),
                       "tool": tool, "tool_path": path,
                       "tool_link": bool(path and D.safe_repo_path(path))})
    # 요약 칩 순서 고정 (원장에 있는 것만 나온다)
    t_counts = {k: t_counts[k] for k in ("🔶", "⏳", "✅", "⛔", "🔴", "기타")
                if k in t_counts}

    # ── Q 네 절: 항목 모양이 절마다 다르다(결과/내용/닫는_법) — 있는 키만 옮긴다 ──
    def _q_rows(items):
        rows = []
        for q in (items or []):
            ans = q.get("결과") or q.get("내용") or ""
            close = q.get("닫는_법") or ""
            rows.append({"id": q.get("id", "?"), "doc": q.get("문서", ""),
                         "q_html": md_html(str(q.get("질문") or "")),
                         "a_html": md_html(str(ans)) if ans else "",
                         "close_html": md_html(str(close)) if close else ""})
        return rows

    qsec = []
    for key, label in (("Q_닫힌_것", "닫힌 것"),
                       ("Q_절반_닫힌_것", "절반 닫힌 것"),
                       ("Q_새로_열린_것", "새로 열린 것"),
                       ("Q_그대로_열려있는_것", "그대로 열려 있는 것")):
        items = led.get(key)
        qsec.append({"key": key, "label": label, "missing": items is None,
                     "rows": _q_rows(items)})

    # ── 들어온 것 / 정정 / 만든 도구: 원장에 절이 없으면 '값 대기' (None ≠ 빈 리스트) ──
    raw_in = led.get("오늘_들어온_것")
    intake = None
    if isinstance(raw_in, dict):
        # ⚠ 키 이름을 "items" 로 두면 Jinja 의 it.items 가 dict 메서드를 잡는다 → "li"
        intake = [{"k": k,
                   "li": [md_html(str(x)) for x in v] if isinstance(v, (list, tuple)) else [],
                   "html": "" if isinstance(v, (list, tuple)) else md_html(str(v))}
                  for k, v in raw_in.items()]
    corr_raw = led.get("오늘_정정한_우리_기록")
    tools_raw = led.get("오늘_만든_도구")
    # ── '오늘' 이 언제인가 (v3 G · 2026-09-09) ────────────────────────────
    #   화면이 "오늘 들어온 것" · "내일 원장이 채운다" 를 12번 넘게 쓰는데 그 '오늘' 은
    #   원장 파일의 날짜다. 실측 2026-09-08 에 그 '내일' 이 13일째 안 왔다.
    #   ⛔ 날짜를 하드코딩하지 않는다 — 원장 날짜와 오늘의 **간격을 계산**한다.
    #     원장에 date 가 없으면 None 이고, 화면은 "날짜 미기재" 라고 말한다(0 이 아니다).
    age_days = None
    try:
        from datetime import date as _date
        y, m, dd = (int(x) for x in str(led.get("date") or "").split("-")[:3])
        age_days = (_date.today() - _date(y, m, dd)).days
    except Exception:                                       # noqa: BLE001
        age_days = None
    return render_template(
        "ledger.html", active="ledger", led=led, broken=broken,
        older=[l["_file"] for l in good[1:]], age_days=age_days,
        t_rows=t_rows, t_counts=t_counts, t_missing=t_raw is None,
        n_pending=n_pending, qsec=qsec, intake=intake,
        corrections=None if corr_raw is None else [md_html(str(s)) for s in corr_raw],
        made_tools=None if tools_raw is None else [md_html(str(s)) for s in tools_raw])


@app.route("/fairchem")
def fairchem_page():
    """Fair-Chem/UMA 공식 지식 — **무엇을 할 수 있나** 가 아니라 **무엇을 우리가 써도 되나**.

    ⚠ 세 축을 절대 한 배지로 합치지 않는다: `http_status`(페이지가 열리나) ·
      `execution_status`(예제가 도나) · `project_status`(우리 계에 쓸 수 있나).
      합치면 200 인데 실행 실패한 튜토리얼이 "정상" 으로 보인다.
    ⛔ 이 페이지가 **못 하는 것**: 공식 주장의 참·거짓을 판정하지 않는다.
      우리 수치를 여기에 복사하지도 않는다 — crosswalk 는 FK 이지 값이 아니다.
    """
    import fairchem as FC
    if not FC.available():
        return render_template("fairchem.html", active="fairchem", ready=False,
                               sections=FC.SECTIONS), 200
    return render_template(
        "fairchem.html", active="fairchem", ready=True,
        sections=FC.SECTIONS, summary=FC.summary(), snap=FC.snapshot(),
        models=FC.entities("models"), tasks=FC.entities("tasks"),
        datasets=FC.entities("datasets"), claims=FC.entities("claims"),
        techs=FC.entities("technologies"), seed=FC.entities("webapp_seed"),
        crosswalk=FC.crosswalk_rows(), papers=FC.papers_rows(),
        pages=FC.page_status_rows(), audit=FC.blob("live_link_audit"),
        licenses=FC.entities("license_observations"),
        stages=FC.PAPER_STAGES, pinned=FC.OUR_PINNED, bans=FC.OUR_BANS,
        newer=FC.newer_models())


@app.route("/api/fairchem/v1/<name>")
def fairchem_api(name):
    """인계 문서가 정한 봉투로 entity 를 낸다 (읽기 전용).

    ⛔ **fail-closed**: 알 수 없는 이름이면 빈 배열을 주지 않고 404 를 낸다.
      빈 배열은 "그런 건 없다" 와 "이름을 틀렸다" 를 구분 못 하게 만든다.
    """
    import fairchem as FC
    if not FC.available():
        abort(404)
    if name == "manifest":
        return jsonify(FC.envelope(FC.manifest()))
    if name == "integrity":
        v = FC.verify_hashes()
        return jsonify(FC.envelope(v, [] if v["ok"] else ["sha256 불일치/누락 — 번들을 다시 받을 것"]))
    if name == "lpscl-crosswalk":
        return jsonify(FC.envelope(FC.crosswalk_rows()))
    if name == "papers":
        return jsonify(FC.envelope(FC.papers_rows()))
    if name == "pages":
        return jsonify(FC.envelope(FC.page_status_rows()))
    allowed = {"models", "tasks", "datasets", "technologies", "claims",
               "packages", "site_pages", "license_observations"}
    if name in allowed:
        return jsonify(FC.envelope(FC.entities(name)))
    abort(404)


@app.route("/nd-survey")
def nd_survey_page():
    """Nd 치환 문헌 54편 — 우리 화학과의 거리를 앞세워 보여준다."""
    d = D.nd_survey()
    if not d:
        abort(404)
    return render_template("nd_survey.html", active="nd", d=d, LAB=D.SYSCLASS_LABEL)


@app.route("/benchmarks")
def benchmarks():
    """외부 재현 표적 + 덱 정정 원장. 우리 값과 **섞이지 않게** 별도 페이지로 분리한다."""
    b = D.external_benchmarks()
    if not b:
        abort(404)
    # ⚠ 힘 벤치는 **물성이 아니라 방법**이다 — 위원회 기준선과 같은 축에 둔다.
    #   UMA 단독 수치만 보이면 "3.6 % 면 좋은가?" 를 판단할 눈금이 없다. 같은 프레임의
    #   SevenNet-0 행이 같이 있어야 softening 이 아키텍처가 아님이 읽힌다 (T1b).
    return render_template("benchmarks.html", active="bench", b=b,
                           ledger=D.deck_correction_ledger(),
                           revisions=D.verdict_revisions(),
                           committee=D.mlip_committee(),
                           force_bench=D.uma_force_benchmark(),
                           lit_have={p["id"] for p in D.list_papers()},
                           talks_have={t["id"] for t in D.list_talks()})


@app.route("/literature")
def literature():
    papers = D.list_papers()
    talks = D.list_talks()
    counts = {"all": len(papers),
              "dft": sum(1 for p in papers if p["track"] == "dft"),
              "dem": sum(1 for p in papers if p["track"] == "dem"),
              "talk": len(talks),
              # 카운트는 **완성 digest 만** 헤드라인으로 쓴다 (뼈대는 스스로 인용을 금지한다).
              "skeleton": sum(1 for p in papers if p["skeleton"]),
              "ban": sum(1 for p in papers if p["ban_n"])}
    counts["full"] = counts["all"] - counts["skeleton"]
    pi_counts = {}
    for it in papers + talks:
        for k in it.get("pis", []):
            pi_counts[k] = pi_counts.get(k, 0) + 1
    pis = [dict(p, n=pi_counts.get(p["key"], 0)) for p in D.PI_REGISTRY if pi_counts.get(p["key"])]
    pis.sort(key=lambda x: (not x["our"], -x["n"]))
    tmeta = D.topic_meta()
    tcounts = {k: sum(1 for p in papers if k in p["topics"]) for k in tmeta}
    # 🆕 최근 30일 — 정렬만으로는 "새로 들어온 것"이 안 보인다(215장 그리드의 첫 줄일 뿐).
    #   ⚠ 오늘 날짜로 재므로 **손으로 쓴 목록이 아니다** — 시간이 지나면 저절로 비워진다.
    from datetime import timedelta as _td
    cut = (_dt.now().date() - _td(days=30)).isoformat()
    recent = [p for p in papers if p["digested"] and p["digested"] >= cut][:12]
    return render_template("literature.html", active="lit", papers=papers,
                           count=len(papers), counts=counts, talks=talks,
                           recent=recent, recent_days=30,
                           tmeta=tmeta, tcounts=tcounts, tprimer=D.topic_primer(),
                           pis=pis, PI=D.PI_BY_KEY, figcount=D.papers_with_figures())


@app.route("/api/lit-index")
def api_lit_index():
    """/literature 의 **검색 색인**(그림·표 캡션 + 내 코멘트) — 페이지 밖으로 뺀 것.

    왜 별도 라우트인가: 종전에는 카드마다 `data-fig`(=279 KB)·`data-cmt` 를 HTML 에
      구워 넣어 /literature 한 장이 899 KB 였다. 색인은 **검색을 시작해야** 필요하므로
      첫 입력 때 한 번 받아 온다.

    ⛔ 못 하는 것: 검색을 서버에서 하지 않는다. 거르는 일은 여전히 브라우저가 한다 —
      이 라우트는 색인을 옮기기만 한다(랭킹·형태소 분석 없음).
    """
    return jsonify({"fig": D.paper_figure_search(), "cmt": D.paper_comment_search()})


# ── API (구조뷰 / 차트 / 원본) ──────────────────────────
@app.route("/api/structure/<path:fn>")
def api_structure(fn):
    return send_from_directory(D.DB / "structures", fn)


@app.route("/api/csv/<path:rel>")
def api_csv(rel):
    # ⛔ 2026-08-14 (Codex Round-3 P0-3) — 정책이 headline 에만 걸려 있어서
    #   화면에서 숨긴 artifact 를 이 경로로 그냥 받을 수 있었다. 이제 공통 resolver 를 탄다.
    # ⛔ 2026-09-07 — resolve 는 `db/…` 로 물어보면서 envelope 에는 접두 없는 rel 을
    #   넘기고 있었다. 봉투의 `artifact` 는 인용 시 지위를 값에 붙들어 두는 식별자인데
    #   그 값이 원장의 source_path(`db/properties/…`)와 **달라서** 대조가 안 됐다.
    #   한 번만 정규화해서 두 곳에 같은 경로를 쓴다.
    gov_rel = rel if str(rel).startswith("db/") else f"db/{rel}"
    v = AP.resolve(gov_rel, request.args)
    if not v["allowed"]:
        return jsonify({"error": v["reason"], "needs": v["needs"],
                        **AP.envelope(gov_rel, v)}), 403
    out = D.read_csv(rel)
    if v["governed"]:
        out = {**out, "_artifact_status": AP.envelope(gov_rel, v)}
    return jsonify(out)


@app.route("/api/file/<path:rel>")
def api_file(rel):
    """개념 문서 첨부 파일 서빙. ?dl=1 이면 다운로드(첨부), 아니면 인라인 미리보기.

    ⚠ docs/ · db/ 안으로만 (data.safe_repo_path 가 경로 탈출·심볼릭 탈출 차단).
    """
    p = D.safe_repo_path(rel)
    if p is None:
        abort(404)
    # cascade artifact 는 원장의 use_scope 를 따른다 (archive=1 / view=diagnostic).
    v = AP.resolve(rel, request.args)
    if not v["allowed"]:
        return jsonify({"error": v["reason"], "needs": v["needs"],
                        **AP.envelope(rel, v)}), 403
    return send_from_directory(p.parent, p.name,
                               as_attachment=bool(request.args.get("dl")),
                               download_name=p.name)


@app.route("/api/note-image", methods=["POST"])
def api_note_image():
    """메모·코멘트에 붙일 그림 업로드 → {"url"}.

    붙여넣기(Ctrl+V)한 캡처가 주 용도라 **multipart 와 data:URL 둘 다** 받는다.
    브라우저가 클립보드 그림을 File 로 주기도 하고 base64 문자열로 주기도 한다.

    ⛔ 확장자는 **매직바이트**로 정한다 — 클라이언트가 보낸 MIME 을 안 믿는다.
    """
    g = _guard_mutation()
    if g:
        return g
    blob, kind = b"", ""
    f = (request.files.get("file") if request.files else None)
    if f is not None:
        blob, kind = f.read(), (f.mimetype or "")
    else:
        d = request.get_json(silent=True) or {}
        raw = str(d.get("data") or "")
        if raw.startswith("data:"):
            head, _, b64 = raw.partition(",")
            kind = head[5:].split(";")[0]
            import base64
            import binascii
            try:
                blob = base64.b64decode(b64, validate=True)
            except (ValueError, binascii.Error):
                return jsonify({"error": "base64 를 못 읽었다"}), 400
    r = D.save_note_image(blob, kind)
    if r.get("error"):
        return jsonify(r), 400
    return jsonify(r)


@app.route("/api/note-image/<name>")
def api_note_image_get(name):
    """저장된 메모 그림. 이름이 규격(해시+확장자)이 아니면 404 — 경로 탈출 차단."""
    p = D.note_image_path(name)
    if p is None:
        abort(404)
    return send_from_directory(p.parent, p.name, max_age=31536000)


@app.route("/api/concept-upload/<cid>", methods=["POST"])
def api_concept_upload(cid):
    """개념 문서 드래그 업로드. 저장 후 페이지 새로고침이 첨부를 다시 수집한다."""
    g = _guard_mutation()
    if g:
        return g
    r = D.save_concept_upload(cid, request.files.getlist("file"))
    if r.get("error"):
        abort(404)
    return jsonify(r)


def _paper_cmt_index(rel):
    """그림 코멘트가 바뀌면 /literature 카드의 검색 색인(data-cmt)도 같이 줘야 한다.

    ⚠ 그 색인은 페이지 HTML 에 **구워져** 나가므로, 방금 단 코멘트는 새로고침 전까지
      검색에 안 걸렸다 (1저자 신고 2026-08-06: "캡션7 처럼 comment1 이렇게 뜨게").
      코멘트를 읽을 때마다 그 논문의 최신 색인을 같이 실어 보내 화면이 스스로 맞추게 한다.
    """
    seg = rel.split("/")
    slug = None
    if rel.startswith("litdb/figures/") and len(seg) == 4:
        slug = seg[2]                                   # litdb/figures/<slug>/<file>
    elif (len(seg) == 3 and seg[0] == "litdb"
          and seg[1] in ("papers", "talks") and seg[2].endswith(".md")):
        slug = seg[2][:-3]                              # litdb/papers/<slug>.md — 본문 여백 메모
    if slug is None:
        return None
    return {"slug": slug, "cmt": D.paper_comment_search().get(slug, "")}


#: 메모·코멘트에 붙일 수 있는 그림 — **우리가 저장한 이름 규격만** 허용한다.
#: 임의 URL 을 허용하면 메모 한 줄로 외부 요청을 만들 수 있다 (comments.js 와 같은 규격).
_NOTE_IMG = re.compile(
    r"!\[([^\]\n]*)\]\((/api/note-image/[0-9a-f]{32}\.(?:png|jpg|gif|webp))\)")


def note_html(text: str) -> str:
    """메모·코멘트 한 줄을 **표시용 HTML** 로. 결속까지 마쳐서 낸다.

    ⛔⛔ 왜 서버가 그리나 (Codex BI-3 P0-3, 2026-09-09)
      `comments.js` 의 `inline()` 이 브라우저에서 따로 `**0.199**` → `<b>0.199</b>` 를
      만들고 있었다. 서버 `_mdlite` 는 고쳤는데 **메모 표시 경로에는 전파되지 않았다** —
      즉 파서가 둘이고 판정도 둘이었다. 실측: 같은 입력이 서버에선 결속되고
      메모에선 `unbound 1` 이었다.
      ⇒ **편집용 원문(`text`)은 그대로 두고, 표시용 HTML 은 여기서만 만든다.**

    ⛔ 못 하는 것: 블록 문법(목록·제목)은 `_mdlite` 가 하는 만큼만. 메모는 문서가 아니다.
    """
    # ⛔ BI-4 P2 (2026-09-09) — 여기서 `annotate_claims` 를 **한 번 더** 불렀다.
    #   그런데 `_mdlite` 가 이미 `_bind_claims` 를 부른다(같은 파일 위쪽). 그래서
    #   실측으로 `0.199` 하나에 `data-claim` 2개 · `.claim-mark` 2개가 중첩됐다.
    #   인용 금지 누출은 아니지만, **결속 건수를 표시 위치 수로 읽으면 지표가 부푼다**
    #   — 그게 §3-1 에서 우리가 자백한 "분모 부풀리기" 와 같은 실수다.
    #   ⇒ 결속은 `_mdlite` 한 곳에서만 붙는다. 여기서는 이미지만 얹는다.
    s = str(_mdlite(text))                       # esc + code/bold/mark/… + **결속**
    return _NOTE_IMG.sub(
        lambda m: '<img class="note-img" src="%s" alt="%s" loading="lazy">'
                  % (m.group(2), m.group(1)), s)


def _with_note_html(obj):
    """코멘트 응답의 모든 item 에 `html` 을 붙인다 (편집용 `text` 는 보존)."""
    if isinstance(obj, dict):
        for k in ("items", "history"):
            if isinstance(obj.get(k), list):
                for it in obj[k]:
                    if isinstance(it, dict) and it.get("text") is not None:
                        it["html"] = note_html(it["text"])
        if obj.get("text") is not None and "html" not in obj:
            obj["html"] = note_html(obj["text"])
        if isinstance(obj.get("item"), dict):
            _with_note_html(obj["item"])
    return obj


@app.route("/api/comments/<path:rel>", methods=["GET", "POST", "PATCH"])
def api_comments(rel):
    """파일 코멘트 읽기/달기/고치기 (Notion 식 💬 · 📝). 대상은 실존 repo 파일만.

    PATCH `{id, text}` = 글 고치기. 옛 글은 지우지 않고 item.history 에 쌓인다.
    """
    if request.method == "GET":
        return jsonify(_with_note_html(
            {"rel": rel, "items": D.file_comments(rel),
             "paper": _paper_cmt_index(rel)}))
    g = _guard_mutation()
    if g:
        return g
    d = request.get_json(silent=True) or {}
    if request.method == "PATCH":
        r = D.edit_file_comment(rel, str(d.get("id", "")), str(d.get("text", "")))
        if r.get("error"):
            return jsonify(r), 400
        r["paper"] = _paper_cmt_index(rel)
        return jsonify(_with_note_html(r))
    # anchor = 본문 여백 메모가 붙은 자리(고른 글/문단 앞머리). 그림 코멘트는 빈 값.
    r = D.add_file_comment(rel, str(d.get("text", "")), str(d.get("who", "")),
                           str(d.get("anchor", "")))
    if r.get("error"):
        return jsonify(r), 400
    # ⚠ GET 과 **같은 모양**으로 돌려준다. 앞 판은 POST 에만 paper 색인이 빠져 있어
    #   화면이 POST 응답으로 색인을 갱신하려 하면 조용히 아무 일도 안 났다
    #   (뒤따르는 GET 이 덮어 줘서 증상이 안 보였을 뿐이다).
    r["paper"] = _paper_cmt_index(rel)
    return jsonify(_with_note_html(r))


@app.route("/api/highlights/<path:rel>", methods=["GET", "POST", "DELETE"])
def api_highlights(rel):
    """형광펜 읽기/칠하기/지우기. 메모와 **저장소가 다르다** (data.HIGHLIGHTS_PATH).

    POST `{text, color}` · DELETE `{id}`. 같은 글을 다시 칠하면 색만 바뀐다.
    """
    if request.method == "GET":
        return jsonify({"rel": rel, "items": D.file_highlights(rel)})
    g = _guard_mutation()
    if g:
        return g
    d = request.get_json(silent=True) or {}
    if request.method == "DELETE":
        r = D.del_file_highlight(rel, str(d.get("id", "")))
    else:
        r = D.add_file_highlight(rel, str(d.get("text", "")), str(d.get("color", "yellow")))
    return (jsonify(r), 400) if r.get("error") else jsonify(r)


@app.route("/api/comments/<path:rel>", methods=["DELETE"])
def api_comment_delete(rel):
    """?id=<cid> 로 한 건 삭제. path 에 넣으면 파일 경로와 섞여 파싱이 애매해진다."""
    g = _guard_mutation()
    if g:
        return g
    r = D.del_file_comment(rel, request.args.get("id", ""))
    return (jsonify(r), 400) if r.get("error") else jsonify(r)


@app.route("/api/file-rename", methods=["POST"])
def api_file_rename():
    """업로드 파일 이름 바꾸기. 파일을 옮기고 **문서에 적힌 경로도 같이** 고친다.

    uploads 밖은 data.rename_upload 가 거절한다 (도구가 같은 이름으로 다시 만들어
    두 벌이 되는 걸 막는다) — 400 으로 사유를 그대로 돌려준다.
    """
    g = _guard_mutation()
    if g:
        return g
    d = request.get_json(silent=True) or {}
    r = D.rename_upload(str(d.get("rel", "")), str(d.get("name", "")))
    return (jsonify(r), 400) if r.get("error") else jsonify(r)


@app.route("/notes")
def notes_page():
    """메모·코멘트를 **날짜별로** 모아 보는 화면 (1저자 요청 2026-08-17).

    여백 메모(📝)는 읽던 문서 옆에 흩어져 있어서, 나중에 "그때 뭐라고 적었더라"
    를 찾으려면 문서를 하나씩 열어야 했다. 날짜로 묶어 두면 그날 무엇을 읽고
    무엇을 판단했는지가 한 화면에 남는다.
    """
    groups = D.notes_by_date()
    return render_template("notes.html", active="notes", groups=groups,
                           total=sum(g["n"] for g in groups),
                           q=request.args.get("q", "").strip())


@app.route("/files")
def files_gallery():
    q = request.args.get("q", "").strip()
    kind = request.args.get("kind", "").strip()
    used = request.args.get("used", "").strip()
    folder = request.args.get("folder", "").strip()
    cmt = request.args.get("cmt", "").strip()
    old = request.args.get("old", "").strip()
    fs = D.gallery_files(q, kind, used, folder, cmt, old)
    # 옛 판(SUPERSEDED/RETRACT) 개수를 탭에 찍는다 — 접혀 있다는 사실이 보여야 한다.
    n_old = len(D.gallery_files(q, kind, used, folder, cmt, "yes")) if old != "yes" else len(fs)
    return render_template("files.html", active="files", files=fs, q=q, kind=kind,
                           used=used, folder=folder, cmt=cmt, old=old, n_old=n_old,
                           days=D.gallery_days(fs),
                           folders=D.gallery_folders(), ccounts=D.comment_counts())


@app.route("/api/property/<name>")
def api_property(name):
    p = D.DB / "properties" / f"{name}.json"
    rel = f"db/properties/{name}.json"
    v = AP.resolve(rel, request.args)
    if not v["allowed"]:
        return jsonify({"error": v["reason"], "needs": v["needs"],
                        **AP.envelope(rel, v)}), 403
    d = D._load_json(p) if p.exists() else None
    if d is None:            # 없거나 깨진 JSON → 500 대신 404 (silent 500+traceback 방지)
        abort(404)
    if v["governed"] and isinstance(d, dict):
        d = {**d, "_artifact_status": AP.envelope(rel, v)}
    return jsonify(d)


@app.route("/api/paper/<pid>")
def api_paper(pid):
    # papers/ 우선, 없으면 talks/ (발표 덱). 같은 모달 JS 를 그대로 쓰기 위한 폴백.
    # ⚠ `_` 접두는 목록에서 빠지는 것(서식·초안)이다 — /talk 은 이미 막고 있었는데
    #   이 API 만 안 막아 `/api/paper/_TEMPLATE` 이 200 이었다. 같은 가드로 맞춘다.
    if pid.startswith("_"):
        abort(404)
    p = D.LITDB / "papers" / f"{pid}.md"
    if not p.exists():
        p = D.LITDB / "talks" / f"{pid}.md"
    if not p.exists():
        abort(404)
    # ⚠ litdb 는 **남의 문서**다 (origin="external"). 우리 계 이름이 근처에 없는 일치는
    #   `suspect` 로 두고 감싸지 않는다 — 실측 오탐 17/18 (deng2026 H₂O 흡착 −0.199 eV 등).
    #   감싸면 원장이 남의 논문으로 부풀고 "미결속 0" 이 더 그럴듯하게 틀린 수가 된다.
    html = md_html(p.read_text(encoding="utf-8", errors="ignore"), origin="external")
    # 크로핑된 논문 그림 — 본문의 "Fig. 5e" 를 브라우저에서 링크로 바꿔 여백에 띄운다.
    # ⚠ rel 을 같이 준다 — 여백 메모(docnote.js)가 이 경로에 붙는다. papers/ 인지
    #   talks/ 인지는 **서버만 안다**. 화면이 papers/ 로 찍으면 발표덱 메모가 조용히 실패한다.
    return jsonify({"id": pid, "html": html, "figures": D.paper_figures(pid),
                    "rel": p.relative_to(D.ROOT).as_posix()})


@app.route("/paper/<slug>")
def paper_page(slug):
    """논문 digest **전체 페이지** (모달 말고 정독용) — /talk 과 같은 자리.

    왜 필요한가: /literature 의 모달은 훑기용인데 digest 는 그보다 크다
      (qian2025 58 KB · wu2026_ta 63 KB). 발표덱 7건에는 '전체 페이지' 버튼이
      있었고 논문 215편에는 라우트 자체가 없었다.

    ⛔ 이 페이지가 못 하는 것
      · 인용 가능 여부를 판정하지 않는다. 머리의 제한 배지는 **digest 산문을
        문자열로 훑은 것**이고(D.paper_notice), 원장(citation_hazards.json)이 아니다.
        배지가 없다고 인용 가능이라는 뜻이 아니다.
      · digest 를 요약하지 않는다 — 본문 전체를 그대로 편다.
    """
    p = D.LITDB / "papers" / f"{slug}.md"
    if not p.exists() or slug.startswith("_"):
        abort(404)
    md = p.read_text(encoding="utf-8", errors="ignore")
    title = md.splitlines()[0].lstrip("# ").strip() if md.startswith("#") else slug
    notice = D.paper_notice(slug)
    return render_template(
        "paper.html", active="lit", title=D.title_plain(title),
        # ⚠ litdb 는 남의 문서다 — origin="external" (결속 매처가 우리 값으로 안 세게)
        content=md_html(md, ("tables", "fenced_code", "toc"), origin="external"),
        parent={"url": "/literature", "label": "문헌 · litdb"},
        paper_notice=notice, paper_rel=p.relative_to(D.ROOT).as_posix(),
        figures=D.paper_figures(slug),
        subtitle=f"litdb/papers/{slug}.md · digest 원문")


@app.route("/talk/<slug>")
def talk_page(slug):
    """학회 발표자료 digest **전체 페이지** (모달 말고 정독용).

    왜 별도 라우트인가: /literature 의 모달은 훑기용이라 40 KB 넘는 digest 를
      읽기 어렵다. 논문세미나를 준비할 때는 §99(구술 판독)처럼 긴 절을 **목차와 함께**
      펼쳐 놓고 봐야 한다.

    ⛔ 이 페이지가 못 하는 것
      · 인용 가능 여부를 화면이 판정하지 않는다 — manifest 의 `citable` 이 정본이고,
        아래 배지는 그 값을 **읽어서** 보일 뿐이다.
      · 발표자 발언으로 승격시키지 않는다. `[STT]` 는 STT 문자열이라는 뜻이다.
    """
    import json as _json
    p = D.LITDB / "talks" / f"{slug}.md"
    if not p.exists() or slug.startswith("_"):
        abort(404)
    md = p.read_text(encoding="utf-8", errors="ignore")

    # manifest 가 있으면 승격 상태를 머리에 띄운다. **없으면 없다고 말한다** —
    # 조용히 빈 배지를 내면 "인용 가능" 으로 오해된다.
    mf = D.LITDB / "talks" / "_transcripts" / f"{slug}_source_manifest.json"
    man = None
    if mf.exists():
        try:
            man = _json.loads(mf.read_text(encoding="utf-8"))
        except Exception:
            man = {"_error": "manifest 를 읽지 못했다"}

    title = md.splitlines()[0].lstrip("# ").strip() if md.startswith("#") else slug
    return render_template(
        "doc.html", active="lit", title=f"🎤 {title}",
        # ⚠ 발표자료도 남의 문서다 (litdb) — origin="external"
        content=md_html(md, ("tables", "fenced_code", "toc"), origin="external"),
        parent={"url": "/literature", "label": "문헌 · 발표자료"},
        talk_manifest=man,
        subtitle=f"litdb/talks/{slug}.md · 인용 규율은 litdb/talks/README.md")


@app.route("/seminar/deck")
def seminar_deck():
    """세미나 pptx 내려받기.

    ⚠ /api/file 로는 못 준다 — safe_repo_path 의 허용 뿌리가 docs·db·litdb/figures 라
      kb/ 는 애초에 막혀 있다. 허용 목록을 넓히면 kb 전체(리뷰 노트 포함)가 열리므로,
      이 파일 하나만 주는 전용 라우트를 판다. (2026-08-06 링크 404 수정)

    ?v= 는 **화이트리스트 키**만 받는다 (D.SEMINAR_DECKS). 경로가 아니므로 주입이 성립하지 않는다.
    """
    key = request.args.get("v", "release")
    entry = D.SEMINAR_DECKS.get(key)
    if not entry:
        abort(404)
    p = D.KB / "seminars" / entry[0]
    if not p.is_file():
        abort(404)
    return send_from_directory(p.parent, p.name, as_attachment=True, download_name=p.name)


@app.route("/seminar")
def seminar():
    """연구세미나 — **정본 덱(29장)과 그 부속 문서**를 한 화면에 모은다.

    ⚠ 이 화면은 뷰어다. 정본은 kb/seminars/ 의 파일이고, 진행표는 대본을 **파싱해서**
      만든다 — 하드코딩하면 대본을 고쳤을 때 화면이 조용히 어긋난다.
      (2026-08-11 개편: 옛 spec·존재하지 않는 덱을 가리키고 있던 것을 정본으로 교체)
    """
    import os
    base = D.KB / "seminars"

    docs = []
    for key, label, path, note in D.SEMINAR_DOCS:
        if not path.is_file():
            continue
        docs.append({"key": key, "label": label, "note": note,
                     "rel": path.relative_to(D.ROOT).as_posix(),
                     "kb": os.path.getsize(path) // 1024,
                     "html": D.md_to_html(path.read_text(encoding="utf-8"))})
    if not docs:
        abort(404)

    script_md = base / D.SEMINAR_SCRIPT
    runsheet = D.seminar_runsheet(script_md.read_text(encoding="utf-8")) if script_md.is_file() else []
    total_sec = sum(p["seconds"] for p in runsheet)

    decks = []
    for key, (name, note) in D.SEMINAR_DECKS.items():
        p = base / name
        if p.is_file():
            decks.append({"key": key, "name": name, "note": note,
                          "kb": os.path.getsize(p) // 1024,
                          "primary": key == "release"})
    return render_template("seminar.html", active="seminar",
                           docs=docs, runsheet=runsheet,
                           total_min=total_sec // 60, total_sec=total_sec % 60,
                           n_body=sum(len(p["slides"]) for p in runsheet),
                           decks=decks, rerank=D.SEMINAR_RERANK_AUDIT,
                           talkprep=D.SEMINAR_TALK_PREP)


@app.route("/glossary")
def glossary():
    gpapers = {g["id"]: D.glossary_papers(g["id"]) for g in G.GLOSSARY}
    return render_template("glossary.html", active="glossary",
                           cats=G.by_category(), cat_order=G.CATS_G,
                           concepts=D.concept_ids(), gpapers=gpapers)


@app.route("/concept/<cid>")
def concept(cid):
    md = D.read_concept(cid)
    if md is None:
        abort(404)
    term = next((g for g in G.GLOSSARY if g["id"] == cid), None)
    # 같은 카테고리 이웃 개념(=상세 문서 있는 것) 링크
    siblings = []
    if term:
        have = D.concept_ids()
        siblings = [g for g in G.GLOSSARY
                    if g["cat"] == term["cat"] and g["id"] != cid and g["id"] in have]
    # ★ 본문은 **서버가 한 번만** 그린다 (Codex BI P0-2b · 2026-09-08). 종전에는
    #   이걸 "fallback" 이라 부르고 브라우저 marked 가 다시 그렸는데, 그 재렌더가
    #   서버 결속을 덮었다. 이제 이게 유일한 렌더다 — 콜아웃·수식보호·결속 포함.
    # frontmatter 는 **본문에서 빼되 화면으로 올린다** (P0-34). 용어집에 안 걸린 문서는
    #   h1 이 슬러그(`msd_reading`)였는데, frontmatter title 이 있으면 그걸 제목으로 쓴다.
    _fm = split_frontmatter(md)[0]
    return render_template("concept.html", active="glossary", cid=cid,
                           docmeta=doc_badges(_fm), docmeta_title=_fm.get("title"),
                           term=term, siblings=siblings, body_html=doc_html(md),
                           papers=D.glossary_papers(cid),
                           attachments=(_att := D.concept_attachments(cid)),
                           att_days=D.gallery_days(_att), ccounts=D.comment_counts())


@app.route("/api/concept/<cid>")
def api_concept(cid):
    md = D.read_concept(cid)
    if md is None:
        abort(404)
    # ⚠ `markdown` 은 **결속이 없는 원문**이다. 화면에 그대로 그리면 결속이 사라진다
    #   (2026-09-08 까지 concept.html 이 정확히 그렇게 했다 — Codex BI P0-2b).
    #   그래서 서버가 그린 `html` 을 같이 보낸다. 새 소비자는 `html` 을 써라.
    return jsonify({"id": cid, "markdown": md, "html": doc_html(md),
                    "⚠_markdown": "결속 없는 원문이다. 화면에 그리려면 html 을 쓴다."})


# ── 작업 로그 (기록·저장) ─────────────────────────────
JOURNAL = D.ROOT / "webapp" / "journal.jsonl"

import records_view as RV                                        # noqa: E402


@app.template_filter("closedaxis")
def _closedaxis(html):
    """**마감된 축의 수**에 표식을 얹는다 (묶음 H · P0, 2026-09-09).

    마감 결정이 축 전체를 닫았는데 스캐너 어휘는 레지스트리 수 둘뿐이라, 기록 화면이
    금지된 수를 **초록인 채로** 권하고 있었다 (/requests 의 `저온 구간 Ea = 0.2241` ·
    /todo 의 `구간 Ea 600→800 0.222` · handoff 의 `✅ 600→800 구간 Ea = 0.222 eV`).
    판정·숫자는 여기서 짓지 않고 `records_view` 가 원장에서 파생시킨다.
    """
    return RV.mark_closed_axis(html)


@app.template_filter("kindlabel")
def _kindlabel(raw):
    """저널 kind → 화면 어휘. ⛔ 원문 journal.jsonl 은 고치지 않는다 (표시층만)."""
    return RV.kind_label(raw)


def _load_journal():
    entries = []
    if JOURNAL.exists():
        for line in JOURNAL.read_text(encoding="utf-8", errors="ignore").splitlines():
            try:
                entries.append(json.loads(line))
            except Exception:
                pass
    return list(reversed(entries))


def _handoffs():
    """kb/results/*.md → 카드. 정렬은 **파일명 역알파벳이 아니라 날짜 역순**이다.

    종전에는 `sorted(reverse=True)` 라 화면 첫 줄이 vgcf·uma·slide2 였다 —
    94장이 3열로 깔리는데 무엇이 최근인지 알 길이 없었다.
    ⛔ 파일은 하나도 빼지 않는다. 화면에서 접는 것과 지우는 것은 다르다.
    """
    rd = D.KB / "results"
    if not rd.exists():
        return []
    return RV.handoff_cards(sorted(rd.glob("*.md")), first_line=RV.first_sentence)


#: journal 이 비어 있는 구간에 무엇이 있었는지 — **여기서 지어내지 않는다.**
#: 커밋 수는 조사 실측(`git log --since=2026-08-26 --until=2026-09-08 --oneline | wc -l`)
#: 이고, 다른 구간이 생기면 그 구간은 "기록 없음" 만 찍힌다(수를 만들지 않는다).
JOURNAL_GAPS = {("2026-08-26", "2026-09-07"): "커밋 806개"}


@app.route("/log")
def log():
    """작업 기록 — **수기 일지다.** 전수 기록이 아니다.

    ⚠ 타임라인은 `ts` 로 정렬한다. journal.jsonl 자체가 시간순이 아니라서(어긋난 쌍 3개)
      줄 순서를 뒤집기만 하면 08-25 구간이 15:40→15:00→13:30→14:30 으로 나왔다.
    ⚠ 기록이 없는 구간은 **회색 줄로 명시한다.** 비어 있는 것과 일이 없었던 것은
      다른 말이다 — 08-26~09-07 에 커밋 806개가 있었는데 기록은 0건이다.
    """
    entries = _load_journal()
    return render_template("log.html", active="log",
                           entries=entries,
                           groups=RV.journal_groups(entries, JOURNAL_GAPS),
                           kinds=RV.KIND_ORDER,
                           handoffs=_handoffs())


#: 주간 정리 문서가 사는 곳 — `kb/reports/weekly_YYYY_MM_DD.md`. 시험이 tmp 로 바꿔 끼운다.
WEEKLY_DIR = D.KB / "reports"
_WEEKLY_RE = re.compile(r"^weekly_(\d{4}_\d{2}_\d{2})\.md$")


def _weekly_docs() -> list[dict]:
    """→ [{key, label, path, title}] **최신순**. 규약(`weekly_YYYY_MM_DD.md`) 밖 파일은 목록에 안 든다.

    ⚠ title 은 frontmatter 에서 읽고, 없으면 파일 stem 을 쓴다 — 지어내지 않는다.
    """
    out = []
    if not WEEKLY_DIR.is_dir():
        return out
    for p in WEEKLY_DIR.glob("weekly_*.md"):
        m = _WEEKLY_RE.match(p.name)
        if not m or not p.is_file():
            continue
        meta, _ = split_frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
        out.append({"key": m.group(1), "label": m.group(1).replace("_", "-"),
                    "path": p, "title": meta.get("title") or p.stem})
    return sorted(out, key=lambda r: r["key"], reverse=True)


@app.route("/weekly")
def weekly():
    """주간 정리 — 작업 기록(/log)의 **하위**. `?w=YYYY_MM_DD` 로 특정 주, 없으면 최신.

    왜 생겼나 (2026-09-14): 주간보고를 쓸 때 "지난주 뭐 했나" 를 git log 471건에서 다시 캐고
    있었다. 정리는 kb 문서(`kb/reports/weekly_*.md`)에 두고 화면은 그것을 **읽기만** 한다 —
    `/todo`·`/kb` 와 같은 경로(md_html → doc.html)라 새 렌더러가 아니다.

    ⛔ 이 라우트가 **못 하는 것**
      · 문서를 만들지 않는다 — 없으면 "없다" 고 말한다(빈 화면이 아니라).
      · 값을 판정하지 않는다 — 문서가 인용한 숫자의 지위는 `md_html` 의 결속이 붙인다
        (같은 판정기 · 서버 한 곳). 문서에 없는 숫자를 화면이 만들어 붙이지 않는다.
      · 파일명 규약 밖의 문서는 안 연다 — `?w=` 는 `YYYY_MM_DD` 만 받고 나머지는 404 다.
    ⚠ 인자 없는 GET 이라 결속 스캔(`test_webapp._html_routes`)에 **자동으로** 든다. 표면별
      음성시험은 `tests/test_weekly.py` 가 합성 문서(철회값)로 한다 — 실제 주간 문서에는
      결속 대상 문자열이 없어서 `must` 목록 방식으로는 검사가 공허하다.
    """
    from flask import request
    docs = _weekly_docs()
    w = request.args.get("w", "").strip()
    parent = {"url": "/log", "label": "✎ 작업 기록"}
    if w:
        if not re.fullmatch(r"\d{4}_\d{2}_\d{2}", w):
            abort(404)
        doc = next((d for d in docs if d["key"] == w), None)
        if doc is None:
            abort(404)
    else:
        doc = docs[0] if docs else None
    if doc is None:
        return render_template(
            "doc.html", active="weekly", title="📅 주간 정리", parent=parent,
            content=Markup('<div class="doc"><b>주간 정리 문서가 없다</b> — '
                           '<code>kb/reports/weekly_YYYY_MM_DD.md</code> 를 만들면 여기 뜬다.</div>'),
            subtitle="kb/reports/weekly_*.md · 문서 0건")
    text = doc["path"].read_text(encoding="utf-8", errors="ignore")
    meta, _ = split_frontmatter(text)
    others = [d for d in docs if d["key"] != doc["key"]]
    switch = ""
    if others:
        switch = ('<div class="doc" style="border-left:4px solid #7c3aed;padding:10px 16px;margin-bottom:14px">'
                  '<b>다른 주</b> · ' + " · ".join(
                      f'<a href="/weekly?w={escape(d["key"])}">{escape(d["label"])}</a>' for d in others)
                  + "</div>")
    return render_template(
        "doc.html", active="weekly", parent=parent,
        title="📅 " + (meta.get("title") or doc["title"]),
        content=Markup(switch) + Markup(md_html(text, ("tables", "fenced_code", "toc"))),
        docmeta=doc_badges(meta), toc=True,
        subtitle=f"kb/reports/{doc['path'].name} · 원본은 이 파일이다 — 화면은 읽기용이다 · "
                 "확정값의 지위는 원장이 정한다")


@app.route("/api/log", methods=["POST"])
def api_log():
    from flask import request
    g = _guard_mutation()
    if g:
        return g
    d = request.get_json(force=True, silent=True)
    if not isinstance(d, dict):          # 본문이 list/str/int 여도 500 대신 400
        return jsonify({"ok": False, "err": "body must be a JSON object"}), 400

    def _s(v, default=""):
        return v if isinstance(v, str) else default

    kind = _s(d.get("kind"), "note") or "note"
    comp = _s(d.get("comp"))
    if comp and comp not in D.COMPOSITIONS:   # 빈 문자열(=조성 미지정)은 허용
        return jsonify({"ok": False, "err": f"unknown comp '{comp[:40]}'"}), 400
    rec = {"ts": _dt.now().isoformat(timespec="minutes"),
           "kind": kind[:40], "comp": comp,
           "text": _s(d.get("text")).strip()}
    if not rec["text"]:
        return jsonify({"ok": False, "err": "empty"}), 400
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return jsonify({"ok": True, "entry": rec})


@app.route("/api/handoff/<hid>")
def api_handoff(hid):
    """handoff 문서 본문 (모달용).

    ⚠ 없는 hid 도 **JSON 으로** 답한다. Flask 기본 404 는 HTML 이라 모달의
      `r.json()` 이 던지고 '로딩...' 상태로 굳었다 (조사 handoff-modal-404-hangs).
    ⚠ 마감된 축의 수에는 표식을 얹는다 — 이 경로가 실제 누출 지점이었다
      (`/api/handoff/b2o3_arrhenius_curvature_2026_08_23` 의 "✅ 600→800 구간 Ea = 0.222 eV").
    """
    f = D.KB / "results" / f"{hid}.md"
    if not f.exists():
        return jsonify({"id": hid, "error": f"문서를 못 읽었다 — kb/results/{hid}.md 없음",
                        "html": ""}), 404
    html = RV.mark_closed_axis(md_html(f.read_text(encoding="utf-8", errors="ignore")))
    return jsonify({"id": hid, "html": html})


@app.route("/health")
def health():
    return jsonify({"ok": True, "asset": _css_ver()})


if __name__ == "__main__":
    # 보안 기본값: 디버거 OFF·localhost 바인드. 자동리로드는 유지(디버거와 분리).
    # LAN 접근: FLASK_HOST=0.0.0.0 · 디버거: FLASK_DEBUG=1 (신뢰 네트워크에서만).
    _dbg = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host=os.environ.get("FLASK_HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", "5001")),
            debug=_dbg, use_reloader=True)
