"""공유 암호 — 바깥에 열었을 때만 서는 문 (ADR 0014).

두 가지가 함께 틀리기 쉽다.  랩 안에서 아무것도 안 바뀌어야 하는데 문이
서거나, 바깥에 열었는데 어떤 경로 하나가 문 밖에 남아 있거나.  뒤쪽은 그
경로가 데이터를 돌려주면 문이 없는 것과 같다.
"""

from __future__ import annotations

import re

import pytest

from app import gate
from app.settings import settings

PASSWORD = "고체전해질"


@pytest.fixture
def locked():
    """암호가 걸린 상태."""
    before = settings.password
    settings.password = PASSWORD
    yield PASSWORD
    settings.password = before


def test_nothing_changes_without_a_password(client):
    """랩 안에서 쓰는 사람은 이 기능이 있는 줄도 몰라야 한다."""
    assert settings.password == ""
    assert client.get("/api/samples").status_code == 200
    assert client.get("/api/meta").status_code == 200


def test_the_api_is_closed_once_a_password_is_set(client, locked):
    response = client.get("/api/samples")
    assert response.status_code == 401
    # 화면이 401 을 알아볼 수 있어야 한다 — HTML 이 오면 JSON 파싱에서 죽는다.
    assert response.headers["content-type"].startswith("application/json")


def test_writes_are_closed_too(client, locked):
    """읽기만 막고 쓰기를 열어 두면 지우는 것을 못 막는다."""
    assert client.post("/api/groups", json={"name": "x"}).status_code == 401
    assert client.delete("/api/samples/1").status_code == 401


def test_health_stays_open(client, locked):
    """`bml use` 가 주소를 확인하는 통로다.

    이것까지 막으면 암호를 아는 사람도 주소를 등록할 수 없다.  대신 응답에
    데이터가 없어야 문 밖에 둘 수 있다.

    **이 집합은 자물쇠다.**  넓히려면 그 값이 문 밖에 있어도 되는 이유를 여기
    적어야 한다 -- `instance` 는 아래 시험이 그 이유를 적어 두었다.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert set(body) <= {"status", "instance", "wrdkit", "data_dir", "max_upload_mb"}


def test_the_instance_name_is_out_there_on_purpose(client, locked):
    """이름표는 **문 밖**이어야 쓸모가 있다 (Codex #8).

    `bml` 이 이것으로 확인하는 것은 "공개 주소가 정말 이 서버인가" 다.  도메인이
    아직 옛 VPS 를 가리키거나 저쪽 포트를 옛 터널이 잡고 있으면, 이번 연결이
    실패했는데도 **다른 워크벤치**가 200 을 준다.  그때 "열렸습니다" 를 내면
    그 주소를 받은 사람은 남의 데이터를 우리 것으로 본다.

    확인하는 쪽(`bml`)은 암호를 들고 있지 않다.  그래서 문 안에 두면 이 확인이
    아예 불가능하다.  대신 이 값으로 **할 수 있는 일이 없어야** 한다: 무작위고,
    아무것도 열지 않고, 서버를 다시 띄우면 버려진다.
    """
    body = client.get("/api/health").json()
    assert body["instance"]
    # 한 프로세스 안에서는 안 바뀐다 -- 바뀌면 자기 자신과도 안 맞는다.
    assert client.get("/api/health").json()["instance"] == body["instance"]
    # 값에서 무엇도 읽히면 안 된다.
    assert re.fullmatch(r"[0-9a-f]{16}", body["instance"])


def test_the_page_asks_instead_of_erroring(client, locked):
    """브라우저로 열면 401 JSON 이 아니라 암호를 묻는 한 장이 와야 한다."""
    response = client.get("/")
    assert response.status_code == 401
    assert "text/html" in response.headers["content-type"]
    assert "암호" in response.text


def test_the_right_password_opens_it(client, locked):
    opened = client.post("/__login", data={"password": PASSWORD}, follow_redirects=False)
    assert opened.status_code == 303
    assert client.get("/api/samples").status_code == 200


def test_the_wrong_password_does_not(client, locked):
    response = client.post("/__login", data={"password": "틀린암호"},
                           follow_redirects=False)
    assert response.status_code == 401
    assert client.get("/api/samples").status_code == 401


def test_the_cookie_does_not_carry_the_password(client, locked):
    """브라우저 저장소를 들여다본 사람이 암호 자체를 얻으면 안 된다 —
    사람들은 같은 암호를 다른 곳에도 쓴다."""
    client.post("/__login", data={"password": PASSWORD}, follow_redirects=False)
    jar = client.cookies.get(gate.COOKIE)
    assert jar and PASSWORD not in jar


def test_a_cookie_from_another_password_is_refused(client, locked):
    """암호를 바꾸면 옛 쿠키는 못 들어와야 한다."""
    client.cookies.set(gate.COOKIE, gate.token("옛날암호"))
    assert client.get("/api/samples").status_code == 401


# --- 순수 함수 ----------------------------------------------------------------

def test_a_cookie_is_not_the_password():
    assert gate.token("abc") != "abc"
    assert gate.token("abc") == gate.token("abc")
    assert gate.token("abc") != gate.token("abd")


def test_empty_never_opens():
    """암호가 비어 있는 것은 '문이 없다' 이지 '빈 암호가 맞다' 가 아니다.
    이 둘이 섞이면, 암호를 지운 순간 아무 쿠키나 통과한다."""
    assert not gate.accepts_cookie("", "")
    assert not gate.accepts_cookie(gate.token(""), "")
    assert not gate.accepts_password("", "")
    assert not gate.accepts_password(None, "x")


def test_the_served_commit_stays_behind_the_door(client, locked):
    """떠 있는 코드는 **문 안**에서만 보인다.

    커밋 해시가 비밀은 아니다.  그런데 문 밖에 두는 것은 꼭 필요한 것만이어야
    한다 — 그 줄이 한 번 넓어지면 다음에 무엇을 더 넣을지 정할 근거가 없어진다.
    갱신 알림은 어차피 문 안에서 보는 화면의 일이다 (ADR 0014).
    """
    assert "served_commit" not in client.get("/api/health").json()
    assert client.get("/api/revision").status_code == 401
