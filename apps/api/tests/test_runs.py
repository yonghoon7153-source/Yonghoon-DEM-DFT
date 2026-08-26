"""Uploading, attaching and re-parsing files."""

from __future__ import annotations

import synthetic


def _upload(client, content, name="cell_012.wrd", sample_id=None):
    params = {"sample_id": sample_id} if sample_id else {}
    return client.post("/api/runs/upload", params=params,
                       files={"file": (name, content, "application/octet-stream")})


def test_upload_parses_metadata_and_cycles(client, wrd_bytes, sample_id):
    response = _upload(client, wrd_bytes, sample_id=sample_id)
    assert response.status_code == 201, response.text
    run = response.json()
    assert run["device_model"] == "WBCS3000S1"
    assert run["row_count"] > 0
    assert run["cycle_count"] == 8
    assert run["complete_cycle_count"] == 7   # the last one is truncated
    assert run["sample_name"] == "TEST-01"


def test_uploading_the_same_bytes_twice_does_not_duplicate(client, wrd_bytes, sample_id):
    first = _upload(client, wrd_bytes, sample_id=sample_id).json()
    second = _upload(client, wrd_bytes, name="renamed.wrd", sample_id=sample_id).json()
    assert first["id"] == second["id"]
    assert len(client.get("/api/runs").json()) == 1


def test_a_second_upload_can_attach_an_orphan_run(client, wrd_bytes, sample_id):
    orphan = _upload(client, wrd_bytes).json()
    assert orphan["sample_id"] is None
    attached = _upload(client, wrd_bytes, sample_id=sample_id).json()
    assert attached["id"] == orphan["id"]
    assert attached["sample_id"] == sample_id


def test_a_non_wrd_upload_is_rejected_with_a_readable_message(client):
    response = _upload(client, b"this is not a wrd file" * 8, name="notes.txt")
    assert response.status_code == 422
    assert "could not read" in response.json()["detail"]


def test_an_empty_upload_is_rejected(client):
    response = _upload(client, b"")
    assert response.status_code == 422


def test_uploading_to_a_missing_sample_is_a_404(client, wrd_bytes):
    response = _upload(client, wrd_bytes, sample_id=9999)
    assert response.status_code == 404


def test_the_decoded_schedule_is_exposed(client, wrd_bytes, sample_id):
    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    schedule = client.get(f"/api/runs/{run['id']}/schedule").json()
    assert schedule["run_id"] == run["id"]
    assert schedule["sequence"] == 12   # from the _012 filename


def test_cycle_offset_can_be_set_by_hand_and_renumbers_the_cycles(
        client, wrd_bytes, sample_id):
    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    assert run["cycle_offset"] == 0

    updated = client.patch(f"/api/runs/{run['id']}",
                           json={"cycle_offset": 200}).json()
    assert updated["cycle_offset"] == 200
    assert updated["cycle_offset_source"] == "manual"

    cycles = client.get(f"/api/runs/{run['id']}/cycles").json()["cycles"]
    assert cycles[0]["cycle"] == 201


def test_a_negative_cycle_offset_is_rejected(client, wrd_bytes, sample_id):
    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    assert client.patch(f"/api/runs/{run['id']}",
                        json={"cycle_offset": -5}).status_code == 422


def test_a_second_file_continues_the_cycle_numbering(client, wrd_bytes,
                                                     finished_wrd_bytes, sample_id):
    first = _upload(client, finished_wrd_bytes, name="cell_011.wrd",
                    sample_id=sample_id).json()
    second = _upload(client, wrd_bytes, name="cell_012.wrd",
                     sample_id=sample_id).json()
    assert first["cycle_offset"] == 0
    assert second["cycle_offset"] == first["cycle_count"]

    cycles = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    numbers = [c["cycle"] for c in cycles]
    assert numbers == sorted(numbers)
    assert len(numbers) == len(set(numbers))   # no collisions between files


def test_reparse_rebuilds_from_the_stored_original(client, wrd_bytes, sample_id):
    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    again = client.post(f"/api/runs/{run['id']}/reparse")
    assert again.status_code == 200
    assert again.json()["cycle_count"] == run["cycle_count"]


def test_deleting_a_run_removes_its_cycles(client, wrd_bytes, sample_id):
    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    assert client.delete(f"/api/runs/{run['id']}").status_code == 204
    assert client.get(f"/api/runs/{run['id']}").status_code == 404
    assert client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"] == []


