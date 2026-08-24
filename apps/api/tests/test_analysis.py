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


@pytest.fixture
def long_sample(client) -> int:
    """A cell with more cycles than the old ceiling of 60 allowed to be drawn."""
    sample = client.post("/api/samples", json={"name": "LONG-01"}).json()["id"]
    samples = synthetic.make_cycles(n_cycles=80, points_per_branch=12)
    _upload(client, sample, synthetic.build_wrd(samples), name="long.wrd")
    return sample


def test_cycle_table_hides_the_cycle_in_progress_by_default(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles").json()
    assert [c["cycle"] for c in body["cycles"]] == [1, 2, 3, 4, 5, 6, 7]
    assert all(c["complete"] for c in body["cycles"])


def test_cycle_table_can_include_the_partial_cycle(client, loaded):
    body = client.get(f"/api/samples/{loaded}/cycles",
                      params={"complete_only": False}).json()
    assert body["cycles"][-1]["cycle"] == 8
    assert body["cycles"][-1]["complete"] is False


def test_the_partial_cycle_comes_back_with_its_numbers_blank(client, loaded):
    """`complete_only=false` 는 "그 행을 보여 달라" 이지 "부분값을 달라" 가 아니다.

    잘린 사이클의 용량은 파일이 끝난 순간까지 쌓인 값이라 셀을 과소평가한다.
    JSON 의 숫자 칸은 ``complete`` 가 뭐라고 하든 측정값으로 읽히므로, 측정처럼
    보이는 칸은 전부 비운다 (불변 규칙 4: 모르면 None).
    """
    body = client.get(f"/api/samples/{loaded}/cycles",
                      params={"complete_only": False}).json()
    partial = body["cycles"][-1]
    assert partial["complete"] is False
    for field in ("charge_capacity", "discharge_capacity",
                  "charge_capacity_mah", "discharge_capacity_mah",
                  "charge_energy_mwh", "discharge_energy_mwh",
                  "coulombic_efficiency", "energy_efficiency",
                  "mean_charge_voltage", "mean_discharge_voltage",
                  "voltage_hysteresis", "voltage_max", "voltage_min",
                  "retention_pct"):
        assert partial[field] is None, field

    # 남는 것: 파일에 무엇이 들어 있는지.  이것들은 셀의 성능을 주장하지 않는다.
    assert partial["cycle"] == 8
    assert partial["n_points"] > 0
    assert partial["duration_h"] > 0

    # 완료된 사이클은 그대로다 — 정책이 표 전체를 비우지 않는다.
    assert body["cycles"][0]["discharge_capacity_mah"] is not None


def test_a_partial_cycle_never_lands_on_a_compare_curve(client, loaded):
    """비교 그래프의 점 하나가 부분값이면, 곡선이 마지막에 꺾여 내려간다."""
    body = client.get("/api/compare/cycles",
                      params={"sample_ids": str(loaded), "complete_only": False}).json()
    cycles = [point["cycle"] for point in body["series"][0]["points"]]
    assert 8 not in cycles
    assert 7 in cycles


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


# --- 숫자가 없는 사이클 --------------------------------------------------------
#
# 실측: multi-step CCCV 파일(260630_MJ1, 41,738행)에 방전이 한 번도 없었다.
# 사이클 표가 비고, 지표가 전부 —, 프로파일이 "그릴 데이터가 없습니다" 였다.
# 전부 맞는 말인데 **왜** 가 어디에도 없어서 파싱 실패로 읽혔다.


@pytest.fixture
def charge_only(client, sample_id):
    """방전 스텝이 아예 없는 스케줄로 충전만 한 파일."""
    samples = [s for s in synthetic.make_cycles(1, 20) if s.current >= 0]
    schedule = (
        synthetic.SchedStep("rest", control=7),
        synthetic.SchedStep("cc", control=0, value=0.00123),
        synthetic.SchedStep("cv", control=1, value=4.25),
    )
    _upload(client, sample_id,
            synthetic.build_wrd(samples, schedule=schedule), name="chg_only.wrd")
    return sample_id


def test_the_table_says_which_cycles_it_left_out_and_why(client, charge_only):
    body = client.get(f"/api/samples/{charge_only}/cycles").json()
    assert body["cycles"] == []
    # 행은 빼되 **있다는 사실**은 뺀 적이 없다.  그 둘을 같이 숨긴 것이 화면을
    # 파싱 실패처럼 보이게 했다.
    [partial] = body["partial_cycles"]
    assert partial["cycle"] == 1
    assert partial["reason"] == "no_discharge"
    assert partial["has_charge"] is True
    assert partial["has_discharge"] is False


def test_partial_cycles_are_reported_even_when_the_rows_are_asked_for(client,
                                                                     charge_only):
    # complete_only=false 는 "그 행을 보여 달라" 이지 "빠진 것을 세지 말라" 가
    # 아니다.  두 화면이 같은 목록을 봐야 한다.
    body = client.get(f"/api/samples/{charge_only}/cycles",
                      params={"complete_only": "false"}).json()
    assert [c["cycle"] for c in body["cycles"]] == [1]
    assert body["cycles"][0]["discharge_capacity"] is None
    assert [c["cycle"] for c in body["partial_cycles"]] == [1]


def test_the_report_says_there_is_no_discharge_rather_than_cut_off(client,
                                                                  charge_only):
    body = client.get(f"/api/samples/{charge_only}/report").json()
    assert body["no_complete_reason"] == "no_discharge"
    # 영영 안 올라갈 사이클 번호를 "진행 중" 으로 걸어 두지 않는다.
    assert body["in_progress_cycle"] is None
    assert not any("cut off" in e["detail"] for e in body["evidence"])
    assert any(e["signal"] == "branch missing" for e in body["evidence"])


def test_a_charge_only_cycle_is_not_drawn_unless_asked_for(client, charge_only):
    # 기본이 False 인 이유: 완료 사이클들 사이에 잘린 곡선이 아무 표시 없이 끼면
    # 셀이 갑자기 용량을 잃은 것처럼 보인다.
    body = client.get(f"/api/samples/{charge_only}/profile",
                      params={"cycles": "all"}).json()
    assert body["series"] == []


def test_asking_for_it_draws_the_charge_curve_and_marks_it(client, charge_only):
    """곡선은 실측이다.  숫자를 내는 것과 그리는 것은 다르다.

    사이클 용량은 여전히 안 낸다(표가 비운다).  하지만 2.9 → 4.25 V 로 올라간
    충전 곡선은 실제로 측정된 것이고, 그리지 않을 이유가 없다 -- 완료 사이클인
    척만 안 하면 된다.
    """
    body = client.get(f"/api/samples/{charge_only}/profile",
                      params={"cycles": "all", "include_partial": "true"}).json()
    [series] = body["series"]
    assert series["cycle"] == 1
    assert series["branch"] == "charge"
    assert series["points"] > 0
    assert series["complete"] is False
    assert series["incomplete_reason"] == "no_discharge"


def test_a_complete_cycle_is_still_marked_complete(client, loaded):
    body = client.get(f"/api/samples/{loaded}/profile",
                      params={"cycles": "3", "branches": "discharge"}).json()
    [series] = body["series"]
    assert series["complete"] is True
    assert series["incomplete_reason"] == ""


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


def test_a_long_record_can_draw_every_cycle(client, long_sample):
    """"전체" 가 정말 전체여야 한다.

    상한이 60 이라, 196 사이클짜리 셀이 자기 기록을 다 못 보여 주고 41번에서
    조용히 끊겼다.
    """
    response = client.get(f"/api/samples/{long_sample}/profile",
                          params={"cycles": "all", "branches": "discharge"})
    assert response.status_code == 200, response.text
    drawn = {item["cycle"] for item in response.json()["series"]}
    assert len(drawn) >= 60


def test_many_curves_share_the_point_budget(client, long_sample):
    """곡선이 많으면 곡선마다 점을 줄인다 — 거절하지 않는다.

    한계는 곡선 수가 아니라 응답 크기다.  곡선당 1,200 점 × 400 곡선이면
    10 MB 짜리 JSON 이 된다.
    """
    few = client.get(f"/api/samples/{long_sample}/profile",
                     params={"cycles": "3", "branches": "discharge"}).json()
    many = client.get(f"/api/samples/{long_sample}/profile",
                      params={"cycles": "all", "branches": "charge,discharge"}).json()
    if len(many["series"]) > len(few["series"]) * 4:
        assert max(s["points"] for s in many["series"]) <= max(
            s["points"] for s in few["series"])


# --- 사이클 간 단차 -----------------------------------------------------------
#
# 유지율과 다른 질문이다.  여기 있는 검사는 전부 "그럴듯한 잘못된 숫자" 를
# 막는 것이라, 없으면 화면에 멀쩡히 찍힌 채 아무도 눈치채지 못한다.

def _cycles(client, sample_id, **params):
    response = client.get(f"/api/samples/{sample_id}/cycles", params=params)
    assert response.status_code == 200, response.text
    return response.json()["cycles"]


def test_the_delta_is_this_cycle_minus_the_previous_one(client, sample_id,
                                                        wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("d.wrd", wrd_bytes, "application/octet-stream")})
    rows = _cycles(client, sample_id, complete_only="true")
    assert len(rows) >= 3

    assert rows[0]["discharge_delta"] is None      # 기준이 없다
    assert rows[0]["delta_base_cycle"] is None
    # 의도적으로 길이가 하나 다르다 — 각 행을 그 앞 행과 짝짓는다.
    for previous, row in zip(rows, rows[1:], strict=False):
        assert row["delta_base_cycle"] == previous["cycle"]
        assert row["discharge_delta"] == pytest.approx(
            row["discharge_capacity"] - previous["discharge_capacity"], rel=1e-6)
        assert row["charge_delta"] == pytest.approx(
            row["charge_capacity"] - previous["charge_capacity"], rel=1e-6)


