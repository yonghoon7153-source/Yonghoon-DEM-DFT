"""The upload endpoint's de-duplication path.

The same bytes arrive from two machines all the time, so this path runs far
more often than a first upload -- and it decides which sample a run belongs
to, which decides every cycle number in that sample.
"""

from __future__ import annotations

import pytest
from starlette.datastructures import UploadFile

from app.settings import settings


def _upload(client, content, name="cell_012.wrd", sample_id=None):
    params = {"sample_id": sample_id} if sample_id else {}
    return client.post("/api/runs/upload", params=params,
                       files={"file": (name, content, "application/octet-stream")})


def _second_sample(client) -> int:
    response = client.post("/api/samples", json={"name": "TEST-02"})
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_reuploading_the_same_bytes_does_not_move_a_run_to_another_sample(
        client, wrd_bytes, sample_id):
    """A duplicate upload is a no-op, never a silent reassignment."""
    run = _upload(client, wrd_bytes, sample_id=sample_id).json()
    other = _second_sample(client)

    response = _upload(client, wrd_bytes, sample_id=other)
    assert response.status_code == 409
    assert "PATCH" in response.json()["detail"]

    assert client.get(f"/api/runs/{run['id']}").json()["sample_id"] == sample_id
    assert len(client.get("/api/runs", params={"sample_id": other}).json()) == 0


def test_reuploading_an_orphan_into_a_missing_sample_is_a_404(client, wrd_bytes):
    orphan = _upload(client, wrd_bytes).json()
    assert _upload(client, wrd_bytes, sample_id=9999).status_code == 404
    assert client.get(f"/api/runs/{orphan['id']}").json()["sample_id"] is None


def test_attaching_an_orphan_by_re_upload_continues_the_cycle_numbering(
        client, wrd_bytes, finished_wrd_bytes, sample_id):
    """Re-upload attach has to shift the file, exactly as PATCH would."""
    first = _upload(client, finished_wrd_bytes, name="cell_011.wrd",
                    sample_id=sample_id).json()
    orphan = _upload(client, wrd_bytes, name="cell_012.wrd").json()
    assert orphan["sample_id"] is None
    assert orphan["cycle_offset"] == 0

    attached = _upload(client, wrd_bytes, name="cell_012.wrd",
                       sample_id=sample_id).json()
    assert attached["id"] == orphan["id"]
    assert attached["cycle_offset"] == first["cycle_count"]

    cycles = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    numbers = [c["cycle"] for c in cycles]
    assert numbers == sorted(numbers)
    assert len(numbers) == len(set(numbers))


def test_an_oversized_upload_is_refused_before_the_body_is_read(
        client, wrd_bytes, monkeypatch):
    """The 413 must not cost a full copy of the file in memory."""
    async def _refuse_to_be_read(self, size=-1):
        raise AssertionError("the body was read before the size check")

    monkeypatch.setattr(settings, "max_upload_bytes", 16)
    monkeypatch.setattr(UploadFile, "read", _refuse_to_be_read)

    response = _upload(client, wrd_bytes)
    assert response.status_code == 413
    assert "limit" in response.json()["detail"]


def test_an_upload_within_the_limit_still_reads(client, wrd_bytes, sample_id,
                                                monkeypatch):
    monkeypatch.setattr(settings, "max_upload_bytes", len(wrd_bytes) + 1)
    assert _upload(client, wrd_bytes, sample_id=sample_id).status_code == 201


@pytest.mark.parametrize("name", ["cell_012.wrd", "renamed.wrd"])
def test_a_duplicate_upload_to_the_same_sample_stays_a_no_op(
        client, wrd_bytes, sample_id, name):
    first = _upload(client, wrd_bytes, sample_id=sample_id).json()
    second = _upload(client, wrd_bytes, name=name, sample_id=sample_id)
    assert second.status_code == 201
    assert second.json()["id"] == first["id"]
