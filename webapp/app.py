"""
app.py — DFT 지식 인프라 Flask 앱.
설계: stoic-knuth webapp 인터페이스(사이드바 + CSS변수 테마 + 폴더모델)를
     흰색+한양네이비로 각색하고, 데이터소스를 db/*.json 으로 교체.
동기화: db 파일을 요청마다 읽으므로 계산 등록 즉시 사이트 반영.
"""
from flask import Flask, render_template, jsonify, send_from_directory, abort
from datetime import datetime
import json
from datetime import datetime as _dt
import data as D
import glossary as G

app = Flask(__name__)
_ASSET_V = str(int(datetime.now().timestamp()))

try:
    import markdown as _md
except Exception:
    _md = None


@app.context_processor
def _inject():
    return {"asset_version": _ASSET_V, "COMPS": D.COMPOSITIONS,
            "CATS": D.CATEGORIES, "FAMILY_ORDER": D.FAMILY_ORDER}


# ── 페이지 ──────────────────────────────────────────────
@app.route("/")
def index():
    b = D.build_matrix()
    cov = D.build_coverage(b["properties"], b["prop_category"], b["index_metrics"])
    return render_template("index.html", active="home", b=b, cov=cov,
                           covstat=D.coverage_stats(cov))


@app.route("/composition/<cid>")
def composition(cid):
    if cid not in D.COMPOSITIONS:
        abort(404)
    b = D.build_matrix()
    cov = D.build_coverage(b["properties"], b["prop_category"], b["index_metrics"])
    dop = D.CASCADE_DOPANT.get(cid)
    return render_template(
        "composition.html", active="", cid=cid, cid_active=cid,
        comp=D.COMPOSITIONS[cid], b=b,
        cov=cov.get(cid, {}), structures=D.structures_for(cid),
        datafiles=D.datafiles_for(cid), metrics=b["index_metrics"].get(cid, []),
        rollup=b["comp_data"].get(cid), icohp=D.icohp_for(cid),
        cascade_dopant=dop,
        cascade_rows=D.cascade_rows_for(dop) if dop else None,
        canonical={k: v.get(cid) for k, v in D.CANONICAL.items()},
        canonical_meta=D.CANONICAL_META)


@app.route("/compare")
def compare():
    b = D.build_matrix()
    cov = D.build_coverage(b["properties"], b["prop_category"], b["index_metrics"])
    return render_template("compare.html", active="compare", b=b, cov=cov)


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
                           stats=stats, deep_map=deep_map)


@app.route("/methods")
def methods():
    md = D.load_canonical_methods()
    html = _md.markdown(md, extensions=["tables", "fenced_code", "toc"]) if _md else "<pre>" + md + "</pre>"
    return render_template("doc.html", active="methods",
                           title="계산 방법 Canonical (단일 기준)", content=html)


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
    if not p.exists():
        abort(404)
    return jsonify(json.loads(p.read_text()))


@app.route("/api/paper/<pid>")
def api_paper(pid):
    p = D.LITDB / "papers" / f"{pid}.md"
    if not p.exists():
        abort(404)
    html = _md.markdown(p.read_text(errors="ignore"), extensions=["tables", "fenced_code"]) if _md else p.read_text()
    return jsonify({"id": pid, "html": html})


@app.route("/glossary")
def glossary():
    return render_template("glossary.html", active="glossary",
                           cats=G.by_category(), cat_order=G.CATS_G,
                           concepts=D.concept_ids())


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
    return render_template("concept.html", active="glossary", cid=cid,
                           term=term, raw_md=md, siblings=siblings)


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
        for line in JOURNAL.read_text(errors="ignore").splitlines():
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
    d = request.get_json(force=True) or {}
    rec = {"ts": _dt.now().isoformat(timespec="minutes"),
           "kind": d.get("kind", "note"), "comp": d.get("comp", ""),
           "text": (d.get("text") or "").strip()}
    if not rec["text"]:
        return jsonify({"ok": False, "err": "empty"}), 400
    with open(JOURNAL, "a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return jsonify({"ok": True, "entry": rec})


@app.route("/api/handoff/<hid>")
def api_handoff(hid):
    f = D.KB / "results" / f"{hid}.md"
    if not f.exists():
        abort(404)
    html = _md.markdown(f.read_text(errors="ignore"), extensions=["tables", "fenced_code"]) if _md else f.read_text()
    return jsonify({"id": hid, "html": html})


@app.route("/health")
def health():
    return jsonify({"ok": True, "asset": _ASSET_V})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
