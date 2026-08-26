"""쓰다가 걸린 것을 겪은 자리에 적는 칸 (ADR 0033)."""

from __future__ import annotations

from app.actor import ACTOR_HEADER as ACTOR


def test_a_note_can_be_written_replied_to_resolved_and_reopened(client):
    """되돌릴 수 없는 버튼은 아무도 안 누른다.

    잘못 눌러 접힌 항목을 되살릴 길이 없으면 사람은 '정리됨' 자체를 안 누르고,
    그러면 목록이 전부 열린 채로 쌓여 아무 뜻이 없어진다.
    """
    made = client.post("/api/feedback",
                       json={"kind": "issue", "body": "클립보드가 전체를 복사한다"})
    assert made.status_code == 201, made.text
    note = made.json()
    assert note["resolved_at"] is None and note["replies"] == []

    with_reply = client.post(f"/api/feedback/{note['id']}/replies",
                             json={"body": "고른 사이클만 나가게 고쳤습니다"})
    assert with_reply.status_code == 201
    assert [r["body"] for r in with_reply.json()["replies"]] == \
        ["고른 사이클만 나가게 고쳤습니다"]

    done = client.patch(f"/api/feedback/{note['id']}", json={"resolved": True}).json()
    assert done["resolved_at"] is not None

    again = client.patch(f"/api/feedback/{note['id']}", json={"resolved": False}).json()
    assert again["resolved_at"] is None
    assert again["resolved_by"] == ""
    # 답글은 접었다 펴는 것과 무관하게 그대로 있어야 한다.
    assert len(again["replies"]) == 1


def test_open_notes_come_first_and_resolved_ones_stay(client):
    """정리된 항목을 목록에서 **빼지 않는다.**

    같은 불편이 두 달 뒤에 다시 올라올 때 "그때 이렇게 정리했다" 가 보여야
    한다.  대신 아래로 내린다 — 지금 할 일이 위에 있어야 하니까.
    """
    ids = [client.post("/api/feedback", json={"body": f"{i}번"}).json()["id"]
           for i in range(3)]
    client.patch(f"/api/feedback/{ids[2]}", json={"resolved": True})

    notes = client.get("/api/feedback").json()
    assert len(notes) == 3
    assert [n["resolved_at"] is None for n in notes] == [True, True, False]
    # 열린 것 안에서는 최근이 위.
    assert notes[0]["body"] == "1번"

    only_open = client.get("/api/feedback", params={"include_resolved": False}).json()
    assert [n["body"] for n in only_open] == ["1번", "0번"]


def test_deleting_a_note_takes_its_replies_with_it(client):
    """답글만 남으면 무엇에 대한 답인지 알 수 없다."""
    note = client.post("/api/feedback", json={"body": "지울 것"}).json()
    client.post(f"/api/feedback/{note['id']}/replies", json={"body": "답"})
    assert client.delete(f"/api/feedback/{note['id']}").status_code == 204
    assert client.get("/api/feedback").json() == []
    # 지운 항목의 답글을 다시 부르면 404 여야 한다 (남아 있으면 안 된다).
    assert client.post(f"/api/feedback/{note['id']}/replies",
                       json={"body": "또"}).status_code == 404


def test_a_reply_can_be_removed_without_touching_the_note(client):
    """해결하면 그 댓글만 지운다 — 항목은 기록으로 남긴다."""
    note = client.post("/api/feedback", json={"body": "본문"}).json()
    full = client.post(f"/api/feedback/{note['id']}/replies", json={"body": "댓글"}).json()
    reply_id = full["replies"][0]["id"]
    assert client.delete(
        f"/api/feedback/{note['id']}/replies/{reply_id}").status_code == 204
    assert client.get("/api/feedback").json()[0]["replies"] == []
    assert client.get("/api/feedback").json()[0]["body"] == "본문"


def test_an_empty_body_is_refused(client):
    """빈 줄이 목록에 쌓이면 목록이 못 쓰게 된다."""
    assert client.post("/api/feedback", json={"body": "   "}).status_code == 422
    note = client.post("/api/feedback", json={"body": "본문"}).json()
    assert client.post(f"/api/feedback/{note['id']}/replies",
                       json={"body": ""}).status_code == 422


def test_a_reply_moves_the_note_so_the_dot_lights_up(client):
    """답글이 붙은 것도 그 항목이 **움직인 것**이다.

    알림 점은 "내가 마지막으로 본 뒤에 뭔가 움직였나" 로 판정한다.  답글에
    `updated_at` 을 안 찍으면, 남이 내 항목에 답을 달아도 점이 안 뜬다.
    """
    note = client.post("/api/feedback", json={"body": "본문"}).json()
    moved = client.post(f"/api/feedback/{note['id']}/replies",
                        json={"body": "답"}).json()
    assert moved["updated_at"] >= note["updated_at"]
    assert moved["updated_at"] >= moved["replies"][0]["created_at"]


def test_the_name_in_the_top_bar_is_who_wrote_it(client):
    """로그인이 아니다 (ADR 0012) — 상단 막대에 적어 둔 이름이 그대로 붙는다.

    헤더는 ASCII 만 담을 수 있어서 브라우저가 퍼센트 인코딩해 보낸다.  한글
    이름이 이 저장소의 기본이므로 시험도 그 길로 간다.
    """
    from urllib.parse import quote

    made = client.post("/api/feedback", json={"body": "누가 썼나"},
                       headers={ACTOR: quote("안혁주")}).json()
    assert made["created_by"] == "안혁주"
    done = client.patch(f"/api/feedback/{made['id']}", json={"resolved": True},
                        headers={ACTOR: quote("안용훈")}).json()
    assert done["resolved_by"] == "안용훈"
