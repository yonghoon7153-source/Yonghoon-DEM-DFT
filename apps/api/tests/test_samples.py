"""Samples, groups, and the cell spec that drives normalisation."""

import pytest


def test_a_sample_resolves_its_cell_spec(client, sample_id):
    sample = client.get(f"/api/samples/{sample_id}").json()
    cell = sample["resolved_cell"]
    assert cell["active_mass_g"] == 0.02528          # 31.6 mg x 80 wt%
    assert round(cell["area_cm2"], 4) == 1.3273      # 13 mm punch
    assert round(cell["loading_mg_cm2"], 2) == 19.05
    assert round(cell["nominal_capacity_mah"], 4) == 5.2052
    assert set(cell["available_bases"]) == {"mAh", "mAh/g", "mAh/cm2", "%"}


def test_an_unavailable_basis_says_what_is_missing(client):
    created = client.post("/api/samples", json={"name": "bare"}).json()
    cell = client.get(f"/api/samples/{created['id']}").json()["resolved_cell"]
    assert cell["available_bases"] == ["mAh"]
    assert cell["unavailable"]["mAh/g"] == "active mass not set"
    assert cell["unavailable"]["mAh/cm2"] == "electrode area not set"


def test_the_spec_explains_how_each_number_was_derived(client, sample_id):
    notes = client.get(f"/api/samples/{sample_id}").json()["resolved_cell"]["notes"]
    assert "80 wt%" in notes["active_mass"]
    assert "13 mm" in notes["area"]


