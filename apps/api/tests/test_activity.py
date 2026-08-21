"""누가 무엇을 했는지 — 기록되는 것과 기록되지 않는 것.

이 기록이 틀리는 방식은 둘이다. 한 종류의 편집만 조용히 빠지거나(목록은
멀쩡해 보인다), 아무도 안 한 편집이 쌓이거나(같은 값을 다시 저장한 것,
업로드가 만든 사이클 만 개). 둘 다 오류를 내지 않는다.
"""

from __future__ import annotations

from urllib.parse import quote

from app.actor import ACTOR_HEADER, clean_actor, decode_actor


def _as(name: str) -> dict:
    """헤더는 ASCII 만 담을 수 있다 — 브라우저가 하는 것과 같이 인코딩한다."""
    return {ACTOR_HEADER: quote(name)}


def _feed(client, **params):
    return client.get("/api/activity", params=params).json()


def test_a_cell_records_who_made_it(client):
    sample = client.post("/api/samples", json={"name": "No_1_dry"},
                         headers=_as("용훈")).json()
    assert sample["created_by"] == "용훈"
    assert sample["updated_by"] == "용훈"

    [entry] = _feed(client, entity="sample")
    assert (entry["actor"], entry["action"], entry["label"]) \
        == ("용훈", "create", "No_1_dry")


def test_an_edit_records_who_and_what(client):
    sample = client.post("/api/samples", json={"name": "No_1_dry"},
                         headers=_as("용훈")).json()
    edited = client.patch(f"/api/samples/{sample['id']}",
                          json={"total_mass_mg": 31.6}, headers=_as("동료")).json()

    # 만든 사람은 그대로, 고친 사람만 바뀐다.
    assert edited["created_by"] == "용훈"
    assert edited["updated_by"] == "동료"

    latest = _feed(client, entity="sample")[0]
    assert latest["actor"] == "동료"
    assert latest["action"] == "update"
    assert latest["fields"] == ["total_mass_mg"]


def test_saving_the_same_value_is_not_an_edit(client):
    """같은 값을 다시 저장한 것은 아무도 한 편집이 아니다.

    세면 목록이 "아무 일 없음" 으로 가득 차고, 진짜 편집이 그 사이에 묻힌다.
    """
    sample = client.post("/api/samples", json={"name": "No_1_dry",
                                               "total_mass_mg": 31.6},
                         headers=_as("용훈")).json()
    before = len(_feed(client))
    client.patch(f"/api/samples/{sample['id']}", json={"total_mass_mg": 31.6},
                 headers=_as("용훈"))
    assert len(_feed(client)) == before


def test_an_upload_is_one_line_not_ten_thousand(client, sample_id, wrd_bytes):
    """사이클 행은 사람이 한 편집이 아니다.  사건은 업로드 쪽이다."""
    run = client.post("/api/runs/upload", params={"sample_id": sample_id},
                      files={"file": ("No_1_dry_011.wrd", wrd_bytes,
                                      "application/octet-stream")},
                      headers=_as("용훈")).json()
    assert run["created_by"] == "용훈"

    runs = _feed(client, entity="run")
    assert [(r["actor"], r["action"], r["label"]) for r in runs] \
        == [("용훈", "create", "No_1_dry_011.wrd")]
    assert not [entry for entry in _feed(client, limit=500)
                if entry["entity"] not in {"sample", "group", "preset", "run"}]


def test_groups_and_presets_are_recorded_too(client):
    """라우터마다 기록을 부르게 하면 언젠가 하나를 빠뜨린다.

    빠뜨린 그 한 종류만 목록에서 사라지는데, 목록은 멀쩡해 보인다.
    """
    client.post("/api/groups", json={"name": "고Ni 60도"}, headers=_as("용훈"))
    client.post("/api/composition-presets",
                json={"name": "건식 80", "settings": {"diameter_mm": 13}},
                headers=_as("동료"))

    seen = {(e["entity"], e["actor"], e["label"]) for e in _feed(client)}
    assert ("group", "용훈", "고Ni 60도") in seen
    assert ("preset", "동료", "건식 80") in seen


