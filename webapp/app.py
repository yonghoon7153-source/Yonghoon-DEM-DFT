"""app.py — Yonghoon-DEM-DFT 모노레포 열람 webapp (로컬 · 읽기 전용).

무엇을 서빙하나
  wiki/ (index·log·papers·questions·concepts·entities·guides…) ·
  mode-observability/ 의 Phase 결과 · degradation-degeneracy 게이트 원장의 최근 절.
  전부 **파일이 정본**이고 이 앱은 그 위에 얹은 읽기 창이다.

무엇을 안 하나
  쓰기. 코멘트·이름변경·업로드·하이라이트 저장이 없다 (라우트 자체가 없고,
  그 위에 `_guard_mutation` 이 GET/HEAD/OPTIONS 외 모든 메서드를 405 로 막는다).
  `wiki/raw/` 는 sha256 으로 봉인된 불변층이고 `degradation-degeneracy/` 의
  코드 트리는 게이트 리뷰 대상 code identity 라, 웹에서 고칠 수 있으면 안 된다.

띄우기:  python3 webapp/app.py       (기본 http://127.0.0.1:5057)
"""
from __future__ import annotations

import os

from flask import (Flask, Response, abort, jsonify, render_template, request,
                   send_from_directory)
from markupsafe import Markup

import content as C

app = Flask(__name__)

# 템플릿·정적파일을 매 요청마다 다시 읽는다.
#
# 이 앱은 debug=False 로 뜬다 (아래 app.run). Flask 의 기본값은
# TEMPLATES_AUTO_RELOAD = app.debug 이므로, 그대로 두면 Jinja 가 첫 렌더에서
# 컴파일한 템플릿을 프로세스가 죽을 때까지 들고 있는다. 그러면 템플릿을
# 고치고 브라우저를 새로고침해도 **옛 화면이 그대로 나온다** — 실제로
# 이 함정에 걸려서 "고쳤는데 똑같다" 를 한 라운드 낭비했다.
# 정적파일도 같은 이유로 캐시 수명을 0 으로 둔다 (CSS 를 고쳐도 안 바뀌는 문제).
#
# 성능 논거는 여기에 없다. 이 앱은 로컬에서 혼자 읽는 창이고, 매 요청 디스크
# 재확인 비용보다 "화면이 파일과 다르다" 가 훨씬 비싸다.
#
# 순서가 중요하다. Flask 는 `app.jinja_env` 에 **처음 접근할 때** Jinja
# 환경을 만들고 그때 config 를 읽는다. 그래서 config 설정은 jinja_env 를
# 건드리기 전에 와야 한다 — 아래 trim_blocks 두 줄이 원래 여기 위에 있었고,
# 그것 때문에 TEMPLATES_AUTO_RELOAD 를 켜도 안 먹었다 (실측으로 확인).
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# 기본 바인딩은 루프백. 외부에 노출할 이유가 없고, 노출하면 이 앱의 전제
# ("혼자 읽는 로컬 창")가 깨진다. 굳이 바꾸려면 WEBAPP_HOST 로 명시해야 한다.
HOST = os.environ.get("WEBAPP_HOST", "127.0.0.1")
PORT = int(os.environ.get("WEBAPP_PORT", "5057"))

_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


@app.before_request
def _guard_mutation():
    """읽기 전용 게이트 — 쓰기 메서드는 라우트에 닿기 전에 거절한다.

    쓰기 라우트를 안 만든 것만으로 충분해 보이지만, 그건 "지금 없다" 일 뿐이다.
    누가 나중에 POST 라우트를 하나 붙여도 이 문을 먼저 지나야 한다 (fail-closed).
    """
    if request.method not in _SAFE_METHODS:
        return jsonify({
            "error": "읽기 전용 앱입니다 — 쓰기 메서드를 받지 않습니다.",
            "why": ("wiki/raw/ 는 sha256 으로 봉인된 불변층이고, "
                    "degradation-degeneracy/ 의 코드는 게이트 리뷰 대상 code identity 입니다. "
                    "웹에서 고칠 수 있으면 그 두 전제가 깨집니다."),
            "method": request.method,
        }), 405
    return None