def test_correcting_the_mass_renormalises_without_reparsing(client, sample_id, wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    before = client.get(f"/api/samples/{sample_id}/cycles",
                        params={"basis": "mAh/g"}).json()["cycles"][0]

    client.patch(f"/api/samples/{sample_id}", json={"total_mass_mg": 15.8})
    after = client.get(f"/api/samples/{sample_id}/cycles",
                       params={"basis": "mAh/g"}).json()["cycles"][0]

    # Halving the mass doubles mAh/g; the raw mAh is untouched.
    assert after["discharge_capacity"] == before["discharge_capacity"] * 2
    assert after["discharge_capacity_mah"] == before["discharge_capacity_mah"]


def test_a_patch_only_touches_the_fields_it_names(client, sample_id):
    client.patch(f"/api/samples/{sample_id}", json={"notes": "재측정"})
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["notes"] == "재측정"
    assert sample["total_mass_mg"] == 31.6
    assert sample["cathode_detail"] == "NCM811"


def test_clear_removes_a_numeric_field(client, sample_id):
    client.patch(f"/api/samples/{sample_id}", json={"clear": ["diameter_mm"]})
    sample = client.get(f"/api/samples/{sample_id}").json()
    assert sample["diameter_mm"] is None
    assert "mAh/cm2" not in sample["resolved_cell"]["available_bases"]


def test_an_invalid_declared_state_is_rejected(client, sample_id):
    response = client.patch(f"/api/samples/{sample_id}",
                            json={"declared_state": "maybe"})
    assert response.status_code == 422


def test_a_reference_cycle_below_one_is_rejected(client, sample_id):
    assert client.patch(f"/api/samples/{sample_id}",
                        json={"reference_cycle": 0}).status_code == 422


def test_samples_can_be_filtered_the_way_the_bench_asks(client):
    client.post("/api/samples", json={"name": "A", "cathode_type": "High-Ni",
                                      "process": "dry", "test_date": "2026-02-01",
                                      "c_rate": 0.2})
    client.post("/api/samples", json={"name": "B", "cathode_type": "Mid-Ni",
                                      "process": "wet", "test_date": "2026-03-01",
                                      "c_rate": 0.5})
    high = client.get("/api/samples", params={"cathode_type": "High-Ni"}).json()
    assert [s["name"] for s in high] == ["A"]
    march = client.get("/api/samples", params={"date_from": "2026-02-15"}).json()
    assert [s["name"] for s in march] == ["B"]
    fast = client.get("/api/samples", params={"c_rate": 0.5}).json()
    assert [s["name"] for s in fast] == ["B"]


def test_facets_list_the_values_actually_present(client, sample_id):
    facets = client.get("/api/samples/facets").json()
    assert facets["cathode_type"] == ["High-Ni"]
    assert facets["process"] == ["dry"]
    assert "mAh/g" in facets["bases"]


def test_a_group_counts_its_samples_and_runs(client, sample_id, wrd_bytes):
    group = client.post("/api/groups", json={"name": "건식 80wt%",
                                             "color": "#3b6"}).json()
    client.patch(f"/api/samples/{sample_id}", json={"group_id": group["id"]})
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    refreshed = client.get(f"/api/groups/{group['id']}").json()
    assert refreshed["sample_count"] == 1
    assert refreshed["run_count"] == 1


def test_deleting_a_group_leaves_its_samples_ungrouped(client, sample_id):
    group = client.post("/api/groups", json={"name": "temp"}).json()
    client.patch(f"/api/samples/{sample_id}", json={"group_id": group["id"]})
    assert client.delete(f"/api/groups/{group['id']}").status_code == 204
    assert client.get(f"/api/samples/{sample_id}").json()["group_id"] is None


def test_deleting_a_sample_keeps_its_files_by_default(client, sample_id, wrd_bytes):
    client.post("/api/runs/upload", params={"sample_id": sample_id},
                files={"file": ("c_012.wrd", wrd_bytes, "application/octet-stream")})
    assert client.delete(f"/api/samples/{sample_id}").status_code == 204
    runs = client.get("/api/runs").json()
    assert len(runs) == 1
    assert runs[0]["sample_id"] is None


def test_deleting_a_sample_with_its_files_drops_their_parse_cache(client, sample_id,
                                                                  wrd_bytes):
    from app import storage

    run = client.post("/api/runs/upload", params={"sample_id": sample_id},
                      files={"file": ("c_012.wrd", wrd_bytes,
                                      "application/octet-stream")}).json()
    assert storage.columns_path(run["id"]).exists()

    assert client.delete(f"/api/samples/{sample_id}",
                         params={"delete_runs": True}).status_code == 204
    # Nothing can reach that run id again, so the npz would leak for good.
    assert not storage.columns_path(run["id"]).exists()
    assert storage.upload_path(run["sha256"]).exists()


def test_an_empty_sample_name_is_rejected(client):
    assert client.post("/api/samples", json={"name": "   "}).status_code == 422


def test_a_rename_cannot_blank_the_name(client, sample_id):
    """The screen lets the title be edited in place; a blank must not land.

    A nameless row is a link with nothing to click, and nothing else on the
    library screen identifies the cell -- the id is never shown.  POST has
    refused this since the beginning; PATCH used to let it through.
    """
    before = client.get(f"/api/samples/{sample_id}").json()["name"]
    assert client.patch(f"/api/samples/{sample_id}", json={"name": "   "}).status_code == 422
    assert client.get(f"/api/samples/{sample_id}").json()["name"] == before


def test_a_rename_stores_the_trimmed_name(client, sample_id):
    renamed = client.patch(f"/api/samples/{sample_id}",
                           json={"name": "  No_7_dry  "}).json()
    assert renamed["name"] == "No_7_dry"


def test_a_new_sample_stores_the_trimmed_name(client):
    """POST and PATCH have to agree on what gets stored, not just on what is
    refused -- otherwise the same typed name sorts differently depending on
    which door it came through."""
    created = client.post("/api/samples", json={"name": "  No_8_dry  "}).json()
    assert created["name"] == "No_8_dry"


# --- 물리량 입력의 문지기 ----------------------------------------------------
#
# 여기가 데이터 계약의 입구다. 음수 질량과 NaN 은 wrdkit 이 뒤에서 걸러 주더라도
# DB 에 남아, 조회할 때마다 같은 잘못된 수를 다시 만들어 낸다.

@pytest.mark.parametrize("payload", [
    {"total_mass_mg": -5},
    {"total_mass_mg": 0},
    {"active_mass_mg": -1},
    {"area_cm2": -2},
    {"diameter_mm": -13},
    {"thickness_um": 0},
    {"active_wt_percent": 800},
    {"active_wt_percent": -80},
    {"reference_cycle": 0},
    {"c_rate": -0.2},
    {"composition": [{"name": "AM", "wt_percent": 150}]},
])
def test_impossible_physical_values_are_refused(client, payload):
    response = client.post("/api/samples", json={"name": "X", **payload})
    assert response.status_code == 422, payload


@pytest.mark.parametrize("field", ["total_mass_mg", "area_cm2", "active_wt_percent"])
@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_nan_and_infinity_are_refused_with_a_serialisable_422(client, field, value):
    """NaN 은 모든 산술을 물들이고 화면엔 빈칸으로 보인다.

    그리고 422 본문에는 문제의 입력이 그대로 되돌아오는데, NaN 은 JSON 으로
    직렬화되지 않아 422 가 500 으로 바뀐다 — 검증을 넣은 바로 그 경우가
    서버 오류로 보고된다.
    """
    import json

    response = client.post(
        "/api/samples",
        content=json.dumps({"name": "X", field: value}, allow_nan=True),
        headers={"content-type": "application/json"})
    assert response.status_code == 422
    response.json()          # 본문이 실제로 직렬화되는지


@pytest.mark.parametrize("payload", [
    {"current_collector_mass_mg": 0},
    {"composition": [{"name": "PTFE", "wt_percent": 0}]},
    {"reference_cycle": 1},
    {"total_mass_mg": 31.6, "active_wt_percent": 100},
    {"total_mass_mg": 31.6, "active_wt_percent": 0},
])
def test_legitimate_edge_values_still_pass(client, payload):
    """0 은 결함이 아니다 — 자립막은 집전체가 없고, PTFE 0 wt% 는 기록이다."""
    response = client.post("/api/samples", json={"name": "OK", **payload})
    assert response.status_code == 201, payload


# --- PATCH 는 보낸 것만 건드린다 ---------------------------------------------

def test_patching_a_group_leaves_unmentioned_fields_alone(client):
    """색만 바꿨는데 설명이 지워지면 안 된다.

    GroupIn 의 기본값은 진짜 값이라, model_dump() 가 "설명을 언급하지 않았다" 를
    "설명을 빈 문자열로 하라" 로 바꿔 놓았다. 그룹 라우터에는 PATCH 테스트가
    아예 없어서 아무도 몰랐다.
    """
    created = client.post("/api/groups", json={
        "name": "고Ni 60도", "description": "NCM811 · 60 °C · 0.2C",
        "color": "#c33"}).json()

    patched = client.patch(f"/api/groups/{created['id']}", json={"color": "#39c"})
    assert patched.status_code == 200
    body = patched.json()
    assert body["color"] == "#39c"
    assert body["description"] == "NCM811 · 60 °C · 0.2C", "설명이 지워졌다"
    assert body["name"] == "고Ni 60도", "이름이 지워졌다"


def test_patching_a_group_can_still_clear_a_field_on_purpose(client):
    """빈 문자열을 명시적으로 보내면 지워진다 — 언급 없음과 다르다."""
    created = client.post("/api/groups", json={
        "name": "G", "description": "지울 설명"}).json()
    body = client.patch(f"/api/groups/{created['id']}",
                        json={"description": ""}).json()
    assert body["description"] == ""


def test_the_reference_electrode_comes_back_out(client):
    """저장은 되는데 응답에 없으면 화면이 조용히 틀린다.

    `reference_electrode` 와 `reference_offset_v` 가 `SampleOut` 에 없었다.
    Li-In 으로 저장한 셀을 다시 열면 기준전극 칸이 "환산 안 함" 으로 보이고,
    화면은 그 칸으로 dirty 를 계산하므로 저장할 것이 없다고 말한다.
    0.62 V 는 4.40 V 컷오프가 3.78 V 로 보이는 차이다.
    """
    sample = client.post("/api/samples", json={
        "name": "REF-01", "reference_electrode": "Li-In"}).json()
    assert sample["reference_electrode"] == "Li-In"

    fetched = client.get(f"/api/samples/{sample['id']}").json()
    assert fetched["reference_electrode"] == "Li-In"
    assert fetched["reference_offset_v"] is None

    patched = client.patch(f"/api/samples/{sample['id']}",
                           json={"reference_offset_v": 0.62}).json()
    assert patched["reference_offset_v"] == 0.62
    assert patched["reference_electrode"] == "Li-In"


def test_the_formation_rate_comes_from_the_schedule(client, scheduled_wrd_bytes):
    """계측기가 아는 것을 사람에게 다시 묻지 않는다 (CLAUDE.md §0.3).

    형성은 루프 밖에서 한 번, 본 사이클 전류의 몇 분의 일로 돈다.  그 전류 비가
    본 사이클 C-rate 를 형성 C-rate 로 환산해 준다 — 스케줄에 이미 다 있는
    값들이다.
    """
    sample = client.post("/api/samples", json={"name": "SCHED-01"}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("s_011.wrd", scheduled_wrd_bytes,
                                "application/octet-stream")})

    filled = client.get(f"/api/samples/{sample['id']}").json()
    if filled["c_rate"] is None:
        pytest.skip("이 픽스처의 스케줄로는 본 사이클 C-rate 를 추론하지 못한다")
    assert filled["c_rate_formation"] is not None
    assert filled["c_rate_formation"] < filled["c_rate"], "형성이 본 사이클보다 빠르다"


