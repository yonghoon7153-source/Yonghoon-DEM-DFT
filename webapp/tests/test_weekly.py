#!/usr/bin/env python3
"""test_weekly.py — 주간 정리 화면(/weekly)의 회귀 + **표면별 음성시험**.

    pytest webapp/tests/test_weekly.py -q

왜 따로인가: `/weekly` 는 인자 없는 GET 이라 `test_webapp._html_routes()` 의 결속 스캔에는
자동으로 들지만, 실제 주간 문서에는 결속 대상 문자열(철회값)이 없어서 그 초록은
"안 마주쳐서" 다. 여기서 **합성 문서에 철회값을 심어** 이 화면이 결속을 붙이는지,
선언을 지우면 미결속으로 떨어지는지 직접 본다 (회신 BG 가 요구한 표면별 음성시험).

⛔ 이 파일이 못 하는 것: 주간 문서의 **내용**이 맞는지 판정하지 않는다. 화면이 문서를
  읽어 그리는지, 작업 기록과 양방향으로 이어졌는지, 그림·링크가 살아 있는지만 본다.
"""
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

import app as A                # noqa: E402
import canonical as C          # noqa: E402
from app import app            # noqa: E402


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_weekly_renders_latest_doc(client):
    r = client.get("/weekly")
    assert r.status_code == 200
    body = r.data.decode()
    assert "주간 정리" in body
    assert "kb/reports/weekly_" in body, "부제가 원본 파일을 대지 않는다"
    assert 'href="/log"' in body, "부모(작업 기록)로 가는 길이 없다"


def test_weekly_is_a_child_of_worklog(client):
    """작업 기록 ↔ 주간 정리는 **양방향**이어야 한다 (test_requests 와 같은 규칙)."""
    log = client.get("/log").data.decode()
    # ⛔ 사이드바에도 /weekly 가 있어서 `in log` 로는 못 잰다 — 2026-09-14 에 링크를 일부러
    #   지웠는데 초록이었다. **본문의 '하위 페이지' 카드 안**에서 찾는다.
    card = log.split("하위 페이지", 1)[1][:2500] if "하위 페이지" in log else ""
    assert 'href="/weekly"' in card, "Work Log 본문(하위 페이지 카드)에서 주간 정리로 가는 길이 없다"
    body = client.get("/weekly").data.decode()
    assert re.search(r'href="/log"[^>]*class="active"', body), \
        "하위 페이지인데 사이드바의 Work Log 가 활성이 아니다"
    assert re.search(r'href="/weekly"[^>]*class="active"', body), "자기 항목이 활성이 아니다"


def test_weekly_specific_week_and_404s(client):
    docs = A._weekly_docs()
    assert docs, "주간 문서가 하나도 없다 (kb/reports/weekly_*.md)"
    assert client.get(f"/weekly?w={docs[0]['key']}").status_code == 200
    # ⛔음성: 없는 주 · 규약 밖 인자 · 경로 탈출 시도는 전부 404 (빈 화면·500 이 아니라)
    assert client.get("/weekly?w=1999_01_01").status_code == 404
    assert client.get("/weekly?w=../../CLAUDE").status_code == 404
    assert client.get("/weekly?w=weekly_2026_09_14.md").status_code == 404


def test_weekly_says_none_when_no_docs(client, tmp_path, monkeypatch):
    """문서가 0건이면 **없다고 말한다** — 빈 화면은 '일이 없었다' 로 읽힌다."""
    monkeypatch.setattr(A, "WEEKLY_DIR", tmp_path)
    r = client.get("/weekly")
    assert r.status_code == 200
    assert "주간 정리 문서가 없다" in r.data.decode()


def test_weekly_binds_retracted_claims_from_the_document(client, tmp_path, monkeypatch):
    """⛔음성 **표면별**: 철회값이 문서에 있으면 화면이 결속을 붙이고, 선언을 지우면 미결속으로 떨어진다."""
    tgt = next(x for x in C.all_claims() if x["state"] == "retracted" and x["text"])
    (tmp_path / "weekly_2099_01_01.md").write_text(
        f"---\ntitle: 시험 주간\n---\n\n# 시험\n\n옛 값 {tgt['text']} eV 를 인용한 문장.\n",
        encoding="utf-8")
    monkeypatch.setattr(A, "WEEKLY_DIR", tmp_path)
    html = client.get("/weekly").data.decode()
    assert f'data-claim="{tgt["id"]}"' in html, "화면이 문서의 철회값에 결속을 안 붙였다"
    assert "claim-mark" in html, "표식이 텍스트 노드로 안 나갔다"
    sc = C.scan_claim_bindings(html, C.all_claims())
    assert sc["bound"] and not sc["unbound"], sc
    naked = re.sub(r'\sdata-claim="[^"]*"', "", html)
    assert C.scan_claim_bindings(naked, C.all_claims())["unbound"], \
        "선언을 지웠는데도 미결속이 아니다 — 스캐너가 이 화면을 안 본다"


def test_weekly_figures_and_links_resolve(client):
    """주간 문서가 거는 그림·내부 링크가 살아 있어야 한다 (죽은 그림은 '안 만든 그림' 으로 읽힌다)."""
    html = client.get("/weekly").data.decode()
    body = html.split('id="docbody"', 1)[1]
    srcs = re.findall(r'<img[^>]+src="([^"]+)"', body)
    assert srcs, "주간 문서에 그림이 하나도 없다"
    for s in srcs:
        assert client.get(s).status_code == 200, f"그림 경로가 죽었다: {s}"
    hrefs = {h for h in re.findall(r'href="(/[^"#]*)"', body) if not h.startswith("/api/")}
    assert hrefs, "본문에 내부 링크가 없다"
    dead = [(h, client.get(h).status_code) for h in sorted(hrefs)
            if client.get(h).status_code not in (200, 403)]
    assert not dead, f"본문 링크가 죽었다: {dead}"
