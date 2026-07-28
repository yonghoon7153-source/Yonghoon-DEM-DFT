"""
app.py — DFT 지식 인프라 Flask 앱.
설계: stoic-knuth webapp 인터페이스(사이드바 + CSS변수 테마 + 폴더모델)를
     흰색+한양네이비로 각색하고, 데이터소스를 db/*.json 으로 교체.
동기화: db 파일을 요청마다 읽으므로 계산 등록 즉시 사이트 반영.
"""
from flask import Flask, render_template, jsonify, send_from_directory, abort, request
from datetime import datetime
import json, os
from datetime import datetime as _dt
import data as D
import glossary as G

app = Flask(__name__)

try:
    import markdown as _md
except Exception:
    _md = None


def md_html(text: str, extensions=("tables", "fenced_code")) -> str:
    """마크다운 → HTML. **raw HTML 통과는 끈다.**

    렌더 결과가 innerHTML(literature.html·log.html) 과 |safe(doc/concept) 로 들어가는데,
    Python-Markdown 은 기본적으로 raw HTML 을 그대로 흘려보낸다(safe_mode 폐지됨).
    litdb digest 는 논문 에이전트가 외부 PDF 를 요약해 쓰는 파일이라 입력이 100% 신뢰
    대상은 아니므로, 태그를 통째로 이스케이프하는 대신 파서 단계에서 raw HTML 만 끈다
    (표·코드블록 등 정상 마크다운 렌더는 그대로 유지된다).
    """
    if _md is None:
        return "<pre>" + (text or "") + "</pre>"
    md = _md.Markdown(extensions=list(extensions))
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
    return md.convert(text or "")


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
    return {"asset_version": _css_ver(), "vsrc": _vsrc, "COMPS": D.COMPOSITIONS,
            "CATS": D.CATEGORIES, "FAMILY_ORDER": D.FAMILY_ORDER}


# ── 페이지 ──────────────────────────────────────────────
@app.route("/")
def index():
    b = D.build_matrix()
    cov = D.build_coverage(b["properties"], b["prop_category"], b["index_metrics"])
    # N/A(성립 안 함/규율상 금지) 칸은 TODO 와 구분해서 렌더 — 튜플 키는 Jinja 에서 못 쓰니 평탄화
    na = {f"{c}|{k}": r for (c, k), r in D.NOT_APPLICABLE.items()}
    return render_template("index.html", active="home", b=b, cov=cov, NA=na,
                           oi=D.open_items_summary(),
                           covstat=D.coverage_stats(cov), highlights=D.dashboard_highlights())


@app.route("/composition/<cid>")
def composition(cid):
    if cid not in D.COMPOSITIONS:
        abort(404)
    b = D.build_matrix()
    dop = D.CASCADE_DOPANT.get(cid)
    return render_template(
        "composition.html", active="", cid=cid, cid_active=cid,
        comp=D.COMPOSITIONS[cid], structures=D.structures_for(cid),
        index_built=b.get("built"),   # Raw 탭 스냅샷 배너 (전체 b 번들은 템플릿에 불필요)
        datafiles=D.datafiles_for(cid), metrics=b["index_metrics"].get(cid, []),
        rollup=b["comp_data"].get(cid), icohp=D.icohp_for(cid),
        cascade_dopant=dop, cascade_meta=D.CASCADE_META,
        cascade_rows=D.cascade_rows_for(dop) if dop else None,
        canonical=D.canonical_values(cid),
        canonical_meta=D.CANONICAL_META,
        canonical_provisional={k: r for (k, c), r in D.CANONICAL_PROVISIONAL.items() if c == cid},
        canonical_na={k: r for (k, c), r in D.CANONICAL_NA.items() if c == cid})


@app.route("/compare")
def compare():
    b = D.build_matrix()
    # ⚠ CANONICAL_PROVISIONAL 은 (key, cid) 튜플 키라 |tojson 이 TypeError 를 낸다 → 문자열로 평탄화.
    prov = {f"{k}|{c}": r for (k, c), r in D.CANONICAL_PROVISIONAL.items()}
    return render_template("compare.html", active="compare", b=b,
                           canonical=D.canonical_table(), canonical_provisional=prov)


