"""패치노트 — 무엇이 바뀌었나를 화면이 읽는 길.

`docs/log.md` 를 그대로 낸다.  두 번째 목록을 만들면 반드시 한쪽만 갱신되고,
그때 사람이 보는 쪽이 틀린 쪽이 된다.

여기서 틀릴 수 있는 방식이 셋이다: 순서가 뒤집혀 옛것이 위에 오거나, 본문이
옆 항목에 붙거나, 목록에 없는 action 이 통째로 빠지거나.  셋 다 오류를 내지
않고 그냥 잘못된 화면이 된다.
"""

from __future__ import annotations

from pathlib import Path

from app.changelog import parse_log, read_notes

SAMPLE = """# 작업 로그

append-only. 형식: `## [YYYY-MM-DD] action | subject`

## [2026-08-20] create | 저장소 초기화
첫 항목의 본문.

## [2026-08-22] fix | 포트 주인을 밝힌다

두 문단짜리 본문.

### 소제목

소제목이 있어도 한 항목이다.

## [2026-08-24] feat | 돋보기
"""


def test_newest_first_because_the_file_is_append_only():
    # 파일은 아래쪽이 최신이다.  그대로 내면 화면 맨 위에 반년 전 항목이 온다.
    notes = parse_log(SAMPLE)
    assert [n.subject for n in notes] == ["돋보기", "포트 주인을 밝힌다", "저장소 초기화"]


def test_the_preamble_is_not_anybody_s_body():
    # `# 작업 로그` 와 형식 안내는 어느 항목에도 속하지 않는다.  첫 제목 앞의
    # 줄을 어딘가에 붙이면 그 항목만 설명문을 달고 나온다.
    notes = parse_log(SAMPLE)
    assert "append-only" not in "".join(n.body for n in notes)


def test_a_subheading_does_not_split_an_entry():
    # `###` 에서 끊으면 한 항목이 둘로 쪼개지고, 뒤쪽은 제목이 없는 채로 남는다.
    [_, middle, _] = parse_log(SAMPLE)
    assert "소제목이 있어도 한 항목이다." in middle.body
    assert middle.body.startswith("두 문단짜리 본문.")


def test_an_entry_can_have_no_body():
    assert parse_log(SAMPLE)[0].body == ""


def test_an_action_outside_the_documented_list_is_still_shown():
    """`docs/SCHEMA.md` 는 일곱 개를 적어 뒀는데 파일에는 `feat` 도 있다.

    목록에 없다고 버리면 그 커밋만 패치노트에서 조용히 사라진다 — 기록을 읽는
    쪽이 기록을 검열하면 안 된다.  화면이 중립 색으로 그리면 될 일이다.
    """
    assert parse_log(SAMPLE)[0].action == "feat"


def test_a_missing_file_is_an_empty_list_not_an_invention(tmp_path: Path):
    assert read_notes(tmp_path / "nope.md", 10) == []


def test_the_limit_takes_the_newest(tmp_path: Path):
    path = tmp_path / "log.md"
    path.write_text(SAMPLE, encoding="utf-8")
    assert [n.subject for n in read_notes(path, 2)] == ["돋보기", "포트 주인을 밝힌다"]


def test_the_endpoint_serves_this_repo_s_own_log(client):
    rows = client.get("/api/changelog", params={"limit": 5}).json()
    assert rows, "저장소의 docs/log.md 를 못 읽었습니다"
    assert len(rows) <= 5
    for row in rows:
        assert row["date"][:2] == "20"
        assert row["subject"]
    # 최신 순 — 날짜가 내림차순이어야 한다 (같은 날은 파일 순서를 지킨다).
    dates = [row["date"] for row in rows]
    assert dates == sorted(dates, reverse=True)


def test_the_endpoint_bounds_the_limit(client):
    assert client.get("/api/changelog", params={"limit": 0}).status_code == 422
    assert client.get("/api/changelog", params={"limit": 9999}).status_code == 422