def test_a_typed_condition_is_never_overwritten_by_a_schedule(client,
                                                              scheduled_wrd_bytes):
    """입력은 덮어쓰기다.  파일을 하나 더 붙였다고 사람이 적은 값이 바뀌면 안 된다."""
    sample = client.post("/api/samples", json={"name": "SCHED-02",
                                               "c_rate": 0.05,
                                               "c_rate_formation": 0.01}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("s_011.wrd", scheduled_wrd_bytes,
                                "application/octet-stream")})

    after = client.get(f"/api/samples/{sample['id']}").json()
    assert (after["c_rate"], after["c_rate_formation"]) == (0.05, 0.01)


# --- 기준 사이클은 스케줄이 정한다 (ADR 0018) --------------------------------
#
# 3 과 1 사이에서 조용히 움직이면 화면의 유지율이 전부 달라진다.  어느 쪽으로도
# 틀릴 수 있으므로 네 갈래를 모두 고정한다.

def test_formation_keeps_the_reference_at_cycle_three(client, scheduled_wrd_bytes):
    sample = client.post("/api/samples", json={"name": "FORM-01"}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("f_011.wrd", scheduled_wrd_bytes,
                                "application/octet-stream")})

    out = client.get(f"/api/samples/{sample['id']}").json()
    assert out["formation"] == "yes"
    assert out["reference_cycle_effective"] == 3
    assert out["reference_cycle_reason"] == "default"


