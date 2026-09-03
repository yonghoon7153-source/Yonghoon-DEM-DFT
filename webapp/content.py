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
                "title": str(meta.get("title") or slug),
                "description": str(meta.get("description") or ""),
                "updated": str(meta.get("updated") or meta.get("ingested") or meta.get("created") or ""),
                "mtime": _mtime(f),
                "bytes": f.stat().st_size if f.exists() else 0,
            }
    return pages


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
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"error": str(e)}
    rows = list(csv.reader(io.StringIO(raw)))
    if not rows:
        return {"error": "빈 파일"}
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
        "name": path.name,
        "relpath": path.relative_to(ROOT).as_posix(),
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
        for f in sorted((MO / "docs").glob("*.md")) if (MO / "docs").is_dir() else []:
            docs.append({"title": f.name, "url": "/results", "kind": "results",
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
            a, b = max(0, i - 90), min(len(text), i + len(q) + 90)
            snips.append({"pre": text[a:i], "hit": text[i:i + len(q)], "post": text[i + len(q):b]})
            start = i + len(q)
        hits.append({"title": d["title"], "url": d["url"], "kind": d["kind"],
                     "path": d["path"], "count": n, "snips": snips})
    hits.sort(key=lambda h: -h["count"])
    return hits[:limit]