def test_a_deleted_thing_is_still_readable(client):
    """지워진 뒤에 찾는 것이 정확히 그때다."""
    group = client.post("/api/groups", json={"name": "지울 그룹"},
                        headers=_as("용훈")).json()
    client.delete(f"/api/groups/{group['id']}", headers=_as("동료"))

    latest = _feed(client, entity="group")[0]
    assert (latest["action"], latest["actor"], latest["label"]) \
        == ("delete", "동료", "지울 그룹")


def test_one_cell_s_history_can_be_asked_for(client):
    """실제로 하는 질문은 "이 질량 누가 바꿨어" 지 "화요일에 무슨 일" 이 아니다."""
    first = client.post("/api/samples", json={"name": "A"},
                        headers=_as("용훈")).json()
    second = client.post("/api/samples", json={"name": "B"},
                         headers=_as("동료")).json()
    client.patch(f"/api/samples/{first['id']}", json={"notes": "n"},
                 headers=_as("동료"))

    history = _feed(client, entity="sample", entity_id=first["id"])
    assert [entry["action"] for entry in history] == ["update", "create"]
    assert all(entry["entity_id"] == first["id"] for entry in history)
    assert second["id"] != first["id"]


def test_nobody_saying_who_they_are_still_works(client):
    """이름을 안 댔다고 저장이 막히면 안 된다 — 이것은 신원 확인이 아니다."""
    sample = client.post("/api/samples", json={"name": "익명"}).json()
    assert sample["created_by"] == ""
    assert _feed(client, entity="sample")[0]["actor"] == ""


def test_the_feed_is_newest_first_and_bounded(client):
    for index in range(5):
        client.post("/api/samples", json={"name": f"S{index}"}, headers=_as("용훈"))
    feed = _feed(client, limit=3)
    assert [entry["label"] for entry in feed] == ["S4", "S3", "S2"]


def test_a_name_is_cleaned_before_it_is_stored():
    # 표에 그려지고 헤더로 오가는 값이다.  줄바꿈 하나가 남의 버그 리포트가 된다.
    assert clean_actor("  용훈  ") == "용훈"
    assert clean_actor("용훈\n") == "용훈"
    assert clean_actor("용\x00훈") == "용훈"
    assert clean_actor(None) == ""
    assert clean_actor("") == ""
    # 사이의 공백은 이름의 일부다 (Kim Yonghoon).
    assert clean_actor("Kim Yonghoon") == "Kim Yonghoon"
    assert len(clean_actor("가" * 200)) == 40


def test_an_odd_name_never_fails_the_write(client):
    """이름이 이상해서 저장이 실패하는 일은 없어야 한다."""
    created = client.post("/api/samples", json={"name": "cell"},
                          headers=_as("가" * 200))
    assert created.status_code == 201
    assert len(created.json()["created_by"]) == 40


def test_a_korean_name_survives_the_header(client):
    """HTTP 헤더는 ASCII 만 담는다.

    한글 이름을 그대로 넣으면 요청이 브라우저를 떠나기도 전에 거절된다.
    이 랩의 이름은 대부분 한글이므로, 이게 안 되면 기능 자체가 없는 것과 같다.
    """
    assert decode_actor(quote("김용훈")) == "김용훈"
    # 인코딩 안 된 ASCII 이름도 그대로 지나간다.
    assert decode_actor("Yonghoon") == "Yonghoon"
    # 이름 안의 % 하나가 이름을 망가뜨리지 않는다.
    assert decode_actor("100%") == "100%"

    sample = client.post("/api/samples", json={"name": "cell"},
                         headers=_as("김용훈")).json()
    assert sample["created_by"] == "김용훈"


def test_the_dashboard_says_whose_cell_each_row_is(client):
    """표에서 남의 셀과 내 셀이 섞인다 — 이름이 없으면 열어 봐야 안다."""
    client.post("/api/samples", json={"name": "A"}, headers=_as("안용훈"))
    client.post("/api/samples", json={"name": "B"})   # 이름을 안 댄 사람

    rows = {row["sample_name"]: row["owner"]
            for row in client.get("/api/dashboard").json()["rows"]}
    assert rows == {"A": "안용훈", "B": ""}
