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
import data as _D           # noqa: E402


def D_rows():
    return _D.requests_ledger()


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


def test_requests_conflict_detection_works():
    """[음성] 이모지와 문장이 어긋나는 행을 **탐지**해야 한다.

    ⚠ 2026-08-25 반성 — 첫 판은 *실제 문서에 불일치가 있다* 고 단언했다(요청 5).
      그 불일치를 고치자 테스트가 깨졌다. **결함의 존재를 단언하면 결함을 고칠 수 없다.**
      → 합성 입력으로 **탐지 로직**을 검사한다. 문서 상태와 무관하게 유효하다.
    """
    import data as D
    md = ("| 요청 | 내용 | 상태 | 이 문서 |\n"
          "|---|---|---|---|\n"
          "| **1** | 되는 것 | ✅ 완료 | §1 |\n"
          "| **2** | 어긋난 것 | 🔴 **재작성 완료** | §2 |\n"
          "| **3** | 막힌 것 | 🔴 아직 | §3 |\n")
    orig = D.load_requests_md
    D.load_requests_md = lambda: md
    try:
        rows = {r["n"]: r for r in D.requests_ledger()}
    finally:
        D.load_requests_md = orig
    assert len(rows) == 3, f"합성 표 파싱 실패: {rows}"
    assert rows["2"]["conflict"] is True, "🔴 + '완료' 불일치를 못 잡았다"
    assert rows["1"]["conflict"] is False, "정상 행을 불일치로 잡았다"
    assert rows["3"]["conflict"] is False, "정상 행을 불일치로 잡았다"
    # 불일치를 만나도 **원문 상태 문자열은 그대로** 남아야 한다 (한쪽으로 정하지 않는다)
    assert "재작성 완료" in rows["2"]["status"]


def test_real_ledger_has_no_unresolved_conflict():
    """실제 문서에 불일치가 남아 있으면 알린다 — 실패가 아니라 **경고**다.
    (원문을 고쳐야 사라지는 것이고, 테스트가 문서 수정을 막으면 안 된다)"""
    import data as D
    conf = [r for r in D.requests_ledger() if r.get("conflict")]
    if conf:
        import warnings
        warnings.warn(f"요청 대장에 표시 불일치 {len(conf)}건: "
                      f"{[r['n'] for r in conf]} — 원문을 고칠 것")


def test_requests_page_renders(client):
    r = client.get("/requests")
    assert r.status_code == 200
    body = r.data.decode()
    # ⚠ 배지 문구("표시 불일치")로 단언하면 불일치가 0건일 때 깨진다 — 상태 요약의
    #   **구조**로 건다.
    assert "요청 대장" in body
    for r in D_rows():
        assert r["what"][:12] in body, f"요청 {r['n']} 이 화면에 없다"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
