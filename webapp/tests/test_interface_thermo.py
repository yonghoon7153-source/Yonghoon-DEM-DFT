"""계면 부반응 통합 보고 화면 (/interface-thermo · 2026-11-17) — 렌더 · 기업 이름 · 없는 파일 · 배지 · 여백 메모 · 형광펜.

사용자 2026-11-17: 'SDI, 혁주 html을 통합해서 같이 한 페이지' → 'docs/collab' 에만 있고 웹앱 캠페인 목록에 없었다 ('아직 추가 안됐는데?').
같은 날 '여기서도 메모랑 하이라이트 넣을 수 있게 만들어줘' → '기존 포멧 가져와' — 논문 페이지의 docnote.js 를 그대로 단다.

⛔ 이 파일이 못 하는 것: 보고서 문장 · 값이 원장과 맞는지는 안 본다 (근거는 카드 · 결정 원장 · 값 결속은 test_v3_surfaces 의
  정의역 자동 열거가 /interface-thermo/report 를 그대로 훑는다). iframe 높이 맞춤 · iframe 안 메모 자리 · 칠하기 (JS) 는
  브라우저 없이는 못 본다 — 그건 docnote_paint.test.mjs 의 'iframe' 절이 본다 (test_webapp 이 돌린다).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as A      # noqa: E402
import data as D     # noqa: E402
import nav as N      # noqa: E402

_COMPANY = ("SDI", "삼성", "Samsung", "samsung")

#: 보고서 본문에 **그대로 있는** 글 — 메모 자리 · 형광펜 지문 (docnote 가 글로 다시 찾는다). 아래 시험이 실제로 있는지부터 본다.
_ANCHOR = "LPSCl 은 Li 금속과 닿으면 분해된다."
_PEN = "Ag₂S 는 1.91 V 보다 높은 전위에서만 안정하다."


def _client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


def _stores(tmp_path, monkeypatch):
    """메모 · 형광펜 창고를 임시 파일로 — 진짜 db/file_comments.json · file_highlights.json 에 시험 메모를 안 쓴다."""
    monkeypatch.setattr(D, "COMMENTS_PATH", tmp_path / "file_comments.json")
    monkeypatch.setattr(D, "HIGHLIGHTS_PATH", tmp_path / "file_highlights.json")
    monkeypatch.setattr(A, "READ_ONLY", False)       # 쓰기 잠금 (Render) 과 무관하게 시험한다


def _text(html):
    return re.sub(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+", "", html)


def test_page_frames_the_report_and_report_is_html():
    """양성: 화면은 보고서 라우트를 iframe 으로 띄우고, 보고서 라우트는 HTML 이다 (그래야 표면 결속 검사가 훑는다)."""
    c = _client()
    r = c.get("/interface-thermo")
    assert r.status_code == 200
    h = r.get_data(as_text=True)
    assert 'src="/interface-thermo/report"' in h and "<iframe" in h
    assert f'href="/api/file/{A.INTERFACE_THERMO_REL}?dl=1"' in h, "내려받기 링크가 없다"
    rr = c.get("/interface-thermo/report")
    assert rr.status_code == 200 and rr.mimetype == "text/html", (rr.status_code, rr.mimetype)
    body = rr.get_data(as_text=True)
    assert "<title>계면 부반응 열역학 계산</title>" in body
    assert 'id="case-a"' in body and 'id="case-b"' in body and 'id="zero-v"' in body, "사례 A · B · 0 V 상자가 다 있어야 한다"
    assert body.count("data:image/") == 5, "그림 5 장이 안 실렸다"


def test_no_company_name_anywhere():
    """⛔음성: 보고서 · 화면 · 사이드바 항목에 기업 이름이 없다 (CLAUDE.md — 회의록 바탕 외부 과제 문서 규칙)."""
    c = _client()
    pages = [_text(c.get("/interface-thermo/report").get_data(as_text=True)),
             c.get("/interface-thermo").get_data(as_text=True)]
    item = next(it for sec in N.SECTIONS for it in sec["items"] if it["url"] == "/interface-thermo")
    pages.append(" ".join(str(item.get(k, "")) for k in ("label", "sub", "kw")))
    for i, t in enumerate(pages):
        hit = [w for w in _COMPANY if w in t]
        assert not hit, f"기업 이름이 들어갔다 ({['보고서', '화면', '사이드바'][i]}): {hit}"


def test_missing_report_says_so_not_blank(monkeypatch):
    """⛔음성: 보고서 파일이 없으면 화면은 '못 읽었다' 를 말하고 iframe 을 안 그린다 · 보고서 라우트는 404.

    메모 장치도 안 단다 — 없는 파일에 메모를 다는 척하면 안 된다 (서버도 거절하지만 화면이 먼저 안 연다).
    """
    monkeypatch.setattr(A, "INTERFACE_THERMO_REL", "docs/collab/__no_such_report__.html")
    c = _client()
    h = c.get("/interface-thermo").get_data(as_text=True)
    assert "보고서 파일을 못 읽었다" in h and "<iframe" not in h
    assert "mountDocNotes(" not in h and 'id="docpen"' not in h, "없는 보고서에 메모 장치를 달았다"
    assert c.get("/interface-thermo/report").status_code == 404


# ── 여백 메모 · 형광펜 (2026-11-17 · 사용자 '여기서도 메모랑 하이라이트' → '기존 포멧 가져와') ─────────────
def test_page_mounts_the_existing_docnote_on_the_report():
    """양성: 화면이 **기존** 여백 메모 · 형광펜 (docnote.js) 을 보고서 본문에 단다 — 같은 #pnotebadge · #docpen · .dn-host,
    rel = 보고서 파일 경로 (새 창고 · 새 주석 라이브러리 없음)."""
    h = _client().get("/interface-thermo").get_data(as_text=True)
    assert "/static/js/docnote.js?v=" in h, "docnote.js 를 안 싣는다"
    assert 'id="pnotebadge"' in h, "메모 개수 · 다는 법 (paintBadge 자리) 이 없다"
    assert 'id="docpen"' in h and "docnotePenToggle()" in h, "형광펜 켜고 끄기가 없다"
    assert 'class="dn-host" id="ithermo-host"' in h, "여백 host 격자가 논문 페이지와 다르다"
    assert f"var REL = {json.dumps(A.INTERFACE_THERMO_REL)};" in h, "메모를 보고서 파일 rel 에 달지 않는다"
    assert "mountDocNotes(body, REL, host)" in h
    # 여백이 열리는 순간 iframe 높이를 맞춘다 — 늦으면 ?note= 딥링크가 자리를 놓친다 (1440px 실측 · 순서는 docnote_paint.test.mjs 가 본다)
    assert "host.addEventListener('dnote:toggle', fit)" in h
    # ⛔ 브라우저 마크다운 파서 · 다른 주석 도구를 끌어오지 않았다
    assert "marked" not in h.lower() and "annotator" not in h.lower()


def test_report_route_still_serves_the_sent_file_byte_for_byte():
    """⛔음성: 메모 장치는 **화면 쪽에만** 있다 — 보고서 라우트는 보낸 파일 그대로 낸다 (sha256 동일 · docnote 흔적 없음).
    그래서 화면의 sha256 · 새 탭 보기 · 내려받기가 다 같은 원본을 가리킨다."""
    body = _client().get("/interface-thermo/report").get_data()
    raw = (D.ROOT / A.INTERFACE_THERMO_REL).read_bytes()
    assert hashlib.sha256(body).hexdigest() == hashlib.sha256(raw).hexdigest(), "보고서 라우트가 원본을 바꿔 낸다"
    assert b"docnote" not in body and b"dn-body-css" not in body


def test_memo_and_highlight_roundtrip_on_the_report(tmp_path, monkeypatch):
    """양성: 보고서 rel 에 여백 메모 (anchor) · 형광펜을 달면 저장되고 다시 읽힌다 — 새로고침 뒤 화면이 다시 그리는 길이다.
    고치기 (옛 글 history) · 지우기도 같은 API 다."""
    _stores(tmp_path, monkeypatch)
    rel = A.INTERFACE_THERMO_REL
    text = (D.ROOT / rel).read_text(encoding="utf-8")
    assert text.count(_ANCHOR) == 1 and text.count(_PEN) == 1, "전제: 메모 자리 · 형광펜 글이 보고서에 한 번씩 있다"
    c = _client()
    r = c.post("/api/comments/" + rel, json={"text": "사례 A 의 **핵심** 문장", "anchor": _ANCHOR})
    assert r.status_code == 200, r.get_json()
    nid = r.get_json()["item"]["id"]
    items = c.get("/api/comments/" + rel).get_json()["items"]
    assert [i["id"] for i in items] == [nid]
    assert items[0]["anchor"] == _ANCHOR, "붙인 자리 (글 지문) 가 그대로 돌아와야 다시 찾는다"
    assert "<strong>핵심</strong>" in items[0]["html"], "표시용 html (서버 렌더 · 결속) 이 같이 와야 한다"
    p = c.patch("/api/comments/" + rel, json={"id": nid, "text": "고쳐 쓴 메모"})
    assert p.status_code == 200 and p.get_json()["item"]["history"][0]["text"] == "사례 A 의 **핵심** 문장"
    h = c.post("/api/highlights/" + rel, json={"text": _PEN, "color": "green"})
    assert h.status_code == 200, h.get_json()
    hid = h.get_json()["item"]["id"]
    pens = c.get("/api/highlights/" + rel).get_json()["items"]
    assert [(x["id"], x["text"], x["color"]) for x in pens] == [(hid, _PEN, "green")]
    # 창고는 임시 파일이다 — 진짜 창고 (db/) 에는 안 썼다
    assert rel in json.loads((tmp_path / "file_comments.json").read_text(encoding="utf-8"))
    assert rel in json.loads((tmp_path / "file_highlights.json").read_text(encoding="utf-8"))
    assert c.delete("/api/highlights/" + rel, json={"id": hid}).status_code == 200
    assert c.delete(f"/api/comments/{rel}?id={nid}").status_code == 200
    assert c.get("/api/comments/" + rel).get_json()["items"] == []
    assert c.get("/api/highlights/" + rel).get_json()["items"] == []


def test_memo_gate_was_not_widened_for_this_page(tmp_path, monkeypatch):
    """⛔음성: 이 화면을 붙이며 메모 게이트 (safe_note_target) 를 넓히지 않았다 — 게이트 밖 파일은 메모 · 형광펜 둘 다 여전히 거절,
    거절하면 창고에 유령 키도 안 생긴다. (보고서는 원래 게이트 안이다: docs/ = 기존 파일 코멘트 대상.)"""
    _stores(tmp_path, monkeypatch)
    assert D.safe_note_target(A.INTERFACE_THERMO_REL) is not None, "전제: 보고서는 기존 게이트로 이미 된다"
    bad = ("kb/projects/hyeokju_lzo_interface_2026_11_16.md",     # 있는 파일 · 메모 대상 폴더 밖
           "webapp/templates/interface_thermo.html",              # 이 화면의 틀 — 대상이 아니다
           "docs/collab/__no_such_report__.html",                 # 없는 파일 (유령 키)
           "docs/collab/../../webapp/app.py")                     # 경로 탈출
    assert (D.ROOT / bad[0]).is_file() and (D.ROOT / bad[1]).is_file(), "전제: 앞의 둘은 실제로 있는 파일이다"
    c = _client()
    for rel in bad:
        r = c.post("/api/comments/" + rel, json={"text": "x", "anchor": "y"})
        assert r.status_code == 400, (rel, r.status_code, r.get_json())
        h = c.post("/api/highlights/" + rel, json={"text": "xyz"})
        assert h.status_code == 400, (rel, h.status_code, h.get_json())
    assert not (tmp_path / "file_comments.json").exists() or D._load_comments() == {}
    assert not (tmp_path / "file_highlights.json").exists() or D._load_comments(D.HIGHLIGHTS_PATH) == {}


def test_report_memos_lead_back_to_this_page(tmp_path, monkeypatch):
    """양성: 이 보고서의 메모는 /notes 카드 · ⌘K 검색에서 **이 화면**으로 데려간다 (/notes 는 ?note=<id> 로 그 메모까지 —
    docnote focusFromUrl 이 읽는다). ⛔음성: 다른 docs 파일 코멘트는 그대로 '파일' (/files) — 딥링크 표를 넓히지 않았다."""
    _stores(tmp_path, monkeypatch)
    rel = A.INTERFACE_THERMO_REL
    assert rel == D.INTERFACE_THERMO_REL, "화면 경로와 딥링크 표가 같은 값을 봐야 한다 (두 벌 금지)"
    nid = D.add_file_comment(rel, "보고 메모 — 0 V 상자 다시 읽기", anchor=_ANCHOR)["item"]["id"]
    o = D.comment_origin(rel)
    assert (o["kind"], o["url"]) == ("보고", "/interface-thermo"), o
    row = next(x for x in D.comment_all() if x["id"] == nid)
    assert D.note_url(row) == f"/interface-thermo?note={nid}"
    h = _client().get("/notes").get_data(as_text=True)
    assert f'href="/interface-thermo?note={nid}"' in h, "/notes 카드가 이 화면의 그 메모로 안 간다"
    hit = [i for i in D.search_index() if i["t"] == "메모" and i["label"].startswith("보고 메모")]
    assert hit and hit[0]["url"] == "/interface-thermo", hit
    # 2026-11-24 — 사례 A 단독 보고 (agc_…_11_16) 는 이제 공유 보고서 표 (data.COLLAB_REPORTS) 에 들어 '보고' 로 간다.
    #   딥링크 표 **밖의** docs/collab 파일로 같은 음성 확인을 한다 (앞 판 · 보기 화면 없음).
    other = "docs/collab/lzo_coated_nca_lpscl_progress_2026_11_17.html"
    assert (D.ROOT / other).is_file(), "전제: 다른 docs/collab 파일이 있다"
    assert other not in {r["rel"] for r in D.COLLAB_REPORTS}, "전제: 이 파일은 딥링크 표 밖이다"
    assert D.comment_origin(other)["kind"] == "파일" and D.comment_origin(other)["url"].startswith("/files?q=")


def test_nav_badge_sums_both_tracks():
    """양성+⛔음성: 사이드바 배지 = 두 트랙 (ag2s · hyeokju) 살아 있는 결정의 합 — 손으로 쓴 수가 아니다.

    'agc' 로 세면 점착 트랙의 Ag–흑연 (W_ad) 결정까지 섞인다 — 그 수와 같으면 슬러그가 잘못된 것이다.
    """
    want = sum(N.campaign_status(s)["decisions"] for s in ("ag2s", "hyeokju"))
    assert want > 0, "전제: 두 트랙에 살아 있는 결정이 있다"
    row = next(it for sec in N.sidebar() for it in sec["links"] if it["url"] == "/interface-thermo")
    assert row["badge"] and f"결정 {want}" in row["badge"], row["badge"]
    wrong = N.campaign_status("agc")["decisions"] + N.campaign_status("hyeokju")["decisions"]
    assert wrong != want, "전제: 'agc' 는 다른 트랙까지 센다 (같으면 이 음성 확인이 헛것을 잰다)"