@app.after_request
def _sec_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    # 완전 로컬 앱이다 — 바깥으로 나가는 요청 경로 자체를 막는다 (폰트 CDN 도 안 쓴다).
    resp.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; connect-src 'self'; form-action 'self'; base-uri 'none'; "
        "frame-ancestors 'self'")
    return resp


def _asset_version() -> str:
    try:
        paths = []
        for sub in ("css", "js"):
            d = os.path.join(app.static_folder, sub)
            if os.path.isdir(d):
                paths += [os.path.join(d, f) for f in os.listdir(d)]
        return str(int(max(os.path.getmtime(p) for p in paths)))
    except (OSError, ValueError):
        return "1"


# 저장소의 표 칸·설명문에는 `**굵게**` 와 `` `코드` `` 가 그냥 들어 있다. 본문
# 렌더러를 태우지 않는 그 짧은 글들을 지금까지 **날것 그대로** 찍고 있었다.
# `md_inline` 은 **escape 를 먼저** 하고 우리 태그만 되살리므로 (content.py 의
# 주석 참조) `|safe` 로 넘겨도 주입 경로가 없다.
@app.template_filter("mdi")
def _mdi(s):
    return Markup(C.md_inline(s))


@app.context_processor
def _inject():
    # wl_index: sources frontmatter 를 실제 페이지로 잇는 데 쓴다 (템플릿 매크로).
    return {"asset_version": _asset_version(), "wl_index": C.page_index()}


def _page_or_404(kind: str, slug: str) -> dict:
    p = C.scan_pages().get(slug)
    if not p or p["kind"] != kind:
        abort(404)
    return p


def _read(p: dict) -> tuple[dict, str]:
    text = p["path"].read_text(encoding="utf-8")
    return C.split_frontmatter(text)


# ─────────────────────────────────────────────────────────────────────────
# 홈
# ─────────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    pages = C.scan_pages()
    idx_file = C.WIKI / "index.md"
    idx_html = C.render_body(idx_file.read_text(encoding="utf-8")) if idx_file.is_file() else ""
    counts: dict[str, int] = {}
    for p in pages.values():
        counts[p["kind"]] = counts.get(p["kind"], 0) + 1
    return render_template("index.html", active="home",
                           index_html=idx_html,
                           log=C.recent_log(10),
                           counts=counts,
                           total=len(pages))


# ─────────────────────────────────────────────────────────────────────────
# 논문 digest
# ─────────────────────────────────────────────────────────────────────────
#: 브랜드 마크 — 파일 하나를 더 두지 않으려고 여기서 만든다 (CSP: 'self').
_FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="7" fill="#175d8d"/>'
    '<path d="M8 22V10h3.4l4.6 7 4.6-7H24v12h-3.2v-6.8L16.6 21h-1.2L11.2 15.2V22z"'
    ' fill="#ffffff"/></svg>')


@app.route("/favicon.svg")
def favicon():
    return Response(_FAVICON, mimetype="image/svg+xml")


@app.route("/papers")
def papers():
    items = []
    for p in C.scan_pages().values():
        if p["kind"] != "paper":
            continue
        meta = p["meta"]
        figs = C.figures_for(p["slug"])
        items.append({
            **p,
            "sha12": str(meta.get("sha256") or "")[:12],
            "source_url": str(meta.get("source_url") or ""),
            "ingested": str(meta.get("ingested") or ""),
            "nfig": len(figs),
            "ntab": sum(1 for f in figs if f["kind"] == "table"),
        })
    items.sort(key=lambda x: (x["ingested"] or "", x["slug"]), reverse=True)
    return render_template("papers.html", active="papers", items=items)


@app.route("/paper/<slug>")
def paper(slug):
    p = _page_or_404("paper", slug)
    meta, body = _read(p)
    figs = C.figures_for(slug)
    doc = C.render_digest(body, title=meta.get('title') or p['title'])
    return render_template("paper.html", active="papers", page=p, meta=meta,
                           body_html=doc["html"], toc=doc["toc"], claims=doc["claims"],
                           figs=figs, figmeta=C.figure_meta(slug),
                           sha=str(meta.get("sha256") or ""))


