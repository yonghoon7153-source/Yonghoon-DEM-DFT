"""content.py — 저장소의 마크다운/그림/CSV 를 읽어 화면용 자료구조로 만든다.

이 모듈은 **읽기만** 한다. 쓰기 함수는 없다 (없는 게 설계다 — README 의 "왜
읽기 전용인가" 참조). `wiki/raw/` 는 sha256 으로 봉인된 불변층이고,
`degradation-degeneracy/` 의 코드 트리는 게이트 리뷰 대상 code identity 라
웹에서 건드리면 기존 산출물이 무효가 된다.

원본(다른 브랜치 webapp/data.py)에서 가져온 것:
  · `safe_repo_path` 의 "허용 뿌리 + resolve + is_relative_to" 경로 탈출 차단
  · 마크다운 렌더에서 raw HTML 을 끄고, 그 다음 href/src scheme 을 다시 거르는 2중 방어
버린 것: db/*.json 도메인 모델, 첨부 자동연결 규칙, journal, 코멘트 저장소.
"""
from __future__ import annotations

import csv
import html as _html
import io
import json
import math
import re
from datetime import datetime
from pathlib import Path

try:
    import yaml
except Exception:  # PyYAML 이 없어도 앱은 뜬다 (frontmatter 만 얕게 읽는다)
    yaml = None

try:
    import markdown as _md
except Exception:
    _md = None

ROOT = Path(__file__).resolve().parent.parent          # 저장소 루트
WIKI = ROOT / "wiki"
FIGROOT = WIKI / "raw" / "figures"
MO = ROOT / "mode-observability"
GATE_DOC = ROOT / "degradation-degeneracy" / "docs" / "08_REVIEW_RESPONSE.md"

# Phase 1b 단독 스윕 차트의 입력. 이 파일이 **정본**이고 화면의 좌표는 사본이다.
SWEEP_CSV = MO / "results" / "phase1b" / "pvs_tracked.csv"

# /api/file 이 열어 주는 뿌리. 이 밖은 404 — 저장소 안이어도 안 준다.
_FILE_ROOTS = (WIKI / "raw" / "figures",)


# ─────────────────────────────────────────────────────────────────────────
# 경로 안전
# ─────────────────────────────────────────────────────────────────────────
def safe_file(rel: str) -> Path | None:
    """허용 뿌리 안의 **파일**만 돌려준다. 경로 탈출·심볼릭 탈출 차단.

    `..` 를 문자열로 막는 것으로는 부족하다 (심볼릭 링크가 뿌리 밖을 가리킬 수
    있다). resolve() 로 실제 경로를 얻은 뒤 뿌리와의 포함 관계를 본다.
    """
    rel = (rel or "").lstrip("/")
    if not rel or "\x00" in rel:
        return None
    for base in _FILE_ROOTS:
        try:
            p = (base / rel).resolve()
            b = base.resolve()
        except OSError:
            continue
        if p.is_relative_to(b) and p.is_file():
            return p
    return None


# ─────────────────────────────────────────────────────────────────────────
# frontmatter + 마크다운
# ─────────────────────────────────────────────────────────────────────────
_FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def split_frontmatter(text: str) -> tuple[dict, str]:
    m = _FM_RE.match(text or "")
    if not m:
        return {}, text or ""
    raw, body = m.group(1), (text or "")[m.end():]
    meta: dict = {}
    if yaml is not None:
        try:
            got = yaml.safe_load(raw)
            if isinstance(got, dict):
                meta = got
        except Exception:
            meta = {}
    if not meta:                                    # PyYAML 없거나 파싱 실패 시 얕은 파서
        for line in raw.splitlines():
            if ":" not in line or line.lstrip().startswith("#"):
                continue
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


# 마크다운 파서에서 raw HTML 을 끄고, 그 뒤 URL scheme 을 한 번 더 거른다.
# ⚠ raw HTML 을 껐다고 끝이 아니다 — 마크다운 링크 문법 자체가
#   `[x](javascript:alert(1))` 를 정상 링크로 만든다 (원본 리뷰 P2 의 실측 발견).
_URL_ATTR = re.compile(r"""(?P<a>\b(?:href|src)\s*=\s*)(?P<q>["'])(?P<v>[^"']*)(?P=q)""", re.I)
_URL_OK = re.compile(r"""^\s*(?:https?:|mailto:|/|\#|\./|\.\./|[^:]*$)""", re.I)


def _sanitize_urls(html: str) -> str:
    def _fix(m):
        v = (m.group("v") or "").strip()
        plain = _html.unescape(v).replace("\t", "").replace("\n", "").replace("\r", "")
        if _URL_OK.match(plain):
            return m.group(0)
        return f'{m.group("a")}{m.group("q")}#blocked-url{m.group("q")} data-blocked-url="1"'
    return _URL_ATTR.sub(_fix, html)


def md_html(text: str) -> str:
    """마크다운 → HTML. raw HTML 통과는 끈다 + href/src 를 허용 scheme 만 통과."""
    if _md is None:
        return "<pre>" + _html.escape(text or "") + "</pre>"
    # ⚠ attr_list 는 넣지 않는다 — `{: onclick="…" }` 로 임의 속성을 붙일 수 있어서
    #   raw HTML 을 끈 의미가 사라진다. digest 는 외부 PDF 요약본이라 100% 신뢰 대상이 아니다.
    md = _md.Markdown(extensions=["tables", "fenced_code", "sane_lists"])
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
    return _sanitize_urls(md.convert(text or ""))