def _two_file_sample(client, wrd_bytes, finished_wrd_bytes, sample_id):
    """``_011`` then ``_012`` of one experiment, numbered as one run."""
    first = _upload(client, finished_wrd_bytes, name="cell_011.wrd",
                    sample_id=sample_id).json()
    second = _upload(client, wrd_bytes, name="cell_012.wrd",
                     sample_id=sample_id).json()
    assert second["cycle_offset"] == first["cycle_count"]
    return first, second


def test_detaching_a_file_renumbers_the_ones_left_behind(
        client, wrd_bytes, finished_wrd_bytes, sample_id):
    """Removing _011 must pull _012 back to cycle 1, or reference cycle 3 is gone."""
    first, second = _two_file_sample(client, wrd_bytes, finished_wrd_bytes, sample_id)

    detached = client.patch(f"/api/runs/{first['id']}",
                            json={"detach_sample": True}).json()
    assert detached["sample_id"] is None

    assert client.get(f"/api/runs/{second['id']}").json()["cycle_offset"] == 0
    cycles = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    assert cycles[0]["cycle"] == 1


def test_moving_a_file_to_another_sample_renumbers_both(
        client, wrd_bytes, finished_wrd_bytes, sample_id):
    first, second = _two_file_sample(client, wrd_bytes, finished_wrd_bytes, sample_id)
    other = client.post("/api/samples", json={"name": "TEST-02"}).json()["id"]

    moved = client.patch(f"/api/runs/{first['id']}",
                         json={"sample_id": other}).json()
    assert moved["sample_id"] == other
    assert moved["cycle_offset"] == 0

    assert client.get(f"/api/runs/{second['id']}").json()["cycle_offset"] == 0
    cycles = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    assert cycles[0]["cycle"] == 1


def test_reparse_renumbers_the_files_that_follow(
        client, wrd_bytes, finished_wrd_bytes, sample_id, monkeypatch):
    """A parser that finds more cycles in _011 has to push _012 along."""
    from app import storage
    from wrdkit import read_wrd_bytes

    import synthetic

    first, second = _two_file_sample(client, wrd_bytes, finished_wrd_bytes, sample_id)

    start = synthetic.ticks_ago(20 * 66 * 10)
    longer = synthetic.build_wrd(
        synthetic.make_cycles(n_cycles=first["cycle_count"] + 2,
                              points_per_branch=30, start_ticks=start),
        start_ticks=start)
    monkeypatch.setattr(storage, "reparse",
                        lambda sha256: read_wrd_bytes(longer,
                                                      source_name="cell_011.wrd"))

    again = client.post(f"/api/runs/{first['id']}/reparse").json()
    assert again["cycle_count"] == first["cycle_count"] + 2

    assert (client.get(f"/api/runs/{second['id']}").json()["cycle_offset"]
            == again["cycle_count"])
    cycles = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    numbers = [c["cycle"] for c in cycles]
    assert numbers == sorted(numbers)
    assert len(numbers) == len(set(numbers))   # no collisions between files


def test_deleting_a_run_keeps_the_original_upload(client, wrd_bytes, sample_id):
    """Non-negotiable #2 / ADR 0003: nothing can rebuild an original."""
    from app import storage

    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    path = storage.upload_path(run["sha256"])
    assert path.exists()

    response = client.delete(f"/api/runs/{run['id']}",
                             params={"delete_original": True})
    assert response.status_code == 204
    assert path.exists()


def test_uploading_fills_blank_sample_conditions_from_the_schedule(
        client, scheduled_wrd_bytes, sample_id):
    """The instrument knows the cut-offs; do not ask the user to retype them.

    This used to feed a schedule-less file and assert that nothing was filled
    in — which passes with the feature deleted.  The fixture now carries a
    schedule, so the assertion is about what actually gets read.
    """
    _upload(client, scheduled_wrd_bytes, sample_id=sample_id)
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["cutoff_upper_v"] == 3.78
    assert sample["cutoff_lower_v"] == 1.88


def test_a_file_without_a_schedule_invents_nothing(client, wrd_bytes, sample_id):
    """모르면 비워 둔다 — 없는 스케줄에서 값을 지어내지 않는다."""
    _upload(client, wrd_bytes, sample_id=sample_id)
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["cutoff_upper_v"] is None


def test_what_the_user_typed_is_not_overwritten_by_the_schedule(
        client, scheduled_wrd_bytes):
    """사용자 입력은 덮어쓰기(override)다 — 파일이 이기지 않는다."""
    sample = client.post("/api/samples", json={"name": "손으로 넣은 셀",
                                               "cutoff_upper_v": 4.4}).json()
    _upload(client, scheduled_wrd_bytes, sample_id=sample["id"])
    after = client.get(f"/api/samples/{sample['id']}").json()
    assert after["cutoff_upper_v"] == 4.4


