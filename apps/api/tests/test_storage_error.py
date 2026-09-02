"""저장 장치가 사라졌을 때 화면이 무엇을 말하는가.

실측 2026-08-30: 데이터 폴더를 둔 외장하드를 뽑았다 끼웠더니 돌던 서버가 죽은
마운트를 계속 쥐었고, 대시보드에는 ``500 Internal Server Error`` 만 떴다.  그
한 줄로는 무엇이 잘못됐는지도, 데이터가 남아 있는지도 알 수 없다 — 사람이 먼저
물은 것이 "초기화된 건가" 였다.

이 시험이 못 박는 것은 둘이다: **이유를 적는가**, 그리고 **아는 것만 적는가**
(§0.4).  잠김이나 스키마 오류까지 "외장하드" 탓으로 돌리면, 그 안내를 따라간
사람이 멀쩡한 드라이브를 뽑았다 끼우게 된다.
"""

from __future__ import annotations

import pytest
from sqlalchemy.exc import (
    DatabaseError,
    IntegrityError,
    InterfaceError,
    OperationalError,
)

from app.db import get_session
from app.main import app


def _dead(said: str, kind=OperationalError):
    """무엇을 부르든 sqlite 가 그 말을 하며 죽는 세션.

    라우터마다 부르는 것이 달라서(`exec` · `get` · `scalar`) 하나만 막으면
    다른 길로 새어 500 이 그대로 나간다.
    """
    class _DeadStorage:
        def __getattr__(self, _name):
            def boom(*_args, **_kwargs):
                raise kind("SELECT 1", {}, Exception(said))
            return boom

    def _yield():
        yield _DeadStorage()

    return _yield


@pytest.fixture
def broken(client):
    def use(said: str, kind=OperationalError):
        app.dependency_overrides[get_session] = _dead(said, kind)
        return client
    yield use
    app.dependency_overrides.pop(get_session, None)


def test_장치가_사라지면_그렇게_말한다(broken):
    response = broken("disk I/O error").get("/api/samples")
    assert response.status_code == 503
    detail = response.json()["detail"]
    # 무엇을 못 읽었는지 — 경로를 적는다.  경로가 없으면 어느 폴더를 봐야
    # 하는지 화면 어디에도 없다.
    assert "데이터 폴더를 읽지 못했습니다" in detail
    assert "외장하드" in detail
    # **데이터가 남아 있다고 말한다.**  이 한 줄이 없어서 "초기화된 건가" 를
    # 먼저 물었다.
    assert "지워지지 않았습니다" in detail
    # 다음에 할 일 — 짐작이 아니라 명령으로.
    assert "bml data" in detail
    # sqlite 가 한 말도 그대로 남긴다.
    assert "disk I/O error" in detail


def test_대시보드만이_아니다(broken):
    """활동 기록도 같은 자리에서 같은 말을 한다 — 화면에서 먼저 눈에 띈 곳이다."""
    detail = broken("disk I/O error").get("/api/activity").json()["detail"]
    assert "데이터 폴더를 읽지 못했습니다" in detail


def test_잠김은_외장하드_탓으로_돌리지_않는다(broken):
    """아는 것만 원인이라고 적는다 — 잠김은 장치 문제가 아니다."""
    detail = broken("database is locked").get("/api/samples").json()["detail"]
    assert "외장하드" not in detail
    assert "database is locked" in detail


def test_스키마_오류도_장치_탓이_아니다(broken):
    detail = broken("no such column: foo").get("/api/samples").json()["detail"]
    assert "외장하드" not in detail
    assert "no such column" in detail


#: **`OperationalError` 하나로는 모자랐다.**  드라이브가 죽으면 sqlite 가 내는
#: 것이 하나가 아니다: `database disk image is malformed` 는 `DatabaseError`,
#: 끊긴 연결은 `InterfaceError` 다.  둘 다 `OperationalError` 의 하위가 아니라
#: **형제**라서 (실측: `issubclass(DatabaseError, OperationalError)` 는 False)
#: 처음 핸들러를 그냥 지나쳤고, 화면에는 고치기 전과 똑같은 맨 500 이 나갔다.
@pytest.mark.parametrize(
    ("kind", "said"),
    [
        (OperationalError, "disk I/O error"),
        (DatabaseError, "database disk image is malformed"),
        (InterfaceError, "Cannot operate on a closed database"),
    ],
)
def test_드라이버가_내는_것은_다_잡는다(broken, kind, said):
    response = broken(said, kind).get("/api/samples")
    assert response.status_code == 503
    assert "데이터 폴더를 읽지 못했습니다" in response.json()["detail"]
    assert said in response.json()["detail"]


#: 같은 가지에 달렸지만 **저장소 문제가 아닌 것**은 감싸지 않는다.  사람이
#: 보낸 것이 잘못된 것을 "외장하드를 보세요" 로 덮으면, 그 안내를 따라간
#: 사람이 멀쩡한 드라이브를 뽑았다 끼운다.  500 과 traceback 그대로 나간다.
def test_사람_잘못은_저장소_탓으로_감싸지_않는다(broken):
    # 핸들러가 도로 던지므로 예외가 그대로 올라온다 — `TestClient` 는 그것을
    # 다시 던지고, 실제 서버에서는 500 과 traceback 이 된다 (예전 그대로).
    with pytest.raises(IntegrityError):
        broken("UNIQUE constraint failed", IntegrityError).get("/api/samples")


def test_health_는_저장소가_죽어도_200(broken):
    """**`bml` 의 진단이 여기에 달려 있다.**

    `bml` 의 도달 검사는 전부 `/api/health` 의 상태 코드 하나로 판정한다
    (`http_code_of` · `server_alive` · `instance_of`).  그리고 터널 너머의
    503 을 "터널이 죽었다" 로 읽고 **터널을 닫는다** (`share_stale`).

    그래서 health 가 DB 를 보게 되는 순간, 외장하드가 빠진 것이 "터널이
    죽었다" 로 읽히고 멀쩡한 터널이 닫힌다 — 남들이 쓰고 있는 주소가.
    health 는 문 밖이고(ADR 0014) DB 밖이어야 한다.
    """
    assert broken("disk I/O error").get("/api/health").status_code == 200


def test_멀쩡한_길은_그대로다(client):
    """핸들러가 정상 응답을 건드리지 않는다."""
    assert client.get("/api/samples").status_code == 200