# ─────────────────────────────────────────────────────────────────────────
# 질문 카드 — Evidence For / Against / Gap / Status Log 를 구분해 렌더
# ─────────────────────────────────────────────────────────────────────────
@app.route("/questions")
def questions():
    items = []
    for p in C.scan_pages().values():
        if p["kind"] != "question":
            continue
        _meta, body = _read(p)
        secs = C.split_sections(body)
        kinds = {C.classify_section(s["title"]) for s in secs}
        items.append({**p, "has": kinds,
                      "nfor": sum(1 for s in secs if C.classify_section(s["title"]) == "for"),
                      "nagainst": sum(1 for s in secs if C.classify_section(s["title"]) == "against")})
    items.sort(key=lambda x: (x["updated"], x["slug"]), reverse=True)
    return render_template("questions.html", active="questions", items=items)


@app.route("/question/<slug>")
def question(slug):
    """질문 카드 — 절의 **종류**가 화면 형태를 정한다.

    이 위키에서 "무엇이 근거이고 무엇이 아직 빈칸인가" 는 본문 순서가 아니라 절의
    종류가 말한다. 그래서 세 가지 형태로 갈라 그린다:
      · Evidence For ↔ Against 가 **연달아** 오면 좌우로 **맞세운다** (`duel`).
        같은 질문에 대한 찬반은 위아래로 읽으면 대조가 안 된다.
      · Status Log 는 날짜 항목으로 쪼개 **타임라인**으로 (`timeline`).
      · 나머지는 종류 라벨을 단 보통 절.
    """
    p = _page_or_404("question", slug)
    meta, body = _read(p)
    idx = C.page_index()
    secs = []
    for n, s in enumerate(C.split_sections(body), 1):
        secs.append({"title": s["title"], "cls": C.classify_section(s["title"]),
                     "raw": s["body"], "id": f"s-{n}"})

    blocks, i = [], 0
    while i < len(secs):
        s = secs[i]
        nxt = secs[i + 1] if i + 1 < len(secs) else None
        if s["cls"] == "for" and nxt and nxt["cls"] == "against":
            blocks.append({"kind": "duel", "sides": [
                {**side, "html": C.render_body(side["raw"], idx)} for side in (s, nxt)]})
            i += 2
            continue
        if s["cls"] == "log":
            entries = C.parse_log_entries(s["raw"])
            if entries:
                blocks.append({"kind": "timeline", "title": s["title"], "cls": s["cls"],
                               "id": s["id"],
                               "entries": [{**e, "html": C.render_body(e["body"], idx)}
                                           for e in entries]})
                i += 1
                continue
        blocks.append({"kind": "sec", **s, "html": C.render_body(s["raw"], idx)})
        i += 1

    nav = [{"id": s["id"], "title": s["title"], "cls": s["cls"]}
           for s in secs if s["title"]]
    return render_template("question.html", active="questions", page=p, meta=meta,
                           blocks=blocks, nav=nav)


# ─────────────────────────────────────────────────────────────────────────
# 개념 · 엔티티 · 그 밖의 위키 문서
# ─────────────────────────────────────────────────────────────────────────
@app.route("/concepts")
def concepts():
    items = [p for p in C.scan_pages().values() if p["kind"] == "concept"]
    items.sort(key=lambda x: (x["updated"], x["slug"]), reverse=True)
    return render_template("concepts.html", active="concepts", items=items)


@app.route("/concept/<slug>")
def concept(slug):
    p = _page_or_404("concept", slug)
    meta, body = _read(p)
    d = C.render_digest(body, title=meta.get('title') or p['title'])
    return render_template("doc.html", active="concepts", page=p, meta=meta,
                           body_html=d["html"], toc=d["toc"], claims=d["claims"])


@app.route("/entities")
def entities():
    items = [p for p in C.scan_pages().values() if p["kind"] == "entity"]
    items.sort(key=lambda x: (x["updated"], x["slug"]), reverse=True)
    return render_template("entities.html", active="entities", items=items)


@app.route("/entity/<slug>")
def entity(slug):
    p = _page_or_404("entity", slug)
    meta, body = _read(p)
    d = C.render_digest(body, title=meta.get('title') or p['title'])
    return render_template("doc.html", active="entities", page=p, meta=meta,
                           body_html=d["html"], toc=d["toc"], claims=d["claims"])