def test_no_formation_moves_the_reference_to_cycle_one(client, formationless_wrd_bytes):
    """임피던스 재고 바로 메인 루프.  1~3 사이의 손실은 formation 이 아니라 열화다."""
    sample = client.post("/api/samples", json={"name": "NOFORM-01"}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("n_011.wrd", formationless_wrd_bytes,
                                "application/octet-stream")})

    out = client.get(f"/api/samples/{sample['id']}").json()
    assert out["formation"] == "no"
    assert out["reference_cycle_effective"] == 1
    assert out["reference_cycle_reason"] == "formationless"
    # 저장된 값은 그대로다 -- 입력란은 사람이 넣은 것을 보여 줘야 한다.
    assert out["reference_cycle"] == 3


def test_the_cycle_table_anchors_where_the_sample_says(client, formationless_wrd_bytes):
    """푼 값이 표까지 간다.  SampleOut 만 맞고 표가 3번에 앵커하면 아무 소용이 없다."""
    sample = client.post("/api/samples", json={"name": "NOFORM-02"}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("n_011.wrd", formationless_wrd_bytes,
                                "application/octet-stream")})

    table = client.get(f"/api/samples/{sample['id']}/cycles").json()
    assert table["reference_cycle"] == 1
    assert table["reference_cycle_reason"] == "formationless"
    assert table["reference_cycle_used"] == 1
    first = next(row for row in table["cycles"] if row["cycle"] == 1)
    assert first["retention_pct"] == pytest.approx(100.0)


