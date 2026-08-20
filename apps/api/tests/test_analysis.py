"""Cycle tables, profiles, the cell report and comparisons."""

import pytest

import synthetic


@pytest.fixture
def loaded(client, sample_id, wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    return sample_id


def _upload(client, sample_id, payload, name="c.wrd"):
    response = client.post("/api/runs/upload", params={"sample_id": sample_id},
                           files={"file": (name, payload, "application/octet-stream")})
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def massless_sample(client, finished_wrd_bytes):
    """A cell nobody weighed -- every specific basis has to fall back for it."""
    bare = client.post("/api/samples", json={"name": "BARE-01"}).json()["id"]
    _upload(client, bare, finished_wrd_bytes, name="bare.wrd")
    return bare


@pytest.fixture
def two_cycle_wrd_bytes() -> bytes:
    """A live cell that has only finished cycles 1 and 2 -- no cycle 3 yet."""
    seconds = 66 * 10 * 3
    start = synthetic.ticks_ago(seconds)
    samples = synthetic.make_cycles(n_cycles=3, points_per_branch=30,
                                    start_ticks=start)
    return synthetic.build_wrd(samples[:-20], start_ticks=start)


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


def test_the_cycle_table_says_the_reference_cycle_was_there(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles").json()
    assert body["reference_cycle_used"] == 3
    assert body["reference_available"] is True
    assert body["retention_note"] == ""


def test_a_continuation_file_names_the_cycle_it_anchored_on(client, loaded):
    """ADR 0004: cycle 3 is absent from a _012 file, and that has to show."""
    run = client.get("/api/runs").json()[0]
    client.patch(f"/api/runs/{run['id']}", json={"cycle_offset": 200})

    body = client.get(f"/api/samples/{loaded}/cycles").json()
    assert body["reference_cycle"] == 3           # still what was asked for
    assert body["reference_cycle_used"] == 201
    assert body["reference_available"] is False
    assert "201" in body["retention_note"]
    rows = {c["cycle"]: c for c in body["cycles"]}
    assert rows[201]["retention_pct"] == pytest.approx(100.0)


def test_a_cell_short_of_cycle_three_does_not_pretend_otherwise(
        client, sample_id, two_cycle_wrd_bytes):
    """Anchoring on formation is the one thing ADR 0004 forbids outright."""
    _upload(client, sample_id, two_cycle_wrd_bytes, name="young.wrd")
    body = client.get(f"/api/samples/{sample_id}/cycles").json()
    assert [c["cycle"] for c in body["cycles"]] == [1, 2]
    assert body["reference_cycle"] == 3
    assert body["reference_cycle_used"] == 1
    assert body["reference_available"] is False
    assert "cycle 3" in body["retention_note"]


def test_the_c_rate_column_holds_still_while_the_cell_fades(
        client, massless_sample):
    """One current, one protocol -- the column must not climb with the fade."""
    body = client.get(f"/api/samples/{massless_sample}/cycles").json()
    rates = [c["c_rate"] for c in body["cycles"]]
    assert all(r is not None for r in rates)
    # 1 mA against cycle 3's 4.8 mAh, for every row.
    assert rates == pytest.approx([1.0e-3 * 1000.0 / 4.8] * len(rates), rel=1e-6)


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


def test_compare_labels_the_axis_with_the_basis_it_actually_used(client, loaded):
    body = client.get("/api/compare/cycles",
                      params={"sample_ids": str(loaded),
                              "metric": "discharge_capacity",
                              "basis": "mAh/g"}).json()
    assert body["basis"] == "mAh/g"
    assert body["requested_basis"] == "mAh/g"
    assert body["y_label"] == "Specific capacity (mAh g⁻¹)"
    assert body["mixed_basis"] is False


def test_compare_flags_a_cell_that_could_not_be_normalised(client, loaded,
                                                           massless_sample):
    body = client.get("/api/compare/cycles",
                      params={"sample_ids": f"{loaded},{massless_sample}",
                              "metric": "discharge_capacity",
                              "basis": "mAh/g"}).json()
    weighed, bare = body["series"]
    assert weighed["basis"] == "mAh/g"
    assert weighed["basis_fallback_reason"] is None
    assert bare["basis"] == "mAh"
    assert bare["basis_fallback_reason"] == "active mass not set"
    assert body["mixed_basis"] is True


def test_compare_carries_the_reference_cycle_per_series(client, loaded):
    run = client.get("/api/runs").json()[0]
    client.patch(f"/api/runs/{run['id']}", json={"cycle_offset": 200})
    body = client.get("/api/compare/cycles",
                      params={"sample_ids": str(loaded),
                              "metric": "retention"}).json()
    series = body["series"][0]
    assert series["reference_cycle_used"] == 201
    assert series["reference_available"] is False
    assert "201" in series["retention_note"]


def test_dashboard_flags_a_cell_that_could_not_be_normalised(client, loaded,
                                                             massless_sample):
    body = client.get("/api/dashboard", params={"basis": "mAh/g"}).json()
    rows = {row["sample_name"]: row for row in body["rows"]}
    assert rows["TEST-01"]["basis"] == "mAh/g"
    assert rows["TEST-01"]["basis_fallback_reason"] is None
    assert rows["BARE-01"]["basis"] == "mAh"
    assert rows["BARE-01"]["basis_fallback_reason"] == "active mass not set"
    assert body["mixed_basis"] is True
    assert body["requested_basis"] == "mAh/g"


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


def test_compare_profiles_rejects_an_unknown_branch(client, loaded):
    """A typo is a 422 here just as it is on the single-cell profile."""
    response = client.get("/api/compare/profiles",
                          params={"sample_ids": str(loaded), "cycle": 3,
                                  "branches": "chg"})
    assert response.status_code == 422
    assert "branch must be charge or discharge" in response.json()["detail"]


def test_profile_rejects_an_unknown_branch(client, loaded):
    response = client.get(f"/api/samples/{loaded}/profile",
                          params={"cycles": "3", "branches": "dis"})
    assert response.status_code == 422


# --- 갱신이 심은 회귀: 비교 축 단위 -----------------------------------------

def test_compare_profiles_labels_the_axis_from_the_curves_it_drew(client, loaded):
    """건너뛴 샘플이 축 단위를 정하면 안 된다.

    질량이 있는 A 뒤에 아무것도 없는 B 를 요청하면, 옛 코드는 B 가 건너뛰어지는
    길에 fallback_cell 을 덮어써서 A 의 mAh/g 곡선에 'mAh' 라벨을 붙였다.
    """
    empty = client.post("/api/samples", json={"name": "빈 셀"}).json()["id"]
    body = client.get("/api/compare/profiles",
                      params={"sample_ids": f"{loaded},{empty}", "cycle": 3,
                              "basis": "mAh/g", "branches": "discharge"}).json()
    assert body["series"], "질량이 있는 셀의 곡선이 나와야 한다"
    assert {s["basis"] for s in body["series"]} == {body["basis"]}, \
        "최상위 단위가 실제 곡선의 단위와 다르다"
    assert body["basis"] == "mAh/g"
    assert body["mixed_basis"] is False


def test_a_uniform_fallback_is_not_reported_as_mixed_units(client, sample_id, wrd_bytes):
    """전부 같은 단위로 떨어지면 혼재가 아니다 — 비교는 유효하다."""
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("a.wrd", wrd_bytes, "application/octet-stream")})
    body = client.get("/api/compare/profiles",
                      params={"sample_ids": str(sample_id), "cycle": 3,
                              "basis": "mAh/g", "branches": "discharge"}).json()
    assert body["series"]
    assert body["mixed_basis"] is False
    assert len({s["basis"] for s in body["series"]}) == 1


def test_both_compare_endpoints_share_one_selection_cap(client):
    """한쪽은 422, 다른 쪽은 조용히 잘림 — 같은 상한이어야 한다."""
    ids = ",".join(str(n) for n in range(1, 33))
    cycles = client.get("/api/compare/cycles",
                        params={"sample_ids": ids, "metric": "discharge_capacity"})
    profiles = client.get("/api/compare/profiles",
                          params={"sample_ids": ids, "cycle": 3})
    assert cycles.status_code == 422
    assert profiles.status_code == 422, "profiles 가 조용히 30개로 잘랐다"