@app.route("/doc/<path:rel>")
def doc(rel):
    """guides · queries · syntheses · comparisons · raw/transcripts 등 나머지 위키 문서.

    URL 의 마지막 조각을 slug 로 보고 **등록부에서** 찾는다 — 경로를 파일시스템에
    직접 붙이지 않으므로 여기로는 경로 탈출이 성립하지 않는다.
    """
    slug = rel.rstrip("/").split("/")[-1]
    p = C.scan_pages().get(slug)
    if not p or p["url"] != "/doc/" + rel.strip("/"):
        abort(404)
    meta, body = _read(p)
    d = C.render_digest(body, title=meta.get('title') or p['title'])
    return render_template("doc.html", active="", page=p, meta=meta,
                           body_html=d["html"], toc=d["toc"], claims=d["claims"])


# ─────────────────────────────────────────────────────────────────────────
# satellite 결과 · 게이트 원장
# ─────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────
# 연구 파이프라인 — 처음 온 사람을 위한 대표 화면
# ─────────────────────────────────────────────────────────────────────────
# ⚠ 이 화면에 **숫자를 새로 만들지 않는다.** 여기 실린 결과 수치는 전부
#   `docs/RESULTS_PAIRED_FIXED5.md` 의 사본이고, 화면에도 그렇게 적는다
#   (정본은 artifact + RESULTS*.md — 저장소 CLAUDE.md 하드룰 4). 사본을 두는
#   이유는 하나다: 파이프라인을 설명하면서 "그래서 답이 뭐였나" 를 말하지 않으면
#   그림만 남는다. 대신 인용은 금지하고 정본으로 보낸다.
@app.route("/pipeline")
def pipeline():
    return render_template("pipeline.html", active="pipeline")


# ─────────────────────────────────────────────────────────────────────────
# 검증층 — "이 연구는 자기를 어떻게 의심하는가"
# ─────────────────────────────────────────────────────────────────────────
# `/pipeline` 이 **연구 내용**의 대표 화면이라면 여기는 **검증층**의 대표
# 화면이다. `/gate` 는 원장 원문을 그대로 펼치므로 기계용이고, 처음 온 사람이
# "왜 이렇게까지 하나" 를 알 곳이 없었다.
#
# 숫자는 `C.trust_numbers()` 가 **실물을 세어** 만든다 — 화면에 상수를 적으면
# 그 순간 사본이 되고 낡는다 (하드룰 4).
@app.route("/trust")
def trust():
    return render_template("trust.html", active="trust",
                           nums=C.trust_numbers())


# ─────────────────────────────────────────────────────────────────────────
# 메모 모아보기 — 브라우저에 흩어진 주석을 한 화면에
# ─────────────────────────────────────────────────────────────────────────
# ⚠ 이 화면에는 **서버가 메모를 하나도 모른다.** 메모·하이라이트는 읽는 사람의
#   주석이지 위키의 내용이 아니라서 localStorage 에만 있다 ("이 앱은 아무것도
#   쓰지 않는다" 는 약속). 그러니 여기서 서버가 하는 일은 **이름표를 주는 것**
#   뿐이다 — 저장 key 의 slug 만으로는 카드에 "wang2025_…" 라는 파일 이름밖에
#   못 적는다. 모으고 거르고 묶는 것은 전부 `static/js/notes.js` 가 한다.
@app.route("/notes")
def notes():
    docs = {}
    for p in C.scan_pages().values():
        if p["kind"] != "paper":
            continue
        docs[p["slug"]] = {"t": p["title"], "u": p["url"]}
    return render_template("notes.html", active="notes", docs=docs)


