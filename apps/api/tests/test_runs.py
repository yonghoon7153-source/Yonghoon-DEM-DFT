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


def test_uploading_fills_blank_sample_conditions_from_the_schedule(
        client, wrd_bytes, sample_id):
    """The instrument knows the cut-offs; do not ask the user to retype them."""
    _upload(client, wrd_bytes, sample_id=sample_id)
    sample = client.get(f"/api/samples/{sample_id}").json()
    # The synthetic fixture carries no schedule, so nothing should be invented.
    assert sample["cutoff_upper_v"] is None
