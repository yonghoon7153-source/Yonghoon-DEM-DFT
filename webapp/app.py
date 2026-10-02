"""app.py — Li2S ASSB 위키 대시보드 (로컬 · 읽기 전용 + 위키 근거 대화).

무엇을 서빙하나
  wiki/ (index·log·논문 digest·질문·개념·프로젝트·가이드…) · 논문 비교표(`compare:`) ·
  연구 로드맵 · /chat (위키 절을 근거로 Claude 와 대화 — 서버는 아무것도 저장하지 않는다).

무엇을 안 하나
  위키 쓰기. 코멘트·이름변경·업로드·하이라이트 저장이 없다. `_guard_mutation` 이 GET/HEAD/
  OPTIONS 외 메서드를 막고, 예외는 `/api/chat`·`/api/md` (둘 다 파일을 쓰지 않는 POST) 뿐이다.

띄우기:  webapp/li2s.sh   또는   python3 webapp/app.py   (기본 http://127.0.0.1:5100)
"""
from __future__ import annotations

import os

from flask import (Flask, Response, abort, jsonify, render_template, request,
                   send_from_directory, stream_with_context)
from markupsafe import Markup

import chat as CH
import content as C

app = Flask(__name__)

# 템플릿·정적파일을 매 요청마다 다시 읽는다 (debug=False 로 뜨므로 명시해야 한다 —
# 선행 브랜치에서 "고쳤는데 똑같다" 를 한 라운드 낭비한 함정). config 는 jinja_env 접근 전에.
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["MAX_CONTENT_LENGTH"] = 512 * 1024      # /api/chat 본문 상한 (대화 기록 포함)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

HOST = os.environ.get("WEBAPP_HOST", "127.0.0.1")
PORT = int(os.environ.get("WEBAPP_PORT", "5100"))

_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
# 쓰기 메서드를 받는 유일한 길 — 둘 다 저장소에 아무것도 쓰지 않는다.
_POST_ALLOWED = {"/api/chat", "/api/md"}


@app.before_request
def _guard_mutation():
    """읽기 전용 게이트 — 허용 목록 밖의 쓰기 메서드는 라우트에 닿기 전에 거절 (fail-closed)."""
    if request.method in _SAFE_METHODS:
        return None
    if request.method == "POST" and request.path in _POST_ALLOWED:
        return None
    return jsonify({
        "error": "읽기 전용 앱입니다 — 쓰기 메서드를 받지 않습니다.",
        "why": "wiki/raw/ 는 sha256 봉인 불변층이고 컴파일 페이지의 정본은 저장소 파일입니다. "
               "예외는 /api/chat 과 /api/md 뿐이며 둘 다 파일을 쓰지 않습니다.",
        "method": request.method,
    }), 405


@app.after_request
def _sec_headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("Referrer-Policy", "same-origin")
    resp.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    # 브라우저는 이 서버와만 이야기한다. Anthropic API 호출은 서버 쪽(chat.py)에서만.
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


@app.template_filter("mdi")
def _mdi(s):
    return Markup(C.md_inline(s))


@app.context_processor
def _inject():
    return {"asset_version": _asset_version(), "wl_index": C.page_index(),
            "chat_status": CH.available()}


def _page_or_404(kind: str, slug: str) -> dict:
    p = C.scan_pages().get(slug)
    if not p or p["kind"] != kind:
        abort(404)
    return p


def _read(p: dict) -> tuple[dict, str]:
    text = p["path"].read_text(encoding="utf-8")
    return C.split_frontmatter(text)


# ─────────────────────────────────────────────────────────────────────────
# 홈 · 로드맵
# ─────────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    pages = C.scan_pages()
    idx_file = C.WIKI / "index.md"
    idx_html = C.render_body(idx_file.read_text(encoding="utf-8")) if idx_file.is_file() else ""
    counts: dict[str, int] = {}
    for p in pages.values():
        counts[p["kind"]] = counts.get(p["kind"], 0) + 1
    # 홈의 "지금 열려 있는 질문" 패널은 **열린 카드를 전부** 보여준다.
    # 2026-10-02: 여기가 `[:4]` 로 잘려 있어서 카드가 5장이 된 순간 하나가 홈에서
    # 사라졌다 (사용자가 "홈페이지에 반영이 안 된다" 고 알려 준 증상의 절반).
    # 갯수를 손으로 세는 상수는 쓰지 않는다 — 닫힌 카드(status 가 open/active 가
    # 아닌 것)는 자연히 빠지므로 이 필터가 스스로 유지된다.
    # smoke.py 의 "home lists open question" 검사가 이 동작을 고정한다.
    OPEN = {"open", "active"}
    questions = sorted(
        [p for p in pages.values()
         if p["kind"] == "question"
         and str(p["meta"].get("status", "open")).strip().lower() in OPEN],
        key=lambda x: x["updated"], reverse=True)
    return render_template("index.html", active="home", index_html=idx_html,
                           log=C.recent_log(8), counts=counts, total=len(pages),
                           questions=questions)