# ─────────────────────────────────────────────────────────────────────────
# 페이지 등록부 (wikilink 해석의 정본)
# ─────────────────────────────────────────────────────────────────────────
# 디렉터리 → (종류 이름, URL 접두사)
_DIRS: dict[str, tuple[str, str]] = {
    "entities": ("entity", "/entity/"),
    "concepts": ("concept", "/concept/"),
    "questions": ("question", "/question/"),
    "guides": ("guide", "/doc/guides/"),
    "queries": ("query", "/doc/queries/"),
    "syntheses": ("synthesis", "/doc/syntheses/"),
    "comparisons": ("comparison", "/doc/comparisons/"),
    "raw/papers": ("paper", "/paper/"),
    "raw/transcripts": ("transcript", "/doc/raw/transcripts/"),
    "raw/articles": ("article", "/doc/raw/articles/"),
    "raw/repositories": ("repository", "/doc/raw/repositories/"),
}
_SKIP_NAMES = {"README", "SCHEMA", "CLAUDE", "AGENTS", "index", "log"}


def _mtime(p: Path) -> float:
    try:
        return p.stat().st_mtime
    except OSError:
        return 0.0


def scan_pages() -> dict[str, dict]:
    """`wiki/` 를 훑어 slug → 페이지 메타 사전을 만든다.

    요청마다 다시 훑는다 (파일이 정본 — 앱을 재시작하지 않아도 반영된다).
    파일 수가 수십 개라 비용이 문제되지 않는다.
    """
    pages: dict[str, dict] = {}
    for rel, (kind, prefix) in _DIRS.items():
        d = WIKI / rel
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.md")):
            if f.stem in _SKIP_NAMES:
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except OSError:
                continue
            meta, _body = split_frontmatter(text)
            slug = f.stem
            pages[slug] = {
                "slug": slug,
                "kind": kind,
                "dir": rel,
                "path": f,
                "relpath": f.relative_to(ROOT).as_posix(),
                "url": prefix + slug,
                "meta": meta,
                "title": str(meta.get("title") or _first_h1(_body) or slug),
                "description": str(meta.get("description") or ""),
                "updated": str(meta.get("updated") or meta.get("ingested") or meta.get("created") or ""),
                "mtime": _mtime(f),
                "bytes": f.stat().st_size if f.exists() else 0,
            }
    return pages


#: 본문 첫 `# 제목` — frontmatter 에 `title` 이 없는 문서의 이름.
_BODY_H1 = re.compile(r"^\s*#\s+(.+?)\s*$", re.M)


def _first_h1(body: str) -> str:
    """`raw/papers/` digest 는 frontmatter 에 `title` 을 두지 않는다.

    거기 있는 것은 `source_url`·`ingested`·`sha256` 뿐이고 (봉인 대상이라
    사람이 나중에 제목을 고칠 수 없게 한 설계다), 제목은 본문 첫 `# ` 줄에
    있다. 그것을 못 읽으면 화면 제목이 slug 로 떨어져
    `rhyu2025_systematic-feature-design-formation` 처럼 나온다 — 실제로 그랬다.
    """
    m = _BODY_H1.search(body or "")
    return m.group(1).strip() if m else ""


def page_index() -> dict[str, str]:
    """wikilink 해석용 slug → URL. `raw/papers/foo` 같은 경로 표기도 받는다."""
    idx = {}
    for slug, p in scan_pages().items():
        idx[slug] = p["url"]
        idx[f'{p["dir"]}/{slug}'] = p["url"]
        idx[f'{p["dir"]}/{slug}.md'] = p["url"]
    return idx


# ─────────────────────────────────────────────────────────────────────────
# wikilink
# ─────────────────────────────────────────────────────────────────────────
_WL = re.compile(r"\[\[([^\[\]|]+?)(?:\|([^\[\]]+?))?\]\]")
_FENCE = re.compile(r"(^```.*?^```|^~~~.*?^~~~)", re.S | re.M)
_CODESPAN = re.compile(r"(`+)(?:.|\n)*?\1")


def linkify_wikilinks(text: str, index: dict[str, str]) -> str:
    """`[[slug]]` · `[[slug|label]]` → 마크다운 링크. 코드는 건드리지 않는다.

    ⚠ 코드 펜스/인라인 코드 안의 `[[...]]` 까지 바꾸면 문서가 거짓말을 한다
      (SCHEMA 예시가 링크로 둔갑). 코드 구간을 먼저 빼돌린 뒤 치환한다.
    """
    stash: list[str] = []

    def _hide(m):
        stash.append(m.group(0))
        return "\x00%d\x00" % (len(stash) - 1)

    s = _FENCE.sub(_hide, text or "")
    s = _CODESPAN.sub(_hide, s)

    def _sub(m):
        target = (m.group(1) or "").strip()
        label = (m.group(2) or target).strip()
        url = index.get(target) or index.get(target.lower())
        if not url:
            # 없는 페이지는 링크하지 않는다 — 죽은 링크를 만드는 대신 표시만 남긴다
            return f"<<WLMISS:{label}>>"
        return f"[{label}]({url})"

    s = _WL.sub(_sub, s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], s)
    return s