@app.route("/cascade")
def cascade_page():
    casc = D.load_cascade()
    ranked = casc.get("ranked", {}).get("data", [])
    ver = casc.get("verified") or {}
    comp = ver.get("compounds")
    stats = {
        "dopants": len(ranked),
        "pareto": sum(1 for r in ranked if str(r.get("pareto", "")).strip().upper() == "Y"),
        "champions": len(casc.get("champions", {}).get("data", [])),
        "verified": (len(comp) if isinstance(comp, (list, dict)) else None),
    }
    deep_map = {v: k for k, v in D.CASCADE_DOPANT.items()}
    return render_template("cascade.html", active="cascade", casc=casc,
                           stats=stats, deep_map=deep_map,
                           mo_db=D.load_molecular_orbitals())


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
    return render_template("explorer.html", active="explorer",
                           canonical=D.canonical_table(), canonical_meta=D.CANONICAL_META,
                           canonical_provisional=D.CANONICAL_PROVISIONAL,
                           comp_elements=D.COMP_ELEMENTS,
                           categories=D.CATEGORIES)


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


@app.route("/api/element")
def api_element():
    from flask import request
    syms = [s.strip() for s in request.args.get("syms", "").split(",") if s.strip()]
    return jsonify(D.element_briefing(syms))


@app.route("/methods")
def methods():
    md = D.load_canonical_methods()
    html = md_html(md, ("tables", "fenced_code", "toc"))
    return render_template("doc.html", active="methods",
                           title="계산 방법 Canonical (단일 기준)", content=html)


@app.route("/todo")
def todo():
    md = D.load_open_items_md()
    html = md_html(md, ("tables", "fenced_code", "toc"))
    return render_template("doc.html", active="todo",
                           title="📋 미결 리스트 (Open Items) — kb/open_items.md",
                           content=html)


@app.route("/literature")
def literature():
    papers = D.list_papers()
    counts = {"all": len(papers),
              "dft": sum(1 for p in papers if p["track"] == "dft"),
              "dem": sum(1 for p in papers if p["track"] == "dem")}
    return render_template("literature.html", active="lit", papers=papers,
                           count=len(papers), counts=counts)


# ── API (구조뷰 / 차트 / 원본) ──────────────────────────
@app.route("/api/structure/<path:fn>")
def api_structure(fn):
    return send_from_directory(D.DB / "structures", fn)


@app.route("/api/csv/<path:rel>")
def api_csv(rel):
    return jsonify(D.read_csv(rel))


@app.route("/api/property/<name>")
def api_property(name):
    p = D.DB / "properties" / f"{name}.json"
    d = D._load_json(p) if p.exists() else None
    if d is None:            # 없거나 깨진 JSON → 500 대신 404 (silent 500+traceback 방지)
        abort(404)
    return jsonify(d)


@app.route("/api/paper/<pid>")
def api_paper(pid):
    p = D.LITDB / "papers" / f"{pid}.md"
    if not p.exists():
        abort(404)
    html = md_html(p.read_text(encoding="utf-8", errors="ignore"))
    return jsonify({"id": pid, "html": html})


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
    # 서버 렌더 fallback — marked.js CDN 미로드시에도 raw dump 대신 서식 유지
    fallback = md_html(md)
    return render_template("concept.html", active="glossary", cid=cid,
                           term=term, raw_md=md, siblings=siblings, fallback_html=fallback,
                           papers=D.glossary_papers(cid))


@app.route("/api/concept/<cid>")
def api_concept(cid):
    md = D.read_concept(cid)
    if md is None:
        abort(404)
    return jsonify({"id": cid, "markdown": md})


# ── 작업 로그 (기록·저장) ─────────────────────────────
JOURNAL = D.ROOT / "webapp" / "journal.jsonl"


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
    out = []
    rd = D.KB / "results"
    if rd.exists():
        for f in sorted(rd.glob("*.md"), reverse=True):
            out.append({"id": f.stem, "name": f.stem.replace("_", " ")})
    return out


@app.route("/log")
def log():
    return render_template("log.html", active="log",
                           entries=_load_journal(), handoffs=_handoffs())


@app.route("/api/log", methods=["POST"])
def api_log():
    from flask import request
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
    f = D.KB / "results" / f"{hid}.md"
    if not f.exists():
        abort(404)
    html = md_html(f.read_text(encoding="utf-8", errors="ignore"))
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