@app.route("/roadmap")
def roadmap():
    """연구 개요 — 처음 온 사람(또는 미래의 나)을 위한 한 장.

    ⚠ 숫자를 새로 만들지 않는다. 화면의 조성·목표는 킥오프 기록(사용자 진술)의 사본이고,
      실험 수치는 화면에 없다 (정본은 실험 노트). 페이지 카운트만 실물을 센다.
    """
    pages = C.scan_pages()
    ents = [p for p in pages.values() if p["kind"] == "entity"]
    qs = [p for p in pages.values() if p["kind"] == "question"]
    papers = [p for p in pages.values() if p["kind"] == "paper"]
    return render_template("roadmap.html", active="roadmap", ents=ents, qs=qs,
                           papers=papers, n_concepts=sum(1 for p in pages.values() if p["kind"] == "concept"))


# ─────────────────────────────────────────────────────────────────────────
# 논문 digest · 비교표
# ─────────────────────────────────────────────────────────────────────────
_FAVICON = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
    '<rect width="32" height="32" rx="7" fill="#0f6f6b"/>'
    '<text x="16" y="21.5" font-family="Helvetica,Arial,sans-serif" font-size="13" font-weight="700"'
    ' text-anchor="middle" fill="#fff">Li₂S</text></svg>')


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
        cmp_ = meta.get("compare") if isinstance(meta.get("compare"), dict) else {}
        items.append({
            **p,
            "sha12": str(meta.get("sha256") or "")[:12],
            "source_url": str(meta.get("source_url") or ""),
            "doi": str(meta.get("doi") or ""),
            "ingested": str(meta.get("ingested") or ""),
            "nfig": len(figs),
            "nsi": sum(1 for f in figs if str(f["label"]).upper().startswith("S")),
            "system": str(cmp_.get("system") or ""),
            "loading": str(cmp_.get("loading_mg_cm2") or ""),
            "anode": str(cmp_.get("anode") or ""),
        })
    items.sort(key=lambda x: (x["ingested"] or "", x["slug"]), reverse=True)
    return render_template("papers.html", active="papers", items=items)


@app.route("/paper/<slug>")
def paper(slug):
    p = _page_or_404("paper", slug)
    meta, body = _read(p)
    figs = C.figures_for(slug)
    doc = C.render_digest(body, title=meta.get('title') or p['title'])
    cmp_ = meta.get("compare") if isinstance(meta.get("compare"), dict) else {}
    cmp_rows = [(h, str(cmp_.get(k))) for k, h, _d in C.COMPARE_COLUMNS if cmp_.get(k) not in (None, "")]
    return render_template("paper.html", active="papers", page=p, meta=meta,
                           body_html=doc["html"], toc=doc["toc"], claims=doc["claims"],
                           figs=figs, figmeta=C.figure_meta(slug), cmp_rows=cmp_rows,
                           sha=str(meta.get("sha256") or ""))


@app.route("/compare")
def compare():
    rows = C.compare_rows()
    return render_template("compare.html", active="compare", rows=rows,
                           columns=C.COMPARE_COLUMNS)


# ─────────────────────────────────────────────────────────────────────────
# 질문 카드
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
    nav = [{"id": s["id"], "title": s["title"], "cls": s["cls"]} for s in secs if s["title"]]
    return render_template("question.html", active="questions", page=p, meta=meta,
                           blocks=blocks, nav=nav)


# ─────────────────────────────────────────────────────────────────────────
# 개념 · 프로젝트 · 그 밖의 위키 문서
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
    """guides · queries · syntheses · comparisons · raw/transcripts 등 — 등록부에서만 찾는다."""
    slug = rel.rstrip("/").split("/")[-1]
    p = C.scan_pages().get(slug)
    if not p or p["url"] != "/doc/" + rel.strip("/"):
        abort(404)
    meta, body = _read(p)
    d = C.render_digest(body, title=meta.get('title') or p['title'])
    active = {"guide": "", "query": "", "comparison": "compare"}.get(p["kind"], "")
    return render_template("doc.html", active=active, page=p, meta=meta,
                           body_html=d["html"], toc=d["toc"], claims=d["claims"])