def test_the_delta_is_in_the_same_unit_as_the_column_beside_it(client, sample_id,
                                                              wrd_bytes):
    """mAh 로 빼고 mAh/g 로 보여 주면, 사람이 두 행을 손으로 뺀 값과 어긋난다."""
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("d.wrd", wrd_bytes, "application/octet-stream")})
    rows = _cycles(client, sample_id, basis="mAh/g", complete_only="true")
    second = rows[1]
    assert second["discharge_delta"] == pytest.approx(
        second["discharge_capacity"] - rows[0]["discharge_capacity"], rel=1e-6)


def test_a_running_cycle_neither_gets_a_delta_nor_becomes_a_base(client,
                                                                 sample_id,
                                                                 wrd_bytes):
    """잘린 사이클의 용량은 파일이 끝난 순간까지 쌓인 부분값이다.

    빼면 급사처럼 보이고, 그것이 다음 사이클의 기준이 되면 잘못이 전파된다.
    """
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("d.wrd", wrd_bytes, "application/octet-stream")})
    rows = _cycles(client, sample_id, complete_only="false")
    running = [r for r in rows if not r["complete"]]
    assert running, "이 픽스처는 마지막 사이클이 잘려 있어야 한다"
    for row in running:
        assert row["discharge_delta"] is None
        assert row["charge_delta"] is None
        assert row["delta_base_cycle"] is None