# --- 수동 cycle_offset 은 겹치면 안 된다 -------------------------------------

def test_a_manual_offset_that_overlaps_a_sibling_is_refused(client, sample_id,
                                                            wrd_bytes, finished_wrd_bytes):
    """두 run 이 같은 사이클 번호를 쓰면 '3번 사이클' 이 조회 순서에 따라 달라진다.

    자동 배정은 고쳤지만 수동 PATCH 는 검사 없이 그대로 받아들이고 있었다.
    """
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("a_001.wrd", wrd_bytes, "application/octet-stream")})
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("a_002.wrd", finished_wrd_bytes,
                                "application/octet-stream")})
    runs = client.get("/api/runs", params={"sample_id": sample_id}).json()
    runs.sort(key=lambda r: r["cycle_offset"])
    first, second = runs[0], runs[-1]
    assert second["cycle_offset"] > 0, "자동 배정이 먼저 동작해야 한다"

    clash = client.patch(f"/api/runs/{second['id']}", json={"cycle_offset": 0})
    assert clash.status_code == 422
    assert "overlap" in clash.json()["detail"].lower()

    # 겹치지 않는 값은 그대로 받아들인다.
    ok = client.patch(f"/api/runs/{second['id']}",
                      json={"cycle_offset": first["cycle_count"] + 5})
    assert ok.status_code == 200
    assert ok.json()["cycle_offset_source"] == "manual"


def test_a_failed_parse_does_not_leave_half_written_cycles(client, sample_id,
                                                           wrd_bytes, monkeypatch):
    """저장 중 실패하면 되돌린다 — 반쯤 쓰인 사이클 표를 커밋하지 않는다."""
    from app import services

    real = services.persist_parse

    def explode(session, run, wrd):
        real(session, run, wrd)           # 사이클을 stage 한 뒤에
        raise RuntimeError("disk full")   # 실패한다

    monkeypatch.setattr("app.routers.runs.persist_parse", explode)
    response = client.post("/api/runs/upload", params={"sample_id": sample_id},
                           files={"file": ("x.wrd", wrd_bytes,
                                           "application/octet-stream")})
    assert response.status_code == 500

    runs = client.get("/api/runs", params={"sample_id": sample_id}).json()
    for run in runs:
        if run["parse_error"]:
            assert run["cycle_count"] == 0, "실패한 run 이 사이클을 들고 있다"


def test_a_later_upload_does_not_collide_with_a_pinned_run(client, sample_id,
                                                           wrd_bytes, finished_wrd_bytes):
    """수동으로 고정한 구간을 자동 배정이 침범하면 안 된다.

    PATCH 한 번은 겹침을 막았지만, 그 뒤에 *더 이른* 파일을 올리면 renumber 가
    수동 예약을 모른 채 1번부터 배정한다 — 같은 사이클 번호가 두 run 에 생기고,
    "3번 사이클" 이 조회 순서에 따라 달라진다.
    """
    # 나중에 시작한 파일을 먼저 올려서 손으로 고정한다.
    pinned = client.post("/api/runs/upload", params={"sample_id": sample_id},
                         files={"file": ("z_099.wrd", wrd_bytes,
                                         "application/octet-stream")}).json()
    assert pinned["cycle_count"] > 2

    pin = 5
    assert client.patch(f"/api/runs/{pinned['id']}",
                        json={"cycle_offset": pin}).status_code == 200

    # 그 뒤에 *더 이른* 파일을 올린다 — 정렬상 앞에 서므로 자동 배정이 1번부터
    # 잡으려 하고, 고정 구간(6-13)과 겹친다.
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("a_001.wrd", finished_wrd_bytes,
                                "application/octet-stream")})

    runs = client.get("/api/runs", params={"sample_id": sample_id}).json()
    spans = [(r["cycle_offset"] + 1, r["cycle_offset"] + r["cycle_count"])
             for r in runs if r["cycle_count"]]
    spans.sort()
    for (_, a_end), (b_start, _) in zip(spans, spans[1:], strict=False):
        assert a_end < b_start, f"사이클 번호가 겹친다: {spans}"

    # 고정한 값은 그대로여야 한다 — 사용자의 지시다.
    still = next(r for r in runs if r["id"] == pinned["id"])
    assert still["cycle_offset"] == pin
    assert still["cycle_offset_source"] == "manual"


