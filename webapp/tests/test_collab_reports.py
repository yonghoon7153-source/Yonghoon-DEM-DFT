"""공유 보고서 화면 (/reports · /reports/<slug> · /reports/<slug>/raw · 2026-11-24) — 렌더 · 원본 그대로 · 기업 이름 · 없는 파일 ·
결속 검사 열거 · 여백 메모 딥링크 · 사이드바.

사용자 2026-11-24: '이렇게 정리했던 html 등 혁주(lzo), …, Wad (DEM-DFT) 관련해서 html 웹페이지에도 링크나 저장을 해줘'.
표 = data.COLLAB_REPORTS (집). 보기 화면은 /interface-thermo 와 같은 꼴 (iframe · docnote 여백 메모 · 형광펜).

⛔ 이 파일이 못 하는 것: 보고서 문장 · 값이 원장과 맞는지는 안 본다 (값 결속은 test_v3_surfaces 의 정의역 자동 열거가
  /reports/<slug>/raw 를 그대로 훑는다 — 아래 test_routes_are_in_the_surface_scan 이 그 열거에 실제로 드는지 본다).
  iframe 높이 · 칠하기 (JS) 는 브라우저 없이는 못 본다 (같은 장치를 interface_thermo 쪽 docnote_paint.test.mjs 가 본다).
"""
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as A      # noqa: E402
import data as D     # noqa: E402
import nav as N      # noqa: E402

_COMPANY = ("SDI", "삼성", "Samsung", "samsung")


def _client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def _text(html):
    return re.sub(r"data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+", "", html)


def _company_hits(t):
    return [w for w in _COMPANY if w in t]


def test_registry_titles_are_the_documents_own_h1():
    """양성+⛔음성: 표의 제목은 그 문서의 <h1> 그대로다 (화면이 제목을 지어내지 않는다) · 슬러그 유일 · docs/collab 의 있는 HTML."""
    slugs = [r["slug"] for r in D.COLLAB_REPORTS]
    assert len(slugs) == len(set(slugs)) == 3, slugs
    for r in D.COLLAB_REPORTS:
        assert r["rel"].startswith("docs/collab/") and r["rel"].endswith(".html"), r["rel"]
        p = D.ROOT / r["rel"]
        assert p.is_file(), r["rel"]
        h1 = re.search(r"<h1>(.*?)</h1>", p.read_text(encoding="utf-8"), re.S).group(1)
        assert re.sub(r"<[^>]+>", "", h1).strip() == r["title"], (r["slug"], h1)
        assert D.COLLAB_BY_SLUG[r["slug"]] is r
        for e in r.get("earlier", ()):
            assert (D.ROOT / e["rel"]).is_file() and e["rel"] != r["rel"], e


def test_list_page_links_every_report():
    """양성: 목록이 통합 보고 + 표의 보고서마다 보기 화면 링크 · 새 탭 · 내려받기 · 앞 판 링크를 준다."""
    h = _client().get("/reports").get_data(as_text=True)
    assert 'href="/interface-thermo"' in h
    for r in D.COLLAB_REPORTS:
        assert f'href="/reports/{r["slug"]}"' in h and r["title"] in h, r["slug"]
        assert f'href="/reports/{r["slug"]}/raw"' in h and f'href="/api/file/{r["rel"]}?dl=1"' in h, r["slug"]
        for e in r.get("earlier", ()):
            assert f'href="/api/file/{e["rel"]}"' in h, e


def test_each_view_frames_its_raw_and_raw_is_the_file_byte_for_byte():
    """양성+⛔음성: 보기 화면은 자기 원문 경로를 iframe 으로 띄우고, 원문 경로는 파일을 바이트 그대로 낸다 (docnote 흔적 없음)."""
    c = _client()
    for r in D.COLLAB_REPORTS:
        v = c.get(f"/reports/{r['slug']}")
        assert v.status_code == 200, r["slug"]
        h = v.get_data(as_text=True)
        assert f'src="/reports/{r["slug"]}/raw"' in h and "<iframe" in h, r["slug"]
        raw = c.get(f"/reports/{r['slug']}/raw")
        assert raw.status_code == 200 and raw.mimetype == "text/html", (r["slug"], raw.status_code, raw.mimetype)
        body = raw.get_data()
        want = (D.ROOT / r["rel"]).read_bytes()
        assert hashlib.sha256(body).hexdigest() == hashlib.sha256(want).hexdigest(), f"{r['slug']}: 원문 경로가 원본을 바꿔 낸다"
        assert b"docnote" not in body and b"dn-body-css" not in body
        assert hashlib.sha256(want).hexdigest()[:16] in h, "화면의 sha256 이 원본과 다르다"