# 마크다운 판본에 따라 `<` 가 그대로 남기도 하고 `&lt;` 로 이스케이프되기도 한다 — 둘 다 받는다.
_WLMISS = re.compile(r"(?:&lt;|<){2}WLMISS:(.*?)(?:&gt;|>){2}")


def render_body(text: str, index: dict[str, str] | None = None) -> str:
    idx = page_index() if index is None else index
    html = md_html(linkify_wikilinks(text, idx))

    def _miss(m):
        label = _html.escape(_html.unescape(m.group(1)))
        return f'<span class="wl-missing" title="이 위키에 없는 페이지">{label}</span>'
    return _WLMISS.sub(_miss, html)


# ─────────────────────────────────────────────────────────────────────────
# 제목 앵커 + 목차 — 6만 자 digest 는 목차 없이 읽히지 않는다
# ─────────────────────────────────────────────────────────────────────────
# ⚠ python-markdown 의 `toc` 확장을 켜지 않는다. id 를 **우리가** 만들면 (h-1, h-2…)
#   문서 내용이 무엇이든 id 충돌·주입이 원천적으로 불가능하다. 확장을 켜면 id 문자열이
#   문서에서 오고, digest 는 외부 PDF 요약본이라 100% 신뢰 대상이 아니다.
_HTAG = re.compile(r"<h([1-4])>(.*?)</h\1>", re.S)
_TAGSTRIP = re.compile(r"<[^>]+>")


_SAFE_ID = re.compile(r"[^a-z0-9]+")


def slug_id(name: str, fallback: str = "h") -> str:
    """임의 문자열 → HTML id 로 써도 안전한 조각 (`PHASE1B_NOTES.md` → `phase1b-notes-md`).

    한 화면에 문서가 둘 이상 실릴 때 **문서마다 다른 앵커 접두사**를 만드는 데 쓴다.
    id 문자열이 문서 *내용*에서 오지 않게 하는 것이 요점이라, 파일 이름처럼
    우리가 아는 값만 넣는다.
    """
    s = _SAFE_ID.sub("-", (name or "").lower()).strip("-")
    return s or fallback


def anchor_headings(html: str, levels=(2, 3), prefix: str = "h") -> tuple[str, list[dict]]:
    """`<h2>`/`<h3>` 에 순번 id 를 붙이고 목차 목록을 함께 돌려준다.

    ⚠ `prefix` 는 **한 페이지에 문서가 둘 이상 실릴 때** 반드시 다르게 준다.
      /results 는 PHASE 노트 두 개를 한 화면에 싣는데, 둘 다 `h-1` 부터 시작하면
      id 가 겹쳐서 목차 링크와 `:target` 이 첫 문서로만 간다 (실측된 버그).
    """
    pre = slug_id(prefix, "h")
    toc: list[dict] = []
    n = 0

    def _sub(m):
        nonlocal n
        lvl, inner = int(m.group(1)), m.group(2)
        if lvl not in levels:
            return m.group(0)
        n += 1
        hid = f"{pre}-{n}"
        text = _html.unescape(_TAGSTRIP.sub("", inner)).strip()
        toc.append({"id": hid, "level": lvl, "text": text})
        return f'<h{lvl} id="{hid}" class="anchored">{inner}'\
               f'<a class="hanchor" href="#{hid}" aria-label="이 절 링크">#</a></h{lvl}>'

    return _HTAG.sub(_sub, html), toc


# ─────────────────────────────────────────────────────────────────────────
# digest 의 3구분 표기 — 이 저장소의 인용 규율을 화면에서 갈라 보인다
# ─────────────────────────────────────────────────────────────────────────
# `[인쇄]` 원문에 글자로 있는 것 / `[도표]` 그림에서 눈으로 읽은 근사값 /
# `[해석]` digest 를 쓰며 붙인 판단(= 논문의 주장이 아니다).
# 셋이 같은 회색 코드 조각으로 보이면 **원문 주장과 우리 판단이 섞여 읽힌다** —
# 이 위키가 가장 피하려는 사고다. 서버가 렌더 결과에 클래스를 붙여 갈라 놓는다.
CLAIM_KINDS = {
    "인쇄": ("printed", "원문에 글자로 인쇄된 것"),
    "도표": ("figure", "그림에서 눈으로 읽은 근사값 — 원 데이터가 아니다"),
    "해석": ("ours", "digest 를 쓰며 붙인 판단 — 논문의 주장이 아니다"),
}
_CLAIM_LEAD = re.compile(r"(<(?:p|li)\b[^>]*)(>)\s*<code>\[(인쇄|도표|해석)\]</code>")
_CLAIM_ANY = re.compile(r"<code>\[(인쇄|도표|해석)\]</code>")