def test_cycle_numbers_are_unique_across_a_samples_runs(client, sample_id,
                                                        wrd_bytes, finished_wrd_bytes):
    """같은 셀 안에서 사이클 번호는 유일해야 한다 — 조회 경로 전체의 전제다."""
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("b_002.wrd", finished_wrd_bytes,
                                "application/octet-stream")})
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("a_001.wrd", wrd_bytes, "application/octet-stream")})
    numbers = [c["cycle"] for c in
               client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]]
    assert len(numbers) == len(set(numbers)), "사이클 번호가 중복된다"
    assert numbers == sorted(numbers)


def test_reparse_all_rereads_every_run(client, wrd_bytes, finished_wrd_bytes):
    """계산이 바뀌면 **이미 올린 것도** 따라와야 한다.

    사이클 요약은 올릴 때 계산해 DB 에 넣는다 (ADR 0003).  그래서 wrdkit 을
    고쳐도 올려 둔 파일은 옛 숫자를 그대로 들고 있다 — 코드는 고쳤는데 화면은
    안 바뀐다.  한 개씩 누르는 길만 두면 쌓인 것을 아무도 안 누르고, 고친 값과
    안 고친 값이 한 저장소에 섞인다.
    """
    sample = client.post("/api/samples", json={"name": "재파싱 셀"}).json()
    # 서로 **다른** 바이트여야 한다 — 같은 파일을 두 번 올리면 sha256 으로
    # 하나로 묶인다 (불변 규칙 2).
    for name, payload in (("a.wrd", wrd_bytes), ("b.wrd", finished_wrd_bytes)):
        assert _upload(client, payload, name=name,
                       sample_id=sample["id"]).status_code == 201

    body = client.post("/api/runs/reparse").json()
    assert body["total"] == 2
    assert body["reparsed"] == 2
    assert body["failed"] == []

    # 값이 그대로 살아 있어야 한다 — 다시 읽는 것이지 지우는 것이 아니다.
    runs = client.get("/api/runs", params={"sample_id": sample["id"]}).json()
    assert len(runs) == 2
    assert all(r["cycle_count"] > 0 for r in runs)


def test_reparse_all_keeps_going_when_one_original_is_gone(
        client, wrd_bytes, finished_wrd_bytes, monkeypatch):
    """원본 하나가 사라졌다고 나머지가 옛 값으로 남으면 안 된다.

    실패는 세는 것이 아니라 **이름을 적는다** — "실패 1건" 만으로는 어느 파일인지
    알 수 없고, 그러면 고칠 수도 없다.
    """
    from app import storage

    sample = client.post("/api/samples", json={"name": "반쪽 셀"}).json()
    for name, payload in (("good.wrd", wrd_bytes), ("gone.wrd", finished_wrd_bytes)):
        _upload(client, payload, name=name, sample_id=sample["id"])

    runs = client.get("/api/runs", params={"sample_id": sample["id"]}).json()
    doomed = next(r for r in runs if r["original_name"] == "gone.wrd")
    real = storage.reparse

    def one_is_missing(sha256):
        if sha256 == doomed["sha256"]:
            raise FileNotFoundError("원본이 없습니다")
        return real(sha256)

    monkeypatch.setattr(storage, "reparse", one_is_missing)
    body = client.post("/api/runs/reparse").json()

    assert body["total"] == 2
    assert body["reparsed"] == 1
    assert [f["name"] for f in body["failed"]] == ["gone.wrd"]
    assert body["failed"][0]["reason"]


def test_the_literal_reparse_path_is_not_read_as_a_run_id(client, wrd_bytes):
    """`/api/runs/reparse` 가 run_id="reparse" 로 읽히지 않아야 한다.

    오늘 라우터 모양에서는 순서를 바꿔도 맞게 걸린다 — 확인했다.  하지만 누가
    `POST /{run_id}` 를 하나 붙이면 그 순간 이 창구가 422 로 바뀐다.  깨지는
    곳과 원인이 다른 파일에 있어서, 그때 찾기 어렵다.
    """
    sample = client.post("/api/samples", json={"name": "순서"}).json()
    _upload(client, wrd_bytes, name="a.wrd", sample_id=sample["id"])

    response = client.post("/api/runs/reparse")
    assert response.status_code == 200, response.text
    assert set(response.json()) == {"total", "reparsed", "failed"}


def _same_start_pair(short_cycles: int, long_cycles: int):
    """같은 계측을 두 시점에 내려받은 두 파일 — 시작 시각이 같다."""
    start = synthetic.ticks_ago(60 * 60 * 24)
    def build(n):
        return synthetic.build_wrd(
            synthetic.make_cycles(n_cycles=n, points_per_branch=20,
                                  start_ticks=start), start_ticks=start)
    return build(short_cycles), build(long_cycles)