# ─────────────────────────────────────────────────────────────────────────
# 대화 — 위키 근거로 Claude 와
# ─────────────────────────────────────────────────────────────────────────
@app.route("/chat")
def chat():
    pages = C.scan_pages()
    starters = [
        "Kim 2023 의 첫 충전 활성화 관찰(Fig. S1)이 우리 reference cell 설계에 주는 함의는?",
        "우리 30:50:20 조성과 Kim 2023 의 75:25 조성은 무엇이 다르고, 옮길 수 있는 것은 무엇인가?",
        "one-step 과 two-step 혼합 중 지금 위키 근거로는 어느 쪽이 유리한가? 무엇이 부족한가?",
        "500–600 mAh g⁻¹ 목표를 (S) 기준과 (Li2S) 기준으로 각각 환산해 줘.",
        "Kim 2023 digest 의 공백표에서 세미나 질문으로 쓸 만한 것 세 개를 골라 줘.",
    ]
    return render_template("chat.html", active="chat", status=CH.available(),
                           n_pages=len(pages), starters=starters)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """SSE 스트림. 본문 {question, history:[{role, content}]}. 서버는 아무것도 저장하지 않는다."""
    data = request.get_json(silent=True) or {}
    q = str(data.get("question") or "").strip()
    if not q:
        return jsonify({"error": "질문이 비어 있다."}), 400
    if len(q) > 8000:
        return jsonify({"error": "질문이 너무 길다 (8000자 상한)."}), 400
    history = data.get("history") or []
    if not isinstance(history, list):
        history = []
    st = CH.available()
    if not st["ok"]:
        return jsonify({"error": "chat 비활성 — ANTHROPIC_API_KEY 가 없거나 SDK 가 없다.",
                        "status": st}), 503
    gen = CH.stream_answer(q, history)
    return Response(stream_with_context(gen), mimetype="text/event-stream",
                    headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.route("/api/chat/status")
def api_chat_status():
    return jsonify(CH.available())


@app.route("/api/md", methods=["POST"])
def api_md():
    """마크다운 → 우리 렌더러(raw HTML 차단 + wikilink) 로 HTML. chat 답변 표시용. 저장 없음."""
    data = request.get_json(silent=True) or {}
    text = str(data.get("text") or "")
    if len(text) > 200_000:
        return jsonify({"error": "too long"}), 400
    return jsonify({"html": C.render_body(text)})


# ─────────────────────────────────────────────────────────────────────────
# 메모 · 검색 · API
# ─────────────────────────────────────────────────────────────────────────
@app.route("/notes")
def notes():
    docs = {}
    for p in C.scan_pages().values():
        if p["kind"] in ("paper", "concept", "entity", "question", "comparison", "query", "guide"):
            docs[p["slug"]] = {"t": p["title"], "u": p["url"]}
    return render_template("notes.html", active="notes", docs=docs)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return render_template("search.html", active="search", q=q, hits=C.search(q))


@app.route("/api/figures/<slug>.json")
def api_figures(slug):
    return jsonify({"slug": slug, "figures": C.figures_for(slug)})


@app.route("/api/palette.json")
def api_palette():
    items = [
        {"t": "홈 · 카탈로그", "u": "/", "k": "화면", "d": "wiki/index.md + 최근 활동"},
        {"t": "연구 로드맵", "u": "/roadmap", "k": "화면", "d": "reference cell → anode-free"},
        {"t": "논문 digest", "u": "/papers", "k": "화면", "d": "wiki/raw/papers/"},
        {"t": "논문 비교표", "u": "/compare", "k": "화면", "d": "digest compare: 블록"},
        {"t": "열린 질문", "u": "/questions", "k": "화면", "d": "wiki/questions/"},
        {"t": "개념", "u": "/concepts", "k": "화면", "d": "wiki/concepts/"},
        {"t": "프로젝트", "u": "/entities", "k": "화면", "d": "wiki/entities/"},
        {"t": "위키와 대화", "u": "/chat", "k": "화면", "d": "위키 절을 근거로 Claude 와"},
        {"t": "검색", "u": "/search", "k": "화면", "d": "전문 부분 문자열 검색"},
    ]
    for p in C.scan_pages().values():
        items.append({"t": p["title"], "u": p["url"], "k": p["kind_label"],
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
    print(f"  serving   : http://{HOST}:{PORT}  (읽기 전용 · chat={'on' if CH.available()['ok'] else 'off'})")
    app.run(host=HOST, port=PORT, debug=False, threaded=True)
