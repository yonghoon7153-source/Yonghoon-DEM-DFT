"""Cycle tables, profiles, the cell report and comparisons."""

import pytest


@pytest.fixture
def loaded(client, sample_id, wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    return sample_id


def test_cycle_table_hides_the_cycle_in_progress_by_default(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles").json()
    assert [c["cycle"] for c in body["cycles"]] == [1, 2, 3, 4, 5, 6, 7]
    assert all(c["complete"] for c in body["cycles"])


def test_cycle_table_can_include_the_partial_cycle(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles",
                      params={"complete_only": False}).json()
    assert body["cycles"][-1]["cycle"] == 8
    assert body["cycles"][-1]["complete"] is False


def test_capacities_carry_the_basis_they_are_in(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles",
                      params={"basis": "mAh/g"}).json()
    assert body["basis"] == "mAh/g"
    assert body["basis_label"] == "Specific capacity (mAh g⁻¹)"
    first = body["cycles"][0]
    assert first["discharge_capacity"] == pytest.approx(5.0 / 0.02528, rel=1e-6)
    assert first["discharge_capacity_mah"] == pytest.approx(5.0)


def test_an_unavailable_basis_falls_back_and_says_why(client, wrd_bytes):
    bare = client.post("/api/samples", json={"name": "bare"}).json()["id"]
    client.post("/api/runs/upload", params={"sample_id": bare},
                files={"file": ("c.wrd", wrd_bytes, "application/octet-stream")})
    body = client.get(f"/api/samples/{bare}/cycles", params={"basis": "mAh/g"}).json()
    assert body["requested_basis"] == "mAh/g"
    assert body["basis"] == "mAh"
    assert body["basis_fallback_reason"] == "active mass not set"


def test_an_unknown_basis_is_rejected(client, loaded):
    assert client.get(f"/api/samples/{loaded}/cycles",
                      params={"basis": "mAh/kg"}).status_code == 422


def test_retention_is_measured_against_the_reference_cycle(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles").json()
    assert body["reference_cycle"] == 3
    rows = {c["cycle"]: c for c in body["cycles"]}
    assert rows[3]["retention_pct"] == pytest.approx(100.0)
    # 2 % fade per cycle: cycle 7 is 0.88 against cycle 3's 0.96.
    assert rows[7]["retention_pct"] == pytest.approx(100 * 0.88 / 0.96, rel=1e-6)


def test_a_what_if_mass_normalises_without_saving(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles",
                      params={"basis": "mAh/g", "active_mass_mg": 10.0}).json()
    assert body["cycles"][0]["discharge_capacity"] == pytest.approx(500.0)
    stored = client.get(f"/api/samples/{loaded}").json()
    assert stored["active_mass_mg"] is None       # nothing was persisted


def test_profile_returns_both_branches_of_a_cycle(client, loaded):
    body = client.get(f"/api/samples/{loaded}/profile",
                      params={"cycles": "2", "basis": "mAh/g"}).json()
    assert [s["branch"] for s in body["series"]] == ["charge", "discharge"]
    discharge = body["series"][1]
    assert discharge["capacity"][0] == pytest.approx(0.0)
    assert discharge["voltage"][0] == pytest.approx(3.6)
    assert discharge["voltage"][-1] == pytest.approx(1.9)
    assert discharge["basis"] == "mAh/g"


def test_profile_accepts_a_range_selection(client, loaded):
    body = client.get(f"/api/samples/{loaded}/profile",
                      params={"cycles": "1,3-5", "branches": "discharge"}).json()
    assert [s["cycle"] for s in body["series"]] == [1, 3, 4, 5]


def test_a_malformed_cycle_selection_is_rejected(client, loaded):
    response = client.get(f"/api/samples/{loaded}/profile",
                          params={"cycles": "3-1"})
    assert response.status_code == 422
    assert "cycle selection" in response.json()["detail"]


def test_profiles_are_downsampled_to_the_requested_budget(client, loaded):
    body = client.get(f"/api/samples/{loaded}/profile",
                      params={"cycles": "2", "max_points": 50}).json()
    assert all(s["points"] <= 50 for s in body["series"])


def test_report_calls_a_truncated_file_running(client, loaded):
    body = client.get(f"/api/samples/{loaded}/report").json()
    assert body["state"] == "running"
    assert body["in_progress_cycle"] == 8
    assert body["reported"]["cycle"] == 7        # the cycle before the live one
    assert any(e["signal"] == "partial cycle" for e in body["evidence"])


def test_report_quotes_retention_against_cycle_three(client, loaded):
    body = client.get(f"/api/samples/{loaded}/report").json()
    assert body["reference"]["cycle"] == 3
    assert body["reference_available"] is True
    assert body["retention_pct"] == pytest.approx(100 * 0.88 / 0.96, rel=1e-6)
    assert body["reference"]["coulombic_efficiency"] == pytest.approx(100.0)


def test_report_honours_a_declared_state(client, loaded):
    client.patch(f"/api/samples/{loaded}", json={"declared_state": "finished"})
    body = client.get(f"/api/samples/{loaded}/report").json()
    assert body["state"] == "finished"
    assert body["state_confidence"] == "high"


def test_a_finished_file_reports_its_last_cycle(client, sample_id, finished_wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("done.wrd", finished_wrd_bytes,
                                "application/octet-stream")})
    client.patch(f"/api/samples/{sample_id}", json={"declared_state": "finished"})
    body = client.get(f"/api/samples/{sample_id}/report").json()
    assert body["reported"]["cycle"] == 8
    assert body["in_progress_cycle"] is None


def test_report_capacities_follow_the_basis(client, loaded):
    body = client.get(f"/api/samples/{loaded}/report",
                      params={"basis": "mAh/cm2"}).json()
    assert body["basis"] == "mAh/cm2"
    assert body["reported"]["discharge_capacity"] == pytest.approx(
        body["reported"]["discharge_capacity_mah"] / 1.327, rel=1e-3)


def test_report_includes_every_knee_criterion(client, loaded):
    knee = client.get(f"/api/samples/{loaded}/report").json()["knee"]
    methods = {r["method"] for r in knee["results"]}
    assert methods == {"threshold", "segmented", "slope_ratio", "curvature"}
    assert knee["search_start_cycle"] == 3
    # A linear fade must not produce a knee, and must say so.
    assert all(r["reason"] for r in knee["results"] if not r["detected"])


def test_dashboard_gives_one_line_per_cell(client, loaded):
    rows = client.get("/api/dashboard").json()["rows"]
    assert len(rows) == 1
    row = rows[0]
    assert row["state"] == "running"
    assert row["reported_cycle"] == 7
    assert row["reference_cycle"] == 3
    assert row["initial_coulombic_efficiency"] == pytest.approx(100.0)
    assert row["loading_mg_cm2"] == pytest.approx(19.045, rel=1e-3)


def test_compare_overlays_a_metric_across_cells(client, loaded, wrd_bytes,
                                                finished_wrd_bytes):
    other = client.post("/api/samples", json={"name": "TEST-02",
                                              "total_mass_mg": 20.0,
                                              "active_wt_percent": 80}).json()["id"]
    client.post("/api/runs/upload", params={"sample_id": other},
                files={"file": ("b.wrd", finished_wrd_bytes,
                                "application/octet-stream")})
    body = client.get("/api/compare/cycles",
                      params={"sample_ids": f"{loaded},{other}",
                              "metric": "discharge_capacity",
                              "basis": "mAh/g"}).json()
    assert [s["sample_name"] for s in body["series"]] == ["TEST-01", "TEST-02"]
    assert body["series"][0]["points"][0]["cycle"] == 1
    # Different masses give different mAh/g for the same raw mAh.
    assert body["series"][0]["points"][0]["value"] != \
        body["series"][1]["points"][0]["value"]


def test_compare_rejects_an_unknown_metric(client, loaded):
    response = client.get("/api/compare/cycles",
                          params={"sample_ids": str(loaded), "metric": "vibes"})
    assert response.status_code == 422


def test_compare_profiles_overlays_the_same_cycle(client, loaded, finished_wrd_bytes):
    other = client.post("/api/samples", json={"name": "TEST-02"}).json()["id"]
    client.post("/api/runs/upload", params={"sample_id": other},
                files={"file": ("b.wrd", finished_wrd_bytes,
                                "application/octet-stream")})
    body = client.get("/api/compare/profiles",
                      params={"sample_ids": f"{loaded},{other}", "cycle": 3}).json()
    assert len(body["series"]) == 2
    assert all(s["branch"] == "discharge" for s in body["series"])