def test_the_same_run_downloaded_twice_is_replaced_not_appended(client):
    """구동 중인 셀을 두 번 내려받으면 뒤엣것이 앞엣것을 **담고 있다.**

    이어 붙이면 사이클이 1..114, 115..314 가 되고 -- 115번이 사실 그 실험의
    1번이라 -- 유지율 곡선이 거기서 도로 올라간다.  셀이 스스로 회복한 그림이
    되는데 아무 오류도 안 난다 (실측 재현: 3+5 를 올렸더니 8 사이클, 용량이
    5.0 4.9 4.8 **5.0** 4.9 …).
    """
    short, long_ = _same_start_pair(3, 5)
    sample = client.post("/api/samples", json={"name": "구동셀"}).json()
    for payload in (short, long_):
        assert _upload(client, payload, name="cell.wrd",
                       sample_id=sample["id"]).status_code == 201

    cycles = client.get(f"/api/samples/{sample['id']}/cycles").json()["cycles"]
    assert [c["cycle"] for c in cycles] == [1, 2, 3, 4, 5]
    # 용량이 단조 감소여야 한다 -- 도로 올라가면 이어 붙인 것이다.
    caps = [c["discharge_capacity"] for c in cycles]
    assert caps == sorted(caps, reverse=True), caps

    runs = client.get("/api/runs", params={"sample_id": sample["id"]}).json()
    by_len = sorted(runs, key=lambda r: r["cycle_count"])
    assert by_len[0]["superseded_by"] == by_len[-1]["id"]
    assert by_len[-1]["superseded_by"] is None
    # **원본은 지우지 않는다** (불변 규칙 2).  목록에는 남는다.
    assert len(runs) == 2


def test_a_run_restarted_after_an_eis_measurement_still_appends(client):
    """돌리다 EIS 찍고 다시 돌린 것은 **이어 붙는 것이 맞다.**

    그때는 계측이 새로 시작하므로 `.wrd` 의 시작 시각이 다르다.  같은 계측을
    두 번 내려받은 것과 이것을 가르는 것이 `acquisition_key` 의 전부다 --
    잘못 묶으면 뒤에 돌린 사이클이 통째로 사라진다.
    """
    first = synthetic.ticks_ago(60 * 60 * 48)
    second = synthetic.ticks_ago(60 * 60 * 12)      # EIS 찍고 12시간 뒤 재시작
    a = synthetic.build_wrd(synthetic.make_cycles(n_cycles=3, points_per_branch=20,
                                                  start_ticks=first), start_ticks=first)
    b = synthetic.build_wrd(synthetic.make_cycles(n_cycles=4, points_per_branch=20,
                                                  start_ticks=second), start_ticks=second)
    sample = client.post("/api/samples", json={"name": "EIS 끼인 셀"}).json()
    for name, payload in (("a.wrd", a), ("b.wrd", b)):
        _upload(client, payload, name=name, sample_id=sample["id"])

    cycles = client.get(f"/api/samples/{sample['id']}/cycles").json()["cycles"]
    assert [c["cycle"] for c in cycles] == [1, 2, 3, 4, 5, 6, 7]
    assert all(r["superseded_by"] is None
               for r in client.get("/api/runs",
                                   params={"sample_id": sample["id"]}).json())


def test_deleting_the_longer_file_gives_the_shorter_one_its_place_back(client):
    """이긴 파일을 지우면 대체됐던 파일이 곧바로 셀의 사이클이 된다.

    대체는 지우는 것이 아니라 **가리는 것**이다.  가린 것을 치웠는데 셀이 빈
    채로 남으면, 실수로 지운 사람에게 데이터가 사라진 것으로 보인다.
    """
    short, long_ = _same_start_pair(3, 5)
    sample = client.post("/api/samples", json={"name": "되돌아오나"}).json()
    for payload in (short, long_):
        _upload(client, payload, name="cell.wrd", sample_id=sample["id"])

    runs = client.get("/api/runs", params={"sample_id": sample["id"]}).json()
    longer = max(runs, key=lambda r: r["cycle_count"])
    assert client.delete(f"/api/runs/{longer['id']}").status_code == 204

    cycles = client.get(f"/api/samples/{sample['id']}/cycles").json()["cycles"]
    assert [c["cycle"] for c in cycles] == [1, 2, 3]
    left = client.get("/api/runs", params={"sample_id": sample["id"]}).json()
    assert [r["superseded_by"] for r in left] == [None]