def test_views_mount_the_existing_docnote_on_the_report_rel():
    """양성: 보기 화면이 **기존** 여백 메모 · 형광펜 (docnote.js) 을 rel = 보고서 파일 경로에 단다 (새 창고 · 새 라이브러리 없음)."""
    c = _client()
    for r in D.COLLAB_REPORTS:
        h = c.get(f"/reports/{r['slug']}").get_data(as_text=True)
        assert "/static/js/docnote.js?v=" in h and 'id="pnotebadge"' in h, r["slug"]
        assert 'id="docpen"' in h and "docnotePenToggle()" in h, r["slug"]
        assert 'class="dn-host" id="creport-host"' in h, r["slug"]
        assert f"var REL = {json.dumps(r['rel'])};" in h and "mountDocNotes(body, REL, host)" in h, r["slug"]
        assert f"var RAW = {json.dumps('/reports/' + r['slug'] + '/raw')};" in h, r["slug"]
        assert "host.addEventListener('dnote:toggle', fit)" in h
        assert "marked" not in h.lower() and "annotator" not in h.lower()


def test_no_company_name_anywhere():
    """⛔음성: 목록 · 보기 화면 · 원문 (그림 데이터 뺀 글) · 사이드바 항목에 기업 이름이 없다 (CLAUDE.md — 회의록 바탕 외부 과제 문서 규칙)."""
    c = _client()
    pages = {"목록": c.get("/reports").get_data(as_text=True)}
    for r in D.COLLAB_REPORTS:
        pages[f"보기 {r['slug']}"] = c.get(f"/reports/{r['slug']}").get_data(as_text=True)
        pages[f"원문 {r['slug']}"] = _text(c.get(f"/reports/{r['slug']}/raw").get_data(as_text=True))
        for e in r.get("earlier", ()):
            pages[f"앞 판 {e['rel']}"] = _text((D.ROOT / e["rel"]).read_text(encoding="utf-8"))
    for it in (it for sec in N.SECTIONS for it in sec["items"] if it["url"].startswith("/reports")):
        pages[f"사이드바 {it['url']}"] = " ".join(str(it.get(k, "")) for k in ("label", "sub", "kw"))
    assert sum(k.startswith("사이드바") for k in pages) == 1, "전제: 사이드바의 보고서 줄은 공유 보고서 하나뿐이다"
    for name, t in pages.items():
        assert not _company_hits(t), f"기업 이름이 들어갔다 ({name}): {_company_hits(t)}"


def test_company_check_is_not_blind(monkeypatch):
    """⛔음성 (시험의 시험): 표 제목에 기업 이름을 넣으면 목록 화면에서 위 검사가 실제로 잡는다 — 헛것을 재지 않는다."""
    r = D.COLLAB_BY_SLUG["agc-crack"]
    monkeypatch.setitem(D.COLLAB_BY_SLUG, "agc-crack", {**r, "title": r["title"] + " (SDI)"})
    h = _client().get("/reports").get_data(as_text=True)
    assert _company_hits(h) == ["SDI"]


def test_missing_report_says_so_not_blank(monkeypatch):
    """⛔음성: 파일이 없으면 보기 화면은 '못 읽었다' 를 말하고 iframe · 메모 장치를 안 단다 · 원문 경로는 404 ·
    목록은 그 줄을 빼지 않고 '파일 없음' 을 적는다."""
    r = D.COLLAB_BY_SLUG["wad-dem"]
    monkeypatch.setitem(D.COLLAB_BY_SLUG, "wad-dem", {**r, "rel": "docs/collab/__no_such_report__.html"})
    c = _client()
    h = c.get("/reports/wad-dem").get_data(as_text=True)
    assert "보고서 파일을 못 읽었다" in h and "<iframe" not in h
    assert "mountDocNotes(" not in h and 'id="docpen"' not in h, "없는 보고서에 메모 장치를 달았다"
    assert c.get("/reports/wad-dem/raw").status_code == 404
    lst = c.get("/reports").get_data(as_text=True)
    row = re.search(r'<tr id="row-wad-dem">(.*?)</tr>', lst, re.S).group(1)
    assert "파일 없음" in row and 'href="/reports/wad-dem"' not in row
    # 다른 보고서는 그대로 열린다 (한 줄 사고가 목록을 비우지 않는다)
    assert c.get("/reports/lzo").status_code == 200 and "<iframe" in c.get("/reports/lzo").get_data(as_text=True)