@app.route("/results")
def results():
    # ⚠ 이 한 화면에 PHASE 노트가 **여러 개** 실린다. 제목 앵커 접두사를 문서마다
    #   다르게 주지 않으면 모든 문서의 id 가 h-1 부터 다시 시작해 겹치고, 목차
    #   링크가 전부 첫 문서로 간다 (실측 버그). 접두사는 **파일 이름**에서만 만든다
    #   — 문서 내용에서 오는 문자열을 id 로 쓰지 않는다.
    docs, csvs = [], []
    dd = C.MO / "docs"
    if dd.is_dir():
        for f in sorted(dd.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            _meta, body = C.split_frontmatter(text)
            did = C.slug_id(f.stem)
            rendered = C.render_digest(body, prefix=did)
            docs.append({"name": f.name, "relpath": f.relative_to(C.ROOT).as_posix(),
                         "html": rendered["html"], "toc": rendered["toc"], "id": did})
    rd = C.MO / "results"
    if rd.is_dir():
        for f in sorted(rd.rglob("*.csv")):
            csvs.append(C.read_csv_view(f))
    return render_template("results.html", active="results", docs=docs, csvs=csvs,
                           phases=C.phase_rail(), chart=C.sweep_chart(),
                           table_max=C.CSV_TABLE_MAX)


@app.route("/gate")
def gate():
    n = request.args.get("n", "3")
    try:
        show = max(1, min(10, int(n)))
    except ValueError:
        show = 3
    g = C.gate_sections(show)
    latest = []
    for n, s in enumerate(g.get("latest", []), 1):
        latest.append({"title": s["title"], "id": f"r-{n}",
                       "meta": C.gate_round_meta(s["title"], s["body"]),
                       "html": C.render_body(s["body"])})
    # 색인은 원장의 **모든** 절을 적지만 화면에 펼친 것은 최근 `show` 개뿐이다.
    # 실제로 이 화면에 있는 절만 링크로 만든다 — 없는 곳으로 가는 링크를 만들지 않는다.
    anchors = {s["title"]: s["id"] for s in latest}
    return render_template("gate.html", active="gate", gate=g, latest=latest,
                           show=show, anchors=anchors)


# ─────────────────────────────────────────────────────────────────────────
# 검색
# ─────────────────────────────────────────────────────────────────────────
@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template("search.html", active="search", q=q, hits=C.search(q))


# ─────────────────────────────────────────────────────────────────────────
# 그림 파일 · 그림 색인 (figref.js 가 쓴다)
# ─────────────────────────────────────────────────────────────────────────
@app.route("/api/figures/<slug>.json")
def api_figures(slug):
    return jsonify({"slug": slug, "figures": C.figures_for(slug)})


# ─────────────────────────────────────────────────────────────────────────
# 커맨드 팔레트 색인 (⌘K / Ctrl-K)
# ─────────────────────────────────────────────────────────────────────────
@app.route("/api/palette.json")
def api_palette():
    """팔레트가 훑을 목적지 목록.

    ⚠ 인라인 `<script>` 나 `<script type="application/json">` 로 심지 않는다 —
      CSP 가 `script-src 'self'` 라서 인라인 script 요소는 종류를 가리지 않고
      막힌다. `connect-src 'self'` 는 열려 있으므로 fetch 로 가져온다.
    """
    items = [
        {"t": "홈 · 카탈로그", "u": "/", "k": "화면", "d": "wiki/index.md + 최근 활동"},
        {"t": "논문 digest", "u": "/papers", "k": "화면", "d": "wiki/raw/papers/"},
        {"t": "열린 질문", "u": "/questions", "k": "화면", "d": "wiki/questions/"},
        {"t": "개념", "u": "/concepts", "k": "화면", "d": "wiki/concepts/"},
        {"t": "satellite 프로젝트", "u": "/entities", "k": "화면", "d": "wiki/entities/"},
        {"t": "Phase 결과", "u": "/results", "k": "화면", "d": "mode-observability"},
        {"t": "게이트 원장", "u": "/gate", "k": "화면", "d": "08_REVIEW_RESPONSE.md"},
        {"t": "검색", "u": "/search", "k": "화면", "d": "전문 부분 문자열 검색"},
    ]
    for p in C.scan_pages().values():
        items.append({"t": p["title"], "u": p["url"], "k": p["kind"],
                      "d": p["description"] or p["relpath"], "s": p["slug"]})
    return jsonify({"items": items})


@app.route("/api/file/<path:rel>")
def api_file(rel):
    """`wiki/raw/figures/<slug>/<file>` 만 서빙 (그 밖은 404)."""
    p = C.safe_file(rel)
    if p is None:
        abort(404)
    return send_from_directory(p.parent, p.name,
                               as_attachment=bool(request.args.get("dl")),
                               download_name=p.name)


@app.errorhandler(404)
def _404(e):
    return render_template("404.html", active=""), 404


if __name__ == "__main__":
    print(f"  repo root : {C.ROOT}")
    print(f"  serving   : http://{HOST}:{PORT}  (읽기 전용)")
    app.run(host=HOST, port=PORT, debug=False)