def mark_claims(html: str) -> tuple[str, dict]:
    """3구분 표기에 클래스를 달고 종류별 개수를 센다."""
    counts = {k: 0 for k in CLAIM_KINDS}

    def _lead(m):
        kind = m.group(3)
        cls = CLAIM_KINDS[kind][0]
        return f'{m.group(1)} class="claim claim-{cls}"{m.group(2)}' \
               f'<code class="ctag ct-{cls}" title="{CLAIM_KINDS[kind][1]}">[{kind}]</code>'

    out = _CLAIM_LEAD.sub(_lead, html)

    # 문단 첫머리가 아닌 자리(제목 안·문장 중간)의 표기도 같은 색으로 물들인다.
    def _any(m):
        kind = m.group(1)
        cls = CLAIM_KINDS[kind][0]
        counts[kind] += 1
        return f'<code class="ctag ct-{cls}" title="{CLAIM_KINDS[kind][1]}">[{kind}]</code>'

    out = _CLAIM_ANY.sub(_any, out)
    # _lead 가 이미 바꾼 것은 위 패턴에 안 걸리므로 따로 센다
    for kind in counts:
        counts[kind] += out.count(f'class="claim claim-{CLAIM_KINDS[kind][0]}"')
    return out, counts


def render_digest(text: str, index: dict[str, str] | None = None,
                  prefix: str = "h", title: str = "") -> dict:
    """논문 digest 전용 렌더 — 본문 + 목차 + 3구분 개수.

    ⚠ `prefix` 는 **한 화면에 이 함수를 두 번 이상 부를 때** 반드시 다르게 준다.
      기본값 그대로 두 번 부르면 두 문서의 제목 id 가 둘 다 `h-1` 부터 다시
      시작해 **중복 id** 가 된다. 그러면 목차 링크와 `#앵커` 가 언제나 첫
      문서로만 가고, 둘째 문서의 절은 링크로 도달할 수 없다 (`/results` 가
      PHASE 노트 두 개를 한 화면에 싣다가 실제로 그랬다).
    """
    html = render_body(text, index)
    html = drop_leading_h1(html, title)
    html, counts = mark_claims(html)
    html, toc = anchor_headings(html, prefix=prefix)
    return {"html": html, "toc": toc, "claims": counts}


#: 본문 첫 `<h1>` — 마크다운 파일이 제목을 한 번 더 적는 관습.
_LEAD_H1 = re.compile(r"\A\s*<h1[^>]*>(.*?)</h1>\s*", re.S | re.I)


def drop_leading_h1(html: str, title: str = "") -> str:
    """머리글이 이미 보여 준 제목을 본문에서 한 번 더 찍지 않는다.

    이 위키의 마크다운은 frontmatter 의 `title` 과 **같은 문장**을 본문 첫
    `# 제목` 으로 다시 적는다 (SCHEMA 의 관습). 화면에서는 머리글이 그것을
    이미 크게 보여 주므로, 본문이 또 찍으면 같은 줄이 두 번 나오고 그 사이
    간격이 페이지 맨 위를 비워 놓는다.

    같은 문장일 때만 지운다 — 다른 제목이면 저자가 일부러 쓴 것이다.
    """
    m = _LEAD_H1.match(html)
    if not m:
        return html
    inner = re.sub(r"<[^>]+>", "", m.group(1))
    if _norm(inner) != _norm(title):
        return html
    return html[m.end():]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


# ─────────────────────────────────────────────────────────────────────────
# Status Log → 타임라인
# ─────────────────────────────────────────────────────────────────────────
# 이 위키의 Status Log 는 두 가지 표기를 쓴다 (둘 다 받는다):
#   `- [2026-09-03] open — …`      (pvs-sev 카드)
#   `- **[2026-08-05]** 세미나 … `  (22p 카드)
_LOG_ITEM = re.compile(r"^-\s+\*{0,2}\[(\d{4}-\d{2}-\d{2})([^\]]*)\]\*{0,2}\s*", re.M)
_LOG_STATE = re.compile(r"^(open|active|answered|parked|closed)(\s*유지)?\b", re.I)
_LIST_LINE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")


def _dedent_rest(first: str, rest: list[str]) -> str:
    """목록 항목의 **이어지는 줄**만 내어쓴다.

    첫 줄은 이미 `- ` 뒤라 들여쓰기가 0 이고, 이어지는 줄은 목록 들여쓰기(보통 2칸)를
    달고 있다. 전부를 함께 재면 pad 가 0 이 되어 중첩 목록이 그대로 남는다 —
    그러면 `  - foo` 가 마크다운에서 **인용 아닌 중첩**으로 잘못 렌더된다.
    """
    filled = [ln for ln in rest if ln.strip()]
    pad = min((len(ln) - len(ln.lstrip(" ")) for ln in filled), default=0)
    lines = [first] + [ln[pad:] if ln.strip() else "" for ln in rest]

    # 내어쓰고 나면 **중첩 목록이 문단에 붙어 버린다.** 원문에서는 상위 항목의
    # 하위 목록이라 성립했지만, 한 단계 올라오면 마크다운은 문단을 끊는 빈 줄을
    # 요구한다 (sane_lists: 목록이 문단을 가로채지 못한다). 빈 줄을 넣어 준다.
    out: list[str] = []
    for ln in lines:
        if (_LIST_LINE.match(ln) and out and out[-1].strip()
                and not _LIST_LINE.match(out[-1])):
            out.append("")
        out.append(ln)
    return "\n".join(out)


