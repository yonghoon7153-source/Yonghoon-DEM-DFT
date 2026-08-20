"""Uploading, attaching and re-parsing files."""

from __future__ import annotations


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
        client, wrd_bytes, sample_id):
    """The instrument knows the cut-offs; do not ask the user to retype them."""
    _upload(client, wrd_bytes, sample_id=sample_id)
    sample = client.get(f"/api/samples/{sample_id}").json()
    # The synthetic fixture carries no schedule, so nothing should be invented.
    assert sample["cutoff_upper_v"] is None


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
