"""End-to-end against a real instrument file.

    WRDKIT_SAMPLE=/path/to/file.wrd pytest apps/api/tests

Asserts on physics and on the shape of the answer, not on values specific to
one file, so any WBCS3000 cycling run satisfies them.
"""

from __future__ import annotations

import pytest


@pytest.fixture
def real_sample(client, real_wrd_path):
    sample = client.post("/api/samples", json={
        "name": real_wrd_path.stem,
        "cathode_type": "High-Ni",
        "process": "dry",
        "total_mass_mg": 31.6,
        "active_wt_percent": 80,
        "diameter_mm": 13,
        "nominal_specific_capacity_mah_g": 205.9,
    }).json()
    with real_wrd_path.open("rb") as handle:
        response = client.post(
            "/api/runs/upload", params={"sample_id": sample["id"]},
            files={"file": (real_wrd_path.name, handle, "application/octet-stream")})
    assert response.status_code == 201, response.text
    return sample["id"], response.json()


def test_upload_reads_the_whole_file(real_sample):
    _, run = real_sample
    assert run["row_count"] > 1000
    assert run["cycle_count"] > 0
    assert run["parse_error"] == ""


def test_the_schedule_is_decoded_into_conditions(client, real_sample):
    sample_id, run = real_sample
    schedule = run["schedule"]
    if not schedule:
        pytest.skip("file carries no schedule")
    assert schedule["upper_cutoff_v"] > schedule["lower_cutoff_v"]
    assert schedule["steps"]
    # Blank sample conditions get filled from the instrument, not from the user.
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["cutoff_upper_v"] == schedule["upper_cutoff_v"]
    assert sample["cutoff_lower_v"] == schedule["lower_cutoff_v"]


def test_specific_capacity_is_physically_plausible(client, real_sample):
    sample_id, _ = real_sample
    cycles = client.get(f"/api/samples/{sample_id}/cycles",
                        params={"basis": "mAh/g"}).json()["cycles"]
    assert cycles
    first = cycles[0]["discharge_capacity"]
    assert 50 < first < 400, f"{first} mAh/g is outside any layered-oxide range"


def test_coulombic_efficiency_stays_below_one_hundred_after_formation(
        client, real_sample):
    sample_id, _ = real_sample
    cycles = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    for cycle in cycles[2:]:
        assert cycle["coulombic_efficiency"] <= 101.0, \
            f"cycle {cycle['cycle']} reports CE {cycle['coulombic_efficiency']}"


def test_the_profile_spans_the_voltage_window(client, real_sample):
    sample_id, run = real_sample
    schedule = run["schedule"]
    body = client.get(f"/api/samples/{sample_id}/profile",
                      params={"cycles": "3", "basis": "mAh/g"}).json()
    if not body["series"]:
        pytest.skip("cycle 3 is not in this file")
    for series in body["series"]:
        assert series["capacity"][0] == pytest.approx(0.0, abs=1e-6)
        assert series["voltage"]
        if schedule:
            assert max(series["voltage"]) <= schedule["upper_cutoff_v"] + 0.05
            assert min(series["voltage"]) >= schedule["lower_cutoff_v"] - 0.05


def test_the_report_answers_the_bench_questions(client, real_sample):
    sample_id, _ = real_sample
    body = client.get(f"/api/samples/{sample_id}/report").json()
    assert body["state"] in ("running", "finished", "unknown")
    assert body["state_summary"]
    assert body["reported"]["complete"] is True
    assert body["retention_pct"] is not None
    assert body["knee"]["results"]
    if body["state"] == "running":
        assert body["reported"]["cycle"] == body["in_progress_cycle"] - 1


def test_export_round_trips_the_real_file(client, real_sample):
    sample_id, run_id = real_sample
    response = client.get(f"/api/export/samples/{sample_id}/cycles.csv",
                          params={"basis": "mAh/g"})
    assert response.status_code == 200
    lines = response.content.decode("utf-8-sig").strip().splitlines()
    complete = client.get(f"/api/samples/{sample_id}/cycles").json()["cycles"]
    assert len(lines) == len(complete) + 1