def test_routes_are_in_the_surface_scan():
    """⛔음성: 보기 · 원문 경로가 **인자 없는 GET** 이라 결속 검사 (test_v3_surfaces._domain) 의 자동 열거에 실제로 든다.
    `/reports/<slug>` 하나로 묶으면 여기서 빨간불이다 — 새 표면이 음성시험을 피해 가는 길을 막는다."""
    spec = importlib.util.spec_from_file_location("tv3", Path(__file__).with_name("test_v3_surfaces.py"))
    tv3 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tv3)
    dom = {u for u, _ in tv3._domain()}
    assert "/reports" in dom
    for r in D.COLLAB_REPORTS:
        assert f"/reports/{r['slug']}" in dom and f"/reports/{r['slug']}/raw" in dom, r["slug"]
    assert not any("<" in str(rule) for rule in A.app.url_map.iter_rules() if str(rule).startswith("/reports"))


def test_report_memos_lead_back_to_each_view(tmp_path, monkeypatch):
    """양성: 표의 보고서에 단 메모는 /notes 딥링크가 그 보기 화면으로 데려간다 (?note=<id>).
    ⛔음성: 앞 판 (보기 화면 없음) 에 단 메모는 그대로 '파일' (/files) — 딥링크 표를 표 밖으로 넓히지 않았다."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    monkeypatch.setattr(D, "HIGHLIGHTS_PATH", tmp_path / "file_highlights.json")
    monkeypatch.setattr(A, "READ_ONLY", False)
    for r in D.COLLAB_REPORTS:
        o = D.comment_origin(r["rel"])
        assert (o["kind"], o["url"]) == ("보고", f"/reports/{r['slug']}"), (r["slug"], o)
    r = D.COLLAB_BY_SLUG["wad-dem"]
    anchor = "종결 둘은 합치지 않았다."                 # 여백 메모 자리 (글 지문) — 딥링크 ?note= 는 자리가 있는 메모에만 붙는다
    assert (D.ROOT / r["rel"]).read_text(encoding="utf-8").count(anchor) == 1, "전제: 메모 자리 글이 보고서에 한 번 있다"
    nid = D.add_file_comment(r["rel"], "공유 보고 메모 — 2-3 절 다시 읽기", anchor=anchor)["item"]["id"]
    row = next(x for x in D.comment_all() if x["id"] == nid)
    assert D.note_url(row) == f"/reports/wad-dem?note={nid}"
    for r in D.COLLAB_REPORTS:
        for e in r.get("earlier", ()):
            o = D.comment_origin(e["rel"])
            assert o["kind"] == "파일" and o["url"].startswith("/files?q="), (e["rel"], o)


def _camp():
    return next(sec for sec in N.SECTIONS if sec["id"] == "nav-camp")


def _sidebar_html(h):
    return h[h.index('<nav'):h.index('</nav>')] if '<nav' in h else h


def test_nav_has_the_reports_item():
    """양성: 사이드바 캠페인 묶음의 **첫 줄 (늘 보이는 줄)** 이 공유 보고서이고, 목록 화면이 active 로 그 줄을 켠다.
    보기 화면 (/reports/<slug>) 에서도 같은 줄이 켜진다 (also) — 그 화면들은 사이드바 줄이 따로 없다."""
    camp = _camp()
    assert camp["fold_after"] == 1 and camp["fold_label"] == "캠페인 페이지", camp.get("fold_after")
    hub = camp["items"][0]
    assert (hub["url"], hub["active"], hub["label"]) == ("/reports", "reports", "공유 보고서"), hub
    c = _client()
    assert re.search(r'href="/reports" aria-current="page"', c.get("/reports").get_data(as_text=True))
    for r in D.COLLAB_REPORTS:
        assert f"report-{r['slug']}" in hub["also"], r["slug"]
        h = c.get(f"/reports/{r['slug']}").get_data(as_text=True)
        assert re.search(r'href="/reports" aria-current="page"', h), f"{r['slug']}: 보기 화면에서 공유 보고서 줄이 안 켜진다"


def test_sidebar_shows_only_the_hub_and_folds_the_campaigns():
    """양성+⛔음성 (사용자 2026-11-24 '공유보고서만 index 에 넣고 · 아님 토글로 피거나 접거나'):
    캠페인 페이지는 토글 (details) 안에만 있다 · 늘 보이는 줄은 공유 보고서 하나 · 보고서 보기 화면 줄은 사이드바에 없다 ·
    토글은 기본으로 닫혀 있고, 지금 페이지가 그 안에 있으면 (예: /sdcp) 서버가 펴서 보낸다."""
    camp = _camp()
    rest = camp["items"][camp["fold_after"]:]
    assert rest and all(not it["url"].startswith("/reports") for it in rest)
    assert not any(it["url"].startswith("/reports/") for sec in N.SECTIONS for it in sec["items"]), "보고서 줄이 사이드바에 남았다"
    c = _client()
    h = _sidebar_html(c.get("/reports").get_data(as_text=True))
    m = re.search(r'<details class="v3-fold nav-fold nav-subfold" data-fold="nav-camp-more"( open)?>(.*?)</details>', h, re.S)
    assert m, "캠페인 접힘 토글이 없다"
    assert not m.group(1), "공유 보고서 화면에서 토글이 펴져 있다 (기본은 접힘)"
    inside = m.group(2)
    assert f"캠페인 페이지 {sum(1 for it in rest if not it.get('nsub'))}" in inside
    for it in rest:
        assert f'href="{it["url"]}"' in inside, f"{it['url']} 이 토글 안에 없다"
    head = h[h.index('id="nav-camp"'):m.start()]
    assert head.count("<li") == 1 and 'href="/reports"' in head, "늘 보이는 줄이 공유 보고서 하나가 아니다"
    hs = _sidebar_html(c.get("/sdcp").get_data(as_text=True))
    assert re.search(r'data-fold="nav-camp-more" open>', hs), "캠페인 페이지에 있을 때 토글이 안 펴진다"


def test_reports_page_lists_every_campaign_with_its_reports():
    """양성+⛔음성: 공유 보고서 화면의 캠페인 표가 사이드바 토글 안의 캠페인을 **전부** (배지와 함께) 싣고,
    공유 보고서마다 그 캠페인 (nav_parent) 줄에 링크가 달린다. 캠페인을 빼먹거나 다른 줄에 달면 여기서 빨간불."""
    camp = _camp()
    rest = camp["items"][camp["fold_after"]:]
    h = _client().get("/reports").get_data(as_text=True)
    tbl = re.search(r'<table class="tbl" id="camp-list"[^>]*>.*?<tbody>(.*?)</tbody>', h, re.S).group(1)
    rows = re.findall(r"<tr>(.*?)</tr>", tbl, re.S)
    assert len(rows) == len(rest), (len(rows), len(rest))
    by_url = {}
    for it, row in zip(rest, rows):
        assert f'href="{it["url"]}"' in row, f"{it['url']}: 표 순서 · 줄이 사이드바와 다르다"
        by_url[it["url"]] = row
    side = {it["url"]: it for sec in N.sidebar() for it in sec["links"]}
    for u, row in by_url.items():
        if side[u].get("badge"):
            assert side[u]["badge"] in row, f"{u}: 배지 (원장에서 센 수) 가 표에 없다"
    for r in D.COLLAB_REPORTS:
        assert f'href="/reports/{r["slug"]}"' in by_url[r["nav_parent"]], f"{r['slug']}: {r['nav_parent']} 줄에 없다"
        others = [u for u in by_url if u != r["nav_parent"]]
        assert not any(f'href="/reports/{r["slug"]}"' in by_url[u] for u in others), f"{r['slug']}: 다른 캠페인 줄에도 달렸다"