def test_a_typed_reference_cycle_survives_a_formationless_schedule(
        client, formationless_wrd_bytes):
    """사용자 입력은 덮어쓰기다 (§0.3).  스케줄이 사람을 이기지 못한다."""
    sample = client.post("/api/samples", json={"name": "NOFORM-03"}).json()
    client.patch(f"/api/samples/{sample['id']}", json={"reference_cycle": 3})
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("n_011.wrd", formationless_wrd_bytes,
                                "application/octet-stream")})

    out = client.get(f"/api/samples/{sample['id']}").json()
    assert out["formation"] == "no"
    assert out["reference_cycle_effective"] == 3
    assert out["reference_cycle_reason"] == "user"


def test_a_reference_cycle_given_at_creation_counts_as_typed(
        client, formationless_wrd_bytes):
    """POST 본문의 reference_cycle 도 사람이 친 값이다.

    스키마 기본값 3 이 model_dump 에 실려 오므로, 보낸 값을 출처 없이 저장하면
    formation 없는 스케줄이 그것을 1 로 덮어쓴다 -- PATCH 로 친 값만 살아남고
    POST 로 준 값은 죽는 비대칭이 있었다.
    """
    sample = client.post("/api/samples",
                         json={"name": "NOFORM-04", "reference_cycle": 3}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("n_011.wrd", formationless_wrd_bytes,
                                "application/octet-stream")})

    out = client.get(f"/api/samples/{sample['id']}").json()
    assert out["reference_cycle_effective"] == 3
    assert out["reference_cycle_reason"] == "user"


def test_clearing_the_reference_cycle_unpins_it(client, formationless_wrd_bytes):
    """clear 는 고정 해제다: 기본값 3 으로 돌아가고 자동 해석이 다시 일한다.

    None 을 그대로 넣으면 NOT NULL 컬럼과 ``SampleOut.reference_cycle: int``
    검증이 깨져 이후 모든 조회가 500 이 된다.
    """
    sample = client.post("/api/samples", json={"name": "NOFORM-05"}).json()
    client.patch(f"/api/samples/{sample['id']}", json={"reference_cycle": 5})
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("n_011.wrd", formationless_wrd_bytes,
                                "application/octet-stream")})
    pinned = client.get(f"/api/samples/{sample['id']}").json()
    assert pinned["reference_cycle_effective"] == 5

    response = client.patch(f"/api/samples/{sample['id']}",
                            json={"clear": ["reference_cycle"]})
    assert response.status_code == 200
    out = client.get(f"/api/samples/{sample['id']}").json()
    assert out["reference_cycle"] == 3
    assert out["reference_cycle_effective"] == 1        # formationless again
    assert out["reference_cycle_reason"] == "formationless"


def test_the_report_names_who_decided_the_anchor(client, formationless_wrd_bytes):
    """리포트 카드도 이유를 말한다.  빼먹으면 스키마 기본값 "default" 가 나가서
    formation 없이 1 에 앵커된 카드가 기본값이라고 주장한다."""
    sample = client.post("/api/samples", json={"name": "NOFORM-06"}).json()
    client.post("/api/runs/upload", params={"sample_id": sample["id"]},
                files={"file": ("n_011.wrd", formationless_wrd_bytes,
                                "application/octet-stream")})

    report = client.get(f"/api/samples/{sample['id']}/report").json()
    assert report["reference_cycle_requested"] == 1
    assert report["reference_cycle_reason"] == "formationless"

    client.patch(f"/api/samples/{sample['id']}", json={"reference_cycle": 5})
    report = client.get(f"/api/samples/{sample['id']}/report").json()
    assert report["reference_cycle_reason"] == "user"


def test_a_sample_with_no_file_cannot_say(client):
    """파일이 없으면 스케줄도 없다.  모르면 기본값을 그대로 둔다 (§0.4)."""
    out = client.post("/api/samples", json={"name": "BARE-01"}).json()
    assert out["formation"] == "unclear"
    assert out["reference_cycle_effective"] == 3
    assert out["reference_cycle_reason"] == "default"