def parse_log_entries(body: str) -> list[dict]:
    """`- [날짜] …` 목록을 타임라인 항목으로 쪼갠다. 못 쪼개면 빈 목록."""
    marks = list(_LOG_ITEM.finditer(body or ""))
    if not marks:
        return []
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        chunk = body[m.end():end].rstrip()
        first, _, rest = chunk.partition("\n")
        text = _dedent_rest(first, rest.split("\n")) if rest else first
        st = _LOG_STATE.match(first.strip())
        out.append({
            "date": m.group(1),
            "suffix": (m.group(2) or "").strip(),      # "(2)" 같은 같은 날 순번
            "state": (st.group(1).lower() if st else ""),
            "held": bool(st and st.group(2)),           # "유지"
            "body": text,
        })
    return out


# ─────────────────────────────────────────────────────────────────────────
# 절 분해 (질문 카드 / 게이트 원장)
# ─────────────────────────────────────────────────────────────────────────
_H2 = re.compile(r"^##\s+(.+?)\s*$", re.M)


def split_sections(body: str, level: str = "##") -> list[dict]:
    """`## ` 제목마다 잘라 [{title, body}] 로. 첫 제목 앞은 title="" 로 담는다."""
    pat = re.compile(r"^%s\s+(.+?)\s*$" % re.escape(level), re.M)
    marks = list(pat.finditer(body or ""))
    out = []
    if not marks:
        return [{"title": "", "body": body or ""}]
    if marks[0].start() > 0:
        out.append({"title": "", "body": body[: marks[0].start()]})
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        out.append({"title": m.group(1), "body": body[m.end():end]})
    return out


# 질문 카드의 핵심 구조 — 이 위키가 실제로 쓰는 제목 표기를 그대로 잡는다.
_QCLASS = (
    ("for", re.compile(r"evidence\s*for", re.I)),
    ("against", re.compile(r"evidence\s*against", re.I)),
    ("gap", re.compile(r"\bgap\b|빈 근거", re.I)),
    ("log", re.compile(r"status\s*log", re.I)),
    ("method", re.compile(r"답하는 방법|설계", re.I)),
    ("hypo", re.compile(r"가설|hypothes", re.I)),
)


def classify_section(title: str) -> str:
    for name, rx in _QCLASS:
        if rx.search(title or ""):
            return name
    return "plain"


# ─────────────────────────────────────────────────────────────────────────
# 그림
# ─────────────────────────────────────────────────────────────────────────
def _figkey(kind: str, label: str) -> str:
    """figref.js 의 keyOf 와 **같은 규칙**으로 키를 다시 만든다.

    ⚠ figures.json 에 적힌 key 를 그냥 쓰면 안 된다 — 세미나 자료는 `F1`(대문자),
      나머지 논문은 `f1`(소문자)로 추출 도구 판본이 달랐다. 브라우저 쪽 규칙은
      "종류 첫 글자(소문자) + 라벨 대문자" 하나이므로 서버에서 통일한다.
    """
    c = (kind or "figure").lower()[:1]
    p = "t" if c == "t" else "s" if c == "s" else "f"
    return p + str(label or "").upper()


