#!/usr/bin/env python3
"""test_requests.py — 1저자 요청 대장 화면(/requests)의 회귀.

이 문서는 캠페인에서 가장 자주 되돌아오는 원장이라, **표가 조용히 안 읽히는 것**이
제일 위험하다(형식이 바뀌면 빈 리스트가 되고 화면은 멀쩡해 보인다).

    pytest webapp/tests/test_requests.py -q

⛔ 이 파일이 못 하는 것: 상태의 옳고 그름을 판정하지 않는다. 표를 옮기는지만 본다.
"""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "webapp"))

from app import app          # noqa: E402


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── 1저자 요청 대장 (/requests) ─────────────────────────────────────────
def test_requests_ledger_parses():
    """표가 실제로 파싱돼야 한다. 형식이 바뀌면 조용히 빈 리스트가 되므로 여기서 막는다."""
    import data as D
    rows = D.requests_ledger()
    assert len(rows) >= 8, f"요청 대장 파싱 실패 ({len(rows)}행)"
    assert all(r["n"] and r["what"] for r in rows)
    assert {r["mark"] for r in rows} <= {"done", "blocked", "partial", "open"}


def test_requests_conflict_is_flagged_not_resolved():
    """[음성] 이모지와 문장이 어긋나는 행(요청 5: 🔴 + '재작성 완료')을
    화면이 한쪽으로 **정하면 안 된다** — 어긋났다고 표시만 한다."""
    import data as D
    rows = D.requests_ledger()
    conf = [r for r in rows if r.get("conflict")]
    assert conf, "원문에 있는 표시 불일치를 못 잡았다"
    for r in conf:
        assert r["status"], "불일치 행의 원문 상태 문자열이 사라졌다"


def test_requests_page_renders(client):
    r = client.get("/requests")
    assert r.status_code == 200
    body = r.data.decode()
    assert "요청 대장" in body and "표시 불일치" in body


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
