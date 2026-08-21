"""공유 서버의 실시간 갱신 — 무엇이 "바뀌었다" 로 세어지는가.

여기서 틀리면 둘 중 하나다: 남이 바꾼 것이 내 화면에 영영 안 나타나거나(놓친
bump), 아무 일도 없는데 모든 화면이 계속 다시 읽거나(과한 bump). 둘 다 조용히
틀리고, 둘 다 사람이 "왜 안 되지" 하기 전까지 아무 오류도 내지 않는다.
"""

from __future__ import annotations

import asyncio

import pytest

from app.live import REVISION_HEADER, Revision, should_bump


def test_a_write_moves_the_revision(client, sample_id):
    before = client.get("/api/revision").json()["revision"]
    written = client.patch(f"/api/samples/{sample_id}", json={"total_mass_mg": 30.0})

    assert written.status_code == 200
    after = client.get("/api/revision").json()["revision"]
    assert after > before
    # 쓴 사람은 이미 답을 들고 있다.  이 헤더로 자기 자신의 공지를 무시해서,
    # 저장 직후 방금 보낸 것을 도로 읽어 오는 일이 없게 한다.
    assert written.headers[REVISION_HEADER] == str(after)


def test_a_read_does_not(client, sample_id):
    before = client.get("/api/revision").json()["revision"]
    client.get(f"/api/samples/{sample_id}")
    client.get("/api/samples")
    assert client.get("/api/revision").json()["revision"] == before


def test_a_refused_write_does_not(client, sample_id):
    """422 는 아무것도 바꾸지 않았다.

    이걸 세면 누가 숫자 칸에 글자를 하나 칠 때마다 열려 있는 모든 화면이
    다시 읽는다.
    """
    before = client.get("/api/revision").json()["revision"]
    refused = client.patch(f"/api/samples/{sample_id}", json={"total_mass_mg": -5})
    assert refused.status_code == 422
    assert client.get("/api/revision").json()["revision"] == before
    assert REVISION_HEADER not in refused.headers


@pytest.mark.parametrize("method,status,path,expected", [
    ("POST", 201, "/api/groups", True),
    ("PATCH", 200, "/api/samples/1", True),
    ("DELETE", 204, "/api/runs/1", True),
    ("GET", 200, "/api/samples", False),
    ("POST", 422, "/api/samples", False),
    ("POST", 500, "/api/samples", False),
    # 화면(정적 파일)은 API 가 아니다.
    ("POST", 200, "/index.html", False),
])
def test_what_counts_as_a_change(method, status, path, expected):
    assert should_bump(method, status, path) is expected


def test_every_router_is_announced_without_being_asked(client, sample_id):
    """미들웨어에 둔 이유.  라우터마다 부르게 하면 언젠가 하나를 빠뜨린다.

    빠뜨린 그 한 종류의 편집만 남의 화면에서 안 보이는데, 그런 종류의 낡음이
    가장 알아차리기 어렵다.
    """
    seen = client.get("/api/revision").json()["revision"]
    for call in (
        lambda: client.post("/api/groups", json={"name": "고Ni"}),
        lambda: client.patch(f"/api/samples/{sample_id}", json={"notes": "n"}),
        lambda: client.post("/api/composition-presets",
                            json={"name": "p", "settings": {"diameter_mm": 13}}),
    ):
        response = call()
        assert response.status_code < 400, response.text
        current = client.get("/api/revision").json()["revision"]
        assert current > seen, f"{response.request.url} 이 아무것도 알리지 않았다"
        seen = current


def test_the_stream_opens_with_where_things_already_are(client, sample_id):
    """연결한 순간의 값을 먼저 준다.

    없으면, 남이 편집하는 도중에 연 페이지는 다음 편집이 일어날 때까지 한 판
    뒤처진 채로 앉아 있게 된다.
    """
    from app.live import revision, revision_stream

    client.patch(f"/api/samples/{sample_id}", json={"total_mass_mg": 31.0})
    current = revision.value

    async def scenario():
        lines = []
        async for chunk in revision_stream(_disconnect_after(1), heartbeat=0.01):
            lines.append(chunk)
        return lines

    assert asyncio.run(scenario())[0] == f"event: revision\ndata: {current}\n\n"


def test_the_stream_announces_a_change(client, sample_id):
    from app.live import revision, revision_stream

    async def scenario():
        chunks = []
        stream = revision_stream(_disconnect_after(2), heartbeat=1.0)
        chunks.append(await stream.__anext__())      # 여는 줄
        revision.bump()
        chunks.append(await stream.__anext__())      # 바뀌었다는 줄
        await stream.aclose()
        return chunks

    opened, changed = asyncio.run(scenario())
    assert opened.split("data: ")[1].strip() != changed.split("data: ")[1].strip()
    assert changed.startswith("event: revision")


def test_a_silent_stream_still_says_something(client):
    """말 없는 연결은 프록시와 잠든 무선이 조용히 끊는다.

    끊긴 것을 브라우저는 모르고, 사람은 화면이 갱신을 멈춘 뒤에야 안다.
    """
    from app.live import revision_stream

    async def scenario():
        return [chunk async for chunk
                in revision_stream(_disconnect_after(2), heartbeat=0.01)]

    assert asyncio.run(scenario())[1] == ": keep-alive\n\n"


def _disconnect_after(loops: int):
    """루프를 *loops* 번 돌고 나면 끊어진 척한다."""
    state = {"left": loops}

    async def is_disconnected() -> bool:
        state["left"] -= 1
        return state["left"] < 0

    return is_disconnected


# --- 카운터 자체 ------------------------------------------------------------

def test_a_waiter_is_woken_exactly_once():
    async def scenario():
        counter = Revision()
        waiting = asyncio.create_task(counter.wait_past(0, timeout=2))
        await asyncio.sleep(0)          # 기다리는 쪽이 실제로 잠들게 한다
        counter.bump()
        return await waiting

    assert asyncio.run(scenario()) == 1


def test_a_bump_between_check_and_wait_is_not_lost():
    """이미 지나간 값이면 기다리지 않고 바로 준다.

    안 그러면 내가 읽은 직후에 들어온 편집 하나가 다음 편집이 올 때까지
    아무에게도 전달되지 않는다.
    """
    async def scenario():
        counter = Revision()
        counter.bump()
        return await counter.wait_past(0, timeout=0.01)

    assert asyncio.run(scenario()) == 1


def test_waiting_gives_up_so_a_heartbeat_can_go_out():
    """말 없는 연결은 프록시와 잠든 무선이 조용히 끊는다."""
    async def scenario():
        counter = Revision()
        counter.value = 7
        return await counter.wait_past(7, timeout=0.01)

    assert asyncio.run(scenario()) == 7