def figures_for(slug: str) -> list[dict]:
    """`wiki/raw/figures/<slug>/figures.json` → 화면용 그림 목록."""
    d = FIGROOT / slug
    j = d / "figures.json"
    if not j.is_file():
        return []
    try:
        data = json.loads(j.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for f in data.get("figures") or []:
        name = str(f.get("file") or "")
        if not name or not (d / name).is_file():
            continue
        kind = str(f.get("kind") or "figure")
        label = str(f.get("label") or "")
        out.append({
            "key": _figkey(kind, label),
            "kind": kind,
            "label": label,
            "title": ("Table " if kind == "table" else "Scheme " if kind == "scheme" else "Fig. ") + label,
            "page": f.get("page"),
            "caption": str(f.get("caption") or ""),
            "rel": f"{slug}/{name}",
            "w": f.get("w"), "h": f.get("h"),
        })
    return out


def figure_meta(slug: str) -> dict:
    j = FIGROOT / slug / "figures.json"
    if not j.is_file():
        return {}
    try:
        d = json.loads(j.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: d.get(k) for k in ("dpi", "maxpx", "generated", "sources", "mode", "nup") if k in d}


# ─────────────────────────────────────────────────────────────────────────
# CSV — 작은 것은 표로, 큰 것은 요약 통계로
# ─────────────────────────────────────────────────────────────────────────
CSV_TABLE_MAX = 200          # 이 행 수까지는 전부 표로 그린다
CSV_PREVIEW = 15             # 그보다 크면 앞부분만 + 요약


def read_csv_view(path: Path) -> dict:
    rel = path.relative_to(ROOT).as_posix()
    # 한 화면에 여러 CSV 가 실린다 — 앵커는 **경로**에서 만든다 (내용에서 오지 않는다).
    # 읽기에 실패한 칸도 목차에서 가리킬 수 있어야 하므로 실패 경로에도 같이 넣는다.
    base = {"name": path.name, "id": "csv-" + slug_id(rel, path.stem), "relpath": rel}
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {**base, "error": str(e)}
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        return {**base, "error": "빈 파일"}
    header, body = rows[0], rows[1:]
    full = len(body) <= CSV_TABLE_MAX
    view = body if full else body[:CSV_PREVIEW]
    stats = []
    if not full:
        for i, col in enumerate(header):
            vals = []
            for r in body:
                if i >= len(r):
                    continue
                try:
                    vals.append(float(r[i]))
                except (TypeError, ValueError):
                    pass
            if len(vals) < max(2, len(body) // 2):     # 숫자열이 아니면 통계 없음
                stats.append({"col": col, "numeric": False, "n": len(body),
                              "uniq": len({r[i] for r in body if i < len(r)})})
                continue
            vals.sort()
            n = len(vals)
            stats.append({
                "col": col, "numeric": True, "n": n,
                "min": vals[0], "max": vals[-1],
                "mean": sum(vals) / n,
                "median": vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2,
            })
    return {
        **base,
        "header": header,
        "rows": view,
        "nrows": len(body),
        "full": full,
        "stats": stats,
        "bytes": path.stat().st_size,
    }


# ─────────────────────────────────────────────────────────────────────────
# 위키 로그 / 홈
# ─────────────────────────────────────────────────────────────────────────
_LOG_H = re.compile(r"^##\s+\[(\d{4}-\d{2}-\d{2})\]\s+(\w+)\s*\|\s*(.+?)\s*$", re.M)


def recent_log(limit: int = 12) -> list[dict]:
    p = WIKI / "log.md"
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8")
    marks = list(_LOG_H.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out.append({"date": m.group(1), "action": m.group(2), "subject": m.group(3),
                    "body": text[m.end():end].strip()})
    out.reverse()                                   # log.md 는 append-only(오래된 것이 위)
    return out[:limit]


# ─────────────────────────────────────────────────────────────────────────
# 게이트 원장 — 최근 절만
# ─────────────────────────────────────────────────────────────────────────
_GATE_H = re.compile(r"^##\s+(§\d+\s+.+?)\s*$", re.M)


# 라운드 머리글이 실제로 인쇄하는 것들. **없으면 없다고 표시한다** — 추정하지 않는다.
_G_VERDICT = re.compile(r"\*\*(NO-GO|GO)\*\*")
_G_P0 = re.compile(r"P0\s*(?:뿌리\s*)?(\d+)\s*(?:묶음|건)")
_G_P1 = re.compile(r"P1\s*(\d+)\s*건")
_G_ID = re.compile(r"\bP([01])-(\d+)")
_G_ROUND = re.compile(r"§(\d+)\s*[—-]?\s*(?:(\d+)차)?")


def gate_round_meta(title: str, body: str) -> dict:
    """라운드 절의 머리 문단에서 **인쇄된 것만** 뽑는다.

    ⚠ 판정·건수는 원장이 그 문단에 글자로 적었을 때만 쓴다. 본문을 세어
      추정하면 화면이 원장보다 더 아는 척을 하게 된다. 대신 본문에 실재하는
      발견 ID 는 그대로 모아 보여 준다 (그건 세는 게 아니라 옮기는 것이다).
    """
    lead = (body or "").strip().split("\n\n")[0]
    v = _G_VERDICT.search(lead)
    p0, p1 = _G_P0.search(lead), _G_P1.search(lead)
    ids = sorted({f"P{a}-{int(b)}" for a, b in _G_ID.findall(body or "")},
                 key=lambda s: (s[1], int(s.split("-")[1])))
    m = _G_ROUND.match(title or "")
    return {
        "sec": int(m.group(1)) if m and m.group(1) else None,
        "round": int(m.group(2)) if m and m.group(2) else None,
        "verdict": v.group(1) if v else "",             # 이 절이 **응답하는** 직전 판정
        "declared": {"p0": int(p0.group(1)) if p0 else None,
                     "p1": int(p1.group(1)) if p1 else None},
        "ids": ids,
        "n_p0": sum(1 for i in ids if i.startswith("P0")),
        "n_p1": sum(1 for i in ids if i.startswith("P1")),
        "bytes": len(body or ""),
    }


def gate_sections(show: int = 3) -> dict:
    if not GATE_DOC.is_file():
        return {"available": False, "path": GATE_DOC.relative_to(ROOT).as_posix()}
    text = GATE_DOC.read_text(encoding="utf-8")
    marks = list(_GATE_H.finditer(text))
    titles = [m.group(1) for m in marks]
    latest = []
    for m in marks[-show:] if marks else []:
        i = marks.index(m)
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        latest.append({"title": m.group(1), "body": text[m.end():end]})
    latest.reverse()                                # 최신이 위
    return {
        "available": True,
        "path": GATE_DOC.relative_to(ROOT).as_posix(),
        "titles": titles,
        "count": len(titles),
        "latest": latest,
        "bytes": GATE_DOC.stat().st_size,
        "mtime": datetime.fromtimestamp(_mtime(GATE_DOC)).strftime("%Y-%m-%d %H:%M"),
    }


# ─────────────────────────────────────────────────────────────────────────
# satellite Phase — 선언된 상태 vs 디스크에 실제로 있는 산출물
# ─────────────────────────────────────────────────────────────────────────
# README 의 Phases 표는 **사람이 적은 선언**이고, `docs/PHASE*_NOTES.md` 와
# `results/phase*/` 는 **실제로 생긴 파일**이다. 둘이 어긋나면 화면이 어느
# 한쪽을 고르지 않고 **둘 다 보이고 어긋났다고 말한다** (이 저장소는 파일이 정본).
_PH_ROW = re.compile(r"^\|\s*(\d+)\s*\|(.+?)\|(.+?)\|(.+?)\|\s*$", re.M)
_PH_NUM = re.compile(r"phase(\d+)", re.I)


def phase_rail() -> list[dict]:
    readme = MO / "README.md"
    rows: dict[int, dict] = {}
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
        block = ""
        for sec in split_sections(text):
            if "phase" in (sec["title"] or "").lower():
                block = sec["body"]
                break
        for m in _PH_ROW.finditer(block):
            n = int(m.group(1))
            rows[n] = {"n": n,
                       "what": m.group(2).strip(),
                       "needs": m.group(3).strip(),
                       "declared": m.group(4).strip()}

    # 디스크 증거를 모은다 — Phase 번호는 파일 이름에서만 읽는다 (본문 추정 금지).
    found: dict[int, dict] = {}
    for f in sorted((MO / "docs").glob("PHASE*_NOTES.md")) if (MO / "docs").is_dir() else []:
        m = re.match(r"PHASE(\d+)", f.name, re.I)
        if m:
            found.setdefault(int(m.group(1)), {"notes": [], "results": []})["notes"].append(
                {"name": f.name, "relpath": f.relative_to(ROOT).as_posix()})
    rd = MO / "results"
    for d in sorted(rd.iterdir()) if rd.is_dir() else []:
        m = _PH_NUM.match(d.name)
        if not (m and d.is_dir()):
            continue
        for f in sorted(d.glob("*.csv")):
            found.setdefault(int(m.group(1)), {"notes": [], "results": []})["results"].append(
                {"name": f.name, "relpath": f.relative_to(ROOT).as_posix(),
                 "bytes": f.stat().st_size})

    out = []
    for n in sorted(set(rows) | set(found)):
        row = rows.get(n, {"n": n, "what": "", "needs": "", "declared": ""})
        ev = found.get(n, {"notes": [], "results": []})
        if ev["results"]:
            state, label = "done", "결과 파일 있음"
        elif ev["notes"]:
            state, label = "partial", "노트만 있음"
        else:
            state, label = "todo", "산출물 없음"
        declared_todo = "미착수" in (row.get("declared") or "")
        out.append({**row, **ev, "state": state, "state_label": label,
                    # 선언이 "미착수" 인데 산출물이 있으면 README 가 뒤처진 것이다
                    "mismatch": bool(declared_todo and state != "todo")})
    return out


# ─────────────────────────────────────────────────────────────────────────
# 단독 스윕 라인 차트 — 좌표를 서버가 계산한다 (JS 차트 라이브러리 없음: CSP)
# ─────────────────────────────────────────────────────────────────────────
SWEEP_MODES = (
    ("lli", "LLI", "a"),
    ("lam_pe", "LAM_PE", "b"),
    ("lam_ne", "LAM_NE", "c"),
)


def _fnum(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if f != f else f                       # NaN 제외


def sweep_rows() -> dict[str, list[tuple[float, float]]]:
    """`pvs_tracked.csv` 에서 **단독 스윕**(나머지 두 모드가 0)만 뽑는다."""
    if not SWEEP_CSV.is_file():
        return {}
    try:
        raw = SWEEP_CSV.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    rows = list(csv.DictReader(io.StringIO(raw)))
    keys = [k for k, _l, _c in SWEEP_MODES]
    out: dict[str, list[tuple[float, float]]] = {}
    for k in keys:
        pts = []
        for r in rows:
            vals = {j: _fnum(r.get(j)) for j in keys}
            y = _fnum(r.get("pvs"))
            if y is None or vals[k] is None:
                continue
            if any(vals[j] != 0.0 for j in keys if j != k):
                continue                                # 단독 스윕이 아니다
            pts.append((vals[k], y))
        pts.sort()
        if pts:
            out[k] = pts
    return out


def _nice_ticks(lo: float, hi: float, target: int = 6) -> list[float]:
    """1·2·5×10ⁿ 눈금. 눈금 없는 예쁜 곡선은 쓸모가 없다."""
    if hi <= lo:
        hi = lo + 1.0
    raw = (hi - lo) / max(1, target)
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1.0
    step = next((m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw), 10 * mag)
    start = math.floor(lo / step) * step
    # 마지막 눈금이 데이터 최대를 **덮도록** 올린다. 안 그러면 최상단 띠에 눈금이
    # 없는 채로 곡선이 지나가고, 그 구간은 눈으로 값을 읽을 수 없다.
    n = max(1, math.ceil((hi - start) / step - 1e-9))
    return [round(start + i * step, 10) for i in range(n + 1)]


def _fmt(v: float) -> str:
    s = f"{v:.10g}"
    return "0" if s in ("-0", "0") else s


def sweep_chart(w: int = 760, h: int = 400) -> dict | None:
    """단독 스윕 3종을 하나의 좌표계에 겹쳐 그릴 **SVG 기하**를 만든다.

    색만으로 계열을 가르지 않는다 — 점 모양·파선 패턴·**선 끝의 직접 라벨**이
    같이 붙는다 (범례를 눈으로 왕복하지 않아도 되고, 색각 이상에서도 읽힌다).
    """
    data = sweep_rows()
    if not data:
        return None
    ml, mr, mt, mb = 66, 104, 18, 54                  # 오른쪽 여백은 직접 라벨 자리
    pw, ph = w - ml - mr, h - mt - mb

    xs = [x for pts in data.values() for x, _ in pts]
    ys = [y for pts in data.values() for _, y in pts]
    xt = _nice_ticks(min(xs), max(xs))
    yt = _nice_ticks(min(ys), max(ys))
    x0, x1 = xt[0], xt[-1]                             # 축 범위 = 눈금의 처음과 끝
    y0, y1 = yt[0], yt[-1]

    def px(x):
        return round(ml + (x - x0) / (x1 - x0) * pw, 2)

    def py(y):
        return round(mt + (y1 - y) / (y1 - y0) * ph, 2)

    series = []
    for key, label, cls in SWEEP_MODES:
        pts = data.get(key) or []
        if not pts:
            continue
        xy = [(px(x), py(y)) for x, y in pts]
        series.append({
            "key": key, "label": label, "cls": cls,
            "n": len(pts),
            "path": "M " + " L ".join(f"{a} {b}" for a, b in xy),
            "pts": [{"cx": a, "cy": b, "x": x, "y": y}
                    for (a, b), (x, y) in zip(xy, pts)],
            "end": {"cx": xy[-1][0], "cy": xy[-1][1], "x": pts[-1][0], "y": pts[-1][1]},
            # 스윕이 x 축 끝까지 못 갔다 = 추적이 끊긴 것이다. 숨기지 않고 표시한다.
            "truncated": pts[-1][0] < max(xs) - 1e-12,
        })
    return {
        "w": w, "h": h, "ml": ml, "mt": mt, "pw": pw, "ph": ph,
        "x_ticks": [{"v": t, "label": _fmt(t), "px": px(t)} for t in xt if x0 <= t <= x1],
        "y_ticks": [{"v": t, "label": _fmt(t), "py": py(t)} for t in yt if y0 <= t <= y1],
        "series": series,
        "source": SWEEP_CSV.relative_to(ROOT).as_posix(),
        "n_rows": sum(s["n"] for s in series),
        "x_label": "단독 열화 손실 분율 [–]",
        "y_label": "PVS [Ah·V⁻²]",
    }


# ─────────────────────────────────────────────────────────────────────────
# 검색 — 단순 전문(부분 문자열)
# ─────────────────────────────────────────────────────────────────────────
def _corpus() -> list[dict]:
    docs = []
    for slug, p in scan_pages().items():
        docs.append({"title": p["title"], "url": p["url"], "kind": p["kind"],
                     "path": p["relpath"], "file": p["path"]})
    for name in ("index.md", "log.md"):
        f = WIKI / name
        if f.is_file():
            docs.append({"title": f"wiki/{name}", "url": "/", "kind": "wiki",
                         "path": f"wiki/{name}", "file": f})
    if MO.is_dir():
        # /results 는 노트 여러 편이 세로로 이어 붙은 긴 화면이다. 히트를 화면 맨 위로
        # 보내면 어느 노트에서 걸렸는지가 사라지므로 그 노트 칸까지 앵커로 데려간다
        # (앵커는 app.py 의 `/results` 가 붙이는 것과 **같은 규칙**으로 만든다).
        for f in sorted((MO / "docs").glob("*.md")) if (MO / "docs").is_dir() else []:
            docs.append({"title": f.name, "url": "/results#" + slug_id(f.stem),
                         "kind": "results",
                         "path": f.relative_to(ROOT).as_posix(), "file": f})
    if GATE_DOC.is_file():
        docs.append({"title": "08_REVIEW_RESPONSE.md", "url": "/gate", "kind": "gate",
                     "path": GATE_DOC.relative_to(ROOT).as_posix(), "file": GATE_DOC})
    return docs


def search(q: str, limit: int = 60) -> list[dict]:
    q = (q or "").strip()
    if len(q) < 2:
        return []
    needle = q.lower()
    hits = []
    for d in _corpus():
        try:
            text = d["file"].read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        low = text.lower()
        n = low.count(needle)
        if not n:
            continue
        snips = []
        start = 0
        for _ in range(min(3, n)):
            i = low.find(needle, start)
            if i < 0:
                break
            a, b = max(0, i - 110), min(len(text), i + len(q) + 110)
            # 줄바꿈·연속 공백을 접는다 — 원문 그대로면 스니펫이 표·목록 조각으로
            # 깨져서 "무슨 문맥이었나" 가 안 읽힌다.
            snips.append({"pre": " ".join(text[a:i].split()),
                          "hit": text[i:i + len(q)],
                          "post": " ".join(text[i + len(q):b].split())})
            start = i + len(q)
        hits.append({"title": d["title"], "url": d["url"], "kind": d["kind"],
                     "path": d["path"], "count": n, "snips": snips})
    hits.sort(key=lambda h: -h["count"])
    return hits[:limit]
