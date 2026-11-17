"""계면 부반응 통합 보고 화면 (/interface-thermo · 2026-11-17) — 렌더 · 기업 이름 · 없는 파일 · 배지.

사용자 2026-11-17: 'SDI, 혁주 html을 통합해서 같이 한 페이지' → 'docs/collab' 에만 있고 웹앱 캠페인 목록에 없었다 ('아직 추가 안됐는데?').

⛔ 이 파일이 못 하는 것: 보고서 문장 · 값이 원장과 맞는지는 안 본다 (근거는 카드 · 결정 원장 · 값 결속은 test_v3_surfaces 의
  정의역 자동 열거가 /interface-thermo/report 를 그대로 훑는다). iframe 높이 맞춤 (JS) 은 브라우저 없이는 못 본다.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app as A      # noqa: E402
import nav as N      # noqa: E402

_COMPANY = ("SDI", "삼성", "Samsung", "samsung")


def _client():
    A.app.config["TESTING"] = True
    return A.app.test_client()


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
    """⛔음성: 보고서 파일이 없으면 화면은 '못 읽었다' 를 말하고 iframe 을 안 그린다 · 보고서 라우트는 404."""
    monkeypatch.setattr(A, "INTERFACE_THERMO_REL", "docs/collab/__no_such_report__.html")
    c = _client()
    h = c.get("/interface-thermo").get_data(as_text=True)
    assert "보고서 파일을 못 읽었다" in h and "<iframe" not in h
    assert c.get("/interface-thermo/report").status_code == 404


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
