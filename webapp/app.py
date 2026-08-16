"""
app.py — DFT 지식 인프라 Flask 앱.
설계: stoic-knuth webapp 인터페이스(사이드바 + CSS변수 테마 + 폴더모델)를
     흰색+한양네이비로 각색하고, 데이터소스를 db/*.json 으로 교체.
동기화: db 파일을 요청마다 읽으므로 계산 등록 즉시 사이트 반영.
"""
from flask import Flask, render_template, jsonify, send_from_directory, abort, request
import re
from markupsafe import Markup, escape
from datetime import datetime
import json, os, re
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
#   로컬에서 쓰기를 켜려면:  ALLOW_MUTATIONS=1 python3 webapp/app.py
#   (RENDER 환경변수가 있으면 명시적으로 켜지 않는 한 항상 잠근다.)
# ─────────────────────────────────────────────────────────────
_ON_RENDER = bool(os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"))
ALLOW_MUTATIONS = os.environ.get("ALLOW_MUTATIONS", "").strip() in ("1", "true", "yes")
READ_ONLY = not ALLOW_MUTATIONS


def _guard_mutation():
    """쓰기 라우트 앞에 건다. 잠겨 있으면 403 과 **켜는 방법**을 같이 준다."""
    if not READ_ONLY:
        return None
    return jsonify({
        "error": "읽기 전용 모드예요 — 이 서버에서는 저장이 꺼져 있어요.",
        "why": ("공개 배포에는 인증이 없고, Render 기본 파일시스템은 재시작 때 초기화돼서 "
                "어차피 기록이 남지 않아요."),
        "how": "로컬에서 쓰려면 ALLOW_MUTATIONS=1 로 실행하세요.",
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
_MDL_MAXB = 300
_MDL_BOLD = re.compile(r"\*\*(?![\s)\]}>,.;:!?])(.{1,%d}?)(?<![\s([{<])\*\*" % _MDL_MAXB, re.S)
_MDL_CODE = re.compile(r"`([^`]+)`")


def _mdlite(text: str) -> Markup:
    s = str(escape(text or ""))
    spans = []                                   # ① 코드 스팬 격리

    def _stash(m):
        spans.append(m.group(1))
        return "\x00%d\x00" % (len(spans) - 1)

    s = _MDL_CODE.sub(_stash, s)
    s = _MDL_BOLD.sub(r"<strong>\1</strong>", s)
    s = re.sub(r"\x00(\d+)\x00",
               lambda m: '<code class="mono">%s</code>' % spans[int(m.group(1))], s)
    return Markup(s)


app.jinja_env.filters['mdlite'] = _mdlite


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

    ⚠ raw HTML 을 껐다고 끝이 아니다 (2026-08-07 리뷰 P2): 파서는 **URL scheme 을 안 본다**.
      `[click](javascript:alert(1))` 이 그대로 `<a href="javascript:...">` 로 나갔다.
      litdb digest 는 논문 에이전트가 외부 PDF 를 요약해 쓰는 파일이라 입력이 100% 신뢰
      대상이 아니므로, 렌더 결과의 href/src 를 **허용 scheme 만 통과**시킨다.
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
    return _sanitize_urls(md.convert(text or ""))


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
                           covstat=D.coverage_stats(cov), highlights=D.dashboard_highlights(),
                           sei=D.sei_summary(), sei_axes=D.sei_axes())


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
        # ⚠ ICOHP JSON 과 COHP 곡선 CSV 는 독립이다 (comp2 는 곡선만 있다) — 따로 넘긴다
        cohp_curves=D.cohp_curves_for(cid), elf_curves=D.elf_curves_for(cid),
        cascade_dopant=dop, cascade_meta=D.CASCADE_META,
        cascade_join=D.CASCADE_JOIN_STATUS.get(cid),
        cascade_rows=D.cascade_rows_for(dop) if dop else None,
        canonical=D.canonical_values(cid),
        canonical_status=D.canonical_status_for(cid), MM=D.metric_meta(),
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
    meta = {f"{k}|{c}": {"group": e.get("comparison_group"),
                         "status": e.get("status"),
                         "method": e.get("method_id"),
                         "n_seed": e.get("n_seed"),
                         "u": e.get("uncertainty"),
                         "src": e.get("source_path"),
                         "note": e.get("note")}
            for (k, c), e in D.CANONICAL_ENTRY.items() if k and c}
    return render_template("compare.html", bvse=bvse, active="compare", b=b,
                           canonical=D.canonical_table(), canonical_provisional=prov,
                           canonical_meta=meta, metric_meta=D.metric_meta(),
                           canonical_prov={f'{k}|{c}': v for (k, c), v in
                                           D.canonical_provenance_flags().items()})


@app.route("/cascade")
def cascade_page():
    casc = D.load_cascade()
    ranked = casc.get("ranked", {}).get("data", [])
    ver = casc.get("verified") or {}
    comp = ver.get("compounds")
    # ⚠ 2026-08-14 — 이 수치들은 **superseded 47종판**의 것이다. 최상단 타일은
    #    D.CASCADE_TRUTH(273/270/90/0)를 쓰고, 아래는 보관함 탭 안에서만 쓴다.
    stats = {
        "dopants": len(ranked),
        "pareto": sum(1 for r in ranked if str(r.get("pareto", "")).strip().upper() == "Y"),
        "champions": len(casc.get("champions", {}).get("data", [])),
        "verified": (len(comp) if isinstance(comp, (list, dict)) else None),
    }
    deep_map = {v: k for k, v in D.CASCADE_DOPANT.items()}
    # 계보 패널의 논문 링크는 실제 digest 가 있는 것만 — 없는 slug 는 링크를 죽인다
    have = {p["id"] for p in D.list_papers()}
    return render_template("cascade.html", active="cascade", casc=casc,
                           stats=stats, deep_map=deep_map,
                           lineage=D.METHOD_LINEAGE, lit_have=have,
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
    return render_template("explorer.html", active="explorer",
                           canonical=D.canonical_table(), canonical_meta=D.CANONICAL_META,
                           canonical_provisional=D.CANONICAL_PROVISIONAL,
                           canonical_status=D.canonical_status_all(), MM=D.metric_meta(),
                           canonical_prov=D.canonical_provenance_flags(),
                           comp_elements=D.COMP_ELEMENTS,
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
                           title="계산 방법 Canonical (단일 기준)", content=html,
                           subtitle="kb/methodology/computational_methods_canonical.md · 값 인용 전 단일 기준")


@app.route("/todo")
def todo():
    md = D.load_open_items_md()
    html = md_html(md, ("tables", "fenced_code", "toc"))
    return render_template("doc.html", active="todo",
                           title="📋 미결 리스트 (Open Items)",
                           content=html,
                           subtitle="kb/open_items.md · 판정 대기 · PDF 확보 대기 · ML 후속 · 심포지엄 대응")


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
    return render_template("benchmarks.html", active="bench", b=b,
                           ledger=D.deck_correction_ledger(),
                           revisions=D.verdict_revisions(),
                           committee=D.mlip_committee(),
                           lit_have={p["id"] for p in D.list_papers()},
                           talks_have={t["id"] for t in D.list_talks()})


@app.route("/literature")
def literature():
    papers = D.list_papers()
    counts = {"all": len(papers),
              "dft": sum(1 for p in papers if p["track"] == "dft"),
              "dem": sum(1 for p in papers if p["track"] == "dem")}
    pi_counts = {}
    for it in papers + D.list_talks():
        for k in it.get("pis", []):
            pi_counts[k] = pi_counts.get(k, 0) + 1
    pis = [dict(p, n=pi_counts.get(p["key"], 0)) for p in D.PI_REGISTRY if pi_counts.get(p["key"])]
    pis.sort(key=lambda x: (not x["our"], -x["n"]))
    tmeta = D.topic_meta()
    tcounts = {k: sum(1 for p in papers if k in p["topics"]) for k in tmeta}
    return render_template("literature.html", active="lit", papers=papers,
                           count=len(papers), counts=counts, talks=D.list_talks(),
                           tmeta=tmeta, tcounts=tcounts, tprimer=D.topic_primer(),
                           pis=pis, PI=D.PI_BY_KEY, figcount=D.papers_with_figures(),
                           figsearch=D.paper_figure_search(),
                           cmtsearch=D.paper_comment_search())


# ── API (구조뷰 / 차트 / 원본) ──────────────────────────
@app.route("/api/structure/<path:fn>")
def api_structure(fn):
    return send_from_directory(D.DB / "structures", fn)


@app.route("/api/csv/<path:rel>")
def api_csv(rel):
    # ⛔ 2026-08-14 (Codex Round-3 P0-3) — 정책이 headline 에만 걸려 있어서
    #   화면에서 숨긴 artifact 를 이 경로로 그냥 받을 수 있었다. 이제 공통 resolver 를 탄다.
    v = AP.resolve(f"db/{rel}" if not str(rel).startswith("db/") else rel, request.args)
    if not v["allowed"]:
        return jsonify({"error": v["reason"], "needs": v["needs"],
                        **AP.envelope(rel, v)}), 403
    out = D.read_csv(rel)
    if v["governed"]:
        out = {**out, "_artifact_status": AP.envelope(rel, v)}
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
    if not rel.startswith("litdb/figures/") or len(seg) != 4:
        return None
    return {"slug": seg[2], "cmt": D.paper_comment_search().get(seg[2], "")}


@app.route("/api/comments/<path:rel>", methods=["GET", "POST"])
def api_comments(rel):
    """파일 코멘트 읽기/달기 (Notion 식 💬). 대상은 실존 repo 파일만."""
    if request.method == "GET":
        return jsonify({"rel": rel, "items": D.file_comments(rel),
                        "paper": _paper_cmt_index(rel)})
    g = _guard_mutation()
    if g:
        return g
    d = request.get_json(silent=True) or {}
    r = D.add_file_comment(rel, str(d.get("text", "")), str(d.get("who", "")))
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


@app.route("/files")
def files_gallery():
    q = request.args.get("q", "").strip()
    kind = request.args.get("kind", "").strip()
    used = request.args.get("used", "").strip()
    folder = request.args.get("folder", "").strip()
    cmt = request.args.get("cmt", "").strip()
    fs = D.gallery_files(q, kind, used, folder, cmt)
    return render_template("files.html", active="files", files=fs, q=q, kind=kind,
                           used=used, folder=folder, cmt=cmt, days=D.gallery_days(fs),
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
    p = D.LITDB / "papers" / f"{pid}.md"
    if not p.exists():
        p = D.LITDB / "talks" / f"{pid}.md"
    if not p.exists():
        abort(404)
    html = md_html(p.read_text(encoding="utf-8", errors="ignore"))
    # 크로핑된 논문 그림 — 본문의 "Fig. 5e" 를 브라우저에서 링크로 바꿔 여백에 띄운다.
    return jsonify({"id": pid, "html": html, "figures": D.paper_figures(pid)})


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
                     "rel": str(path.relative_to(D.ROOT)),
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
                           decks=decks)


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
                           papers=D.glossary_papers(cid),
                           attachments=(_att := D.concept_attachments(cid)),
                           att_days=D.gallery_days(_att), ccounts=D.comment_counts())


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