def test_the_span_says_how_far_back_the_base_is(client, sample_id, wrd_bytes):
    """이웃한 사이클끼리면 1 이다.  1 이 아니면 그 단차는 여러 사이클치다."""
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("d.wrd", wrd_bytes, "application/octet-stream")})
    rows = _cycles(client, sample_id, complete_only="true")
    for row in rows[1:]:
        assert row["delta_span"] == 1
        assert row["discharge_delta_per_cycle"] == pytest.approx(
            row["discharge_delta"], rel=1e-9)


def test_the_percentage_is_against_the_previous_cycle_not_the_reference(
        client, sample_id, wrd_bytes):
    """유지율의 분모는 기준 사이클, 단차의 분모는 직전 사이클이다."""
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("d.wrd", wrd_bytes, "application/octet-stream")})
    rows = _cycles(client, sample_id, complete_only="true")
    row, previous = rows[2], rows[1]
    assert row["discharge_delta_pct"] == pytest.approx(
        100.0 * row["discharge_delta"] / previous["discharge_capacity"], rel=1e-6)


def test_the_delta_columns_survive_a_what_if_mass(client, sample_id, wrd_bytes):
    """질량을 바꾸면 표의 모든 수치가 재파싱 없이 따라와야 한다 (§0.1).

    단차는 정규화된 값의 차라 같은 배율로 움직인다.
    """
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("d.wrd", wrd_bytes, "application/octet-stream")})
    base = _cycles(client, sample_id, basis="mAh/g", active_mass_mg=20.0,
                   complete_only="true")
    doubled = _cycles(client, sample_id, basis="mAh/g", active_mass_mg=40.0,
                      complete_only="true")
    assert base[1]["discharge_delta"] == pytest.approx(
        doubled[1]["discharge_delta"] * 2, rel=1e-6)
